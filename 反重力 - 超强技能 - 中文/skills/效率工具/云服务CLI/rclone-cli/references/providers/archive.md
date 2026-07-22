---
title: "Archive"
description: "Archive 后端的 rclone 文档"
versionIntroduced: "v1.72"
---

> **官方文档:** [https://rclone.org/archive/](https://rclone.org/archive/)
# Archive

Archive 后端允许对云存储上的归档文件内容进行**只读**访问，无需下载完整的归档。这
意味着你可以挂载一个大型归档文件，仅使用其中你的应用所需的部分，而无需解压整个归档。

归档文件通过扩展名识别。

| 归档格式  | 扩展名 |
| -------- | --------- |
| Zip      | `.zip`    |
| Squashfs | `.sqfs`   |

所支持的归档文件类型都对云友好 - 可以找到并下载单个文件，而无需下载整个归档。

如果你只想创建、列出或解压归档，并不想挂载它们，那么 `rclone archive` 命令可能更加方便。

- [rclone archive create](/commands/rclone_archive_create/)
- [rclone archive list](/commands/rclone_archive_list/)
- [rclone archive extract](/commands/rclone_archive_extract/)

这些命令支持更广泛的不具备云友好特性的归档格式（但不支持 squashfs），但不能用于 `rclone mount`
或任何其他 rclone 命令（例如 `rclone check`）。

## 配置

此后端最好在不进行配置的情况下使用。

通过在另一个远程之前添加字符串 `:archive:` 来使用它，例如 `remote:dir` 变为
`:archive:remote:dir`。

`remote:dir` 中的任何归档都将变成目录，可以单独读取其中的文件。

例如

```
$ rclone lsf s3:rclone/dir
100files.sqfs
100files.zip
```

注意 `100files.zip` 和 `100files.sqfs` 现在变成了目录：

```
$ rclone lsf :archive:s3:rclone/dir
100files.sqfs/
100files.zip/
```

我们可以查看其内部：

```
$ rclone lsf :archive:s3:rclone/dir/100files.zip/
cofofiy5jun
gigi
hevupaz5z
kacak/
kozemof/
lamapaq4
qejahen
quhenen2rey
soboves8
vibat/
wose
xade
zilupot
```

不在归档中的文件可以正常读写。归档中的文件只能读取。

archive 后端也可以在配置文件中使用。使用 `remote` 变量指向归档的目标位置。

```
[remote]
type = archive
remote = s3:rclone/dir/100files.zip
```

将得到

```
$ rclone lsf remote:
cofofiy5jun
gigi
hevupaz5z
kacak/
...
```


## 修改时间

修改时间以依赖于归档类型的精度予以保留。

```
$ rclone lsl --max-depth 1 :archive:s3:rclone/dir/100files.zip
       12 2025-10-27 14:39:20.000000000 cofofiy5jun
       81 2025-10-27 14:39:20.000000000 gigi
       58 2025-10-27 14:39:20.000000000 hevupaz5z
        6 2025-10-27 14:39:20.000000000 lamapaq4
       43 2025-10-27 14:39:20.000000000 qejahen
       66 2025-10-27 14:39:20.000000000 quhenen2rey
       95 2025-10-27 14:39:20.000000000 soboves8
       71 2025-10-27 14:39:20.000000000 wose
       76 2025-10-27 14:39:20.000000000 xade
       15 2025-10-27 14:39:20.000000000 zilupot
```

对于 `zip` 和 `squashfs` 文件，该精度为 1 秒。

## 哈希

所支持的哈希类型取决于归档类型。Zip 文件使用 CRC32，Squashfs 不支持任何哈希。例如：

```
$ rclone hashsum crc32 :archive:s3:rclone/dir/100files.zip/
b2288554  cofofiy5jun
a87e62b6  wose
f90f630b  xade
c7d0ef29  gigi
f1c64740  soboves8
cb7b4a5d  quhenen2rey
5115242b  kozemof/fonaxo
afeabd9a  qejahen
71202402  kozemof/fijubey5di
bd99e512  kozemof/napux
...
```

从归档中读取文件时将校验哈希，并在可能的情况下作为同步的一部分使用。

```
$ rclone copy -vv :archive:s3:rclone/dir/100files.zip /tmp/100files
...
2025/10/27 14:56:44 DEBUG : kacak/turovat5c/yuyuquk: crc32 = abd05cc8 OK
2025/10/27 14:56:44 DEBUG : kacak/turovat5c/yuyuquk.aeb661dc.partial: renamed to: kacak/turovat5c/yuyuquk
2025/10/27 14:56:44 INFO  : kacak/turovat5c/yuyuquk: Copied (new)
...
```

## Zip

[Zip 文件格式](https://en.wikipedia.org/wiki/ZIP_(file_format))
是一种广泛使用的归档格式，将一个或多个文件和文件夹打包到单个文件中，主要用于
更便捷的存储或传输。它通常使用压缩（最常见的是 DEFLATE 算法）来减小归档内容的总体大小。
Zip 文件被大多数现代操作系统原生支持。

Rclone 不支持 Zip 文件的以下高级特性：

- 将大型归档拆分为较小的部分
- 密码保护
- Zstd 压缩

## Squashfs

Squashfs 是一种压缩的、只读的文件系统格式，主要用于基于 Linux 的系统。它被设计为
将整个文件系统（包括文件、目录和元数据）压缩到单个归档文件中，然后可以直接挂载和读取，
表现为普通的目录结构。由于其只读和高度压缩的特性，Squashfs 非常适合用于 Live CD/USB、
存储空间有限的嵌入式设备以及软件包分发，因为它节省空间并确保原始文件的完整性。

Rclone 支持以下 squashfs 压缩格式：

- `Gzip`
- `Lzma`
- `Xz`
- `Zstd`

以下格式暂未生效：

- `Lzo` - 暂不支持
- `Lz4` - 已损坏，提示 "error decompressing: lz4: bad magic number"

Rclone 在较大的 squashfs 块大小下运行速度最快。例如：

```
mksquashfs 100files 100files.sqfs -comp zstd -b 1M
```

## 限制

archive 后端的文件是只读的。目前还无法使用 archive 后端创建归档。但你可以使用 [rclone archive create](/commands/rclone_archive_create/) 创建归档。

仅支持 `.zip` 和 `.sqfs` 归档，因为它们是仅有的两种常见的归档格式，可以在不下载整个归档的情况下轻松读取其中的目录列表。

在内部，archive 后端使用 VFS 访问文件。目前还无法配置内部 VFS，这可能是有用的。

## 归档格式

下面是一个表格，对常见归档格式按其"云优化"程度进行评级，该评级基于它们能否
在无需读取整个归档的情况下访问单个文件。

此能力取决于该格式是否具有一个集中的 **索引**（或称"目录表"），
程序可以先读取它以找到特定文件的准确位置。

| 格式 | 扩展名 | 云优化 | 说明 |
| :--- | :--- | :--- | :--- |
| **ZIP** | `.zip` | **极佳** | **Zip 文件具有索引**（即"中央目录"），存储在文件的*末尾*。程序可以定位到末尾，读取索引以查找某个文件的位置和大小，然后直接定位到该文件的数据以解压它。 |
| **SquashFS** | `.squashfs`, `.sqfs`, `.sfs` | **极佳** | 这是一种压缩的只读*文件系统映像*，而不仅仅是归档。它**专为随机访问而设计**。它使用元数据和索引表，允许系统按需查找并解压单个文件或数据块。 |
| **ISO Image** | `.iso` | **极佳** | 与 SquashFS 类似，这是一种*文件系统映像*（用于光盘介质）。它包含一个文件系统（如 ISO 9660 或 UDF），**在已知位置具有目录表**，允许直接访问任何文件而无需读取整个光盘。 |
| **RAR** | `.rar` | **良好** | RAR 支持"非固实"和"固实"模式。在常见的**非固实**模式下，文件被单独压缩，索引允许轻松提取单个文件（与 ZIP 类似）。在"固实"模式下，该评级将是"非常差"。 |
| **7z** | `.7z` | **较差** | 默认情况下，7z 使用"固实"归档以最大化压缩率。它将文件作为一个连续的流进行压缩。要提取中间的文件，必须先解压其前面所有的文件。（如果显式创建为"非固实"，其评级将是"极佳"）。 |
| **tar** | `.tar` | **较差** | "Tape Archive"是一种*流式*格式，**没有中央索引**。要查找某个文件，必须从开头读取归档，逐个检查每个文件头直到找到所需的那个。速度较慢，但不需要解压数据。 |
| **Gzipped Tar** | `.tar.gz`, `.tgz` | **非常差** | 这是一个 `tar` 文件（已"较差"）以 `gzip` 压缩为**单个不可定位的流**。无法进行定位。要获取*任何*文件，必须从开头将*整个*归档解压到该文件为止。 |
| **Bzipped/XZ Tar** | `.tar.bz2`, `.tar.xz` | **非常差** | 原理与 `tar.gz` 相同。整个归档是一个大型压缩块，使随机访问变得不可能。 |

## 改进思路

可以较容易地添加 ISO 支持，因为我们使用的库（[go-diskfs](https://github.com/diskfs/go-diskfs/)）支持它。
我们也可以用同样的方式添加 `ext4` 和 `fat32`，但根据我的经验，这些格式作为文件并不常见，
因此可能不值得添加。Go-diskfs 还可以读取分区，这也许能加以利用。

可以添加写入支持，但这仅用于创建新归档，而非更新已有归档。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/archive/archive.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 archive（读取归档）专属的标准选项。

#### --archive-remote

要包装以读取归档的远程端。

通常应包含 ':' 和路径，例如 "myremote:path/to/dir"、
"myremote:bucket" 或 "myremote:"。

如果留空，则 archive 后端将以根作为远程端。

这意味着你可以使用 :archive:remote:path，它等价于设置 remote="remote:path"。


属性：

- Config:      remote
- Env Var:     RCLONE_ARCHIVE_REMOTE
- Type:        string
- Required:    false

### 高级选项

以下是 archive（读取归档）专属的高级选项。

#### --archive-description

远程端的描述。

属性：

- Config:      description
- Env Var:     RCLONE_ARCHIVE_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

任何底层远程所支持的元数据都会被读取和写入。

详见 [metadata](/docs/#metadata) 文档以获取更多信息。

<!-- autogenerated options stop -->
