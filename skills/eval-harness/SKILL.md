---
name: eval-harness
description: Claude Code会话的正式评估框架，实现评估驱动开发（EDD）原则
tools: Read, Write, Edit, Bash, Grep, Glob
---

# 评估线束技能 (Eval Harness Skill)

<!-- 中文说明：Claude Code会话的正式评估框架，实现评估驱动开发（EDD）原则 -->

Claude Code会话的正式评估框架，实现评估驱动开发（EDD）原则。

## 哲学 (Philosophy)

<!-- 中文说明：评估驱动开发将评估视为"AI开发的单元测试" -->
评估驱动开发将评估视为"AI开发的单元测试"：
- 在实现之前定义预期行为
- 在开发过程中持续运行评估
- 跟踪每次变更的回归
- 使用pass@k指标进行可靠性测量

## 评估类型 (Eval Types)

### 能力评估 (Capability Evals)
<!-- 中文说明：测试Claude是否能做以前做不到的事情 -->
测试Claude是否能做以前做不到的事情：
```markdown
[能力评估(CAPABILITY EVAL): feature-name]
任务(Task): Claude应该完成什么的描述
成功标准(Success Criteria):
  - [ ] 标准1
  - [ ] 标准2
  - [ ] 标准3
预期输出(Expected Output): 预期结果的描述
```

### 回归评估 (Regression Evals)
<!-- 中文说明：确保变更不会破坏现有功能 -->
确保变更不会破坏现有功能：
```markdown
[回归评估(REGRESSION EVAL): feature-name]
基线(Baseline): SHA或检查点名称
测试(Tests):
  - existing-test-1: PASS/FAIL
  - existing-test-2: PASS/FAIL
  - existing-test-3: PASS/FAIL
结果(Result): X/Y通过（之前是Y/Y）
```

## 评分器类型 (Grader Types)

### 1. 基于代码的评分器 (Code-Based Grader)
<!-- 中文说明：使用代码进行确定性检查 -->
使用代码进行确定性检查：
```bash
# 检查文件是否包含预期模式
grep -q "export function handleAuth" src/auth.ts && echo "PASS" || echo "FAIL"

# 检查测试是否通过
npm test -- --testPathPattern="auth" && echo "PASS" || echo "FAIL"

# 检查构建是否成功
npm run build && echo "PASS" || echo "FAIL"
```

### 2. 基于模型的评分器 (Model-Based Grader)
<!-- 中文说明：使用Claude评估开放式输出 -->
使用Claude评估开放式输出：
```markdown
[模型评分器提示(MODEL GRADER PROMPT)]
评估以下代码变更：
1. 是否解决了陈述的问题？
2. 结构是否良好？
3. 边界情况是否处理？
4. 错误处理是否适当？

评分(Score): 1-5（1=差，5=优秀）
推理(Reasoning): [解释]
```

### 3. 人工评分器 (Human Grader)
<!-- 中文说明：标记需要人工审查 -->
标记需要人工审查：
```markdown
[需要人工审查(HUMAN REVIEW REQUIRED)]
变更(Change): 变更内容的描述
原因(Reason): 为什么需要人工审查
风险级别(Risk Level): LOW/MEDIUM/HIGH
```

## 指标 (Metrics)

### pass@k
<!-- 中文说明："k次尝试中至少一次成功" -->
"k次尝试中至少一次成功"
- pass@1: 第一次尝试成功率
- pass@3: 3次尝试内成功
- 典型目标: pass@3 > 90%

### pass^k
<!-- 中文说明："所有k次试验都成功" -->
"所有k次试验都成功"
- 更高的可靠性标准
- pass^3: 3次连续成功
- 用于关键路径

## 评估工作流 (Eval Workflow)

### 1. 定义（编码前）(Define - Before Coding)
<!-- 中文说明：在编码前定义评估标准 -->
```markdown
## 评估定义(EVAL DEFINITION): feature-xyz

### 能力评估(Capability Evals)
1. 可以创建新用户账户
2. 可以验证邮箱格式
3. 可以安全哈希密码

### 回归评估(Regression Evals)
1. 现有登录仍然工作
2. 会话管理不变
3. 注销流程完整

### 成功指标(Success Metrics)
- 能力评估pass@3 > 90%
- 回归评估pass^3 = 100%
```

### 2. 实现 (Implement)
编写代码以通过定义的评估。

### 3. 评估 (Evaluate)
<!-- 中文说明：运行评估并记录结果 -->
```bash
# 运行能力评估
[运行每个能力评估，记录PASS/FAIL]

# 运行回归评估
npm test -- --testPathPattern="existing"

# 生成报告
```

### 4. 报告 (Report)
<!-- 中文说明：生成评估报告 -->
```markdown
评估报告(EVAL REPORT): feature-xyz
========================

能力评估(Capability Evals):
  create-user:     PASS (pass@1)
  validate-email:  PASS (pass@2)
  hash-password:   PASS (pass@1)
  总体(Overall):         3/3通过

回归评估(Regression Evals):
  login-flow:      PASS
  session-mgmt:    PASS
  logout-flow:     PASS
  总体(Overall):         3/3通过

指标(Metrics):
  pass@1: 67% (2/3)
  pass@3: 100% (3/3)

状态(Status): 准备审查(READY FOR REVIEW)
```

## 集成模式 (Integration Patterns)

### 实现前 (Pre-Implementation)
<!-- 中文说明：创建评估定义文件 -->
```
/eval define feature-name
```
在`.claude/evals/feature-name.md`创建评估定义文件

### 实现期间 (During Implementation)
<!-- 中文说明：运行当前评估并报告状态 -->
```
/eval check feature-name
```
运行当前评估并报告状态

### 实现后 (Post-Implementation)
<!-- 中文说明：生成完整评估报告 -->
```
/eval report feature-name
```
生成完整评估报告

## 评估存储 (Eval Storage)

<!-- 中文说明：在项目中存储评估 -->
在项目中存储评估：
```
.claude/
  evals/
    feature-xyz.md      # 评估定义
    feature-xyz.log     # 评估运行历史
    baseline.json       # 回归基线
```

## 最佳实践 (Best Practices)

<!-- 中文说明：评估驱动开发最佳实践 -->
1. **编码前定义评估** - 强制清晰思考成功标准
2. **频繁运行评估** - 早期捕获回归
3. **随时间跟踪pass@k** - 监控可靠性趋势
4. **尽可能使用代码评分器** - 确定性 > 概率性
5. **安全需人工审查** - 永远不要完全自动化安全检查
6. **保持评估快速** - 慢评估不会被运行
7. **与代码一起版本化评估** - 评估是一等公民

## 示例：添加认证 (Example: Adding Authentication)

<!-- 中文说明：添加认证功能的完整评估示例 -->
```markdown
## 评估(EVAL): add-authentication

### 阶段1：定义（10分钟）(Phase 1: Define)
能力评估(Capability Evals):
- [ ] 用户可以用邮箱/密码注册
- [ ] 用户可以用有效凭据登录
- [ ] 无效凭据被正确错误拒绝
- [ ] 会话在页面刷新后持久化
- [ ] 注销清除会话

回归评估(Regression Evals):
- [ ] 公共路由仍然可访问
- [ ] API响应不变
- [ ] 数据库模式兼容

### 阶段2：实现（不定）(Phase 2: Implement)
[编写代码]

### 阶段3：评估 (Phase 3: Evaluate)
运行: /eval check add-authentication

### 阶段4：报告 (Phase 4: Report)
评估报告(EVAL REPORT): add-authentication
==============================
能力(Capability): 5/5通过 (pass@3: 100%)
回归(Regression): 3/3通过 (pass^3: 100%)
状态(Status): 发布(SHIP IT)
```
