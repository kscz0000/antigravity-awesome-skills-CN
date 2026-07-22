# psql CLI 选项、变量与环境

psql 命令行标志、配置变量和环境变量的完整参考。

## 目录

- [CLI 选项](#cli-选项)
- [连接参数](#连接参数)
- [输入/输出选项](#输入输出选项)
- [输出格式选项](#输出格式选项)
- [psql 变量](#psql-变量)
- [环境变量](#环境变量)
- [配置文件](#配置文件)
- [Tab 补全](#tab-补全)
- [编辑器集成](#编辑器集成)

---

## CLI 选项

### 概要

```
psql [option...] [dbname [user]]
```

当 `dbname` 是第一个非选项参数时，它指定数据库。第二个非选项参数指定用户。

### 通用选项

| 标志 | 描述 |
|------|------|
| `-a` / `--echo-all` | 将所有非空输入行打印到标准输出。等价于 `ECHO=all`。 |
| `-b` / `--echo-errors` | 将失败的 SQL 命令打印到 stderr。等价于 `ECHO=errors`。 |
| `-c command` / `--command=command` | 执行一个或多个 SQL 命令后退出。命令可用分号分隔。每个 `-c` 字符串作为单个请求发送——其中的多个 SQL 命令在一个事务中执行（除非显式 `BEGIN`/`COMMIT`）。不能在一个 `-c` 中混合 SQL 和元命令。成功返回 0，错误返回 1，连接失败返回 2。 |
| `-d dbname` / `--dbname=dbname` | 要连接的数据库名 |
| `-e` / `--echo-queries` | 将所有发送到服务器的 SQL 命令同时复制到标准输出 |
| `-E` / `--echo-hidden` | 将隐藏查询（\d 命令和其他元命令生成的 SQL）回显到 stderr。有助于了解 psql 内部工作原理。 |
| `-f filename` / `--file=filename` | 从文件执行命令后退出。使用 `-` 表示 stdin（读取直到 EOF 或 `\q`；Readline 不可用）。`-f` 提供带行号的错误消息，不同于 shell 重定向。 |
| `-F separator` / `--field-separator=separator` | 非对齐输出的字段分隔符（默认：`|`） |
| `-H` / `--html` | HTML 输出模式 |
| `-l` / `--list` | 列出可用数据库后退出。连接到 `postgres` 数据库，除非通过 `-d` 或非选项参数指定了其他数据库。 |
| `-L filename` / `--log-file=filename` | 将所有会话输出记录到文件 |
| `-n` / `--no-readline` | 禁用增强的命令行编辑和 tab 补全 |
| `-o filename` / `--output=filename` | 将所有查询输出重定向到文件 |
| `-P assignment` / `--pset=assignment` | 设置打印选项（格式：`option=value`） |
| `-q` / `--quiet` | 安静模式——无启动消息、无信息消息 |
| `-R separator` / `--record-separator=separator` | 非对齐输出的记录分隔符（默认：换行） |
| `-s` / `--single-step` | 单步模式。每个命令发送到服务器前确认。 |
| `-S` / `--single-line` | 单行模式。换行终止查询（如同分号）。不推荐——混合 SQL 和元命令在同一行时，执行顺序可能不明确。 |
| `-t` / `--tuples-only` | 仅打印行——无表头、页脚 |
| `-T table_options` / `--table-attr=table_options` | HTML 表属性 |
| `-v assignment` / `--set=assignment` / `--variable=assignment` | 设置 psql 变量（格式：`name=value` 设置、`name` 取消设置、`name=` 设为空）。赋值在命令行处理时发生，因此连接状态变量之后会被覆盖。 |
| `-V` / `--version` | 打印 psql 版本并退出 |
| `-w` / `--no-password` | 永不提示密码。需要密码时失败。此设置在整个会话期间持续，包括 `\connect` 尝试。 |
| `-W` / `--password` | 强制密码提示。此设置在整个会话期间持续，包括 `\connect` 尝试。 |
| `-x` / `--expanded` | 开启展开表输出 |
| `-X` / `--no-psqlrc` | 不读取启动文件（~/.psqlrc） |
| `-z` / `--field-separator-zero` | 将字段分隔符设为 NUL 字节 |
| `-0` / `--record-separator-zero` | 将记录分隔符设为 NUL 字节 |
| `-1` / `--single-transaction` | 将 `-f` 或 `-c` 命令包裹在单个事务中。任何命令失败则全部回滚。警告：如果脚本本身包含 `BEGIN`/`COMMIT`/`ROLLBACK`，此选项不会产生预期效果。 |
| `-?` / `--help[=topic]` | 显示帮助。`topic` 可为 `commands`（反斜杠命令）、`options`（CLI 选项，默认）或 `variables`（配置变量）。 |
| `--csv` | 切换到 CSV 输出模式。等价于 `\pset format csv`。 |

---

## 连接参数

这些选项控制 psql 如何连接 PostgreSQL。

| 标志 | 环境变量 | 描述 |
|------|---------|------|
| `-h host` | `PGHOST` | 主机名或套接字目录（默认：本地套接字） |
| `-p port` | `PGPORT` | 端口号（默认：5432） |
| `-U user` | `PGUSER` | 数据库用户名 |
| `-d dbname` | `PGDATABASE` | 数据库名 |
| `-w` | — | 不提示密码 |
| `-W` | — | 强制密码提示 |

**连接 URI：**
```
psql postgresql://user:password@host:5432/dbname?sslmode=require
psql postgresql:///dbname?host=/var/run/postgresql
```

**服务查找：** 如果设置了 `PGSERVICE` 或连接字符串中的 `service=name`，psql 从 `pg_service.conf` 读取连接参数。

---

## 输入/输出选项

| 标志 | 描述 |
|------|------|
| `-c command` | 执行命令后退出。多个命令用 `;` 分隔。 |
| `-f filename` | 从文件读取命令后退出。使用 `-` 表示 stdin。 |
| `-1` | 在单个事务中运行（仅对 `-c` 或 `-f` 有效） |
| `-a` | 将所有输入行回显到 stdout |
| `-b` | 将失败的 SQL 回显到 stderr |
| `-e` | 将查询回显到 stdout |
| `-E` | 将隐藏查询（\d 内部查询）回显到 stderr |
| `-L file` | 将所有输出记录到文件 |
| `-o file` | 将输出重定向到文件 |
| `-n` | 禁用 readline |

**常用模式：**
```bash
# Run a migration in a transaction
psql -1 -f migration.sql mydb

# Execute a single query
psql -c "SELECT count(*) FROM users" mydb

# Pass a variable from the command line
psql -v table=users -c 'SELECT count(*) FROM :"table"' mydb

# Batch process with for-loop
for f in /tmp/*.sql; do psql -1 -f "$f" mydb; done

# Echo internal queries to learn psql
psql -E mydb -c "\d+ users"
```

---

## 输出格式选项

| 标志 | 描述 |
|------|------|
| `-A` / `--no-align` | 非对齐（分隔符分隔）输出 |
| `-F sep` | 字段分隔符（默认：`|`） |
| `-H` / `--html` | HTML 表输出 |
| `-P opt=val` | 设置 pset 选项（如 `-P pager=off`） |
| `-R sep` | 记录分隔符（默认：换行） |
| `-t` | 仅元组（无表头/页脚） |
| `-T attrs` | HTML 表属性 |
| `-x` | 展开显示 |
| `-z` / `-0` | NUL 分隔符 |

**脚本友好的输出模式：**
```bash
# CSV output
psql --csv -c "SELECT id, name FROM users" mydb

# Custom delimiter output
psql -A -F ',' -t -c "SELECT id, name FROM users" mydb

# NUL-separated for xargs -0
psql -A -z -t -c "SELECT filename FROM files_to_process" mydb | xargs -0 process

# JSON-friendly (one value per line)
psql -A -t -c "SELECT json_agg(row_to_json(t)) FROM (SELECT id, name FROM users) t" mydb
```

---

## psql 变量

psql 维护控制行为的内部变量。用 `\set` 设置、`\unset` 取消设置、`\set`（无参数）查看所有变量。

### 自动变量

| 变量 | 描述 |
|------|------|
| `AUTOCOMMIT` | `on`（默认）或 `off`。关闭时，psql 在任何不在事务块中的命令之前自动发出隐式 `BEGIN`（`BEGIN`/`VACUUM` 等除外）。你必须显式 `COMMIT` 或 `ROLLBACK`。 |
| `COMP_KEYWORD_CASE` | `lower`、`upper`、`preserve-lower`（默认）、`preserve-upper`。控制 tab 补全关键字大小写。`preserve-lower`/`preserve-upper` 保留已输入内容的大小写；空输入以小写/大写补全。 |
| `DBNAME` | 当前数据库名。连接时自动设置。 |
| `ECHO` | `none`（默认）、`all`、`queries`、`errors`。控制回显内容。`all` 回显所有命令（包括脚本）。`queries` 仅回显 SQL 查询，不回显元命令。`errors` 将失败的 SQL 命令回显到 stderr（由 `-b` 设置）。 |
| `ECHO_HIDDEN` | `off`、`on`、`noexec`。`on` 时显示隐藏查询（\d 命令背后的 SQL）。`noexec` 显示但不执行。 |
| `ENCODING` | 当前客户端编码。自动设置。 |
| `ERROR` | 最近查询失败时为 `true`，否则为 `false`。 |
| `FETCH_COUNT` | 整数（默认：0）。设置后，psql 按此大小的批次获取行，而非一次全部获取。适用于大型结果集。 |
| `HIDE_TABLEAM` | 设置后在 `\d+` 输出中隐藏表访问方法。 |
| `HIDE_TOAST_COMPRESSION` | 设置后在 `\d+` 输出中隐藏压缩方法。 |
| `HISTCONTROL` | `none`（默认）、`ignorespace`、`ignoredups`、`ignoreboth`。控制历史保存。 |
| `HISTFILE` | 历史文件路径（默认：`~/.psql_history`）。可包含 psql 变量引用，如 `\set HISTFILE ~/.psql_history-:DBNAME`。 |
| `HISTSIZE` | 最大历史条目数（默认：500）。负值禁用限制。 |
| `HOST` | 当前服务器主机。连接时自动设置。 |
| `IGNOREEOF` | 设置后阻止 Ctrl-D 退出。值为退出前忽略的 EOF 次数。 |
| `LAST_ERROR_MESSAGE` | 最近失败查询的错误消息。 |
| `LAST_ERROR_SQLSTATE` | 最近失败查询的 SQLSTATE 错误码（无错误时为 `00000`）。 |
| `LASTOID` | `INSERT` 或 `\lo_import` 最后影响行的 OID。PG 12+ 表始终为 0（OID 列已移除）。 |
| `ON_ERROR_ROLLBACK` | `off`（默认）、`on`、`interactive`。`on` 时，事务内的错误自动创建保存点，允许继续执行。`interactive` 仅在交互会话中激活，读取脚本时不激活。 |
| `ON_ERROR_STOP` | `off`（默认）或 `on`。`on` 时，查询错误或元命令错误停止脚本执行并退出。安全脚本的关键设置。 |
| `PIPELINE_COMMAND_COUNT` | 当前管道中排队的命令数。 |
| `PIPELINE_RESULT_COUNT` | 当前管道中待处理结果的命令数。 |
| `PIPELINE_SYNC_COUNT` | 当前管道中排队的同步消息数。 |
| `PORT` | 当前服务器端口。连接时自动设置。 |
| `PROMPT1`、`PROMPT2`、`PROMPT3` | 提示符格式字符串（见下文）。 |
| `QUIET` | `on` 或 `off`。安静模式。 |
| `ROW_COUNT` | 最近查询影响的行数。 |
| `SERVER_VERSION_NAME` | 服务器版本字符串。 |
| `SERVER_VERSION_NUM` | 服务器版本整数（如 160000 表示 16.0）。 |
| `SERVICE` | 连接中的服务名（如适用）。 |
| `SHELL_ERROR` | 最近 shell 命令（`\!`、`\g`、`\o`、`\w`、`\copy`、反引号）失败时为 `true`，否则为 `false`。 |
| `SHELL_EXIT_CODE` | 最近 shell 命令的退出码（0-127 正常退出，128-255 信号终止，-1 启动失败）。 |
| `SHOW_ALL_RESULTS` | `on`（默认）或 `off`。开启时显示组合查询的所有结果。 |
| `SHOW_CONTEXT` | `never`、`errors`、`always`。控制消息中 `CONTEXT:` 的显示。默认：`errors`。 |
| `SINGLELINE` | `on` 或 `off`。换行作为查询终止符。 |
| `SINGLESTEP` | `on` 或 `off`。每个命令前确认。 |
| `SQLSTATE` | 最近查询的 SQLSTATE 错误码。 |
| `USER` | 当前数据库用户。连接时自动设置。 |
| `VERSION` | psql 客户端完整版本字符串。 |
| `VERSION_NAME` | psql 客户端短版本（如 `18beta1`）。 |
| `VERSION_NUM` | psql 客户端版本整数（如 `180000`）。 |
| `WATCH_INTERVAL` | `\watch` 命令的默认间隔秒数（默认：2）。 |
| `VERBOSITY` | `default`、`verbose`、`terse`、`sqlstate`。控制错误消息详细程度。 |

### SQL 插值

psql 变量可以使用冒号前缀语法插入 SQL 语句中。这是**纯文本替换**，不是参数化查询——了解差异以安全使用。

| 语法 | 行为 | 示例 |
|------|------|------|
| `:varname` | 不带引号的替换。变量值字面替换 `:varname`，如果值包含特殊字符，可能破坏 SQL 语法或启用注入。 | `\set table users` → `SELECT * FROM :table;` → `SELECT * FROM users;` |
| `:'varname'` | 单引号字符串替换。值放在单引号内，内嵌单引号和反斜杠被转义。这是值替换最安全的形式。 | `\set name O'Brien` → `SELECT * FROM users WHERE name = :'name';` → `SELECT * FROM users WHERE name = 'O''Brien';` |
| `:"varname"` | 双引号标识符替换。值放在双引号内，内嵌双引号加倍。用于表名/列名。 | `\set col first name` → `SELECT :"col" FROM users;` → `SELECT "first name" FROM users;` |
| `:{?varname}` | 变量存在性测试。始终展开——已定义则 `TRUE`，否则 `FALSE`。设计用于 `\if` 条件。 | `\if :{?myvar}` → 如果 `myvar` 已设置则为 true |
| `\:varname` | 转义冒号。冒号不被视为变量引用——`:varname` 按字面传递。 | `SELECT \:not_a_var FROM t;` → `SELECT :not_a_var FROM t;` |

注意：变量插值不会在带引号的 SQL 字面量或标识符内部发生。因此 `':foo'` 不会从变量产生带引号的字符串（即使发生了也不安全——无法正确处理内嵌引号）。改用 `:'foo'`。

**安全指南**：替换用户提供的值时，始终优先使用 `:'varname'`（带引号字符串）而非 `:varname`（不带引号）。不带引号的替换可能破坏 SQL 语法或启用注入。对于最安全的程序化参数传递，使用 `\bind` 配合扩展查询协议（提供真正的参数化查询）。

### 脚本关键变量

**ON_ERROR_STOP** — 脚本中最重要的变量。在脚本中设置它以确保在第一个错误时中止而非继续：

```
-- At the top of any script:
\set ON_ERROR_STOP on

-- Now any error stops execution
INSERT INTO users (id) VALUES (1);
INSERT INTO users (id) VALUES ('bad');  -- aborts here
INSERT INTO users (id) VALUES (2);      -- never reached
```

**AUTOCOMMIT** — 关闭以手动管理事务：

```
\set AUTOCOMMIT off
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
\set AUTOCOMMIT on
```

**FETCH_COUNT** — 用于会消耗过多内存的超大结果集：

```
\set FETCH_COUNT 1000
SELECT * FROM huge_table;
```

**ERROR / SQLSTATE / LAST_ERROR_MESSAGE** — 用于条件逻辑：

```
INSERT INTO unique_table (id) VALUES (1);
\if :ERROR
  \echo 'Insert failed: ' :LAST_ERROR_MESSAGE
\else
  \echo 'Insert succeeded, rows affected: ' :ROW_COUNT
\endif
```

### 提示符自定义

`PROMPT1` 是正常提示符（默认：`'%/%R%x%# '`）。`PROMPT2` 在命令不完整时出现（续行）（默认：`'%/%R%x%# '`）。`PROMPT3` 在 `COPY FROM STDIN` 需要行值时出现（默认：`'>> '`）。

**格式说明符：**

| 说明符 | 输出 |
|--------|------|
| `%/` | 当前数据库名 |
| `%~` | 类似 `%/`，但如果数据库是你的默认数据库则显示 `~` |
| `%m` | 主机名（在第一个点处截断），Unix 套接字显示 `[local]` |
| `%M` | 完整主机名，非默认 Unix 套接字显示 `[local:/dir/name]` |
| `%>` | 端口号 |
| `%n` | 用户名 |
| `%s` | 服务名（来自连接） |
| `%#` | 超级用户显示 `#`，否则显示 `>` |
| `%p` | 服务器后端进程 ID |
| `%R` | PROMPT1：`=` 正常、`^` 单行模式、`@` 条件栈非活动（如在被跳过的 `\if` 内）、`!` 未连接。PROMPT2：`-`（续行）、`*`（注释）、`'`（单引号）、`"`（双引号）、`$`（美元引号）、`(`（括号内）。PROMPT3：空。 |
| `%w` | 与上次 PROMPT1 输出可见宽度匹配的空白（用于对齐 PROMPT2） |
| `%x` | 事务状态：空（空闲）、`*`（在事务块中）、`!`（失败的事务）、`?`（未知或无连接） |
| `%l` | 当前语句内的行号，从 1 开始 |
| `%P` | 管道状态：`on`（管道模式活动）、`off`（非管道模式）、`abort`（管道中止） |
| `%%` | 字面 `%` |
| `%` 数字 | 具有给定八进制码的字符（如 `%033` = ESC 字符） |
| `%:varname:` | psql 变量的值 |
| `` %`[command]` `` | shell 命令的输出（去掉尾部换行） |
| `%[ ... %]` | 告诉 Readline 包含的文本不可见（用于 ANSI 转义码） |

**常用提示符配置：**
```
-- Show database and user
\set PROMPT1 '%n@%m %/%R%# '

-- Show transaction status
\set PROMPT1 '%/%x%# '

-- Production-safe prompt (color-coded)
-- Note: %033 is octal for ESC character; %[...%] tells Readline these chars are invisible
\set PROMPT1 '%[%033[1;31m%]%/%[%033[0m%]%R%# '
```

---

## 环境变量

| 变量 | 描述 |
|------|------|
| `PGDATABASE` | 默认数据库名 |
| `PGHOST` | 默认主机（或套接字目录） |
| `PGPORT` | 默认端口（5432） |
| `PGUSER` | 默认用户 |
| `PGPASSWORD` | 密码（不推荐——改用 `~/.pgpass`） |
| `PGPASSFILE` | 密码文件路径（默认：`~/.pgpass`） |
| `PGSERVICE` | `pg_service.conf` 中的服务名 |
| `PGSERVICEFILE` | 服务文件路径 |
| `PGOPTIONS` | 传递给服务器的默认选项 |
| `PGSSLMODE` | SSL 模式（`disable`、`allow`、`prefer`、`require`、`verify-ca`、`verify-full`） |
| `PGREQUIRESSL` | 旧版 SSL 标志（改用 `PGSSLMODE`） |
| `PGSSLCERT` | 客户端证书路径 |
| `PGSSLKEY` | 客户端密钥路径 |
| `PGSSLROOTCERT` | 根证书路径 |
| `PGSSLCRL` | 证书吊销列表路径 |
| `PGREQUIREPEER` | Unix 套接字连接需要的对端用户名 |
| `PGKRBSRVNAME` | Kerberos 服务名 |
| `PGGSSLIB` | 使用的 GSS 库 |
| `PGCONNECT_TIMEOUT` | 连接超时（秒） |
| `PGCLIENTENCODING` | 客户端编码（覆盖自动检测的 locale 设置） |
| `PGDATESTYLE` | 日期显示格式 |
| `PGTZ` | 时区 |
| `PGSYSCONFDIR` | 系统配置目录 |
| `PG_COLOR` | 彩色输出（`auto`、`always`、`never`） |
| `COLUMNS` | 当 `\pset columns` 为 0 时，控制 `wrapped` 格式宽度和激活分页器或切换到展开自动模式的阈值 |
| `PSQL_EDITOR` | `\e`、`\ef`、`\ev` 的编辑器。优先于 `EDITOR` 和 `VISUAL`。 |
| `PSQL_EDITOR_LINENUMBER_ARG` | 向编辑器传递行号的命令行参数（默认：`+`）。如设为 `--line ` 用于使用 `--line N` 语法的编辑器。 |
| `PSQL_HISTORY` | 替代历史文件路径（覆盖 `HISTFILE`） |
| `PSQLRC` | 替代 `.psqlrc` 位置 |
| `PSQL_PAGER` | 分页器命令（覆盖 `PAGER`） |
| `PSQL_WATCH_PAGER` | 专门用于 `\watch` 输出的分页器命令（设置后覆盖 `PSQL_PAGER` 和 `PAGER`）。仅 Unix。 |
| `EDITOR` / `VISUAL` | `\e`、`\ef`、`\ev` 的编辑器（在 `PSQL_EDITOR` 之后检查） |
| `SHELL` | `\!` 使用的 shell |
| `TMPDIR` | 临时文件目录 |
| `LANG` | locale（影响排序、数字格式化） |

### ~/.pgpass 文件

安全存储密码，而非使用 `PGPASSWORD`：

```
# Format: hostname:port:database:username:password
# Use * as wildcard
localhost:5432:mydb:myuser:YOUR_PASSWORD
*:5432:*:admin:YOUR_PASSWORD
```

权限必须为 0600：`chmod 600 ~/.pgpass`

---

## 配置文件

### ~/.psqlrc

每次交互式 psql 启动时执行（除非使用 `-X`）。适合个人自定义：

```sql
-- ~/.psqlrc example
\set ON_ERROR_STOP on
\timing on
\pset null '(null)'

-- Custom prompt showing database and transaction status
\set PROMPT1 '%n@%m %/%x%# '

-- Shortcuts
\set HISTSIZE 10000
\set HISTCONTROL ignoredups

-- Show how long queries took
\echo 'Welcome to' :DBNAME
```

### 版本特定的 psqlrc

追加 `-` 和版本号用于版本特定配置。psql 读取最具体的匹配：

- `~/.psqlrc-18` — 适用于 psql 18.x
- `~/.psqlrc-18.3` — 专门适用于 psql 18.3
- 系统级：`pg_config --sysconfdir` 目录中的 `psqlrc-18`

### 系统级 psqlrc

位于 `pg_config --sysconfdir`/psqlrc 的系统级 psql 配置（使用 `PGSYSCONFDIR` 覆盖）。在用户 `~/.psqlrc` 之前应用。

### Windows 路径

在 Windows 上，用户配置位于 `%APPDATA%\postgresql\psqlrc.conf`，历史记录位于 `%APPDATA%\postgresql\psql_history`。

---

## Tab 补全

psql 为以下内容提供智能 tab 补全：
- SQL 关键字
- 表、视图和列名
- 函数名和参数
- 带模式限定的名称
- `\d` 命令模式

Tab 补全会向服务器发送查询以获取元数据。这可能干扰操作：例如 `BEGIN` 之后，tab 补全查询意味着 `SET TRANSACTION ISOLATION LEVEL` 已太迟。

要永久禁用 tab 补全，在 `~/.inputrc` 中添加：
```
$if psql
set disable-completion on
$endif
```

或使用 `-n` 对单次会话禁用。

---

## 编辑器集成

`\e`、`\ef` 和 `\ev` 使用以下顺序指定的编辑器：
1. `PSQL_EDITOR` 环境变量（最高优先级）
2. `EDITOR` 环境变量
3. `VISUAL` 环境变量
4. 默认：`vi`（Unix）、`notepad.exe`（Windows）

使用 `PSQL_EDITOR_LINENUMBER_ARG` 控制行号传递方式（默认：`+`）。

**有用的编辑器设置：**
```bash
export EDITOR='vim'
# or for VS Code:
export EDITOR='code --wait'
# or for nano:
export EDITOR='nano'
```
