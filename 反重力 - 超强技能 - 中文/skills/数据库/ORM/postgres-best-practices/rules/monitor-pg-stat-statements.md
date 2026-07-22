---
title: 启用 pg_stat_statements 进行查询分析
impact: LOW-MEDIUM
impactDescription: 识别资源消耗最高的查询
tags: pg-stat-statements, monitoring, statistics, performance
---

## 启用 pg_stat_statements 进行查询分析

pg_stat_statements 跟踪所有查询的执行统计信息，帮助识别慢查询和高频查询。

**错误（无法了解查询模式）：**

```sql
-- 数据库很慢，但哪些查询是问题所在？
-- 没有 pg_stat_statements 就无法知道
```

**正确（启用并查询 pg_stat_statements）：**

```sql
-- 启用扩展
create extension if not exists pg_stat_statements;

-- 按总时间查找最慢的查询
select
  calls,
  round(total_exec_time::numeric, 2) as total_time_ms,
  round(mean_exec_time::numeric, 2) as mean_time_ms,
  query
from pg_stat_statements
order by total_exec_time desc
limit 10;

-- 查找最频繁的查询
select calls, query
from pg_stat_statements
order by calls desc
limit 10;

-- 优化后重置统计信息
select pg_stat_statements_reset();
```

关键监控指标：

```sql
-- 高平均时间的查询（优化候选）
select query, mean_exec_time, calls
from pg_stat_statements
where mean_exec_time > 100  -- 平均 > 100ms
order by mean_exec_time desc;
```

参考：[pg_stat_statements](https://supabase.com/docs/guides/database/extensions/pg_stat_statements)
