---
name: skill-create
description: Analyze local git history to extract coding patterns and generate SKILL.md files. Local version of the Skill Creator GitHub App.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /skill-create - 本地技能生成命令

<!--
================================================================================
命令说明（中文）
================================================================================

用途：分析本地 Git 历史以提取编码模式并生成 SKILL.md 文件，
      教会 Claude 你的团队实践。

用法：
  /skill-create                    # 分析当前仓库
  /skill-create --commits 100      # 分析最近100次提交
  /skill-create --output ./skills  # 自定义输出目录
  /skill-create --instincts        # 同时为 continuous-learning-v2 生成本能

功能：
1. 解析 Git 历史 - 分析提交、文件变更和模式
2. 检测模式 - 识别重复的工作流和约定
3. 生成 SKILL.md - 创建有效的 Claude Code 技能文件
4. 可选创建本能 - 用于 continuous-learning-v2 系统

检测的模式类型：
| 模式 | 检测方法 |
|------|----------|
| 提交约定 | 提交消息正则匹配 (feat:, fix:, chore:) |
| 文件共变 | 总是一起变化的文件 |
| 工作流序列 | 重复的文件变更模式 |
| 架构 | 文件夹结构和命名约定 |
| 测试模式 | 测试文件位置、命名、覆盖率 |

输出格式示例：
```markdown
---
name: my-app-patterns
description: Coding patterns from my-app repository
version: 1.0.0
source: local-git-analysis
analyzed_commits: 150
---

# My App Patterns

## Commit Conventions
- `feat:` - 新功能
- `fix:` - Bug修复
- `chore:` - 维护任务

## Code Architecture
src/
├── components/     # React组件
├── hooks/          # 自定义钩子
├── utils/          # 工具函数
└── services/       # API和外部服务
```

GitHub App 集成：
对于高级功能（10k+提交、团队共享、自动PR），
可以使用 Skill Creator GitHub App：
https://github.com/apps/skill-creator

================================================================================
-->

Analyze your repository's git history to extract coding patterns and generate SKILL.md files that teach Claude your team's practices.

## Usage

```bash
/skill-create                    # Analyze current repo
/skill-create --commits 100      # Analyze last 100 commits
/skill-create --output ./skills  # Custom output directory
/skill-create --instincts        # Also generate instincts for continuous-learning-v2
```

## What It Does

1. **Parses Git History** - Analyzes commits, file changes, and patterns
2. **Detects Patterns** - Identifies recurring workflows and conventions
3. **Generates SKILL.md** - Creates valid Claude Code skill files
4. **Optionally Creates Instincts** - For the continuous-learning-v2 system

## Analysis Steps

### Step 1: Gather Git Data

```bash
# Get recent commits with file changes
git log --oneline -n ${COMMITS:-200} --name-only --pretty=format:"%H|%s|%ad" --date=short

# Get commit frequency by file
git log --oneline -n 200 --name-only | grep -v "^$" | grep -v "^[a-f0-9]" | sort | uniq -c | sort -rn | head -20

# Get commit message patterns
git log --oneline -n 200 | cut -d' ' -f2- | head -50
```

### Step 2: Detect Patterns

Look for these pattern types:

| Pattern | Detection Method |
|---------|-----------------|
| **Commit conventions** | Regex on commit messages (feat:, fix:, chore:) |
| **File co-changes** | Files that always change together |
| **Workflow sequences** | Repeated file change patterns |
| **Architecture** | Folder structure and naming conventions |
| **Testing patterns** | Test file locations, naming, coverage |

### Step 3: Generate SKILL.md

Output format:

```markdown
---
name: {repo-name}-patterns
description: Coding patterns extracted from {repo-name}
version: 1.0.0
source: local-git-analysis
analyzed_commits: {count}
---

# {Repo Name} Patterns

## Commit Conventions
{detected commit message patterns}

## Code Architecture
{detected folder structure and organization}

## Workflows
{detected repeating file change patterns}

## Testing Patterns
{detected test conventions}
```

### Step 4: Generate Instincts (if --instincts)

For continuous-learning-v2 integration:

```yaml
---
id: {repo}-commit-convention
trigger: "when writing a commit message"
confidence: 0.8
domain: git
source: local-repo-analysis
---

# Use Conventional Commits

## Action
Prefix commits with: feat:, fix:, chore:, docs:, test:, refactor:

## Evidence
- Analyzed {n} commits
- {percentage}% follow conventional commit format
```

## Example Output

Running `/skill-create` on a TypeScript project might produce:

```markdown
---
name: my-app-patterns
description: Coding patterns from my-app repository
version: 1.0.0
source: local-git-analysis
analyzed_commits: 150
---

# My App Patterns

## Commit Conventions

This project uses **conventional commits**:
- `feat:` - New features
- `fix:` - Bug fixes
- `chore:` - Maintenance tasks
- `docs:` - Documentation updates

## Code Architecture

```
src/
├── components/     # React components (PascalCase.tsx)
├── hooks/          # Custom hooks (use*.ts)
├── utils/          # Utility functions
├── types/          # TypeScript type definitions
└── services/       # API and external services
```

## Workflows

### Adding a New Component
1. Create `src/components/ComponentName.tsx`
2. Add tests in `src/components/__tests__/ComponentName.test.tsx`
3. Export from `src/components/index.ts`

### Database Migration
1. Modify `src/db/schema.ts`
2. Run `pnpm db:generate`
3. Run `pnpm db:migrate`

## Testing Patterns

- Test files: `__tests__/` directories or `.test.ts` suffix
- Coverage target: 80%+
- Framework: Vitest
```

## GitHub App Integration

For advanced features (10k+ commits, team sharing, auto-PRs), use the [Skill Creator GitHub App](https://github.com/apps/skill-creator):

- Install: [github.com/apps/skill-creator](https://github.com/apps/skill-creator)
- Comment `/skill-creator analyze` on any issue
- Receives PR with generated skills

## Related Commands

- `/instinct-import` - Import generated instincts
- `/instinct-status` - View learned instincts
- `/evolve` - Cluster instincts into skills/agents

---

*Part of [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)*
