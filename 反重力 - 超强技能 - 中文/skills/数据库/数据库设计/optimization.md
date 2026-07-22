# 查询优化

> N+1 问题、EXPLAIN ANALYZE 与优化优先级。

## N+1 问题

```
What is N+1?
├── 1 query to get parent records
├── N queries to get related records
└── Very slow!

Solutions:
├── JOIN → Single query with all data
├── Eager loading → ORM handles JOIN
├── DataLoader → Batch and cache (GraphQL)
└── Subquery → Fetch related in one query
```

## 查询分析的思考方式

```
Before optimizing:
├── EXPLAIN ANALYZE the query
├── Look for Seq Scan (full table scan)
├── Check actual vs estimated rows
└── Identify missing indexes
```

## 优化优先级

1. **添加缺失的索引**（最常见的问题）
2. **只查询必要字段**（避免 SELECT *）
3. **使用合适的 JOIN**（尽量避免子查询）
4. **尽早分页**（在数据库层做分页）
5. **合理使用缓存**
