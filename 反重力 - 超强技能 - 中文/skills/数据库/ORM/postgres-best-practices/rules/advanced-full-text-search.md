---
title: 使用 tsvector 实现全文搜索
impact: MEDIUM
impactDescription: 比 LIKE 快 100 倍，支持排序
tags: full-text-search, tsvector, gin, search
---

## 使用 tsvector 实现全文搜索

带通配符的 LIKE 无法使用索引。使用 tsvector 的全文搜索快几个数量级。

**错误（LIKE 模式匹配）：**

```sql
-- 无法使用索引，扫描所有行
select * from articles where content like '%postgresql%';

-- 不区分大小写更糟
select * from articles where lower(content) like '%postgresql%';
```

**正确（使用 tsvector 的全文搜索）：**

```sql
-- 添加 tsvector 列和索引
alter table articles add column search_vector tsvector
  generated always as (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))) stored;

create index articles_search_idx on articles using gin (search_vector);

-- 快速全文搜索
select * from articles
where search_vector @@ to_tsquery('english', 'postgresql & performance');

-- 带排序
select *, ts_rank(search_vector, query) as rank
from articles, to_tsquery('english', 'postgresql') query
where search_vector @@ query
order by rank desc;
```

多词搜索：

```sql
-- AND: 两个词都需要
to_tsquery('postgresql & performance')

-- OR: 任一词
to_tsquery('postgresql | mysql')

-- 前缀匹配
to_tsquery('post:*')
```

参考：[全文搜索](https://supabase.com/docs/guides/database/full-text-search)
