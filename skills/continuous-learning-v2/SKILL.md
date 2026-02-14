---
name: continuous-learning-v2
description: 基于本能的学习系统，通过钩子观察会话，创建带置信度评分的原子本能，并将其演化为技能/命令/代理。
version: 2.0.0
---

# 持续学习v2 - 基于本能的架构 (Continuous Learning v2 - Instinct-Based Architecture)

<!-- 中文说明：通过原子"本能"将Claude Code会话转化为可复用知识的高级学习系统 -->

一个高级学习系统，通过原子"本能"将你的Claude Code会话转化为可复用知识——带有置信度评分的小型学习行为。

## v2新特性 (What's New in v2)

<!-- 中文说明：v1与v2的功能对比 -->
| 特性 | v1 | v2 |
|------|----|----|
| 观察 | 停止钩子（会话结束） | PreToolUse/PostToolUse（100%可靠） |
| 分析 | 主上下文 | 后台代理（Haiku） |
| 粒度 | 完整技能 | 原子"本能" |
| 置信度 | 无 | 0.3-0.9加权 |
| 演化 | 直接到技能 | 本能 → 聚类 → 技能/命令/代理 |
| 共享 | 无 | 导出/导入本能 |

## 本能模型 (The Instinct Model)

<!-- 中文说明：本能是一个小型学习行为 -->
一个本能是一个小型学习行为：

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
---

# 优先使用函数式风格 (Prefer Functional Style)

## 行动(Action)
在适当时优先使用函数式模式而非类。

## 证据(Evidence)
- 观察到5次函数式模式偏好
- 用户在2025-01-15将基于类的方法更正为函数式
```

**属性：**
- **原子性** — 一个触发器，一个行动
- **置信度加权** — 0.3 = 尝试性，0.9 = 接近确定
- **领域标记** — 代码风格、测试、git、调试、工作流等
- **证据支持** — 跟踪哪些观察创建了它

## 如何工作 (How It Works)

<!-- 中文说明：系统工作流程图 -->
```
会话活动(Session Activity)
      │
      │ 钩子捕获提示+工具使用（100%可靠）
      ▼
┌─────────────────────────────────────────┐
│         observations.jsonl              │
│   （提示、工具调用、结果）                │
└─────────────────────────────────────────┘
      │
      │ 观察者代理读取（后台，Haiku）
      ▼
┌─────────────────────────────────────────┐
│          模式检测(PATTERN DETECTION)              │
│   • 用户更正 → 本能         │
│   • 错误解决 → 本能        │
│   • 重复工作流 → 本能       │
└─────────────────────────────────────────┘
      │
      │ 创建/更新
      ▼
┌─────────────────────────────────────────┐
│         instincts/personal/             │
│   • prefer-functional.md (0.7)          │
│   • always-test-first.md (0.9)          │
│   • use-zod-validation.md (0.6)         │
└─────────────────────────────────────────┘
      │
      │ /evolve聚类
      ▼
┌─────────────────────────────────────────┐
│              evolved/                   │
│   • commands/new-feature.md             │
│   • skills/testing-workflow.md          │
│   • agents/refactor-specialist.md       │
└─────────────────────────────────────────┘
```

## 快速开始 (Quick Start)

### 1. 启用观察钩子 (Enable Observation Hooks)

<!-- 中文说明：添加钩子到settings.json -->
添加到你的`~/.claude/settings.json`。

**如果作为插件安装**（推荐）：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh pre"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh post"
      }]
    }]
  }
}
```

**如果手动安装**到`~/.claude/skills`：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh pre"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh post"
      }]
    }]
  }
}
```

### 2. 初始化目录结构 (Initialize Directory Structure)

<!-- 中文说明：Python CLI会自动创建这些，也可以手动创建 -->
Python CLI会自动创建这些，但你也可以手动创建：

```bash
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands}}
touch ~/.claude/homunculus/observations.jsonl
```

### 3. 使用本能命令 (Use the Instinct Commands)

<!-- 中文说明：可用的命令列表 -->
```bash
/instinct-status     # 显示带置信度分数的学习本能
/evolve              # 将相关本能聚类为技能/命令
/instinct-export     # 导出本能以供共享
/instinct-import     # 从他人导入本能
```

## 命令 (Commands)

| 命令 | 描述 |
|------|------|
| `/instinct-status` | 显示所有学习本能及其置信度 |
| `/evolve` | 将相关本能聚类为技能/命令 |
| `/instinct-export` | 导出本能以供共享 |
| `/instinct-import <file>` | 从他人导入本能 |

## 配置 (Configuration)

<!-- 中文说明：编辑config.json配置系统行为 -->
编辑`config.json`：

```json
{
  "version": "2.0",
  "observation": {
    "enabled": true,
    "store_path": "~/.claude/homunculus/observations.jsonl",
    "max_file_size_mb": 10,
    "archive_after_days": 7
  },
  "instincts": {
    "personal_path": "~/.claude/homunculus/instincts/personal/",
    "inherited_path": "~/.claude/homunculus/instincts/inherited/",
    "min_confidence": 0.3,
    "auto_approve_threshold": 0.7,
    "confidence_decay_rate": 0.05
  },
  "observer": {
    "enabled": true,
    "model": "haiku",
    "run_interval_minutes": 5,
    "patterns_to_detect": [
      "user_corrections",
      "error_resolutions",
      "repeated_workflows",
      "tool_preferences"
    ]
  },
  "evolution": {
    "cluster_threshold": 3,
    "evolved_path": "~/.claude/homunculus/evolved/"
  }
}
```

## 文件结构 (File Structure)

<!-- 中文说明：系统的文件目录结构 -->
```
~/.claude/homunculus/
├── identity.json           # 你的配置文件，技术水平
├── observations.jsonl      # 当前会话观察
├── observations.archive/   # 已处理的观察
├── instincts/
│   ├── personal/           # 自动学习的本能
│   └── inherited/          # 从他人导入的
└── evolved/
    ├── agents/             # 生成的专业代理
    ├── skills/             # 生成的技能
    └── commands/           # 生成的命令
```

## 与技能创建器集成 (Integration with Skill Creator)

<!-- 中文说明：Skill Creator现在生成两种格式 -->
当你使用[Skill Creator GitHub App](https://skill-creator.app)时，它现在生成**两种**：
- 传统SKILL.md文件（向后兼容）
- 本能集合（用于v2学习系统）

来自仓库分析的本能有`source: "repo-analysis"`并包含源仓库URL。

## 置信度评分 (Confidence Scoring)

<!-- 中文说明：置信度随时间演化 -->
置信度随时间演化：

| 分数 | 含义 | 行为 |
|------|------|------|
| 0.3 | 尝试性 | 建议但不强制 |
| 0.5 | 中等 | 相关时应用 |
| 0.7 | 强 | 自动批准应用 |
| 0.9 | 接近确定 | 核心行为 |

**置信度增加**当：
- 重复观察到模式
- 用户不更正建议的行为
- 来自其他来源的类似本能一致

**置信度降低**当：
- 用户明确更正行为
- 长时间未观察到模式
- 出现矛盾证据

## 为什么用钩子而不是技能来观察？ (Why Hooks vs Skills for Observation?)

<!-- 中文说明：钩子比技能更可靠 -->
> "v1依赖技能来观察。技能是概率性的——基于Claude的判断，它们大约50-80%的时间触发。"

钩子**100%的时间**触发，确定性地。这意味着：
- 每个工具调用都被观察
- 没有模式被遗漏
- 学习是全面的

## 向后兼容性 (Backward Compatibility)

<!-- 中文说明：v2与v1完全兼容 -->
v2与v1完全兼容：
- 现有`~/.claude/skills/learned/`技能仍然工作
- 停止钩子仍然运行（但现在也输入到v2）
- 渐进迁移路径：并行运行两者

## 隐私 (Privacy)

<!-- 中文说明：隐私保护措施 -->
- 观察保留在你的机器**本地**
- 只有**本能**（模式）可以导出
- 不共享实际代码或对话内容
- 你控制导出什么

## 相关资源 (Related)

<!-- 中文说明：相关资源链接 -->
- [Skill Creator](https://skill-creator.app) - 从仓库历史生成本能
- [Homunculus](https://github.com/humanplane/homunculus) - v2架构的灵感来源
- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - 持续学习部分

---

<!-- 中文说明：基于本能的学习：一次一个观察，教会Claude你的模式 -->
*基于本能的学习：一次一个观察，教会Claude你的模式。*
