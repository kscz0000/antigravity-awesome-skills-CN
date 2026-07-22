# 直接 HTTP API（不使用 pycarlo）

`pycarlo` SDK 是可选的。你可以从任何语言或工具（curl、Postman 等）通过 HTTPS 直接调用 push API，只要：
- 使用 scope 为 `Ingestion` 的集成 key 进行认证
- 发送与 ingest schema 匹配的 JSON body
- 发送到正确的集成网关端点

## 端点

主机因环境而异：
- **生产环境**：`https://integrations.getmontecarlo.com`

## 认证头

所有请求使用相同的头：
```
x-mcd-id:       <integration-key-id>
x-mcd-token:    <integration-key-secret>
Content-Type:   application/json
```

## 响应

成功时，所有端点返回：
```json
{"invocation_id": "<uuid>"}
```

保存 `invocation_id` — 这是在下游系统中调试的主要追踪 ID。

---

## 元数据示例

`POST /ingest/v1/metadata`

```bash
curl -X POST "https://integrations.getmontecarlo.com/ingest/v1/metadata" \
  -H "Content-Type: application/json" \
  -H "x-mcd-id: <integration-key-id>" \
  -H "x-mcd-token: <integration-key-secret>" \
  -d '{
    "event_type": "RELATIONAL_ASSET",
    "resource": {
      "uuid": "<warehouse-uuid>",
      "resource_type": "snowflake"
    },
    "events": [
      {
        "type": "TABLE",
        "metadata": {
          "name": "orders",
          "database": "analytics",
          "schema": "public",
          "description": "Orders table"
        },
        "fields": [
          {"name": "id", "type": "INTEGER"},
          {"name": "amount", "type": "DECIMAL(10,2)"}
        ],
        "volume": {
          "row_count": 1000000,
          "byte_count": 111111111
        },
        "freshness": {
          "last_update_time": "2026-03-12T14:30:00Z"
        }
      }
    ]
  }'
```

`volume` 和 `freshness` 是可选的 — 你可以仅推送 schema 元数据。

---

## 表血缘示例

`POST /ingest/v1/lineage`，`event_type: "LINEAGE"`

```bash
curl -X POST "https://integrations.getmontecarlo.com/ingest/v1/lineage" \
  -H "Content-Type: application/json" \
  -H "x-mcd-id: <integration-key-id>" \
  -H "x-mcd-token: <integration-key-secret>" \
  -d '{
    "event_type": "LINEAGE",
    "resource": {
      "uuid": "<warehouse-uuid>",
      "resource_type": "snowflake"
    },
    "events": [
      {
        "source": {
          "name": "orders_raw",
          "database": "analytics",
          "schema": "public"
        },
        "destination": {
          "name": "orders_curated",
          "database": "analytics",
          "schema": "public"
        }
      }
    ]
  }'
```

---

## 列血缘示例

`POST /ingest/v1/lineage`，`event_type: "COLUMN_LINEAGE"`

与表血缘相同的端点。列血缘会自动创建父表级边。

```bash
curl -X POST "https://integrations.getmontecarlo.com/ingest/v1/lineage" \
  -H "Content-Type: application/json" \
  -H "x-mcd-id: <integration-key-id>" \
  -H "x-mcd-token: <integration-key-secret>" \
  -d '{
    "event_type": "COLUMN_LINEAGE",
    "resource": {
      "uuid": "<warehouse-uuid>",
      "resource_type": "snowflake"
    },
    "events": [
      {
        "source": {
          "name": "customers",
          "database": "analytics",
          "schema": "public"
        },
        "destination": {
          "name": "customer_orders",
          "database": "analytics",
          "schema": "public"
        },
        "col_mappings": [
          {
            "destination_col": "customer_id",
            "source_cols": ["customer_id"]
          },
          {
            "destination_col": "full_name",
            "source_cols": ["first_name", "last_name"]
          }
        ]
      }
    ]
  }'
```

---

## 查询日志示例

`POST /ingest/v1/querylogs`

**重要**：此端点在资源对象中使用 `log_type` 而不是 `resource_type`。这是唯一一个字段名称不同的端点。

```bash
curl -X POST "https://integrations.getmontecarlo.com/ingest/v1/querylogs" \
  -H "Content-Type: application/json" \
  -H "x-mcd-id: <integration-key-id>" \
  -H "x-mcd-token: <integration-key-secret>" \
  -d '{
    "event_type": "QUERY_LOG",
    "resource": {
      "uuid": "<warehouse-uuid>",
      "log_type": "snowflake"
    },
    "events": [
      {
        "start_time": "2026-03-02T12:00:00Z",
        "end_time": "2026-03-02T12:00:05Z",
        "query_text": "SELECT * FROM analytics.public.orders",
        "query_id": "query-123",
        "user": "analyst@company.com",
        "returned_rows": 10
      }
    ]
  }'
```

支持的 `log_type` 值：`snowflake`、`bigquery`、`databricks`、`redshift`、`hive-s3`、`athena`、`teradata`、`clickhouse`、`databricks-metastore-sql-warehouse`、`s3`、`presto-s3`。

---

## 批处理

压缩的请求体不得超过 **1MB**（Kinesis 限制）。对于大型负载，将事件拆分为多个请求。每个请求返回自己的 `invocation_id`。

## 过期时间总结

| 流程 | 过期时间 |
|---|---|
| 表元数据 | 永不过期 |
| 表血缘 | 永不过期 |
| 列血缘 | 10 天后过期 |
| 查询日志 | 与拉取的查询日志相同 |