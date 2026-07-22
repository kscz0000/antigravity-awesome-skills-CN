---
title: 为多列查询创建复合索引
impact: HIGH
impactDescription: 多列查询加速 5-10 倍
tags: indexes, composite-index, multi-column, query-optimization
---

## 为多列查询创建复合索引

当查询过滤多个列时，复合索引比单独的单列索引更高效。

**错误做法（单独的索引需要位图扫描）：**

```sql
-- 两个单独的索引
create index orders_status_idx on orders (status);
create index orders_created_idx on orders (created_at);

-- 查询必须合并两个索引（更慢）
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**正确做法（复合索引）：**

```sql
-- 单一复合索引（等值检查列放最左）
create index orders_status_created_idx on orders (status, created_at);

-- 查询使用一次高效的索引扫描
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**列顺序很重要** — 等值列放前面，范围列放后面：

```sql
-- 好：status (=) 在 created_at (>) 前面
create index idx on orders (status, created_at);

-- 适用于：WHERE status = 'pending'
-- 适用于：WHERE status = 'pending' AND created_at > '2024-01-01'
-- 不适用于：WHERE created_at > '2024-01-01'（最左前缀规则）
```

参考：[多列索引](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
