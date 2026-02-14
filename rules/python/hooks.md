# Python 钩子配置 (Python Hooks)

<!--
  【中文注释说明】
  本文件定义了 Python 相关的 Claude Code 钩子配置，用于自动化代码质量检查。

  主要内容包括：
  1. PostToolUse 钩子 - 工具使用后自动执行的检查
  2. 代码格式化和类型检查的自动触发
  3. 代码警告配置

  来源: https://github.com/affaan-m/everything-claude-code/blob/master/rules/python/hooks.md
-->

> This file extends [common/hooks.md](../common/hooks.md) with Python specific content.
> 本文件扩展了通用钩子规则，添加了 Python 特定的内容。

## PostToolUse Hooks（工具使用后钩子）

Configure in `~/.claude/settings.json`:
<!-- 【中文说明】在 ~/.claude/settings.json 中配置以下钩子 -->

- **black/ruff**: Auto-format `.py` files after edit
  <!-- 【中文说明】编辑 .py 文件后自动使用 black 或 ruff 格式化代码 -->

- **mypy/pyright**: Run type checking after editing `.py` files
  <!-- 【中文说明】编辑 .py 文件后自动运行 mypy 或 pyright 进行类型检查 -->

## Warnings（警告设置）

- Warn about `print()` statements in edited files (use `logging` module instead)
  <!-- 【中文说明】警告编辑文件中的 print() 语句，建议使用 logging 模块替代，因为 logging 提供更好的日志级别控制和输出格式 -->

<!--
  【配置示例】

  在 settings.json 中的配置示例：

  {
    "hooks": {
      "PostToolUse": [
        {
          "matcher": "*.py",
          "hooks": [
            {
              "type": "command",
              "command": "ruff format $FILE"
            },
            {
              "type": "command",
              "command": "mypy $FILE"
            }
          ]
        }
      ]
    }
  }
-->
