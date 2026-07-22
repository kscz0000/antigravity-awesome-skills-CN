---
title: 启用 pg_stat_statements 进行查询分析
impact: LOW-MEDIUM
impactDescription: 识别消耗资源最多的查询
tags: pg-stat-statements, monitoring, statistics, performance
---

## 启用 pg_stat_statements 进行查询分析

pg_stat_statements 跟踪所有查询的执行统计，帮助识别慢查询和频繁查询。

**错误做法（无法了解查询模式）：**

```sql
-- 数据库很慢，但哪些查询是问题所在？
-- 没有 pg_stat_statements 无法知道
```

**正确做法（启用并查询 pg_stat_statements）：**

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

-- 优化后重置统计
select pg_stat_statements_reset();
```

需要监控的关键指标：

```sql
-- 平均时间高的查询（优化候选）
select query, mean_exec_time, calls
from pg_stat_statements
where mean_exec_time > 100  -- > 100ms 平均
order by mean_exec_time desc;
```

参考：[pg_stat_statements](https://supabase.com/docs/guides/database/extensions/pg_stat_statements)
