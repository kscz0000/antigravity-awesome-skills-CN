---
title: "rclone serve nfs"
description: "通过 NFS 挂载方式提供远程访问"
status: Experimental
versionIntroduced: v1.65
# 自动生成 - 请勿编辑，如有修改请编辑 cmd/serve/nfs/ 中的源代码，并在发布时运行 "make commanddocs"
---

> **官方文档：** [https://rclone.org/commands/rclone_serve_nfs/](https://rclone.org/commands/rclone_serve_nfs/)
# rclone serve nfs

通过 NFS 挂载方式提供远程访问

## Synopsis

创建一个 NFS 服务器，通过网络提供指定的远程访问。

该命令实现了一个 NFSv3 服务器，可通过 NFS 提供任意 rclone 远程。

该命令的主要目的是在最新版 macOS 上启用 [mount
命令](/commands/rclone_mount/) on recent macOS versions where
installing FUSE is very cumbersome.

此服务器不实现任何身份认证，因此任何客户端都可以访问数据。若要限制访问，你可以在环回地址上使用 `serve nfs` on
环回地址，或者依赖安全隧道（如 SSH）进行连接，或者使用防火墙。

因此默认情况下，服务器会随机选择一个 TCP 端口，
并默认在环回接口上监听；
这意味着它仅对本地机器可用。若希望其他机器通过本地网络访问此 NFS 挂载，你需要使用 `--addr` 参数指定监听地址和端口。

通过 NFS 协议修改文件需要启用 VFS 缓存。Usually
通常你必须指定 `--vfs-cache-mode` 才能写入挂载点（推荐使用 `full`）。如果未指定 VFS 缓存模式，挂载将是只读的。

`--nfs-cache-type` 控制 NFS 句柄缓存的类型。By default this is `memory`，即按需随机分配新的句柄。这些句柄存储在内存中。如果服务器重启，句柄缓存将丢失，已连接的 NFS 客户端将收到过时的句柄错误。

`--nfs-cache-type disk` 使用磁盘上的 NFS 句柄缓存。Rclone
哈希对象的路径，并将结果存储在以哈希命名的文件中。These hashes are stored on disk the directory controlled by
`--cache-dir` or the exact directory may be specified with
`--nfs-cache-dir`. Using this means that the NFS server can be
restarted at will without affecting the connected clients.

`--nfs-cache-type symlink` 与 `--nfs-cache-type disk` 类似，也使用磁盘上的缓存，but the cache entries are held as
符号链接。Rclone 将底层文件的句柄用作 NFS 句柄，从而提升性能。这类缓存无法备份和恢复，as the underlying handles will change. This is Linux
only. It requires running rclone as root or with `CAP_DAC_READ_SEARCH`。
可以通过对 rclone 可执行文件执行 `sudo setcap cap_dac_read_search+ep /path/to/rclone` 来为其授予该权限。

`--nfs-cache-handle-limit` 控制缓存处理器保存的最大 NFS 句柄数。
此值不应设得过低，否则访问文件时可能会遇到错误。默认值为 `1000000`，但如果服务器的系统资源占用过高，可以考虑降低此上限。仅 `memory` 类型缓存使用此项。

若要在网络上提供 NFS 服务，可使用以下命令：

```sh
rclone serve nfs remote: --addr 0.0.0.0:$PORT --vfs-cache-mode=full
```

该命令指定一个可在 mount 命令中使用的端口。
在 Linux/macOS 上挂载该服务器，可使用以下命令：

```sh
mount -t nfs -o port=$PORT,mountport=$PORT,tcp $HOSTNAME:/ path/to/mountpoint
```

其中 `$PORT` 是 `serve nfs` 命令中使用的相同端口号，`$HOSTNAME` 是运行 `serve nfs` 的机器的网络地址。

如果启用了 `--vfs-metadata-extension`，那么对于 `--nfs-cache-type disk`
and `--nfs-cache-type cache` 元数据文件的文件句柄将以父文件句柄加 `0x00, 0x00, 0x00, 0x01` 作为后缀。
这意味着它们可以通过父文件句柄直接查找（如果需要）。

该命令仅在 Unix 平台上可用。

## VFS - 虚拟文件系统

此命令使用 VFS 层。This adapts the cloud storage objects
that rclone uses into something which looks much more like a disk
filing system.

云存储对象有许多与磁盘文件不同的属性——无法扩展它们，也无法在中间写入数据，所以 VFS 层必须处理这些问题。Because there is no one right way of
doing this there are various options explained below。

VFS 层还实现了目录缓存——它会缓存文件和目录的相关信息（但不缓存数据）到内存中。

## VFS 目录缓存

使用 `--dir-cache-time` 参数，可以控制目录被视为最新、无需从后端刷新的时长。
通过 VFS 所做的修改会立即生效，或使缓存失效。

```text
    --dir-cache-time duration   Time to cache directory entries for (default 5m0s)
    --poll-interval duration    Time to wait between polling for changes. Must be smaller than dir-cache-time. Only on supported remotes. Set to 0 to disable (default 1m0s)
```

但是，如果所配置的后端不支持变更轮询，however, changes made directly on the cloud storage by the web
interface or a different copy of rclone will only be picked up once
the directory cache expires if the backend configured does not support
polling for changes。如果后端支持轮询，则会在轮询间隔内发现这些修改。

你可以向 rclone 发送 `SIGHUP` 信号，让它刷新所有目录缓存，无论缓存有多旧。Assuming only one
rclone instance is running, you can reset the cache like this：

```console
kill -SIGHUP $(pidof rclone)
```

如果使用 [remote control](/rc) 配置 rclone，then you can use
rclone rc to flush the whole directory cache：

```console
rclone rc vfs/forget
```

或者针对单个文件或目录：

```console
rclone rc vfs/forget file=path/to/file dir=path/to/dir
```

## VFS 文件缓冲

`--buffer-size` 参数决定用于预读数据所使用的内存量，that will be used to buffer data in advance。

每个打开的文件都会尽量在内存中保持指定大小的数据。
缓冲数据绑定到单个打开的文件，不会被共享。

此参数是单个打开文件所占用内存的上限。The
buffer will only use memory for data that is downloaded but not not
yet read. If the buffer is empty, only a small amount of memory will
be used.

rclone 用于缓冲的最大内存可达到
`--buffer-size * open files`。

## VFS 文件缓存

以下参数控制 VFS 文件缓存选项。File caching is
necessary to make the VFS layer appear compatible with a normal file
system. It can be disabled at the cost of some compatibility.

例如，如果你希望同时读写一个文件，就需要启用 VFS 缓存。See below for more details。

请注意，VFS 缓存与 cache 后端是相互独立的，你可能需要其中之一或两者同时使用。

```text
    --cache-dir string                     Directory rclone will use for caching.
    --vfs-cache-mode CacheMode             Cache mode off|minimal|writes|full (default off)
    --vfs-cache-max-age duration           Max time since last access of objects in the cache (default 1h0m0s)
    --vfs-cache-max-size SizeSuffix        Max total size of objects in the cache (default off)
    --vfs-cache-min-free-space SizeSuffix  Target minimum free space on the disk containing the cache (default off)
    --vfs-cache-poll-interval duration     Interval to poll the cache for stale objects (default 1m0s)
    --vfs-write-back duration              Time to writeback files after last use when using cache (default 5s)
```

如果使用 `-vv` 运行 rclone，它将输出文件缓存的位置。The
files are stored in the user cache file area which is OS dependent but
can be controlled with `--cache-dir` or setting the appropriate
environment variable.

缓存有 4 种不同的模式，可通过 `--vfs-cache-mode` 选择。
The higher the cache mode the more compatible rclone becomes at the
cost of using disk space.

请注意，只有当文件被关闭且在 `--vfs-write-back`
秒内未被访问时，文件才会被写回远程。If rclone is quit or dies with files that haven't been
uploaded, these will be uploaded next time rclone is run with the same
flags.

如果使用了 `--vfs-cache-max-size` 或 `--vfs-cache-min-free-space`，请注意缓存可能会超出这些配额，原因有二。Firstly
because it is only checked every `--vfs-cache-poll-interval`. Secondly
because open files cannot be evicted from the cache. When
`--vfs-cache-max-size` 或 `--vfs-cache-min-free-space` 超出时，
rclone 会首先尝试从缓存中逐出访问最少的文件。rclone will start with files that haven't been accessed for the
longest. This cache flushing strategy is efficient and more relevant
files are likely to remain cached.

`--vfs-cache-max-age` 会在距离上次访问时间超过设定值后，将文件从缓存中逐出。
默认值 1 小时会从缓存中逐出超过 1 小时未被访问的文件。When a cached file is accessed the 1 hour timer is reset to 0
and will wait for 1 more hour before evicting. Specify the time with
standard notation, s, m, h, d, w .

如果使用了 `--vfs-cache-mode > off`，**不应**同时使用相同或重叠的远程运行两份 rclone。
This can potentially cause data corruption if you do. You can work
around this by giving each rclone its own cache hierarchy with
`--cache-dir`. 如果使用的远程之间没有重叠，则无需担心。

### --vfs-cache-mode off

在此模式（默认模式）下，缓存将直接从远程读取，并直接写入远程，不在磁盘上缓存任何内容。

这意味着某些操作将无法执行

- 无法同时以读和写方式打开文件
- 以写方式打开的文件无法进行 seek 操作
- 以写方式打开的已存在文件必须设置 O_TRUNC
- 以 O_TRUNC 打开的只读文件将被以只写方式打开
- 以只写方式打开的文件，其行为等同于提供了 O_TRUNC
- 打开模式 O_APPEND、O_TRUNC 将被忽略
- 上传失败时无法重试

### --vfs-cache-mode minimal

此模式与 "off" 非常相似，区别在于会以读和写方式打开的文件将被缓冲到磁盘上。This means that files opened for
write will be a lot more compatible, but uses the minimal disk space.

这些操作无法执行

- 以只写方式打开的文件无法进行 seek 操作
- 以写方式打开的已存在文件必须设置 O_TRUNC
- 以只写方式打开的文件将忽略 O_APPEND、O_TRUNC
- 上传失败时无法重试

### --vfs-cache-mode writes

在此模式下，以只读方式打开的文件仍然直接从远程读取，write only and read/write files are buffered to disk
first。

此模式应支持所有常规的文件系统操作。

如果上传失败，将以指数递增的间隔进行重试，最长 1 分钟。

### --vfs-cache-mode full

在此模式下，所有读取和写入都会缓冲到磁盘，然后再与磁盘交互。When
data is read from the remote this is buffered to disk as well.

在此模式下，缓存中的文件将是稀疏文件，rclone 会跟踪已下载的文件部分。

所以，如果某个应用程序仅读取每个文件的开头部分，那么 rclone 将只会缓冲文件的开头部分。These files will appear to be
their full size in the cache, but they will be sparse files with only
the data that has been downloaded present in them.

此模式应支持所有常规的文件系统操作，其他方面与 `--vfs-cache-mode` writes 相同。

读取文件时，rclone 将预读 `--buffer-size` 加上
`--vfs-read-ahead` 字节。The `--buffer-size` is buffered in memory
whereas the `--vfs-read-ahead` is buffered on disk.

使用此模式时，建议 `--buffer-size` 不要设得过大，而 `--vfs-read-ahead` 可根据需要设置得较大。

**重要提示** 并非所有文件系统都支持稀疏文件。In particular
FAT/exFAT do not. Rclone will perform very badly if the cache
directory is on a filesystem which doesn't support sparse files and it
will log an ERROR message if one is detected.

### 指纹识别

VFS 的各个部分使用指纹识别来判断本地文件副本相较于远程文件是否已更改。Fingerprints are made
from：

- size
- modification time
- hash

凡对象上可用的属性。

在某些后端上，部分属性读取较慢（每个对象需要额外的 API 调用或额外的工作）。

例如，`local` 和 `sftp` 后端的 `hash` 较慢，
因为它们必须读取整个文件并进行哈希运算；而 `s3`、`swift`、`ftp` 和 `qinqstor` 后端的 `modtime` 较慢，
because they
need to do an extra API call to fetch it。

如果使用 `--vfs-fast-fingerprint` 参数，rclone 将不会把那些耗时的操作纳入指纹计算。This makes the
fingerprinting less accurate but much faster and will improve the
opening time of cached files.

如果对 `local`、`s3` 或 `swift` 后端运行 vfs 缓存，建议启用此参数。

请注意，如果更改此参数的值，缓存中的文件指纹可能会失效，需要重新下载文件。

## VFS 分块读取

当 rclone 从远程读取文件时，会按块读取。This
means that rather than requesting the whole file rclone reads the
chunk specified. This can reduce the used download quota for some
remotes by requesting only chunks from the remote that are actually
read, at the cost of an increased number of requests.

以下参数控制分块行为：

```text
    --vfs-read-chunk-size SizeSuffix        Read the source objects in chunks (default 128M)
    --vfs-read-chunk-size-limit SizeSuffix  Max chunk doubling size (default off)
    --vfs-read-chunk-streams int            The number of parallel streams to read at once
```

分块的行为因 `--vfs-read-chunk-streams` 参数而异。

### `--vfs-read-chunk-streams` == 0

Rclone 将以 `--vfs-read-chunk-size` 大小开始读取一个块，
然后在每次读取后翻倍。When `--vfs-read-chunk-size-limit` is
specified, and greater than `--vfs-read-chunk-size`, the chunk size for each
open file will get doubled only until the specified value is reached. If the
value is "off"，即默认值，限制被禁用，块大小
将无限增长。

例如，使用 `--vfs-read-chunk-size 100M` 和 `--vfs-read-chunk-size-limit 0`
时，将依次下载以下部分：0-100M、100M-200M、200M-300M、300M-400M，以此类推。When `--vfs-read-chunk-size-limit 500M` is specified, the result would
be 0-100M, 100M-300M, 300M-700M, 700M-1200M, 1200M-1700M and so on.

将 `--vfs-read-chunk-size` 设为 `0` 或 "off" 将禁用分块读取。

块不会被缓存在内存中。

### `--vfs-read-chunk-streams` > 0

Rclone 会并发读取 `--vfs-read-chunk-streams` chunks of size
`--vfs-read-chunk-size` 块。每次读取的大小保持不变。

这在高延迟链路或对高性能对象存储使用高带宽链路时，
显著提升性能。

需要通过反复试验来找到 `--vfs-read-chunk-size` 和 `--vfs-read-chunk-streams` 的最优值，as these will
depend on the backend in use and the latency to the backend。

对于高性能对象存储（例如 AWS S3），一个合理的起点是
`--vfs-read-chunk-streams 16` 和
`--vfs-read-chunk-size 4M`. In testing with AWS S3 the performance
scaled roughly as the `--vfs-read-chunk-streams` setting.

类似的设置也适用于高延迟链路，but depending on
the latency they may need more `--vfs-read-chunk-streams` in order to
get the throughput.

## VFS 性能

以下参数可用于启用或禁用 VFS 的某些功能，以提升性能或其他目的。See also the [chunked reading](#vfs-chunked-reading)
feature.

特别是 S3 和 Swift 可从 `--no-modtime` 参数（或使用 `--use-server-modtime` 以获得略有不同的效果）中获益匪浅，as each
read of the modification time takes a transaction.

```text
    --no-checksum     Don't compare checksums on up/download.
    --no-modtime      Don't read/write the modification time (can speed things up).
    --no-seek         Don't allow seeking in files.
    --read-only       Only allow read-only access.
```

有时 rclone 收到的读取或写入是乱序的。Rather
than seeking rclone will wait a short time for the in sequence read or
write to come in. These flags only come into effect when not using an
on disk cache file.

```text
    --vfs-read-wait duration   Time to wait for in-sequence read before seeking (default 20ms)
    --vfs-write-wait duration  Time to wait for in-sequence write before giving error (default 1s)
```

当使用 VFS 写入缓存（`--vfs-cache-mode` 值为 writes 或 full）时，
the global flag `--transfers` can be set to adjust the number of parallel uploads
of modified files from the cache (the related global flag `--checkers` has no
effect on the VFS)。

```text
    --transfers int  Number of file transfers to run in parallel (default 4)
```

## 符号链接

默认情况下，VFS 不支持符号链接。However this may be
enabled with either of the following flags：

```text
    --links      Translate symlinks to/from regular files with a '.rclonelink' extension.
    --vfs-links  Translate symlinks to/from regular files with a '.rclonelink' extension for the VFS
```

由于大多数云存储系统都不直接支持符号链接，rclone
将符号链接存储为带有特殊扩展名的普通文件。So a
file which appears as a symlink `link-to-file.txt` would be stored on
cloud storage as `link-to-file.txt.rclonelink` and the contents would
be the path to the symlink destination.

请注意，`--links` 会在 rclone 中全局启用符号链接转换——this includes any backend which supports the concept (for example the
local backend). `--vfs-links` just enables it for the VFS layer。

此方案与通过 [`--local-links` 参数的 local 后端](/local/#symlinks-junction-points)所使用的方案兼容。

`--vfs-links` 参数专为 `rclone mount`、`rclone
nfsmount` 和 `rclone serve nfs` 设计。

尚未对其他 `rclone serve` 命令进行过测试。

当前实现的一个限制是，它要求调用者自行解析子符号链接。For example given this directory tree

```text
.
├── dir
│   └── file.txt
└── linked-dir -> dir
```

VFS 可以正确解析 `linked-dir`，但无法解析
`linked-dir/file.txt`。This is not a problem for the tested commands
but may be for other commands.

**请注意**，符号链接支持存在一个未解决的问题
[issue #8245](https://github.com/rclone/rclone/issues/8245)：with duplicate
files being created when symlinks are moved into directories where
there is a file of the same name (or vice versa)。

## VFS 大小写敏感性

Linux 文件系统区分大小写：two files can differ only
by case, and the exact case must be used when opening a file。

现代 Windows 上的文件系统不区分大小写但保留大小写：although existing files can be opened using any case, the exact case used
to create the file is preserved and available for programs to query。
It is not allowed for two files in the same directory to differ only by case。

通常，macOS 上的文件系统不区分大小写。It is possible to make macOS
file systems case-sensitive but that is not the default。

`--vfs-case-insensitive` VFS 参数控制 rclone 如何处理这些
两种情况。If its value is "false", rclone passes file names to the remote
as-is. If the flag is "true"（或在命令行中不带值出现），rclone may perform a "fixup" as explained below。

用户可以使用与远程存储的文件名大小写不同的大小写来指定要打开/删除/重命名等的文件名。If an argument refers
to an existing file with exactly the same name, then the case of the existing
file on the disk will be used. However, if a file name with exactly the same
name is not found but a name differing only by case exists, rclone will
transparently fixup the name. This fixup happens only when an existing file
is requested. Case sensitivity of file names created anew by rclone is
controlled by the underlying remote.

请注意，运行 rclone 的操作系统（目标）的大小写敏感性
may differ from case sensitivity of a file system presented by rclone (the source)。
The flag controls whether "fixup" is performed to satisfy the target。

如果未在命令行中提供该参数，then its default value depends
on the operating system where rclone runs: "true" on Windows and macOS, "false"
otherwise。如果提供该参数时不带值，则为 "true"。

`--no-unicode-normalization` 参数控制是否对名称不同但通过 Unicode 规范化后[规范化等效](https://en.wikipedia.org/wiki/Unicode_equivalence)的文件名执行类似的 "fixup"。Unicode normalization can be particularly helpful for users of macOS,
which prefers form NFD instead of the NFC used by most other platforms. It is
therefore highly recommended to keep the default of `false` on macOS, to avoid
encoding compatibility issues.

在（可能不太常见的）情况下，if a directory has multiple duplicate
filenames after applying case and unicode normalization, the `--vfs-block-norm-dupes`
flag allows hiding these duplicates. This comes with a performance tradeoff, as
rclone will have to scan the entire directory for duplicates when listing a
directory. For this reason, it is recommended to leave this disabled if not
needed. However, macOS users may wish to consider using it, as otherwise, if a
remote directory contains both NFC and NFD versions of the same filename, an odd
situation will occur: both versions of the file will be visible in the mount,
and both will appear to be editable, however, editing either version will
actually result in only the NFD version getting edited under the hood. `--vfs-block-
norm-dupes` prevents this confusion by detecting this scenario, hiding the
duplicates, and logging an error, similar to how this is handled in `rclone
sync`.

## VFS 磁盘选项

此参数允许你手动设置文件系统的统计信息。It can be useful when those statistics cannot be read correctly automatically。

```text
    --vfs-disk-space-total-size    Manually set the total disk space size (example: 256G, default: -1)
```

## 已用字节数的替代报告

某些后端（尤其是 S3）不会报告已用的字节数。If you need this information to be available when running `df` on the
filesystem, then pass the flag `--vfs-used-is-size` to rclone。
With this flag set, instead of relying on the backend to report this
information, rclone will scan the whole remote similar to `rclone size`
and compute the total used space itself.

**警告**：Contrary to `rclone size`, this flag ignores filters so that the
result is accurate. However, this is very inefficient and may cost lots of API
calls resulting in extra charges. Use it as a last resort and only with caching。

## VFS 元数据

如果使用 `--vfs-metadata-extension` 参数，可以让 VFS to
expose files which contain the [metadata](/docs/#metadata) as a JSON
blob. These files will not appear in the directory listing, but can be
`stat`-ed and opened and once they have been they **will** appear in
directory listings until the directory cache expires.

请注意，某些后端只有在传入 `--metadata` 参数时才会创建元数据。

例如，使用 `rclone mount` 并配合 `--metadata --vfs-metadata-extension .metadata`，
we get

```console
$ ls -l /mnt/
total 1048577
-rw-rw-r-- 1 user user 1073741824 Mar  3 16:03 1G

$ cat /mnt/1G.metadata
{
        "atime": "2025-03-04T17:34:22.317069787Z",
        "btime": "2025-03-03T16:03:37.708253808Z",
        "gid": "1000",
        "mode": "100664",
        "mtime": "2025-03-03T16:03:39.640238323Z",
        "uid": "1000"
}

$ ls -l /mnt/
total 1048578
-rw-rw-r-- 1 user user 1073741824 Mar  3 16:03 1G
-rw-rw-r-- 1 user user        185 Mar  3 16:03 1G.metadata
```

如果文件没有元数据，it will be returned as `{}` and if there
is an error reading the metadata the error will be returned as
`{"error":"error string"}`。

```
rclone serve nfs remote:path [flags]
```

## Options

```
      --addr string                            IPaddress:Port or :Port to bind server to
      --dir-cache-time Duration                Time to cache directory entries for (default 5m0s)
      --dir-perms FileMode                     Directory permissions (default 777)
      --file-perms FileMode                    File permissions (default 666)
      --gid uint32                             Override the gid field set by the filesystem (not supported on Windows) (default 1000)
  -h, --help                                   help for nfs
      --link-perms FileMode                    Link permissions (default 666)
      --nfs-cache-dir string                   The directory the NFS handle cache will use if set
      --nfs-cache-handle-limit int             max file handles cached simultaneously (min 5) (default 1000000)
      --nfs-cache-type memory|disk|symlink     Type of NFS handle cache to use (default memory)
      --no-checksum                            Don't compare checksums on up/download
      --no-modtime                             Don't read/write the modification time (can speed things up)
      --no-seek                                Don't allow seeking in files
      --poll-interval Duration                 Time to wait between polling for changes, must be smaller than dir-cache-time and only on supported remotes (set 0 to disable) (default 1m0s)
      --read-only                              Only allow read-only access
      --uid uint32                             Override the uid field set by the filesystem (not supported on Windows) (default 1000)
      --umask FileMode                         Override the permission bits set by the filesystem (not supported on Windows) (default 002)
      --vfs-block-norm-dupes                   If duplicate filenames exist in the same directory (after normalization), log an error and hide the duplicates (may have a performance cost)
      --vfs-cache-max-age Duration             Max time since last access of objects in the cache (default 1h0m0s)
      --vfs-cache-max-size SizeSuffix          Max total size of objects in the cache (default off)
      --vfs-cache-min-free-space SizeSuffix    Target minimum free space on the disk containing the cache (default off)
      --vfs-cache-mode CacheMode               Cache mode off|minimal|writes|full (default off)
      --vfs-cache-poll-interval Duration       Interval to poll the cache for stale objects (default 1m0s)
      --vfs-case-insensitive                   If a file name not found, find a case insensitive match
      --vfs-disk-space-total-size SizeSuffix   Specify the total space of disk (default off)
      --vfs-fast-fingerprint                   Use fast (less accurate) fingerprints for change detection
      --vfs-links                              Translate symlinks to/from regular files with a '.rclonelink' extension for the VFS
      --vfs-metadata-extension string          Set the extension to read metadata from
      --vfs-read-ahead SizeSuffix              Extra read ahead over --buffer-size when using cache-mode full
      --vfs-read-chunk-size SizeSuffix         Read the source objects in chunks (default 128Mi)
      --vfs-read-chunk-size-limit SizeSuffix   If greater than --vfs-read-chunk-size, double the chunk size after each chunk read, until the limit is reached ('off' is unlimited) (default off)
      --vfs-read-chunk-streams int             The number of parallel streams to read at once
      --vfs-read-wait Duration                 Time to wait for in-sequence read before seeking (default 20ms)
      --vfs-refresh                            Refreshes the directory cache recursively in the background on start
      --vfs-used-is-size rclone size           Use the rclone size algorithm for Used size
      --vfs-write-back Duration                Time to writeback files after last use when using cache (default 5s)
      --vfs-write-wait Duration                Time to wait for in-sequence write before giving error (default 1s)
```

与其他命令共享的 options 见下文。
未在此列出的全局 options 请参阅 [global flags page](/flags/)。

### Filter Options

用于过滤目录列表的 flag

```text
      --delete-excluded                     Delete files on dest excluded from sync
      --exclude stringArray                 Exclude files matching pattern
      --exclude-from stringArray            Read file exclude patterns from file (use - to read from stdin)
      --exclude-if-present stringArray      Exclude directories if filename is present
      --files-from stringArray              Read list of source-file names from file (use - to read from stdin)
      --files-from-raw stringArray          Read list of source-file names from file without any processing of lines (use - to read from stdin)
  -f, --filter stringArray                  Add a file filtering rule
      --filter-from stringArray             Read file filtering patterns from a file (use - to read from stdin)
      --hash-filter string                  Partition filenames by hash k/n or randomly @/n
      --ignore-case                         Ignore case in filters (case insensitive)
      --include stringArray                 Include files matching pattern
      --include-from stringArray            Read file include patterns from file (use - to read from stdin)
      --max-age Duration                    Only transfer files younger than this in s or suffix ms|s|m|h|d|w|M|y (default off)
      --max-depth int                       If set limits the recursion depth to this (default -1)
      --max-size SizeSuffix                 Only transfer files smaller than this in KiB or suffix B|K|M|G|T|P (default off)
      --metadata-exclude stringArray        Exclude metadatas matching pattern
      --metadata-exclude-from stringArray   Read metadata exclude patterns from file (use - to read from stdin)
      --metadata-filter stringArray         Add a metadata filtering rule
      --metadata-filter-from stringArray    Read metadata filtering patterns from a file (use - to read from stdin)
      --metadata-include stringArray        Include metadatas matching pattern
      --metadata-include-from stringArray   Read metadata include patterns from file (use - to read from stdin)
      --min-age Duration                    Only transfer files older than this in s or suffix ms|s|m|h|d|w|M|y (default off)
      --min-size SizeSuffix                 Only transfer files bigger than this in KiB or suffix B|K|M|G|T|P (default off)
```

## See Also

<!-- markdownlint-capture -->
<!-- markdownlint-disable ul-style line-length -->

* [rclone serve](/commands/rclone_serve/)	 - Serve a remote over a protocol.


<!-- markdownlint-restore -->
