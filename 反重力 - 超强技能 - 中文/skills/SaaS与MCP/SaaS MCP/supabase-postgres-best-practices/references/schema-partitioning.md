---
title: 对大表进行分区以提升性能
impact: MEDIUM-HIGH
impactDescription: 大表查询和维护加速 5-20 倍
tags: partitioning, large-tables, time-series, performance
---

## 对大表进行分区以提升性能

分区将大表拆分为更小的部分，改善查询性能和维护操作。

**错误做法（单个大表）：**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz,
  data jsonb
);

-- 5 亿行，查询扫描所有内容
select * from events where created_at > '2024-01-01';  -- 很慢
vacuum events;  -- 需要数小时，锁定表
```

**正确做法（按时间范围分区）：**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz not null,
  data jsonb
) partition by range (created_at);

-- 为每个月创建分区
create table events_2024_01 partition of events
  for values from ('2024-01-01') to ('2024-02-01');

create table events_2024_02 partition of events
  for values from ('2024-02-01') to ('2024-03-01');

-- 查询仅扫描相关分区
select * from events where created_at > '2024-01-15';  -- 仅扫描 events_2024_01+

-- 瞬间删除旧数据
drop table events_2023_01;  -- 瞬间完成，而 DELETE 需要数小时
```

何时分区：

- 表超过 1 亿行
- 带有基于日期查询的时序数据
- 需要高效删除旧数据

参考：[表分区](https://www.postgresql.org/docs/current/ddl-partitioning.html)
