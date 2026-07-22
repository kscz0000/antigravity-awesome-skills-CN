---
title: "Akamai Netstorage"
description: "rclone 的 Akamai NetStorage 提供方文档"
versionIntroduced: "v1.58"
---

> **官方文档：** [https://rclone.org/netstorage/](https://rclone.org/netstorage/)
# Akamai NetStorage

路径以 `remote:` 形式指定。
你也可以在其中放入子目录，例如 `remote:/path/to/dir`。
如果你拥有 CP code，可以将其作为域名之后的文件夹来使用，格式为
\<domain>\/\<cpcode>\/\<cpcode 内部的子目录>。

例如，常见配置会使用或不使用 CP code：

- **使用 CP code**。`[your-domain-prefix]-nsu.akamaihd.net/123456/subdirectory/`
- **不使用 CP code**。`[your-domain-prefix]-nsu.akamaihd.net`

查看所有存储桶

```console
rclone lsd remote:
```

Netstorage 的初始设置包括获取账户和密钥。
使用 `rclone config` 可引导你完成整个设置流程。

## 配置

下面示例演示如何创建一个名为 `ns1` 的远端。

1. 启动交互式配置流程，输入以下命令：

    ```console
    rclone config
    ```

2. 输入 `n` 创建一个新的远端。

    ```text
    n) New remote
    d) Delete remote
    q) Quit config
    e/n/d/q> n
    ```

3. 在本例中，当出现 name> 提示时，输入 `ns1`。

    ```text
    name> ns1
    ```

4. 输入 `netstorage` 作为要配置的存储类型。

    ```text
    Type of storage to configure.
    Enter a string value. Press Enter for the default ("").
    Choose a number from below, or type in your own value
    XX / NetStorage
       \ "netstorage"
    Storage> netstorage
    ```

5. 在 HTTP 或 HTTPS 协议之间进行选择。大多数用户应选择 HTTPS，
这也是默认值。HTTP 主要用于调试。

    ```text
    Enter a string value. Press Enter for the default ("").
    Choose a number from below, or type in your own value
     1 / HTTP protocol
       \ "http"
     2 / HTTPS protocol
       \ "https"
    protocol> 1
    ```

6. 使用以下格式指定你的 NetStorage 主机、CP code 以及任何必要的内容路径：
`<domain>/<cpcode>/<content>/`

    ```text
    Enter a string value. Press Enter for the default ("").
    host> baseball-nsu.akamaihd.net/123456/content/
    ```

7. 设置 netstorage 账户名

    ```text
    Enter a string value. Press Enter for the default ("").
    account> username
    ```

8. 设置 Netstorage 账户密钥/G2O key，将用于身份验证。
选择 `y` 选项以设置你自己的密码，然后输入你的密钥。
注意：密钥会以十六进制编码加密的形式存储在 `rclone.conf` 文件中。

    ```text
    y) Yes type in my own password
    g) Generate random password
    y/g> y
    Enter the password:
    password:
    Confirm the password:
    password:
    ```

9. 查看摘要并确认你的远端配置。

    ```text
    [ns1]
    type = netstorage
    protocol = http
    host = baseball-nsu.akamaihd.net/123456/content/
    account = username
    secret = *** ENCRYPTED ***
    --------------------
    y) Yes this is OK (default)
    e) Edit this remote
    d) Delete this remote
    y/e/d> y
    ```

这个远端称为 `ns1`，现在可以使用。

## 示例操作

通过这些示例开始使用 rclone 和 NetStorage。有关其他 rclone
命令，请访问 <https://rclone.org/commands/>。

### 查看项目中某个目录的内容

```console
rclone lsd ns1:/974012/testing/
```

### 将本地内容与远端同步

```console
rclone sync . ns1:/974012/testing/
```

### 将本地内容上传到远端

```console
rclone copy notes.txt ns1:/974012/testing/
```

### 删除远端上的内容

```console
rclone delete ns1:/974012/testing/notes.txt
```

### 在 CP code 之间移动或复制内容

你的凭据必须能访问同一远端上的两个 CP code。
你无法在不同的远端之间执行操作。

```console
rclone move ns1:/974012/testing/notes.txt ns1:/974450/testing2/
```

## 功能特性

### 符号链接支持

Netstorage 后端会改变 rclone `--links, -l` 的行为。上传时，
它不再创建 .rclonelink 文件，而是使用 "symlink" API 在远端上创建
相应的符号链接。.rclonelink 文件将不会被创建，
上传会被拦截，只会在远端上创建与源文件同名（无后缀）的符号链接文件。

这将有效地允许 copy/copyto、move/moveto 和 sync 等命令
在本地与远端之间上传和下载包含符号链接的目录。由于 rclone 内部限制，
无法将单个符号链接文件上传到任何远端后端。你随时可以使用 "backend
symlink" 命令在 NetStorage 服务器上创建符号链接，参见下面的 "symlink"
小节。

远端上的单个符号链接文件可以与 "cat"（打印目标名称）、
"delete"（删除符号链接）、copy、copyto
以及 move/moveto 等命令配合使用，从远端下载到本地。注意：远端上的
单个符号链接文件应在指定时包含 .rclonelink 后缀。

**注意**：服务器上绝不能存在带 .rclonelink 后缀的文件，
因为使用 rclone 实际上无法上传/创建带 .rclonelink 后缀的文件，
它只有在通过非 rclone 的方式在远端上手动创建时才可能存在。

### 隐式目录与显式目录

使用 NetStorage 时，目录可以以下面两种形式之一存在：

1. **显式目录（Explicit Directory）**。这是一个你在存储组中
  创建的真实物理目录。
2. **隐式目录（Implicit Directory）**。这是指某个路径中
  并未被物理创建的目录。例如，在上传文件时，目标路径中可以指定
  尚未存在的子目录。NetStorage 会将这些目录创建为"隐式"目录。
  虽然这些目录并未被物理创建，但它们隐式地存在，并且所记录的路径
  与上传的文件相关联。

Rclone 会拦截所有针对 NetStorage 远端的文件上传和 mkdir 命令，
并为上传路径中的每个目录显式地发出 mkdir 命令。这有助于与 SFTP
等其他 Akamai 服务以及 Content Management Shell (CMShell) 之间的互操作。
Rclone 不保证对隐式目录的操作正确性，这些隐式目录可能是通过直接
使用上传 API 创建的。

### `--fast-list` / ListR 支持

NetStorage 远端通过使用 "list" NetStorage API 操作来支持 ListR 功能，
返回指定 CP code 内所有对象的字典序列表，并在遇到子目录时递归进入。

- **Rclone 默认会对某些命令使用 ListR 方法**。诸如 `lsf -R`
等命令默认使用 ListR。要禁用此行为，请包含
`--disable listR` 选项以使用非递归方式列出对象。

- **Rclone 不会对某些命令使用 ListR 方法**。诸如 `sync`
等命令默认不使用 ListR。要强制使用 ListR 方法，请包含
`--fast-list` 选项。

ListR 方法有利有弊，参考 [rclone 文档](https://rclone.org/docs/#fast-list)。
通常情况下，对远端上已有的深层目录树执行 sync 命令时，
使用 "--fast-list" 标志会运行得更快，但代价是会占用更多内存。
它也可能导致更高的 CPU 利用率，但整个任务可以更快完成。

**注意**：存在一个已知限制，当使用 ListR 方法时，"lsf -R" 会将目录中
的文件数和目录大小显示为 -1。如果这些数字在输出中很重要，
解决办法是传入 "--disable listR" 标志。

### 清除（Purge）

NetStorage 远端通过使用 "quick-delete"
NetStorage API 操作来支持清除功能。出于安全考虑，quick-delete 操作默认是禁用的，
可以通过 Akamai 门户为账户启用。Rclone 将首先尝试对 purge 命令
使用 quick-delete 操作，如果该功能被禁用，则会回退到标准的删除方法。

**注意**：在使用 "quick-delete" 之前，请阅读 [NetStorage Usage API](https://learn.akamai.com/en-us/webhelp/netstorage/netstorage-http-api-developer-guide/GUID-15836617-9F50-405A-833C-EA2556756A30.html)
了解相关注意事项。一般来说，使用 quick-delete
方法不会立即删除目录树，被标记为 quick-delete 的对象
可能仍然可以访问。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/netstorage/netstorage.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 netstorage (Akamai NetStorage) 特有的标准选项。

#### --netstorage-host

要连接的 NetStorage 主机的域名+路径。

格式应为 `<domain>/<internal folders>`

属性：

- Config:      host
- Env Var:     RCLONE_NETSTORAGE_HOST
- Type:        string
- Required:    true

#### --netstorage-account

设置 NetStorage 账户名

属性：

- Config:      account
- Env Var:     RCLONE_NETSTORAGE_ACCOUNT
- Type:        string
- Required:    true

#### --netstorage-secret

设置用于身份验证的 NetStorage 账户密钥/G2O key。

请选择 'y' 选项以设置你自己的密码，然后输入你的密钥。

**注意** 输入内容必须进行混淆处理 - 参见 [rclone obscure](/commands/rclone_obscure/)。

属性：

- Config:      secret
- Env Var:     RCLONE_NETSTORAGE_SECRET
- Type:        string
- Required:    true

### 高级选项

以下是 netstorage (Akamai NetStorage) 特有的高级选项。

#### --netstorage-protocol

在 HTTP 或 HTTPS 协议之间选择。

大多数用户应选择 HTTPS，这也是默认值。
HTTP 主要用于调试。

属性：

- Config:      protocol
- Env Var:     RCLONE_NETSTORAGE_PROTOCOL
- Type:        string
- Default:     "https"
- Examples:
  - "http"
    - HTTP 协议
  - "https"
    - HTTPS 协议

#### --netstorage-description

远端的描述。

属性：

- Config:      description
- Env Var:     RCLONE_NETSTORAGE_DESCRIPTION
- Type:        string
- Required:    false

## 后端命令

以下是 netstorage 后端特有的命令。

使用以下方式运行：

```console
rclone backend COMMAND remote:
```

下面的帮助将说明每个命令接受的参数。

参见 [backend](/commands/rclone_backend/) 命令了解如何
传递选项和参数的更多信息。

这些命令可以在运行中的后端上通过 rc 命令
[backend/command](/rc/#backend-command) 执行。

### du

返回指定目录的磁盘使用信息。

```console
rclone backend du remote: [options] [<arguments>+]
```

返回的使用信息包括目标目录以及所有
可能存在的子目录中存储的文件。

### symlink

你可以使用 symlink 操作在 ObjectStore 中创建符号链接。

```console
rclone backend symlink remote: [options] [<arguments>+]
```

所需路径位置（包括适用的子目录）以
将成为符号链接目标的对象结尾（例如 /links/mylink）。
如果适用，请包含对象的文件扩展名。

使用示例：

```console
rclone backend symlink <src> <path>
```

<!-- autogenerated options stop -->