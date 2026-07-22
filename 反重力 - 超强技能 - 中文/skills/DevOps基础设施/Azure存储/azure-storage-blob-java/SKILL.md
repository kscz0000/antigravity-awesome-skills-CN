---
name: azure-storage-blob-java
description: "使用 Azure Storage Blob SDK for Java 构建 Blob 存储应用程序。当用户要求'Azure Blob Storage Java开发'、'上传下载Blob'、'Blob容器SDK'、'存储流式操作'、'SAS令牌生成'、'Blob元数据属性'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Storage Blob SDK for Java

使用 Azure Storage Blob SDK for Java 构建 Blob 存储应用程序。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-storage-blob</artifactId>
    <version>12.33.0</version>
</dependency>
```

## 客户端创建

### BlobServiceClient

```java
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;

// 使用 SAS 令牌
BlobServiceClient serviceClient = new BlobServiceClientBuilder()
    .endpoint("<storage-account-url>")
    .sasToken("<sas-token>")
    .buildClient();

// 使用连接字符串
BlobServiceClient serviceClient = new BlobServiceClientBuilder()
    .connectionString("<connection-string>")
    .buildClient();
```

### 使用 DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

BlobServiceClient serviceClient = new BlobServiceClientBuilder()
    .endpoint("<storage-account-url>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

### BlobContainerClient

```java
import com.azure.storage.blob.BlobContainerClient;

// 从服务客户端创建
BlobContainerClient containerClient = serviceClient.getBlobContainerClient("mycontainer");

// 直接构建
BlobContainerClient containerClient = new BlobContainerClientBuilder()
    .connectionString("<connection-string>")
    .containerName("mycontainer")
    .buildClient();
```

### BlobClient

```java
import com.azure.storage.blob.BlobClient;

// 从容器客户端创建
BlobClient blobClient = containerClient.getBlobClient("myblob.txt");

// 带目录结构
BlobClient blobClient = containerClient.getBlobClient("folder/subfolder/myblob.txt");

// 直接构建
BlobClient blobClient = new BlobClientBuilder()
    .connectionString("<connection-string>")
    .containerName("mycontainer")
    .blobName("myblob.txt")
    .buildClient();
```

## 核心模式

### 创建容器

```java
// 创建容器
serviceClient.createBlobContainer("mycontainer");

// 不存在时创建
BlobContainerClient container = serviceClient.createBlobContainerIfNotExists("mycontainer");

// 从容器客户端创建
containerClient.create();
containerClient.createIfNotExists();
```

### 上传数据

```java
import com.azure.core.util.BinaryData;

// 上传字符串
String data = "Hello, Azure Blob Storage!";
blobClient.upload(BinaryData.fromString(data));

// 上传并覆盖
blobClient.upload(BinaryData.fromString(data), true);
```

### 从文件上传

```java
blobClient.uploadFromFile("local-file.txt");

// 带覆盖
blobClient.uploadFromFile("local-file.txt", true);
```

### 从流上传

```java
import com.azure.storage.blob.specialized.BlockBlobClient;

BlockBlobClient blockBlobClient = blobClient.getBlockBlobClient();

try (ByteArrayInputStream dataStream = new ByteArrayInputStream(data.getBytes())) {
    blockBlobClient.upload(dataStream, data.length());
}
```

### 带选项上传

```java
import com.azure.storage.blob.models.BlobHttpHeaders;
import com.azure.storage.blob.options.BlobParallelUploadOptions;

BlobHttpHeaders headers = new BlobHttpHeaders()
    .setContentType("text/plain")
    .setCacheControl("max-age=3600");

Map<String, String> metadata = Map.of("author", "john", "version", "1.0");

try (InputStream stream = new FileInputStream("large-file.bin")) {
    BlobParallelUploadOptions options = new BlobParallelUploadOptions(stream)
        .setHeaders(headers)
        .setMetadata(metadata);
    
    blobClient.uploadWithResponse(options, null, Context.NONE);
}
```

### 不存在时上传

```java
import com.azure.storage.blob.models.BlobRequestConditions;

BlobParallelUploadOptions options = new BlobParallelUploadOptions(inputStream, length)
    .setRequestConditions(new BlobRequestConditions().setIfNoneMatch("*"));

blobClient.uploadWithResponse(options, null, Context.NONE);
```

### 下载数据

```java
// 下载到 BinaryData
BinaryData content = blobClient.downloadContent();
String text = content.toString();

// 下载到文件
blobClient.downloadToFile("downloaded-file.txt");
```

### 下载到流

```java
try (ByteArrayOutputStream outputStream = new ByteArrayOutputStream()) {
    blobClient.downloadStream(outputStream);
    byte[] data = outputStream.toByteArray();
}
```

### 使用 InputStream 下载

```java
import com.azure.storage.blob.specialized.BlobInputStream;

try (BlobInputStream blobIS = blobClient.openInputStream()) {
    byte[] buffer = new byte[1024];
    int bytesRead;
    while ((bytesRead = blobIS.read(buffer)) != -1) {
        // 处理缓冲区
    }
}
```

### 通过 OutputStream 上传

```java
import com.azure.storage.blob.specialized.BlobOutputStream;

try (BlobOutputStream blobOS = blobClient.getBlockBlobClient().getBlobOutputStream()) {
    blobOS.write("Data to upload".getBytes());
}
```

### 列出 Blob

```java
import com.azure.storage.blob.models.BlobItem;

// 列出所有 Blob
for (BlobItem blobItem : containerClient.listBlobs()) {
    System.out.println("Blob: " + blobItem.getName());
}

// 按前缀列出（虚拟目录）
import com.azure.storage.blob.models.ListBlobsOptions;

ListBlobsOptions options = new ListBlobsOptions().setPrefix("folder/");
for (BlobItem blobItem : containerClient.listBlobs(options, null)) {
    System.out.println("Blob: " + blobItem.getName());
}
```

### 按层级列出 Blob

```java
import com.azure.storage.blob.models.BlobListDetails;

String delimiter = "/";
ListBlobsOptions options = new ListBlobsOptions()
    .setPrefix("data/")
    .setDetails(new BlobListDetails().setRetrieveMetadata(true));

for (BlobItem item : containerClient.listBlobsByHierarchy(delimiter, options, null)) {
    if (item.isPrefix()) {
        System.out.println("Directory: " + item.getName());
    } else {
        System.out.println("Blob: " + item.getName());
    }
}
```

### 删除 Blob

```java
blobClient.delete();

// 存在时删除
blobClient.deleteIfExists();

// 连同快照一起删除
import com.azure.storage.blob.models.DeleteSnapshotsOptionType;
blobClient.deleteWithResponse(DeleteSnapshotsOptionType.INCLUDE, null, null, Context.NONE);
```

### 复制 Blob

```java
import com.azure.storage.blob.models.BlobCopyInfo;
import com.azure.core.util.polling.SyncPoller;

// 异步复制（适用于大型 Blob 或跨账户）
SyncPoller<BlobCopyInfo, Void> poller = blobClient.beginCopy("<source-blob-url>", Duration.ofSeconds(1));
poller.waitForCompletion();

// 从 URL 同步复制（适用于同账户）
blobClient.copyFromUrl("<source-blob-url>");
```

### 生成 SAS 令牌

```java
import com.azure.storage.blob.sas.*;
import java.time.OffsetDateTime;

// Blob 级别 SAS
BlobSasPermission permissions = new BlobSasPermission().setReadPermission(true);
OffsetDateTime expiry = OffsetDateTime.now().plusDays(1);

BlobServiceSasSignatureValues sasValues = new BlobServiceSasSignatureValues(expiry, permissions);
String sasToken = blobClient.generateSas(sasValues);

// 容器级别 SAS
BlobContainerSasPermission containerPermissions = new BlobContainerSasPermission()
    .setReadPermission(true)
    .setListPermission(true);
    
BlobServiceSasSignatureValues containerSasValues = new BlobServiceSasSignatureValues(expiry, containerPermissions);
String containerSas = containerClient.generateSas(containerSasValues);
```

### Blob 属性与元数据

```java
import com.azure.storage.blob.models.BlobProperties;

// 获取属性
BlobProperties properties = blobClient.getProperties();
System.out.println("Size: " + properties.getBlobSize());
System.out.println("Content-Type: " + properties.getContentType());
System.out.println("Last Modified: " + properties.getLastModified());

// 设置元数据
Map<String, String> metadata = Map.of("key1", "value1", "key2", "value2");
blobClient.setMetadata(metadata);

// 设置 HTTP 头
BlobHttpHeaders headers = new BlobHttpHeaders()
    .setContentType("application/json")
    .setCacheControl("max-age=86400");
blobClient.setHttpHeaders(headers);
```

### 租约 Blob

```java
import com.azure.storage.blob.specialized.BlobLeaseClient;
import com.azure.storage.blob.specialized.BlobLeaseClientBuilder;

BlobLeaseClient leaseClient = new BlobLeaseClientBuilder()
    .blobClient(blobClient)
    .buildClient();

// 获取租约（-1 表示无限期）
String leaseId = leaseClient.acquireLease(60);

// 续约
leaseClient.renewLease();

// 释放租约
leaseClient.releaseLease();
```

## 错误处理

```java
import com.azure.storage.blob.models.BlobStorageException;

try {
    blobClient.download(outputStream);
} catch (BlobStorageException e) {
    System.out.println("Status: " + e.getStatusCode());
    System.out.println("Error code: " + e.getErrorCode());
    // 404 = Blob 未找到
    // 409 = 冲突（租约等）
}
```

## 代理配置

```java
import com.azure.core.http.ProxyOptions;
import com.azure.core.http.netty.NettyAsyncHttpClientBuilder;
import java.net.InetSocketAddress;

ProxyOptions proxyOptions = new ProxyOptions(
    ProxyOptions.Type.HTTP,
    new InetSocketAddress("localhost", 8888));

BlobServiceClient client = new BlobServiceClientBuilder()
    .endpoint("<endpoint>")
    .sasToken("<sas-token>")
    .httpClient(new NettyAsyncHttpClientBuilder().proxy(proxyOptions).build())
    .buildClient();
```

## 环境变量

```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net
```

## 触发短语

- "Azure Blob Storage Java"
- "上传下载Blob"
- "Blob容器SDK"
- "存储流式操作"
- "SAS令牌生成"
- "Blob元数据属性"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
