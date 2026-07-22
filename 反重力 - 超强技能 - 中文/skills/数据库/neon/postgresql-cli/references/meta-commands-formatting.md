psql 元命令参考的一部分。另见：meta-commands-core.md、meta-commands-inspection.md

# psql 元命令 — 输出格式化与管道模式

## 目录

- [输出格式化](#输出格式化)
- [管道模式](#管道模式)
- [会话管理](#会话管理)

---

## 输出格式化

### `\pset [ option [ value ] ]`

设置影响查询结果表输出的选项。不带参数时显示当前设置。

| 选项 | 值 | 描述 |
|------|-----|------|
| `border` | 0-2（latex 为 3） | 边框/线条样式。数值越高线条越多。 |
| `columns` | 整数 | wrapped 格式的目标宽度。0 = 使用 `COLUMNS` 环境变量或屏幕宽度。非零值在输出到文件或管道时也会折行（通常文件/管道输出不折行）。 |
| `csv_fieldsep` | 字符 | CSV 字段分隔符（默认：逗号） |
| `expanded`（或 `x`） | `on`、`off`、`auto` | 垂直显示。`auto` 在比屏幕宽时使用展开模式。注意：`auto` 仅在 `aligned` 和 `wrapped` 格式中有效。 |
| `fieldsep` | 字符串 | 非对齐输出的字段分隔符（默认：`\|`） |
| `fieldsep_zero` | — | 将字段分隔符设为 NUL 字节 |
| `footer` | `on`、`off` | 切换行数页脚显示 |
| `format` | `aligned`、`asciidoc`、`csv`、`html`、`latex`、`latex-longtable`、`troff-ms`、`unaligned`、`wrapped` | 输出格式。见下方格式描述。 |
| `linestyle` | `ascii`、`old-ascii`、`unicode` | 边框字符样式。`ascii` 使用 `+`、`-`、`|` 字符。`old-ascii` 使用 `:` 和 `;` 绘制边框。`unicode` 使用 Unicode 绘图字符。 |
| `null` | 字符串 | NULL 值的显示字符串（默认：空） |
| `numericlocale` | `on`、`off` | 本地化数字格式化 |
| `pager` | `on`、`off`、`always` | 分页器控制。使用 `PSQL_PAGER` 或 `PAGER` 环境变量。对于 `\watch` 输出，`PSQL_WATCH_PAGER` 优先于两者。 |
| `pager_min_lines` | 整数 | 激活分页器的最小行数（默认：0） |
| `recordsep` | 字符串 | 非对齐模式的记录分隔符（默认：换行） |
| `recordsep_zero` | — | 将记录分隔符设为 NUL 字节 |
| `tableattr`（或 `T`） | 字符串 | HTML：table 标签属性（如 `border=1`）。latex-longtable：空格分隔的比例列宽（如 `'0.2 0.2 0.6'`）。 |
| `title`（或 `C`） | 字符串 | 表标题。不带值时取消设置。 |
| `tuples_only`（或 `t`） | `on`、`off` | 仅显示数据，无表头/页脚 |
| `unicode_border_linestyle` | `single`、`double` | Unicode 边框绘制 |
| `unicode_column_linestyle` | `single`、`double` | Unicode 列绘制 |
| `unicode_header_linestyle` | `single`、`double` | Unicode 表头绘制 |
| `xheader_width` | `full`、`column`、`page` 或整数 | 展开输出表头的最大宽度 |

### 格式描述

| 格式 | 描述 |
|------|------|
| `aligned` | 标准的可读表格，列对齐（默认）。 |
| `wrapped` | 类似 `aligned`，但长值折行以适应列宽。带下划线的表头在续行中不重复。 |
| `unaligned` | 所有列在一行上，以 `fieldsep` 分隔。适用于脚本输出。 |
| `csv` | 符合 RFC 4180 的 CSV 输出。使用 `csv_fieldsep`（默认：逗号）。可安全导入电子表格等工具。 |
| `html` | HTML `<table>` 标记。 |
| `asciidoc` | 用于文档的 AsciiDoc 表格格式。 |
| `latex` | LaTeX tabular 格式。 |
| `latex-longtable` | 用于多页表格的 LaTeX longtable 格式。通过 `\pset tableattr` 支持比例列宽（如 `'0.2 0.2 0.6'`）。 |
| `troff-ms` | troff ms 宏表格格式。 |

### 格式化快捷方式

| 快捷方式 | 等价命令 |
|----------|---------|
| `\a` | `\pset format unaligned`（切换） |
| `\C [title]` | `\pset title` |
| `\f [string]` | `\pset fieldsep` |
| `\H` | `\pset format html`（切换） |
| `\t` | `\pset tuples_only`（切换） |
| `\T table_options` | `\pset tableattr` |
| `\x [on\|off\|auto]` | `\pset expanded` |

---

## 管道模式

管道模式将 SQL 语句批量打包为更少的网络往返，提高性能。PostgreSQL 14+ 可用。

### 管道命令

| 命令 | 描述 |
|------|------|
| `\startpipeline` | 开始管道块 |
| `\endpipeline` | 结束管道块并处理剩余结果 |
| `\sendpipeline` | 将当前查询缓冲区追加到管道，不等待结果 |
| `\syncpipeline` | 发送同步消息但不结束管道 |
| `\flushrequest` | 请求服务器刷新但不同步 |
| `\flush` | 手动推送未发送的数据到服务器 |
| `\getresults [N]` | 读取待处理结果（N=0 或省略 = 全部） |

### 管道规则

- 管道模式中所有查询使用扩展查询协议
- 查询以分号或 `\sendpipeline` 追加
- 允许的元命令：`\bind`、`\bind_named`、`\parse`、`\close_prepared`
- 不允许：`\g`、`\gx`、`\gdesc`（及其他消费结果的命令）
- 管道模式不支持 `COPY`
- `%P` 提示符变量可用于显示管道状态（`on`、`off` 或 `abort`）

### 示例

```sql
\startpipeline
  SELECT * FROM pg_class;
  SELECT 1 \bind \sendpipeline
  \flushrequest
  \getresults
\endpipeline
```

---

## 会话管理

### `\e` / `\edit [ filename ] [ line_number ]`

在外部编辑器中打开查询缓冲区（或文件）。保存时，缓冲区被重新解析。完整查询立即执行。光标定位到指定行号。见 `$EDITOR` / `$VISUAL` 配置编辑器。

### `\ef [ function_description [ line_number ] ]`

以 `CREATE OR REPLACE FUNCTION/PROCEDURE` 命令的形式编辑函数或过程定义。通过名称或名称加参数类型指定函数。不带参数时显示空白模板。行号定位到函数体内。

与大多数元命令不同，整行都是参数——无变量插值。

### `\ev [ view_name [ line_number ] ]`

以 `CREATE OR REPLACE VIEW` 命令的形式编辑视图定义。不带参数时显示空白模板。

### `\cd [ directory ]`

更改当前工作目录。不带参数时切换到主目录。

```sql
\cd /tmp
\! pwd           -- /tmp
\cd              -- back to home directory
```

### `\r` / `\reset`

清空查询缓冲区。

### `\s [ filename ]`

将命令历史打印到文件或 stdout。需要 Readline 支持。

### `\timing [ on | off ]`

切换（或显式设置）查询执行时间显示。以毫秒显示；超过 1 秒的间隔还显示分:秒、小时、天数等。

### `\errverbose`

以最高详细程度重复最近的服务器错误消息（如同 `VERBOSITY=verbose` 且 `SHOW_CONTEXT=always`）。

### `\restrict restrict_key` / `\unrestrict restrict_key`

进入/退出仅允许 `\unrestrict` 的受限模式。密钥必须为字母数字。主要由 `pg_dump`/`pg_restore` 使用。
