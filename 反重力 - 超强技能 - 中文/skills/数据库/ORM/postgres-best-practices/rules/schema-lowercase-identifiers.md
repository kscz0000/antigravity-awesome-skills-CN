---
title: 使用小写标识符以保证兼容性
impact: MEDIUM
impactDescription: 避免工具、ORM 和 AI 助手的大小写敏感问题
tags: naming, identifiers, case-sensitivity, schema, conventions
---

## 使用小写标识符以保证兼容性

PostgreSQL 将未引用的标识符折叠为小写。带引号的混合大小写标识符需要永远加引号，并导致工具、ORM 和 AI 助手无法识别。

**错误（混合大小写标识符）：**

```sql
-- 带引号的标识符保留大小写，但处处需要引号
CREATE TABLE "Users" (
  "userId" bigint PRIMARY KEY,
  "firstName" text,
  "lastName" text
);

-- 必须始终加引号，否则查询失败
SELECT "firstName" FROM "Users" WHERE "userId" = 1;

-- 这会失败 - Users 不加引号变成 users
SELECT firstName FROM Users;
-- ERROR: relation "users" does not exist
```

**正确（小写 snake_case）：**

```sql
-- 未引用的小写标识符可移植且工具友好
CREATE TABLE users (
  user_id bigint PRIMARY KEY,
  first_name text,
  last_name text
);

-- 无需引号，所有工具都能识别
SELECT first_name FROM users WHERE user_id = 1;
```

混合大小写标识符的常见来源：

```sql
-- ORM 通常生成带引号的 camelCase - 配置为使用 snake_case
-- 从其他数据库迁移可能保留原始大小写
-- 一些 GUI 工具默认给标识符加引号 - 禁用此功能

-- 如果必须使用混合大小写，创建视图作为兼容层
CREATE VIEW users AS SELECT "userId" AS user_id, "firstName" AS first_name FROM "Users";
```

参考：[标识符和关键字](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)
