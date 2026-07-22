---
title: "云存储系统概览"
description: "云存储系统概览"
type: page
---

> **官方文档：** [https://rclone.org/overview/](https://rclone.org/overview/)
# Overview of cloud storage systems

每种云存储系统都略有不同。Rclone 尝试为它们提供统一接口，但一些底层差异仍然会体现出来。

## 功能特性

以下是各云存储系统主要功能的概览。

在技能转换期间从 `testdata/rclone/docs/data/backends/*.yaml` 生成。

| 名称 | 层级 | 哈希 | 修改时间 | 大小写不敏感 | 重复文件 | MIME 类型 | 元数据 |
|---|---|---|---|---|---|---|---|
| [Azure Blob](providers/azureblob.md) | Tier 1 | md5 | R/W | 否 | 否 | R/W | RWU |
| [Azure Files](providers/azurefiles.md) | Tier 2 | md5 | R/W | 是 | 否 | R/W | - |
| [B2](providers/b2.md) | Tier 1 | sha1 | R/W | 否 | 否 | R/W | - |
| [Box](providers/box.md) | Tier 1 | sha1 | R/W | 是 | 否 | - | - |
| [Cloudinary](providers/cloudinary.md) | Tier 3 | md5 | R | 否 | 否 | - | - |
| [Doi](https://rclone.org/doi/) | Tier 2 | - | R/W | 否 | 否 | - | - |
| [Drime](providers/drime.md) | Tier 1 | - | R | 否 | 否 | R/W | - |
| [Drive](providers/drive.md) | Tier 1 | md5, sha1, sha256 | DR/W | 否 | 是 | R/W | DRWU |
| [Dropbox](providers/dropbox.md) | Tier 1 | dropbox | R/W | 是 | 否 | - | - |
| [Fichier](providers/fichier.md) | Tier 3 | whirlpool | R | 否 | 是 | R | - |
| [Filefabric](providers/filefabric.md) | Tier 4 | - | R/W | 是 | 否 | R/W | - |
| [Filelu](providers/filelu.md) | Tier 1 | - | R | 否 | 否 | - | - |
| [Filen](providers/filen.md) | Tier 1 | blake3 | R/W | 否 | 否 | R/W | - |
| [Filescom](providers/filescom.md) | Tier 1 | md5, crc32 | DR/W | 是 | 否 | R | - |
| [FTP](providers/ftp.md) | Tier 1 | - | R/W | 否 | 否 | - | - |
| [Gofile](providers/gofile.md) | Tier 1 | md5 | DR/W | 否 | 是 | R | - |
| [Google Cloud Storage](providers/googlecloudstorage.md) | Tier 1 | md5 | R/W | 否 | 否 | R/W | - |
| [Google Photos](providers/googlephotos.md) | Tier 5 | - | R | 否 | 否 | R | - |
| [HDFS](providers/hdfs.md) | Tier 2 | - | R/W | 否 | 否 | - | - |
| [Hidrive](providers/hidrive.md) | Tier 1 | hidrive | R/W | 否 | 否 | - | - |
| [HTTP](providers/http.md) | Tier 3 | - | R/W | 否 | 否 | - | R |
| [Iclouddrive](providers/iclouddrive.md) | Tier 4 | - | R/W | 否 | 否 | - | - |
| [Imagekit](https://rclone.org/imagekit/) | Tier 1 | - | R | 否 | 否 | R | R |
| [Internet Archive](providers/internetarchive.md) | Tier 3 | md5, sha1, crc32 | R/W | 否 | 否 | - | RWU |
| [Internxt](providers/internxt.md) | Tier 2 | - | R | 否 | 否 | - | - |
| [Jottacloud](providers/jottacloud.md) | Tier 2 | md5 | R/W | 是 | 否 | R | RW |
| [Koofr](providers/koofr.md) | Tier 2 | md5 | R/W | 是 | 否 | - | - |
| [Linkbox](providers/linkbox.md) | Tier 5 | - | R | 是 | 否 | - | - |
| [Local](providers/local.md) | Tier 1 | ALL | DR/W | 否 | 否 | - | DRWU |
| [Mailru](providers/mailru.md) | Tier 1 | mailru | R/W | 是 | 否 | - | - |
| [Mega](providers/mega.md) | Tier 2 | - | R | 否 | 是 | - | - |
| [Memory](providers/memory.md) | Tier 1 | md5 | R/W | 否 | 否 | R/W | - |
| [Netstorage](providers/netstorage.md) | Tier 1 | md5 | R/W | 否 | 否 | - | - |
| [Onedrive](providers/onedrive.md) | Tier 1 | quickxor | DR/W | 是 | 否 | R | DRW |
| [Opendrive](providers/opendrive.md) | Tier 1 | md5 | R/W | 是 | 否 | - | - |
| [Oracle Object Storage](https://rclone.org/oracleobjectstorage/) | Tier 1 | md5 | R/W | 否 | 否 | R/W | R |
| [Pcloud](providers/pcloud.md) | Tier 1 | sha1, sha256 | R/W | 否 | 否 | - | - |
| [Pikpak](providers/pikpak.md) | Tier 1 | md5 | R | 否 | 否 | R | - |
| [Pixeldrain](providers/pixeldrain.md) | Tier 1 | sha256 | DR/W | 否 | 否 | R | RW |
| [Premiumizeme](providers/premiumizeme.md) | Tier 3 | - | R | 是 | 否 | R | - |
| [Proton Drive](providers/protondrive.md) | Tier 5 | sha1 | R/W | 否 | 否 | R | - |
| [Putio](providers/putio.md) | Tier 2 | crc32 | R/W | 否 | 是 | R | - |
| [Qingstor](providers/qingstor.md) | Tier 3 | md5 | R | 否 | 否 | R/W | - |
| [Quatrix](providers/quatrix.md) | Tier 3 | - | R/W | 否 | 否 | - | - |
| [S3](providers/s3.md) | Tier 1 | md5 | R/W | 否 | 否 | R/W | RWU |
| [Seafile](providers/seafile.md) | Tier 3 | - | R | 否 | 否 | - | - |
| [SFTP](providers/sftp.md) | Tier 1 | md5, sha1 | DR/W | 否 | 否 | - | - |
| [Shade](providers/shade.md) | Tier 1 | - | R | 否 | 否 | - | - |
| [Sharefile](providers/sharefile.md) | Tier 5 | md5 | R/W | 否 | 否 | - | - |
| [Sia](providers/sia.md) | Tier 4 | - | R | 否 | 否 | - | - |
| [SMB](providers/smb.md) | Tier 2 | - | R/W | 是 | 否 | - | - |
| [Storj](providers/storj.md) | Tier 1 | - | R/W | 否 | 否 | - | - |
| [Sugarsync](providers/sugarsync.md) | Tier 3 | - | R | 是 | 否 | - | - |
| [Swift](providers/swift.md) | Tier 1 | md5 | R/W | 否 | 否 | R/W | - |
| [Ulozto](providers/ulozto.md) | Tier 3 | md5, sha256 | R/W | 否 | 是 | - | - |
| [WebDAV](providers/webdav.md) | Tier 1 | sha1 | R/W | 否 | 否 | - | - |
| [Yandex](providers/yandex.md) | Tier 1 | md5 | R/W | 否 | 否 | R | - |
| [Zoho](providers/zoho.md) | Tier 3 | - | R | 否 | 否 | - | - |

### 哈希

云存储系统支持对象的多种哈希类型。哈希在传输数据时用作完整性校验，也可在同步操作中通过 `--checksum` 标志或在 `check` 命令中专门使用。

在云存储系统之间传输时要使用校验和，它们必须支持相同的哈希类型。

### 修改时间

几乎所有云存储系统都会在对象上存储某种时间戳，但其中一些并不适合用于同步。例如，某些后端只会写入表示上传时间的时间戳。要适用于同步，它应该能够存储源对象的修改时间。如果不支持此功能，rclone 默认只会检查文件大小，但可以配置为检查文件哈希（使用 `--checksum` 标志）。理想情况下，还应能够在不重新上传的情况下更改现有文件的时间戳。

| 键 | 说明 |
|-----|------|
| `-` | 不支持修改时间 — 时间可能是上传时间 |
| `R` | 文件支持修改时间，但无法在不重新上传的情况下更改 |
| `R/W` | 文件完全支持修改时间的读取和写入 |
| `DR` | 文件和目录支持修改时间，但无法在不重新上传的情况下更改 |
| `DR/W` | 文件和目录完全支持修改时间的读取和写入 |

修改时间列中为 `-` 的存储系统，表示读取到的对象修改时间并非文件上传时的修改时间。它很可能是文件上传的时间，也可能是其他内容（例如 Google Photos 中照片的拍摄时间）。

修改时间列中为 `R`（只读）的存储系统，表示它会在对象上保留修改时间，并在上传对象时更新，但不支持仅更改修改时间（`SetModTime` 操作）而不重新上传，甚至可能需要先删除已有文件才能实现。rclone 中的某些操作（如 `copy` 和 `sync` 命令）会自动检查 `SetModTime` 支持情况，并在必要时重新上传以保持修改时间同步。其他命令在没有 `SetModTime` 支持的情况下将无法工作，例如对已有文件执行 `touch` 命令会失败，`mount` 中仅修改时间的更改会被静默忽略。

修改时间列中为 `R/W`（读/写）的存储系统，表示它们也支持仅修改时间的操作。

修改时间列中带有 `D` 的存储系统，表示以下符号同样适用于目录和文件。

### 大小写不敏感

如果云存储系统区分大小写，则可能存在仅大小写不同的两个文件，例如 `file.txt` 和 `FILE.txt`。如果云存储系统不区分大小写，则不可能存在这种情况。

在区分大小写和不区分大小写的系统之间同步时，这可能会导致问题。其症状是无论运行多少次同步，都永远无法完全完成。

本地文件系统和 SFTP 可能区分也可能不区分大小写，取决于操作系统。

- Windows — 通常不区分大小写，但会保留大小写
- OSX — 通常不区分大小写，但可以格式化为区分大小写
- Linux — 通常区分大小写，但也存在不区分大小写的文件系统（例如 FAT 格式的 U 盘）

大多数情况下这不会造成问题，因为即使在区分大小写的系统上，人们也倾向于避免使用仅大小写不同的文件名。

### 重复文件

如果云存储系统允许重复文件，则可能存在两个同名对象。

这会导致 rclone 在同步时产生严重混乱 — 使用 `rclone dedupe` 命令来重命名或删除重复项。

### 受限文件名

某些云存储系统可能对文件或目录名中可使用的字符有限制。当 `rclone` 在文件上传期间检测到此类名称时，会透明地将受限字符替换为外观相似的 Unicode 字符。为处理不同后端的不同受限字符集，rclone 使用了它称之为[编码](#encoding)的机制。

此过程旨在尽可能避免文件名歧义，并允许在多种云存储系统之间透明地移动文件。

`rclone` 向用户显示或在日志输出中的名称将仅包含最少的[替换字符](#restricted-characters)，以确保正确的格式化，而不一定是云存储上使用的实际名称。

此转换在下载文件或解析 `rclone` 参数时会被逆转。例如，当上传名为 `my file?.txt` 的文件到 Onedrive 时，控制台上将显示为 `my file?.txt`，但在 Onedrive 上存储为 `my file？.txt`（`?` 被替换为外观相似的 `？` 字符，即所谓的"全角问号"）。逆向转换允许从 Google Drive 读取名为 `unusual/name.txt` 的文件，只需在命令行中传入 `unusual／name.txt`（`/` 需要替换为外观相似的 `／` 字符）。

#### 注意事项 {#restricted-filenames-caveats}

文件名编码系统在大多数情况下运行良好，至少在文件名使用英语或类似语言的情况下。你可能甚至不会注意到它：它就是正常工作。但在某些情况下可能会导致问题。例如，当文件名使用中文或日文时，其中总是使用标点符号的 Unicode 全角变体。

在 Windows 上，字符 `:`、`*` 和 `?` 是受限字符的示例。如果在支持这些字符的远程存储上的文件名中使用了它们，Rclone 在下载到 Windows 时会透明地将它们转换为其全角 Unicode 变体 `＊`、`？` 和 `：`，上传时再转换回来。这样，名称在 Windows 上不被允许的文件仍然可以被存储。

然而，如果你的 Windows 系统上原本就有包含这些 Unicode 字符的文件，它们也会被纳入相同的转换过程。例如，如果你在 Windows 文件系统中创建了一个名为 `Test：1.jpg` 的文件（其中 `：` 是 Unicode 全角冒号符号），并使用 rclone 将其上传到支持常规 `:`（半角冒号）的 Google Drive，rclone 会将全角 `:` 替换为半角 `:`，并在 Google Drive 中将文件存储为 `Test:1.jpg`。由于 Windows 和 Google Drive 都允许 `Test：1.jpg` 这个名称，在这种情况下 rclone 保持原名不变可能更好。

在相反的情况下，如果你在 Google Drive 中有一个名为 `Test:1.jpg` 的文件（例如从 `:` 在文件名中合法的 Linux 系统上传的），然后使用 rclone 将此文件复制到 Windows 计算机，你会发现本地磁盘上它被重命名为 `Test：1.jpg`。原始文件名由于包含 `:` 在 Windows 上不合法，因此 rclone 对其重命名以使复制成为可能。这本身没问题。然而，这也可能导致一个问题：如果你在 Windows 上已经有一个名为 `Test：1.jpg` 的*不同*文件，然后使用 rclone 进行任意方向的复制。rclone 会将 Google Drive 上最初名为 `Test:1.jpg` 的文件和 Windows 上最初名为 `Test：1.jpg` 的文件视为同一个文件，并将其中一个的内容替换为另一个的内容。

在所有情况下正确处理所有此类情况几乎是不可能的，但通过自定义[编码选项](#encoding)，更改 rclone 应转换的字符集，你应该能够创建适合你特定情况的配置。另见下面的[示例](/overview/#encoding-example-windows)。

（Windows 被用作具有许多受限字符的文件系统示例，Google Drive 被用作受限字符较少的存储系统示例。）

#### 默认受限字符 {#restricted-characters}

下表显示了默认被替换的字符。

当文件名中发现替换字符时，该字符将使用 `‛` 字符进行转义以避免文件名歧义。（例如，名为 `␀.txt` 的文件将显示为 `‛␀.txt`）

每个云存储后端可以使用不同的字符集，具体在各自后端的文档中说明。

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
| DEL       | 0x7F  | ␡           |

默认编码还会编码以下文件名，因为它们在许多云存储系统中都有问题。

| 文件名 | 替换为 |
| --------- |:-----------:|
| .         | ．          |
| ..        | ．．         |

#### 无效的 UTF-8 字节 {#invalid-utf8}

某些后端仅支持格式良好的 UTF-8 字节序列作为文件或目录名。

在这种情况下，所有无效的 UTF-8 字节将被替换为字节值的引号表示形式，以允许将文件上传到此类后端。例如，无效字节 `0xFE` 将被编码为 `‛FE`。

无效 UTF-8 字节的常见来源是本地文件系统，这些系统使用非 UTF-8 或 UTF-16 的编码存储名称，如 latin1。详见[本地文件名](/local/#filenames)部分。

#### 编码选项 {#encoding}

大多数后端都有编码选项，以标志 `--backend-encoding` 的形式指定（其中 `backend` 是后端名称），或作为配置参数 `encoding`（你需要在 `rclone config` 中选择高级配置才能看到它）。

它有一个默认值，以尽可能保留最多字符的方式进行编码和解码（见上文）。

然而在某些场景下这可能不正确，例如你有一个 Windows 文件系统，其中包含 Unicode 全角字符 `＊`、`？` 或 `：`，你希望它们在远程存储上保持为这些字符，而不是被转换为常规（半角）`*`、`?` 和 `:`。

`--backend-encoding` 标志允许你更改此设置。你可以使用 `--backend-encoding Raw` 完全禁用编码，或在配置文件中设置 `encoding = Raw`。

编码接受逗号分隔的编码列表。你可以通过向此标志传递无效值来查看所有可能的值列表，例如 `--local-encoding "help"`。命令 `rclone help flags encoding` 将显示各后端的默认值。

| 编码  | 字符 | 编码为 |
| --------- | ---------- | ---------- |
| Asterisk | `*` | `＊` |
| BackQuote | `` ` `` | `｀` |
| BackSlash | `\` | `＼` |
| Colon | `:` | `：` |
| CrLf | CR 0x0D, LF 0x0A | `␍`, `␊` |
| Ctl | 所有控制字符 0x00-0x1F | `␀␁␂␃␄␅␆␇␈␉␊␋␌␍␎␏␐␑␒␓␔␕␖␗␘␙␚␛␜␝␞␟` |
| Del | DEL 0x7F | `␡` |
| Dollar | `$` | `＄` |
| Dot | `.` 或 `..` 作为整个字符串 | `．`, `．．` |
| DoubleQuote | `"` | `＂` |
| Exclamation | `!` | `！` |
| Hash | `#` | `＃` |
| InvalidUtf8 | 无效的 UTF-8 字符（如 latin1） | `�` |
| LeftCrLfHtVt | 字符串左侧的 CR 0x0D、LF 0x0A、HT 0x09、VT 0x0B | `␍`, `␊`, `␉`, `␋` |
| LeftPeriod | 字符串左侧的 `.` | `.` |
| LeftSpace | 字符串左侧的空格 | `␠` |
| LeftTilde | 字符串左侧的 `~` | `～` |
| LtGt | `<`, `>` | `＜`, `＞` |
| None ¹ | NUL 0x00 | ␀ |
| Percent | `%` | `％` |
| Pipe | \| | `｜` |
| Question | `?` | `？` |
| RightCrLfHtVt | 字符串右侧的 CR 0x0D、LF 0x0A、HT 0x09、VT 0x0B | `␍`, `␊`, `␉`, `␋` |
| RightPeriod | 字符串右侧的 `.` | `.` |
| RightSpace | 字符串右侧的空格 | `␠` |
| Semicolon | `;` | `；` |
| SingleQuote | `'` | `＇` |
| Slash | `/` | `／` |
| SquareBracket | `[`, `]` | `［`, `］` |

¹ 从 NUL 0x00 到 ␀ 的编码在使用 Raw 时除外，始终是隐式的。它以前被错误地记录为禁用编码，为保持向后兼容性，其行为未被更改。

##### 编码示例：FTP

以具体示例来说，FTP 后端的默认编码为

```text
--ftp-encoding "Slash,Del,Ctl,RightSpace,Dot"
```

然而，假设 FTP 服务器运行在 Windows 上，文件名中不能包含任何 Windows 无效字符。你正在将 Linux 服务器备份到此 FTP 服务器，而 Linux 文件名中确实包含这些字符。那么你需要添加 Windows 字符集，即

```text
Slash,LtGt,DoubleQuote,Colon,Question,Asterisk,Pipe,BackSlash,Ctl,RightSpace,RightPeriod,InvalidUtf8,Dot
```

加到已有的编码上，得到：

```text
Slash,LtGt,DoubleQuote,Colon,Question,Asterisk,Pipe,BackSlash,Ctl,RightSpace,RightPeriod,InvalidUtf8,Dot,Del,RightSpace
```

这可以通过 `--ftp-encoding` 标志或配置文件中的 `encoding` 参数来指定。

##### 编码示例：Windows

再举一个例子，在 Windows 系统上有一个名为 `Test：1.jpg` 的文件，其中 `：` 是 Unicode 全角冒号符号。使用 rclone 将此文件复制到支持 `:`（常规半角冒号，如 Google Drive）的远程存储时，你会注意到文件被重命名为 `Test:1.jpg`。

为避免此情况，你可以使用命令行参数 `--local-encoding` 更改 rclone 应为本地文件系统转换的字符集。rclone 在 Windows 上的默认行为对应于

```text
--local-encoding "Slash,LtGt,DoubleQuote,Colon,Question,Asterisk,Pipe,BackSlash,Ctl,RightSpace,RightPeriod,InvalidUtf8,Dot"
```

如果你希望在文件名中使用全角字符 `：`、`＊` 和 `？`，而不让 rclone 在上传到远程存储时更改它们，则设置为与默认值相同但不包含 `Colon,Question,Asterisk`：

```text
--local-encoding "Slash,LtGt,DoubleQuote,Pipe,BackSlash,Ctl,RightSpace,RightPeriod,InvalidUtf8,Dot"
```

或者，你可以使用 `--local-encoding Raw` 禁用任何字符的转换。

除了使用命令行参数 `--local-encoding`，你还可以将其设置为[环境变量](/docs/#environment-variables) `RCLONE_LOCAL_ENCODING`，或在配置中[配置](/docs/#configure)一个 `local` 类型的远程存储，并在那里设置 `encoding` 选项。

这样做的风险是，如果你的云存储中有一个文件名包含常规（半角）`:`、`*` 和 `?`，而你尝试将其下载到 Windows 文件系统，这将失败。这些字符在 Windows 文件名中无效，而你已告诉 rclone 不要通过将它们转换为有效的全角变体来解决此问题。

### MIME 类型

MIME 类型（也称为媒体类型）使用简单的文本分类来对文档类型进行分类，例如 `text/html` 或 `application/pdf`。

某些云存储系统支持读取（`R`）对象的 MIME 类型，某些支持写入（`W`）对象的 MIME 类型。

如果你直接从存储系统向 HTTP 提供文件服务，MIME 类型可能很重要。

如果你从支持读取（`R`）的远程存储复制到支持写入（`W`）的远程存储，rclone 将保留 MIME 类型。否则，MIME 类型将从扩展名猜测，或由远程存储本身分配。

### 元数据

后端可能支持也可能不支持读取或写入元数据。它们可能支持读取和写入系统元数据（该后端固有的元数据）和/或用户元数据（通用元数据）。

元数据支持级别如下：

| 键 | 说明 |
|-----|------|
| `R` | 仅文件上的只读系统元数据 |
| `RW` | 仅文件上的读写系统元数据 |
| `RWU` | 仅文件上的读写系统元数据以及读写用户元数据 |
| `DR` | 文件和目录上的只读系统元数据 |
| `DRW` | 文件和目录上的读写系统元数据 |
| `DRWU` | 文件和目录上的读写系统元数据以及读写用户元数据 |

更多信息请参见[元数据文档](/docs/#metadata)。

## 可选功能

所有 rclone 远程存储都支持基本命令集。其他功能取决于后端特定的能力。

在技能转换期间从 `testdata/rclone/docs/data/backends/*.yaml` 生成。

| 名称 | Purge | Copy | Move | DirMove | CleanUp | ListR | StreamUpload | MultithreadUpload | LinkSharing | About | EmptyDir |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Azure Blob](providers/azureblob.md) | yes | yes | no | no | no | yes | yes | yes | no | no | no |
| [Azure Files](providers/azurefiles.md) | no | yes | yes | yes | no | no | yes | yes | no | yes | yes |
| [B2](providers/b2.md) | yes | yes | no | no | yes | yes | yes | yes | yes | no | no |
| [Box](providers/box.md) | yes | yes | yes | yes | yes | no | yes | no | yes | yes | yes |
| [Cloudinary](providers/cloudinary.md) | no | no | no | no | no | no | no | no | no | no | yes |
| [Doi](https://rclone.org/doi/) | no | no | no | no | no | no | no | no | no | no | no |
| [Drime](providers/drime.md) | yes | yes | yes | yes | no | no | yes | yes | no | yes | yes |
| [Drive](providers/drive.md) | yes | yes | yes | yes | yes | yes | yes | no | yes | yes | yes |
| [Dropbox](providers/dropbox.md) | yes | yes | yes | yes | no | no | yes | no | yes | yes | yes |
| [Fichier](providers/fichier.md) | no | yes | yes | yes | no | no | no | no | yes | yes | yes |
| [Filefabric](providers/filefabric.md) | yes | yes | yes | yes | yes | no | no | no | no | no | yes |
| [Filelu](providers/filelu.md) | yes | no | yes | no | no | no | no | no | no | yes | yes |
| [Filen](providers/filen.md) | yes | no | yes | yes | yes | yes | yes | yes | no | yes | yes |
| [Filescom](providers/filescom.md) | yes | yes | yes | yes | no | no | yes | no | yes | no | yes |
| [FTP](providers/ftp.md) | no | no | yes | yes | no | no | yes | no | no | no | yes |
| [Gofile](providers/gofile.md) | yes | yes | yes | yes | no | yes | yes | no | yes | yes | yes |
| [Google Cloud Storage](providers/googlecloudstorage.md) | no | yes | no | no | no | yes | yes | no | no | no | yes |
| [Google Photos](providers/googlephotos.md) | no | no | no | no | no | no | no | no | no | no | no |
| [HDFS](providers/hdfs.md) | yes | no | yes | yes | no | no | yes | no | no | yes | yes |
| [Hidrive](providers/hidrive.md) | yes | yes | yes | yes | no | no | yes | no | no | no | yes |
| [HTTP](providers/http.md) | no | no | no | no | no | no | yes | no | no | no | yes |
| [Iclouddrive](providers/iclouddrive.md) | no | no | no | no | no | no | no | no | no | no | no |
| [Imagekit](https://rclone.org/imagekit/) | yes | no | no | no | no | no | no | no | yes | no | yes |
| [Internet Archive](providers/internetarchive.md) | no | yes | no | no | yes | yes | no | no | yes | yes | no |
| [Internxt](providers/internxt.md) | no | no | no | no | no | no | no | no | no | yes | yes |
| [Jottacloud](providers/jottacloud.md) | yes | yes | yes | yes | yes | yes | no | no | yes | yes | yes |
| [Koofr](providers/koofr.md) | no | yes | yes | yes | no | no | yes | no | yes | yes | yes |
| [Linkbox](providers/linkbox.md) | yes | no | no | no | no | no | no | no | no | no | yes |
| [Local](providers/local.md) | no | no | yes | yes | no | no | yes | yes | no | yes | yes |
| [Mailru](providers/mailru.md) | yes | yes | yes | yes | yes | no | no | no | yes | yes | yes |
| [Mega](providers/mega.md) | yes | no | yes | yes | yes | no | no | no | yes | yes | yes |
| [Memory](providers/memory.md) | no | yes | no | no | no | yes | yes | no | no | no | no |
| [Netstorage](providers/netstorage.md) | yes | no | no | no | no | yes | yes | no | no | no | yes |
| [Onedrive](providers/onedrive.md) | yes | yes | yes | yes | yes | no | no | no | yes | yes | yes |
| [Opendrive](providers/opendrive.md) | yes | yes | yes | yes | no | no | no | no | no | yes | yes |
| [Oracle Object Storage](https://rclone.org/oracleobjectstorage/) | no | yes | no | no | yes | yes | yes | yes | no | no | no |
| [Pcloud](providers/pcloud.md) | yes | yes | yes | yes | no | yes | no | no | yes | yes | yes |
| [Pikpak](providers/pikpak.md) | yes | yes | yes | yes | yes | no | no | no | yes | yes | yes |
| [Pixeldrain](providers/pixeldrain.md) | yes | no | yes | yes | no | no | yes | no | yes | yes | yes |
| [Premiumizeme](providers/premiumizeme.md) | yes | no | yes | yes | no | no | no | no | yes | yes | yes |
| [Proton Drive](providers/protondrive.md) | yes | no | yes | yes | yes | no | no | no | no | yes | yes |
| [Putio](providers/putio.md) | yes | yes | yes | yes | yes | no | no | no | no | yes | yes |
| [Qingstor](providers/qingstor.md) | no | yes | no | no | yes | yes | no | no | no | no | no |
| [Quatrix](providers/quatrix.md) | yes | yes | yes | yes | no | no | no | no | no | yes | yes |
| [S3](providers/s3.md) | yes | yes | no | no | yes | yes | yes | yes | yes | no | no |
| [Seafile](providers/seafile.md) | yes | yes | yes | yes | yes | yes | yes | no | yes | yes | yes |
| [SFTP](providers/sftp.md) | no | yes | yes | yes | no | no | yes | no | no | yes | yes |
| [Shade](providers/shade.md) | no | no | yes | yes | no | no | no | yes | no | no | yes |
| [Sharefile](providers/sharefile.md) | no | no | no | no | no | no | no | no | no | no | no |
| [Sia](providers/sia.md) | no | no | no | no | no | no | yes | no | no | no | yes |
| [SMB](providers/smb.md) | no | no | yes | yes | no | no | yes | yes | no | yes | yes |
| [Storj](providers/storj.md) | yes | yes | yes | no | no | yes | yes | no | yes | no | no |
| [Sugarsync](providers/sugarsync.md) | yes | yes | yes | yes | no | no | yes | no | yes | no | yes |
| [Swift](providers/swift.md) | yes | yes | no | no | no | yes | yes | no | no | yes | no |
| [Ulozto](providers/ulozto.md) | no | no | yes | yes | no | no | no | no | no | yes | yes |
| [WebDAV](providers/webdav.md) | yes | yes | yes | yes | no | no | no | no | no | yes | yes |
| [Yandex](providers/yandex.md) | yes | yes | yes | yes | yes | no | yes | no | yes | yes | yes |
| [Zoho](providers/zoho.md) | yes | yes | yes | yes | no | no | no | no | no | yes | yes |

### Purge

此操作比仅删除目录中所有文件更快地删除整个目录。

### Copy

在同一远程存储内复制对象时使用。这被称为服务端复制，因此你无需下载再上传即可复制文件。如果你使用 `rclone copy`，或在远程存储不直接支持 `Move` 时使用 `rclone move`，则会使用此功能。

如果服务器不直接支持 `Copy`，则复制操作会先下载文件再重新上传。

### Move

在同一远程存储上移动/重命名对象时使用。这被称为文件的服务端移动。如果服务器不支持 `DirMove`，则在 `rclone move` 中使用此功能。

如果服务器不具备 `Move` 能力，rclone 会通过 `Copy` 然后删除来模拟。如果服务器不支持 `Copy`，rclone 将下载文件并重新上传。

### DirMove

此功能用于实现 `rclone move` 来移动目录（如果可能）。如果不可能，则对每个文件使用 `Move`（这会回退到 `Copy`，然后下载和上传 — 见 `Move` 部分）。

### CleanUp

此功能用于通过 `rclone cleanup` 清空远程存储的回收站。

如果服务器无法执行 `CleanUp`，则 `rclone cleanup` 将返回错误。

‡‡ 注意，虽然 Box 实现了此功能，但它必须逐个删除文件，因此比通过 WebUI 清空回收站更慢。

### ListR

远程存储支持递归列表以快速列出目录下的所有内容。这使 `--fast-list` 标志能够工作。更多详情请参见 [rclone 文档](/docs/#fast-list)。

### StreamUpload

某些远程存储允许在不知道文件大小的情况下上传文件。这允许某些操作无需先将文件缓存到本地磁盘即可工作，例如 `rclone rcat`。

### MultithreadUpload

某些远程存储允许将传输以分块并行方式发送到远程存储。如果支持此功能，rclone 将使用多线程复制来大幅加快文件传输速度。

### LinkSharing

在文件或文件夹上设置必要的权限，并打印一个链接，允许其他人访问它们，即使他们在特定云提供商上没有账户。

### About

Rclone `about` 打印远程存储的配额信息。典型输出包括已用字节、可用字节、配额和回收站中的内容。

如果远程存储不具备 about 功能，`rclone about remote:` 将返回错误。

不具备 about 功能的后端无法确定 rclone 挂载的可用空间，也无法在 rclone union 远程存储中使用 `mfs`（最大可用空间）策略。

参见 [rclone about 命令](https://rclone.org/commands/rclone_about/)

### EmptyDir

远程存储支持空目录。详情请参见[限制](/bugs/#limitations)。大多数基于对象/存储桶的远程存储不支持此功能。
