---
description: 全面的 Python 代码审查，检查 PEP 8 合规、类型提示、安全和 Pythonic 惯用法。
---

# /python-review 命令

调用 **python-reviewer** 代理进行全面的 Python 代码审查。

## 这个命令做什么

1. **识别 Python 变更**：通过 `git diff` 查找修改的 `.py` 文件
2. **运行静态分析**：执行 `ruff`、`mypy`、`pylint`、`black --check`
3. **安全扫描**：检查 SQL 注入、命令注入、不安全反序列化
4. **类型安全审查**：分析类型提示和 mypy 错误
5. **Pythonic 代码检查**：验证代码遵循 PEP 8 和 Python 最佳实践
6. **生成报告**：按严重性分类问题

## 审查类别

### 关键（必须修复）
- SQL/命令注入漏洞
- 不安全的 eval/exec 使用
- Pickle 不安全反序列化
- 硬编码凭证
- YAML 不安全加载
- 裸 except 子句隐藏错误

### 高（应该修复）
- 公共函数缺少类型提示
- 可变默认参数
- 静默吞掉异常
- 资源不使用上下文管理器
- C 风格循环而非推导式
- 使用 type() 而非 isinstance()
- 无锁的竞态条件

### 中（考虑修复）
- PEP 8 格式违规
- 公共函数缺少 docstrings
- 使用 print 而非 logging
- 低效字符串操作
- 魔法数字无命名常量
- 不使用 f-strings 格式化

## 自动检查

```bash
# 类型检查
mypy .

# 代码检查和格式
ruff check .
black --check .
isort --check-only .

# 安全扫描
bandit -r .

# 依赖审计
pip-audit
safety check

# 测试
pytest --cov=app --cov-report=term-missing
```

## 批准标准

| 状态 | 条件 |
|------|------|
| ✅ 批准 | 无关键或高优先级问题 |
| ⚠️ 警告 | 仅中优先级问题（谨慎合并） |
| ❌ 阻止 | 发现关键或高优先级问题 |

## 常见修复

### 添加类型提示
```python
# 之前
def calculate(x, y):
    return x + y

# 之后
def calculate(x: int | float, y: int | float) -> int | float:
    return x + y
```

### 使用上下文管理器
```python
# 之前
f = open("file.txt")
data = f.read()
f.close()

# 之后
with open("file.txt") as f:
    data = f.read()
```

### 使用列表推导式
```python
# 之前
result = []
for item in items:
    if item.active:
        result.append(item.name)

# 之后
result = [item.name for item in items if item.active]
```

### 修复可变默认参数
```python
# 之前
def append(value, items=[]):
    items.append(value)
    return items

# 之后
def append(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items
```
