---
title: "Swift"
description: "OpenStack Swift 对象存储（Rackspace Cloud Files、Blomp Cloud Storage、Memset Memstore、OVH）后端配置与使用"
versionIntroduced: "v0.91"
---

> **官方文档：** [https://rclone.org/swift/](https://rclone.org/swift/)
# Swift

Swift 指的是 [OpenStack Object Storage](https://docs.openstack.org/swift/latest/)。
其商业实现包括：

- [Rackspace Cloud Files](https://www.rackspace.com/cloud/files/)
- [Memset Memstore](https://www.memset.com/cloud/storage/)
- [OVH Object Storage](https://www.ovhcloud.com/en/public-cloud/object-storage/)
- [Oracle Cloud Storage](https://docs.oracle.com/en-us/iaas/integration/doc/configure-object-storage.html)
- [Blomp Cloud Storage](https://www.blomp.com/cloud-storage/)
- [IBM Bluemix Cloud ObjectStorage Swift](https://console.bluemix.net/docs/infrastructure/objectstorage-swift/index.html)

路径指定为 `remote:container`（或 `lsd` 命令使用 `remote:`）。
也可以包含子目录，例如 `remote:container/path/to/dir`。

## 配置

以下是创建 swift 配置的示例。首先运行

```console
rclone config
```

这将引导你完成交互式设置过程。

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
XX / OpenStack Swift (Rackspace Cloud Files, Blomp Cloud Storage, Memset Memstore, OVH)
   \ "swift"
[snip]
Storage> swift
Get swift credentials from environment variables in standard OpenStack form.
Choose a number from below, or type in your own value
 1 / Enter swift credentials in the next step
   \ "false"
 2 / Get swift credentials from environment vars. Leave other fields blank if using this.
   \ "true"
env_auth> true
User name to log in (OS_USERNAME).
user>
API key or password (OS_PASSWORD).
key>
Authentication URL for server (OS_AUTH_URL).
Choose a number from below, or type in your own value
 1 / Rackspace US
   \ "https://auth.api.rackspacecloud.com/v1.0"
 2 / Rackspace UK
   \ "https://lon.auth.api.rackspacecloud.com/v1.0"
 3 / Rackspace v2
   \ "https://identity.api.rackspacecloud.com/v2.0"
 4 / Memset Memstore UK
   \ "https://auth.storage.memset.com/v1.0"
 5 / Memset Memstore UK v2
   \ "https://auth.storage.memset.com/v2.0"
 6 / OVH
   \ "https://auth.cloud.ovh.net/v3"
 7  / Blomp Cloud Storage
   \ "https://authenticate.ain.net"
auth>
User ID to log in - optional - most swift systems use user and leave this blank (v3 auth) (OS_USER_ID).
user_id>
User domain - optional (v3 auth) (OS_USER_DOMAIN_NAME)
domain>
Tenant name - optional for v1 auth, this or tenant_id required otherwise (OS_TENANT_NAME or OS_PROJECT_NAME)
tenant>
Tenant ID - optional for v1 auth, this or tenant required otherwise (OS_TENANT_ID)
tenant_id>
Tenant domain - optional (v3 auth) (OS_PROJECT_DOMAIN_NAME)
tenant_domain>
Region name - optional (OS_REGION_NAME)
region>
Storage URL - optional (OS_STORAGE_URL)
storage_url>
Auth Token from alternate authentication - optional (OS_AUTH_TOKEN)
auth_token>
AuthVersion - optional - set to (1,2,3) if your auth URL has no version (ST_AUTH_VERSION)
auth_version>
Endpoint type to choose from the service catalogue (OS_ENDPOINT_TYPE)
Choose a number from below, or type in your own value
 1 / Public (default, choose this if not sure)
   \ "public"
 2 / Internal (use internal service net)
   \ "internal"
 3 / Admin
   \ "admin"
endpoint_type>
Remote config
--------------------
[test]
env_auth = true
user =
key =
auth =
user_id =
domain =
tenant =
tenant_id =
tenant_domain =
region =
storage_url =
auth_token =
auth_version =
endpoint_type =
--------------------
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

此远程存储称为 `remote`，现在可以这样使用

查看所有容器

```console
rclone lsd remote:
```

创建新容器

```console
rclone mkdir remote:container
```

列出容器内容

```console
rclone ls remote:container
```

将 `/home/local/directory` 同步到远程容器，删除容器中多余的文件。

```console
rclone sync --interactive /home/local/directory remote:container
```

### 从 OpenStack 凭据文件配置

OpenStack 凭据文件通常类似于以下内容（不含注释）

```sh
export OS_AUTH_URL=https://a.provider.net/v2.0
export OS_TENANT_ID=ffffffffffffffffffffffffffffffff
export OS_TENANT_NAME="1234567890123456"
export OS_USERNAME="123abc567xy"
echo "Please enter your OpenStack Password: "
read -sr OS_PASSWORD_INPUT
export OS_PASSWORD=$OS_PASSWORD_INPUT
export OS_REGION_NAME="SBG1"
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi
```

配置文件需要类似于以下内容，其中 `$OS_USERNAME` 表示 `OS_USERNAME` 变量的值——在上例中为 `123abc567xy`。

```ini
[remote]
type = swift
user = $OS_USERNAME
key = $OS_PASSWORD
auth = $OS_AUTH_URL
tenant = $OS_TENANT_NAME
```

注意你可能（也可能不需要）设置 `region`——先不设置试试。

### 从环境变量配置

如果你愿意，可以让 rclone 使用标准的 OpenStack 环境变量来配置 swift。

在运行配置时，确保为 `env_auth` 选择 `true`，其他所有字段留空。

rclone 随后将使用标准 OpenStack 环境变量来设置任何空配置参数。swift 库文档中有[环境变量列表](https://godoc.org/github.com/ncw/swift#Connection.ApplyEnvironment)。

### 使用备用认证方法

如果你的 OpenStack 安装使用了 rclone 或底层 swift 库可能尚未支持的非标准认证方法，你可以从外部认证（例如手动调用 `openstack` 命令获取令牌）。然后，只需传递 ``auth_token`` 和 ``storage_url`` 两个配置变量。
如果两者都提供了，其他变量将被忽略。rclone 不会尝试认证，而是假定已经认证，并使用这两个变量访问 OpenStack 安装。

#### 不使用配置文件运行 rclone

如果需要，可以不使用配置文件运行 rclone 的 swift 后端，如下所示：

```sh
source openstack-credentials-file
export RCLONE_CONFIG_MYREMOTE_TYPE=swift
export RCLONE_CONFIG_MYREMOTE_ENV_AUTH=true
rclone lsd myremote:
```

### --fast-list

此远程存储支持 `--fast-list`，允许以更多内存换取更少的事务数。详见 [rclone 文档](/docs/#fast-list)。

### --update 和 --use-server-modtime

如下所述，修改时间存储在对象的元数据中。默认情况下，所有需要检查文件最后更新时间的操作都会使用它。这让 rclone 能将远程存储当作真正的文件系统来处理，但效率较低，因为需要额外的 API 调用来获取元数据。

对于许多操作来说，对象最后上传到远程存储的时间足以判断它是否"脏"了。通过使用 `--update` 加上 `--use-server-modtime`，可以避免额外的 API 调用，只上传本地修改时间晚于最后上传时间的文件。

### 修改时间和哈希

修改时间作为元数据存储在对象上，键为 `X-Object-Meta-Mtime`，值为自纪元以来的浮点数，精度为 1 纳秒。

这是事实上的标准（官方 python-swiftclient 等也使用），用于存储对象的修改时间。

支持 MD5 哈希算法。

### 受限文件名字符

| 字符 | 值 | 替换字符 |
| ---- |:---:|:--------:|
| NUL  | 0x00 | ␀       |
| /    | 0x2F | ／      |

无效的 UTF-8 字节也将被[替换](/overview/#invalid-utf8)，因为它们无法用于 JSON 字符串中。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/swift/swift.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 swift（OpenStack Swift (Rackspace Cloud Files, Blomp Cloud Storage, Memset Memstore, OVH)）特有的标准选项。

#### --swift-env-auth

从标准 OpenStack 格式的环境变量获取 swift 凭据。

Properties:

- Config:      env_auth
- Env Var:     RCLONE_SWIFT_ENV_AUTH
- Type:        bool
- Default:     false
- Examples:
  - "false"
    - 在下一步中输入 swift 凭据。
  - "true"
    - 从环境变量获取 swift 凭据。
    - 使用此选项时，其他字段留空。

#### --swift-user

登录用户名（OS_USERNAME）。

Properties:

- Config:      user
- Env Var:     RCLONE_SWIFT_USER
- Type:        string
- Required:    false

#### --swift-key

API 密钥或密码（OS_PASSWORD）。

Properties:

- Config:      key
- Env Var:     RCLONE_SWIFT_KEY
- Type:        string
- Required:    false

#### --swift-auth

服务器认证 URL（OS_AUTH_URL）。

Properties:

- Config:      auth
- Env Var:     RCLONE_SWIFT_AUTH
- Type:        string
- Required:    false
- Examples:
  - "https://auth.api.rackspacecloud.com/v1.0"
    - Rackspace US
  - "https://lon.auth.api.rackspacecloud.com/v1.0"
    - Rackspace UK
  - "https://identity.api.rackspacecloud.com/v2.0"
    - Rackspace v2
  - "https://auth.storage.memset.com/v1.0"
    - Memset Memstore UK
  - "https://auth.storage.memset.com/v2.0"
    - Memset Memstore UK v2
  - "https://auth.cloud.ovh.net/v3"
    - OVH
  - "https://authenticate.ain.net"
    - Blomp Cloud Storage

#### --swift-user-id

登录用户 ID - 可选 - 大多数 swift 系统使用 user 并将此留空（v3 认证）（OS_USER_ID）。

Properties:

- Config:      user_id
- Env Var:     RCLONE_SWIFT_USER_ID
- Type:        string
- Required:    false

#### --swift-domain

用户域 - 可选（v3 认证）（OS_USER_DOMAIN_NAME）

Properties:

- Config:      domain
- Env Var:     RCLONE_SWIFT_DOMAIN
- Type:        string
- Required:    false

#### --swift-tenant

租户名称 - v1 认证时可选，其他情况下此字段或 tenant_id 为必填（OS_TENANT_NAME 或 OS_PROJECT_NAME）。

Properties:

- Config:      tenant
- Env Var:     RCLONE_SWIFT_TENANT
- Type:        string
- Required:    false

#### --swift-tenant-id

租户 ID - v1 认证时可选，其他情况下此字段或 tenant 为必填（OS_TENANT_ID）。

Properties:

- Config:      tenant_id
- Env Var:     RCLONE_SWIFT_TENANT_ID
- Type:        string
- Required:    false

#### --swift-tenant-domain

租户域 - 可选（v3 认证）（OS_PROJECT_DOMAIN_NAME）。

Properties:

- Config:      tenant_domain
- Env Var:     RCLONE_SWIFT_TENANT_DOMAIN
- Type:        string
- Required:    false

#### --swift-region

区域名称 - 可选（OS_REGION_NAME）。

Properties:

- Config:      region
- Env Var:     RCLONE_SWIFT_REGION
- Type:        string
- Required:    false

#### --swift-storage-url

存储 URL - 可选（OS_STORAGE_URL）。

Properties:

- Config:      storage_url
- Env Var:     RCLONE_SWIFT_STORAGE_URL
- Type:        string
- Required:    false

#### --swift-auth-token

备用认证的认证令牌 - 可选（OS_AUTH_TOKEN）。

Properties:

- Config:      auth_token
- Env Var:     RCLONE_SWIFT_AUTH_TOKEN
- Type:        string
- Required:    false

#### --swift-application-credential-id

应用凭据 ID（OS_APPLICATION_CREDENTIAL_ID）。

Properties:

- Config:      application_credential_id
- Env Var:     RCLONE_SWIFT_APPLICATION_CREDENTIAL_ID
- Type:        string
- Required:    false

#### --swift-application-credential-name

应用凭据名称（OS_APPLICATION_CREDENTIAL_NAME）。

Properties:

- Config:      application_credential_name
- Env Var:     RCLONE_SWIFT_APPLICATION_CREDENTIAL_NAME
- Type:        string
- Required:    false

#### --swift-application-credential-secret

应用凭据密钥（OS_APPLICATION_CREDENTIAL_SECRET）。

Properties:

- Config:      application_credential_secret
- Env Var:     RCLONE_SWIFT_APPLICATION_CREDENTIAL_SECRET
- Type:        string
- Required:    false

#### --swift-auth-version

认证版本 - 可选 - 如果认证 URL 不含版本，则设为 (1,2,3)（ST_AUTH_VERSION）。

Properties:

- Config:      auth_version
- Env Var:     RCLONE_SWIFT_AUTH_VERSION
- Type:        int
- Default:     0

#### --swift-endpoint-type

从服务目录中选择的端点类型（OS_ENDPOINT_TYPE）。

Properties:

- Config:      endpoint_type
- Env Var:     RCLONE_SWIFT_ENDPOINT_TYPE
- Type:        string
- Default:     "public"
- Examples:
  - "public"
    - 公共（默认，不确定时选此项）
  - "internal"
    - 内部（使用内部服务网络）
  - "admin"
    - 管理员

#### --swift-storage-policy

创建新容器时使用的存储策略。

在创建新容器时应用指定的存储策略。策略创建后无法更改。允许的配置值及其含义取决于你的 Swift 存储提供商。

Properties:

- Config:      storage_policy
- Env Var:     RCLONE_SWIFT_STORAGE_POLICY
- Type:        string
- Required:    false
- Examples:
  - ""
    - 默认
  - "pcs"
    - OVH 公有云存储
  - "pca"
    - OVH 公有云归档

### 高级选项

以下是 swift（OpenStack Swift (Rackspace Cloud Files, Blomp Cloud Storage, Memset Memstore, OVH)）特有的高级选项。

#### --swift-leave-parts-on-error

如果为 true，则在失败时不调用中止上传。

应设为 true 以便在不同会话之间恢复上传。

Properties:

- Config:      leave_parts_on_error
- Env Var:     RCLONE_SWIFT_LEAVE_PARTS_ON_ERROR
- Type:        bool
- Default:     false

#### --swift-fetch-until-empty-page

分页时，始终获取直到收到空页为止。

如果 rclone 列表显示的对象数量少于预期，或者重复同步时复制了未更改的对象，请考虑使用此选项。

启用此项是安全的，但 rclone 可能会进行比必要更多的 API 调用。

这是处理 Swift API 实现中分页行为异常的一对解决方案之一。另见 "partial_page_fetch_threshold"。

Properties:

- Config:      fetch_until_empty_page
- Env Var:     RCLONE_SWIFT_FETCH_UNTIL_EMPTY_PAGE
- Type:        bool
- Default:     false

#### --swift-partial-page-fetch-threshold

分页时，如果当前页数在限制的此百分比范围内，则继续获取。

如果 rclone 列表显示的对象数量少于预期，或者重复同步时复制了未更改的对象，请考虑使用此选项。

启用此项是安全的，但 rclone 可能会进行比必要更多的 API 调用。

这是处理 Swift API 实现中分页行为异常的一对解决方案之一。另见 "fetch_until_empty_page"。

Properties:

- Config:      partial_page_fetch_threshold
- Env Var:     RCLONE_SWIFT_PARTIAL_PAGE_FETCH_THRESHOLD
- Type:        int
- Default:     0

#### --swift-chunk-size

超过此大小的文件将分块处理。

超过此大小的文件将分块存储到 `_segments` 容器或 `.file-segments` 目录中。（详见 `use_segments_container` 选项）。默认值为 5 GiB，这也是其最大值，意味着只有超过此大小的文件才会被分块。

Rclone 将分块文件作为动态大对象（DLO）上传。


Properties:

- Config:      chunk_size
- Env Var:     RCLONE_SWIFT_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     5Gi

#### --swift-no-chunk

流式上传时不分块文件。

当进行流式上传（例如使用 `rcat` 或 `mount` 配合 `--vfs-cache-mode off`）时，设置此标志将使 swift 后端不分块上传文件。

这将把最大流式上传大小限制为 5 GiB。这很有用，因为非分块文件更容易处理且具有 MD5SUM。

rclone 在执行普通复制操作时，仍会对大于 `chunk_size` 的文件进行分块。

Properties:

- Config:      no_chunk
- Env Var:     RCLONE_SWIFT_NO_CHUNK
- Type:        bool
- Default:     false

#### --swift-no-large-objects

禁用对静态大对象和动态大对象的支持

Swift 无法透明地存储大于 5 GiB 的文件。有两种大文件分块方案：静态大对象（SLO）或动态大对象（DLO），而 API 不允许 rclone 在不对对象执行 HEAD 请求的情况下判断文件是静态还是动态大对象。由于两者需要不同处理，这意味着 rclone 必须对对象发出 HEAD 请求，例如在读取校验和时。

当设置了 `no_large_objects` 时，rclone 将假定不存在静态或动态大对象。这意味着它可以停止执行额外的 HEAD 调用，从而大幅提升性能，尤其是在设置了 `--checksum` 进行 swift 到 swift 传输时。

设置此选项意味着 `no_chunk`，并且文件不会以分块方式上传，因此大于 5 GiB 的文件在上传时会直接失败。

如果你设置了此选项但**确实**存在静态或动态大对象，则会导致它们的哈希值不正确。下载会成功，但其他操作如删除和复制会失败。


Properties:

- Config:      no_large_objects
- Env Var:     RCLONE_SWIFT_NO_LARGE_OBJECTS
- Type:        bool
- Default:     false

#### --swift-use-segments-container

选择大对象分段的存储目标

Swift 无法透明地存储大于 5 GiB 的文件，rclone 会将大于 `chunk_size`（默认 5 GiB）的文件分块上传。

如果此值为 `true`，分块将存储在一个额外容器中，该容器名称与目标容器相同但附加了 `_segments`。这意味着原始容器中不会有重复数据，但额外创建容器可能不被接受。

如果此值为 `false`，分块将存储在容器根目录的 `.file-segments` 目录中。列出容器时将省略此目录。某些提供商（如 Blomp）需要此模式，因为不允许创建额外容器。如果希望看到根目录中的 `.file-segments` 目录，则必须将此标志设为 `true`。

如果此值为 `unset`（默认），rclone 将自动选择使用哪个值。除非 rclone 检测到已知需要 `true` 的 `auth_url`，否则将是 `false`。在这种情况下，你会在 DEBUG 日志中看到一条消息。


Properties:

- Config:      use_segments_container
- Env Var:     RCLONE_SWIFT_USE_SEGMENTS_CONTAINER
- Type:        Tristate
- Default:     unset

#### --swift-encoding

后端的编码方式。

详见[概述中的编码部分](/overview/#encoding)。

Properties:

- Config:      encoding
- Env Var:     RCLONE_SWIFT_ENCODING
- Type:        Encoding
- Default:     Slash,InvalidUtf8

#### --swift-description

远程存储的描述。

Properties:

- Config:      description
- Env Var:     RCLONE_SWIFT_DESCRIPTION
- Type:        string
- Required:    false

<!-- autogenerated options stop -->

## 限制

Swift API 不会为分段文件（动态或静态大对象）返回正确的 MD5SUM，因此 rclone 不会对这些文件检查或使用 MD5SUM。

## 故障排除

### Rclone 报错 Failed to create file system for "remote:": Bad Request

由于底层 swift 库的一个特殊行为，当 Swift 认证失败时，它返回的是 "Bad Request" 错误而不是更合理的错误。

所以这最可能意味着你的用户名/密码有误。你可以使用 `--dump-bodies` 标志进一步排查。

这也可能是由于不应指定区域时指定了（例如 OVH）。

### Rclone 报错 Failed to create file system: Response didn't have storage url and auth token

这最可能是因为设置 swift 远程存储时忘记指定租户。

## OVH 云归档

要使用 rclone 访问 OVH 云归档，首先使用 `rclone config` 设置一个 `swift` 后端并选择 OVH，将 `storage_policy` 设为 `pca`。

### 上传对象

向 OVH 云归档上传对象与对象存储没有区别，只需运行你想要的命令（move、copy 或 sync）来上传对象。上传后，对象在 OVH 控制面板中将显示为"冻结"状态。

### 检索对象

使用 `rclone copy` 正常检索对象即可。如果对象处于冻结状态，rclone 会请求解冻所有对象，并在输出末尾等待，显示如下消息：

```text
2019/03/23 13:06:33 NOTICE: Received retry after error - sleeping until 2019-03-23T13:16:33.481657164+01:00 (9m59.99985121s)
```

rclone 将等待指定时间后重试复制。
