# 性能指南

## 模型选择

### 任务类型 vs 模型

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 简单查询 | Haiku | 快速、低成本 |
| 代码编写 | Sonnet | 平衡性能与质量 |
| 复杂推理 | Opus | 最高质量 |
| 代码审查 | Sonnet | 足够准确 |

### 上下文管理

**警告**：200k 上下文窗口可能因以下原因缩减到 70k：
- 启用过多 MCP 服务器
- 加载过多工具

**建议**：
- 配置 20-30 个 MCP 服务器
- 每个项目启用 <10 个
- 活动工具 <80 个

## 文件处理优化

### 大文件处理
```python
# ❌ 错误 - 一次性加载大文件
content = open("huge_file.txt").read()

# ✅ 正确 - 流式处理
with open("huge_file.txt") as f:
    for line in f:
        process(line)
```

### R 数据处理
```r
# ❌ 错误 - 慢
data <- read.csv("large.csv")

# ✅ 正确 - 快
library(data.table)
data <- fread("large.csv")
```

## 并行处理

### Python
```python
# 简单并行
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_item, items))
```

### R
```r
# 并行计算
library(parallel)
cl <- makeCluster(detectCores() - 1)
results <- parLapply(cl, items, process_item)
stopCluster(cl)
```

## 内存优化

### 及时释放
```python
# 处理完成后释放大对象
large_data = load_data()
result = process(large_data)
del large_data  # 显式释放
```

### 使用生成器
```python
# ❌ 错误 - 内存中保存所有结果
def get_all_results():
    return [expensive_operation(i) for i in range(10000)]

# ✅ 正确 - 按需生成
def get_all_results():
    for i in range(10000):
        yield expensive_operation(i)
```

## 数据库查询优化

- 使用索引
- 避免 SELECT *
- 使用分页
- 批量操作代替循环单条操作

## 缓存策略

### 适用场景
- 计算结果不经常变化
- 相同输入产生相同输出
- 计算成本高于缓存成本

### R 缓存示例
```r
# 使用 qs2 快速缓存
library(qs2)

cache_file <- "cache/processed_data.qs"
if (file.exists(cache_file)) {
    data <- qs_read(cache_file)
} else {
    data <- expensive_processing()
    qs_save(data, cache_file)
}
```
