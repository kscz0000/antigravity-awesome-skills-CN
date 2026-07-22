---
title: 通过批量加载消除 N+1 查询
impact: MEDIUM-HIGH
impactDescription: 数据库往返减少 10-100 倍
tags: n-plus-one, batch, performance, queries
---

## 通过批量加载消除 N+1 查询

N+1 查询在循环中为每个项目执行一次查询。使用数组或 JOIN 将它们批量为单次查询。

**错误（N+1 查询）：**

```sql
-- 第一个查询：获取所有用户
select id from users where active = true;  -- 返回 100 个 ID

-- 然后 N 次查询，每个用户一次
select * from orders where user_id = 1;
select * from orders where user_id = 2;
select * from orders where user_id = 3;
-- ... 还有 97 次查询！

-- 总计：101 次数据库往返
```

**正确（单次批量查询）：**

```sql
-- 收集 ID 并使用 ANY 查询一次
select * from orders where user_id = any(array[1, 2, 3, ...]);

-- 或使用 JOIN 代替循环
select u.id, u.name, o.*
from users u
left join orders o on o.user_id = u.id
where u.active = true;

-- 总计：1 次往返
```

应用模式：

```sql
-- 不要在应用代码中循环:
-- for user in users: db.query("SELECT * FROM orders WHERE user_id = $1", user.id)

-- 传递数组参数:
select * from orders where user_id = any($1::bigint[]);
-- 应用传递: [1, 2, 3, 4, 5, ...]
```

参考：[N+1 查询问题](https://supabase.com/docs/guides/database/query-optimization)
