# /learn - 提取可复用模式

<!--
================================================================================
命令说明（中文）
================================================================================

用途：分析当前会话并提取值得保存为技能的模式。

触发时机：
- 在会话中解决了一个非平凡问题时，随时可以运行 /learn

提取内容：
1. 错误解决模式 - 发生了什么错误？根本原因是什么？如何修复的？
2. 调试技巧 - 非显而易见的调试步骤、有效的工具组合
3. 变通方案 - 库的怪异行为、API限制、版本特定的修复
4. 项目特定模式 - 发现的代码库约定、架构决策、集成模式

输出位置：~/.claude/skills/learned/[pattern-name].md

注意：
- 不要提取琐碎的修复（拼写错误、简单语法错误）
- 不要提取一次性问题（特定的API中断等）
- 专注于将来会话中能节省时间的模式
- 每个技能文件只包含一个模式

================================================================================
-->

Analyze the current session and extract any patterns worth saving as skills.

## Trigger

Run `/learn` at any point during a session when you've solved a non-trivial problem.

## What to Extract

Look for:

1. **Error Resolution Patterns**
   - What error occurred?
   - What was the root cause?
   - What fixed it?
   - Is this reusable for similar errors?

2. **Debugging Techniques**
   - Non-obvious debugging steps
   - Tool combinations that worked
   - Diagnostic patterns

3. **Workarounds**
   - Library quirks
   - API limitations
   - Version-specific fixes

4. **Project-Specific Patterns**
   - Codebase conventions discovered
   - Architecture decisions made
   - Integration patterns

## Output Format

Create a skill file at `~/.claude/skills/learned/[pattern-name].md`:

```markdown
# [Descriptive Pattern Name]

**Extracted:** [Date]
**Context:** [Brief description of when this applies]

## Problem
[What problem this solves - be specific]

## Solution
[The pattern/technique/workaround]

## Example
[Code example if applicable]

## When to Use
[Trigger conditions - what should activate this skill]
```

## Process

1. Review the session for extractable patterns
2. Identify the most valuable/reusable insight
3. Draft the skill file
4. Ask user to confirm before saving
5. Save to `~/.claude/skills/learned/`

## Notes

- Don't extract trivial fixes (typos, simple syntax errors)
- Don't extract one-time issues (specific API outages, etc.)
- Focus on patterns that will save time in future sessions
- Keep skills focused - one pattern per skill
