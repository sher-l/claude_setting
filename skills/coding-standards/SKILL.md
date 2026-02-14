---
name: coding-standards
description: 通用编码标准、最佳实践和模式，适用于TypeScript、JavaScript、React和Node.js开发。
---

# 编码标准与最佳实践 (Coding Standards & Best Practices)

<!-- 中文说明：适用于所有项目的通用编码标准 -->

适用于所有项目的通用编码标准。

## 代码质量原则 (Code Quality Principles)

### 1. 可读性优先 (Readability First)
<!-- 中文说明：代码被阅读的次数远多于被编写的次数 -->
- 代码被阅读的次数远多于被编写的次数
- 清晰的变量和函数名
- 自文档化代码优于注释
- 一致的格式

### 2. KISS原则 (Keep It Simple, Stupid)
<!-- 中文说明：保持简单，愚蠢 -->
- 最简单的可行解决方案
- 避免过度工程
- 不做过早优化
- 易于理解 > 聪明的代码

### 3. DRY原则 (Don't Repeat Yourself)
<!-- 中文说明：不要重复自己 -->
- 将通用逻辑提取到函数中
- 创建可复用组件
- 跨模块共享工具
- 避免复制粘贴编程

### 4. YAGNI原则 (You Aren't Gonna Need It)
<!-- 中文说明：你不会需要它 -->
- 不要在需要之前构建功能
- 避免投机性泛化
- 只在需要时增加复杂性
- 从简单开始，需要时重构

## TypeScript/JavaScript标准 (TypeScript/JavaScript Standards)

### 变量命名 (Variable Naming)

<!-- 中文说明：变量命名的正确与错误示例 -->
```typescript
// ✅ 好的做法：描述性名称
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// ❌ 不好的做法：不清楚的名称
const q = 'election'
const flag = true
const x = 1000
```

### 函数命名 (Function Naming)

<!-- 中文说明：函数命名的正确与错误示例 -->
```typescript
// ✅ 好的做法：动词-名词模式
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// ❌ 不好的做法：不清楚或只有名词
async function market(id: string) { }
function similarity(a, b) { }
function email(e) { }
```

### 不可变模式（关键）(Immutability Pattern - CRITICAL)

<!-- 中文说明：永远使用展开运算符，永远不要直接修改 -->
```typescript
// ✅ 永远使用展开运算符
const updatedUser = {
  ...user,
  name: '新名字'
}

const updatedArray = [...items, newItem]

// ❌ 永远不要直接修改
user.name = '新名字'  // 错误
items.push(newItem)     // 错误
```

### 错误处理 (Error Handling)

<!-- 中文说明：正确的错误处理示例 -->
```typescript
// ✅ 好的做法：全面的错误处理
async function fetchData(url: string) {
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('获取失败:', error)
    throw new Error('获取数据失败')
  }
}

// ❌ 不好的做法：没有错误处理
async function fetchData(url) {
  const response = await fetch(url)
  return response.json()
}
```

### Async/Await最佳实践 (Async/Await Best Practices)

<!-- 中文说明：并行执行优于不必要的顺序执行 -->
```typescript
// ✅ 好的做法：尽可能并行执行
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// ❌ 不好的做法：不必要时的顺序执行
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

### 类型安全 (Type Safety)

<!-- 中文说明：正确的类型定义示例 -->
```typescript
// ✅ 好的做法：正确的类型
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> {
  // 实现
}

// ❌ 不好的做法：使用'any'
function getMarket(id: any): Promise<any> {
  // 实现
}
```

## React最佳实践 (React Best Practices)

### 组件结构 (Component Structure)

<!-- 中文说明：带类型的功能组件示例 -->
```typescript
// ✅ 好的做法：带类型的功能组件
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}

// ❌ 不好的做法：没有类型，结构不清楚
export function Button(props) {
  return <button onClick={props.onClick}>{props.children}</button>
}
```

### 自定义Hook (Custom Hooks)

<!-- 中文说明：可复用的自定义Hook示例 -->
```typescript
// ✅ 好的做法：可复用的自定义Hook
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// 使用
const debouncedQuery = useDebounce(searchQuery, 500)
```

### 状态管理 (State Management)

<!-- 中文说明：正确的状态更新方式 -->
```typescript
// ✅ 好的做法：正确的状态更新
const [count, setCount] = useState(0)

// 基于前一个状态的功能更新
setCount(prev => prev + 1)

// ❌ 不好的做法：直接状态引用
setCount(count + 1)  // 在异步场景中可能是陈旧的
```

### 条件渲染 (Conditional Rendering)

<!-- 中文说明：清晰的条件渲染示例 -->
```typescript
// ✅ 好的做法：清晰的条件渲染
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}

// ❌ 不好的做法：三元运算符地狱
{isLoading ? <Spinner /> : error ? <ErrorMessage error={error} /> : data ? <DataDisplay data={data} /> : null}
```

## API设计标准 (API Design Standards)

### REST API约定 (REST API Conventions)

<!-- 中文说明：RESTful API端点命名约定 -->
```
GET    /api/markets              # 列出所有市场
GET    /api/markets/:id          # 获取特定市场
POST   /api/markets              # 创建新市场
PUT    /api/markets/:id          # 更新市场（完整）
PATCH  /api/markets/:id          # 更新市场（部分）
DELETE /api/markets/:id          # 删除市场

# 查询参数用于过滤
GET /api/markets?status=active&limit=10&offset=0
```

### 响应格式 (Response Format)

<!-- 中文说明：一致的响应结构 -->
```typescript
// ✅ 好的做法：一致的响应结构
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}

// 成功响应
return NextResponse.json({
  success: true,
  data: markets,
  meta: { total: 100, page: 1, limit: 10 }
})

// 错误响应
return NextResponse.json({
  success: false,
  error: '无效请求'
}, { status: 400 })
```

### 输入验证 (Input Validation)

<!-- 中文说明：使用zod进行模式验证 -->
```typescript
import { z } from 'zod'

// ✅ 好的做法：模式验证
const CreateMarketSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().min(1).max(2000),
  endDate: z.string().datetime(),
  categories: z.array(z.string()).min(1)
})

export async function POST(request: Request) {
  const body = await request.json()

  try {
    const validated = CreateMarketSchema.parse(body)
    // 使用验证后的数据继续
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        error: '验证失败',
        details: error.errors
      }, { status: 400 })
    }
  }
}
```

## 文件组织 (File Organization)

### 项目结构 (Project Structure)

<!-- 中文说明：推荐的项目目录结构 -->
```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API路由
│   ├── markets/           # 市场页面
│   └── (auth)/           # 认证页面（路由组）
├── components/            # React组件
│   ├── ui/               # 通用UI组件
│   ├── forms/            # 表单组件
│   └── layouts/          # 布局组件
├── hooks/                # 自定义React Hook
├── lib/                  # 工具和配置
│   ├── api/             # API客户端
│   ├── utils/           # 辅助函数
│   └── constants/       # 常量
├── types/                # TypeScript类型
└── styles/              # 全局样式
```

### 文件命名 (File Naming)

<!-- 中文说明：文件命名约定 -->
```
components/Button.tsx          # 组件使用PascalCase
hooks/useAuth.ts              # Hook使用camelCase带'use'前缀
lib/formatDate.ts             # 工具使用camelCase
types/market.types.ts         # 类型文件使用camelCase带.types后缀
```

## 注释与文档 (Comments & Documentation)

### 何时注释 (When to Comment)

<!-- 中文说明：解释为什么，而不是做什么 -->
```typescript
// ✅ 好的做法：解释为什么，而不是做什么
// 使用指数退避避免在故障期间压垮API
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)

// 为了大数组的性能，故意使用变异
items.push(newItem)

// ❌ 不好的做法：陈述显而易见的内容
// 将计数器加1
count++

// 将名称设置为用户的名称
name = user.name
```

### 公共API的JSDoc (JSDoc for Public APIs)

<!-- 中文说明：公共API应该有完整的JSDoc文档 -->
```typescript
/**
 * 使用语义相似度搜索市场。
 *
 * @param query - 自然语言搜索查询
 * @param limit - 最大结果数（默认：10）
 * @returns 按相似度分数排序的市场数组
 * @throws {Error} 如果OpenAI API失败或Redis不可用
 *
 * @example
 * ```typescript
 * const results = await searchMarkets('选举', 5)
 * console.log(results[0].name) // "特朗普对拜登"
 * ```
 */
export async function searchMarkets(
  query: string,
  limit: number = 10
): Promise<Market[]> {
  // 实现
}
```

## 性能最佳实践 (Performance Best Practices)

### 记忆化 (Memoization)

<!-- 中文说明：使用useMemo和useCallback优化性能 -->
```typescript
import { useMemo, useCallback } from 'react'

// ✅ 好的做法：记忆化昂贵计算
const sortedMarkets = useMemo(() => {
  return markets.sort((a, b) => b.volume - a.volume)
}, [markets])

// ✅ 好的做法：记忆化回调
const handleSearch = useCallback((query: string) => {
  setSearchQuery(query)
}, [])
```

### 懒加载 (Lazy Loading)

<!-- 中文说明：懒加载重型组件 -->
```typescript
import { lazy, Suspense } from 'react'

// ✅ 好的做法：懒加载重型组件
const HeavyChart = lazy(() => import('./HeavyChart'))

export function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart />
    </Suspense>
  )
}
```

### 数据库查询 (Database Queries)

<!-- 中文说明：只选择需要的列 -->
```typescript
// ✅ 好的做法：只选择需要的列
const { data } = await supabase
  .from('markets')
  .select('id, name, status')
  .limit(10)

// ❌ 不好的做法：选择所有
const { data } = await supabase
  .from('markets')
  .select('*')
```

## 测试标准 (Testing Standards)

### 测试结构（AAA模式）(Test Structure - AAA Pattern)

<!-- 中文说明：安排-执行-断言模式 -->
```typescript
test('正确计算相似度', () => {
  // 安排 (Arrange)
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // 执行 (Act)
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // 断言 (Assert)
  expect(similarity).toBe(0)
})
```

### 测试命名 (Test Naming)

<!-- 中文说明：描述性的测试名称 -->
```typescript
// ✅ 好的做法：描述性的测试名称
test('当没有市场匹配查询时返回空数组', () => { })
test('当OpenAI API密钥缺失时抛出错误', () => { })
test('当Redis不可用时回退到子字符串搜索', () => { })

// ❌ 不好的做法：模糊的测试名称
test('工作', () => { })
test('测试搜索', () => { })
```

## 代码异味检测 (Code Smell Detection)

<!-- 中文说明：注意这些反模式 -->
注意这些反模式：

### 1. 过长的函数 (Long Functions)
```typescript
// ❌ 不好的做法：函数超过50行
function processMarketData() {
  // 100行代码
}

// ✅ 好的做法：拆分成更小的函数
function processMarketData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}
```

### 2. 深层嵌套 (Deep Nesting)
```typescript
// ❌ 不好的做法：5层以上嵌套
if (user) {
  if (user.isAdmin) {
    if (market) {
      if (market.isActive) {
        if (hasPermission) {
          // 做某事
        }
      }
    }
  }
}

// ✅ 好的做法：早返回
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return

// 做某事
```

### 3. 魔法数字 (Magic Numbers)
```typescript
// ❌ 不好的做法：未解释的数字
if (retryCount > 3) { }
setTimeout(callback, 500)

// ✅ 好的做法：命名常量
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500

if (retryCount > MAX_RETRIES) { }
setTimeout(callback, DEBOUNCE_DELAY_MS)
```

<!-- 中文说明：代码质量不可妥协。清晰、可维护的代码支持快速开发和自信重构 -->
**记住**：代码质量不可妥协。清晰、可维护的代码支持快速开发和自信重构。
