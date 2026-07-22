---
name: azure-storage-file-share-ts
description: Azure File Share JavaScript/TypeScript SDK (@azure/storage-file-share)，用于 SMB 文件共享操作。当用户要求'Azure文件共享操作'、'SMB文件共享'、'Azure File Share上传下载'、'文件共享目录管理'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# @azure/storage-file-share (TypeScript/JavaScript)

用于 Azure File Share 操作的 SDK — SMB 文件共享、目录和文件操作。

## 安装

```bash
npm install @azure/storage-file-share @azure/identity
```

**当前版本**: 12.x  
**Node.js**: >= 18.0.0

## 环境变量

```bash
AZURE_STORAGE_ACCOUNT_NAME=<account-name>
AZURE_STORAGE_ACCOUNT_KEY=<account-key>
# OR connection string
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
```

## 身份验证

### 连接字符串（最简单）

```typescript
import { ShareServiceClient } from "@azure/storage-file-share";

const client = ShareServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING!
);
```

### StorageSharedKeyCredential（仅 Node.js）

```typescript
import { ShareServiceClient, StorageSharedKeyCredential } from "@azure/storage-file-share";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const accountKey = process.env.AZURE_STORAGE_ACCOUNT_KEY!;

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
const client = new ShareServiceClient(
  `https://${accountName}.file.core.windows.net`,
  sharedKeyCredential
);
```

### DefaultAzureCredential

```typescript
import { ShareServiceClient } from "@azure/storage-file-share";
import { DefaultAzureCredential } from "@azure/identity";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const client = new ShareServiceClient(
  `https://${accountName}.file.core.windows.net`,
  new DefaultAzureCredential()
);
```

### SAS Token

```typescript
import { ShareServiceClient } from "@azure/storage-file-share";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const sasToken = process.env.AZURE_STORAGE_SAS_TOKEN!;

const client = new ShareServiceClient(
  `https://${accountName}.file.core.windows.net${sasToken}`
);
```

## 客户端层级

```
ShareServiceClient (账户级别)
└── ShareClient (共享级别)
    └── ShareDirectoryClient (目录级别)
        └── ShareFileClient (文件级别)
```

## 共享操作

### 创建共享

```typescript
const shareClient = client.getShareClient("my-share");
await shareClient.create();

// Create with quota (in GB)
await shareClient.create({ quota: 100 });
```

### 列出共享

```typescript
for await (const share of client.listShares()) {
  console.log(share.name, share.properties.quota);
}

// With prefix filter
for await (const share of client.listShares({ prefix: "logs-" })) {
  console.log(share.name);
}
```

### 删除共享

```typescript
await shareClient.delete();

// Delete if exists
await shareClient.deleteIfExists();
```

### 获取共享属性

```typescript
const properties = await shareClient.getProperties();
console.log("Quota:", properties.quota, "GB");
console.log("Last Modified:", properties.lastModified);
```

### 设置共享配额

```typescript
await shareClient.setQuota(200); // 200 GB
```

## 目录操作

### 创建目录

```typescript
const directoryClient = shareClient.getDirectoryClient("my-directory");
await directoryClient.create();

// Create nested directory
const nestedDir = shareClient.getDirectoryClient("parent/child/grandchild");
await nestedDir.create();
```

### 列出目录和文件

```typescript
const directoryClient = shareClient.getDirectoryClient("my-directory");

for await (const item of directoryClient.listFilesAndDirectories()) {
  if (item.kind === "directory") {
    console.log(`[DIR] ${item.name}`);
  } else {
    console.log(`[FILE] ${item.name} (${item.properties.contentLength} bytes)`);
  }
}
```

### 删除目录

```typescript
await directoryClient.delete();

// Delete if exists
await directoryClient.deleteIfExists();
```

### 检查目录是否存在

```typescript
const exists = await directoryClient.exists();
if (!exists) {
  await directoryClient.create();
}
```

## 文件操作

### 上传文件（简单方式）

```typescript
const fileClient = shareClient
  .getDirectoryClient("my-directory")
  .getFileClient("my-file.txt");

// Upload string
const content = "Hello, World!";
await fileClient.create(content.length);
await fileClient.uploadRange(content, 0, content.length);
```

### 上传文件（Node.js - 从本地文件）

```typescript
import * as fs from "fs";
import * as path from "path";

const fileClient = shareClient.rootDirectoryClient.getFileClient("uploaded.txt");
const localFilePath = "/path/to/local/file.txt";
const fileSize = fs.statSync(localFilePath).size;

await fileClient.create(fileSize);
await fileClient.uploadFile(localFilePath);
```

### 上传文件（Buffer）

```typescript
const buffer = Buffer.from("Hello, Azure Files!");
const fileClient = shareClient.rootDirectoryClient.getFileClient("buffer-file.txt");

await fileClient.create(buffer.length);
await fileClient.uploadRange(buffer, 0, buffer.length);
```

### 上传文件（Stream）

```typescript
import * as fs from "fs";

const fileClient = shareClient.rootDirectoryClient.getFileClient("streamed.txt");
const readStream = fs.createReadStream("/path/to/local/file.txt");
const fileSize = fs.statSync("/path/to/local/file.txt").size;

await fileClient.create(fileSize);
await fileClient.uploadStream(readStream, fileSize, 4 * 1024 * 1024, 4); // 4MB buffer, 4 concurrency
```

### 下载文件

```typescript
const fileClient = shareClient
  .getDirectoryClient("my-directory")
  .getFileClient("my-file.txt");

const downloadResponse = await fileClient.download();

// Read as string
const chunks: Buffer[] = [];
for await (const chunk of downloadResponse.readableStreamBody!) {
  chunks.push(Buffer.from(chunk));
}
const content = Buffer.concat(chunks).toString("utf-8");
```

### 下载到文件（Node.js）

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
await fileClient.downloadToFile("/path/to/local/destination.txt");
```

### 下载到 Buffer（Node.js）

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
const buffer = await fileClient.downloadToBuffer();
console.log(buffer.toString());
```

### 删除文件

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
await fileClient.delete();

// Delete if exists
await fileClient.deleteIfExists();
```

### 复制文件

```typescript
const sourceUrl = "https://account.file.core.windows.net/share/source.txt";
const destFileClient = shareClient.rootDirectoryClient.getFileClient("destination.txt");

// Start copy operation
const copyPoller = await destFileClient.startCopyFromURL(sourceUrl);
await copyPoller.pollUntilDone();
```

## 文件属性与元数据

### 获取文件属性

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
const properties = await fileClient.getProperties();

console.log("Content-Length:", properties.contentLength);
console.log("Content-Type:", properties.contentType);
console.log("Last Modified:", properties.lastModified);
console.log("ETag:", properties.etag);
```

### 设置元数据

```typescript
await fileClient.setMetadata({
  author: "John Doe",
  category: "documents",
});
```

### 设置 HTTP 头

```typescript
await fileClient.setHttpHeaders({
  fileContentType: "text/plain",
  fileCacheControl: "max-age=3600",
  fileContentDisposition: "attachment; filename=download.txt",
});
```

## 范围操作

### 上传范围

```typescript
const data = Buffer.from("partial content");
await fileClient.uploadRange(data, 100, data.length); // Write at offset 100
```

### 下载范围

```typescript
const downloadResponse = await fileClient.download(100, 50); // offset 100, length 50
```

### 清除范围

```typescript
await fileClient.clearRange(0, 100); // Clear first 100 bytes
```

## 快照操作

### 创建快照

```typescript
const snapshotResponse = await shareClient.createSnapshot();
console.log("Snapshot:", snapshotResponse.snapshot);
```

### 访问快照

```typescript
const snapshotShareClient = shareClient.withSnapshot(snapshotResponse.snapshot!);
const snapshotFileClient = snapshotShareClient.rootDirectoryClient.getFileClient("file.txt");
const content = await snapshotFileClient.downloadToBuffer();
```

### 删除快照

```typescript
await shareClient.delete({ deleteSnapshots: "include" });
```

## SAS Token 生成（仅 Node.js）

### 生成文件 SAS

```typescript
import {
  generateFileSASQueryParameters,
  FileSASPermissions,
  StorageSharedKeyCredential,
} from "@azure/storage-file-share";

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);

const sasToken = generateFileSASQueryParameters(
  {
    shareName: "my-share",
    filePath: "my-directory/my-file.txt",
    permissions: FileSASPermissions.parse("r"), // read only
    expiresOn: new Date(Date.now() + 3600 * 1000), // 1 hour
  },
  sharedKeyCredential
).toString();

const sasUrl = `https://${accountName}.file.core.windows.net/my-share/my-directory/my-file.txt?${sasToken}`;
```

### 生成共享 SAS

```typescript
import { ShareSASPermissions, generateFileSASQueryParameters } from "@azure/storage-file-share";

const sasToken = generateFileSASQueryParameters(
  {
    shareName: "my-share",
    permissions: ShareSASPermissions.parse("rcwdl"), // read, create, write, delete, list
    expiresOn: new Date(Date.now() + 24 * 3600 * 1000), // 24 hours
  },
  sharedKeyCredential
).toString();
```

## 错误处理

```typescript
import { RestError } from "@azure/storage-file-share";

try {
  await shareClient.create();
} catch (error) {
  if (error instanceof RestError) {
    switch (error.statusCode) {
      case 404:
        console.log("Share not found");
        break;
      case 409:
        console.log("Share already exists");
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
  ShareServiceClient,
  ShareClient,
  ShareDirectoryClient,
  ShareFileClient,

  // Authentication
  StorageSharedKeyCredential,
  AnonymousCredential,

  // SAS
  FileSASPermissions,
  ShareSASPermissions,
  AccountSASPermissions,
  AccountSASServices,
  AccountSASResourceTypes,
  generateFileSASQueryParameters,
  generateAccountSASQueryParameters,

  // Options & Responses
  ShareCreateResponse,
  FileDownloadResponseModel,
  DirectoryItem,
  FileItem,
  ShareProperties,
  FileProperties,

  // Errors
  RestError,
} from "@azure/storage-file-share";
```

## 最佳实践

1. **开发环境使用连接字符串** — 最简单的设置方式
2. **生产环境使用 DefaultAzureCredential** — 启用 Azure 托管标识
3. **为共享设置配额** — 防止意外的存储费用
4. **大文件使用流式传输** — 文件超过 256MB 时使用 `uploadStream`/`downloadToFile`
5. **部分更新使用范围操作** — 比替换整个文件更高效
6. **重大变更前创建快照** — 实现时间点恢复
7. **优雅地处理错误** — 检查 `RestError.statusCode` 进行针对性处理
8. **使用 `*IfExists` 方法** — 实现幂等操作

## 平台差异

| 功能 | Node.js | 浏览器 |
|------|---------|--------|
| `StorageSharedKeyCredential` | ✅ | ❌ |
| `uploadFile()` | ✅ | ❌ |
| `uploadStream()` | ✅ | ❌ |
| `downloadToFile()` | ✅ | ❌ |
| `downloadToBuffer()` | ✅ | ❌ |
| SAS 生成 | ✅ | ❌ |
| DefaultAzureCredential | ✅ | ❌ |
| 匿名/SAS 访问 | ✅ | ✅ |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
