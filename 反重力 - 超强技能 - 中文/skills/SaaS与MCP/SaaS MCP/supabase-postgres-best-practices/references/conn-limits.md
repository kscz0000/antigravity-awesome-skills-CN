---
title: 设置合适的连接限制
impact: CRITICAL
impactDescription: 防止数据库崩溃和内存耗尽
tags: connections, max-connections, limits, stability
---

## 设置合适的连接限制

过多连接会耗尽内存并降低性能。根据可用资源设置限制。

**错误做法（无限或过多的连接）：**

```sql
-- 默认 max_connections = 100，但经常盲目调高
show max_connections;  -- 500（对 4GB 内存来说太高了）

-- 每个连接占用 1-3MB 内存
-- 500 个连接 * 2MB = 1GB 仅用于连接！
-- 负载下会出现内存不足错误
```

**正确做法（根据资源计算）：**

```sql
-- 公式：max_connections = (内存 MB / 每连接 5MB) - 预留
-- 对 4GB 内存：(4096 / 5) - 10 = 约 800 理论最大值
-- 但实际中，100-200 对查询性能更好

-- 4GB 内存的推荐设置
alter system set max_connections = 100;

-- 同时设置合适的 work_mem
-- work_mem * max_connections 不应超过内存的 25%
alter system set work_mem = '8MB';  -- 8MB * 100 = 800MB 上限
```

监控连接使用情况：

```sql
select count(*), state from pg_stat_activity group by state;
```

参考：[数据库连接](https://supabase.com/docs/guides/platform/performance#connection-management)
