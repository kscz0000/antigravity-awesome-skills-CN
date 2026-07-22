---
title: 优化 RLS 策略性能
impact: HIGH
impactDescription: 使用正确的模式，RLS 查询加速 5-10 倍
tags: rls, performance, security, optimization
---

## 优化 RLS 策略性能

编写不当的 RLS 策略会导致严重的性能问题。战略性地使用子查询和索引。

**错误做法（每行调用函数）：**

```sql
create policy orders_policy on orders
  using (auth.uid() = user_id);  -- auth.uid() 每行都调用！

-- 100 万行时，auth.uid() 被调用 100 万次
```

**正确做法（将函数包裹在 SELECT 中）：**

```sql
create policy orders_policy on orders
  using ((select auth.uid()) = user_id);  -- 调用一次，缓存结果

-- 在大表上快 100 倍以上
```

对复杂检查使用安全定义者函数：

`SECURITY DEFINER` 函数以创建者的权限运行，并绕过其接触的任何表上的 RLS — 这正是它们适用于内部查找的原因，但也是误用时危险的原因。始终在函数体内包含显式的 `auth.uid()` 检查，将它们放在非公开模式中，并撤销任何不应直接调用它们的角色的 `EXECUTE` 权限。

```sql
-- 在私有模式中创建辅助函数
create or replace function private.is_team_member(team_id bigint)
returns boolean
language sql
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members
    -- 始终在函数内部检查调用用户的身份
    where team_id = $1 and user_id = (select auth.uid())
  );
$$;

-- 撤销公共角色的直接执行权限
revoke execute on function private.is_team_member(bigint) from PUBLIC, anon, authenticated, service_role;

-- 在策略中使用（索引查找，而非逐行检查）
create policy team_orders_policy on orders
  using ((select private.is_team_member(team_id)));
```

始终为 RLS 策略中使用的列添加索引：

```sql
create index orders_user_id_idx on orders (user_id);
```

参考：[RLS 性能](https://supabase.com/docs/guides/database/postgres/row-level-security#rls-performance-recommendations)
