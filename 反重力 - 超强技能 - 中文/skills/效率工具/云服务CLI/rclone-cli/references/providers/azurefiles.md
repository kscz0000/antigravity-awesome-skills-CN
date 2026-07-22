---
title: "Microsoft Azure Files Storage"
description: "Rclone 的 Microsoft Azure Files 存储文档"
versionIntroduced: "v1.65"
---

> **官方文档：** [https://rclone.org/azurefiles/](https://rclone.org/azurefiles/)
# Microsoft Azure Files Storage

路径指定为 `remote:`，也可以包含子目录，
例如 `remote:path/to/dir`。

## 配置

以下是为 Microsoft Azure Files Storage 创建配置的示例。假设远程名称为 `remote`。首先运行：

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
XX / Microsoft Azure Files Storage
   \ "azurefiles"
[snip]

Option account.
Azure Storage Account Name.
Set this to the Azure Storage Account Name in use.
Leave blank to use SAS URL or connection string, otherwise it needs to be set.
If this is blank and if env_auth is set it will be read from the
environment variable `AZURE_STORAGE_ACCOUNT_NAME` if possible.
Enter a value. Press Enter to leave empty.
account> account_name

Option share_name.
Azure Files Share Name.
This is required and is the name of the share to access.
Enter a value. Press Enter to leave empty.
share_name> share_name

Option env_auth.
Read credentials from runtime (environment variables, CLI or MSI).
See the [authentication docs](/azurefiles#authentication) for full info.
Enter a boolean value (true or false). Press Enter for the default (false).
env_auth>

Option key.
Storage Account Shared Key.
Leave blank to use SAS URL or connection string.
Enter a value. Press Enter to leave empty.
key> base64encodedkey==

Option sas_url.
SAS URL.
Leave blank if using account/key or connection string.
Enter a value. Press Enter to leave empty.
sas_url>

Option connection_string.
Azure Files Connection String.
Enter a value. Press Enter to leave empty.
connection_string>
[snip]

Configuration complete.
Options:
- type: azurefiles
- account: account_name
- share_name: share_name
- key: base64encodedkey==
Keep this "remote" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d>
```

配置完成后即可使用 rclone。

查看顶层目录中的所有文件：

```console
rclone lsf remote:
```

在根目录中创建新目录：

```console
rclone mkdir remote:dir
```

递归列出内容：

```console
rclone ls remote:
```

将 `/home/local/directory` 同步到远程目录，并删除目录中多余的文件。

```console
rclone sync --interactive /home/local/directory remote:dir
```

### 修改时间

修改时间存储为 Azure 标准的 `LastModified` 时间。

### 性能

上传大文件时，增加 `--azurefiles-upload-concurrency` 的值可以提高性能，但会使用更多内存。默认值 16 设置得较为保守，以减少内存占用。可能需要将其提高到 64 或更高，才能在单文件传输时充分利用 1 GBit/s 的链路。

### 受限文件名字符

除了[默认受限字符集](/overview/#restricted-characters)之外，以下字符也会被替换：

| 字符 | 值 | 替换为 |
| ---- |:---:|:------:|
| "    | 0x22 | ＂     |
| *    | 0x2A | ＊     |
| :    | 0x3A | ：     |
| <    | 0x3C | ＜     |
| >    | 0x3E | ＞     |
| ?    | 0x3F | ？     |
| \    | 0x5C | ＼     |
| \|   | 0x7C | ｜     |

文件名也不能以以下字符结尾。
仅在它们是名称的最后一个字符时才会被替换：

| 字符 | 值 | 替换为 |
| ---- |:---:|:------:|
| .    | 0x2E | ．     |

无效的 UTF-8 字节也会被[替换](/overview/#invalid-utf8)，
因为它们不能用于 JSON 字符串中。

### 哈希

文件会存储 MD5 哈希值。并非所有文件都有 MD5 哈希值，因为这些哈希值需要在上传文件时一起上传。

### 认证 {#authentication}

有多种方式可以为 Azure Files Storage 提供凭据。Rclone 按以下各节的顺序依次尝试。

#### 环境认证

如果 `env_auth` 配置参数为 `true`，则 rclone 将从环境或运行时获取凭据。

它按以下顺序尝试这些认证方法：

1. 环境变量
2. 托管服务标识凭据
3. Azure CLI 凭据（az 工具所使用的）

以下各节将分别描述这些方法。

##### 环境认证：1. 环境变量

如果设置了 `env_auth` 且存在环境变量，rclone 将根据所设置的环境变量，使用密钥或证书认证服务主体，或使用密码认证用户。
它按以下顺序从这些变量读取配置：

1. 使用客户端密钥的服务主体
    - `AZURE_TENANT_ID`：服务主体的租户 ID，也称为"目录"ID。
    - `AZURE_CLIENT_ID`：服务主体的客户端 ID
    - `AZURE_CLIENT_SECRET`：服务主体的客户端密钥之一
2. 使用证书的服务主体
    - `AZURE_TENANT_ID`：服务主体的租户 ID，也称为"目录"ID。
    - `AZURE_CLIENT_ID`：服务主体的客户端 ID
    - `AZURE_CLIENT_CERTIFICATE_PATH`：包含私钥的 PEM 或 PKCS12 证书文件路径
    - `AZURE_CLIENT_CERTIFICATE_PASSWORD`：（可选）证书文件的密码。
    - `AZURE_CLIENT_SEND_CERTIFICATE_CHAIN`：（可选）指定认证请求是否包含 x5c 头以支持基于主题名称/颁发者的认证。设置为 "true" 或 "1" 时，认证请求将包含 x5c 头。
3. 使用用户名和密码的用户
    - `AZURE_TENANT_ID`：（可选）要认证的租户。默认为 "organizations"。
    - `AZURE_CLIENT_ID`：用户将认证到的应用程序的客户端 ID
    - `AZURE_USERNAME`：用户名（通常是电子邮件地址）
    - `AZURE_PASSWORD`：用户密码
4. 工作负载标识
    - `AZURE_TENANT_ID`：要认证的租户
    - `AZURE_CLIENT_ID`：用户将认证到的应用程序的客户端 ID
    - `AZURE_FEDERATED_TOKEN_FILE`：投影服务账号令牌文件路径
    - `AZURE_AUTHORITY_HOST`：Azure Active Directory 端点的颁发机构（默认：login.microsoftonline.com）。

##### 环境认证：2. 托管服务标识凭据

使用托管服务标识时，如果运行此程序的 VM(SS) 具有系统分配的标识，则默认使用该标识。如果资源没有系统分配的标识，但恰好有一个用户分配的标识，则默认使用该用户分配的标识。

如果资源有多个用户分配的标识，则需要取消设置 `env_auth` 并改为设置 `use_msi`。参见 [`use_msi` 小节](#use_msi)。

如果你在断开连接的云或 Azure Stack 等私有云中操作，可能需要设置 `disable_instance_discovery = true`。这决定了 rclone 是否在认证前从 `https://login.microsoft.com/` 请求 Microsoft Entra 实例元数据。将此设置为 `true` 将跳过此请求，你需要自行确保配置的颁发机构有效且可信。

##### 环境认证：3. Azure CLI 凭据（az 工具所使用的）

使用 `az` 工具创建的凭据可以通过 `env_auth` 获取。

例如，如果你使用服务主体登录：

```console
az login --service-principal -u XXX -p XXX --tenant XXX
```

然后你可以这样访问 rclone 资源：

```console
rclone lsf :azurefiles,env_auth,account=ACCOUNT:
```

或者

```console
rclone lsf --azurefiles-env-auth --azurefiles-account=ACCOUNT :azurefiles:
```

#### 账户和共享密钥

这是最直接但灵活性最低的方式。只需填写 `account` 和 `key` 行，其余留空。

#### SAS URL

使用时将 `account`、`key` 和 `connection_string` 留空，填写 `sas_url`。

#### 连接字符串

使用时将 `account`、`key` 和 `sas_url` 留空，填写 `connection_string`。

#### 使用客户端密钥的服务主体

如果设置了这些变量，rclone 将使用客户端密钥认证服务主体。

- `tenant`：服务主体的租户 ID，也称为"目录"ID。
- `client_id`：服务主体的客户端 ID
- `client_secret`：服务主体的客户端密钥之一

凭据也可以通过 `service_principal_file` 配置选项放入文件中。

#### 使用证书的服务主体

如果设置了这些变量，rclone 将使用证书认证服务主体。

- `tenant`：服务主体的租户 ID，也称为"目录"ID。
- `client_id`：服务主体的客户端 ID
- `client_certificate_path`：包含私钥的 PEM 或 PKCS12 证书文件路径
- `client_certificate_password`：（可选）证书文件的密码。
- `client_send_certificate_chain`：（可选）指定认证请求是否包含 x5c 头以支持基于主题名称/颁发者的认证。设置为 "true" 或 "1" 时，认证请求将包含 x5c 头。

**注意** `client_certificate_password` 必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

#### 使用用户名和密码的用户

如果设置了这些变量，rclone 将使用用户名和密码进行认证。

- `tenant`：（可选）要认证的租户。默认为 "organizations"。
- `client_id`：用户将认证到的应用程序的客户端 ID
- `username`：用户名（通常是电子邮件地址）
- `password`：用户密码

Microsoft 不推荐这种认证方式，因为它不如其他认证流程安全。此方法是非交互式的，因此不兼容任何形式的多因素认证，且应用程序必须已获得用户或管理员同意。此凭据只能认证工作和学校账号，无法认证 Microsoft 账号。

**注意** `password` 必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

#### 托管服务标识凭据 {#use_msi}

如果设置了 `use_msi`，则使用托管服务标识凭据。此认证仅在 Azure 服务中运行时有效。使用此选项时需要取消设置 `env_auth`。

但是，如果有多个用户标识可供选择，则必须使用 `msi_object_id`、`msi_client_id` 或 `msi_mi_res_id` 参数中的确切一个来显式指定。

如果 `msi_object_id`、`msi_client_id` 和 `msi_mi_res_id` 均未设置，则等效于使用 `env_auth`。

#### 联合标识凭据

如果设置了这些变量，rclone 将使用联合标识进行认证。

- `tenant_id`：用于存储认证的租户 ID
- `client_id`：用于存储认证的应用程序客户端 ID
- `msi_client_id`：用于认证的应用程序的托管标识客户端 ID

默认情况下，使用 "api://AzureADTokenExchange" 作为通过 MSI 获取令牌的范围。然后使用 'tenant_id' 和 'client_id' 将此令牌交换为实际的存储令牌。

#### Azure CLI 工具 `az` {#use_az}

设置为使用 [Azure CLI 工具 `az`](https://learn.microsoft.com/en-us/cli/azure/) 作为唯一的认证方式。
如果你想在具有系统托管标识但不想使用该标识的主机上使用 `az` CLI，设置此选项会有用。
不要同时设置 `env_auth`。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/azurefiles/azurefiles.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 azurefiles（Microsoft Azure Files）的特定标准选项。

#### --azurefiles-account

Azure 存储账户名称。

将其设置为正在使用的 Azure 存储账户名称。

留空以使用 SAS URL 或模拟器，否则需要设置。

如果留空且设置了 env_auth，则尽可能从环境变量 `AZURE_STORAGE_ACCOUNT_NAME` 中读取。


Properties:

- Config:      account
- Env Var:     RCLONE_AZUREFILES_ACCOUNT
- Type:        string
- Required:    false

#### --azurefiles-env-auth

从运行时（环境变量、CLI 或 MSI）读取凭据。

详见[认证文档](/azureblob#authentication)。

Properties:

- Config:      env_auth
- Env Var:     RCLONE_AZUREFILES_ENV_AUTH
- Type:        bool
- Default:     false

#### --azurefiles-key

存储账户共享密钥。

留空以使用 SAS URL 或模拟器。

Properties:

- Config:      key
- Env Var:     RCLONE_AZUREFILES_KEY
- Type:        string
- Required:    false

#### --azurefiles-sas-url

仅用于容器级别访问的 SAS URL。

如果使用 account/key 或模拟器则留空。

Properties:

- Config:      sas_url
- Env Var:     RCLONE_AZUREFILES_SAS_URL
- Type:        string
- Required:    false

#### --azurefiles-connection-string

存储连接字符串。

存储的连接字符串。如果使用其他认证方法则留空。


Properties:

- Config:      connection_string
- Env Var:     RCLONE_AZUREFILES_CONNECTION_STRING
- Type:        string
- Required:    false

#### --azurefiles-tenant

服务主体的租户 ID，也称为目录 ID。

在使用以下方式时设置此项
- 使用客户端密钥的服务主体
- 使用证书的服务主体
- 使用用户名和密码的用户


Properties:

- Config:      tenant
- Env Var:     RCLONE_AZUREFILES_TENANT
- Type:        string
- Required:    false

#### --azurefiles-client-id

正在使用的客户端 ID。

在使用以下方式时设置此项
- 使用客户端密钥的服务主体
- 使用证书的服务主体
- 使用用户名和密码的用户


Properties:

- Config:      client_id
- Env Var:     RCLONE_AZUREFILES_CLIENT_ID
- Type:        string
- Required:    false

#### --azurefiles-client-secret

服务主体的客户端密钥之一

在使用以下方式时设置此项
- 使用客户端密钥的服务主体


Properties:

- Config:      client_secret
- Env Var:     RCLONE_AZUREFILES_CLIENT_SECRET
- Type:        string
- Required:    false

#### --azurefiles-client-certificate-path

包含私钥的 PEM 或 PKCS12 证书文件路径。

在使用以下方式时设置此项
- 使用证书的服务主体


Properties:

- Config:      client_certificate_path
- Env Var:     RCLONE_AZUREFILES_CLIENT_CERTIFICATE_PATH
- Type:        string
- Required:    false

#### --azurefiles-client-certificate-password

证书文件的密码（可选）。

在使用以下方式时可选设置此项
- 使用证书的服务主体

且证书有密码。


**注意** 输入必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

Properties:

- Config:      client_certificate_password
- Env Var:     RCLONE_AZUREFILES_CLIENT_CERTIFICATE_PASSWORD
- Type:        string
- Required:    false

#### --azurefiles-share-name

Azure Files 共享名称。

这是必需的，即要访问的共享名称。


Properties:

- Config:      share_name
- Env Var:     RCLONE_AZUREFILES_SHARE_NAME
- Type:        string
- Required:    false

### 高级选项

以下是 azurefiles（Microsoft Azure Files）的特定高级选项。

#### --azurefiles-client-send-certificate-chain

使用证书认证时发送证书链。

指定认证请求是否包含 x5c 头以支持基于主题名称/颁发者的认证。设置为 true 时，认证请求将包含 x5c 头。

在使用以下方式时可选设置此项
- 使用证书的服务主体


Properties:

- Config:      client_send_certificate_chain
- Env Var:     RCLONE_AZUREFILES_CLIENT_SEND_CERTIFICATE_CHAIN
- Type:        bool
- Default:     false

#### --azurefiles-username

用户名（通常是电子邮件地址）

在使用以下方式时设置此项
- 使用用户名和密码的用户


Properties:

- Config:      username
- Env Var:     RCLONE_AZUREFILES_USERNAME
- Type:        string
- Required:    false

#### --azurefiles-password

用户密码

在使用以下方式时设置此项
- 使用用户名和密码的用户


**注意** 输入必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

Properties:

- Config:      password
- Env Var:     RCLONE_AZUREFILES_PASSWORD
- Type:        string
- Required:    false

#### --azurefiles-service-principal-file

包含服务主体凭据的文件路径。

通常留空。仅当你想使用服务主体而非交互式登录时才需要。

    $ az ad sp create-for-rbac --name "<name>" \
      --role "Storage Blob Data Owner" \
      --scopes "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>/blobServices/default/containers/<container>" \
      > azure-principal.json

详见["创建 Azure 服务主体"](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli)和["分配 Azure 角色以访问 blob 数据"](https://docs.microsoft.com/en-us/azure/storage/common/storage-auth-aad-rbac-cli)页面。

将凭据直接放入 rclone 配置文件的 `client_id`、`tenant` 和 `client_secret` 键中可能比设置 `service_principal_file` 更方便。


Properties:

- Config:      service_principal_file
- Env Var:     RCLONE_AZUREFILES_SERVICE_PRINCIPAL_FILE
- Type:        string
- Required:    false

#### --azurefiles-disable-instance-discovery

跳过请求 Microsoft Entra 实例元数据

仅在断开连接的云或 Azure Stack 等私有云中认证的应用程序才应设置为 true。

它决定 rclone 是否在认证前从 `https://login.microsoft.com/` 请求 Microsoft Entra 实例元数据。

将此设置为 true 将跳过此请求，你需要自行确保配置的颁发机构有效且可信。


Properties:

- Config:      disable_instance_discovery
- Env Var:     RCLONE_AZUREFILES_DISABLE_INSTANCE_DISCOVERY
- Type:        bool
- Default:     false

#### --azurefiles-use-msi

使用托管服务标识进行认证（仅在 Azure 中有效）。

为 true 时，使用[托管服务标识](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/)认证 Azure 存储，而非 SAS 令牌或账户密钥。

如果运行此程序的 VM(SS) 具有系统分配的标识，则默认使用该标识。如果资源没有系统分配的标识，但恰好有一个用户分配的标识，则默认使用该用户分配的标识。如果资源有多个用户分配的标识，则必须使用 msi_object_id、msi_client_id 或 msi_mi_res_id 参数中的确切一个来显式指定要使用的标识。

Properties:

- Config:      use_msi
- Env Var:     RCLONE_AZUREFILES_USE_MSI
- Type:        bool
- Default:     false

#### --azurefiles-msi-object-id

要使用的用户分配 MSI 的对象 ID（如有）。

如果指定了 msi_client_id 或 msi_mi_res_id 则留空。

Properties:

- Config:      msi_object_id
- Env Var:     RCLONE_AZUREFILES_MSI_OBJECT_ID
- Type:        string
- Required:    false

#### --azurefiles-msi-client-id

要使用的用户分配 MSI 的对象 ID（如有）。

如果指定了 msi_object_id 或 msi_mi_res_id 则留空。

Properties:

- Config:      msi_client_id
- Env Var:     RCLONE_AZUREFILES_MSI_CLIENT_ID
- Type:        string
- Required:    false

#### --azurefiles-msi-mi-res-id

要使用的用户分配 MSI 的 Azure 资源 ID（如有）。

如果指定了 msi_client_id 或 msi_object_id 则留空。

Properties:

- Config:      msi_mi_res_id
- Env Var:     RCLONE_AZUREFILES_MSI_MI_RES_ID
- Type:        string
- Required:    false

#### --azurefiles-use-emulator

如果提供为 'true'，则使用本地存储模拟器。

如果使用真实的 Azure 存储端点则留空。

Properties:

- Config:      use_emulator
- Env Var:     RCLONE_AZUREFILES_USE_EMULATOR
- Type:        bool
- Default:     false

#### --azurefiles-use-az

使用 Azure CLI 工具 az 进行认证

设置为使用 [Azure CLI 工具 az](https://learn.microsoft.com/en-us/cli/azure/) 作为唯一的认证方式。

如果你想在具有系统托管标识但不想使用该标识的主机上使用 az CLI，设置此选项会有用。

不要同时设置 env_auth。


Properties:

- Config:      use_az
- Env Var:     RCLONE_AZUREFILES_USE_AZ
- Type:        bool
- Default:     false

#### --azurefiles-endpoint

服务端点。

通常留空。

Properties:

- Config:      endpoint
- Env Var:     RCLONE_AZUREFILES_ENDPOINT
- Type:        string
- Required:    false

#### --azurefiles-chunk-size

上传分块大小。

注意，分块存储在内存中，内存中可能同时存储最多 "--transfers" * "--azurefile-upload-concurrency" 个分块。

Properties:

- Config:      chunk_size
- Env Var:     RCLONE_AZUREFILES_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     4Mi

#### --azurefiles-upload-concurrency

多部分上传的并发数。

这是同一文件中同时上传的分块数量。

如果你通过高速链路上传少量大文件，且这些上传未充分利用带宽，则增加此值可能有助于加速传输。

注意，分块存储在内存中，内存中可能同时存储最多 "--transfers" * "--azurefile-upload-concurrency" 个分块。

Properties:

- Config:      upload_concurrency
- Env Var:     RCLONE_AZUREFILES_UPLOAD_CONCURRENCY
- Type:        int
- Default:     16

#### --azurefiles-max-stream-size

流式文件的最大大小。

Azure Files 需要预先知道文件的大小。当 rclone 不知道时，使用此值代替。

此值在 rclone 流式传输数据时使用，最常见的用途是：

- 使用 `rclone mount` 且 `--vfs-cache-mode off` 上传文件
- 使用 `rclone rcat`
- 复制未知长度的文件

共享中需要有这么多可用空间，因为文件将暂时占用此大小。


Properties:

- Config:      max_stream_size
- Env Var:     RCLONE_AZUREFILES_MAX_STREAM_SIZE
- Type:        SizeSuffix
- Default:     10Gi

#### --azurefiles-encoding

后端的编码方式。

详见[概述中的编码小节](/overview/#encoding)。

Properties:

- Config:      encoding
- Env Var:     RCLONE_AZUREFILES_ENCODING
- Type:        Encoding
- Default:     Slash,LtGt,DoubleQuote,Colon,Question,Asterisk,Pipe,BackSlash,Del,Ctl,RightPeriod,InvalidUtf8,Dot

#### --azurefiles-description

远程的描述。

Properties:

- Config:      description
- Env Var:     RCLONE_AZUREFILES_DESCRIPTION
- Type:        string
- Required:    false

<!-- autogenerated options stop -->

### 自定义上传头

你可以使用 `--header-upload` 标志设置自定义上传头。

- Cache-Control
- Content-Disposition
- Content-Encoding
- Content-Language
- Content-Type

例如 `--header-upload "Content-Type: text/potato"`

## 限制

MD5 校验和仅在源文件具有 MD5 校验和时才随分块文件一起上传。对于本地到 Azure 的复制，这种情况始终成立。
