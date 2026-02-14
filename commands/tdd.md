---
description: 测试驱动开发工作流 - 先写测试，后写代码。
---

# /tdd 命令

强制执行测试驱动开发工作流。

## 工作流

### 1. RED - 先写测试

```python
def test_new_feature():
    # 描述预期行为
    result = new_function(input)

    assert result == expected_output
```

### 2. 运行测试（应该失败）

```bash
pytest test_file.py
# 测试失败 ✓ - 我们还没实现
```

### 3. GREEN - 编写最小实现

```python
def new_function(input):
    # 最小代码使测试通过
    return expected_output
```

### 4. 运行测试（应该通过）

```bash
pytest test_file.py
# 测试通过 ✓
```

### 5. REFACTOR - 改进代码

- 消除重复
- 改进命名
- 优化性能
- 确保测试仍然通过

### 6. 验证覆盖率

```bash
pytest --cov=. --cov-report=html
# 目标：80%+
```

## 测试类型要求

- **单元测试**：所有公共函数
- **集成测试**：所有API端点
- **E2E测试**：关键用户流程

## 检查清单

- [ ] 测试先写
- [ ] 测试先失败（RED）
- [ ] 最小实现（GREEN）
- [ ] 重构（IMPROVE）
- [ ] 覆盖率80%+
