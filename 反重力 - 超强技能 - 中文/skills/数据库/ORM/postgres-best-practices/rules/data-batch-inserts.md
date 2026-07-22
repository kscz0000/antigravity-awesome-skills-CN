---
title: 批量 INSERT 语句处理大数据
impact: MEDIUM
impactDescription: 批量插入提速 10-50 倍
tags: batch, insert, bulk, performance, copy
---

## 批量 INSERT 语句处理大数据

单独的 INSERT 语句开销很高。在单条语句中批量插入多行或使用 COPY。

**错误（逐条插入）：**

```sql
-- 每次插入都是单独的事务和往返
insert into events (user_id, action) values (1, 'click');
insert into events (user_id, action) values (1, 'view');
insert into events (user_id, action) values (2, 'click');
-- ... 还有 1000 条单独插入

-- 1000 次插入 = 1000 次往返 = 慢
```

**正确（批量插入）：**

```sql
-- 单条语句插入多行
insert into events (user_id, action) values
  (1, 'click'),
  (1, 'view'),
  (2, 'click'),
  -- ... 每批最多约 1000 行
  (999, 'view');

-- 1000 行只需一次往返
```

大量导入使用 COPY：

```sql
-- COPY 是批量加载最快的
copy events (user_id, action, created_at)
from '/path/to/data.csv'
with (format csv, header true);

-- 或从 stdin 在应用中使用
copy events (user_id, action) from stdin with (format csv);
1,click
1,view
2,click
\.
```

参考：[COPY](https://www.postgresql.org/docs/current/sql-copy.html)
