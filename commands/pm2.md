# PM2 Init - PM2 初始化命令

<!--
================================================================================
命令说明（中文）
================================================================================

用途：自动分析项目并生成 PM2 服务命令。

用法：$ARGUMENTS（在命令后跟参数）

工作流程：
1. 检查 PM2（如果缺失则通过 npm install -g pm2 安装）
2. 扫描项目识别服务（frontend/backend/database）
3. 生成配置文件和独立命令文件

服务检测：
| 类型 | 检测方法 | 默认端口 |
|------|----------|----------|
| Vite | vite.config.* | 5173 |
| Next.js | next.config.* | 3000 |
| Nuxt | nuxt.config.* | 3000 |
| CRA | react-scripts in package.json | 3000 |
| Express/Node | server/backend/api 目录 + package.json | 3000 |
| FastAPI/Flask | requirements.txt / pyproject.toml | 8000 |
| Go | go.mod / main.go | 8080 |

端口检测优先级：用户指定 > .env > 配置文件 > 脚本参数 > 默认端口

生成的文件：
- ecosystem.config.cjs - PM2 配置
- {backend}/start.cjs - Python 包装脚本（如适用）
- .claude/commands/pm2-*.md - 各种 PM2 命令

Windows 配置重要说明：
- 必须使用 .cjs 扩展名
- 需要指定 Node.js 解释器路径
- Python 服务需要 Node.js 包装脚本

关键规则：
1. 配置文件：ecosystem.config.cjs（不是 .js）
2. Node.js：直接指定 bin 路径 + 解释器
3. Python：Node.js 包装脚本 + windowsHide: true
4. 打开新窗口：start wt.exe -d "{path}" pwsh -NoExit -c "command"
5. 最小内容：每个命令文件只有1-2行描述 + bash 块
6. 直接执行：不需要 AI 解析，只需运行 bash 命令

初始化后操作：
1. 扫描项目服务
2. 生成 ecosystem.config.cjs
3. 为 Python 服务生成 {backend}/start.cjs
4. 在 .claude/commands/ 生成命令文件
5. 在 .claude/scripts/ 生成脚本文件
6. 更新项目 CLAUDE.md 添加 PM2 信息
7. 显示完成摘要和终端命令

================================================================================
-->

Auto-analyze project and generate PM2 service commands.

**Command**: `$ARGUMENTS`

---

## Workflow

1. Check PM2 (install via `npm install -g pm2` if missing)
2. Scan project to identify services (frontend/backend/database)
3. Generate config files and individual command files

---

## Service Detection

| Type | Detection | Default Port |
|------|-----------|--------------|
| Vite | vite.config.* | 5173 |
| Next.js | next.config.* | 3000 |
| Nuxt | nuxt.config.* | 3000 |
| CRA | react-scripts in package.json | 3000 |
| Express/Node | server/backend/api directory + package.json | 3000 |
| FastAPI/Flask | requirements.txt / pyproject.toml | 8000 |
| Go | go.mod / main.go | 8080 |

**Port Detection Priority**: User specified > .env > config file > scripts args > default port

---

## Generated Files

```
project/
├── ecosystem.config.cjs              # PM2 config
├── {backend}/start.cjs               # Python wrapper (if applicable)
└── .claude/
    ├── commands/
    │   ├── pm2-all.md                # Start all + monit
    │   ├── pm2-all-stop.md           # Stop all
    │   ├── pm2-all-restart.md        # Restart all
    │   ├── pm2-{port}.md             # Start single + logs
    │   ├── pm2-{port}-stop.md        # Stop single
    │   ├── pm2-{port}-restart.md     # Restart single
    │   ├── pm2-logs.md               # View all logs
    │   └── pm2-status.md             # View status
    └── scripts/
        ├── pm2-logs-{port}.ps1       # Single service logs
        └── pm2-monit.ps1             # PM2 monitor
```

---

## Windows Configuration (IMPORTANT)

### ecosystem.config.cjs

**Must use `.cjs` extension**

```javascript
module.exports = {
  apps: [
    // Node.js (Vite/Next/Nuxt)
    {
      name: 'project-3000',
      cwd: './packages/web',
      script: 'node_modules/vite/bin/vite.js',
      args: '--port 3000',
      interpreter: 'C:/Program Files/nodejs/node.exe',
      env: { NODE_ENV: 'development' }
    },
    // Python
    {
      name: 'project-8000',
      cwd: './backend',
      script: 'start.cjs',
      interpreter: 'C:/Program Files/nodejs/node.exe',
      env: { PYTHONUNBUFFERED: '1' }
    }
  ]
}
```

**Framework script paths:**

| Framework | script | args |
|-----------|--------|------|
| Vite | `node_modules/vite/bin/vite.js` | `--port {port}` |
| Next.js | `node_modules/next/dist/bin/next` | `dev -p {port}` |
| Nuxt | `node_modules/nuxt/bin/nuxt.mjs` | `dev --port {port}` |
| Express | `src/index.js` or `server.js` | - |

### Python Wrapper Script (start.cjs)

```javascript
const { spawn } = require('child_process');
const proc = spawn('python', ['-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'], {
  cwd: __dirname, stdio: 'inherit', windowsHide: true
});
proc.on('close', (code) => process.exit(code));
```

---

## Command File Templates (Minimal Content)

### pm2-all.md (Start all + monit)
```markdown
Start all services and open PM2 monitor.
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 start ecosystem.config.cjs && start wt.exe -d "{PROJECT_ROOT}" pwsh -NoExit -c "pm2 monit"
\`\`\`
```

### pm2-all-stop.md
```markdown
Stop all services.
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 stop all
\`\`\`
```

### pm2-all-restart.md
```markdown
Restart all services.
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 restart all
\`\`\`
```

### pm2-{port}.md (Start single + logs)
```markdown
Start {name} ({port}) and open logs.
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 start ecosystem.config.cjs --only {name} && start wt.exe -d "{PROJECT_ROOT}" pwsh -NoExit -c "pm2 logs {name}"
\`\`\`
```

### pm2-{port}-stop.md
```markdown
Stop {name} ({port}).
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 stop {name}
\`\`\`
```

### pm2-{port}-restart.md
```markdown
Restart {name} ({port}).
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 restart {name}
\`\`\`
```

### pm2-logs.md
```markdown
View all PM2 logs.
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 logs
\`\`\`
```

### pm2-status.md
```markdown
View PM2 status.
\`\`\`bash
cd "{PROJECT_ROOT}" && pm2 status
\`\`\`
```

### PowerShell Scripts (pm2-logs-{port}.ps1)
```powershell
Set-Location "{PROJECT_ROOT}"
pm2 logs {name}
```

### PowerShell Scripts (pm2-monit.ps1)
```powershell
Set-Location "{PROJECT_ROOT}"
pm2 monit
```

---

## Key Rules

1. **Config file**: `ecosystem.config.cjs` (not .js)
2. **Node.js**: Specify bin path directly + interpreter
3. **Python**: Node.js wrapper script + `windowsHide: true`
4. **Open new window**: `start wt.exe -d "{path}" pwsh -NoExit -c "command"`
5. **Minimal content**: Each command file has only 1-2 lines description + bash block
6. **Direct execution**: No AI parsing needed, just run the bash command

---

## Execute

Based on `$ARGUMENTS`, execute init:

1. Scan project for services
2. Generate `ecosystem.config.cjs`
3. Generate `{backend}/start.cjs` for Python services (if applicable)
4. Generate command files in `.claude/commands/`
5. Generate script files in `.claude/scripts/`
6. **Update project CLAUDE.md** with PM2 info (see below)
7. **Display completion summary** with terminal commands

---

## Post-Init: Update CLAUDE.md

After generating files, append PM2 section to project's `CLAUDE.md` (create if not exists):

```markdown
## PM2 Services

| Port | Name | Type |
|------|------|------|
| {port} | {name} | {type} |

**Terminal Commands:**
```bash
pm2 start ecosystem.config.cjs   # First time
pm2 start all                    # After first time
pm2 stop all / pm2 restart all
pm2 start {name} / pm2 stop {name}
pm2 logs / pm2 status / pm2 monit
pm2 save                         # Save process list
pm2 resurrect                    # Restore saved list
```
```

**Rules for CLAUDE.md update:**
- If PM2 section exists, replace it
- If not exists, append to end
- Keep content minimal and essential

---

## Post-Init: Display Summary

After all files generated, output:

```
## PM2 Init Complete

**Services:**
| Port | Name | Type |
|------|------|------|
| {port} | {name} | {type} |

**Claude Commands:** /pm2-all, /pm2-all-stop, /pm2-{port}, /pm2-{port}-stop, /pm2-logs, /pm2-status

**Terminal Commands:**
# First time (with config file)
pm2 start ecosystem.config.cjs && pm2 save

# After first time (simplified)
pm2 start all          # Start all
pm2 stop all           # Stop all
pm2 restart all        # Restart all
pm2 start {name}       # Start single
pm2 stop {name}        # Stop single
pm2 logs               # View logs
pm2 monit              # Monitor panel
pm2 resurrect          # Restore saved processes

**Tip:** Run `pm2 save` after first start to enable simplified commands.
```
