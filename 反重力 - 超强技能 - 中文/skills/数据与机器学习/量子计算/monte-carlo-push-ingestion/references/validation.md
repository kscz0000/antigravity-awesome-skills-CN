# 验证推送的数据

所有验证查询使用 **GraphQL API key**，端点为 `https://api.getmontecarlo.com/graphql`。

---

## 解析表的 MCON 和 fullTableId

在运行大多数查询之前，你需要 `mcon` 或 `fullTableId`。

`fullTableId` 格式：`<database>:<schema>.<table>` — 例如 `analytics:public.orders`

```graphql
query GetTable($fullTableId: String!, $dwId: UUID!) {
  getTable(fullTableId: $fullTableId, dwId: $dwId) {
    mcon
    fullTableId
    displayName
  }
}
```

变量：
```json
{
  "fullTableId": "analytics:public.orders",
  "dwId": "<warehouse-uuid>"
}
```

---

## 验证元数据（schema + 列）

```graphql
query GetTableMetadata($mcon: String!) {
  getTable(mcon: $mcon) {
    mcon
    fullTableId
    versions {
      edges {
        node {
          fields {
            name
            fieldType
          }
        }
      }
    }
  }
}
```

检查字段列表是否与你推送的 schema 匹配。

---

## 验证数据量和新鲜度指标

使用 `getMetricsV4` 获取行数和最后修改时间戳：

```graphql
query GetMetrics(
  $mcon: String!
  $metricName: String!
  $startTime: DateTime!
  $endTime: DateTime!
) {
  getMetricsV4(
    dwId: null
    mcon: $mcon
    metricName: $metricName
    startTime: $startTime
    endTime: $endTime
  ) {
    metricsJson
  }
}
```

变量（行数）：
```json
{
  "mcon": "<table-mcon>",
  "metricName": "total_row_count",
  "startTime": "2024-03-01T00:00:00Z",
  "endTime": "2024-03-02T00:00:00Z"
}
```

`metricsJson` 是一个 JSON 字符串。解析它并在每个数据点中查找 `value` 和 `measurementTimestamp`（驼峰命名）。

其他有用的指标名称：
- `"total_row_count"` — 行数
- `"total_byte_count"` — 字节大小
- `"total_row_count_last_changed_on"` — 行数最后更改时间的 Unix epoch 浮点数

---

## 验证表血缘

```graphql
query GetTableLineage($mcon: String!) {
  getTableLineage(mcon: $mcon, direction: "upstream", hops: 1) {
    connectedNodes {
      mcon
      displayName
      objectType
    }
    flattenedEdges {
      directlyConnectedMcons
    }
  }
}
```

检查你期望的源表是否出现在 `connectedNodes` 或 `flattenedEdges[].directlyConnectedMcons` 中。

---

## 验证列血缘

```graphql
query GetColumnLineage($mcon: String!, $column: String!) {
  getDerivedTablesPartialLineage(mcon: $mcon, column: $column, pageSize: 1000) {
    destinations {
      table { mcon displayName }
      columns { columnName }
    }
  }
}
```

变量：`mcon` = 源表 MCON，`column` = 源列名。

检查每个目标表和列是否出现在响应中。

---

## 验证查询日志

```graphql
query GetAggregatedQueries(
  $mcon: String!
  $queryType: String!
  $startTime: DateTime!
  $endTime: DateTime!
  $first: Int
  $after: String
) {
  getAggregatedQueries(
    mcon: $mcon
    queryType: $queryType
    startTime: $startTime
    endTime: $endTime
    first: $first
    after: $after
  ) {
    edges { node { queryHash queryCount lastSeen } }
    pageInfo { hasNextPage endCursor }
  }
}
```

变量：
```json
{
  "mcon": "<table-mcon>",
  "queryType": "read",
  "startTime": "2024-03-01T00:00:00Z",
  "endTime": "2024-03-02T00:00:00Z",
  "first": 100
}
```

**记住**：查询日志在推送后最多需要 1 小时才能处理完成。如果推送后立即看到 0 条结果，请等待后重试。

---

## 检查检测器阈值（异常检测状态）

```graphql
query GetDetectorStatus($mcon: String!) {
  getTable(mcon: $mcon) {
    thresholds {
      freshness {
        lower { value }
        upper { value }
        status
      }
      size {
        lower { value }
        upper { value }
        status
      }
    }
  }
}
```

对于新推送的表，`status` 将是 `"no data"` 或 `"inactive"`。检测器需要历史数据来训练 — 有关要求，请参阅 `references/anomaly-detection.md`。

---

## 表管理操作

### 删除 push-ingested 表

仅适用于 push-ingested 表 — pull-collected 表默认被排除。

```graphql
mutation DeletePushTables($mcons: [String!]!) {
  deletePushIngestedTables(mcons: $mcons) {
    success
    deletedCount
  }
}
```

变量：
```json
{
  "mcons": ["<mcon-1>", "<mcon-2>"]
}
```

先使用 `getTable(fullTableId: ..., dwId: ...)` 解析 MCON。

---

## Python 辅助函数

```python
import requests, json

GRAPHQL_URL = "https://api.getmontecarlo.com/graphql"

def graphql(query: str, variables: dict, key_id: str, key_token: str) -> dict:
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={
            "x-mcd-id": key_id,
            "x-mcd-token": key_token,
            "Content-Type": "application/json",
        },
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data["data"]
```