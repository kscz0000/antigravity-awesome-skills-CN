---
name: azure-storage-file-share-py
description: Azure Storage File Share Python SDK，用于云端 SMB 文件共享、目录和文件操作。当用户要求'管理Azure文件共享'、'操作SMB文件共享'、'上传下载Azure文件'、'Azure File Share'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Storage File Share SDK for Python

管理 SMB 文件共享，适用于云原生和迁移上云场景。

## 安装

```bash
pip install azure-storage-file-share
```

## 环境变量

```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...
# 或
AZURE_STORAGE_ACCOUNT_URL=https://<account>.file.core.windows.net
```

## 身份验证

### 连接字符串

```python
from azure.storage.fileshare import ShareServiceClient

service = ShareServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)
```

### Entra ID

```python
from azure.storage.fileshare import ShareServiceClient
from azure.identity import DefaultAzureCredential

service = ShareServiceClient(
    account_url=os.environ["AZURE_STORAGE_ACCOUNT_URL"],
    credential=DefaultAzureCredential()
)
```

## 文件共享操作

### 创建共享

```python
share = service.create_share("my-share")
```

### 列出共享

```python
for share in service.list_shares():
    print(f"{share.name}: {share.quota} GB")
```

### 获取共享客户端

```python
share_client = service.get_share_client("my-share")
```

### 删除共享

```python
service.delete_share("my-share")
```

## 目录操作

### 创建目录

```python
share_client = service.get_share_client("my-share")
share_client.create_directory("my-directory")

# 嵌套目录
share_client.create_directory("my-directory/sub-directory")
```

### 列出目录和文件

```python
directory_client = share_client.get_directory_client("my-directory")

for item in directory_client.list_directories_and_files():
    if item["is_directory"]:
        print(f"[DIR] {item['name']}")
    else:
        print(f"[FILE] {item['name']} ({item['size']} bytes)")
```

### 删除目录

```python
share_client.delete_directory("my-directory")
```

## 文件操作

### 上传文件

```python
file_client = share_client.get_file_client("my-directory/file.txt")

# 从字符串
file_client.upload_file("Hello, World!")

# 从本地文件
with open("local-file.txt", "rb") as f:
    file_client.upload_file(f)

# 从字节
file_client.upload_file(b"Binary content")
```

### 下载文件

```python
file_client = share_client.get_file_client("my-directory/file.txt")

# 下载为字节
data = file_client.download_file().readall()

# 下载到文件
with open("downloaded.txt", "wb") as f:
    data = file_client.download_file()
    data.readinto(f)

# 流式分块读取
download = file_client.download_file()
for chunk in download.chunks():
    process(chunk)
```

### 获取文件属性

```python
properties = file_client.get_file_properties()
print(f"Size: {properties.size}")
print(f"Content type: {properties.content_settings.content_type}")
print(f"Last modified: {properties.last_modified}")
```

### 删除文件

```python
file_client.delete_file()
```

### 复制文件

```python
source_url = "https://account.file.core.windows.net/share/source.txt"
dest_client = share_client.get_file_client("destination.txt")
dest_client.start_copy_from_url(source_url)
```

## Range 操作

### 上传 Range

```python
# 上传到指定范围
file_client.upload_range(data=b"content", offset=0, length=7)
```

### 下载 Range

```python
# 下载指定范围
download = file_client.download_file(offset=0, length=100)
data = download.readall()
```

## 快照操作

### 创建快照

```python
snapshot = share_client.create_snapshot()
print(f"Snapshot: {snapshot['snapshot']}")
```

### 访问快照

```python
snapshot_client = service.get_share_client(
    "my-share",
    snapshot=snapshot["snapshot"]
)
```

## 异步客户端

```python
from azure.storage.fileshare.aio import ShareServiceClient
from azure.identity.aio import DefaultAzureCredential

async def upload_file():
    credential = DefaultAzureCredential()
    service = ShareServiceClient(account_url, credential=credential)
    
    share = service.get_share_client("my-share")
    file_client = share.get_file_client("test.txt")
    
    await file_client.upload_file("Hello!")
    
    await service.close()
    await credential.close()
```

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `ShareServiceClient` | 账户级操作 |
| `ShareClient` | 共享操作 |
| `ShareDirectoryClient` | 目录操作 |
| `ShareFileClient` | 文件操作 |

## 最佳实践

1. **使用连接字符串** 进行最简单的配置
2. **使用 Entra ID** 在生产环境中配合 RBAC
3. **流式传输大文件** 使用 chunks() 避免内存问题
4. **创建快照** 在重大变更前
5. **设置配额** 防止意外存储费用
6. **使用 Range** 进行部分文件更新
7. **显式关闭异步客户端**

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
