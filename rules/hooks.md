# Hooks 系统

## Hook 类型

- **PreToolUse**：工具执行前（验证、参数修改）
- **PostToolUse**：工具执行后（自动格式化、检查）
- **Stop**：会话结束时（最终验证）
- **SessionStart**：会话开始时（加载上下文）
- **SessionEnd**：会话结束时（保存状态）

## 自动接受权限

谨慎使用：
- 为可信、明确的计划启用
- 探索性工作时禁用
- 永不使用 dangerously-skip-permissions 标志
- 改为在 `~/.claude.json` 中配置 `allowedTools`

## Hook 最佳实践

### 1. 保持Hook轻量

Hook 应该快速执行，不阻塞用户：
- 避免长时间运行的操作
- 使用超时防止卡住
- 异步执行非关键检查

### 2. 提供清晰的反馈

```javascript
// ✓ 好：清晰的中文提示
console.error('[Hook] 警告：可能包含敏感信息')
console.error('[Hook] 文件：' + filePath)
console.error('[Hook] 请检查并使用环境变量')

// ✗ 差：模糊的英文
console.error('Warning: potential issue')
```

### 3. 使用返回码

- `exit(0)` 或正常退出：允许继续
- `exit(1)` 或错误：阻止操作

### 4. 条件匹配

```json
{
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.py$\"",
  "hooks": [...]
}
```

常用匹配模式：
- `tool == "Edit"` - 编辑操作
- `tool == "Write"` - 写入操作
- `tool == "Bash"` - 命令执行
- `tool_input.file_path matches "\\.py$"` - Python文件
- `tool_input.command matches "git push"` - Git推送

## TodoWrite 最佳实践

使用 TodoWrite 工具：
- 跟踪多步骤任务的进度
- 验证对指令的理解
- 启用实时指导
- 显示细粒度的实现步骤

待办事项列表可以揭示：
- 乱序步骤
- 缺失项目
- 多余的不必要项目
- 错误的粒度
- 误解的需求

## 常见 Hook 模式

### 阻止操作

```javascript
// 阻止并显示原因
console.error('[Hook] 已阻止：原因')
process.exit(1)
```

### 警告但允许

```javascript
// 警告但继续
console.error('[Hook] 警告：注意点')
console.log(stdin)  // 必须传递原始输入
```

### 修改输入

```javascript
// 读取、修改、输出
let data = JSON.parse(stdin)
data.tool_input.some_param = 'modified'
console.log(JSON.stringify(data))
```
