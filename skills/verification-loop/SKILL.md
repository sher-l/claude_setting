---
name: verification-loop
description: Claude Code会话的综合验证系统，用于完成功能或重要代码更改后、创建PR前、确保质量门通过时使用。
---

# 验证循环技能 (Verification Loop Skill)

<!-- 中文说明：Claude Code会话的综合验证系统 -->

Claude Code会话的综合验证系统。

## 何时使用 (When to Use)

<!-- 中文说明：以下情况应该使用此技能 -->
调用此技能：
- 完成功能或重要代码更改后
- 创建PR之前
- 确保质量门通过时
- 重构后

## 验证阶段 (Verification Phases)

### 阶段1：构建验证 (Phase 1: Build Verification)
<!-- 中文说明：检查项目是否能正常构建 -->
```bash
# 检查项目是否构建
npm run build 2>&1 | tail -20
# 或者
pnpm build 2>&1 | tail -20
```

如果构建失败，停止并在继续之前修复。

### 阶段2：类型检查 (Phase 2: Type Check)
<!-- 中文说明：检查类型错误 -->
```bash
# TypeScript项目
npx tsc --noEmit 2>&1 | head -30

# Python项目
pyright . 2>&1 | head -30
```

报告所有类型错误。在继续之前修复关键错误。

### 阶段3：Lint检查 (Phase 3: Lint Check)
<!-- 中文说明：代码风格检查 -->
```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

### 阶段4：测试套件 (Phase 4: Test Suite)
<!-- 中文说明：运行测试并检查覆盖率 -->
```bash
# 运行带覆盖率的测试
npm run test -- --coverage 2>&1 | tail -50

# 检查覆盖率阈值
# 目标：最低80%
```

报告：
- 总测试数：X
- 通过：X
- 失败：X
- 覆盖率：X%

### 阶段5：安全扫描 (Phase 5: Security Scan)
<!-- 中文说明：检查安全问题和敏感信息泄露 -->
```bash
# 检查密钥
grep -rn "sk-" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# 检查console.log
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### 阶段6：差异审查 (Phase 6: Diff Review)
<!-- 中文说明：查看变更内容 -->
```bash
# 显示变更内容
git diff --stat
git diff HEAD~1 --name-only
```

审查每个变更文件的：
- 非预期变更
- 缺失的错误处理
- 潜在的边界情况

## 输出格式 (Output Format)

<!-- 中文说明：验证报告的标准格式 -->
运行所有阶段后，生成验证报告：

```
验证报告 (VERIFICATION REPORT)
==================

构建(Build):     [通过/失败(PASS/FAIL)]
类型(Types):     [通过/失败(PASS/FAIL)] (X个错误)
Lint:           [通过/失败(PASS/FAIL)] (X个警告)
测试(Tests):     [通过/失败(PASS/FAIL)] (X/Y通过, Z%覆盖率)
安全(Security):  [通过/失败(PASS/FAIL)] (X个问题)
差异(Diff):      [X个文件变更]

总体(Overall):   [准备就绪/未准备好(READY/NOT READY)] 提交PR

需要修复的问题：
1. ...
2. ...
```

## 持续模式 (Continuous Mode)

<!-- 中文说明：长时间会话中的验证策略 -->
对于长时间会话，每15分钟或主要变更后运行验证：

```markdown
设置心理检查点：
- 完成每个函数后
- 完成组件后
- 进入下一个任务前

运行：/verify
```

## 与钩子集成 (Integration with Hooks)

<!-- 中文说明：此技能与PostToolUse钩子互补，但提供更深入的验证 -->
此技能与PostToolUse钩子互补，但提供更深入的验证。
钩子立即捕获问题；此技能提供全面审查。
