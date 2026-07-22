---
title: 选择最优主键策略
impact: HIGH
impactDescription: 更好的索引局部性，减少碎片化
tags: primary-key, identity, uuid, serial, schema
---

## 选择最优主键策略

主键选择影响插入性能、索引大小和复制效率。

**错误做法（有问题的主键选择）：**

```sql
-- identity 是 SQL 标准方式
create table users (
  id serial primary key  -- 可用，但推荐使用 IDENTITY
);

-- 随机 UUID (v4) 导致索引碎片化
create table orders (
  id uuid default gen_random_uuid() primary key  -- UUIDv4 = 随机 = 分散插入
);
```

**正确做法（最优主键策略）：**

```sql
-- 使用 IDENTITY 作为顺序 ID（SQL 标准，大多数情况最佳）
create table users (
  id bigint generated always as identity primary key
);

-- 对于需要 UUID 的分布式系统，使用 UUIDv7（时间有序）
-- 需要 pg_uuidv7 扩展：create extension pg_uuidv7;
create table orders (
  id uuid default uuid_generate_v7() primary key  -- 时间有序，无碎片化
);

-- 替代方案：时间前缀 ID，可排序的分布式 ID（无需扩展）
create table events (
  id text default concat(
    to_char(now() at time zone 'utc', 'YYYYMMDDHH24MISSMS'),
    gen_random_uuid()::text
  ) primary key
);
```

指南：

- 单数据库：`bigint identity`（顺序、8 字节、SQL 标准）
- 分布式/暴露的 ID：UUIDv7（需要 pg_uuidv7）或 ULID（时间有序，无
  碎片化）
- `serial` 可用但 `identity` 是 SQL 标准，推荐用于新
  应用
- 避免在大表上使用随机 UUID (v4) 作为主键（会导致索引
  碎片化）

参考：
[Identity Columns](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY)
