# Commit 命令

当用户要求提交代码时，严格遵循以下格式：

## Commit Message 格式

```
<类型>: <英文描述>

<类型>: <英文描述>

- <英文描述1>
- <英文描述2>

<类型>: <中文描述>

- <中文描述1>
- <中文描述2>
```

**注意：不要加 Co-Authored-By**

## 类型
- `feat` - 新功能
- `fix` - Bug 修复
- `refactor` - 重构
- `docs` - 文档更新
- `style` - 代码格式
- `test` - 测试相关
- `chore` - 构建/工具
- `perf` - 性能优化

## 示例

```
feat: add --skip-suppl option to skip GEO supplementary files

feat: add --skip-suppl option to skip GEO supplementary files

- Add skip_suppl parameter
- Add --skip-suppl command line option
- Remove debug logging

feat: 添加跳过GEO附件文件的选项

- 添加 skip_suppl 参数
- 添加 --skip-suppl 命令行选项
- 移除调试日志
```

## 执行步骤

1. 运行 `git status` 查看改动
2. 运行 `git diff` 查看具体变更
3. 分析变更内容，确定类型和描述
4. 标题纯英文，描述先英文后中文
5. 执行 `git add` 暂存文件
6. 执行 `git commit`（hook 会自动检查格式）
7. 推送到所有远程仓库
