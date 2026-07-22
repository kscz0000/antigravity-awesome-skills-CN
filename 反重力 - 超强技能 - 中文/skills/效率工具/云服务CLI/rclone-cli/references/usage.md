---
title: "文档"
description: "Rclone 使用文档"
---

> **官方文档：** [https://rclone.org/docs/](https://rclone.org/docs/)
# 使用 rclone

Rclone 是一个命令行程序，用于管理云存储上的文件。
完成[下载](/downloads/)和[安装](/install)后，继续阅读本文以学习如何使用：初始[配置](#configure)、
[基本语法](#basic-syntax)是什么样的、各[子命令](#subcommands)的说明、各[选项](#options) 等。

## 配置

首先，你需要配置 rclone。由于对象存储系统的认证相当复杂，认证信息都保存在一个配置文件中。
（有关如何找到该配置文件并选择其位置，请参阅 [`--config`](#config-string) 条目。）

最简单的配置方式是运行带 config 选项的 rclone：

```console
rclone config
```

以下列出各项详细说明：

- [1Fichier](/fichier/)
- [Akamai Netstorage](/netstorage/)
- [Alias](/alias/)
- [Archive](/archive/)
- [Amazon S3](/s3/)
- [Backblaze B2](/b2/)
- [Box](/box/)
- [Chunker](/chunker/) - 为其他远端透明地拆分大文件
- [Citrix ShareFile](/sharefile/)
- [Compress](/compress/)
- [Cloudinary](/cloudinary/)
- [Combine](/combine/)
- [Crypt](/crypt/) - 用于加密其他远端
- [DigitalOcean Spaces](/s3/#digitalocean-spaces)
- [Digi Storage](/koofr/#digi-storage)
- [Drime](/drime/)
- [Dropbox](/dropbox/)
- [Enterprise File Fabric](/filefabric/)
- [FileLu Cloud Storage](/filelu/)
- [Filen](/filen/)
- [Files.com](/filescom/)
- [FTP](/ftp/)
- [Gofile](/gofile/)
- [Google Cloud Storage](/googlecloudstorage/)
- [Google Drive](/drive/)
- [Google Photos](/googlephotos/)
- [Hasher](/hasher/) - 为其他远端处理校验和
- [HDFS](/hdfs/)
- [Hetzner Storage Box](/sftp/#hetzner-storage-box)
- [HiDrive](/hidrive/)
- [HTTP](/http/)
- [iCloud Drive](/iclouddrive/)
- [Internet Archive](/internetarchive/)
- [Internxt](/internxt/)
- [Jottacloud](/jottacloud/)
- [Koofr](/koofr/)
- [Linkbox](/linkbox/)
- [Mail.ru Cloud](/mailru/)
- [Mega](/mega/)
- [Memory](/memory/)
- [Microsoft Azure Blob Storage](/azureblob/)
- [Microsoft Azure Files Storage](/azurefiles/)
- [Microsoft OneDrive](/onedrive/)
- [OpenStack Swift / Rackspace Cloudfiles / Blomp Cloud Storage / Memset Memstore](/swift/)
- [OpenDrive](/opendrive/)
- [Oracle Object Storage](/oracleobjectstorage/)
- [Pcloud](/pcloud/)
- [PikPak](/pikpak/)
- [Pixeldrain](/pixeldrain/)
- [premiumize.me](/premiumizeme/)
- [put.io](/putio/)
- [Proton Drive](/protondrive/)
- [QingStor](/qingstor/)
- [Quatrix by Maytech](/quatrix/)
- [rsync.net](/sftp/#rsync-net)
- [Seafile](/seafile/)
- [SFTP](/sftp/)
- [Shade](/shade/)
- [Sia](/sia/)
- [SMB](/smb/)
- [Storj](/storj/)
- [SugarSync](/sugarsync/)
- [Union](/union/)
- [Uloz.to](/ulozto/)
- [WebDAV](/webdav/)
- [Yandex Disk](/yandex/)
- [Zoho WorkDrive](/zoho/)
- [本地文件系统](/local/)

## 基本语法

Rclone 将一棵目录树从一个存储系统同步到另一个。

其语法如下：

```console
rclone subcommand [options] <parameters> <parameters...>
```

`subcommand` 是必需的 rclone 操作（例如 `sync`、`copy`、`ls`）。

`option` 是一个字母的标志（如 `-v`），或一组字母的标志（如 `-Pv`），或一个长标志（如 `--progress`）。选项都不是必需的。选项可以放在 `subcommand` 之后，也可以放在参数之间或末尾，但只有全局选项可以放在 `subcommand` 之前。`--` 选项之后的任何内容都不会被解释为选项，所以如果你需要添加一个以 `-` 开头的参数，可以先单独放一个 `--`，例如：

```console
rclone lsf -- -directory-starting-with-dash
```

`parameter` 通常是文件路径或 [rclone 远端](#syntax-of-remote-paths)，例如 `/path/to/file` 或 `remote:path/to/file`，但也可以是其他内容——`subcommand` 的帮助会告诉你是什么。

源路径和目标路径由你在配置文件中给该存储系统起的名字加上子路径组成，例如
"drive:myfolder" 表示 Google Drive 中的 "myfolder"。

你可以在配置文件中定义任意多个存储路径。

学习 rclone 时请使用 [`--interactive`/`-i`](#interactive) 标志以避免误删数据。

## 子命令

rclone 使用子命令系统。例如：

```console
rclone ls remote:path # lists a remote
rclone copy /local/path remote:path # copies /local/path to the remote
rclone sync --interactive /local/path remote:path # syncs /local/path to the remote
```

主要的 rclone 命令按使用频率排序：

<!-- markdownlint-capture -->
<!-- markdownlint-disable line-length -->
- [rclone config](/commands/rclone_config/) - 进入交互式配置会话。
- [rclone copy](/commands/rclone_copy/) - 将文件从源复制到目标，跳过已复制的。
- [rclone sync](/commands/rclone_sync/) - 让源和目标保持一致，只修改目标。
- [rclone bisync](/commands/rclone_bisync/) - 两条路径之间的[双向同步](/bisync/)。
- [rclone move](/commands/rclone_move/) - 将文件从源移动到目标。
- [rclone delete](/commands/rclone_delete/) - 删除路径下的内容。
- [rclone purge](/commands/rclone_purge/) - 删除路径及其全部内容。
- [rclone mkdir](/commands/rclone_mkdir/) - 如果路径不存在则创建。
- [rclone rmdir](/commands/rclone_rmdir/) - 删除路径。
- [rclone rmdirs](/commands/rclone_rmdirs/) - 删除路径下所有空目录。
- [rclone check](/commands/rclone_check/) - 检查源和目标中的文件是否一致。
- [rclone ls](/commands/rclone_ls/) - 列出路径下的所有对象及其大小与路径。
- [rclone lsd](/commands/rclone_lsd/) - 列出路径下的所有目录/容器/桶。
- [rclone lsl](/commands/rclone_lsl/) - 列出路径下的所有对象及其大小、修改时间和路径。
- [rclone md5sum](/commands/rclone_md5sum/) - 为路径下的所有对象生成 md5sum 文件。
- [rclone sha1sum](/commands/rclone_sha1sum/) - 为路径下的所有对象生成 sha1sum 文件。
- [rclone size](/commands/rclone_size/) - 返回 remote:path 的总大小和对象数量。
- [rclone version](/commands/rclone_version/) - 显示版本号。
- [rclone cleanup](/commands/rclone_cleanup/) - 如果可能，清理远端。
- [rclone dedupe](/commands/rclone_dedupe/) - 交互式查找重复文件并删除/重命名。
- [rclone authorize](/commands/rclone_authorize/) - 远端授权。
- [rclone cat](/commands/rclone_cat/) - 拼接任意文件并发送到标准输出。
- [rclone copyto](/commands/rclone_copyto/) - 将文件从源复制到目标，跳过已复制的。
- [rclone completion](/commands/rclone_completion/) - 输出 rclone 的 shell 补全脚本。
- [rclone gendocs](/commands/rclone_gendocs/) - 将 rclone 的 markdown 文档输出到指定目录。
- [rclone listremotes](/commands/rclone_listremotes/) - 列出配置文件中的所有远端。
- [rclone mount](/commands/rclone_mount/) - 将远端挂载为挂载点。
- [rclone moveto](/commands/rclone_moveto/) - 将文件或目录从源移动到目标。
- [rclone obscure](/commands/rclone_obscure/) - 对 rclone.conf 中使用的密码进行编码。
- [rclone cryptcheck](/commands/rclone_cryptcheck/) - 检查加密远端的完整性。
- [rclone about](/commands/rclone_about/) - 从远端获取配额信息。
<!-- markdownlint-restore -->

完整列表请参见[命令索引](/commands/)。

## 复制单个文件

rclone 通常同步或复制目录。但如果源远端指向一个文件，rclone 只会复制该文件。目标远端必须指向一个目录——否则 rclone 会报错 `Failed to create file system for "remote:file": is a file not a directory`。

例如，假设你的远端中有一个名为 `test.jpg` 的文件，你可以这样仅复制该文件：

```console
rclone copy remote:test.jpg /tmp/download
```

文件 `test.jpg` 将被放置在 `/tmp/download` 中。

这等价于：

```console
rclone copy --files-from /tmp/files remote: /tmp/download
```

其中 `/tmp/files` 包含一行：

```console
test.jpg
```

复制单个文件时建议使用 `copy` 而非 `sync`。两者效果基本相同，但 `copy` 占用的内存要少得多。

## 远端路径语法

传递给 rclone 命令的路径语法如下。

### /path/to/dir

这表示本地文件系统。

在 Windows 上，本地路径中可以使用 `\` 代替 `/`（**仅限**本地路径），非本地路径必须使用 `/`。有关 Windows 特定路径的更多信息，请参阅[本地文件系统](https://rclone.org/local/#paths-on-windows)文档。

这些路径不需要以 `/` 开头——如果不带前导 `/`，则相对当前目录解析。

### remote:path/to/dir

这表示配置文件中定义的（通过 `rclone config` 配置的）`remote:` 上的目录 `path/to/dir`。

### remote:/path/to/dir

在大多数后端上，这与 `remote:path/to/dir` 指向同一目录，推荐使用该格式。在极少数远端（FTP、SFTP、Dropbox 企业版）上，它指向不同的目录。在这些远端上，没有前导 `/` 的路径指向你的"主"目录，有前导 `/` 的路径指向根目录。

### :backend:path/to/dir

这是一种即时创建远端的高级形式。`backend` 应是后端的名称或前缀（配置文件中的 `type`），后端的所有配置都应通过命令行（或环境变量）提供。

示例如下：

```console
rclone lsd --http-url https://pub.rclone.org :http:
```

列出 `https://pub.rclone.org/` 根目录下的所有目录。

```console
rclone lsf --http-url https://example.com :http:path/to/dir
```

列出 `https://example.com/path/to/dir/` 下的文件和目录。

```console
rclone copy --http-url https://example.com :http:path/to/dir /tmp/dir
```

将 `https://example.com/path/to/dir` 中的文件和目录复制到 `/tmp/dir`。

```console
rclone copy --sftp-host example.com :sftp:path/to/dir /tmp/dir
```

使用 sftp 将 `example.com` 上相对目录 `path/to/dir` 中的文件和目录复制到 `/tmp/dir`。

### 连接字符串 {#connection-strings}

上述示例也可以用连接字符串语法来写，参数不是作为命令行参数 `--http-url https://pub.rclone.org` 提供，而是作为远端规格的一部分作为连接字符串提供。

```console
rclone lsd ":http,url='https://pub.rclone.org':"
rclone lsf ":http,url='https://example.com':path/to/dir"
rclone copy ":http,url='https://example.com':path/to/dir" /tmp/dir
rclone copy :sftp,host=example.com:path/to/dir /tmp/dir
```

这些不仅可以用于即时语法创建新远端，还可以用于修改现有远端。下面的示例等同于向远端 `gdrive:` 添加 `--drive-shared-with-me` 参数。

```console
rclone lsf "gdrive,shared_with_me:path/to/dir"
```

使用连接字符串语法的主要优势是它只作用于当前远端，而不会作用于命令行中该类型的所有远端。一个常见的混淆是下面这种将 Google Drive 共享文件复制到普通 Drive 的尝试——它**不起作用**，因为 `--drive-shared-with-me` 标志同时作用于源和目标。

```console
rclone copy --drive-shared-with-me gdrive:shared-file.txt gdrive:
```

但使用连接字符串语法，下面的写法可以正常工作。

```console
rclone copy "gdrive,shared_with_me:shared-file.txt" gdrive:
```

注意，连接字符串只会影响直接后端的选项。例如，假设 gdriveCrypt 是基于 gdrive 的 crypt，那么下面的命令**无法**按预期工作，因为 `shared_with_me` 会被 crypt 后端忽略：

```console
rclone copy "gdriveCrypt,shared_with_me:shared-file.txt" gdriveCrypt:
```

连接字符串具有以下语法：

```text
remote,parameter=value,parameter2=value2:path/to/dir
:backend,parameter=value,parameter2=value2:path/to/dir
```

如果 `parameter` 含有 `:` 或 `,`，则必须用 `"` 或 `'` 括起来，例如：

```text
remote,parameter="colon:value",parameter2="comma,value":path/to/dir
:backend,parameter='colon:value',parameter2='comma,value':path/to/dir
```

如果带引号的值中需要包含引号本身，则应将引号字符加倍，例如：

```text
remote,parameter="with""quote",parameter2='with''quote':path/to/dir
```

这表示 `parameter` 的值为 `with"quote`，`parameter2` 的值为 `with'quote`。

如果省略 `=parameter`，rclone 将替换为 `=true`，这与标志配合得很好。例如，要使用通过环境变量配置的 s3，可以这样：

```console
rclone lsd :s3,env_auth:
```

等价于：

```console
rclone lsd :s3,env_auth=true:
```

注意，在命令行上你可能需要用 `"` 或 `'` 将这些连接字符串包起来，以避免 shell 解释其中的任何特殊字符。

如果你精通 shell，就能知道哪些字符串是安全的，哪些不安全；如果你不确定，请用 `"` 包裹，并在内部使用 `'` 作为引号。该语法在所有操作系统上都适用。

```console
rclone copy ":http,url='https://example.com':path/to/dir" /tmp/dir
```

在 Linux/macOS 上，shell 内部 `"` 字符串中的一些字符仍会被解释（特别是 `\`、`$` 和 `"`），所以如果你的字符串包含这些字符，可以交换 `"` 和 `'` 的角色，如下所示。（该语法在 Windows 上不适用。）

```console
rclone copy ':http,url="https://example.com":path/to/dir' /tmp/dir
```

你可以使用 [rclone config string](/commands/rclone_config_string/) 将远端转换为连接字符串。

#### 连接字符串、配置和日志

如果你通过命令行标志、环境变量或连接字符串为后端提供了额外的配置，rclone 会根据配置的哈希在远端名称后添加一个后缀，例如：

```console
rclone -vv lsf --s3-chunk-size 20M s3:
```

对应的日志消息为：

```text
DEBUG : s3: detected overridden config - adding "{Srj1p}" suffix to name
```

这是为了让 rclone 在缓存后端时能够区分被修改的远端和未被修改的远端。

这通常只在日志中能看出来。

这意味着即时后端，例如：

```console
rclone -vv lsf :s3,env_auth:
```

将拥有自己的名称：

```text
DEBUG : :s3: detected overridden config - adding "{YTu53}" suffix to name
```

### 合法的远端名称

远端名称区分大小写，必须遵守以下规则：

- 可以包含数字、字母、`_`、`-`、`.`、`+`、`@` 和空格。
- 不能以 `-` 或空格开头。
- 不能以空格结尾。

从 rclone 1.61 版本开始，允许任何 Unicode 数字和字母，而早期版本仅限于纯 ASCII（0-9、A-Z、a-z）。如果你在不同 shell 下使用相同的 rclone 配置（这些 shell 可能配置了不同的字符编码），则必须谨慎地使用所有 shell 都能输入的字符。这在 Windows 上尤为常见，因为 Windows 控制台传统上使用非 Unicode 字符集——由所谓的"代码页"定义。

不要在 Windows 上使用单个字符的名称，因为这样会与 Windows 盘符的名称产生歧义，例如：名为 `C` 的远端与 `C` 盘无法区分。Rclone 始终会将单字母名称解释为盘符。

## 向远端添加全局配置 {#globalconfig}

可以为远端配置添加全局配置，这些配置将在远端创建之前应用。

可以通过两种方式实现。第一种是在配置文件中或连接字符串中使用 `override.var = value` 进行临时修改，第二种是在配置文件或连接字符串中使用 `global.var = value` 进行永久修改。

下面会详细说明。

### override.var

用于**仅**在远端创建期间覆盖一个全局变量。它不会影响其他远端，即使它们同时被创建。

这对于仅为该远端覆盖网络配置非常有用。例如，假设你有一个远端需要 `--no-check-certificate`，因为它运行在没有合适证书的测试基础设施上。你可以向 rclone 提供 `--no-check-certificate` 标志，但这会影响**所有**远端。要只影响该远端，可以使用 override。你可以在配置文件中这样写：

```ini
[remote]
type = XXX
...
override.no_check_certificate = true
```

或者在连接字符串中使用 `remote,override.no_check_certificate=true:`（或仅 `remote,override.no_check_certificate:`）。

注意全局标志名如何去掉开头的 `--`，并把 `-` 替换为 `_`，再添加 `override.` 前缀。

并非所有全局变量都适合这样覆盖，因为配置仅在远端创建期间应用。下面列出一个可能会有用的不完整列表：

- `bind_addr`
- `ca_cert`
- `client_cert`
- `client_key`
- `connect_timeout`
- `disable_http2`
- `disable_http_keep_alives`
- `dump`
- `expect_continue_timeout`
- `headers`
- `http_proxy`
- `low_level_retries`
- `max_connections`
- `no_check_certificate`
- `no_gzip`
- `timeout`
- `traffic_class`
- `use_cookies`
- `use_server_modtime`
- `user_agent`

`override.var` 将覆盖所有其他配置方法，但**仅**在该远端创建期间生效。

### global.var

用于为**所有内容**设置一个全局变量。该全局变量在远端创建之前设置。

这对于不能设置为 `override` 的参数（例如 sync 参数）很有用。例如，假设你有一个远端，希望始终使用 `--checksum` 标志。你可以在每次运行 rclone 命令时都提供 `--checksum` 标志，但更方便的做法是在配置文件中这样写：

```ini
[remote]
type = XXX
...
global.checksum = true
```

或者在连接字符串中使用 `remote,global.checksum=true:`（或仅 `remote,global.checksum:`）。这等价于使用 `--checksum` 标志。

注意全局标志名如何去掉开头的 `--`，并把 `-` 替换为 `_`，再添加 `global.` 前缀。

任何全局变量都可以这样设置，它与在命令行上使用等价的标志完全相同。这意味着它会影响 rclone 的所有使用。

如果两个远端设置了相同的全局变量，那么第一个实例化的远端将被第二个覆盖。`global.var` 将在远端创建时覆盖所有其他配置方法。

## 引号与 shell

当你在计算机上输入命令时，你正在使用一个叫做命令行 shell 的东西。它会以操作系统特定的方式解释各种字符。

下面列出一些对不熟悉 shell 规则的用户可能有帮助的注意事项。

### Linux / macOS

如果你的文件名包含空格或 shell 元字符（例如 `*`、`?`、`$`、`'`、`"` 等），则必须将它们引起来。默认使用单引号 `'`。

```console
rclone copy 'Important files?' remote:backup
```

如果你想发送一个 `'`，则需要使用 `"`，例如：

```console
rclone copy "O'Reilly Reviews" remote:backup
```

引号元字符的规则很复杂，如果你想了解完整细节，必须查阅你的 shell 手册页。

### Windows

如果你的文件名中含有空格，需要用 `"` 括起来，例如：

```bat
rclone copy "E:\folder name\folder name\folder name" remote:backup
```

如果使用根目录本身，请不要加引号（原因见 [#464](https://github.com/rclone/rclone/issues/464)），例如：

```bat
rclone copy E:\ remote:backup
```

## 复制文件名或目录名中含 `:` 的文件或目录

rclone 使用 `:` 标记远端名称。然而，在非 Windows 系统上，`:` 是合法的文件名组成部分。远端名称解析器只会查找第一个 `/` 之前的 `:`，所以如果你需要对这样的文件或目录进行操作，请使用以 `/` 开头的完整路径，或使用 `./` 作为当前目录前缀。

例如，要将名为 `sync:me` 的目录同步到名为 `remote:` 的远端：

```console
rclone sync --interactive ./sync:me remote:path
```

或者：

```console
rclone sync --interactive /full/path/to/sync:me remote:path
```

## 服务端复制

大多数远端都支持服务端复制（但并非全部——请参阅[概述](/overview/#optional-features)）。

这意味着，如果你想将一个文件夹复制到另一个文件夹，rclone 不会下载所有文件再重新上传；它会指示服务器就地复制。

例如：

```console
rclone copy s3:oldbucket s3:newbucket
```

会将 `oldbucket` 的内容复制到 `newbucket`，而无需下载和重新上传。

不支持服务端复制的远端**会**在这种情况下下载并重新上传。

服务端复制在 `sync` 和 `copy` 中使用，使用 `-v` 标志时会在日志中标出。如果远端不直接支持服务端 move，`move` 命令也可能使用服务端复制。它通过先执行服务端复制再执行删除来完成，这比下载再重新上传要快得多。

只有当远端名称相同时，才会尝试进行服务端复制。

在脚本中可以使用它来高效地制作按时间轮换的备份，例如：

```console
rclone sync --interactive remote:current-backup remote:previous-backup
rclone sync --interactive /path/to/files remote:current-backup
```

## 元数据支持 {#metadata}

元数据是关于文件（或目录）的数据，但不属于文件（或目录）的内容。通常 rclone 只会尽可能保留修改时间和内容（MIME）类型。

在使用 `--metadata` 或 `-M` 标志时，rclone 会在文件和目录上保留所有可用的元数据。

具体支持哪些元数据以及这些支持意味着什么，取决于后端。支持元数据的后端在其文档中有元数据小节，并列在[功能表](/overview/#features)中（例如 [local](/local/#metadata)、[s3](/s3/#metadata)）。

有些后端不支持元数据，有些仅支持文件的元数据，有些则同时支持文件和目录的元数据。

Rclone 仅支持一次性的元数据同步。这意味着，只有当源对象发生变化并需要重新上传时，元数据才会从源对象同步到目标对象。如果之后源对象的元数据发生变化而对象本身没有变化，则不会同步到目标对象。这与 rclone 在不使用 `--metadata` 标志时同步 `Content-Type` 的方式一致。

在本地到本地的同步中使用 `--metadata` 时，将保留文件属性，例如文件模式、所有者、扩展属性（Windows 上不支持）。

注意，可以使用 `--metadata-set key=value` 标志在对象首次上传时向其添加任意元数据。该标志可以根据需要重复使用。

`[--metadata-mapper](#metadata-mapper)` 标志可用于传入一个程序名，在元数据从源复制到目标的过程中对其进行转换。

Rclone 在执行服务端 `Move` 和服务端 `Copy` 时支持 `--metadata-set` 和 `--metadata-mapper`，但在执行服务端 `DirMove`（重命名目录）时不支持，因为这需要递归到目录中。注意，你可以使用 `--disable DirMove` 禁用 `DirMove`，rclone 将回退到对每个对象使用 `Move`，此时支持 `--metadata-set` 和 `--metadata-mapper`。

### 元数据的类型

元数据分为两种类型：系统元数据和用户元数据。

后端自身使用的元数据称为系统元数据。例如，在本地后端上，系统元数据 `uid` 在基于 unix 的平台上使用时，会存储文件的用户 ID。

任意元数据称为用户元数据，可以按需设置。

当对象从一个后端复制到另一个后端时，如果提供了系统元数据，系统会尝试解释它。对象在不同后端之间复制时，元数据可能从用户元数据变为系统元数据。例如，将对象从 s3 复制会设置 `content-type` 元数据。在理解该元数据的后端（如 `azureblob`）中，它将成为该对象的 Content-Type。在不理解该元数据的后端（如 `local` 后端）中，它将成为用户元数据。但是，如果将本地对象复制回 s3，Content-Type 将被正确设置。

### 元数据框架

Rclone 实现了一个元数据框架，可以在对象被读取时读取其元数据，并仅在对象被上传时将元数据写入对象。

该元数据以字典形式存储，键和值均为字符串。

键名有一些限制（这些限制将来可能会进一步澄清）。

- 必须为小写
- 可以包含 `a-z`、`0-9`，以及 `.`、`-` 或 `_`
- 长度取决于后端

每个后端可以提供它所理解的系统元数据。一些后端还可以存储任意用户元数据。

在可能的情况下，键名是标准化的，因此，例如，可以将对象的元数据从 s3 复制到 azureblob，元数据会被适当地转换。

一些后端对元数据的大小有限制，如果超过，rclone 在上传时会报错。

### 元数据保留

实现的目标是：

1. 尽可能保留元数据
2. 尽可能解释元数据

第 1 条的结果是，你可以将一个 S3 对象复制到本地磁盘，然后再无损地复制回 S3。同样，你可以将一个带有文件属性和 xattr 的本地文件从本地磁盘复制到 s3 并再次无损地复制回来。

第 2 条的结果是，你可以将带有元数据的 S3 对象复制到 Azureblob（比如说），使元数据也出现在 Azureblob 对象上。

### 标准系统元数据

下表列出了标准系统元数据，如果适用的话，后端可以实现这些元数据。

| key                 | description | example |
|---------------------|-------------|---------|
| mode                | File type and mode: octal, unix style | 0100664 |
| uid                 | User ID of owner: decimal number | 500 |
| gid                 | Group ID of owner: decimal number | 500 |
| rdev                | Device ID (if special file)  => hexadecimal | 0 |
| atime               | Time of last access:  RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 |
| mtime               | Time of last modification:  RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 |
| btime               | Time of file creation (birth):  RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 |
| utime               | Time of file upload:  RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 |
| cache-control       | Cache-Control header | no-cache |
| content-disposition | Content-Disposition header | inline |
| content-encoding    | Content-Encoding header | gzip |
| content-language    | Content-Language header | en-US |
| content-type        | Content-Type header | text/plain |

如果在元数据中提供了 `mtime` 和 `content-type` 键，它们的值将优先于读取源对象的 `Content-Type` 或修改时间。

哈希不包含在系统元数据中，因为已经有定义良好的方式来读取这些哈希。

## 选项

Rclone 有许多选项来控制其行为。这些选项将在下文和 [flags](/flags) 页面中记录。

接受参数的选项可以通过两种方式传值：`--option=value` 或 `--option value`。然而，布尔（true/false）选项与其他选项略有不同：`--boolean` 将选项设置为 `true`，而缺少该标志则将其设置为 `false`。也可以指定 `--boolean=false` 或 `--boolean=true`。注意 `--boolean false` 是无效的——它会被解析为 `--boolean`，而 `false` 会被解析为 rclone 的额外命令行参数。

被识别为特殊标识符的字符串值（例如用 `--log-level` 选项设置的日志级别名称）不区分大小写，例如 `--log-level ERROR` 和 `--log-level error` 是相同的。

被记录为接受 `stringArray` 参数的选项可以接受多个值。要传入多个值，请重复该选项；例如：`--include value1 --include value2`。其他选项可能只接受单个值，并且只能指定一次，但指定的参数可能表示以空格或逗号分隔的列表。这样的选项在文档中如果接受逗号分隔的参数则为 `CommaSepList`，如果接受空格分隔的参数则为 `SpaceSepList`，不过有些选项可能使用不同的参数，例如 `DumpFlags`，或者直接使用 `string`，帮助文本会说明这将被解释为一个列表。

包含小数部分的浮点值必须使用句点（`.`）作为小数分隔符，这在英语国家很常见，与你配置的系统区域设置无关。`float` 参数类型接受十进制和十六进制浮点数，遵循 Go 语法中关于[浮点字面量](https://go.dev/ref/spec#Floating-point_literals)的定义。

### 时间和时长选项 {#time-options}

接受 `Time` 或 `Duration` 参数的选项必须以格式化的字符串形式指定，描述绝对或相对时间。注意 `Time` 和 `Duration` 参数类型都可以表示为绝对或相对时间，只是解释方式不同，例如，作为 `Time` 值传递时，相对时间将被视为距当前时间的偏移量。

绝对时间可以用以下格式之一的字符串指定：

- RFC3339 - 例如 `2006-01-02T15:04:05Z` 或 `2006-01-02T15:04:05+07:00`
- ISO8601 日期和时间，本地时区 - `2006-01-02T15:04:05`
- ISO8601 日期和时间，本地时区 - `2006-01-02 15:04:05`
- ISO8601 日期 - `2006-01-02`（YYYY-MM-DD）

相对时间是一个由可能带符号的十进制数字组成的字符串，每个数字可以带可选的小数部分，每个数字带一个单位后缀。如果字符串只包含单个数字，则单位后缀是可选的，默认为秒，即纯十进制值将被视为秒数。以下是有效的后缀：

- `ms` - 毫秒
- `s`  - 秒
- `m`  - 分钟
- `h`  - 小时
- `d`  - 天
- `w`  - 周
- `M`  - 月
- `y`  - 年

例如："10"、"300ms"、"-1.5h" 或 "2h45m"。

### 大小选项

接受 SizeSuffix 参数的选项可以指定为整数值，默认将被视为 KiB 值（1024 字节的倍数）。可以通过添加后缀来改变解释方式：`B` 表示字节，`K` 表示 KiB，`M` 表示 MiB，`G` 表示 GiB，`T` 表示 TiB，`P` 表示 PiB。这些是二进制单位，分别为 1、2\*\*10、2\*\*20、2\*\*30。

另请参阅 [--human-readable](#human-readable)。

## 主要选项

### --backup-dir string

在使用 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 或 [move](/commands/rclone_move/) 时，任何将被覆盖或删除的文件都会按其原始层次结构移入此目录。

如果设置了 `--suffix`，则被移动的文件将添加此后缀。如果目录中存在具有相同路径的文件（添加后缀之后），则该文件将被覆盖。

使用的远端必须支持服务端 move 或 copy，并且必须使用与同步目标相同的远端。备份目录不能与目标目录重叠，除非通过过滤规则将其排除。

例如：

```console
rclone sync --interactive /path/to/local remote:current --backup-dir remote:old
```

会将 `/path/to/local` 同步到 `remote:current`，但任何将被更新或删除的文件会存储在 `remote:old` 中。

如果在脚本中运行 rclone，你可能希望使用今天的日期作为传递给 `--backup-dir` 的目录名来存储旧文件，或者你可能希望使用今天的日期作为 `--suffix` 的值。在 bash 中可以使用 `--suffix $(date +%F)`，在 PowerShell 中可以使用 `--suffix $(Get-Date -Format 'yyyy-MM-dd')`。

请参阅 `--compare-dest` 和 `--copy-dest`。

### --bind string

用于出站连接的本地地址。可以是 IPv4 地址（1.2.3.4）、IPv6 地址（1234::789A）或主机名。如果主机名无法解析或解析为多个 IP 地址，则会报错。

你可以使用 `--bind 0.0.0.0` 强制 rclone 使用 IPv4 地址，使用 `--bind ::0` 强制 rclone 使用 IPv6 地址。

### --bwlimit BwTimetable

此选项控制带宽限制。例如：

```text
--bwlimit 10M
```

表示将上传和下载带宽限制为 10 MiB/s。
**注意** 单位是**字节**每秒，而不是**比特**每秒。要使用单一限制，请以 KiB/s 为单位指定所需带宽，或使用后缀 B|K|M|G|T|P。默认值为 `0`，表示不限制带宽。

可以分别指定上传和下载带宽，格式为 `--bwlimit UP:DOWN`，例如：

```text
--bwlimit 10M:100k
```

表示将上传带宽限制为 10 MiB/s，将下载带宽限制为 100 KiB/s。任一限制都可以是 "off"，表示无限制，因此要仅限制上传带宽，你可以使用：

```text
--bwlimit 10M:off
```

这会将上传带宽限制为 10 MiB/s，但下载带宽不受限制。

如上所述，带宽限制在 rclone 二进制文件运行期间持续生效。

也可以指定一个"时刻表"形式的限制，它将在指定的时间应用某些限制。要指定时刻表，请将条目格式化为 `WEEKDAY-HH:MM,BANDWIDTH WEEKDAY-HH:MM,BANDWIDTH...`，其中：`WEEKDAY` 是可选元素。

- `BANDWIDTH` 可以是单个数字，例如 `100k`，也可以是一对数字表示上传:下载，例如 `10M:1M`。
- `WEEKDAY` 可以写全称或仅使用前 3 个字符。它是可选的。
- `HH:MM` 是从 00:00 到 23:59 的某个小时。

条目可以用空格或分号分隔。

**注意：** 可以使用分号作为分隔符代替空格，以避免在 Docker 等环境中出现解析问题。

一个典型的工作时间避免链路饱和的时刻表示例如下：

使用空格作为分隔符：
`--bwlimit "08:00,512k 12:00,10M 13:00,512k 18:00,30M 23:00,off"`

使用分号作为分隔符：
`--bwlimit "08:00,512k;12:00,10M;13:00,512k;18:00,30M;23:00,off"`

在这些示例中，每天的早上 8 点，传输带宽将设置为 512 KiB/s。中午时，它将上升到 10 MiB/s，下午 1 点时回落到 512 KiB/s。下午 6 点时，带宽限制将设置为 30 MiB/s，晚上 11 点时将完全禁用（不限速）。晚上 11 点到早上 8 点之间将保持不限速。

带有 `WEEKDAY` 的时刻表示例：

使用空格作为分隔符：
`--bwlimit "Mon-00:00,512 Fri-23:59,10M Sat-10:00,1M Sun-20:00,off"`

使用分号作为分隔符：
`--bwlimit "Mon-00:00,512;Fri-23:59,10M;Sat-10:00,1M;Sun-20:00,off"`

这表示：周一的传输带宽将设置为 512 KiB/s。周五结束前上升到 10 MiB/s。周六上午 10:00 设为 1 MiB/s。周日 20:00 起恢复为不限速。

没有 `WEEKDAY` 的时间段会扩展到整个星期。所以下面这个示例：

```text
--bwlimit "Mon-00:00,512 12:00,1M Sun-20:00,off"
```

等价于：

```text
--bwlimit "Mon-00:00,512Mon-12:00,1M Tue-12:00,1M Wed-12:00,1M Thu-12:00,1M Fri-12:00,1M Sat-12:00,1M Sun-12:00,1M Sun-20:00,off"
```

带宽限制适用于所有后端的数据传输。对于大多数后端，目录列表的带宽也包含在内（例外的是非 HTTP 后端，`ftp`、`sftp` 和 `storj`）。

注意单位是**字节/秒**，而不是**比特/秒**。通常连接速度以比特/秒为单位——转换时需除以 8。例如，假设你有一个 10 Mbit/s 的连接，希望 rclone 使用其中的一半，即 5 Mbit/s。这相当于 5/8 = 0.625 MiB/s，因此你应该为 rclone 使用 `--bwlimit 0.625M` 参数。

在 Unix 系统（Linux、macOS 等）上，可以通过向 rclone 发送 `SIGUSR2` 信号来切换带宽限制器。这允许移除长时间运行的 rclone 传输的限制，并在需要时快速恢复到 `--bwlimit` 指定的值。假设只有一个 rclone 实例在运行，你可以像下面这样切换限制器：

```console
kill -SIGUSR2 $(pidof rclone)
```

如果你使用[远程控制](/rc)配置 rclone，则可以动态更改 bwlimit：

```console
rclone rc core/bwlimit rate=1M
```

### --bwlimit-file BwTimetable

此选项控制每个文件的带宽限制。选项说明请参见 `--bwlimit` 标志。

例如，使用此选项将所有传输限制为不超过 1 MiB/s：

```text
--bwlimit-file 1M
```

此选项可以与 `--bwlimit` 结合使用。

注意，如果提供了时间表，文件将使用传输开始时生效的时间表。

### --buffer-size SizeSuffix

使用此大小的缓冲区来加速文件传输。每个 `--transfer` 将使用这么多内存进行缓冲。

使用 `mount` 或 `cmount` 时，每个打开的文件描述符将使用这么多内存进行缓冲。
更多详细信息，请参阅 [mount](/commands/rclone_mount/#file-buffering) 文档。

设置为 `0` 可禁用缓冲以最小化内存使用。

注意，缓冲区的内存分配受 [--use-mmap](#use-mmap) 标志的影响。

### --cache-dir string

指定 rclone 用于缓存的目录，以覆盖默认值。

默认值取决于操作系统：

- Windows `%LocalAppData%\rclone`，如果 `LocalAppData` 已定义。
- macOS `$HOME/Library/Caches/rclone`，如果 `HOME` 已定义。
- Unix `$XDG_CACHE_HOME/rclone`，如果 `XDG_CACHE_HOME` 已定义；否则 `$HOME/.cache/rclone`，如果 `HOME` 已定义。
- 在所有操作系统上回退到 `$TMPDIR/rclone`，其中 `TMPDIR` 是来自 [--temp-dir](#temp-dir-string) 的值。

你可以使用 [config paths](/commands/rclone_config_paths/) 命令查看当前值。

缓存目录被 [VFS File Caching](/commands/rclone_mount/#vfs-file-caching) 挂载功能大量使用，也被 [serve](/commands/rclone_serve/)、[GUI](/gui) 和 rclone 的其他部分使用。

### --check-first

如果设置了此标志，则在 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 或 [move](/commands/rclone_move/) 中，rclone 会在执行任何传输之前先做完所有检查以确定文件是否需要传输。通常 rclone 会尽快开始运行传输。

此标志在 IO 受限的系统上非常有用，因为传输会干扰检查。

在结合使用 `--order-by` 时，它对于确保完美的顺序也很有用。

如果在 `rclone move` 时同时设置了 `--check-first` 和 `--order-by`，rclone 将使用传输线程删除不需要传输的源文件。这将实现传输和删除的完美顺序，但会导致传输统计中包含比预期更多的项目。

使用此标志可能会占用更多内存，因为它实际上将 `--max-backlog` 设置为无穷大。这意味着所有待传输对象的信息都会在传输开始之前保存在内存中。

### --checkers int

最初仅控制并行运行的文件检查器数量，例如通过 `rclone copy`。现在它是一个被 `rclone` 在多个地方使用的相当通用的并行控制。

注意：检查器在同步过程中执行文件的相等性检查。对于某些存储系统（例如 S3、Swift、Dropbox），这可能需要大量时间，因此它们是并行运行的。

默认并行运行 8 个检查器。但是，对于响应较慢的后端，你可能需要通过将 `--checkers` 设置为 4 或更少的线程来降低（而不是增加）这个默认值。尤其建议在文件检查阶段遇到后端服务器崩溃时（例如在后续或追加备份中，几乎不进行文件复制而检查占用了大部分时间）使用此设置。仅当极度谨慎时才增加此设置，同时监控服务器健康状况和文件检查吞吐量。

### -c, --checksum

通常 rclone 会查看文件的修改时间和大小来判断它们是否相等。如果设置此标志，rclone 将检查文件的哈希和大小来判断文件是否相等。

当远端不支持设置修改时间，并且需要比仅检查文件大小更精确的同步时，这很有用。

当在对象上存储相同哈希类型的远端之间传输时，这非常有用，例如 Drive 和 Swift。有关哪些远端支持哪些哈希类型的详细信息，请参见[概述部分](/overview/)的表格。

例如 `rclone --checksum sync s3:/bucket swift:/bucket` 比不使用 `--checksum` 标志要快得多。

使用此标志时，rclone 不会像通常那样在远程文件 mtime 不正确时更新它们。

### --color AUTO|NEVER|ALWAYS

指定何时应向输出添加颜色（和其他 ANSI 代码）。

`AUTO` 仅在输出是终端时允许 ANSI 代码。这是默认设置。

`NEVER` 永远不允许 ANSI 代码。

`ALWAYS` 始终添加 ANSI 代码，无论输出格式是终端还是文件。

### --compare-dest stringArray

在使用 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 或 [move](/commands/rclone_move/) 时，除了目标之外，还会检查指定路径下的文件。如果在指定路径中找到与源相同的文件，则**不会**从源复制该文件。这对于仅复制自上次备份以来已更改的文件非常有用。

必须使用与同步目标相同的远端。比较目录不能与目标目录重叠。

请参阅 `--copy-dest` 和 `--backup-dir`。

### --config string

指定 rclone 配置文件的位置，以覆盖默认值。例如 `rclone config --config="rclone.conf"`。

确切的默认值有点复杂，因为 rclone 在不同版本中引入了更改同时保持了向后兼容性，但在大多数情况下很简单：

- Windows 上为 `%APPDATA%/rclone/rclone.conf`
- 其他系统上为 `~/.config/rclone/rclone.conf`

完整逻辑如下：Rclone 将按以下优先级顺序在任何以下位置查找现有配置文件：

1. `rclone.conf`（在程序目录中，即 rclone 可执行文件所在目录）
2. `%APPDATA%/rclone/rclone.conf`（仅在 Windows 上）
3. `$XDG_CONFIG_HOME/rclone/rclone.conf`（在所有系统上，包括 Windows）
4. `~/.config/rclone/rclone.conf`（有关 `~` 符号的解释见下文）
5. `~/.rclone.conf`

如果未找到现有配置文件，则会在以下位置创建一个新文件：

- Windows 上：上面列出的位置 2，除非不太可能的情况 `APPDATA` 未定义，则使用位置 4。
- Unix 上：如果 `XDG_CONFIG_HOME` 已定义，则使用位置 3，否则使用位置 4。
- 在所有操作系统上回退到位置 5，当 rclone 目录无法创建时，但如果没有找到主目录，则最终将使用相对于当前工作目录的路径 `.rclone.conf` 作为最终手段。

上面路径中的 `~` 符号表示任何操作系统上当前用户的主目录，其定义如下：

- Windows 上：`%HOME%`（如果已定义），否则 `%USERPROFILE%`，否则 `%HOMEDRIVE%\%HOMEPATH%`。
- Unix 上：`$HOME`（如果已定义），否则通过在操作系统特定的用户数据库中（例如 passwd 文件）查找当前用户，否则使用 shell 命令 `cd && pwd` 的结果。

如果运行 `rclone config file`，你将看到你的默认位置。运行 `rclone config touch` 将确保配置文件存在，如果不存在则在默认位置创建一个空文件。

始终优先使用与 rclone 可执行文件位于同一目录的现有 `rclone.conf` 文件这一事实，意味着通过将 rclone 可执行文件下载到一个可写目录然后在同一目录中创建一个空文件 `rclone.conf`，就可以轻松地以"便携"模式运行。

如果该位置设置为空字符串 `""` 或名为 `notfound` 的文件路径，或操作系统空设备（Windows 上为 `NUL`，Unix 系统上为 `/dev/null`），则 rclone 将只在内存中保存配置文件。

如果没有配置文件，你可能会看到日志消息"Config file not found - using defaults"。可以抑制此消息，例如如果你完全使用[即时远端](/docs/#backend-path-to-dir)，可以使用仅内存的配置文件或创建一个空配置文件，如上所述。

文件格式是基本的 [INI](https://en.wikipedia.org/wiki/INI_file#Format)：以 `[section]` 标题开头的文本段，后跟单独行的 `key=value` 条目。在 rclone 中，每个远端由其自己的段表示，段名定义远端的名称。选项被指定为 `key=value` 条目，其中键是不带 `--backend-` 前缀的选项名称，小写，用 `_` 代替 `-`。例如选项 `--mega-hard-delete` 对应键 `hard_delete`。只能指定后端选项。一个特殊且必需的键 `type` 标识[存储系统](/overview/)，其值是 `rclone help backends` 命令返回的内部小写名称。注释以行首的 `;` 或 `#` 表示。

示例：

```ini
[megaremote]
type = mega
user = you@example.com
pass = PDPcQVVjVtzFY-GTdDFozqBhTdsPg3qH
```

注意密码以[混淆](/commands/rclone_obscure/)形式存在。此外，许多存储系统使用基于令牌的认证而不是密码，这需要额外的步骤。使用交互式命令 `rclone config` 更容易也更安全，而不是手动编辑配置文件。

配置文件通常包含登录信息，因此应具有受限的权限，以便只有当前用户可以读取它。Rclone 在写入文件时会尝试确保这一点。你也可以选择[加密](#configuration-encryption)该文件。

当使用基于令牌的认证时，配置文件必须是可写的，因为 rclone 需要更新其中的令牌。

为了降低损坏现有配置文件的风险，rclone 在保存更改时不会直接写入该文件。它会先写入一个新的临时文件。如果配置文件已存在（在 Unix 系统上），它会尝试将其权限镜像到新文件。然后它会将现有文件重命名为临时名称作为备份。接下来，rclone 会将新文件重命名为正确的名称，最后通过删除备份文件来完成清理。

如果 rclone 使用的配置文件路径是符号链接，则会对其进行解析，rclone 将写入解析后的路径，而不是覆盖符号链接。此过程中使用的临时文件（如上所述）将写入解析后的配置文件的同一父目录，但如果该目录也是符号链接，则不会解析它，临时文件将写入该目录符号链接的位置。

### --contimeout Duration

设置连接超时。应以 Go 时间格式表示，例如 `5s` 表示 5 秒，`10m` 表示 10 分钟，或 `3h30m`。

连接超时是 rclone 等待与远程对象存储系统建立连接的时间。默认值为 `1m`。

### --copy-dest stringArray

在使用 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 或 [move](/commands/rclone_move/) 时，除了目标之外，还会检查指定路径下的文件。这一部分与 `--compare-dest` 相同，但区别在于使用 `--copy-dest` 时，如果在指定路径中找到与源相同的文件，该文件将通过服务端复制从指定路径复制到目标。这对于增量备份非常有用。

使用的远端必须支持服务端 copy，并且必须使用与同步目标相同的远端。比较目录不能与目标目录重叠。

请参阅 `--compare-dest` 和 `--backup-dir`。

### --dedupe-mode interactive|skip|first|newest|oldest|largest|smallest|rename|list

运行 dedupe 命令的模式。可选值为 `interactive`、`skip`、`first`、`newest`、`oldest`、`largest`、`smallest`、`rename`、`list`。默认值为 `interactive`。有关这些选项含义的更多信息，请参阅 [dedupe](/commands/rclone_dedupe/) 命令。

### --default-time Time

如果文件或目录没有可读取的修改时间，rclone 将显示这个固定时间代替。

默认值为 `2000-01-01 00:00:00 UTC`。这可以通过[时间选项](#time-options)中显示的任何方式进行配置。

例如 `--default-time 2020-06-01` 将默认时间设置为 2020 年 6 月 1 日，或 `--default-time 0s` 将默认时间设置为 rclone 启动的时间。

### --disable string

此选项禁用一个以逗号分隔的可选功能列表。例如，要禁用服务端 move 和服务端 copy，使用：

```text
--disable move,copy
```

这些功能可以用任何大小写。

要查看可以禁用哪些功能，请使用：

```text
--disable help
```

远端具有的功能可以以 JSON 格式查看：

```console
rclone backend features remote:
```

请参阅[功能](/overview/#features)和[可选功能](/overview/#optional-features)概述，了解每个功能的作用。

注意，对于一些 `true`/`false` 功能标志类功能，可以通过为其添加 `!` 前缀来强制设置为 `true`。例如，`CaseInsensitive` 功能可以通过 `--disable CaseInsensitive` 强制为 `false`，并通过 `--disable '!CaseInsensitive'` 强制为 `true`。一般来说这不是一个好主意，但在极端情况下可能有用。

（注意 `!` 是一个 shell 命令，在类 unix 平台上你需要使用单引号或反斜杠进行转义。）

此标志在调试和特殊情况下（例如 Google Drive 将服务端复制的总容量限制为 100 GiB/天）非常有用。

### --disable-http2

这会阻止 rclone 尝试使用 HTTP/2（如果可用）。由于 [Go 标准库的问题](https://github.com/golang/go/issues/37373)，有时这可以加快传输速度。

### --dscp string

指定要在连接中使用的 DSCP 值或名称。这可以帮助 QoS 系统识别流量类。允许使用 BE、EF、DF、LE、CSx 和 AFxx。

请参阅[差分服务](https://en.wikipedia.org/wiki/Differentiated_services)的描述以了解此字段。将此设置为 1（LE）以将流标识为 SCAVENGER 类，可以避免在支持 DiffServ 的网络中占用过多带宽（[RFC 8622](https://tools.ietf.org/html/rfc8622)）。

例如，如果你在路由器上配置了 QoS 来正确处理 LE，运行：

```console
rclone copy --dscp LE from:/from to:/to
```

将使得优先级低于普通互联网流量。

此选项在 Windows 上无效（请参阅 [golang/go#42728](https://github.com/golang/go/issues/42728)）。

### -n, --dry-run

进行试运行，不做永久更改。使用此选项可以查看 rclone 将要做什么而不实际执行。在设置会删除目标文件的 [sync](/commands/rclone_sync/) 命令时非常有用。

### --expect-continue-timeout Duration

此选项指定在完全写入请求头后，如果请求带有 "Expect: 100-continue" 头，等待服务器首次响应头的时长。并非所有后端都支持使用此选项。

零表示无超时，并导致立即发送请求体，而无需等待服务器批准。此时间不包括发送请求头的时间。

默认值为 `1s`。设置为 `0` 以禁用。

### --error-on-no-transfer

默认情况下，如果没有错误，rclone 将以返回码 0 退出。

此选项允许 rclone 在源和目标之间没有文件被传输时返回退出码 9。这允许在脚本中使用 rclone，并在复制了数据时触发后续操作，或者在没有复制时跳过。

注意：启用此选项会将通常非致命的错误变为潜在致命的错误——请检查并相应地调整你的脚本！

### --fix-case

通常，同步到不区分大小写的目标（例如 macOS / Windows）时，如果源和目标文件名大小写不同但其他方面相同，则不会得到匹配的文件名。例如，将 `hello.txt` 同步到 `HELLO.txt` 通常会使目标文件名保持为 `HELLO.txt`。如果设置了 `--fix-case`，则 `HELLO.txt` 将被重命名为 `hello.txt` 以匹配源。

注意：

- 大小写不正确的目录名也会被修正
- 如果设置了 `--immutable`，`--fix-case` 将被忽略
- 不建议改用 `--local-case-sensitive`；它会导致 `HELLO.txt` 被删除！
- 旧的目标文件名不能被过滤器排除。
  要特别注意 [`--files-from`](/filtering/#files-from-read-list-of-source-file-names)，它不遵循 [`--ignore-case`](/filtering/#ignore-case-make-searches-case-insensitive)！
- 在不支持服务端 move 的远端上，`--fix-case` 将需要下载文件并重新上传。要避免这种情况，请不要使用 `--fix-case`。

### --fs-cache-expire-duration Duration

通过 API 使用 rclone 时，默认情况下，rclone 会在"fs 缓存"中缓存已创建的远端 5 分钟。这意味着如果对同一远端重复执行操作，rclone 无需从头开始构建它，从而更高效。

此标志设置远端缓存的时间。如果将其设置为 `0`（或负数），rclone 将根本不缓存远端。

注意，如果使用某些标志，例如 `--backup-dir`，并且将其设置为 `0`，rclone 可能会构建两个远端（一个用于源或目标，一个用于 `--backup-dir`），而之前可能只构建了一个。

### --fs-cache-expire-interval Duration

这控制 rclone 检查缓存远端是否过期的频率。有关更多信息，请参阅上面的 `--fs-cache-expire-duration` 文档。默认值为 60s，设置为 0 禁用过期。

### --header stringArray

为所有事务添加 HTTP 头。该标志可以重复以添加多个头。

如果只想为上传添加头，请使用 `--header-upload`；如果只想为下载添加头，请使用 `--header-download`。

此标志受所有基于 HTTP 的后端支持，即使是不受 `--header-upload` 和 `--header-download` 支持的后端也支持，因此可以谨慎地用作这些后端的替代方案。

```console
rclone ls remote:test --header "X-Rclone: Foo" --header "X-LetMeIn: Yes"
```

### --header-download stringArray

为所有下载事务添加 HTTP 头。该标志可以重复以添加多个头。

```console
rclone sync --interactive s3:test/src ~/dst --header-download "X-Amz-Meta-Test: Foo" --header-download "X-Amz-Meta-Test2: Bar"
```

有关当前支持的后端，请参阅 GitHub issue [#59](https://github.com/rclone/rclone/issues/59)。

### --header-upload stringArray

为所有上传事务添加 HTTP 头。该标志可以重复以添加多个头。

```console
rclone sync --interactive ~/src s3:test/dst --header-upload "Content-Disposition: attachment; filename='cool.html'" --header-upload "X-Amz-Meta-Test: FooBar"
```

有关当前支持的后端，请参阅 GitHub issue [#59](https://github.com/rclone/rclone/issues/59)。

### --http-proxy string

使用此选项为所有基于 HTTP 的服务设置 HTTP 代理。

Rclone 还支持标准的 HTTP 代理环境变量，它会自动获取。这通常是设置 HTTP 代理的方式，但此标志可用于覆盖它。

### --human-readable

Rclone 命令输出大小（例如字节数）和计数（例如文件数）的值，可以是**原始**数字，也可以是**人类可读**格式。

在人类可读格式中，值被缩放为更大的单位，用值后面的后缀表示，并四舍五入到三位小数。Rclone 一致地对大小使用二进制单位（2 的幂），对计数使用十进制单位（10 的幂）。大小单位前缀遵循 IEC 标准表示法，例如 `Ki` 表示 kibi。配合字节单位使用时，`1 KiB` 表示 1024 字节。在列表类型的输出中，仅显示附加到值的单位前缀（例如 `9.762Ki`），而在更文本化的输出中显示完整单位（例如 `9.762 KiB`）。对于计数，使用 SI 标准表示法，例如前缀 `k` 表示 kilo。配合文件计数使用时，`1k` 表示 1000 个文件。

各种 [list](/commands/rclone_ls/) 命令默认输出原始数字。
选项 `--human-readable` 将使它们以人类可读格式输出值（使用简短的单位前缀）。

[about](/commands/rclone_about/) 命令默认以人类可读格式输出，使用命令特定的选项 `--full` 输出原始数字。

[size](/commands/rclone_size/) 命令在同一输出中同时输出人类可读和原始数字。

[tree](/commands/rclone_tree/) 命令也会考虑 `--human-readable`，但它不会使用与其他命令完全相同的表示法：它四舍五入到一位小数，并使用单字母后缀，例如 `K` 而不是 `Ki`。这样做是因为它依赖于外部库。

交互式命令 [ncdu](/commands/rclone_ncdu/) 默认显示人类可读格式，并通过按 `u` 键切换人类可读格式。

### --ignore-case-sync

使用此选项将使 rclone 在同步时忽略文件名的大小写，因此当现有文件名相同时（即使大小写不同）也不会被复制/同步。

### --ignore-checksum

通常 rclone 会检查已传输文件的校验和，如果不匹配则会给出"corrupted on transfer"错误。

你可以使用此选项跳过该检查。仅当你收到"corrupted on transfer"错误消息并且确定可能想要传输潜在损坏的数据时才应使用此选项。

### --ignore-existing

使用此选项将使 rclone 无条件跳过目标上已存在的所有文件，无论这些文件的内容如何。

虽然这不是一般推荐的选项，但在你的文件因加密而变化的情况下可能很有用。但是，如果传输被中断，它无法纠正部分传输。

执行 `move`/`moveto` 命令时，当目标上存在同名文件时，此标志将保留源位置的跳过文件不变。

### --ignore-size

通常 rclone 会查看文件的修改时间和大小来判断它们是否相等。如果设置此标志，rclone 将仅检查修改时间。如果设置了 `--checksum`，则仅检查校验和。

它还会导致 rclone 跳过验证传输后大小是否相同。

这对于与 OneDrive 之间传输文件很有用，因为 OneDrive 偶尔会错误地报告图像文件的大小（有关更多信息，请参阅 [#399](https://github.com/rclone/rclone/issues/399)）。

### -I, --ignore-times

使用此选项将使 rclone 无条件地上传所有文件，而不管目标上文件的状态如何。

通常 rclone 会跳过任何修改时间相同且大小相同的文件（或者在使用 `--checksum` 时具有相同校验和的文件）。

### --immutable

将源文件和目标文件视为不可变并禁止修改。

设置此选项后，将按请求创建和删除文件，但永远不会更新现有文件。如果现有文件在源和目标之间不匹配，rclone 将给出错误 `Source and destination exist but do not match: immutable file modified`。

注意，只有传输文件的命令（例如 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 或 [move](/commands/rclone_move/)）受此行为影响，并且仅禁止修改。文件仍然可以被显式删除（例如 [delete](/commands/rclone_delete/)、[purge](/commands/rclone_purge/)）或隐式删除（例如 [sync](/commands/rclone_sync/)、[move](/commands/rclone_move/)）。如果希望同时避免删除和修改，请使用 `copy --immutable`。

对于不可变或仅追加的数据集（特别是备份归档）来说，这可以作为额外的保护层，因为修改意味着损坏，不应传播。

### --inplace {#inplace}

`--inplace` 标志改变 rclone 在将文件上传到某些后端（设置了 `PartialUploads` 功能标志的后端）时的行为，例如：

- local
- ftp
- sftp
- pcloud

不使用 `--inplace`（默认情况）时，rclone 将首先上传到一个具有如下扩展名的临时文件，其中 `XXXXXX` 表示源文件指纹的哈希，`.partial` 是 [--partial-suffix](#partial-suffix) 的值（默认为 `.partial`）。

```text
original-file-name.XXXXXX.partial
```

（rclone 将通过在必要时截断 `original-file-name` 部分来确保最终名称不超过 100 个字符。）

当上传完成时，rclone 会将 `.partial` 文件重命名为正确的名称，覆盖该位置任何现有文件。如果上传失败，则 `.partial` 文件将被删除。

这可以防止其他用户在其新名称中看到部分上传的文件，并防止在完全上传新文件之前覆盖旧文件。

如果提供 `--inplace` 标志，rclone 将直接上传到最终名称，而不创建 `.partial` 文件。

这意味着在上传过程中，不完整的文件将在目录列表中可见，并且任何现有文件将在上传开始时被覆盖。如果传输失败，则该文件将被删除。如果传输失败，这可能导致现有文件的数据丢失。

注意，在本地文件系统上，如果你不使用 `--inplace`，硬链接（仅限 Unix）将被破坏。如果你使用 `--inplace`，将无法更新正在使用的可执行文件。

还要注意，v1.63.0 之前的 rclone 版本的行为就好像始终提供 `--inplace` 标志一样。

### -i, --interactive {#interactive}

此标志可用于告诉 rclone 你希望在执行破坏性操作之前进行手动确认。

建议在学习 rclone 时使用此标志，特别是配合 `rclone sync`。

例如：

```console
$ rclone delete --interactive /tmp/dir
rclone: delete "important-file.txt"?
y) Yes, this is OK (default)
n) No, skip this
s) Skip all delete operations with no more questions
!) Do all delete operations with no more questions
q) Exit rclone now.
y/n/s/!/q> n
```

各选项含义：

- `y`：**是**，应该执行此操作。你也可以按 Return 键触发此操作。除非你选择 `s` 或 `!`，否则每次都会询问。
- `n`：**否**，不执行此操作。除非你选择 `s` 或 `!`，否则每次都会询问。
- `s`：**跳过**以下所有此类操作，不再询问。该效果持续到 rclone 退出。如果有其他不同类型的操作，仍会提示。
- `!`：**全部执行**以下所有操作，不再询问。如果你已经决定不介意 rclone 执行此类操作，则非常有用。该效果持续到 rclone 退出。如果有其他不同类型的操作，仍会提示。
- `q`：**退出** rclone，以防万一！

### --leave-root

在 rmdirs 期间，即使根目录为空，也不会删除根目录。

### -l, --links

通常 rclone 会忽略符号链接或连接点（在 Windows 上行为类似符号链接）。被忽略的文件在同步中不会被复制、移动或删除。

如果提供此标志，rclone 将从任何受支持的后端复制符号链接，并将其作为文本文件存储在目标中，后缀为 `.rclonelink`。

文本文件将包含符号链接的目标。

`--links` / `-l` 标志为所有受支持的后端和 VFS 启用此功能。如果需要，还有仅用于 VFS 的 `--vfs-links` 和仅用于本地后端的 `--local-links` 标志。

### --list-cutoff int {#list-cutoff}

同步时，rclone 需要对目录条目进行排序后再进行比较。低于此阈值（默认 1,000,000）时，rclone 会将目录条目存储在内存中。1,000,000 个条目将占用大约 1GB 的内存来存储。高于此阈值，rclone 会将目录条目存储在磁盘上并对其进行排序，而无需占用大量内存。

这样做比在内存中排序效率稍低，并且只对基于桶的后端（例如 s3、b2、azureblob、swift）效果良好，但这些也是唯一可能在目录中拥有数百万个条目的后端。

### --log-file string

将 rclone 的所有输出记录到文件。默认情况下未启用。配合 `-v` 标志可用于跟踪同步问题。有关更多信息，请参阅[日志](#logging)部分。

如果文件存在，rclone 将追加到该文件。

注意，如果你使用 `logrotate` 程序来管理 rclone 的日志，则应使用 `copytruncate` 选项，因为 rclone 没有用于轮转日志的信号。

或者，你可以使用以下选项来管理 rclone 的内置日志轮转。

### --log-file-max-size SizeSuffix

日志文件被轮转之前的最大大小（例如 `10M`）。此 SizeSuffix 会向上取整到最接近的 MiB，或如果小于则取整为 1 MiB。

如果未设置 `--log-file`，则此选项将被忽略。

如果未设置此选项，则其他日志轮转选项也将被忽略。

例如，如果使用以下标志：

```console
rclone --log-file rclone.log --log-file-max-size 1M --log-file-max-backups 3
```

则会创建如下所示的日志文件：

```console
$ ls -l
-rw-------  1 user user  1048491 Apr 11 17:15 rclone-2025-04-11T17-15-29.998.log
-rw-------  1 user user  1048511 Apr 11 17:15 rclone-2025-04-11T17-15-30.467.log
-rw-------  1 user user  1048559 Apr 11 17:15 rclone-2025-04-11T17-15-30.543.log
-rw-------  1 user user   521602 Apr 11 17:15 rclone.log
```

其中 `rclone.log` 是当前文件。

### --log-file-compress

如果设置，则使用 gzip 压缩轮转的日志文件。这会将旧日志文件的扩展名更改为 `.log.gz`。

默认为 false——不压缩日志文件。

### --log-file-max-age Duration

保留旧日志文件的最长时间（例如 `7d`）。此值向上取整到最近的天，或如果小于则取整为 1 天。

默认值为保留所有旧日志文件。

### --log-file-max-backups int

要保留的旧日志文件的最大数量。

默认值为保留所有旧日志文件。

### --log-format string

以逗号分隔的日志格式选项列表。可接受的选项包括：

- `date` - 以 YYYY/MM/YY 格式在日志中添加日期。
- `time` - 以 HH:MM:SS 格式在日志中添加时间。
- `microseconds` - 以 HH:MM:SS.SSSSSS 格式在时间中添加微秒。
- `UTC` - 使日志使用 UTC 而不是本地时间。
- `longfile` - 添加日志语句的源文件和行号。
- `shortfile` - 添加日志语句的源文件和行号。

- `pid` - 将进程 ID 添加到日志中——与 `rclone mount --daemon` 一起使用很有用。
- `nolevel` - 不将级别添加到日志中。
- `json` - 等价于添加 `--use-json-log`

它们按上述顺序添加到日志行中。

默认日志格式为 `"date,time"`。

### --log-level LogLevel

这设置 rclone 的日志级别。默认日志级别为 `NOTICE`。

`DEBUG` 等价于 `-vv`。它会输出大量调试信息——对错误报告和深入了解 rclone 的行为非常有用。

`INFO` 等价于 `-v`。它会输出每次传输的信息，并默认每分钟打印一次统计信息。

`NOTICE` 是未提供任何日志记录标志时的默认日志级别。它在一切正常运行时输出很少的内容。它会输出警告和重要事件。

`ERROR` 等价于 `-q`。它只输出错误消息。

另请参阅[日志](#logging)部分。

### --windows-event-log LogLevel

如果配置了此项（默认为 `OFF`），那么此级别及以上的日志将**除了**正常日志之外，还会被记录到 Windows 事件日志中。这些日志将以下面描述的 JSON 格式记录，而不管主日志的配置格式如何。

Windows 事件日志只有 3 个严重级别 `Info`、`Warning` 和 `Error`。如果启用，我们将按如下方式映射 rclone 级别：

- `Error` ← `ERROR`（及以上）
- `Warning` ← `WARNING`（注意，此级别已定义但当前未使用）。
- `Info` ← `NOTICE`、`INFO` 和 `DEBUG`。

如果 rclone 拥有创建所需注册表项的足够权限，它会将其日志源声明为 "rclone"。如果没有，则日志将显示为 "Application"。你可以以管理员身份运行一次 `rclone version --windows-event-log DEBUG` 来预先创建注册表项。

**注意** `--windows-event-log` 级别必须大于（更严重）或等于 `--log-level`。例如，要将 DEBUG 记录到日志文件但将 ERROR 记录到事件日志，你可以使用：

```text
--log-file rclone.log --log-level DEBUG --windows-event-log ERROR
```

此选项仅在 Windows 平台上受支持。

### --use-json-log

此选项将日志格式切换为 JSON。然后日志消息将作为单个 JSON 对象流式传输，包含字段：`level`、`msg`、`source` 和 `time`。生成的格式有时称为[换行符分隔的 JSON](https://en.wikipedia.org/wiki/JSON_streaming#Newline-delimited_JSON)（NDJSON），或 JSON Lines（JSONL）。这非常适合由传统的面向行的工具和 shell 管道处理，但完整的日志文件不是严格有效的 JSON，需要能够处理它的解析器。

JSON 日志将打印在单行上，但此处显示为展开以增加清晰度。

```json
{
  "time": "2025-05-13T17:30:51.036237518+01:00",
  "level": "debug",
  "msg": "4 go routines active\n",
  "source": "cmd/cmd.go:298"
}
```

完成的数据传输日志将包含额外的 `size` 信息。关于特定对象的日志还将包含 `object` 和 `objectType` 字段。

```json
{
  "time": "2025-05-13T17:38:05.540846352+01:00",
  "level": "info",
  "msg": "Copied (new) to: file2.txt",
  "size": 6,
  "object": "file.txt",
  "objectType": "*local.Object",
  "source": "operations/copy.go:368"
}
```

统计日志将包含 `stats` 字段，这与从 rc 调用 [core/stats](/rc/#core-stats) 返回的内容相同。

```json
{
  "time": "2025-05-13T17:38:05.540912847+01:00",
  "level": "info",
  "msg": "...text version of the stats...",
  "stats": {
    "bytes": 6,
    "checks": 0,
    "deletedDirs": 0,
    "deletes": 0,
    "elapsedTime": 0.000904825,
    ...truncated for clarity...
    "totalBytes": 6,
    "totalChecks": 0,
    "totalTransfers": 1,
    "transferTime": 0.000882794,
    "transfers": 1
  },
  "source": "accounting/stats.go:569"
}
```

### --low-level-retries int

此选项控制 rclone 进行的低级重试次数。

低级重试用于重试失败的操作——通常是一次 HTTP 请求。例如，这可能是上传大文件的一个块。你将在使用 `-v` 标志时在日志中看到低级重试。

在正常操作中不需要从默认值更改。但是，如果你遇到大量低级重试，你可能希望减小该值，以便 rclone 更快地进入高级重试（请参阅 `--retries` 标志）。

使用 `--low-level-retries 1` 禁用低级重试。

### --max-backlog int

这是同步/复制/移动中排队等待检查或传输的文件积压的最大允许数量。

此值可以设置得任意大。仅当队列在使用时才会使用内存。注意，当积压正在使用时，它将使用大约 N KiB 的内存。

将此值设置得大一些允许 rclone 更准确地计算待处理文件的数量，给出更准确的预计完成时间，并使 `--order-by` 工作得更准确。

将此值设置得小一些将使 rclone 更加同步于远端列表，这可能是可取的。

将此值设置为负数将使积压尽可能大。

### --max-buffer-memory SizeSuffix {#max-buffer-memory}

如果设置，则不要分配超过给定数量的内存作为缓冲区。如果未设置或设置为 `0` 或 `off`，则不会限制正在使用的内存量。

这包括 `--buffer` 标志创建的缓冲区使用的内存，以及多线程传输使用的缓冲区。

大多数多线程传输不占用额外的内存，但有些会（取决于后端，例如 s3 后端用于上传）。这意味着在将 `--transfers` 设置得尽可能高与内存使用之间存在矛盾。

设置 `--max-buffer-memory` 允许控制缓冲区内存，使其不会让机器不堪重负，并允许将 `--transfers` 设置得很大。

### --max-connections int

这设置对后端 API 的最大并发调用数。根据所使用后端以及 HTTP1 与 HTTP2 的使用情况，它可能无法 1:1 映射到 TCP 或 HTTP 连接。

下载文件时，后端仅限制流的初始打开。批量数据下载不计入连接数。这意味着 `--max-connections` 标志不会限制下载的总数。

注意，此设置可能导致死锁，因此应谨慎使用。

如果你正在执行 sync 或 copy，请确保 `--max-connections` 比 `--transfers` 和 `--checkers` 之和多 1。

如果你使用 `--check-first`，则 `--max-connections` 只需要比 `--checkers` 和 `--transfers` 中的最大值多 1。

因此对于 `--max-connections 3`，你可以使用 `--checkers 2 --transfers 2 --check-first` 或 `--checkers 1 --transfers 1`。

对于执行多部分上传的后端，此标志可用于限制同时传输的块数。

### --max-delete int

这告诉 rclone 删除的文件不超过 N 个。如果超过该限制，将产生致命错误，rclone 将停止正在进行的操作。

### --max-delete-size SizeSuffix

当删除的总大小达到指定大小时，rclone 将停止删除文件。默认为关闭。

如果超过该限制，将产生致命错误，rclone 将停止正在进行的操作。

### --max-depth int

这会修改除 purge 之外的所有命令的递归深度。

因此，如果执行 `rclone --max-depth 1 ls remote:path`，你将只看到顶层目录中的文件。使用 `--max-depth 2` 表示你将看到前两个目录级别中的所有文件，依此类推。

出于历史原因，`lsd` 命令默认使用 `--max-depth` 1——你可以使用命令行标志覆盖此值。

你可以使用此命令禁用递归（使用 `--max-depth 1`）。

注意，如果将其与 `sync` 和 `--delete-excluded` 一起使用，未递归访问的文件将被视为已排除，并将在目标上被删除。如果你不确定会发生什么，请先使用 `--dry-run` 进行测试。

### --max-duration Duration

Rclone 将在运行达到指定时长时停止传输。默认为关闭。

达到限制时，所有传输将立即停止。使用 `--cutoff-mode` 修改此行为。

如果达到时长限制，rclone 将以退出码 10 退出。

### --max-transfer SizeSuffix

Rclone 将在传输达到指定大小时停止传输。默认为关闭。

达到限制时，所有传输将立即停止。使用 `--cutoff-mode` 修改此行为。

如果达到传输限制，rclone 将以退出码 8 退出。

### --cutoff-mode HARD|SOFT|CAUTIOUS

配置 `--max-transfer` 和 `--max-duration` 的行为。

`HARD` 将在 rclone 达到限制时立即停止传输。这是默认设置。

`SOFT` 将在 rclone 达到限制时停止启动新传输。

`CAUTIOUS` 将尝试阻止 rclone 达到限制。仅适用于 `--max-transfer`。

### -M, --metadata

设置此标志使 rclone 能够将元数据从源复制到目标。对于本地后端，这是所有权、权限、xattr 等。有关更多信息，请参阅[元数据部分](#metadata)。

### --metadata-mapper SpaceSepList {#metadata-mapper}

如果提供参数 `--metadata-mapper /path/to/program`，rclone 将使用该程序将元数据从源对象映射到目标对象。

此标志的参数应该是一个命令，后跟可选的以空格分隔的参数列表。如果某个参数中包含空格，则用 `"` 括起来；如果想在参数中使用字面的 `"`，则用 `"` 括起参数并将 `"` 加倍。有关更多信息，请参阅 [CSV encoding](https://godoc.org/encoding/csv)。

```text
--metadata-mapper "python bin/test_metadata_mapper.py"
--metadata-mapper 'python bin/test_metadata_mapper.py "argument with a space"'
--metadata-mapper 'python bin/test_metadata_mapper.py "argument with ""two"" quotes"'
```

这使用一个简单的基于 JSON 的协议，输入来自 STDIN，输出到 STDOUT。对于复制的每个文件和目录都会调用此程序，并且可能会并发调用。

程序的职责是接收输入上的元数据 blob，并将其转换为适合目标后端的输出元数据 blob。

程序的输入（通过 STDIN）可能如下所示。这为 `Metadata` 提供了一些可能很重要的上下文。

- `SrcFs` 是对象当前所在远端的配置字符串。
- `SrcFsType` 是源后端的名称。
- `DstFs` 是对象要复制到的远端的配置字符串
- `DstFsType` 是目标后端的名称。
- `Remote` 是对象相对于根的路径。
- `Size`、`MimeType`、`ModTime` 是对象的属性。
- `IsDir` 如果是目录则为 `true`（尚未实现）。
- `ID` 是对象的源 `ID`（如果已知）。
- `Metadata` 是后端特定的元数据，如后端文档中所述。

```json
{
  "SrcFs": "gdrive:",
  "SrcFsType": "drive",
  "DstFs": "newdrive:user",
  "DstFsType": "onedrive",
  "Remote": "test.txt",
  "Size": 6,
  "MimeType": "text/plain; charset=utf-8",
  "ModTime": "2022-10-11T17:53:10.286745272+01:00",
  "IsDir": false,
  "ID": "xyz",
  "Metadata": {
    "btime": "2022-10-11T16:53:11Z",
    "content-type": "text/plain; charset=utf-8",
    "mtime": "2022-10-11T17:53:10.286745272+01:00",
    "owner": "user1@domain1.com",
    "permissions": "...",
    "description": "my nice file",
    "starred": "false"
  }
}
```

然后程序应按需修改输入并将其发送到 STDOUT。返回的 `Metadata` 字段将整体用于目标对象。其他字段将被忽略。注意，在此示例中，我们翻译了用户名和权限，并向描述中添加了一些内容：

```json
{
  "Metadata": {
    "btime": "2022-10-11T16:53:11Z",
    "content-type": "text/plain; charset=utf-8",
    "mtime": "2022-10-11T17:53:10.286745272+01:00",
    "owner": "user1@domain2.com",
    "permissions": "...",
    "description": "my nice file [migrated from domain1]",
    "starred": "false"
  }
}
```

也可以在此处删除元数据。

一个实现上述转换的 Python 程序示例可能如下所示。

```python
import sys, json

i = json.load(sys.stdin)
metadata = i["Metadata"]
# Add tag to description
if "description" in metadata:
    metadata["description"] += " [migrated from domain1]"
else:
    metadata["description"] = "[migrated from domain1]"
# Modify owner
if "owner" in metadata:
    metadata["owner"] = metadata["owner"].replace("domain1.com", "domain2.com")
o = { "Metadata": metadata }
json.dump(o, sys.stdout, indent="\t")
```

你可以在 rclone 源代码的 [bin/test_metadata_mapper.py](https://github.com/rclone/rclone/blob/master/bin/test_metadata_mapper.py) 中找到此示例（略有扩展）。

如果你想在日志中查看元数据映射器的输入和它返回的输出，可以使用 `-vv --dump mapper`。

请参阅[元数据部分](#metadata)了解更多信息。

### --metadata-set stringArray

以 `key=value` 格式指定字符串值，以便在上传时添加具有值 `value` 的元数据 `key`。可以根据需要重复多次。请参阅[元数据部分](#metadata)了解更多信息。

### --modify-window Duration

在检查文件是否已修改时，这是文件可以具有且仍被视为等效的最大允许时间差。

默认值为 `1ns`，除非被远端覆盖。例如，OS X 仅将修改时间存储到最近的秒，因此如果你在 OS X 文件系统上读写，默认值将是 `1s`。

此命令行标志允许你覆盖计算出的默认值。

### --multi-thread-write-buffer-size SizeSuffix

使用多线程传输时，rclone 将在写入磁盘之前为每个线程在内存中缓冲指定数量的字节。

如果底层文件系统不能很好地处理文件中不同位置的大量小写操作，这可以提高性能，因此如果看到传输受磁盘写入速度限制，可以尝试不同的值。对于机械磁盘和远程文件系统，较大的值可能很有用。

尽管如此，默认值 `128k` 几乎可以应对所有用例，所以在更改之前请确保网络不是真正的瓶颈。

最后一个提示，大小不是唯一因素：块大小（或类似概念）也会产生影响。在一种情况下，我们观察到正好是 16k 的倍数比其它值表现要好得多。

### --multi-thread-chunk-size SizeSuffix

通常多线程传输的块大小由后端设置。但是某些后端（如 `local` 和 `smb`，它们实现了 `OpenWriterAt` 但未实现 `OpenChunkWriter`）没有自然的块大小。

在这种情况下，将使用此选项的值（默认 64Mi）。

### --multi-thread-cutoff SizeSuffix {#multi-thread-cutoff}

在将超过指定大小的文件传输到支持的后端时，rclone 将使用多个线程来传输该文件（默认 256M）。

支持的后端在[概述](/overview/#optional-features)中标记为 `MultithreadUpload`。（它们需要实现 `OpenWriterAt` 或 `OpenChunkWriter` 内部接口之一。）其中包括 `local`、`s3`、`azureblob`、`b2`、`oracleobjectstorage` 和 `smb`（在撰写本文时）。

在本地磁盘上，rclone 预分配文件（在 unix 上使用 `fallocate(FALLOC_FL_KEEP_SIZE)`，在 Windows 上使用 `NTSetInformationFile`，两者都不耗时），然后每个线程直接在文件的正确位置写入。这意味着 rclone 不会创建碎片化或稀疏文件，并且在传输结束时不会有任何组装时间。

用于传输的线程数由 `--multi-thread-streams` 控制。

如果你希望查看有关线程的信息，请使用 `-vv`。

这将适用于 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 和 [move](/commands/rclone_move/) 命令以及相关的 [copyto](/commands/rclone_copyto/)、[moveto](/commands/rclone_moveto/) 命令。如果 `--vfs-cache-mode` 设置为 `writes` 或更高，则多线程传输将用于 `rclone mount` 和 `rclone serve`。

大多数多线程传输不占用额外的内存，但有些会（例如上传到 s3）。在最坏的情况下，内存使用量最多为 `--transfers` \* `--multi-thread-chunk-size` \* `--multi-thread-streams`，或者具体对于 s3 后端为 `--transfers` \* `--s3-chunk-size` \* `--s3-concurrency`。但是你可以使用 [--max-buffer-memory](/docs/#max-buffer-memory) 标志来控制此处使用的最大内存。

**注意** 这**仅**适用于作为目标的支持后端，但作为源可以适用于任何后端。

**注意** 对于本地到本地的复制，多线程复制被禁用，因为不使用多线程会更快，除非显式设置 `--multi-thread-streams`。

**注意** 在 Windows 上，对本地磁盘使用多线程传输会导致生成的文件成为[稀疏文件](https://en.wikipedia.org/wiki/Sparse_file)。使用 `--local-no-sparse` 禁用稀疏文件（这可能会在传输开始时造成长时间延迟），或者使用 `--multi-thread-streams 0` 禁用多线程传输。

### --multi-thread-streams int

使用多线程传输时（参见上面的 `--multi-thread-cutoff`），这设置要使用的流数。设置为 `0` 以禁用多线程传输（默认 4）。

如果后端有 `--backend-upload-concurrency` 设置（例如 `--s3-upload-concurrency`），则当该设置大于 `--multi-thread-streams` 的值或未设置 `--multi-thread-streams` 时，将使用该设置作为传输数。

### --name-transform stringArray

`--name-transform` 为 `rclone copy`、`rclone sync` 和 `rclone move` 引入路径名转换。这些转换允许在传输操作期间通过应用前缀、后缀和其他更改来修改源和目标文件名。有关详细文档和示例，请参阅 [`convmv`](/commands/rclone_convmv/)。

### --no-check-dest

`--no-check-dest` 可与 `move` 或 `copy` 一起使用，导致 rclone 在复制文件时不检查目标。

这意味着：

- 不列出目标，从而最小化 API 调用
- 始终传输文件
- 这可能会在允许重复的远端（例如 Google Drive）上造成重复
- 建议使用 `--retries 1`，否则在重试时会再次传输所有内容

如果你知道目标上没有任何文件，此标志可用于最小化事务。

这是一个专门标志，大多数用户应忽略！

### --no-gzip-encoding

不要设置 `Accept-Encoding: gzip`。这意味着 rclone 不会自动向服务器请求压缩文件。如果你已将服务器设置为返回带有 `Content-Encoding: gzip` 的文件，但上传了压缩文件，则此选项很有用。

在正常操作中无需设置此选项，这样做会降低 rclone 的网络传输效率。

### --no-traverse

`--no-traverse` 标志控制在使用 `copy` 或 `move` 命令时是否遍历目标文件系统。`--no-traverse` 与 `sync` 不兼容，如果与 `sync` 一起提供，则会被忽略。

如果你只复制少量文件（或过滤掉了大部分文件）和/或目标上有大量文件，则 `--no-traverse` 将阻止 rclone 列出目标并节省时间。

但是，如果你正在复制大量文件，特别是当所考虑的大量文件未更改且不需要复制时，则不应使用 `--no-traverse`。

请参阅 [rclone copy](/commands/rclone_copy/) 了解使用示例。

### --no-unicode-normalization

在同步过程中不要对文件名中的 unicode 字符进行规范化。

有时，操作系统会以分解形式存储包含 unicode 部分的文件名（特别是 macOS）。然后一些云存储系统会重新组合 unicode，导致如果数据被复制回本地文件系统时会出现重复文件。

使用此标志将禁用该功能，将每个 unicode 字符视为唯一。例如，默认情况下，é 和 é 会被规范化为同一字符。使用 `--no-unicode-normalization` 时，它们将被视为唯一字符。

### --no-update-modtime

使用此标志时，rclone 不会像通常那样在远程文件的修改时间不正确时更新它们。

当远程与其他工具（例如 Google Drive 客户端）也进行同步时，这可能很有用。

### --no-update-dir-modtime

使用此标志时，rclone 不会像通常那样在远程目录的修改时间不正确时更新它们。

### --order-by string

`--order-by` 标志控制 `rclone sync`、`rclone copy` 和 `rclone move` 中积压文件的处理顺序。

排序字符串的构造方式如下。第一部分描述要测量的内容：

- `size` - 按文件大小排序
- `name` - 按文件的完整路径排序
- `modtime` - 按文件的修改日期排序

可以通过逗号附加修饰符：

- `ascending` 或 `asc` - 排序时最小（或最旧）的优先处理
- `descending` 或 `desc` - 排序时最大（或最新）的优先处理
- `mixed` - 排序时一部分线程优先处理最小的，另一部分处理最大的

如果修饰符是 `mixed`，则可以有一个可选的百分比（默认为 `50`），例如 `size,mixed,25`，表示 25% 的线程应处理最小的项，75% 处理最大的。处理最小的线程始终先处理最小的，处理最大的线程始终先处理最大的。当你要传输大文件和小文件的混合时，`mixed` 模式可用于最小化传输时间——大文件保证有上传线程和带宽，而小文件会持续处理。

如果未提供修饰符，则顺序为 `ascending`。

例如：

- `--order-by size,desc` - 先发送最大的文件
- `--order-by modtime,ascending` - 先发送最旧的文件
- `--order-by name` - 按路径字母顺序先发送文件

如果未提供 `--order-by` 标志或提供的为空字符串，则使用默认排序，即按扫描顺序。使用 `--checkers 1` 时，这基本是字母顺序，但使用默认的 `--checkers 8` 时，这在某种程度上是随机的。

#### 限制

`--order-by` 标志不会对数据进行单独的扫描。这意味着在以下情况下，它可能会按指定顺序之外传输一些文件：

- 积压中没有文件或源尚未完全扫描
- 积压中的文件数超过 [--max-backlog](#max-backlog-int)

Rclone 将尽力传输其拥有的最佳文件，因此实际上这应该不会引起问题。可以将 `--order-by` 视为尽力而为的标志，而不是完美的顺序。

如果需要完美的顺序，则需要指定 [--check-first](#check-first)，它将在传输任何文件之前先找到所有需要传输的文件。

### --partial-suffix string {#partial-suffix}

当不使用 [--inplace](#inplace) 时，它会导致 rclone 使用 `--partial-suffix` 作为临时文件的后缀。

后缀长度限制为 16 个字符。

默认值为 `.partial`。

### --password-command SpaceSepList {#password-command}

此标志提供一个程序，在运行时应提供配置密码。这是 rclone 提示输入密码或设置 `RCLONE_CONFIG_PASS` 变量之外的另一种选择。它也用于首次设置配置密码时。

此参数应该是一个命令，后跟以空格分隔的参数列表。如果某个参数中包含空格，则用 `"` 括起来；如果想在参数中使用字面的 `"`，则用 `"` 括起参数并将 `"` 加倍。有关更多信息，请参阅 [CSV encoding](https://godoc.org/encoding/csv)。

例如：

```text
--password-command "echo hello"
--password-command 'echo "hello with space"'
--password-command 'echo "hello with ""quotes"" and space"'
```

注意，更改配置密码时，将设置环境变量 `RCLONE_PASSWORD_CHANGE=1`。这可用于区分对配置文件的初次解密和新密码。

有关更多信息，请参阅[配置加密](#configuration-encryption)。

有关示例，请参阅 [Wiki 上的 Windows PowerShell 示例](https://github.com/rclone/rclone/wiki/Windows-Powershell-use-rclone-password-command-for-Config-file-password)。

### -P, --progress

此标志使 rclone 在终端的一个静态块中更新统计信息，提供传输的实时概览。

任何日志消息都会在静态块上方滚动。日志消息会将静态块向下推到终端底部，并使其停留在那里。

通常此信息每 500 毫秒更新一次，但此周期可以通过 `--stats` 标志覆盖。

此标志可以与 `--stats-one-line` 标志一起使用，以获得更简单的显示。

要更改文件名的显示长度（以适应不同的终端宽度），请参阅 `--stats-file-name-length` 选项。默认输出针对 80 个字符宽的终端格式化。

注意：在 Windows 上，在[此 bug](https://github.com/Azure/go-ansiterm/issues/26) 修复之前，使用 `--progress` 时，所有非 ASCII 字符都将替换为 `.`。

### --progress-terminal-title

当与 `-P/--progress` 一起使用时，此标志会将字符串 `ETA: %s` 打印到终端标题。

### -q, --quiet

此标志将 rclone 的输出限制为仅错误消息。

### --refresh-times

`--refresh-times` 标志可用于在不支持哈希的后端上更新不同步的现有文件的修改时间。

如果你上传了带有不正确时间戳的文件，现在希望更正它们，则这很有用。

此标志**仅**对不支持哈希的目标（例如 `crypt`）有用。

此标志可用于任何同步命令 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 或 [move](/commands/rclone_move/)。

要使用此标志，你需要执行修改时间同步（因此不使用 `--size-only` 或 `--checksum`）。使用 `--size-only` 或 `--checksum` 时，该标志无效。

如果使用此标志，当 rclone 准备上传文件时，它会检查目标上是否存在现有文件。如果该文件与源在大小（和校验和，如果可用）上匹配但时间戳不同，则 rclone 不会重新上传，而是更新目标文件上的时间戳。如果校验和不匹配，rclone 将上传新文件。如果缺少校验和（例如在 `crypt` 后端上），rclone 将更新时间戳。

注意，一些远端无法在不重新上传文件的情况下设置修改时间，因此此标志在这些远端上用处不大。

通常，如果你正在执行修改时间同步，rclone 将在不使用 `--refresh-times` 的情况下更新修改时间，前提是远端支持校验和**且**校验和匹配。但是，如果缺少校验和，rclone 将上传文件而不是设置时间戳，因为这是安全的行为。

### --retries int

如果整个同步失败，重试那么多次（默认 3 次）。

某些远端可能不可靠，几次重试有助于获取因错误而未传输的文件。

使用 `--retries 1` 禁用重试。

### --retries-sleep Duration

这设置由 `--retries` 指定的每次重试之间的间隔。

默认值为 `0`。使用 `0` 禁用。

### --server-side-across-configs

允许服务端操作（例如 copy 或 move）跨不同配置工作。

如果你希望在使用相同后端但配置不同的两个远端之间执行服务端 copy 或 move，这可能会很有用。

注意默认情况下未启用此功能，因为 rclone 难以判断它是否可以在任何两个配置之间工作。

### --size-only

通常 rclone 会查看文件的修改时间和大小来判断它们是否相等。如果设置此标志，rclone 将仅检查大小。

当从 Dropbox 传输由桌面同步客户端修改的文件时，这可能很有用，因为该客户端不像 rclone 那样设置校验和或修改时间。

### --stats Duration

传输数据的命令（[sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/)、[copyto](/commands/rclone_copyto/)、[move](/commands/rclone_move/)、[moveto](/commands/rclone_moveto/)）会按固定间隔打印数据传输统计信息以显示其进度。

这设置间隔。

默认值为 `1m`。使用 `0` 禁用。

如果设置了统计间隔，则所有命令都可以显示统计信息。这对于运行其他命令（例如 `check` 或 `mount`）时很有用。

统计信息默认在 `INFO` 级别记录，这意味着它们不会在默认日志级别 `NOTICE` 下显示。使用 `--stats-log-level NOTICE` 或 `-v` 使其显示。有关日志级别的更多信息，请参阅[日志](#logging)部分。

注意，在 macOS 上，你可以发送 SIGINFO（通常是终端中的 ctrl-T）以立即打印统计信息。

### --stats-file-name-length int

默认情况下，`--stats` 输出会将超过 40 个字符的文件名和路径截断。这等同于提供 `--stats-file-name-length 40`。使用 `--stats-file-name-length 0` 禁用对统计信息中打印的文件名的任何截断。

### --stats-log-level LogLevel

显示 `--stats` 输出的日志级别。可以是 `DEBUG`、`INFO`、`NOTICE` 或 `ERROR`。默认值为 `INFO`。这意味着在默认的 `NOTICE` 日志级别下，统计信息将不会显示——如果希望它们显示，请使用 `--stats-log-level NOTICE`。有关日志级别的更多详细信息，请参阅[日志](#logging)部分。

### --stats-one-line

当指定此选项时，rclone 将统计信息压缩为单行，仅显示最重要的统计信息。

### --stats-one-line-date

当指定此选项时，rclone 会启用单行统计信息，并在
<!-- markdownlint-disable-next-line no-space-in-code -->
显示前添加一个日期字符串。默认值为 `2006/01/02 15:04:05 - `

### --stats-one-line-date-format string

当指定此选项时，rclone 会启用单行统计信息，并在显示前添加用户提供的日期字符串。日期字符串必须用引号引起来。日期格式语法遵循 [golang 规范](https://golang.org/pkg/time/#Time.Format)。

### --stats-unit string

默认情况下，数据传输速率将以字节/秒为单位打印，对应 `--stats-unit bytes`。

此选项允许通过指定 `--stats-unit bits` 以比特/秒为单位打印数据速率。数据传输量仍将以字节为单位报告。

速率以二进制单位而非 SI 单位报告。因此 1 Mbit/s 等于 1,048,576 bit/s 而不是 1,000,000 bit/s。

### --suffix string

在使用 [sync](/commands/rclone_sync/)、[copy](/commands/rclone_copy/) 或 [move](/commands/rclone_move/) 时，任何将被覆盖或删除的文件都将添加此后缀。如果存在具有相同路径的文件（添加后缀之后），则该文件将被覆盖。

使用的远端必须支持服务端 move 或 copy，并且必须使用与同步目标相同的远端。

这用于向当前目录中的文件添加后缀，或与 `--backup-dir` 一起使用。有关更多信息，请参阅 `--backup-dir`。

例如：

```console
rclone copy --interactive /path/to/local/file remote:current --suffix .bak
```

会将 `/path/to/local` 复制到 `remote:current`，但任何将被更新或删除的文件会添加 .bak 后缀。

如果在没有 `--backup-dir` 的情况下将 `rclone sync` 与 `--suffix` 一起使用，建议添加一条过滤规则排除此后缀，否则 `sync` 将删除备份文件。

```console
rclone sync --interactive /path/to/local/file remote:current --suffix .bak --exclude "*.bak"
```

### --suffix-keep-extension

在使用 `--suffix` 时，设置此选项会导致 rclone 将后缀放在它备份的文件的扩展名之前，而不是之后。

因此假设我们使用 `--suffix -2019-01-01`，没有该标志时 `file.txt` 将被备份为 `file.txt-2019-01-01`，使用该标志时将被备份为 `file-2019-01-01.txt`。这有助于确保带后缀的文件仍然可以打开。

如果文件有两个（或更多）扩展名，并且第二个（或后续）扩展名被识别为有效的 mime 类型，则后缀将放在该扩展名之前。因此 `file.tar.gz` 将被备份为 `file-2019-01-01.tar.gz`，而 `file.badextension.gz` 将被备份为 `file.badextension-2019-01-01.gz`。

### --syslog

在支持的操作系统上（不包括 Windows 或 Plan9）将所有日志输出发送到 syslog。

这对于在脚本中或 `rclone mount` 中运行 rclone 非常有用。

### --syslog-facility string

如果使用 `--syslog`，这将设置 syslog 工具（例如 `KERN`、`USER`）。有关可能的工具列表，请参阅 `man syslog`。默认工具为 `DAEMON`。

### --temp-dir string

指定 rclone 用于临时文件的目录，以覆盖默认值。确保该目录存在并具有可访问的权限。

默认情况下，将使用操作系统的临时目录：

- 在 Unix 系统上，`$TMPDIR`（如果非空），否则 `/tmp`。
- 在 Windows 上，来自 `%TMP%`、`%TEMP%`、`%USERPROFILE%` 或 Windows 目录的第一个非空值。

当使用此选项覆盖默认值时，指定的路径将在 Unix 系统上设置为环境变量 `TMPDIR` 的值，在 Windows 上设置为 `TMP` 和 `TEMP` 的值。

你可以使用 [config paths](/commands/rclone_config_paths/) 命令查看当前值。

### --tpslimit float

将每秒事务数限制为此数字。默认为 0，表示不限速。

事务大致定义为一次 API 调用；其确切含义将取决于后端。对于基于 HTTP 的后端，它是一次 HTTP PUT/GET/POST 等及其响应。对于 FTP/SFTP，它是 TCP 上的一次往返事务。

例如，要将 rclone 限制为每秒 10 个事务，使用 `--tpslimit 10`，或每 2 秒 1 个事务，使用 `--tpslimit 0.5`。

当 rclone 的每秒事务数对云存储提供商造成问题时（例如导致你被封禁或限速），请使用此选项。

这对于 `rclone mount` 控制使用它的应用程序的行为非常有用。

此限制适用于所有基于 HTTP 的后端以及 FTP 和 SFTP 后端。它不适用于本地后端或 Storj 后端。

另请参阅 `--tpslimit-burst`。

### --tpslimit-burst int

`--tpslimit` 的最大突发事务数（默认 `1`）。

通常 `--tpslimit` 恰好每秒执行指定数量的事务。但是，如果你提供 `--tps-burst`，那么 rclone 可以在空闲时节省一些事务，从而提供最多与所提供参数相等的突发。

例如，如果你提供 `--tpslimit-burst 10`，那么如果 rclone 空闲了超过 10*`--tpslimit` 的时间，它可以非常快速地执行 10 个事务，然后再次受到限制。

这可以在不改变长期平均每秒事务数的情况下提高 `--tpslimit` 的性能。

### --track-renames

默认情况下，rclone 不跟踪重命名的文件，因此如果你在本地重命名一个文件然后将其同步到远端，rclone 将删除远端上的旧文件并上传一个新副本。

带 `--track-renames` 的 rclone 同步像普通同步一样运行，但会跟踪存在于目标但不存在于源（通常会被删除）以及存在于源但不存在于目标（通常会被传输）的对象。这些对象成为重命名的候选。

同步之后，rclone 根据指定的 `--track-renames-strategy` 匹配仅在源和仅在目标的对象，然后要么重命名目标对象，要么传输源并删除目标对象。`--track-renames` 像所有 rclone 同步一样是无状态的。

要使用此标志，目标必须支持服务端 copy 或服务端 move，并且要使用基于哈希的 `--track-renames-strategy`（默认），源和目标必须具有兼容的哈希。

如果目标不支持服务端 copy 或 move，rclone 将回退到默认行为，并在控制台上记录一条错误级别的消息。

如果 `--track-renames-strategy` 包含 `hash`，则目前不支持加密目标。

注意 `--track-renames` 与 `--no-traverse` 不兼容，并且它使用额外的内存来跟踪所有重命名候选。

还要注意 `--track-renames` 与 `--delete-before` 不兼容，并将选择 `--delete-after` 而不是 `--delete-during`。

### --track-renames-strategy string

此选项更改 `--track-renames` 的文件匹配条件。

匹配由这些标记的逗号分隔选择控制：

- `modtime` - 文件的修改时间 - 并非所有后端都支持
- `hash` - 文件内容的哈希 - 并非所有后端都支持
- `leaf` - 不包括其目录名的文件名
- `size` - 文件的大小（始终启用）

默认选项为 `hash`。

使用 `--track-renames-strategy modtime,leaf` 将仅根据修改时间、文件名的 leaf 和大小来匹配文件。

使用 `--track-renames-strategy modtime` 或 `leaf` 可以为加密目标启用 `--track-renames` 支持。

注意 `hash` 策略不支持加密目标。

### --delete-(before,during,after)

此选项允许你在同步文件夹时指定目标上的文件何时被删除。

指定值 `--delete-before` 将在开始任何新文件或更新文件的传输**之前**删除目标上存在但源上不存在的所有文件。这使用两次文件系统遍历，一次用于删除，一次用于复制。

指定 `--delete-during` 将在检查和上传文件时删除文件。这是最快的选项，占用内存最少。

指定 `--delete-after`（默认值）将延迟删除文件，直到所有新/已更新的文件成功传输。要删除的文件在复制阶段收集，然后在复制阶段成功完成后删除。要删除的文件保存在内存中，因此此模式可能使用更多内存。这是最安全的模式，因为它仅在没有后续错误的情况下删除文件。如果在开始删除之前有错误，你将收到消息 `not deleting files as there were IO errors`。

### --fast-list

当进行涉及目录列表的任何操作时（例如 `sync`、`copy`、`ls`——几乎每个命令），rclone 有不同的策略可供选择。

基本策略是列出一个目录并在处理完该目录后使用更多目录列表处理任何子目录。这是一项强制性的后端功能，称为 `List`，意味着所有后端都支持此功能。此策略使用少量内存，并且由于可以并行化，对于涉及处理列表结果的操作来说速度很快。

某些后端支持替代策略，其中可以在一次（或少量）事务中列出目录下的所有文件。Rclone 通过名为 [`ListR`](/overview/#listr) 的可选后端功能支持此替代策略。你可以在存储系统概述文档的[可选功能](/overview/#optional-features)部分中查看哪些后端启用了此功能（这些往往是基于桶的后端，例如 S3、B2、GCS、Swift）。此策略对高度递归操作需要的事务数更少，这在按事务收费或严重限速的后端上很重要。根据不同的参数，它可能更快（由于事务更少）或更慢（因为无法并行化），并且如果 rclone 必须将整个列表保存在内存中，则可能需要更多内存。

rclone 为给定操作选择哪种列出策略比较复杂，但总的来说它会尝试选择最佳策略。在不需要将列出的文件存储在内存中的情况下，例如对于无限制递归的 `ls` 命令变体，它将优先使用 `ListR`。在其他情况下，它将优先使用 `List`，例如对于 `sync` 和 `copy`，此时它需要将列出的文件保存在内存中，并在其上执行并行化可能带来巨大优势的操作。

Rclone 无法考虑所有相关参数来决定最佳策略，因此允许你通过两种方式影响选择：可以通过使用 [--disable](#disable-string) 选项（`--disable ListR`）禁用该功能来阻止 rclone 使用 `ListR`，或者可以通过使用 `--fast-list` 选项允许 rclone 在通常由于内存使用较高而不会使用 `ListR` 的情况下使用它。Rclone 无论哪种方式都应始终产生相同的结果。在不支持 `ListR` 的远端上使用 `--disable ListR` 或 `--fast-list` 不起任何作用，rclone 将仅忽略它。

经验法则是，如果你为事务付费并且能够将整个同步列表放入内存，则建议使用 `--fast-list`。如果你有一个非常大的同步要执行，则不要使用 `--fast-list`，否则你将耗尽内存。运行一些测试并比较之后再决定，如有疑问，请保持默认，让 rclone 决定，即不使用 `--fast-list`。

### --timeout Duration

这设置 IO 空闲超时。如果传输已开始但随后空闲了这么长时间，则认为它已损坏并已断开连接。

默认值为 `5m`。设置为 `0` 以禁用。

### --transfers int

并行运行的文件传输数。如果远端给出大量超时，可以将此值设置得稍小一些；如果你有大量带宽和快速的远端，可以设置得大一些。

默认并行运行 4 个文件传输。

如果你想控制单个文件传输，请查看 --multi-thread-streams。

### -u, --update

这会强制 rclone 跳过目标上存在且修改时间比源文件更新的所有文件。

当传输到不支持直接修改时间的远端时（或使用 `--use-server-modtime` 避免额外的 API 调用时），这对于避免不必要的传输非常有用，因为它比 `--size-only` 检查更准确，比 `--checksum` 更快。在此类远端上（或使用 `--use-server-modtime` 时），将检查上传时间。

如果现有的目标文件的修改时间比源文件旧，并且大小不同，则会更新该文件。如果大小相同，则在校验和不同或不可用时进行更新。

如果现有的目标文件的修改时间（在计算的修改窗口内）等于源文件的修改时间，则在大小不同时会更新该文件。除非提供了 `--checksum` 标志，否则在这种情况下不会检查校验和。

在所有其他情况下，文件将不会被更新。

考虑使用 `--modify-window` 标志来补偿源和后端之间的时间偏差，对于那些不支持修改时间并改用上传时间的后端。但是，如果后端不支持校验和，请注意在时间偏差窗口内同步或复制可能仍会导致出于安全考虑而进行额外的传输。

### --use-mmap

如果设置此标志，rclone 将使用由 mmap 在基于 Unix 的平台上分配的匿名内存以及 Windows 上的 VirtualAlloc 作为其传输缓冲区（大小由 `--buffer-size` 控制）。以这种方式分配的内存不会进入 Go 堆，并可以在使用完毕后立即返回给操作系统。

如果未设置此标志，rclone 将使用 Go 内存分配器分配和释放缓冲区，由于内存页返回给操作系统的积极性较低，可能会使用更多内存。

这可能在某些平台上不能很好地工作，因此默认情况下被禁用；将来可能默认启用。

### --use-server-modtime

某些对象存储后端（例如 Swift、S3）不保留文件修改时间（modtime）。在这些后端上，rclone 将原始 modtime 作为附加元数据存储在对象上。默认情况下，当某个操作需要 modtime 时，它会进行一次 API 调用来检索元数据。

使用此标志可禁用额外的 API 调用，而依赖于服务器的修改时间。在某些情况下（例如使用 `--update` 的本地到远端同步），知道本地文件比上次上传到远端的时间更新就足够了。在这些情况下，此标志可以加快处理速度并减少所需的 API 调用数。

此标志仅在某些后端上受支持，在不受支持的后端上将被静默忽略。支持的远端包括 `azureblob`、`oracleobjectstorage`、`s3`、`swift`。

在同步操作中使用此标志而不同时使用 `--update` 会导致除最后上传时间外其他时间修改过的所有文件被再次上传，这可能不是你所希望的。

### -v, -vv, --verbose

使用 `-v` 时，rclone 会告诉你传输的每个文件以及少量重要事件。

使用 `-vv` 时，rclone 会变得非常详细，告诉你它考虑和传输的每个文件。提交错误报告时请附上此设置的日志。

当将详细程度设置为环境变量时，使用 `RCLONE_VERBOSE=1` 或 `RCLONE_VERBOSE=2` 分别表示 `-v` 和 `-vv`。

### -V, --version

打印版本号

## SSL/TLS 选项

rclone 发出的 SSL/TLS 连接可以使用这些选项进行控制。例如，这在与 HTTP 或 WebDAV 后端一起使用时非常有用。Rclone HTTP 服务器拥有自己的一组 SSL/TLS 配置，你可以在其文档中找到。

### --ca-cert stringArray

这将加载 PEM 编码的证书颁发机构证书，并使用它来验证 rclone 要连接的服务器的证书。

如果你生成了由本地 CA 签名的证书，则需要此标志来连接使用这些证书的服务器。

### --client-cert string

这将加载 PEM 编码的客户端证书。

这用于[双向 TLS 身份验证](https://en.wikipedia.org/wiki/Mutual_authentication)。

使用此标志时也需要 `--client-key` 标志。

### --client-key string

这将加载用于双向 TLS 身份验证的 PEM 编码的客户端私钥。与 `--client-cert` 结合使用。

支持的类型包括：

- 未加密的 PKCS#1（"BEGIN RSA PRIVATE KEY"）
- 未加密的 PKCS#8（"BEGIN PRIVATE KEY"）
- 加密的 PKCS#8（"BEGIN ENCRYPTED PRIVATE KEY"）
- 旧式 PEM 加密（例如 DEK-Info 头），会自动检测。

### --client-pass string

这可用于提供一个可选的密码来解密客户端密钥文件。

**注意** 密码应进行混淆处理，因此应该是 `rclone obscure YOURPASSWORD` 的输出。

### --no-check-certificate

`--no-check-certificate` 控制客户端是否验证服务器的证书链和主机名。
如果 `--no-check-certificate` 为 true，则 TLS 接受服务器提供的任何证书以及该证书中的任何主机名。
在此模式下，TLS 容易受到中间人攻击。

此选项默认为 `false`。

**这应仅用于测试。**

## 配置加密

你的配置文件包含用于登录云服务的信息。这意味着你应该将 `rclone.conf` 文件保存在安全的位置。

如果你的环境无法做到这一点，你可以为配置添加密码。这意味着你每次启动 rclone 时都必须提供密码。

要为 rclone 配置添加密码，请执行 `rclone config`。

```console
$ rclone config
Current remotes:

e) Edit existing remote
n) New remote
d) Delete remote
s) Set configuration password
q) Quit config
e/n/d/s/q>
```

进入 `s`，设置配置密码：

```text
e/n/d/s/q> s
Your configuration is not encrypted.
If you add a password, you will protect your login information to cloud services.
a) Add Password
q) Quit to main menu
a/q> a
Enter NEW configuration password:
password:
Confirm NEW password:
password:
Password set
Your configuration is encrypted.
c) Change Password
u) Unencrypt configuration
q) Quit to main menu
c/u/q>
```

你的配置现已加密，每次启动 rclone 时都必须提供密码。有关详细信息，请参阅下文。在同一菜单中，你可以更改密码或完全删除配置的加密。

如果丢失密码，则无法恢复配置。

你也可以使用：

- [rclone config encryption set](/commands/rclone_config_encryption_set/)
  直接设置配置加密
- [rclone config encryption remove](/commands/rclone_config_encryption_remove/)
  移除它
- [rclone config encryption check](/commands/rclone_config_encryption_check/)
  检查它是否已正确加密。

rclone 使用 [nacl secretbox](https://godoc.org/golang.org/x/crypto/nacl/secretbox)，它又使用 XSalsa20 和 Poly1305 来使用密钥加密和验证你的配置。
密码经过 SHA-256 哈希，生成的密钥用于 secretbox。
哈希后的密码不会被存储。

虽然这提供了非常好的安全性，但如果加密的 rclone 配置包含敏感信息，我们不建议将其公开存储，除非你使用非常强的密码。

如果在你的环境中是安全的，你可以将环境变量 `RCLONE_CONFIG_PASS` 设置为包含你的密码，在这种情况下，它将用于解密配置。

你可以从脚本中为一个会话设置此变量。对于类 unix 系统，将以下内容保存到名为 `set-rclone-password` 的文件中：

```sh
#!/bin/echo Source this file don't run it

read -s RCLONE_CONFIG_PASS
export RCLONE_CONFIG_PASS
```

然后在要使用时加载该文件。在 shell 中你可以执行 `source set-rclone-password`。它将提示你输入密码并将其设置在环境变量中。

提供密码的另一种方法是提供一个脚本，该脚本将检索密码并打印到标准输出。该脚本应具有完全限定的路径名，并且不依赖于任何环境变量。该脚本可以通过 [`--password-command="..."`](#password-command) 命令行参数或通过 `RCLONE_PASSWORD_COMMAND` 环境变量提供。

这种用法的一个有用示例是使用 `passwordstore` 应用程序来检索密码：

```console
export RCLONE_PASSWORD_COMMAND="pass rclone/config"
```

如果 `passwordstore` 密码管理器保存了 rclone 配置的密码，则使用脚本方法意味着该密码主要受 `passwordstore` 系统保护，并且永远不会以明文形式嵌入到脚本中，也不会通过标准命令可用于检查。对于长时间运行的 rclone 会话，很可能会无意中将密码副本捕获到日志文件或终端滚动缓冲区中。使用脚本方法提供密码可以显著提高配置密码的安全性。

如果你在脚本中运行 rclone，除非使用 `--password-command` 方法，否则你可能希望禁用密码提示。为此，向 rclone 传递参数 `--ask-password=false`。这将使 rclone 在 `RCLONE_CONFIG_PASS` 不包含有效密码且未提供 `--password-command` 时失败而不是要求输入密码。

每当运行可能受配置文件中的选项影响的命令时，rclone 将根据[上文](#config-string)中描述的规则查找现有文件，并加载其找到的任何文件。如果找到加密文件，这包括解密它，可能会导致密码提示。当你执行一个你知道实际并未使用此类配置文件中的任何内容的命令行时，你可以通过覆盖位置来避免加载它，例如使用用于内存配置的一个已记录特殊值。由于配置文件中只能存储后端选项，因此对于不操作后端的命令（例如 `completion`），通常这是不必要的。但是，对于通常操作后端但使用时不引用存储的远端的命令（例如列出本地文件系统路径或[连接字符串](#connection-strings)），它将是相关的：`rclone --config="" ls .`

### 配置加密速查表

你可以快速应用配置加密，而无需在静止或传输时使用明文。流行操作系统的详细说明：

#### Mac

- 生成并存储密码

  ```console
  security add-generic-password -a rclone -s config -w $(openssl rand -base64 40)
  ```

- 将检索指令添加到你的 `.zprofile` / `.profile`

  ```console
  export RCLONE_PASSWORD_COMMAND="/usr/bin/security find-generic-password -a rclone -s config -w"
  ```

#### Linux

- 先决条件：Linux 没有默认的密码管理器。让我们使用包管理器安装 "pass" 实用程序，例如 `apt install pass`、`yum install pass`、[等等](https://www.passwordstore.org/#download)；然后初始化密码存储：`pass init rclone`。

- 生成并存储密码

  ```console
  echo $(openssl rand -base64 40) | pass insert -m rclone/config
  ```

- 添加检索指令

  ```console
  export RCLONE_PASSWORD_COMMAND="/usr/bin/pass rclone/config"
  ```

#### Windows

- 生成并存储密码

  ```powershell
  New-Object -TypeName PSCredential -ArgumentList "rclone", (ConvertTo-SecureString -String ([System.Web.Security.Membership]::GeneratePassword(40, 10)) -AsPlainText -Force) | Export-Clixml -Path "rclone-credential.xml"
  ```

- 添加密码检索指令

  ```powershell
  [Environment]::SetEnvironmentVariable("RCLONE_PASSWORD_COMMAND", "[System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR((Import-Clixml -Path "rclone-credential.xml").Password))")
  ```

#### 加密配置文件（所有系统）

- 执行 `rclone config`，然后选择选项 `s) Set configuration password`

- 从前面的步骤添加/更新密码

## 开发者选项

这些选项在开发或调试 rclone 时很有用。还有一些未在此处记录的特定于远端的选项，用于测试。这些选项以远端名称开头，例如 `--drive-test-option`——请参阅相关远端的文档。

### --cpuprofile string

将 CPU profile 写入文件。这可以使用 `go tool pprof` 进行分析。

### --memprofile string

将内存 profile 写入文件。这可以使用 `go tool pprof` 进行分析。

### --dump DumpFlags

`--dump` 标志接受一个逗号分隔的标志列表来转储信息。

注意，某些头（例如 `Accept-Encoding`）在请求中显示的可能不正确，并且如果 Go 标准库自动 gzip 编码生效，则响应可能不会显示 `Content-Encoding`。在这种情况下，将在显示之前对请求正文进行 gunzip 解压。

可用的标志包括：

- `headers` 转储 HTTP 头。任何 `Authorization:` 头都将被排除，但输出仍可能包含敏感信息。可能会非常冗长。仅用于调试。如果确实需要 `Authorization:` 头，请使用 `auth`。
- `auth` 像 `headers` 一样转储 HTTP 头，但也包括任何 `Authorization:` 头。这意味着输出可能包含敏感信息。使用 `headers` 转储时不包含 `Authorization:` 头。可能会非常冗长。仅用于调试。
- `bodies` 转储 HTTP 头和正文。可能包含敏感信息。可能会非常冗长。仅用于调试。注意，正文在内存中缓冲，因此不要对巨大的文件使用此选项。
- `requests` 类似于 `bodies`，但转储请求正文和响应头。可用于调试下载问题。
- `responses` 类似于 `bodies`，但转储响应正文和请求头。可用于调试上传问题。
- `filters` 转储过滤器。可用于准确查看 include 和 exclude 选项正在过滤什么。
- `goroutines` 在命令结束时转储正在运行的 go-routines 列表。
- `openfiles` 在命令结束时转储打开的文件列表。它使用 Unix 命令 `lsof` 来执行此操作，因此你需要安装它才能使用。
- `mapper` 转储发送到 `--metadata-mapper` 提供的程序以及从其接收的 JSON blob。它可用于调试元数据映射器接口。

## 过滤

有关过滤选项：

- `--delete-excluded`
- `--filter`
- `--filter-from`
- `--exclude`
- `--exclude-from`
- `--exclude-if-present`
- `--include`
- `--include-from`
- `--files-from`
- `--files-from-raw`
- `--min-size`
- `--max-size`
- `--min-age`
- `--max-age`
- `--hash-filter`
- `--dump filters`
- `--metadata-include`
- `--metadata-include-from`
- `--metadata-exclude`
- `--metadata-exclude-from`
- `--metadata-filter`
- `--metadata-filter-from`

请参阅[过滤部分](/filtering/)。

## 远程控制

有关远程控制选项以及如何远程控制 rclone 的说明：

- `--rc`
- 任何以 `--rc-` 开头的选项

请参阅[远程控制部分](/rc/)。

## 日志

rclone 有 4 个日志级别，`ERROR`、`NOTICE`、`INFO` 和 `DEBUG`。

默认情况下，rclone 记录到标准错误。这意味着你可以重定向标准错误，同时仍能看到 rclone 命令的正常输出（例如 `rclone ls`）。

默认情况下，rclone 将生成 `Error` 和 `Notice` 级别的消息。

如果使用 `-q` 标志，rclone 将只生成 `Error` 消息。

如果使用 `-v` 标志，rclone 将生成 `Error`、`Notice` 和 `Info` 消息。

如果使用 `-vv` 标志，rclone 将生成 `Error`、`Notice`、`Info` 和 `Debug` 消息。

你也可以使用 `--log-level` 标志来控制日志级别。

如果使用 `--log-file` 选项，rclone 会将 `Error`、`Info` 和 `Debug` 消息以及标准错误重定向到文件。

如果使用 `--syslog` 标志，那么 rclone 将记录到 syslog，`--syslog-facility` 控制其使用的工具。

Rclone 在所有日志消息前面加上大写的级别，例如 INFO，这使得在日志文件中搜索不同类型的信息变得容易。

## 指标

Rclone 可以以 OpenMetrics/Prometheus 格式发布指标。

要启用指标端点，请使用 `--metrics-addr` 标志。如果提供了 `--rc` 标志和 `--rc-enable-metrics` 标志，或者使用 rclone rcd `--rc-enable-metrics`，指标也可以发布在 `--rc-addr` 端口上。

Rclone 为指标 HTTP 端点提供了广泛的配置选项。这些设置在 Metrics 部分下分组，前缀为 `--metrics-*`。

当使用 `--rc-enable-metrics` 启用指标时，它们将发布在与 rc API 相同的端口上。在这种情况下，`--metrics-*` 标志将被忽略，HTTP 端点配置将由 `--rc-*` 参数管理。

## 退出码

如果在命令执行期间发生任何错误，rclone 将以非零退出码退出。这允许脚本检测 rclone 操作何时失败。

在启动阶段，如果检测到配置错误，rclone 将立即退出。退出之前总是会有一条日志消息。

当 rclone 正在运行时，它会在运行过程中累积错误，并且仅当（重试之后）仍然存在失败的传输时才以非零退出码退出。对于每个计数的错误，都会有一条高优先级日志消息（使用 `-q` 时可见），显示消息以及导致问题的文件。开始重试时也会显示一条高优先级消息，以便用户可以看到重试后任何先前的错误消息可能不再有效。如果 rclone 进行了重试，则会在重试成功时记录一条高优先级消息。

### 退出码列表

- `0` - 成功
- `1` - 未另行归类的错误
- `2` - 语法或使用错误
- `3` - 未找到目录
- `4` - 未找到文件
- `5` - 临时错误（更多重试可能会修复的错误）（重试错误）
- `6` - 不太严重的错误（例如来自 dropbox 的 461 错误）（不重试错误）
- `7` - 致命错误（更多重试也无法修复的错误，例如账户被暂停）
  （致命错误）
- `8` - 传输超出 - 已达到 --max-transfer 设置的限制
- `9` - 操作成功，但未传输文件（需要
  [`--error-on-no-transfer`](#error-on-no-transfer)）
- `10` - 时长超出 - 已达到 --max-duration 设置的限制

## 环境变量

Rclone 可以完全使用环境变量进行配置。这些可用于为选项或配置文件条目设置默认值。

### 选项

rclone 中的每个选项都可以通过环境变量设置其默认值。

要查找环境变量的名称，首先取长选项名称，去掉前导 `--`，将 `-` 更改为 `_`，将其大写并添加前缀 `RCLONE_`。

例如，要始终设置 `--stats 5s`，请设置环境变量 `RCLONE_STATS=5s`。如果你在命令行上设置了 stats，它将覆盖环境变量设置。

或者要始终在 drive 中使用回收站 `--drive-use-trash`，请设置 `RCLONE_DRIVE_USE_TRASH=true`。

详细程度略有不同，`--verbose` 或 `-v` 的等效环境变量是 `RCLONE_VERBOSE=1`，`-vv` 的等效环境变量是 `RCLONE_VERBOSE=2`。

选项和环境变量使用相同的解析器，因此它们的形式完全相同。

通过环境变量设置的选项可以使用 `-vv` 标志查看，例如 `rclone version -vv`。

可以多次出现的选项（类型 `stringArray`）作为环境变量时的处理方式略有不同，因为环境变量只能定义一次。为了允许添加一个或多个项的简单机制，输入被视为 [CSV 编码](https://godoc.org/encoding/csv)字符串。例如：

| 环境变量 | 等效选项 |
|----------------------|--------------------|
| `RCLONE_EXCLUDE="*.jpg"` | `--exclude "*.jpg"` |
| `RCLONE_EXCLUDE="*.jpg,*.png"` | `--exclude "*.jpg"` `--exclude "*.png"` |
| `RCLONE_EXCLUDE='"*.jpg","*.png"'` | `--exclude "*.jpg"` `--exclude "*.png"` |
| `RCLONE_EXCLUDE='"/directory with comma , in it /**"'` | `--exclude "/directory with comma , in it /**" |

如果 `stringArray` 选项**同时**定义为环境变量和命令行上的选项，则将使用所有值。

### 配置文件

你可以按远端基础为配置文件中的值设置默认值。配置项的名称记录在每个后端的页面中。

要查找你要设置的环境变量的名称，请使用 `RCLONE_CONFIG_` + 远端名称 + `_` + 配置文件选项的名称，并将其全部大写。
注意这里的一个含义是远端的名称必须可以转换为有效的环境变量名称，
因此它只能包含字母、数字或 `_`（下划线）字符。

例如，要在不使用配置文件的情况下配置名为 `mys3:` 的 S3 远端（使用 unix 方式设置环境变量）：

```console
$ export RCLONE_CONFIG_MYS3_TYPE=s3
$ export RCLONE_CONFIG_MYS3_ACCESS_KEY_ID=XXX
$ export RCLONE_CONFIG_MYS3_SECRET_ACCESS_KEY=XXX
$ rclone lsd mys3:
          -1 2016-09-21 12:54:21        -1 my-bucket
$ rclone listremotes | grep mys3
mys3:
```

注意，如果要使用环境变量创建远端，则必须如上创建 `..._TYPE` 变量。

注意，使用环境变量创建的远端的名称不区分大小写，与[上文](#valid-remote-names)中记录的存储在配置文件中的常规远端相反。
你必须在环境变量中以大写形式编写该名称，但如上面的示例所示，它将以小写形式列出并可以被访问，同时你也可以用大写形式引用同一远端：

```console
$ rclone lsd mys3:
          -1 2016-09-21 12:54:21        -1 my-bucket
$ rclone lsd MYS3:
          -1 2016-09-21 12:54:21        -1 my-bucket
```

注意，你只能设置直接后端的选项，因此如果 myS3Crypt 是基于 S3 远端的 crypt 远端，则 RCLONE_CONFIG_MYS3CRYPT_ACCESS_KEY_ID 不起作用。但是 RCLONE_S3_ACCESS_KEY_ID 将设置所有使用 S3 的远端的访问密钥，包括 myS3Crypt。

还要注意，现在 rclone 具有[连接字符串](#connection-strings)，可能更容易使用它们，这使得上面的示例变为：

```console
rclone lsd :s3,access_key_id=XXX,secret_access_key=XXX:
```

### 优先级

各种不同的后端配置方法按以下顺序读取，并使用第一个有值的项。

- 连接字符串中的参数，例如 `myRemote,skip_links:`
- 命令行上提供的标志值，例如 `--skip-links`
- 特定于远端的环境变量，例如 `RCLONE_CONFIG_MYREMOTE_SKIP_LINKS`
  （见上文）。
- 特定于后端的环境变量，例如 `RCLONE_LOCAL_SKIP_LINKS`。
- 后端通用环境变量，例如 `RCLONE_SKIP_LINKS`。
- 配置文件，例如 `skip_links = true`。
- 默认值，例如 `false`——这些无法更改。

因此，如果命令行上同时提供了 `--skip-links` 并设置了环境变量 `RCLONE_LOCAL_SKIP_LINKS`，命令行标志将优先。

通过环境变量设置的后端配置可以使用 `-vv` 标志查看，例如 `rclone about myRemote: -vv`。

对于非后端配置，顺序如下：

- 命令行上提供的标志值，例如 `--stats 5s`。
- 环境变量，例如 `RCLONE_STATS=5s`。
- 默认值，例如 `1m`——这些无法更改。

### 其他环境变量

- `RCLONE_CONFIG_PASS` 设置为包含你的配置文件密码（请参阅[配置加密](#configuration-encryption)部分）
- `HTTP_PROXY`、`HTTPS_PROXY` 和 `NO_PROXY`（或它们的小写版本）。
  - 对于 https 请求，`HTTPS_PROXY` 优先于 `HTTP_PROXY`。
  - 环境值可以是完整 URL 或 "host[:port]"，在后一种情况下假定使用 "http" 方案。
- `USER` 和 `LOGNAME` 值用作当前用户名的后备。查找用户名的主要方法是操作系统特定的：Windows 上是 Windows API，Unix 系统上是 /etc/passwd 中的真实用户 ID。在文档中，当前用户名简称为 `$USER`。
- `RCLONE_CONFIG_DIR` - rclone **设置** 此变量用于配置文件和子进程，指向保存配置文件的目录。

通过环境变量设置的选项可以使用 `-vv` 和 `--log-level=DEBUG` 标志查看，例如 `rclone version -vv`。
