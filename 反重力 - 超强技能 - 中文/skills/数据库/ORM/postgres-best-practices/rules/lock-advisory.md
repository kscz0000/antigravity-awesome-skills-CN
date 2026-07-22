---
title: 使用 Advisory Lock 实现应用级锁定
impact: MEDIUM
impactDescription: 无需行级锁开销的高效协调
tags: advisory-locks, coordination, application-locks
---

## 使用 Advisory Lock 实现应用级锁定

Advisory lock 提供应用级协调，无需锁定数据库行。

**错误（仅为锁定创建行）：**

```sql
-- 创建虚拟行用于锁定
create table resource_locks (
  resource_name text primary key
);

insert into resource_locks values ('report_generator');

-- 通过选择行来锁定
select * from resource_locks where resource_name = 'report_generator' for update;
```

**正确（Advisory lock）：**

```sql
-- 会话级 advisory lock（断开连接或解锁时释放）
select pg_advisory_lock(hashtext('report_generator'));
-- ... 执行独占工作 ...
select pg_advisory_unlock(hashtext('report_generator'));

-- 事务级锁（提交/回滚时释放）
begin;
select pg_advisory_xact_lock(hashtext('daily_report'));
-- ... 执行工作 ...
commit;  -- 锁自动释放
```

非阻塞操作的 try-lock：

```sql
-- 立即返回 true/false 而非等待
select pg_try_advisory_lock(hashtext('resource_name'));

-- 在应用中使用
if (acquired) {
  -- 执行工作
  select pg_advisory_unlock(hashtext('resource_name'));
} else {
  -- 跳过或稍后重试
}
```

参考：[Advisory Locks](https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS)
