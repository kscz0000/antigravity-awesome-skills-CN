---
name: azure-storage-blob-ts
description: Azure Blob Storage JavaScript/TypeScript SDK（@azure/storage-blob）用于 Blob 操作。支持上传、下载、列出和管理 Blob 及容器。当用户要求'Azure Blob Storage操作'、'上传下载Blob'、'管理Azure存储容器'、'使用@azure/storage-blob'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# @azure/storage-blob (TypeScript/JavaScript)

Azure Blob Storage 操作 SDK — 上传、下载、列出和管理 Blob 及容器。

## 安装

```bash
npm install @azure/storage-blob @azure/identity
```

**当前版本**：12.x  
**Node.js**：>= 18.0.0

## 环境变量

```bash
AZURE_STORAGE_ACCOUNT_NAME=<account-name>
AZURE_STORAGE_ACCOUNT_KEY=<account-key>
# 或连接字符串
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
```

## 身份认证

### DefaultAzureCredential（推荐）

```typescript
import { BlobServiceClient } from "@azure/storage-blob";
import { DefaultAzureCredential } from "@azure/identity";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const client = new BlobServiceClient(
  `https://${accountName}.blob.core.windows.net`,
  new DefaultAzureCredential()
);
```

### 连接字符串

```typescript
import { BlobServiceClient } from "@azure/storage-blob";

const client = BlobServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING!
);
```

### StorageSharedKeyCredential（仅 Node.js）

```typescript
import { BlobServiceClient, StorageSharedKeyCredential } from "@azure/storage-blob";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const accountKey = process.env.AZURE_STORAGE_ACCOUNT_KEY!;

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
const client = new BlobServiceClient(
  `https://${accountName}.blob.core.windows.net`,
  sharedKeyCredential
);
```

### SAS Token

```typescript
import { BlobServiceClient } from "@azure/storage-blob";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const sasToken = process.env.AZURE_STORAGE_SAS_TOKEN!; // 以 "?" 开头

const client = new BlobServiceClient(
  `https://${accountName}.blob.core.windows.net${sasToken}`
);
```

## 客户端层级

```
BlobServiceClient（账户级别）
└── ContainerClient（容器级别）
    └── BlobClient（Blob 级别）
        ├── BlockBlobClient（块 Blob — 最常用）
        ├── AppendBlobClient（追加 Blob）
        └── PageBlobClient（页 Blob — VHD）
```

## 容器操作

### 创建容器

```typescript
const containerClient = client.getContainerClient("my-container");
await containerClient.create();

// 或不存在时创建
await containerClient.createIfNotExists();
```

### 列出容器

```typescript
for await (const container of client.listContainers()) {
  console.log(container.name);
}

// 使用前缀筛选
for await (const container of client.listContainers({ prefix: "logs-" })) {
  console.log(container.name);
}
```

### 删除容器

```typescript
await containerClient.delete();
// 或存在时删除
await containerClient.deleteIfExists();
```

## Blob 操作

### 上传 Blob（简单）

```typescript
const containerClient = client.getContainerClient("my-container");
const blockBlobClient = containerClient.getBlockBlobClient("my-file.txt");

// 上传字符串
await blockBlobClient.upload("Hello, World!", 13);

// 上传 Buffer
const buffer = Buffer.from("Hello, World!");
await blockBlobClient.upload(buffer, buffer.length);
```

### 从文件上传（仅 Node.js）

```typescript
const blockBlobClient = containerClient.getBlockBlobClient("uploaded-file.txt");
await blockBlobClient.uploadFile("/path/to/local/file.txt");
```

### 从流上传（仅 Node.js）

```typescript
import * as fs from "fs";

const blockBlobClient = containerClient.getBlockBlobClient("streamed-file.txt");
const readStream = fs.createReadStream("/path/to/local/file.txt");

await blockBlobClient.uploadStream(readStream, 4 * 1024 * 1024, 5, {
  // bufferSize: 4MB, maxConcurrency: 5
  onProgress: (progress) => console.log(`Uploaded ${progress.loadedBytes} bytes`),
});
```

### 从浏览器上传

```typescript
const blockBlobClient = containerClient.getBlockBlobClient("browser-upload.txt");

// 从 File 输入
const fileInput = document.getElementById("fileInput") as HTMLInputElement;
const file = fileInput.files![0];
await blockBlobClient.uploadData(file);

// 从 Blob/ArrayBuffer
const arrayBuffer = new ArrayBuffer(1024);
await blockBlobClient.uploadData(arrayBuffer);
```

### 下载 Blob

```typescript
const blobClient = containerClient.getBlobClient("my-file.txt");
const downloadResponse = await blobClient.download();

// 读取为字符串（浏览器和 Node.js）
const downloaded = await streamToText(downloadResponse.readableStreamBody!);

async function streamToText(readable: NodeJS.ReadableStream): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of readable) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf-8");
}
```

### 下载到文件（仅 Node.js）

```typescript
const blockBlobClient = containerClient.getBlockBlobClient("my-file.txt");
await blockBlobClient.downloadToFile("/path/to/local/destination.txt");
```

### 下载到 Buffer（仅 Node.js）

```typescript
const blockBlobClient = containerClient.getBlockBlobClient("my-file.txt");
const buffer = await blockBlobClient.downloadToBuffer();
console.log(buffer.toString());
```

### 列出 Blob

```typescript
// 列出所有 Blob
for await (const blob of containerClient.listBlobsFlat()) {
  console.log(blob.name, blob.properties.contentLength);
}

// 使用前缀列出
for await (const blob of containerClient.listBlobsFlat({ prefix: "logs/" })) {
  console.log(blob.name);
}

// 按层级列出（虚拟目录）
for await (const item of containerClient.listBlobsByHierarchy("/")) {
  if (item.kind === "prefix") {
    console.log(`Directory: ${item.name}`);
  } else {
    console.log(`Blob: ${item.name}`);
  }
}
```

### 删除 Blob

```typescript
const blobClient = containerClient.getBlobClient("my-file.txt");
await blobClient.delete();

// 存在时删除
await blobClient.deleteIfExists();

// 连同快照一起删除
await blobClient.delete({ deleteSnapshots: "include" });
```

### 复制 Blob

```typescript
const sourceBlobClient = containerClient.getBlobClient("source.txt");
const destBlobClient = containerClient.getBlobClient("destination.txt");

// 启动复制操作
const copyPoller = await destBlobClient.beginCopyFromURL(sourceBlobClient.url);
await copyPoller.pollUntilDone();
```

## Blob 属性与元数据

### 获取属性

```typescript
const blobClient = containerClient.getBlobClient("my-file.txt");
const properties = await blobClient.getProperties();

console.log("Content-Type:", properties.contentType);
console.log("Content-Length:", properties.contentLength);
console.log("Last Modified:", properties.lastModified);
console.log("ETag:", properties.etag);
```

### 设置元数据

```typescript
await blobClient.setMetadata({
  author: "John Doe",
  category: "documents",
});
```

### 设置 HTTP 头

```typescript
await blobClient.setHTTPHeaders({
  blobContentType: "text/plain",
  blobCacheControl: "max-age=3600",
  blobContentDisposition: "attachment; filename=download.txt",
});
```

## SAS Token 生成（仅 Node.js）

### 生成 Blob SAS

```typescript
import {
  BlobSASPermissions,
  generateBlobSASQueryParameters,
  StorageSharedKeyCredential,
} from "@azure/storage-blob";

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);

const sasToken = generateBlobSASQueryParameters(
  {
    containerName: "my-container",
    blobName: "my-file.txt",
    permissions: BlobSASPermissions.parse("r"), // 只读
    startsOn: new Date(),
    expiresOn: new Date(Date.now() + 3600 * 1000), // 1 小时
  },
  sharedKeyCredential
).toString();

const sasUrl = `https://${accountName}.blob.core.windows.net/my-container/my-file.txt?${sasToken}`;
```

### 生成容器 SAS

```typescript
import { ContainerSASPermissions, generateBlobSASQueryParameters } from "@azure/storage-blob";

const sasToken = generateBlobSASQueryParameters(
  {
    containerName: "my-container",
    permissions: ContainerSASPermissions.parse("racwdl"), // 读取、追加、创建、写入、删除、列出
    expiresOn: new Date(Date.now() + 24 * 3600 * 1000), // 24 小时
  },
  sharedKeyCredential
).toString();
```

### 生成账户 SAS

```typescript
import {
  AccountSASPermissions,
  AccountSASResourceTypes,
  AccountSASServices,
  generateAccountSASQueryParameters,
} from "@azure/storage-blob";

const sasToken = generateAccountSASQueryParameters(
  {
    services: AccountSASServices.parse("b").toString(), // blob
    resourceTypes: AccountSASResourceTypes.parse("sco").toString(), // service, container, object
    permissions: AccountSASPermissions.parse("rwdlacupi"), // 所有权限
    expiresOn: new Date(Date.now() + 24 * 3600 * 1000),
  },
  sharedKeyCredential
).toString();
```

## Blob 类型

### 块 Blob（默认）

文本和二进制文件最常用的类型。

```typescript
const blockBlobClient = containerClient.getBlockBlobClient("document.pdf");
await blockBlobClient.uploadFile("/path/to/document.pdf");
```

### 追加 Blob

针对追加操作优化（日志、审计追踪）。

```typescript
const appendBlobClient = containerClient.getAppendBlobClient("app.log");

// 创建追加 Blob
await appendBlobClient.create();

// 追加数据
await appendBlobClient.appendBlock("Log entry 1\n", 12);
await appendBlobClient.appendBlock("Log entry 2\n", 12);
```

### 页 Blob

用于随机读写的固定大小 Blob（VHD）。

```typescript
const pageBlobClient = containerClient.getPageBlobClient("disk.vhd");

// 创建 512 字节对齐的页 Blob
await pageBlobClient.create(1024 * 1024); // 1MB

// 写入页（必须 512 字节对齐）
const buffer = Buffer.alloc(512);
await pageBlobClient.uploadPages(buffer, 0, 512);
```

## 错误处理

```typescript
import { RestError } from "@azure/storage-blob";

try {
  await containerClient.create();
} catch (error) {
  if (error instanceof RestError) {
    switch (error.statusCode) {
      case 404:
        console.log("Container not found");
        break;
      case 409:
        console.log("Container already exists");
        break;
      case 403:
        console.log("Access denied");
        break;
      default:
        console.error(`Storage error ${error.statusCode}: ${error.message}`);
    }
  }
  throw error;
}
```

## TypeScript 类型参考

```typescript
import {
  // Clients
  BlobServiceClient,
  ContainerClient,
  BlobClient,
  BlockBlobClient,
  AppendBlobClient,
  PageBlobClient,

  // Authentication
  StorageSharedKeyCredential,
  AnonymousCredential,

  // SAS
  BlobSASPermissions,
  ContainerSASPermissions,
  AccountSASPermissions,
  AccountSASServices,
  AccountSASResourceTypes,
  generateBlobSASQueryParameters,
  generateAccountSASQueryParameters,

  // Options & Responses
  BlobDownloadResponseParsed,
  BlobUploadCommonResponse,
  ContainerCreateResponse,
  BlobItem,
  ContainerItem,

  // Errors
  RestError,
} from "@azure/storage-blob";
```

## 最佳实践

1. **使用 DefaultAzureCredential** — 优先使用 AAD 而非连接字符串/密钥
2. **大文件使用流式传输** — 文件超过 256MB 时使用 `uploadStream`/`downloadToFile`
3. **设置正确的内容类型** — 使用 `setHTTPHeaders` 设置正确的 MIME 类型
4. **客户端访问使用 SAS Token** — 为浏览器上传生成短期 Token
5. **优雅处理错误** — 检查 `RestError.statusCode` 进行针对性处理
6. **使用 `*IfNotExists` 方法** — 实现幂等的容器/Blob 创建
7. **关闭客户端** — 非必需但在长时间运行的应用中是好习惯

## 平台差异

| 功能 | Node.js | 浏览器 |
|------|---------|--------|
| `StorageSharedKeyCredential` | ✅ | ❌ |
| `uploadFile()` | ✅ | ❌ |
| `uploadStream()` | ✅ | ❌ |
| `downloadToFile()` | ✅ | ❌ |
| `downloadToBuffer()` | ✅ | ❌ |
| `uploadData()` | ✅ | ✅ |
| SAS 生成 | ✅ | ❌ |
| DefaultAzureCredential | ✅ | ❌ |
| 匿名/SAS 访问 | ✅ | ✅ |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
