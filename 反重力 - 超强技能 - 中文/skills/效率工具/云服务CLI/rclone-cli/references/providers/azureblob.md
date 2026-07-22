---
title: "Microsoft Azure Blob Storage"
description: "Microsoft Azure Blob Storage 的 Rclone 文档"
versionIntroduced: "v1.38"
---

> **官方文档：** [https://rclone.org/azureblob/](https://rclone.org/azureblob/)
# Microsoft Azure Blob Storage

路径指定为 `remote:container`（或 `lsd` 命令使用 `remote:`）。也可以包含子目录，例如 `remote:container/path/to/dir`。

## 配置

以下是一个创建 Microsoft Azure Blob Storage 配置的示例。对于一个名为 `remote` 的远程存储，首先运行：

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
XX / Microsoft Azure Blob Storage
   \ "azureblob"
[snip]
Storage> azureblob
Storage Account Name
account> account_name
Storage Account Key
key> base64encodedkey==
Endpoint for the service - leave blank normally.
endpoint>
Remote config
Configuration complete.
Options:
- type: azureblob
- account: account_name
- key: base64encodedkey==
- endpoint:
Keep this "remote" remote?
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

查看所有容器

```console
rclone lsd remote:
```

创建新容器

```console
rclone mkdir remote:container
```

列出容器的内容

```console
rclone ls remote:container
```

将 `/home/local/directory` 同步到远程容器，删除容器中的多余文件。

```console
rclone sync --interactive /home/local/directory remote:container
```

### --fast-list

此远程存储支持 `--fast-list`，允许你用更多内存换取更少的事务数。详见 [rclone 文档](/docs/#fast-list)。

### 修改时间和哈希

修改时间以 `mtime` 键作为元数据存储在对象上。使用 RFC3339 格式存储，精度为纳秒。该元数据在目录列表时提供，因此使用它没有性能开销。

如果你想使用存储在对象上的 Azure 标准 `LastModified` 时间作为修改时间，请使用 `--use-server-modtime` 标志。注意 rclone 无法设置 `LastModified`，因此如果使用 `--use-server-modtime`，建议在同步时使用 `--update` 标志。

MD5 哈希与 blob 一起存储。但是，分块上传的 blob 只有在源远程存储支持 MD5 哈希时才有 MD5，例如本地磁盘。

### 元数据和标签

当启用 `--metadata`（或使用 `--metadata-set` / `--metadata-mapper`）时，Rclone 可以将任意元数据映射到 Azure Blob 头部、用户元数据和标签。

- 头部：在元数据中设置这些键以映射到对应的 blob 头部：
  - `cache-control`、`content-disposition`、`content-encoding`、`content-language`、`content-type`。
- 用户元数据：任何其他非保留键将作为用户元数据写入（键会被规范化为小写）。以 `x-ms-` 开头的键是保留的，不会作为用户元数据存储。
- 标签：以逗号分隔的 `key=value` 对列表形式提供 `x-ms-tags`，例如 `x-ms-tags=env=dev,team=sync`。这些在上传和服务端复制时作为 blob 标签应用。键/值周围的空格会被忽略。
- 修改时间覆盖：以 RFC3339/RFC3339Nano 格式提供 `mtime` 以覆盖存储在用户元数据中的修改时间。如果 `mtime` 无法解析，rclone 会记录调试消息并忽略该覆盖。

注意：
- Rclone 会忽略保留的 `x-ms-*` 键（`x-ms-tags` 除外）作为用户元数据。

### 性能

上传大文件时，增加 `--azureblob-upload-concurrency` 的值可以提高性能，但会使用更多内存。默认值 16 设置得较为保守以使用较少内存。可能需要将其提高到 64 或更高才能充分利用 1 GBit/s 链路进行单文件传输。

### 受限文件名字符

除了[默认受限字符集](/overview/#restricted-characters)之外，以下字符也会被替换：

| 字符 | 值 | 替换为 |
| ---- |:---:|:------:|
| /    | 0x2F | ／     |
| \    | 0x5C | ＼     |

文件名也不能以以下字符结尾。仅当它们是名称中的最后一个字符时才会被替换：

| 字符 | 值 | 替换为 |
| ---- |:---:|:------:|
| .    | 0x2E | ．     |

无效的 UTF-8 字节也会被[替换](/overview/#invalid-utf8)，因为它们不能用于 JSON 字符串。

### 认证 {#authentication}

Azure Blob Storage 有多种提供凭据的方式。Rclone 按以下各节的顺序尝试。

#### 环境认证

如果 `env_auth` 配置参数为 `true`，则 rclone 将从环境或运行时中获取凭据。

它按以下顺序尝试这些认证方法：

1. 环境变量
2. 托管服务标识凭据
3. Azure CLI 凭据（az 工具使用的）

以下各节对这些方法进行说明

##### 环境认证：1. 环境变量

如果设置了 `env_auth` 且存在环境变量，rclone 会根据设置的环境变量使用客户端密钥或证书认证服务主体，或使用密码认证用户。它按以下顺序从这些变量读取配置：

1. 使用客户端密钥的服务主体
    - `AZURE_TENANT_ID`：服务主体的租户 ID。也称为其"目录"ID。
    - `AZURE_CLIENT_ID`：服务主体的客户端 ID
    - `AZURE_CLIENT_SECRET`：服务主体的客户端密钥之一
2. 使用证书的服务主体
    - `AZURE_TENANT_ID`：服务主体的租户 ID。也称为其"目录"ID。
    - `AZURE_CLIENT_ID`：服务主体的客户端 ID
    - `AZURE_CLIENT_CERTIFICATE_PATH`：包含私钥的 PEM 或 PKCS12 证书文件路径
    - `AZURE_CLIENT_CERTIFICATE_PASSWORD`：（可选）证书文件的密码。
    - `AZURE_CLIENT_SEND_CERTIFICATE_CHAIN`：（可选）指定认证请求是否包含 x5c 头部以支持基于主题名称/颁发者的认证。设置为 "true" 或 "1" 时，认证请求包含 x5c 头部。
3. 使用用户名和密码的用户
    - `AZURE_TENANT_ID`：（可选）要认证的租户。默认为 "organizations"。
    - `AZURE_CLIENT_ID`：用户将认证到的应用程序的客户端 ID
    - `AZURE_USERNAME`：用户名（通常是电子邮件地址）
    - `AZURE_PASSWORD`：用户密码
4. 工作负载标识
    - `AZURE_TENANT_ID`：要认证的租户
    - `AZURE_CLIENT_ID`：用户将认证到的应用程序的客户端 ID
    - `AZURE_FEDERATED_TOKEN_FILE`：投影的服务账户令牌文件路径
    - `AZURE_AUTHORITY_HOST`：Azure Active Directory 端点的授权机构（默认：login.microsoftonline.com）。

##### 环境认证：2. 托管服务标识凭据

使用托管服务标识时，如果运行此程序的 VM(SS) 具有系统分配的标识，则默认使用它。如果资源没有系统分配的标识但恰好有一个用户分配的标识，则默认使用该用户分配的标识。

如果资源有多个用户分配的标识，你需要取消设置 `env_auth` 并改为设置 `use_msi`。参见 [`use_msi` 章节](#use_msi)。

如果你在断开连接的云或私有云（如 Azure Stack）中操作，可能需要设置 `disable_instance_discovery = true`。这决定了 rclone 是否在认证前从 `https://login.microsoft.com/` 请求 Microsoft Entra 实例元数据。将其设置为 `true` 将跳过此请求，你需要自行确保配置的授权机构是有效且可信的。

##### 环境认证：3. Azure CLI 凭据（az 工具使用的）

使用 `az` 工具创建的凭据可以通过 `env_auth` 获取。

例如，如果你使用服务主体登录：

```console
az login --service-principal -u XXX -p XXX --tenant XXX
```

然后你可以这样访问 rclone 资源：

```console
rclone lsf :azureblob,env_auth,account=ACCOUNT:CONTAINER
```

或者

```console
rclone lsf --azureblob-env-auth --azureblob-account=ACCOUNT :azureblob:CONTAINER
```

这类似于使用 `az` 工具：

```console
az storage blob list --container-name CONTAINER --account-name ACCOUNT --auth-mode login
```

#### 账户和共享密钥

这是最直接但最不灵活的方式。只需填写 `account` 和 `key` 行，其余留空即可。

#### SAS URL

可以是账户级 SAS URL 或容器级 SAS URL。

使用时将 `account` 和 `key` 留空，填写 `sas_url`。

账户级 SAS URL 或容器级 SAS URL 可以从 Azure 门户或 Azure 存储资源管理器获取。要获取容器级 SAS URL，请在 Azure 门户的 Azure Blob 资源管理器中右键点击容器。

如果使用容器级 SAS URL，rclone 操作仅允许在特定容器上进行，例如

```console
rclone ls azureblob:container
```

你也可以从根目录列出单个容器。这只会显示 SAS URL 指定的容器。

```console
$ rclone lsd azureblob:
container/
```

注意你不能查看或访问任何其他容器——以下操作将失败

```console
rclone ls azureblob:othercontainer
```

容器级 SAS URL 适用于临时允许第三方访问单个容器，或将凭据放入不受信任的环境（如 CI 构建服务器）。

#### 使用客户端密钥的服务主体

如果设置了这些变量，rclone 将使用客户端密钥认证服务主体。

- `tenant`：服务主体的租户 ID。也称为其"目录"ID。
- `client_id`：服务主体的客户端 ID
- `client_secret`：服务主体的客户端密钥之一

凭据也可以通过 `service_principal_file` 配置选项放入文件中。

#### 使用证书的服务主体

如果设置了这些变量，rclone 将使用证书认证服务主体。

- `tenant`：服务主体的租户 ID。也称为其"目录"ID。
- `client_id`：服务主体的客户端 ID
- `client_certificate_path`：包含私钥的 PEM 或 PKCS12 证书文件路径
- `client_certificate_password`：（可选）证书文件的密码。
- `client_send_certificate_chain`：（可选）指定认证请求是否包含 x5c 头部以支持基于主题名称/颁发者的认证。设置为 "true" 或 "1" 时，认证请求包含 x5c 头部。

**注意** `client_certificate_password` 必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

#### 使用用户名和密码的用户

如果设置了这些变量，rclone 将使用用户名和密码认证。

- `tenant`：（可选）要认证的租户。默认为 "organizations"。
- `client_id`：用户将认证到的应用程序的客户端 ID
- `username`：用户名（通常是电子邮件地址）
- `password`：用户密码

Microsoft 不推荐这种认证方式，因为它不如其他认证流程安全。此方法是非交互式的，因此与任何形式的多因素认证不兼容，且应用程序必须已获得用户或管理员同意。此凭据只能认证工作和学校账户，不能认证 Microsoft 账户。

**注意** `password` 必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

#### 托管服务标识凭据 {#use_msi}

如果设置了 `use_msi`，则使用托管服务标识凭据。此认证仅在 Azure 服务中运行时有效。使用此选项需要取消设置 `env_auth`。

但是，如果你有多个用户标识可供选择，则必须使用 `msi_object_id`、`msi_client_id` 或 `msi_mi_res_id` 参数中的恰好一个来明确指定。

如果 `msi_object_id`、`msi_client_id` 和 `msi_mi_res_id` 均未设置，则等同于使用 `env_auth`。

#### 联合标识凭据

如果设置了这些变量，rclone 将使用联合标识进行认证。

- `tenant_id`：用于存储认证的租户 ID
- `client_id`：用户将认证到存储的应用程序客户端 ID
- `msi_client_id`：用户将认证到的托管标识客户端 ID

默认使用 "api://AzureADTokenExchange" 作为通过 MSI 获取令牌的范围。然后使用 'tenant_id' 和 'client_id' 将此令牌交换为实际的存储令牌。

#### Azure CLI 工具 `az` {#use_az}

设置为使用 [Azure CLI 工具 `az`](https://learn.microsoft.com/en-us/cli/azure/) 作为唯一的认证方式。

如果你想在具有系统托管标识但不想使用该标识的主机上使用 `az` CLI，设置此选项会很有用。

不要同时设置 `env_auth`。

#### 匿名访问 {#anonymous}

如果你想以公共匿名方式访问资源，则只需设置 `account`。你无需创建 rclone 配置即可执行此操作：

```console
rclone lsf :azureblob,account=ACCOUNT:CONTAINER
```

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/azureblob/azureblob.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 azureblob（Microsoft Azure Blob Storage）的特定标准选项。

#### --azureblob-account

Azure 存储账户名称。

将其设置为正在使用的 Azure 存储账户名称。

留空以使用 SAS URL 或模拟器，否则需要设置。

如果此值为空且设置了 env_auth，则会尝试从环境变量 `AZURE_STORAGE_ACCOUNT_NAME` 中读取。


属性：

- Config:      account
- Env Var:     RCLONE_AZUREBLOB_ACCOUNT
- Type:        string
- Required:    false

#### --azureblob-env-auth

从运行时读取凭据（环境变量、CLI 或 MSI）。

完整信息参见[认证文档](/azureblob#authentication)。

属性：

- Config:      env_auth
- Env Var:     RCLONE_AZUREBLOB_ENV_AUTH
- Type:        bool
- Default:     false

#### --azureblob-key

存储账户共享密钥。

留空以使用 SAS URL 或模拟器。

属性：

- Config:      key
- Env Var:     RCLONE_AZUREBLOB_KEY
- Type:        string
- Required:    false

#### --azureblob-sas-url

仅用于容器级访问的 SAS URL。

如果使用 account/key 或模拟器则留空。

属性：

- Config:      sas_url
- Env Var:     RCLONE_AZUREBLOB_SAS_URL
- Type:        string
- Required:    false

#### --azureblob-connection-string

存储连接字符串。

存储的连接字符串。如果使用其他认证方法则留空。


属性：

- Config:      connection_string
- Env Var:     RCLONE_AZUREBLOB_CONNECTION_STRING
- Type:        string
- Required:    false

#### --azureblob-tenant

服务主体的租户 ID。也称为其目录 ID。

使用以下方式时设置此项
- 使用客户端密钥的服务主体
- 使用证书的服务主体
- 使用用户名和密码的用户


属性：

- Config:      tenant
- Env Var:     RCLONE_AZUREBLOB_TENANT
- Type:        string
- Required:    false

#### --azureblob-client-id

正在使用的客户端 ID。

使用以下方式时设置此项
- 使用客户端密钥的服务主体
- 使用证书的服务主体
- 使用用户名和密码的用户


属性：

- Config:      client_id
- Env Var:     RCLONE_AZUREBLOB_CLIENT_ID
- Type:        string
- Required:    false

#### --azureblob-client-secret

服务主体的客户端密钥之一

使用以下方式时设置此项
- 使用客户端密钥的服务主体


属性：

- Config:      client_secret
- Env Var:     RCLONE_AZUREBLOB_CLIENT_SECRET
- Type:        string
- Required:    false

#### --azureblob-client-certificate-path

包含私钥的 PEM 或 PKCS12 证书文件路径。

使用以下方式时设置此项
- 使用证书的服务主体


属性：

- Config:      client_certificate_path
- Env Var:     RCLONE_AZUREBLOB_CLIENT_CERTIFICATE_PATH
- Type:        string
- Required:    false

#### --azureblob-client-certificate-password

证书文件的密码（可选）。

使用以下方式时可选设置此项
- 使用证书的服务主体

且证书有密码。


**注意** 输入必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

属性：

- Config:      client_certificate_password
- Env Var:     RCLONE_AZUREBLOB_CLIENT_CERTIFICATE_PASSWORD
- Type:        string
- Required:    false

### 高级选项

以下是 azureblob（Microsoft Azure Blob Storage）的特定高级选项。

#### --azureblob-client-send-certificate-chain

使用证书认证时发送证书链。

指定认证请求是否包含 x5c 头部以支持基于主题名称/颁发者的认证。设置为 true 时，认证请求包含 x5c 头部。

使用以下方式时可选设置此项
- 使用证书的服务主体


属性：

- Config:      client_send_certificate_chain
- Env Var:     RCLONE_AZUREBLOB_CLIENT_SEND_CERTIFICATE_CHAIN
- Type:        bool
- Default:     false

#### --azureblob-username

用户名（通常是电子邮件地址）

使用以下方式时设置此项
- 使用用户名和密码的用户


属性：

- Config:      username
- Env Var:     RCLONE_AZUREBLOB_USERNAME
- Type:        string
- Required:    false

#### --azureblob-password

用户密码

使用以下方式时设置此项
- 使用用户名和密码的用户


**注意** 输入必须经过混淆处理——参见 [rclone obscure](/commands/rclone_obscure/)。

属性：

- Config:      password
- Env Var:     RCLONE_AZUREBLOB_PASSWORD
- Type:        string
- Required:    false

#### --azureblob-service-principal-file

包含服务主体凭据的文件路径。

通常留空。仅当你想使用服务主体而非交互式登录时才需要。

    $ az ad sp create-for-rbac --name "<name>" \
      --role "Storage Blob Data Owner" \
      --scopes "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>/blobServices/default/containers/<container>" \
      > azure-principal.json

更多详情参见["创建 Azure 服务主体"](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli)和["为访问 blob 数据分配 Azure 角色"](https://docs.microsoft.com/en-us/azure/storage/common/storage-auth-aad-rbac-cli)页面。

将凭据直接放入 rclone 配置文件的 `client_id`、`tenant` 和 `client_secret` 键下可能比设置 `service_principal_file` 更方便。


属性：

- Config:      service_principal_file
- Env Var:     RCLONE_AZUREBLOB_SERVICE_PRINCIPAL_FILE
- Type:        string
- Required:    false

#### --azureblob-disable-instance-discovery

跳过请求 Microsoft Entra 实例元数据

仅当在断开连接的云或私有云（如 Azure Stack）中进行认证的应用程序才应设置为 true。

它决定了 rclone 是否在认证前从 `https://login.microsoft.com/` 请求 Microsoft Entra 实例元数据。

将其设置为 true 将跳过此请求，你需要自行确保配置的授权机构是有效且可信的。


属性：

- Config:      disable_instance_discovery
- Env Var:     RCLONE_AZUREBLOB_DISABLE_INSTANCE_DISCOVERY
- Type:        bool
- Default:     false

#### --azureblob-use-msi

使用托管服务标识进行认证（仅在 Azure 中有效）。

设置为 true 时，使用[托管服务标识](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/)认证 Azure 存储而非 SAS 令牌或账户密钥。

如果运行此程序的 VM(SS) 具有系统分配的标识，则默认使用它。如果资源没有系统分配的标识但恰好有一个用户分配的标识，则默认使用该用户分配的标识。如果资源有多个用户分配的标识，则必须使用 msi_object_id、msi_client_id 或 msi_mi_res_id 参数中的恰好一个来明确指定要使用的标识。

属性：

- Config:      use_msi
- Env Var:     RCLONE_AZUREBLOB_USE_MSI
- Type:        bool
- Default:     false

#### --azureblob-msi-object-id

要使用的用户分配 MSI 的对象 ID（如果有）。

如果指定了 msi_client_id 或 msi_mi_res_id 则留空。

属性：

- Config:      msi_object_id
- Env Var:     RCLONE_AZUREBLOB_MSI_OBJECT_ID
- Type:        string
- Required:    false

#### --azureblob-msi-client-id

要使用的用户分配 MSI 的对象 ID（如果有）。

如果指定了 msi_object_id 或 msi_mi_res_id 则留空。

属性：

- Config:      msi_client_id
- Env Var:     RCLONE_AZUREBLOB_MSI_CLIENT_ID
- Type:        string
- Required:    false

#### --azureblob-msi-mi-res-id

要使用的用户分配 MSI 的 Azure 资源 ID（如果有）。

如果指定了 msi_client_id 或 msi_object_id 则留空。

属性：

- Config:      msi_mi_res_id
- Env Var:     RCLONE_AZUREBLOB_MSI_MI_RES_ID
- Type:        string
- Required:    false

#### --azureblob-use-emulator

如果设置为 'true' 则使用本地存储模拟器。

如果使用真实的 Azure 存储端点则留空。

属性：

- Config:      use_emulator
- Env Var:     RCLONE_AZUREBLOB_USE_EMULATOR
- Type:        bool
- Default:     false

#### --azureblob-use-az

使用 Azure CLI 工具 az 进行认证

设置为使用 [Azure CLI 工具 az](https://learn.microsoft.com/en-us/cli/azure/) 作为唯一的认证方式。

如果你想在具有系统托管标识但不想使用该标识的主机上使用 az CLI，设置此选项会很有用。

不要同时设置 env_auth。


属性：

- Config:      use_az
- Env Var:     RCLONE_AZUREBLOB_USE_AZ
- Type:        bool
- Default:     false

#### --azureblob-endpoint

服务的端点。

通常留空。

属性：

- Config:      endpoint
- Env Var:     RCLONE_AZUREBLOB_ENDPOINT
- Type:        string
- Required:    false

#### --azureblob-upload-cutoff

切换到分块上传的截止大小（<= 256 MiB）（已弃用）。

属性：

- Config:      upload_cutoff
- Env Var:     RCLONE_AZUREBLOB_UPLOAD_CUTOFF
- Type:        string
- Required:    false

#### --azureblob-chunk-size

上传块大小。

注意这些块存储在内存中，同时可能有多达 "--transfers" * "--azureblob-upload-concurrency" 个块存储在内存中。

属性：

- Config:      chunk_size
- Env Var:     RCLONE_AZUREBLOB_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     4Mi

#### --azureblob-upload-concurrency

分块上传的并发数。

这是同一文件同时上传的块数。

如果你在高速链路上上传少量大文件，且这些上传没有充分利用你的带宽，那么增加此值可能有助于加快传输速度。

在测试中，上传速度几乎与上传并发数呈线性增长。例如，要填满千兆管道，可能需要将此值提高到 64。注意这会使用更多内存。

注意这些块存储在内存中，同时可能有多达 "--transfers" * "--azureblob-upload-concurrency" 个块存储在内存中。

属性：

- Config:      upload_concurrency
- Env Var:     RCLONE_AZUREBLOB_UPLOAD_CONCURRENCY
- Type:        int
- Default:     16

#### --azureblob-copy-cutoff

切换到分块复制的截止大小。

任何大于此大小且需要服务端复制的文件将以 chunk_size 大小的块使用 put block list API 进行复制。

小于此限制的文件将使用 Copy Blob API 复制。

属性：

- Config:      copy_cutoff
- Env Var:     RCLONE_AZUREBLOB_COPY_CUTOFF
- Type:        SizeSuffix
- Default:     8Mi

#### --azureblob-copy-concurrency

分块复制的并发数。

这是同一文件同时复制的块数。

这些块不会在内存中缓冲，Microsoft 在 azcopy 文档中建议将此值设置为大于 1000。

https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-optimize#increase-concurrency

在测试中，复制速度几乎与复制并发数呈线性增长。

属性：

- Config:      copy_concurrency
- Env Var:     RCLONE_AZUREBLOB_COPY_CONCURRENCY
- Type:        int
- Default:     512

#### --azureblob-use-copy-blob

复制到同一存储账户时是否使用 Copy Blob API。

如果为 true（默认值），则即使大小超过 copy_cutoff，rclone 也会对同一存储账户的复制使用 Copy Blob API。

Rclone 假定同一存储账户意味着相同的配置，不会检查不同配置中的同一存储账户。

通常无需更改此值。


属性：

- Config:      use_copy_blob
- Env Var:     RCLONE_AZUREBLOB_USE_COPY_BLOB
- Type:        bool
- Default:     true

#### --azureblob-list-chunk

Blob 列表的大小。

这设置了每个列表块中请求的 blob 数量。默认值为最大值 5000。"列出 blob" 请求允许每兆字节 2 分钟完成。如果操作平均每兆字节耗时超过 2 分钟，它将超时（[来源](https://docs.microsoft.com/en-us/rest/api/storageservices/setting-timeouts-for-blob-service-operations#exceptions-to-default-timeout-interval)）。这可用于限制返回的 blob 条目数，以避免超时。

属性：

- Config:      list_chunk
- Env Var:     RCLONE_AZUREBLOB_LIST_CHUNK
- Type:        int
- Default:     5000

#### --azureblob-access-tier

Blob 的访问层：热、冷、寒或归档。

归档的 blob 可以通过将访问层设置为热、冷或寒来恢复。如果你想使用在账户级别设置的默认访问层，则留空

如果未指定"访问层"，rclone 不会应用任何层。rclone 在上传时对 blob 执行"设置层"操作，如果对象未被修改，指定新的"访问层"不会有任何效果。如果远程存储中的 blob 处于"归档层"，尝试从远程存储执行数据传输操作将不被允许。用户应先通过将 blob 层设置为"热"、"冷"或"寒"来恢复。

属性：

- Config:      access_tier
- Env Var:     RCLONE_AZUREBLOB_ACCESS_TIER
- Type:        string
- Required:    false

#### --azureblob-archive-tier-delete

覆盖前删除归档层 blob。

归档层 blob 无法更新。因此如果不使用此标志，当你尝试更新归档层 blob 时，rclone 将产生以下错误：

    can't update archive tier blob without --azureblob-archive-tier-delete

设置此标志后，在 rclone 尝试覆盖归档层 blob 之前，它会先删除现有 blob 再上传替换内容。如果上传失败，这可能会导致数据丢失（与更新普通 blob 不同），并且由于提前删除归档层 blob 可能会产生费用。


属性：

- Config:      archive_tier_delete
- Env Var:     RCLONE_AZUREBLOB_ARCHIVE_TIER_DELETE
- Type:        bool
- Default:     false

#### --azureblob-disable-checksum

不将 MD5 校验和与对象元数据一起存储。

通常 rclone 会在上传前计算输入的 MD5 校验和，以便将其添加到对象的元数据中。这对于数据完整性检查很有利，但可能导致大文件开始上传前出现长时间延迟。

属性：

- Config:      disable_checksum
- Env Var:     RCLONE_AZUREBLOB_DISABLE_CHECKSUM
- Type:        bool
- Default:     false

#### --azureblob-memory-pool-flush-time

内部内存缓冲池刷新频率。（已不再使用）

属性：

- Config:      memory_pool_flush_time
- Env Var:     RCLONE_AZUREBLOB_MEMORY_POOL_FLUSH_TIME
- Type:        Duration
- Default:     1m0s

#### --azureblob-memory-pool-use-mmap

是否在内部内存池中使用 mmap 缓冲区。（已不再使用）

属性：

- Config:      memory_pool_use_mmap
- Env Var:     RCLONE_AZUREBLOB_MEMORY_POOL_USE_MMAP
- Type:        bool
- Default:     false

#### --azureblob-encoding

后端的编码。

更多信息参见[概览中的编码章节](/overview/#encoding)。

属性：

- Config:      encoding
- Env Var:     RCLONE_AZUREBLOB_ENCODING
- Type:        Encoding
- Default:     Slash,BackSlash,Del,Ctl,RightPeriod,InvalidUtf8

#### --azureblob-public-access

容器的公共访问级别：blob 或 container。

属性：

- Config:      public_access
- Env Var:     RCLONE_AZUREBLOB_PUBLIC_ACCESS
- Type:        string
- Required:    false
- Examples:
  - ""
    - 容器及其 blob 只能通过授权请求访问。
    - 这是默认值。
  - "blob"
    - 此容器内的 blob 数据可以通过匿名请求读取。
  - "container"
    - 允许对容器和 blob 数据进行完全公共读取访问。

#### --azureblob-directory-markers

创建新目录时上传带有尾随斜杠的空对象

基于桶的远程存储不支持空文件夹，此选项创建以 "/" 结尾的空对象以持久化文件夹。

此对象还具有元数据 "hdi_isfolder = true" 以符合 Microsoft 标准。


属性：

- Config:      directory_markers
- Env Var:     RCLONE_AZUREBLOB_DIRECTORY_MARKERS
- Type:        bool
- Default:     false

#### --azureblob-no-check-container

如果设置，则不尝试检查容器是否存在或创建它。

当你知道容器已存在时，这有助于最小化 rclone 执行的事务数。


属性：

- Config:      no_check_container
- Env Var:     RCLONE_AZUREBLOB_NO_CHECK_CONTAINER
- Type:        bool
- Default:     false

#### --azureblob-no-head-object

如果设置，获取对象时不执行 HEAD 再 GET。

属性：

- Config:      no_head_object
- Env Var:     RCLONE_AZUREBLOB_NO_HEAD_OBJECT
- Type:        bool
- Default:     false

#### --azureblob-delete-snapshots

设置为指定删除 blob 时如何处理快照。

属性：

- Config:      delete_snapshots
- Env Var:     RCLONE_AZUREBLOB_DELETE_SNAPSHOTS
- Type:        string
- Required:    false
- Choices:
  - ""
    - 默认情况下，如果 blob 有快照，删除操作将失败
  - "include"
    - 指定 'include' 以删除根 blob 及其所有快照
  - "only"
    - 指定 'only' 以仅删除快照但保留根 blob。

#### --azureblob-description

远程存储的描述。

属性：

- Config:      description
- Env Var:     RCLONE_AZUREBLOB_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

用户元数据存储为 x-ms-meta- 键。Azure 元数据键不区分大小写，始终以小写返回。

以下是 azureblob 后端可能的系统元数据项。

| 名称 | 说明 | 类型 | 示例 | 只读 |
| ---- | ---- | ---- | ---- | ---- |
| cache-control | Cache-Control 头部 | string | no-cache | N |
| content-disposition | Content-Disposition 头部 | string | inline | N |
| content-encoding | Content-Encoding 头部 | string | gzip | N |
| content-language | Content-Language 头部 | string | en-US | N |
| content-type | Content-Type 头部 | string | text/plain | N |
| mtime | 最后修改时间，从 rclone 元数据读取 | RFC 3339 | 2006-01-02T15:04:05.999999999Z07:00 | N |
| tier | 对象的层 | string | Hot | **Y** |

更多信息参见[元数据](/docs/#metadata)文档。

<!-- autogenerated options stop -->

### 自定义上传头部

你可以使用 `--header-upload` 标志设置自定义上传头部。

- Cache-Control
- Content-Disposition
- Content-Encoding
- Content-Language
- Content-Type
- X-MS-Tags

例如 `--header-upload "Content-Type: text/potato"` 或 `--header-upload "X-MS-Tags: foo=bar"`。

## 限制

MD5 校验和仅在源具有 MD5 校验和时分块文件才会被上传。对于本地到 Azure 的复制，这始终是成立的。

Microsoft Azure Blob 存储后端不支持 `rclone about`。不支持此功能的后端无法确定 rclone 挂载的可用空间，也无法在 rclone union 远程存储中使用 `mfs`（最大可用空间）策略。

参见[不支持 rclone about 的后端列表](https://rclone.org/overview/#optional-features)和 [rclone about](https://rclone.org/commands/rclone_about/)。

## Azure 存储模拟器支持

你可以使用存储模拟器（通常是 _azurite_）运行 rclone。

为此，只需按照简介中的说明使用 `rclone config` 设置新的远程存储，并在高级设置中将 `use_emulator` 设置为 `true`。你不需要提供默认账户名或账户密钥。但你可以在 `account` 和 `key` 选项中覆盖它们。（在 v1.61 之前，它们被硬编码为 _azurite_ 的 `devstoreaccount1`。）

此外，如果你想访问运行在不同机器上的存储模拟器实例，你可以在高级设置中覆盖 `endpoint` 参数，将其设置为 `http(s)://<host>:<port>/devstoreaccount1`（例如 `http://10.254.2.5:10000/devstoreaccount1`）。
