# psql 提示 — 高级调试、性能与安全

psql 提示参考的一部分。另见：tips-workflows.md

用于调试、性能调优和 psql 安全使用的高级技巧。

## 目录

- [性能提示](#性能提示)
- [调试与内省](#调试与内省)
- [安全最佳实践](#安全最佳实践)
- [常见陷阱与错误](#常见陷阱与错误)

---

## 性能提示

### 大结果集

```sql
-- Don't load entire result into memory
\set FETCH_COUNT 1000
SELECT * FROM billion_row_table;

-- Use \copy instead of COPY for client-side operations
\copy huge_table TO '/data/export.csv' WITH (FORMAT csv)
```

### 批量操作使用管道模式

管道模式将多个查询批量打包为单次网络往返：

```sql
\startpipeline
  INSERT INTO logs (msg) VALUES ($1)
  \bind 'entry 1' \sendpipeline
  INSERT INTO logs (msg) VALUES ($1)
  \bind 'entry 2' \sendpipeline
  INSERT INTO logs (msg) VALUES ($1)
  \bind 'entry 3' \sendpipeline
  \getresults
\endpipeline
```

这将在一次网络往返中发送所有三个 INSERT，而非三次。

### 脚本执行

```bash
# Run in a single transaction (faster, and all-or-nothing)
psql -1 -f migration.sql mydb

# Multiple files sequentially
psql -1 -f 001.sql -f 002.sql -f 003.sql mydb
```

---

## 调试与内省

### 查看 psql 发送给服务器的内容

```sql
-- Echo all SQL commands
\set ECHO queries

-- See the SQL behind \d commands (incredibly useful for learning)
\set ECHO_HIDDEN on

-- Or in noexec mode (show but don't execute)
\set ECHO_HIDDEN noexec

-- Now run any \d command to see its SQL
\dt
\d users
```

### 检查查询计划

```sql
-- Basic plan
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- With actual execution time
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Detailed with buffer info
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) SELECT ...;

-- JSON format for tooling
EXPLAIN (FORMAT JSON) SELECT ...;
```

### 锁分析

```sql
-- Current locks waiting to be granted
SELECT * FROM pg_locks WHERE NOT granted;

-- Blocked sessions with their blockers (PostgreSQL 9.6+)
SELECT blocked.pid,
       blocked.query,
       pg_blocking_pids(blocked.pid) AS blocked_by_pids
FROM pg_stat_activity blocked
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;
```

---

## 安全最佳实践

### 始终在脚本中设置 ON_ERROR_STOP

没有 `ON_ERROR_STOP`，脚本在遇到错误后继续执行，可能导致数据库处于不一致状态：

```sql
-- Top of every script
\set ON_ERROR_STOP on
```

### 迁移使用单事务模式

```bash
# -1 wraps everything in BEGIN...COMMIT
# On error, the entire migration rolls back
psql -1 -f migration.sql mydb
```

### 永远不要在脚本中使用 PGPASSWORD

```bash
# BAD: Password visible in process list, env vars
PGPASSWORD=secret psql -c "SELECT 1" mydb# GOOD: Use ~/.pgpass (manually edit to avoid shell history)
touch ~/.pgpass && chmod 600 ~/.pgpass
# Then edit ~/.pgpass and your add:
# hostname:port:database:username:password
# Example: localhost:5432:mydb:myuser:mysecret
psql -c "SELECT 1" mydb
```

### 执行前预览

```sql
-- Dry-run a script to see what commands will execute (shows SQL, does NOT execute)
\set ECHO all
BEGIN;
-- Paste or review migration SQL here, then ROLLBACK instead of COMMIT
\i migration.sql
ROLLBACK;

-- Or use \gdesc to check result columns without executing
SELECT * FROM complex_view \gdesc
```

### 使用 \copy 而非 COPY

`\copy` 使用客户端权限和文件系统。SQL `COPY` 在服务器端运行，需要超级用户或 `pg_read_server_files`/`pg_write_server_files` 角色。`\copy` 通过客户端/服务器连接传输所有数据，对于非常大的数据集不如 SQL `COPY` 高效。当服务器端文件访问可用时，对于批量数据传输优先使用 SQL `COPY`。

```sql
-- BAD (requires server-side file access)
COPY users TO '/tmp/users.csv' WITH CSV HEADER;

-- GOOD (uses client-side file access)
\copy users TO '/tmp/users.csv' WITH CSV HEADER
```

### 针对不受信任用户的 search_path 安全

如果不受信任的用户可以访问数据库，在会话开始时从 `search_path` 中移除公开可写的模式：

```sql
SELECT pg_catalog.set_config('search_path', '', false);
```

### 自动 LISTEN/NOTIFY 轮询

每当执行命令时，psql 自动轮询由 `LISTEN`/`NOTIFY` 生成的异步通知事件。这无需任何特殊配置。

---

## 常见陷阱与错误

### \copy 中的分号

`\copy` 不以分号结尾。它是元命令：

```sql
-- CORRECT
\copy users TO '/tmp/users.csv' WITH CSV HEADER

-- WRONG (psql interprets the semicolon oddly)
\copy users TO '/tmp/users.csv' WITH CSV HEADER;
```

### 变量替换与 SQL 注入

psql 变量是简单的文本替换。它们不是参数化查询：

```sql
-- The :'varname' form (single-quoted) escapes embedded single quotes, making it
-- safe against SQL injection for STRING VALUES in WHERE clauses:
\set name "Robert'); DROP TABLE students;--"
SELECT * FROM users WHERE name = :'name';
-- Expands to: WHERE name = 'Robert''); DROP TABLE students;--'
-- The '' is an escaped quote, so the entire value is a single string literal — NOT injected.

-- However, :'varname' is NOT safe for identifiers or unquoted contexts.
-- For identifiers (table/column names), use :"varname" (double-quoted form).
-- For the safest parameterized queries, use \bind:
SELECT * FROM users WHERE name = $1;
\bind 'Robert' \g
```

### 错误后的事务状态

事务块中发生错误后，所有后续命令都会失败，直到 ROLLBACK：

```sql
BEGIN;
INSERT INTO users (id) VALUES (1);
INSERT INTO users (id) VALUES ('bad');  -- ERROR
INSERT INTO users (id) VALUES (2);      -- Also fails!
COMMIT;                                  -- Also fails!
```

使用 `ON_ERROR_ROLLBACK` 自动保存点：

```sql
\set ON_ERROR_ROLLBACK on
BEGIN;
INSERT INTO users (id) VALUES (1);
INSERT INTO users (id) VALUES ('bad');  -- ERROR, auto-rollback to savepoint
INSERT INTO users (id) VALUES (2);      -- This works now
COMMIT;
```

### 模式匹配使用正则表达式

\d 命令中的 `*` 和 `?` 被转换为正则表达式（`.*` 和 `.`）。`[0-9]` 等高级正则语法也可用。与标准正则的重要区别：

- `.` 是模式/对象分隔符，非任意字符（使用 `?` 匹配单个字符）
- `$` 按字面匹配，非锚点（模式必须匹配整个名称）
- 双引号内，所有特殊字符（`*`、`?`、正则字符）为字面值

```sql
-- These work as expected
\dt user*              -- matches users, user_accounts, etc.
\dt user?              -- matches users, user1, etc.
\dt user[0-9]*         -- matches user1, user2, user123

-- If your table name contains special chars, use double quotes
\dt "table.with.dots"  -- matches literally, dots not treated as separator
```

### 连接字符串与 CLI 参数

```bash
# These are equivalent
psql -h localhost -p 5432 -U admin -d mydb
psql "postgresql://admin@localhost:5432/mydb"

# But you can't mix freely — URI overrides individual flags
psql -h otherhost "postgresql://admin@localhost:5432/mydb"  -- uses localhost, not otherhost
```

### \i 与 \ir

- `\i filename` — 相对于**当前工作目录**（psql 启动位置）解析
- `\ir filename` — 相对于**当前执行的脚本所在目录**解析

脚本可移植性优先使用 `\ir`：

```sql
-- In /scripts/migrations/run_all.sql:
\ir 001_schema.sql    -- resolves to /scripts/migrations/001_schema.sql
\ir 002_data.sql      -- resolves to /scripts/migrations/002_data.sql
```

### \o 与查询输出

`\o` 重定向查询输出，而非元命令输出：

```sql
\o /tmp/output.txt
SELECT * FROM users;     -- goes to file
\d users                 -- also goes to file
\echo 'hello'            -- goes to STDOUT (not affected by \o)
\qecho 'hello'           -- goes to /tmp/output.txt (affected by \o)
```
