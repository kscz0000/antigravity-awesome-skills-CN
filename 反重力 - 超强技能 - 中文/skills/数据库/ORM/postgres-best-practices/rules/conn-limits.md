---
title: 设置合适的连接限制
impact: CRITICAL
impactDescription: 防止数据库崩溃和内存耗尽
tags: connections, max-connections, limits, stability
---

## 设置合适的连接限制

连接过多会耗尽内存并降低性能。根据可用资源设置限制。

**错误（无限制或过多连接）：**

```sql
-- 默认 max_connections = 100，但经常被盲目增大
show max_connections;  -- 500（对 4GB 内存来说太高了）

-- 每个连接使用 1-3MB 内存
-- 500 连接 * 2MB = 仅连接就占 1GB！
-- 负载下出现内存不足错误
```

**正确（基于资源计算）：**

```sql
-- 公式: max_connections = (RAM MB / 每连接 5MB) - 预留
-- 4GB 内存: (4096 / 5) - 10 = ~800 理论上限
-- 但实际 100-200 对查询性能更好

-- 4GB 内存的推荐设置
alter system set max_connections = 100;

-- 同时合理设置 work_mem
-- work_mem * max_connections 不应超过 25% 的内存
alter system set work_mem = '8MB';  -- 8MB * 100 = 800MB 最大
```

监控连接使用情况：

```sql
select count(*), state from pg_stat_activity group by state;
```

参考：[数据库连接](https://supabase.com/docs/guides/platform/performance#connection-management)
