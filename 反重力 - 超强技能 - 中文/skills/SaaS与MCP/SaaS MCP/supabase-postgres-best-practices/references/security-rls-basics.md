---
title: 为多租户数据启用行级安全
impact: CRITICAL
impactDescription: 数据库强制租户隔离，防止数据泄露
tags: rls, row-level-security, multi-tenant, security
---

## 为多租户数据启用行级安全

行级安全（RLS）在数据库层面强制数据访问，确保用户只能看到自己的数据。

**错误做法（仅依赖应用层过滤）：**

```sql
-- 仅依赖应用来过滤
select * from orders where user_id = $current_user_id;

-- bug 或绕过意味着所有数据暴露！
select * from orders;  -- 返回所有订单
```

**正确做法（数据库强制的 RLS）：**

```sql
-- 在表上启用 RLS
alter table orders enable row level security;

-- 创建策略，让用户只能看到自己的订单
create policy orders_user_policy on orders
  for all
  using (user_id = current_setting('app.current_user_id')::bigint);

-- 即使对表所有者也强制 RLS
alter table orders force row level security;

-- 设置用户上下文并查询
set app.current_user_id = '123';
select * from orders;  -- 仅返回用户 123 的订单
```

authenticated 角色的策略：

```sql
create policy orders_user_policy on orders
  for all
  to authenticated
  using (user_id = auth.uid());
```

参考：[行级安全](https://supabase.com/docs/guides/database/postgres/row-level-security)
