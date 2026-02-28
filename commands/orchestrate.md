# Orchestrate Command - 编排命令

<!--
================================================================================
命令说明（中文）
================================================================================

用途：为复杂任务执行顺序代理工作流。

用法：/orchestrate [workflow-type] [task-description]

工作流类型：
1. feature（功能）- 完整功能实现工作流
   流程：planner -> tdd-guide -> code-reviewer -> security-reviewer

2. bugfix（修复）- Bug调查和修复工作流
   流程：explorer -> tdd-guide -> code-reviewer

3. refactor（重构）- 安全重构工作流
   流程：architect -> code-reviewer -> tdd-guide

4. security（安全）- 安全审查
   流程：security-reviewer -> code-reviewer -> architect

5. custom（自定义）- 自定义代理序列
   用法：/orchestrate custom "architect,tdd-guide,code-reviewer" "描述"

执行模式：
- 每个代理使用上一个代理的上下文
- 收集输出作为结构化交接文档
- 传递给链中的下一个代理
- 将结果聚合到最终报告中

使用提示：
1. 复杂功能从 planner 开始
2. 合并前始终包含 code-reviewer
3. 涉及认证/支付/PII时使用 security-reviewer
4. 保持交接简洁 - 关注下一个代理需要什么

================================================================================
-->

Sequential agent workflow for complex tasks.

## Usage

`/orchestrate [workflow-type] [task-description]`

## Workflow Types

### feature
Full feature implementation workflow:
```
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

### bugfix
Bug investigation and fix workflow:
```
explorer -> tdd-guide -> code-reviewer
```

### refactor
Safe refactoring workflow:
```
architect -> code-reviewer -> tdd-guide
```

### security
Security-focused review:
```
security-reviewer -> code-reviewer -> architect
```

## Execution Pattern

For each agent in the workflow:

1. **Invoke agent** with context from previous agent
2. **Collect output** as structured handoff document
3. **Pass to next agent** in chain
4. **Aggregate results** into final report

## Handoff Document Format

Between agents, create handoff document:

```markdown
## HANDOFF: [previous-agent] -> [next-agent]

### Context
[Summary of what was done]

### Findings
[Key discoveries or decisions]

### Files Modified
[List of files touched]

### Open Questions
[Unresolved items for next agent]

### Recommendations
[Suggested next steps]
```

## Example: Feature Workflow

```
/orchestrate feature "Add user authentication"
```

Executes:

1. **Planner Agent**
   - Analyzes requirements
   - Creates implementation plan
   - Identifies dependencies
   - Output: `HANDOFF: planner -> tdd-guide`

2. **TDD Guide Agent**
   - Reads planner handoff
   - Writes tests first
   - Implements to pass tests
   - Output: `HANDOFF: tdd-guide -> code-reviewer`

3. **Code Reviewer Agent**
   - Reviews implementation
   - Checks for issues
   - Suggests improvements
   - Output: `HANDOFF: code-reviewer -> security-reviewer`

4. **Security Reviewer Agent**
   - Security audit
   - Vulnerability check
   - Final approval
   - Output: Final Report

## Final Report Format

```
ORCHESTRATION REPORT
====================
Workflow: feature
Task: Add user authentication
Agents: planner -> tdd-guide -> code-reviewer -> security-reviewer

SUMMARY
-------
[One paragraph summary]

AGENT OUTPUTS
-------------
Planner: [summary]
TDD Guide: [summary]
Code Reviewer: [summary]
Security Reviewer: [summary]

FILES CHANGED
-------------
[List all files modified]

TEST RESULTS
------------
[Test pass/fail summary]

SECURITY STATUS
---------------
[Security findings]

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

## Parallel Execution

For independent checks, run agents in parallel:

```markdown
### Parallel Phase
Run simultaneously:
- code-reviewer (quality)
- security-reviewer (security)
- architect (design)

### Merge Results
Combine outputs into single report
```

## Arguments

$ARGUMENTS:
- `feature <description>` - Full feature workflow
- `bugfix <description>` - Bug fix workflow
- `refactor <description>` - Refactoring workflow
- `security <description>` - Security review workflow
- `custom <agents> <description>` - Custom agent sequence

## Custom Workflow Example

```
/orchestrate custom "architect,tdd-guide,code-reviewer" "Redesign caching layer"
```

## Tips

1. **Start with planner** for complex features
2. **Always include code-reviewer** before merge
3. **Use security-reviewer** for auth/payment/PII
4. **Keep handoffs concise** - focus on what next agent needs
5. **Run verification** between agents if needed
