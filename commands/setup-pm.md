---
description: Configure your preferred package manager (npm/pnpm/yarn/bun)
disable-model-invocation: true
---

# Package Manager Setup - 包管理器设置命令

<!--
================================================================================
命令说明（中文）
================================================================================

用途：配置项目的首选包管理器（npm/pnpm/yarn/bun）。

用法：
  node scripts/setup-package-manager.js --detect    # 检测当前包管理器
  node scripts/setup-package-manager.js --global pnpm   # 设置全局偏好
  node scripts/setup-package-manager.js --project bun   # 设置项目偏好
  node scripts/setup-package-manager.js --list      # 列出可用的包管理器

检测优先级（从高到低）：
1. 环境变量：CLAUDE_PACKAGE_MANAGER
2. 项目配置：.claude/package-manager.json
3. package.json：packageManager 字段
4. 锁文件：package-lock.json、yarn.lock、pnpm-lock.yaml、bun.lockb 的存在
5. 全局配置：~/.claude/package-manager.json
6. 回退：第一个可用的包管理器（pnpm > bun > yarn > npm）

配置文件位置：

全局配置：
~/.claude/package-manager.json
{
  "packageManager": "pnpm"
}

项目配置：
.claude/package-manager.json
{
  "packageManager": "bun"
}

package.json：
{
  "packageManager": "pnpm@8.6.0"
}

环境变量：
# Windows (PowerShell)
$env:CLAUDE_PACKAGE_MANAGER = "pnpm"

# macOS/Linux
export CLAUDE_PACKAGE_MANAGER=pnpm

运行检测：
node scripts/setup-package-manager.js --detect

================================================================================
-->

Configure your preferred package manager for this project or globally.

## Usage

```bash
# Detect current package manager
node scripts/setup-package-manager.js --detect

# Set global preference
node scripts/setup-package-manager.js --global pnpm

# Set project preference
node scripts/setup-package-manager.js --project bun

# List available package managers
node scripts/setup-package-manager.js --list
```

## Detection Priority

When determining which package manager to use, the following order is checked:

1. **Environment variable**: `CLAUDE_PACKAGE_MANAGER`
2. **Project config**: `.claude/package-manager.json`
3. **package.json**: `packageManager` field
4. **Lock file**: Presence of package-lock.json, yarn.lock, pnpm-lock.yaml, or bun.lockb
5. **Global config**: `~/.claude/package-manager.json`
6. **Fallback**: First available package manager (pnpm > bun > yarn > npm)

## Configuration Files

### Global Configuration
```json
// ~/.claude/package-manager.json
{
  "packageManager": "pnpm"
}
```

### Project Configuration
```json
// .claude/package-manager.json
{
  "packageManager": "bun"
}
```

### package.json
```json
{
  "packageManager": "pnpm@8.6.0"
}
```

## Environment Variable

Set `CLAUDE_PACKAGE_MANAGER` to override all other detection methods:

```bash
# Windows (PowerShell)
$env:CLAUDE_PACKAGE_MANAGER = "pnpm"

# macOS/Linux
export CLAUDE_PACKAGE_MANAGER=pnpm
```

## Run the Detection

To see current package manager detection results, run:

```bash
node scripts/setup-package-manager.js --detect
```
