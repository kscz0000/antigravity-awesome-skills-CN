---
title: "Box"
description: "Rclone Box 存储后端文档"
versionIntroduced: "v1.38"
---

> **官方文档：** [https://rclone.org/box/](https://rclone.org/box/)
# Box

路径以 `remote:path` 形式指定。

路径可以任意深度，例如 `remote:directory/subdirectory`。

Box 的初始设置需要从 Box 获取令牌，你可以通过浏览器完成，也可以使用从 Box 下载的 config.json 文件进行 JWT 认证。`rclone config` 会引导你完成整个过程。

## 配置

以下是如何创建一个名为 `remote` 的远程存储的示例。首先运行：

```console
rclone config
```

这将引导你完成交互式设置过程：

```text
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> remote
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / Box
   \ "box"
[snip]
Storage> box
Box App Client Id - leave blank normally.
client_id>
Box App Client Secret - leave blank normally.
client_secret>
Box App config.json location
Leave blank normally.
Enter a string value. Press Enter for the default ("").
box_config_file>
Box App Primary Access Token
Leave blank normally.
Enter a string value. Press Enter for the default ("").
access_token>

Enter a string value. Press Enter for the default ("user").
Choose a number from below, or type in your own value
 1 / Rclone should act on behalf of a user
   \ "user"
 2 / Rclone should act on behalf of a service account
   \ "enterprise"
box_sub_type>
Remote config
Use web browser to automatically authenticate rclone with remote?
 * Say Y if the machine running rclone has a web browser you can use
 * Say N if running rclone on a (remote) machine without web browser access
If not sure try Y. If Y failed, try N.
y) Yes
n) No
y/n> y
If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth?state=XXXXXXXXXXXXXXXXXXXXXX
Log in and authorize rclone for access
Waiting for code...
Got code
Configuration complete.
Options:
- type: box
- client_id:
- client_secret:
- token: {"access_token":"XXX","token_type":"bearer","refresh_token":"XXX","expiry":"XXX"}
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

关于在没有互联网浏览器的机器上设置的说明，请参阅[远程设置文档](/remote_setup/)。

注意，rclone 会在本地机器上运行一个 Web 服务器来收集从 Box 返回的令牌。该服务器仅在你打开浏览器到收到验证码之间运行。它监听在 `http://127.0.0.1:53682/`，如果你运行了主机防火墙，可能需要临时解除对该端口的阻止。

配置完成后，你可以像这样使用 `rclone`（将 `remote` 替换为你给远程存储起的名称）：

列出 Box 顶层的目录

```console
rclone lsd remote:
```

列出 Box 中的所有文件

```console
rclone ls remote:
```

将本地目录复制到 Box 中名为 backup 的目录

```console
rclone copy /home/source remote:backup
```

### 使用带有 SSO 的企业版账户

如果你拥有 Box 的"企业版"账户并启用了单点登录（SSO），则需要创建一个密码才能将 Box 与 rclone 配合使用。可以在你的企业版 Box 账户中完成此操作：进入设置，"账户"选项卡，然后在"身份验证"字段中设置密码。

完成后，你可以按照上面详述的相同流程来设置你的企业版 Box 账户，使用你刚刚设置的密码。

### 无效的刷新令牌

根据 [Box 文档](https://developer.box.com/v2.0/docs/oauth-20#section-6-using-the-access-and-refresh-tokens)：

> 每个 refresh_token 在 60 天内有效一次。

这意味着如果你

- 60 天未使用该 box 远程存储
- 复制包含 box 刷新令牌的配置文件并在两个地方使用
- 在令牌刷新时遇到错误

那么 rclone 将返回包含 `Invalid refresh token` 文本的错误。

要修复此问题，你需要再次使用 oauth2 来更新刷新令牌。你可以使用[远程设置文档](/remote_setup/)中的方法，但请注意，如果你使用了复制配置文件的方法，则不应在执行认证的计算机上使用该远程存储。

操作步骤如下。

```console
$ rclone config
Current remotes:

Name                 Type
====                 ====
remote               box

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> e
Choose a number from below, or type in an existing value
 1 > remote
remote> remote
Configuration complete.
Options:
- type: box
- token: {"access_token":"XXX","token_type":"bearer","refresh_token":"XXX","expiry":"2017-07-08T23:40:08.059167677+01:00"}
Keep this "remote" remote?
Edit remote
Value "client_id" = ""
Edit? (y/n)>
y) Yes
n) No
y/n> n
Value "client_secret" = ""
Edit? (y/n)>
y) Yes
n) No
y/n> n
Remote config
Already have a token - refresh?
y) Yes
n) No
y/n> y
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
Configuration complete.
Options:
- type: box
- token: {"access_token":"YYY","token_type":"bearer","refresh_token":"YYY","expiry":"2017-07-23T12:22:29.259137901+01:00"}
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

### 修改时间和哈希

Box 允许在对象上设置修改时间，精度为 1 秒。这些时间将用于检测对象是否需要同步。

Box 支持 SHA1 类型的哈希，因此你可以使用 `--checksum` 标志。

### 受限文件名字符

除了[默认受限字符集](/overview/#restricted-characters)之外，以下字符也会被替换：

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| \         | 0x5C  | ＼           |

文件名也不能以以下字符结尾。这些字符仅当它们是名称中的最后一个字符时才会被替换：

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| SP        | 0x20  | ␠           |

无效的 UTF-8 字节也会被[替换](/overview/#invalid-utf8)，因为它们不能用于 JSON 字符串中。

### 传输

对于大于 50 MiB 的文件，rclone 将使用分块传输。rclone 会同时上传最多 `--transfers` 个分块（在所有多部分上传之间共享）。分块在内存中缓冲，通常为 8 MiB，因此增加 `--transfers` 会增加内存使用量。

### 删除文件

根据你的用户的企业版设置，项目将被实际从 Box 中删除或移到回收站。

rclone 支持通过 cleanup 命令清空回收站，但这会逐个删除每个被回收的文件和文件夹，因此可能需要很长时间。

通过 WebUI 清空回收站不受此限制，因此建议通过 WebUI 清空回收站。

### 根文件夹 ID

你可以为 rclone 设置 `root_folder_id`。这是 rclone 视为 Box 驱动器根目录的目录（通过其 `Folder ID` 标识）。

通常你会将此项留空，rclone 会自动确定正确的根目录。

但是，你可以设置此项来将 rclone 限制到特定的文件夹层级。

为此，你需要找到希望 rclone 显示的目录的 `Folder ID`。这将是你在 Box 网页界面中打开相应文件夹时 URL 的最后一段。

因此，如果你想让 rclone 使用的文件夹的 URL 在浏览器中看起来像 `https://app.box.com/folder/11xxxxxxxxx8`，那么你就在配置中使用 `11xxxxxxxxx8` 作为 `root_folder_id`。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/box/box.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 box (Box) 特有的标准选项。

#### --box-client-id

OAuth 客户端 ID。

通常留空。

属性：

- Config:      client_id
- Env Var:     RCLONE_BOX_CLIENT_ID
- Type:        string
- Required:    false

#### --box-client-secret

OAuth 客户端密钥。

通常留空。

属性：

- Config:      client_secret
- Env Var:     RCLONE_BOX_CLIENT_SECRET
- Type:        string
- Required:    false

#### --box-box-config-file

Box App config.json 文件位置

通常留空。

文件名中的前导 `~` 将被展开，环境变量如 `${RCLONE_CONFIG_DIR}` 也会被展开。

属性：

- Config:      box_config_file
- Env Var:     RCLONE_BOX_BOX_CONFIG_FILE
- Type:        string
- Required:    false

#### --box-config-credentials

Box App config.json 内容。

通常留空。

属性：

- Config:      config_credentials
- Env Var:     RCLONE_BOX_CONFIG_CREDENTIALS
- Type:        string
- Required:    false

#### --box-access-token

Box App 主访问令牌

通常留空。

属性：

- Config:      access_token
- Env Var:     RCLONE_BOX_ACCESS_TOKEN
- Type:        string
- Required:    false

#### --box-box-sub-type



属性：

- Config:      box_sub_type
- Env Var:     RCLONE_BOX_BOX_SUB_TYPE
- Type:        string
- Default:     "user"
- Examples:
  - "user"
    - Rclone 以用户身份操作。
  - "enterprise"
    - Rclone 以服务账户身份操作。

### 高级选项

以下是 box (Box) 特有的高级选项。

#### --box-token

OAuth 访问令牌，JSON 格式。

属性：

- Config:      token
- Env Var:     RCLONE_BOX_TOKEN
- Type:        string
- Required:    false

#### --box-auth-url

认证服务器 URL。

留空以使用提供者默认值。

属性：

- Config:      auth_url
- Env Var:     RCLONE_BOX_AUTH_URL
- Type:        string
- Required:    false

#### --box-token-url

令牌服务器 URL。

留空以使用提供者默认值。

属性：

- Config:      token_url
- Env Var:     RCLONE_BOX_TOKEN_URL
- Type:        string
- Required:    false

#### --box-client-credentials

使用客户端凭证 OAuth 流程。

这将使用 RFC 6749 中描述的 OAUTH2 客户端凭证流程。

请注意，并非所有后端都支持此选项。

属性：

- Config:      client_credentials
- Env Var:     RCLONE_BOX_CLIENT_CREDENTIALS
- Type:        bool
- Default:     false

#### --box-root-folder-id

填写此项以让 rclone 使用非根文件夹作为起始点。

属性：

- Config:      root_folder_id
- Env Var:     RCLONE_BOX_ROOT_FOLDER_ID
- Type:        string
- Default:     "0"

#### --box-upload-cutoff

切换到多部分上传的阈值（>= 50 MiB）。

属性：

- Config:      upload_cutoff
- Env Var:     RCLONE_BOX_UPLOAD_CUTOFF
- Type:        SizeSuffix
- Default:     50Mi

#### --box-commit-retries

尝试提交多部分文件的最大次数。

属性：

- Config:      commit_retries
- Env Var:     RCLONE_BOX_COMMIT_RETRIES
- Type:        int
- Default:     100

#### --box-list-chunk

列表分块大小，1-1000。

属性：

- Config:      list_chunk
- Env Var:     RCLONE_BOX_LIST_CHUNK
- Type:        int
- Default:     1000

#### --box-owned-by

仅显示由传入的登录名（电子邮件地址）所拥有的项目。

属性：

- Config:      owned_by
- Env Var:     RCLONE_BOX_OWNED_BY
- Type:        string
- Required:    false

#### --box-impersonate

使用服务账户时模拟此用户 ID。

设置此标志允许 rclone 在使用 JWT 服务账户时，通过设置 as-user 标头以另一用户身份操作。

用户 ID 是 Box 中用户的标识符。任何用户的用户 ID 都可以通过 GET /users 端点获取（仅管理员可用），或通过已认证用户会话调用 GET /users/me 端点获取。

参见：https://developer.box.com/guides/authentication/jwt/as-user/


属性：

- Config:      impersonate
- Env Var:     RCLONE_BOX_IMPERSONATE
- Type:        string
- Required:    false

#### --box-encoding

后端的编码方式。

详见[概述中的编码部分](/overview/#encoding)。

属性：

- Config:      encoding
- Env Var:     RCLONE_BOX_ENCODING
- Type:        Encoding
- Default:     Slash,BackSlash,Del,Ctl,RightSpace,InvalidUtf8,Dot

#### --box-description

远程存储的描述。

属性：

- Config:      description
- Env Var:     RCLONE_BOX_DESCRIPTION
- Type:        string
- Required:    false

<!-- autogenerated options stop -->

## 限制

请注意，Box 不区分大小写，因此你不能同时拥有名为 "Hello.doc" 和 "hello.doc" 的文件。

Box 文件名中不能包含 `\` 字符。rclone 会将其映射为外观相同的 Unicode 等效字符 `＼`（U+FF3C 全角反斜杠）。

Box 仅支持最长 255 个字符的文件名。

Box 有 [API 速率限制](https://developer.box.com/guides/api-calls/permissions-and-errors/rate-limits/)，有时会降低 rclone 的速度。

Box 后端不支持 `rclone about`。不支持此功能的后端无法为 rclone mount 确定可用空间，也无法在 rclone union 远程存储中使用 `mfs`（最大可用空间）策略。

参见[不支持 rclone about 的后端列表](https://rclone.org/overview/#optional-features)和 [rclone about](https://rclone.org/commands/rclone_about/)。

## 获取你自己的 Box App ID

以下是如何为 rclone 创建你自己的 Box App ID：

1. 前往 [Box 开发者控制台](https://app.box.com/developers/console)并登录，然后点击侧边栏上的 `My Apps`。点击 `Create New App` 并选择 `Custom App`。

2. 在弹出的第一个屏幕中，你基本可以随意填写。`App Name` 可以随意命名。对于 `Purpose`，选择 automation 以避免填写其他内容。点击 `Next`。

3. 在创建流程的第二个屏幕中，选择 `User Authentication (OAuth 2.0)`。然后点击 `Create App`。

4. 现在你应该在新应用的 `Configuration` 选项卡上。如果不在，点击网页顶部的该选项卡。记下 `Client ID` 和 `Client Secret`，你在 rclone 中会用到它们。

5. 在 "OAuth 2.0 Redirect URI" 下，添加 `http://127.0.0.1:53682/`

6. 对于 `Application Scopes`，选择 `Read all files and folders stored in Box` 和 `Write all files and folders stored in box`（假设你想同时拥有读写权限）。其他保持未选中。点击右上角的 `Save Changes`。
