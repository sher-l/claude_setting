# Claude Code 配置备份

基于 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 定制的 Claude Code 配置。

## 目录结构

```
├── CLAUDE.md           # 全局配置文件
├── settings.json       # Claude Code 设置（需替换 YOUR_TOKEN_HERE）
├── agents/             # 专业代理
│   ├── architect.md
│   ├── planner.md
│   ├── code-reviewer.md
│   ├── python-reviewer.md
│   ├── security-reviewer.md
│   ├── tdd-guide.md
│   ├── build-error-resolver.md
│   └── refactor-cleaner.md
├── commands/           # 斜杠命令
│   ├── plan.md
│   ├── code-review.md
│   ├── python-review.md
│   ├── tdd.md
│   ├── build-fix.md
│   ├── verify.md
│   ├── test-coverage.md
│   └── refactor-clean.md
├── rules/              # 规则文件
│   ├── security.md
│   ├── coding-style.md
│   ├── testing.md
│   ├── git-workflow.md
│   ├── performance.md
│   ├── agents.md
│   ├── hooks.md
│   └── patterns.md
└── skills/             # 技能文件
    ├── python-patterns/
    ├── python-testing/
    └── backend-patterns/
```

## 安装

```bash
# 复制到 ~/.claude/ 目录
cp CLAUDE.md ~/.claude/
cp settings.json ~/.claude/  # 记得替换 YOUR_TOKEN_HERE
cp -r agents/* ~/.claude/agents/
cp -r commands/* ~/.claude/commands/
cp -r rules/* ~/.claude/rules/
cp -r skills/* ~/.claude/skills/
```

## 特色

- 中文注释和说明
- 针对 Python/R 优化
- 包含生物信息学相关技能库引用
- Linus 三问代码审查原则
