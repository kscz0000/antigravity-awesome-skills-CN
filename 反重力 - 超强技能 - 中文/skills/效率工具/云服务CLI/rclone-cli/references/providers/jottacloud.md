---
title: "Jottacloud"
description: "Rclone Jottacloud 文档"
versionIntroduced: "v1.43"
---

> **官方文档：** [https://rclone.org/jottacloud/](https://rclone.org/jottacloud/)
# Jottacloud

Jottacloud 是一家挪威公司提供的云存储服务，使用其位于挪威的自有数据中心。

除了 [jottacloud.com](https://www.jottacloud.com/) 上的官方服务外，
它还向不同公司提供白标解决方案。本后端目前支持以下白标服务，
使用[下方](#traditional)所述的不同认证方式：

- Elkjøp（含子公司）：
  - Elkjøp Cloud (cloud.elkjop.no)
  - Elgiganten Cloud (cloud.elgiganten.dk)
  - Elgiganten Cloud (cloud.elgiganten.se)
  - ELKO Cloud (cloud.elko.is)
  - Gigantti Cloud (cloud.gigantti.fi)
- Telia
  - Telia Cloud (cloud.telia.se)
  - Telia Sky (sky.telia.no)
- Tele2
  - Tele2 Cloud (mittcloud.tele2.se)
- Onlime
  - Onlime (onlime.dk)
- MediaMarkt
  - MediaMarkt Cloud (mediamarkt.jottacloud.com)
  - Let's Go Cloud (letsgo.jotta.cloud)

路径指定为 `remote:path`

路径可以按需嵌套任意深度，例如 `remote:directory/subdirectory`。

## 认证

Jottacloud 的认证通常基于 OAuth 和 OpenID Connect (OIDC)。有不同变体可供选择，
具体取决于您使用的服务，例如白标服务可能只支持其中一种。请注意，没有官方文档可供参考，
因此此处提供的描述基于观察，可能不完全准确。

Jottacloud 使用两种可选的 OAuth 安全机制，分别称为"刷新令牌轮换"和"自动重用检测"，
这会产生一些影响。访问令牌通常有一小时的有效期，之后需要刷新（轮换），
此操作需要提供刷新令牌。Rclone 会自动执行此操作。这是标准 OAuth 行为。
但在 Jottacloud 中，此类刷新操作不仅会创建新的访问令牌，还会创建新的刷新令牌，
并使所提供的现有刷新令牌失效。它会跟踪刷新令牌的历史记录，
有时称为令牌族，从初始认证后颁发的原始刷新令牌向下延伸。
这用于检测任何重用旧刷新令牌的尝试，并触发立即使当前刷新令牌失效，
实际上也使整个刷新令牌族失效。

当当前刷新令牌被失效后，下次 rclone 尝试执行令牌刷新时，
将会失败并显示类似以下的错误消息：

```text
CRITICAL: Failed to create file system for "remote:": (...): couldn't fetch token: invalid_grant: maybe token expired? - try refreshing with "rclone config reconnect remote:"
```

如果您以详细级别 2 (`-vv`) 运行 rclone，将看到一条调试消息，
其中包含来自 OAuth 响应的附加错误描述：

```text
DEBUG : remote: got fatal oauth error: oauth2: "invalid_grant" "Session doesn't have required client"
```

（错误描述以前是"Stale token"而不是"Session doesn't have required client"，
因此您可能在较旧的描述中看到对该措辞的引用。）

当发生这种情况时，您需要重新认证才能继续使用您的远程连接，
例如使用错误消息中建议的 [config reconnect](/commands/rclone_config_reconnect/)
命令。这将创建一个全新的刷新令牌（族）。

导致此情况的典型场景是：您在一个位置使用 rclone 创建了 Jottacloud 远程连接，
然后将配置文件复制到第二个位置，在该位置使用 rclone 访问同一个远程连接。
最终会出现使用已失效令牌（即刷新令牌重用）的令牌刷新尝试，
导致两个实例都开始出现"invalid_grant"错误。复制远程配置是可行的，
但您必须随后使用 [config reconnect](https://rclone.org/commands/rclone_config_reconnect/)
命令替换其中一个的令牌。

您可以在服务的 Web 用户界面中查看活动令牌的概览，
导航到"Settings"然后"Security"（此时您将进入
<https://www.jottacloud.com/web/secure> 或类似页面）。
在该页面下方有一个"My logged in devices"部分。其中包含一个列表条目，
似乎代表当前有效的刷新令牌或刷新令牌族。从该列表的右侧，
您可以点击按钮（"X"）来撤销（使失效）它，这意味着您仍然可以使用现有访问令牌
访问直到其过期，但您将无法执行令牌刷新。请注意，整个"My logged in devices"
功能在不同认证变体和不同（白标）服务下的行为似乎略有不同。

### 标准

这是一种专为命令行应用程序设计的 OAuth 变体。主要由官方服务 (jottacloud.com) 支持，
但也可能被某些白标服务支持。执行认证所需的必要信息，
如域名和要连接的端点，会自动发现（编码在所提供的登录令牌中，下文将描述），
因此您无需指定要配置哪个服务。

配置远程连接时，系统会要求您输入一次性个人登录令牌，
您必须从服务 Web 界面中的账户安全设置手动生成。
您不需要在同一台机器上有 Web 浏览器（与传统 OAuth 不同），
但需要在某处使用 Web 浏览器，并能够将生成的字符串复制到您的 rclone 配置会话中。
登录到您服务的 Web 用户界面，导航到"Settings"然后"Security"，
或者，对于官方服务，使用 rclone 配置远程连接时呈现给您的直接链接：
<https://www.jottacloud.com/web/secure>。
向下滚动到"Personal login token"部分，点击"Generate"按钮。
复制显示的字符串并粘贴到 rclone 要求的位置。
Rclone 随后将使用此令牌执行初始令牌请求，并接收一个常规 OAuth 令牌，
存储在您的远程配置中。Web 界面中的"My logged in devices"列表中也会出现一个新条目，
设备名称和应用程序名称为"Jottacloud CLI"。

每次以这种方式创建新令牌时，即生成新的个人登录令牌并换取 OAuth 令牌，
您都会获得一个全新的刷新令牌族，并在"My logged in devices"中有新条目。
您可以创建任意数量的远程连接，并在相同或不同的机器上使用多个 rclone 实例，
只要您像这样分别配置它们，就不会遇到上述刷新令牌重用问题。

### 传统

Jottacloud 还支持一种更传统的 OAuth 变体。大多数白标服务支持此方式，
对于其中许多服务，这是唯一的选择，因为它们不支持个人登录令牌。
此方法依赖预定义的服务特定域名和端点，rclone 需要您指定要配置的服务。
这也意味着对现有白标服务的任何更改或新增白标服务，都需要更新 rclone 后端实现。

配置远程连接时，您必须交互式登录到 OAuth 授权网站，
一次性授权码会在后台发送回 rclone，rclone 用它来请求 OAuth 令牌。
这意味着您需要在具有联网 Web 浏览器的机器上操作。
如果您需要在没有此条件的机器上使用，则必须在另一台机器上创建配置并从那里复制。
Jottacloud 后端不支持 `rclone authorize` 命令。详情请参阅
[远程设置文档](/remote_setup)。

使用此方法认证时，Jottacloud 会施加某种严格的会话管理。
这会导致上述"invalid_grant"错误出现一些意外情况，
实际上限制了您在同一台机器上只能使用一个活动认证。
即您只能创建一个 rclone 远程连接，甚至在配置了 rclone 远程连接的情况下
无法同时使用服务的官方桌面客户端登录，否则最终所有会话都会被失效，
迫使您重新认证。

成功认证后，Web 界面中的"My logged in devices"列表中会出现一个代表您会话的条目。
通常会以应用程序名称"Jottacloud for Desktop"或类似名称列出
（取决于白标服务配置）。

### 遗留

最初 Jottacloud 使用一种需要指定账户用户名和密码的 OAuth 变体。
当 Jottacloud 迁移到较新方法时，一些白标版本（来自 Elkjøp 的那些）
在很长一段时间内仍使用此遗留方法。目前没有已知服务仍在使用此方法，
rclone 仍然支持它，但该支持将在未来版本中移除。

## 配置

以下是如何使用默认设置创建名为 `remote` 的远程连接的示例。
首先运行：

```console
rclone config
```

这将引导您完成交互式设置过程：

```text
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n

Enter name for new remote.
name> remote

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
[snip]
XX / Jottacloud
   \ (jottacloud)
[snip]
Storage> jottacloud

Option client_id.
OAuth Client Id.
Leave blank normally.
Enter a value. Press Enter to leave empty.
client_id>

Option client_secret.
OAuth Client Secret.
Leave blank normally.
Enter a value. Press Enter to leave empty.
client_secret>

Edit advanced config?
y) Yes
n) No (default)
y/n> n

Option config_type.
Type of authentication.
Choose a number from below, or type in an existing value of type string.
Press Enter for the default (standard).
   / Standard authentication.
   | This is primarily supported by the official service, but may also be
   | supported by some white-label services. It is designed for command-line
 1 | applications, and you will be asked to enter a single-use personal login
   | token which you must manually generate from the account security settings
   | in the web interface of your service.
   \ (standard)
   / Traditional authentication.
   | This is supported by the official service and all white-label services
   | that rclone knows about. You will be asked which service to connect to.
 2 | It has a limitation of only a single active authentication at a time. You
   | need to be on, or have access to, a machine with an internet-connected
   | web browser.
   \ (traditional)
   / Legacy authentication.
 3 | This is no longer supported by any known services and not recommended
   | used. You will be asked for your account's username and password.
   \ (legacy)
config_type> 1

Option config_login_token.
Personal login token.
Generate it from the account security settings in the web interface of your
service, for the official service on https://www.jottacloud.com/web/secure.
Enter a value.
config_login_token> <your token here>

Use a non-standard device/mountpoint?
Choosing no, the default, will let you access the storage used for the archive
section of the official Jottacloud client. If you instead want to access the
sync or the backup section, for example, you must choose yes.
y) Yes
n) No (default)
y/n> n

Configuration complete.
Options:
- type: jottacloud
- configVersion: 1
- client_id: jottacli
- client_secret:
- tokenURL: https://id.jottacloud.com/auth/realms/jottacloud/protocol/openid-connect/token
- token: {........}
- username: 2940e57271a93d987d6f8a21
- device: Jotta
- mountpoint: Archive
Keep this "remote" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

配置完成后，您可以像这样使用 `rclone`（将 `remote` 替换为您给远程连接命名的名称）：

列出 Jottacloud 顶层目录

```console
rclone lsd remote:
```

列出 Jottacloud 中的所有文件

```console
rclone ls remote:
```

将本地目录复制到 Jottacloud 中名为 backup 的目录

```console
rclone copy /home/source remote:backup
```

### 设备和挂载点

官方 Jottacloud 客户端会为每台安装它的计算机注册一个设备，
并在用户界面的备份部分显示它们。对于您选择备份的每个文件夹，
它将在该设备内创建一个挂载点。名为 Jotta 的内置设备是特殊的，
包含 Archive、Sync 等挂载点，用于官方客户端中的对应功能。

使用 rclone 时，大多数情况下您会希望使用标准的 Jotta/Archive 设备/挂载点。
但是，您可能希望访问官方客户端提供的同步或备份功能中的文件，
因此 rclone 提供了在配置期间选择其他设备和挂载点的选项。

您可以创建新的设备和挂载点。除内置 Jotta 设备外的所有设备
都被官方 Jottacloud 客户端视为备份设备，其上的挂载点是独立的备份集。

对于内置 Jotta 设备，只能选择现有的内置挂载点。
除了上述 Archive 和 Sync 之外，它还可能包含多个其他挂载点，
如：Latest、Links、Shared 和 Trash。所有这些都是特殊的挂载点，
其内部表示与"常规"挂载点不同。Rclone 只会在非常有限的程度上支持它们。
通常您应该避免使用这些，除非您清楚自己在做什么。

### --fast-list

此后端支持 `--fast-list`，允许您以更多内存为代价使用更少的事务。
详情请参阅 [rclone 文档](/docs/#fast-list)。

请注意，Jottacloud 中的实现始终仅使用单个 API 请求来获取整个列表，
因此对于大型文件夹，这可能导致在显示第一个结果之前等待较长时间。

另请注意，使用 rclone 1.58 及更高版本时，使用 `--fast-list` 时
[MIME 类型](/overview/#mime-type)和元数据项 [utime](#metadata) 的信息不可用。

### 修改时间和哈希

Jottacloud 允许在对象上设置修改时间，精度为 1 秒。这些将用于检测对象是否需要同步。

Jottacloud 支持 MD5 类型哈希，因此您可以使用 `--checksum` 标志。

请注意，Jottacloud 在上传前需要 MD5 哈希，因此如果源没有 MD5 校验和，
则文件将在上传前临时缓存在磁盘上（位于
[--temp-dir](/docs/#temp-dir-string) 指定的位置）。
小文件将缓存在内存中——请参阅
[--jottacloud-md5-memory-limit](#jottacloud-md5-memory-limit) 标志。
从本地磁盘上传时，源校验和始终可用，因此这不适用。
从 rclone 1.52 版本开始，加密远程连接也是如此
（在旧版本中，crypt 后端不会为从本地磁盘的上传计算哈希，
因此 Jottacloud 后端必须如上所述进行处理）。

### 受限文件名字符

除了[默认受限字符集](/overview/#restricted-characters)之外，
还会替换以下字符：

| 字符 | 值 | 替换为 |
|------|:---:|:------:|
| "         | 0x22  | ＂          |
| *         | 0x2A  | ＊          |
| :         | 0x3A  | ：          |
| <         | 0x3C  | ＜          |
| >         | 0x3E  | ＞          |
| ?         | 0x3F  | ？          |
| \|        | 0x7C  | ｜          |
| %         | 0x25  | ％          |

无效的 UTF-8 字节也将被[替换](/overview/#invalid-utf8)，
因为它们无法用于 XML 字符串中。

### 删除文件

默认情况下，rclone 在删除文件时会将所有文件发送到回收站。
它们将在 30 天后自动永久删除。您可以使用 [--jottacloud-hard-delete](#jottacloud-hard-delete)
标志或设置等效的环境变量来绕过回收站并立即永久删除文件。
支持通过 [cleanup](/commands/rclone_cleanup/) 命令清空回收站。

### 版本

Jottacloud 支持文件版本控制。当 rclone 上传文件的新版本时，
它会创建该文件的新版本。目前 rclone 仅支持检索当前版本，
但旧版本可以通过 Jottacloud 网站访问。

可以通过 `--jottacloud-no-versions` 选项禁用版本控制。
这是通过在上传新版本之前删除远程文件来实现的。
如果上传失败，远程上将不会有该文件的任何版本可用。

### 配额信息

要查看当前配额，您可以使用 `rclone about remote:` 命令，
它将显示您的使用限额（除非是无限的）和当前使用量。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/jottacloud/jottacloud.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 jottacloud (Jottacloud) 特定的标准选项。

#### --jottacloud-client-id

OAuth 客户端 ID。

通常留空。

属性：

- Config:      client_id
- Env Var:     RCLONE_JOTTACLOUD_CLIENT_ID
- Type:        string
- Required:    false

#### --jottacloud-client-secret

OAuth 客户端密钥。

通常留空。

属性：

- Config:      client_secret
- Env Var:     RCLONE_JOTTACLOUD_CLIENT_SECRET
- Type:        string
- Required:    false

### 高级选项

以下是 jottacloud (Jottacloud) 特定的高级选项。

#### --jottacloud-token

OAuth 访问令牌（JSON 格式）。

属性：

- Config:      token
- Env Var:     RCLONE_JOTTACLOUD_TOKEN
- Type:        string
- Required:    false

#### --jottacloud-auth-url

认证服务器 URL。

留空以使用提供者默认值。

属性：

- Config:      auth_url
- Env Var:     RCLONE_JOTTACLOUD_AUTH_URL
- Type:        string
- Required:    false

#### --jottacloud-token-url

令牌服务器 URL。

留空以使用提供者默认值。

属性：

- Config:      token_url
- Env Var:     RCLONE_JOTTACLOUD_TOKEN_URL
- Type:        string
- Required:    false

#### --jottacloud-client-credentials

使用客户端凭据 OAuth 流程。

这将使用 RFC 6749 中描述的 OAUTH2 客户端凭据流程。

请注意，并非所有后端都支持此选项。

属性：

- Config:      client_credentials
- Env Var:     RCLONE_JOTTACLOUD_CLIENT_CREDENTIALS
- Type:        bool
- Default:     false

#### --jottacloud-md5-memory-limit

超过此大小的文件将在磁盘上缓存以计算 MD5（如果需要）。

属性：

- Config:      md5_memory_limit
- Env Var:     RCLONE_JOTTACLOUD_MD5_MEMORY_LIMIT
- Type:        SizeSuffix
- Default:     10Mi

#### --jottacloud-trashed-only

仅显示回收站中的文件。

这将在原始目录结构中显示已删除的文件。

属性：

- Config:      trashed_only
- Env Var:     RCLONE_JOTTACLOUD_TRASHED_ONLY
- Type:        bool
- Default:     false

#### --jottacloud-hard-delete

永久删除文件而不是将其放入回收站。

属性：

- Config:      hard_delete
- Env Var:     RCLONE_JOTTACLOUD_HARD_DELETE
- Type:        bool
- Default:     false

#### --jottacloud-upload-resume-limit

超过此大小的文件可以在上传失败时恢复。

属性：

- Config:      upload_resume_limit
- Env Var:     RCLONE_JOTTACLOUD_UPLOAD_RESUME_LIMIT
- Type:        SizeSuffix
- Default:     10Mi

#### --jottacloud-no-versions

通过删除文件并重新创建而非覆盖来避免服务端版本控制。

属性：

- Config:      no_versions
- Env Var:     RCLONE_JOTTACLOUD_NO_VERSIONS
- Type:        bool
- Default:     false

#### --jottacloud-encoding

后端的编码方式。

详情请参阅[概览中的编码部分](/overview/#encoding)。

属性：

- Config:      encoding
- Env Var:     RCLONE_JOTTACLOUD_ENCODING
- Type:        Encoding
- Default:     Slash,LtGt,DoubleQuote,Colon,Question,Asterisk,Pipe,Del,Ctl,InvalidUtf8,Dot

#### --jottacloud-description

远程连接的描述。

属性：

- Config:      description
- Env Var:     RCLONE_JOTTACLOUD_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

Jottacloud 对元数据的支持有限，目前为扩展的时间戳集。

以下是 jottacloud 后端可能的系统元数据项。

| 名称 | 帮助 | 类型 | 示例 | 只读 |
|------|------|------|------|------|
| btime | 文件创建时间，从 rclone 元数据中读取 | RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 | N |
| content-type | MIME 类型，也称为媒体类型 | string | text/plain | **Y** |
| mtime | 最后修改时间，从 rclone 元数据中读取 | RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 | N |
| utime | 最后上传时间，当前修订版本创建时间，由后端生成 | RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 | **Y** |

详情请参阅[元数据](/docs/#metadata)文档。

<!-- autogenerated options stop -->

## 限制

请注意，Jottacloud 不区分大小写，因此您不能同时拥有名为
"Hello.doc"和"hello.doc"的文件。

Jottacloud 文件名中不能包含相当多的字符。
Rclone 会将这些名称映射为外观相同的 Unicode 等效字符。
例如，如果文件名中包含 ?，则会被映射为 ？。

Jottacloud 仅支持长度不超过 255 个字符的文件名。

## 故障排除

Jottacloud 在已删除文件和文件夹方面表现出一些不一致的行为，
这可能导致对先前已删除路径的复制、移动和目录移动操作失败。
在这种情况下，清空回收站应该能解决问题。
