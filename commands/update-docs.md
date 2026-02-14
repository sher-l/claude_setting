# Update Documentation - 更新文档命令

<!--
================================================================================
命令说明（中文）
================================================================================

用途：从真实来源同步文档。

工作流程：
1. 读取 package.json 的 scripts 部分
   - 生成脚本参考表
   - 包含注释中的描述

2. 读取 .env.example
   - 提取所有环境变量
   - 文档化用途和格式

3. 生成 docs/CONTRIB.md，包含：
   - 开发工作流
   - 可用脚本
   - 环境设置
   - 测试流程

4. 生成 docs/RUNBOOK.md，包含：
   - 部署流程
   - 监控和告警
   - 常见问题和修复
   - 回滚流程

5. 识别过时文档：
   - 查找90天以上未修改的文档
   - 列出以供手动审查

6. 显示差异摘要

真实来源：package.json 和 .env.example

================================================================================
-->

Sync documentation from source-of-truth:

1. Read package.json scripts section
   - Generate scripts reference table
   - Include descriptions from comments

2. Read .env.example
   - Extract all environment variables
   - Document purpose and format

3. Generate docs/CONTRIB.md with:
   - Development workflow
   - Available scripts
   - Environment setup
   - Testing procedures

4. Generate docs/RUNBOOK.md with:
   - Deployment procedures
   - Monitoring and alerts
   - Common issues and fixes
   - Rollback procedures

5. Identify obsolete documentation:
   - Find docs not modified in 90+ days
   - List for manual review

6. Show diff summary

Single source of truth: package.json and .env.example
