---
title: 在连接池环境中正确使用预处理语句
impact: HIGH
impactDescription: 避免池化环境中的预处理语句冲突
tags: prepared-statements, connection-pooling, transaction-mode
---

## 在连接池环境中正确使用预处理语句

预处理语句绑定到单独的数据库连接。在事务模式池化中，连接是共享的，会导致冲突。

**错误做法（事务池化中使用命名预处理语句）：**

```sql
-- 命名预处理语句
prepare get_user as select * from users where id = $1;

-- 在事务模式池化中，下一个请求可能获得不同的连接
execute get_user(123);
-- 错误：预处理语句 "get_user" 不存在
```

**正确做法（使用匿名语句或会话模式）：**

```sql
-- 方案 1：使用匿名预处理语句（大多数 ORM 自动这样做）
-- 查询在单个协议消息中准备和执行

-- 方案 2：事务模式中使用后释放
prepare get_user as select * from users where id = $1;
execute get_user(123);
deallocate get_user;

-- 方案 3：使用会话模式池化（端口 5432 vs 6543）
-- 连接在整个会话期间持有，预处理语句持久存在
```

检查你的驱动设置：

```sql
-- 许多驱动默认使用预处理语句
-- Node.js pg：{ prepare: false } 禁用
-- JDBC：prepareThreshold=0 禁用
```

参考：[池化与预处理语句](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool-modes)
