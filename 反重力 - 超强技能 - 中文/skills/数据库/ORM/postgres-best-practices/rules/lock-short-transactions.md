---
title: 保持事务简短以减少锁竞争
impact: MEDIUM-HIGH
impactDescription: 吞吐量提升 3-5 倍，死锁更少
tags: transactions, locking, contention, performance
---

## 保持事务简短以减少锁竞争

长时间运行的事务持有锁会阻塞其他查询。尽量保持事务简短。

**错误（包含外部调用的长事务）：**

```sql
begin;
select * from orders where id = 1 for update;  -- 获取锁

-- 应用向支付 API 发起 HTTP 调用（2-5 秒）
-- 该行的其他查询被阻塞！

update orders set status = 'paid' where id = 1;
commit;  -- 整个过程持有锁
```

**正确（最小事务范围）：**

```sql
-- 在事务外验证数据和调用 API
-- 应用: response = await paymentAPI.charge(...)

-- 仅在实际更新时持有锁
begin;
update orders
set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- 锁仅持有毫秒级
```

使用 `statement_timeout` 防止失控事务：

```sql
-- 终止运行超过 30 秒的查询
set statement_timeout = '30s';

-- 或按会话设置
set local statement_timeout = '5s';
```

参考：[事务管理](https://www.postgresql.org/docs/current/tutorial-transactions.html)
