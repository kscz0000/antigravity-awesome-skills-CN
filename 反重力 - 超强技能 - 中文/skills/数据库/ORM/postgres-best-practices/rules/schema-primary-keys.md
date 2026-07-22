---
title: 选择最优主键策略
impact: HIGH
impactDescription: 更好的索引局部性，减少碎片化
tags: primary-key, identity, uuid, serial, schema
---

## 选择最优主键策略

主键选择影响插入性能、索引大小和复制效率。

**错误（有问题的主键选择）：**

```sql
-- identity 是 SQL 标准方式
create table users (
  id serial primary key  -- 可用，但推荐 IDENTITY
);

-- 随机 UUID（v4）导致索引碎片化
create table orders (
  id uuid default gen_random_uuid() primary key  -- UUIDv4 = 随机 = 分散插入
);
```

**正确（最优主键策略）：**

```sql
-- 使用 IDENTITY 生成顺序 ID（SQL 标准，大多数情况最佳）
create table users (
  id bigint generated always as identity primary key
);

-- 需要 UUID 的分布式系统，使用 UUIDv7（时间有序）
-- 需要 pg_uuidv7 扩展: create extension pg_uuidv7;
create table orders (
  id uuid default uuid_generate_v7() primary key  -- 时间有序，无碎片化
);

-- 替代方案：时间前缀 ID，可排序、分布式（无需扩展）
create table events (
  id text default concat(
    to_char(now() at time zone 'utc', 'YYYYMMDDHH24MISSMS'),
    gen_random_uuid()::text
  ) primary key
);
```

指南：
- 单数据库：`bigint identity`（顺序、8 字节、SQL 标准）
- 分布式/暴露 ID：UUIDv7（需要 pg_uuidv7）或 ULID（时间有序、无碎片化）
- `serial` 可用但 `identity` 是 SQL 标准，新应用推荐使用
- 避免随机 UUID（v4）作为大表主键（导致索引碎片化）

参考：[Identity Columns](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY)
