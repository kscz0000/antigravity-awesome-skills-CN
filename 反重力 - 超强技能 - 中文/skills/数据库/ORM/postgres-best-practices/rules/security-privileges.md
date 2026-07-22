---
title: 应用最小权限原则
impact: MEDIUM
impactDescription: 减少攻击面，更好的审计追踪
tags: privileges, security, roles, permissions
---

## 应用最小权限原则

仅授予所需的最低权限。永远不要用超级用户执行应用查询。

**错误（权限过宽）：**

```sql
-- 应用使用超级用户连接
-- 或授予应用角色 ALL 权限
grant all privileges on all tables in schema public to app_user;
grant all privileges on all sequences in schema public to app_user;

-- 任何 SQL 注入都会变成灾难
-- drop table users; 级联删除一切
```

**正确（最小化、精确授权）：**

```sql
-- 创建无默认权限的角色
create role app_readonly nologin;

-- 仅授予特定表的 SELECT 权限
grant usage on schema public to app_readonly;
grant select on public.products, public.categories to app_readonly;

-- 创建有限写入权限的角色
create role app_writer nologin;
grant usage on schema public to app_writer;
grant select, insert, update on public.orders to app_writer;
grant usage on sequence orders_id_seq to app_writer;
-- 无 DELETE 权限

-- 登录角色继承这些权限
create role app_user login password 'xxx';
grant app_writer to app_user;
```

撤销公共默认权限：

```sql
-- 撤销默认公共访问
revoke all on schema public from public;
revoke all on all tables in schema public from public;
```

参考：[角色与权限](https://supabase.com/blog/postgres-roles-and-privileges)
