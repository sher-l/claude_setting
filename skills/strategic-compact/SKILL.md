---
name: strategic-compact
description: 建议在逻辑间隔手动压缩上下文，以保持任务阶段的上下文，而不是任意的自动压缩。
---

# 战略压缩技能 (Strategic Compact Skill)

<!-- 中文说明：在工作流的战略点建议手动/compact，而不是依赖任意的自动压缩 -->

建议在工作流的战略点手动执行`/compact`，而不是依赖任意的自动压缩。

## 为什么要战略压缩？ (Why Strategic Compaction?)

<!-- 中文说明：自动压缩的问题 -->
自动压缩在任意点触发：
- 经常在任务中间，丢失重要上下文
- 没有逻辑任务边界的意识
- 可能中断复杂的多步操作

<!-- 中文说明：战略压缩的优势 -->
在逻辑边界的战略压缩：
- **探索后，执行前** - 压缩研究上下文，保留实现计划
- **完成里程碑后** - 为下一阶段全新开始
- **重大上下文切换前** - 在不同任务前清除探索上下文

## 如何工作 (How It Works)

<!-- 中文说明：suggest-compact.sh脚本的工作原理 -->
`suggest-compact.sh`脚本在PreToolUse（Edit/Write）时运行：

1. **跟踪工具调用** - 计算会话中的工具调用次数
2. **阈值检测** - 在可配置阈值（默认：50次调用）时建议
3. **定期提醒** - 阈值后每25次调用提醒一次

## 钩子设置 (Hook Setup)

<!-- 中文说明：将钩子添加到settings.json -->
添加到你的`~/.claude/settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "tool == \"Edit\" || tool == \"Write\"",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/strategic-compact/suggest-compact.sh"
      }]
    }]
  }
}
```

## 配置 (Configuration)

<!-- 中文说明：可配置的环境变量 -->
环境变量：
- `COMPACT_THRESHOLD` - 第一次建议前的工具调用次数（默认：50）

## 最佳实践 (Best Practices)

<!-- 中文说明：战略压缩的最佳实践 -->
1. **规划后压缩** - 计划确定后，压缩以全新开始
2. **调试后压缩** - 在继续之前清除错误解决上下文
3. **不要在实现中间压缩** - 为相关变更保留上下文
4. **阅读建议** - 钩子告诉你*何时*，你决定*是否*

## 相关资源 (Related)

<!-- 中文说明：相关资源链接 -->
- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Token优化部分
- 内存持久化钩子 - 用于在压缩后保留状态
