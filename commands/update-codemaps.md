# Update Codemaps - 更新代码地图命令

<!--
================================================================================
命令说明（中文）
================================================================================

用途：分析代码库结构并更新架构文档。

工作流程：
1. 扫描所有源文件的导入、导出和依赖关系

2. 生成精简的代码地图，格式如下：
   - codemaps/architecture.md - 整体架构
   - codemaps/backend.md - 后端结构
   - codemaps/frontend.md - 前端结构
   - codemaps/data.md - 数据模型和模式

3. 计算与上一版本的差异百分比

4. 如果变更 > 30%，在更新前请求用户批准

5. 为每个代码地图添加新鲜度时间戳

6. 将报告保存到 .reports/codemap-diff.txt

技术说明：
- 使用 TypeScript/Node.js 进行分析
- 关注高层结构，而非实现细节

================================================================================
-->

Analyze the codebase structure and update architecture documentation:

1. Scan all source files for imports, exports, and dependencies
2. Generate token-lean codemaps in the following format:
   - codemaps/architecture.md - Overall architecture
   - codemaps/backend.md - Backend structure
   - codemaps/frontend.md - Frontend structure
   - codemaps/data.md - Data models and schemas

3. Calculate diff percentage from previous version
4. If changes > 30%, request user approval before updating
5. Add freshness timestamp to each codemap
6. Save reports to .reports/codemap-diff.txt

Use TypeScript/Node.js for analysis. Focus on high-level structure, not implementation details.
