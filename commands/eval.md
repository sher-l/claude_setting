# Eval Command - 评估命令

<!--
================================================================================
命令说明（中文）
================================================================================

用途：管理评估驱动开发工作流。

用法：/eval [define|check|report|list] [feature-name]

操作类型：
1. define <name> - 创建新的评估定义
   创建 .claude/evals/feature-name.md 文件，包含：
   - 能力评估（Capability Evals）
   - 回归评估（Regression Evals）
   - 成功标准（pass@3 > 90% 等）

2. check <name> - 运行并检查评估
   - 读取评估定义
   - 验证每个能力标准
   - 运行回归测试
   - 记录通过/失败

3. report <name> - 生成完整评估报告
   包含：能力评估结果、回归评估结果、指标统计、建议

4. list - 显示所有评估定义及其状态

5. clean - 删除旧评估日志（保留最近10次运行）

指标说明：
- pass@1：首次尝试通过率
- pass@3：最多3次尝试通过率
- pass^3：连续3次通过率（用于回归测试）

================================================================================
-->

Manage eval-driven development workflow.

## Usage

`/eval [define|check|report|list] [feature-name]`

## Define Evals

`/eval define feature-name`

Create a new eval definition:

1. Create `.claude/evals/feature-name.md` with template:

```markdown
## EVAL: feature-name
Created: $(date)

### Capability Evals
- [ ] [Description of capability 1]
- [ ] [Description of capability 2]

### Regression Evals
- [ ] [Existing behavior 1 still works]
- [ ] [Existing behavior 2 still works]

### Success Criteria
- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
```

2. Prompt user to fill in specific criteria

## Check Evals

`/eval check feature-name`

Run evals for a feature:

1. Read eval definition from `.claude/evals/feature-name.md`
2. For each capability eval:
   - Attempt to verify criterion
   - Record PASS/FAIL
   - Log attempt in `.claude/evals/feature-name.log`
3. For each regression eval:
   - Run relevant tests
   - Compare against baseline
   - Record PASS/FAIL
4. Report current status:

```
EVAL CHECK: feature-name
========================
Capability: X/Y passing
Regression: X/Y passing
Status: IN PROGRESS / READY
```

## Report Evals

`/eval report feature-name`

Generate comprehensive eval report:

```
EVAL REPORT: feature-name
=========================
Generated: $(date)

CAPABILITY EVALS
----------------
[eval-1]: PASS (pass@1)
[eval-2]: PASS (pass@2) - required retry
[eval-3]: FAIL - see notes

REGRESSION EVALS
----------------
[test-1]: PASS
[test-2]: PASS
[test-3]: PASS

METRICS
-------
Capability pass@1: 67%
Capability pass@3: 100%
Regression pass^3: 100%

NOTES
-----
[Any issues, edge cases, or observations]

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

## List Evals

`/eval list`

Show all eval definitions:

```
EVAL DEFINITIONS
================
feature-auth      [3/5 passing] IN PROGRESS
feature-search    [5/5 passing] READY
feature-export    [0/4 passing] NOT STARTED
```

## Arguments

$ARGUMENTS:
- `define <name>` - Create new eval definition
- `check <name>` - Run and check evals
- `report <name>` - Generate full report
- `list` - Show all evals
- `clean` - Remove old eval logs (keeps last 10 runs)
