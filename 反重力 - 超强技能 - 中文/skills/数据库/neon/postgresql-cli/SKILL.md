---
name: postgresql-cli
description: PostgreSQL 交互式终端 (psql) 参考与使用指南。当用户提到 psql、PostgreSQL 命令行客户端、反斜杠命令、元命令、\d 命令、数据库检查、PostgreSQL 脚本编写、psql 导入/导出数据、\copy 时使用此技能。
risk: unknown
source: https://github.com/chaunsin/agent-skills/tree/master/skills/postgresql-cli
source_repo: chaunsin/agent-skills
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/chaunsin/agent-skills/blob/master/LICENSE
---

# psql — PostgreSQL 交互式终端

psql 是 PostgreSQL 功能丰富的交互式终端。它允许你在命令行中编写和执行查询、检查数据库对象、导入/导出数据、编写批处理脚本以及自定义输出格式。

## 前提条件

在使用 psql 之前，确认它已安装并可用：

```bash
# Check if psql is installed
psql --version

# If not found, install PostgreSQL client tools:

# macOS (Homebrew)
brew install libpq
brew link --force libpq

# Ubuntu / Debian
sudo apt install postgresql-client

# CentOS / RHEL
sudo yum install postgresql

# Alpine
apk add postgresql-client

# Windows — install PostgreSQL via the official installer or use WSL
```

psql 作为 `postgresql-client` 包的一部分发布。服务器端（`postgresql`）不是必需的——你只需要客户端即可连接远程 PostgreSQL 实例。

## 快速参考

### 连接

```
# 1. CLI flags
psql -h host -p port -U user -d dbname

# 2. Connection URI
# WARNING: Password in URI is visible in shell history and process listings.
#          Prefer ~/.pgpass for production use (see method 4 below).
psql "postgresql://user:YOUR_PASSWORD@host:port/dbname"

# 3. Environment variables (no flags needed)
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mydb
export PGUSER=postgres
# WARNING: PGPASSWORD is visible in process listings (e.g. `ps aux`).
#          Use ~/.pgpass in production instead.
export PGPASSWORD=YOUR_PASSWORD
psql                       # picks up all params from env

# 4. ~/.pgpass file (RECOMMENDED for passwords)
#    Format: hostname:port:database:username:password
touch ~/.pgpass && chmod 600 ~/.pgpass
# Then manually edit ~/.pgpass and add entries (avoids password in shell history):
# hostname:port:database:username:password
# Example: localhost:5432:mydb:postgres:YOUR_PASSWORD
psql -h localhost -U postgres -d mydb   # no password prompt

# 5. Execute and exit
psql -f script.sql dbname                        # execute file then exit
psql -c "SELECT 1" dbname                        # run single command then exit
psql -1 -f migration.sql dbname                  # run in single transaction

# 6. Service connection (reads from pg_service.conf)
psql service=mydb_prod

# 7. Reconnect within a session
\c dbname                                       # reconnect to different db
\c -reuse-previous=on sslmode=require           # change only sslmode
\c "host=newhost port=5432 dbname=mydb"         # conninfo string
```

连接失败时：交互模式保留前一个连接；脚本模式关闭连接，所有后续数据库命令将失败，直到下一次成功的 `\c`。

关键标志：`-h` 主机、`-p` 端口、`-U` 用户、`-d` 数据库、`-w` 不提示密码、`-W` 强制密码提示、`-1` 单事务、`-f` 执行文件、`-c` 执行命令、`-t` 仅元组、`-x` 展开模式、`-A` 非对齐、`-E` 显示隐藏查询（`\d` 内部查询）、`-L` 日志文件、`-X` 跳过 `~/.psqlrc`。

**连接优先级**：CLI 标志 > 环境变量 > `pg_service.conf` > 默认值。**密码优先级**：连接字符串/密码标志 > `PGPASSWORD` 环境变量 > `~/.pgpass`。在生产环境中使用 `~/.pgpass` 而非 `PGPASSWORD`——`PGPASSWORD` 在进程列表（`ps aux`）中可见。

### 对象检查（\d 家族）

| 命令             | 显示内容                                                                                             |
| ----------------- | ---------------------------------------------------------------------------------------------------- |
| `\d`            | 所有表、视图、物化视图、序列、外部表（等价于 `\dtvmsE`）                                            |
| `\dP`           | 分区表                                                                                               |
| `\dt`           | 仅表                                                                                                 |
| `\dv`           | 仅视图                                                                                               |
| `\di`           | 仅索引                                                                                               |
| `\ds`           | 仅序列                                                                                               |
| `\dm`           | 仅物化视图                                                                                           |
| `\det`          | 外部表（记忆法："external tables"）                                                                  |
| `\dT`           | 数据类型                                                                                             |
| `\df`           | 函数（使用修饰符：`a`=聚合、`n`=普通、`p`=过程、`t`=触发器、`w`=窗口）                            |
| `\da`           | 聚合函数                                                                                             |
| `\dn`           | 模式                                                                                                 |
| `\du` / `\dg` | 角色                                                                                                 |
| `\db`           | 表空间                                                                                               |
| `\dc`           | 转换                                                                                                 |
| `\dD`           | 域                                                                                                   |
| `\dl`           | 大对象（`\lo_list` 的别名）                                                                          |
| `\dF`           | 文本搜索配置                                                                                         |
| `\dFd`          | 文本搜索字典                                                                                         |
| `\dFp`          | 文本搜索解析器                                                                                       |
| `\dFt`          | 文本搜索模板                                                                                         |
| `\des`          | 外部服务器                                                                                           |
| `\deu`          | 用户映射                                                                                             |
| `\dew`          | 外部数据包装器                                                                                       |
| `\dp`           | 权限（GRANT/REVOKE）                                                                                 |
| `\drds`         | 每角色和每数据库的配置设置                                                                           |
| `\l`            | 列出数据库（接受模式：`\l test*`）                                                                   |

| `\dA`           | 访问方法                                                                                             |
| `\dAc` / `\dAf` / `\dAo` / `\dAp` | 操作符类、操作符族、操作符、支持函数                                 |
| `\dC`           | 类型转换                                                                                             |
| `\dconfig`      | 服务器配置参数（`\dconfig *` 显示全部，PostgreSQL 16+）                                              |
| `\dd`           | 对象描述（注释）                                                                                     |
| `\ddp`          | 默认权限                                                                                             |
| `\dL`           | 过程语言                                                                                             |
| `\do`           | 操作符（接受参数类型模式）                                                                           |
| `\dO`           | 排序规则                                                                                             |
| `\dP[itn]`      | 分区表（`t`=表、`i`=索引、`n`=嵌套）                                                                 |
| `\drg`          | 已授予的角色成员关系                                                                                 |
| `\dRp` / `\dRs` | 复制发布 / 订阅                                                                                      |
| `\dX`           | 扩展统计信息                                                                                         |
| `\dx`           | 已安装的扩展                                                                                         |
| `\dy`           | 事件触发器                                                                                           |
| `\sf[+]`        | 显示函数定义                                                                                         |
| `\sv[+]`        | 显示视图定义                                                                                         |
| `\z`            | 权限（`\dp` 的别名）                                                                                 |

**修饰符**（追加到大多数 `\d` 命令后）：

- `+` — 额外信息（大小、描述）：`\dt+`、`\l+`、`\du+`
- `S` — 包含系统对象：`\dtS`、`\dfS+`
- `x` — 展开显示模式：`\dt+x`（注意：`\dx` 是不同的命令；`x` 必须在 `S` 或 `+` 之后）

提供名称以查看详情：`\d table_name` 显示列、类型、索引、约束、外键。

**\d 命令中的模式匹配**：

- `*` = 任意字符序列，`?` = 单个字符
- `.` 分隔模式与对象：`\dt public.*` 或 `\dt my_schema.users`
- `..` 分隔数据库.模式.对象：`\dt mydb.public.*`（数据库必须与当前数据库匹配）
- 双引号阻止大小写折叠和通配符展开：`\dt "FOO"` 匹配 `FOO` 而非 `foo`
- `$` 按字面匹配（不是正则锚点）
- 正则字符如 `[0-9]` 可用：`\dt user[0-9]*` 匹配 `user1`、`user2`
- 无模式：显示当前 `search_path` 中可见的所有对象（不是数据库中的所有对象）
- 使用 `*.*` 查看所有模式中的所有对象，无论可见性如何

### 查询执行

| 命令                                 | 操作                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------ |
| `;`                                 | 执行当前查询缓冲区                                                                   |
| `\g`                                | 执行（类似 `;`，但可添加选项）                                                       |
| `\gx`                               | 以展开输出执行（类似 `\g`，强制 `\x on`）                                            |
| `\g filename`                       | 执行并将输出发送到文件                                                               |
| `\g \| command`                      | 执行并将输出通过管道发送到 shell 命令                                                 |
| `\g (format=csv footer=off) file`   | 使用一次性格式化选项执行                                                              |
| `\gdesc`                            | 描述结果列而不执行                                                                   |
| `\gset [prefix]`                    | 执行并将结果存储在 psql 变量中                                                       |
| `\gexec`                            | 将结果的每个单元格作为 SQL 命令执行                                                   |
| `\crosstabview`                     | 以交叉表（透视表）形式显示结果                                                       |
| `\watch`                            | 周期性重复执行查询（见下文）                                                          |
| `\bind [params...]`                 | 使用带参数的扩展查询协议。与 `\g`、`\gx` 和 `\gset` 配合使用                      |
| `\bind_named stmt_name [params...]` | 绑定命名的预处理语句                                                                  |
| `\parse stmt_name`                  | 从当前查询缓冲区创建预处理语句                                                        |
| `\close_prepared stmt_name`         | 关闭预处理语句                                                                       |
| `\;`                                | 将分号追加到缓冲区但不执行                                                            |

### 数据导入/导出

```sql
-- Server-side (requires superuser for file access, uses server filesystem)
COPY table TO '/path/file.csv' WITH (FORMAT csv, HEADER true);
COPY table FROM '/path/file.csv' WITH (FORMAT csv, HEADER true);

-- Client-side (runs with client permissions, no superuser needed) — preferred
\copy table TO '/path/file.csv' WITH (FORMAT csv, HEADER true)
\copy table FROM '/path/file.csv' WITH (FORMAT csv, HEADER true)
\copy (SELECT ...) TO '/path/output.csv' WITH (FORMAT csv, HEADER true)

-- Advanced: specific columns, NULL handling, custom delimiter
\copy table (col1, col2) FROM 'data.csv' WITH (FORMAT csv, HEADER true, NULL 'N/A')
```

`\copy` 是日常工作的首选——它使用客户端的文件系统和权限，而非服务器的。

**\copy 语法详情：**

```
-- FROM (import): sources are 'filename', program 'command', stdin, pstdin
\copy table FROM 'file.csv' WITH (FORMAT csv, HEADER true) [ WHERE condition ]

-- TO (export): destinations are 'filename', program 'command', stdout, pstdout
\copy table TO 'file.csv' WITH (FORMAT csv, HEADER true)
```

对于 `\copy ... FROM stdin`，数据行持续读取直到遇到仅含 `\.` 的行或 EOF。使用 `pstdin`/`pstdout` 始终读写 psql 的实际 stdin/stdout，无论 `\o` 设置如何。

警告：`program` 选项会执行 shell 命令。如果由用户输入构造，可能导致命令注入。避免与不受信任的数据进行字符串拼接。

**提示**：`\copy` 将该行剩余全部内容作为参数（无变量插值）。需要变量插值或多行查询时，改用 SQL `COPY ... TO STDOUT` 配合 `\g`：

```sql
-- This allows variable interpolation and multi-line queries
COPY (SELECT * FROM :table WHERE id > :min_id) TO STDOUT WITH (FORMAT csv, HEADER true) \g /tmp/output.csv
```

### 输出格式化

```
\a                  Toggle aligned/unaligned output
\x                  Toggle expanded display (vertical vs table)
\t                  Toggle tuples only (no headers/footers)
\pset format FORMAT  Set output format: aligned, asciidoc, csv, html, latex, latex-longtable, troff-ms, unaligned, wrapped
\pset border N       Set border style (0-2; 3 for latex data-row lines)
\pset null STRING    Display NULL as STRING
\pset pager [off]    Control pager usage
\pset title 'TEXT'   Set table title
\pset recordsep SEP  Set record separator for unaligned mode
\pset fieldsep SEP   Set field separator for unaligned mode (default: |)
\pset footer [on|off] Toggle row count footer
\pset columns N      Set target width for wrapped format
\pset csv_fieldsep C  Set CSV field separator (default: comma)
\pset numericlocale [on|off]  Toggle locale-specific number formatting
\pset linestyle STYLE Set border style: ascii, old-ascii, unicode
\pset pager_min_lines N  Minimum lines before pager activates
\pset xheader_width MODE  Expanded header width: full, column, page, or N (PostgreSQL 17+)
\H                   Toggle HTML output (shortcut)
\C [title]           Set table title (shortcut for \pset title)
\f [string]          Set field separator (shortcut for \pset fieldsep)
\T table_options     Set HTML table attributes (shortcut for \pset tableattr)
```

### 大对象

```
\lo_import filename [comment]   Import file as large object, returns OID
\lo_export loid filename        Export large object to file
\lo_list[x+]                    List all large objects
\lo_unlink loid                 Delete large object
```

大对象 OID 是持久化引用。导入时始终关联人类可读的注释。使用 `\lo_list` 查找 OID。

### 脚本与控制流

```
\i filename         Execute file (relative to current working directory)
\ir filename        Execute file (relative to the script being processed)
\o [filename]       Redirect query output to file (or pipe with |cmd)
\o                   Stop output redirection
\qecho TEXT          Output text to redirected output
\echo TEXT           Output text to stdout (-n suppresses trailing newline)
\warn TEXT           Output text to stderr
\! command           Execute shell command
\cd [dir]            Change working directory
\set NAME VALUE      Set psql variable
\unset NAME          Unset psql variable
\prompt [TEXT] NAME  Prompt user for variable value
\getenv psql_var env_var   Copy environment variable into psql variable
\setenv name [value]       Set or unset environment variable
\p                  Print current query buffer
\w filename         Write query buffer to file (or pipe with |cmd)

-- Conditional execution (useful in scripts)
\if EXPR
  \echo 'true branch'
\else
  \echo 'false branch'
\endif

\elif EXPR           Else-if inside \if block
```

`\if` 和 `\elif` 将其参数作为布尔值求值。有效值（不区分大小写，支持无歧义前缀匹配）：`true`、`false`、`1`、`0`、`on`、`off`、`yes`、`no`。无法求值为 true/false 的表达式会产生警告并被视为 false。跳过行中的变量引用不会被展开。

SQL 中的变量：`:'varname'`（带引号的字符串值，转义内嵌引号）、`:"varname"`（双引号标识符）、`:'varname'::type`（带类型转换）、`:varname`（不带引号——可能破坏 SQL）、`:{?varname}`（测试存在性，展开为 TRUE/FALSE）。

### 会话管理

```
\c [dbname [user]]  Connect to database (or reconnect)
\conninfo           Display connection info (includes SSL info)
\encoding [ENC]     Set or show client encoding
\password [USER]    Change password (does NOT appear in command history or server log)
\q                   Quit psql. In a script file, only that script is terminated. In interactive mode, the entire program exits.
\r                   Reset (clear) the query buffer
\e                   Edit query buffer in external editor
\ef [FUNCNAME]       Edit function definition
\ev [VIEWNAME]       Edit view definition
\sf[+] FUNCNAME      Show function definition (read-only)
\sv[+] VIEWNAME      Show view definition (read-only)
\s [FILE]            Print command history (or save to file)
\restrict KEY        Enter restricted mode (only \unrestrict allowed)
\unrestrict KEY      Exit restricted mode
\timing [on\|off]    Toggle query execution time display (milliseconds)
\errverbose          Repeat last error at maximum verbosity
\? [topic]           Help: commands, options, or variables
\h [command]         SQL syntax help (use * for all: \h *)
\copyright           Show PostgreSQL copyright
```

### 管道模式（PostgreSQL 14+）

```
\startpipeline
  SELECT $1 \bind 42 \sendpipeline
  SELECT $1 \bind 100 \sendpipeline
  \getresults
\endpipeline
```

管道模式无需等待每个结果即可发送多个查询，减少往返延迟。所有查询使用扩展查询协议。

**管道命令：**

- `\startpipeline` — 开始管道块
- `\endpipeline` — 结束管道块并处理剩余结果
- `\sendpipeline` — 将当前查询缓冲区追加到管道，不等待结果
- `\syncpipeline` — 发送同步消息但不结束管道
- `\flushrequest` — 请求服务器刷新但不同步
- `\flush` — 手动推送未发送的数据到服务器
- `\getresults [N]` — 读取待处理结果（N=0 或省略表示全部）

**管道限制：**

- 管道模式不支持 `COPY`
- 管道内不允许 `\g`、`\gx`、`\gdesc` 等元命令
- 所有查询使用扩展查询协议
- 管道内使用 `\bind`、`\bind_named`、`\parse`、`\close_prepared` 或 `\sendpipeline`
- `%P` 提示符变量显示管道状态（`on`、`off` 或 `abort`）

### \watch 语法

```
\watch [i[nterval]=SECONDS] [c[ount]=TIMES] [m[in_rows]=ROWS] [SECONDS]
```

`count` 和 `min_rows` 需要 PostgreSQL 17+。

- `interval` — 执行间隔秒数（默认：2，可通过 `WATCH_INTERVAL` 变量覆盖）
- `count` — 执行 N 次后停止
- `min_rows` — 查询返回少于 N 行时停止

如果查询缓冲区为空，`\watch` 重新执行最近发送的查询。

示例：

```sql
SELECT * FROM pg_stat_activity WHERE state = 'active';
\watch interval=5 count=10      -- every 5s, stop after 10 runs

SELECT count(*) FROM queue WHERE status = 'pending';
\watch i=1 min_rows=1            -- every 1s, stop when queue is empty
```

### 退出码

| 代码 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| 0    | 成功完成                                                     |
| 1    | 发生致命错误（服务器错误、连接失败等）                       |
| 2    | 连接失败（无法连接到服务器）                                 |
| 3    | 因 ON_ERROR_STOP 导致脚本执行终止                            |

## 安全注意事项

### 破坏性操作检查清单

在运行任何破坏性 SQL 之前，先验证影响范围：

```sql
-- BEFORE DELETE: check how many rows are affected
SELECT count(*) FROM users WHERE condition;  -- verify scope
BEGIN;
DELETE FROM users WHERE condition RETURNING *;  -- see what was deleted
-- ROLLBACK if wrong; COMMIT only after verification

-- BEFORE DROP TABLE: verify no foreign keys depend on it
\d table_name  -- check "Referenced by" section
-- Consider renaming first: ALTER TABLE old RENAME TO old_backup;
```

### 需要额外注意的危险命令

| 命令/模式                              | 风险                                                      | 缓解措施                                                                                           |
| --------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `\gexec`                              | 不经确认即执行生成的 SQL                                   | 始终先不使用 `\gexec` 运行生成查询来检查；设置 `ON_ERROR_STOP on`                              |
| `\! command`                          | 任意 shell 执行                                            | 无沙箱；命令以 psql 用户的完整权限运行                                                              |
| `\copy ... program 'cmd'`             | 如果文件名来自用户输入则可能导致 shell 命令注入              | 永远不要将不受信任的输入拼接到 `program` 字符串中                                                   |
| `\deu+`                               | 可能显示远程用户密码                                       | 避免在共享/管道输出中使用 `\deu+`；使用不带 `+` 的 `\deu`                                        |
| 不带 `WHERE` 的 `DELETE`/`UPDATE` | 影响表中的每一行                                           | 始终使用 `WHERE`；用 `BEGIN`/`ROLLBACK` 包裹以预览                                              |
| `DROP DATABASE/TABLE`                 | 不可逆的数据丢失                                           | 先用 `\conninfo` 确认你在正确的数据库上                                                            |

### 变量插值安全性

psql 变量是**纯文本替换**，不是参数化查询。这意味着：

```sql
-- UNSAFE: if :name contains "Robert'); DROP TABLE users;--" it will execute the injection
SELECT * FROM users WHERE name = :'name';

-- SAFER: use \prompt for interactive input (user sees what they typed)
\prompt 'Enter name: ' search_name
SELECT * FROM users WHERE name = :'search_name';

-- SAFEST: use \bind for programmatic parameter passing (truly parameterized)
SELECT * FROM users WHERE name = $1;
\bind 'Robert' \g
```

`:'varname'` 形式（带引号）始终比 `:varname`（不带引号）更安全，因为不带引号的替换可能破坏 SQL 语法或启用注入。对标识符（表名/列名）使用 `:"varname"`——它会正确转义内嵌的双引号。

## 何时使用什么

| 场景                         | 推荐命令                                                           |
| ---------------------------- | ------------------------------------------------------------------ |
| 快速检查表                   | `\d table_name`                                              |
| 列出模式中的所有表           | `\dt schema.*`                                               |
| 检查表上的索引               | `\di+ table_name*` 或 `\d table_name`                      |
| 将查询导出为 CSV             | `\copy (SELECT ...) TO 'file.csv' WITH (FORMAT csv, HEADER)` |
| 将 CSV 导入表                | `\copy table FROM 'file.csv' WITH (FORMAT csv, HEADER)`      |
| 运行迁移脚本                 | `psql -1 -f migration.sql dbname`                            |
| 监视实时查询                 | `SELECT ... \watch 5`                                        |
| 透视查询结果                 | `SELECT ... \crosstabview`                                   |
| 带条件逻辑的脚本             | `\if :var ... \endif`                                        |
| 批量插入多行                 | 使用 `\startpipeline` / `\endpipeline`                      |
| SQL 语法帮助                 | `\h CREATE TABLE`                                            |
| psql 命令帮助                | `\? commands`                                                |
| 检查查询执行时间             | `\timing on` 然后运行查询                                    |
| 调试错误详情                 | `\errverbose`                                                |
| 处理大型结果集               | `\set FETCH_COUNT 1000` 然后运行查询                         |
| 错误时自动保存点             | `\set ON_ERROR_ROLLBACK on` 然后使用事务                     |

- **`references/meta-commands-core.md`** — 核心元命令：查询缓冲区行为、参数解析规则、连接管理、查询执行、`\copy` 语法和脚本命令（`\if`、`\i`、`\o`、反引号展开）。需要任何反斜杠命令的精确语法或行为细节时阅读此文件。
- **`references/meta-commands-inspection.md`** — 完整的 `\d` 命令参考：所有对象检查命令、修饰符（`S`、`+`、`x`）和模式匹配规则。探索数据库模式或需要检查表、索引、视图、函数、权限等时阅读此文件。
- **`references/meta-commands-formatting.md`** — 输出格式化（`\pset` 选项及所有格式描述）、管道模式、`\watch`、`\crosstabview` 和会话管理（`\e`、`\ef`、`\ev`、`\timing` 等）。需要控制输出格式或使用管道模式时阅读此文件。
- **`references/cli-options-and-variables.md`** — 所有 CLI 标志、环境变量、psql 内部变量（AUTOCOMMIT、ON_ERROR_STOP、ECHO、FETCH_COUNT 等）、提示符自定义、`~/.psqlrc` 配置和 SQL 插值语法。配置 psql 启动行为、编写依赖变量状态的脚本或自定义提示符时阅读此文件。
- **`references/tips-workflows.md`** — 实用工作流（探索新数据库、理解表结构）、脚本模式（安全脚本、条件执行、`\gexec`）、自动化输出控制和数据导入/导出模式。当用户问如何用 psql 完成特定任务时阅读此文件。
- **`references/tips-advanced.md`** — 性能提示、调试/内省（`EXPLAIN`、锁分析、`ECHO_HIDDEN`）、安全最佳实践（ON_ERROR_STOP、事务模式、search_path 安全）和常见陷阱。用于锁分析、查询计划检查和故障排查。

## 重要说明

psql 对两种注释风格的处理方式不同：

- **C 风格块注释**（`/* ... */`）：传递给服务器处理和移除。
- **SQL 标准注释**（`--`）：由 psql 自身在发送到服务器之前移除。

当编写依赖注释行为的脚本时，这个区别很重要——只有 SQL 标准注释在客户端被剥离。

### 变量的变量（软引用）

psql 允许通过 `\set` 进行间接变量引用：

```sql
\set foo 'my_table'
\set bar :foo         -- copies the value of foo into bar
\echo :bar            -- outputs: my_table
```

虽然 `\set :foo 'something'` 这样的结构在语法上是有效的，但它们产生的是实际用途有限的"软链接"。对于简单的变量复制，使用 `\set new_var :old_var`。

### 版本兼容性

psql 与相同或更旧主版本的服务器配合使用效果最佳。反斜杠命令（尤其是 `\d` 家族）可能在更新的服务器版本上失败。连接多个服务器版本时，使用最新可用的 psql 客户端。`\d` 命令通常可向后兼容到 9.2 版本的服务器。

## 外部参考

- [PostgreSQL Client Applications](https://www.postgresql.org/docs/current/app-psql.html)
- [Official PostgreSQL Documentation](https://www.postgresql.org/docs/current/index.html)
- [The SQL Language](https://www.postgresql.org/docs/current/sql.html)
- [SQL Syntax - The SQL Language](https://www.postgresql.org/docs/current/sql-syntax.html)
- [SQL Command](https://www.postgresql.org/docs/current/sql-commands.html)
- [PostgreSQL Wiki](https://wiki.postgresql.org/)

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用更改之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代特定环境的测试、安全审查或用户对破坏性或高成本操作的批准。
