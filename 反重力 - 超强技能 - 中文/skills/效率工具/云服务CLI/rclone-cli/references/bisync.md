---
title: "Bisync"
description: "rclone 双向云同步解决方案（触发词：bisync、双向同步、双向、rclone 同步、cloud sync、双向文件同步、双向拷贝、文件同步、目录同步、双向备份）"
versionIntroduced: "v1.58"
---

> **官方文档：** [https://rclone.org/bisync/](https://rclone.org/bisync/)
## Bisync

`bisync` 被视为一个**高级命令**，请谨慎使用。
请确保在开始使用之前通读并理解整个
[手册](https://rclone.org/bisync)（特别是 [Limitations](#limitations)
章节），否则可能导致数据丢失。如有疑问可在
[Rclone 论坛](https://forum.rclone.org/) 提问。

## 入门指引 {#getting-started}

- [安装 rclone](/install/) 并配置好你的 remotes。
- Bisync 会在 Linux 上的 `~/.cache/rclone/bisync`，
  Mac 上的 `/Users/yourusername/Library/Caches/rclone/bisync`，
  或 Windows 上的 `C:\Users\MyLogin\AppData\Local\rclone\bisync`
  创建其工作目录。请确保该位置可写。
- 使用 `--resync` 标志运行 bisync，并指定本地和远端同步根目录的路径。
- 后续的同步运行，请去掉 `--resync` 标志。（**重要！**）
- 建议使用 [过滤规则文件](#filtering) 排除同步中不需要的文件和目录。
- 建议启用 [--check-access](#check-access) 功能以提高安全性。
- 在 Linux 或 Mac 上，建议配置一条 [crontab 任务](#cron)。
  由于 bisync 通过锁文件维持状态，因此可以安全地在并发的 cron 任务中运行。

例如，你的第一个命令可能像这样：

```console
rclone bisync remote1:path1 remote2:path2 --create-empty-src-dirs --compare size,modtime,checksum --slow-hash-sync-only --resilient -MvP --drive-skip-gdocs --fix-case --resync --dry-run
```

如果输出看起来正常，再去掉 `--dry-run` 重新运行。
之后，再去掉 `--resync`。

下面是一个典型的运行日志（已去除时间戳以保持清晰）：

```console
rclone bisync /testdir/path1/ /testdir/path2/ --verbose
INFO  : Synching Path1 "/testdir/path1/" with Path2 "/testdir/path2/"
INFO  : Path1 checking for diffs
INFO  : - Path1    File is new                         - file11.txt
INFO  : - Path1    File is newer                       - file2.txt
INFO  : - Path1    File is newer                       - file5.txt
INFO  : - Path1    File is newer                       - file7.txt
INFO  : - Path1    File was deleted                    - file4.txt
INFO  : - Path1    File was deleted                    - file6.txt
INFO  : - Path1    File was deleted                    - file8.txt
INFO  : Path1:    7 changes:    1 new,    3 newer,    0 older,    3 deleted
INFO  : Path2 checking for diffs
INFO  : - Path2    File is new                         - file10.txt
INFO  : - Path2    File is newer                       - file1.txt
INFO  : - Path2    File is newer                       - file5.txt
INFO  : - Path2    File is newer                       - file6.txt
INFO  : - Path2    File was deleted                    - file3.txt
INFO  : - Path2    File was deleted                    - file7.txt
INFO  : - Path2    File was deleted                    - file8.txt
INFO  : Path2:    7 changes:    1 new,    3 newer,    0 older,    3 deleted
INFO  : Applying changes
INFO  : - Path1    Queue copy to Path2                 - /testdir/path2/file11.txt
INFO  : - Path1    Queue copy to Path2                 - /testdir/path2/file2.txt
INFO  : - Path2    Queue delete                        - /testdir/path2/file4.txt
NOTICE: - WARNING  New or changed in both paths        - file5.txt
NOTICE: - Path1    Renaming Path1 copy                 - /testdir/path1/file5.txt..path1
NOTICE: - Path1    Queue copy to Path2                 - /testdir/path2/file5.txt..path1
NOTICE: - Path2    Renaming Path2 copy                 - /testdir/path2/file5.txt..path2
NOTICE: - Path2    Queue copy to Path1                 - /testdir/path1/file5.txt..path2
INFO  : - Path2    Queue copy to Path1                 - /testdir/path1/file6.txt
INFO  : - Path1    Queue copy to Path2                 - /testdir/path2/file7.txt
INFO  : - Path2    Queue copy to Path1                 - /testdir/path1/file1.txt
INFO  : - Path2    Queue copy to Path1                 - /testdir/path1/file10.txt
INFO  : - Path1    Queue delete                        - /testdir/path1/file3.txt
INFO  : - Path2    Do queued copies to                 - Path1
INFO  : - Path1    Do queued copies to                 - Path2
INFO  : -          Do queued deletes on                - Path1
INFO  : -          Do queued deletes on                - Path2
INFO  : Updating listings
INFO  : Validating listings for Path1 "/testdir/path1/" vs Path2 "/testdir/path2/"
INFO  : Bisync successful
```

## 命令行语法

```console
$ rclone bisync --help
Usage:
  rclone bisync remote1:path1 remote2:path2 [flags]

Positional arguments:
  Path1, Path2  Local path, or remote storage with ':' plus optional path.
                Type 'rclone listremotes' for list of configured remotes.

Optional Flags:
      --backup-dir1 string                   --backup-dir for Path1. Must be a non-overlapping path on the same remote.
      --backup-dir2 string                   --backup-dir for Path2. Must be a non-overlapping path on the same remote.
      --check-access                         Ensure expected RCLONE_TEST files are found on both Path1 and Path2 filesystems, else abort.
      --check-filename string                Filename for --check-access (default: RCLONE_TEST)
      --check-sync string                    Controls comparison of final listings: true|false|only (default: true) (default "true")
      --compare string                       Comma-separated list of bisync-specific compare options ex. 'size,modtime,checksum' (default: 'size,modtime')
      --conflict-loser ConflictLoserAction   Action to take on the loser of a sync conflict (when there is a winner) or on both files (when there is no winner): , num, pathname, delete (default: num)
      --conflict-resolve string              Automatically resolve conflicts by preferring the version that is: none, path1, path2, newer, older, larger, smaller (default: none) (default "none")
      --conflict-suffix string               Suffix to use when renaming a --conflict-loser. Can be either one string or two comma-separated strings to assign different suffixes to Path1/Path2. (default: 'conflict')
      --create-empty-src-dirs                Sync creation and deletion of empty directories. (Not compatible with --remove-empty-dirs)
      --download-hash                        Compute hash by downloading when otherwise unavailable. (warning: may be slow and use lots of data!)
      --filters-file string                  Read filtering patterns from a file
      --force                                Bypass --max-delete safety check and run the sync. Consider using with --verbose
  -h, --help                                 help for bisync
      --ignore-listing-checksum              Do not use checksums for listings (add --ignore-checksum to additionally skip post-copy checksum checks)
      --max-lock Duration                    Consider lock files older than this to be expired (default: 0 (never expire)) (minimum: 2m) (default 0s)
      --no-cleanup                           Retain working files (useful for troubleshooting and testing).
      --no-slow-hash                         Ignore listing checksums only on backends where they are slow
      --recover                              Automatically recover from interruptions without requiring --resync.
      --remove-empty-dirs                    Remove ALL empty directories at the final cleanup step.
      --resilient                            Allow future runs to retry after certain less-serious errors, instead of requiring --resync.
  -1, --resync                               Performs the resync run. Equivalent to --resync-mode path1. Consider using --verbose or --dry-run first.
      --resync-mode string                   During resync, prefer the version that is: path1, path2, newer, older, larger, smaller (default: path1 if --resync, otherwise none for no resync.) (default "none")
      --retries int                          Retry operations this many times if they fail (requires --resilient). (default 3)
      --retries-sleep Duration               Interval between retrying operations if they fail, e.g. 500ms, 60s, 5m (0 to disable) (default 0s)
      --slow-hash-sync-only                  Ignore slow checksums for listings and deltas, but still consider them during sync calls.
      --workdir string                       Use custom working dir - useful for testing. (default: {WORKDIR})
      --max-delete PERCENT                   Safety check on maximum percentage of deleted files allowed. If exceeded, the bisync run will abort. (default: 50%)
  -n, --dry-run                              Go through the motions - No files are copied/deleted.
  -v, --verbose                              Increases logging verbosity. May be specified more than once for more details.
```

可以在
[bisync 命令行](/commands/rclone_bisync/) 上指定任意 rclone 标志，例如
`rclone bisync ./testdir/path1/ gdrive:testdir/path2/ --drive-skip-gdocs -v -v
--timeout 10s`
请注意，bisync 流程与各 rclone 标志之间的相互作用
尚未经过完整测试。

### 路径

Path1 与 Path2 参数可以是任何混合的本地目录路径（绝对或相对）、
UNC 路径（`//server/share/path`）、Windows 驱动器路径（带盘符加 `:`），
或已配置的 [remotes](/docs/#syntax-of-remote-paths) 加可选的子目录路径。
通过参数中包含 `:` 来区分云端引用（见下文 [Windows 支持](#windows)）。

Path1 与 Path2 被平等对待——对文件变更没有任何一方具有优先权
（[`--resync`](#resync) 期间除外），
且访问效率不会因 remote 被放在 Path1 还是 Path2 而有所不同。

bisync 工作目录中的列表文件（默认 `~/.cache/rclone/bisync`）
以 Path1 和 Path2 参数命名，以便对同一棵树内的不同子目录
分别设置同步，例如：
`path_to_local_tree..dropbox_subdir.lst`。

默认情况下，同步之后 Path1 和 Path2 两端文件系统上的空目录不会被删除，
除非显式指定 `--create-empty-src-dirs`。如果指定了
`--remove-empty-dirs` 标志，则作为流程的最后一步，
两个路径上的所有空目录都会被清除。

## 命令行标志

### --resync

这将有效地让 Path1 和 Path2 两个文件系统包含一个匹配的全集文件。
默认情况下，Path1 中不存在的 Path2 文件会被复制到 Path1，
然后再将 Path1 树复制到 Path2。

`--resync` 流程大致等同于以下命令
（其他选项请见 [`--resync-mode`](#resync-mode)）：

```console
rclone copy Path2 Path1 --ignore-existing [--create-empty-src-dirs]
rclone copy Path1 Path2 [--create-empty-src-dirs]
```

Path1 和 Path2 两端文件系统的基础目录必须存在，否则 bisync 会失败。
这是一个安全要求——bisync 必须能验证两个路径都有效。

当使用 `--resync` 时，默认情况下 Path2 文件系统上较新版本的文件
会被 Path1 上的版本覆盖。
（请注意，这[并非完全对称](https://github.com/rclone/rclone/issues/5681#issuecomment-938761815)，
可通过 [`--resync-mode`](#resync-mode) 标志指定更对称的选项。）
请使用 [--dry-run](/flags/#non-backend-flags) 仔细评估差异。

在 resync 运行中，两个路径中允许其中一个为空（路径树中没有文件）。
resync 运行应当使两个路径上都有文件，否则后续的普通非 resync
运行会失败。

对于非 resync 运行，若任一路径为空（树中没有文件），
则会失败并提示
`Empty current PathN listing. Cannot sync to an empty directory: X.pathN.lst`
这是一项安全检查，以避免意外的空路径导致另一端**所有**文件被删除。

请注意，除非显式指定了不同的
[`--resync-mode`](#resync-mode)，否则 `--resync` 等同于 `--resync-mode path1`。
`--resync` 和 `--resync-mode` 标志不需要同时使用——
只用其中一个即可。

**注意：** `--resync`（包括 `--resync-mode`）只应在以下三种
特殊（罕见）情况下使用：

1. 这是你的*第一次* bisync 运行（在这两个路径之间）
2. 你刚修改了 bisync 设置（例如编辑了 `--filters-file` 的内容）
3. 上一次运行出错，因此 bisync 现在需要 `--resync` 才能恢复

其余时间，你应该*省略* `--resync`。原因是 `--resync`
只会进行*复制*（而不是*同步*）两侧的内容。
因此，如果每次 bisync 都带上 `--resync`，
将永远无法删除任何文件——因为被删除的文件在另一端仍然存在，
每次运行结束都会重新出现。同样地，重命名一个文件
也会在两侧都产生一份副本（旧名称和新名称都在）。

如果发现 #3 导致的频繁中断成为问题，比起自动运行 `--resync`，
更推荐的做法是同时使用 [`--resilient`](#resilient)、
[`--recover`](#recover) 和
[`--conflict-resolve`](#conflict-resolve) 标志（必要时配合
[优雅停机](#graceful-shutdown) 模式），
从而获得一个非常稳健的"一次设置、永久运行"的 bisync 配置，
使其能从几乎任何中断中自动恢复。可以考虑加入类似下面的参数：

```text
--resilient --recover --max-lock 2m --conflict-resolve newer
```

### --resync-mode CHOICE {#resync-mode}

当在 `--resync` 期间两个路径上的文件存在差异时，
`--resync-mode` 控制哪一个版本会覆盖另一个。
支持的选项与 [`--conflict-resolve`](#conflict-resolve) 类似。
在下面所有选项中，被保留的版本称为"赢家"（winner），
被覆盖（删除）的版本称为"输家"（loser）。
选项以其所代表的"赢家"来命名：

- `path1` -（默认）——来自 Path1 的版本被无条件地视为赢家
（无论 `modtime` 和 `size` 怎样）。在 `--resync` 时，
如果某一端更可信或更新，使用此选项会非常方便。
- `path2` - 与 `path1` 相同，但将 path2 版本视为赢家。
- `newer` - 较新的文件（按 `modtime`）被视为赢家，
无论它来自哪一端。这可能导致赢家部分来自 Path1、部分来自 Path2。
（其实现类似于在两个方向上执行 `rclone copy --update`。）
- `older` - 与 `newer` 相同，但较旧的文件被视为赢家，
较新的文件被视为输家。
- `larger` - 较大的文件（按 `size`）被视为赢家
（无论 `modtime` 怎样）。这对于不支持 `modtime` 的 remote，
或者那些文件（如日志）通常只会增长而不会缩小的场景非常有用。
- `smaller` - 较小的文件（按 `size`）被视为赢家
（无论 `modtime` 怎样）。

针对以上所有选项，请注意以下几点：

- 如果底层 remote 中有一端不支持所选方法，该方法会被忽略，
并回退到 `path1` 默认值。
（例如，设置了 `--resync-mode newer`，但其中一个路径使用的 remote
不支持 `modtime`。）
- 如果因为所选方法的属性缺失或相等而无法确定赢家，
该方法会被忽略，bisync 会改为尝试根据当前生效的其他
`--compare` 方法判断文件是否不同。
（例如，设置了 `--resync-mode newer`，但 Path1 和 Path2 的 modtime
相同，bisync 会改为比较 size。）如果 bisync 最终判断文件不同，
则优先保留当前作为"源"的那一端。
（实际上，这给 Path2 略占优势，因为 2to1 的复制在 1to2 复制之前进行。）
如果文件*确实没有*差异，则不会复制任何内容（因为两侧都已经正确）。
- 这些选项只适用于两侧都存在（且名称、相对路径相同）的文件。
仅在某一端存在的文件，在 `--resync` 期间*总是*被复制到另一端
（这是 resync 与非 resync 运行的主要区别之一）。
- `--conflict-resolve`、`--conflict-loser` 和 `--conflict-suffix`
在 `--resync` 期间不生效，与这些标志不同，
`--resync` 期间不会进行任何重命名。当文件在 `--resync` 期间两侧不同时，
永远是一个版本覆盖另一个版本（与 `rclone copy` 行为类似）。
（可考虑使用 [`--backup-dir`](#backup-dir1-and-backup-dir2)
来保留输家版本的备份。）
- 与 `--conflict-resolve` 不同，`--resync-mode none` 不是一个有效选项
（或者更准确地说，除非同时指定了 `--resync`，否则它会被解释为"不进行 resync"，
而如果同时指定了 `--resync`，它会被忽略。）
- 赢家与输家只按单个文件粒度决定（目前还没有选项可以一次性选择
整个目录作为赢家，虽然 `path1` 和 `path2` 选项通常会产生类似效果。）
- 为保持向后兼容，除非显式指定了不同的 `--resync-mode`，
否则 `--resync` 标志等同于 `--resync-mode path1`。
类似地，所有 `--resync-mode` 选项（`none` 除外）
也等同于 `--resync`，因此不需要同时使用 `--resync` 和
`--resync-mode` 标志——只用其中一个即可。

### --check-access

访问检查文件是一项防止数据丢失的额外安全措施。
bisync 会确保在 Path1 和 Path2 文件系统的相同位置能找到匹配的
`RCLONE_TEST` 文件。
`RCLONE_TEST` 文件不会自动生成。
要让 `--check-access` 成功，你必须先完成以下操作之一：
**A)** 在两个系统中各放置一个或多个 `RCLONE_TEST` 文件，或
**B)** 将 `--check-filename` 设置为同步文件集中已在各位置使用的某个文件名。
关于 **A)** 的推荐方法包括：

- `rclone touch Path1/RCLONE_TEST`（新建一个文件）
- `rclone copyto Path1/RCLONE_TEST Path2/RCLONE_TEST`（复制一个已存在的文件）
- `rclone copy Path1/RCLONE_TEST Path2/RCLONE_TEST  --include "RCLONE_TEST"`
（一次性递归复制多个文件）
- 手动创建文件（在 rclone 之外）
- 先*不带* `--check-access` 运行一次 `bisync`，
使两个文件系统上都设置好匹配的文件，
此方法也可以，但不推荐，因为有用户出错的风险
（你临时禁用了这个安全特性）。

请注意 `--check-access` 在 `--resync` 期间仍会强制检查，
因此 `bisync --resync --check-access` 不能作为初始设置检查文件的方法
（这是为了确保 bisync 不会
[无意间规避自己的安全开关](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=3.%20%2D%2Dcheck%2Daccess%20doesn%27t%20always%20fail%20when%20it%20should).)）。

`RCLONE_TEST` 文件的时间戳和内容并不重要，
重要的是文件名和位置。如果你的同步树中有符号链接，
建议将 `RCLONE_TEST` 文件放在链接目标所在的目录树下，
以防止当链接目标不可访问时 bisync 错误地认为有一大堆文件被删除。
另请参见 [--check-filename](--check-filename) 标志。

### --check-filename

用于访问健康验证的文件名。
`--check-filename` 的默认值是 `RCLONE_TEST`。
必须在源和目标文件集之间同步一个或多个具有该文件名的文件，
`--check-access` 才能成功。
更多细节请参见 [--check-access](#check-access)。

### --compare

从 `v1.66` 开始，bisync 完全支持基于 size、modtime、checksum
任意组合的比较（取消了之前对没有 modtime 支持的后端的限制）。

默认情况下（不指定 `--compare` 标志），
bisync 继承与 `sync` 相同的比较选项
（即默认为 `size` 和 `modtime`，除非使用 [`--checksum`](/docs/#c-checksum)
或 [`--size-only`](/docs/#size-only) 等标志进行了修改）。

如果设置了 `--compare` 标志，它会覆盖这些默认值。
当你希望按 `sync` 目前尚不支持的组合进行比较时，这非常有用，
例如同时比较 `size` **与** `modtime` **与** `checksum` 三者
（或仅 `modtime` **与** `checksum`）。

`--compare` 接受逗号分隔的列表，目前支持的值有
`size`、`modtime`、`checksum`。例如，如果想比较 size 和 checksum
但不比较 modtime，可以这样写：

```text
--compare size,checksum
```

或者想同时比较这三项：

```text
--compare size,modtime,checksum
```

`--compare` 会覆盖任何与之冲突的标志。例如，
如果设置了冲突的 `--compare checksum --size-only`，
`--size-only` 会被忽略，bisync 将比较 checksum 而不是 size。
为避免混淆，建议要么使用 `--compare`，要么使用普通的 `sync` 标志，
不要同时使用两者。

如果 `--compare` 包含 `checksum`，但两个 remote 都支持 checksum
但彼此之间没有共同的哈希类型，则 checksum 只用于
*同一端*内部的比较（以确定自上次同步以来发生了什么变化），
不用于跨端的比较。如果一端支持 checksum 而另一端不支持，
则 checksum 只会用于支持 checksum 的那一端。

当使用 `checksum` 和/或 `size`（但不含 `modtime`）进行比较时，
bisync 无法判断一个文件是 `newer` 还是 `older`——
只能判断它是 `changed` 还是 `unchanged`。
（如果两侧都是 `changed`，bisync 仍会进行标准相等性检查，
以避免在非必要时不必要地声明同步冲突。）

建议在修改 `--compare` 设置时执行一次 `--resync`，
否则你之前的列表文件可能不包含你希望比较的属性
（例如，如果之前没有比较 checksum，那么列表中也不会存储 checksum）。

### --ignore-listing-checksum

当设置了 `--checksum` 或 `--compare checksum` 时，
bisync 在为两个路径创建列表时会获取（或生成）
（对于支持的后端）checksum，并将其存放在列表文件中。
`--ignore-listing-checksum` 会禁用此行为，
这可以显著加快速度，特别是在那些必须实时计算哈希
而非读取已有哈希的后端（如 [local](/local/)）上。请注意以下几点：

- 从 `v1.66` 开始，当既未使用 `--checksum` 也未使用 `--compare checksum` 时，
会自动启用 `--ignore-listing-checksum`（因为这些 checksum 无处可用）。
- `--ignore-listing-checksum` 与
[`--ignore-checksum`](/docs/#ignore-checksum) **并不相同**，
你可以根据需要单独使用其中一个、两个都使用或都不使用。简而言之：
`--ignore-listing-checksum` 控制扫描差异时是否考虑 checksum，
而 `--ignore-checksum` 控制后续 copy/sync 操作中是否考虑 checksum
（前提是确实存在差异）。
- 除非显式传入 `--ignore-listing-checksum`，否则 bisync 当前
会为某一个路径计算哈希，*即使该路径与另一路径没有共同的哈希类型*
（例如 [crypt](/crypt/#modification-times-and-hashes) remote）。
这仍然是有益的，因为这些哈希仍可用于检测同一端内部的变化
（当设置了 `--checksum` 或 `--compare checksum` 时），
即使无法用于与对端的比较。
- 如果你希望*仅*在计算 checksum 较慢的 remote 上忽略列表 checksum，
可以考虑使用
[`--no-slow-hash`](#no-slow-hash)（或
[`--slow-hash-sync-only`](#slow-hash-sync-only)），
而不是 `--ignore-listing-checksum`。
- 如果同时使用 `--ignore-listing-checksum` 和 `--compare checksum`
（或 `--checksum`），bisync 的差异计算会忽略 checksum，
但后续的 sync 操作仍会考虑它们（如果差异是基于 modtime 和/或 size
检测出来的）。

### --no-slow-hash

在某些 remote（特别是 `local`）上，checksum 会显著拖慢 bisync 运行，
因为哈希无法被存储，必须在请求时实时计算。
在另一些 remote（如 `drive`）上，checksum 几乎不增加任何时间。
`--no-slow-hash` 标志会在计算 checksum 较慢的 remote 上自动跳过，
同时在其它 remote 上仍进行比较（前提是
[`--compare`](#compare) 包含 `checksum`）。
当你的两个 bisync 路径中有一个较慢、但你仍希望在另一端
对 checksum 进行更稳健的同步时，这个选项非常有用。

### --slow-hash-sync-only

与 [`--no-slow-hash`](#no-slow-hash) 类似，区别在于
`slow-hash-sync-only` 在 sync 调用中仍会考虑慢速哈希。
它们仍然不参与差异判定，也不会写入列表。
在 `--resync` 期间也会被跳过。
此标志的主要使用场景是：文件数量很大，
但每次运行时只有相对较少的文件发生变化——
你不想每次都对整棵树做 checksum 检查（这会花费太长时间），
但仍希望对那小部分检测到 `modtime` 或 `size` 变化的文件
考虑 checksum。请记住，这种速度提升伴随着安全性上的权衡：
如果一个文件的内容发生了变化，但 `modtime` 或 `size` 没有变化，
bisync 不会检测到这种变化，文件也不会被同步。

仅当两个 remote 共享同一哈希类型时，
`--slow-hash-sync-only` 才有意义（如果不共享，
bisync 会自动回退到 `--no-slow-hash`）。
在没有 `--compare checksum`（或 `--checksum`）的情况下，
`--no-slow-hash` 和 `--slow-hash-sync-only` 均无效。

### --download-hash

如果设置了 `--download-hash`，当 checksum 不可用时
（例如 remote 本身不支持），bisync 会尽力通过下载文件
并实时计算来获取 MD5 checksum。
请注意，由于 rclone 必须下载整个文件，这可能会显著拖慢你的
bisync 运行，并且可能消耗大量数据，因此对于总文件量很大的
bisync 路径来说，可能并不实用。但是，对于需要以最高准确性
同步少量重要文件的场景（例如 `crypt` remote 上的源代码仓库），
这会是一个不错的选择。
相较于 [`cryptcheck`](/commands/rclone_cryptcheck/) 等方法，
它有一个额外优势：不需要原始文件即可进行比较
（例如，`--download-hash` 可用于同步两个密码不同的 crypt remote）。

当设置了 `--download-hash` 时，bisync 仍会优先寻找更高效的 checksum，
只有在找不到时才会回退到下载方式。
它的优先级高于 `--no-slow-hash` 这类相互冲突的标志。
`--download-hash` 不适用于 [Google Docs](#gdocs) 和其他大小未知的文件，
因为这些文件的 checksum 在每次运行间都可能不同
（因为生成的导出文件内部存在细微差异）。
因此，bisync 会自动对 size 小于 0 的文件跳过 `--download-hash`。

另请参阅：[`Hasher`](https://rclone.org/hasher/) backend、
[`cryptcheck`](/commands/rclone_cryptcheck/) 命令、
[`rclone check --download`](/commands/rclone_check/) 选项、
[`md5sum`](/commands/rclone_md5sum/) 命令

### --max-delete

作为一项安全检查，如果在 Path1 或 Path2 任意一端
被删除的文件比例超过了 `--max-delete` 百分比，
则 bisync 会在不进行任何更改的情况下中止，并给出警告信息。
`--max-delete` 的默认值为 `50%`。
触发该限制的一种方式是将包含超过一半文件的目录重命名。
对 bisync 而言，这看上去就像一大批文件被删除、一大批新文件出现。
此安全检查旨在阻止以下情况：因临时网络访问问题，
或用户不小心删除了某一端的文件，
导致 bisync 删除两个文件系统上的所有文件。
若要强制同步，可以设置一个不同的删除百分比限制，
例如 `--max-delete 75`（允许最多 75% 的删除），
或使用 `--force` 绕过该检查。

另请参见 [all files changed](#all-files-changed) 检查。

### --filters-file {#filters-file}

通过使用 rclone 的过滤功能，你可以将某些文件类型或目录子树
排除在同步之外。
参见 [bisync 过滤](#filtering) 章节以及通用的
[--filter-from](/filtering/#filter-from-read-filtering-patterns-from-a-file)
文档。
一个 [过滤文件示例](#example-filters-file) 包含
针对 Dropbox 同步中不允许的文件的过滤规则。

如果你修改了过滤文件，那么 bisync 需要配合 `--resync` 运行。
这是一个安全特性，用以防止 Path1 和/或 Path2 端的已有文件
看起来"消失"了（因为它们在新列表中被排除了），
导致 bisync 误以为它们已被删除（与上一次运行的列表相比），
然后 bisync 真的会去删除它们。

为阻止这种情况发生，bisync 会计算过滤文件的 MD5 哈希，
并将该哈希存放在过滤文件同目录的 `.md5` 文件中。
在下一次设置了 `--filters-file` 的运行中，bisync 会重新计算
当前过滤文件的 MD5 哈希，并与 `.md5` 文件中保存的哈希进行比较。
如果两者不匹配，运行会以关键错误中止，从而强制你执行
`--resync`，大概率避免一场灾难。

### --conflict-resolve CHOICE {#conflict-resolve}

在 bisync 中，"冲突"是指在（相对于上一次运行）*两侧*都是*新文件*
或*已更改*，且*当前内容并不相同*的文件。
`--conflict-resolve` 控制 bisync 如何处理这种情况。
当前支持的选项包括：

- `none` -（默认）——不尝试选出赢家，而是根据
[`--conflict-loser`](#conflict-loser) 和
[`--conflict-suffix`](#conflict-suffix) 设置同时保留并重命名两个文件。
例如，使用默认设置时，Path1 上的 `file.txt` 会被重命名为
`file.txt.conflict1`，Path2 上的 `file.txt` 会被重命名为
`file.txt.conflict2`。两者都会在本次运行中被复制到对端，
因此最终两侧都会拥有这两个文件的副本。
（因为 `none` 是默认值，所以不必显式指定
`--conflict-resolve none`——直接省略该标志即可。）
- `newer` - 较新的文件（按 `modtime`）被视为赢家，
会被原样复制；较旧的文件（即"输家"）按照
`--conflict-loser` 和 `--conflict-suffix` 的设置处理
（重命名或删除）。例如，如果 Path1 上的 `file.txt` 比
Path2 上的 `file.txt` 更新，那么在两侧（其它为默认设置时）
最终结果将是：`file.txt`（来自 Path1 的赢家）和
`file.txt.conflict1`（来自 Path2 的输家）。
- `older` - 与 `newer` 相同，但较旧的文件被视为赢家，
较新的文件被视为输家。
- `larger` - 较大的文件（按 `size`）被视为赢家
（无论 `modtime` 怎样）。
- `smaller` - 较小的文件（按 `size`）被视为赢家
（无论 `modtime` 怎样）。
- `path1` - 来自 Path1 的版本被无条件视为赢家
（无论 `modtime` 和 `size` 怎样）。在某一端通常更可信
或更新时，这会非常方便。
- `path2` - 与 `path1` 相同，但将 path2 版本视为赢家。

针对以上所有选项，请注意以下几点：

- 如果底层 remote 中有一端不支持所选方法，该方法会被忽略，
并回退到 `none`。
（例如，设置了 `--conflict-resolve newer`，但其中一个路径使用的
remote 不支持 `modtime`。）
- 如果因为所选方法的属性缺失或相等而无法确定赢家，
该方法会被忽略，并回退到 `none`。
（例如，设置了 `--conflict-resolve newer`，但 Path1 和 Path2 的
modtime 相同，即便 size 可能不同。）
- 如果一个文件当前在两侧内容完全相同，即使自上一次同步以来
在两侧都是新文件或被修改过，也不会被视为"冲突"。
（例如，你在某一端做了一些修改，然后通过其他方式把它同步到了对端。）
因此，在这种情况下所有冲突解决标志都不会生效。
- 冲突解决标志在 `--resync` 期间不生效，因为没有所谓的
"上一次运行"可参照（但请参见 [`--resync-mode`](#resync-mode) 中的
类似选项。）

### --conflict-loser CHOICE {#conflict-loser}

`--conflict-loser` 决定同步冲突中"输家"会被如何处理
（当 [`--conflict-resolve`](#conflict-resolve) 能决定赢家时），
或者当无法决定赢家时两个文件会如何处理。
当前支持的选项包括：

- `num` -（默认）——按时间顺序自动为冲突编号，
在 `--conflict-suffix` 之后自动追加下一个可用的数字。
例如，使用默认设置时，`file.txt` 的第一个冲突会被重命名为
`file.txt.conflict1`。如果 `file.txt.conflict1` 已经存在，
则使用 `file.txt.conflict2`（依此类推，最多
9223372036854775807 个冲突）。
- `pathname` - 根据冲突来源对冲突文件进行重命名，
这是 `v1.66` 之前的默认行为。例如，使用
`--conflict-suffix path` 时，Path1 的 `file.txt` 会被重命名为
`file.txt.path1`，Path2 的 `file.txt` 会被重命名为
`file.txt.path2`。如果提供了两个不同的后缀
（例如 `--conflict-suffix cloud,local`），
则省略末尾的数字。请务必注意，在 `pathname` 模式下，
除了 `2` 之外不会再自动增加编号，因此如果 `file.txt.path2`
已经存在，它将被覆盖。在 `--conflict-suffix` 中使用
动态日期变量（见下文）是避免这种情况的一种方式。
还要注意，如果原始冲突没有手动解决，可能出现"冲突中的冲突"——
例如，假设出于某种原因你同时编辑了两端的 `file.txt.path1`，
且两次编辑内容不同，结果将得到 `file.txt.path1.path1` 和
`file.txt.path1.path2`（以及 `file.txt.path2`）。
- `delete` - 仅保留赢家，并删除输家，而不是将其重命名。
如果无法确定赢家（详见 `--conflict-resolve` 中关于这种情况的说明），
`delete` 会被忽略，转而使用默认的 `num`
（即两个版本都被保留并重命名，且都不会被删除）。
`delete` 本身就是最具破坏性的选项，请仅在确实需要时谨慎使用。

针对以上所有选项，请注意：如果无法确定赢家
（详见 `--conflict-resolve` 中关于这种情况的说明），
或未使用 `--conflict-resolve`，那么*两个*文件都会被重命名。

### --conflict-suffix STRING[,STRING] {#conflict-suffix}

`--conflict-suffix` 控制 bisync 重命名
[`--conflict-loser`](#conflict-loser) 时追加的后缀
（默认：`conflict`）。
`--conflict-suffix` 接受一个字符串或两个逗号分隔的字符串，
以便为 Path1 和 Path2 分配不同的后缀。这在之后识别
冲突来源时可能会有所帮助。
（例如，`--conflict-suffix dropboxconflict,laptopconflict`）

使用 `--conflict-loser num` 时，总会在后缀后追加一个数字。
使用 `--conflict-loser pathname` 时，仅当指定了一个后缀
（或指定了两个相同的后缀）时才会追加数字。
也就是说，使用 `--conflict-loser pathname` 时，
下面所有写法都将产生完全相同的结果：

```text
--conflict-suffix path
--conflict-suffix path,path
--conflict-suffix path1,path2
```

后缀可以短到 1 个字符。默认情况下，后缀会被追加到
任何其他扩展名之后（例如 `file.jpg.conflict1`），
但可以通过 [`--suffix-keep-extension`](/docs/#suffix-keep-extension)
标志修改这一行为（即改为 `file.conflict1.jpg`）。

`--conflict-suffix` 支持若干 *动态日期变量*，当用大括号括起来作为
glob 时会展开。这在追踪每个冲突被 bisync 处理的日期和/或时间
时非常有用。例如：

```text
--conflict-suffix {DateOnly}-conflict
// result: myfile.txt.2006-01-02-conflict1
```

[这里（go Time.Layout 常量）](https://pkg.go.dev/time#pkg-constants)
和 [这里（go Time.Format 示例）](https://pkg.go.dev/time#example-Time.Format)
描述的所有格式都受支持，但请务必确保你选择的格式不使用
在 remote 上非法的字符（例如 macOS 不允许文件名中包含冒号，
斜杠也应尽量避免，因为它们通常会被解释为目录分隔符）。
为了解决这个特定问题，额外支持一个 `{MacFriendlyTime}`（或简写 `{mac}`），
结果形如 `2006-01-02 0304PM`。

请注意，`--conflict-suffix` 与 rclone 的主
[`--suffix`](/docs/#suffix-string) 标志完全独立。这是有意为之的，
因为如果同时使用 [`--backup-dir`](#backup-dir1-and-backup-dir2)，
用户可能希望同时使用这两个标志。

最后，请注意，`v1.66` 之前的 bisync 默认使用
`..path1` 和 `..path2`（两个点，且为 `path` 而非 `conflict`）来重命名冲突。
现在 bisync 默认改为单个点，但如果在指定的后缀字符串中包含额外的点，
也可以添加更多点。例如，要获得与之前默认行为等效的结果，可使用：

```text
[--conflict-resolve none] --conflict-loser pathname --conflict-suffix .path
```

### --check-sync

默认启用，check-sync 函数会检查 Path1 和 Path2 历史列表中
是否都存在相同的文件。默认情况下，这个 *check-sync* 完整性检查
会在同步运行结束时执行。
两个路径之间任何未被捕获的失败 copy/delete 可能会导致两个列表之间
出现差异，以及两个路径之间未被追踪的文件内容差异。
通过 resync 运行可以纠正这种错误。

请注意，默认启用的完整性检查会在本地同时加载最终的
Path1 和 Path2 列表，因此会增加同步的运行时间。
使用 `--check-sync=false` 将会禁用它，对于文件数量极多的场景，
可能会显著缩短同步运行时间。

可以使用 `--check-sync=only` 手动运行该检查。
它仅执行完整性检查，然后直接终止，不会真正进行同步。

请注意，目前 `--check-sync` **只检查列表快照，而不会检查
remote 上的实际文件。** 同样请注意，最新一次 bisync 运行
期间或之后发生的任何变更，列表快照都不会反映这些变更，
它们会在下一次运行时被发现。
因此，虽然列表在 bisync 运行结束时应当始终彼此一致，
但与底层 remote 不一致是 *正常* 现象——如果运行期间或之后发生了变更，
remote 之间也可能彼此不一致。这些差异会在下一次运行时被发现并同步。

如果要对 remote 的当前状态进行更可靠的完整性检查
（而不仅仅是它们的列表快照），可考虑使用
[`check`](commands/rclone_check/)（如果至少有一个路径是
`crypt` remote，则使用 [`cryptcheck`](/commands/rclone_cryptcheck/)），
而不是 `--check-sync`，但请注意，如果文件在上次 bisync 运行期间
或之后发生过变化，那么出现差异是预期的。

例如，一个可行的操作序列可能如下：

1. 按计划正常运行的 bisync：

    ```console
    rclone bisync Path1 Path2 -MPc --check-access --max-delete 10 --filters-file /path/to/filters.txt -v --no-cleanup --ignore-listing-checksum --disable ListR --checkers=16 --drive-pacer-min-sleep=10ms --create-empty-src-dirs --resilient
    ```

2. 定期独立完整性检查（可以安排在每晚或每周）：

    ```console
    rclone check -MvPc Path1 Path2 --filter-from /path/to/filters.txt
    ```

3. 如果发现差异，你有几种选择来纠正。
如果你更信任某一端，并希望另一端与之对齐，可以运行：

    ```console
    rclone sync Path1 Path2 --filter-from /path/to/filters.txt --create-empty-src-dirs -MPc -v
    ```

（或者交换 Path1 和 Path2，让 Path2 作为单一来源）

或者，如果两端都不完全是最新的，可以运行 `--resync` 让它们重新对齐
（但请注意，这可能会导致已删除的文件重新出现）。

*还要注意 `rclone check` 目前不包括空目录，
因此如果想知道是否有空目录处于不同步状态，
可以考虑在上面的 `rclone sync` 命令中加上 `--dry-run` 来检查。*

另请参见：[并发修改](#concurrent-modifications)、[`--resilient`](#resilient)

### --resilient

默认情况下，大多数错误或中断都会导致 bisync 中止，并要求通过
[`--resync`](#resync) 来恢复。这是一项安全特性，
用以防止 bisync 在用户检查问题之前再次运行。
然而在某些情况下，bisync 可能会过度严格地执行锁止，
而实际上并没有这个必要，例如对那些可能在下次运行时
自行解决的、不太严重的错误。
当指定 `--resilient` 时，bisync 会尽最大努力进行恢复和自我纠正，
仅在确实需要人工介入的最后关头才要求使用 `--resync`。
该选项的预期用途是将 bisync 作为后台进程运行
（例如通过计划任务 [cron](#cron)）。

使用 `--resilient` 模式时，bisync 仍会报告错误并中止，
但它不会锁止后续运行——允许在下一个正常调度的时刻重试，
而不必先执行 `--resync`。这类可重试错误的例子包括
访问检查失败、列表文件丢失和过滤规则变更。
这些安全特性仍会阻止*当前*运行继续——区别在于，
如果到*下一次*运行时情况已经改善，那么下一次运行将被允许继续。
某些更严重的错误即使在 `--resilient` 模式下仍会强制 `--resync`
锁止，以防止数据丢失。

`--resilient` 的行为在未来版本中可能会发生变化。
（另请参见：[`--recover`](#recover)、[`--max-lock`](#max-lock)、
[优雅停机](#graceful-shutdown)）

### --recover

如果设置了 `--recover`，在突然中断或其他非优雅停机的情况下，
bisync 将尝试在下次运行时自动恢复，而不需要 `--resync`。
bisync 能稳健地实现这一点，方法是始终保留一份"备份"列表，
表示两次路径在上一次成功同步后的状态。
然后 bisync 可以将当前状态与这份快照进行比较，
确定哪些变更需要重试。在该快照之后（即在被中断的运行中）
已经同步完成的变更，对 bisync 而言会表现为"两侧都是新文件或已变更"，
但在大多数情况下这并不是问题，因为 bisync 只是执行常规的
"相等性检查"，并发现这些文件无需任何操作——因为它们在两侧已经相同。

在少数情况下：一个文件在被中止的运行中成功同步后，
在下一次运行之前又发生了*再次*变更，bisync 会将其视为
同步冲突并相应处理。（从 bisync 的角度看，
该文件自上次可信同步以来在两侧都发生了变化，
且两侧的文件当前并不相同。）因此，`--recover` 略微增加了
发生冲突的可能性——虽然在实践中这种情况非常罕见，
因为触发它的条件相当具体。可以通过使用 bisync 的
["优雅停机"](#graceful-shutdown) 模式（通过发送 `SIGINT`
或 `Ctrl+C` 触发）来降低这种风险，前提是你有选择权，
而不是强制突然终止。

`--recover` 和 `--resilient` 类似但并不相同——主要区别在于，
`--resilient` 关注的是*重试*，而 `--recover` 关注的是*恢复*。
大多数用户可能希望两者都使用。
`--resilient` 允许在 bisync 因安全特性（如 `--check-access`
失败或检测到过滤规则变更）而主动中止时进行重试。
而 `--resilient` 不涵盖外部中断，例如用户在同步过程中关机——
那正是 `--recover` 的用武之地。

### --max-lock

Bisync 使用 [锁文件](#lock-file) 作为安全特性，
以防止在自身运行期间被其他 bisync 运行干扰。
Bisync 通常会在运行结束时删除这些锁文件，
但如果 bisync 被突然中断，这些文件会被留下。
默认情况下，它们会锁止所有后续运行，直到用户有机会手动检查
并删除锁文件。作为替代方案，可以使用 `--max-lock` 让锁文件
在一段时间后自动过期，这样后续运行就不会被永久锁止，
从而可以实现自动恢复。`--max-lock` 可以是 `2m` 或更大的任意时长
（或设为 `0` 禁用）。如果设置了该选项，
超过该时间的锁文件将被视为"已过期"，后续运行将允许忽略它们
并继续进行。（请注意，`--max-lock` 的持续时间必须由留下锁文件
的进程设置——而不是由之后读取它的进程设置。）

如果设置了 `--max-lock`，bisync 还会在一次运行的整个过程中，
每 `--max-lock minus one minute` 自动"续期"这些锁文件，
以提供额外的安全性。（例如，使用 `--max-lock 5m` 时，
bisync 会每 4 分钟将锁文件续期一次（再续 5 分钟），
直到该次运行结束。）换言之，进程仍在运行时，
锁文件不应会过期——因此你可以比较有把握地认为
任何"已过期"的锁文件都是由被中断的运行留下的，
而不是某个仍在运行、只是比较慢的进程留下的。

如果锁文件存在但内容不可读（例如因为写入未完成或磁盘错误），
当 `--max-lock` 大于 `0` 时，它会被视为已过期。
如果 `--max-lock` 为 `0` 或未设置，不可读的锁文件会引发错误
并阻塞后续运行，直到被手动删除。

如果 `--max-lock` 为 `0` 或未设置，则默认行为是
锁文件永远不会过期，并将持续（针对这两个 bisync 路径的）
后续运行无限期地阻塞。

为获得对中断的最大韧性，建议将 `--max-lock 2m` 与
[`--resilient`](#resilient)、[`--recover`](#recover)
以及一个相对频繁的 [cron 计划](#cron) 搭配使用。
这样就能形成一个非常稳健的"一次设置、永久运行"的 bisync 配置，
使其能在几乎任何中断情况下自动恢复，而无需用户介入并执行
`--resync`。（另请参见：[优雅停机](#graceful-shutdown) 模式）

### --backup-dir1 and --backup-dir2

从 `v1.66` 开始，bisync 支持
[`--backup-dir`](/docs/#backup-dir-string)。
因为 `--backup-dir` 必须是同一 remote 上不重叠的路径，
bisync 引入了新的 `--backup-dir1` 和 `--backup-dir2` 标志，
以便为 `Path1` 和 `Path2` 分别指定 backup-dir
（否则在不同 remote 之间做 bisync 时将无法使用 `--backup-dir`）。
`--backup-dir1` 和 `--backup-dir2` 彼此之间可以使用不同的 remote，
但 `--backup-dir1` 必须与 `Path1` 使用同一个 remote，
`--backup-dir2` 必须与 `Path2` 使用同一个 remote。
每个 backup 目录都不能与对应的 bisync Path 重叠，
除非通过过滤规则排除。

标准的 `--backup-dir` 也能正常工作，前提是两个路径使用同一 remote
（但请注意，来自两个路径的已删除文件会混合存放在同一目录中）。
如果设置了 `--backup-dir1` 或 `--backup-dir2`，
它们将覆盖 `--backup-dir`。

示例：

```console
rclone bisync /Users/someuser/some/local/path/Bisync gdrive:Bisync --backup-dir1 /Users/someuser/some/local/path/BackupDir --backup-dir2 gdrive:BackupDir --suffix -2023-08-26 --suffix-keep-extension --check-access --max-delete 10 --filters-file /Users/someuser/some/local/path/bisync_filters.txt --no-cleanup --ignore-listing-checksum --checkers=16 --drive-pacer-min-sleep=10ms --create-empty-src-dirs --resilient -MvP --drive-skip-gdocs --fix-case
```

在本例中，如果用户在
`/Users/someuser/some/local/path/Bisync` 中删除了一个文件，
bisync 会将相应的文件从 `gdrive:Bisync` 移动到
`gdrive:BackupDir` 来把这次删除传播到对端。
如果用户在 `gdrive:Bisync` 上删除了一个文件，
bisync 会把该文件从 `/Users/someuser/some/local/path/Bisync`
移动到 `/Users/someuser/some/local/path/BackupDir`。

发生 [因同步冲突而产生的重命名](#conflict-loser) 时，
该重命名不会被视为删除，除非已经存在同名冲突文件
并将被覆盖。

另请参见：[`--suffix`](/docs/#suffix-string)、
[`--suffix-keep-extension`](/docs/#suffix-keep-extension)

## 运行机制

### 运行时流程细节

bisync 会在每次运行时保留上一次运行中 Path1 和 Path2
文件系统的列表。
在后续每次运行中，它将：

- 列出 `path1` 和 `path2` 上的文件，并检查每端的变化。
  变化包括 `New`、`Newer`、`Older` 和 `Deleted` 文件。
- 将 `path1` 上的变更传播到 `path2`，反之亦然。

### 安全措施

- 锁文件可防止当一次同步耗时较长时出现多个并发运行。
  如果 bisync 由 cron 调度运行，这会特别有用。
- 通过创建 `.conflict1`、`.conflict2` 等文件副本来
  非破坏性地处理变更冲突，具体规则取决于
  [`--conflict-resolve`](#conflict-resolve)、
  [`--conflict-loser`](#conflict-loser) 和
  [`--conflict-suffix`](#conflict-suffix) 设置。
- 使用 `RCLONE_TEST` 文件进行文件系统访问健康检查
  （参见 `--check-access` 标志）。
- 在过度删除时中止——防止将失败的列表错误地解读为
  所有文件都已删除。
  参见 `--max-delete` 和 `--force` 标志。
- 如果出现严重问题，bisync 会进入安全状态以阻止后续运行
  造成进一步破坏。（参见 [错误处理](#error-handling)）

### 常规同步检查

 Type         | Description                                   | Result                   | Implementation
--------------|-----------------------------------------------|--------------------------|-----------------------------
Path2 new     | File is new on Path2, does not exist on Path1 | Path2 version survives   | `rclone copy` Path2 to Path1
Path2 newer   | File is newer on Path2, unchanged on Path1    | Path2 version survives   | `rclone copy` Path2 to Path1
Path2 deleted | File is deleted on Path2, unchanged on Path1  | File is deleted          | `rclone delete` Path1
Path1 new     | File is new on Path1, does not exist on Path2 | Path1 version survives   | `rclone copy` Path1 to Path2
Path1 newer   | File is newer on Path1, unchanged on Path2    | Path1 version survives   | `rclone copy` Path1 to Path2
Path1 older   | File is older on Path1, unchanged on Path2    | *Path1 version survives* | `rclone copy` Path1 to Path2
Path2 older   | File is older on Path2, unchanged on Path1    | *Path2 version survives* | `rclone copy` Path2 to Path1
Path1 deleted | File no longer exists on Path1                | File is deleted          | `rclone delete` Path2

### 非常规同步检查

 Type                           | Description                           | Result                             | Implementation
--------------------------------|---------------------------------------|------------------------------------|-----------------------
Path1 new/changed AND Path2 new/changed AND Path1 == Path2       | File is new/changed on Path1 AND new/changed on Path2 AND Path1 version is currently identical to Path2 | No change | None
Path1 new AND Path2 new         | File is new on Path1 AND new on Path2 (and Path1 version is NOT identical to Path2) | Conflicts handled according to [`--conflict-resolve`](#conflict-resolve) & [`--conflict-loser`](#conflict-loser) settings | default: `rclone copy` renamed `Path2.conflict2` file to Path1, `rclone copy` renamed `Path1.conflict1` file to Path2
Path2 newer AND Path1 changed   | File is newer on Path2 AND also changed (newer/older/size) on Path1 (and Path1 version is NOT identical to Path2) | Conflicts handled according to [`--conflict-resolve`](#conflict-resolve) & [`--conflict-loser`](#conflict-loser) settings | default: `rclone copy` renamed `Path2.conflict2` file to Path1, `rclone copy` renamed `Path1.conflict1` file to Path2
Path2 newer AND Path1 deleted   | File is newer on Path2 AND also deleted on Path1 | Path2 version survives  | `rclone copy` Path2 to Path1
Path2 deleted AND Path1 changed | File is deleted on Path2 AND changed (newer/older/size) on Path1 | Path1 version survives |`rclone copy` Path1 to Path2
Path1 deleted AND Path2 changed | File is deleted on Path1 AND changed (newer/older/size) on Path2 | Path2 version survives  | `rclone copy` Path2 to Path1

从 `rclone v1.64` 开始，bisync 在检测 *假阳性* 同步冲突方面
有了明显改进——在之前的版本中，这些假阳性会导致不必要的重命名
和重复文件。现在，当 bisync 处理一个它想要重命名的文件时
（因为它在两侧都是新文件或已变更），它会先检查 Path1 和 Path2 的版本
当前是否 *完全相同*（使用与
[`check`](commands/rclone_check/) 相同的底层函数）。
如果 bisync 判断两个文件相同，它会跳过该文件并继续处理。
否则，它会像之前一样创建重命名后的副本。
这种行为还[改进了重命名目录的体验](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=Renamed%20directories)，
只要两侧都做了相同的修改，就不再需要 `--resync`。

### 所有文件都变化检查 {#all-files-changed}

如果某个文件系统上*所有*原先存在的文件都已变化
（例如，由于更改了系统时区导致时间戳发生变化），
bisync 将在不做任何更改的情况下中止。
任何新文件都不会纳入此检查。你可以使用 `--force` 强制同步
（哪一端拥有变化时间戳的文件，哪一端就胜出）。
也可以使用 `--resync`（Path1 的版本将被推送到 Path2）。
请谨慎考虑情况，并可能先使用 `--dry-run` 看看会发生什么，
再决定提交这些更改。

### 修改时间

默认情况下，bisync 通过修改时间和大小来比较文件。
如果你或你的应用在*不*改变文件修改时间和大小的前提下
修改了文件内容，那么 bisync 将*不会*察觉到这次变化，
也就不会将其复制到另一端。
作为替代方案，可考虑使用 checksum 比较（前提是你的 remote 支持）。
详情请参见 [`--compare`](#compare)。

### 错误处理 {#error-handling}

某些 bisync 关键错误（例如文件 copy/move 失败）会导致
后续 bisync 运行被锁止。之所以会锁止，是因为 Path1 和 Path2 文件系统
的同步状态和历史记录已经不可信，
因此在有人介入检查之前，阻止任何进一步的变更会更安全。
恢复方法就是再次执行 `--resync`。

建议最初先使用 `--resync --dry-run --verbose`，
并*仔细*审阅将要进行的变更，然后再在没有 `--dry-run`
的情况下执行 `--resync`。

这些事件大多源于内部调用返回错误状态。
当发生这样的关键错误时，`{...}.path1.lst` 和 `{...}.path2.lst`
列表文件会被重命名为 `.lst-err` 扩展名，
这会阻塞所有未来的 bisync 运行（因为找不到正常的 `.lst` 文件）。
Bisync 将它们保存在 rclone 缓存目录的 `bisync` 子目录下，
通常在 Linux 上的 `${HOME}/.cache/rclone/bisync/`。

某些错误被视为临时错误，不会阻止重新运行 bisync。
而 *关键返回* 会阻止进一步的 bisync 运行。

另请参见：[`--resilient`](#resilient)、[`--recover`](#recover)、
[`--max-lock`](#max-lock)、[优雅停机](#graceful-shutdown)

### 锁文件

当 bisync 运行时，会在 bisync 工作目录下创建一个锁文件，
通常位于 Linux 上的 `~/.cache/rclone/bisync/PATH1..PATH2.lck`。
如果 bisync 崩溃或挂起，锁文件将保留在原位，
并阻塞该路径的*任何*后续 bisync 运行。
作为调试工作的一部分，请删除锁文件。
当先前的调用耗时较长时，锁文件实际上会阻塞后续（例如由 *cron*
调度的）运行。
锁文件包含阻塞进程的 *PID*，这在调试时可能会有所帮助。
锁文件可以通过 [`--max-lock`](#max-lock) 标志
设置在一段时间后自动过期。

**注意**
虽然允许并发的 bisync 运行，但请*格外小心*，
确保并发运行之间同步的目录树没有重叠，
否则可能会出现文件复制、文件被删除以及一连串混乱。

### 退出码

`rclone bisync` 向调用程序返回以下退出码：

- `0` 表示成功运行，
- `1` 表示非关键性的失败运行（重试可能成功），
- `2` 表示语法或使用错误，
- `7` 表示被关键性地中止的运行（需要 `--resync` 才能恢复）。

另请参见主文档中关于 [退出码](/docs/#exit-code) 的章节。

### 优雅停机

Bisync 拥有一个"优雅停机"模式，通过在运行期间发送 `SIGINT`
或按下 `Ctrl+C` 来激活。触发后，bisync 会尽最大努力在计时器
耗尽前干净地退出。如果 bisync 当时正在传输文件，
它会尝试清空自己的队列——完成已经开始的任务，但不再接受新任务。
如果在 30 秒内无法完成，它将在那个时刻取消正在进行的传输，
然后给自己最多 60 秒的时间收尾、保存下次运行所需的状态并退出。
使用 `-vP` 标志时，你会看到持续的状态更新以及一个关于
优雅停机是否成功的最终确认。

在"优雅停机"序列进行中的任何时刻，第二次 `SIGINT`
或 `Ctrl+C` 将触发一次立即的、不优雅的退出，
这会使状态变得更加混乱。如果使用了
[`--recover`](#recover) 模式，通常仍然可以稳健地恢复，
否则就需要执行 `--resync`。

如果你打算使用优雅停机模式，建议同时使用
[`--resilient`](#resilient) 和 [`--recover`](#recover)，
并且**不要**使用 [`--inplace`](/docs/#inplace)，
否则可能在一端留下未写完的文件，这些文件在下次运行时
可能被误认为是真实文件。另请注意，在突然中断的情况下，
会留下一个 [锁文件](#lock-file) 阻塞并发运行。
你需要将其删除后才能继续下一次运行
（如果使用了 `--max-lock`，也可以等它自动过期）。

## 局限性

### 支持的后端

Bisync 通过与所有 rclone 后端进行集成测试来验证兼容性。
大多数后端（包括下面未列出的所有后端）被认为完全受支持，
不存在已知问题。然而，这些测试偶尔会揭示出某些后端的问题，
通常与特定服务商自身的限制有关
（例如不允许的特殊字符和文件编码等），
这超出了 rclone 的控制范围。

以下后端存在已知问题，需要进一步调查：

<!--- start list_failures - DO NOT EDIT THIS SECTION - use make commanddocs --->
- `TestDropbox` (`dropbox`)
  - [`TestBisyncRemoteRemote/normalization`](https://pub.rclone.org/integration-tests/current/dropbox-cmd.bisync-TestDropbox-1.txt)
- `TestSeafile` (`seafile`)
  - [`TestBisyncLocalRemote/volatile`](https://pub.rclone.org/integration-tests/current/seafile-cmd.bisync-TestSeafile-1.txt)
- `TestSeafileV6` (`seafile`)
  - [`TestBisyncLocalRemote/volatile`](https://pub.rclone.org/integration-tests/current/seafile-cmd.bisync-TestSeafileV6-1.txt)
- Updated: 2026-01-30-010015
<!--- end list_failures - DO NOT EDIT THIS SECTION - use make commanddocs --->

以下后端要么近期未经测试，要么存在目前认为无法修复的已知问题：

<!--- start list_ignores - DO NOT EDIT THIS SECTION - use make commanddocs --->
- `TestArchive` (`archive`)
- `TestCache` (`cache`)
- `TestDrime` (`drime`)
- `TestFileLu` (`filelu`)
- `TestFilesCom` (`filescom`)
- `TestImageKit` (`imagekit`)
- `TestJottacloud` (`jottacloud`)
- `TestLinkbox` (`linkbox`)
- `TestMailru` (`mailru`)
- `TestMega` (`mega`)
- `TestOpenDrive` (`opendrive`)
- `TestOracleObjectStorage` (`oracleobjectstorage`)
- `TestPikPak` (`pikpak`)
- `TestPixeldrain` (`pixeldrain`)
- `TestProtonDrive` (`protondrive`)
- `TestPutio` (`putio`)
- `TestQuatrix` (`quatrix`)
- `TestS3GCS` (`s3`)
  - `TestBisyncRemoteRemote/extended_filenames`
- `TestS3Rclone` (`s3`)
- `TestSFTPRsyncNet` (`sftp`)
- `TestStorj` (`storj`)
- `TestWebdavInfiniteScale` (`webdav`)
- `TestWebdavNextcloud` (`webdav`)
- `TestWebdavOwncloud` (`webdav`)
- `TestnStorage` (`netstorage`)
<!--- end list_ignores - DO NOT EDIT THIS SECTION - use make commanddocs --->
([更多信息](https://github.com/rclone/rclone/blob/master/fstest/test_all/config.yaml))

上述列表会针对 rclone 的每个稳定版本进行更新。
若要查看基于最新 beta 版本、每晚更新的测试结果，
请访问 rclone 的 [集成测试状态页面](https://pub.rclone.org/integration-tests/current/)。

`rclone bisync` 的早期 beta 版本要求两个底层后端都必须支持
修改时间，否则拒绝运行。
该限制已在 `v1.66` 中被取消，因为 bisync 现在支持使用
checksum 和/或 size 进行比较（而非 modtime，或与之结合使用）。
详见 [`--compare`](#compare)。

### 并发修改

当使用 **Local、FTP 或 SFTP** remote 并配合
[`--inplace`](/docs/#inplace) 时，rclone 在复制时
不会在目标端创建 *临时* 文件，因此如果连接中断，
已创建的文件可能已损坏，并可能在下次同步时被传播回原始路径，
从而导致数据丢失。因此建议*省略* `--inplace`。

在 bisync 运行*期间*被修改的文件可能导致数据丢失。
在 `rclone v1.66` 之前，这通常出现在同步过程中文件系统
被运行中的进程持续大量写入的动态环境中。
从 `rclone v1.66` 开始，bisync 被重新设计为采用"快照"模型，
大幅降低了同步过程中发生变化所带来的风险。
当前同步未检测到的变更会在下一次同步时被检测到，
不再会导致整个运行抛出关键错误。
此外还存在一种机制，可以将文件标记为下次需要内部重新检查，
以提供额外的安全保障。因此，应该不再需要在系统空闲时
才进行同步——但是请注意，如果一个文件恰好在
bisync 读取/写入它的同一时刻发生了变化，仍然可能出错
（这与 `rclone sync` 中会发生的情况一样）。
（另请参见：[`--ignore-checksum`](https://rclone.org/docs/#ignore-checksum)、
[`--local-no-check-updated`](https://rclone.org/local/#local-no-check-updated)）

### 空目录

默认情况下，一端上新创建/删除的空目录*不会*被传播到另一端。
这是因为 bisync（以及 rclone）天然以文件而非目录为操作对象。
但是，可以通过 `--create-empty-src-dirs` 标志改变这一行为，
其工作方式与 [`sync`](/commands/rclone_sync/) 和
[`copy`](/commands/rclone_copy/) 中的方式大致相同。
当使用该标志时，一端创建或删除的空目录也会在另一端
被创建或删除。需要注意以下几点：

- `--create-empty-src-dirs` 与 `--remove-empty-dirs` 不兼容。
两者只能使用其中一个（或都不用）。
- 建议*不要*在 `--create-empty-src-dirs` 和默认（不使用
`--create-empty-src-dirs`）之间反复切换，除非配合运行 `--resync`。
这是因为看起来好像所有目录（而不只是空目录）都被创建/删除了，
实际上你只是在切换是否让 bisync 看到它们。
这看起来比实际情况更吓人，但最好还是坚持使用其中一种，
并在需要切换时使用 `--resync`。

### 重命名目录

默认情况下，在 Path1 端重命名一个目录会导致 Path2 端所有
文件被删除，然后从 Path1 端把所有文件再复制到 Path2。
Bisync 会将原目录名下的所有文件视为已删除，将新目录名下的
所有文件视为新建。

一个推荐的解决方案是使用
[`--track-renames`](/docs/#track-renames)，
从 `rclone v1.66` 开始 bisync 已支持该选项。
请注意 `--track-renames` 在 `--resync` 期间不可用，
因为 `--resync` 不会删除任何东西
（`--track-renames` 仅支持 `sync`，不支持 `copy`。）

另一种方法，在两侧将目录重命名为相同的名称，是最高效
也最有效的目录重命名方式。（从 `rclone v1.64` 开始，
完成这样的重命名后不再需要执行 `--resync`，
因为 bisync 会自动检测到 Path1 和 Path2 是一致的。）

### 默认使用 `--fast-list`

与大多数其他 rclone 命令不同，bisync 默认使用
[`--fast-list`](/docs/#fast-list)（对于支持的后端）。
在很多场景下这是理想的，但也有一些场景
bisync 在*不*使用 `--fast-list` 时反而更快，
并且还有一个 [Google Drive 用户拥有大量空目录时的已知问题](https://github.com/rclone/rclone/commit/cbf3d4356135814921382dd3285d859d15d0aa77)。
目前，避免使用 `--fast-list` 的推荐方法是在所有 bisync 命令
中加上 `--disable ListR`。默认行为在未来版本中可能会改变。

### 大小写（与 Unicode）敏感性 {#case-sensitivity}

从 `v1.66` 开始，大小写和 Unicode 形式上的差异不再导致关键错误，
并且（跨文件系统比较时的）规范化处理遵循与 `rclone sync`
相同的标志和默认值。参见以下选项（bisync 全部支持），
以更细粒度地控制这一行为：

- [`--fix-case`](/docs/#fix-case)
- [`--ignore-case-sync`](/docs/#ignore-case-sync)
- [`--no-unicode-normalization`](/docs/#no-unicode-normalization)
- [`--local-unicode-normalization`](/local/#local-unicode-normalization) 和
[`--local-case-sensitive`](/local/#local-case-sensitive)
（注意：这些通常不是你所期望的行为。）

请注意，在（可能罕见的）同时使用 `--fix-case` 且文件在两侧
都是新文件/已变更、checksum 匹配但文件名大小写不一致的情况下，
就 `--fix-case` 的目的而言，Path1 的文件名会被视为赢家
（Path2 会被重命名以与其匹配）。

## Windows 支持 {#windows}

Bisync 已在 Windows 8.1、Windows 10 Pro 64-bit 以及 Windows 的
GitHub runner 上测试通过。

允许使用驱动器盘符，包括映射到网络驱动器的盘符
（`rclone bisync J:\localsync GDrive:`）。
如果省略盘符，则默认为 shell 当前所在的驱动器。
驱动器盘符是一个单字符后接 `:`，因此云端名称必须长于一个字符。

支持绝对路径（带或不带盘符），以及相对路径
（带或不带盘符）。

工作目录创建于 `C:\Users\MyLogin\AppData\Local\rclone\bisync`。

请注意，bisync 的输出中可能会混合显示正斜杠 `/` 和反斜杠 `\`。

请注意 Windows 上大小写不敏感的目录和文件命名
与 Linux 上大小写敏感的差异。

## 过滤 {#filtering}

关于过滤规则的写法与解释，请参见 [过滤文档](/filtering/)。

Bisync 的 [`--filters-file`](#filters-file) 标志对 rclone 的
[--filter-from](/filtering/#filter-from-read-filtering-patterns-from-a-file)
过滤机制进行了少量扩展。
对于某次 bisync 运行，你只能提供*一个* `--filters-file`。
同时也支持 `--include*`、`--exclude*` 和 `--filter` 标志。

### 如何过滤目录

对目录树进行过滤是同步中的一项关键特性。

你可能希望排除在同步之外的目录树示例
（始终在 Path1/Path2 根级别之下）：

- 仅包含软件构建中间文件的目录树。
- 包含应用临时文件和数据的目录树，例如 Windows 的
  `C:\Users\MyLogin\AppData\` 目录树。
- 包含体量较大、不太重要、或者被运行中的进程持续频繁读写的
  文件的目录树。

反过来，也可能只希望同步选定的几个目录，而排除其他所有目录。
请参见下面的
[Windows 用户目录的 include 风格过滤示例](#include-filters)。

### 过滤文件编写指南

1. 首先排除目录树：
    - 例如 `- /AppData/`
    - 末尾不需要 `**`。一旦排除了某个目录层级，
      它下面的所有内容 rclone 都不会再去查看。
    - 优先排除那些不需要、体量大、动态变化剧烈、
      或可能存在访问权限问题的目录。
    - 优先排除这些目录可以让 rclone 的操作（明显）更快。
    - 也可以排除特定文件，参考下面的 Dropbox 排除示例。
2. 决定哪种方式更简单（或更清晰）：
    - 仅包含选定的目录，从而*排除其他所有内容* —— 或者 ——
    - 排除选定的目录，从而*包含其他所有内容*
3. 包含选定的目录：
    - 加上形如 `+ /Documents/PersonalFiles/**` 的行来选择
      哪些目录被包含进同步。
    - 末尾的 `**` 表示包含指定目录树的所有层级。
    - 使用 include 风格的过滤时，Path1/Path2 根目录下的文件
      不会被包含。可以使用 `+ /*` 来包含它们。
    - 将 RCLONE_TEST 文件放在这些被包含的目录树内。
      只会查找这些目录树中的 RCLONE_TEST 文件。
    - 最后在过滤文件末尾添加 `- **` 来排除其他所有内容。
    - 跳过第 4 步。
4. 排除选定的目录：
    - 加上更多类似第 1 步的行。
      例如：`-/Desktop/tempfiles/`，或 `- /testdir/`。
      同样地，末尾不需要 `**`。
    - *不要*在文件中添加 `- **`。如果没有这一行，
      所有未被显式排除的内容都会被包含。
    - 跳过第 3 步。

关于过滤文件语法的几条规则，是对
[过滤文档](/filtering/) 的补充：

- 行首可以是空格和制表符——rclone 会去除前导空白。
- 如果第一个非空白字符是 `#`，则该行为注释，会被忽略。
- 空行会被忽略。
- 过滤行的第一个非空白字符必须是 `+` 或 `-`。
- 在 `+/-` 与路径项之间允许且仅允许 1 个空格。
- 路径项中只使用正斜杠（`/`），即便在 Windows 上也是如此。
- 行的其余部分会被视为路径项。
  尾部空白会被原样保留，这很可能是一个错误。

### Windows 用户目录的 include 风格过滤示例 {#include-filters}

本 Windows *include 风格* 示例基于将同步根（Path1）设置为
`C:\Users\MyLogin`。其策略是选择特定的目录，
与一个网络驱动器（Path2）进行同步。

- `- /AppData/` 排除整个 Windows 系统存储目录树，
  这些内容不需要同步。
  在我的场景下，AppData 拥有超过 11 GB 的我并不关心的内容，
  其中部分子目录对我的用户登录不可访问，
  会导致 bisync 关键性中止。
- Windows 会以大写和小写形式同时创建 `NTUSER` 开头的缓存文件，
  位于 `C:\Users\MyLogin`。这些文件可能处于动态变化状态、
  被锁定，并且通常属于 *不需要关心* 的内容。
- 只有少数几个包含*我的*数据的目录是我希望同步的，
  形式是 `+ /<path>`。通过只选择我需要的目录树，
  可以避开各种应用在
  `C:\Users\MyLogin\Documents` 下创建的十几个目录。
- 通过添加 `+ /*` 这一行，包含同步根目录
  `C:\Users\MyLogin` 下的文件。
- 这是一个 include 风格的过滤文件，因此文件以 `- **` 结尾，
  排除所有未被显式包含的内容。

```text
- /AppData/
- NTUSER*
- ntuser*
+ /Documents/Family/**
+ /Documents/Sketchup/**
+ /Documents/Microcapture_Photo/**
+ /Documents/Microcapture_Video/**
+ /Desktop/**
+ /Pictures/**
+ /*
- **
```

还要注意，Windows 实现了多个"库"链接，例如
`C:\Users\MyLogin\My Documents\My Music` 指向
`C:\Users\MyLogin\Music`。
rclone 将这些视为链接，因此如果你希望跟随这些链接，
必须在 bisync 命令行加上 `--links`。
我的实践是跟随链接时会出现权限错误，
因此我不加 rclone 的 `--links` 标志，
但这样就会产生大量 `Can't follow symlink…` 噪音。
可以通过在 bisync 命令行加上 `--quiet` 来抑制这些噪音。

## 用于 Dropbox 的 exclude 风格过滤文件示例 {#exclude-filters}

- Dropbox 不允许同步所列出的临时文件和配置/数据文件。
  `- <filename>` 过滤规则会在同步树的任意位置排除这些文件。
  建议为不需要同步的文件类型添加类似的排除，
  例如核心转储文件和软件构建产物。
- bisync 测试会在同步树顶层创建 `/testdir/`，
  并在测试结束后通常会删除该目录。
  如果在 `/testdir/` 存在期间运行普通同步，
  `--check-access` 阶段可能因为 RCLONE_TEST 文件不平衡而失败。
  `- /testdir/` 过滤规则会阻止该目录被同步。
  如果你并不进行 bisync 的开发测试，则不需要此排除项。
- Path1/Path2 根下的其他所有内容都会被同步。
- RCLONE_TEST 文件可以放在树中的任何位置，包括根目录。

### 适用于 Dropbox 的过滤文件示例 {#example-filters-file}

```text
# Filter file for use with bisync
# See https://rclone.org/filtering/ for filtering rules
# NOTICE: If you make changes to this file you MUST do a --resync run.
#         Run with --dry-run to see what changes will be made.

# Dropbox won't sync some files so filter them away here.
# See https://help.dropbox.com/installs-integrations/sync-uploads/files-not-syncing
- .dropbox.attr
- ~*.tmp
- ~$*
- .~*
- desktop.ini
- .dropbox

# Used for bisync testing, so excluded from normal runs
- /testdir/

# Other example filters
#- /TiBU/
#- /Photos/
```

### --check-access 如何处理过滤

在一次 bisync 运行的开始，会使用用户的 `--filters-file`
为 Path1 和 Path2 收集列表。在 check access 阶段，
bisync 会扫描这些列表，查找 `RCLONE_TEST` 文件。
任何被 `--filters-file` 隐藏的 `RCLONE_TEST` 文件
都不会出现在列表中，因此在 check access 阶段不会被检查。

## 故障排除 {#troubleshooting}

### 阅读 bisync 日志

下面是两次正常的运行。第一次是远端有一个较新的文件。
第二次是本地和远端之间没有任何差异。

```text
2021/05/16 00:24:38 INFO  : Synching Path1 "/path/to/local/tree/" with Path2 "dropbox:/"
2021/05/16 00:24:38 INFO  : Path1 checking for diffs
2021/05/16 00:24:38 INFO  : - Path1    File is new                         - file.txt
2021/05/16 00:24:38 INFO  : Path1:    1 changes:    1 new,    0 newer,    0 older,    0 deleted
2021/05/16 00:24:38 INFO  : Path2 checking for diffs
2021/05/16 00:24:38 INFO  : Applying changes
2021/05/16 00:24:38 INFO  : - Path1    Queue copy to Path2                 - dropbox:/file.txt
2021/05/16 00:24:38 INFO  : - Path1    Do queued copies to                 - Path2
2021/05/16 00:24:38 INFO  : Updating listings
2021/05/16 00:24:38 INFO  : Validating listings for Path1 "/path/to/local/tree/" vs Path2 "dropbox:/"
2021/05/16 00:24:38 INFO  : Bisync successful

2021/05/16 00:36:52 INFO  : Synching Path1 "/path/to/local/tree/" with Path2 "dropbox:/"
2021/05/16 00:36:52 INFO  : Path1 checking for diffs
2021/05/16 00:36:52 INFO  : Path2 checking for diffs
2021/05/16 00:36:52 INFO  : No changes found
2021/05/16 00:36:52 INFO  : Updating listings
2021/05/16 00:36:52 INFO  : Validating listings for Path1 "/path/to/local/tree/" vs Path2 "dropbox:/"
2021/05/16 00:36:52 INFO  : Bisync successful
```

### 试运行（dry run）的怪异现象

`--dry-run` 的消息可能会提示它将尝试删除某些文件。
例如，如果一个文件在 Path2 上是新的、Path1 上不存在，
正常情况下它会被复制到 Path1，但启用 `--dry-run` 后
这些复制不会发生，于是会出现试图在 Path2 上删除的操作，
该删除又会被 `--dry-run` 阻止：`... Not deleting as --dry-run`。

这一令人困惑的情形完全是 `--dry-run` 标志造成的副作用。
请仔细审视被建议的删除操作——如果这些文件本来是要被复制到
Path1 的，那么 Path2 上那些被"威胁"的删除可以忽略。

### 重试

Rclone 内置了重试机制。如果你使用 `--verbose` 运行，
你会看到类似下方的错误和重试信息，这通常不是 bug。
如果在运行结束时看到 `Bisync successful` 而不是
`Bisync critical error` 或 `Bisync aborted`，
那么本次运行是成功的，可以忽略这些错误信息。

下面的运行展示了一次间歇性失败。第 *5* 行和第 *6* 行
是底层消息。第 *6* 行是冒出来的 *warning* 消息，
用于传达错误。Rclone 通常会对失败命令进行重试，
因此日志中可能包含大量类似的消息。

由于第 *7* 行没有任何最终的 error/warning 消息，
rclone 已经在重试后从失败中恢复，本次同步整体成功。

```text
1: 2021/05/14 00:44:12 INFO  : Synching Path1 "/path/to/local/tree" with Path2 "dropbox:"
2: 2021/05/14 00:44:12 INFO  : Path1 checking for diffs
3: 2021/05/14 00:44:12 INFO  : Path2 checking for diffs
4: 2021/05/14 00:44:12 INFO  : Path2:  113 changes:   22 new,    0 newer,    0 older,   91 deleted
5: 2021/05/14 00:44:12 ERROR : /path/to/local/tree/objects/af: error listing: unexpected end of JSON input
6: 2021/05/14 00:44:12 NOTICE: WARNING  listing try 1 failed.                 - dropbox:
7: 2021/05/14 00:44:12 INFO  : Bisync successful
```

下面的日志展示了一次 *关键性失败*，需要执行 `--resync` 才能恢复。
参见 [运行时错误处理](#error-handling) 章节。

```text
2021/05/12 00:49:40 INFO  : Google drive root '': Waiting for checks to finish
2021/05/12 00:49:40 INFO  : Google drive root '': Waiting for transfers to finish
2021/05/12 00:49:40 INFO  : Google drive root '': not deleting files as there were IO errors
2021/05/12 00:49:40 ERROR : Attempt 3/3 failed with 3 errors and: not deleting files as there were IO errors
2021/05/12 00:49:40 ERROR : Failed to sync: not deleting files as there were IO errors
2021/05/12 00:49:40 NOTICE: WARNING  rclone sync try 3 failed.           - /path/to/local/tree/
2021/05/12 00:49:40 ERROR : Bisync aborted. Must run --resync to recover.
```

### "被感染"或"滥用"文件被拒绝下载

Google Drive 对某些文件类型（`.exe`、`.apk` 等）设有过滤器，
默认情况下无法从 Google Drive 复制到本地文件系统。
如果遇到问题，请使用 `--verbose` 运行，以查看具体是哪些文件
产生了投诉。如果错误信息是
`This file has been identified as malware or spam and cannot be downloaded`，
建议使用
[--drive-acknowledge-abuse](/drive/#drive-acknowledge-abuse) 标志。

### Google Docs（以及其他大小未知的文件） {#gdocs}

从 `v1.66` 开始，[Google Docs](/drive/#import-export-of-google-documents)
（包括 Google Sheets、Slides 等）已在 bisync 中受支持，
受与 `rclone sync` 相同的选项、默认值和限制约束。
当使用 drive 与非 drive 后端进行 bisync 时，
drive -> 非 drive 方向由
[`--drive-export-formats`](/drive/#drive-export-formats) 控制
（默认 `"docx,xlsx,pptx,svg"`），
非 drive -> drive 方向由
[`--drive-import-formats`](/drive/#drive-import-formats) 控制（默认无）。

例如，使用默认的 export/import 格式时，
drive 端的 Google Sheet 会被同步为非 drive 端的 `.xlsx` 文件。
在反方向，文件名匹配某个已存在 Google Sheet 的 `.xlsx` 文件
会被同步为该 Google Sheet，而那些不匹配任何已存在 Google Sheet 的
`.xlsx` 文件则会被作为普通 `.xlsx` 文件复制到 drive
（不会转换为 Sheet，尽管 Google Drive 的 Web UI 可能会给你
将其作为 Sheet 打开的选项。）

如果设置了 `--drive-import-formats`（默认未设置），
那么所有指定的格式在没有匹配名称的 Google Doc 时都会被转换为
Google Doc。注意：这种转换可能损失较大，并且在大多数情况下
很可能并非你所期望的！

如果希望以 URL 快捷方式链接的形式同步 Google Docs
（类似"Drive for Desktop"的方式），可使用：
`--drive-export-formats url`（或
[其他选项](https://rclone.org/drive/#exportformats:~:text=available%20Google%20Documents.-,Extension,macOS,-Standard%20options)）。

请注意，这些链接文件无法在非 drive 端被编辑——
如果你试图把编辑后的链接文件同步回 drive，将会出错。
它们*可以*被删除（删除的结果是对应的 Google Doc 被删除）。
如果你在非 drive 端创建了一个 `.url` 文件，且它不匹配
任何已存在的 Google Doc，那么 bisync 它只会把这个 `.url` 文件
原样复制到 drive（不会创建 Google Doc）。
因此，作为一般经验法则，可以将它们视为非 drive 端上的
只读占位符，所有编辑操作都在 drive 端进行。

同样地，即便使用其他 export-format，也建议只在 drive 端
对 Google Docs 进行移动/重命名。这是因为在其他情况下，
bisync 会将其解读为"一个文件被删除、另一个文件被创建"，
相应地，它会删除那个 Google Doc，并在新路径创建一个新文件。
（这个新文件是否为 Google Doc，取决于 `--drive-import-formats` 设置。）

最后，请注意 drive 端的所有 Google Docs 的大小均为 `-1`，
且没有 checksum。因此，不能通过 `--checksum` 或 `--size-only`
标志可靠地同步它们。（准确地说：它们仍然会被创建/删除，
bisync 的差异引擎也会注意到变化并加入同步队列，
但底层的 sync 函数会认为它们是相同的并跳过它们。）
要绕过此问题，请使用默认（modtime 和 size）方式，
而不是 `--checksum` 或 `--size-only`。

若要完全忽略 Google Docs，请使用
[`--drive-skip-gdocs`](/drive/#drive-skip-gdocs)。

## 使用示例

### Cron {#cron}

Rclone 目前还没有内置的本地文件系统变更监控能力，
只能周期性地盲目运行。
在 Windows 上可以使用 *任务计划程序* 实现这一点，
在 Linux 上可以使用下文介绍的 *Cron*。

第 1 个示例每 5 分钟在本地目录和 OwnCloud 服务器之间
进行一次同步，输出记录到 runlog 文件：

```text
# Minute (0-59)
#      Hour (0-23)
#           Day of Month (1-31)
#                Month (1-12 or Jan-Dec)
#                     Day of Week (0-6 or Sun-Sat)
#                         Command
  */5  *    *    *    *   /path/to/rclone bisync /local/files MyCloud: --check-access --filters-file /path/to/bysync-filters.txt --log-file /path/to//bisync.log
```

关于 crontab 时间间隔表达式的细节，请参见
[crontab 语法](https://www.man7.org/linux/man-pages/man1/crontab.1p.html#INPUT_FILES)。

如果将 `rclone bisync` 作为 cron 任务运行，请将 stdout/stderr
重定向到一个文件。
第 2 个示例每小时将本地与 Dropbox 同步一次，
并把所有 stdout（通过 `>>`）和 stderr（通过 `2>&1`）
记录到日志文件。

```text
0 * * * * /path/to/rclone bisync /path/to/local/dropbox Dropbox: --check-access --filters-file /home/user/filters.txt >> /path/to/logs/dropbox-run.log 2>&1
```

### 在多台主机之间共享一个加密的文件夹树

bisync 可以让本地文件夹与云服务保持同步，
但如果你有一些需要同步的高度敏感文件该怎么办？

云服务的用途是用于在家庭网络、旅途中的个人笔记本
以及工作电脑之间交换常规和敏感的个人文件。
常规数据并不敏感。
对于敏感数据，可以配置一个 rclone [crypt remote](/crypt/)，
指向本地磁盘树中一个被 bisync 同步到 Dropbox 的子目录，
然后再为这个本地 crypt 目录设置一条 bisync，指向
主同步树之外的一个目录。

### Linux 服务器配置

- `/path/to/DBoxroot` 是我的本地同步树的根。
  下面有大量子目录。
- `/path/to/DBoxroot/crypt` 是加密文件的根子目录。
  该本地目录被配置为一个名为 `Dropcrypt:` 的 rclone crypt remote。
  参见下方的 [rclone.conf 片段](#rclone-conf-snippet)。
- `/path/to/my/unencrypted/files` 是我的敏感文件的根——
  未加密、且不在同步到 Dropbox 的树中。
- 为了让本地未加密的文件与加密的 Dropbox 版本保持同步，
  我手动运行 `bisync /path/to/my/unencrypted/files DropCrypt:`。
  该步骤可以打包为一个脚本，在最后一步完整 Dropbox 树同步
  的前后运行，从而主动保持敏感文件的同步。
- `bisync /path/to/DBoxroot Dropbox:` 由 cron 周期性运行，
  让我的整个本地同步树与 Dropbox 保持同步。

### Windows 笔记本配置

- Dropbox 客户端在后台保持本地树
  `C:\Users\MyLogin\Dropbox` 与 Dropbox 持续同步。
  我也可以改用 `rclone bisync` 来实现。
- 在 `C:\Users\MyLogin\Documents\DropLocal` 下的一个独立目录树
  承载未加密的文件/文件夹。
- 为了让本地未加密的文件与加密的 Dropbox 版本保持同步，
  我手动运行以下命令：
  `rclone bisync C:\Users\MyLogin\Documents\DropLocal Dropcrypt:`。
- 之后由 Dropbox 客户端把变更同步到 Dropbox。

### rclone.conf 片段 {#rclone-conf-snippet}

```ini
[Dropbox]
type = dropbox
...

[Dropcrypt]
type = crypt
remote = /path/to/DBoxroot/crypt          # on the Linux server
remote = C:\Users\MyLogin\Dropbox\crypt   # on the Windows notebook
filename_encryption = standard
directory_name_encryption = true
password = ...
...
```

## 测试 {#testing}

只有当你正在为 rclone 做开发时，才需要阅读本节。
你需要在本地准备好 rclone 源代码，才能进行 bisync 测试。

Bisync 拥有专门的测试框架，实现在 rclone 源码树中的
`bisync_test.go` 文件里。测试套件基于
`go test` 命令。测试用例序列存储在 `cmd/bisync/testdata`
目录下的子目录中。可以通过目录名单独调用各个测试，例如
`go test . -case basic -remote local -remote2 gdrive: -v`

测试会在远端创建一个临时目录，并在结束后清除。
如果在测试运行过程中出现间歇性错误且 rclone 进行了重试，
这些错误会被捕获并标记为无效的 MISCOMPARE。
重新运行测试通常会通过。请将这类失败视为噪声。

### 测试命令语法

```text
usage: go test ./cmd/bisync [options...]

Options:
  -case NAME        Name(s) of the test case(s) to run. Multiple names should
                    be separated by commas. You can remove the `test_` prefix
                    and replace `_` by `-` in test name for convenience.
                    If not `all`, the name(s) should map to a directory under
                    `./cmd/bisync/testdata`.
                    Use `all` to run all tests (default: all)
  -remote PATH1     `local` or name of cloud service with `:` (default: local)
  -remote2 PATH2    `local` or name of cloud service with `:` (default: local)
  -no-compare       Disable comparing test results with the golden directory
                    (default: compare)
  -no-cleanup       Disable cleanup of Path1 and Path2 testdirs.
                    Useful for troubleshooting. (default: cleanup)
  -golden           Store results in the golden directory (default: false)
                    This flag can be used with multiple tests.
  -debug            Print debug messages
  -stop-at NUM      Stop test after given step number. (default: run to the end)
                    Implies `-no-compare` and `-no-cleanup`, if the test really
                    ends prematurely. Only meaningful for a single test case.
  -refresh-times    Force refreshing the target modtime, useful for Dropbox
                    (default: false)
  -verbose          Run tests verbosely
```

注意：与必须以双横线（`--`）开头的 rclone 标志不同，
测试命令的标志既可以使用单横线 `-`，也可以使用双横线 `--`。

### 运行测试

- `go test . -case basic -remote local -remote2 local`
  仅使用本地文件系统运行 `test_basic` 测试用例，
  将一个本地目录与另一个本地目录进行同步。
  测试脚本的输出会显示到控制台，而 scenario.txt 中的命令
  其输出会被送到 `.../workdir/test.log` 文件中，
  并最终与 golden 副本进行比较。
- `go test` 之后的第一个参数应当是包含 bisync 源代码的目录的相对名。
  如果你就在该目录下运行测试，则参数为 `.`（当前目录），
  如下方大多数示例所示。
  如果你从 rclone 源码目录运行 bisync 测试，命令应当是
  `go test ./cmd/bisync ...`。
- 测试引擎会扭曲 rclone 的输出，以确保与 golden 列表和日志可比。
- 测试用例位于 `./cmd/bisync/testdata`。
  测试 `-case` 参数应当与该目录下的某个子目录的全名匹配。
  磁盘上每个测试子目录名都必须以 `test_` 开头，
  在命令行上为了简洁可以省略此前缀。
  同样，名称中的下划线可以替换为短横线以便输入。
- `go test . -remote local -remote2 local -case all` 运行所有测试。
- Path1 和 Path2 既可以是关键字 `local`，
  也可以是已配置的云服务名称。
  `go test . -remote gdrive: -remote2 dropbox: -case basic`
  会在这两个服务之间运行测试，且不会向本地文件系统传输任何文件。
- 测试运行的 stdout 和 stderr 控制台输出可以重定向到文件，例如
  `go test . -remote gdrive: -remote2 local -case all > runlog.txt 2>&1`

### 测试执行流程

1. 将测试用例 `initial` 目录中的基础设置
   应用到 Path1 和 Path2 文件系统
   （通过 rclone copy 将 initial 目录复制到 Path1，
   再 rclone sync Path1 到 Path2）。
2. 应用 scenario.txt 文件中的命令，输出被重定向
   到测试工作目录中的 `test.log` 文件。
   通常，`scenario.txt` 中的第一个实际命令
   是执行一次 `--resync`，它会在测试工作目录中
   （相对于临时测试目录的 `.../workdir/`）
   建立基线的 `{...}.path1.lst` 和 `{...}.path2.lst` 文件。
   测试过程中会执行各种命令并生成列表快照。
3. 最后，将测试工作目录的内容与测试用例的 golden 目录内容进行比较。

### 关于测试的注意事项

- 测试用例位于 `./cmd/bisync/testdata` 之下的各个目录。
  对测试的命令行引用被理解为引用 `testdata` 下的某个目录。
  例如，
  `go test ./cmd/bisync -case dry-run -remote gdrive: -remote2 local`
  引用的是 `./cmd/bisync/testdata/test_dry_run` 中的测试用例。
- 测试工作目录位于相对临时测试目录的 `.../workdir`，
  在 Linux 上通常位于 `/tmp` 下。
- 本地测试同步树创建于系统临时目录下，
  名称类似 `bisync.XXX`。
- 远端测试同步树位于
  `<remote:>/bisync.XXX/` 下的一个临时目录中。
- 会在对应的本地或云测试 remote 的临时目录下
  创建 `path1` 和/或 `path2` 子目录。
- 默认情况下，每次测试运行后 Path1 和 Path2 的测试目录
  以及 workdir 都会被删除。
  `-no-cleanup` 标志在校验和调试某个测试时禁用
  这些目录的清除。在运行下一个测试之前，
  这些目录会被清空，与是否使用 `-no-cleanup` 无关。
- 你很可能希望将 `- /testdir/` 添加到常规的
  bisync `--filters-file` 中，以免常规同步尝试同步
  测试用的临时目录——在某些测试用例中，这些目录可能存在
  `RCLONE_TEST` 误匹配，这会触发 `--check-access` 系统。
  `--check-access` 机制被硬编码为忽略 `bisync/testdata`
  之下的 `RCLONE_TEST` 文件，因此即便测试树中存在
  检查文件不匹配的情况，测试用例也可以驻留在同步树上。
- 部分 Dropbox 测试可能会失败，特别会打印以下消息：
  `src and dst identical but can't set mod time without deleting and re-uploading`
  这是预期内的，是由于 Dropbox 处理修改时间的方式导致的。
  应当使用 `-refresh-times` 测试标志来弥补这一行为。
- 如果 Dropbox 测试因为请求限制而失败，并打印
  `too_many_requests/...: Too many requests or write operations.`
  这样的错误信息，请按
  [Dropbox App ID 说明](/dropbox/#get-your-own-dropbox-app-id) 处理。

### 更新 golden 结果

即使 bisync 源码的一个小改动也可能导致许多日志文件中
出现细微的变化。手动更新这些文件将是一场噩梦。

`-golden` 标志会将每个测试用例的 `test.log` 和 `*.lst` 列表
保存到对应的 golden 目录中。
Golden 结果会自动将本地或云的路径替换为通用字符串，
这意味着使用不同的云服务运行时结果仍能匹配。

你的常规工作流可能如下：

1. 在本地 git clone rclone 源码
2. 修改 bisync 源码并确认能够构建
3. 运行整个测试套件 `go test ./cmd/bisync -remote local`
4. 如果某些测试出现日志差异，请单独重新检查它们，例如：
   `go test ./cmd/bisync -remote local -case basic`
5. 如果你确信差异合理，可以一次性为所有测试生成 golden：
   `go test ./cmd/bisync -remote local -golden`
6. 使用单词级 diff：`git diff --word-diff ./cmd/bisync/testdata/`。
   请注意，普通的行级 diff 在这里通常没有参考价值。
7. 请*仔细*检查差异！
8. *只有*在确信无疑时才提交变更（`git commit`）。
   如果不确定，先保存你的代码变更，然后将日志差异从 git 中清除：
   `git reset [--hard]`。

### 测试用例的结构

- `<testname>/initial/` 包含一棵文件树，会被设置为
  Path1 和 Path2 测试目录上的初始状态。
- `<testname>/modfiles/` 包含将被用于修改
  Path1 和/或 Path2 文件系统的文件。
- `<testname>/golden/` 包含测试工作目录（`workdir`）
  在测试用例完成时应有的内容。
- `<testname>/scenario.txt` 包含测试主体，形式为
  各种修改文件、运行 bisync、抓取列表的命令。
  这些命令的输出被捕获到 `.../workdir/test.log`，
  用于与 golden 文件进行比较。

### 受支持的测试命令

- `test <some message>`
  将该行输出到控制台和 `test.log`：
  `test sync is working correctly with options x, y, z`
- `copy-listings <prefix>`
  以指定前缀保存测试工作目录中所有 `.lst` 列表的副本：
  `save-listings exclude-pass-run`
- `move-listings <prefix>`
  与 `copy-listings` 类似，但会移除源文件
- `purge-children <dir>`
  删除给定目录下所有子文件并清除所有子目录，但保留父目录本身。
  这一行为对 Google Drive 的测试很重要，因为删除并重新创建
  父目录会改变其 ID。
- `delete-file <file>`
  删除单个文件。
- `delete-glob <dir> <pattern>`
  删除位于给定目录下一级深度、且文件名匹配指定 glob 模式的一组文件。
- `touch-glob YYYY-MM-DD <dir> <pattern>`
  修改一组文件的修改时间。
- `touch-copy YYYY-MM-DD <source-file> <dest-dir>`
  修改文件修改时间，然后将其复制到目标目录。
- `copy-file <source-file> <dest-dir>`
  将单个文件复制到指定目录。
- `copy-as <source-file> <dest-file>`
  与上面类似，但目标必须同时包含目录和目标文件名。
- `copy-dir <src> <dst>` 和 `sync-dir <src> <dst>`
  复制/同步目录。等价于 `rclone copy` 和 `rclone sync`。
- `list-dirs <dir>`
  等价于 `rclone lsf -R --dirs-only <dir>`。
- `bisync [options]`
  针对 `-remote` 和 `-remote2` 运行 bisync。

### 受支持的替换项

- `{testdir/}` - 测试用例的根目录
- `{datadir/}` - 测试用例根目录下的 `modfiles` 目录
- `{workdir/}` - 临时测试工作目录
- `{path1/}` - Path1 测试目录树的根
- `{path2/}` - Path2 测试目录树的根
- `{session}` - 测试列表的基本名
- `{/}` - 与操作系统相关的路径分隔符
- `{spc}`、`{tab}`、`{eol}` - 空白字符
- `{chr:HH}` - 十六进制代码为 HH 的原始字节

形如 `{dir/}` 的替换项的展开结果将以 `/` 结尾
（Windows 上为反斜杠），因此在使用时不必再添加斜杠，
例如 `delete-file {path1/}file1.txt`。

## 基准测试

*本节仍在完善中。*

以下是一些关于规模、执行时间和内存使用的数据点。

第一组数据来自本地磁盘到 Dropbox 之间的测试。
[speedtest.net](https://speedtest.net) 测得的下载速度约为 170 Mbps，
上传速度约为 10 Mbps。
已有 500 个文件（每个约 9.5 MB）被同步过。
新增 50 个文件到新目录中，每个约 9.5 MB，总计约 475 MB。

Change                                | Operations and times                                   | Overall run time
--------------------------------------|--------------------------------------------------------|------------------
500 files synched (nothing to move)   | 1x listings for Path1 & Path2                          | 1.5 sec
500 files synched with --check-access | 1x listings for Path1 & Path2                          | 1.5 sec
50 new files on remote                | Queued 50 copies down: 27 sec                          |  29 sec
Moved local dir                       | Queued 50 copies up: 410 sec, 50 deletes up: 9 sec     | 421 sec
Moved remote dir                      | Queued 50 copies down: 31 sec, 50 deletes down: <1 sec |  33 sec
Delete local dir                      | Queued 50 deletes up: 9 sec                            |  13 sec

下一组数据来自一个用户的实际应用。他们有约 400 GB 的数据，
分布于 196 万个文件之间，在 Windows 本地磁盘和某个云端 remote
之间进行同步。文件的完整路径长度平均为 35 个字符
（这会影响加载时间和所需内存）。

- 将先前的列表加载到内存中（196 万个文件，列表文件大小 140 MB）
  花费约 30 秒，占用约 1 GB 内存。
- 重新获取本地文件系统的列表（生成 140 MB 的输出文件）
  花费约 XXX 秒。
- 重新获取远端文件系统的列表（生成 140 MB 的输出文件）
  花费约 XXX 秒。测得的网络下载速度为 XXX Mb/s。
- 一旦先前的和当前的 Path1、Path2 列表加载完成（总共四个，分两次加载），
  确定差异的过程非常快（本测试用例中只需几秒钟），
  任何需要复制的文件的传输时间主要由网络带宽决定。

## 参考资料

rclone 的 bisync 实现源自
[rclonesync-V2](https://github.com/cjnaz/rclonesync-V2) 项目，
包括文档和测试机制，并得到了 [@cjnaz](https://github.com/cjnaz)
的全力支持与鼓励。

`rclone bisync` 在性质上与一系列其他项目类似：

- [unison](https://github.com/bcpierce00/unison)
- [syncthing](https://github.com/syncthing/syncthing)
- [cjnaz/rclonesync](https://github.com/cjnaz/rclonesync-V2)
- [ConorWilliams/rsinc](https://github.com/ConorWilliams/rsinc)
- [jwink3101/syncrclone](https://github.com/Jwink3101/syncrclone)
- [DavideRossi/upback](https://github.com/DavideRossi/upback)

Bisync 采用差异同步技术，其基础是维护两侧同步所执行变更的历史。
请参阅
[Neil Fraser 的文章](https://neil.fraser.name/writing/sync/) 中
*Dual Shadow Method* 一节。

另请参阅 [Benjamin Pierce](http://www.cis.upenn.edu/%7Ebcpierce/papers/index.shtml#File%20Synchronization)
关于 *Unison* 以及同步问题的一系列学术论文。

## 变更日志

### `v1.74`

- 新增若干缺失的 `rc` 参数。
- 可选的 `rc` 参数现在真正是可选的。
- `rc` 输出现在提供更具结构化的信息。

### `v1.71`

- `bisync` 现在正式从 beta 版发布。

- 修复了一个问题：当 `path2` 哈希较慢且使用了 `--no-slow-hash`
或 `--slow-hash-sync-only` 时，错误地设置了哈希类型。

- 修复了在 `rc` 中并发运行 bisync 时报错的问题。

### `v1.69.1`

- 修复了在某些条件下，列表无法捕获并发修改的问题

### `v1.68`

- 修复了影响将 modtime 四舍五入到较低精度的后端的问题。

### `v1.67`

- 针对所有后端增加了集成测试。

### `v1.66`

- 复制和删除现在合并为一次操作处理，而不是两次

- 现在支持 `--track-renames` 和 `--backup-dir`
- 在 `local`/`ftp`/`sftp` 上的部分上传已知问题已被解决
（除非使用 `--inplace`）
- 最终列表现在由同步结果生成，无需重新列出
- Bisync 现在对在运行过程中发生的变化更具韧性，
  出现关键错误/未检测到的变更的可能性大大降低
- Bisync 现在具备在不确定的情况下回滚文件列表的能力，
  本质上等同于将该文件标记为下次需要重新检查。
- 现在支持若干基本的终端颜色，可通过
[`--color`](/docs/#color) 控制（`AUTO`|`NEVER`|`ALWAYS`）
- Path1 和 Path2 的初始列表快照现在以并发方式生成，
  使用与 `check` 和 `sync` 相同的"march"基础设施，
  以提升性能并降低
[出错风险](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=4.%20Listings%20should%20alternate%20between%20paths%20to%20minimize%20errors)
- 修复了 Unicode 规范化和大小写不敏感的处理，支持
[`--fix-case`](/docs/#fix-case)、[`--ignore-case-sync`](/docs/#ignore-case-sync)、
[`--no-unicode-normalization`](/docs/#no-unicode-normalization)
- `--resync` 现在效率大幅提升（特别是对使用
`--create-empty-src-dirs` 的用户）
- Google Docs（以及其他大小未知的文件）现已受支持
（选项与 `sync` 相同）
- 同步冲突重命名前的相等性检查现在在 `check` 不可用时，
会回退到 `cryptcheck`（如果可能）或 `--download`，
而不是 `--size-only`。
- Bisync 不再因使用后端特定标志覆盖配置而找不到正确的列表文件
- Bisync 现在完全支持基于 size、modtime、checksum
任意组合的比较，取消了对不支持 modtime 的后端的限制
- Bisync 现在支持"优雅停机"模式，可在早期干净地取消一次运行，
而无需执行 `--resync`
- 新的 `--recover` 标志允许在中断情况下稳健恢复，
而无需执行 `--resync`
- 新的 `--max-lock` 设置允许锁文件自动续期和过期，
以便在运行被中断时实现更好的自动恢复
- Bisync 现在支持自动解决同步冲突以及通过
新的 [`--conflict-resolve`](#conflict-resolve)、
[`--conflict-loser`](#conflict-loser) 和
[`--conflict-suffix`](#conflict-suffix) 标志自定义重命名行为
- 新的 [`--resync-mode`](#resync-mode) 标志允许在
`--resync` 期间更精细地控制保留文件的哪一版本
- Bisync 现在支持 [`--retries`](/docs/#retries-int) 和
[`--retries-sleep`](/docs/#retries-sleep-time)
（当设置了 [`--resilient`](#resilient) 时）

### `v1.64`

- 修复了导致试运行（dry run）意外提交过滤规则变更的
[问题](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=1.%20Dry%20runs%20are%20not%20completely%20dry)

- 修复了导致 `--resync` 错误地删除空目录并复制 Path2 独有文件的
[问题](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=2.%20%2D%2Dresync%20deletes%20data%2C%20contrary%20to%20docs)
- `--check-access` 现在在 `--resync` 期间也会强制执行，
防止在
[某些用户误操作场景](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=%2D%2Dcheck%2Daccess%20doesn%27t%20always%20fail%20when%20it%20should) 中发生数据丢失
- 修复了因过滤规则过于宽泛，导致 bisync 在删除操作中
考虑过多文件的
[问题](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=5.%20Bisync%20reads%20files%20in%20excluded%20directories%20during%20delete%20operations)
- [改进了对假阳性变更冲突的检测](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=1.%20Identical%20files%20should%20be%20left%20alone%2C%20even%20if%20new%2Fnewer%2Fchanged%20on%20both%20sides)
（相同的文件现在保持不变，而不是被重命名）
- 新增
[对 `--create-empty-src-dirs` 的支持](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=3.%20Bisync%20should%20create%2Fdelete%20empty%20directories%20as%20sync%20does%2C%20when%20%2D%2Dcreate%2Dempty%2Dsrc%2Ddirs%20is%20passed)
- 新增实验性 `--resilient` 模式，以支持
[从可自我纠正的错误中恢复](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=2.%20Bisync%20should%20be%20more%20resilient%20to%20self-correctable%20errors)
- 新增
[新的 `--ignore-listing-checksum` 标志](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=6.%20%2D%2Dignore%2Dchecksum%20should%20be%20split%20into%20two%20flags%20for%20separate%20purposes)
以区分 `--ignore-checksum`
- 针对大型 remote 的
[性能改进](https://forum.rclone.org/t/bisync-bugs-and-feature-requests/37636#:~:text=6.%20Deletes%20take%20several%20times%20longer%20than%20copies)
- 文档和测试改进
