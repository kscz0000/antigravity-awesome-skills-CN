---
name: neon-postgres-egress-optimizer
description: 诊断并修复代码库中 Postgres 出站流量（网络数据传输）过高的问题。当用户提到数据库账单过高、数据传输费用异常、网络传输费用、出站流量激增、"Neon 账单怎么这么高"、"数据库费用跳涨"、SELECT * 优化、查询优化、egress 优化、Postgres 流量优化、出站数据量过大时使用此技能。
risk: unknown
source: https://github.com/neondatabase/agent-skills/tree/main/skills/neon-postgres-egress-optimizer
source_repo: neondatabase/agent-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/neondatabase/agent-skills/blob/main/LICENSE
---

# Postgres 出站流量优化器

## 何时使用

当需要诊断并修复代码库中 Postgres 出站流量（网络数据传输）过高的问题时使用此技能。当用户提到数据库账单过高、数据传输费用异常、网络传输费用、出站流量激增、"Neon 账单怎么这么高"、"数据库费用跳涨"、SELECT * 优化、查询优化等场景时触发。

引导用户诊断并修复应用侧查询模式导致的数据库出站数据传输过高问题。大多数高昂的出站流量账单，根源在于应用查询了远超实际使用量的数据。

## 第 1 步：诊断

识别哪些查询传输了最多的数据。主要工具是 `pg_stat_statements` 扩展。

### 检查 pg_stat_statements 是否可用

```sql
SELECT 1 FROM pg_stat_statements LIMIT 1;
```

如果报错，需要创建该扩展：

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

在 Neon 上，该扩展默认可用，但可能需要执行上述 CREATE EXTENSION 步骤。

### 处理空统计

Neon 的计算节点在缩容至零并重启时会清空统计数据。如果统计为空或计算节点刚被唤醒：

1. 重置统计以开启一个干净的测量窗口：`SELECT pg_stat_statements_reset();`
2. 让应用在具有代表性的流量下运行至少一小时。
3. 回来运行下面的诊断查询。

如果用户有生产数据库的统计数据，直接使用。如果无法访问生产统计，跳到第 2 步直接分析代码库——代码层面的模式通常足以定位最大的问题来源。

### 诊断查询

运行以下查询识别出站流量贡献最大的部分。重点关注返回行数多的查询、行宽度大的查询（含 JSONB、TEXT、BYTEA 列），以及调用频率极高的查询。

**返回总行数最多的查询：**

```sql
SELECT query, calls, rows AS total_rows, rows / calls AS avg_rows_per_call
FROM pg_stat_statements
WHERE calls > 0
ORDER BY rows DESC
LIMIT 10;
```

**每次执行返回行数最多的查询**（SELECT 范围过大、缺少分页）：

```sql
SELECT query, calls, rows AS total_rows, rows / calls AS avg_rows_per_call
FROM pg_stat_statements
WHERE calls > 0
ORDER BY avg_rows_per_call DESC
LIMIT 10;
```

**调用频率最高的查询**（适合加缓存的候选）：

```sql
SELECT query, calls, rows AS total_rows, rows / calls AS avg_rows_per_call
FROM pg_stat_statements
WHERE calls > 0
ORDER BY calls DESC
LIMIT 10;
```

**运行时间最长的查询**（不直接衡量出站流量，但有助于在流量激增时定位问题查询）：

```sql
SELECT query, calls, rows AS total_rows,
  round(total_exec_time::numeric, 2) AS total_exec_time_ms
FROM pg_stat_statements
WHERE calls > 0
ORDER BY total_exec_time DESC
LIMIT 10;
```

### 解读结果

按预估出站流量影响对发现进行排序：

- **高行数 + 宽行** = 出站流量最大。一条返回 1,000 行的查询，如果每行包含 50KB 的 JSONB 列，每次调用就传输约 50MB。
- **极高调用频率**，即使单次查询很小，累积起来也很可观。一条每天调用 50,000 次、每次返回 10 行的查询 = 每天 500,000 行。
- **结合表结构**识别哪些列是宽列。重点关注 JSONB、TEXT、BYTEA 和大字段 VARCHAR 列。

## 第 2 步：分析代码库

对第 1 步识别出的每条查询，或者在无法获取统计时对代码库中的每条数据库查询，检查：

- 是否只选择了响应所需的列？
- 是否返回有限行数（有 LIMIT/分页）？
- 调用频率是否高到值得加缓存？
- 是否查询了原始数据然后在应用代码中做聚合？
- 是否使用了会导致父表数据在子行中重复的 JOIN？

## 第 3 步：修复

针对发现的每个问题应用对应的修复方案。以下是最常见的出站流量反模式及其修复方法。

### 未使用的列（SELECT \*）

**问题：** 查询获取了所有列，但应用只使用了其中几列。大列（JSONB 大对象、TEXT 字段）通过网络传输后被丢弃。

**修改前：**

```sql
SELECT * FROM products;
```

**修改后：**

```sql
SELECT id, name, price, image_urls FROM products;
```

### 缺少分页

**问题：** 列表接口返回所有行，没有 LIMIT。这是一个无界的出站流量风险——表中每新增一行，每次请求的数据传输量都会增加。无论当前表大小如何，都应标记此问题。

这很容易被忽略，因为应用在小数据集下可能运行正常。但在规模增长后，一个无分页的接口返回 10,000 行，即使列宽适中，每天也可能传输数百兆字节。

**修改前：**

```sql
SELECT id, name, price FROM products;
```

**修改后：**

```sql
SELECT id, name, price FROM products
ORDER BY id
LIMIT 50 OFFSET 0;
```

添加分页时，检查消费方客户端是否已支持分页响应。如果未支持，选择合理的默认值并在 API 文档中说明分页参数。

### 静态数据上的高频查询

**问题：** 一条查询每天被调用数千次，但返回的数据很少变化。每次调用都从数据库传输相同的行。这种模式只能从 `pg_stat_statements` 中发现——代码本身看起来很正常。

查找相对其他查询调用次数异常高的查询。常见例子：配置表、分类列表、功能开关、用户角色定义。

**修复：** 在应用和数据库之间添加缓存层，避免每次请求都访问数据库。

### 应用侧聚合

**问题：** 应用从表中获取所有行，然后在应用代码中计算聚合值（平均值、计数、求和、分组）。完整的数据集通过网络传输，尽管结果只是一个小的汇总。

**修复：** 将聚合下推到 SQL 中。

**修改前：** 应用获取整张表，用循环或 `.reduce()` 在代码中聚合。

**修改后：**

```sql
SELECT p.category_id,
       AVG(r.rating) AS avg_rating,
       COUNT(r.id) AS review_count
FROM reviews r
INNER JOIN products p ON r.product_id = p.id
GROUP BY p.category_id;
```

### JOIN 导致的数据重复

**问题：** 宽父表与子表之间的 JOIN 会导致父表所有列在每一行子数据中重复。如果一个商品有 200 条评论，而商品行包含一个 50KB 的 JSONB 列，这个 JOIN 每次请求就传输 50KB x 200 = 约 10MB。

这与 SELECT \* 问题不同。即使只选择了需要的列，JOIN 仍然会在每一行子数据中重复父表数据。修复方式是结构性的：完全避免 JOIN。

**修改前：**

```sql
SELECT * FROM products
LEFT JOIN reviews ON reviews.product_id = products.id
WHERE products.id = 1;
```

**修改后（两条独立查询）：**

```sql
SELECT id, name, price, description, image_urls FROM products WHERE id = 1;
SELECT id, user_name, rating, body FROM reviews WHERE product_id = 1;
```

用两条查询替代一个 JOIN。商品数据只获取一次。评论数据只获取一次。没有重复。

## 第 4 步：验证

应用修复后：

1. **运行现有测试**确认没有引入问题。
2. **检查响应**——确保 API 仍然返回相同的数据结构。列选择和分页变更可能破坏依赖特定字段或完整结果集的客户端。
3. **度量改进效果**——如果 pg_stat_statements 数据可用，重置统计（`SELECT pg_stat_statements_reset();`），让流量运行一段时间，然后重新运行诊断查询对比修改前后。

## Neon 基础设施即代码（`neon.ts`）

上述修复减少的是**出站流量**（从 Postgres 传出的数据）。非生产环境的另一个主要成本杠杆是**计算资源**，可以通过 `neon.ts`——Neon 的基础设施即代码文件（完整参考见 `neon` 技能）——持久化地定义，使开发、预览和 CI 分支默认保持低成本，而不依赖逐分支的手动配置：

```bash
npm i @neon/config
```

```typescript
// neon.ts
import { defineConfig } from "@neon/config/v1";

export default defineConfig({
  branch: (branch) => {
    if (branch.exists || branch.isDefault) return {}; // don't touch prod
    return {
      ttl: "7d", // ephemeral branches auto-expire instead of accruing storage
      postgres: {
        computeSettings: {
          autoscalingLimitMinCu: 0.25, // scale to zero when idle
          autoscalingLimitMaxCu: 1, // cap autoscaling on throwaway branches
          suspendTimeout: "5m",
        },
      },
    };
  },
});
```

```bash
neon config apply   # apply to the current branch (neon deploy is an alias)
```

这是互补措施，而非替代方案：查询模式修复才是真正降低出站流量费用的手段，而这些设置则防止非生产环境的计算和存储悄悄推高同一张账单。因为 `neon checkout` 在创建分支时会应用该策略，新的开发/预览分支会自动继承低成本配置。

## 延伸阅读

- https://neon.com/docs/introduction/network-transfer.md
- https://neon.com/docs/introduction/cost-optimization.md

## 局限性

- 仅在任务明确匹配其上游产品或 API 范围时使用此技能。
- 在执行变更前，务必对照当前官方文档验证命令、API 行为、定价、配额、凭证和部署影响。
- 不要将生成的示例替代特定环境的测试、安全审查，或用户对破坏性/高成本操作的审批。
