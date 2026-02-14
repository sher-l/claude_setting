---
description: 修复构建和类型错误，最小变更，不做架构修改。
---

# /build-fix 命令

快速修复构建错误，最小变更策略。

## 执行步骤

1. **收集所有错误**
```bash
npx tsc --noEmit
npm run build
```

2. **分类错误**
- 类型推断失败
- 缺失类型定义
- 导入/导出错误
- 配置错误
- 依赖问题

3. **按优先级修复**
- 阻塞构建：优先
- 类型错误：按顺序
- 警告：时间允许时

4. **最小变更原则**
- 添加缺失的类型注解
- 修复导入语句
- 添加null检查
- 最后手段才用类型断言

## 常见修复

### 类型推断失败
```typescript
// ❌ 错误
function add(x, y) { return x + y }

// ✓ 修复
function add(x: number, y: number): number { return x + y }
```

### Null错误
```typescript
// ❌ 错误
const name = user.name.toUpperCase()

// ✓ 修复
const name = user?.name?.toUpperCase()
```

### 导入错误
```typescript
// ❌ 错误
import { foo } from '@/lib/utils'

// ✓ 修复
import { foo } from '../lib/utils'
```

## 不应该做

❌ 重构无关代码
❌ 更改架构
❌ 添加新功能
❌ 优化性能

## 成功标准

- ✅ `npx tsc --noEmit` 通过
- ✅ `npm run build` 成功
- ✅ 无新错误
- ✅ 最小行数变更
