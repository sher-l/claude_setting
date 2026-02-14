# 安全指南

## 提交前必须检查

每次提交代码前必须确认：
- [ ] 没有硬编码的敏感信息（API密钥、密码、令牌）
- [ ] 所有用户输入已验证
- [ ] SQL注入防护（使用参数化查询）
- [ ] XSS防护（HTML已净化）
- [ ] CSRF保护已启用
- [ ] 认证/授权已验证
- [ ] 所有端点有速率限制
- [ ] 错误信息不泄露敏感数据

## 敏感信息管理

- **绝不**在源代码中硬编码敏感信息
- **始终**使用环境变量或密钥管理器
- 启动时验证必需的密钥是否存在
- 轮换任何可能已暴露的密钥

## 安全响应协议

发现安全问题时：
1. **立即停止**
2. 使用 `security-reviewer` 代理进行审查
3. **先修复严重问题**再继续
4. 轮换所有已暴露的密钥
5. 审查整个代码库查找类似问题

## 常见安全陷阱

### 硬编码敏感信息
```python
# ❌ 错误
API_KEY = "sk-abc123..."

# ✅ 正确
import os
API_KEY = os.environ.get("API_KEY")
```

### SQL 注入
```python
# ❌ 错误
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 正确
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### 命令注入
```python
# ❌ 错误
os.system(f"ls {user_input}")

# ✅ 正确
import shlex
os.system(f"ls {shlex.quote(user_input)}")
```
