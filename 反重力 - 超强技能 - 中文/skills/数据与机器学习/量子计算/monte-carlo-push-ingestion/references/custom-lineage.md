# 自定义血缘节点和边

## 何时使用

`send_lineage()` pycarlo 方法适用于你拥有的仓库表。本文档中的 **GraphQL mutations** 适用于：
- 非仓库资产：dbt 模型、Airflow DAG、Fivetran 连接器、自定义 ETL 作业
- 跨不同 MC 资源（仓库）连接节点
- 不绑定到收集器运行的一次性血缘修正
- 对节点属性、对象类型和过期时间的精细控制

所有 mutations 使用 **GraphQL API key**（不是 Ingestion key），端点为 `https://api.getmontecarlo.com/graphql`。

## 关键：expireAt

如果不设置 `expireAt`，节点和边在 **7 天后过期**并从血缘图中静默消失。对于任何应该持久化的节点或边：

```
expireAt: "9999-12-31"
```

这与 `PushLineageProcessor` 内部为所有 push-ingested 血缘使用的值相同。忘记这一点是"我的血缘一周后消失了"最常见的原因。

---

## createOrUpdateLineageNode

在血缘图中创建或更新节点。如果具有相同 `objectType` + `objectId` + `resourceId` 的节点已存在，则更新它。

```graphql
mutation CreateOrUpdateLineageNode(
  $objectType: String!
  $objectId:   String!
  $resourceId:   UUID
  $resourceName: String
  $name:       String
  $properties: [ObjectPropertyInput]
  $expireAt:   DateTime
) {
  createOrUpdateLineageNode(
    objectType:   $objectType
    objectId:     $objectId
    resourceId:   $resourceId
    resourceName: $resourceName
    name:         $name
    properties:   $properties
    expireAt:     $expireAt
  ) {
    node {
      mcon
      displayName
      objectType
      isCustom
      expireAt
    }
  }
}
```

**变量：**
```json
{
  "objectType":  "table",
  "objectId":    "analytics:analytics.orders",
  "resourceId":  "<warehouse-uuid>",
  "name":        "orders",
  "expireAt":    "9999-12-31"
}
```

`objectType` 可以是任何字符串 — 常见值：`"table"`、`"view"`、`"report"`、`"dashboard"`、`"job"`、`"model"`。

`objectId` 应该是资源内资产的稳定唯一标识符。对于表，使用 `fullTableId` 格式：`database:schema.table`。

返回的 `mcon` 是此节点的稳定 MC 标识符 — 如果你计划在边或删除中引用它，请保存它。

---

## createOrUpdateLineageEdge

创建或更新有向边：源 → 目标（默认：IS_DOWNSTREAM）。

```graphql
mutation CreateOrUpdateLineageEdge(
  $source:      NodeInput!
  $destination: NodeInput!
  $expireAt:    DateTime
  $edgeType:    EdgeType
) {
  createOrUpdateLineageEdge(
    source:      $source
    destination: $destination
    expireAt:    $expireAt
    edgeType:    $edgeType
  ) {
    edge {
      source      { mcon displayName objectType }
      destination { mcon displayName objectType }
      isCustom
      expireAt
    }
  }
}
```

`NodeInput` 结构：
```json
{
  "objectType":   "table",
  "objectId":     "analytics:analytics.orders",
  "resourceId":   "<warehouse-uuid>"
}
```

**完整示例 — dbt 模型 → 仓库表：**
```json
{
  "source": {
    "objectType": "model",
    "objectId":   "dbt://my_project/models/staging/stg_orders",
    "resourceName": "dbt-production"
  },
  "destination": {
    "objectType": "table",
    "objectId":   "analytics:analytics.orders",
    "resourceId": "<snowflake-warehouse-uuid>"
  },
  "expireAt":  "9999-12-31",
  "edgeType":  "IS_DOWNSTREAM"
}
```

---

## deleteLineageNode

删除节点及其**所有边和对象**。此操作不可逆。

```graphql
mutation DeleteLineageNode($mcon: String!) {
  deleteLineageNode(mcon: $mcon) {
    objectsDeleted
    nodesDeleted
    edgesDeleted
  }
}
```

从 `createOrUpdateLineageNode` 的响应中获取 MCON，或从以下查询获取：
```graphql
query {
  getTable(fullTableId: "analytics:analytics.orders", dwId: "<warehouse-uuid>") {
    mcon
  }
}
```

---

## 三个 mutations 的 Python 辅助函数

```python
import requests

GRAPHQL_URL = "https://api.getmontecarlo.com/graphql"
HEADERS = {
    "x-mcd-id":    "<graphql-api-key-id>",
    "x-mcd-token": "<graphql-api-key-secret>",
    "Content-Type": "application/json",
}

def run_mutation(query: str, variables: dict) -> dict:
    resp = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]

# Example: create a permanent node
result = run_mutation(
    """mutation($objectType: String!, $objectId: String!, $resourceId: UUID, $expireAt: DateTime) {
         createOrUpdateLineageNode(objectType: $objectType, objectId: $objectId,
                                   resourceId: $resourceId, expireAt: $expireAt) {
           node { mcon displayName }
         }
       }""",
    {
        "objectType": "table",
        "objectId":   "analytics:analytics.orders",
        "resourceId": "<warehouse-uuid>",
        "expireAt":   "9999-12-31",
    }
)
print("MCON:", result["createOrUpdateLineageNode"]["node"]["mcon"])
```