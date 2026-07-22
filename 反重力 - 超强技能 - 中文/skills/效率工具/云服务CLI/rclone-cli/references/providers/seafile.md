---
title: "Seafile"
description: "Seafile 后端的 rclone 文档"
versionIntroduced: "v1.52"
---

> **官方文档:** [https://rclone.org/seafile/](https://rclone.org/seafile/)
# Seafile

这是 [Seafile](https://www.seafile.com/) 存储服务的后端:

- 它同时适用于免费社区版和专业版。
- 支持 Seafile 6.x、7.x、8.x 和 9.x 所有版本。
- 也支持加密资料库。
- 支持启用 2FA（两步验证）的用户
- **不支持** 使用 Library API Token

## 配置

有两种不同的模式可以设置你的远程:

- 你将远程指向**服务器的根目录**，这意味着你在配置过程中不指定资料库：路径以 `remote:library` 的形式指定。你也可以在其中放入子目录，例如 `remote:library/path/to/dir`。
- 你在配置过程中将远程指向特定的资料库：路径以 `remote:path/to/dir` 的形式指定。**在处理加密资料库时推荐使用此模式**。
  (*此模式可能比根模式略快一些*)

### 在根模式下配置

下面是为**未启用**两步验证的用户创建 seafile 配置的示例。首先运行

```console
rclone config
```

这将引导你完成交互式设置过程。要进行身份验证,你需要服务器的 URL、你的电子邮箱(或用户名)和密码。

```text
No remotes found, make a new one\?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> seafile
Type of storage to configure.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
[snip]
XX / Seafile
   \ "seafile"
[snip]
Storage> seafile
** See help for seafile backend at: https://rclone.org/seafile/ **

URL of seafile host to connect to
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
 1 / Connect to cloud.seafile.com
   \ "https://cloud.seafile.com/"
url> http://my.seafile.server/
User name (usually email address)
Enter a string value. Press Enter for the default ("").
user> me@example.com
Password
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank (default)
y/g> y
Enter the password:
password:
Confirm the password:
password:
Two-factor authentication ('true' if the account has 2FA enabled)
Enter a boolean value (true or false). Press Enter for the default ("false").
2fa> false
Name of the library. Leave blank to access all non-encrypted libraries.
Enter a string value. Press Enter for the default ("").
library>
Library password (for encrypted libraries only). Leave blank if you pass it through the command line.
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank (default)
y/g/n> n
Edit advanced config? (y/n)
y) Yes
n) No (default)
y/n> n
Remote config
Two-factor authentication is not enabled on this account.
--------------------
[seafile]
type = seafile
url = http://my.seafile.server/
user = me@example.com
pass = *** ENCRYPTED ***
2fa = false
--------------------
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

此远程名为 `seafile`。它指向你的 seafile 服务器的根目录,现在可以这样使用:

查看所有资料库

```console
rclone lsd seafile:
```

创建一个新资料库

```console
rclone mkdir seafile:library
```

列出某个资料库的内容

```console
rclone ls seafile:library
```

将 `/home/local/directory` 同步到远程资料库,同时删除资料库中的多余文件。

```console
rclone sync --interactive /home/local/directory seafile:library
```

### 在资料库模式下配置

下面是一个针对启用了两步验证的用户的资料库模式配置示例。配置结束时将要求你输入 2FA 验证码,并将尝试验证你的身份:

```text
No remotes found, make a new one\?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> seafile
Type of storage to configure.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
[snip]
XX / Seafile
   \ "seafile"
[snip]
Storage> seafile
** See help for seafile backend at: https://rclone.org/seafile/ **

URL of seafile host to connect to
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
 1 / Connect to cloud.seafile.com
   \ "https://cloud.seafile.com/"
url> http://my.seafile.server/
User name (usually email address)
Enter a string value. Press Enter for the default ("").
user> me@example.com
Password
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank (default)
y/g> y
Enter the password:
password:
Confirm the password:
password:
Two-factor authentication ('true' if the account has 2FA enabled)
Enter a boolean value (true or false). Press Enter for the default ("false").
2fa> true
Name of the library. Leave blank to access all non-encrypted libraries.
Enter a string value. Press Enter for the default ("").
library> My Library
Library password (for encrypted libraries only). Leave blank if you pass it through the command line.
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank (default)
y/g/n> n
Edit advanced config? (y/n)
y) Yes
n) No (default)
y/n> n
Remote config
Two-factor authentication: please enter your 2FA code
2fa code> 123456
Authenticating...
Success!
--------------------
[seafile]
type = seafile
url = http://my.seafile.server/
user = me@example.com
pass =
2fa = true
library = My Library
--------------------
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

你会注意到配置中的密码是空白的。这是因为我们只需要密码对你进行一次身份验证。

你在配置过程中指定了 `My Library`。远程的根目录指向资料库 `My Library` 的根:

查看资料库中的所有文件:

```console
rclone lsd seafile:
```

在资料库中创建一个新目录

```console
rclone mkdir seafile:directory
```

列出某个目录的内容

```console
rclone ls seafile:directory
```

将 `/home/local/directory` 同步到远程资料库,同时删除资料库中的多余文件。

```console
rclone sync --interactive /home/local/directory seafile:
```

### --fast-list

Seafile 7+ 版本支持 `--fast-list`,它允许你以更少的交易次数为代价来使用更多内存。更多细节请参阅 [rclone 文档](/docs/#fast-list)。
请注意,seafile 服务器 6.x 版本不支持此功能。

### 受限文件名字符

除了 [默认受限字符集](/overview/#restricted-characters)之外,以下字符也会被替换:

| 字符 | 值 | 替换为 |
| --------- |:-----:|:-----------:|
| /         | 0x2F  | ／          |
| "         | 0x22  | ＂          |
| \         | 0x5C  | ＼           |

无效的 UTF-8 字节也会被 [替换](/overview/#invalid-utf8),因为它们不能在 JSON 字符串中使用。

### Seafile 和 rclone link

Rclone 仅支持为未加密的资料库生成分享链接。这些链接可以针对某个文件或某个目录:

```console
$ rclone link seafile:seafile-tutorial.doc
http://my.seafile.server/f/fdcd8a2f93f84b8b90f4/

```

如果对某个目录运行,则会得到:

```console
$ rclone link seafile:dir
http://my.seafile.server/d/9ea2455f6f55478bbb0d/
```

请注意,每个文件或目录的分享链接都是唯一的。如果对已经分享过的文件/目录运行 link 命令,你将得到完全相同的链接。

### 兼容性

一直使用以下版本的 [seafile docker 镜像](https://github.com/haiwen/seafile-docker)进行积极开发:

- 6.3.4 社区版
- 7.0.5 社区版
- 7.1.3 社区版
- 9.0.10 社区版

不支持 6.0 以下版本。
6.0 到 6.3 之间的版本未经测试,可能无法正常运行。

每个新版本的 `rclone` 都会使用 seafile 社区服务器的 [最新 docker 镜像](https://hub.docker.com/r/seafileltd/seafile-mc/)进行自动测试。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/seafile/seafile.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是与 seafile (seafile) 相关的标准选项。

#### --seafile-url

要连接的 seafile 主机的 URL。

属性:

- Config:      url
- Env Var:     RCLONE_SEAFILE_URL
- Type:        string
- Required:    true
- Examples:
  - "https://cloud.seafile.com/"
    - 连接到 cloud.seafile.com。

#### --seafile-user

用户名(通常是电子邮箱地址)。

属性:

- Config:      user
- Env Var:     RCLONE_SEAFILE_USER
- Type:        string
- Required:    true

#### --seafile-pass

密码。

**注意** 输入此项必须经过混淆处理 - 参见 [rclone obscure](/commands/rclone_obscure/)。

属性:

- Config:      pass
- Env Var:     RCLONE_SEAFILE_PASS
- Type:        string
- Required:    false

#### --seafile-2fa

两步验证(如果账户启用了 2FA,则为 'true')。

属性:

- Config:      2fa
- Env Var:     RCLONE_SEAFILE_2FA
- Type:        bool
- Default:     false

#### --seafile-library

资料库的名称。

留空以访问所有未加密的资料库。

属性:

- Config:      library
- Env Var:     RCLONE_SEAFILE_LIBRARY
- Type:        string
- Required:    false

#### --seafile-library-key

资料库密码(仅适用于加密资料库)。

如果你通过命令行传递,则留空。

**注意** 输入此项必须经过混淆处理 - 参见 [rclone obscure](/commands/rclone_obscure/)。

属性:

- Config:      library_key
- Env Var:     RCLONE_SEAFILE_LIBRARY_KEY
- Type:        string
- Required:    false

#### --seafile-auth-token

身份验证令牌。

属性:

- Config:      auth_token
- Env Var:     RCLONE_SEAFILE_AUTH_TOKEN
- Type:        string
- Required:    false

### 高级选项

以下是与 seafile (seafile) 相关的高级选项。

#### --seafile-create-library

如果资料库不存在,rclone 是否应该创建一个。

属性:

- Config:      create_library
- Env Var:     RCLONE_SEAFILE_CREATE_LIBRARY
- Type:        bool
- Default:     false

#### --seafile-encoding

后端的编码。

更多信息请参阅 [overview 中的编码部分](/overview/#encoding)。

属性:

- Config:      encoding
- Env Var:     RCLONE_SEAFILE_ENCODING
- Type:        Encoding
- Default:     Slash,DoubleQuote,BackSlash,Ctl,InvalidUtf8,Dot

#### --seafile-description

远程的描述。

属性:

- Config:      description
- Env Var:     RCLONE_SEAFILE_DESCRIPTION
- Type:        string
- Required:    false

<!-- autogenerated options stop -->
