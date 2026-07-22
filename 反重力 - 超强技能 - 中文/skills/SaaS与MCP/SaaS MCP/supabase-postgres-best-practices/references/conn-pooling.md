---
title: 为所有应用使用连接池
impact: CRITICAL
impactDescription: 支撑 10-100 倍的并发用户
tags: connection-pooling, pgbouncer, performance, scalability
---

## 为所有应用使用连接池

Postgres 连接很昂贵（每个 1-3MB 内存）。没有连接池，应用在负载下会耗尽连接。

**错误做法（每个请求新建连接）：**

```sql
-- 每个请求创建新连接
-- 应用代码：每个请求 db.connect()
-- 结果：500 个并发用户 = 500 个连接 = 数据库崩溃

-- 检查当前连接
select count(*) from pg_stat_activity;  -- 487 个连接！
```

**正确做法（连接池）：**

```sql
-- 在应用和数据库之间使用 PgBouncer 等池化器
-- 应用连接到池化器，池化器复用到 Postgres 的小型连接池

-- 配置 pool_size 基于：(CPU 核心数 * 2) + 磁盘数
-- 例如 4 核：pool_size = 10

-- 结果：500 个并发用户共享 10 个实际连接
select count(*) from pg_stat_activity;  -- 10 个连接
```

池模式：

- **事务模式**：每个事务后归还连接（适合大多数应用）
- **会话模式**：整个会话期间持有连接（预处理语句、临时表需要）

参考：[连接池](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
