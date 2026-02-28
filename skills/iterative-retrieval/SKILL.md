---
name: iterative-retrieval
description: 渐进式上下文检索模式，用于解决子代理上下文问题 - 子代理在开始工作之前不知道需要什么上下文
---

# 迭代检索模式 (Iterative Retrieval Pattern)

<!-- 中文说明：解决多代理工作流中的"上下文问题"，子代理在开始工作之前不知道需要什么上下文 -->

解决多代理工作流中的"上下文问题"，子代理在开始工作之前不知道需要什么上下文。

## 问题 (The Problem)

<!-- 中文说明：子代理的上下文限制问题 -->
子代理在有限的上下文中被生成。他们不知道：
- 哪些文件包含相关代码
- 代码库中存在哪些模式
- 项目使用什么术语

标准方法会失败：
- **发送所有内容**：超出上下文限制
- **什么都不发送**：代理缺乏关键信息
- **猜测需要什么**：经常猜错

## 解决方案：迭代检索 (The Solution: Iterative Retrieval)

<!-- 中文说明：4阶段循环渐进式优化上下文 -->
一个4阶段循环，渐进式优化上下文：

```
┌─────────────────────────────────────────────┐
│                                             │
│   ┌──────────┐      ┌──────────┐            │
│   │  分发    │─────▶│  评估    │            │
│   │ DISPATCH │      │ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   循环   │◀─────│  优化    │            │
│   │   LOOP   │      │  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        最多3个循环，然后继续                  │
└─────────────────────────────────────────────┘
```

### 阶段1：分发 (Phase 1: DISPATCH)

<!-- 中文说明：初始广泛查询收集候选文件 -->
初始广泛查询以收集候选文件：

```javascript
// 从高级意图开始
const initialQuery = {
  patterns: ['src/**/*.ts', 'lib/**/*.ts'],
  keywords: ['authentication', 'user', 'session'],
  excludes: ['*.test.ts', '*.spec.ts']
};

// 分发给检索代理
const candidates = await retrieveFiles(initialQuery);
```

### 阶段2：评估 (Phase 2: EVALUATE)

<!-- 中文说明：评估检索内容的相关性 -->
评估检索内容的相关性：

```javascript
function evaluateRelevance(files, task) {
  return files.map(file => ({
    path: file.path,
    relevance: scoreRelevance(file.content, task),
    reason: explainRelevance(file.content, task),
    missingContext: identifyGaps(file.content, task)
  }));
}
```

评分标准：
- **高 (0.8-1.0)**：直接实现目标功能
- **中 (0.5-0.7)**：包含相关模式或类型
- **低 (0.2-0.4)**：间接相关
- **无 (0-0.2)**：不相关，排除

### 阶段3：优化 (Phase 3: REFINE)

<!-- 中文说明：根据评估更新搜索条件 -->
根据评估更新搜索条件：

```javascript
function refineQuery(evaluation, previousQuery) {
  return {
    // 添加在高相关文件中发现的新模式
    patterns: [...previousQuery.patterns, ...extractPatterns(evaluation)],

    // 添加代码库中发现的术语
    keywords: [...previousQuery.keywords, ...extractKeywords(evaluation)],

    // 排除确认不相关的路径
    excludes: [...previousQuery.excludes, ...evaluation
      .filter(e => e.relevance < 0.2)
      .map(e => e.path)
    ],

    // 针对特定缺口
    focusAreas: evaluation
      .flatMap(e => e.missingContext)
      .filter(unique)
  };
}
```

### 阶段4：循环 (Phase 4: LOOP)

<!-- 中文说明：使用优化后的条件重复（最多3个循环） -->
使用优化后的条件重复（最多3个循环）：

```javascript
async function iterativeRetrieve(task, maxCycles = 3) {
  let query = createInitialQuery(task);
  let bestContext = [];

  for (let cycle = 0; cycle < maxCycles; cycle++) {
    const candidates = await retrieveFiles(query);
    const evaluation = evaluateRelevance(candidates, task);

    // 检查是否有足够的上下文
    const highRelevance = evaluation.filter(e => e.relevance >= 0.7);
    if (highRelevance.length >= 3 && !hasCriticalGaps(evaluation)) {
      return highRelevance;
    }

    // 优化并继续
    query = refineQuery(evaluation, query);
    bestContext = mergeContext(bestContext, highRelevance);
  }

  return bestContext;
}
```

## 实际示例 (Practical Examples)

### 示例1：Bug修复上下文 (Example 1: Bug Fix Context)

<!-- 中文说明：修复认证令牌过期bug的示例 -->
```
任务：修复认证令牌过期bug

循环1：
  分发：在src/**中搜索"token", "auth", "expiry"
  评估：找到auth.ts (0.9), tokens.ts (0.8), user.ts (0.3)
  优化：添加"refresh", "jwt"关键词；排除user.ts

循环2：
  分发：搜索优化后的术语
  评估：找到session-manager.ts (0.95), jwt-utils.ts (0.85)
  优化：足够的上下文（2个高相关文件）

结果：auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts
```

### 示例2：功能实现 (Example 2: Feature Implementation)

<!-- 中文说明：为API端点添加限流的示例 -->
```
任务：为API端点添加限流

循环1：
  分发：在routes/**中搜索"rate", "limit", "api"
  评估：无匹配 - 代码库使用"throttle"术语
  优化：添加"throttle", "middleware"关键词

循环2：
  分发：搜索优化后的术语
  评估：找到throttle.ts (0.9), middleware/index.ts (0.7)
  优化：需要路由器模式

循环3：
  分发：搜索"router", "express"模式
  评估：找到router-setup.ts (0.8)
  优化：足够的上下文

结果：throttle.ts, middleware/index.ts, router-setup.ts
```

## 与代理集成 (Integration with Agents)

<!-- 中文说明：在代理提示中使用 -->
在代理提示中使用：

```markdown
为此任务检索上下文时：
1. 从广泛的关键词搜索开始
2. 评估每个文件的相关性（0-1分）
3. 识别仍然缺失的上下文
4. 优化搜索条件并重复（最多3个循环）
5. 返回相关性>= 0.7的文件
```

## 最佳实践 (Best Practices)

<!-- 中文说明：迭代检索的最佳实践 -->
1. **从广泛开始，渐进式缩小** - 不要过度指定初始查询
2. **学习代码库术语** - 第一个循环通常揭示命名约定
3. **跟踪缺失什么** - 明确的缺口识别驱动优化
4. **在"足够好"时停止** - 3个高相关文件胜过10个平庸的
5. **自信地排除** - 低相关文件不会变得相关

## 相关资源 (Related)

<!-- 中文说明：相关资源链接 -->
- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - 子代理编排部分
- `continuous-learning` 技能 - 用于随时间改进的模式
- `~/.claude/agents/` 中的代理定义
