---
title: "Rclone Filtering"
description: "Rclone 过滤规则，包含包含和排除模式"
versionIntroduced: "v1.22"
---

> **官方文档：** [https://rclone.org/filtering/](https://rclone.org/filtering/)
# Filtering, includes and excludes

过滤标志决定 rclone `sync`、`move`、`ls`、`lsl`、`md5sum`、`sha1sum`、`size`、`delete`、`check` 及类似命令作用于哪些文件。

它们通过路径/文件名模式、路径/文件列表、文件年龄和大小，或目录中是否存在某文件来指定。基于桶且没有目录概念的远程存储，以类似方式对对象键、年龄和大小应用过滤。

Rclone `purge` 不遵守过滤规则。

要在不损坏数据的情况下测试过滤规则，可将其应用于 `rclone ls`，或使用 `--dry-run` 和 `-vv` 标志。

Rclone 过滤模式只能用于过滤命令行选项中，不能用于远程存储的指定中。

例如 `rclone copy "remote:dir*.jpg" /path/to/dir` 不会产生过滤效果。
`rclone copy remote:dir /path/to/dir --include "*.jpg"` 会。

**重要** 避免在同一条 rclone 命令中混合使用 `--include...`、`--exclude...` 或 `--filter...` 标志中的任意两种。结果可能不符合预期。请改用 `--filter...` 标志。

## 匹配路径/文件名的模式

### 模式语法 {#patterns}

以下是模式语法的正式定义，[示例](#examples)在下方。

Rclone 匹配规则遵循 glob 风格：

```text
*         matches any sequence of non-separator (/) characters
**        matches any sequence of characters including / separators
?         matches any single non-separator (/) character
[ [ ! ] { character-range } ]
          character class (must be non-empty)
{ pattern-list }
          pattern alternatives
{{ regexp }}
          regular expression to match
c         matches character c (c != *, **, ?, \, [, {, })
\c        matches reserved character c (c = *, **, ?, \, [, {, }) or character class
```

字符范围：

```text
c         matches character c (c != \, -, ])
\c        matches reserved character c (c = \, -, ])
lo - hi   matches character c for lo <= c <= hi
```

模式列表：

```text
pattern { , pattern }
          comma-separated (without spaces) patterns
```

字符类（参见 [Go 正则表达式参考](https://golang.org/pkg/regexp/syntax/)）包括：

```text
Named character classes (e.g. [\d], [^\d], [\D], [^\D])
Perl character classes (e.g. \s, \S, \w, \W)
ASCII character classes (e.g. [[:alnum:]], [[:alpha:]], [[:punct:]], [[:xdigit:]])
```

高级用户可插入正则表达式 regexp — 参见[下文](#regexp)获取更多信息：

```text
Any re2 regular expression not containing `}}`
```

如果过滤模式以 `/` 开头，则它仅在目录树的顶层匹配，**相对于远程存储的根**（不一定是驱动器的根）。如果不以 `/` 开头，则从**路径/文件名的末尾**开始匹配，但只匹配完整的路径元素 — 必须从 `/` 分隔符或路径/文件的开头匹配。

```text
file.jpg   - matches "file.jpg"
           - matches "directory/file.jpg"
           - doesn't match "afile.jpg"
           - doesn't match "directory/afile.jpg"
/file.jpg  - matches "file.jpg" in the root directory of the remote
           - doesn't match "afile.jpg"
           - doesn't match "directory/file.jpg"
```

远程存储的顶层不一定是驱动器的顶层。

例如 Microsoft Windows 本地目录结构

```text
F:
├── bkp
├── data
│   ├── excl
│   │   ├── 123.jpg
│   │   └── 456.jpg
│   ├── incl
│   │   └── document.pdf
```

要将文件夹 `data` 的内容复制到文件夹 `bkp`，并排除子文件夹 `excl` 的内容，以下命令将 `F:\data` 和 `F:\bkp` 视为过滤的顶层。

`rclone copy F:\data\ F:\bkp\ --exclude=/excl/**`

**重要** 在路径/文件名模式中使用 `/` 而非 `\`，即使在 Microsoft Windows 上运行也是如此。

简单模式区分大小写，除非使用 `--ignore-case` 标志。

不使用 `--ignore-case`（默认）

```text
potato - matches "potato"
       - doesn't match "POTATO"
```

使用 `--ignore-case`

```text
potato - matches "potato"
       - matches "POTATO"
```

## 在过滤模式中使用正则表达式 {#regexp}

过滤模式的语法是 glob 风格匹配（类似 `bash` 所使用的），以方便用户使用。但这无法提供对匹配的绝对控制，因此 rclone 也为高级用户提供了正则表达式语法。

Rclone 通常接受 Perl 风格正则表达式，确切语法定义在 [Go 正则表达式参考](https://golang.org/pkg/regexp/syntax/) 中。正则表达式应包含在 `{{` `}}` 中。如果 glob 不以 `/` 开头，它们只匹配最后一个路径段；如果以 `/` 开头，则匹配整个路径名。注意 rclone 不会尝试解析所提供的正则表达式，这意味着使用任何正则表达式过滤将阻止 rclone 使用[目录过滤规则](#directory_filter)，因为它会转而检查每个路径是否符合所提供的正则表达式。

以下是 `{{regexp}}` 如何转换为完整正则表达式以匹配整个路径：

```text
{{regexp}}  becomes (^|/)(regexp)$
/{{regexp}} becomes ^(regexp)$
```

正则表达式语法可以与 glob 语法混合使用，例如

```text
*.{{jpe?g}} to match file.jpg, file.jpeg but not file.png
```

你也可以使用正则表达式标志 — 例如设置不区分大小写

```text
*.{{(?i)jpg}} to match file.jpg, file.JPG but not file.png
```

在正则表达式中使用通配符时要小心 — 通常你不想让它们匹配路径分隔符。要匹配以 `start` 开头、以 `end` 结尾的任何文件名，应写为

```text
{{start[^/]*end\.jpg}}
```

而不是

```text
{{start.*end\.jpg}}
```

后者会匹配名为 `start` 的目录中名为 `end.jpg` 的文件，因为 `.*` 会匹配 `/` 字符。

注意你可以使用 `-vv --dump filters` 以正则表达式格式显示过滤模式 — rclone 通过将 glob 模式转换为正则表达式来实现它们。

## 过滤模式示例 {#examples}

| 描述 | 模式 | 匹配 | 不匹配 |
| ---- | ---- | ---- | ------ |
| 通配符    | `*.jpg` | `/file.jpg`     | `/file.png`    |
|             |         | `/dir/file.jpg` | `/dir/file.png` |
| 根定位      | `/*.jpg` | `/file.jpg`    | `/file.png`    |
|             |          | `/file2.jpg`    | `/dir/file.jpg` |
| 替代选项  | `*.{jpg,png}` | `/file.jpg`     | `/file.gif`    |
|             |         | `/dir/file.png` | `/dir/file.gif` |
| 路径通配符 | `dir/**` | `/dir/anyfile`     | `file.png`    |
|             |          | `/subdir/dir/subsubdir/anyfile` | `/subdir/file.png` |
| 任意字符    | `*.t?t` | `/file.txt`     | `/file.qxt`    |
|             |         | `/dir/file.tzt` | `/dir/file.png` |
| 范围       | `*.[a-z]` | `/file.a`     | `/file.0`    |
|             |         | `/dir/file.b` | `/dir/file.1` |
| 转义      | `*.\?\?\?` | `/file.???`     | `/file.abc`    |
|             |         | `/dir/file.???` | `/dir/file.def` |
| 字符类       | `*.\d\d\d` | `/file.012`     | `/file.abc`    |
|             |         | `/dir/file.345` | `/dir/file.def` |
| 正则表达式      | `*.{{jpe?g}}` | `/file.jpeg`     | `/file.png`    |
|             |         | `/dir/file.jpg` | `/dir/file.jpeeg` |
| 根定位正则表达式 | `/{{.*\.jpe?g}}` | `/file.jpeg`  | `/file.png`    |
|             |                  | `/file.jpg`   | `/dir/file.jpg` |

## 过滤规则如何应用于文件 {#how-filter-rules-work}

Rclone 路径/文件名过滤器由以下一个或多个标志组成：

- `--include`
- `--include-from`
- `--exclude`
- `--exclude-from`
- `--filter`
- `--filter-from`

各个标志可以有多个实例。

Rclone 在内部使用所有包含和排除规则的组合列表。规则处理的顺序会影响过滤结果。

所有相同类型的标志按照上述顺序一起处理，无论不同类型的标志在命令行中以何种顺序出现。

同一标志的多个实例按照它们在命令行中从左到右的位置进行处理。

要混合包含和排除的处理顺序，请使用 `--filter...` 标志。

在 `--include-from`、`--exclude-from` 和 `--filter-from` 标志中，规则从所引用文件的顶部到底部依次处理。

如果指定了 `--include` 或 `--include-from` 标志，rclone 会在内部规则列表底部隐含添加一条 `- **` 规则。通过 `--filter...` 标志指定 `+` 规则不会隐含该规则。

每个经过 rclone 的路径/文件名都与组合过滤列表进行匹配。在首次匹配到某条规则时，该路径/文件名即被包含或排除，不再对该路径/文件处理更多过滤规则。

如果 rclone 在测试所有规则（包括适用的隐含规则）后未找到匹配，则该路径/文件名被包含。

在该阶段被包含的任何路径/文件都由 rclone 命令处理。

`--files-from` 和 `--files-from-raw` 标志会覆盖且不能与其他过滤选项组合使用。

要查看命令的内部组合规则列表（正则表达式形式），请添加 `--dump filters` 标志。使用 `--dump filters` 和 `-vv` 标志运行 rclone 命令会列出内部过滤元素，并显示它们如何应用于每个源路径/文件。目前没有提供直接将正则表达式过滤选项传入 rclone 的方法，尽管字符类过滤规则包含字符类。[Go 正则表达式参考](https://golang.org/pkg/regexp/syntax/)

### 过滤规则如何应用于目录 {#directory_filter}

Rclone 命令应用于路径/文件名而非目录。目录的全部内容可通过模式 `directory/*` 匹配过滤，或通过 `directory/**` 递归匹配。

目录过滤规则以结尾的 `/` 分隔符定义。

例如 `/directory/subdirectory/` 是一条 rclone 目录过滤规则。

Rclone 命令可以使用目录过滤规则来确定是否递归进入子目录。这有可能通过避免列出不必要的目录来优化对远程存储的访问。是否需要优化取决于具体的过滤规则和源远程存储的内容。

如果使用了任何[正则表达式过滤](#regexp)，则无法进行目录递归优化，因为 rclone 必须检查每个路径是否符合所提供的正则表达式。

目录递归优化在以下情况之一发生时生效：

- 源远程存储不支持 rclone `ListR` 原语。local、sftp、Microsoft OneDrive 和 WebDAV 不支持 `ListR`。Google Drive 和大多数桶类型存储支持。[完整列表](https://rclone.org/overview/#optional-features)

- 在其他远程存储（支持 `ListR` 的）上，如果 rclone 命令不是自然递归的，并且未使用 `--fast-list` 标志运行。`ls`、`lsf -R` 和 `size` 是自然递归的，而 `sync`、`copy` 和 `move` 不是。

- 对 rclone 命令应用了 `--disable ListR` 标志时。

Rclone 命令从路径/文件过滤规则中推导出目录过滤规则。要查看 rclone 为命令推导的目录过滤规则，请指定 `--dump filters` 标志。

例如对于包含规则

```text
/a/*.jpg
```

Rclone 推导出目录包含规则

```text
/a/
```

在 rclone 命令中指定的目录过滤规则可以限制 rclone 命令的范围，但仍需指定路径/文件过滤器。

例如 `rclone ls remote: --include /directory/` 不会匹配任何文件。因为它是 `--include` 选项，所以隐含了 `--exclude **` 规则，而 `/directory/` 模式仅用于优化对远程存储的访问（忽略该目录之外的所有内容）。

例如 `rclone ls remote: --filter-from filter-list.txt`，其中 `filter-list.txt` 文件内容为：

```text
- /dir1/
- /dir2/
+ *.pdf
- **
```

`dir1` 或 `dir2` 目录及其子目录中的所有文件被完全排除在列表之外。仅列出 `remote:` 根目录或其子目录中后缀为 `pdf` 的文件。`- **` 规则阻止列出未被上述规则匹配的任何路径/文件。

`exclude-if-present` 选项根据目录中是否存在某文件创建目录排除规则，优先级高于其他 rclone 目录过滤规则。

当使用模式列表语法时，如果模式项包含 `/` 或 `**`，则 rclone 将无法从该模式列表推导目录过滤规则。

例如对于包含规则

```text
{dir1/**,dir2/**}
```

Rclone 只会匹配 `dir1` 或 `dir2` 目录下的文件，但无法使用此过滤器排除目录 `dir3` 的遍历。

目录递归优化可能影响性能，但通常不影响结果。一个例外是使用 `--create-empty-src-dirs` 选项的同步操作，任何被遍历的空目录都会被创建。对于上面的模式列表示例 `{dir1/**,dir2/**}`，这会在目标上创建一个空目录 `dir3`（当它存在于源上时）。将过滤器改为 `{dir1,dir2}/**`，或拆分为两条包含规则 `--include dir1/** --include dir2/**`，将匹配相同的文件，同时也会过滤目录，结果是空目录 `dir3` 不再被创建。

### `--exclude` - 排除匹配模式的文件

基于单个排除规则从 rclone 命令中排除路径/文件名。

此标志可重复使用。过滤标志的处理顺序见上文。

`--exclude` 不应与 `--include`、`--include-from`、`--filter` 或 `--filter-from` 标志一起使用。

`--exclude` 与 `--files-from` 或 `--files-from-raw` 标志组合时无效。

例如 `rclone ls remote: --exclude *.bak` 从列表中排除所有 .bak 文件。

例如 `rclone size remote: --exclude "/dir/**"` 返回 `remote:` 上排除根目录 `dir` 及其子目录中文件后的总大小。

例如在 Microsoft Windows 上 `rclone ls remote: --exclude "*\[{JP,KR,HK}\]*"` 列出 `remote:` 中名称不含 `[JP]`、`[KR]` 或 `[HK]` 的文件。引号阻止 shell 解释 `\` 字符。`\` 字符转义 `[` 和 `]`，使 rclone 过滤器将它们视为字面值而非字符范围。`{` 和 `}` 定义 rclone 模式列表。对于其他操作系统需要使用单引号，即 `rclone ls remote: --exclude '*\[{JP,KR,HK}\]*'`

### `--exclude-from` - 从文件读取排除模式

基于命名文件中的规则从 rclone 命令中排除路径/文件名。该文件包含注释和模式规则列表。

例如 `exclude-file.txt`：

```text
# a sample exclude rule file
*.bak
file2.jpg
```

`rclone ls remote: --exclude-from exclude-file.txt` 列出 `remote:` 上的文件，排除名为 `file2.jpg` 或后缀为 `.bak` 的文件。这等效于 `rclone ls remote: --exclude file2.jpg --exclude "*.bak"`。

此标志可重复使用。过滤标志的处理顺序见上文。

当多个排除过滤规则应用于 rclone 命令时，`--exclude-from` 标志很有用。

`--exclude-from` 不应与 `--include`、`--include-from`、`--filter` 或 `--filter-from` 标志一起使用。

`--exclude-from` 与 `--files-from` 或 `--files-from-raw` 标志组合时无效。

`--exclude-from` 后跟 `-` 从标准输入读取过滤规则。

### `--include` - 包含匹配模式的文件

基于路径/文件名为 rclone 命令添加单条包含规则。

此标志可重复使用。过滤标志的处理顺序见上文。

`--include` 与 `--files-from` 或 `--files-from-raw` 标志组合时无效。

`--include` 在 rclone 内部过滤列表末尾隐含 `--exclude **`。因此，如果将 `--include` 和 `--include-from` 标志与 `--exclude`、`--exclude-from`、`--filter` 或 `--filter-from` 混合使用，必须在包含语句中为所有需要的文件使用包含规则。要获得更大灵活性，请使用 `--filter-from` 标志。

例如 `rclone ls remote: --include "*.{png,jpg}"` 列出 `remote:` 上后缀为 `.png` 和 `.jpg` 的文件。所有其他文件被排除。

例如多条 rclone copy 命令可与 `--include` 和模式列表组合。

```console
rclone copy /vol1/A remote:A
rclone copy /vol1/B remote:B
```

等效于：

```console
rclone copy /vol1 remote: --include "{A,B}/**"
```

例如 `rclone ls remote:/wheat --include "??[^[:punct:]]*"` 列出 `remote:` 目录 `wheat`（及其子目录）中第三个字符不是标点符号的文件。此示例使用了 [ASCII 字符类](https://golang.org/pkg/regexp/syntax/)。

### `--include-from` - 从文件读取包含模式

基于命名文件中的规则为 rclone 命令添加路径/文件名。该文件包含注释和模式规则列表。

例如 `include-file.txt`：

```text
# a sample include rule file
*.jpg
file2.avi
```

`rclone ls remote: --include-from include-file.txt` 列出 `remote:` 上名为 `file2.avi` 或后缀为 `.jpg` 的文件。这等效于 `rclone ls remote: --include file2.avi --include "*.jpg"`。

此标志可重复使用。过滤标志的处理顺序见上文。

当多个包含过滤规则应用于 rclone 命令时，`--include-from` 标志很有用。

`--include-from` 在 rclone 内部过滤列表末尾隐含 `--exclude **`。因此，如果将 `--include` 和 `--include-from` 标志与 `--exclude`、`--exclude-from`、`--filter` 或 `--filter-from` 混合使用，必须在包含语句中为所有需要的文件使用包含规则。要获得更大灵活性，请使用 `--filter-from` 标志。

`--include-from` 与 `--files-from` 或 `--files-from-raw` 标志组合时无效。

`--include-from` 后跟 `-` 从标准输入读取过滤规则。

### `--filter` - 添加文件过滤规则

基于单条包含或排除规则（以 `+` 或 `-` 格式），为 rclone 命令指定路径/文件名。

此标志可重复使用。过滤标志的处理顺序见上文。

`--filter +` 与 `--include` 不同。在 `--include` 的情况下，rclone 隐含一条 `--exclude *` 规则，添加到内部规则列表底部。`--filter...+` 不会隐含该规则。

`--filter` 与 `--files-from` 或 `--files-from-raw` 标志组合时无效。

`--filter` 不应与 `--include`、`--include-from`、`--exclude` 或 `--exclude-from` 标志一起使用。

例如 `rclone ls remote: --filter "- *.bak"` 从 `remote:` 列表中排除所有 `.bak` 文件。

### `--filter-from` - 从文件读取过滤模式

基于命名文件中的规则为 rclone 命令添加路径/文件名。该文件包含注释和模式规则列表。包含
<!-- markdownlint-disable-next-line no-space-in-code -->
规则以 `+ ` 开头，排除规则以 `- ` 开头。`!` 清除现有规则。规则按定义的顺序处理。

此标志可重复使用。过滤标志的处理顺序见上文。

按最严格的规则在前、逐渐放宽的顺序排列过滤规则。

以 # 或 ; 开头的行被忽略，可用于编写注释。不支持行内注释。*使用 `-vv --dump filters` 查看它们在最终正则表达式中的形式。*

例如 `filter-file.txt`：

```text
# a sample filter rule file
- secret*.jpg
+ *.jpg
+ *.png
+ file2.avi
- /dir/tmp/** # WARNING! This text will be treated as part of the path.
- /dir/Trash/**
+ /dir/**
# exclude everything else
- *
```

`rclone ls remote: --filter-from filter-file.txt` 列出 `remote:` 上的路径/文件，包含所有 `jpg` 和 `png` 文件，排除任何匹配 `secret*.jpg` 的文件，并包含 `file2.avi`。它还包含 `remote` 根目录下 `dir` 目录中的所有内容，但排除 `remote:dir/Trash`。其他所有内容被排除。

例如替代 `filter-file.txt`：

```text
- secret*.jpg
+ *.jpg
+ *.png
+ file2.avi
- *
```

列出文件 `file1.jpg`、`file3.png` 和 `file2.avi`，而 `secret17.jpg` 以及不含 `.jpg` 或 `.png` 后缀的文件被排除。

例如替代 `filter-file.txt`：

```text
+ *.jpg
+ *.gif
!
+ 42.doc
- *
```

仅列出文件 42.doc。先前的规则被 `!` 清除。

### `--files-from` - 读取源文件名列表

从命名文件的列表中为 rclone 命令添加路径/文件。Rclone 按列表顺序处理路径/文件名，不处理其他文件。

使用 `--files-from` 时，其他过滤标志（`--include`、`--include-from`、`--exclude`、`--exclude-from`、`--filter` 和 `--filter-from`）被忽略。

`--files-from` 期望文件列表作为输入。输入行的前导和尾随空白被去除。以 `#` 或 `;` 开头的行被忽略。

`--files-from` 后跟 `-` 从标准输入读取文件列表。

带 `--files-from` 标志的 rclone 命令会遍历远程存储，将 `--files-from` 中的名称视为一组过滤器。

如果同时使用 `--no-traverse` 和 `--files-from` 标志，rclone 命令不遍历远程存储。而是单独处理文件中命名的每个路径/文件。对于每个路径/文件名，通常需要 1 次 API 调用。对于较短的 `--files-from` 列表和包含大量文件的远程存储，这可能很高效。

如果 `--files-from` 文件中有任何名称在源远程存储中不存在，rclone 命令不会报错。

`--files-from` 标志可在单条 rclone 命令中重复使用，以从多个文件读取路径/文件名。文件按命令行中从左到右的顺序读取。

`--files-from` 文件中的路径被解释为以 rclone 命令中指定的根为起始。前导 `/` 分隔符被忽略。如需以原始方式处理输入，参见 [--files-from-raw](#files-from-raw-read-list-of-source-file-names-without-any-processing)。

例如文件 `files-from.txt`：

```text
# comment
file1.jpg
subdir/file2.jpg
```

`rclone copy --files-from files-from.txt /home/me/pics remote:pics`
复制以下文件（如果存在），且仅复制这些文件。

```text
/home/me/pics/file1.jpg        → remote:pics/file1.jpg
/home/me/pics/subdir/file2.jpg → remote:pics/subdir/file2.jpg
```

例如通过绝对路径引用复制以下文件：

```text
/home/user1/42
/home/user1/dir/ford
/home/user2/prefect
```

首先找到一个公共子目录 — 此例中为 `/home`，将剩余文件放入 `files-from.txt`，带或不带前导 `/`，例如：

```text
user1/42
user1/dir/ford
user2/prefect
```

然后复制到远程存储：

```console
rclone copy --files-from files-from.txt /home remote:backup
```

三个文件传输如下：

```text
/home/user1/42       → remote:backup/user1/important
/home/user1/dir/ford → remote:backup/user1/dir/file
/home/user2/prefect  → remote:backup/user2/stuff
```

或者如果选择 `/` 作为根，`files-from.txt` 将为：

```text
/home/user1/42
/home/user1/dir/ford
/home/user2/prefect
```

复制命令为：

```console
rclone copy --files-from files-from.txt / remote:backup
```

然后远程存储上将多一个 `home` 目录：

```text
/home/user1/42       → remote:backup/home/user1/42
/home/user1/dir/ford → remote:backup/home/user1/dir/ford
/home/user2/prefect  → remote:backup/home/user2/prefect
```

### `--files-from-raw` - 读取源文件名列表（不做任何处理）

此标志与 `--files-from` 相同，只是输入以原始方式读取。带前导/尾随空白的行，以及以 `;` 或 `#` 开头的行不做任何处理。[rclone lsf](/commands/rclone_lsf/) 具有兼容格式，可用于从远程存储导出文件列表作为 `--files-from-raw` 的输入。

### `--ignore-case` - 使搜索不区分大小写

默认情况下，rclone 过滤模式区分大小写。`--ignore-case` 标志使命令行上所有过滤模式不区分大小写。

例如 `--include "zaphod.txt"` 不匹配文件 `Zaphod.txt`。使用 `--ignore-case` 则匹配。

## 引用 shell 元字符

包含 shell 元字符的过滤模式在 shell 中的行为可能不符合预期，可能需要引用。

例如 linux、OSX（`*` 元字符）

- `--include \*.jpg`
- `--include '*.jpg'`
- `--include='*.jpg'`

Microsoft Windows 由命令而非 shell 进行扩展，因此 `--include *.jpg` 不需要引用。

如果遇到 rclone 错误
`Command .... needs .... arguments maximum: you provided .... non flag arguments:`
其原因通常是远程存储名称或标志值中包含空格。解决方法是引用包含空格的值。

## 其他过滤器

### `--min-size` - 不传输任何小于此大小的文件

控制 rclone 命令范围内的最小文件大小。默认单位为 `KiB`，但缩写 `B`、`K`、`M`、`G`、`T` 或 `P` 均有效。

例如 `rclone ls remote: --min-size 50k` 列出 `remote:` 上 50 KiB 或更大的文件。

参见[大小选项文档](/docs/#size-options)获取更多信息。

### `--max-size` - 不传输任何大于此大小的文件

控制 rclone 命令范围内的最大文件大小。默认单位为 `KiB`，但缩写 `B`、`K`、`M`、`G`、`T` 或 `P` 均有效。

例如 `rclone ls remote: --max-size 1G` 列出 `remote:` 上 1 GiB 或更小的文件。

参见[大小选项文档](/docs/#size-options)获取更多信息。

### `--max-age` - 不传输任何超过此时间的文件

控制 rclone 命令范围内文件的最大年龄。

`--max-age` 仅适用于文件，不适用于目录。

例如 `rclone ls remote: --max-age 2d` 列出 `remote:` 上 2 天或更短时间内修改的文件。

参见[时间选项文档](/docs/#time-options)获取有效格式。

### `--min-age` - 不传输任何新于此时间的文件

控制 rclone 命令范围内文件的最小年龄。（参见 `--max-age` 获取有效格式）

`--min-age` 仅适用于文件，不适用于目录。

例如 `rclone ls remote: --min-age 2d` 列出 `remote:` 上 2 天或更长时间前修改的文件。

参见[时间选项文档](/docs/#time-options)获取有效格式。

### `--hash-filter` - 确定性地选择文件子集 {#hash-filter}

`--hash-filter` 标志可选择确定性的文件子集，适用于：

1. 在多台机器上运行大型同步操作。
2. 检查文件子集是否存在位腐。
3. 任何需要文件样本的其他操作。

#### 语法

该标志接受以分数表示的两个参数：

```text
--hash-filter K/N
```

- `N`：总分分区数（必须为正整数）。
- `K`：要选择的特定分区（从 `0` 到 `N` 的整数）。

例如：

- `--hash-filter 1/3`：选择前三分之一的文件。
- `--hash-filter 2/3` 和 `--hash-filter 3/3`：分别选择第二和第三分区。

每个分区不重叠，确保所有文件被覆盖且不重复。

#### 随机分区选择

使用 `@` 作为 `K` 来随机选择一个分区：

```text
--hash-filter @/M
```

例如 `--hash-filter @/3` 将随机选择 0 到 2 之间的一个数字。这在重试之间保持不变。

#### 工作原理

- Rclone 取每个文件的完整路径，将其规范化为小写，并应用 Unicode 规范化。
- 然后对规范化路径进行哈希，生成 64 位数字。
- 哈希结果对 `N` 取模，将文件分配到某个分区。
- 如果计算出的分区与 `K` 不匹配，则排除该文件。
- 如果文件未被排除，其他过滤器仍可应用。

**重要：** Rclone 将遍历所有目录以应用过滤。

#### 使用注意事项

- 可安全用于 `rclone sync`；源和目标的选择将匹配。
- **不要**与 `--delete-excluded` 一起使用，因为这可能删除未选中的文件。
- 如果使用了 `--files-from` 则被忽略。

#### 示例

##### 将文件分为 4 个分区

假设当前目录包含 `file1.jpg` 到 `file9.jpg`：

```console
$ rclone lsf --hash-filter 0/4 .
file1.jpg
file5.jpg

$ rclone lsf --hash-filter 1/4 .
file3.jpg
file6.jpg
file9.jpg

$ rclone lsf --hash-filter 2/4 .
file2.jpg
file4.jpg

$ rclone lsf --hash-filter 3/4 .
file7.jpg
file8.jpg

$ rclone lsf --hash-filter 4/4 . # the same as --hash-filter 0/4
file1.jpg
file5.jpg
```

##### 同步前四分之一的文件

```console
rclone sync --hash-filter 1/4 source:path destination:path
```

##### 随机检查 1% 的文件完整性

```console
rclone check --download --hash-filter @/100 source:path destination:path
```

## 其他标志

### `--delete-excluded` - 删除目标上被排除的文件

**重要** 此标志对数据有危险 — 先使用 `--dry-run` 和 `-v`。

与 `rclone sync` 配合使用时，`--delete-excluded` 删除目标上被命令排除的任何文件。

例如 `rclone sync --interactive A: B:` 的范围可以这样限制：

```console
rclone --min-size 50k --delete-excluded sync A: B:
```

`B:` 上所有小于 50 KiB 的文件被删除，因为它们被 rclone sync 命令排除。

### `--dump filters` - 将过滤器输出到标准输出

以正则表达式格式将定义的过滤器输出到标准输出。

可用于调试。

## 基于文件排除目录

`--exclude-if-present` 标志根据目录中是否存在命名文件来控制该目录是否在 rclone 命令范围内。该标志可重复使用以检查多个文件名，其中任何一个的存在都会排除该目录。

此标志优先级高于其他过滤标志。

例如以下目录结构：

```text
dir1/file1
dir1/dir2/file2
dir1/dir2/dir3/file3
dir1/dir2/dir3/.ignore
```

命令 `rclone ls --exclude-if-present .ignore dir1` 不会列出 `dir3`、`file3` 或 `.ignore`。

## 元数据过滤器 {#metadata}

元数据过滤器的工作方式与普通文件名过滤器非常相似，只是它们匹配对象上的[元数据](/docs/#metadata)。

元数据应以 `key=value` 模式指定。可以使用正常的[过滤模式](#patterns)或[正则表达式](#regexp)进行通配。

例如，如果你想仅列出模式为 `100664` 的本地文件，可以这样做：

```console
rclone lsf -M --files-only --metadata-include "mode=100664" .
```

或者如果你想显示在给定日期具有 `atime`、`mtime` 或 `btime` 的文件：

```console
rclone lsf -M --files-only --metadata-include "[abm]time=2022-12-16*" .
```

与文件过滤类似，元数据过滤仅适用于文件，不适用于目录。

可使用以下标志应用过滤器。

- `--metadata-include`      - 包含匹配模式的元数据
- `--metadata-include-from` - 从文件读取元数据包含模式
  （使用 - 从标准输入读取）
- `--metadata-exclude`      - 排除匹配模式的元数据
- `--metadata-exclude-from` - 从文件读取元数据排除模式
  （使用 - 从标准输入读取）
- `--metadata-filter`       - 添加元数据过滤规则
- `--metadata-filter-from`  - 从文件读取元数据过滤模式
  （使用 - 从标准输入读取）

每个标志可重复使用。参见[过滤规则如何应用](#how-filter-rules-work)部分了解更多详情 — 这些标志与文件名过滤标志的工作方式相同，只是将文件名模式替换为元数据模式。

## 常见陷阱

[rclone 论坛](https://forum.rclone.org/)上最常见的过滤支持问题是：

- 未使用相对于远程存储根的路径
- 未使用 `/` 从远程存储根开始匹配
- 未使用 `**` 匹配目录的内容
