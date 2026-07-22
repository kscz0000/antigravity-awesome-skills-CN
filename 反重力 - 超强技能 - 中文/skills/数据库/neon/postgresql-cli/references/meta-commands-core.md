psql 元命令参考的一部分。另见：meta-commands-inspection.md、meta-commands-formatting.md

# psql 元命令 — 核心参考

按类别组织的所有 psql 反斜杠命令的完整参考。涵盖官方 PostgreSQL 文档中的每个元命令。

## 目录

- [查询缓冲区](#查询缓冲区)
- [元命令参数解析](#元命令参数解析)
- [通用](#通用)
- [连接管理](#连接管理)
- [查询执行](#查询执行)
- [数据导入/导出](#数据导入导出)
- [大对象](#大对象)
- [脚本与控制流](#脚本与控制流)
- [帮助与信息](#帮助与信息)

---

## 查询缓冲区

psql 维护一个内部**查询缓冲区**——一个在发送到服务器之前组装 SQL 命令的工作区。理解缓冲区的工作方式可以阐明许多元命令的行为：

- **输入 SQL**（不以分号结束）将文本追加到查询缓冲区。
- **分号（`;`）** 将缓冲区内容发送到服务器并清空缓冲区。
- **`\r` / `\reset`** 丢弃缓冲区内容而不执行。
- **`\p` / `\print`** 显示当前缓冲区内容。
- **`\w` / `\write`** 将缓冲区写入文件或管道。
- **`\e` / `\edit`** 在外部编辑器中打开缓冲区；编辑器关闭时，修改后的内容被重新解析——完整的查询（以 `;` 结尾的）立即执行，剩余文本留在缓冲区中。
- **`\g`** 像分号一样发送缓冲区，但接受可选的格式化和输出重定向参数。
- 许多操作"查询缓冲区"的元命令在缓冲区为空时回退到最近执行的查询（如 `\g`、`\gdesc`、`\p`）。

---

## 元命令参数解析

大多数元命令接受参数。理解 psql 如何解析这些参数对于正确使用它们至关重要，尤其在脚本中。

### 引用规则

参数以空白分隔。要在参数中包含空白：

- **单引号**：`'hello world'`——参数为 `hello world`。单引号阻止变量插值和反引号展开。
- **双引号**：`"hello world"`——参数为 `hello world`。双引号内会执行变量插值（`:varname`），但不执行反引号展开。
- **不带引号**：参数以空白分隔；单个 token 无需引号。

### 类 C 转义序列

在单引号字符串内，识别以下类 C 转义序列：

| 转义 | 含义 |
|------|------|
| `\n` | 换行 |
| `\t` | 制表符 |
| `\b` | 退格 |
| `\r` | 回车 |
| `\f` | 换页 |
| `\digits` | 八进制字节值 |
| `\xhexdigits` | 十六进制字节值 |

反斜杠后跟任何其他字符按该字符字面处理（如 `\\` → `\`，`\'` → `'`）。

### 参数中的变量插值

psql 变量引用（`:varname`）在元命令参数中出现时都会被展开，但单引号字符串内除外。双引号字符串内会展开变量引用。

```sql
\set dest '/tmp/output.txt'
\echo :dest              -- expands to /tmp/output.txt
\echo ':dest'            -- literal :dest (no expansion)
\echo ":dest"            -- expands to /tmp/output.txt
```

### 使用 `:{?varname}` 测试变量存在性

语法 `:{?variable_name}` 测试变量是否已定义。它展开为 `TRUE` 或 `FALSE`（字面值），在 `\if` 条件中很有用：

```sql
\if :{?myvar}
  \echo 'myvar is defined'
\else
  \echo 'myvar is not defined'
\endif
```

### 反引号展开

元命令参数中包含在反引号（`` ` ``）内的文本作为 shell 命令执行，其标准输出（去掉尾部换行）替换反引号文本。这对于注入动态值很有用：

```sql
\echo `date`                    -- shows current date
\echo `whoami`                  -- shows current OS user
\set mydate `date +%Y%m%d`
\echo :mydate                   -- e.g., 20260402
```

反引号展开不会在单引号字符串内或被 `\if`/`\else`/`\elif` 跳过的行中执行。

**反引号内的变量插值**：psql 变量引用（`:varname`、`:'varname'`）在 shell 命令执行之前于反引号文本内展开。这意味着你可以在 shell 命令中使用 psql 变量：

```sql
\set logfile /tmp/query.log
\echo `cat :logfile`              -- expands :logfile before running cat
\echo `echo :'%varname'`          -- :'...' form is preferred for shell safety
```

`:'varname'` 形式（带引号）在反引号内更受推荐，因为它正确转义特殊字符。但是，如果变量值包含回车（`\r`）或换行（`\n`）字符，`:'varname'` 会报错。

### SQL 标识符参数

某些元命令接受描述数据库对象的参数（如 `\df`、`\ef`）。这些遵循特殊规则：

- 不带引号的名称折叠为小写（匹配 SQL 标识符行为）
- 双引号保留大小写：`\df "MyFunction"`
- 混合引用：不带引号的部分折叠，双引号部分保留。`FOO"BAR"BAZ` 变为 `fooBARbaz`
- 尾部 `()` 加可选类型名指定参数类型：`\df my_func(integer, text)`
- `*` 匹配全部：`\df *`

### 参数解析停止规则

- `\!`、`\copy`、`\o |command`、`\echo` 等命令的整行剩余部分作为参数（经过引用和插值处理后）。
- 参数文本中任何位置的 `\\`（双反斜杠）导致 psql 在该点停止解析——`\\` 之前的内容是参数，之后的内容被忽略。这对于添加行内注释很有用：
  ```sql
  \echo hello \\ this is a comment
  -- outputs: hello
  ```

---

## 通用

### `\;`

将分号追加到查询缓冲区而不触发命令执行。这允许将多个 SQL 语句组合为单个服务器请求：

```sql
select 1\; select 2\; select 3;
```

当非反斜杠分号到达时，所有三条语句在一个请求中发送。服务器将它们作为单个事务执行，除非包含显式的 `BEGIN`/`COMMIT`。

### `\! [command]`

不带参数时，逃逸到子 shell（子 shell 退出时 psql 恢复）。带参数时，执行 shell 命令。整行剩余部分作为命令——无变量插值或反引号展开。

```sql
\! ls -la /tmp
\! pwd
```

### `\copyright`

显示 PostgreSQL 的版权和分发条款。

---

## 连接管理

### `\c` 或 `\connect [ -reuse-previous=on|off ] [ dbname [ username ] [ host ] [ port ] | conninfo ]`

建立到 PostgreSQL 服务器的新连接。如果连接成功，前一个连接被关闭。

**位置语法：**
```sql
\c mydb myuser host.dom 6432
\c - - newhost -              -- change only the host
```

**连接字符串语法：**
```sql
\c service=foo
\c "host=localhost port=5432 dbname=mydb connect_timeout=10 sslmode=disable"
\c postgresql://tom@localhost/mydb?application_name=myapp
```

**`-reuse-previous` 标志：**
- 默认情况下，位置语法中参数被复用，但连接字符串不复用
- 传入 `-reuse-previous=on` 复用当前连接中所有未指定的参数
- 传入 `-reuse-previous=off` 阻止复用

```sql
\c -reuse-previous=on sslmode=require    -- changes only sslmode
```

**失败时的行为：**
- 交互模式：保留前一个连接
- 脚本模式：关闭前一个连接；所有数据库命令失败，直到下一次成功的 `\c`

### `\conninfo`

输出连接信息，包括数据库、用户、主机、端口和 SSL 状态。`Client User` 字段显示连接时的用户；`Superuser` 显示当前执行上下文是否具有超级用户权限（`SET ROLE` 后可能不同）。

### `\encoding [ encoding ]`

设置客户端字符集编码。不带参数时显示当前编码。

### `\password [ username ]`

更改指定用户的密码（默认：当前用户）。提示输入新密码，加密后以 `ALTER ROLE` 发送。新密码不会出现在命令历史、服务器日志或任何其他地方。

---

## 查询执行

### `\g [ (option=value [...]) ] [ filename ]` / `\g [ (option=value [...]) ] [ |command ]`

将当前查询缓冲区发送到服务器执行。

- 不带参数：等价于分号
- 带文件名：输出写入文件（仅当查询成功并返回零个或多个元组时）
- 带 `|command`：输出通过管道发送到 shell 命令（命令中无变量插值）。仅当查询成功并返回零个或多个元组时写入。

**注意**：仅当查询成功返回零个或多个元组时才写入文件或命令——查询失败或非数据返回的 SQL 命令不会写入。这意味着即使是空结果集（0 行）也会触发输出。

```sql
SELECT * FROM users \g (format=csv footer=off) /tmp/users.csv
SELECT count(*) FROM users \g | wc -l
```

如果查询缓冲区为空，重新执行最近发送的查询。

### `\gx [ (option=value [...]) ] [ filename ]`

类似 `\g`，但强制对此查询使用展开输出模式（如同包含了 `expanded=on`）。

### `\gdesc`

显示结果的列名和数据类型，而不实际执行查询。语法错误仍会报告。如果查询缓冲区为空，描述最近发送的查询。

### `\gset [ prefix ]`

执行查询并将结果存储在 psql 变量中。查询必须恰好返回一行。每列成为以列名命名的变量（可选加前缀）。NULL 列取消设置变量而非设置它。如果查询失败或未返回一行，变量不变。

```sql
SELECT 'hello' AS var1, 10 AS var2
\gset result_
\echo :result_var1 :result_var2
-- outputs: hello 10
```

### `\gexec`

执行当前查询，然后将每行的每列作为 SQL 语句执行。NULL 字段被忽略。生成的查询按字面发送——不含 psql 元命令或变量引用。除非设置 `ON_ERROR_STOP`，否则出错时继续执行。使用 `\gexec` 时建议将 `ECHO` 设为 `all` 或 `queries` 以查看正在执行的内容。

```sql
SELECT format('CREATE INDEX ON my_table(%I)', attname)
FROM pg_attribute
WHERE attrelid = 'my_table'::regclass AND attnum > 0
ORDER BY attnum
\gexec
```

### `\crosstabview [ colV [ colH [ colD [ sortcolH ] ] ] ]`

执行查询并以交叉表（透视表）形式显示结果。查询必须返回至少三列。列规范可以是列号（从 1 开始）或列名。

- `colV` — 垂直表头（默认：第 1 列）
- `colH` — 水平表头（默认：第 2 列，必须与 colV 不同）
- `colD` — 网格中显示的数据（默认：剩余列）
- `sortcolH` — 水平表头的可选排序列（必须为整数）

如果多行映射到同一单元格则报错。

### `\bind [ parameter ] ...`

为下一次查询执行设置查询参数。使用扩展查询协议。可与 `\g`、`\gx` 或 `\gset` 组合：

```sql
INSERT INTO tbl1 VALUES ($1, $2) \bind 'first value' 'second value' \g
SELECT * FROM tbl1 WHERE id = $1 \bind 'first value' \gx
SELECT id, name FROM tbl1 WHERE id = $1 \bind 'first value' \gset result_
```

### `\bind_named statement_name [ parameter ] ...`

类似 `\bind`，但将现有预处理语句的名称作为第一个参数。

```sql
INSERT INTO tbls1 VALUES ($1, $2) \parse stmt1
\bind_named stmt1 'first value' 'second value' \g
```

### `\parse statement_name`

从当前查询缓冲区创建预处理语句。空字符串表示未命名的预处理语句。

```sql
SELECT $1 \parse stmt1
```

### `\close_prepared statement_name`

关闭指定的预处理语句。不存在时为空操作。

```sql
SELECT $1 \parse stmt1
\close_prepared stmt1
```

---

## 数据导入/导出

### `\copy`

执行客户端侧复制。与 SQL `COPY` 不同，它使用客户端的文件系统和权限（无需超级用户）。

```
\copy { table [(column_list)] } FROM { 'filename' | program 'command' | stdin | pstdin }
      [ [ WITH ] ( option [, ...] ) ] [ WHERE condition ]

\copy { table [(column_list)] | (query) } TO { 'filename' | program 'command' | stdout | pstdout }
      [ [ WITH ] ( option [, ...] ) ]
```

**关键行为：**
- 整行剩余部分始终作为参数（无变量插值或反引号展开）
- 对于 `FROM stdin`，数据持续到 `\.` 或 EOF
- `pstdin`/`pstdout` 始终使用 psql 的实际 stdin/stdout，无论 `\o` 设置如何
- 除源/目标外的所有选项与 SQL `COPY` 相同

**警告**：`program 'command'` 以客户端用户权限执行 shell 命令。永远不要拼接不受信任的输入。

**提示**：对于多行复制或变量插值，使用 `COPY ... TO STDOUT` 以 `\g filename` 或 `\g |command` 结尾。

---

## 大对象

### `\lo_export loid filename`

从数据库读取指定 OID 的大对象并写入指定文件。使用客户端权限（不同于服务器端的 `lo_export`）。

### `\lo_import filename [ comment ]`

将文件导入为大对象。返回分配的 OID。始终提供人类可读的注释。

```sql
\lo_import '/home/user/photo.jpg' 'product photo'
-- Returns: lo_import 152801
```

### `\lo_list[x+]`

列出数据库中所有大对象及其注释。`+` 显示权限。

### `\lo_unlink loid`

删除指定 OID 的大对象。

---

## 脚本与控制流

### `\i` / `\include` filename

从文件读取并执行输入。相对于当前工作目录。使用 `-` 表示 stdin。

**stdin 行为**：使用 `\i -` 时，psql 从标准输入读取直到 EOF 指示或 `\q` 元命令。这可用于在文件输入与交互输入之间交替。注意 Readline 编辑仅在最外层可用——从嵌套文件读取时不活动。

### `\ir` / `\include_relative` filename

类似 `\i`，但相对路径从当前执行的脚本目录解析（而非工作目录）。对于可移植脚本优先使用 `\ir`。

### `\o` / `\out [ filename ]` / `\o [ |command ]`

将查询输出重定向到文件或管道。不带参数的 `\o` 重置为 stdout。参数以 `|` 开头时，剩余部分按字面传递给 shell（无变量插值）。

**被重定向的内容**："查询结果"包括表、命令响应、通知和 `\d` 命令的输出——但**不包括错误消息**。错误消息始终输出到 stderr。

**不被重定向的内容**：`\echo` 输出到 stdout（不受 `\o` 影响）；使用 `\qecho` 输出到重定向目标。

**提示**：要在重定向输出文件中的查询结果之间插入文本，使用 `\qecho`。

### `\echo text [ ... ]`

将参数打印到 stdout，以空格分隔，后跟换行。如果第一个参数是不带引号的 `-n`，则不写尾部换行。

### `\qecho text [ ... ]`

类似 `\echo` 但输出到查询输出通道（由 `\o` 设置）。

### `\warn text [ ... ]`

类似 `\echo` 但输出到 stderr。

### `\set [ name [ value [ ... ] ] ]`

设置 psql 变量。多个值被拼接。不带参数的 `\set` 显示所有变量。变量名区分大小写，可包含字母、数字、下划线。

这与 SQL `SET` 命令无关。

### `\unset name`

取消设置（删除）psql 变量。大多数控制变量无法真正取消设置；它们恢复为默认值。

### `\prompt [ text ] name`

提示用户输入并存储在命名变量中。多词提示用单引号包围。

**使用 `-f` 标志时的行为**：当 psql 使用 `-f`（从文件读取命令）调用时，`\prompt` 从 stdin/stdout 读取而非终端。交互模式下直接使用终端。

### `\getenv psql_var env_var`

读取环境变量并存储在 psql 变量中。环境变量未定义时不改变。

```sql
\getenv home HOME
\echo :home
-- outputs: /home/postgres
```

### `\setenv name [ value ]`

在 psql 内设置或取消设置环境变量。

```sql
\setenv PAGER less
\setenv LESS -imx4F
```

### `\p` / `\print`

将当前查询缓冲区打印到 stdout。如果缓冲区为空，打印最近执行的查询。

### `\w` / `\write` filename / `\w |command`

将当前查询缓冲区写入文件或通过管道发送到 shell 命令。如果缓冲区为空，写入最近执行的查询。参数以 `|` 开头时，剩余部分按字面传递给 shell。

### `\if` / `\elif` / `\else` / `\endif`

可嵌套的条件块。`\if` 和 `\elif` 将其参数作为布尔值求值（true/false/1/0/on/off/yes/no，不区分大小写）。条件块中的所有反斜杠命令必须出现在同一源文件中。

```sql
SELECT EXISTS(SELECT 1 FROM customer WHERE customer_id = 123) as is_customer,
       EXISTS(SELECT 1 FROM employee WHERE employee_id = 456) as is_employee
\gset
\if :is_customer
    SELECT * FROM customer WHERE customer_id = 123;
\elif :is_employee
    \echo 'is not a customer but is an employee'
    SELECT * FROM employee WHERE employee_id = 456;
\else
    \echo 'not a customer or employee'
\endif
```

被跳过行中的变量引用不会被展开。被跳过行中不执行反引号展开。

---

## 帮助与信息

### `\? [ topic ]`

显示 psql 帮助。主题：
- `commands`（默认）— 反斜杠命令
- `options` — 命令行选项
- `variables` — 配置变量

### `\h` / `\help [ command ]`

SQL 语法帮助。不带参数时列出可用命令。`*` 显示所有命令的帮助。多词命令无需引号：`\h ALTER TABLE`。

与大多数元命令不同，整行都是参数——无变量插值。
