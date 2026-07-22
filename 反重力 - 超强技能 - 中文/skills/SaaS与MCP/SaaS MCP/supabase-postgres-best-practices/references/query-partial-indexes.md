---
title: 对过滤查询使用部分索引
impact: HIGH
impactDescription: 索引缩小 5-20 倍，写入和查询更快
tags: indexes, partial-index, query-optimization, storage
---

## 对过滤查询使用部分索引

部分索引仅包含匹配 WHERE 条件的行，当查询一致过滤相同条件时，索引更小、更快。

**错误做法（完整索引包含不相关的行）：**

```sql
-- 索引包含所有行，包括软删除的行
create index users_email_idx on users (email);

-- 查询总是过滤活跃用户
select * from users where email = 'user@example.com' and deleted_at is null;
```

**正确做法（部分索引匹配查询过滤条件）：**

```sql
-- 索引仅包含活跃用户
create index users_active_email_idx on users (email)
where deleted_at is null;

-- 查询使用更小、更快的索引
select * from users where email = 'user@example.com' and deleted_at is null;
```

部分索引的常见用例：

```sql
-- 仅待处理订单（完成后状态很少再变）
create index orders_pending_idx on orders (created_at)
where status = 'pending';

-- 仅非空值
create index products_sku_idx on products (sku)
where sku is not null;
```

参考：[部分索引](https://www.postgresql.org/docs/current/indexes-partial.html)
