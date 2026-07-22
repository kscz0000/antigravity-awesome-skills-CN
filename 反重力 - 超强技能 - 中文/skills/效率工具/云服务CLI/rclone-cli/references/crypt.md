---
title: "Crypt"
description: "加密覆盖远程存储"
versionIntroduced: "v1.33"
---

> **官方文档：** [https://rclone.org/crypt/](https://rclone.org/crypt/)
# Crypt

Rclone `crypt` 远程存储可对其他远程存储进行加密和解密。

`crypt` 类型的远程存储不直接访问[存储系统](https://rclone.org/overview/)，
而是包装另一个远程存储，由后者访问存储系统。这与 [alias](https://rclone.org/alias/)、
[union](https://rclone.org/union/)、[chunker](https://rclone.org/chunker/)
等的工作方式类似。这种设计使使用非常灵活，因为您可以在任何其他后端之上
添加一层——在此场景下是加密层——甚至可以多层叠加。Rclone 的功能可以像
使用其他远程存储一样使用，例如您可以[挂载](https://rclone.org/commands/rclone_mount/)
一个 crypt 远程存储。

通过 crypt 远程存储访问存储系统实现了客户端加密，这使得将数据保存在您不信任
不会遭到入侵的位置是安全的。当对 `crypt` 远程存储进行操作时，rclone 会根据
需要在本地系统上即时加密（上传前）和解密（下载后），使数据在被包装的远程存储中
保持加密状态。如果您使用 rclone 以外的应用程序访问存储系统，或直接使用 rclone
访问被包装的远程存储，则不会进行任何加密/解密：下载已有内容只会得到加密
（乱码）格式的内容，而您上传的任何内容都*不会*被加密。

该加密使用密钥加密（也称为对称密钥加密）算法，其中密码（或口令）用于生成
真正的加密密钥。密码可由用户提供，也可选择让 rclone 生成。它将以轻度混淆的
形式存储在配置文件中。如果您所处的环境无法保证配置的安全，则应添加
[配置加密](https://rclone.org/docs/#configuration-encryption)作为保护。
只要您拥有此配置文件，就能解密您的数据。如果没有配置文件，只要您记得密码
（或将其保存在安全的地方），就可以重新创建配置并访问已有数据。您也可以在
不同的安装中配置相应的远程存储来访问相同的数据。
请参阅下方关于[更改密码](#changing-password)的指南。

加密使用[加密盐](https://en.wikipedia.org/wiki/Salt_(cryptography))来变换
加密密钥，使相同的字符串可以以不同的方式加密。配置 crypt 远程存储时，
输入盐是可选的，也可以让 rclone 生成唯一盐。如果省略，rclone 使用内置的
唯一字符串。通常在密码学中，盐与加密内容一起存储，用户无需记忆。但在
rclone 中并非如此，因为 rclone 不会在远程存储上存储任何额外信息。使用
自定义盐实际上相当于第二个必须记忆的密码。

[文件内容](#file-encryption)加密使用 [NaCl SecretBox](https://godoc.org/golang.org/x/crypto/nacl/secretbox) 执行，
基于 XSalsa20 密码和 Poly1305 用于完整性验证。[名称](#name-encryption)（文件名和目录名）
默认也会被加密，但这有一些影响，因此可以被关闭。

## 配置

以下是如何创建名为 `secret` 的远程存储的示例。

要使用 `crypt`，首先设置底层远程存储。按照特定后端的 `rclone config` 说明操作。

在配置 crypt 远程存储之前，请检查底层远程存储是否正常工作。在此示例中，
底层远程存储名为 `remote`。我们将在此远程存储中配置一个路径 `path` 来存放
加密内容。`remote:path` 内的所有内容将被加密，之外的内容则不会。

使用 `rclone config` 配置 `crypt`。在此示例中，`crypt` 远程存储名为
`secret`，以区别于底层的 `remote`。

配置完成后，您可以像使用其他远程存储一样使用名为 `secret` 的 crypt 远程存储，
例如 `rclone copy D:\docs secret:\docs`，rclone 将根据需要即时加密和解密。
如果您直接访问被包装的远程存储 `remote:path`，则会绕过加密，读取到的任何内容
都是加密形式的，写入的任何内容都是未加密的。为避免问题，最好为加密内容
配置专用路径，并仅通过 crypt 远程存储访问它。

```text
No remotes found, make a new one\?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> secret
Type of storage to configure.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
[snip]
XX / Encrypt/Decrypt a remote
   \ "crypt"
[snip]
Storage> crypt
** See help for crypt backend at: https://rclone.org/crypt/ **

Remote to encrypt/decrypt.
Normally should contain a ':' and a path, eg "myremote:path/to/dir",
"myremote:bucket" or maybe "myremote:" (not recommended).
Enter a string value. Press Enter for the default ("").
remote> remote:path
How to encrypt the filenames.
Enter a string value. Press Enter for the default ("standard").
Choose a number from below, or type in your own value.
   / Encrypt the filenames.
 1 | See the docs for the details.
   \ "standard"
 2 / Very simple filename obfuscation.
   \ "obfuscate"
   / Don't encrypt the file names.
 3 | Adds a ".bin" extension only.
   \ "off"
filename_encryption>
Option to either encrypt directory names or leave them intact.

NB If filename_encryption is "off" then this option will do nothing.
Enter a boolean value (true or false). Press Enter for the default ("true").
Choose a number from below, or type in your own value
 1 / Encrypt directory names.
   \ "true"
 2 / Don't encrypt directory names, leave them intact.
   \ "false"
directory_name_encryption>
Password or pass phrase for encryption.
y) Yes type in my own password
g) Generate random password
y/g> y
Enter the password:
password:
Confirm the password:
password:
Password or pass phrase for salt. Optional but recommended.
Should be different to the previous password.
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank (default)
y/g/n> g
Password strength in bits.
64 is just about memorable
128 is secure
1024 is the maximum
Bits> 128
Your password is: JAsJvRcgR-_veXNfy_sGmQ
Use this password? Please note that an obscured version of this
password (and not the password itself) will be stored under your
configuration file, so keep this generated password in a safe place.
y) Yes (default)
n) No
y/n>
Edit advanced config? (y/n)
y) Yes
n) No (default)
y/n>
Remote config
--------------------
[secret]
type = crypt
remote = remote:path
password = *** ENCRYPTED ***
password2 = *** ENCRYPTED ***
--------------------
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d>
```

**重要提示** 存储在 `rclone.conf` 中的 crypt 密码仅经过轻度混淆。
这只能防止粗略查看。除非指定了 `rclone.conf` 的
[配置加密](https://rclone.org/docs/#configuration-encryption)，否则它并不安全。

建议使用较长的口令，或者 `rclone config` 可以生成随机口令。

混淆密码使用 AES-CTR 和静态密钥创建。IV（nonce）原样存储在混淆密码的
开头。此静态密钥在所有版本的 rclone 之间共享。

如果您在其他地方使用相同的密码/口令重新配置 rclone，则是兼容的，
但由于盐值不同，混淆版本会有所不同。

Rclone 不加密以下内容：

- 文件长度 - 可在 16 字节内计算
- 修改时间 - 用于同步

### 指定远程存储

配置要加密/解密的远程存储时，您可以指定 rclone 接受作为其他命令
源/目标的任何字符串。

主要用例是指向已配置远程存储中的路径（例如 `remote:path/to/dir` 或
`remote:bucket`），使得远程不受信任位置中的数据可以加密存储。

您也可以指定本地文件系统路径，例如 Linux 上的 `/path/to/dir`，
Windows 上的 `C:\path\to\dir`。通过创建指向此类本地文件系统路径的
crypt 远程存储，您可以将 rclone 用作纯本地文件加密工具，例如在可移动
USB 驱动器上保存加密文件。

**注意**：不包含 `:` 的字符串会被 rclone 视为本地文件系统中的相对路径。
例如，如果您输入名称 `remote` 而不带尾部的 `:`，它将被视为当前目录下
名为 "remote" 的子目录。

如果指定了路径 `remote:path/to/dir`，rclone 会在远程存储的
`path/to/dir` 中存储加密文件。启用文件名加密时，保存到
`secret:subdir/subfile` 的文件存储在未加密路径 `path/to/dir` 中，
但 `subdir/subpath` 部分是加密的。

您指定的路径不必存在，rclone 会在需要时创建它。

如果您打算既直接使用被包装的远程存储保存未加密内容，又通过 crypt 远程存储
保存加密内容，建议将 crypt 远程存储指向被包装远程存储中的独立目录。
如果您使用基于桶的存储系统（例如 Swift、S3、Google Compute Storage、B2），
通常建议将 crypt 远程存储包装在特定桶（`s3:bucket`）周围。
如果包装整个存储根（`s3:`），并使用可选的文件名加密，rclone 将加密桶名。

### 更改密码

如果密码或包含密码轻度混淆形式的配置文件泄露，您需要使用新密码重新加密数据。
由于 rclone 使用密钥加密，其中加密密钥直接由保存在客户端的密码生成，因此
无法更改已加密内容的密码/密钥。仅更改已有 crypt 远程存储配置的密码意味着
您将无法再解密任何之前加密的内容。唯一的可能就是通过使用新密码配置的 crypt
远程存储重新上传所有内容。

根据数据大小、带宽、存储配额等，您可以采取不同的方法：

- 如果您在其他位置拥有所有内容的副本，例如本地系统上，您可以删除所有先前
  加密的文件，更改已配置 crypt 远程存储的密码（或删除并重新创建 crypt 配置），
  然后从替代位置重新上传所有内容。
- 如果存储系统上有足够的空间，您可以创建一个新的 crypt 远程存储指向同一后端上
  的独立目录，然后使用 rclone 将所有内容从原始 crypt 远程存储复制到新的远程存储，
  从而使用旧密码即时解密所有内容，并使用新密码重新加密。完成后，删除原始 crypt
  远程存储目录，最后删除使用旧密码的 rclone crypt 配置。所有数据将从存储系统
  流出并返回，因此如果存储系统有上传和下载配额，您只能获得一半的带宽，且会被
  收取双倍费用。

**注意**：与随机密码生成器相关的安全问题已在 rclone 1.53.3 版本
（2020-11-19 发布）中修复。rclone 1.49.0 版本（2019-08-26 发布）到
1.53.2 版本（2020-10-26 发布）中由 rclone config 生成的密码不被视为安全，
应予更改。如果您自行设定了密码，或使用早于 1.49.0 或晚于 1.53.2 的 rclone
版本生成密码，则*不受*此问题影响。请参阅 [issue #4783](https://github.com/rclone/rclone/issues/4783)
了解更多详情，以及可用于检查您是否受影响的工具。

### 示例

使用"标准"文件名加密创建以下文件结构。

```text
plaintext/
├── file0.txt
├── file1.txt
└── subdir
    ├── file2.txt
    ├── file3.txt
    └── subsubdir
        └── file4.txt
```

将这些文件复制到远程存储并列出

```console
$ rclone -q copy plaintext secret:
$ rclone -q ls secret:
        7 file1.txt
        6 file0.txt
        8 subdir/file2.txt
       10 subdir/subsubdir/file4.txt
        9 subdir/file3.txt
```

crypt 远程存储看起来如下

```console
$ rclone -q ls remote:path
       55 hagjclgavj2mbiqm6u6cnjjqcg
       54 v05749mltvv1tf4onltun46gls
       57 86vhrsv86mpbtd3a0akjuqslj8/dlj7fkq4kdq72emafg7a7s41uo
       58 86vhrsv86mpbtd3a0akjuqslj8/7uu829995du6o42n32otfhjqp4/b9pausrfansjth5ob3jkdqd4lc
       56 86vhrsv86mpbtd3a0akjuqslj8/8njh1sk437gttmep3p70g81aps
```

目录结构被保留

```console
$ rclone -q ls secret:subdir
        8 file2.txt
        9 file3.txt
       10 subsubdir/file4.txt
```

不启用文件名加密时，底层名称会添加 `.bin` 扩展名。这可以防止云服务商
尝试解释文件内容。

```console
$ rclone -q ls remote:path
       54 file0.txt.bin
       57 subdir/file3.txt.bin
       56 subdir/file2.txt.bin
       58 subdir/subsubdir/file4.txt.bin
       55 file1.txt.bin
```

### 文件名加密模式

关闭（Off）

- 不隐藏文件名或目录结构
- 允许更长的文件名（约 246 个字符）
- 可以使用子路径和复制单个文件

标准（Standard）

- 文件名被加密
- 文件名不能太长（约 143 个字符）
- 可以使用子路径和复制单个文件
- 目录结构可见
- 相同的文件名将产生相同的上传名称
- 可以使用快捷方式缩短目录递归

混淆（Obfuscation）

这是一种简单的文件名"旋转"，每个文件根据文件名有一个旋转距离。
rclone 将距离存储在文件名开头。一个名为 "hello" 的文件可能变成
"53.jgnnq"。

混淆不是文件名的强加密，但会妨碍自动扫描工具识别文件名模式。
它是"关闭"和"标准"之间的折中方案，允许更长的路径段名称。

某些基于 unicode 的文件名可能存在混淆较弱的情况，可能将小写
字符映射为大写等效字符。

混淆不能被视为提供强保护。

- 文件名仅轻度混淆
- 文件名可以比标准加密更长
- 可以使用子路径和复制单个文件
- 目录结构可见
- 相同的文件名将产生相同的上传名称

云存储系统对文件名长度和总路径长度有限制，使用"标准"文件名加密时
rclone 更有可能超出这些限制。当文件名为 143 个字符或更少时，
无论云存储提供商如何，都不应遇到问题。

现在提供了一个实验性高级选项 `filename_encoding` 来在一定程度上解决
此问题。对于文件名区分大小写的云存储系统（例如 Google Drive），
可以使用 `base64` 来缩短文件名长度。对于内部使用 UTF-16 存储文件名
的云存储系统（例如 OneDrive、Dropbox、Box），可以使用 `base32768`
来大幅缩短文件名长度。

未来的 rclone 文件名加密模式可能会容忍后端提供商的路径长度限制。

### 目录名加密

Crypt 提供加密目录名或保持原样的选项。有两个选项：

True（真）

加密包括目录名在内的整个文件路径
示例：
`1/12/123.txt` 被加密为
`p0e52nreeaj0a5ea7s64m4j72s/l42g6771hnv3an9cgc8cr2n1ng/qgm4avr35m5loi1th53ato71v0`

False（假）

仅加密文件名，跳过目录名
示例：
`1/12/123.txt` 被加密为
`1/12/qgm4avr35m5loi1th53ato71v0`

### 修改时间和哈希值

Crypt 使用底层远程存储存储修改时间，因此支持情况取决于底层远程存储。

Crypt 不存储哈希值。但是数据完整性由极其强大的加密认证器保护。

请使用 `rclone cryptcheck` 命令来检查加密远程存储的完整性，
而不是 `rclone check`，后者无法正确检查校验和。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/crypt/crypt.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 crypt（加密/解密远程存储）的特有标准选项。

#### --crypt-remote

要加密/解密的远程存储。

通常应包含 ':' 和路径，例如 "myremote:path/to/dir"、"myremote:bucket"
或可能是 "myremote:"（不推荐）。

属性：

- Config:      remote
- Env Var:     RCLONE_CRYPT_REMOTE
- Type:        string
- Required:    true

#### --crypt-filename-encryption

如何加密文件名。

属性：

- Config:      filename_encryption
- Env Var:     RCLONE_CRYPT_FILENAME_ENCRYPTION
- Type:        string
- Default:     "standard"
- 示例：
  - "standard"
    - 加密文件名。
    - 详见文档。
  - "obfuscate"
    - 非常简单的文件名混淆。
  - "off"
    - 不加密文件名。
    - 仅添加 ".bin" 或 "suffix" 扩展名。

#### --crypt-directory-name-encryption

加密目录名或保持原样的选项。

注意 如果 filename_encryption 为 "off"，则此选项无效。

属性：

- Config:      directory_name_encryption
- Env Var:     RCLONE_CRYPT_DIRECTORY_NAME_ENCRYPTION
- Type:        bool
- Default:     true
- 示例：
  - "true"
    - 加密目录名。
  - "false"
    - 不加密目录名，保持原样。

#### --crypt-password

用于加密的密码或口令。

**注意** 此输入必须经过混淆 - 参见 [rclone obscure](/commands/rclone_obscure/)。

属性：

- Config:      password
- Env Var:     RCLONE_CRYPT_PASSWORD
- Type:        string
- Required:    true

#### --crypt-password2

用于盐的密码或口令。

可选但建议使用。
应与前面的密码不同。

**注意** 此输入必须经过混淆 - 参见 [rclone obscure](/commands/rclone_obscure/)。

属性：

- Config:      password2
- Env Var:     RCLONE_CRYPT_PASSWORD2
- Type:        string
- Required:    false

### 高级选项

以下是 crypt（加密/解密远程存储）的特有高级选项。

#### --crypt-server-side-across-configs

已弃用：请改用 --server-side-across-configs。

允许服务端操作（例如 copy）跨不同的 crypt 配置工作。

通常这不是您想要的选项，但如果您有两个指向同一后端的 crypt，可以使用它。

例如，这可用于更改文件名加密类型而无需重新上传所有数据。
只需创建两个指向不同目录的 crypt 后端，仅更改一个参数，
然后使用 rclone move 在两个 crypt 远程存储之间移动文件。

属性：

- Config:      server_side_across_configs
- Env Var:     RCLONE_CRYPT_SERVER_SIDE_ACROSS_CONFIGS
- Type:        bool
- Default:     false

#### --crypt-show-mapping

对于列出的所有文件，显示名称如何加密。

如果设置了此标志，则对于远程存储被要求列出的每个文件，它将记录（INFO 级别）
一行，说明解密文件名和加密文件名。

这使您可以在需要处理加密文件名或进行调试时，了解哪些加密名称对应哪些
解密名称。

属性：

- Config:      show_mapping
- Env Var:     RCLONE_CRYPT_SHOW_MAPPING
- Type:        bool
- Default:     false

#### --crypt-no-data-encryption

加密文件数据或保持未加密的选项。

属性：

- Config:      no_data_encryption
- Env Var:     RCLONE_CRYPT_NO_DATA_ENCRYPTION
- Type:        bool
- Default:     false
- 示例：
  - "true"
    - 不加密文件数据，保持未加密状态。
  - "false"
    - 加密文件数据。

#### --crypt-pass-bad-blocks

如果设置，将把坏块作为全 0 传递。

正常操作中不应设置此项，仅在尝试恢复有错误的加密文件且希望尽可能多地
恢复文件内容时才应设置。

属性：

- Config:      pass_bad_blocks
- Env Var:     RCLONE_CRYPT_PASS_BAD_BLOCKS
- Type:        bool
- Default:     false

#### --crypt-strict-names

如果设置，当 crypt 遇到无法解密的文件名时将引发错误。

（默认情况下，rclone 只会记录一条 NOTICE 并正常继续。）
这可能发生在加密和未加密文件存储在同一目录中的情况（不推荐）。
它也可能表明存在应予调查的更严重问题。

属性：

- Config:      strict_names
- Env Var:     RCLONE_CRYPT_STRICT_NAMES
- Type:        bool
- Default:     false

#### --crypt-filename-encoding

如何将加密后的文件名编码为文本字符串。

此选项可以帮助缩短加密文件名。合适的选项取决于您的远程存储计算文件名
长度的方式以及是否区分大小写。

属性：

- Config:      filename_encoding
- Env Var:     RCLONE_CRYPT_FILENAME_ENCODING
- Type:        string
- Default:     "base32"
- 示例：
  - "base32"
    - 使用 base32 编码。适用于所有远程存储。
  - "base64"
    - 使用 base64 编码。适用于区分大小写的远程存储。
  - "base32768"
    - 使用 base32768 编码。适用于您的远程存储按 UTF-16 或
    - Unicode 码点而非 UTF-8 字节长度计数的场景。（例如 Onedrive、Dropbox）

#### --crypt-suffix

如果设置，将覆盖默认的 ".bin" 后缀。

将后缀设置为 "none" 将产生空后缀。当路径长度至关重要时，这可能很有用。

属性：

- Config:      suffix
- Env Var:     RCLONE_CRYPT_SUFFIX
- Type:        string
- Default:     ".bin"

#### --crypt-description

远程存储的描述。

属性：

- Config:      description
- Env Var:     RCLONE_CRYPT_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

底层远程存储支持的任何元数据都可以读取和写入。

请参阅[元数据](/docs/#metadata)文档了解更多信息。

## 后端命令

以下是 crypt 后端特有的命令。

运行方式：

```console
rclone backend COMMAND remote:
```

下面的帮助将解释每个命令接受哪些参数。

请参阅 [backend](/commands/rclone_backend/) 命令了解如何传递选项和参数。

这些可以在运行中的后端上使用 rc 命令
[backend/command](/rc/#backend-command) 来运行。

### encode

编码给定的文件名。

```console
rclone backend encode remote: [options] [<arguments>+]
```

这将编码作为参数给定的文件名，返回编码结果的字符串列表。

使用示例：

```console
rclone backend encode crypt: file1 [file2...]
rclone rc backend/command command=encode fs=crypt: file1 [file2...]
```

### decode

解码给定的文件名。

```console
rclone backend decode remote: [options] [<arguments>+]
```

这将解码作为参数给定的文件名，返回解码结果的字符串列表。
如果任何输入无效，将返回错误。

使用示例：

```console
rclone backend decode crypt: encryptedfile1 [encryptedfile2...]
rclone rc backend/command command=decode fs=crypt: encryptedfile1 [encryptedfile2...]
```

<!-- autogenerated options stop -->

## 备份加密远程存储

如果您希望备份加密远程存储，建议对加密文件使用 `rclone sync`，
并确保新加密远程存储中的密码相同。

这将带来以下优势

- `rclone sync` 在复制时会检查校验和
- 您可以在加密远程存储之间使用 `rclone check`
- 您不需要进行不必要的解密和加密

例如，假设您的原始远程存储在 `remote:`，加密版本在 `eremote:`，
路径为 `remote:crypt`。然后您设置新的远程存储 `remote2:`，
然后设置加密版本 `eremote2:`，路径为 `remote2:crypt`，
使用与 `eremote:` 相同的密码。

同步两个远程存储的命令为

```console
rclone sync --interactive remote:crypt remote2:crypt
```

检查完整性的命令为

```console
rclone check remote:crypt remote2:crypt
```

## 文件格式

### 文件加密

文件以 1:1 的方式从源文件加密到目标对象。文件包含头部并分为数据块。

#### 头部

- 8 字节魔术字符串 `RCLONE\x00\x00`
- 24 字节 Nonce（IV）

初始 nonce 由操作系统的加密强随机数生成器生成。每读取一个数据块
nonce 递增，确保每个写入块的 nonce 唯一。nonce 被重复使用的可能性
微乎其微。如果您写入一艾字节的数据（10¹⁸ 字节），重复使用 nonce
的概率约为 2×10⁻³²。

#### 数据块

每个数据块包含 64 KiB 的数据，最后一个块可能包含更少的数据。
数据块采用标准 NaCl SecretBox 格式。SecretBox 使用 XSalsa20 和
Poly1305 来加密和验证消息。

每个数据块包含：

- 16 字节 Poly1305 认证器
- 1 - 65536 字节 XSalsa20 加密数据

选择 64k 数据块大小是因为它是性能最佳的数据块大小（低于此大小时认证器
耗时过多，高于此大小时由于缓存效应性能下降）。注意这些数据块在内存中
缓冲，因此不能太大。

这使用从用户密码派生的 32 字节（256 位）密钥。

#### 示例

1 字节文件将加密为

- 32 字节头部
- 17 字节数据块

共 49 字节

1 MiB（1048576 字节）文件将加密为

- 32 字节头部
- 16 个 65568 字节的数据块

共 1049120 字节（0.05% 的开销）。这是大文件的开销。

### 名称加密

文件名逐段加密 - 路径被拆分为由 `/` 分隔的字符串，这些字符串分别加密。

文件段在加密前使用 PKCS#7 填充到 16 字节的倍数。

然后使用 AES 256 位密钥通过 EME 加密。EME（ECB-Mix-ECB）是一种宽块
加密模式，出自 Halevi 和 Rogaway 2003 年的论文"A Parallelizable
Enciphering Mode"。

这实现了确定性加密，这正是我们需要的 - 相同的文件名必须加密为相同的
结果，否则我们无法在云存储系统中找到它。

这意味着

- 同名的文件名将加密为相同的结果
- 以相同内容开头的文件名不会有共同前缀

这使用从用户密码派生的 32 字节密钥（256 位）和 16 字节 IV（128 位）。

加密后，使用 RFC4648 中描述的标准 `base32` 编码的修改版本输出。
标准编码在两个方面被修改：

- 变为小写（没人喜欢大写文件名！）
- 去除填充字符 `=`

使用 `base32` 而非更高效的 `base64`，是为了让 rclone 可以在
不区分大小写的远程存储上使用（例如 Windows、Box、Dropbox、Onedrive 等）。

### 密钥派生

Rclone 使用 `scrypt`，参数为 `N=16384, r=8, p=1`，以及可选的
用户提供的盐（password2）来派生所需的 32+32+16 = 80 字节密钥材料。
如果用户不提供盐，rclone 使用内部盐。

`scrypt` 使得对 rclone 加密数据进行字典攻击变得不可行。
要获得对此的完整保护，您应始终使用盐。

## 另请参阅

- [rclone cryptdecode](/commands/rclone_cryptdecode/) - 显示加密文件名
  的正向/反向映射。
