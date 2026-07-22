---
title: "本地文件系统"
description: "Rclone 本地文件系统文档"
versionIntroduced: "v0.91"
---

> **官方文档：** [https://rclone.org/local/](https://rclone.org/local/)
# Local Filesystem

本地路径使用普通文件系统路径指定，例如 `/path/to/wherever`，因此

```console
rclone sync --interactive /home/source /tmp/destination
```

将把 `/home/source` 同步到 `/tmp/destination`。

## 配置

为保持一致性，也可以在配置文件中配置一个类型为 `local` 的远程端，并使用 rclone 远程路径访问本地文件系统，例如 `remote:path/to/wherever`，但这可能不如直接使用更方便。

### 修改时间

Rclone 以操作系统决定的精度读取和写入修改时间。通常在 Linux 上为 1 纳秒，在 Windows 上为 10 纳秒，在 OS X 上为 1 秒。

### 文件名

磁盘上的文件名应以 UTF-8 编码。这对 Windows 和 OS X 来说是常规情况。

在 Linux 世界中存在更多不确定性，但新发行版将使用 UTF-8 编码的文件名。如果使用的是带有非 UTF-8 文件名（例如 latin1）的旧 Linux 文件系统，则可以使用 `convmv` 工具将文件系统转换为 UTF-8。该工具在大多数发行版的包管理器中可用。

如果读取到无效的（非 UTF-8）文件名，无效字符将被替换为无效字节的引用表示。名称 `gro\xdf` 将被传输为 `gro‛DF`。`rclone` 在此情况下会输出调试消息（使用 `-v` 查看），例如

```text
Local file system at .: Replacing invalid UTF-8 characters in "gro\xdf"
```

#### 受限字符

使用本地后端时，文件或目录名中可用字符的限制取决于操作系统。要检查 rclone 在您的系统上默认会替换哪些字符，请运行 `rclone help flags local-encoding`。

在非 Windows 平台上，处理文件名时会替换以下字符。

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| NUL       | 0x00  | ␀           |
| /         | 0x2F  | ／           |

在 Windows 上运行时，会替换以下字符。此列表基于 [Windows 文件命名约定](https://docs.microsoft.com/windows/desktop/FileIO/naming-a-file#naming-conventions)。

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| NUL       | 0x00  | ␀           |
| SOH       | 0x01  | ␁           |
| STX       | 0x02  | ␂           |
| ETX       | 0x03  | ␃           |
| EOT       | 0x04  | ␄           |
| ENQ       | 0x05  | ␅           |
| ACK       | 0x06  | ␆           |
| BEL       | 0x07  | ␇           |
| BS        | 0x08  | ␈           |
| HT        | 0x09  | ␉           |
| LF        | 0x0A  | ␊           |
| VT        | 0x0B  | ␋           |
| FF        | 0x0C  | ␌           |
| CR        | 0x0D  | ␍           |
| SO        | 0x0E  | ␎           |
| SI        | 0x0F  | ␏           |
| DLE       | 0x10  | ␐           |
| DC1       | 0x11  | ␑           |
| DC2       | 0x12  | ␒           |
| DC3       | 0x13  | ␓           |
| DC4       | 0x14  | ␔           |
| NAK       | 0x15  | ␕           |
| SYN       | 0x16  | ␖           |
| ETB       | 0x17  | ␗           |
| CAN       | 0x18  | ␘           |
| EM        | 0x19  | ␙           |
| SUB       | 0x1A  | ␚           |
| ESC       | 0x1B  | ␛           |
| FS        | 0x1C  | ␜           |
| GS        | 0x1D  | ␝           |
| RS        | 0x1E  | ␞           |
| US        | 0x1F  | ␟           |
| /         | 0x2F  | ／           |
| "         | 0x22  | ＂           |
| *         | 0x2A  | ＊           |
| :         | 0x3A  | ：           |
| <         | 0x3C  | ＜           |
| >         | 0x3E  | ＞           |
| ?         | 0x3F  | ？           |
| \         | 0x5C  | ＼           |
| \|        | 0x7C  | ｜           |

Windows 上的文件名也不能以以下字符结尾。仅当这些字符是名称中的最后一个字符时才会被替换：

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| SP        | 0x20  | ␠           |
| .         | 0x2E  | ．           |

无效的 UTF-8 字节也会被[替换](/overview/#invalid-utf8)，因为它们无法转换为 UTF-16。

### Windows 上的路径

在 Windows 上，指定文件系统资源路径的方式有很多种。本地路径可以是绝对路径，如 `C:\path\to\wherever`，或相对路径，如 `..\wherever`。UNC 格式的网络路径 `\\server\share` 也受支持。路径分隔符可以是 `\`（如 `C:\path\to\wherever`）或 `/`（如 `C:/path/to/wherever`）。这些路径的长度限制为文件 259 个字符、目录 247 个字符，但有一种扩展长度路径格式可将限制增加到（约）32,767 个字符。此格式要求使用绝对路径并加上 `\\?\` 前缀，例如 `\\?\D:\some\very\long\path`。为方便起见，rclone 会自动将常规路径转换为对应的扩展长度路径，因此在大多数情况下您无需担心此问题（详情见[下文](#long-paths)）。使用相同的前缀 `\\?\` 还可以指定由 GUID 标识的卷的路径，例如 `\\?\Volume{b75e2c83-0000-0000-0000-602f00000000}\some\path`。

#### 长路径

Rclone 自动处理长路径，将所有路径转换为[扩展长度路径格式](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation)，允许路径长达 32,767 个字符。

此转换会确保路径为绝对路径，并为其添加 `\\?\` 前缀。这就是您会看到路径如 `.\files` 在输出中显示为 `\\?\C:\files`，而 `\\server\share` 显示为 `\\?\UNC\server\share` 的原因。

但在极少数情况下，这可能会导致有缺陷的文件系统驱动程序出现问题，例如 [EncFS](https://github.com/rclone/rclone/issues/261)。要全局禁用 UNC 转换，请在 `.rclone.conf` 文件中添加：

```ini
[local]
nounc = true
```

如果您想选择性地禁用 UNC，可以将其添加到单独的配置项中：

```ini
[nounc]
type = local
nounc = true
```

然后像这样使用 rclone：

`rclone copy c:\src nounc:z:\dst`

这将在 `c:\src` 上使用 UNC 路径，但在 `z:\dst` 上不使用。当然，如果 z 上的文件绝对路径长度超过 259 个字符，这将导致问题，因此仅在必要时使用此选项。

### 符号链接 / 接合点

通常 rclone 会忽略符号链接或接合点（在 Windows 上的行为类似于符号链接）。

如果提供 `--copy-links` 或 `-L`，则 rclone 将跟踪符号链接并复制其指向的文件或目录。请注意，此标志与 `--links` / `-l` 不兼容。

此标志适用于所有命令。

例如，假设您有如下目录结构

```console
$ tree /tmp/a
/tmp/a
├── b -> ../b
├── expected -> ../expected
├── one
└── two
    └── three
```

然后您可以看到有无此标志的区别

```console
$ rclone ls /tmp/a
        6 one
        6 two/three
```

以及

```console
$ rclone -L ls /tmp/a
     4174 expected
        6 one
        6 two/three
        6 b/two
        6 b/one
```

#### --local-links, --links, -l

通常 rclone 会忽略符号链接或接合点（在 Windows 上的行为类似于符号链接）。

如果提供此标志，rclone 将从本地存储复制符号链接，并将其作为文本文件存储在远程存储中，后缀为 `.rclonelink`。

文本文件将包含符号链接的目标（参见示例）。

此标志适用于所有命令。

例如，假设您有如下目录结构

```console
$ tree /tmp/a
/tmp/a
├── file1 -> ./file4
└── file2 -> /home/user/file3
```

使用 '-l' 复制整个目录

```console
rclone copy -l /tmp/a/ remote:/tmp/a/
```

远程文件将带有 `.rclonelink` 后缀创建

```console
$ rclone ls remote:/tmp/a
       5 file1.rclonelink
      14 file2.rclonelink
```

远程文件将包含符号链接的目标

```console
$ rclone cat remote:/tmp/a/file1.rclonelink
./file4

$ rclone cat remote:/tmp/a/file2.rclonelink
/home/user/file3
```

使用 '-l' 将其复制回来

```console
$ rclone copy -l remote:/tmp/a/ /tmp/b/

$ tree /tmp/b
/tmp/b
├── file1 -> ./file4
└── file2 -> /home/user/file3
```

但是，如果不使用 '-l' 复制回来

```console
$ rclone copyto remote:/tmp/a/ /tmp/b/

$ tree /tmp/b
/tmp/b
├── file1.rclonelink
└── file2.rclonelink
```

如果要使用 `-l` 复制单个文件，则必须使用 `.rclonelink` 后缀。

```console
$ rclone copy -l remote:/tmp/a/file1.rclonelink /tmp/c

$ tree /tmp/c
/tmp/c
└── file1 -> ./file4
```

请注意，`--local-links` 仅为本地后端启用此功能。`--links` 和 `-l` 为所有支持的后端和 VFS 启用此功能。

请注意，此标志与 `-copy-links` / `-L` 不兼容。

### 使用 --one-file-system 限制文件系统

通常 rclone 会递归遍历已挂载的文件系统。

但如果设置 `--one-file-system` 或 `-x`，则告诉 rclone 保持在根目录所指定的文件系统中，不递归进入不同的文件系统。

例如，如果您有如下目录层级

```console
root
├── disk1     - disk1 mounted on the root
│   └── file3 - stored on disk1
├── disk2     - disk2 mounted on the root
│   └── file4 - stored on disk12
├── file1     - stored on the root disk
└── file2     - stored on the root disk
```

使用 `rclone --one-file-system copy root remote:` 将只复制 `file1` 和 `file2`。例如

```console
$ rclone -q --one-file-system ls root
        0 file1
        0 file2
```

```console
$ rclone -q ls root
        0 disk1/file3
        0 disk2/file4
        0 file1
        0 file2
```

**注意** Rclone（像大多数 Unix 工具如 `du`、`rsync` 和 `tar`）将同一设备的绑定挂载视为在同一文件系统上。

**注意** 此标志仅在基于 Unix 的系统上可用。在不支持此功能的系统（例如 Windows）上，它将被忽略。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/local/local.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 高级选项

以下是本地（本地磁盘）的特定高级选项。

#### --local-nounc

在 Windows 上禁用 UNC（长路径名）转换。

属性：

- Config:      nounc
- Env Var:     RCLONE_LOCAL_NOUNC
- Type:        bool
- Default:     false
- 示例：
  - "true"
    - 禁用长文件名。

#### --copy-links / -L

跟踪符号链接并复制其指向的项目。

属性：

- Config:      copy_links
- Env Var:     RCLONE_LOCAL_COPY_LINKS
- Type:        bool
- Default:     false

#### --local-links

将符号链接转换为/自带有 '.rclonelink' 扩展名的常规文件（仅限本地后端）。

属性：

- Config:      links
- Env Var:     RCLONE_LOCAL_LINKS
- Type:        bool
- Default:     false

#### --skip-links

不对跳过的符号链接发出警告。

此标志禁用对跳过的符号链接或接合点的警告消息，因为您明确确认它们应被跳过。

属性：

- Config:      skip_links
- Env Var:     RCLONE_LOCAL_SKIP_LINKS
- Type:        bool
- Default:     false

#### --skip-specials

不对跳过的管道、套接字和设备对象发出警告。

此标志禁用对跳过的管道、套接字和设备对象的警告消息，因为您明确确认它们应被跳过。

属性：

- Config:      skip_specials
- Env Var:     RCLONE_LOCAL_SKIP_SPECIALS
- Type:        bool
- Default:     false

#### --local-zero-size-links

假定链接的 Stat 大小为零（并改为读取链接）（已弃用）。

Rclone 过去使用链接的 Stat 大小作为链接大小，但这在不少地方会失败：

- Windows
- 某些虚拟文件系统（如 LucidLink）
- Android

因此 rclone 现在总是读取链接。


属性：

- Config:      zero_size_links
- Env Var:     RCLONE_LOCAL_ZERO_SIZE_LINKS
- Type:        bool
- Default:     false

#### --local-unicode-normalization

对路径和文件名应用 unicode NFC 规范化。

此标志可用于将本地文件系统读取的文件名规范化为 unicode NFC 形式。

Rclone 通常不会修改从文件系统读取的文件名的编码。

这在 macOS 上可能有用，因为它通常提供分解形式（NFD）的 unicode，在某些语言（如韩语）中无法在某些操作系统上正常显示。

请注意，rclone 在同步例程中比较文件名时会使用 unicode 规范化，因此通常不需要使用此标志。

属性：

- Config:      unicode_normalization
- Env Var:     RCLONE_LOCAL_UNICODE_NORMALIZATION
- Type:        bool
- Default:     false

#### --local-no-check-updated

不检查文件在上传期间是否发生变化。

通常 rclone 会在上传过程中检查文件的大小和修改时间，如果文件在上传期间发生变化，则以一条以"can't copy - source file is being updated"开头的消息中止。

但在某些文件系统上，此修改时间检查可能失败（例如 [Glusterfs #2206](https://github.com/rclone/rclone/issues/2206)），因此可以使用此标志禁用此检查。

如果设置了此标志，rclone 将尽最大努力传输正在更新的文件。如果文件只是被追加内容（例如日志），则 rclone 将以首次看到该日志文件时的大小传输它。

如果文件在整个过程中都被修改（不只是追加），则传输可能因哈希校验失败而失败。

具体而言，一旦文件首次调用了 stat()，我们：

- 仅传输 stat 给出的大小
- 仅对 stat 给出的大小进行校验和计算
- 不更新该文件的 stat 信息

**注意** 请勿在 Windows 卷影副本（VSS）上使用此标志。由于某些未知原因，VSS 中的文件有时会显示与目录列表（Windows 上初始 stat 值的来源）不同的大小，而对它们直接调用 stat 时大小也不同。其他复制工具始终使用直接 stat 值，设置此标志将禁用此行为。


属性：

- Config:      no_check_updated
- Env Var:     RCLONE_LOCAL_NO_CHECK_UPDATED
- Type:        bool
- Default:     false

#### --one-file-system / -x

不跨越文件系统边界（仅限 unix/macOS）。

属性：

- Config:      one_file_system
- Env Var:     RCLONE_LOCAL_ONE_FILE_SYSTEM
- Type:        bool
- Default:     false

#### --local-case-sensitive

强制文件系统报告自身为区分大小写。

通常本地后端在 Windows/macOS 上声明自身为不区分大小写，在其他系统上为区分大小写。使用此标志可覆盖默认选择。

属性：

- Config:      case_sensitive
- Env Var:     RCLONE_LOCAL_CASE_SENSITIVE
- Type:        bool
- Default:     false

#### --local-case-insensitive

强制文件系统报告自身为不区分大小写。

通常本地后端在 Windows/macOS 上声明自身为不区分大小写，在其他系统上为区分大小写。使用此标志可覆盖默认选择。

属性：

- Config:      case_insensitive
- Env Var:     RCLONE_LOCAL_CASE_INSENSITIVE
- Type:        bool
- Default:     false

#### --local-no-clone

禁用 reflink 克隆以进行服务端复制。

通常，对于本地到本地的传输，rclone 会在可能时"克隆"文件，仅在克隆不支持时回退到"复制"。

克隆创建一个浅拷贝（或"reflink"），最初与原始文件共享数据块。与"硬链接"不同，这两个文件是独立的，如果后续被修改，两者互不影响。

克隆通常优于复制，因为它快得多，并且默认是去重的（即拥有两个相同的文件不会比只有一个消耗更多存储空间）。但是，对于需要数据冗余的场景，--local-no-clone 可用于禁用克隆并强制执行"深拷贝"。

目前，仅在 macOS 上使用 APFS 时支持克隆（未来可能添加对其他平台的支持）。

属性：

- Config:      no_clone
- Env Var:     RCLONE_LOCAL_NO_CLONE
- Type:        bool
- Default:     false

#### --local-no-preallocate

禁用为传输文件预分配磁盘空间。

磁盘空间预分配有助于防止文件系统碎片化。但是，某些虚拟文件系统层（如 Google Drive File Stream）可能会错误地将实际文件大小设置为等于预分配空间，导致校验和和文件大小检查失败。使用此标志可禁用预分配。

属性：

- Config:      no_preallocate
- Env Var:     RCLONE_LOCAL_NO_PREALLOCATE
- Type:        bool
- Default:     false

#### --local-no-sparse

禁用多线程下载的稀疏文件。

在 Windows 平台上，rclone 在进行多线程下载时会创建稀疏文件。这避免了在大型文件上操作系统将文件清零时出现的长时间暂停。但是稀疏文件可能并不理想，因为它们会导致磁盘碎片化并且处理速度可能较慢。

属性：

- Config:      no_sparse
- Env Var:     RCLONE_LOCAL_NO_SPARSE
- Type:        bool
- Default:     false

#### --local-no-set-modtime

禁用设置修改时间。

通常 rclone 在文件上传完成后更新其修改时间。这在 Linux 平台上可能导致权限问题，当运行 rclone 的用户不拥有已上传的文件时（例如复制到由其他用户拥有的 CIFS 挂载时）。如果启用此选项，rclone 将不再在复制文件后更新修改时间。

属性：

- Config:      no_set_modtime
- Env Var:     RCLONE_LOCAL_NO_SET_MODTIME
- Type:        bool
- Default:     false

#### --local-time-type

设置返回的时间类型。

通常 rclone 对所有操作使用 mtime 或修改时间。

如果设置此标志，rclone 将返回的修改时间为您在此设置的值。因此，如果使用 "rclone lsl --local-time-type ctime"，则列表中将显示 ctime。

如果操作系统不支持返回指定的 time_type，rclone 将静默替换为所有操作系统都支持的修改时间。

- mtime 在所有操作系统上受支持
- atime 在除 plan9、js 之外的所有操作系统上受支持
- btime 仅在 Windows、macOS、freebsd、netbsd 上受支持
- ctime 在除 Windows、plan9、js 之外的所有操作系统上受支持

请注意，设置时间仍然会设置修改时间，因此这仅对读取有用。


属性：

- Config:      time_type
- Env Var:     RCLONE_LOCAL_TIME_TYPE
- Type:        mtime|atime|btime|ctime
- Default:     mtime
- 示例：
  - "mtime"
    - 最后修改时间。
  - "atime"
    - 最后访问时间。
  - "btime"
    - 创建时间。
  - "ctime"
    - 最后状态变更时间。

#### --local-hashes

逗号分隔的支持的校验和类型列表。

属性：

- Config:      hashes
- Env Var:     RCLONE_LOCAL_HASHES
- Type:        CommaSepList
- Default:

#### --local-encoding

后端的编码。

更多信息请参见[概述中的编码部分](/overview/#encoding)。

属性：

- Config:      encoding
- Env Var:     RCLONE_LOCAL_ENCODING
- Type:        Encoding
- Default:     Slash,Dot

#### --local-description

远程端的描述。

属性：

- Config:      description
- Env Var:     RCLONE_LOCAL_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

根据所使用的操作系统，本地后端可能仅返回部分系统元数据。设置系统元数据在所有操作系统上受支持，但设置用户元数据仅在 linux、freebsd、netbsd、macOS 和 Solaris 上受支持。Windows 上**尚不**受支持（[参见 pkg/attrs#47](https://github.com/pkg/xattr/issues/47)）。

用户元数据以扩展属性存储（可能并非所有文件系统都支持），使用 "user.*" 前缀。

元数据在文件和目录上受支持。

以下是本地后端可能的系统元数据项。

| 名称 | 帮助 | 类型 | 示例 | 只读 |
|------|------|------|---------|-----------|
| atime | 最后访问时间 | RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 | N |
| btime | 文件创建（诞生）时间 | RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 | N |
| gid | 所有者的组 ID | 十进制数 | 500 | N |
| mode | 文件类型和模式 | 八进制，unix 风格 | 0100664 | N |
| mtime | 最后修改时间 | RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 | N |
| rdev | 设备 ID（如果是特殊文件） | 十六进制 | 1abc | N |
| uid | 所有者的用户 ID | 十进制数 | 500 | N |

更多信息请参见[元数据](/docs/#metadata)文档。

## 后端命令

以下是本地后端的特定命令。

使用方式：

```console
rclone backend COMMAND remote:
```

下面的帮助将解释每个命令接受的参数。

关于如何传递选项和参数的更多信息，请参见 [backend](/commands/rclone_backend/) 命令。

这些命令可以在运行中的后端上使用 rc 命令 [backend/command](/rc/#backend-command) 执行。

### noop

用于测试后端命令的空操作。

```console
rclone backend noop remote: [options] [<arguments>+]
```

这是一个测试命令，有一些选项可以尝试改变输出。

选项：

- "echo"：回显输入参数。
- "error"：根据选项值返回错误。

<!-- autogenerated options stop -->