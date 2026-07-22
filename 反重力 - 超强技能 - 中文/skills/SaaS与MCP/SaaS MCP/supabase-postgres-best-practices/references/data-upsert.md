---
title: 使用 UPSERT 实现插入或更新操作
impact: MEDIUM
impactDescription: 原子操作，消除竞态条件
tags: upsert, on-conflict, insert, update
---

## 使用 UPSERT 实现插入或更新操作

使用单独的 SELECT-then-INSERT/UPDATE 会产生竞态条件。使用 INSERT ... ON CONFLICT 实现原子 upsert。

**错误做法（先检查再插入的竞态条件）：**

```sql
-- 竞态条件：两个请求同时检查
select * from settings where user_id = 123 and key = 'theme';
-- 两者都没找到

-- 两者都尝试插入
insert into settings (user_id, key, value) values (123, 'theme', 'dark');
-- 一个成功，另一个因重复键错误而失败！
```

**正确做法（原子 UPSERT）：**

```sql
-- 单次原子操作
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value, updated_at = now();

-- 返回插入/更新的行
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value
returning *;
```

插入或忽略模式：

```sql
-- 仅在不存在时插入（不更新）
insert into page_views (page_id, user_id)
values (1, 123)
on conflict (page_id, user_id) do nothing;
```

参考：[INSERT ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
