---
name: python-patterns
description: Pythonic 惯用法、PEP 8 标准、类型提示和最佳实践。
---

# Python 开发模式

Pythonic 模式和最佳实践，构建健壮、高效、可维护的应用程序。

## 核心原则

### 1. 可读性很重要

Python 优先考虑可读性。代码应该显而易见且易于理解。

```python
# 好：清晰可读
def get_active_users(users: list[User]) -> list[User]:
    """从提供的列表中返回活跃用户。"""
    return [user for user in users if user.is_active]

# 坏：聪明但令人困惑
def get_active_users(u):
    return [x for x in u if x.a]
```

### 2. 显式优于隐式

避免魔法；清楚说明代码做什么。

### 3. EAFP - 请求原谅比许可更容易

Python 偏好异常处理而非检查条件。

```python
# 好：EAFP 风格
def get_value(dictionary: dict, key: str) -> Any:
    try:
        return dictionary[key]
    except KeyError:
        return default_value
```

## 类型提示

### 基本类型注解

```python
from typing import Optional, List, Dict, Any

def process_user(
    user_id: str,
    data: Dict[str, Any],
    active: bool = True
) -> Optional[User]:
    """处理用户并返回更新后的 User 或 None。"""
    if not active:
        return None
    return User(user_id, data)
```

### 现代 Python (3.9+)

```python
# Python 3.9+ - 使用内置类型
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

## 错误处理模式

### 特定异常处理

```python
# 好：捕获特定异常
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except FileNotFoundError as e:
        raise ConfigError(f"配置文件未找到: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"配置 JSON 无效: {path}") from e

# 坏：裸 except
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except:
        return None  # 静默失败！
```

## 上下文管理器

### 资源管理

```python
# 好：使用上下文管理器
def process_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

# 坏：手动资源管理
def process_file(path: str) -> str:
    f = open(path, 'r')
    try:
        return f.read()
    finally:
        f.close()
```

### 自定义上下文管理器

```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """计时代码块的上下文管理器。"""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{name} 耗时 {elapsed:.4f} 秒")

# 使用
with timer("数据处理"):
    process_large_dataset()
```

## 推导式和生成器

### 列表推导式

```python
# 好：列表推导式用于简单转换
names = [user.name for user in users if user.is_active]

# 坏：手动循环
names = []
for user in users:
    if user.is_active:
        names.append(user.name)
```

### 生成器表达式

```python
# 好：生成器用于惰性求值
total = sum(x * x for x in range(1_000_000))

# 坏：创建大型中间列表
total = sum([x * x for x in range(1_000_000)])
```

### 生成器函数

```python
def read_large_file(path: str) -> Iterator[str]:
    """逐行读取大文件。"""
    with open(path) as f:
        for line in f:
            yield line.strip()

# 使用
for line in read_large_file("huge.txt"):
    process(line)
```

## 数据类

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    """用户实体，自动生成 __init__、__repr__ 和 __eq__。"""
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

# 使用
user = User(
    id="123",
    name="Alice",
    email="alice@example.com"
)
```

## 装饰器

### 函数装饰器

```python
import functools
import time

def timer(func: Callable) -> Callable:
    """计时函数执行的装饰器。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 耗时 {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

## 并发模式

### 线程用于 I/O 密集任务

```python
import concurrent.futures

def fetch_url(url: str) -> str:
    """获取 URL（I/O 密集操作）。"""
    import urllib.request
    with urllib.request.urlopen(url) as response:
        return response.read().decode()

def fetch_all_urls(urls: list[str]) -> dict[str, str]:
    """使用线程并发获取多个 URL。"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        results = {}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as e:
                results[url] = f"错误: {e}"
    return results
```

### 多进程用于 CPU 密集任务

```python
def process_data(data: list[int]) -> int:
    """CPU 密集计算。"""
    return sum(x ** 2 for x in data)

def process_all(datasets: list[list[int]]) -> list[int]:
    """使用多进程处理多个数据集。"""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(process_data, datasets))
    return results
```

## 反模式（避免）

```python
# 坏：可变默认参数
def append_to(item, items=[]):
    items.append(item)
    return items

# 好：使用 None 并创建新列表
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# 坏：使用 type() 检查类型
if type(obj) == list:
    process(obj)

# 好：使用 isinstance
if isinstance(obj, list):
    process(obj)

# 坏：使用 == 与 None 比较
if value == None:
    process()

# 好：使用 is
if value is None:
    process()

# 坏：from module import *
from os.path import *

# 好：显式导入
from os.path import join, exists

# 坏：裸 except
try:
    risky_operation()
except:
    pass

# 好：特定异常
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"操作失败: {e}")
```

## 工具命令

```bash
# 代码格式化
black .
isort .

# 代码检查
ruff check .
pylint mypackage/

# 类型检查
mypy .

# 测试
pytest --cov=mypackage --cov-report=html

# 安全扫描
bandit -r .

# 依赖审计
pip-audit
safety check
```

## 快速参考

| 惯用法 | 描述 |
|--------|------|
| EAFP | 请求原谅比许可更容易 |
| 上下文管理器 | 使用 `with` 进行资源管理 |
| 列表推导式 | 用于简单转换 |
| 生成器 | 用于惰性求值和大数据集 |
| 类型提示 | 注解函数签名 |
| 数据类 | 自动生成方法的数据容器 |
| `__slots__` | 用于内存优化 |
| f-strings | 字符串格式化（Python 3.6+） |
| `pathlib.Path` | 路径操作（Python 3.4+） |
| `enumerate` | 循环中的索引-元素对 |

**记住**：Python 代码应该是可读的、显式的，并遵循最小惊讶原则。有疑问时，优先考虑清晰而非聪明。
