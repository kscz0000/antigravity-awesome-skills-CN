---
title: 批量 INSERT 语句用于大量数据
impact: MEDIUM
impactDescription: 批量插入加速 10-50 倍
tags: batch, insert, bulk, performance, copy
---

## 批量 INSERT 语句用于大量数据

单独的 INSERT 语句开销很大。在单条语句中批量插入多行或使用 COPY。

**错误做法（逐条插入）：**

```sql
-- 每次插入是单独的事务和往返
insert into events (user_id, action) values (1, 'click');
insert into events (user_id, action) values (1, 'view');
insert into events (user_id, action) values (2, 'click');
-- ... 还有 1000 条单独插入

-- 1000 次插入 = 1000 次往返 = 很慢
```

**正确做法（批量插入）：**

```sql
-- 单条语句中插入多行
insert into events (user_id, action) values
  (1, 'click'),
  (1, 'view'),
  (2, 'click'),
  -- ... 每批最多约 1000 行
  (999, 'view');

-- 1000 行只需一次往返
```

对于大型导入，使用 COPY：

```sql
-- COPY 是最快的批量加载方式
copy events (user_id, action, created_at)
from '/path/to/data.csv'
with (format csv, header true);

-- 或从应用的标准输入
copy events (user_id, action) from stdin with (format csv);
1,click
1,view
2,click
\.
```

参考：[COPY](https://www.postgresql.org/docs/current/sql-copy.html)
