---
title: 在 WHERE 和 JOIN 列上添加索引
impact: CRITICAL
impactDescription: 大表查询提速 100-1000 倍
tags: indexes, performance, sequential-scan, query-optimization
---

## 在 WHERE 和 JOIN 列上添加索引

对未索引列进行过滤或 JOIN 会导致全表扫描，表越大性能下降越严重。

**错误（大表上的顺序扫描）：**

```sql
-- customer_id 没有索引，导致全表扫描
select * from orders where customer_id = 123;

-- EXPLAIN 显示: Seq Scan on orders (cost=0.00..25000.00 rows=100 width=85)
```

**正确（索引扫描）：**

```sql
-- 在常用过滤列上创建索引
create index orders_customer_id_idx on orders (customer_id);

select * from orders where customer_id = 123;

-- EXPLAIN 显示: Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)
```

对于 JOIN 列，始终为外键侧创建索引：

```sql
-- 为引用列创建索引
create index orders_customer_id_idx on orders (customer_id);

select c.name, o.total
from customers c
join orders o on o.customer_id = c.id;
```

参考：[查询优化](https://supabase.com/docs/guides/database/query-optimization)
