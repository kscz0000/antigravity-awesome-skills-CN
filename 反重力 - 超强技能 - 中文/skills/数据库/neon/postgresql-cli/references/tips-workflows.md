# psql 提示 — 工作流与模式

psql 提示参考的一部分。另见：tips-advanced.md

充分发挥 psql 作用的实用工作流和常见模式。

## 目录

- [\d 命令中的模式匹配](#d-命令中的模式匹配)
- [常见工作流](#常见工作流)
- [脚本模式](#脚本模式)
- [脚本与自动化的输出](#脚本与自动化的输出)
- [数据导入/导出模式](#数据导入导出模式)

---

## \d 命令中的模式匹配

所有接受模式参数的 `\d` 命令使用相同的匹配规则。理解这些规则是高效探索数据库的关键。

### 模式语法

| 模式 | 含义 | 示例 |
| ---- | ---- | ---- |
| `*` | 任意字符序列 | `\dt user*` 匹配 `users`、`user_accounts` |
| `?` | 任意单个字符 | `\dt user?` 匹配 `users` 但不匹配 `user_accounts` |
| `.` | 分隔模式与对象 | `\dt public.*` 列出 `public` 中的所有表 |

### 匹配工作方式

1. **点号表示法**：如果模式包含点号，点号前的部分匹配模式名，点号后的部分匹配对象名。`\dt public.users` 表示 schema=`public`、table=`users`。

2. **无点号**：匹配当前 `search_path` 上各模式中的对象。`\dt users` 在任何可搜索模式中查找 `users`。

3. **通配符展开**：`*` 和 `?` 被展开为正则表达式：
   - `*` 变为 `.*`（任意字符）
   - `?` 变为 `.`（单个字符）
   - `[0-9]` 等高级正则语法可用于字符类
   - 模式位置的 `.` 是模式/对象分隔符（非正则的任意字符）
   - `$` 按字面匹配（非正则锚点）

4. **大小写折叠**：模式中不带引号的字母折叠为小写（匹配 SQL 标识符行为）。`\dt FOO` 查找表 `foo`。双引号阻止折叠：`\dt "FOO"` 查找表 `FOO`（而非 `foo`）。

### 实用示例

```sql
-- All tables in any schema containing "user"
\dt *.user*

-- All tables in the public schema
\dt public.*

-- All tables starting with "order" in any schema
\dt *.order*

-- Detail view of a specific table
\d+ public.users

-- All indexes on tables starting with "user"
\di user*

-- All functions in the public schema
\df public.*

-- All materialized views
\dm

-- Check table size and description
\dt+ public.*
```

---

## 常见工作流

### 探索新数据库

```sql
-- Step 1: What databases exist?
\l

-- Step 2: Connect to one
\c mydb

-- Step 3: What schemas are there?
\dn

-- Step 4: What tables exist?
\dt

-- Step 5: What does this table look like?
\d users

-- Step 6: Any indexes?
\di

-- Step 7: Any views?
\dv

-- Step 8: What functions exist?
\df

-- Step 9: What extensions are installed?
\dx

-- Step 10: Check current settings
SHOW all;
```

### 理解表结构

```sql
-- Basic structure: columns, types, nullable, defaults
\d table_name

-- Detailed: everything above plus indexes, constraints, triggers, storage info
\d+ table_name

-- Just the indexes
\di table_name*

-- Just the foreign keys (shown in \d output)
\d table_name
-- Look for "Foreign-key constraints" section

-- Column comments
\dS+ table_name  -- includes system columns

-- Storage details (toast, compression)
\d+ table_name
```

### 检查查询性能

```sql
-- Enable timing
\timing on

-- See the execution plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- See what the optimizer actually does
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- Check current activity
SELECT * FROM pg_stat_activity WHERE state = 'active';

-- Watch a query
SELECT pg_size_pretty(pg_database_size(current_database()));
\watch 60
```

### 手动管理事务

```sql
\set AUTOCOMMIT off

BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

\set AUTOCOMMIT on
```

---

## 脚本模式

### 安全脚本模板

```sql
-- Always start with this in scripts
\set ON_ERROR_STOP on
\set VERBOSITY verbose

-- Optional: echo commands for debugging
\set ECHO all

-- Your migration or operations go here
BEGIN;

ALTER TABLE users ADD COLUMN IF NOT EXISTS phone varchar(20);

COMMIT;
```

### 条件执行

```sql
-- \if evaluates its argument as a boolean (true/false/1/0/on/off/yes/no)
-- For string comparison, use SQL to set a boolean variable:
SELECT current_setting('is_production', true) = 'true' AS is_prod \gset
\if :is_prod
  \echo 'WARNING: Running on PRODUCTION'
  -- \if only accepts boolean values. To check user input for a specific string,
  -- use SQL to produce a boolean result:
  \prompt 'Type YES to continue: ' confirm
  SELECT :'confirm' = 'YES' AS confirmed \gset
  \if :confirmed
    \echo 'Continuing...'
  \else
    \echo 'Aborted.'
  \endif
\endif

-- Check if a variable is defined using :{?varname}
\if :{?required_var}
  \echo 'required_var is set to:' :required_var
\else
  \echo 'ERROR: required_var is not defined. Aborting.'
  \q
\endif
```

### 使用 \gexec 动态生成 SQL

```sql
-- Generate and execute ANALYZE for all tables
SELECT 'ANALYZE ' || schemaname || '.' || tablename
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
\gexec

-- Generate GRANT statements
SELECT 'GRANT SELECT ON ' || tablename || ' TO readonly;'
FROM pg_tables
WHERE schemaname = 'public';
\gexec

-- Create partition tables dynamically
SELECT 'CREATE TABLE measurements_' || to_char(d, 'YYYY_MM') ||
       ' PARTITION OF measurements FOR VALUES FROM (''' ||
       to_char(d, 'YYYY-MM-01') || ''') TO (''' ||
       to_char(d + interval '1 month', 'YYYY-MM-01') || ''');'
FROM generate_series('2024-01-01'::date, '2024-12-01'::date, '1 month') AS d;
\gexec
```

### 反引号展开（Shell 命令替换）

元命令参数中包含在反引号（`` ` ``）内的文本作为 shell 命令执行，其输出替换反引号文本。这允许从操作系统向 psql 注入动态值：

```sql
-- Inject current date into a variable
\set report_date `date +%Y-%m-%d`
\echo :report_date
-- outputs: 2026-04-02

-- Use shell output in a file path
\o /tmp/query_output_`date +%Y%m%d_%H%M%S`.csv
SELECT * FROM users;
\o

-- Show system information
\echo 'Running as user: ' `whoami`
\echo 'Hostname: ' `hostname`

-- Use shell arithmetic
\set batch_size `echo 1000`
SELECT * FROM users LIMIT :batch_size;

-- Combine with \setenv for dynamic configuration
\setenv PAGER `which less`
```

**限制**：

- 反引号展开不会在单引号字符串内执行
- 不会在被 `\if`/`\else`/`\elif` 跳过的行中执行
- 不会在 `\copy` 参数中执行（整行按字面取值）

**反引号内的变量展开**：psql 变量引用（`:varname`、`:'varname'`）在 shell 命令执行之前于反引号文本内展开。`:'varname'` 形式更受推荐，因为它正确转义特殊字符以保证 shell 安全。但是，如果变量值包含回车或换行字符，`:'varname'` 会报错。

```sql
-- Get table count and use it
SELECT count(*) as user_count FROM users;
\gset
\echo 'Total users: ' :user_count

-- Get max ID and use in next query
SELECT max(id) as max_id FROM orders;
\gset
SELECT * FROM orders WHERE id > :max_id - 10;

-- Prefix to avoid collisions
SELECT oid, relname FROM pg_class WHERE relname = 'users';
\gset pg_
\echo 'OID of users table: ' :pg_oid
```

### 包含其他脚本

```sql
-- Relative to current working directory
\i init/001_schema.sql
\i init/002_seed.sql
\i init/003_permissions.sql

-- Relative to this file's location (better for portability)
\ir ../shared/helpers.sql
```

### 循环模式（使用 shell）

```bash
# Not a psql feature, but a common pattern combining shell and psql
for table in users orders products; do
  psql -c "SELECT count(*) FROM $table" mydb
done
```

---

## 脚本与自动化的输出

### 机器可读输出

```bash
# CSV output
psql -A -F ',' -t -c "SELECT id, name FROM users" mydb

# TSV output
psql -A -F $'\t' -t -c "SELECT id, name FROM users" mydb

# Single value (no header, no border)
psql -A -t -c "SELECT count(*) FROM users" mydb

# JSON output (use PostgreSQL's JSON functions)
psql -A -t -c "SELECT json_agg(t) FROM (SELECT id, name FROM users) t" mydb

# NUL-separated (for xargs -0)
# WARNING: Ensure filenames from the database are trusted before piping to destructive commands
psql -A -0 -t -c "SELECT filename FROM files_to_process" mydb | xargs -0 process_file
```

### 会话内输出控制

```sql
-- Quick CSV dump
\pset format csv
\o /tmp/output.csv
SELECT id, name, email FROM users;
\o
\pset format aligned

-- Using \g options (no need to change global settings)
SELECT * FROM users \g (format=csv footer=off) /tmp/users.csv

-- Pipe to a command
SELECT pg_database_size(current_database()) \g | numfmt --to=iec

-- Unaligned for quick copy-paste
\a
\t on
SELECT string_agg(column_name, ', ') FROM information_schema.columns WHERE table_name = 'users';
\t off
\a
```

---

## 数据导入/导出模式

### CSV 导入

```sql
-- Standard CSV import
\copy table_name FROM 'data.csv' WITH (FORMAT csv, HEADER true)

-- Custom delimiter
\copy table_name FROM 'data.tsv' WITH (FORMAT csv, HEADER true, DELIMITER E'\t')

-- Handle NULLs
\copy table_name FROM 'data.csv' WITH (FORMAT csv, HEADER true, NULL 'N/A')

-- Specific columns only
\copy table_name (col1, col2, col3) FROM 'partial.csv' WITH (FORMAT csv, HEADER true)
```

### CSV 导出

```sql
-- Full table export
\copy table_name TO 'export.csv' WITH (FORMAT csv, HEADER true)

-- Query export
\copy (SELECT id, name, created_at FROM users WHERE active ORDER BY created_at DESC) TO 'active_users.csv' WITH (FORMAT csv, HEADER true)

-- Compressed export (pipe through gzip, no intermediate file)
\copy table_name TO program 'gzip > export.csv.gz' WITH (FORMAT csv, HEADER true)-- Import from compressed (decompress on the fly)
\copy table_name FROM program 'gzip -dc import.csv.gz' WITH (FORMAT csv, HEADER true)
```

### 服务器间的数据库迁移

```bash
# Dump and restore via pipe (no intermediate file)
pg_dump -Fc source_db | pg_restore -d target_db

# Schema-only dump
pg_dump --schema-only source_db | psql target_db

# Data-only with parallel jobs
pg_dump -j4 -Fd source_db -f /tmp/dump_dir
pg_restore -j4 -d target_db /tmp/dump_dir
```
