---
title: 使用覆盖索引避免回表查询
impact: MEDIUM-HIGH
impactDescription: 消除堆表读取，查询加速 2-5 倍
tags: indexes, covering-index, include, index-only-scan
---

## 使用覆盖索引避免回表查询

覆盖索引包含查询所需的所有列，实现仅索引扫描，完全跳过表访问。

**错误做法（索引扫描 + 堆表读取）：**

```sql
create index users_email_idx on users (email);

-- 必须从表堆中获取 name 和 created_at
select email, name, created_at from users where email = 'user@example.com';
```

**正确做法（使用 INCLUDE 的仅索引扫描）：**

```sql
-- 在索引中包含非搜索列
create index users_email_idx on users (email) include (name, created_at);

-- 所有列从索引提供，无需访问表
select email, name, created_at from users where email = 'user@example.com';
```

对 SELECT 但不过滤的列使用 INCLUDE：

```sql
-- 按状态搜索，但还需要 customer_id 和 total
create index orders_status_idx on orders (status) include (customer_id, total);

select status, customer_id, total from orders where status = 'shipped';
```

参考：[仅索引扫描](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
