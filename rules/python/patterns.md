# Python 设计模式 (Python Patterns)

<!--
  【中文注释说明】
  本文件介绍了 Python 中常用的设计模式和编程范式。

  主要内容包括：
  1. Protocol（鸭子类型的结构化子类型）
  2. Dataclass 作为 DTO（数据传输对象）
  3. 上下文管理器和生成器

  来源: https://github.com/affaan-m/everything-claude-code/blob/master/rules/python/patterns.md
-->

> This file extends [common/patterns.md](../common/patterns.md) with Python specific content.
> 本文件扩展了通用设计模式规则，添加了 Python 特定的内容。

## Protocol (Duck Typing)（协议 - 鸭子类型）

<!-- 【中文说明】
  Protocol 是 Python 3.8+ 引入的结构化子类型机制。
  它允许定义"协议"（接口），只要类实现了协议中定义的方法，就被视为该协议的子类型。
  这就是"鸭子类型"的静态类型版本 - "如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子"。
-->

```python
from typing import Protocol

# 定义一个仓库协议（接口）
# 【中文说明】任何实现了 find_by_id 和 save 方法的类都可以作为 Repository 使用
class Repository(Protocol):
    def find_by_id(self, id: str) -> dict | None: ...
    def save(self, entity: dict) -> dict: ...
```

## Dataclasses as DTOs（使用 Dataclass 作为数据传输对象）

<!-- 【中文说明】
  Dataclass 是 Python 3.7+ 引入的装饰器，用于自动生成 __init__、__repr__ 等方法。
  它非常适合用作 DTO（Data Transfer Object），即在不同层之间传输数据的容器。
-->

```python
from dataclasses import dataclass

# 创建用户请求的数据传输对象
# 【中文说明】使用 dataclass 减少样板代码，自动生成初始化方法
# age 字段使用 | None 表示可选，默认值为 None
@dataclass
class CreateUserRequest:
    name: str
    email: str
    age: int | None = None  # 可选字段，使用 Python 3.10+ 的联合类型语法
```

## Context Managers & Generators（上下文管理器和生成器）

- Use context managers (`with` statement) for resource management
  <!-- 【中文说明】使用上下文管理器（with 语句）管理资源，如文件、数据库连接等，确保资源正确释放 -->

- Use generators for lazy evaluation and memory-efficient iteration
  <!-- 【中文说明】使用生成器实现惰性求值和内存高效的迭代，特别适合处理大数据集 -->

<!--
  【中文示例】

  # 上下文管理器示例
  with open('file.txt', 'r') as f:  # 文件会自动关闭
      content = f.read()

  # 生成器示例
  def read_large_file(file_path):
      """逐行读取大文件，避免一次性加载到内存"""
      with open(file_path, 'r') as f:
          for line in f:
              yield line.strip()

  # 使用生成器
  for line in read_large_file('large_file.txt'):
      process(line)
-->

## Reference（参考资源）

See skill: `python-patterns` for comprehensive patterns including decorators, concurrency, and package organization.
<!-- 【中文说明】查看 python-patterns 技能获取更全面的模式，包括装饰器、并发和包组织等 -->
