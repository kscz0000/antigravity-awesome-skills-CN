---
title: 所有应用使用连接池
impact: CRITICAL
impactDescription: 支持 10-100 倍更多并发用户
tags: connection-pooling, pgbouncer, performance, scalability
---

## 所有应用使用连接池

Postgres 连接成本高昂（每个 1-3MB 内存）。没有连接池时，应用在负载下会耗尽连接。

**错误（每个请求新建连接）：**

```sql
-- 每个请求创建新连接
-- 应用代码: 每次请求 db.connect()
-- 结果: 500 并发用户 = 500 连接 = 数据库崩溃

-- 检查当前连接数
select count(*) from pg_stat_activity;  -- 487 个连接！
```

**正确（连接池）：**

```sql
-- 在应用和数据库之间使用 PgBouncer 等连接池
-- 应用连接到连接池，连接池复用少量连接到 Postgres

-- 根据以下公式配置 pool_size: (CPU 核心数 * 2) + 磁盘数
-- 4 核示例: pool_size = 10

-- 结果: 500 并发用户共享 10 个实际连接
select count(*) from pg_stat_activity;  -- 10 个连接
```

连接池模式：

- **事务模式**：每个事务结束后归还连接（大多数应用最佳选择）
- **会话模式**：整个会话期间持有连接（prepared statements、临时表需要）

参考：[连接池](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
