# Python 安全规范 (Python Security)

<!--
  【中文注释说明】
  本文件定义了 Python 代码的安全最佳实践。

  主要内容包括：
  1. 密钥管理 - 如何安全地处理敏感信息
  2. 安全扫描 - 使用工具进行静态安全分析

  来源: https://github.com/affaan-m/everything-claude-code/blob/master/rules/python/security.md
-->

> This file extends [common/security.md](../common/security.md) with Python specific content.
> 本文件扩展了通用安全规则，添加了 Python 特定的内容。

## Secret Management（密钥管理）

<!-- 【中文说明】
  永远不要在代码中硬编码敏感信息（如 API 密钥、密码等）。
  使用环境变量和 .env 文件来管理这些配置。
-->

```python
import os
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
# 【中文说明】load_dotenv() 会从项目根目录的 .env 文件中读取环境变量
load_dotenv()

# 从环境变量获取 API 密钥
# 【中文说明】使用 os.environ["KEY"] 会在键不存在时抛出 KeyError，
# 这是一种"快速失败"的策略，提醒你配置缺失
# 如果想要更温和的处理，可以使用 os.environ.get("KEY", "default_value")
api_key = os.environ["OPENAI_API_KEY"]  # Raises KeyError if missing
```

<!--
  【中文说明】.env 文件示例（不要提交到版本控制！）：

  ```
  OPENAI_API_KEY=sk-your-api-key-here
  DATABASE_URL=postgresql://user:password@localhost/db
  SECRET_KEY=your-secret-key
  ```

  记得将 .env 添加到 .gitignore 文件中！
-->

## Security Scanning（安全扫描）

- Use **bandit** for static security analysis:
  <!-- 【中文说明】使用 bandit 进行静态安全分析，它可以检测常见的安全问题 -->

  ```bash
  bandit -r src/
  ```
  <!-- 【中文说明】-r 表示递归扫描 src/ 目录下的所有 Python 文件 -->

<!--
  【中文补充】

  常见的安全检查工具：

  1. bandit - 专门针对 Python 的安全 linter
     pip install bandit
     bandit -r src/ -f json -o security_report.json  # 生成 JSON 报告

  2. safety - 检查依赖包的已知漏洞
     pip install safety
     safety check -r requirements.txt

  3. pip-audit - PyPA 官方的依赖审计工具
     pip install pip-audit
     pip-audit

  常见安全问题：
  - SQL 注入：使用参数化查询
  - XSS 攻击：对用户输入进行转义
  - 硬编码密钥：使用环境变量
  - 不安全的反序列化：避免 pickle，使用 JSON
-->

## Reference（参考资源）

See skill: `django-security` for Django-specific security guidelines (if applicable).
<!-- 【中文说明】如果使用 Django 框架，查看 django-security 技能获取 Django 特定的安全指南 -->
