# SQL 优化模式实现手册

本文件包含该技能引用的详细模式、清单和代码示例。

# SQL 优化模式

通过系统化优化、合理索引和查询计划分析，将缓慢的数据库查询转变为闪电般快速的操作。

## 不要使用此技能的情况

- 任务与 SQL 优化模式无关
- 你需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 何时使用此技能

- 调试运行缓慢的查询
- 设计高性能数据库模式
- 优化应用响应时间
- 降低数据库负载和成本
- 提升不断增长的数据集的可扩展性
- 分析 EXPLAIN 查询计划
- 实现高效索引
- 解决 N+1 查询问题

## 核心概念

### 1. 查询执行计划（EXPLAIN）

理解 EXPLAIN 输出是优化的基础。

**PostgreSQL EXPLAIN：**
```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- With actual execution stats
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'user@example.com';

-- Verbose output with more details
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.*, o.order_total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days';
```

**关键指标：**
- **Seq Scan**：全表扫描（大表通常较慢）
- **Index Scan**：使用索引（良好）
- **Index Only Scan**：使用索引而不访问表（最佳）
- **Nested Loop**：连接方法（适用于小数据集）
- **Hash Join**：连接方法（适用于较大数据集）
- **Merge Join**：连接方法（适用于已排序数据）
- **Cost**：估计查询成本（越低越好）
- **Rows**：估计返回行数
- **Actual Time**：实际执行时间

### 2. 索引策略

索引是最强大的优化工具。

**索引类型：**
- **B-Tree**：默认类型，适用于等值和范围查询
- **Hash**：仅用于等值（=）比较
- **GIN**：全文搜索、数组查询、JSONB
- **GiST**：几何数据、全文搜索
- **BRIN**：块范围索引，适用于具有相关性的超大表

```sql
-- Standard B-Tree index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index (index subset of rows)
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Covering index (include additional columns)
CREATE INDEX idx_users_email_covering ON users(email)
INCLUDE (name, created_at);

-- Full-text search index
CREATE INDEX idx_posts_search ON posts
USING GIN(to_tsvector('english', title || ' ' || body));

-- JSONB index
CREATE INDEX idx_metadata ON events USING GIN(metadata);
```

### 3. 查询优化模式

**避免 SELECT \*：**
```sql
-- Bad: Fetches unnecessary columns
SELECT * FROM users WHERE id = 123;

-- Good: Fetch only what you need
SELECT id, email, name FROM users WHERE id = 123;
```

**高效使用 WHERE 子句：**
```sql
-- Bad: Function prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good: Create functional index or use exact match
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
-- Then:
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Or store normalized data
SELECT * FROM users WHERE email = 'user@example.com';
```

**优化 JOIN：**
```sql
-- Bad: Cartesian product then filter
SELECT u.name, o.total
FROM users u, orders o
WHERE u.id = o.user_id AND u.created_at > '2024-01-01';

-- Good: Filter before join
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- Better: Filter both tables
SELECT u.name, o.total
FROM (SELECT * FROM users WHERE created_at > '2024-01-01') u
JOIN orders o ON u.id = o.user_id;
```

## 优化模式

### 模式 1：消除 N+1 查询

**问题：N+1 查询反模式**
```python
# Bad: Executes N+1 queries
users = db.query("SELECT * FROM users LIMIT 10")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)
    # Process orders
```

**解决方案：使用 JOIN 或批量加载**
```sql
-- Solution 1: JOIN
SELECT
    u.id, u.name,
    o.id as order_id, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id IN (1, 2, 3, 4, 5);

-- Solution 2: Batch query
SELECT * FROM orders
WHERE user_id IN (1, 2, 3, 4, 5);
```

```python
# Good: Single query with JOIN or batch load
# Using JOIN
results = db.query("""
    SELECT u.id, u.name, o.id as order_id, o.total
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.id IN (1, 2, 3, 4, 5)
""")

# Or batch load
users = db.query("SELECT * FROM users LIMIT 10")
user_ids = [u.id for u in users]
orders = db.query(
    "SELECT * FROM orders WHERE user_id IN (?)",
    user_ids
)
# Group orders by user_id
orders_by_user = {}
for order in orders:
    orders_by_user.setdefault(order.user_id, []).append(order)
```

### 模式 2：优化分页

**错误做法：在大表上使用 OFFSET**
```sql
-- Slow for large offsets
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;  -- Very slow!
```

**正确做法：基于游标的分页**
```sql
-- Much faster: Use cursor (last seen ID)
SELECT * FROM users
WHERE created_at < '2024-01-15 10:30:00'  -- Last cursor
ORDER BY created_at DESC
LIMIT 20;

-- With composite sorting
SELECT * FROM users
WHERE (created_at, id) < ('2024-01-15 10:30:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Requires index
CREATE INDEX idx_users_cursor ON users(created_at DESC, id DESC);
```

### 模式 3：高效聚合

**优化 COUNT 查询：**
```sql
-- Bad: Counts all rows
SELECT COUNT(*) FROM orders;  -- Slow on large tables

-- Good: Use estimates for approximate counts
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'orders';

-- Good: Filter before counting
SELECT COUNT(*) FROM orders
WHERE created_at > NOW() - INTERVAL '7 days';

-- Better: Use index-only scan
CREATE INDEX idx_orders_created ON orders(created_at);
SELECT COUNT(*) FROM orders
WHERE created_at > NOW() - INTERVAL '7 days';
```

**优化 GROUP BY：**
```sql
-- Bad: Group by then filter
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 10;

-- Better: Filter first, then group (if possible)
SELECT user_id, COUNT(*) as order_count
FROM orders
WHERE status = 'completed'
GROUP BY user_id
HAVING COUNT(*) > 10;

-- Best: Use covering index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### 模式 4：子查询优化

**转换关联子查询：**
```sql
-- Bad: Correlated subquery (runs for each row)
SELECT u.name, u.email,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- Good: JOIN with aggregation
SELECT u.name, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name, u.email;

-- Better: Use window functions
SELECT DISTINCT ON (u.id)
    u.name, u.email,
    COUNT(o.id) OVER (PARTITION BY u.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
```

**使用 CTE 提升可读性：**
```sql
-- Using Common Table Expressions
WITH recent_users AS (
    SELECT id, name, email
    FROM users
    WHERE created_at > NOW() - INTERVAL '30 days'
),
user_order_counts AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT ru.name, ru.email, COALESCE(uoc.order_count, 0) as orders
FROM recent_users ru
LEFT JOIN user_order_counts uoc ON ru.id = uoc.user_id;
```

### 模式 5：批量操作

**批量 INSERT：**
```sql
-- Bad: Multiple individual inserts
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Carol', 'carol@example.com');

-- Good: Batch insert
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com');

-- Better: Use COPY for bulk inserts (PostgreSQL)
COPY users (name, email) FROM '/tmp/users.csv' CSV HEADER;
```

**批量 UPDATE：**
```sql
-- Bad: Update in loop
UPDATE users SET status = 'active' WHERE id = 1;
UPDATE users SET status = 'active' WHERE id = 2;
-- ... repeat for many IDs

-- Good: Single UPDATE with IN clause
UPDATE users
SET status = 'active'
WHERE id IN (1, 2, 3, 4, 5, ...);

-- Better: Use temporary table for large batches
CREATE TEMP TABLE temp_user_updates (id INT, new_status VARCHAR);
INSERT INTO temp_user_updates VALUES (1, 'active'), (2, 'active'), ...;

UPDATE users u
SET status = t.new_status
FROM temp_user_updates t
WHERE u.id = t.id;
```

## 高级技术

### 物化视图

预计算昂贵的查询。

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT
    u.id,
    u.name,
    COUNT(o.id) as total_orders,
    SUM(o.total) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Add index to materialized view
CREATE INDEX idx_user_summary_spent ON user_order_summary(total_spent DESC);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW user_order_summary;

-- Concurrent refresh (PostgreSQL)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_order_summary;

-- Query materialized view (very fast)
SELECT * FROM user_order_summary
WHERE total_spent > 1000
ORDER BY total_spent DESC;
```

### 分区

拆分大表以提升性能。

```sql
-- Range partitioning by date (PostgreSQL)
CREATE TABLE orders (
    id SERIAL,
    user_id INT,
    total DECIMAL,
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Queries automatically use appropriate partition
SELECT * FROM orders
WHERE created_at BETWEEN '2024-02-01' AND '2024-02-28';
-- Only scans orders_2024_q1 partition
```

### 查询提示与优化

```sql
-- Force index usage (MySQL)
SELECT * FROM users
USE INDEX (idx_users_email)
WHERE email = 'user@example.com';

-- Parallel query (PostgreSQL)
SET max_parallel_workers_per_gather = 4;
SELECT * FROM large_table WHERE condition;

-- Join hints (PostgreSQL)
SET enable_nestloop = OFF;  -- Force hash or merge join
```

## 最佳实践

1. **选择性索引**：过多索引会拖慢写入速度
2. **监控查询性能**：使用慢查询日志
3. **保持统计信息更新**：定期运行 ANALYZE
4. **使用合适的数据类型**：更小的类型 = 更好的性能
5. **合理规范化**：平衡规范化与性能
6. **缓存频繁访问的数据**：使用应用级缓存
7. **连接池**：复用数据库连接
8. **定期维护**：VACUUM、ANALYZE、重建索引

```sql
-- Update statistics
ANALYZE users;
ANALYZE VERBOSE orders;

-- Vacuum (PostgreSQL)
VACUUM ANALYZE users;
VACUUM FULL users;  -- Reclaim space (locks table)

-- Reindex
REINDEX INDEX idx_users_email;
REINDEX TABLE users;
```

## 常见陷阱

- **过度索引**：每个索引都会拖慢 INSERT/UPDATE/DELETE
- **未使用的索引**：浪费空间并拖慢写入
- **缺失索引**：查询缓慢、全表扫描
- **隐式类型转换**：阻止索引使用
- **OR 条件**：无法高效使用索引
- **前导通配符的 LIKE**：`LIKE '%abc'` 无法使用索引
- **WHERE 中的函数**：阻止索引使用，除非存在函数索引

## 监控查询

```sql
-- Find slow queries (PostgreSQL)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Find missing indexes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan AS avg_seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;

-- Find unused indexes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

## 参考资料

- **references/postgres-optimization-guide.md**：PostgreSQL 特定优化
- **references/mysql-optimization-guide.md**：MySQL/MariaDB 优化
- **references/query-plan-analysis.md**：深入分析 EXPLAIN 计划
- **assets/index-strategy-checklist.md**：何时以及如何创建索引
- **assets/query-optimization-checklist.md**：逐步优化指南
- **scripts/analyze-slow-queries.sql**：识别数据库中的慢查询
- **scripts/index-recommendations.sql**：生成索引建议
