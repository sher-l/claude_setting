---
name: python-testing
description: Python 测试策略，使用 pytest、TDD 方法论、fixtures、mocking、参数化和覆盖率要求。
---

# Python 测试模式

使用 pytest、TDD 方法论和最佳实践的全面测试策略。

## 核心测试理念

### 测试驱动开发（TDD）

始终遵循 TDD 循环：

1. **RED**：为期望行为编写失败的测试
2. **GREEN**：编写最小代码使测试通过
3. **REFACTOR**：改进代码同时保持测试通过

```python
# 步骤1：编写失败测试（RED）
def test_add_numbers():
    result = add(2, 3)
    assert result == 5

# 步骤2：编写最小实现（GREEN）
def add(a, b):
    return a + b

# 步骤3：按需重构（REFACTOR）
```

### 覆盖率要求

- **目标**：80%+ 代码覆盖率
- **关键路径**：100% 覆盖率
- 使用 `pytest --cov` 测量覆盖率

```bash
pytest --cov=mypackage --cov-report=term-missing --cov-report=html
```

## pytest 基础

### 基本测试结构

```python
import pytest

def test_addition():
    """测试基本加法。"""
    assert 2 + 2 == 4

def test_string_uppercase():
    """测试字符串大写。"""
    text = "hello"
    assert text.upper() == "HELLO"

def test_list_append():
    """测试列表追加。"""
    items = [1, 2, 3]
    items.append(4)
    assert 4 in items
    assert len(items) == 4
```

### 断言

```python
# 相等
assert result == expected

# 真值
assert result  # 真值
assert not result  # 假值
assert result is None  # 恰好 None

# 成员
assert item in collection
assert item not in collection

# 类型检查
assert isinstance(result, str)

# 异常测试
with pytest.raises(ValueError):
    raise ValueError("error message")

# 检查异常消息
with pytest.raises(ValueError, match="invalid input"):
    raise ValueError("invalid input provided")
```

## Fixtures

### 基本 Fixture 使用

```python
import pytest

@pytest.fixture
def sample_data():
    """提供样本数据的 fixture。"""
    return {"name": "Alice", "age": 30}

def test_sample_data(sample_data):
    """使用 fixture 的测试。"""
    assert sample_data["name"] == "Alice"
    assert sample_data["age"] == 30
```

### 带 Setup/Teardown 的 Fixture

```python
@pytest.fixture
def database():
    """带 setup 和 teardown 的 fixture。"""
    # Setup
    db = Database(":memory:")
    db.create_tables()
    db.insert_test_data()

    yield db  # 提供给测试

    # Teardown
    db.close()

def test_database_query(database):
    """测试数据库操作。"""
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Fixture 作用域

```python
# 函数作用域（默认）- 每个测试运行
@pytest.fixture
def temp_file():
    with open("temp.txt", "w") as f:
        yield f
    os.remove("temp.txt")

# 模块作用域 - 每个模块运行一次
@pytest.fixture(scope="module")
def module_db():
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

# 会话作用域 - 每个测试会话运行一次
@pytest.fixture(scope="session")
def shared_resource():
    resource = ExpensiveResource()
    yield resource
    resource.cleanup()
```

## 参数化

### 基本参数化

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("PyThOn", "PYTHON"),
])
def test_uppercase(input, expected):
    """测试运行3次，每次不同输入。"""
    assert input.upper() == expected
```

### 多参数

```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    """使用多个输入测试加法。"""
    assert add(a, b) == expected
```

## Mocking

### Mock 函数

```python
from unittest.mock import patch, Mock

@patch("mypackage.external_api_call")
def test_with_mock(api_call_mock):
    """使用 mock 的外部 API 测试。"""
    api_call_mock.return_value = {"status": "success"}

    result = my_function()

    api_call_mock.assert_called_once()
    assert result["status"] == "success"
```

### Mock 异常

```python
@patch("mypackage.api_call")
def test_api_error_handling(api_call_mock):
    """使用 mock 异常测试错误处理。"""
    api_call_mock.side_effect = ConnectionError("Network error")

    with pytest.raises(ConnectionError):
        api_call()

    api_call_mock.assert_called_once()
```

## 测试异步代码

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """测试异步函数。"""
    result = await async_add(2, 3)
    assert result == 5

@pytest.mark.asyncio
async def test_async_with_fixture(async_client):
    """使用异步 fixture 测试。"""
    response = await async_client.get("/api/users")
    assert response.status_code == 200
```

## 测试组织

### 目录结构

```
tests/
├── conftest.py                 # 共享 fixtures
├── __init__.py
├── unit/                       # 单元测试
│   ├── __init__.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/                # 集成测试
│   ├── __init__.py
│   └── test_api.py
└── e2e/                        # 端到端测试
    ├── __init__.py
    └── test_user_flow.py
```

### 测试类

```python
class TestUserService:
    """在类中组织相关测试。"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """setup 在此类每个测试前运行。"""
        self.service = UserService()

    def test_create_user(self):
        """测试用户创建。"""
        user = self.service.create_user("Alice")
        assert user.name == "Alice"

    def test_delete_user(self):
        """测试用户删除。"""
        user = User(id=1, name="Bob")
        self.service.delete_user(user)
        assert not self.service.user_exists(1)
```

## 最佳实践

### 应该做

- **遵循 TDD**：先写测试再写代码（红-绿-重构）
- **测试一件事**：每个测试验证单一行为
- **使用描述性名称**：`test_user_login_with_invalid_credentials_fails`
- **使用 fixtures**：用 fixtures 消除重复
- **Mock 外部依赖**：不依赖外部服务
- **测试边界情况**：空输入、None 值、边界条件
- **目标 80%+ 覆盖率**：专注于关键路径
- **保持测试快速**：使用标记分离慢测试

### 不应该做

- **不测试实现**：测试行为，而非内部
- **不在测试中使用复杂条件**：保持测试简单
- **不忽略测试失败**：所有测试必须通过
- **不测试第三方代码**：信任库能工作
- **不在测试间共享状态**：测试应该独立
- **不在测试中捕获异常**：使用 `pytest.raises`

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_utils.py

# 运行特定测试
pytest tests/test_utils.py::test_function

# 详细输出
pytest -v

# 带覆盖率
pytest --cov=mypackage --cov-report=html

# 只运行快速测试
pytest -m "not slow"

# 运行直到第一个失败
pytest -x

# 运行最后失败的测试
pytest --lf

# 运行匹配模式的测试
pytest -k "test_user"
```

## 快速参考

| 模式 | 用法 |
|------|------|
| `pytest.raises()` | 测试预期异常 |
| `@pytest.fixture()` | 创建可重用的测试 fixtures |
| `@pytest.mark.parametrize()` | 使用多个输入运行测试 |
| `@pytest.mark.slow` | 标记慢测试 |
| `pytest -m "not slow"` | 跳过慢测试 |
| `@patch()` | Mock 函数和类 |
| `tmp_path` fixture | 自动临时目录 |
| `pytest --cov` | 生成覆盖率报告 |

**记住**：测试也是代码。保持它们干净、可读、可维护。好的测试捕获 bug；优秀的测试防止它们。
