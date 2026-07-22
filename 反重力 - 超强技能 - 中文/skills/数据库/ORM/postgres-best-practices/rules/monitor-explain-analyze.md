---
title: 使用 EXPLAIN ANALYZE 诊断慢查询
impact: LOW-MEDIUM
impactDescription: 精确定位查询执行瓶颈
tags: explain, analyze, diagnostics, query-plan
---

## 使用 EXPLAIN ANALYZE 诊断慢查询

EXPLAIN ANALYZE 执行查询并显示实际耗时，揭示真正的性能瓶颈。

**错误（猜测性能问题）：**

```sql
-- 查询很慢，但为什么？
select * from orders where customer_id = 123 and status = 'pending';
-- "一定是缺索引" - 但哪个索引？
```

**正确（使用 EXPLAIN ANALYZE）：**

```sql
explain (analyze, buffers, format text)
select * from orders where customer_id = 123 and status = 'pending';

-- 输出揭示问题:
-- Seq Scan on orders (cost=0.00..25000.00 rows=50 width=100) (actual time=0.015..450.123 rows=50 loops=1)
--   Filter: ((customer_id = 123) AND (status = 'pending'::text))
--   Rows Removed by Filter: 999950
--   Buffers: shared hit=5000 read=15000
-- Planning Time: 0.150 ms
-- Execution Time: 450.500 ms
```

关键检查点：

```sql
-- 大表上的 Seq Scan = 缺少索引
-- Rows Removed by Filter = 选择性差或缺少索引
-- Buffers: read >> hit = 数据未缓存，需要更多内存
-- 高循环次数的 Nested Loop = 考虑不同的连接策略
-- Sort Method: external merge = work_mem 太低
```

参考：[EXPLAIN](https://supabase.com/docs/guides/database/inspect)
