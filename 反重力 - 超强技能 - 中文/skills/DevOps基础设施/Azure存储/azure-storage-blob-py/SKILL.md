---
name: azure-storage-blob-py
description: Azure Blob Storage Python SDK。用于上传、下载、列出 Blob、管理容器和 Blob 生命周期。当用户要求'上传下载Azure Blob'、'管理Blob容器'、'Azure对象存储操作'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Blob Storage SDK for Python

Azure Blob Storage 的客户端库——用于非结构化数据的对象存储服务。

## 安装

```bash
pip install azure-storage-blob azure-identity
```

## 环境变量

```bash
AZURE_STORAGE_ACCOUNT_NAME=<your-storage-account>
# Or use full URL
AZURE_STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net
```

## 身份认证

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()
account_url = "https://<account>.blob.core.windows.net"

blob_service_client = BlobServiceClient(account_url, credential=credential)
```

## 客户端层级

| 客户端 | 用途 | 获取方式 |
|--------|------|----------|
| `BlobServiceClient` | 账户级操作 | 直接实例化 |
| `ContainerClient` | 容器操作 | `blob_service_client.get_container_client()` |
| `BlobClient` | 单个 Blob 操作 | `container_client.get_blob_client()` |

## 核心工作流

### 创建容器

```python
container_client = blob_service_client.get_container_client("mycontainer")
container_client.create_container()
```

### 上传 Blob

```python
# From file path
blob_client = blob_service_client.get_blob_client(
    container="mycontainer",
    blob="sample.txt"
)

with open("./local-file.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# From bytes/string
blob_client.upload_blob(b"Hello, World!", overwrite=True)

# From stream
import io
stream = io.BytesIO(b"Stream content")
blob_client.upload_blob(stream, overwrite=True)
```

### 下载 Blob

```python
blob_client = blob_service_client.get_blob_client(
    container="mycontainer",
    blob="sample.txt"
)

# To file
with open("./downloaded.txt", "wb") as file:
    download_stream = blob_client.download_blob()
    file.write(download_stream.readall())

# To memory
download_stream = blob_client.download_blob()
content = download_stream.readall()  # bytes

# Read into existing buffer
stream = io.BytesIO()
num_bytes = blob_client.download_blob().readinto(stream)
```

### 列出 Blob

```python
container_client = blob_service_client.get_container_client("mycontainer")

# List all blobs
for blob in container_client.list_blobs():
    print(f"{blob.name} - {blob.size} bytes")

# List with prefix (folder-like)
for blob in container_client.list_blobs(name_starts_with="logs/"):
    print(blob.name)

# Walk blob hierarchy (virtual directories)
for item in container_client.walk_blobs(delimiter="/"):
    if item.get("prefix"):
        print(f"Directory: {item['prefix']}")
    else:
        print(f"Blob: {item.name}")
```

### 删除 Blob

```python
blob_client.delete_blob()

# Delete with snapshots
blob_client.delete_blob(delete_snapshots="include")
```

## 性能调优

```python
# Configure chunk sizes for large uploads/downloads
blob_client = BlobClient(
    account_url=account_url,
    container_name="mycontainer",
    blob_name="large-file.zip",
    credential=credential,
    max_block_size=4 * 1024 * 1024,  # 4 MiB blocks
    max_single_put_size=64 * 1024 * 1024  # 64 MiB single upload limit
)

# Parallel upload
blob_client.upload_blob(data, max_concurrency=4)

# Parallel download
download_stream = blob_client.download_blob(max_concurrency=4)
```

## SAS 令牌

```python
from datetime import datetime, timedelta, timezone
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

sas_token = generate_blob_sas(
    account_name="<account>",
    container_name="mycontainer",
    blob_name="sample.txt",
    account_key="<account-key>",  # Or use user delegation key
    permission=BlobSasPermissions(read=True),
    expiry=datetime.now(timezone.utc) + timedelta(hours=1)
)

# Use SAS token
blob_url = f"https://<account>.blob.core.windows.net/mycontainer/sample.txt?{sas_token}"
```

## Blob 属性与元数据

```python
# Get properties
properties = blob_client.get_blob_properties()
print(f"Size: {properties.size}")
print(f"Content-Type: {properties.content_settings.content_type}")
print(f"Last modified: {properties.last_modified}")

# Set metadata
blob_client.set_blob_metadata(metadata={"category": "logs", "year": "2024"})

# Set content type
from azure.storage.blob import ContentSettings
blob_client.set_http_headers(
    content_settings=ContentSettings(content_type="application/json")
)
```

## 异步客户端

```python
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

async def upload_async():
    credential = DefaultAzureCredential()
    
    async with BlobServiceClient(account_url, credential=credential) as client:
        blob_client = client.get_blob_client("mycontainer", "sample.txt")
        
        with open("./file.txt", "rb") as data:
            await blob_client.upload_blob(data, overwrite=True)

# Download async
async def download_async():
    async with BlobServiceClient(account_url, credential=credential) as client:
        blob_client = client.get_blob_client("mycontainer", "sample.txt")
        
        stream = await blob_client.download_blob()
        data = await stream.readall()
```

## 最佳实践

1. **使用 DefaultAzureCredential** 而非连接字符串
2. **异步客户端使用上下文管理器**
3. **重新上传时显式设置 `overwrite=True`**
4. **大文件传输使用 `max_concurrency`**
5. **内存效率优先使用 `readinto()` 而非 `readall()`**
6. **层级列表使用 `walk_blobs()`**
7. **为 Web 服务的 Blob 设置合适的 Content-Type**

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不能替代针对特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
