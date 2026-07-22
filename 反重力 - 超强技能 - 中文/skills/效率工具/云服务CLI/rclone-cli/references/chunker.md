---
title: "Chunker"
description: "分块覆盖远程"
versionIntroduced: "v1.50"
---

> **官方文档：** [https://rclone.org/chunker/](https://rclone.org/chunker/)
# Chunker

`chunker` 覆盖层在上传到被包裹远程时透明地将大文件拆分为较小的数据块，
在下载时又透明地将其重新组装。这可以有效地克服存储提供商施加的大小限制。

## 配置

要使用此功能，首先按照对应远程的配置说明设置底层远程。
你也可以使用本地路径名代替远程。

首先检查你选择的远程是否正常工作——我们在此将其称为 `remote:path`。
注意，`remote:path` 内部的所有内容都会被分块，外部的则不会。
这意味着如果你使用基于存储桶的远程（如 S3、B2、swift），
则可能应将存储桶放入远程 `s3:bucket` 中。

现在使用 `rclone config` 配置 `chunker`。我们将此配置称为 `overlay`，
以将其与 `remote` 本身区分开。

```text
No remotes found, make a new one\?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> overlay
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / Transparently chunk/split large files
   \ "chunker"
[snip]
Storage> chunker
Remote to chunk/unchunk.
Normally should contain a ':' and a path, e.g. "myremote:path/to/dir",
"myremote:bucket" or maybe "myremote:" (not recommended).
Enter a string value. Press Enter for the default ("").
remote> remote:path
Files larger than chunk size will be split in chunks.
Enter a size with suffix K,M,G,T. Press Enter for the default ("2G").
chunk_size> 100M
Choose how chunker handles hash sums. All modes but "none" require metadata.
Enter a string value. Press Enter for the default ("md5").
Choose a number from below, or type in your own value
 1 / Pass any hash supported by wrapped remote for non-chunked files, return nothing otherwise
   \ "none"
 2 / MD5 for composite files
   \ "md5"
 3 / SHA1 for composite files
   \ "sha1"
 4 / MD5 for all files
   \ "md5all"
 5 / SHA1 for all files
   \ "sha1all"
 6 / Copying a file to chunker will request MD5 from the source falling back to SHA1 if unsupported
   \ "md5quick"
 7 / Similar to "md5quick" but prefers SHA1 over MD5
   \ "sha1quick"
hash_type> md5
Edit advanced config? (y/n)
y) Yes
n) No
y/n> n
Remote config
--------------------
[overlay]
type = chunker
remote = remote:bucket
chunk_size = 100M
hash_type = md5
--------------------
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

### 指定远程

在正常使用中，请确保远程中包含 `:`。如果你指定的远程不含 `:`，
rclone 将使用该名称的本地目录。因此，如果你使用远程 `/path/to/secret/files`，
rclone 将在该目录中进行分块。如果你使用远程 `name`，
rclone 将把文件放在当前目录下名为 `name` 的目录中。

### 分块

当 rclone 开始上传文件时，chunker 会检查文件大小。如果不超过配置的分块大小，
chunker 会直接将文件传递给被包裹的远程（但请参见下方的注意事项）。
如果文件很大，chunker 会透明地按临时名称切割数据并逐个流式传输。
每个数据块将包含指定数量的字节，最后一个块可能数据较少。
如果事先不知道文件大小（即流式上传），chunker 将在内部创建临时副本，
记录其大小，然后重复上述过程。

上传完成后，临时分块文件最终会被重命名。此方案保证操作可以并行运行，
且从外部看来是原子的。其他操作（复制/移动/重命名等）也使用类似的隐藏临时分块方法。
如果操作失败，隐藏的分块通常会被销毁，目标组合文件保持完整。

当请求下载组合文件时，chunker 通过按顺序拼接数据块来透明地组装它。
由于拆分是简单的操作，甚至可以手动拼接数据块来获取原始内容。

当 `list` rclone 命令扫描被包裹远程上的目录时，潜在的分块文件会被识别、
分组并组装成组合目录条目。任何临时分块都会被隐藏。

List 和其他命令有时会遇到具有缺失或无效分块的组合文件，
例如被同名目录或其他文件遮蔽。这通常意味着被包裹的文件系统被直接篡改或损坏。
如果 chunker 检测到缺失的分块，默认会打印警告，跳过整个不完整的分块组，
但继续执行当前命令。你可以设置 `--chunker-fail-hard` 标志，
使命令在此类情况下中止并输出错误信息。

**注意事项**：目前，即使文件低于分块阈值，chunker 也总是会在后端创建临时文件然后重命名它。
这会导致不必要的 API 调用，在某些后端（如 Box）处理主要由小文件组成的传输时，
可能会严重限制吞吐量。解决此问题的方法是，通过 `--min-size` 仅对超过分块阈值的文件使用 chunker，
然后对剩余文件单独执行不使用 chunker 的调用。

#### 分块名称

默认的分块名称格式为 `*.rclone_chunk.###`，因此默认情况下分块名称为
`BIG_FILE_NAME.rclone_chunk.001`、`BIG_FILE_NAME.rclone_chunk.002` 等。
你可以使用 `name_format` 配置文件选项配置其他名称格式。
格式中使用星号 `*` 作为基础文件名的占位符，
使用一个或多个连续的井号 `#` 作为顺序分块编号的占位符。
必须有且仅有一个星号。连续井号的数量定义了表示分块编号字符串的最小长度。
如果十进制分块编号的位数少于井号数量，则用零左填充。
如果十进制字符串更长，则保持不变。默认编号从 1 开始，
但也有另一个选项允许用户从 0 开始，例如为了与旧版软件兼容。

例如，如果名称格式为 `big_*-##.part`，原始文件名为 `data.txt`，
编号从 0 开始，则第一个分块将被命名为 `big_data.txt-00.part`，
第 99 个分块为 `big_data.txt-98.part`，第 302 个分块为 `big_data.txt-301.part`。

注意，`list` 仅在分块名称匹配配置格式时才组装组合目录条目，
将不符合格式的文件名视为普通的非分块文件。

使用 `norename` 事务时，分块名称还会附加唯一的文件版本后缀。
例如，`BIG_FILE_NAME.rclone_chunk.001_bp562k`。

### 元数据

除数据分块外，chunker 默认还会为组合文件创建元数据对象。
该对象以原始文件名命名。Chunker 允许用户完全禁用元数据（`none` 格式）。
注意，通常不会为小于配置分块大小的文件创建元数据。
这可能在未来的 rclone 版本中改变。

#### 简单 JSON 元数据格式

这是默认格式。它支持组合文件的哈希校验和与分块验证。
元数据对象包含以下字段：

- `ver`     - 格式版本，当前为 `1`
- `size`    - 组合文件的总大小
- `nchunks` - 文件中数据分块的数量
- `md5`     - 组合文件的 MD5 哈希值（如果存在）
- `sha1`    - SHA1 哈希值（如果存在）
- `txn`     - 标识当前文件版本

没有组合文件名字段，因为它简单地等于被包裹远程上元数据对象的名称。
有关哈希值和修改时间处理的详细信息，请参阅相应章节。

#### 无元数据

你可以通过将元数据格式选项设为 `none` 来禁用元数据对象。
在此模式下，chunker 将扫描目录中所有符合配置的分块名称格式的文件，
通过检测具有相同基础名称的分块来分组，并将组名显示为虚拟组合文件。
此方法比启用元数据的格式更容易出现缺失分块错误（尤其是缺失最后一个分块）。

### 哈希校验和

Chunker 仅在存在兼容元数据时支持哈希校验和。因此，如果你选择元数据格式为 `none`，
chunker 将报告哈希值为 `UNSUPPORTED`。

请注意，默认情况下元数据仅存储组合文件。如果文件小于配置的分块大小，
chunker 会透明地将哈希请求重定向到被包裹的远程，因此支持取决于该远程。
如果被包裹的远程不支持请求的哈希类型，你将看到小文件的哈希值为空字符串。

许多存储后端支持 MD5 和 SHA1 哈希类型，chunker 也一样。
使用 chunker 时你可以选择其一，但不能同时选择两者。
MD5 默认设置为最受支持的类型。由于 chunker 为组合文件保留哈希值，
并为非分块文件回退到被包裹远程的哈希，我们建议你选择与被包裹远程相同的哈希类型，
以便文件列表看起来一致。

如果你的存储后端不支持 MD5 或 SHA1 但需要一致的文件哈希，
请使用 `md5all` 或 `sha1all` 配置 chunker。这两种模式保证所有文件都具有指定的哈希。
如果被包裹的远程不支持，chunker 将为所有文件（包括小文件）添加元数据。
然而，这会使存储中小文件数量翻倍，并产生额外的服务费用。
你甚至可以使用 chunker 在任何其他远程上强制 md5/sha1 支持，
代价是伴随的元数据对象——设置例如 `hash_type=sha1all` 强制哈希校验和，
`chunk_size=1P` 有效禁用分块。

通常，当文件被复制到 chunker 控制的远程时，chunker 会向文件源请求兼容的文件哈希，
如果未找到则回退到即时计算。这会带来一些 CPU 开销，但保证指定的哈希值可用。
此外，如果源和目标的哈希类型不同，chunker 将拒绝服务端复制或移动操作，
这也意味着额外的网络带宽。在少数情况下这可能是不希望的，
因此 chunker 提供两个可选模式：`sha1quick` 和 `md5quick`。
如果源不支持主要哈希类型且启用了快速模式，chunker 将尝试回退到次要类型。
这会节省 CPU 和带宽，但可能导致目标处的哈希值为空。
请注意后果：如果源和目标之间未找到兼容的哈希值，`sync` 命令将回退
（有时是静默地）到时间/大小比较。

### 修改时间

Chunker 使用被包裹远程存储修改时间，因此支持取决于该远程。
对于小的非分块文件，chunker 覆盖层直接操作被包裹远程文件的修改时间。
对于带元数据的组合文件，chunker 将获取和设置被包裹远程上元数据对象的修改时间。
如果文件被分块但元数据格式为 `none`，则 chunker 将使用第一个数据分块的修改时间。

### 迁移

迁移到不同分块大小、哈希类型、事务风格或分块命名方案的惯用方法是：

- 将所有分块文件收集到一个目录下，并让你的 chunker 远程指向它。
- 创建另一个目录（最可能在同一云存储上），
  并使用所需的元数据格式、哈希类型、分块命名等配置新远程。
- 现在运行 `rclone sync --interactive oldchunks: newchunks:`，
  所有数据将在传输中透明转换。
  这可能需要一些时间，但 chunker 会尽可能尝试服务端复制。
- 检查数据完整性后，你可以删除旧远程的配置节。

如果 rclone 在对大型组合文件执行长时间操作时被终止，
隐藏的临时分块可能会留在目录中。`list` 命令不会显示它们，但它们会占用你的账户配额。
请注意，`deletefile` 命令仅删除文件的活跃分块。
作为变通方法，你可以使用被包裹文件系统的远程来查看它们。
清除隐藏垃圾的一种简单方法是使用 chunker 远程将散落目录复制到别处，
然后清除原始目录。`copy` 命令仅复制活跃分块，而 `purge` 将删除包括垃圾在内的所有内容。

### 注意事项与限制

Chunker 要求被包裹远程支持服务端 `move`（或 `copy` + `delete`）操作，
否则将明确拒绝启动。这是因为它在操作成功完成时需要在内部将临时分块文件重命名为最终名称。

Chunker 在文件名中编码分块编号，因此使用默认 `name_format` 设置时会增加 17 个字符。
此外，chunker 在操作期间还会添加 7 个字符的临时后缀。
许多文件系统将不含路径的基础文件名限制为 255 个字符。
使用 rclone 的 crypt 远程作为基础文件系统会将文件名限制为 143 个字符。
因此，大多数文件的最大名称长度为 231，chunker-over-crypt 为 119。
有需要的用户可以将名称格式改为例如 `*.rcc##`，节省 10 个字符
（前提是每个文件最多 99 个分块）。

注意，使用复制加删除方法实现的移动操作可能会在某些云存储提供商处产生双重计费。

当你在活跃远程上运行 `rclone config` 并更改分块名称格式时，
chunker 不会自动重命名现有分块。请注意，这可能导致一些在更改前被视为分块的文件
在目录列表中显示为普通文件，反之亦然。同样的警告也适用于分块大小。
如果你迫切需要更改关键分块设置，应按照上述方法运行数据迁移。

如果被包裹远程不区分大小写，chunker 覆盖层将继承该属性
（因此你不能在同一目录中拥有名为 "Hello.doc" 和 "hello.doc" 的文件）。

rclone 版本直至 `v1.54` 中包含的 chunker 有时无法检测较新版本 rclone 生成的元数据。
我们建议用户保持 rclone 为最新版本以避免数据损坏。

更改 `transactions` 是危险操作，需要显式迁移。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/chunker/chunker.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 chunker（透明分块/拆分大文件）的特定标准选项。

#### --chunker-remote

要进行分块/反分块的远程。

通常应包含 `:` 和路径，例如 "myremote:path/to/dir"、"myremote:bucket" 或可能 "myremote:"（不推荐）。

属性：

- Config:      remote
- Env Var:     RCLONE_CHUNKER_REMOTE
- Type:        string
- Required:    true

#### --chunker-chunk-size

大于分块大小的文件将被拆分为分块。

属性：

- Config:      chunk_size
- Env Var:     RCLONE_CHUNKER_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     2Gi

#### --chunker-hash-type

选择 chunker 如何处理哈希校验和。

除 "none" 外的所有模式都需要元数据。

属性：

- Config:      hash_type
- Env Var:     RCLONE_CHUNKER_HASH_TYPE
- Type:        string
- Default:     "md5"
- Examples:
  - "none"
    - 传递被包裹远程支持的任意哈希（仅限非分块文件）。
    - 否则不返回任何内容。
  - "md5"
    - 组合文件使用 MD5。
  - "sha1"
    - 组合文件使用 SHA1。
  - "md5all"
    - 所有文件使用 MD5。
  - "sha1all"
    - 所有文件使用 SHA1。
  - "md5quick"
    - 将文件复制到 chunker 时从源请求 MD5。
    - 如果不支持则回退到 SHA1。
  - "sha1quick"
    - 类似于 "md5quick"，但优先使用 SHA1 而非 MD5。

### 高级选项

以下是 chunker（透明分块/拆分大文件）的特定高级选项。

#### --chunker-name-format

分块文件名的字符串格式。

两个占位符为：基础文件名（*）和分块编号（#...）。
必须有且仅有一个星号和一个或多个连续的井号字符。
如果分块编号的位数少于井号数量，则用零左填充。
如果数字位数更多，则保持原样。
名称不匹配给定格式的潜在分块文件将被忽略。

属性：

- Config:      name_format
- Env Var:     RCLONE_CHUNKER_NAME_FORMAT
- Type:        string
- Default:     "*.rclone_chunk.###"

#### --chunker-start-from

最小有效分块编号。通常为 0 或 1。

默认分块编号从 1 开始。

属性：

- Config:      start_from
- Env Var:     RCLONE_CHUNKER_START_FROM
- Type:        int
- Default:     1

#### --chunker-meta-format

元数据对象的格式或 "none"。

默认为 "simplejson"。
元数据是以组合文件命名的小型 JSON 文件。

属性：

- Config:      meta_format
- Env Var:     RCLONE_CHUNKER_META_FORMAT
- Type:        string
- Default:     "simplejson"
- Examples:
  - "none"
    - 完全不使用元数据文件。
    - 需要哈希类型为 "none"。
  - "simplejson"
    - 简单 JSON 支持哈希校验和与分块验证。
    -
    - 包含以下字段：ver、size、nchunks、md5、sha1。

#### --chunker-failhard

选择 chunker 如何处理具有缺失或无效分块的文件。

属性：

- Config:      fail_hard
- Env Var:     RCLONE_CHUNKER_FAIL_HARD
- Type:        bool
- Default:     false
- Examples:
  - "true"
    - 报告错误并中止当前命令。
  - "false"
    - 警告用户，跳过不完整文件并继续。

#### --chunker-transactions

选择 chunker 在事务期间如何处理临时文件。

属性：

- Config:      transactions
- Env Var:     RCLONE_CHUNKER_TRANSACTIONS
- Type:        string
- Default:     "rename"
- Examples:
  - "rename"
    - 事务成功后重命名临时文件。
  - "norename"
    - 保留临时文件名并将事务 ID 写入元数据文件。
    - 无重命名事务需要元数据（元数据格式不能为 "none"）。
    - 如果你使用 norename 事务，应注意不要降级 Rclone，
    - 因为旧版本的 Rclone 不支持此事务风格，会误解
    - 由 norename 事务操作的文件。
    - 此方法是实验性的，不要在生产系统上使用。
  - "auto"
    - 根据后端能力使用 rename 或 norename。
    - 如果元数据格式设为 "none"，则始终使用 rename 事务。
    - 此方法是实验性的，不要在生产系统上使用。

#### --chunker-description

远程的描述。

属性：

- Config:      description
- Env Var:     RCLONE_CHUNKER_DESCRIPTION
- Type:        string
- Required:    false

<!-- autogenerated options stop -->
