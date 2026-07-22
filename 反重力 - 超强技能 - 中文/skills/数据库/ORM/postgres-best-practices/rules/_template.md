---
title: 清晰、面向操作的标题（如"对过滤查询使用部分索引"）
impact: MEDIUM
impactDescription: 过滤查询提速 5-20 倍
tags: indexes, query-optimization, performance
---

## [规则标题]

[1-2 句说明问题及其重要性。聚焦性能影响。]

**错误（描述问题）：**

```sql
-- 注释说明为什么这样写慢/有问题
CREATE INDEX users_email_idx ON users(email);

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- 这会不必要地扫描已删除的记录
```

**正确（描述方案）：**

```sql
-- 注释说明为什么这样更好
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- 仅为活跃用户建索引，索引小 10 倍，查询更快
```

[可选：补充上下文、边界情况或权衡取舍]

Reference: [Postgres 文档](https://www.postgresql.org/docs/current/)
