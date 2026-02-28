---
name: backend-patterns
description: 后端架构模式、API 设计、数据库优化和服务端最佳实践。
---

# 后端开发模式

后端架构模式和可扩展服务端应用程序的最佳实践。

## API 设计模式

### RESTful API 结构

```
# 基于资源的 URL
GET    /api/markets                 # 列出资源
GET    /api/markets/:id             # 获取单个资源
POST   /api/markets                 # 创建资源
PUT    /api/markets/:id             # 替换资源
PATCH  /api/markets/:id             # 更新资源
DELETE /api/markets/:id             # 删除资源

# 查询参数用于过滤、排序、分页
GET /api/markets?status=active&sort=volume&limit=20&offset=0
```

### 仓库模式

抽象数据访问逻辑：

```python
from abc import ABC, abstractmethod

class MarketRepository(ABC):
    @abstractmethod
    def find_all(self, filters=None) -> list[Market]:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Market | None:
        pass

    @abstractmethod
    def create(self, data: dict) -> Market:
        pass

class DatabaseMarketRepository(MarketRepository):
    def __init__(self, db):
        self.db = db

    def find_all(self, filters=None) -> list[Market]:
        query = self.db.query(Market)
        if filters and filters.get('status'):
            query = query.filter(Market.status == filters['status'])
        return query.all()
```

### 服务层模式

业务逻辑与数据访问分离：

```python
class MarketService:
    def __init__(self, market_repo: MarketRepository):
        self.market_repo = market_repo

    def search_markets(self, query: str, limit: int = 10) -> list[Market]:
        # 业务逻辑
        embedding = generate_embedding(query)
        results = self._vector_search(embedding, limit)

        # 获取完整数据
        markets = self.market_repo.find_by_ids([r.id for r in results])

        # 按相似度排序
        return sorted(markets, key=lambda m: results.get(m.id, 0), reverse=True)
```

## 数据库模式

### 查询优化

```python
# ✓ 好：只选择需要的列
markets = session.query(Market.id, Market.name, Market.status).filter(
    Market.status == 'active'
).order_by(Market.volume.desc()).limit(10).all()

# ❌ 坏：选择所有
markets = session.query(Market).all()
```

### N+1 查询预防

```python
# ❌ 坏：N+1 查询问题
markets = get_markets()
for market in markets:
    market.creator = get_user(market.creator_id)  # N 次查询

# ✓ 好：批量获取
markets = get_markets()
creator_ids = [m.creator_id for m in markets]
creators = get_users(creator_ids)  # 1 次查询
creator_map = {c.id: c for c in creators}

for market in markets:
    market.creator = creator_map.get(market.creator_id)
```

### 事务模式

```python
from contextlib import contextmanager

@contextmanager
def transaction(session):
    """事务上下文管理器。"""
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# 使用
with transaction(session) as s:
    market = Market(name="New Market")
    s.add(market)
    position = Position(market_id=market.id)
    s.add(position)
```

## 缓存策略

### Redis 缓存层

```python
import redis
import json

class CachedRepository:
    def __init__(self, base_repo, redis_client):
        self.base_repo = base_repo
        self.redis = redis_client

    def find_by_id(self, id: str) -> dict | None:
        # 先检查缓存
        cache_key = f"market:{id}"
        cached = self.redis.get(cache_key)

        if cached:
            return json.loads(cached)

        # 缓存未命中 - 从数据库获取
        market = self.base_repo.find_by_id(id)

        if market:
            # 缓存5分钟
            self.redis.setex(cache_key, 300, json.dumps(market))

        return market

    def invalidate_cache(self, id: str):
        """使缓存失效。"""
        self.redis.delete(f"market:{id}")
```

### 缓存旁路模式

```python
async def get_market_with_cache(id: str) -> Market:
    cache_key = f"market:{id}"

    # 尝试缓存
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # 缓存未命中 - 从数据库获取
    market = await db.markets.find_unique(where={"id": id})

    if not market:
        raise NotFoundError("Market not found")

    # 更新缓存
    await redis.setex(cache_key, 300, json.dumps(market))

    return market
```

## 错误处理模式

### 集中式错误处理器

```python
from fastapi import HTTPException

class ApiError(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)

# 使用
def get_user(user_id: str):
    user = db.find_user(user_id)
    if not user:
        raise ApiError(404, f"User not found: {user_id}")
    return user
```

### 带指数退避的重试

```python
import time
from functools import wraps

def retry(max_retries=3, backoff_factor=1):
    """带指数退避的重试装饰器。"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if i < max_retries - 1:
                        # 指数退避：1s, 2s, 4s
                        delay = (2 ** i) * backoff_factor
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

# 使用
@retry(max_retries=3)
def fetch_from_api():
    return requests.get("https://api.example.com/data")
```

## 认证与授权

### JWT 令牌验证

```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id: str, secret: str) -> str:
    """创建 JWT 令牌。"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def verify_token(token: str, secret: str) -> dict:
    """验证 JWT 令牌。"""
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ApiError(401, "Token expired")
    except jwt.InvalidTokenError:
        raise ApiError(401, "Invalid token")
```

### 基于角色的访问控制

```python
from enum import Enum
from functools import wraps

class Role(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

ROLE_PERMISSIONS = {
    Role.ADMIN: ["read", "write", "delete", "admin"],
    Role.MODERATOR: ["read", "write", "delete"],
    Role.USER: ["read", "write"]
}

def has_permission(user_role: Role, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(user_role, [])

def require_permission(permission: str):
    """权限检查装饰器。"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, user=None, **kwargs):
            if not user or not has_permission(user.role, permission):
                raise ApiError(403, "Insufficient permissions")
            return func(*args, user=user, **kwargs)
        return wrapper
    return decorator
```

## 速率限制

```python
import time
from collections import defaultdict

class RateLimiter:
    """简单的内存速率限制器。"""

    def __init__(self):
        self.requests = defaultdict(list)

    def check_limit(self, identifier: str, max_requests: int, window_ms: int) -> bool:
        now = time.time() * 1000
        requests = self.requests[identifier]

        # 移除窗口外的旧请求
        requests[:] = [t for t in requests if now - t < window_ms]

        if len(requests) >= max_requests:
            return False  # 超过速率限制

        requests.append(now)
        return True

# 使用
limiter = RateLimiter()

def handle_request(request):
    ip = request.client.host
    if not limiter.check_limit(ip, 100, 60000):  # 100 请求/分钟
        raise ApiError(429, "Rate limit exceeded")
```

## 结构化日志

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """结构化 JSON 日志记录器。"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def log(self, level: str, message: str, **context):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **context
        }
        self.logger.log(
            getattr(logging, level.upper()),
            json.dumps(entry)
        )

    def info(self, message: str, **context):
        self.log("info", message, **context)

    def error(self, message: str, error: Exception = None, **context):
        if error:
            context["error"] = str(error)
            context["error_type"] = type(error).__name__
        self.log("error", message, **context)

# 使用
logger = StructuredLogger(__name__)

def process_request(request_id: str):
    logger.info("Processing request", request_id=request_id, path="/api/markets")
    try:
        result = do_work()
        logger.info("Request completed", request_id=request_id)
        return result
    except Exception as e:
        logger.error("Request failed", error=e, request_id=request_id)
        raise
```

## 最佳实践总结

### 应该做

- 使用仓库模式抽象数据访问
- 使用服务层封装业务逻辑
- 实现适当的错误处理
- 使用缓存减轻数据库负载
- 实施速率限制保护 API
- 记录结构化日志便于调试

### 不应该做

- 不在业务逻辑中直接写 SQL
- 不忽略错误或异常
- 不在循环中执行数据库查询
- 不将密钥硬编码在代码中
- 不在无速率限制的情况下暴露 API

**记住**：后端模式支持可扩展、可维护的服务端应用程序。选择适合您复杂度的模式。
