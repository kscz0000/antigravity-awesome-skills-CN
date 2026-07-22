---
title: 使用 VACUUM 和 ANALYZE 维护表统计信息
impact: MEDIUM
impactDescription: 准确的统计信息带来 2-10 倍更好的查询计划
tags: vacuum, analyze, statistics, maintenance, autovacuum
---

## 使用 VACUUM 和 ANALYZE 维护表统计信息

过时的统计信息导致查询规划器做出糟糕的决策。VACUUM 回收空间，ANALYZE 更新统计信息。

**错误做法（统计信息过时）：**

```sql
-- 表有 100 万行但统计信息显示 1000 行
-- 查询规划器选择错误策略
explain select * from orders where status = 'pending';
-- 显示：Seq Scan（因为统计信息显示小表）
-- 实际：Index Scan 会快得多
```

**正确做法（维护最新统计信息）：**

```sql
-- 大量数据变更后手动分析
analyze orders;

-- 分析 WHERE 子句中使用的特定列
analyze orders (status, created_at);

-- 检查表上次分析时间
select
  relname,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
from pg_stat_user_tables
order by last_analyze nulls first;
```

高负载表的自动清理调优：

```sql
-- 增加高频变更表的频率
alter table orders set (
  autovacuum_vacuum_scale_factor = 0.05,     -- 5% 死元组时清理（默认 20%）
  autovacuum_analyze_scale_factor = 0.02     -- 2% 变更时分析（默认 10%）
);

-- 检查自动清理状态
select * from pg_stat_progress_vacuum;
```

参考：[VACUUM](https://supabase.com/docs/guides/database/database-size#vacuum-operations)
