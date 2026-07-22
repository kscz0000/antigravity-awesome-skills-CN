---
title: 使用 SKIP LOCKED 实现非阻塞队列处理
impact: MEDIUM-HIGH
impactDescription: 工作队列吞吐量提升 10 倍
tags: skip-locked, queue, workers, concurrency
---

## 使用 SKIP LOCKED 实现非阻塞队列处理

当多个工作线程处理队列时，SKIP LOCKED 允许工作线程处理不同的行而无需等待。

**错误做法（工作线程互相阻塞）：**

```sql
-- 工作线程 1 和工作线程 2 都尝试获取下一个任务
begin;
select * from jobs where status = 'pending' order by created_at limit 1 for update;
-- 工作线程 2 等待工作线程 1 的锁释放！
```

**正确做法（SKIP LOCKED 并行处理）：**

```sql
-- 每个工作线程跳过已锁定的行并获取下一个可用行
begin;
select * from jobs
where status = 'pending'
order by created_at
limit 1
for update skip locked;

-- 工作线程 1 获得任务 1，工作线程 2 获得任务 2（无需等待）

update jobs set status = 'processing' where id = $1;
commit;
```

完整队列模式：

```sql
-- 单条语句原子领取并更新
update jobs
set status = 'processing', worker_id = $1, started_at = now()
where id = (
  select id from jobs
  where status = 'pending'
  order by created_at
  limit 1
  for update skip locked
)
returning *;
```

参考：[SELECT FOR UPDATE SKIP LOCKED](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)
