---
title: "Union"
description: "远程统一"
versionIntroduced: "v1.44"
---

> **官方文档：** [https://rclone.org/union/](https://rclone.org/union/)
# Union

`union` 后端将多个远程存储连接在一起，形成统一的视图。

在通过 `rclone config` 进行初始设置时，你需要以空格分隔的列表形式指定上游远程。上游远程可以是本地路径或其他远程。

属性 `:ro`、`:nc` 和 `:writeback` 可以附加在远程末尾，将远程标记为**只读**、**禁止创建**或**回写**，例如 `remote:directory/subdirectory:ro` 或 `remote:directory/subdirectory:nc`。

- `:ro` 表示文件仅从此处读取，永不写入
- `:nc` 表示不会在此处创建新文件或目录
- `:writeback` 表示在其他远程中找到的文件将被回写到此远程。详见[回写章节](#writeback)。

上游远程中可以使用子文件夹。假设有一个名为 `backup` 的 union 远程，对应远程 `mydrive:private/backup`。调用 `rclone mkdir backup:desktop` 与调用 `rclone mkdir mydrive:private/backup/desktop` 完全相同。

对于包含 `..` 段的路径没有特殊处理。调用 `rclone mkdir backup:../desktop` 与调用 `rclone mkdir mydrive:private/backup/../desktop` 完全相同。

## 配置

以下是为本地文件夹创建名为 `remote` 的 union 的示例。首先运行：

```console
rclone config
```

这将引导你完成交互式设置过程：

```text
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> remote
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / Union merges the contents of several remotes
   \ "union"
[snip]
Storage> union
List of space separated upstreams.
Can be 'upstreama:test/dir upstreamb:', '\"upstreama:test/space:ro dir\" upstreamb:', etc.
Enter a string value. Press Enter for the default ("").
upstreams> remote1:dir1 remote2:dir2 remote3:dir3
Policy to choose upstream on ACTION class.
Enter a string value. Press Enter for the default ("epall").
action_policy>
Policy to choose upstream on CREATE class.
Enter a string value. Press Enter for the default ("epmfs").
create_policy>
Policy to choose upstream on SEARCH class.
Enter a string value. Press Enter for the default ("ff").
search_policy>
Cache time of usage and free space (in seconds). This option is only useful when a path preserving policy is used.
Enter a signed integer. Press Enter for the default ("120").
cache_time>
Remote config
Configuration complete.
Options:
- type: union
- upstreams: remote1:dir1 remote2:dir2 remote3:dir3
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
Current remotes:

Name                 Type
====                 ====
remote               union

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> q
```

配置完成后，你可以这样使用 `rclone`：

列出 `remote1:dir1`、`remote2:dir2` 和 `remote3:dir3` 中顶层目录

```console
rclone lsd remote:
```

列出 `remote1:dir1`、`remote2:dir2` 和 `remote3:dir3` 中的所有文件

```console
rclone ls remote:
```

将另一个本地目录复制到 union 目录中名为 source 的位置，该文件将被放入 `remote3:dir3`

```console
rclone copy C:\source remote:source
```

### 行为 / 策略

union 后端的行为灵感来自 [trapexit/mergerfs](https://github.com/trapexit/mergerfs)。所有功能被分为 3 个类别：**action**、**create** 和 **search**。这些功能和类别可以分配策略，策略决定了执行该行为时选择哪个文件或目录。任何策略都可以分配给功能或类别，但有些策略在实际中可能不太有用。例如：**rand**（随机）对于文件创建（create）可能有用，但如果用于 `delete` 且文件有多个副本，则可能导致非常奇怪的行为。

### 功能 / 类别分类

| 类别 | 描述 | 功能 |
|----------|--------------------------|-------------------------------------------------------------------------------------|
| action | 写入已有文件 | move, rmdir, rmdirs, delete, purge 以及 copy, sync（作为目标且文件已存在时） |
| create | 创建不存在的文件 | copy, sync（作为目标且文件不存在时） |
| search | 读取和列出文件 | ls, lsd, lsl, cat, md5sum, sha1sum 以及 copy, sync（作为源） |
| N/A | | size, about |

### 路径保留

策略（如下所述）分为两种基本类型：`路径保留` 和 `非路径保留`。

所有以 `ep` 开头的策略（**epff**、**eplfs**、**eplus**、**epmfs**、**eprand**）都是 `路径保留` 策略。`ep` 代表 `existing path`（已有路径）。

路径保留策略只会考虑相对路径已经存在的上游。

使用非路径保留策略时，路径将在目标上游中按需创建。

### 与配额相关的策略

某些策略依赖配额信息。只有当你的上游支持相应的配额字段时，才应使用这些策略。

| 策略 | 所需字段 |
|------------|----------------|
| lfs, eplfs | Free |
| mfs, epmfs | Free |
| lus, eplus | Used |
| lno, eplno | Objects |

要检查你的上游是否支持该字段，运行 `rclone about remote: [flags]` 并查看所需字段是否存在。

### 过滤器

策略的基本工作方式是搜索上游远程并创建文件/路径列表供功能操作。策略负责过滤和排序。策略类型决定了排序方式，但过滤规则基本统一，如下所述。

- 没有 **search** 策略会进行过滤。
- 所有 **action** 策略会过滤掉标记为**只读**的远程。
- 所有 **create** 策略会过滤掉标记为**只读**或**禁止创建**的远程。

如果所有远程都被过滤，将返回错误。

### 策略说明

策略定义灵感来自 [trapexit/mergerfs](https://github.com/trapexit/mergerfs)，但并不完全相同。由于远程文件系统的延迟大得多，某些策略定义可能有所不同。

| 策略 | 描述 |
|------------------|------------------------------------------------------------|
| all | 搜索类别：与 **epall** 相同。操作类别：与 **epall** 相同。创建类别：在所有上游上执行操作。 |
| epall (existing path, all) | 搜索类别：按配置顺序，在相对路径存在的第一个上游上操作。操作类别：在所有找到的上游上执行。创建类别：在相对路径存在的所有上游上执行操作。 |
| epff (existing path, first found) | 按上游响应顺序，在相对路径存在的第一个上游上操作。 |
| eplfs (existing path, least free space) | 在相对路径存在的所有上游中，选择可用空间最少的。 |
| eplus (existing path, least used space) | 在相对路径存在的所有上游中，选择已用空间最少的。 |
| eplno (existing path, least number of objects) | 在相对路径存在的所有上游中，选择对象数最少的。 |
| epmfs (existing path, most free space) | 在相对路径存在的所有上游中，选择可用空间最多的。 |
| eprand (existing path, random) | 调用 **epall** 然后随机化。仅返回一个上游。 |
| ff (first found) | 搜索类别：与 **epff** 相同。操作类别：与 **epff** 相同。创建类别：按上游响应顺序，在第一个找到的上游上操作。 |
| lfs (least free space) | 搜索类别：与 **eplfs** 相同。操作类别：与 **eplfs** 相同。创建类别：选择可用空间最少的上游。 |
| lus (least used space) | 搜索类别：与 **eplus** 相同。操作类别：与 **eplus** 相同。创建类别：选择已用空间最少的上游。 |
| lno (least number of objects) | 搜索类别：与 **eplno** 相同。操作类别：与 **eplno** 相同。创建类别：选择对象数最少的上游。 |
| mfs (most free space) | 搜索类别：与 **epmfs** 相同。操作类别：与 **epmfs** 相同。创建类别：选择可用空间最多的上游。 |
| newest | 选择 mtime 最大的文件/目录。 |
| rand (random) | 调用 **all** 然后随机化。仅返回一个上游。 |

### 回写 {#writeback}

上游远程上的 `:writeback` 标签可以用来创建一个简单的缓存系统，如下所示：

```ini
[union]
type = union
action_policy = all
create_policy = all
search_policy = ff
upstreams = /local:writeback remote:dir
```

当文件被打开读取时，如果文件在 `remote:dir` 中但不在 `/local` 中，rclone 会先将整个文件复制到 `/local`，然后返回 `/local` 中文件的引用。复制操作等同于 `rclone copy`，因此在配置后会使用 `--multi-thread-streams`。任何复制操作都会以 INFO 级别记录日志。

当文件被写入时，它们将被同时写入 `remote:dir` 和 `/local`。

可以向 `upstreams` 添加任意数量的远程，但 `:writeback` 标签应该只有一个。

Rclone 不会以任何方式管理 `:writeback` 远程，除了将文件回写到它。因此，如果你需要过期旧文件或管理大小，你需要自行处理。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/union/union.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 union（Union 合并多个上游文件系统内容）的特有标准选项。

#### --union-upstreams

以空格分隔的上游列表。

可以是 'upstreama:test/dir upstreamb:'、'"upstreama:test/space:ro dir" upstreamb:' 等。

属性：

- Config:      upstreams
- Env Var:     RCLONE_UNION_UPSTREAMS
- Type:        string
- Required:    true

#### --union-action-policy

在 ACTION 类别中选择上游的策略。

属性：

- Config:      action_policy
- Env Var:     RCLONE_UNION_ACTION_POLICY
- Type:        string
- Default:     "epall"

#### --union-create-policy

在 CREATE 类别中选择上游的策略。

属性：

- Config:      create_policy
- Env Var:     RCLONE_UNION_CREATE_POLICY
- Type:        string
- Default:     "epmfs"

#### --union-search-policy

在 SEARCH 类别中选择上游的策略。

属性：

- Config:      search_policy
- Env Var:     RCLONE_UNION_SEARCH_POLICY
- Type:        string
- Default:     "ff"

#### --union-cache-time

使用量和可用空间的缓存时间（秒）。

此选项仅在使用路径保留策略时有意义。

属性：

- Config:      cache_time
- Env Var:     RCLONE_UNION_CACHE_TIME
- Type:        int
- Default:     120

### 高级选项

以下是 union（Union 合并多个上游文件系统内容）的特有高级选项。

#### --union-min-free-space

lfs/eplfs 策略的最低可用空间。

如果远程的可用空间少于此值，则不会在 lfs 或 eplfs 策略中被考虑使用。

属性：

- Config:      min_free_space
- Env Var:     RCLONE_UNION_MIN_FREE_SPACE
- Type:        SizeSuffix
- Default:     1Gi

#### --union-description

远程的描述。

属性：

- Config:      description
- Env Var:     RCLONE_UNION_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

底层远程支持的任何元数据都可以读取和写入。

详见[元数据](/docs/#metadata)文档。

<!-- autogenerated options stop -->
