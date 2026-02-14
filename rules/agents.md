# 代理调度规则

## 可用代理

位于 `~/.claude/agents/`：

| 代理 | 用途 | 何时使用 |
|------|------|---------|
| planner | 实现规划 | 复杂功能、重构 |
| code-reviewer | 代码审查 | 写完代码后 |
| tdd-guide | 测试驱动开发 | 新功能、bug修复 |
| security-reviewer | 安全分析 | 提交前 |
| build-error-resolver | 修复构建错误 | 构建失败时 |
| refactor-cleaner | 死代码清理 | 代码维护 |

## 立即使用代理（无需用户确认）

1. 复杂功能请求 → 使用 **planner** 代理
2. 代码刚写完/修改完 → 使用 **code-reviewer** 代理
3. Bug修复或新功能 → 使用 **tdd-guide** 代理
4. 架构决策 → 使用 **architect** 代理
5. 构建失败 → 使用 **build-error-resolver** 代理
6. 发现安全问题 → 使用 **security-reviewer** 代理

## 并行执行原则

**始终**对独立操作使用并行Task执行：

```markdown
# ✓ 好：并行执行
同时启动3个代理：
1. 代理1：auth模块安全分析
2. 代理2：缓存系统性能审查
3. 代理3：工具类型检查

# ✗ 差：不必要的顺序
先代理1，然后代理2，然后代理3
```

## 多角度分析

对于复杂问题，使用分角色子代理：
- 事实审查员
- 高级工程师
- 安全专家
- 一致性审查员
- 冗余检查员

## 代理使用时机

| 场景 | 使用代理 | 原因 |
|------|---------|------|
| 用户说"实现X" | planner | 需要先规划 |
| 代码修改完成 | code-reviewer | 自动审查 |
| 构建失败 | build-error-resolver | 快速修复 |
| 涉及用户输入 | security-reviewer | 安全检查 |
| 测试失败 | tdd-guide | TDD方法论 |
| 代码库膨胀 | refactor-cleaner | 清理死代码 |
