---
name: continuous-learning
description: 自动从 Claude Code 会话中提取可复用模式，保存为学习技能供未来使用。
---

# 持续学习技能

自动评估 Claude Code 会话，提取可复用模式并保存为学习技能。

## 工作原理

此技能作为 **Stop hook** 在每个会话结束时运行：

1. **会话评估**：检查会话是否有足够消息（默认：10+）
2. **模式检测**：识别会话中可提取的模式
3. **技能提取**：将有用模式保存到 `~/.claude/skills/learned/`

## 配置

编辑 `config.json` 自定义：

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/skills/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## 模式类型

| 模式 | 描述 |
|------|------|
| `error_resolution` | 如何解决特定错误 |
| `user_corrections` | 来自用户纠正的模式 |
| `workarounds` | 框架/库怪癖的解决方案 |
| `debugging_techniques` | 有效的调试方法 |
| `project_specific` | 项目特定约定 |

## Hook 设置

添加到 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "node -e \"console.error('[Learning] 会话结束，可手动运行 /learn 提取模式')\""
      }]
    }]
  }
}
```

## 为什么用 Stop Hook？

- **轻量级**：会话结束时运行一次
- **非阻塞**：不给每条消息增加延迟
- **完整上下文**：可访问完整会话记录

## 手动使用

```
/learn    # 手动从当前会话提取模式
```

## 相关

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - 持续学习部分
- `/learn` 命令 - 会话中手动提取模式

---

**记住**：从会话中学习的模式可以帮助你在未来避免重复工作。
