# Python 编码风格 (Python Coding Style)

<!--
  【中文注释说明】
  本文件定义了 Python 代码的编码规范，是对通用编码风格规则的扩展。

  主要内容包括：
  1. PEP 8 标准遵循
  2. 类型注解使用
  3. 不可变数据结构
  4. 代码格式化工具

  来源: https://github.com/affaan-m/everything-claude-code/blob/master/rules/python/coding-style.md
-->

> This file extends [common/coding-style.md](../common/coding-style.md) with Python specific content.
> 本文件扩展了通用编码风格规则，添加了 Python 特定的内容。

## Standards（编码标准）

- Follow **PEP 8** conventions
  <!-- 【中文说明】遵循 PEP 8 Python 编码规范，这是 Python 社区广泛接受的代码风格指南 -->

- Use **type annotations** on all function signatures
  <!-- 【中文说明】在所有函数签名上使用类型注解，提高代码可读性和 IDE 支持 -->

## Immutability（不可变性）

Prefer immutable data structures:
<!-- 【中文说明】优先使用不可变数据结构，这有助于减少副作用和 bug -->

```python
from dataclasses import dataclass

# 使用 frozen=True 创建不可变的数据类
# 【中文说明】frozen=True 使实例创建后不可修改
@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

# 使用 NamedTuple 创建不可变的命名元组
# 【中文说明】NamedTuple 是创建轻量级不可变数据结构的另一种方式
class Point(NamedTuple):
    x: float
    y: float
```

## Formatting（代码格式化）

- **black** for code formatting
  <!-- 【中文说明】使用 black 进行代码格式化，它是 Python 社区最流行的格式化工具 -->

- **isort** for import sorting
  <!-- 【中文说明】使用 isort 自动排序和整理 import 语句 -->

- **ruff** for linting
  <!-- 【中文说明】使用 ruff 进行代码检查，它是一个用 Rust 编写的超快速 linter -->

## Reference（参考资源）

See skill: `python-patterns` for comprehensive Python idioms and patterns.
<!-- 【中文说明】查看 python-patterns 技能获取更全面的 Python 惯用法和设计模式 -->
