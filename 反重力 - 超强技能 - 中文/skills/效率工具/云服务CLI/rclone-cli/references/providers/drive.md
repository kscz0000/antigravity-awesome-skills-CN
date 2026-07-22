---
title: "Google drive"
description: "Rclone Google Drive 后端文档：身份验证、配置、scope、服务账号、Shared Drive、性能优化。触发词：Google Drive、rclone、Drive 后端、Google Drive API、Drive 配置、Shared Drive、Team Drive。"
versionIntroduced: "v0.91"
---

> **官方文档:** [https://rclone.org/drive/](https://rclone.org/drive/)
# Google Drive

路径以 `drive:path` 形式指定

Drive 路径可以按需指定任意深度，例如 `drive:directory/subdirectory`。

## Configuration

drive 的初始设置需要从 Google drive 获取一个令牌，这一步需要在浏览器中完成。`rclone config` 会引导你完成整个过程。

下面是一个示例，演示如何创建一个名为 `remote` 的远端。首先运行：

```console
rclone config
```

这将引导你完成一个交互式设置流程：

```text
No remotes found, make a new one?
n) New remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
n/r/c/s/q> n
name> remote
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / Google Drive
   \ "drive"
[snip]
Storage> drive
Google Application Client Id - leave blank normally.
client_id>
Google Application Client Secret - leave blank normally.
client_secret>
Scope that rclone should use when requesting access from drive.
Choose a number from below, or type in your own value
 1 / Full access all files, excluding Application Data Folder.
   \ "drive"
 2 / Read-only access to file metadata and file contents.
   \ "drive.readonly"
   / Access to files created by rclone only.
 3 | These are visible in the drive website.
   | File authorization is revoked when the user deauthorizes the app.
   \ "drive.file"
   / Allows read and write access to the Application Data folder.
 4 | This is not visible in the drive website.
   \ "drive.appfolder"
   / Allows read-only access to file metadata but
 5 | does not allow any access to read or download file content.
   \ "drive.metadata.readonly"
scope> 1
Service Account Credentials JSON file path - needed only if you want use SA instead of interactive login.
service_account_file>
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
Configure this as a Shared Drive (Team Drive)?
y) Yes
n) No
y/n> n
Configuration complete.
Options:
type: drive
- client_id:
- client_secret:
- scope: drive
- root_folder_id:
- service_account_file:
- token: {"access_token":"XXX","token_type":"Bearer","refresh_token":"XXX","expiry":"2014-03-16T13:57:58.955387075Z"}
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

参见 [remote setup docs](/remote_setup/) 了解在没有可联网的 Web 浏览器的机器上如何设置。

注意，如果使用 Web 浏览器自动认证，rclone 会在你的本机启动一个 Web 服务来收集 Google 返回的令牌。该服务仅在从打开浏览器到获取验证码这一段时间内运行。它监听在 `http://127.0.0.1:53682/`，如果你开启了主机防火墙，可能需要临时放行该端口，或者改用手动模式。

之后你可以这样使用它：

列出你的 drive 顶层目录

```console
rclone lsd remote:
```

列出你 drive 中的所有文件

```console
rclone ls remote:
```

将本地目录复制到 drive 中名为 backup 的目录

```console
rclone copy /home/source remote:backup
```

### Scopes

Rclone 允许你选择希望它使用的 scope。这会决定授予 rclone 哪种类型的令牌。[scopes 的定义可参见此处](https://developers.google.com/drive/v3/web/about-auth)。

可以使用以逗号分隔的列表，例如 `drive.readonly,drive.file`。

可用的 scope 包括

#### drive

这是默认的 scope，允许访问除 Application Data Folder 之外的全部文件（见下文）。

如果你不确定选哪个，就选这个。

#### drive.readonly

允许对所有文件进行只读访问。可以列出和下载文件，但无法上传、重命名或删除。

#### drive.file

使用此 scope 时，rclone 只能读取/查看/修改由它自己创建的文件和文件夹。

因此，如果你是通过 Web 界面（或其他方式）上传文件到 drive，rclone 将看不到这些文件。

当你使用 rclone 备份数据并希望确保 drive 上的机密数据不被 rclone 看到时，这非常有用。

使用此 scope 创建的文件可以在 Web 界面中看到。

#### drive.appfolder

这为 rclone 提供了它自己的私有存储区域。Rclone 将无法看到你 drive 上的任何其他文件，你也无法从 Web 界面看到 rclone 的文件。

#### drive.metadata.readonly

这仅允许对文件名进行只读访问。它不允许 rclone 下载或上传数据，也不允许重命名或删除文件或目录。

### Root folder ID

此选项已移至高级部分。你可以为 rclone 设置 `root_folder_id`。这是 rclone 视作你 drive 根目录的目录（通过其 `Folder ID` 标识）。

通常你应保持此项留空，rclone 会自行确定正确的根目录。

不过你也可以设置它，以便将 rclone 限制在特定的文件夹层次结构内，或访问 drive Web 界面中 "Computers" 选项卡下的数据（即 Google Backup and Sync 桌面程序存放文件的位置）。

要做到这一点，你需要找到希望 rclone 使用的目录的 `Folder ID`。这将是该文件夹在 drive Web 界面中打开时 URL 的最后一段。

因此，如果希望 rclone 使用的文件夹在浏览器中的 URL 形如
`https://drive.google.com/drive/folders/1XyfxxxxxxxxxxxxxxxxxxxxxxxxxKHCh`
那么你就可以在配置中使用 `1XyfxxxxxxxxxxxxxxxxxxxxxxxxxKHCh` 作为 `root_folder_id`。

**注意** 使用 rclone 时，"Computers" 选项卡下的文件夹似乎为只读（drive 会返回 500 错误）。

目前似乎没有 API 可以发现 "Computers" 选项卡的文件夹 ID——如果你知道，烦请告知我们！

还要注意，rclone 目前还无法访问 google drive Web 界面中 "Backups" 选项卡下的任何数据。

### Service Account support

你可以以无人值守模式使用 Google Drive 配置 rclone，即不绑定到特定的最终用户 Google 账户。当希望将文件同步到没有活跃登录用户的机器上（例如构建机器）时，这非常有用。

要使用 Service Account 代替 OAuth2 令牌流程，请在 `rclone config` 的 `service_account_file` 提示处输入你的 Service Account 凭据文件路径，rclone 不会使用基于浏览器的认证流程。如果你想将凭据文件的内容直接放入 rclone 配置文件，也可以改为设置 `service_account_credentials`，填入文件的实际内容，或者设置相应的环境变量。

#### Use case - Google Workspace account and individual Drive

假设你是 Google Workspace 的管理员。目标是对属于该域的某个个人 Drive 账户进行读写。我们称该域为 <example.com>，该用户为 <foo@example.com>。

完成此任务需要执行以下几步：

##### 1. Create a service account for example.com

- 要创建 service account 并获取其凭据，请前往 [Google Developer Console](https://console.developers.google.com)。
- 你必须有一个 project——如果还没有请新建一个，并确保你已切换到该项目。
- 然后进入 "IAM & admin" -> "Service Accounts"。
- 点击 "Create Service Account" 按钮。在 "Service account name" 和 "Service account ID" 中填写可以标识你的客户端的内容。
- 选择 "Create And Continue"。第 2 步和第 3 步为可选。
- 点击新创建的 service account
- 点击 "Keys"，然后点击 "Add Key"，再点击 "Create new key"
- 选择类型 "JSON" 并点击 create
- 这将下载一个小的 JSON 文件，rclone 将使用它进行认证。

如果你需要撤销访问权限，请点击 "Delete service account key" 按钮。

##### 2. Allowing API access to example.com Google Drive

- 进入 example.com 的 [Workspace Admin Console](https://admin.google.com)
- 进入 "Security"（或使用搜索栏）
- 选择 "Access and data control"，然后选择 "API controls"
- 点击 "Manage domain-wide delegation"
- 点击 "Add new"
- 在 "Client ID" 字段中输入 service account 的
  "Client ID"——可以在 Developer Console 的
  "IAM & Admin" -> "Service Accounts" 下，对新创建的
  service account 点击 "View Client ID" 找到该值。
  它是一个约 21 位的数字字符串。
- 在下一个字段 "OAuth Scopes" 中输入
  `https://www.googleapis.com/auth/drive`
  以专门授予对 Google Drive 的读写访问权限。
  你也可以使用 `https://www.googleapis.com/auth/drive.readonly` 配合 `--drive-scope=drive.readonly` 实现只读访问。
- 点击 "Authorise"

##### 3. Configure rclone, assuming a new install

```text
rclone config

n/s/q> n         # New
name>gdrive      # Gdrive is an example name
Storage>         # Type drive
client_id>       # Can be left blank
client_secret>   # Can be left blank
scope>           # Select the scope use used in step 2
root_folder_id>  # Can be left blank
service_account_file> /home/foo/myJSONfile.json # Path to the JSON file you downloaded in step 1.
y/n>             # Auto config, n

```

##### 4. Verify that it's working

- `rclone -v --drive-impersonate foo@example.com lsf gdrive:backup`
- 参数说明：
  - `-v` - 详细日志
  - `--drive-impersonate foo@example.com` - 这是起关键作用的部分，模拟用户 foo
  - `lsf` - 以便于解析的方式列出文件
  - `gdrive:backup` - 使用名为 gdrive 的远端，操作名为 backup 的文件夹

注意：如果你在 gdrive 上配置了特定根目录，而 rclone 在使用 `--drive-impersonate` 时无法访问该目录的内容，请改用以下方法：

- 在 gdrive Web 界面中，将你的根目录共享给第 1 步中创建/选择的 Service Account 的用户/邮箱
- 不使用 `--drive-impersonate` 选项运行 rclone，例如：
  `rclone -v lsf gdrive:backup`

### Shared drives (team drives)

如果你希望将远端配置指向 Google Shared Drive（旧称 Team Drives），请在 "Configure this as a Shared Drive (Team Drive)?" 这一问题处回答 `y`。

这会从 Google 拉取 Shared Drive 列表，并允许你选择希望使用哪一个。如果你愿意，也可以直接输入 Shared Drive ID。

例如：

```text
Configure this as a Shared Drive (Team Drive)?
y) Yes
n) No
y/n> y
Fetching Shared Drive list...
Choose a number from below, or type in your own value
 1 / Rclone Test
   \ "xxxxxxxxxxxxxxxxxxxx"
 2 / Rclone Test 2
   \ "yyyyyyyyyyyyyyyyyyyy"
 3 / Rclone Test 3
   \ "zzzzzzzzzzzzzzzzzzzz"
Enter a Shared Drive ID> 1
Configuration complete.
Options:
- type: drive
- client_id:
- client_secret:
- token: {"AccessToken":"xxxx.x.xxxxx_xxxxxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","RefreshToken":"1/xxxxxxxxxxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxxxx","Expiry":"2014-03-16T13:57:58.955387075Z","Extra":null}
- team_drive: xxxxxxxxxxxxxxxxxxxx
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

### --fast-list

该远端支持 `--fast-list`，它能让你以更多内存为代价减少事务次数。详见 [rclone docs](/docs/#fast-list)。

其原理是将多个 `list` 调用合并为单个 API 请求。

具体做法是将多个 `'%s' in parents` 过滤条件合并为一个表达式。例如要列出目录 a、b、c 的内容，普通 `List` 函数会发出以下请求：

```text
trashed=false and 'a' in parents
trashed=false and 'b' in parents
trashed=false and 'c' in parents
```

这些请求现在可以合并为单个请求：

```text
trashed=false and ('a' in parents or 'b' in parents or 'c' in parents)
```

`ListR` 的实现一次请求最多可放入 50 个 `parents` 过滤条件。它会使用 `--checkers` 值来指定并行运行的请求数。

在测试中，这些批处理请求比普通方法最多快 20 倍。对不同大小的文件夹运行以下命令得到：

```console
rclone lsjson -vv -R --checkers=6 gdrive:folder
```

小文件夹（220 个目录，700 个文件）：

- 不使用 `--fast-list`：38s
- 使用 `--fast-list`：10s

大文件夹（10600 个目录，39000 个文件）：

- 不使用 `--fast-list`：22:05 min
- 使用 `--fast-list`：58s

### Modification times and hashes

Google drive 以 1 毫秒的精度存储修改时间。

支持 MD5、SHA1 和 SHA256 哈希算法。但请注意，有一小部分上传的文件可能没有 SHA1 或 SHA256 哈希，尤其是 2018 年之前上传的文件。

### Restricted filename characters

只有非法的 UTF-8 字节会被 [替换](/overview/#invalid-utf8)，因为它们无法在 JSON 字符串中使用。

与其他后端不同，`/` 也可以在名称中使用，且 `.` 或 `..` 是合法名称。

### Revisions

Google drive 会保存文件的修订版本。当你对 drive 中已存在的文件使用 rclone 上传更改时，它会为该文件创建一个新版本。

修订版本的保留遵循 Google 的标准策略，撰写本文时为：

- 在 30 天或 100 个版本后删除（以先到者为准）。
- 不计入用户的存储配额。

### Deleting files

默认情况下，rclone 在删除文件时会把所有文件放入回收站。如果需要永久删除，请使用 `--drive-use-trash=false` 标志，或设置相应的环境变量。

### Shortcuts

2020 年 3 月，Google 在 Google Drive 中引入了一项新功能，称为 [drive shortcuts](https://support.google.com/drive/answer/9700156)（[API](https://developers.google.com/drive/api/v3/shortcuts)）。该功能将（到 2020 年 9 月时）[取代文件或文件夹可同时存在于多个位置的能力](https://cloud.google.com/blog/products/g-suite/simplifying-google-drives-folder-structure-and-sharing-models)。

Shortcuts 是指向 Google Drive 上其他文件的文件，类似于 unix 中的符号链接，只不过它们指向底层的文件数据（例如 unix 中的 inode），因此当源文件被重命名或移动时它们不会失效。

默认情况下，rclone 对它们的处理方式如下。

对于指向文件的 shortcuts：

- 列出时，文件快捷方式显示为目标文件。
- 下载时，会下载目标文件的内容。
- 使用非快捷方式文件更新快捷方式文件时，会先移除该快捷方式，然后上传新文件以代替该快捷方式。
- 服务端移动（重命名）时，会重命名快捷方式本身，而不是目标文件。
- 服务端复制时，会复制快捷方式本身，而不是快捷方式的内容。
  （除非使用 `--drive-copy-shortcut-content`，此时复制的是快捷方式的内容。）
- 删除时，删除的是快捷方式本身，而不是所链接的文件。
- 设置修改时间时，会设置所链接文件的修改时间。

对于指向文件夹的 shortcuts：

- 列出时，快捷方式显示为文件夹，且该文件夹中会显示所链接文件夹的内容（包括任何子文件夹）。
- 下载时，下载的是所链接文件夹及其子项的内容。
- 上传到快捷方式文件夹时，文件会被放到所链接的文件夹中。
- 服务端移动（重命名）时，会重命名快捷方式本身，而不是目标文件夹。
- 服务端复制时，复制的是所链接文件夹的内容，而不是快捷方式本身。
- 使用 `rclone rmdir` 或 `rclone purge` 删除时，删除的是快捷方式本身，而不是所链接的文件夹。
- **注意** 使用 `rclone remove` 或 `rclone mount` 删除时，删除的将是所链接文件夹的内容。

[rclone backend](https://rclone.org/commands/rclone_backend/) 命令可用于创建快捷方式。

可以使用 `--drive-skip-shortcuts` 标志或对应的 `skip_shortcuts` 配置项完全忽略快捷方式。

如果你的 drive 中存在导致无限递归的快捷方式（例如指向父文件夹的快捷方式），可能必须设置 `skip_shortcuts` 才能成功复制该 drive。

### Emptying trash

如果你希望清空回收站，可以使用 `rclone cleanup remote:` 命令，它会永久删除所有已放入回收站的文件。此命令不接受任何路径参数。

注意，即使命令在数秒内返回，Google Drive 真正清空回收站也需要一些时间（从几分钟到几天不等）。不会有任何输出回显，所以即使使用 `-v` 或 `-vv` 也看不到确认信息。

### Quota information

要查看当前配额，可以使用 `rclone about remote:` 命令，它会显示你的使用上限（配额）、Google Drive 中的用量、回收站中所有文件的大小以及 Gmail 等其他 Google 服务占用的空间。此命令不接受任何路径参数。

#### Import/Export of google documents

可以从 Google Drive 导出 Google 文档，也可以上传到 Google Drive。

当 rclone 下载一个 Google 文档时，它会根据 `--drive-export-formats` 设置选择下载格式。
默认的导出格式是 `docx,xlsx,pptx,svg`，对于可编辑文档来说这是一个合理的默认选择。

选择格式时，rclone 会按顺序遍历提供的列表，并选择该文档可被导出为的第一个格式。如果该文件无法导出为列表中的任何格式，rclone 会从默认列表中选择一种格式。

如果你希望保留归档副本，可以使用 `--drive-export-formats pdf`；如果你偏好 openoffice/libreoffice 格式，可以使用 `--drive-export-formats ods,odt,odp`。

注意，rclone 会为 Google 文档添加扩展名。因此如果它在 google docs 中叫 `My Spreadsheet`，导出后将变成 `My Spreadsheet.xlsx` 或 `My Spreadsheet.pdf` 等。

当将文件导入 Google Drive 时，rclone 会将扩展名出现在 `--drive-import-formats` 中的所有文件转换为对应的文档类型。
rclone 默认不会转换任何文件，因为转换过程是有损的。

转换后得到的文件，其扩展名在应用 `--drive-export-formats` 规则到上传文档时必须保持一致。

下表给出了一些允许和禁止的转换示例。

| export-formats | import-formats | Upload Ext | Document Ext | Allowed |
| -------------- | -------------- | ---------- | ------------ | ------- |
| odt | odt | odt | odt | Yes |
| odt | docx,odt | odt | odt | Yes |
|  | docx | docx | docx | Yes |
|  | odt | odt | docx | No |
| odt,docx | docx,odt | docx | odt | No |
| docx,odt | docx,odt | docx | docx | Yes |
| docx,odt | docx,odt | odt | docx | No |

可以通过指定 `--drive-allow-import-name-change` 来解除此限制。使用此标志时，rclone 可以一次性将多种文件类型转换为同一种文档类型，例如使用 `--drive-import-formats docx,odt,txt` 时，所有具有这些扩展名的文件最终都会表示为 docx 文件。
这会带来额外的文件覆盖风险——如果多个文件具有相同的主文件名。Rclone 的许多操作都不会处理这种名称变化。它们在复制文件时假设名称相同，并可能在名称变化时再次复制或删除文件。

下面列出所有可能的导出扩展名及其对应的 mime 类型。
其中大多数也可用于导入，但还有一些未在此列出的扩展名。某些额外的扩展名可能只有当操作系统提供了正确的 MIME 类型条目时才可用。

此列表可能随时被 Google Drive 修改，可能并不反映当前可用的转换。

| Extension | Mime Type | Description |
| --------- |-----------| ------------|
| bmp  | image/bmp | Windows Bitmap format |
| csv  | text/csv | Standard CSV format for Spreadsheets |
| doc  | application/msword | Classic Word file |
| docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document | Microsoft Office Document |
| epub | application/epub+zip | E-book format |
| html | text/html | An HTML Document |
| jpg  | image/jpeg | A JPEG Image File |
| json | application/vnd.google-apps.script+json | JSON Text Format for Google Apps scripts |
| md   | text/markdown | Markdown Text Format |
| odp  | application/vnd.oasis.opendocument.presentation | Openoffice Presentation |
| ods  | application/vnd.oasis.opendocument.spreadsheet | Openoffice Spreadsheet |
| ods  | application/x-vnd.oasis.opendocument.spreadsheet | Openoffice Spreadsheet |
| odt  | application/vnd.oasis.opendocument.text | Openoffice Document |
| pdf  | application/pdf | Adobe PDF Format |
| pjpeg | image/pjpeg | Progressive JPEG Image |
| png  | image/png | PNG Image Format|
| pptx | application/vnd.openxmlformats-officedocument.presentationml.presentation | Microsoft Office Powerpoint |
| rtf  | application/rtf | Rich Text Format |
| svg  | image/svg+xml | Scalable Vector Graphics Format |
| tsv  | text/tab-separated-values | Standard TSV format for spreadsheets |
| txt  | text/plain | Plain Text |
| wmf  | application/x-msmetafile | Windows Meta File |
| xls  | application/vnd.ms-excel | Classic Excel file |
| xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | Microsoft Office Spreadsheet |
| zip  | application/zip | A ZIP file of HTML, Images CSS |

Google 文档也可以导出为链接文件。打开这类文件时，会弹出浏览器窗口打开该 Google Docs 网站上的对应文档。链接文件的扩展名需要以 `--drive-export-formats` 参数的形式指定，它们会匹配所有可用的 Google 文档。

| Extension | Description | OS Support |
| --------- | ----------- | ---------- |
| desktop | freedesktop.org specified desktop entry | Linux |
| link.html | An HTML Document with a redirect | All |
| url | INI style link file | macOS, Windows |
| webloc | macOS specific XML format | macOS |

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/drive/drive.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### Standard options

以下是 drive（Google Drive）特有的 Standard options。

#### --drive-client-id

Google Application Client Id
建议设置为你自己的。
请参阅 https://rclone.org/drive/#making-your-own-client-id 了解如何创建你自己的。
如果留空，将使用内置 key，性能较低。

Properties:

- Config:      client_id
- Env Var:     RCLONE_DRIVE_CLIENT_ID
- Type:        string
- Required:    false

#### --drive-client-secret

OAuth Client Secret。

通常保持留空。

Properties:

- Config:      client_secret
- Env Var:     RCLONE_DRIVE_CLIENT_SECRET
- Type:        string
- Required:    false

#### --drive-scope

rclone 向 drive 请求访问权限时使用的、以逗号分隔的 scope 列表。

Properties:

- Config:      scope
- Env Var:     RCLONE_DRIVE_SCOPE
- Type:        string
- Required:    false
- Examples:
  - "drive"
    - Full access all files, excluding Application Data Folder.
  - "drive.readonly"
    - Read-only access to file metadata and file contents.
  - "drive.file"
    - Access to files created by rclone only.
    - These are visible in the drive website.
    - File authorization is revoked when the user deauthorizes the app.
  - "drive.appfolder"
    - Allows read and write access to the Application Data folder.
    - This is not visible in the drive website.
  - "drive.metadata.readonly"
    - Allows read-only access to file metadata but
    - does not allow any access to read or download file content.

#### --drive-service-account-file

Service Account 凭据 JSON 文件路径。

通常保持留空。
仅当你希望使用 SA 代替交互式登录时才需要设置。

文件名前导的 `~` 会被展开，环境变量（例如 `${RCLONE_CONFIG_DIR}`）也会被展开。

Properties:

- Config:      service_account_file
- Env Var:     RCLONE_DRIVE_SERVICE_ACCOUNT_FILE
- Type:        string
- Required:    false

#### --drive-alternate-export

已弃用：不再需要。

Properties:

- Config:      alternate_export
- Env Var:     RCLONE_DRIVE_ALTERNATE_EXPORT
- Type:        bool
- Default:     false

### Advanced options

以下是 drive（Google Drive）特有的 Advanced options。

#### --drive-token

以 JSON blob 形式给出的 OAuth 访问令牌。

Properties:

- Config:      token
- Env Var:     RCLONE_DRIVE_TOKEN
- Type:        string
- Required:    false

#### --drive-auth-url

授权服务器 URL。

留空以使用 provider 默认值。

Properties:

- Config:      auth_url
- Env Var:     RCLONE_DRIVE_AUTH_URL
- Type:        string
- Required:    false

#### --drive-token-url

令牌服务器 URL。

留空以使用 provider 默认值。

Properties:

- Config:      token_url
- Env Var:     RCLONE_DRIVE_TOKEN_URL
- Type:        string
- Required:    false

#### --drive-client-credentials

使用 client credentials OAuth 流程。

将使用 RFC 6749 中描述的 OAUTH2 client Credentials Flow。

注意该选项并非所有后端都支持。

Properties:

- Config:      client_credentials
- Env Var:     RCLONE_DRIVE_CLIENT_CREDENTIALS
- Type:        bool
- Default:     false

#### --drive-root-folder-id

根目录的 ID。
通常保持留空。

填写此项以访问 "Computers" 文件夹（参见文档），或让 rclone 以非根目录作为起点。


Properties:

- Config:      root_folder_id
- Env Var:     RCLONE_DRIVE_ROOT_FOLDER_ID
- Type:        string
- Required:    false

#### --drive-service-account-credentials

Service Account 凭据 JSON blob。

通常保持留空。
仅当你希望使用 SA 代替交互式登录时才需要设置。

Properties:

- Config:      service_account_credentials
- Env Var:     RCLONE_DRIVE_SERVICE_ACCOUNT_CREDENTIALS
- Type:        string
- Required:    false

#### --drive-team-drive

Shared Drive（Team Drive）的 ID。

Properties:

- Config:      team_drive
- Env Var:     RCLONE_DRIVE_TEAM_DRIVE
- Type:        string
- Required:    false

#### --drive-auth-owner-only

仅考虑经过身份验证的用户拥有的文件。

Properties:

- Config:      auth_owner_only
- Env Var:     RCLONE_DRIVE_AUTH_OWNER_ONLY
- Type:        bool
- Default:     false

#### --drive-use-trash

将文件放入回收站而不是永久删除。

默认为 true，即将文件放入回收站。
使用 `--drive-use-trash=false` 可改为永久删除文件。

Properties:

- Config:      use_trash
- Env Var:     RCLONE_DRIVE_USE_TRASH
- Type:        bool
- Default:     true

#### --drive-copy-shortcut-content

在服务端复制快捷方式的内容而不是快捷方式本身。

执行服务端复制时，rclone 默认会按快捷方式复制快捷方式。

如果使用此标志，rclone 会在服务端复制时复制快捷方式的内容，而不是快捷方式本身。

Properties:

- Config:      copy_shortcut_content
- Env Var:     RCLONE_DRIVE_COPY_SHORTCUT_CONTENT
- Type:        bool
- Default:     false

#### --drive-skip-gdocs

在所有列出操作中跳过 google 文档。

如果启用，gdocs 对 rclone 几乎变为不可见。

Properties:

- Config:      skip_gdocs
- Env Var:     RCLONE_DRIVE_SKIP_GDOCS
- Type:        bool
- Default:     false

#### --drive-show-all-gdocs

在列出中显示所有 Google Docs，包括不可导出的。

如果你在不带此标志的情况下对 Google Form 执行服务端复制，将出现以下错误：

    No export formats found for "application/vnd.google-apps.form"

但加上此标志后即可在服务端复制该表单。

注意，在此模式下 rclone 不会为 Google Docs 文件名添加扩展名。

不要在尝试下载 Google Docs 时使用此标志——rclone 将无法下载它们。


Properties:

- Config:      show_all_gdocs
- Env Var:     RCLONE_DRIVE_SHOW_ALL_GDOCS
- Type:        bool
- Default:     false

#### --drive-skip-checksum-gphotos

仅对 Google photos 和 videos 跳过校验和。

当传输 Google photos 或 videos 出现校验和错误时，可使用此标志。

设置此标志会导致 Google photos 和 videos 返回空白校验和。

Google photos 通过位于 "photos" 空间来识别。

校验和损坏是由 Google 修改了图片/视频但未更新校验和造成的。

Properties:

- Config:      skip_checksum_gphotos
- Env Var:     RCLONE_DRIVE_SKIP_CHECKSUM_GPHOTOS
- Type:        bool
- Default:     false

#### --drive-shared-with-me

仅显示与我共享的文件。

指示 rclone 操作你的 "Shared with me" 文件夹（即 Google Drive 中存放他人与你共享的文件和文件夹的位置）。

这对于 "list"（lsd、lsl 等）和 "copy"（copy、sync 等）命令以及其他所有命令都生效。

Properties:

- Config:      shared_with_me
- Env Var:     RCLONE_DRIVE_SHARED_WITH_ME
- Type:        bool
- Default:     false

#### --drive-trashed-only

仅显示回收站中的文件。

这会在原始目录结构中显示已放入回收站的文件。

Properties:

- Config:      trashed_only
- Env Var:     RCLONE_DRIVE_TRASHED_ONLY
- Type:        bool
- Default:     false

#### --drive-starred-only

仅显示已加星标的文件。

Properties:

- Config:      starred_only
- Env Var:     RCLONE_DRIVE_STARRED_ONLY
- Type:        bool
- Default:     false

#### --drive-formats

已弃用：请参见 export_formats。

Properties:

- Config:      formats
- Env Var:     RCLONE_DRIVE_FORMATS
- Type:        string
- Required:    false

#### --drive-export-formats

下载 Google 文档时优先格式的逗号分隔列表。

Properties:

- Config:      export_formats
- Env Var:     RCLONE_DRIVE_EXPORT_FORMATS
- Type:        string
- Default:     "docx,xlsx,pptx,svg"

#### --drive-import-formats

上传 Google 文档时优先格式的逗号分隔列表。

Properties:

- Config:      import_formats
- Env Var:     RCLONE_DRIVE_IMPORT_FORMATS
- Type:        string
- Required:    false

#### --drive-allow-import-name-change

允许在上传 Google 文档时改变文件类型。

例如 file.doc 变为 file.docx。这会让 sync 出现混乱，导致每次都重新上传。

Properties:

- Config:      allow_import_name_change
- Env Var:     RCLONE_DRIVE_ALLOW_IMPORT_NAME_CHANGE
- Type:        bool
- Default:     false

#### --drive-use-created-date

使用文件创建日期而非修改日期。

在下载数据并希望使用创建日期代替最后修改日期时很有用。

**警告**：此标志可能产生一些意料之外的后果。

当上传到你的 drive 时，除非自创建以来未被修改，否则所有文件都将被覆盖；下载时则相反。可以通过使用 "--checksum" 标志来避免这种副作用。

实现此特性是为了保留 google photos 记录的拍摄日期。你首先需要在 google drive 设置中勾选 "Create a Google Photos folder" 选项。然后可以在本地复制或移动照片，使用照片的拍摄（创建）日期作为修改日期。

Properties:

- Config:      use_created_date
- Env Var:     RCLONE_DRIVE_USE_CREATED_DATE
- Type:        bool
- Default:     false

#### --drive-use-shared-date

使用文件被共享的日期而非修改日期。

注意，与 "--drive-use-created-date" 类似，此标志在上传/下载文件时也可能产生意料之外的后果。

如果同时设置了此标志和 "--drive-use-created-date"，则使用创建日期。

Properties:

- Config:      use_shared_date
- Env Var:     RCLONE_DRIVE_USE_SHARED_DATE
- Type:        bool
- Default:     false

#### --drive-list-chunk

列表块大小 100-1000，0 表示禁用。

Properties:

- Config:      list_chunk
- Env Var:     RCLONE_DRIVE_LIST_CHUNK
- Type:        int
- Default:     1000

#### --drive-impersonate

使用 service account 时以此用户身份进行模拟。

Properties:

- Config:      impersonate
- Env Var:     RCLONE_DRIVE_IMPERSONATE
- Type:        string
- Required:    false

#### --drive-upload-cutoff

切换到分块上传的阈值。

Properties:

- Config:      upload_cutoff
- Env Var:     RCLONE_DRIVE_UPLOAD_CUTOFF
- Type:        SizeSuffix
- Default:     8Mi

#### --drive-chunk-size

上传块大小。

必须是 >= 256k 的 2 的幂。

增大该值可以提升性能，但请注意每个块在每个传输中都会被缓存在内存中。

减小该值可以降低内存占用，但会降低性能。

Properties:

- Config:      chunk_size
- Env Var:     RCLONE_DRIVE_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     8Mi

#### --drive-acknowledge-abuse

设置为允许下载返回 cannotDownloadAbusiveFile 的文件。

如果下载文件时返回错误 "This file has been identified as malware or spam and cannot be downloaded" 且错误码为 "cannotDownloadAbusiveFile"，请向 rclone 提供此标志，以表明你了解下载该文件的风险，rclone 仍会下载它。

注意，如果你使用 service account，则需要 Manager 权限（而不是 Content Manager）才能使该标志生效。如果 SA 没有相应权限，Google 会直接忽略该标志。

Properties:

- Config:      acknowledge_abuse
- Env Var:     RCLONE_DRIVE_ACKNOWLEDGE_ABUSE
- Type:        bool
- Default:     false

#### --drive-keep-revision-forever

永久保留每个文件的最新 head 版本。

Properties:

- Config:      keep_revision_forever
- Env Var:     RCLONE_DRIVE_KEEP_REVISION_FOREVER
- Type:        bool
- Default:     false

#### --drive-size-as-quota

将文件大小显示为存储配额使用量，而非实际大小。

将文件大小显示为占用的存储配额，即当前版本加上任何被设置为永久保留的旧版本。

**警告**：此标志可能产生一些意料之外的后果。

不建议在配置中设置此标志——推荐用法是在执行 rclone ls/lsl/lsf/lsjson 等命令时使用 `--drive-size-as-quota` 标志形式。

如果对 sync 使用此标志（不推荐），则还需要同时使用 `--ignore size`。


Properties:

- Config:      size_as_quota
- Env Var:     RCLONE_DRIVE_SIZE_AS_QUOTA
- Type:        bool
- Default:     false

#### --drive-v2-download-min-size

若对象大小超过该值，则使用 drive v2 API 下载。

Properties:

- Config:      v2_download_min_size
- Env Var:     RCLONE_DRIVE_V2_DOWNLOAD_MIN_SIZE
- Type:        SizeSuffix
- Default:     off

#### --drive-pacer-min-sleep

API 调用之间的最小休眠时间。

Properties:

- Config:      pacer_min_sleep
- Env Var:     RCLONE_DRIVE_PACER_MIN_SLEEP
- Type:        Duration
- Default:     100ms

#### --drive-pacer-burst

允许不进行休眠的连续 API 调用次数。

Properties:

- Config:      pacer_burst
- Env Var:     RCLONE_DRIVE_PACER_BURST
- Type:        int
- Default:     100

#### --drive-server-side-across-configs

已弃用：请改用 --server-side-across-configs。

允许服务端操作（例如 copy）跨不同的 drive 配置工作。

当希望在不同 Google drive 之间执行服务端复制时，这非常有用。注意默认未启用，因为难以预判它在任意两个配置间能否工作。

Properties:

- Config:      server_side_across_configs
- Env Var:     RCLONE_DRIVE_SERVER_SIDE_ACROSS_CONFIGS
- Type:        bool
- Default:     false

#### --drive-disable-http2

禁用 drive 使用 http2。

目前 google drive 后端与 HTTP/2 存在一个未解决的问题。因此 drive 后端默认禁用 HTTP/2，但可以在这里重新启用。该问题解决后此标志将被移除。

参见：https://github.com/rclone/rclone/issues/3631



Properties:

- Config:      disable_http2
- Env Var:     RCLONE_DRIVE_DISABLE_HTTP2
- Type:        bool
- Default:     true

#### --drive-stop-on-upload-limit

将上传限制错误视为致命错误。

撰写本文时，每天最多只能向 Google Drive 上传 750 GiB 数据（这是未文档化的限制）。当达到该限制时，Google Drive 会产生略有不同的错误消息。设置此标志后，这些错误将被视为致命错误，并终止正在进行的同步。

注意该检测依赖于 Google 未文档化的错误消息字符串，未来可能会失效。

参见：https://github.com/rclone/rclone/issues/3857


Properties:

- Config:      stop_on_upload_limit
- Env Var:     RCLONE_DRIVE_STOP_ON_UPLOAD_LIMIT
- Type:        bool
- Default:     false

#### --drive-stop-on-download-limit

将下载限制错误视为致命错误。

撰写本文时，每天最多只能从 Google Drive 下载 10 TiB 数据（这是未文档化的限制）。当达到该限制时，Google Drive 会产生略有不同的错误消息。设置此标志后，这些错误将被视为致命错误，并终止正在进行的同步。

注意该检测依赖于 Google 未文档化的错误消息字符串，未来可能会失效。


Properties:

- Config:      stop_on_download_limit
- Env Var:     RCLONE_DRIVE_STOP_ON_DOWNLOAD_LIMIT
- Type:        bool
- Default:     false

#### --drive-skip-shortcuts

如果设置，则跳过快捷方式文件。

通常 rclone 会解引用快捷方式文件，使它们看起来就像原始文件本身（参见 [shortcuts 章节](#shortcuts)）。如果设置了此标志，rclone 将完全忽略快捷方式文件。


Properties:

- Config:      skip_shortcuts
- Env Var:     RCLONE_DRIVE_SKIP_SHORTCUTS
- Type:        bool
- Default:     false

#### --drive-skip-dangling-shortcuts

如果设置，则跳过悬空的快捷方式文件。

如果设置了此标志，rclone 在列出时将不会显示任何悬空的快捷方式。


Properties:

- Config:      skip_dangling_shortcuts
- Env Var:     RCLONE_DRIVE_SKIP_DANGLING_SHORTCUTS
- Type:        bool
- Default:     false

#### --drive-resource-key

用于访问通过链接共享的文件的 resource key。

如果你需要访问通过链接共享的文件，形如：

    https://drive.google.com/drive/folders/XXX?resourcekey=YYY&usp=sharing

则需要将第一部分 "XXX" 作为 "root_folder_id"，将第二部分 "YYY" 作为 "resource_key"，否则在尝试访问该目录时会出现 404 not found 错误。

参见：https://developers.google.com/drive/api/guides/resource-keys

该 resource key 要求仅适用于一部分较老的文件。

另外注意，在 Web 界面中（使用你已为 rclone 认证的用户）打开该文件夹一次后，似乎就不再需要 resource key 了。


Properties:

- Config:      resource_key
- Env Var:     RCLONE_DRIVE_RESOURCE_KEY
- Type:        string
- Required:    false

#### --drive-fast-list-bug-fix

规避 Google Drive 列表中的一个 bug。

通常 rclone 会在使用 --fast-list（ListR）时规避 Google Drive 中的一个 bug，该 bug 会导致搜索 "(A in parents) or (B in parents)" 有时返回空。参见 #3114、#4289 和 https://issuetracker.google.com/issues/149522397

Rclone 通过在列出时发现多个目录中都找不到任何项来检测该问题，并将它们作为独立目录的列表进行重试。

这意味着如果你有大量空目录，rclone 最终会逐个列出它们，这会消耗更多的 API 调用。

此标志允许禁用该规避方案。**不**建议在常规使用中关闭——仅当你在某些特殊场景下（例如存在大量空目录）遇到问题时才应禁用。


Properties:

- Config:      fast_list_bug_fix
- Env Var:     RCLONE_DRIVE_FAST_LIST_BUG_FIX
- Type:        bool
- Default:     true

#### --drive-metadata-owner

控制是否在元数据中读取或写入 owner。

Owner 是文件元数据的标准组成部分，因此易于读取。但并不总是希望通过元数据来设置 owner。

注意，你无法在 Shared Drives 上设置 owner；设置所有权会向新 owner 发送一封邮件（这无法禁用）；也无法将所有权转移给你所在组织之外的人员。


Properties:

- Config:      metadata_owner
- Env Var:     RCLONE_DRIVE_METADATA_OWNER
- Type:        Bits
- Default:     read
- Examples:
  - "off"
    - Do not read or write the value
  - "read"
    - Read the value only
  - "write"
    - Write the value only
  - "failok"
    - If writing fails log errors only, don't fail the transfer
  - "read,write"
    - Read and Write the value.

#### --drive-metadata-permissions

控制是否在元数据中读取或写入 permissions。

从文件读取 permissions 元数据的速度很快，但并不总是希望通过元数据来设置 permissions。

注意，rclone 会丢弃 Shared Drives 上的所有继承权限，以及 My Drives 上的所有 owner 权限，因为这些信息已在 owner 元数据中重复出现。


Properties:

- Config:      metadata_permissions
- Env Var:     RCLONE_DRIVE_METADATA_PERMISSIONS
- Type:        Bits
- Default:     off
- Examples:
  - "off"
    - Do not read or write the value
  - "read"
    - Read the value only
  - "write"
    - Write the value only
  - "failok"
    - If writing fails log errors only, don't fail the transfer
  - "read,write"
    - Read and Write the value.

#### --drive-metadata-labels

控制是否在元数据中读取或写入 labels。

从文件读取 labels 元数据需要额外的 API 事务，会减慢列出速度。并不总是希望通过元数据来设置 labels。

labels 的格式在 drive API 文档中说明，地址为 https://developers.google.com/drive/api/reference/rest/v3/Label —— rclone 只是提供该格式的 JSON dump。

设置 labels 时，label 和字段必须已经存在——rclone 不会创建它们。这意味着如果你要从两个不同账户间转移 labels，则必须预先创建这些 labels，并使用 metadata mapper 在两个账户间转换 ID。


Properties:

- Config:      metadata_labels
- Env Var:     RCLONE_DRIVE_METADATA_LABELS
- Type:        Bits
- Default:     off
- Examples:
  - "off"
    - Do not read or write the value
  - "read"
    - Read the value only
  - "write"
    - Write the value only
  - "failok"
    - If writing fails log errors only, don't fail the transfer
  - "read,write"
    - Read and Write the value.

#### --drive-metadata-enforce-expansive-access

请求是否应强制执行 expansive access 规则。

自 2026 年 2 月起，此标志将默认启用，因此该标志可以在此之前用于测试。

参见：https://developers.google.com/workspace/drive/api/guides/limited-expansive-access


Properties:

- Config:      metadata_enforce_expansive_access
- Env Var:     RCLONE_DRIVE_METADATA_ENFORCE_EXPANSIVE_ACCESS
- Type:        bool
- Default:     false

#### --drive-encoding

后端的编码方式。

更多信息请参见 [overview 中的 encoding 章节](/overview/#encoding)。

Properties:

- Config:      encoding
- Env Var:     RCLONE_DRIVE_ENCODING
- Type:        Encoding
- Default:     InvalidUtf8

#### --drive-env-auth

从运行时获取 IAM 凭据（环境变量，或在没有环境变量时从实例元数据获取）。

仅在 service_account_file 和 service_account_credentials 都为空时生效。

Properties:

- Config:      env_auth
- Env Var:     RCLONE_DRIVE_ENV_AUTH
- Type:        bool
- Default:     false
- Examples:
  - "false"
    - Enter credentials in the next step.
  - "true"
    - Get GCP IAM credentials from the environment (env vars or IAM).

#### --drive-description

远端的描述。

Properties:

- Config:      description
- Env Var:     RCLONE_DRIVE_DESCRIPTION
- Type:        string
- Required:    false

### Metadata

用户元数据存储在 drive 对象的 properties 字段中。

文件和目录都支持元数据。

以下是 drive 后端可能的系统元数据项。

| Name | Help | Type | Example | Read Only |
|------|------|------|---------|-----------|
| btime | Time of file birth (creation) with mS accuracy. Note that this is only writable on fresh uploads - it can't be written for updates. | RFC 3339 | 2006-01-02T15:04:05.999Z07:00 | N |
| content-type | The MIME type of the file. | string | text/plain | N |
| copy-requires-writer-permission | Whether the options to copy, print, or download this file, should be disabled for readers and commenters. | boolean | true | N |
| description | A short description of the file. | string | Contract for signing | N |
| folder-color-rgb | The color for a folder or a shortcut to a folder as an RGB hex string. | string | 881133 | N |
| labels | Labels attached to this file in a JSON dump of Googled drive format. Enable with --drive-metadata-labels. | JSON | [] | N |
| mtime | Time of last modification with mS accuracy. | RFC 3339 | 2006-01-02T15:04:05.999Z07:00 | N |
| owner | The owner of the file. Usually an email address. Enable with --drive-metadata-owner. | string | user@example.com | N |
| permissions | Permissions in a JSON dump of Google drive format. On shared drives these will only be present if they aren't inherited. Enable with --drive-metadata-permissions. | JSON | {} | N |
| starred | Whether the user has starred the file. | boolean | false | N |
| viewed-by-me | Whether the file has been viewed by this user. | boolean | true | **Y** |
| writers-can-share | Whether users with only writer permission can modify the file's permissions. Not populated and ignored when setting for items in shared drives. | boolean | false | N |

更多信息请参见 [metadata](/docs/#metadata) 文档。

## Backend commands

以下是 drive 后端特有的命令。

使用以下方式运行：

```console
rclone backend COMMAND remote:
```

下面的帮助将说明每个命令接受的参数。

关于如何传递选项和参数，请参见 [backend](/commands/rclone_backend/) 命令。

这些命令也可以在已运行的后端上使用 rc 命令 [backend/command](/rc/#backend-command) 执行。

### get

用于获取 drive 配置参数的 get 命令。

```console
rclone backend get remote: [options] [<arguments>+]
```

这是一个 get 命令，用于获取各种 drive 配置参数。

使用示例：

```console
rclone backend get drive: [-o service_account_file] [-o chunk_size]
rclone rc backend/command command=get fs=drive: [-o service_account_file] [-o chunk_size]
```

Options:

- "chunk_size": Show the current upload chunk size.
- "service_account_file": Show the current service account file.

### set

用于更新 drive 配置参数的 set 命令。

```console
rclone backend set remote: [options] [<arguments>+]
```

这是一个 set 命令，用于更新各种 drive 配置参数。

使用示例：

```console
rclone backend set drive: [-o service_account_file=sa.json] [-o chunk_size=67108864]
rclone rc backend/command command=set fs=drive: [-o service_account_file=sa.json] [-o chunk_size=67108864]
```

Options:

- "chunk_size": Update the current upload chunk size.
- "service_account_file": Update the current service account file.

### shortcut

从文件或目录创建快捷方式。

```console
rclone backend shortcut remote: [options] [<arguments>+]
```

此命令从文件或目录创建快捷方式。

使用示例：

```console
rclone backend shortcut drive: source_item destination_shortcut
rclone backend shortcut drive: source_item -o target=drive2: destination_shortcut
```

第一个示例从 "source_item"（可以是文件或目录）创建一个指向 "destination_shortcut" 的快捷方式。"source_item" 和 "destination_shortcut" 应为相对于 "drive:" 的路径。

第二个示例从相对于 "drive:" 的 "source_item" 创建一个指向相对于 "drive2:" 的 "destination_shortcut" 的快捷方式。如果通过 "drive2:" 认证的用户无法读取 "drive:" 中的文件，则可能因权限错误而失败。

Options:

- "target": Optional target remote for the shortcut destination.

### drives

列出该账户可用的 Shared Drives。

```console
rclone backend drives remote: [options] [<arguments>+]
```

此命令列出该账户可用的 Shared Drives（Team Drives）。

使用示例：

```console
rclone backend [-o config] drives drive:
```

这将返回一个 JSON 列表，形式如下：

```json
[
    {
        "id": "0ABCDEF-01234567890",
        "kind": "drive#teamDrive",
        "name": "My Drive"
    },
    {
        "id": "0ABCDEFabcdefghijkl",
        "kind": "drive#teamDrive",
        "name": "Test Drive"
    }
]
```

使用 -o config 参数时，会以适合直接添加到配置文件中以便为所有找到的 drive 创建别名以及一个合并 drive 的格式输出该列表。

```ini
[My Drive]
type = alias
remote = drive,team_drive=0ABCDEF-01234567890,root_folder_id=:

[Test Drive]
type = alias
remote = drive,team_drive=0ABCDEFabcdefghijkl,root_folder_id=:

[AllDrives]
type = combine
upstreams = "My Drive=My Drive:" "Test Drive=Test Drive:"
```

将其添加到 rclone 配置文件后，便可通过所示的别名访问这些 team drive。任何非法字符都会被替换为 "_"，重名的会追加编号。同时还会添加一个名为 AllDrives 的远端，将所有共享 drive 合并到同一棵目录树中显示。

### untrash

恢复文件和目录。

```console
rclone backend untrash remote: [options] [<arguments>+]
```

此命令会递归地恢复指定目录中所有已放入回收站的文件和目录。

使用示例：

```console
rclone backend untrash drive:directory
rclone backend --interactive untrash drive:directory subdir
```

它接受一个可选的目录参数，通过 API 使用时更方便。

可使用 --interactive/-i 或 --dry-run 标志预览将要恢复的内容。

结果：

```json
{
    "Untrashed": 17,
    "Errors": 0
}
```

### copyid

按 ID 复制文件。

```console
rclone backend copyid remote: [options] [<arguments>+]
```

此命令按 ID 复制文件。

使用示例：

```console
rclone backend copyid drive: ID path
rclone backend copyid drive: ID1 path1 ID2 path2
```

它将给定 ID 对应的 drive 文件复制到指定 path（一个 rclone 路径，将在内部传递给 rclone copyto）。ID 和 path 对可以重复指定。

path 应以 `/` 结尾，表示将文件按原名复制到该目录。如果不以 `/` 结尾，则最后一段路径将作为文件名。

如果目标是 drive 后端，则会尽可能尝试服务端复制。

可使用 --interactive/-i 或 --dry-run 标志预览将要复制的内容。

### moveid

按 ID 移动文件。

```console
rclone backend moveid remote: [options] [<arguments>+]
```

此命令按 ID 移动文件。

使用示例：

```console
rclone backend moveid drive: ID path
rclone backend moveid drive: ID1 path1 ID2 path2
```

它将给定 ID 对应的 drive 文件移动到指定 path（一个 rclone 路径，将在内部传递给 rclone moveto）。

path 应以 `/` 结尾，表示将文件按原名移动到该目录。如果不以 `/` 结尾，则最后一段路径将作为文件名。

如果目标是 drive 后端，则会尽可能尝试服务端移动。

可使用 --interactive/-i 或 --dry-run 标志预览将要移动的内容。

### exportformats

为调试目的输出导出格式。

```console
rclone backend exportformats remote: [options] [<arguments>+]
```

### importformats

为调试目的输出导入格式。

```console
rclone backend importformats remote: [options] [<arguments>+]
```

### query

使用 Google Drive 查询语言列出文件。

```console
rclone backend query remote: [options] [<arguments>+]
```

此命令基于查询条件列出文件。

使用示例：

```console
rclone backend query drive: query
```

查询语法请参见 [Google Drive Search query terms and operators](https://developers.google.com/drive/api/guides/ref-search-terms)。

例如：

```console
rclone backend query drive: "'0ABc9DEFGHIJKLMNop0QRatUVW3X' in parents and name contains 'foo'"
```

如果查询中包含字面量的 ' 或 \ 字符，需要使用 \ 进行转义。' 变为 \'，\ 变为 \\，例如要匹配名为 "foo ' \.txt" 的文件：

```console
rclone backend query drive: "name = 'foo \' \\\.txt'"
```

结果是 JSON 数组，例如：

```json
[
    {
        "createdTime": "2017-06-29T19:58:28.537Z",
        "id": "0AxBe_CDEF4zkGHI4d0FjYko2QkD",
        "md5Checksum": "68518d16be0c6fbfab918be61d658032",
        "mimeType": "text/plain",
        "modifiedTime": "2024-02-02T10:40:02.874Z",
        "name": "foo ' \\.txt",
        "parents": [
            "0BxAe_BCDE4zkFGZpcWJGek0xbzC"
        ],
        "resourceKey": "0-ABCDEFGHIXJQpIGqBJq3MC",
        "sha1Checksum": "8f284fa768bfb4e45d076a579ab3905ab6bfa893",
        "size": "311",
        "webViewLink": "https://drive.google.com/file/d/0AxBe_CDEF4zkGHI4d0FjYko2QkD/view?usp=drivesdk\u0026resourcekey=0-ABCDEFGHIXJQpIGqBJq3MC"
    }
]
```console

### rescue

恢复或删除孤立文件。

```console
rclone backend rescue remote: [options] [<arguments>+]
```

此命令恢复或删除孤立文件或目录。

有时文件会在 Google Drive 中变为孤立。这意味着它们不再属于 Google Drive 中的任何文件夹。

此命令会找到这些文件，并将其恢复到你指定的目录或将其删除。

此命令有 3 种用法。

首先，列出所有孤立文件：

```console
rclone backend rescue drive:
```

其次，将所有孤立文件恢复到指定目录：

```console
rclone backend rescue drive: "relative/path/to/rescue/directory"
```

例如，要将所有孤立文件恢复到顶层名为 "Orphans" 的目录：

```console
rclone backend rescue drive: Orphans
```

第三，将所有孤立文件删除到回收站：

```console
rclone backend rescue drive: -o delete
```

<!-- autogenerated options stop -->

## Limitations

Drive 存在大量速率限制。这导致 rclone 只能以每秒约 2 个文件的速率进行传输。单个文件的传输速度可能快得多，达到每秒数百 MiB，但大量小文件会需要很长时间。

服务端复制也受另一个单独的速率限制。如果你看到 User rate limit exceeded 错误，请至少等待 24 小时后重试。你也可以使用 `--disable copy` 禁用服务端复制，改用下载加上传的方式。

### Limitations of Google Docs

Google 文档在 `rclone ls`、`rclone ncdu` 等中显示为大小 -1，在任何使用 VFS 层的内容（例如 `rclone mount` 和 `rclone serve`）中显示为大小 0。在计算目录总和时（例如 `rclone size` 和 `rclone ncdu`），它们会被计为空文件。

这是因为 rclone 必须下载 Google 文档才能得知其大小。

Google 文档可以通过 `rclone sync`、`rclone copy` 等正确传输，因为 rclone 在传输时会忽略大小。

然而一个不幸的后果是，你可能无法通过 `rclone mount` 下载 Google 文档。如果不能正常工作，你将得到一个 0 大小的文件。如果重试，文档可能会获得正确的大小并变得可下载。能否工作取决于访问挂载的应用程序以及你运行的操作系统——请自行实验是否可行！

### Duplicated files

有时，由于我无法追查的原因，drive 会复制 rclone 上传的文件。与所有其他远端不同，drive 中可能会出现重复文件。

重复文件会导致 sync 出现问题，你会在日志中看到关于重复的消息。

可以使用 `rclone dedupe` 来修复重复文件。

注意这不仅是 rclone 的问题——即使是 Android 上的 Google Photos 也会偶尔在 drive 上复制文件。

### Rclone appears to be re-copying files it shouldn't

最可能的原因就是上面提到的重复文件问题——运行 `rclone dedupe` 并检查日志中是否有 duplicate object 或 duplicate directory 消息。

另一个可能原因是 google drive 端在进行目录列表比较时存在延迟/缓存。尤其是将 team drives 与 --fast-list 组合使用时，最近上传的文件可能不会出现在使用 --fast-list 时发送给 rclone 的目录列表中。

在尝试之间等待一段适度的时间（估计约 1 小时）和/或不使用 --fast-list 似乎都能有效防止该问题。

### SHA1 or SHA256 hashes may be missing

所有文件都有 MD5 哈希，但有一小部分上传的文件可能没有 SHA1 或 SHA256 哈希，尤其是 2018 年之前上传的文件。

## Making your own client_id

当你以默认配置使用 rclone 与 Google drive 配合时，你正在使用的是 rclone 的 client_id。该 ID 在所有 rclone 用户之间共享。Google 为每个 client_id 设置了每秒查询次数的全局速率限制。Rclone 本身已经拥有较高的配额，我会继续与 Google 沟通以确保其足够高。

强烈建议使用你自己的 client ID，因为默认的 rclone ID 已被大量使用。如果你运行着多个服务，建议为每个服务使用一个 API key。Google 的默认配额为每秒 10 个事务，因此建议保持在此数量之下——超过该值会导致 rclone 触发速率限制，从而使速度变慢。

以下是为 rclone 创建你自己的 Google Drive client ID 的方法：

1. 使用你的 Google 账户登录 [Google API Console](https://console.developers.google.com/)。使用哪个 Google 账户无关紧要（不必与希望访问的 Google Drive 是同一个账户）。

2. 选择一个 project，或新建一个 project。

3. 在 "ENABLE APIS AND SERVICES" 下搜索 "Drive"，并启用 "Google Drive API"。

4. 点击左侧面板中的 "Credentials"（注意不是 "Create credentials"，后者会打开向导）。

5. 如果你已经配置了 "Oauth Consent Screen"，请跳到下一步；如果没有，请点击 "CONFIGURE CONSENT SCREEN" 按钮（位于右侧面板右上角附近），然后点击 "Get started"。在下一屏中输入 "Application name"（填写 "rclone" 即可）；输入 "User Support Email"（填写你自己的邮箱即可）；下一步在 Audience 下选择 "External"。接下来输入你自己的联系信息，同意条款并点击 "Create"。此时你应该可以在屏幕左上角的方框中看到 rclone（或你的 project 名称）。

    （附注：如果你使用的是 GSuite 用户，也可以在上述步骤中选择 "Internal" 代替 "External"，但这会将 API 使用限制为你组织内的 Google Workspace 用户。）

    你还需要添加 [一些 scopes](https://developers.google.com/drive/api/guides/api-specific-auth)，包括
    - `https://www.googleapis.com/auth/docs`
    - `https://www.googleapis.com/auth/drive` 以便能够通过 RClone 编辑、创建和删除文件
    - `https://www.googleapis.com/auth/drive.metadata.readonly`，你可能也希望添加

    为此，请点击左侧面板的 Data Access，点击 "add or remove scopes" 并选择上述三个，然后按 update；或者转到 "Manually add scopes" 文本框（向下滚动）并输入
    "https://www.googleapis.com/auth/docs,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/drive.metadata.readonly"，按 add to table 然后 update。

    现在你应该在 Data access 页面看到这三个 scopes。最后点击底部的 save！

6. 添加 scopes 后，点击 Audience
向下滚动并点击 "+ Add users"。将自己添加为测试用户并点击 save。

7. 转到左侧面板的 Overview，点击 "Create OAuth client"。选择 "Desktop app" 作为 application type，然后点击 "Create"（使用默认名称即可）。

8. 它会显示一个 client ID 和 client secret。请记下它们。
   （如果在第 5 步选择了 "External"，请继续第 9 步。
   如果选择的是 "Internal"，则不需要发布，可以直接跳到第 10 步，但你的目标 drive 必须是同一个 Google Workspace 的一部分。）

9. 转到 "Audience"，然后点击 "PUBLISH APP" 按钮并确认。
   如果还没有将自己添加为测试用户，请添加。

10. 将记下的 client ID 和 client secret 提供给 rclone。

请注意，由于 Google 最近引入的 "enhanced security"（增强安全），理论上你应该 "submit your app for verification"（提交应用以供验证）并等待几周（！）才能收到他们的回复；但实际上，你可以直接使用 client ID 和 client secret 与 rclone 配合使用，唯一的问题是通过浏览器连接以使 rclone 获取其 token-id 时会显示一个非常吓人的确认界面（但这只在远端配置时发生，所以并不是什么大问题）。让 application 保持在 "Testing" 状态下也可以工作，但限制是任何授权都会在一周后过期，需要不断刷新，这会让人有些烦。如果出于任何原因，较短的授权时间不是问题，那么让 application 保持测试模式也足够了。

（感谢 github 上的 @balazer 提供这些说明。）

有时在 Google API Console 中创建 OAuth consent 会因错误消息 "The request failed because changes to one of the field of the resource is not supported" 而失败。作为一种便捷的替代方案，可以在 [Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python) 页面上创建所需的 Google Drive API key。只需点击 Enable the Drive API 按钮即可获取 Client ID 和 Secret。
注意该操作会在 API Console 中自动创建一个新 project。
