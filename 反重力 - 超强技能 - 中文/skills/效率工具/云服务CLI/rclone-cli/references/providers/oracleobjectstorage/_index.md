---
title: "Oracle Object Storage"
description: "Oracle Object Storage 的 Rclone 文档"
type: page
versionIntroduced: "v1.60"
---

> **官方文档：** [https://rclone.org/oracleobjectstorage/](https://rclone.org/oracleobjectstorage/)
# Oracle Object Storage

由 Oracle Cloud Infrastructure (OCI) 提供的对象存储服务。
更多信息请访问 <oracle.com>：

- [Oracle Object Storage 概述](https://docs.oracle.com/iaas/Content/Object/Concepts/objectstorageoverview.htm)
- [Oracle Object Storage 常见问题](https://www.oracle.com/cloud/storage/object-storage/faq/)

路径指定为 `remote:bucket`（或 `lsd` 命令使用 `remote:`）。
也可以包含子目录，例如 `remote:bucket/path/to/dir`。

将本地构建产物传输到 Oracle Object Storage 中 remote:bucket 的示例命令：

```console
rclone -vvv  --progress --stats-one-line --max-stats-groups 10 --log-format date,time,UTC,longfile --fast-list --buffer-size 256Mi --oos-no-check-bucket --oos-upload-cutoff 10Mi --multi-thread-cutoff 16Mi --multi-thread-streams 3000 --transfers 3000 --checkers 64  --retries 2  --oos-chunk-size 10Mi --oos-upload-concurrency 10000  --oos-attempt-resume-upload --oos-leave-parts-on-error sync ./artifacts  remote:bucket -vv
```

## 配置

以下是一个创建 Oracle Object Storage 配置的示例。`rclone config` 会引导你完成配置。

以下是如何创建名为 `remote` 的远程存储的示例。首先运行：

```console
rclone config
```

这将引导你完成交互式配置过程：

```text
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> n

Enter name for new remote.
name> remote

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
[snip]
XX / Oracle Cloud Infrastructure Object Storage
   \ (oracleobjectstorage)
Storage> oracleobjectstorage

Option provider.
Choose your Auth Provider
Choose a number from below, or type in your own string value.
Press Enter for the default (env_auth).
 1 / automatically pickup the credentials from runtime(env), first one to provide auth wins
   \ (env_auth)
   / use an OCI user and an API key for authentication.
 2 | you’ll need to put in a config file your tenancy OCID, user OCID, region, the path, fingerprint to an API key.
   | https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm
   \ (user_principal_auth)
   / use instance principals to authorize an instance to make API calls.
 3 | each instance has its own identity, and authenticates using the certificates that are read from instance metadata.
   | https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm
   \ (instance_principal_auth)
   / use workload identity to grant Kubernetes pods policy-driven access to Oracle Cloud
 4 | Infrastructure (OCI) resources using OCI Identity and Access Management (IAM).
   | https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contenggrantingworkloadaccesstoresources.htm
   \ (workload_identity_auth)
 5 / use resource principals to make API calls
   \ (resource_principal_auth)
 6 / no credentials needed, this is typically for reading public buckets
   \ (no_auth)
provider> 2

Option namespace.
Object storage namespace
Enter a value.
namespace> idbamagbg734

Option compartment.
Object storage compartment OCID
Enter a value.
compartment> ocid1.compartment.oc1..aaaaaaaapufkxc7ame3sthry5i7ujrwfc7ejnthhu6bhanm5oqfjpyasjkba

Option region.
Object storage Region
Enter a value.
region> us-ashburn-1

Option endpoint.
Endpoint for Object storage API.
Leave blank to use the default endpoint for the region.
Enter a value. Press Enter to leave empty.
endpoint>

Option config_file.
Full Path to OCI config file
Choose a number from below, or type in your own string value.
Press Enter for the default (~/.oci/config).
 1 / oci configuration file location
   \ (~/.oci/config)
config_file> /etc/oci/dev.conf

Option config_profile.
Profile name inside OCI config file
Choose a number from below, or type in your own string value.
Press Enter for the default (Default).
 1 / Use the default profile
   \ (Default)
config_profile> Test

Edit advanced config?
y) Yes
n) No (default)
y/n> n

Configuration complete.
Options:
- type: oracleobjectstorage
- namespace: idbamagbg734
- compartment: ocid1.compartment.oc1..aaaaaaaapufkxc7ame3sthry5i7ujrwfc7ejnthhu6bhanm5oqfjpyasjkba
- region: us-ashburn-1
- provider: user_principal_auth
- config_file: /etc/oci/dev.conf
- config_profile: Test
Keep this "remote" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

查看所有存储桶

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
rclone ls remote:bucket --max-depth 1
```

## 认证提供者

OCI 提供多种认证方式。要了解更多认证方式，请参阅 [OCI 认证方式](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdk_authentication_methods.htm)
这些选项可以在 rclone 配置文件中指定。

Rclone 支持以下 OCI 认证提供者。

```text
User Principal
Instance Principal
Resource Principal
Workload Identity
No authentication
```

### User Principal

认证提供者 User Principal 的 rclone 配置文件示例：

```ini
[oos]
type = oracleobjectstorage
namespace = id<redacted>34
compartment = ocid1.compartment.oc1..aa<redacted>ba
region = us-ashburn-1
provider = user_principal_auth
config_file = /home/opc/.oci/config
config_profile = Default
```

优点：

- 可以在 OCI 内的任何服务器、本地环境或其他云服务商处使用此方法。

注意事项：

- 需要配置用户权限/策略以允许访问对象存储
- 管理用户和密钥的开销
- 如果用户被删除，配置文件将不再工作，可能导致使用该用户凭据的自动化流程出现回归问题。

### Instance Principal

OCI 计算实例可以通过使用其身份和证书作为实例主体来获得使用 rclone 的授权。使用此方法无需存储和管理凭据。

认证提供者 Instance Principal 的 rclone 配置文件示例：

```console
[opc@rclone ~]$ cat ~/.config/rclone/rclone.conf
[oos]
type = oracleobjectstorage
namespace = id<redacted>fn
compartment = ocid1.compartment.oc1..aa<redacted>k7a
region = us-ashburn-1
provider = instance_principal_auth
```

优点：

- 使用实例主体，无需在计算实例上配置用户凭据、传输或保存到磁盘，也无需轮换凭据。
- 无需处理用户和密钥。
- 极大简化自动化，因为不必管理访问密钥、用户私钥、将它们存储在保险库中、使用 KMS 等。

注意事项：

- 需要配置一个包含此实例为成员的动态组，并向该动态组添加读取对象存储的策略。
- 任何有权访问此机器的人都可以执行 CLI 命令。
- 仅适用于 OCI 计算实例，不能用于外部实例或资源。

### Resource Principal

Resource Principal 认证与 Instance Principal 认证非常相似，但用于非计算实例的资源，例如[无服务器函数](https://docs.oracle.com/en-us/iaas/Content/Functions/Concepts/functionsoverview.htm)。
要使用 Resource Principal，请确保在 Rclone 进程中设置了以下环境变量。

```console
export OCI_RESOURCE_PRINCIPAL_VERSION=2.2
export OCI_RESOURCE_PRINCIPAL_REGION=us-ashburn-1
export OCI_RESOURCE_PRINCIPAL_PRIVATE_PEM=/usr/share/model-server/key.pem
export OCI_RESOURCE_PRINCIPAL_RPST=/usr/share/model-server/security_token
```

认证提供者 Resource Principal 的 rclone 配置文件示例：

```ini
[oos]
type = oracleobjectstorage
namespace = id<redacted>34
compartment = ocid1.compartment.oc1..aa<redacted>ba
region = us-ashburn-1
provider = resource_principal_auth
```

### Workload Identity

当在容器引擎 for Kubernetes (OKE) 集群上的 Kubernetes Pod 中运行 Rclone 时，可以使用 Workload Identity 认证。有关配置 Workload Identity 的更多详细信息，请参阅[授予工作负载对 OCI 资源的访问权限](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contenggrantingworkloadaccesstoresources.htm)。
要使用 Workload Identity，请确保在 Rclone 进程中设置了以下环境变量。

```console
export OCI_RESOURCE_PRINCIPAL_VERSION=2.2
export OCI_RESOURCE_PRINCIPAL_REGION=us-ashburn-1
```

### 无认证

公共存储桶不需要任何认证机制即可读取对象。
无认证的 rclone 配置文件示例：

```ini
[oos]
type = oracleobjectstorage
namespace = id<redacted>34
compartment = ocid1.compartment.oc1..aa<redacted>ba
region = us-ashburn-1
provider = no_auth
```

### 修改时间和哈希

修改时间以 `opc-meta-mtime` 元数据的形式存储在对象上，以自纪元以来的浮点数表示，精度为 1 纳秒。

如果需要更新修改时间，rclone 会尝试执行服务端复制来更新修改时间（前提是对象可以在单次分片中完成复制）。
如果对象大于 5GB，则会重新上传而非复制。

注意，从对象中读取此信息需要一个额外的 `HEAD` 请求，因为元数据不会在对象列表中返回。

支持 MD5 哈希算法。

### 分片上传

rclone 支持对 OOS 进行分片上传，这意味着可以上传大于 5 GiB 的文件。

注意，同时通过分片上传和 crypt 远程存储上传的文件没有 MD5 校验和。

rclone 在 `--oos-upload-cutoff` 指定的阈值处从单分片上传切换到分片上传。最大值为 5 GiB，最小值为 0（即始终使用分片上传文件）。

分片上传中使用的分片大小由 `--oos-chunk-size` 指定，并发上传的分片数量由 `--oos-upload-concurrency` 指定。

分片上传将使用 `--transfers` * `--oos-upload-concurrency` * `--oos-chunk-size` 的额外内存。单分片上传不使用额外内存。

单分片传输可能比分片传输更快或更慢，取决于你与 OOS 之间的延迟——延迟越高，单分片传输更可能更快。

增加 `--oos-upload-concurrency` 将提高吞吐量（8 是一个合理的值），增加 `--oos-chunk-size` 也会提高吞吐量（16M 是合理的）。增加其中任何一个都会使用更多内存。默认值已经足够高，可以在不占用过多内存的情况下获得大部分可能的性能提升。

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/oracleobjectstorage/oracleobjectstorage.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 oracleobjectstorage（Oracle Cloud Infrastructure Object Storage）特有的标准选项。

#### --oos-provider

选择你的认证提供者

属性：

- Config:      provider
- Env Var:     RCLONE_OOS_PROVIDER
- Type:        string
- Default:     "env_auth"
- Examples:
  - "env_auth"
    - 自动从运行时环境获取凭据，第一个提供认证的获胜
  - "user_principal_auth"
    - 使用 OCI 用户和 API 密钥进行认证。
    - 需要在配置文件中填入租户 OCID、用户 OCID、区域、路径和 API 密钥的指纹。
    - https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm
  - "instance_principal_auth"
    - 使用实例主体授权实例进行 API 调用。
    - 每个实例都有自己的身份，并使用从实例元数据中读取的证书进行认证。
    - https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm
  - "workload_identity_auth"
    - 使用工作负载身份授予 OCI 容器引擎 for Kubernetes 工作负载通过 OCI 身份和访问管理 (IAM) 对 OCI 资源的策略驱动访问。
    - https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contenggrantingworkloadaccesstoresources.htm
  - "resource_principal_auth"
    - 使用资源主体进行 API 调用
  - "no_auth"
    - 无需凭据，通常用于读取公共存储桶

#### --oos-namespace

对象存储命名空间

属性：

- Config:      namespace
- Env Var:     RCLONE_OOS_NAMESPACE
- Type:        string
- Required:    true

#### --oos-compartment

指定区间 OCID，如果需要列出存储桶。

列出对象无需区间 OCID。

属性：

- Config:      compartment
- Env Var:     RCLONE_OOS_COMPARTMENT
- Provider:    !no_auth
- Type:        string
- Required:    false

#### --oos-region

对象存储区域

属性：

- Config:      region
- Env Var:     RCLONE_OOS_REGION
- Type:        string
- Required:    true

#### --oos-endpoint

对象存储 API 的端点。

留空则使用该区域的默认端点。

属性：

- Config:      endpoint
- Env Var:     RCLONE_OOS_ENDPOINT
- Type:        string
- Required:    false

#### --oos-config-file

OCI 配置文件的路径

属性：

- Config:      config_file
- Env Var:     RCLONE_OOS_CONFIG_FILE
- Provider:    user_principal_auth
- Type:        string
- Default:     "~/.oci/config"
- Examples:
  - "~/.oci/config"
    - OCI 配置文件位置

#### --oos-config-profile

OCI 配置文件中的配置文件名称

属性：

- Config:      config_profile
- Env Var:     RCLONE_OOS_CONFIG_PROFILE
- Provider:    user_principal_auth
- Type:        string
- Default:     "Default"
- Examples:
  - "Default"
    - 使用默认配置文件

### 高级选项

以下是 oracleobjectstorage（Oracle Cloud Infrastructure Object Storage）特有的高级选项。

#### --oos-storage-tier

在存储中存储新对象时使用的存储层级。https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm

属性：

- Config:      storage_tier
- Env Var:     RCLONE_OOS_STORAGE_TIER
- Type:        string
- Default:     "Standard"
- Examples:
  - "Standard"
    - 标准存储层级，这是默认层级
  - "InfrequentAccess"
    - 低频访问存储层级
  - "Archive"
    - 归档存储层级

#### --oos-upload-cutoff

切换到分块上传的阈值。

任何大于此值的文件将以 chunk_size 的大小分块上传。
最小值为 0，最大值为 5 GiB。

属性：

- Config:      upload_cutoff
- Env Var:     RCLONE_OOS_UPLOAD_CUTOFF
- Type:        SizeSuffix
- Default:     200Mi

#### --oos-chunk-size

上传时使用的分块大小。

当上传大于 upload_cutoff 的文件或大小未知的文件（例如来自 "rclone rcat" 或通过 "rclone mount" 上传的文件）时，将使用此分块大小进行分片上传。

注意，每次传输会在内存中缓冲 "upload_concurrency" 个此大小的分块。

如果你在高速链路上传输大文件且有足够的内存，增加此值可以加速传输。

rclone 会在上传已知大小的大文件时自动增加分块大小，以保持在 10,000 个分块的限制以下。

大小未知的文件会使用配置的 chunk_size 上传。由于默认分块大小为 5 MiB 且最多可有 10,000 个分块，这意味着默认情况下流式上传的文件最大为 48 GiB。如果你想流式上传更大的文件，则需要增加 chunk_size。

增加分块大小会降低使用 "-P" 标志显示的进度统计的准确性。


属性：

- Config:      chunk_size
- Env Var:     RCLONE_OOS_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     5Mi

#### --oos-max-upload-parts

分片上传中的最大分块数。

此选项定义执行分片上传时使用的最大分块数。

OCI 的最大分块限制为 10,000 个分块。

rclone 会在上传已知大小的大文件时自动增加分块大小，以保持在此分块数量限制以下。


属性：

- Config:      max_upload_parts
- Env Var:     RCLONE_OOS_MAX_UPLOAD_PARTS
- Type:        int
- Default:     10000

#### --oos-upload-concurrency

分片上传的并发数。

这是同一文件中并发上传的分块数量。

如果你在高速链路上上传少量大文件，且这些上传没有充分利用你的带宽，增加此值可能有助于加速传输。

属性：

- Config:      upload_concurrency
- Env Var:     RCLONE_OOS_UPLOAD_CONCURRENCY
- Type:        int
- Default:     10

#### --oos-copy-cutoff

切换到分片复制的阈值。

任何大于此值且需要服务端复制的文件将以此大小的分块进行复制。

最小值为 0，最大值为 5 GiB。

属性：

- Config:      copy_cutoff
- Env Var:     RCLONE_OOS_COPY_CUTOFF
- Type:        SizeSuffix
- Default:     4.656Gi

#### --oos-copy-timeout

复制操作的超时时间。

复制是异步操作，指定等待复制成功完成的超时时间


属性：

- Config:      copy_timeout
- Env Var:     RCLONE_OOS_COPY_TIMEOUT
- Type:        Duration
- Default:     1m0s

#### --oos-disable-checksum

不在对象元数据中存储 MD5 校验和。

通常 rclone 会在上传前计算输入的 MD5 校验和，以便将其添加到对象的元数据中。这对数据完整性检查很有利，但可能导致大文件开始上传前出现较长的延迟。

属性：

- Config:      disable_checksum
- Env Var:     RCLONE_OOS_DISABLE_CHECKSUM
- Type:        bool
- Default:     false

#### --oos-encoding

后端的编码方式。

更多信息请参阅[概述中的编码部分](/overview/#encoding)。

属性：

- Config:      encoding
- Env Var:     RCLONE_OOS_ENCODING
- Type:        Encoding
- Default:     Slash,InvalidUtf8,Dot

#### --oos-leave-parts-on-error

如果设为 true，在失败时避免调用中止上传，保留所有已成功上传的分块以便手动恢复。

如果需要跨不同会话恢复上传，应设为 true。

警告：存储未完成的分片上传的分块会占用对象存储的空间使用量，如果不清理将产生额外费用。


属性：

- Config:      leave_parts_on_error
- Env Var:     RCLONE_OOS_LEAVE_PARTS_ON_ERROR
- Type:        bool
- Default:     false

#### --oos-attempt-resume-upload

如果设为 true，尝试恢复该对象之前已启动的分片上传。这有助于通过从上次会话恢复上传来加速分片传输。

警告：如果恢复会话中的分块大小与之前未完成会话中的不同，则恢复的分片上传将被中止，并以新的分块大小重新启动分片上传。

leave_parts_on_error 标志必须设为 true 才能恢复，并优化跳过已成功上传的分块。


属性：

- Config:      attempt_resume_upload
- Env Var:     RCLONE_OOS_ATTEMPT_RESUME_UPLOAD
- Type:        bool
- Default:     false

#### --oos-no-check-bucket

如果设置，不尝试检查存储桶是否存在或创建它。

当你知道存储桶已经存在时，这有助于减少 rclone 执行的事务数量。

当你使用的用户没有存储桶创建权限时，也可能需要此选项。


属性：

- Config:      no_check_bucket
- Env Var:     RCLONE_OOS_NO_CHECK_BUCKET
- Type:        bool
- Default:     false

#### --oos-sse-customer-key-file

使用 SSE-C 时，包含与对象关联的 AES-256 加密密钥的 base64 编码字符串的文件。请注意，sse_customer_key_file|sse_customer_key|sse_kms_key_id 三者中只需设置一个。

属性：

- Config:      sse_customer_key_file
- Env Var:     RCLONE_OOS_SSE_CUSTOMER_KEY_FILE
- Type:        string
- Required:    false
- Examples:
  - ""
    - 无

#### --oos-sse-customer-key

使用 SSE-C 时，指定用于加密或解密数据的 base64 编码 256 位加密密钥的可选请求头。请注意，sse_customer_key_file|sse_customer_key|sse_kms_key_id 三者中只需设置一个。更多信息请参阅使用自有密钥进行服务端加密 (https://docs.cloud.oracle.com/Content/Object/Tasks/usingyourencryptionkeys.htm)

属性：

- Config:      sse_customer_key
- Env Var:     RCLONE_OOS_SSE_CUSTOMER_KEY
- Type:        string
- Required:    false
- Examples:
  - ""
    - 无

#### --oos-sse-customer-key-sha256

如果使用 SSE-C，指定加密密钥的 base64 编码 SHA256 哈希值的可选请求头。此值用于检查加密密钥的完整性。参见使用自有密钥进行服务端加密 (https://docs.cloud.oracle.com/Content/Object/Tasks/usingyourencryptionkeys.htm)。

属性：

- Config:      sse_customer_key_sha256
- Env Var:     RCLONE_OOS_SSE_CUSTOMER_KEY_SHA256
- Type:        string
- Required:    false
- Examples:
  - ""
    - 无

#### --oos-sse-kms-key-id

如果在保险库中使用自有主密钥，此请求头指定用于调用密钥管理服务以生成数据加密密钥或加密/解密数据加密密钥的主加密密钥的 OCID (https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm)。请注意，sse_customer_key_file|sse_customer_key|sse_kms_key_id 三者中只需设置一个。

属性：

- Config:      sse_kms_key_id
- Env Var:     RCLONE_OOS_SSE_KMS_KEY_ID
- Type:        string
- Required:    false
- Examples:
  - ""
    - 无

#### --oos-sse-customer-algorithm

如果使用 SSE-C，指定 "AES256" 作为加密算法的可选请求头。
对象存储支持 "AES256" 作为加密算法。更多信息请参阅使用自有密钥进行服务端加密 (https://docs.cloud.oracle.com/Content/Object/Tasks/usingyourencryptionkeys.htm)。

属性：

- Config:      sse_customer_algorithm
- Env Var:     RCLONE_OOS_SSE_CUSTOMER_ALGORITHM
- Type:        string
- Required:    false
- Examples:
  - ""
    - 无
  - "AES256"
    - AES256

#### --oos-description

远程存储的描述。

属性：

- Config:      description
- Env Var:     RCLONE_OOS_DESCRIPTION
- Type:        string
- Required:    false

### 元数据

用户元数据以 opc-meta- 前缀键存储。

以下是 oracleobjectstorage 后端可能的系统元数据项。

| 名称 | 帮助 | 类型 | 示例 | 只读 |
|------|------|------|---------|-----------|
| opc-meta-atime | 最后访问时间 | ISO 8601 | 2025-06-30T22:27:43-04:00 | N |
| opc-meta-btime | 文件创建（诞生）时间 | ISO 8601 | 2025-06-30T22:27:43-04:00 | N |
| opc-meta-gid | 所有者的组 ID | decimal number | 500 | N |
| opc-meta-mode | 文件类型和模式 | octal, unix style | 0100664 | N |
| opc-meta-mtime | 最后修改时间 | ISO 8601 | 2025-06-30T22:27:43-04:00 | N |
| opc-meta-uid | 所有者的用户 ID | decimal number | 500 | N |

更多信息请参阅[元数据](/docs/#metadata)文档。

## 后端命令

以下是 oracleobjectstorage 后端特有的命令。

运行方式：

```console
rclone backend COMMAND remote:
```

以下帮助将说明每个命令接受的参数。

有关如何传递选项和参数的更多信息，请参阅 [backend](/commands/rclone_backend/) 命令。

这些命令可以在运行中的后端上使用 rc 命令 [backend/command](/rc/#backend-command) 执行。

### rename

更改对象的名称。

```console
rclone backend rename remote: [options] [<arguments>+]
```

此命令可用于重命名对象。

用法示例：

```console
rclone backend rename oos:bucket relative-object-path-under-bucket object-new-name
```

### list-multipart-uploads

列出未完成的分片上传。

```console
rclone backend list-multipart-uploads remote: [options] [<arguments>+]
```

此命令以 JSON 格式列出未完成的分片上传。

用法示例：

```console
rclone backend list-multipart-uploads oos:bucket/path/to/object
```

它返回一个以存储桶为键、未完成分片上传列表为值的字典。

可以在不指定存储桶的情况下调用（此时列出所有存储桶），也可以指定存储桶，或指定存储桶和路径。

```json
{
    "test-bucket": [
        {
            "namespace": "test-namespace",
            "bucket": "test-bucket",
            "object": "600m.bin",
            "uploadId": "51dd8114-52a4-b2f2-c42f-5291f05eb3c8",
            "timeCreated": "2022-07-29T06:21:16.595Z",
            "storageTier": "Standard"
        }
    ]
}

### cleanup

移除未完成的分片上传。

```console
rclone backend cleanup remote: [options] [<arguments>+]
```

此命令移除超过 max-age（默认 24 小时）的未完成分片上传。

注意，你可以使用 --interactive/-i 或 --dry-run 选项来预览此命令将执行的操作。

用法示例：

```console
rclone backend cleanup oos:bucket/path/to/object
rclone backend cleanup -o max-age=7w oos:bucket/path/to/object
```

持续时间按 rclone 的其余部分方式解析，2h、7d、7w 等。

选项：

- "max-age": 要删除的上传的最大存在时间。

### restore

将对象从归档存储恢复到标准存储。

```console
rclone backend restore remote: [options] [<arguments>+]
```

此命令可用于将一个或多个对象从归档存储恢复到标准存储。

用法示例：

```console
rclone backend restore oos:bucket/path/to/directory -o hours=HOURS
rclone backend restore oos:bucket -o hours=HOURS
```

此标志也遵循过滤器规则。先用 --interactive/-i 或 --dry-run 标志测试

```console
rclone --interactive backend restore --include "*.txt" oos:bucket/path -o hours=72
```

显示的所有对象将被标记为待恢复，然后：

```console
rclone backend restore --include "*.txt" oos:bucket/path -o hours=72
```

它返回一个状态字典列表，包含对象名称和状态键。
状态为 "RESTORED" 表示成功，否则为错误消息。

```json
[
    {
        "Object": "test.txt"
        "Status": "RESTORED",
    },
    {
        "Object": "test/file4.txt"
        "Status": "RESTORED",
    }
]
```

选项：

- "hours": 此对象将被恢复的小时数。
默认为 24 小时。

<!-- autogenerated options stop -->

## 教程

### [挂载存储桶](/oracleobjectstorage/tutorial_mount/)
