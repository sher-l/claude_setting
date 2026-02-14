# 测试规范

## 最低测试覆盖率：80%

### 必需的测试类型：

1. **单元测试** - 独立函数、工具、组件
2. **集成测试** - API端点、数据库操作
3. **端到端测试** - 关键用户流程

## 测试驱动开发 (TDD)

**强制工作流**：
1. 先写测试（RED 红灯）
2. 运行测试 - 应该**失败**
3. 编写最小实现（GREEN 绿灯）
4. 运行测试 - 应该**通过**
5. 重构（IMPROVE 改进）
6. 验证覆盖率（80%+）

```
RED → GREEN → REFACTOR → REPEAT
```

## 测试命名规范

### Python (pytest)
```python
# 格式: test_<功能>_<场景>_<预期结果>
def test_divide_by_zero_raises_error():
    ...

def test_user_login_valid_credentials_returns_token():
    ...
```

### R (testthat)
```r
# 格式: test_<功能>_<场景>
test_that("divide by zero raises error", {
    ...
})

test_that("user login with valid credentials returns token", {
    ...
})
```

## 测试排查

测试失败时：
1. 检查测试隔离性
2. 验证 mock 是否正确
3. 修复实现，而非测试（除非测试确实错误）
4. 确保没有外部依赖（网络、文件系统）

## 测试最佳实践

### 独立性
- 每个测试应该独立运行
- 不依赖其他测试的执行顺序
- 使用 setup/teardown 清理状态

### 可读性
- 测试名称描述清楚测试内容
- 使用 Given-When-Then 模式
- 避免过度抽象

### 速度
- 单元测试应该快速（毫秒级）
- 集成测试可以稍慢
- E2E测试要精简，只覆盖关键路径

## 测试覆盖率例外

以下代码可以豁免 80% 覆盖率要求：
- 第三方库的包装器
- 简单的数据类/结构体
- 生成的代码（如 protobuf）
- 配置文件

但必须有明确的注释说明豁免原因。
