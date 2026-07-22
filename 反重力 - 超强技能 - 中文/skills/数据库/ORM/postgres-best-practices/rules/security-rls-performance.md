---
title: 优化 RLS 策略以提升性能
impact: HIGH
impactDescription: 正确的模式下 RLS 查询提速 5-10 倍
tags: rls, performance, security, optimization
---

## 优化 RLS 策略以提升性能

编写不当的 RLS 策略会导致严重的性能问题。战略性地使用子查询和索引。

**错误（每行都调用函数）：**

```sql
create policy orders_policy on orders
  using (auth.uid() = user_id);  -- 每行都调用 auth.uid()！

-- 100 万行时，auth.uid() 被调用 100 万次
```

**正确（将函数包装在 SELECT 中）：**

```sql
create policy orders_policy on orders
  using ((select auth.uid()) = user_id);  -- 调用一次，缓存结果

-- 大表上快 100 倍以上
```

对复杂检查使用 security definer 函数：

```sql
-- 创建辅助函数（以定义者身份运行，绕过 RLS）
create or replace function is_team_member(team_id bigint)
returns boolean
language sql
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members
    where team_id = $1 and user_id = (select auth.uid())
  );
$$;

-- 在策略中使用（索引查找，非逐行检查）
create policy team_orders_policy on orders
  using ((select is_team_member(team_id)));
```

始终在 RLS 策略使用的列上添加索引：

```sql
create index orders_user_id_idx on orders (user_id);
```

参考：[RLS 性能](https://supabase.com/docs/guides/database/postgres/row-level-security#rls-performance-recommendations)
