# 推送表和列血缘

## 概述

表级和列级血缘使用相同的端点：`POST /ingest/v1/lineage`。`event_type` 字段区分它们：
- `LINEAGE` — 表级：源表 → 目标表
- `COLUMN_LINEAGE` — 列级：源表.列 → 目标表.列（同时自动创建父表级边）

推送的血缘**通常在几秒到几分钟内**通过快速直接路径（PushLineageProcessor → S3 CSVs → neo4jLineageLoaderPrivate → Neo4j）在 MC 血缘图中可见。

**过期时间**：
- 推送的**表血缘永不过期**（`expire_at = 9999-12-31`）。
- 推送的**列血缘在 10 天后过期**（与拉取的列血缘相同）。

**批处理**：对于大量血缘事件，拆分为批次。压缩的请求体不得超过 **1MB**（Kinesis 限制）。

## pycarlo 模型

```python
from pycarlo.features.ingestion import (
    IngestionService,
    LineageEvent,
    LineageAssetRef,
    ColumnLineageField,
    ColumnLineageSourceField,
)
```

## 表血缘示例

```python
event = LineageEvent(
    destination=LineageAssetRef(
        database="analytics",
        schema="public",
        table="customer_orders",
    ),
    sources=[
        LineageAssetRef(database="analytics", schema="public", table="customers"),
        LineageAssetRef(database="analytics", schema="public", table="orders"),
    ],
)

result = service.send_lineage(
    resource_uuid="<your-resource-uuid>",
    resource_type="data-lake",
    events=[event],
)
invocation_id = service.extract_invocation_id(result)
print("invocation_id:", invocation_id)
```

## 列血缘示例

```python
event = LineageEvent(
    destination=LineageAssetRef(
        database="analytics",
        schema="public",
        table="customer_orders",
    ),
    sources=[
        LineageAssetRef(database="analytics", schema="public", table="customers"),
        LineageAssetRef(database="analytics", schema="public", table="orders"),
    ],
    # column mappings: dest_col ← src_table.src_col
    fields=[
        ColumnLineageField(
            destination_field="customer_id",
            source_fields=[
                ColumnLineageSourceField(
                    database="analytics", schema="public",
                    table="customers", field="customer_id",
                )
            ],
        ),
        ColumnLineageField(
            destination_field="order_amount",
            source_fields=[
                ColumnLineageSourceField(
                    database="analytics", schema="public",
                    table="orders", field="amount",
                )
            ],
        ),
    ],
)

result = service.send_lineage(
    resource_uuid=resource_uuid,
    resource_type="data-lake",
    events=[event],
)
```

列血缘推送会自动创建表级边，因此你不需要为同一关系分别发送表和列血缘事件。

## 从 SQL 日志中提取血缘

对于不暴露原生血缘表的仓库，通过解析查询历史 SQL 中的 `CREATE TABLE AS SELECT`、`INSERT INTO ... SELECT` 和 `MERGE INTO` 模式来提取血缘。

简化的正则表达式示例：
```python
import re

CTAS_PATTERN = re.compile(
    r"CREATE\s+(?:OR\s+REPLACE\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\S+)\s+AS\s+SELECT",
    re.IGNORECASE,
)
INSERT_PATTERN = re.compile(
    r"INSERT\s+(?:OVERWRITE\s+)?(?:INTO\s+)?(\S+).*?FROM\s+(\S+)",
    re.IGNORECASE | re.DOTALL,
)
```

对于 Snowflake、BigQuery 和 Redshift，查询历史表提供此 SQL。
对于 Databricks，直接使用 `system.access.table_lineage`（无需解析）。
对于 Hive，解析 HiveServer2 日志文件。

## 输出 manifest（包含 invocation_id）

```python
manifest = {
    "resource_uuid": resource_uuid,
    "invocation_id": service.extract_invocation_id(result),   # ← save this
    "collected_at": datetime.now(tz=timezone.utc).isoformat(),
    "edges": [
        {
            "destination": {"database": e.destination.database, "table": e.destination.table},
            "sources": [{"database": s.database, "table": s.table} for s in e.sources],
        }
        for e in events
    ],
}
with open("lineage_output.json", "w") as f:
    json.dump(manifest, f, indent=2)
```

## 推送血缘与查询派生血缘的区分

Push-ingested 的血缘节点和边在 Neo4j 中携带 `origin = push_ingest`，在标准化血缘模型中携带 `origin_type = DIRECT_LINEAGE`。这防止血缘 DAG 用查询日志派生的边覆盖它们，并为 MC 提供清晰的审计跟踪。

## Neo4j 节点过期

Push-ingested 的**表血缘**节点和边以 `expire_at = 9999-12-31`（永不过期）写入。这由 PushLineageProcessor 内部处理 — 使用 `send_lineage()` 时你不需要手动设置。

Push-ingested 的**列血缘**在 **10 天后过期**，与拉取的列血缘相同。

对于通过 GraphQL mutations 创建的自定义节点，你**确实**需要显式设置 `expireAt: "9999-12-31"` — 请参阅 `references/custom-lineage.md`。