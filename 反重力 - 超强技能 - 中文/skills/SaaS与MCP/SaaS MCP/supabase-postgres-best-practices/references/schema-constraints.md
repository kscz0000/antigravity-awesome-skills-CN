---
title: 在迁移中安全地添加约束
impact: HIGH
impactDescription: 防止迁移失败，实现幂等模式变更
tags: constraints, migrations, schema, alter-table
---

## 在迁移中安全地添加约束

PostgreSQL 不支持 `ADD CONSTRAINT IF NOT EXISTS`。使用此语法的迁移将会失败。

**错误做法（导致语法错误）：**

```sql
-- 错误：在 "not" 附近有语法错误 (SQLSTATE 42601)
alter table public.profiles
add constraint if not exists profiles_birthchart_id_unique unique (birthchart_id);
```

**正确做法（幂等的约束创建）：**

```sql
-- 使用 DO 块在添加前检查
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profiles_birthchart_id_unique'
    and conrelid = 'public.profiles'::regclass
  ) then
    alter table public.profiles
    add constraint profiles_birthchart_id_unique unique (birthchart_id);
  end if;
end $$;
```

所有约束类型：

```sql
-- 检查约束
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'check_age_positive'
  ) then
    alter table users add constraint check_age_positive check (age > 0);
  end if;
end $$;

-- 外键
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profiles_birthchart_id_fkey'
  ) then
    alter table profiles
    add constraint profiles_birthchart_id_fkey
    foreign key (birthchart_id) references birthcharts(id);
  end if;
end $$;
```

检查约束是否存在：

```sql
-- 查询约束是否存在
select conname, contype, pg_get_constraintdef(oid)
from pg_constraint
where conrelid = 'public.profiles'::regclass;

-- contype 值：
-- 'p' = PRIMARY KEY
-- 'f' = FOREIGN KEY
-- 'u' = UNIQUE
-- 'c' = CHECK
```

参考：[约束](https://www.postgresql.org/docs/current/ddl-constraints.html)
