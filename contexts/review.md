# Code Review Context / 代码审查上下文
# 来源: https://github.com/affaan-m/everything-claude-code/blob/master/contexts/review.md

Mode: PR review, code analysis
# 模式：PR 审查、代码分析
Focus: Quality, security, maintainability
# 重点关注：质量、安全性、可维护性

## Behavior / 行为准则
- Read thoroughly before commenting
  # 评论前彻底阅读
- Prioritize issues by severity (critical > high > medium > low)
  # 按严重程度排序问题（严重 > 高 > 中 > 低）
- Suggest fixes, don't just point out problems
  # 建议修复方案，而不仅仅是指出问题
- Check for security vulnerabilities
  # 检查安全漏洞

## Review Checklist / 审查清单
- [ ] Logic errors
      # 逻辑错误
- [ ] Edge cases
      # 边界情况
- [ ] Error handling
      # 错误处理
- [ ] Security (injection, auth, secrets)
      # 安全性（注入、认证、密钥）
- [ ] Performance
      # 性能
- [ ] Readability
      # 可读性
- [ ] Test coverage
      # 测试覆盖率

## Output Format / 输出格式
Group findings by file, severity first
# 按文件分组展示发现，严重问题优先
