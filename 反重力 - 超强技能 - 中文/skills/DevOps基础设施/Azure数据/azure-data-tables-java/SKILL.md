---
name: azure-data-tables-java
description: "使用 Azure Tables Java SDK 构建表存储应用程序。适用于 Azure 表存储和 Cosmos DB 表 API。触发词：Azure Tables Java、表存储SDK、Cosmos DB Table API、NoSQL键值存储、分区键行键、表实体CRUD"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Tables SDK for Java

使用 Azure Tables Java SDK 构建表存储应用程序。适用于 Azure 表存储和 Cosmos DB 表 API。

## 安装

```xml
<dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-data-tables</artifactId>
  <version>12.6.0-beta.1</version>
</dependency>
```

## 客户端创建

### 使用连接字符串

```java
import com.azure.data.tables.TableServiceClient;
import com.azure.data.tables.TableServiceClientBuilder;
import com.azure.data.tables.TableClient;

TableServiceClient serviceClient = new TableServiceClientBuilder()
    .connectionString("<your-connection-string>")
    .buildClient();
```

### 使用共享密钥

```java
import com.azure.core.credential.AzureNamedKeyCredential;

AzureNamedKeyCredential credential = new AzureNamedKeyCredential(
    "<account-name>",
    "<account-key>");

TableServiceClient serviceClient = new TableServiceClientBuilder()
    .endpoint("<your-table-account-url>")
    .credential(credential)
    .buildClient();
```

### 使用 SAS 令牌

```java
TableServiceClient serviceClient = new TableServiceClientBuilder()
    .endpoint("<your-table-account-url>")
    .sasToken("<sas-token>")
    .buildClient();
```

### 使用 DefaultAzureCredential（仅限存储）

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

TableServiceClient serviceClient = new TableServiceClientBuilder()
    .endpoint("<your-table-account-url>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

## 核心概念

- **TableServiceClient**：管理表（创建、列出、删除）
- **TableClient**：管理表内的实体（CRUD）
- **Partition Key**：用于高效查询的实体分组
- **Row Key**：分区内的唯一标识符
- **Entity**：最多包含 252 个属性的行（存储 1MB，Cosmos 2MB）

## 核心模式

### 创建表

```java
// 创建表（已存在则抛出异常）
TableClient tableClient = serviceClient.createTable("mytable");

// 不存在时创建（不抛出异常）
TableClient tableClient = serviceClient.createTableIfNotExists("mytable");
```

### 获取表客户端

```java
// 从服务客户端获取
TableClient tableClient = serviceClient.getTableClient("mytable");

// 直接构建
TableClient tableClient = new TableClientBuilder()
    .connectionString("<connection-string>")
    .tableName("mytable")
    .buildClient();
```

### 创建实体

```java
import com.azure.data.tables.models.TableEntity;

TableEntity entity = new TableEntity("partitionKey", "rowKey")
    .addProperty("Name", "Product A")
    .addProperty("Price", 29.99)
    .addProperty("Quantity", 100)
    .addProperty("IsAvailable", true);

tableClient.createEntity(entity);
```

### 获取实体

```java
TableEntity entity = tableClient.getEntity("partitionKey", "rowKey");

String name = (String) entity.getProperty("Name");
Double price = (Double) entity.getProperty("Price");
System.out.printf("Product: %s, Price: %.2f%n", name, price);
```

### 更新实体

```java
import com.azure.data.tables.models.TableEntityUpdateMode;

// 合并（仅更新指定属性）
TableEntity updateEntity = new TableEntity("partitionKey", "rowKey")
    .addProperty("Price", 24.99);
tableClient.updateEntity(updateEntity, TableEntityUpdateMode.MERGE);

// 替换（替换整个实体）
TableEntity replaceEntity = new TableEntity("partitionKey", "rowKey")
    .addProperty("Name", "Product A Updated")
    .addProperty("Price", 24.99)
    .addProperty("Quantity", 150);
tableClient.updateEntity(replaceEntity, TableEntityUpdateMode.REPLACE);
```

### Upsert 实体

```java
// 插入或更新（合并模式）
tableClient.upsertEntity(entity, TableEntityUpdateMode.MERGE);

// 插入或替换
tableClient.upsertEntity(entity, TableEntityUpdateMode.REPLACE);
```

### 删除实体

```java
tableClient.deleteEntity("partitionKey", "rowKey");
```

### 列出实体

```java
import com.azure.data.tables.models.ListEntitiesOptions;

// 列出所有实体
for (TableEntity entity : tableClient.listEntities()) {
    System.out.printf("%s - %s%n",
        entity.getPartitionKey(),
        entity.getRowKey());
}

// 带过滤和选择
ListEntitiesOptions options = new ListEntitiesOptions()
    .setFilter("PartitionKey eq 'sales'")
    .setSelect("Name", "Price");

for (TableEntity entity : tableClient.listEntities(options, null, null)) {
    System.out.printf("%s: %.2f%n",
        entity.getProperty("Name"),
        entity.getProperty("Price"));
}
```

### 使用 OData 过滤器查询

```java
// 按分区键过滤
ListEntitiesOptions options = new ListEntitiesOptions()
    .setFilter("PartitionKey eq 'electronics'");

// 多条件过滤
options.setFilter("PartitionKey eq 'electronics' and Price gt 100");

// 比较运算符过滤
options.setFilter("Quantity ge 10 and Quantity le 100");

// 前 N 条结果
options.setTop(10);

for (TableEntity entity : tableClient.listEntities(options, null, null)) {
    System.out.println(entity.getRowKey());
}
```

### 批量操作（事务）

```java
import com.azure.data.tables.models.TableTransactionAction;
import com.azure.data.tables.models.TableTransactionActionType;
import java.util.Arrays;

// 所有实体必须具有相同的分区键
List<TableTransactionAction> actions = Arrays.asList(
    new TableTransactionAction(
        TableTransactionActionType.CREATE,
        new TableEntity("batch", "row1").addProperty("Name", "Item 1")),
    new TableTransactionAction(
        TableTransactionActionType.CREATE,
        new TableEntity("batch", "row2").addProperty("Name", "Item 2")),
    new TableTransactionAction(
        TableTransactionActionType.UPSERT_MERGE,
        new TableEntity("batch", "row3").addProperty("Name", "Item 3"))
);

tableClient.submitTransaction(actions);
```

### 列出表

```java
import com.azure.data.tables.models.TableItem;
import com.azure.data.tables.models.ListTablesOptions;

// 列出所有表
for (TableItem table : serviceClient.listTables()) {
    System.out.println(table.getName());
}

// 过滤表
ListTablesOptions options = new ListTablesOptions()
    .setFilter("TableName eq 'mytable'");

for (TableItem table : serviceClient.listTables(options, null, null)) {
    System.out.println(table.getName());
}
```

### 删除表

```java
serviceClient.deleteTable("mytable");
```

## 类型化实体

```java
public class Product implements TableEntity {
    private String partitionKey;
    private String rowKey;
    private OffsetDateTime timestamp;
    private String eTag;
    private String name;
    private double price;
    
    // 所有字段的 getter 和 setter
    @Override
    public String getPartitionKey() { return partitionKey; }
    @Override
    public void setPartitionKey(String partitionKey) { this.partitionKey = partitionKey; }
    @Override
    public String getRowKey() { return rowKey; }
    @Override
    public void setRowKey(String rowKey) { this.rowKey = rowKey; }
    // ... 其他 getter/setter
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
}

// 使用
Product product = new Product();
product.setPartitionKey("electronics");
product.setRowKey("laptop-001");
product.setName("Laptop");
product.setPrice(999.99);

tableClient.createEntity(product);
```

## 错误处理

```java
import com.azure.data.tables.models.TableServiceException;

try {
    tableClient.createEntity(entity);
} catch (TableServiceException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
    // 409 = 冲突（实体已存在）
    // 404 = 未找到
}
```

## 环境变量

```bash
# 存储账户
AZURE_TABLES_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_TABLES_ENDPOINT=https://<account>.table.core.windows.net

# Cosmos DB 表 API
COSMOS_TABLE_ENDPOINT=https://<account>.table.cosmosdb.azure.com
```

## 最佳实践

1. **分区键设计**：选择能够均匀分布负载的键
2. **批量操作**：使用事务进行原子性多实体更新
3. **查询优化**：尽可能按 PartitionKey 过滤
4. **选择投影**：仅选择需要的属性以提高性能
5. **实体大小**：保持实体在 1MB（存储）或 2MB（Cosmos）以下

## 触发词

- "Azure Tables Java"
- "表存储 SDK"
- "Cosmos DB 表 API"
- "NoSQL 键值存储"
- "分区键 行键"
- "表实体 CRUD"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
