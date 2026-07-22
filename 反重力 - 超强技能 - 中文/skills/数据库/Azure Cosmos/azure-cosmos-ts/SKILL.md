---
name: azure-cosmos-ts
description: Azure Cosmos DB JavaScript/TypeScript SDK (@azure/cosmos) 数据平面操作。用于文档 CRUD 操作、查询、批量操作和容器管理。触发词：Cosmos DB、Azure Cosmos、NoSQL API、文档数据库、@azure/cosmos、CosmosClient、分区键、跨分区查询、批量操作、ETag 并发
risk: unknown
source: community
date_added: '2026-02-27'
---

# @azure/cosmos (TypeScript/JavaScript)

Azure Cosmos DB NoSQL API 数据平面操作 SDK — 文档 CRUD、查询、批量操作。

> **⚠️ 数据平面 vs 管理平面**
> - **本 SDK (@azure/cosmos)**：文档 CRUD 操作、查询、存储过程
> - **管理 SDK (@azure/arm-cosmosdb)**：通过 ARM 创建账户、数据库、容器

## 安装

```bash
npm install @azure/cosmos @azure/identity
```

**当前版本**：4.9.0  
**Node.js**：>= 20.0.0

## 环境变量

```bash
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_DATABASE=<database-name>
COSMOS_CONTAINER=<container-name>
# 仅用于基于密钥的认证（推荐使用 AAD）
COSMOS_KEY=<account-key>
```

## 认证

### 使用 DefaultAzureCredential 的 AAD 认证（推荐）

```typescript
import { CosmosClient } from "@azure/cosmos";
import { DefaultAzureCredential } from "@azure/identity";

const client = new CosmosClient({
  endpoint: process.env.COSMOS_ENDPOINT!,
  aadCredentials: new DefaultAzureCredential(),
});
```

### 基于密钥的认证

```typescript
import { CosmosClient } from "@azure/cosmos";

// 方式 1：端点 + 密钥
const client = new CosmosClient({
  endpoint: process.env.COSMOS_ENDPOINT!,
  key: process.env.COSMOS_KEY!,
});

// 方式 2：连接字符串
const client = new CosmosClient(process.env.COSMOS_CONNECTION_STRING!);
```

## 资源层级结构

```
CosmosClient
└── Database
    └── Container
        ├── Items (文档)
        ├── Scripts (存储过程、触发器、UDF)
        └── Conflicts
```

## 核心操作

### 数据库与容器设置

```typescript
const { database } = await client.databases.createIfNotExists({
  id: "my-database",
});

const { container } = await database.containers.createIfNotExists({
  id: "my-container",
  partitionKey: { paths: ["/partitionKey"] },
});
```

### 创建文档

```typescript
interface Product {
  id: string;
  partitionKey: string;
  name: string;
  price: number;
}

const item: Product = {
  id: "product-1",
  partitionKey: "electronics",
  name: "Laptop",
  price: 999.99,
};

const { resource } = await container.items.create<Product>(item);
```

### 读取文档

```typescript
const { resource } = await container
  .item("product-1", "electronics") // id, partitionKey
  .read<Product>();

if (resource) {
  console.log(resource.name);
}
```

### 更新文档（替换）

```typescript
const { resource: existing } = await container
  .item("product-1", "electronics")
  .read<Product>();

if (existing) {
  existing.price = 899.99;
  const { resource: updated } = await container
    .item("product-1", "electronics")
    .replace<Product>(existing);
}
```

### Upsert 文档

```typescript
const item: Product = {
  id: "product-1",
  partitionKey: "electronics",
  name: "Laptop Pro",
  price: 1299.99,
};

const { resource } = await container.items.upsert<Product>(item);
```

### 删除文档

```typescript
await container.item("product-1", "electronics").delete();
```

### Patch 文档（部分更新）

```typescript
import { PatchOperation } from "@azure/cosmos";

const operations: PatchOperation[] = [
  { op: "replace", path: "/price", value: 799.99 },
  { op: "add", path: "/discount", value: true },
  { op: "remove", path: "/oldField" },
];

const { resource } = await container
  .item("product-1", "electronics")
  .patch<Product>(operations);
```

## 查询

### 简单查询

```typescript
const { resources } = await container.items
  .query<Product>("SELECT * FROM c WHERE c.price < 1000")
  .fetchAll();
```

### 参数化查询（推荐）

```typescript
import { SqlQuerySpec } from "@azure/cosmos";

const querySpec: SqlQuerySpec = {
  query: "SELECT * FROM c WHERE c.partitionKey = @category AND c.price < @maxPrice",
  parameters: [
    { name: "@category", value: "electronics" },
    { name: "@maxPrice", value: 1000 },
  ],
};

const { resources } = await container.items
  .query<Product>(querySpec)
  .fetchAll();
```

### 分页查询

```typescript
const queryIterator = container.items.query<Product>(querySpec, {
  maxItemCount: 10, // 每页条目数
});

while (queryIterator.hasMoreResults()) {
  const { resources, continuationToken } = await queryIterator.fetchNext();
  console.log(`Page with ${resources?.length} items`);
  // 如需要，使用 continuationToken 获取下一页
}
```

### 跨分区查询

```typescript
const { resources } = await container.items
  .query<Product>(
    "SELECT * FROM c WHERE c.price > 500",
    { enableCrossPartitionQuery: true }
  )
  .fetchAll();
```

## 批量操作

### 执行批量操作

```typescript
import { BulkOperationType, OperationInput } from "@azure/cosmos";

const operations: OperationInput[] = [
  {
    operationType: BulkOperationType.Create,
    resourceBody: { id: "1", partitionKey: "cat-a", name: "Item 1" },
  },
  {
    operationType: BulkOperationType.Upsert,
    resourceBody: { id: "2", partitionKey: "cat-a", name: "Item 2" },
  },
  {
    operationType: BulkOperationType.Read,
    id: "3",
    partitionKey: "cat-b",
  },
  {
    operationType: BulkOperationType.Replace,
    id: "4",
    partitionKey: "cat-b",
    resourceBody: { id: "4", partitionKey: "cat-b", name: "Updated" },
  },
  {
    operationType: BulkOperationType.Delete,
    id: "5",
    partitionKey: "cat-c",
  },
  {
    operationType: BulkOperationType.Patch,
    id: "6",
    partitionKey: "cat-c",
    resourceBody: {
      operations: [{ op: "replace", path: "/name", value: "Patched" }],
    },
  },
];

const response = await container.items.executeBulkOperations(operations);

response.forEach((result, index) => {
  if (result.statusCode >= 200 && result.statusCode < 300) {
    console.log(`Operation ${index} succeeded`);
  } else {
    console.error(`Operation ${index} failed: ${result.statusCode}`);
  }
});
```

## 分区键

### 简单分区键

```typescript
const { container } = await database.containers.createIfNotExists({
  id: "products",
  partitionKey: { paths: ["/category"] },
});
```

### 层级分区键（MultiHash）

```typescript
import { PartitionKeyDefinitionVersion, PartitionKeyKind } from "@azure/cosmos";

const { container } = await database.containers.createIfNotExists({
  id: "orders",
  partitionKey: {
    paths: ["/tenantId", "/userId", "/sessionId"],
    version: PartitionKeyDefinitionVersion.V2,
    kind: PartitionKeyKind.MultiHash,
  },
});

// 操作需要分区键值数组
const { resource } = await container.items.create({
  id: "order-1",
  tenantId: "tenant-a",
  userId: "user-123",
  sessionId: "session-xyz",
  total: 99.99,
});

// 使用层级分区键读取
const { resource: order } = await container
  .item("order-1", ["tenant-a", "user-123", "session-xyz"])
  .read();
```

## 错误处理

```typescript
import { ErrorResponse } from "@azure/cosmos";

try {
  const { resource } = await container.item("missing", "pk").read();
} catch (error) {
  if (error instanceof ErrorResponse) {
    switch (error.code) {
      case 404:
        console.log("Document not found");
        break;
      case 409:
        console.log("Conflict - document already exists");
        break;
      case 412:
        console.log("Precondition failed (ETag mismatch)");
        break;
      case 429:
        console.log("Rate limited - retry after:", error.retryAfterInMs);
        break;
      default:
        console.error(`Cosmos error ${error.code}: ${error.message}`);
    }
  }
  throw error;
}
```

## 乐观并发（ETags）

```typescript
// 带 ETag 读取
const { resource, etag } = await container
  .item("product-1", "electronics")
  .read<Product>();

if (resource && etag) {
  resource.price = 899.99;
  
  try {
    // 仅当 ETag 匹配时替换
    await container.item("product-1", "electronics").replace(resource, {
      accessCondition: { type: "IfMatch", condition: etag },
    });
  } catch (error) {
    if (error instanceof ErrorResponse && error.code === 412) {
      console.log("Document was modified by another process");
    }
  }
}
```

## TypeScript 类型参考

```typescript
import {
  // 客户端与资源
  CosmosClient,
  Database,
  Container,
  Item,
  Items,
  
  // 操作
  OperationInput,
  BulkOperationType,
  PatchOperation,
  
  // 查询
  SqlQuerySpec,
  SqlParameter,
  FeedOptions,
  
  // 分区键
  PartitionKeyDefinition,
  PartitionKeyDefinitionVersion,
  PartitionKeyKind,
  
  // 响应
  ItemResponse,
  FeedResponse,
  ResourceResponse,
  
  // 错误
  ErrorResponse,
} from "@azure/cosmos";
```

## 最佳实践

1. **使用 AAD 认证** — 优先使用 `DefaultAzureCredential` 而非密钥
2. **始终使用参数化查询** — 防止注入，改善计划缓存
3. **指定分区键** — 尽可能避免跨分区查询
4. **使用批量操作** — 多次写入时使用 `executeBulkOperations`
5. **处理 429 错误** — 实现指数退避重试逻辑
6. **使用 ETags 处理并发** — 防止并发场景下的更新丢失
7. **关闭时释放客户端** — 在清理时调用 `client.dispose()`

## 常见模式

### 服务层模式

```typescript
export class ProductService {
  private container: Container;

  constructor(client: CosmosClient) {
    this.container = client
      .database(process.env.COSMOS_DATABASE!)
      .container(process.env.COSMOS_CONTAINER!);
  }

  async getById(id: string, category: string): Promise<Product | null> {
    try {
      const { resource } = await this.container
        .item(id, category)
        .read<Product>();
      return resource ?? null;
    } catch (error) {
      if (error instanceof ErrorResponse && error.code === 404) {
        return null;
      }
      throw error;
    }
  }

  async create(product: Omit<Product, "id">): Promise<Product> {
    const item = { ...product, id: crypto.randomUUID() };
    const { resource } = await this.container.items.create<Product>(item);
    return resource!;
  }

  async findByCategory(category: string): Promise<Product[]> {
    const querySpec: SqlQuerySpec = {
      query: "SELECT * FROM c WHERE c.partitionKey = @category",
      parameters: [{ name: "@category", value: category }],
    };
    const { resources } = await this.container.items
      .query<Product>(querySpec)
      .fetchAll();
    return resources;
  }
}
```

## 相关 SDK

| SDK | 用途 | 安装命令 |
|-----|------|---------|
| `@azure/cosmos` | 数据平面（本 SDK） | `npm install @azure/cosmos` |
| `@azure/arm-cosmosdb` | 管理平面（ARM） | `npm install @azure/arm-cosmosdb` |
| `@azure/identity` | 认证 | `npm install @azure/identity` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不应替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
