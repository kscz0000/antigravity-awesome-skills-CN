# 推送查询日志

## 概述

查询日志让 Monte Carlo 构建表使用历史、填充查询血缘关系，并在目录中显示查询级别的洞察。通过 `POST /ingest/v1/querylogs` 推送。

**重要时间说明**：MC 异步处理推送的查询日志。现在推送的日志可能在 **至少 15-20 分钟**内不会在 `getAggregatedQueries` 中可见。这是预期行为，不是 bug。

**过期时间**：推送的查询日志与拉取的查询日志使用相同的过期时间表。

**批处理**：对于大型查询日志集，将事件拆分为批次。压缩的请求体不得超过 **1MB**（Kinesis 限制）。保守的默认值是每批 250 条记录。

## pycarlo 模型

```python
from pycarlo.features.ingestion import IngestionService, QueryLogEntry
```

`QueryLogEntry` 必填字段：
- `start_time` (`datetime`) — 查询开始时间
- `end_time` (`datetime`) — 查询结束时间（**必填**，容易遗漏）
- `query_text` (`str`) — SQL 语句

可选字段：
- `query_id` (`str`) — 仓库分配的查询 ID
- `user` (`str`) — 运行查询的用户/邮箱
- `returned_rows` (`int`) — 返回给客户端的行数
- `default_database` (`str`) — 默认数据库上下文

## 基本示例

```python
from datetime import datetime, timezone

entries = [
    QueryLogEntry(
        start_time=datetime(2024, 3, 1, 10, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2024, 3, 1, 10, 0, 5, tzinfo=timezone.utc),
        query_text="SELECT * FROM analytics.public.orders WHERE status = 'pending'",
        query_id="query-abc-123",
        user="analyst@company.com",
        returned_rows=847,
    ),
]

result = service.send_query_logs(
    resource_uuid="<your-resource-uuid>",
    log_type="snowflake",   # ← warehouse-specific! see table below
    entries=entries,
)
invocation_id = service.extract_invocation_id(result)
print("invocation_id:", invocation_id)
```

## 每个仓库的 log_type

**重要**：查询日志端点使用 `log_type`，而不是 `resource_type`。这是唯一一个字段名称与元数据/血缘不同的 push 端点。`log_type` 值必须与 MC 标准化器为你的仓库期望的值匹配。使用错误的值会导致：`ValueError: Unsupported ingest query-log log_type: <value>`

| 仓库 | log_type |
|---|---|
| Snowflake | `"snowflake"` |
| BigQuery | `"bigquery"` |
| Databricks | `"databricks"` |
| Redshift | `"redshift"` |
| Hive (EMR/S3) | `"hive-s3"` |
| Athena | `"athena"` |
| Teradata | `"teradata"` |
| ClickHouse | `"clickhouse"` |
| Databricks (SQL Warehouse) | `"databricks-metastore-sql-warehouse"` |
| S3 | `"s3"` |
| Presto (S3) | `"presto-s3"` |

## 仓库特定字段

某些仓库支持超出基本 `QueryLogEntry` 的额外字段。将它们作为关键字参数传递 — 标准化器知道每个仓库哪些字段是有效的。

**Snowflake 扩展：**
```python
QueryLogEntry(
    ...
    bytes_scanned=1024000,
    warehouse_name="COMPUTE_WH",
    warehouse_size="X-Small",
    role_name="ANALYST",
    query_tag="reporting",
    execution_status="SUCCESS",
)
```

**BigQuery 扩展：**
```python
QueryLogEntry(
    ...
    total_bytes_billed=10485760,
    statement_type="SELECT",
    job_type="QUERY",
    default_dataset="analytics.public",
)
```

**Athena 扩展：**
```python
QueryLogEntry(
    ...
    bytes_scanned=2048000,
    catalog="AwsDataCatalog",
    database="analytics",
    output_location="s3://my-bucket/results/",
    state="SUCCEEDED",
)
```

## 每个仓库的查询日志收集

### Snowflake
```sql
SELECT
    query_id,
    query_text,
    start_time,
    end_time,
    user_name,
    database_name,
    warehouse_name,
    bytes_scanned,
    rows_produced AS returned_rows,
    execution_status
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
  AND execution_status = 'SUCCESS'
ORDER BY start_time
```

注意：`ACCOUNT_USAGE` 视图最多有 45 分钟的延迟。不要收集最近一小时的数据。

### BigQuery
```python
from google.cloud import bigquery
client = bigquery.Client(project=project_id)
jobs = client.list_jobs(all_users=True, min_creation_time=start_dt, max_creation_time=end_dt)
for job in jobs:
    if hasattr(job, 'query') and job.query:
        # job.job_id, job.query, job.created, job.ended, job.user_email
```

### Databricks
```sql
SELECT
    statement_id AS query_id,
    statement_text AS query_text,
    start_time,
    end_time,
    executed_by AS user,
    produced_rows AS returned_rows
FROM system.query.history
WHERE start_time >= DATEADD(HOUR, -24, NOW())
  AND status = 'FINISHED'
```

### Redshift（现代集群）
```sql
SELECT
    query_id,
    query_text,   -- may need text assembly from SYS_QUERYTEXT for long queries
    start_time,
    end_time,
    user_id,
    status
FROM sys_query_history
WHERE start_time >= DATEADD(hour, -24, GETDATE())
  AND status = 'success'
```

对于长查询（文本 > 4000 字符），从 `SYS_QUERYTEXT` 组装：
```sql
SELECT query_id, LISTAGG(text, '') WITHIN GROUP (ORDER BY sequence) AS full_text
FROM sys_querytext
WHERE query_id = <id>
GROUP BY query_id
```

### Hive
解析 HiveServer2 日志文件（默认：`/tmp/root/hive.log`）中匹配以下模式的行：
```
(Executing|Starting) command\(queryId=(\S*)\): (?P<command>.*)
```

## 输出 manifest（包含 invocation_id）

```python
manifest = {
    "resource_uuid": resource_uuid,
    "invocation_id": service.extract_invocation_id(result),   # ← save this
    "collected_at": datetime.now(tz=timezone.utc).isoformat(),
    "entry_count": len(entries),
    "window_start": min(e.start_time for e in entries).isoformat(),
    "window_end": max(e.end_time for e in entries).isoformat(),
    "queries": [
        {
            "query_id": e.query_id,
            "start_time": e.start_time.isoformat(),
            "end_time": e.end_time.isoformat(),
            "returned_rows": e.returned_rows,
            "query": e.query_text[:200],   # truncate for readability
        }
        for e in entries
    ],
}
with open("query_logs_output.json", "w") as f:
    json.dump(manifest, f, indent=2)
```