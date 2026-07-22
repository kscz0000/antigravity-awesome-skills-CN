---
title: 为 JSONB 列建立索引以实现高效查询
impact: MEDIUM
impactDescription: 正确索引后 JSONB 查询加速 10-100 倍
tags: jsonb, gin, indexes, json
---

## 为 JSONB 列建立索引以实现高效查询

没有索引的 JSONB 查询会扫描整个表。使用 GIN 索引处理包含查询。

**错误做法（JSONB 没有索引）：**

```sql
create table products (
  id bigint primary key,
  attributes jsonb
);

-- 每次查询都是全表扫描
select * from products where attributes @> '{"color": "red"}';
select * from products where attributes->>'brand' = 'Nike';
```

**正确做法（GIN 索引用于 JSONB）：**

```sql
-- GIN 索引用于包含运算符（@>、?、?&、?|）
create index products_attrs_gin on products using gin (attributes);

-- 现在包含查询使用索引
select * from products where attributes @> '{"color": "red"}';

-- 对于特定键查找，使用表达式索引
create index products_brand_idx on products ((attributes->>'brand'));
select * from products where attributes->>'brand' = 'Nike';
```

选择正确的运算符类：

```sql
-- jsonb_ops（默认）：支持所有运算符，索引较大
create index idx1 on products using gin (attributes);

-- jsonb_path_ops：仅支持 @> 运算符，但索引小 2-3 倍
create index idx2 on products using gin (attributes jsonb_path_ops);
```

参考：[JSONB 索引](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING)
