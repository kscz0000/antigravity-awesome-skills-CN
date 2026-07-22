---
title: 为 WHERE 和 JOIN 列添加索引
impact: CRITICAL
impactDescription: 大表查询加速 100-1000 倍
tags: indexes, performance, sequential-scan, query-optimization
---

## 为 WHERE 和 JOIN 列添加索引

在未索引列上过滤或连接会导致全表扫描，随着表的增长会呈指数级变慢。

**错误做法（大表上的顺序扫描）：**

```sql
-- customer_id 没有索引导致全表扫描
select * from orders where customer_id = 123;

-- EXPLAIN 显示：Seq Scan on orders (cost=0.00..25000.00 rows=100 width=85)
```

**正确做法（索引扫描）：**

```sql
-- 为频繁过滤的列创建索引
create index orders_customer_id_idx on orders (customer_id);

select * from orders where customer_id = 123;

-- EXPLAIN 显示：Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)
```

对于 JOIN 列，始终索引外键一侧：

```sql
-- 索引引用列
create index orders_customer_id_idx on orders (customer_id);

select c.name, o.total
from customers c
join orders o on o.customer_id = c.id;
```

参考：[查询优化](https://supabase.com/docs/guides/database/query-optimization)
