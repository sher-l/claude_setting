# 全局 Claude 配置
# 此配置对所有项目生效

## 🤖 核心行为准则

### 绝对禁止
- ❌ 质疑用户的陈述（如有不同，立即询问确认）
- ❌ 自己推测环境信息
- ❌ 说"你可能记错了"，然后自行推测。如果觉得用户错了那么应该询问确认

### 任务执行前检查
- 理解用户需求，不明确时提问
- 确认文件路径和命名规范
- 阅读项目相关文档（如存在）

### 问题处理时限

**防止死循环**：
- 语法错误：15分钟
- 逻辑错误：45分钟
- 性能问题：60分钟

**超时后**：
- 记录问题
- 暂时跳过
- 寻求替代方案

### Linus 三问（代码审查原则）⭐

> "Talk is cheap. Show me the code." — Linus Torvalds

**在提出任何代码修改之前，必须逐条回答以下三个问题：**

#### 1️⃣ 这是一个真实的问题吗？

- [ ] 错误是否实际发生过？有日志/报错截图吗？
- [ ] 是否只是"理论上可能出问题"的担忧？
- [ ] 是否只是为了"代码看起来更优雅"？
- [ ] 用户是否真的需要这个改动？

**❌ 不应修改的情况**：
- 理论上的边界情况（实际不会发生）
- 纯粹的代码风格偏好
- 过度防御性编程

#### 2️⃣ 有没有更简单的解决方案？

- [ ] 能否通过调整参数解决？
- [ ] 能否通过配置/文档说明解决？
- [ ] 改动是否最小化？只改必要的部分？
- [ ] 是否引入了不必要的抽象？

**✅ 好的工程**：
- 简单、直接、可维护
- 一眼能看懂意图
- 不为了"炫技"而增加复杂度

#### 3️⃣ 会不会破坏现有的东西？

- [ ] 现有API是否保持兼容？
- [ ] 现有配置文件是否仍然有效？
- [ ] 现有用户代码是否需要修改？
- [ ] 是否有充分的测试覆盖？

**⚠️ 向后兼容原则**：
- "We do not break userspace."
- 如必须破坏兼容，需要：
  1. 明确的迁移指南
  2. 充分的警告期
  3. 用户的明确同意

---

**决策流程**：
```
问题发生 → Linus三问 → 全部通过 → 才能修改代码
         ↓
    任一不通过 → 不修改 / 换方案
```

### 输出风格

**使用中文回复**
- 代码用Markdown格式化
- 文件名用反引号
- 简洁专业

---

## 全局技能库

所有项目都可以访问全局技能库：
- **位置**: `~/.claude/skills/`
- **来源**: Claude Scientific Skills (140+ 技能包)

### 常用技能参考

#### 数据分析与科学计算
- `pandas` - 数据处理
- `numpy` - 数值计算
- `matplotlib` - 数据可视化
- `seaborn` - 统计可视化
- `scipy` - 科学计算
- `scikit-learn` - 机器学习
- `statsmodels` - 统计建模

#### 生物信息学
- `biopython` - 分子生物学工具包
- `bioservices` - 生物信息学服务接口
- `gene-database` - 基因数据库查询
- `uniprot-database` - 蛋白质数据库
- `geo-database` - 基因表达数据

#### 临床与医学
- `clinical-reports` - 临床报告生成
- `clinical-decision-support` - 临床决策支持
- `pubmed-database` - 医学文献查询

#### 文献与写作
- `literature-review` - 系统文献综述
- `citation-management` - 文献管理
- `scientific-writing` - 科技写作

查看完整技能列表：
```bash
ls ~/.claude/skills/
```

---

## 全局编码规范

### Python
- 使用 `snake_case` 命名
- 添加类型提示
- 编写 docstrings
- 使用 `with` 语句处理文件
- 优先使用列表推导式

### R 语言

#### 1. 包加载
```r
suppressPackageStartupMessages({
  library(optparse)
  library(data.table)
  library(tidyverse)
  library(dplyr)
  library(qs2)
})
```

#### 2. 设置镜像
```r
options(scipen = 5)
options(BioC_mirror="https://mirrors.tuna.tsinghua.edu.cn/bioconductor")
options("repos"=c(CRAN="https://mirrors.tuna.tsinghua.edu.cn/CRAN"))
```

#### 3. 数据读取
**优先使用 `data.table::fread()`**：
```r
data <- fread("file.csv", data.table = FALSE)
```
**避免使用**：`read.csv()`, `read.delim()`, `read.table()`

#### 4. 数据保存
```r
# 保存为CSV
fwrite(data, "output.csv")

# 保存为RDS
saveRDS(data, "output.rds")

# 使用qs2缓存
qs_save(data, cache_file)
data <- qs_read(cache_file)
```

#### 5. 编码风格
- 函数命名：`snake_case`
- 管道操作：`%>%`
- 章节分隔：`# ----`
- 使用 `cat()` 输出，不是 `message()`

#### 6. 文件组织
```
project_name/
├── script_name.R           # 主脚本
├── data/                   # 数据
├── output/                 # 输出
└── cache/                  # 缓存
```

---

---

## 模块化规则

详细规则文件位于 `~/.claude/rules/` 目录：

| 规则文件 | 内容 |
|---------|------|
| `security.md` | 安全检查清单、敏感信息管理 |
| `coding-style.md` | 不可变性、文件组织、错误处理 |
| `testing.md` | TDD 工作流、80% 覆盖率要求 |
| `git-workflow.md` | 提交格式、PR 流程、分支策略 |
| `performance.md` | 模型选择、上下文管理、缓存策略 |
| `agents.md` | 代理调度原则、并行执行 |
| `hooks.md` | Hook 系统、最佳实践 |
| `patterns.md` | 设计模式、API 响应格式 |

**这些规则会自动被 Claude Code 加载并遵循。**

---

## 可用代理

位于 `~/.claude/agents/`，用于复杂任务委托：

| 代理 | 用途 | 何时使用 |
|------|------|---------|
| `planner` | 实现规划 | 复杂功能、重构 |
| `code-reviewer` | 代码审查 | 写完代码后自动使用 |
| `tdd-guide` | 测试驱动开发 | 新功能、bug修复 |
| `security-reviewer` | 安全分析 | 涉及用户输入、认证 |
| `build-error-resolver` | 构建错误修复 | 构建失败时 |
| `refactor-cleaner` | 死代码清理 | 代码维护 |

### 代理调度原则

**立即使用代理（无需用户确认）**：
1. 复杂功能请求 → **planner**
2. 代码刚写完 → **code-reviewer**
3. Bug修复/新功能 → **tdd-guide**
4. 构建失败 → **build-error-resolver**
5. 安全问题 → **security-reviewer**

**并行执行**：独立任务始终并行执行，不顺序等待。

---

## 可用命令

位于 `~/.claude/commands/`：

| 命令 | 用途 |
|------|------|
| `/plan` | 创建实现计划，等待确认后再执行 |
| `/code-review` | 全面安全和质量审查 |
| `/tdd` | 测试驱动开发工作流 |
| `/build-fix` | 快速修复构建错误 |

---

## Hooks 自动化检查

配置在 `~/.claude/settings.json` 中的自动化检查：

| Hook | 触发时机 | 功能 |
|------|---------|------|
| 文档文件阻止 | PreToolUse | 阻止创建随机 .md/.txt 文件 |
| push 提醒 | PreToolUse | git push 前提醒检查变更 |
| tmux 建议 | PreToolUse | 长时间命令建议使用 tmux |
| 大文件警告 | PreToolUse | 写入超过50KB时提醒拆分 |
| Python 语法检查 | PostToolUse | 编辑 .py 文件后检查语法 |
| R 语法检查 | PostToolUse | 编辑 .R 文件后检查语法 |
| 敏感信息检查 | PostToolUse | 检查代码中的硬编码密钥 |
| TODO/FIXME 检查 | PostToolUse | 提醒待办事项 |
| 调试输出检查 | PostToolUse | 检查 console.log/print |
| PR 链接显示 | PostToolUse | PR 创建后显示链接 |
| 未提交检查 | Stop | 会话结束检查未提交变更 |
| 调试语句检查 | Stop | 会话结束提醒检查调试语句 |

---

## 配置优先级

1. **项目配置** `{project}/CLAUDE.md` - 优先（主要配置）
2. **规则文件** `~/.claude/rules/*.md` - 补充规则
3. **全局配置**（此文件）- 补充（项目未覆盖时生效）

> 例如：如果项目 CLAUDE.md 定义了 Python 规范，则使用项目的；否则使用全局的 Python 规范。
