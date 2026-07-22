---
title: "Google Cloud Storage"
description: "rclone 的 Google Cloud Storage 文档"
versionIntroduced: "v1.02"
---

> **官方文档：** [https://rclone.org/googlecloudstorage/](https://rclone.org/googlecloudstorage/)
# Google Cloud Storage

路径指定为 `remote:bucket`（或 `lsd` 命令使用 `remote:`）。也可以包含子目录，例如 `remote:bucket/path/to/dir`。

## 配置

Google Cloud Storage 的初始设置需要从浏览器中获取令牌。`rclone config` 会引导你完成此过程。

以下是如何创建一个名为 `remote` 的远程存储的示例。首先运行：

```console
rclone config
```

这将引导你完成交互式设置过程：

```text
n) New remote
d) Delete remote
q) Quit config
e/n/d/q> n
name> remote
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / Google Cloud Storage (this is not Google Drive)
   \ "google cloud storage"
[snip]
Storage> google cloud storage
Google Application Client Id - leave blank normally.
client_id>
Google Application Client Secret - leave blank normally.
client_secret>
Project number optional - needed only for list/create/delete buckets - see your developer console.
project_number> 12345678
Service Account Credentials JSON file path - needed only if you want use SA instead of interactive login.
service_account_file>
Access Control List for new objects.
Choose a number from below, or type in your own value
 1 / Object owner gets OWNER access, and all Authenticated Users get READER access.
   \ "authenticatedRead"
 2 / Object owner gets OWNER access, and project team owners get OWNER access.
   \ "bucketOwnerFullControl"
 3 / Object owner gets OWNER access, and project team owners get READER access.
   \ "bucketOwnerRead"
 4 / Object owner gets OWNER access [default if left blank].
   \ "private"
 5 / Object owner gets OWNER access, and project team members get access according to their roles.
   \ "projectPrivate"
 6 / Object owner gets OWNER access, and all Users get READER access.
   \ "publicRead"
object_acl> 4
Access Control List for new buckets.
Choose a number from below, or type in your own value
 1 / Project team owners get OWNER access, and all Authenticated Users get READER access.
   \ "authenticatedRead"
 2 / Project team owners get OWNER access [default if left blank].
   \ "private"
 3 / Project team members get access according to their roles.
   \ "projectPrivate"
 4 / Project team owners get OWNER access, and all Users get READER access.
   \ "publicRead"
 5 / Project team owners get OWNER access, and all Users get WRITER access.
   \ "publicReadWrite"
bucket_acl> 2
Location for the newly created buckets.
Choose a number from below, or type in your own value
 1 / Empty for default location (US).
   \ ""
 2 / Multi-regional location for Asia.
   \ "asia"
 3 / Multi-regional location for Europe.
   \ "eu"
 4 / Multi-regional location for United States.
   \ "us"
 5 / Taiwan.
   \ "asia-east1"
 6 / Tokyo.
   \ "asia-northeast1"
 7 / Singapore.
   \ "asia-southeast1"
 8 / Sydney.
   \ "australia-southeast1"
 9 / Belgium.
   \ "europe-west1"
10 / London.
   \ "europe-west2"
11 / Iowa.
   \ "us-central1"
12 / South Carolina.
   \ "us-east1"
13 / Northern Virginia.
   \ "us-east4"
14 / Ohio.
   \ "us-east5"
15 / Oregon.
   \ "us-west1"
location> 12
The storage class to use when storing objects in Google Cloud Storage.
Choose a number from below, or type in your own value
 1 / Default
   \ ""
 2 / Multi-regional storage class
   \ "MULTI_REGIONAL"
 3 / Regional storage class
   \ "REGIONAL"
 4 / Nearline storage class
   \ "NEARLINE"
 5 / Coldline storage class
   \ "COLDLINE"
 6 / Durable reduced availability storage class
   \ "DURABLE_REDUCED_AVAILABILITY"
storage_class> 5
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
Configuration complete.
Options:
- type: google cloud storage
- client_id:
- client_secret:
- token: {"AccessToken":"xxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","RefreshToken":"x/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_xxxxxxxxx","Expiry":"2014-07-17T20:49:14.929208288+01:00","Extra":null}
- project_number: 12345678
- object_acl: private
- bucket_acl: private
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

关于如何在没有互联网连接的浏览器的机器上进行设置，请参阅[远程设置文档](/remote_setup/)。

请注意，如果使用浏览器自动认证，rclone 会在本地机器上运行一个 Web 服务器来收集从 Google 返回的令牌。该服务器仅在打开浏览器到获取验证码期间运行，监听地址为 `http://127.0.0.1:53682/`。如果你运行了主机防火墙，可能需要临时解除阻止，或使用手动模式。

此远程存储名为 `remote`，现在可以如下使用

查看项目中的所有存储桶

```console
rclone lsd remote:
```

创建新存储桶

```console
rclone mkdir remote:bucket
```

列出存储桶内容

```console
rclone ls remote:bucket
```

将 `/home/local/directory` 同步到远程存储桶，删除存储桶中多余的文件。

```console
rclone sync --interactive /home/local/directory remote:bucket
```

### 服务账号支持

你可以在无人值守模式下使用 rclone 配置 Google Cloud Storage，即不绑定到特定终端用户的 Google 账号。这在你想要将文件同步到没有活跃登录用户的机器上时非常有用，例如构建机器。

要获取 Google Cloud Platform [IAM 服务账号](https://cloud.google.com/iam/docs/service-accounts)的凭据，请前往 Google 开发者控制台的[服务账号](https://console.cloud.google.com/permissions/serviceaccounts)部分。服务账号在 [Google Cloud Storage ACL](https://cloud.google.com/storage/docs/access-control) 中的行为与普通 `User` 权限相同，因此你可以限制其访问权限（例如设为只读）。创建账号后，包含服务账号凭据的 JSON 文件将被下载到你的机器上。这些凭据就是 rclone 用于认证的内容。

要使用服务账号而非 OAuth2 令牌流程，请在 `service_account_file` 提示处输入服务账号凭据的路径，rclone 将不会使用基于浏览器的认证流程。如果你更希望将凭据文件的内容直接放入 rclone 配置文件中，可以设置 `service_account_credentials` 为文件的实际内容，或设置等效的环境变量。

### 使用访问令牌的服务账号认证

服务账号认证的另一种选择是通过 *gcloud impersonate-service-account* 使用访问令牌。访问令牌通过避免使用可能被泄露的 JSON 密钥文件来保护安全。它们还绕过了 OAuth 登录流程，对于缺少 Web 浏览器的远程虚拟机来说更简单。

如果你已经有一个可用的服务账号，请跳到第 3 步。

#### 1. 使用以下命令创建服务账号

```console
gcloud iam service-accounts create gcs-read-only
```

你也可以复用现有的服务账号（如上面创建的那个）

#### 2. 为服务账号附加 Viewer（只读）或 User（读写）角色

```console
$ PROJECT_ID=my-project
$ gcloud --verbose iam service-accounts add-iam-policy-binding \
   gcs-read-only@${PROJECT_ID}.iam.gserviceaccount.com  \
   --member=serviceAccount:gcs-read-only@${PROJECT_ID}.iam.gserviceaccount.com \
   --role=roles/storage.objectViewer
```

使用 Google Cloud 控制台确定受限角色。一些相关的预定义角色：

- *roles/storage.objectUser* -- 读写访问但没有管理员权限
- *roles/storage.objectViewer* -- 对象的只读访问
- *roles/storage.admin*  -- 创建存储桶和管理员角色

#### 3. 获取服务账号的临时访问密钥

```console
$ gcloud auth application-default print-access-token  \
   --impersonate-service-account \
      gcs-read-only@${PROJECT_ID}.iam.gserviceaccount.com

ya29.c.c0ASRK0GbAFEewXD [truncated]
```

#### 4. 更新 `access_token` 设置

当你看到 *waiting for code* 时按 `CTRL-C`。这将保存配置而不执行 OAuth 流程

```console
rclone config update ${REMOTE_NAME} access_token ya29.c.c0Axxxx
```

#### 5. 像往常一样运行 rclone

```console
rclone ls dev-gcs:${MY_BUCKET}/
```

### 服务账号更多信息

- [GCS 官方文档](https://cloud.google.com/compute/docs/access/service-accounts)
- [使用密钥文件的服务账号指南（安全性较低，但概念类似）](https://forum.rclone.org/t/access-using-google-service-account/24822/2)

### 匿名访问

对于允许公开访问的对象下载，你可以通过将 `anonymous` 设为 `true` 来配置 rclone 使用匿名访问。使用未授权访问时，你无法写入或创建文件，只能读取或列出具有公开读取访问权限的存储桶和对象。

### 应用默认凭据

如果未提供其他凭据来源，rclone 将回退到[应用默认凭据](https://cloud.google.com/video-intelligence/docs/common/auth#authenticating_with_application_default_credentials)，这在以下情况很有用：你已经为开发者账号配置了认证，或在生产环境中运行于 Google 计算主机上。注意，如果在 Docker 中运行，你可能需要在 Google 计算机器上运行额外命令 — [参见此页面](https://cloud.google.com/container-registry/docs/advanced-authentication#gcloud_as_a_docker_credential_helper)。

注意，在使用应用默认凭据的情况下，无需显式配置项目编号。

### --fast-list

此远程存储支持 `--fast-list`，允许你以更多内存为代价减少事务数。详见 [rclone 文档](/docs/#fast-list)。

### 自定义上传头

你可以使用 `--header-upload` 标志设置自定义上传头。Google Cloud Storage 支持的请求头如[元数据操作文档](https://cloud.google.com/storage/docs/gsutil/addlhelp/WorkingWithObjectMetadata)所述：

- Cache-Control
- Content-Disposition
- Content-Encoding
- Content-Language
- Content-Type
- X-Goog-Storage-Class
- X-Goog-Meta-

例如 `--header-upload "Content-Type text/potato"`

注意最后一个用于设置自定义元数据，格式为 `--header-upload "x-goog-meta-key: value"`

### 修改时间

Google Cloud Storage 原生存储 md5sum。Google 的 [gsutil](https://cloud.google.com/storage/docs/gsutil) 工具以秒级精度将修改时间存储为文件元数据中的 `goog-reserved-file-mtime`。

为确保与 gsutil 兼容，rclone 将修改时间存储在 2 个独立的元数据条目中。`mtime` 使用 RFC3339 格式，精度为纳秒级。`goog-reserved-file-mtime` 使用 Unix 时间戳格式，精度为秒级。rclone 按以下顺序从对象元数据读取修改时间：`mtime`、`goog-reserved-file-mtime`、对象更新时间。

注意 rclone 的默认修改窗口为 1ns。由 gsutil 上传的文件仅包含秒级精度的时间戳。如果你使用 rclone 同步之前由 gsutil 上传的文件，rclone 会尝试更新所有这些文件的修改时间。要避免这些可能不必要的更新，请使用 `--modify-window 1s`。

### 受限文件名字符

| 字符 | 值 | 替换为 |
| ---- |:---:|:-----:|
| NUL  | 0x00 | ␀    |
| LF   | 0x0A | ␊    |
| CR   | 0x0D | ␍    |
| /    | 0x2F | ／   |

无效的 UTF-8 字节也会被[替换](/overview/#invalid-utf8)，因为它们无法用于 JSON 字符串中。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/googlecloudstorage/googlecloudstorage.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 google cloud storage（Google Cloud Storage，非 Google Drive）特有的标准选项。

#### --gcs-client-id

OAuth 客户端 ID。

通常留空。

Properties:

- Config:      client_id
- Env Var:     RCLONE_GCS_CLIENT_ID
- Type:        string
- Required:    false

#### --gcs-client-secret

OAuth 客户端密钥。

通常留空。

Properties:

- Config:      client_secret
- Env Var:     RCLONE_GCS_CLIENT_SECRET
- Type:        string
- Required:    false

#### --gcs-project-number

项目编号。

可选 — 仅在列出/创建/删除存储桶时需要 — 参见开发者控制台。

Properties:

- Config:      project_number
- Env Var:     RCLONE_GCS_PROJECT_NUMBER
- Type:        string
- Required:    false

#### --gcs-user-project

用户项目。

可选 — 仅在请求者付费时需要。

Properties:

- Config:      user_project
- Env Var:     RCLONE_GCS_USER_PROJECT
- Type:        string
- Required:    false

#### --gcs-service-account-file

服务账号凭据 JSON 文件路径。

通常留空。
仅在你想使用服务账号而非交互式登录时需要。

文件名中的前导 `~` 会被展开，`${RCLONE_CONFIG_DIR}` 等环境变量也会被展开。

Properties:

- Config:      service_account_file
- Env Var:     RCLONE_GCS_SERVICE_ACCOUNT_FILE
- Type:        string
- Required:    false

#### --gcs-service-account-credentials

服务账号凭据 JSON 内容。

通常留空。
仅在你想使用服务账号而非交互式登录时需要。

Properties:

- Config:      service_account_credentials
- Env Var:     RCLONE_GCS_SERVICE_ACCOUNT_CREDENTIALS
- Type:        string
- Required:    false

#### --gcs-anonymous

无需凭据访问公开存储桶和对象。

如果你只想下载文件且不配置凭据，设为 'true'。

Properties:

- Config:      anonymous
- Env Var:     RCLONE_GCS_ANONYMOUS
- Type:        bool
- Default:     false

#### --gcs-object-acl

新对象的访问控制列表。

Properties:

- Config:      object_acl
- Env Var:     RCLONE_GCS_OBJECT_ACL
- Type:        string
- Required:    false
- Examples:
  - "authenticatedRead"
    - 对象所有者获得 OWNER 访问权限。
    - 所有已认证用户获得 READER 访问权限。
  - "bucketOwnerFullControl"
    - 对象所有者获得 OWNER 访问权限。
    - 项目团队所有者获得 OWNER 访问权限。
  - "bucketOwnerRead"
    - 对象所有者获得 OWNER 访问权限。
    - 项目团队所有者获得 READER 访问权限。
  - "private"
    - 对象所有者获得 OWNER 访问权限。
    - 留空时的默认值。
  - "projectPrivate"
    - 对象所有者获得 OWNER 访问权限。
    - 项目团队成员根据各自角色获得访问权限。
  - "publicRead"
    - 对象所有者获得 OWNER 访问权限。
    - 所有用户获得 READER 访问权限。

#### --gcs-bucket-acl

新存储桶的访问控制列表。

Properties:

- Config:      bucket_acl
- Env Var:     RCLONE_GCS_BUCKET_ACL
- Type:        string
- Required:    false
- Examples:
  - "authenticatedRead"
    - 项目团队所有者获得 OWNER 访问权限。
    - 所有已认证用户获得 READER 访问权限。
  - "private"
    - 项目团队所有者获得 OWNER 访问权限。
    - 留空时的默认值。
  - "projectPrivate"
    - 项目团队成员根据各自角色获得访问权限。
  - "publicRead"
    - 项目团队所有者获得 OWNER 访问权限。
    - 所有用户获得 READER 访问权限。
  - "publicReadWrite"
    - 项目团队所有者获得 OWNER 访问权限。
    - 所有用户获得 WRITER 访问权限。

#### --gcs-bucket-policy-only

访问检查应使用存储桶级 IAM 策略。

如果你要上传对象到启用了 Bucket Policy Only 的存储桶，则需要设置此项。

设置后，rclone 会：

- 忽略存储桶上设置的 ACL
- 忽略对象上设置的 ACL
- 创建启用了 Bucket Policy Only 的存储桶

文档：https://cloud.google.com/storage/docs/bucket-policy-only


Properties:

- Config:      bucket_policy_only
- Env Var:     RCLONE_GCS_BUCKET_POLICY_ONLY
- Type:        bool
- Default:     false

#### --gcs-location

新创建存储桶的位置。

Properties:

- Config:      location
- Env Var:     RCLONE_GCS_LOCATION
- Type:        string
- Required:    false
- Examples:
  - ""
    - 留空为默认位置 (US)
  - "asia"
    - 亚洲多区域位置
  - "eu"
    - 欧洲多区域位置
  - "us"
    - 美国多区域位置
  - "asia-east1"
    - 台湾
  - "asia-east2"
    - 香港
  - "asia-northeast1"
    - 东京
  - "asia-northeast2"
    - 大阪
  - "asia-northeast3"
    - 首尔
  - "asia-south1"
    - 孟买
  - "asia-south2"
    - 德里
  - "asia-southeast1"
    - 新加坡
  - "asia-southeast2"
    - 雅加达
  - "australia-southeast1"
    - 悉尼
  - "australia-southeast2"
    - 墨尔本
  - "europe-north1"
    - 芬兰
  - "europe-west1"
    - 比利时
  - "europe-west2"
    - 伦敦
  - "europe-west3"
    - 法兰克福
  - "europe-west4"
    - 荷兰
  - "europe-west6"
    - 苏黎世
  - "europe-central2"
    - 华沙
  - "us-central1"
    - 爱荷华
  - "us-east1"
    - 南卡罗来纳
  - "us-east4"
    - 北弗吉尼亚
  - "us-east5"
    - 俄亥俄
  - "us-west1"
    - 俄勒冈
  - "us-west2"
    - 加利福尼亚
  - "us-west3"
    - 盐湖城
  - "us-west4"
    - 拉斯维加斯
  - "northamerica-northeast1"
    - 蒙特利尔
  - "northamerica-northeast2"
    - 多伦多
  - "southamerica-east1"
    - 圣保罗
  - "southamerica-west1"
    - 圣地亚哥
  - "asia1"
    - 双区域：asia-northeast1 和 asia-northeast2。
  - "eur4"
    - 双区域：europe-north1 和 europe-west4。
  - "nam4"
    - 双区域：us-central1 和 us-east1。

#### --gcs-storage-class

在 Google Cloud Storage 中存储对象时使用的存储类别。

Properties:

- Config:      storage_class
- Env Var:     RCLONE_GCS_STORAGE_CLASS
- Type:        string
- Required:    false
- Examples:
  - ""
    - 默认
  - "MULTI_REGIONAL"
    - 多区域存储类别
  - "REGIONAL"
    - 区域存储类别
  - "NEARLINE"
    - 近线存储类别
  - "COLDLINE"
    - 冷线存储类别
  - "ARCHIVE"
    - 归档存储类别
  - "DURABLE_REDUCED_AVAILABILITY"
    - 持久低可用性存储类别

#### --gcs-env-auth

从运行时获取 GCP IAM 凭据（环境变量或实例元数据，若无环境变量）。

仅在 service_account_file 和 service_account_credentials 为空时适用。

Properties:

- Config:      env_auth
- Env Var:     RCLONE_GCS_ENV_AUTH
- Type:        bool
- Default:     false
- Examples:
  - "false"
    - 在下一步中输入凭据。
  - "true"
    - 从环境（环境变量或 IAM）获取 GCP IAM 凭据。

### 高级选项

以下是 google cloud storage（Google Cloud Storage，非 Google Drive）特有的高级选项。

#### --gcs-token

OAuth 访问令牌（JSON 格式）。

Properties:

- Config:      token
- Env Var:     RCLONE_GCS_TOKEN
- Type:        string
- Required:    false

#### --gcs-auth-url

认证服务器 URL。

留空以使用提供商默认值。

Properties:

- Config:      auth_url
- Env Var:     RCLONE_GCS_AUTH_URL
- Type:        string
- Required:    false

#### --gcs-token-url

令牌服务器 URL。

留空以使用提供商默认值。

Properties:

- Config:      token_url
- Env Var:     RCLONE_GCS_TOKEN_URL
- Type:        string
- Required:    false

#### --gcs-client-credentials

使用客户端凭据 OAuth 流程。

这将使用 RFC 6749 中描述的 OAUTH2 客户端凭据流程。

注意并非所有后端都支持此选项。

Properties:

- Config:      client_credentials
- Env Var:     RCLONE_GCS_CLIENT_CREDENTIALS
- Type:        bool
- Default:     false

#### --gcs-access-token

短期访问令牌。

通常留空。
仅在你想使用短期访问令牌而非交互式登录时需要。

Properties:

- Config:      access_token
- Env Var:     RCLONE_GCS_ACCESS_TOKEN
- Type:        string
- Required:    false

#### --gcs-directory-markers

创建新目录时上传一个带尾部斜杠的空对象

基于存储桶的远程存储不支持空文件夹，此选项创建一个以 "/" 结尾的空对象来持久化该文件夹。


Properties:

- Config:      directory_markers
- Env Var:     RCLONE_GCS_DIRECTORY_MARKERS
- Type:        bool
- Default:     false

#### --gcs-no-check-bucket

如果设置，不尝试检查存储桶是否存在或创建它。

当你知道存储桶已经存在时，这有助于减少 rclone 执行的事务数量。


Properties:

- Config:      no_check_bucket
- Env Var:     RCLONE_GCS_NO_CHECK_BUCKET
- Type:        bool
- Default:     false

#### --gcs-decompress

如果设置，将解压缩 gzip 编码的对象。

可以将对象上传到 GCS 并设置 "Content-Encoding: gzip"。通常 rclone 会将这些文件作为压缩对象下载。

如果设置了此标志，rclone 将在接收时解压缩这些设置了 "Content-Encoding: gzip" 的文件。这意味着 rclone 无法检查大小和哈希，但文件内容将被解压缩。


Properties:

- Config:      decompress
- Env Var:     RCLONE_GCS_DECOMPRESS
- Type:        bool
- Default:     false

#### --gcs-endpoint

存储 API 的自定义端点。留空以使用提供商默认值。

当使用包含子路径的自定义端点（例如 example.org/custom/endpoint）时，由于底层 Google API Go 客户端库的限制，上传操作将忽略子路径。
下载和列出操作可以正确使用完整端点路径。
如果你需要上传操作支持子路径，请避免在自定义端点配置中使用子路径。

Properties:

- Config:      endpoint
- Env Var:     RCLONE_GCS_ENDPOINT
- Type:        string
- Required:    false
- Examples:
  - "storage.example.org"
    - 指定自定义端点
  - "storage.example.org:4443"
    - 指定带端口的自定义端点
  - "storage.example.org:4443/gcs/api"
    - 指定子路径，参见注意事项，上传不会使用自定义路径！

#### --gcs-encoding

后端的编码方式。

详见[概述中的编码部分](/overview/#encoding)。

Properties:

- Config:      encoding
- Env Var:     RCLONE_GCS_ENCODING
- Type:        Encoding
- Default:     Slash,CrLf,InvalidUtf8,Dot

#### --gcs-description

远程存储的描述。

Properties:

- Config:      description
- Env Var:     RCLONE_GCS_DESCRIPTION
- Type:        string
- Required:    false

<!-- autogenerated options stop -->

## 限制

Google Cloud Storage 后端不支持 `rclone about`。不支持此功能的后端无法为 rclone mount 确定可用空间，也无法在 rclone union 远程存储中作为 `mfs`（最大可用空间）策略的成员使用。

参见[不支持 rclone about 的后端列表](https://rclone.org/overview/#optional-features)和[rclone about](https://rclone.org/commands/rclone_about/)。
