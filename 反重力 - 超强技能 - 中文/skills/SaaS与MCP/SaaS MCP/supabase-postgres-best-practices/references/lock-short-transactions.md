---
title: 保持事务简短以减少锁竞争
impact: MEDIUM-HIGH
impactDescription: 吞吐量提升 3-5 倍，减少死锁
tags: transactions, locking, contention, performance
---

## 保持事务简短以减少锁竞争

长时间运行的事务持有锁，阻塞其他查询。尽量保持事务简短。

**错误做法（长事务中包含外部调用）：**

```sql
begin;
select * from orders where id = 1 for update;  -- 获取锁

-- 应用调用支付 API（2-5 秒）
-- 该行的其他查询被阻塞！

update orders set status = 'paid' where id = 1;
commit;  -- 整个期间持有锁
```

**正确做法（最小事务范围）：**

```sql
-- 在事务外验证数据和调用 API
-- 应用：response = await paymentAPI.charge(...)

-- 仅在实际更新时持有锁
begin;
update orders
set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- 锁仅持有几毫秒
```

使用 `statement_timeout` 防止失控事务：

```sql
-- 终止运行超过 30 秒的查询
set statement_timeout = '30s';

-- 或按会话设置
set local statement_timeout = '5s';
```

参考：[事务管理](https://www.postgresql.org/docs/current/tutorial-transactions.html)
