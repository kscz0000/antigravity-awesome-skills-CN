---
title: "SFTP"
description: "SFTP（SSH 文件传输协议）后端配置"
versionIntroduced: "v1.36"
---

> **官方文档：** [https://rclone.org/sftp/](https://rclone.org/sftp/)
# SFTP

SFTP 是[安全（或 SSH）文件传输协议](https://en.wikipedia.org/wiki/SSH_File_Transfer_Protocol)。

SFTP 后端可与多种不同的提供商配合使用：

<!-- markdownlint-capture -->
<!-- markdownlint-disable line-length no-bare-urls -->

| 提供商 | 配置 |
|---|---|
| [Hetzner Storage Box](https://www.hetzner.com/storage/storage-box) | [rclone 配置](https://rclone.org/sftp/#hetzner-storage-box) |
| [rsync.net](https://rsync.net/products/rclone.html) | [rclone 配置](https://rclone.org/sftp/#rsync-net) |

<!-- markdownlint-restore -->

SFTP 运行在 SSH v2 之上，在大多数现代 SSH 安装中均为标配。

路径以 `remote:path` 的形式指定。如果路径不以 `/` 开头，则相对于用户的家目录。空路径 `remote:` 指代用户的家目录。例如，`rclone lsd remote:` 将列出 rclone 远端配置中所设用户的家目录（即 `/home/sftpuser`）。而 `rclone lsd remote:/` 将列出远端机器的根目录（即 `/`）。

注意，某些 SFTP 服务器需要前导 `/`——Synology 就是一个典型例子。另一方面，rsync.net 和 Hetzner 要求用户省略前导 `/`。

注意，默认情况下 rclone 会尝试在服务器上执行 shell 命令，参见 [shell 访问注意事项](#shell-access-considerations)。

## 配置

以下是创建 SFTP 配置的示例。首先运行

```console
rclone config
```

这将引导你完成交互式配置过程。

```text
No remotes found, make a new one\?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> remote
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / SSH/SFTP
   \ "sftp"
[snip]
Storage> sftp
SSH host to connect to
Choose a number from below, or type in your own value
 1 / Connect to example.com
   \ "example.com"
host> example.com
SSH username
Enter a string value. Press Enter for the default ("$USER").
user> sftpuser
SSH port number
Enter a signed integer. Press Enter for the default (22).
port>
SSH password, leave blank to use ssh-agent.
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank
y/g/n> n
Path to unencrypted PEM-encoded private key file, leave blank to use ssh-agent.
key_file>
Remote config
Configuration complete.
Options:
- type: sftp
- host: example.com
- user: sftpuser
- port:
- pass:
- key_file:
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

此远端名为 `remote`，现在可以这样使用：

查看家目录中的所有目录

```console
rclone lsd remote:
```

查看根目录中的所有目录

```console
rclone lsd remote:/
```

创建新目录

```console
rclone mkdir remote:path/to/directory
```

列出目录的内容

```console
rclone ls remote:path/to/directory
```

将 `/home/local/directory` 同步到远端目录，删除目录中多余文件。

```console
rclone sync --interactive /home/local/directory remote:directory
```

将远端路径 `/srv/www-data/` 挂载到本地路径 `/mnt/www-data`

```console
rclone mount remote:/srv/www-data/ /mnt/www-data
```

### SSH 认证

SFTP 远端支持三种认证方式：

- 密码
- 密钥文件，包括证书签名的密钥
- ssh-agent

密钥文件应为 PEM 编码的私钥文件。例如 `/home/$USER/.ssh/id_rsa`。
仅支持未加密的 OpenSSH 格式或 PEM 加密的文件。

密钥文件可以通过外部文件（key_file）指定，也可以包含在 rclone 配置文件中（key_pem）。如果在配置文件中使用 key_pem，该条目应在单行内，用换行符（'\n' 或 '\r\n'）分隔各行。即

```text
key_pem = -----BEGIN RSA PRIVATE KEY-----\nMaMbaIXtE\n0gAMbMbaSsd\nMbaass\n-----END RSA PRIVATE KEY-----
```

以下命令将为 key_pem 生成正确的单行格式：

```console
awk '{printf "%s\\n", $0}' < ~/.ssh/id_rsa
```

如果不指定 `pass`、`key_file`、`key_pem` 或 `ask_password`，rclone 将尝试连接 ssh-agent。你也可以指定 `key_use_agent` 来强制使用 ssh-agent。在这种情况下，还可以指定 `key_file` 或 `key_pem` 来强制使用 ssh-agent 中的特定密钥。

目前，使用 ssh-agent 是加载加密 OpenSSH 密钥的唯一方式。

如果设置了 `ask_password` 选项，rclone 将在需要密码且未配置密码时提示输入。

#### 证书签名密钥

使用传统的基于密钥的认证时，你只需配置私钥，认证过程中将使用内置于其中的公钥。

如果你有证书，可以用来签名你的公钥，创建一个单独的 SSH 用户证书，该证书应在认证时使用，而非从私钥中提取的普通公钥。然后你必须在 `pubkey_file` 中提供用户证书公钥文件的路径，或在 `pubkey` 中提供该文件的内容。

注意：这不是与你私钥配对的传统公钥（通常保存为 `/home/$USER/.ssh/id_rsa.pub`）。在 `pubkey_file` 中设置此路径将无法工作。

示例：

```ini
[remote]
type = sftp
host = example.com
user = sftpuser
key_file = ~/id_rsa
pubkey_file = ~/id_rsa-cert.pub
````

如果你将证书与私钥拼接，则可以在两处都指定合并后的文件。

注意：证书必须在文件中排在前面。例如

```console
cat id_rsa-cert.pub id_rsa > merged_key
```

### 主机密钥验证

默认情况下，rclone 不会验证服务器的主机密钥。这可能允许攻击者用自己的服务器替换原服务器，如果你使用密码认证，可能导致密码泄露。

使用标准 `known_hosts` 文件进行主机密钥匹配，可以通过启用 `known_hosts_file` 选项来开启。该选项可以指向由 `OpenSSH` 维护的文件，也可以指向独立文件。

例如，使用 OpenSSH 的 `known_hosts` 文件：

```ini
[remote]
type = sftp
host = example.com
user = sftpuser
pass =
known_hosts_file = ~/.ssh/known_hosts
````

或者你可以这样创建自己的 known hosts 文件：

```console
ssh-keyscan -t dsa,rsa,ecdsa,ed25519 example.com >> known_hosts
```

存在一些限制：

- `rclone` 不会为你*管理*此文件。如果密钥缺失或错误，连接将被拒绝。
- 如果服务器设置为证书主机密钥，则 `known_hosts` 文件中的条目*必须*是 CA 的 `@cert-authority` 条目。

如果服务器提供的主机密钥与文件中的不匹配（或缺失），连接将被中止并返回错误，例如

```text
NewFs: couldn't connect SSH: ssh: handshake failed: knownhosts: key mismatch
```

或

```text
NewFs: couldn't connect SSH: ssh: handshake failed: knownhosts: key is unknown
```

如果你看到类似以下错误

```text
NewFs: couldn't connect SSH: ssh: handshake failed: ssh: no authorities for hostname: example.com:22
```

则可能是服务器出示了 CA 签名的主机证书，你需要添加相应的 `@cert-authority` 条目。

`known_hosts_file` 设置可以在 `rclone config` 中作为高级选项设置。

### macOS 上的 ssh-agent

注意，由于操作系统最近的变更，在 macOS 上使用 ssh-agent 似乎存在各种问题。最有效的变通方法似乎是在每个会话中启动一个 ssh-agent，例如

```console
eval `ssh-agent -s` && ssh-add -A
```

然后在会话结束时

```console
eval `ssh-agent -k`
```

这些命令当然可以在脚本中使用。

### Shell 访问

SFTP 后端的某些功能依赖于远端 shell 访问以及执行命令的能力。这包括[校验和](#checksum)，在某些情况下也包括 [about](#about-command)。必须执行的 shell 命令可能因 shell 类型不同而异，包含特殊字符的文件路径参数的引号/转义方式也可能不同。因此，rclone 需要知道 shell 的类型，以及是否有 shell 访问权限。

大多数服务器运行某种版本的 Unix，此时可以假定基本的 Unix shell，无需进一步区分。Windows 10、Server 2019 及更高版本也可以运行 SSH 服务器，这是 OpenSSH 的移植版（参见官方[安装指南](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse)）。在 Windows 服务器上，shell 处理方式不同：虽然也可以设置为使用 Unix 类型 shell（如 Cygwin bash），但默认使用 Windows 命令提示符（cmd.exe），PowerShell 是推荐的替代方案。所有这些的行为都不同，rclone 必须加以处理。

rclone 会在首次访问 SFTP 远端时尝试自动检测服务器使用的 shell 类型。如果远端 shell 会话成功创建，它将查找 CMD 或 PowerShell 的迹象，如果未检测到其他类型则回退到 Unix。如果甚至无法创建远端 shell 会话，则 shell 命令执行将被完全禁用。结果存储在 SFTP 远端配置的 `shell_type` 选项中，因此自动检测只需执行一次。如果你在首次运行前手动设置了此选项的值，将跳过自动检测；如果之后设置了不同的值，这将覆盖已有的值。值 `none` 可设置以避免任何执行 shell 命令的尝试，例如如果不允许在服务器上执行命令。如果你在配置中设置了 `shell_type = none`，则不得设置 [ssh](#sftp-ssh)。

当服务器为 [rclone serve sftp](/commands/rclone_serve_sftp/) 时，rclone SFTP 远端会将其检测为 Unix 类型 shell——即使它在 Windows 上运行。此服务器实际上没有 shell，但它接受与 SFTP 后端在 Unix shell 上所依赖的特定命令匹配的输入命令，例如 `md5sum` 和 `df`。它还处理 Unix shell 使用的字符串转义规则。因此，从 SFTP 远端将其视为 Unix 类型 shell 将始终正确，并支持所有功能。

#### Shell 访问注意事项

上述 shell 类型自动检测逻辑意味着，默认情况下 rclone 会在首次访问新的 sftp 远端时尝试运行 shell 命令。如果你在没有配置文件的情况下配置 sftp 远端，例如[即时](/docs/#backend-path-to-dir])远端，rclone 将无处存储结果，每次访问都会重新运行该命令。为避免此情况，你应将 `shell_type` 选项显式设置为正确值，或者如果你希望阻止 rclone 执行任何远端 shell 命令，则设置为 `none`。

同样需要注意的是，由于 shell 类型决定了用作命令行参数的文件路径的引号和转义方式，配置错误的 shell 类型可能使你暴露于命令注入攻击。请务必确认自动检测的 shell 类型，或显式设置你知道正确的 shell 类型，或在确认之前禁用 shell 访问。

### 校验和

SFTP 本身不支持校验和（文件哈希），但如果同一登录具有 shell 访问权限且能执行远端命令，rclone 就能使用校验和功能。如果在远端系统上有能计算兼容校验和的命令，rclone 可以配置为在需要校验和时执行该命令并读取结果。默认考虑 MD5 和 SHA-1，但也支持 CRC32、SHA-256、BLAKE3、XXH3 和 XXH128，可通过设置 `hashes` 选项指定要考虑哪些。

通常这需要服务器上有可用的外部工具。例如对于 MD5 校验和，默认情况下 rclone 会尝试命令 `md5sum`、`md5` 和 `rclone md5sum`，找到第一个可用的即被选用。这些工具通常需要在远端的 PATH 中才能被发现。

在某些情况下，shell 本身就能计算校验和。PowerShell 就是这样一个例子。如果 rclone 检测到远端 shell 是 PowerShell（这意味着很可能是 Windows OpenSSH 服务器），rclone 将在未找到外部校验和命令时使用预定义脚本块来生成 MD5、SHA-1 和 SHA-256 校验和（参见 [shell 访问](#shell-access)）。这假定 PowerShell 版本为 4.0 或更高。

选项 `md5sum_command`、`sha1_command` 等可用于自定义计算校验和所执行的命令。例如，你可以设置 md5sum 可执行文件所在的具体路径，或指定其他以兼容格式输出校验和的工具。值可以包含命令行参数，甚至是 PowerShell 的 shell 脚本块。rclone 有子命令 [hashsum](/commands/rclone_hashsum/)、[md5sum](/commands/rclone_md5sum/) 和 [sha1sum](/commands/rclone_sha1sum/) 使用兼容格式，这意味着如果服务器上有 rclone 可执行文件就可以使用。如上所述，如果在 PATH 中找到它们将自动被选用，但如果未找到，你可以设置如 `/path/to/rclone md5sum` 作为 `md5sum_command` 选项的值，确保使用特定的可执行文件。

远端校验和功能推荐且默认启用。首次使用 SFTP 远端时，如果未设置 `md5sum_command` 或 `sha1_command` 选项，它将检查上述各自的默认命令是否有可用的。结果将保存在远端配置中，下次将使用相同命令。如果特定算法的默认命令均不可用，则将设置值 `none`，此算法将不被远端支持。

如果你连接的 SFTP 服务器不受你控制，且禁止执行远端 shell 命令，则可能需要完全禁用校验和功能。将配置选项 `disable_hashcheck` 设置为 `true` 可完全禁用校验和（将选项 `hashes` 设置为 `none` 或将选项 `md5sum_command`、`sha1_command` 等设置为 `none` 效果相同）。将选项 `shell_type` 设置为 `none` 不仅可以禁用校验和，还可以禁用所有其他基于远端 shell 命令执行的功能。

### 修改时间和哈希

修改时间在服务器上以 1 秒精度存储。

修改时间用于同步，且完全支持。

某些 SFTP 服务器在上传后禁用设置/修改文件修改时间（例如，ProFTPd 的某些 mod_sftp 配置）。如果你使用的是这类服务器，可以在 RClone 后端配置中设置选项 `set_modtime = false` 来禁用此行为。

### About 命令

`about` 命令返回远端上指定路径所在磁盘的总空间、可用空间和已用空间；如果未指定路径，则返回远端根磁盘的信息。

SFTP 通常支持 [about](/commands/rclone_about/) 命令，但这取决于服务器。如果服务器实现了厂商特定的 VFS 统计扩展（OpenSSH 实例通常是这种情况），将使用该扩展。如果没有，但同一登录可以访问 Unix shell（其中 `df` 命令可用，例如在远端的 PATH 中），则将使用此方式。如果服务器 shell 是 PowerShell（可能搭配 Windows OpenSSH 服务器），rclone 将使用内置 shell 命令（参见 [shell 访问](#shell-access)）。如果以上均不适用，`about` 将失败。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/sftp/sftp.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 sftp（SSH/SFTP）特有的标准选项。

#### --sftp-host

要连接的 SSH 主机。

例如 "example.com"。

Properties:

- Config:      host
- Env Var:     RCLONE_SFTP_HOST
- Type:        string
- Required:    true

#### --sftp-user

SSH 用户名。

Properties:

- Config:      user
- Env Var:     RCLONE_SFTP_USER
- Type:        string
- Default:     "$USER"

#### --sftp-port

SSH 端口号。

Properties:

- Config:      port
- Env Var:     RCLONE_SFTP_PORT
- Type:        int
- Default:     22

#### --sftp-pass

SSH 密码，留空以使用 ssh-agent。

**注意** 输入值必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

Properties:

- Config:      pass
- Env Var:     RCLONE_SFTP_PASS
- Type:        string
- Required:    false

#### --sftp-key-pem

原始 PEM 编码私钥。

注意，这应在单行内，行尾替换为 '\n'，例如

    key_pem = -----BEGIN RSA PRIVATE KEY-----\nMaMbaIXtE\n0gAMbMbaSsd\nMbaass\n-----END RSA PRIVATE KEY-----

以下命令将正确生成单行格式：

    awk '{printf "%s\\n", $0}' < ~/.ssh/id_rsa

如果指定此选项，将覆盖 key_file 参数。

Properties:

- Config:      key_pem
- Env Var:     RCLONE_SFTP_KEY_PEM
- Type:        string
- Required:    false

#### --sftp-key-file

PEM 编码私钥文件的路径。

留空或设置 key-use-agent 以使用 ssh-agent。

文件名中的前导 `~` 将被展开，`${RCLONE_CONFIG_DIR}` 等环境变量也会被展开。

Properties:

- Config:      key_file
- Env Var:     RCLONE_SFTP_KEY_FILE
- Type:        string
- Required:    false

#### --sftp-key-file-pass

用于解密 PEM 编码私钥文件的密码短语。

仅支持 PEM 加密的密钥文件（旧 OpenSSH 格式）。不支持新 OpenSSH 格式的加密密钥。

**注意** 输入值必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

Properties:

- Config:      key_file_pass
- Env Var:     RCLONE_SFTP_KEY_FILE_PASS
- Type:        string
- Required:    false

#### --sftp-pubkey

用于基于公证书认证的 SSH 公共证书。

如果你有用于认证的签名证书，请设置此项。如果指定，将覆盖 pubkey_file。

Properties:

- Config:      pubkey
- Env Var:     RCLONE_SFTP_PUBKEY
- Type:        string
- Required:    false

#### --sftp-pubkey-file

公钥文件的可选路径。

如果你有用于认证的签名证书，请设置此项。

文件名中的前导 `~` 将被展开，`${RCLONE_CONFIG_DIR}` 等环境变量也会被展开。

Properties:

- Config:      pubkey_file
- Env Var:     RCLONE_SFTP_PUBKEY_FILE
- Type:        string
- Required:    false

#### --sftp-key-use-agent

设置后强制使用 ssh-agent。

当同时设置了 key-file 时，将读取指定密钥文件的 ".pub" 文件，并仅从 ssh-agent 请求关联的密钥。这样可以避免当 ssh-agent 包含多个密钥时出现 `Too many authentication failures for *username*` 错误。

Properties:

- Config:      key_use_agent
- Env Var:     RCLONE_SFTP_KEY_USE_AGENT
- Type:        bool
- Default:     false

#### --sftp-use-insecure-cipher

启用不安全的加密算法和密钥交换方法。

这将启用以下不安全的加密算法和密钥交换方法：

- aes128-cbc
- aes192-cbc
- aes256-cbc
- 3des-cbc
- diffie-hellman-group-exchange-sha256
- diffie-hellman-group-exchange-sha1

这些算法不安全，可能允许攻击者恢复明文数据。

如果你使用了 ciphers 或 key_exchange 高级选项，则此选项必须为 false。


Properties:

- Config:      use_insecure_cipher
- Env Var:     RCLONE_SFTP_USE_INSECURE_CIPHER
- Type:        bool
- Default:     false
- Examples:
  - "false"
    - 使用默认加密算法列表。
  - "true"
    - 启用 aes128-cbc 加密算法以及 diffie-hellman-group-exchange-sha256、diffie-hellman-group-exchange-sha1 密钥交换方法。

#### --sftp-disable-hashcheck

禁用执行 SSH 命令来确定远端文件哈希是否可用。

留空或设为 false 以启用哈希（推荐），设为 true 以禁用哈希。

Properties:

- Config:      disable_hashcheck
- Env Var:     RCLONE_SFTP_DISABLE_HASHCHECK
- Type:        bool
- Default:     false

#### --sftp-ssh

外部 ssh 二进制文件的路径和参数。

通常 rclone 会使用内部 ssh 库连接到 SFTP 服务器。但内部库并未实现所有可能的 ssh 选项，因此可能需要使用外部 ssh 二进制文件。

如果使用此选项，rclone 将忽略所有内部配置，并期望你通过 ssh 二进制文件配置用户/主机/端口及其他所需选项。

**重要** ssh 命令必须能在不询问密码的情况下登录，因此需要配置密钥或证书。

rclone 将运行提供的命令，附加参数 "-s sftp" 以访问 SFTP 子系统，或附加如 "md5sum /path/to/file" 的命令来读取校验和。

包含空格的参数应用"双引号"括起来。

示例设置：

    ssh -o ServerAliveInterval=20 user@example.com

注意，使用外部 ssh 二进制文件时，rclone 会为每次哈希计算建立新的 ssh 连接。


Properties:

- Config:      ssh
- Env Var:     RCLONE_SFTP_SSH
- Type:        SpaceSepList
- Default:

### 高级选项

以下是 sftp（SSH/SFTP）特有的高级选项。

#### --sftp-known-hosts-file

known_hosts 文件的可选路径。

设置此值以启用服务器主机密钥验证。

文件名中的前导 `~` 将被展开，`${RCLONE_CONFIG_DIR}` 等环境变量也会被展开。

Properties:

- Config:      known_hosts_file
- Env Var:     RCLONE_SFTP_KNOWN_HOSTS_FILE
- Type:        string
- Required:    false
- Examples:
  - "~/.ssh/known_hosts"
    - 使用 OpenSSH 的 known_hosts 文件。

#### --sftp-ask-password

允许在需要时询问 SFTP 密码。

如果设置了此选项且未提供密码，rclone 将：
- 询问密码
- 不连接 ssh agent


Properties:

- Config:      ask_password
- Env Var:     RCLONE_SFTP_ASK_PASSWORD
- Type:        bool
- Default:     false

#### --sftp-path-override

覆盖 SSH shell 命令使用的路径。

这允许在 SFTP 和 SSH 路径不同时进行校验和计算。此问题影响 Synology NAS 等设备。

例如，如果共享文件夹可以在代表卷的目录中找到：

    rclone sync /home/local/directory remote:/directory --sftp-path-override /volume2/directory

例如，如果家目录可以在名为 "home" 的共享文件夹中找到：

    rclone sync /home/local/directory remote:/home/directory --sftp-path-override /volume1/homes/USER/directory

要仅指定 SFTP 远端根目录的路径，并让 rclone 自动添加任何相对子路径（包括按需解包/解密远端），请在路径开头添加 '@' 字符。

例如，上面第一个示例可以改写为：

	rclone sync /home/local/directory remote:/directory --sftp-path-override @/volume2

注意，将此方法用于 Synology "home" 文件夹时，应指定完整的 "/homes/USER" 路径而非 "/home"。

例如，上面第二个示例应改写为：

	rclone sync /home/local/directory remote:/homes/USER/directory --sftp-path-override @/volume1

Properties:

- Config:      path_override
- Env Var:     RCLONE_SFTP_PATH_OVERRIDE
- Type:        string
- Required:    false

#### --sftp-set-modtime

如果设置，则在远端设置修改时间。

Properties:

- Config:      set_modtime
- Env Var:     RCLONE_SFTP_SET_MODTIME
- Type:        bool
- Default:     true

#### --sftp-shell-type

远端服务器上 SSH shell 的类型（如果有）。

留空以自动检测。

Properties:

- Config:      shell_type
- Env Var:     RCLONE_SFTP_SHELL_TYPE
- Type:        string
- Required:    false
- Examples:
  - "none"
    - 无 shell 访问
  - "unix"
    - Unix shell
  - "powershell"
    - PowerShell
  - "cmd"
    - Windows 命令提示符

#### --sftp-hashes

以逗号分隔的支持校验和类型列表。

Properties:

- Config:      hashes
- Env Var:     RCLONE_SFTP_HASHES
- Type:        CommaSepList
- Default:

#### --sftp-md5sum-command

用于读取 MD5 哈希的命令。

留空以自动检测。

Properties:

- Config:      md5sum_command
- Env Var:     RCLONE_SFTP_MD5SUM_COMMAND
- Type:        string
- Required:    false

#### --sftp-sha1sum-command

用于读取 SHA-1 哈希的命令。

留空以自动检测。

Properties:

- Config:      sha1sum_command
- Env Var:     RCLONE_SFTP_SHA1SUM_COMMAND
- Type:        string
- Required:    false

#### --sftp-crc32sum-command

用于读取 CRC-32 哈希的命令。

留空以自动检测。

Properties:

- Config:      crc32sum_command
- Env Var:     RCLONE_SFTP_CRC32SUM_COMMAND
- Type:        string
- Required:    false

#### --sftp-sha256sum-command

用于读取 SHA-256 哈希的命令。

留空以自动检测。

Properties:

- Config:      sha256sum_command
- Env Var:     RCLONE_SFTP_SHA256SUM_COMMAND
- Type:        string
- Required:    false

#### --sftp-blake3sum-command

用于读取 BLAKE3 哈希的命令。

留空以自动检测。

Properties:

- Config:      blake3sum_command
- Env Var:     RCLONE_SFTP_BLAKE3SUM_COMMAND
- Type:        string
- Required:    false

#### --sftp-xxh3sum-command

用于读取 XXH3 哈希的命令。

留空以自动检测。

Properties:

- Config:      xxh3sum_command
- Env Var:     RCLONE_SFTP_XXH3SUM_COMMAND
- Type:        string
- Required:    false

#### --sftp-xxh128sum-command

用于读取 XXH128 哈希的命令。

留空以自动检测。

Properties:

- Config:      xxh128sum_command
- Env Var:     RCLONE_SFTP_XXH128SUM_COMMAND
- Type:        string
- Required:    false

#### --sftp-skip-links

设置以跳过任何符号链接及任何其他非常规文件。

Properties:

- Config:      skip_links
- Env Var:     RCLONE_SFTP_SKIP_LINKS
- Type:        bool
- Default:     false

#### --sftp-subsystem

指定远端主机上的 SSH2 子系统。

Properties:

- Config:      subsystem
- Env Var:     RCLONE_SFTP_SUBSYSTEM
- Type:        string
- Default:     "sftp"

#### --sftp-server-command

指定在远端主机上运行的 sftp 服务器路径或命令。

定义 server_command 时，subsystem 选项将被忽略。

如果在配置文件中添加 server_command，请注意不要用引号括起，否则会导致 rclone 失败。

可用示例：

    [remote_name]
    type = sftp
    server_command = sudo /usr/libexec/openssh/sftp-server

Properties:

- Config:      server_command
- Env Var:     RCLONE_SFTP_SERVER_COMMAND
- Type:        string
- Required:    false

#### --sftp-use-fstat

设置后使用 fstat 代替 stat。

某些服务器限制打开文件的数量，在打开文件后调用 Stat 会从服务器抛出错误。设置此标志将调用 Fstat 代替 Stat，Fstat 在已打开的文件句柄上调用。

已发现此选项对 IBM Sterling SFTP 服务器有帮助，此类服务器的"extractability"级别设为 1，意味着任意时刻只能打开 1 个文件。


Properties:

- Config:      use_fstat
- Env Var:     RCLONE_SFTP_USE_FSTAT
- Type:        bool
- Default:     false

#### --sftp-disable-concurrent-reads

设置后不使用并发读取。

通常并发读取是安全的，不使用并发读取会降低性能，因此此选项默认禁用。

某些服务器限制文件可被下载的次数。使用并发读取可能触发此限制，因此如果你的服务器返回

    Failed to copy: file does not exist

则可能需要启用此标志。

如果禁用了并发读取，use_fstat 选项将被忽略。


Properties:

- Config:      disable_concurrent_reads
- Env Var:     RCLONE_SFTP_DISABLE_CONCURRENT_READS
- Type:        bool
- Default:     false

#### --sftp-disable-concurrent-writes

设置后不使用并发写入。

通常 rclone 使用并发写入上传文件。这大大提高了性能，特别是对远端服务器。

此选项在必要时禁用并发写入。


Properties:

- Config:      disable_concurrent_writes
- Env Var:     RCLONE_SFTP_DISABLE_CONCURRENT_WRITES
- Type:        bool
- Default:     false

#### --sftp-idle-timeout

关闭空闲连接前的最长等待时间。

如果在给定时间内没有连接被归还到连接池，rclone 将清空连接池。

设为 0 以无限期保持连接。


Properties:

- Config:      idle_timeout
- Env Var:     RCLONE_SFTP_IDLE_TIMEOUT
- Type:        Duration
- Default:     1m0s

#### --sftp-chunk-size

上传和下载的块大小。

此选项控制 SFTP 协议包中载荷的最大大小。RFC 将此限制为 32768 字节（32k），这也是默认值。然而，许多服务器支持更大的大小，通常受限于最大总包大小 256k，将其设大可显著提高高延迟链路上的传输速度。这包括 OpenSSH，例如使用 255k 的值效果良好，为开销留有充足空间，同时仍在 256k 的总包大小内。

在使用高于 32k 的值之前，请务必充分测试，且仅在你始终连接同一服务器或经过充分广泛测试后才使用。如果在复制较大文件时遇到如 "failed to send packet payload: EOF"、大量 "connection lost" 或 "corrupted on transfer" 等错误，请尝试降低该值。由 [rclone serve sftp](/commands/rclone_serve_sftp/) 运行的服务器以标准 32k 最大载荷发送数据包，因此下载文件时不得设置不同的 chunk_size，但它接受最大 256k 总大小的数据包，因此上传时 chunk_size 可如上述 OpenSSH 示例设置。


Properties:

- Config:      chunk_size
- Env Var:     RCLONE_SFTP_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     32Ki

#### --sftp-concurrency

单个文件的最大未完成请求数

此选项控制单个文件的最大未完成请求数。增加此值将提高高延迟链路上的吞吐量，代价是使用更多内存。


Properties:

- Config:      concurrency
- Env Var:     RCLONE_SFTP_CONCURRENCY
- Type:        int
- Default:     64

#### --sftp-connections

SFTP 同时连接的最大数量，0 表示不限。

注意，设置此值很可能导致死锁，因此应谨慎使用。

如果你进行 sync 或 copy 操作，请确保 connections 比 `--transfers` 与 `--checkers` 之和多 1。

如果使用 `--check-first`，则只需比 `--checkers` 和 `--transfers` 中的较大值多 1。

因此对于 `connections 3`，你应使用 `--checkers 2 --transfers 2
--check-first` 或 `--checkers 1 --transfers 1`。



Properties:

- Config:      connections
- Env Var:     RCLONE_SFTP_CONNECTIONS
- Type:        int
- Default:     0

#### --sftp-set-env

传递给 sftp 和命令的环境变量

以以下格式设置环境变量：

    VAR=value

传递给 sftp 客户端和任何运行的命令（如 md5sum）。

传递多个变量时用空格分隔，例如

    VAR1=value VAR2=value

包含空格的变量用引号括起，例如

    "VAR3=value with space" "VAR4=value with space" VAR5=nospacehere



Properties:

- Config:      set_env
- Env Var:     RCLONE_SFTP_SET_ENV
- Type:        SpaceSepList
- Default:

#### --sftp-ciphers

以空格分隔的用于会话加密的加密算法列表，按偏好排序。

至少一个必须与服务器配置匹配。可以使用 ssh -Q cipher 检查。

如果 use_insecure_cipher 为 true，则不得设置此选项。

示例：

    aes128-ctr aes192-ctr aes256-ctr aes128-gcm@openssh.com aes256-gcm@openssh.com


Properties:

- Config:      ciphers
- Env Var:     RCLONE_SFTP_CIPHERS
- Type:        SpaceSepList
- Default:

#### --sftp-key-exchange

以空格分隔的密钥交换算法列表，按偏好排序。

至少一个必须与服务器配置匹配。可以使用 ssh -Q kex 检查。

如果 use_insecure_cipher 为 true，则不得设置此选项。

示例：

    sntrup761x25519-sha512@openssh.com curve25519-sha256 curve25519-sha256@libssh.org ecdh-sha2-nistp256


Properties:

- Config:      key_exchange
- Env Var:     RCLONE_SFTP_KEY_EXCHANGE
- Type:        SpaceSepList
- Default:

#### --sftp-macs

以空格分隔的 MAC（消息认证码）算法列表，按偏好排序。

至少一个必须与服务器配置匹配。可以使用 ssh -Q mac 检查。

示例：

    umac-64-etm@openssh.com umac-128-etm@openssh.com hmac-sha2-256-etm@openssh.com


Properties:

- Config:      macs
- Env Var:     RCLONE_SFTP_MACS
- Type:        SpaceSepList
- Default:

#### --sftp-host-key-algorithms

以空格分隔的主机密钥算法列表，按偏好排序。

至少一个必须与服务器配置匹配。可以使用 ssh -Q HostKeyAlgorithms 检查。

注意：即使未启用服务器主机密钥验证，这也可能影响与服务器密钥协商的结果。

示例：

    ssh-ed25519 ssh-rsa ssh-dss


Properties:

- Config:      host_key_algorithms
- Env Var:     RCLONE_SFTP_HOST_KEY_ALGORITHMS
- Type:        SpaceSepList
- Default:

#### --sftp-socks-proxy

Socks 5 代理主机。

支持格式 user:pass@host:port、user@host:port、host:port。

示例：

	myUser:myPass@localhost:9005


Properties:

- Config:      socks_proxy
- Env Var:     RCLONE_SFTP_SOCKS_PROXY
- Type:        string
- Required:    false

#### --sftp-http-proxy

HTTP CONNECT 代理的 URL

将其设置为支持 HTTP CONNECT 方法的 HTTP 代理的 URL。

支持格式 http://user:pass@host:port、http://host:port、http://host。

示例：

    http://myUser:myPass@proxyhostname.example.com:8000


Properties:

- Config:      http_proxy
- Env Var:     RCLONE_SFTP_HTTP_PROXY
- Type:        string
- Required:    false

#### --sftp-copy-is-hardlink

设置以启用使用硬链接的服务端复制。

SFTP 协议未定义复制命令，因此通常 sftp 后端不允许服务端复制。

然而 SFTP 协议确实支持硬链接，如果你启用此标志，sftp 后端将支持服务端复制。这些将通过从源到目标的硬链接来实现。

并非所有 sftp 服务器都支持此功能。

注意，硬链接两个文件不会使用额外空间，因为源和目标将是同一个文件。

此功能可能对使用 --copy-dest 进行的备份有用。

Properties:

- Config:      copy_is_hardlink
- Env Var:     RCLONE_SFTP_COPY_IS_HARDLINK
- Type:        bool
- Default:     false

#### --sftp-description

远端的描述。

Properties:

- Config:      description
- Env Var:     RCLONE_SFTP_DESCRIPTION
- Type:        string
- Required:    false

<!-- autogenerated options stop -->

## 限制

在某些 SFTP 服务器（如 Synology）上，SSH 和 SFTP 的路径不同，因此无法正确计算哈希。你可以使用 [`--sftp-path-override`](#--sftp-path-override) 或 [`disable_hashcheck`](#--sftp-disable-hashcheck)。

Windows 下唯一支持的 ssh agent 是 Putty 的 pageant。

Go SSH 库默认禁用 aes128-cbc 加密算法，出于安全考虑。可以在配置文件中将 `use_insecure_cipher` 设置为 `true` 来在逐连接基础上重新启用。有关此加密算法不安全性的更多细节，参见[此论文](http://www.isg.rhul.ac.uk/~kp/SandPfinal.pdf)。

SFTP 在 plan9 下不受支持，直到[此问题](https://github.com/pkg/sftp/issues/156)被修复。

注意，由于 SFTP 非基于 HTTP，以下标志对其无效：`--dump-headers`、`--dump-bodies`、`--dump-auth`。

注意，`--timeout` 和 `--contimeout` 均受支持。

## rsync.net {#rsync-net}

rsync.net 通过 SFTP 后端支持。

参见 [rsync.net 的 rclone 示例文档](https://www.rsync.net/products/rclone.html)。

## Hetzner Storage Box {#hetzner-storage-box}

Hetzner Storage Boxes 通过 SFTP 后端在端口 23 上支持。

参见 [Hetzner 文档了解详情](https://docs.hetzner.com/robot/storage-box/access/access-ssh-rsync-borg#rclone)