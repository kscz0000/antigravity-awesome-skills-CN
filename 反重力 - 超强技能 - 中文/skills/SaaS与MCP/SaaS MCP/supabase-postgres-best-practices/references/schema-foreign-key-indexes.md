---
title: 为外键列添加索引
impact: HIGH
impactDescription: JOIN 和 CASCADE 操作加速 10-100 倍
tags: foreign-key, indexes, joins, schema
---

## 为外键列添加索引

Postgres 不会自动索引外键列。缺少索引导致慢 JOIN 和 CASCADE 操作。

**错误做法（未索引的外键）：**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- customer_id 没有索引！
-- JOIN 和 ON DELETE CASCADE 都需要全表扫描
select * from orders where customer_id = 123;  -- Seq Scan
delete from customers where id = 123;          -- 锁定表，扫描所有 orders
```

**正确做法（索引外键）：**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- 始终索引外键列
create index orders_customer_id_idx on orders (customer_id);

-- 现在 JOIN 和级联操作都很快
select * from orders where customer_id = 123;  -- Index Scan
delete from customers where id = 123;          -- 使用索引，快速级联
```

查找缺失的外键索引：

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
