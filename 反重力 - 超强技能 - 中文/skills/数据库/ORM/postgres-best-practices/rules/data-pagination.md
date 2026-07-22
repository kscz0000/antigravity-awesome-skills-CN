---
title: 使用游标分页代替 OFFSET
impact: MEDIUM-HIGH
impactDescription: 无论页深度如何，始终保持 O(1) 性能
tags: pagination, cursor, keyset, offset, performance
---

## 使用游标分页代替 OFFSET

基于 OFFSET 的分页会扫描所有跳过的行，页越深越慢。游标分页是 O(1)。

**错误（OFFSET 分页）：**

```sql
-- 第 1 页：扫描 20 行
select * from products order by id limit 20 offset 0;

-- 第 100 页：扫描 2000 行以跳过 1980 行
select * from products order by id limit 20 offset 1980;

-- 第 10000 页：扫描 200,000 行！
select * from products order by id limit 20 offset 199980;
```

**正确（游标/键集分页）：**

```sql
-- 第 1 页：获取前 20 条
select * from products order by id limit 20;
-- 应用存储 last_id = 20

-- 第 2 页：从最后一个 ID 之后开始
select * from products where id > 20 order by id limit 20;
-- 使用索引，无论页深度如何始终快速

-- 第 10000 页：与第 1 页速度相同
select * from products where id > 199980 order by id limit 20;
```

多列排序：

```sql
-- 游标必须包含所有排序列
select * from products
where (created_at, id) > ('2024-01-15 10:00:00', 12345)
order by created_at, id
limit 20;
```

参考：[分页](https://supabase.com/docs/guides/database/pagination)
