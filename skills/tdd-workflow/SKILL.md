---
name: tdd-workflow
description: 编写新功能、修复bug或重构代码时使用此技能。强制执行测试驱动开发，要求80%以上的覆盖率，包括单元测试、集成测试和端到端测试。
---

# 测试驱动开发工作流 (Test-Driven Development Workflow)

<!-- 中文说明：此技能确保所有代码开发遵循TDD原则，并具有全面的测试覆盖 -->

本技能确保所有代码开发遵循TDD原则，并具有全面的测试覆盖。

## 何时激活 (When to Activate)

<!-- 中文说明：以下情况应该激活此技能 -->
- 编写新功能或新功能时
- 修复bug或问题时
- 重构现有代码时
- 添加API端点时
- 创建新组件时

## 核心原则 (Core Principles)

### 1. 测试先于代码 (Tests BEFORE Code)
<!-- 中文说明：永远先写测试，然后实现代码让测试通过 -->
永远先写测试，然后实现代码让测试通过。

### 2. 覆盖率要求 (Coverage Requirements)
<!-- 中文说明：最低覆盖率要求 -->
- 最低80%覆盖率（单元 + 集成 + E2E）
- 所有边界情况都要覆盖
- 错误场景要测试
- 边界条件要验证

### 3. 测试类型 (Test Types)

#### 单元测试 (Unit Tests)
<!-- 中文说明：测试独立的函数和组件 -->
- 独立的函数和工具
- 组件逻辑
- 纯函数
- 辅助函数和工具

#### 集成测试 (Integration Tests)
<!-- 中文说明：测试模块间的交互 -->
- API端点
- 数据库操作
- 服务交互
- 外部API调用

#### E2E测试 (E2E Tests - Playwright)
<!-- 中文说明：测试完整的用户流程 -->
- 关键用户流程
- 完整工作流
- 浏览器自动化
- UI交互

## TDD工作流步骤 (TDD Workflow Steps)

### 步骤1：编写用户旅程 (Step 1: Write User Journeys)
<!-- 中文说明：以用户故事形式描述功能需求 -->
```
作为一个[角色]，我想要[操作]，以便[收益]

示例：
作为一个用户，我想要语义化搜索市场，
以便即使没有精确关键词也能找到相关市场。
```

### 步骤2：生成测试用例 (Step 2: Generate Test Cases)
<!-- 中文说明：为每个用户旅程创建全面的测试用例 -->
为每个用户旅程，创建全面的测试用例：

```typescript
describe('语义搜索 (Semantic Search)', () => {
  it('为查询返回相关市场', async () => {
    // 测试实现
  })

  it('优雅处理空查询', async () => {
    // 测试边界情况
  })

  it('Redis不可用时回退到子字符串搜索', async () => {
    // 测试回退行为
  })

  it('按相似度分数排序结果', async () => {
    // 测试排序逻辑
  })
})
```

### 步骤3：运行测试（应该失败）(Step 3: Run Tests - They Should Fail)
<!-- 中文说明：测试应该失败，因为我们还没有实现 -->
```bash
npm test
# 测试应该失败 - 我们还没有实现
```

### 步骤4：实现代码 (Step 4: Implement Code)
<!-- 中文说明：编写最小代码使测试通过 -->
编写最小代码使测试通过：

```typescript
// 由测试引导的实现
export async function searchMarkets(query: string) {
  // 实现代码
}
```

### 步骤5：再次运行测试 (Step 5: Run Tests Again)
<!-- 中文说明：现在测试应该通过 -->
```bash
npm test
# 测试现在应该通过
```

### 步骤6：重构 (Step 6: Refactor)
<!-- 中文说明：在保持测试通过的同时改进代码质量 -->
在保持测试绿色的同时改进代码质量：
- 消除重复
- 改进命名
- 优化性能
- 增强可读性

### 步骤7：验证覆盖率 (Step 7: Verify Coverage)
<!-- 中文说明：确认达到80%以上的覆盖率 -->
```bash
npm run test:coverage
# 验证达到80%以上的覆盖率
```

## 测试模式 (Testing Patterns)

### 单元测试模式 (Unit Test Pattern - Jest/Vitest)
<!-- 中文说明：使用Jest或Vitest进行单元测试的示例 -->
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('按钮组件 (Button Component)', () => {
  it('使用正确的文本渲染', () => {
    render(<Button>点击我</Button>)
    expect(screen.getByText('点击我')).toBeInTheDocument()
  })

  it('点击时调用onClick', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>点击</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('disabled属性为true时禁用', () => {
    render(<Button disabled>点击</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API集成测试模式 (API Integration Test Pattern)
<!-- 中文说明：API端点集成测试示例 -->
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('成功返回市场列表', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('验证查询参数', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('优雅处理数据库错误', async () => {
    // 模拟数据库失败
    const request = new NextRequest('http://localhost/api/markets')
    // 测试错误处理
  })
})
```

### E2E测试模式 (E2E Test Pattern - Playwright)
<!-- 中文说明：使用Playwright进行端到端测试的示例 -->
```typescript
import { test, expect } from '@playwright/test'

test('用户可以搜索和过滤市场', async ({ page }) => {
  // 导航到市场页面
  await page.goto('/')
  await page.click('a[href="/markets"]')

  // 验证页面已加载
  await expect(page.locator('h1')).toContainText('市场')

  // 搜索市场
  await page.fill('input[placeholder="搜索市场"]', '选举')

  // 等待防抖和结果
  await page.waitForTimeout(600)

  // 验证搜索结果显示
  const results = page.locator('[data-testid="market-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })

  // 验证结果包含搜索词
  const firstResult = results.first()
  await expect(firstResult).toContainText('选举', { ignoreCase: true })

  // 按状态过滤
  await page.click('button:has-text("活跃")')

  // 验证过滤结果
  await expect(results).toHaveCount(3)
})

test('用户可以创建新市场', async ({ page }) => {
  // 先登录
  await page.goto('/creator-dashboard')

  // 填写市场创建表单
  await page.fill('input[name="name"]', '测试市场')
  await page.fill('textarea[name="description"]', '测试描述')
  await page.fill('input[name="endDate"]', '2025-12-31')

  // 提交表单
  await page.click('button[type="submit"]')

  // 验证成功消息
  await expect(page.locator('text=市场创建成功')).toBeVisible()

  // 验证重定向到市场页面
  await expect(page).toHaveURL(/\/markets\/test-market/)
})
```

## 测试文件组织 (Test File Organization)

<!-- 中文说明：推荐的测试文件目录结构 -->
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # 单元测试
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # 集成测试
└── e2e/
    ├── markets.spec.ts               # E2E测试
    ├── trading.spec.ts
    └── auth.spec.ts
```

## 模拟外部服务 (Mocking External Services)

### Supabase模拟 (Supabase Mock)
<!-- 中文说明：模拟Supabase数据库调用 -->
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: '测试市场' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### Redis模拟 (Redis Mock)
<!-- 中文说明：模拟Redis调用 -->
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

### OpenAI模拟 (OpenAI Mock)
<!-- 中文说明：模拟OpenAI API调用 -->
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // 模拟1536维嵌入向量
  ))
}))
```

## 测试覆盖率验证 (Test Coverage Verification)

### 运行覆盖率报告 (Run Coverage Report)
```bash
npm run test:coverage
```

### 覆盖率阈值 (Coverage Thresholds)
<!-- 中文说明：推荐的覆盖率阈值配置 -->
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## 常见测试错误及避免方法 (Common Testing Mistakes to Avoid)

### 错误：测试实现细节 (Testing Implementation Details)
<!-- 中文说明：不要测试内部状态 -->
```typescript
// ❌ 错误：测试内部状态
expect(component.state.count).toBe(5)
```

### 正确：测试用户可见行为 (Test User-Visible Behavior)
<!-- 中文说明：测试用户看到的内容 -->
```typescript
// ✅ 正确：测试用户看到的内容
expect(screen.getByText('计数: 5')).toBeInTheDocument()
```

### 错误：脆弱的选择器 (Brittle Selectors)
<!-- 中文说明：容易破裂的选择器 -->
```typescript
// ❌ 错误：容易破裂
await page.click('.css-class-xyz')
```

### 正确：语义化选择器 (Semantic Selectors)
<!-- 中文说明：对变化有弹性的选择器 -->
```typescript
// ✅ 正确：对变化有弹性
await page.click('button:has-text("提交")')
await page.click('[data-testid="submit-button"]')
```

### 错误：没有测试隔离 (No Test Isolation)
<!-- 中文说明：测试相互依赖 -->
```typescript
// ❌ 错误：测试相互依赖
test('创建用户', () => { /* ... */ })
test('更新同一用户', () => { /* 依赖前一个测试 */ })
```

### 正确：独立测试 (Independent Tests)
<!-- 中文说明：每个测试设置自己的数据 -->
```typescript
// ✅ 正确：每个测试设置自己的数据
test('创建用户', () => {
  const user = createTestUser()
  // 测试逻辑
})

test('更新用户', () => {
  const user = createTestUser()
  // 更新逻辑
})
```

## 持续测试 (Continuous Testing)

### 开发时监听模式 (Watch Mode During Development)
<!-- 中文说明：文件变化时自动运行测试 -->
```bash
npm test -- --watch
# 文件变化时自动运行测试
```

### 预提交钩子 (Pre-Commit Hook)
<!-- 中文说明：每次提交前运行 -->
```bash
# 每次提交前运行
npm test && npm run lint
```

### CI/CD集成 (CI/CD Integration)
<!-- 中文说明：GitHub Actions配置示例 -->
```yaml
# GitHub Actions
- name: 运行测试 (Run Tests)
  run: npm test -- --coverage
- name: 上传覆盖率 (Upload Coverage)
  uses: codecov/codecov-action@v3
```

## 最佳实践 (Best Practices)

<!-- 中文说明：TDD最佳实践清单 -->
1. **先写测试** - 永远TDD
2. **每个测试一个断言** - 专注于单一行为
3. **描述性测试名称** - 解释测试内容
4. **安排-执行-断言** - 清晰的测试结构
5. **模拟外部依赖** - 隔离单元测试
6. **测试边界情况** - null、undefined、空值、大值
7. **测试错误路径** - 不仅仅是正常路径
8. **保持测试快速** - 单元测试每个<50ms
9. **测试后清理** - 无副作用
10. **审查覆盖率报告** - 识别缺口

## 成功指标 (Success Metrics)

<!-- 中文说明：TDD成功的衡量标准 -->
- 达到80%以上代码覆盖率
- 所有测试通过（绿色）
- 没有跳过或禁用的测试
- 测试执行快速（单元测试<30秒）
- E2E测试覆盖关键用户流程
- 测试在上线前捕获bug

---

<!-- 中文说明：记住测试是可选的，它们是安全网，支持自信重构、快速开发和生产可靠性 -->
**记住**：测试不是可选的。它们是安全网，支持自信重构、快速开发和生产可靠性。
