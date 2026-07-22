---
title: 为外键列创建索引
impact: HIGH
impactDescription: JOIN 和 CASCADE 操作提速 10-100 倍
tags: foreign-key, indexes, joins, schema
---

## 为外键列创建索引

Postgres 不会自动为外键列创建索引。缺失索引会导致慢 JOIN 和 CASCADE 操作。

**错误（外键无索引）：**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- customer_id 没有索引！
-- JOIN 和 ON DELETE CASCADE 都需要全表扫描
select * from orders where customer_id = 123;  -- Seq Scan
delete from customers where id = 123;          -- 锁表，扫描所有订单
```

**正确（外键有索引）：**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- 始终为 FK 列创建索引
create index orders_customer_id_idx on orders (customer_id);

-- 现在 JOIN 和级联操作都很快
select * from orders where customer_id = 123;  -- Index Scan
delete from customers where id = 123;          -- 使用索引，快速级联
```

查找缺失的 FK 索引：

```sql
select
  conrelid::regclass as table_name,
  a.attname as fk_column
from pg_constraint c
join pg_attribute a on a.attrelid = c.conrelid and a.attnum = any(c.conkey)
where c.contype = 'f'
  and not exists (
    select 1 from pg_index i
    where i.indrelid = c.conrelid and a.attnum = any(i.indkey)
  );
```

参考：[外键](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
