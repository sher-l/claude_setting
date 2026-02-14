# 通用设计模式

## 骨架项目

实现新功能时：
1. 搜索经过实战检验的骨架项目
2. 使用并行代理评估选项：
   - 安全性评估
   - 可扩展性分析
   - 相关性评分
   - 实现规划
3. 克隆最佳匹配作为基础
4. 在已验证的结构内迭代

## 设计模式

### 仓库模式（Repository Pattern）

将数据访问封装在一致的接口后面：
- 定义标准操作：findAll、findById、create、update、delete
- 具体实现处理存储细节（数据库、API、文件等）
- 业务逻辑依赖抽象接口，而非存储机制
- 支持轻松切换数据源，简化测试mock

```python
# 抽象接口
class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass

# 具体实现
class DatabaseUserRepository(UserRepository):
    def find_by_id(self, user_id: str) -> Optional[User]:
        # 数据库查询逻辑
        pass

# 使用
def get_user(repo: UserRepository, user_id: str):
    return repo.find_by_id(user_id)
```

### API 响应格式

对所有API响应使用一致的包装：

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T           // 成功时有数据
  error?: string     // 失败时有错误信息
  meta?: {           // 分页响应的元数据
    total: number
    page: number
    limit: number
  }
}
```

使用示例：
```typescript
// 成功响应
return {
  success: true,
  data: users,
  meta: { total: 100, page: 1, limit: 10 }
}

// 错误响应
return {
  success: false,
  error: '用户未找到'
}
```

### 错误处理模式

```python
def safe_operation():
    try:
        result = risky_operation()
        return {'success': True, 'data': result}
    except SpecificError as e:
        logger.error(f'操作失败: {e}')
        return {'success': False, 'error': '用户友好的错误信息'}
    except Exception as e:
        logger.exception('未预期的错误')
        return {'success': False, 'error': '服务器内部错误'}
```

### 配置模式

```python
# 使用环境变量 + 默认值
import os

class Config:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    API_KEY: str = os.getenv('API_KEY')  # 必需，无默认值

    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            raise ValueError('API_KEY 环境变量未设置')
```

## 文件组织模式

### 按功能组织（推荐）

```
src/
├── auth/              # 认证功能
│   ├── auth.service.ts
│   ├── auth.controller.ts
│   └── auth.test.ts
├── users/             # 用户功能
│   ├── users.service.ts
│   └── users.controller.ts
└── shared/            # 共享工具
    └── utils.ts
```

### 按类型组织（不推荐）

```
src/
├── services/          # 所有服务
├── controllers/       # 所有控制器
├── tests/             # 所有测试
└── utils/             # 所有工具
```

**原因**：按功能组织使相关代码在一起，更易于维护和理解。
