---
title: 使用 VACUUM 和 ANALYZE 维护表统计信息
impact: MEDIUM
impactDescription: 准确的统计信息使查询计划提升 2-10 倍
tags: vacuum, analyze, statistics, maintenance, autovacuum
---

## 使用 VACUUM 和 ANALYZE 维护表统计信息

过时的统计信息会导致查询计划器做出错误决策。VACUUM 回收空间，ANALYZE 更新统计信息。

**错误（过时的统计信息）：**

```sql
-- 表有 100 万行但统计信息显示 1000
-- 查询计划器选择错误的策略
explain select * from orders where status = 'pending';
-- 显示: Seq Scan（因为统计信息显示小表）
-- 实际: Index Scan 会快得多
```

**正确（维护最新的统计信息）：**

```sql
-- 大量数据变更后手动分析
analyze orders;

-- 分析 WHERE 子句中使用的特定列
analyze orders (status, created_at);

-- 检查表上次分析的时间
select
  relname,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
from pg_stat_user_tables
order by last_analyze nulls first;
```

繁忙表的 autovacuum 调优：

```sql
-- 为高更新频率的表增加频率
alter table orders set (
  autovacuum_vacuum_scale_factor = 0.05,     -- 5% 死元组时 vacuum（默认 20%）
  autovacuum_analyze_scale_factor = 0.02     -- 2% 变更时 analyze（默认 10%）
);

-- 检查 autovacuum 状态
select * from pg_stat_progress_vacuum;
```

参考：[VACUUM](https://supabase.com/docs/guides/database/database-size#vacuum-operations)
