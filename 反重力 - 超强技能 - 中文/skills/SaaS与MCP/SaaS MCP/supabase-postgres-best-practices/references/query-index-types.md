---
title: 为你的数据选择正确的索引类型
impact: HIGH
impactDescription: 使用正确的索引类型可提升 10-100 倍
tags: indexes, btree, gin, gist, brin, hash, index-types
---

## 为你的数据选择正确的索引类型

不同的索引类型擅长不同的查询模式。默认的 B-tree 并不总是最优选择。

**错误做法（B-tree 用于 JSONB 包含查询）：**

```sql
-- B-tree 无法优化包含运算符
create index products_attrs_idx on products (attributes);
select * from products where attributes @> '{"color": "red"}';
-- 全表扫描 - B-tree 不支持 @> 运算符
```

**正确做法（GIN 用于 JSONB）：**

```sql
-- GIN 支持 @>、?、?&、?| 运算符
create index products_attrs_idx on products using gin (attributes);
select * from products where attributes @> '{"color": "red"}';
```

索引类型指南：

```sql
-- B-tree（默认）：=、<、>、BETWEEN、IN、IS NULL
create index users_created_idx on users (created_at);

-- GIN：数组、JSONB、全文搜索
create index posts_tags_idx on posts using gin (tags);

-- GiST：几何数据、范围类型、最近邻 (KNN) 查询
create index locations_idx on places using gist (location);

-- BRIN：大型时序表（索引小 10-100 倍）
create index events_time_idx on events using brin (created_at);

-- Hash：仅等值查询（比 B-tree 的 = 稍快）
create index sessions_token_idx on sessions using hash (token);
```

参考：[索引类型](https://www.postgresql.org/docs/current/indexes-types.html)
