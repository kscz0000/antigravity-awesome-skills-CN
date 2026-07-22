---
title: 应用最小权限原则
impact: MEDIUM
impactDescription: 减少攻击面，更好的审计追踪
tags: privileges, security, roles, permissions
---

## 应用最小权限原则

仅授予所需的最低权限。永远不要使用超级用户进行应用查询。

**错误做法（权限过宽）：**

```sql
-- 应用使用超级用户连接
-- 或向应用角色授予 ALL 权限
grant all privileges on all tables in schema public to app_user;
grant all privileges on all sequences in schema public to app_user;

-- 任何 SQL 注入都会造成灾难性后果
-- drop table users; 会级联影响一切
```

**正确做法（最小、具体的授权）：**

```sql
-- 创建没有默认权限的角色
create role app_readonly nologin;

-- 仅授予特定表的 SELECT
grant usage on schema public to app_readonly;
grant select on public.products, public.categories to app_readonly;

-- 创建范围有限的写入角色
create role app_writer nologin;
grant usage on schema public to app_writer;
grant select, insert, update on public.orders to app_writer;
grant usage on sequence orders_id_seq to app_writer;
-- 没有 DELETE 权限

-- 登录角色继承这些权限
create role app_user login password 'xxx';
grant app_writer to app_user;
```

撤销 public 默认权限：

```sql
-- 撤销默认的 public 访问权限
revoke all on schema public from public;
revoke all on all tables in schema public from public;
```

参考：[角色和权限](https://supabase.com/blog/postgres-roles-and-privileges)
