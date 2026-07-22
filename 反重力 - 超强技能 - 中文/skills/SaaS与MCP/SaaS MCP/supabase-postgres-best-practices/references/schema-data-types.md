---
title: 选择合适的数据类型
impact: HIGH
impactDescription: 存储减少 50%，比较更快
tags: data-types, schema, storage, performance
---

## 选择合适的数据类型

使用正确的数据类型可减少存储、提高查询性能并防止 bug。

**错误做法（错误的数据类型）：**

```sql
create table users (
  id int,                    -- 会在 21 亿时溢出
  email varchar(255),        -- 不必要的长度限制
  created_at timestamp,      -- 缺少时区信息
  is_active varchar(5),      -- 用字符串表示布尔值
  price varchar(20)          -- 用字符串表示数值
);
```

**正确做法（合适的数据类型）：**

```sql
create table users (
  id bigint generated always as identity primary key,  -- 最大 9 百亿亿
  email text,                     -- 无人为限制，与 varchar 性能相同
  created_at timestamptz,         -- 始终存储带时区的时间戳
  is_active boolean default true, -- 1 字节 vs 可变字符串长度
  price numeric(10,2)             -- 精确的十进制运算
);
```

关键指南：

```sql
-- ID：使用 bigint，而非 int（面向未来）
-- 字符串：使用 text，而非 varchar(n)（除非需要约束）
-- 时间：使用 timestamptz，而非 timestamp
-- 金额：使用 numeric，而非 float（精度很重要）
-- 枚举：使用带检查约束的 text 或创建枚举类型
```

参考：[数据类型](https://www.postgresql.org/docs/current/datatype.html)
