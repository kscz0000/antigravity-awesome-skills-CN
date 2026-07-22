# 推送表元数据

## 概述

元数据推送为每个表发送三种类型的信号：
- **Schema** — 列名和类型
- **数据量** — 行数和字节数
- **新鲜度** — 最后更新时间戳

这三种信号通过 `POST /ingest/v1/metadata` 在单个 `RelationalAsset` 对象中一起传输。

**过期时间**：推送的表元数据**永不过期**。一旦推送，它将保留在 Monte Carlo 中，直到通过 `deletePushIngestedTables` 显式删除。

**批处理**：对于大量表，将资产拆分为批次。压缩的请求体不得超过 **1MB**（Kinesis 限制）。

## pycarlo 模型

```python
from pycarlo.features.ingestion import (
    IngestionService,
    RelationalAsset,
    AssetMetadata,
    AssetField,
    AssetVolume,
    AssetFreshness,
)
```

## 最小示例

```python
asset = RelationalAsset(
    type="TABLE",  # ONLY "TABLE" or "VIEW" — normalize warehouse-native values
    metadata=AssetMetadata(
        name="orders",
        database="analytics",
        schema="public",
        description="Order transactions",
    ),
    fields=[
        AssetField(name="order_id", type="INTEGER"),
        AssetField(name="amount",   type="DECIMAL"),
        AssetField(name="created_at", type="TIMESTAMP"),
    ],
    volume=AssetVolume(
        row_count=1_500_000,
        byte_count=250_000_000,
    ),
    freshness=AssetFreshness(
        last_update_time="2024-03-01T12:00:00Z",  # ISO 8601 string, NOT a datetime object
    ),
)

result = service.send_metadata(
    resource_uuid="<your-resource-uuid>",
    resource_type="data-lake",   # see note below on resource_type
    events=[asset],
)
invocation_id = service.extract_invocation_id(result)
print("invocation_id:", invocation_id)   # save this!
```

## resource_type

`resource_type` 值必须与你要推送到的 MC 资源（仓库连接）的类型匹配。使用 MC UI 中显示的字符串或 `getUser { account { warehouses { connectionType } } }` 中的 `connectionType` 字段。

常见值：
- `"data-lake"` — Hive、EMR、Glue、通用数据湖连接
- `"snowflake"` — Snowflake
- `"bigquery"` — BigQuery
- `"databricks"` — Databricks Unity Catalog
- `"redshift"` — Redshift

## 资产类型

`RelationalAsset` 上的 `type` 参数必须是以下两个值之一（大写）：
- `"TABLE"` — 表、外部表、动态表、物化视图等
- `"VIEW"` — 视图、安全视图

**重要**：仓库原生类型值如 `"BASE TABLE"`（Snowflake）、`"MANAGED"` / `"EXTERNAL"`（Databricks）或 `"MATERIALIZED_VIEW"`（BigQuery）**不被** MC API 接受，会导致 400 错误。推送前始终规范化为 `"TABLE"` 或 `"VIEW"`。

## 字段类型

规范化为 SQL 标准大写字符串。Monte Carlo 接受任何字符串，但规范值如 `INTEGER`、`BIGINT`、`VARCHAR`、`FLOAT`、`BOOLEAN`、`TIMESTAMP`、`DATE`、`DECIMAL`、`ARRAY`、`STRUCT` 与下游功能配合效果最好。

## 数据量和新鲜度是可选的

如果你的仓库不暴露行数或最后修改时间戳，可以省略 `volume` 和/或 `freshness` — 仅 schema 的元数据是有效的。

如果你发送 `freshness`，每次推送必须携带**变化的** `last_update_time` 才能算作异常检测器的新数据点（重复相同的时间戳不会推进训练时钟）。

## 仅新鲜度 + 数据量模式（跳过 schema）

对于定期推送（例如每小时 cron），你通常不需要在每次运行时重新收集完整的 schema — 字段定义很少改变。收集脚本可以支持 `--only-freshness-and-volume` 标志，跳过 `COLUMNS` / `INFORMATION_SCHEMA` 查询并从 manifest 中省略 `fields`。这在拥有大量表的仓库上明显更快。首次推送和每日计划使用完整收集（包含字段），中间的每小时推送使用仅新鲜度+数据量模式。有关此模式的工作实现，请参阅 [BigQuery Iceberg 示例](https://github.com/monte-carlo-data/mcd-public-resources/tree/main/examples/push-ingestion/bigquery/push-iceberg-tables)。

## 批量处理多个表

`events` 接受列表。在单次调用或分批推送所有表：

```python
result = service.send_metadata(
    resource_uuid=resource_uuid,
    resource_type="data-lake",
    events=[asset1, asset2, asset3, ...],
)
```

## 输出 manifest（包含 invocation_id）

始终写入本地 manifest，以便稍后追踪问题：

```python
import json
from datetime import datetime, timezone

manifest = {
    "resource_uuid": resource_uuid,
    "invocation_id": service.extract_invocation_id(result),   # ← critical for debugging
    "collected_at": datetime.now(tz=timezone.utc).isoformat(),
    "assets": [
        {
            "database": a.metadata.database,
            "schema": a.metadata.schema,
            "table": a.metadata.name,
            "row_count": a.volume.row_count if a.volume else None,
            "fields": [{"name": f.name, "type": f.type} for f in a.fields],
        }
        for a in assets
    ],
}
with open("metadata_output.json", "w") as f:
    json.dump(manifest, f, indent=2)
```

## 异常检测的推送频率

要保持数据量和新鲜度异常检测器活跃：
- 最多**每小时推送一次**（更频繁的推送会产生不可预测的行为）
- **持续推送** — 超过几天的间隔会停用检测器
- 有关最小样本要求，请参阅 `references/anomaly-detection.md`