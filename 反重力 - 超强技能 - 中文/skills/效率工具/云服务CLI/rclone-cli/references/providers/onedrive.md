---
title: "Microsoft OneDrive"
description: "Rclone Microsoft OneDrive 提供商文档：身份验证、配置、Client ID 创建、OAuth 客户端凭据流、修改时间和哈希、受限字符、删除与版本、清理、故障排除。OneDrive、onedrive。"
versionIntroduced: "v1.24"
---

> **官方文档:** [https://rclone.org/onedrive/](https://rclone.org/onedrive/)
# Microsoft OneDrive

路径以 `remote:path` 形式指定

路径可以根据需要任意深，例如 `remote:directory/subdirectory`。

## 配置

OneDrive 的初始设置需要从 Microsoft 那里获取一个 token，这一步需要在浏览器中完成。`rclone config` 会一步步引导你完成。

下面是一个创建名为 `remote` 的远程存储的示例。首先运行：

```console
rclone config
```

这将引导你完成一个交互式设置流程：

```text
e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> n
name> remote
Type of storage to configure.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
[snip]
XX / Microsoft OneDrive
   \ "onedrive"
[snip]
Storage> onedrive
Microsoft App Client Id
Leave blank normally.
Enter a string value. Press Enter for the default ("").
client_id>
Microsoft App Client Secret
Leave blank normally.
Enter a string value. Press Enter for the default ("").
client_secret>
Edit advanced config? (y/n)
y) Yes
n) No
y/n> n
Remote config
Use web browser to automatically authenticate rclone with remote?
 * Say Y if the machine running rclone has a web browser you can use
 * Say N if running rclone on a (remote) machine without web browser access
If not sure try Y. If Y failed, try N.
y) Yes
n) No
y/n> y
If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth
Log in and authorize rclone for access
Waiting for code...
Got code
Choose a number from below, or type in an existing value
 1 / OneDrive Personal or Business
   \ "onedrive"
 2 / Sharepoint site
   \ "sharepoint"
 3 / Type in driveID
   \ "driveid"
 4 / Type in SiteID
   \ "siteid"
 5 / Search a Sharepoint site
   \ "search"
Your choice> 1
Found 1 drives, please select the one you want to use:
0: OneDrive (business) id=b!Eqwertyuiopasdfghjklzxcvbnm-7mnbvcxzlkjhgfdsapoiuytrewqk
Chose drive to use:> 0
Found drive 'root' of type 'business', URL: https://org-my.sharepoint.com/personal/you/Documents
Is that okay?
y) Yes
n) No
y/n> y
Configuration complete.
Options:
- type: onedrive
- token: {"access_token":"youraccesstoken","token_type":"Bearer","refresh_token":"yourrefreshtoken","expiry":"2018-08-26T22:39:52.486512262+08:00"}
- drive_id: b!Eqwertyuiopasdfghjklzxcvbnm-7mnbvcxzlkjhgfdsapoiuytrewqk
- drive_type: business
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

关于在没有可联网浏览器的情况下如何设置，请参阅 [remote setup docs](/remote_setup/)。

注意，rclone 会在你的本机启动一个 web 服务器，用于收集 Microsoft 返回的 token。该服务从打开浏览器的那一刻运行，直到你拿到验证码。它监听 `http://127.0.0.1:53682/`，如果你启用了主机防火墙，可能需要临时放行该端口。

配置完成后，你就可以这样使用 `rclone`（请将 `remote` 替换为你给远程存储取的名字）：

列出 OneDrive 顶层目录

```console
rclone lsd remote:
```

列出 OneDrive 中的所有文件

```console
rclone ls remote:
```

将本地目录复制到 OneDrive 中名为 backup 的目录

```console
rclone copy /home/source remote:backup
```

### 获取你自己的 Client ID 和 Key

与 OneDrive 通信时，rclone 默认使用一个内置的 Client ID，除非在配置中显式指定了自定义的 `client_id`。该默认的 Client ID 和 Key 被所有 rclone 用户在执行请求时共用。

如果默认 ID 表现不佳（例如遇到限流），你可以选择创建并使用自己的 Client ID。

#### 为 OneDrive Personal 创建 Client ID

要创建你自己的 Client ID，请按以下步骤操作：

1. 打开 <https://portal.azure.com/?quickstart=true#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview>
  然后在 `Add` 菜单下点击 `App registration`。
   - 如果你还没有创建 Azure 账户，系统会提示你创建。Azure 注册是免费的，但需要提供手机号、地址和信用卡用于身份验证。
2. 为你的应用输入一个名称，账户类型选择 `Accounts in any organizational
   directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts
   (e.g. Skype, Xbox)`，
  在 `Redirect URI` 中选择 `Web`，然后输入（请勿复制粘贴）
  `http://localhost:53682/` 并点击 Register。复制并妥善保存应用名下方显示的
  `Application (client) ID`，以备后用。
3. 在 `manage` 下选择 `Certificates & secrets`，点击 `New client secret`。
  输入一个描述（可任意），并将 `Expires` 设为 24 个月。
  复制并妥善保存该密钥的 *Value*（之后你将无法再次看到该值）。
4. 在 `manage` 下选择 `API permissions`，点击 `Add a permission`，选择
  `Microsoft Graph` 后再选择 `delegated permissions`。
5. 搜索并勾选以下权限：`Files.Read`、`Files.ReadWrite`、
  `Files.Read.All`、`Files.ReadWrite.All`、`offline_access`、`User.Read` 以及
  `Sites.Read.All`（如果配置了自定义访问范围，请相应选择权限）。选择完成后点击底部的 `Add permissions`。

至此应用创建完成。运行 `rclone config` 来创建或编辑一个 OneDrive 远程存储，
将前面保存的 App ID 和密码分别填入 Client ID 和 Secret，rclone 将引导你完成后续步骤。

`access_scopes` 选项允许你配置 rclone 请求的权限范围。更多关于不同范围的信息，
请参阅 [Microsoft Docs](https://docs.microsoft.com/en-us/graph/permissions-reference#files-permissions)。

如果需要在[配置远程存储时搜索 SharePoint 站点](https://github.com/rclone/rclone/pull/5883)，
则必须授予 `Sites.Read.All` 权限。但是，如果未分配该权限，你需要从访问范围中排除
`Sites.Read.All`，或在高级选项中将 `disable_site_permission` 选项设为 true。

#### 为 OneDrive Business 创建 Client ID

OneDrive Personal 的步骤对 OneDrive Business 不一定有效，
具体取决于所在组织的安全设置。
一个常见错误是应用的发布者未经验证。

你可以尝试[验证你的账户](https://docs.microsoft.com/en-us/azure/active-directory/develop/publisher-verification-overview)，
或者像下面这样把应用限制为仅你的组织使用。

1. 务必使用你的企业账户创建该 App。
2. 按上述步骤创建 App。但此处需要选择不同的账户类型：
   `Accounts in this organizational directory only (*** - Single tenant)`。
   注意，你也可以在创建 App 之后再更改账户类型。
3. 查询你所在组织的 [tenant ID](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-how-to-find-tenant)。
4. 在 rclone 配置中，将 `auth_url` 设为 `https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/authorize`。
5. 在 rclone 配置中，将 `token_url` 设为 `https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token`。

注意：如果你所在的是特殊区域，第 4 步和第 5 步可能需要使用不同的 host。
这里有[一些提示](https://github.com/rclone/rclone/blob/bc23bf11db1c78c6ebbf8ea538fbebf7058b4176/backend/onedrive/onedrive.go#L86)。

### 使用 OAuth 客户端凭据流

OAuth 客户端凭据流允许 rclone 直接使用与 Azure AD 企业应用相关联的权限，
而不是采用某个 Azure AD 用户账户的上下文。

可以通过以下步骤启用该流程：

1. 如上所述，在 Azure AD 门户中创建企业应用注册并获取 Client ID 和 Client Secret。
2. 确认应用已具备相应权限，并且这些权限被分配为 *Application Permissions*。
3. 配置远程存储，确保 *Client ID* 和 *Client Secret* 填写正确。
4. 在 *Advanced Config* 部分，为 `client_credentials` 输入 `true`，并在 `tenant` 部分输入 tenant ID。

在选择连接类型以配合客户端凭据流使用时，需要特别注意
"onedrive" 选项不可用。可以使用 "sharepoint" 选项；
如果该选项也无法找到正确的 drive ID，可使用 "driveid" 选项手动输入。

要使用此流程备份任意用户的数据，需要为你的 Azure AD 应用授予相应的
Microsoft Graph *Application permissions*（例如 `Files.Read.All`、`Sites.Read.All`
和/或 `Sites.Selected`）。拥有这些权限后，rclone 可以访问租户内的所有 drive，
但需要明确告知它要备份的是哪个用户或哪个 drive。提供与目标用户的 OneDrive
对应的 `drive_id`，或与 SharePoint 文档库对应的 SharePoint 站点 ID。
可以通过 Microsoft Graph 获取用户的 drive ID（例如 `/users/{userUPN}/drive`），
然后在 rclone 中进行配置。提供正确的 drive ID 后，rclone 即可使用仅限应用的 token
备份该用户的数据，而无需该用户本身的凭据。

**注意** 直接将权限分配给应用意味着任何拥有 *Client ID* 和 *Client Secret* 的人
都可以访问你的 OneDrive 文件。请务必妥善保管这些凭据。

### 修改时间和哈希

OneDrive 允许在对象上设置精确到 1 秒的修改时间，rclone 会用它来判断对象是否需要同步。

OneDrive Personal、OneDrive for Business 和 Sharepoint Server 都支持
[QuickXorHash](https://docs.microsoft.com/en-us/onedrive/developer/code-snippets/quickxorhash)。

在 rclone 1.62 之前，OneDrive Personal 的默认哈希是 `SHA1`。
自 rclone 1.62 起，所有 Onedrive 后端的默认哈希均为 `QuickXorHash`。

从 2023 年 7 月开始，`SHA1` 在 Onedrive Personal 中逐步被弃用，转而使用 `QuickXorHash`。
如有必要，可在过渡期使用 `--onedrive-hash-type` flag（或 `hash_type` 配置选项）
选择 `SHA1`，前提是这对你的工作流很重要。

对于所有 OneDrive 类型，你都可以使用 `--checksum` flag。

### --fast-list

该远程存储支持 `--fast-list`，可以通过消耗更多内存来减少事务次数。详情请参阅
[rclone docs](/docs/#fast-list)。

必须配合 `--onedrive-delta` flag（或配置文件中的 `delta = true`）一起启用，
因为它可能带来性能下降。

它通过使用 OneDrive 的 delta 列表功能来高效返回远程存储中的所有文件。
相比递归地列出目录，这种方式效率要高得多，也是 Microsoft 推荐的读取驱动器
全部文件信息的方法。

配合 `rclone mount` 和 [rclone rc vfs/refresh recursive=true](/rc/#vfs-refresh)）
使用时，可以非常快速地把挂载填充上所有文件信息。

用于递归列表的 API（`ListR`）仅支持从 drive 的根目录开始列出。
距离根目录越远，效率会越低，因为 rclone 必须丢弃不在你所用目录下的文件。

部分命令（例如 `rclone lsf -R`）默认会使用 `ListR` —— 如有需要，
可以用 `--disable ListR` 关闭。

### 受限文件名字符

除[默认的受限字符集](/overview/#restricted-characters)外，
以下字符也会被替换：

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| "         | 0x22  | ＂          |
| *         | 0x2A  | ＊          |
| :         | 0x3A  | ：          |
| <         | 0x3C  | ＜          |
| >         | 0x3E  | ＞          |
| ?         | 0x3F  | ？          |
| \         | 0x5C  | ＼          |
| \|        | 0x7C  | ｜          |

文件名的末尾不能是以下字符。只有当字符位于文件名末尾时才会被替换：

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| SP        | 0x20  | ␠           |
| .         | 0x2E  | ．          |

文件名的开头不能是以下字符。只有当字符位于文件名开头时才会被替换：

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| SP        | 0x20  | ␠           |
| ~         | 0x7E  | ～          |

无效的 UTF-8 字节也会被[替换](/overview/#invalid-utf8)，
因为它们无法在 JSON 字符串中使用。

### 删除文件

使用 rclone 删除的任何文件都会进入回收站。Microsoft 没有提供永久删除文件
或清空回收站的 API，因此你需要通过 Microsoft 任意一款应用或 OneDrive 网站
来完成这些操作。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/onedrive/onedrive.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下为 onedrive (Microsoft OneDrive) 特有的标准选项。

#### --onedrive-client-id

OAuth Client Id。

通常留空即可。

Properties:

- Config:      client_id
- Env Var:     RCLONE_ONEDRIVE_CLIENT_ID
- Type:        string
- Required:    false

#### --onedrive-client-secret

OAuth Client Secret。

通常留空即可。

Properties:

- Config:      client_secret
- Env Var:     RCLONE_ONEDRIVE_CLIENT_SECRET
- Type:        string
- Required:    false

#### --onedrive-region

选择 OneDrive 所属的国家云区域。

Properties:

- Config:      region
- Env Var:     RCLONE_ONEDRIVE_REGION
- Type:        string
- Default:     "global"
- Examples:
  - "global"
    - 微软云全球版
  - "us"
    - 微软云美国政府版
  - "de"
    - 微软云德国版（已弃用 —— 请优先尝试 global 区域）
  - "cn"
    - 由世纪互联在中国运营的 Azure 和 Office 365

#### --onedrive-tenant

服务主体的 tenant ID。也称为其 directory ID。

当使用
- Client Credential 流

时需要设置


Properties:

- Config:      tenant
- Env Var:     RCLONE_ONEDRIVE_TENANT
- Type:        string
- Required:    false

### 高级选项

以下为 onedrive (Microsoft OneDrive) 特有的高级选项。

#### --onedrive-token

以 JSON blob 形式表示的 OAuth 访问 token。

Properties:

- Config:      token
- Env Var:     RCLONE_ONEDRIVE_TOKEN
- Type:        string
- Required:    false

#### --onedrive-auth-url

授权服务器 URL。

留空则使用 provider 默认值。

Properties:

- Config:      auth_url
- Env Var:     RCLONE_ONEDRIVE_AUTH_URL
- Type:        string
- Required:    false

#### --onedrive-token-url

Token 服务器 URL。

留空则使用 provider 默认值。

Properties:

- Config:      token_url
- Env Var:     RCLONE_ONEDRIVE_TOKEN_URL
- Type:        string
- Required:    false

#### --onedrive-client-credentials

使用客户端凭据 OAuth 流。

将使用 RFC 6749 中描述的 OAUTH2 客户端凭据流。

注意并非所有后端都支持该选项。

Properties:

- Config:      client_credentials
- Env Var:     RCLONE_ONEDRIVE_CLIENT_CREDENTIALS
- Type:        bool
- Default:     false

#### --onedrive-upload-cutoff

切换到分块上传的阈值。

任何大于该值的文件都会以 chunk_size 为单位分块上传。

默认禁用此功能，因为使用单段上传时，Onedrive for Business 上的存储占用
会是 rclone 设置上传后修改时间时的两倍 —— Onedrive 会创建一个新版本。

参见: https://github.com/rclone/rclone/issues/1716


Properties:

- Config:      upload_cutoff
- Env Var:     RCLONE_ONEDRIVE_UPLOAD_CUTOFF
- Type:        SizeSuffix
- Default:     off

#### --onedrive-chunk-size

上传文件的分块大小 —— 必须是 320k (327,680 字节) 的整数倍。

超过该大小的文件将被分块 —— 必须是 320k (327,680 字节) 的整数倍，
且不得超过 250M (262,144,000 字节)，否则你可能会遇到 \"Microsoft.SharePoint.Client.InvalidClientQueryException: The request message is too big.\"
注意分块会被缓存在内存中。

Properties:

- Config:      chunk_size
- Env Var:     RCLONE_ONEDRIVE_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     10Mi

#### --onedrive-drive-id

要使用的 drive 的 ID。

Properties:

- Config:      drive_id
- Env Var:     RCLONE_ONEDRIVE_DRIVE_ID
- Type:        string
- Required:    false

#### --onedrive-drive-type

drive 的类型（personal | business | documentLibrary）。

Properties:

- Config:      drive_type
- Env Var:     RCLONE_ONEDRIVE_DRIVE_TYPE
- Type:        string
- Required:    false

#### --onedrive-root-folder-id

根文件夹的 ID。

通常不需要此项，但在某些特殊场景下，你可能知道要访问的文件夹 ID，
却无法通过路径遍历到达它。


Properties:

- Config:      root_folder_id
- Env Var:     RCLONE_ONEDRIVE_ROOT_FOLDER_ID
- Type:        string
- Required:    false

#### --onedrive-access-scopes

设置 rclone 请求的权限范围。

选择或手动输入一个空格分隔的自定义列表，列出 rclone 应请求的全部范围。


Properties:

- Config:      access_scopes
- Env Var:     RCLONE_ONEDRIVE_ACCESS_SCOPES
- Type:        SpaceSepList
- Default:     Files.Read Files.ReadWrite Files.Read.All Files.ReadWrite.All Sites.Read.All offline_access
- Examples:
  - "Files.Read Files.ReadWrite Files.Read.All Files.ReadWrite.All Sites.Read.All offline_access"
    - 对所有资源的读写权限
  - "Files.Read Files.Read.All Sites.Read.All offline_access"
    - 对所有资源的只读权限
  - "Files.Read Files.ReadWrite Files.Read.All Files.ReadWrite.All offline_access"
    - 对所有资源的读写权限，但不能浏览 SharePoint 站点。
    - 等同于将 disable_site_permission 设为 true

#### --onedrive-disable-site-permission

禁用对 Sites.Read.All 权限的请求。

如果设为 true，将无法在配置 drive ID 时搜索 SharePoint 站点，
因为 rclone 不会再请求 Sites.Read.All 权限。
如果你的组织没有为该应用分配 Sites.Read.All 权限，
且组织不允许用户自行同意应用权限请求，请将该项设为 true。

Properties:

- Config:      disable_site_permission
- Env Var:     RCLONE_ONEDRIVE_DISABLE_SITE_PERMISSION
- Type:        bool
- Default:     false

#### --onedrive-expose-onenote-files

设为该项后，OneNote 文件会出现在目录列表中。

默认情况下，rclone 会在目录列表中隐藏 OneNote 文件，
因为对它们执行 "Open" 和 "Update" 等操作会失败。
但这种行为也会导致你无法删除这些文件。
如果希望删除 OneNote 文件，或希望它们显示在目录列表中，请启用该选项。

Properties:

- Config:      expose_onenote_files
- Env Var:     RCLONE_ONEDRIVE_EXPOSE_ONENOTE_FILES
- Type:        bool
- Default:     false

#### --onedrive-server-side-across-configs

已弃用：请改用 --server-side-across-configs。

允许服务端操作（例如 copy）跨不同的 onedrive 配置生效。

如果你是在两个 OneDrive *Personal* drive 之间复制，且待复制的文件
已经在它们之间共享，则该选项可以工作。此外，对于在同一 *tenant* 下的
Onedrive for *business* 与 *SharePoint* 之间，以及同一 *tenant* 下的
*SharePoint* 与另一个 *SharePoint* 之间的复制，该选项也应该可以工作。
在其它情况下，rclone 会回退到普通 copy（速度会稍慢）。

Properties:

- Config:      server_side_across_configs
- Env Var:     RCLONE_ONEDRIVE_SERVER_SIDE_ACROSS_CONFIGS
- Type:        bool
- Default:     false

#### --onedrive-list-chunk

列表分块大小。

Properties:

- Config:      list_chunk
- Env Var:     RCLONE_ONEDRIVE_LIST_CHUNK
- Type:        int
- Default:     1000

#### --onedrive-no-versions

在修改类操作上移除所有版本。

Onedrive for business 会在 rclone 上传覆盖已有文件以及设置修改时间时
创建版本。

这些版本会占用配额空间。

该 flag 会在文件上传和设置修改时间之后检查版本，并删除除最新版本外的所有版本。

**注意** Onedrive personal 目前无法删除版本，请勿在那里使用该 flag。


Properties:

- Config:      no_versions
- Env Var:     RCLONE_ONEDRIVE_NO_VERSIONS
- Type:        bool
- Default:     false

#### --onedrive-hard-delete

删除时永久删除文件。

默认情况下，删除的文件会被送入回收站。设置该 flag 后，
文件将被永久删除，请谨慎使用。

OneDrive 个人账户不支持 permanentDelete API，
该选项仅适用于 OneDrive for Business 和 SharePoint 文档库。


Properties:

- Config:      hard_delete
- Env Var:     RCLONE_ONEDRIVE_HARD_DELETE
- Type:        bool
- Default:     false

#### --onedrive-link-scope

设置 link 命令创建的链接的作用域。

Properties:

- Config:      link_scope
- Env Var:     RCLONE_ONEDRIVE_LINK_SCOPE
- Type:        string
- Default:     "anonymous"
- Examples:
  - "anonymous"
    - 任何拿到链接的人都可以访问，无需登录。
    - 可能包括你组织外部的人员。
    - 匿名链接功能可能被管理员禁用。
  - "organization"
    - 任何登录到你的组织（tenant）的人都可以通过该链接获得访问权限。
    - 仅在 OneDrive for Business 和 SharePoint 中可用。

#### --onedrive-link-type

设置 link 命令创建的链接的类型。

Properties:

- Config:      link_type
- Env Var:     RCLONE_ONEDRIVE_LINK_TYPE
- Type:        string
- Default:     "view"
- Examples:
  - "view"
    - 创建一个只读链接。
  - "edit"
    - 创建一个读写链接。
  - "embed"
    - 创建一个可嵌入的链接。

#### --onedrive-link-password

为 link 命令创建的链接设置密码。

在撰写本文档时，该选项仅适用于 OneDrive personal 付费账户。


Properties:

- Config:      link_password
- Env Var:     RCLONE_ONEDRIVE_LINK_PASSWORD
- Type:        string
- Required:    false

#### --onedrive-hash-type

指定后端使用的哈希类型。

用于指定当前使用的哈希类型。如果设为 "auto"，则使用默认哈希
即 QuickXorHash。

在 rclone 1.62 之前，Onedrive Personal 默认使用 SHA1 哈希。
自 1.62 起，所有 onedrive 类型的默认值都改为 QuickXorHash。
如果需要使用 SHA1 哈希，请相应地设置该选项。

从 2023 年 7 月起，QuickXorHash 将成为 OneDrive for Business 和
OneDrive Personal 唯一可用的哈希。

也可以设为 "none" 表示不使用任何哈希。

如果对象上不存在所请求的哈希，将返回空字符串，rclone 会将其视为缺失哈希。


Properties:

- Config:      hash_type
- Env Var:     RCLONE_ONEDRIVE_HASH_TYPE
- Type:        string
- Default:     "auto"
- Examples:
  - "auto"
    - 由 rclone 选择最佳哈希
  - "quickxor"
    - QuickXor
  - "sha1"
    - SHA1
  - "sha256"
    - SHA256
  - "crc32"
    - CRC32
  - "none"
    - 无 —— 不使用任何哈希

#### --onedrive-av-override

允许下载服务器认为带有病毒的文件。

onedrive/sharepoint 服务器可能会使用杀毒软件检查上传的文件。
如果它检测到潜在的病毒或恶意软件，将阻止该文件的下载。

这种情况下你会看到类似下面的提示信息：

    server reports this file is infected with a virus - use --onedrive-av-override to download anyway: Infected (name of virus): 403 Forbidden:

如果你 100% 确定仍要下载该文件，请使用 --onedrive-av-override flag，
或在配置文件中设置 av_override = true。


Properties:

- Config:      av_override
- Env Var:     RCLONE_ONEDRIVE_AV_OVERRIDE
- Type:        bool
- Default:     false

#### --onedrive-delta

如果设置，rclone 将使用 delta 列表来实现递归列表。

如果设置了该 flag，onedrive 后端会声明支持 `ListR` 的递归列表。

启用该 flag 后会显著加速以下操作：

    rclone lsf -R onedrive:
    rclone size onedrive:
    rclone rc vfs/refresh recursive=true

**但是** delta 列表 API **仅** 在 drive 根目录下生效。如果你在非根目录下使用，
它会从根目录开始递归，并丢弃不在你请求目录下的所有数据。
结果会是正确的，但效率可能不高。

这也是为什么该 flag 没有作为默认值。

经验法则是：如果你的绝大部分数据都在 rclone 的根目录（即
`onedrive:root/directory` 中的 `root/directory`）下，
启用该 flag 将会带来很大的性能提升。如果数据大多不在根目录下，
启用该 flag 反而会造成很大的性能损失。

如果你将 onedrive 挂载在根目录（或者在使用 crypt 时接近根目录），
并使用 rclone `rc vfs/refresh`，推荐启用该 flag。


Properties:

- Config:      delta
- Env Var:     RCLONE_ONEDRIVE_DELTA
- Type:        bool
- Default:     false

#### --onedrive-metadata-permissions

控制在元数据中读取还是写入权限。

从文件读取权限元数据可以快速完成，但不一定总是希望从元数据中设置权限。


Properties:

- Config:      metadata_permissions
- Env Var:     RCLONE_ONEDRIVE_METADATA_PERMISSIONS
- Type:        Bits
- Default:     off
- Examples:
  - "off"
    - 既不读取也不写入该值
  - "read"
    - 仅读取该值
  - "write"
    - 仅写入该值
  - "read,write"
    - 读取和写入该值
  - "failok"
    - 如果写入失败仅记录错误，不中断传输

#### --onedrive-encoding

后端使用的编码。

更多信息请参阅 [overview 中的编码章节](/overview/#encoding)。

Properties:

- Config:      encoding
- Env Var:     RCLONE_ONEDRIVE_ENCODING
- Type:        Encoding
- Default:     Slash,LtGt,DoubleQuote,Colon,Question,Asterisk,Pipe,BackSlash,Del,Ctl,LeftSpace,LeftTilde,RightSpace,RightPeriod,InvalidUtf8,Dot

#### --onedrive-description

对远程存储的描述。

Properties:

- Config:      description
- Env Var:     RCLONE_ONEDRIVE_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

OneDrive 对文件和目录都支持系统元数据（撰写本文档时尚不支持用户元数据）。
绝大部分元数据是只读的，且 OneDrive Personal 和 Business 之间存在一些差异
（详见下表）。

如果设置了 `--onedrive-metadata-permissions`，也会支持权限。
`--onedrive-metadata-permissions` 接受的值有 "`read`"、"`write`"、
"`read,write`" 和 "`off`"（默认）。"`write`" 支持新增权限、
更新已有权限的 "role"，以及删除权限。更新和删除需要知道 Permission ID，
因此如果希望更新/删除权限，推荐使用 "`read,write`" 而非 "`write`"。

权限以 JSON 格式读写，使用的 schema 与
[OneDrive API](https://learn.microsoft.com/en-us/onedrive/developer/rest-api/resources/permission?view=odsp-graph-online)
相同，OneDrive Personal 和 Business 之间略有差异。

OneDrive Personal 示例：
```json
[
	{
		"id": "1234567890ABC!123",
		"grantedTo": {
			"user": {
				"id": "ryan@contoso.com"
			},
			"application": {},
			"device": {}
		},
		"invitation": {
			"email": "ryan@contoso.com"
		},
		"link": {
			"webUrl": "https://1drv.ms/t/s!1234567890ABC"
		},
		"roles": [
			"read"
		],
		"shareId": "s!1234567890ABC"
	}
]
```

OneDrive Business 示例：
```json
[
	{
		"id": "48d31887-5fad-4d73-a9f5-3c356e68a038",
		"grantedToIdentities": [
			{
				"user": {
					"displayName": "ryan@contoso.com"
				},
				"application": {},
				"device": {}
			}
		],
		"link": {
			"type": "view",
			"scope": "users",
			"webUrl": "https://contoso.sharepoint.com/:w:/t/design/a577ghg9hgh737613bmbjf839026561fmzhsr85ng9f3hjck2t5s"
		},
		"roles": [
			"read"
		],
		"shareId": "u!LKj1lkdlals90j1nlkascl"
	},
	{
		"id": "5D33DD65C6932946",
		"grantedTo": {
			"user": {
				"displayName": "John Doe",
				"id": "efee1b77-fb3b-4f65-99d6-274c11914d12"
			},
			"application": {},
			"device": {}
		},
		"roles": [
			"owner"
		],
		"shareId": "FWxc1lasfdbEAGM5fI7B67aB5ZMPDMmQ11U"
	}
]
```

要写入权限，请使用相同格式传入 "permissions" 元数据键。
[`--metadata-mapper`](https://rclone.org/docs/#metadata-mapper) 工具
对此非常有用。

添加权限时，可以在 `grantedTo` 或 `grantedToIdentities` 的 `User.ID` 或
`DisplayName` 属性中提供 email 地址。或者也可以在 `User.ID` 中提供
ObjectID。必须至少提供一个有效的接收者，才能为用户添加权限。
如果将 `Link.Scope` 设为 `"anonymous"`，也支持创建公开链接。

使用 `--metadata-mapper` 添加 "read" 权限的请求示例：

```json
{
    "Metadata": {
        "permissions": "[{\"grantedToIdentities\":[{\"user\":{\"id\":\"ryan@contoso.com\"}}],\"roles\":[\"read\"]}]"
    }
}
```

注意，如果文件/文件夹已经存在冲突的权限，添加权限的操作可能会失败。

要更新已有权限，需要同时提供 Permission ID 和要分配的新 `roles`。
`roles` 是唯一可被修改的属性。

要删除权限，请传入一个只包含你希望保留的权限的 blob（可以为空，表示删除全部）。
注意 `owner` 角色会被忽略，因为它不能被删除。

注意读取和写入权限都需要额外的 API 调用，所以如果你不需要读写权限，
建议省略 `--onedrive-metadata-permissions`。

文件夹（即目录）和文件都支持元数据和权限。
注意在 Folder 上设置 `mtime` 或 `btime` 在 OneDrive Business 上
需要多一次 API 调用。

OneDrive 目前不支持用户元数据。写入元数据时，只会写入可写的系统属性 —— 任何
只读或无法识别的键都会被忽略。

小贴士：要查看任意文件或文件夹的元数据和权限，请运行：

```
rclone lsjson remote:path --stat -M --onedrive-metadata-permissions read
```

下面是 onedrive 后端可能的系统元数据项。

| 名称 | 说明 | 类型 | 示例 | 只读 |
|------|------|------|---------|-----------|
| btime | 文件创建（出生）时间，秒级精度（OneDrive Personal 上为毫秒）。 | RFC 3339 | 2006-01-02T15:04:05Z | N |
| content-type | 文件的 MIME 类型。 | string | text/plain | **Y** |
| created-by-display-name | 创建该项目的用户的显示名。 | string | John Doe | **Y** |
| created-by-id | 创建该项目的用户的 ID。 | string | 48d31887-5fad-4d73-a9f5-3c356e68a038 | **Y** |
| description | 文件的简短描述。最多 1024 字符。Microsoft 已不再支持。 | string | Contract for signing | N |
| id | OneDrive 中该项目的唯一标识符。 | string | 01BYE5RZ6QN3ZWBTUFOFD3GSPGOHDJD36K | **Y** |
| last-modified-by-display-name | 最后修改该项目的用户的显示名。 | string | John Doe | **Y** |
| last-modified-by-id | 最后修改该项目的用户的 ID。 | string | 48d31887-5fad-4d73-a9f5-3c356e68a038 | **Y** |
| malware-detected | OneDrive 是否检测到该项目包含恶意软件。 | boolean | true | **Y** |
| mtime | 最后修改时间，秒级精度（OneDrive Personal 上为毫秒）。 | RFC 3339 | 2006-01-02T15:04:05Z | N |
| package-type | 如果存在，表明该项目是一个 package 而非文件夹或文件。Package 在某些场景下被视为文件，在另一些场景下被视为文件夹。 | string | oneNote | **Y** |
| permissions | 以 OneDrive 格式 JSON dump 形式表示的权限。需要使用 --onedrive-metadata-permissions 启用。属性：id, grantedTo, grantedToIdentities, invitation, inheritedFrom, link, roles, shareId | JSON | {} | N |
| shared-by-id | 分享该项目的用户的 ID（若已分享）。 | string | 48d31887-5fad-4d73-a9f5-3c356e68a038 | **Y** |
| shared-owner-id | 共享项目所有者的 ID（若已分享）。 | string | 48d31887-5fad-4d73-a9f5-3c356e68a038 | **Y** |
| shared-scope | 若已分享，表明该项目的分享范围：anonymous、organization 或 users。 | string | users | **Y** |
| shared-time | 项目被分享的时间，秒级精度（OneDrive Personal 上为毫秒）。 | RFC 3339 | 2006-01-02T15:04:05Z | **Y** |
| utime | 上传时间，秒级精度（OneDrive Personal 上为毫秒）。 | RFC 3339 | 2006-01-02T15:04:05Z | **Y** |

更多详情请参阅 [metadata](/docs/#metadata) 文档。

<!-- autogenerated options stop -->

### 以管理员身份模拟其他用户

与 Google Drive 以及通过服务账号模拟任意域用户不同，
OneDrive 要求你以管理员账户进行身份验证，并手动为每个要模拟的用户
单独设置一个远程存储。

1. 在 [Microsoft 365 管理中心](https://admin.microsoft.com) 中，依次打开你需要"模拟"的
   每个用户，进入 OneDrive 板块。那里有一个名为 "Get access to files" 的标题，
   你需要点击它来创建链接，该链接格式为
   `https://{tenant}-my.sharepoint.com/personal/{user_name_domain_tld}/`，
   同时会修改权限，使你的管理员用户获得访问权限。
2. 然后在 PowerShell 中运行以下命令：

   ```console
   Install-Module Microsoft.Graph -Scope CurrentUser -Repository PSGallery -Force
   Import-Module Microsoft.Graph.Files
   Connect-MgGraph -Scopes "Files.ReadWrite.All"
   # Follow the steps to allow access to your admin user
   # Then run this for each user you want to impersonate to get the Drive ID
   Get-MgUserDefaultDrive -UserId '{emailaddress}'
   # This will give you output of the format:
   # Name     Id                                                                 DriveType CreatedDateTime
   # ----     --                                                                 --------- ---------------
   # OneDrive b!XYZ123                                                           business  14/10/2023    1:00:58 pm
   ```

3. 接下来在 rclone 中添加一个 onedrive 远程存储类型，使用 `Type in driveID`，
   并填入上一步获得的 DriveID。每个用户对应一个远程存储。
   然后它会确认 drive ID，并希望你能看到类似
   `Found drive "root" of type "business"` 的消息，以及格式为
   `https://{tenant}-my.sharepoint.com/personal/{user_name_domain_tld}/Documents` 的 URL。

## 局限性

如果超过 90 天不使用 rclone，refresh token 将过期。这会导致授权问题。
修复方法很简单，只需运行 `rclone config reconnect remote:` 命令
来获取新的 access token 和 refresh token。

### 命名

注意 OneDrive 是大小写不敏感的，因此你不能同时拥有名为
"Hello.doc" 和 "hello.doc" 的两个文件。

OneDrive 文件名中有相当多的字符不能使用。这些字符在 Windows 平台上不会出现，
但在非 Windows 平台上却很常见。Rclone 会将这些字符映射到外观相同
但编码不同的 Unicode 等价字符。例如，如果文件名中包含 `?`，
它会被映射为 `？`。

### 文件大小

OneDrive Personal 和 OneDrive for Business 允许的最大单文件大小均为 250 GiB
[(更新于 2021 年 1 月 13 日)](https://support.microsoft.com/en-us/office/invalid-file-names-and-file-types-in-onedrive-and-sharepoint-64883a5d-228e-48f5-b3d2-eb39e07630fa?ui=en-us&rs=en-us&ad=us#individualfilesize)。

### 路径长度

包括文件名在内的完整路径，对于 OneDrive、OneDrive for Business 和 SharePoint Online
都必须少于 400 个字符。如果你使用 rclone 加密文件和文件夹名，
请注意这个限制，因为加密后的名称通常比原始名称更长。

### 文件数量

OneDrive 在单个文件夹中至少可以容纳 50,000 个文件，但当文件数达到 100,000 时，
rclone 在列出该目录时会遇到类似 `couldn't list files: UnknownError:` 的错误。
更多信息请参阅 [#2707](https://github.com/rclone/rclone/issues/2707)。

关于不同类型 OneDrive 限制的官方文档
可以[在此](https://support.office.com/en-us/article/invalid-file-names-and-file-types-in-onedrive-onedrive-for-business-and-sharepoint-64883a5d-228e-48f5-b3d2-eb39e07630fa)查阅。

## 版本

OneDrive 中文件的每次变动都会导致服务为该文件创建一个新版本。
这会占用用户配额。例如，修改文件的修改时间会产生第二个版本，
因此文件看起来占用了两倍的空间。

例如 `copy` 命令就会受到这个影响，因为 rclone 复制文件之后
还会将修改时间设置为与源文件一致，这又会使用一个版本。

你可以使用 `rclone cleanup` 命令（见下文）来移除所有旧版本。

或者将 `no_versions` 参数设为 `true`，rclone 就会在那些会创建新版本
的操作之后移除版本。这会消耗额外的事务次数，因此仅在确实需要时启用。

**注意** 在撰写本文档时，Onedrive Personal 会创建版本
（但不会为设置修改时间而创建），但用于删除这些版本的 API
返回 "API not found"，因此在 Onedrive Personal 上不应使用
cleanup 和 `no_versions`。

### 禁用版本控制

自 2018 年 10 月起，用户默认将无法再自行禁用版本控制。
这是因为 Microsoft 对该机制做了一次
[更新](https://techcommunity.microsoft.com/t5/Microsoft-OneDrive-Blog/New-Updates-to-OneDrive-and-SharePoint-Team-Site-Versioning/ba-p/204390)。
要更改这个新的默认设置，SharePoint 管理员需要运行 PowerShell 命令。
如果你是管理员，可以在 PowerShell 中运行以下命令来更改该设置：

1. `Install-Module -Name Microsoft.Online.SharePoint.PowerShell`（如果尚未安装）
2. `Import-Module Microsoft.Online.SharePoint.PowerShell -DisableNameChecking`
3. `Connect-SPOService -Url https://YOURSITE-admin.sharepoint.com -Credential YOU@YOURSITE.COM`
   （将 `YOURSITE`、`YOU`、`YOURSITE.COM` 替换为实际值；系统会提示你输入凭据）
4. `Set-SPOTenant -EnableMinimumVersionRequirement $False`
5. `Disconnect-SPOService`（断开与服务端的连接）

*以下是普通用户禁用版本控制的步骤。如果你看不到 "No Versioning" 选项，
请确认满足上述前置条件。*

用户 [Weropol](https://github.com/Weropol) 提供了一种在 OneDrive
上禁用版本控制的方法：

1. 通过点击 OneDrive Business 页面顶部的齿轮图标打开设置菜单。
2. 点击 Site settings。
3. 进入 Site settings 页面后，导航到 Site Administration > Site libraries
   and lists。
4. 点击 Customize "Documents"。
5. 点击 General Settings > Versioning Settings。
6. 在 Document Version History 下选择 No versioning 选项。
   注意：这将禁用新文件版本的创建，但不会删除任何已有版本。你的文档是安全的。
7. 点击 OK 应用更改。
8. 使用 rclone 上传或修改文件。（我也会使用 --no-update-modtime flag）
9. 在使用 rclone 之后恢复版本控制设置。（可选）

## 清理

OneDrive 支持 `rclone cleanup`，该命令会扫描所提供路径下的每个文件，
并删除除当前版本外的所有版本。因为这需要遍历所有文件，然后逐一查询每个文件的版本，
所以可能相当慢。Rclone 会以 `--checkers` 指定的并发数并行执行检查。
该命令还支持 `--interactive`/`i` 或 `--dry-run`，非常适合用来预览将执行的操作。

```text
rclone cleanup --interactive remote:path/subdir # interactively remove all old version for path/subdir
rclone cleanup remote:path/subdir               # unconditionally remove all old version for path/subdir
```

**注意** Onedrive personal 目前无法删除版本

## 故障排除

### SharePoint 上出现过度限流或被封禁

如果你在 SharePoint 上遇到过度限流或被封禁的情况，
可以尝试使用类似下面的 flag 显式设置 user agent：
`--user-agent "ISV|rclone.org|rclone/v1.55.1"`

具体细节可以参阅 Microsoft 文档：
[Avoid getting throttled or blocked in SharePoint Online](https://docs.microsoft.com/en-us/sharepoint/dev/general-development/how-to-avoid-getting-throttled-or-blocked-in-sharepoint-online#how-to-decorate-your-http-traffic-to-avoid-throttling)

### Sharepoint 上文件大小/哈希出现意外差异

Sharepoint（不是 OneDrive 或 OneDrive for Business）会
[静默](https://github.com/OneDrive/onedrive-api-docs/issues/935#issuecomment-441741631)
修改已上传的文件（主要是 Office 文件，如 .docx、.xlsx 等），
从而导致文件大小和哈希校验失败，这是一个
[已知](https://github.com/OneDrive/onedrive-api-docs/issues/935#issuecomment-441741631)
问题。还有其它一些情况也会导致 OneDrive 报告不一致的文件大小。
如果要在 Sharepoint 上用 rclone 处理这些受影响文件，
你可以通过以下命令行参数禁用相关检查：

```text
--ignore-checksum --ignore-size
```

另外，如果你对 OneDrive 文件拥有写权限，也可以尝试以下步骤，
或许能修复某些文件的该问题。
打开 [OneDrive](https://onedrive.live.com) 的 Web 界面，
找到受影响的文件（这些文件会出现在 rclone 的错误消息/日志中）。
只需依次点击这些文件，让 OneDrive 在 Web 端打开它们。
这会让每个文件就地转换为功能等价但不会再触发大小差异的格式。
所有有问题的文件都转换完成后，你就不再需要上面的 ignore 选项。

### 在 Sharepoint 上替换/删除已有文件时出现 "item not found"

Sharepoint（不是 OneDrive 或 OneDrive for Business）在用户尝试替换或删除
已上传文件时可能会返回 "item not found" 错误，这是一个
[已知](https://github.com/OneDrive/onedrive-api-docs/issues/1068) 问题；
看起来主要影响 Office 文件（.docx、.xlsx 等）和 Web 文件（.html、.aspx 等）。
作为变通方案，你可以使用 `--backup-dir <BACKUP_DIR>` 命令行参数，
让 rclone 把要替换/删除的文件移动到指定的备份目录中（而不是直接替换/删除）。
例如，要让 rclone 把这些文件移动到后端 `mysharepoint` 上的
`rclone-backup-dir` 目录中，你可以使用：

```text
--backup-dir mysharepoint:rclone-backup-dir
```

### access\_denied (AADSTS65005)

```text
Error: access_denied
Code: AADSTS65005
Description: Using application 'rclone' is currently not supported for your organization [YOUR_ORGANIZATION] because it is in an unmanaged state. An administrator needs to claim ownership of the company by DNS validation of [YOUR_ORGANIZATION] before the application rclone can be provisioned.
```

这表示 rclone 无法使用 OneDrive for Business API 连接你的账户。
你做不了太多，可以考虑给管理员写一封邮件。

不过，你也可以通过其它方式与 OneDrive 账户交互。请参阅 WebDAV 后端：
<https://rclone.org/webdav/#sharepoint>

### invalid\_grant (AADSTS50076)

```text
Error: invalid_grant
Code: AADSTS50076
Description: Due to a configuration change made by your administrator, or because you moved to a new location, you must use multi-factor authentication to access '...'.
```

如果你在为账户启用多因素认证后遇到上述错误，
可以通过刷新 OAuth refresh token 来解决。运行 `rclone config`，
选择编辑你的 OneDrive 后端。然后在到达这个问题之前
你不需要做任何实际修改：
`Already have a token - refresh?`。对该问题回答 `y`，并像首次配置后端时
一样走一遍刷新 token 的流程。完成后，rclone 应该就能再次正常使用该后端。

### 创建公开链接时出现 Invalid request

在 Sharepoint 和 OneDrive for Business 上，`rclone link` 可能会返回
"Invalid request" 错误。一个可能的原因是组织管理员不允许为该组织/Sharepoint
文档库创建公开链接。若要以管理员身份修复该权限，请参考文档：
[1](https://docs.microsoft.com/en-us/sharepoint/turn-external-sharing-on-or-off)，
[2](https://support.microsoft.com/en-us/office/set-up-and-manage-access-requests-94b26e0b-2822-49d4-929a-8455698654b3)。

### 无法访问 "Shared" with me 中的文件

rclone [目前](https://github.com/rclone/rclone/issues/4062) 不支持
"Shared with me" 中的文件，但有一个变通方案：

1. 访问 [https://onedrive.live.com](https://onedrive.live.com/)
2. 右键点击 `Shared` 中的某个项，在右键菜单中点击 `Add shortcut to My files`
    ![make_shortcut](https://user-images.githubusercontent.com/60313789/206118040-7e762b3b-aa61-41a1-8649-cc18889f3572.png "Screenshot (Shared with me)")
3. 快捷方式会出现在 `My files` 中，你可以通过 rclone 访问它，
   它的行为和普通文件夹/文件一样。
    ![in_my_files](https://i.imgur.com/0S8H3li.png "Screenshot (My Files)")
    ![rclone_mount](https://i.imgur.com/2Iq66sW.png "Screenshot (rclone mount)")

### 从 iOS 上传的 Live Photos（.heic 文件中的短视频片段）

iOS 版 OneDrive 应用在 2020 年引入了对 [Live Photos](https://support.apple.com/en-gb/HT207310)
的[上传与存储](https://techcommunity.microsoft.com/t5/microsoft-onedrive-blog/live-photos-come-to-onedrive/ba-p/1953452)。
遗憾的是，这些上传的 Live Photos 的使用和下载功能仍在开发中，
这在 rclone 和 Windows 原生 OneDrive 客户端中都会带来复制、同步和挂载方面的多个问题。

你可以在 OneDrive Web 界面中找到一张 Live Photo，然后通过 Web 界面下载它，
即可轻松看出根本原因。下载后你会发现 .heic 文件的大小比 Web 界面上显示的要小。
下载的文件较小，是因为它只包含从 OneDrive 中存储的 Live Photo（影片）中
抽取的单一帧（静态照片）。

大小不同会导致 `rclone copy/sync` 反复重新复制未修改的照片，输出类似下面这样：

```text
DEBUG : 20230203_123826234_iOS.heic: Sizes differ (src 4470314 vs dst 1298667)
DEBUG : 20230203_123826234_iOS.heic: sha1 = fc2edde7863b7a7c93ca6771498ac797f8460750 OK
INFO  : 20230203_123826234_iOS.heic: Copied (replaced existing)
```

可以通过添加 `--ignore-size` 来规避这些重复复制。
请注意该变通方案只会同步静态图片而不会同步短视频片段，
并且依赖于在所有情况下所有文件的修改日期都能被正确更新。

大小不同还会导致 `rclone check` 报告类似下面这样的错误：

```text
ERROR : 20230203_123826234_iOS.heic: sizes differ
```

这些检查错误可以通过添加 `--ignore-size` 来抑制。

大小不同也会导致 `rclone mount` 在下载时失败，报类似下面的错误：

```text
ERROR : 20230203_123826234_iOS.heic: ReadFileHandle.Read error: low level retry 1/10: unexpected EOF
```

或者在使用 `--cache-mode=full` 时报类似下面的错误：

```text
INFO  : 20230203_123826234_iOS.heic: vfs cache: downloader: error count now 1: vfs reader: failed to write to cache file: 416 Requested Range Not Satisfiable:
ERROR : 20230203_123826234_iOS.heic: vfs cache: failed to download: vfs reader: failed to write to cache file: 416 Requested Range Not Satisfiable:
```
