---
title: 使用 SKIP LOCKED 实现非阻塞队列处理
impact: MEDIUM-HIGH
impactDescription: 工作队列吞吐量提升 10 倍
tags: skip-locked, queue, workers, concurrency
---

## 使用 SKIP LOCKED 实现非阻塞队列处理

当多个工作者处理队列时，SKIP LOCKED 允许工作者处理不同行而无需等待。

**错误（工作者互相阻塞）：**

```sql
-- Worker 1 和 Worker 2 都尝试获取下一个任务
begin;
select * from jobs where status = 'pending' order by created_at limit 1 for update;
-- Worker 2 等待 Worker 1 释放锁！
```

**正确（SKIP LOCKED 实现并行处理）：**

```sql
-- 每个工作者跳过已锁定的行，获取下一个可用的
begin;
select * from jobs
where status = 'pending'
order by created_at
limit 1
for update skip locked;

-- Worker 1 获取任务 1，Worker 2 获取任务 2（无需等待）

update jobs set status = 'processing' where id = $1;
commit;
```

完整队列模式：

```sql
-- 单条语句原子性获取并更新
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
