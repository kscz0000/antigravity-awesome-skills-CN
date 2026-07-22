---
name: azure-data-tables-py
description: Azure Tables Python SDK（Storage 和 Cosmos DB）。用于 NoSQL 键值存储、实体 CRUD 和批量操作。当用户要求'Azure Tables'、'Cosmos DB Table API'、'NoSQL键值存储'、'实体CRUD'或'批量表操作'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Tables SDK for Python

用于结构化数据的 NoSQL 键值存储（Azure Storage Tables 或 Cosmos DB Table API）。

## 安装

```bash
pip install azure-data-tables azure-identity
```

## 环境变量

```bash
# Azure Storage Tables
AZURE_STORAGE_ACCOUNT_URL=https://<account>.table.core.windows.net

# Cosmos DB Table API
COSMOS_TABLE_ENDPOINT=https://<account>.table.cosmos.azure.com
```

## 身份认证

```python
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient, TableClient

credential = DefaultAzureCredential()
endpoint = "https://<account>.table.core.windows.net"

# Service client (manage tables)
service_client = TableServiceClient(endpoint=endpoint, credential=credential)

# Table client (work with entities)
table_client = TableClient(endpoint=endpoint, table_name="mytable", credential=credential)
```

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `TableServiceClient` | 创建/删除表、列出表 |
| `TableClient` | 实体 CRUD、查询 |

## 表操作

```python
# Create table
service_client.create_table("mytable")

# Create if not exists
service_client.create_table_if_not_exists("mytable")

# Delete table
service_client.delete_table("mytable")

# List tables
for table in service_client.list_tables():
    print(table.name)

# Get table client
table_client = service_client.get_table_client("mytable")
```

## 实体操作

**重要**：每个实体都需要 `PartitionKey` 和 `RowKey`（两者共同构成唯一 ID）。

### 创建实体

```python
entity = {
    "PartitionKey": "sales",
    "RowKey": "order-001",
    "product": "Widget",
    "quantity": 5,
    "price": 9.99,
    "shipped": False
}

# Create (fails if exists)
table_client.create_entity(entity=entity)

# Upsert (create or replace)
table_client.upsert_entity(entity=entity)
```

### 获取实体

```python
# Get by key (fastest)
entity = table_client.get_entity(
    partition_key="sales",
    row_key="order-001"
)
print(f"Product: {entity['product']}")
```

### 更新实体

```python
# Replace entire entity
entity["quantity"] = 10
table_client.update_entity(entity=entity, mode="replace")

# Merge (update specific fields only)
update = {
    "PartitionKey": "sales",
    "RowKey": "order-001",
    "shipped": True
}
table_client.update_entity(entity=update, mode="merge")
```

### 删除实体

```python
table_client.delete_entity(
    partition_key="sales",
    row_key="order-001"
)
```

## 查询实体

### 分区内查询

```python
# Query by partition (efficient)
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales'"
)
for entity in entities:
    print(entity)
```

### 带过滤条件查询

```python
# Filter by properties
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales' and quantity gt 3"
)

# With parameters (safer)
entities = table_client.query_entities(
    query_filter="PartitionKey eq @pk and price lt @max_price",
    parameters={"pk": "sales", "max_price": 50.0}
)
```

### 选择特定属性

```python
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales'",
    select=["RowKey", "product", "price"]
)
```

### 列出所有实体

```python
# List all (cross-partition - use sparingly)
for entity in table_client.list_entities():
    print(entity)
```

## 批量操作

```python
from azure.data.tables import TableTransactionError

# Batch operations (same partition only!)
operations = [
    ("create", {"PartitionKey": "batch", "RowKey": "1", "data": "first"}),
    ("create", {"PartitionKey": "batch", "RowKey": "2", "data": "second"}),
    ("upsert", {"PartitionKey": "batch", "RowKey": "3", "data": "third"}),
]

try:
    table_client.submit_transaction(operations)
except TableTransactionError as e:
    print(f"Transaction failed: {e}")
```

## 异步客户端

```python
from azure.data.tables.aio import TableServiceClient, TableClient
from azure.identity.aio import DefaultAzureCredential

async def table_operations():
    credential = DefaultAzureCredential()
    
    async with TableClient(
        endpoint="https://<account>.table.core.windows.net",
        table_name="mytable",
        credential=credential
    ) as client:
        # Create
        await client.create_entity(entity={
            "PartitionKey": "async",
            "RowKey": "1",
            "data": "test"
        })
        
        # Query
        async for entity in client.query_entities("PartitionKey eq 'async'"):
            print(entity)

import asyncio
asyncio.run(table_operations())
```

## 数据类型

| Python 类型 | Table Storage 类型 |
|-------------|-------------------|
| `str` | String |
| `int` | Int64 |
| `float` | Double |
| `bool` | Boolean |
| `datetime` | DateTime |
| `bytes` | Binary |
| `UUID` | Guid |

## 最佳实践

1. **设计分区键**时应考虑查询模式和均匀分布
2. **尽量在分区内查询**（跨分区查询代价高）
3. **使用批量操作**处理同一分区中的多个实体
4. **使用 `upsert_entity`** 实现幂等写入
5. **使用参数化查询**防止注入
6. **保持实体精简**——每个实体最大 1MB
7. **使用异步客户端**处理高吞吐场景

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
