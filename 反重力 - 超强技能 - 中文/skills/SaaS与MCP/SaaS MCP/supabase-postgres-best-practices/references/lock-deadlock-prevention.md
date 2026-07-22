---
title: 通过一致的锁顺序防止死锁
impact: MEDIUM-HIGH
impactDescription: 消除死锁错误，提高可靠性
tags: deadlocks, locking, transactions, ordering
---

## 通过一致的锁顺序防止死锁

当事务以不同顺序锁定资源时会发生死锁。始终以一致的顺序获取锁。

**错误做法（不一致的锁顺序）：**

```sql
-- 事务 A                    -- 事务 B
begin;                              begin;
update accounts                     update accounts
set balance = balance - 100         set balance = balance - 50
where id = 1;                       where id = 2;  -- B 锁定行 2

update accounts                     update accounts
set balance = balance + 100         set balance = balance + 50
where id = 2;  -- A 等待 B          where id = 1;  -- B 等待 A

-- 死锁！两者互相等待
```

**正确做法（先按一致顺序锁定行）：**

```sql
-- 在更新前按 ID 顺序显式获取锁
begin;
select * from accounts where id in (1, 2) order by id for update;

-- 现在可以按任意顺序更新 - 锁已持有
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;
```

替代方案：使用单条语句原子更新：

```sql
-- 单条语句原子获取所有锁
begin;
update accounts
set balance = balance + case id
  when 1 then -100
  when 2 then 100
end
where id in (1, 2);
commit;
```

检测日志中的死锁：

```sql
-- 检查最近的死锁
select * from pg_stat_database where deadlocks > 0;

-- 启用死锁日志
set log_lock_waits = on;
set deadlock_timeout = '1s';
```

参考：
[死锁](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS)
