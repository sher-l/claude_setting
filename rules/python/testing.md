# Python 测试规范 (Python Testing)

<!--
  【中文注释说明】
  本文件定义了 Python 代码的测试最佳实践。

  主要内容包括：
  1. 测试框架选择
  2. 测试覆盖率
  3. 测试组织和分类

  来源: https://github.com/affaan-m/everything-claude-code/blob/master/rules/python/testing.md
-->

> This file extends [common/testing.md](../common/testing.md) with Python specific content.
> 本文件扩展了通用测试规则，添加了 Python 特定的内容。

## Framework（测试框架）

Use **pytest** as the testing framework.
<!-- 【中文说明】
  使用 pytest 作为测试框架，它是 Python 社区最受欢迎的测试框架，具有以下优势：
  - 简洁的语法（不需要继承 TestCase 类）
  - 强大的断言机制（assert 语句）
  - 丰富的插件生态
  - 内置的参数化测试支持
-->

## Coverage（测试覆盖率）

```bash
pytest --cov=src --cov-report=term-missing
```
<!-- 【中文说明】
  运行测试并生成覆盖率报告：
  - --cov=src：指定要测量覆盖率的源代码目录
  - --cov-report=term-missing：在终端输出报告，并显示未覆盖的具体行号

  其他有用的选项：
  - --cov-report=html：生成 HTML 格式的详细报告
  - --cov-fail-under=80：覆盖率低于 80% 时测试失败
-->

## Test Organization（测试组织）

Use `pytest.mark` for test categorization:
<!-- 【中文说明】使用 pytest.mark 装饰器对测试进行分类，便于选择性运行 -->

```python
import pytest

# 单元测试标记
# 【中文说明】单元测试测试单个函数或方法，不依赖外部资源
@pytest.mark.unit
def test_calculate_total():
    ...

# 集成测试标记
# 【中文说明】集成测试测试多个组件的协作，可能依赖数据库、API 等外部资源
@pytest.mark.integration
def test_database_connection():
    ...
```

<!--
  【中文补充】

  1. 配置 pytest.ini 或 pyproject.toml 来注册自定义标记：

     # pytest.ini
     [pytest]
     markers =
         unit: 单元测试
         integration: 集成测试
         slow: 运行缓慢的测试

  2. 选择性运行测试：

     # 只运行单元测试
     pytest -m unit

     # 跳过缓慢的测试
     pytest -m "not slow"

     # 运行特定标记组合
     pytest -m "unit and not slow"

  3. 常用 pytest 命令：

     pytest                    # 运行所有测试
     pytest -v                 # 详细输出
     pytest -x                 # 第一次失败就停止
     pytest --tb=short         # 简短的错误追溯
     pytest -k "keyword"       # 运行名称包含关键字的测试

  4. 测试文件命名约定：

     test_*.py 或 *_test.py
     测试类以 Test 开头
     测试函数以 test_ 开头
-->

## Reference（参考资源）

See skill: `python-testing` for detailed pytest patterns and fixtures.
<!-- 【中文说明】查看 python-testing 技能获取详细的 pytest 模式和 fixture 使用方法 -->
