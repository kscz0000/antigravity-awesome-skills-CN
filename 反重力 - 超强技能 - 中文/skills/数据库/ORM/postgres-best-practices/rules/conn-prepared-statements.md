---
title: 在连接池中正确使用 Prepared Statements
impact: HIGH
impactDescription: 避免池化环境中的 prepared statement 冲突
tags: prepared-statements, connection-pooling, transaction-mode
---

## 在连接池中正确使用 Prepared Statements

Prepared statements 绑定到特定数据库连接。在事务模式连接池中，连接被共享，会导致冲突。

**错误（在事务池中使用命名 prepared statements）：**

```sql
-- 命名 prepared statement
prepare get_user as select * from users where id = $1;

-- 在事务模式连接池中，下一个请求可能获得不同的连接
execute get_user(123);
-- ERROR: prepared statement "get_user" does not exist
```

**正确（使用匿名语句或会话模式）：**

```sql
-- 方案 1: 使用匿名 prepared statements（大多数 ORM 自动处理）
-- 查询在单个协议消息中准备并执行

-- 方案 2: 在事务模式中使用后释放
prepare get_user as select * from users where id = $1;
execute get_user(123);
deallocate get_user;

-- 方案 3: 使用会话模式连接池（端口 5432 vs 6543）
-- 连接在整个会话期间持有，prepared statements 持久化
```

检查驱动设置：

```sql
-- 许多驱动默认使用 prepared statements
-- Node.js pg: { prepare: false } 禁用
-- JDBC: prepareThreshold=0 禁用
```

参考：[连接池中的 Prepared Statements](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool-modes)
