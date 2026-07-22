---
title: 清晰、行动导向的标题（例如："对过滤查询使用部分索引"）
impact: MEDIUM
impactDescription: 过滤查询加速 5-20 倍
tags: indexes, query-optimization, performance
---

## [规则标题]

[1-2 句话解释问题及其重要性。聚焦性能影响。]

**错误做法（描述问题）：**

```sql
-- 注释解释为什么这很慢/有问题
CREATE INDEX users_email_idx ON users(email);

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- 这会扫描已删除的记录，造成不必要的开销
```

**正确做法（描述解决方案）：**

```sql
-- 注释解释为什么这更好
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- 仅索引活跃用户，索引小 10 倍，查询更快
```

[可选：附加上下文、边界情况或权衡]

参考：[Postgres 文档](https://www.postgresql.org/docs/current/)
