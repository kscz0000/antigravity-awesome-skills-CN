---
title: 使用覆盖索引避免表查找
impact: MEDIUM-HIGH
impactDescription: 消除堆获取，查询提速 2-5 倍
tags: indexes, covering-index, include, index-only-scan
---

## 使用覆盖索引避免表查找

覆盖索引包含查询所需的所有列，支持仅索引扫描，完全跳过表访问。

**错误（索引扫描 + 堆获取）：**

```sql
create index users_email_idx on users (email);

-- 必须从表堆中获取 name 和 created_at
select email, name, created_at from users where email = 'user@example.com';
```

**正确（使用 INCLUDE 的仅索引扫描）：**

```sql
-- 将非搜索列包含在索引中
create index users_email_idx on users (email) include (name, created_at);

-- 所有列从索引提供，无需表访问
select email, name, created_at from users where email = 'user@example.com';
```

对 SELECT 但不过滤的列使用 INCLUDE：

```sql
-- 按 status 搜索，但也需要 customer_id 和 total
create index orders_status_idx on orders (status) include (customer_id, total);

select status, customer_id, total from orders where status = 'shipped';
```

参考：[仅索引扫描](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
