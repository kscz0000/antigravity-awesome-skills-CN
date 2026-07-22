---
title: "Storj"
description: "Storj 的 Rclone 文档"
aliases:
  - tardigrade
versionIntroduced: "v1.52"
---

> **官方文档：** [https://rclone.org/storj/](https://rclone.org/storj/)
# Storj

[Storj](https://storj.io) 正在重新定义云存储，以可持续且经济的方式支持数据的未来。Storj 利用全球大量未被充分利用的资源，提供更安全、更持久、更高性能的服务。使用 Storj 可降低高达 90% 的成本并减少碳排放。

Storj 是一种加密、安全且高性价比的对象存储服务，支持以去中心化方式存储、备份和归档大量数据。

## 后端选项

Storj 既可以使用此原生后端，也可以通过[使用 Storj S3 兼容网关的 s3 后端](/s3/#storj)（共享或私有）来使用。

使用此原生后端可利用客户端加密，并获得最佳的下载性能。上传时数据会在本地进行纠删码编码，因此 1GB 的上传会导致 2.68GB 的数据被上传到网络中的存储节点。

使用 s3 后端和 S3 兼容的托管网关可提高上传性能，并减轻系统和网络的负载。上传时数据会在服务端进行加密和纠删码编码，因此 1GB 的上传只需上传 1GB 的数据到网络中的存储节点。

更详细的对比：

- 特性：
  - *Storj 后端*：使用原生 RPC 协议，直接连接托管数据的存储节点。编解码需要更多 CPU 资源，且存在网络放大效应（尤其是上传时），会使用大量 TCP 连接
  - *S3 后端*：通过共享网关使用 S3 兼容的 HTTP REST API。没有网络放大效应，但性能取决于共享网关，且加密密钥与网关共享
- 典型用途：
  - *Storj 后端*：具有足够资源、网速和连接性的服务器环境和桌面端——以及需要 Storj 客户端加密的应用场景
  - *S3 后端*：资源、网速或连接性有限的桌面端及类似环境
- 安全性：
  - *Storj 后端*：**更强**。私有加密密钥无需离开本地计算机。
  - *S3 后端*：**较弱**。私有加密密钥[与](https://docs.storj.io/dcs/api-reference/s3-compatible-gateway#security-and-encryption)托管网关的认证服务共享，在那里以加密形式存储。与 rclone [crypt](/crypt) 后端结合使用时可增强安全性。
- 带宽使用（上传）：
  - *Storj 后端*：**较高**。由于数据在客户端进行纠删码编码，原始数据和校验数据都需要上传，上传量约为原始数据的 2.7 倍。客户端可能先以更多节点（约 3.7 倍）开始上传，然后放弃/停止较慢的上传。
  - *S3 后端*：**正常**。仅上传原始数据，纠删码编码在网关上完成。
- 带宽使用（下载）：
  - *Storj 后端*：**接近正常**。仅需最少量的数据，但为避免极慢的数据提供者，会多使用少量数据源并忽略最慢的源（最多 1.2 倍开销）。
  - *S3 后端*：**正常**。仅下载原始数据，纠删码编码在共享网关上完成。
- CPU 使用：
  - *Storj 后端*：**较高**，但更可预测。纠删码编码和加密/解密在本地进行，需要显著的 CPU 资源。
  - *S3 后端*：**较低**。纠删码编码和加密/解密在共享 S3 网关上进行（因此取决于网关当前的负载）
- TCP 连接使用：
  - *Storj 后端*：**高**。需要与每个 Storj 节点建立直连，每个 64MB 段上传时需要 110 个连接，下载时需要 35 个。并非所有连接都处于活跃使用状态（慢连接会被修剪），但它们都会被打开。可能需要[调整最大打开文件数限制](/storj/#known-issues)。
  - *S3 后端*：**正常**。每个下载/上传线程仅需一个到共享网关的连接。
- 整体性能：
  - *Storj 后端*：在资源充足（CPU 和带宽）的情况下，Storj 后端可提供高达 2 倍的性能优势。数据直接从客户端下载/上传到存储节点，而非通过网关中转。
  - *S3 后端*：在 CPU 和网络带宽有限的边缘设备上可能更快，因为共享的 S3 兼容网关负责加密/解密和纠删码编码，且没有下载/上传放大效应。
- 去中心化程度：
  - *Storj 后端*：**高**。数据直接从分布式云存储提供者下载。
  - *S3 后端*：**低**。需要运行 S3 网关（自托管或 Storj 托管）。
- 限制：
  - *Storj 后端*：无法在不下载的情况下执行 `rclone checksum`，因为上传时不会计算校验和元数据
  - *S3 后端*：加密密钥与网关共享

## 配置

要创建新的 Storj 配置，您需要以下之一：

- 他人共享给您的访问授权（Access Grant）。
- 您所属 Storj 项目的 [API 密钥](https://documentation.storj.io/getting-started/uploading-your-first-object/create-an-api-key)。

以下是如何创建名为 `remote` 的远程存储的示例。首先运行：

```console
rclone config
```

这将引导您完成交互式配置过程：

### 使用访问授权配置

```text
No remotes found, make a new one\?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> remote
Type of storage to configure.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
[snip]
XX / Storj Decentralized Cloud Storage
   \ "storj"
[snip]
Storage> storj
** See help for storj backend at: https://rclone.org/storj/ **

Choose an authentication method.
Enter a string value. Press Enter for the default ("existing").
Choose a number from below, or type in your own value
 1 / Use an existing access grant.
   \ "existing"
 2 / Create a new access grant from satellite address, API key, and passphrase.
   \ "new"
provider> existing
Access Grant.
Enter a string value. Press Enter for the default ("").
access_grant> your-access-grant-received-by-someone-else
Remote config
Configuration complete.
Options:
- type: storj
- access_grant: your-access-grant-received-by-someone-else
Keep this "remote" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

### 使用 API 密钥和密码短语配置

```text
No remotes found, make a new one\?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> remote
Type of storage to configure.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
[snip]
XX / Storj Decentralized Cloud Storage
   \ "storj"
[snip]
Storage> storj
** See help for storj backend at: https://rclone.org/storj/ **

Choose an authentication method.
Enter a string value. Press Enter for the default ("existing").
Choose a number from below, or type in your own value
 1 / Use an existing access grant.
   \ "existing"
 2 / Create a new access grant from satellite address, API key, and passphrase.
   \ "new"
provider> new
Satellite Address. Custom satellite address should match the format: `<nodeid>@<address>:<port>`.
Enter a string value. Press Enter for the default ("us1.storj.io").
Choose a number from below, or type in your own value
 1 / US1
   \ "us1.storj.io"
 2 / EU1
   \ "eu1.storj.io"
 3 / AP1
   \ "ap1.storj.io"
satellite_address> 1
API Key.
Enter a string value. Press Enter for the default ("").
api_key> your-api-key-for-your-storj-project
Encryption Passphrase. To access existing objects enter passphrase used for uploading.
Enter a string value. Press Enter for the default ("").
passphrase> your-human-readable-encryption-passphrase
Remote config
Configuration complete.
Options:
- type: storj
- satellite_address: 12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S@us1.storj.io:7777
- api_key: your-api-key-for-your-storj-project
- passphrase: your-human-readable-encryption-passphrase
- access_grant: the-access-grant-generated-from-the-api-key-and-passphrase
Keep this "remote" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/storj/storj.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 Storj（Storj 去中心化云存储）特有的标准选项。

#### --storj-provider

选择认证方式。

属性：

- 配置项：      provider
- 环境变量：     RCLONE_STORJ_PROVIDER
- 类型：        string
- 默认值：     "existing"
- 示例：
  - "existing"
    - 使用已有的访问授权。
  - "new"
    - 通过卫星地址、API 密钥和密码短语创建新的访问授权。

#### --storj-access-grant

访问授权。

属性：

- 配置项：      access_grant
- 环境变量：     RCLONE_STORJ_ACCESS_GRANT
- 提供者：    existing
- 类型：        string
- 必填：    false

#### --storj-satellite-address

卫星地址。

自定义卫星地址应匹配格式：`<nodeid>@<address>:<port>`。

属性：

- 配置项：      satellite_address
- 环境变量：     RCLONE_STORJ_SATELLITE_ADDRESS
- 提供者：    new
- 类型：        string
- 默认值：     "us1.storj.io"
- 示例：
  - "us1.storj.io"
    - US1
  - "eu1.storj.io"
    - EU1
  - "ap1.storj.io"
    - AP1

#### --storj-api-key

API 密钥。

属性：

- 配置项：      api_key
- 环境变量：     RCLONE_STORJ_API_KEY
- 提供者：    new
- 类型：        string
- 必填：    false

#### --storj-passphrase

加密密码短语。

要访问已有对象，请输入上传时使用的密码短语。

属性：

- 配置项：      passphrase
- 环境变量：     RCLONE_STORJ_PASSPHRASE
- 提供者：    new
- 类型：        string
- 必填：    false

### 高级选项

以下是 Storj（Storj 去中心化云存储）特有的高级选项。

#### --storj-description

远程存储的描述。

属性：

- 配置项：      description
- 环境变量：     RCLONE_STORJ_DESCRIPTION
- 类型：        string
- 必填：    false

<!-- autogenerated options stop -->

## 使用方法

路径指定为 `remote:bucket`（或 `lsf` 命令使用 `remote:`）。也可以包含子目录，例如 `remote:bucket/path/to/dir`。

配置完成后，您可以像这样使用 `rclone`。

### 创建新存储桶

使用 `mkdir` 命令创建新存储桶，例如 `bucket`。

```console
rclone mkdir remote:bucket
```

### 列出所有存储桶

使用 `lsf` 命令列出所有存储桶。

```console
rclone lsf remote:
```

注意命令行末尾的冒号（`:`）字符。

### 删除存储桶

使用 `rmdir` 命令删除空存储桶。

```console
rclone rmdir remote:bucket
```

使用 `purge` 命令删除非空存储桶及其所有内容。

```console
rclone purge remote:bucket
```

### 上传对象

使用 `copy` 命令上传对象。

```console
rclone copy --progress /home/local/directory/file.ext remote:bucket/path/to/dir/
```

`--progress` 标志用于显示进度信息。如果不需要此信息，可以移除。

使用本地路径中的文件夹可上传其中的所有对象。

```console
rclone copy --progress /home/local/directory/ remote:bucket/path/to/dir/
```

仅会复制已修改的文件。

### 列出对象

使用 `ls` 命令递归列出存储桶中的所有对象。

```console
rclone ls remote:bucket
```

在远程路径中添加文件夹可递归列出该文件夹中的所有对象。

```console
$ rclone ls remote:bucket
/path/to/dir/
```

使用 `lsf` 命令非递归地列出存储桶或文件夹中的所有对象。

```console
rclone lsf remote:bucket/path/to/dir/
```

### 下载对象

使用 `copy` 命令下载对象。

```console
rclone copy --progress remote:bucket/path/to/dir/file.ext /home/local/directory/
```

`--progress` 标志用于显示进度信息。如果不需要此信息，可以移除。

使用远程路径中的文件夹可下载其中的所有对象。

```console
rclone copy --progress remote:bucket/path/to/dir/ /home/local/directory/
```

### 删除对象

使用 `deletefile` 命令删除单个对象。

```console
rclone deletefile remote:bucket/path/to/dir/file.ext
```

使用 `delete` 命令删除文件夹中的所有对象。

```console
rclone delete remote:bucket/path/to/dir/
```

### 打印对象总大小

使用 `size` 命令打印存储桶或文件夹中对象的总大小。

```console
rclone size remote:bucket/path/to/dir/
```

### 同步两个位置

使用 `sync` 命令将源同步到目标，仅修改目标端，删除多余的文件。

```console
rclone sync --interactive --progress /home/local/directory/ remote:bucket/path/to/dir/
```

`--progress` 标志用于显示进度信息。如果不需要此信息，可以移除。

由于此操作可能导致数据丢失，请先使用 `--dry-run` 标志进行测试，以查看具体将被复制和删除的内容。

也可以从 Storj 同步到本地文件系统。

```console
rclone sync --interactive --progress remote:bucket/path/to/dir/ /home/local/directory/
```

或在两个 Storj 存储桶之间同步。

```console
rclone sync --interactive --progress remote-us:bucket/path/to/dir/ remote-europe:bucket/path/to/dir/
```

甚至在其他云存储与 Storj 之间同步。

```console
rclone sync --interactive --progress s3:bucket/path/to/dir/ storj:bucket/path/to/dir/
```

## 限制

rclone Storj 后端不支持 `rclone about`。不具备此功能的后端无法确定 rclone 挂载的可用空间，也无法将策略 `mfs`（最多可用空间）作为 rclone union 远程存储的成员使用。

参见[不支持 rclone about 的后端列表](https://rclone.org/overview/#optional-features)和 [rclone about](https://rclone.org/commands/rclone_about/)。

## 已知问题

如果遇到类似 `too many open files` 的错误，通常是因为超出了系统最大打开文件数的默认 `ulimit` 限制。原生 Storj 协议会打开大量 TCP 连接（每个连接都被计为一个打开的文件）。单个上传流预计会打开 110 个 TCP 连接，单个下载流预计会打开 35 个。每 64 MiB 的段都会打开一批连接，同时 TCP 连接也会被复用。如果进行大量传输，最终会与大多数存储节点（数千个节点）建立连接。

要解决此问题，请提高系统限制。可以在运行 rclone 之前执行 `ulimit -n 65536`。要进行更永久的更改，可以将其添加到 shell 启动脚本（例如 `$HOME/.bashrc`），或修改系统级配置（通常是 `/etc/sysctl.conf` 和/或 `/etc/security/limits.conf`），但请参考您的操作系统手册。
