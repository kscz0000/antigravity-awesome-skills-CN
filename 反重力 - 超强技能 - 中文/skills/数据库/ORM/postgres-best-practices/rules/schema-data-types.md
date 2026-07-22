---
title: 选择合适的数据类型
impact: HIGH
impactDescription: 存储减少 50%，比较操作更快
tags: data-types, schema, storage, performance
---

## 选择合适的数据类型

使用正确的数据类型可以减少存储、提升查询性能并防止 Bug。

**错误（错误的数据类型）：**

```sql
create table users (
  id int,                    -- 21 亿时溢出
  email varchar(255),        -- 不必要的长度限制
  created_at timestamp,      -- 缺少时区信息
  is_active varchar(5),      -- 字符串代替布尔值
  price varchar(20)          -- 字符串代替数值
);
```

**正确（合适的数据类型）：**

```sql
create table users (
  id bigint generated always as identity primary key,  -- 最大 9 百亿亿
  email text,                     -- 无人为限制，性能与 varchar 相同
  created_at timestamptz,         -- 始终存储带时区的时间戳
  is_active boolean default true, -- 1 字节 vs 可变字符串长度
  price numeric(10,2)             -- 精确十进制运算
);
```

关键指南：

```sql
-- ID: 用 bigint，不用 int（面向未来）
-- 字符串: 用 text，不用 varchar(n)，除非需要约束
-- 时间: 用 timestamptz，不用 timestamp
-- 金额: 用 numeric，不用 float（精度很重要）
-- 枚举: 用 text 加 check 约束，或创建 enum 类型
```

参考：[数据类型](https://www.postgresql.org/docs/current/datatype.html)
