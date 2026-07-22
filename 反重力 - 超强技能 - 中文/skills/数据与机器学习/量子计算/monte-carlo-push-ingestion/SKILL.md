---
name: monte-carlo-push-ingestion
description: "从任意数据仓库向 Monte Carlo 推送元数据、血缘关系和查询日志的专家指南。当用户要求推送元数据、血缘或查询日志到 Monte Carlo 时使用。"
category: data
risk: safe
source: community
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: "2026-04-08"
author: monte-carlo-data
tags: [data-observability, ingestion, monte-carlo, pycarlo, metadata]
tools: [claude, cursor, codex]
---

# Monte Carlo Push Ingestion

你是一个帮助客户从数据仓库收集元数据、血缘关系和查询日志，并通过 push ingestion API 将这些数据推送到 Monte Carlo 的智能体。Push 模式适用于**任何数据源** — 如果客户的仓库没有现成模板，可以从该仓库的系统目录或元数据 API 推导出合适的收集查询。无论数据源是什么，push 格式和 pycarlo SDK 调用都是相同的。

Monte Carlo 的 push 模式允许客户直接向 Monte Carlo 发送元数据、血缘关系和查询日志，而无需等待 pull collector 来收集。它填补了 pull 模式无法覆盖的空白 — 那些不暴露查询历史的集成、非仓库资产之间的自定义血缘关系，或者客户已有这些数据并希望直接发送的场景。

## 何时使用

当用户需要从仓库或相邻系统收集元数据、血缘关系、新鲜度、数据量或查询日志数据，并通过 push-ingestion API 推送到 Monte Carlo 时，使用此技能。

Push 数据通过集成网关 → 专用 Kinesis 流 → 精简的适配器/标准化器代码 → 与 pull 模式相同的下游系统。唯一的新基础设施是入口层；之后的所有内容都是共享的。

## 必须 — 始终从模板开始

生成任何 push-ingestion 脚本时，你**必须**：

1. **读取相应模板**再编写任何代码。模板位于此技能目录下的 `scripts/templates/<warehouse>/`。要找到它们，使用 glob 搜索 `**/push-ingestion/scripts/templates/<warehouse>/*.py` — 无论技能安装在哪里都有效。不要仅从当前工作目录搜索。
2. **根据客户需求调整模板** — 不要凭记忆编写 pycarlo 导入、模型构造器或 SDK 方法调用。
3. 如果目标仓库没有模板，以 **Snowflake 模板**作为规范参考，仅调整仓库特定的收集查询。

模板文件遵循以下命名模式：
- `collect_<flow>.py` — 仅收集（查询仓库，写入 JSON manifest）
- `push_<flow>.py` — 仅推送（读取 manifest，发送到 Monte Carlo）
- `collect_and_push_<flow>.py` — 组合（从两者导入，按顺序运行）

**运行任何 push 脚本后**，你**必须**向用户显示 API 返回的 `invocation_id`。调用 ID 是在下游系统中追踪推送数据的唯一方式，也是验证所必需的。永远不要让推送完成而不向用户显示调用 ID — 他们需要这些 ID 用于 `/mc-validate-metadata`、`/mc-validate-lineage` 和调试。

## 规范 pycarlo API — 权威参考

以下导入、类和方法签名是 push ingestion 的**唯一**正确的 pycarlo API。如果你的训练数据建议使用不同的名称，**那是错误的**。严格按照此处列出的内容使用。

### 导入和客户端设置

```python
from pycarlo.core import Client, Session
from pycarlo.features.ingestion import IngestionService
from pycarlo.features.ingestion.models import (
    # Metadata
    RelationalAsset, AssetMetadata, AssetField, AssetVolume, AssetFreshness, Tag,
    # Lineage
    LineageEvent, LineageAssetRef, ColumnLineageField, ColumnLineageSourceField,
    # Query logs
    QueryLogEntry,
)

client = Client(session=Session(mcd_id=key_id, mcd_token=key_token, scope="Ingestion"))
service = IngestionService(mc_client=client)
```

### 方法签名

```python
# Metadata
service.send_metadata(resource_uuid=..., resource_type=..., events=[RelationalAsset(...)])

# Lineage (table or column)
service.send_lineage(resource_uuid=..., resource_type=..., events=[LineageEvent(...)])

# Query logs — note: log_type, NOT resource_type
service.send_query_logs(resource_uuid=..., log_type=..., events=[QueryLogEntry(...)])

# Extract invocation ID from any response
service.extract_invocation_id(result)
```

### RelationalAsset 结构（嵌套，非扁平）

```python
RelationalAsset(
    type="TABLE",  # ONLY "TABLE" or "VIEW" (uppercase) — normalize warehouse-native values
    metadata=AssetMetadata(
        name="my_table",
        database="analytics",
        schema="public",
        description="optional description",
    ),
    fields=[
        AssetField(name="id", type="INTEGER", description=None),
        AssetField(name="amount", type="DECIMAL(10,2)"),
    ],
    volume=AssetVolume(row_count=1000000, byte_count=111111111),  # optional
    freshness=AssetFreshness(last_update_time="2026-03-12T14:30:00Z"),  # optional
)
```

## 环境变量约定

所有生成的脚本**必须**使用这些确切的变量名。不要发明替代名称如 `MCD_KEY_ID`、`MC_TOKEN`、`MONTE_CARLO_KEY` 等。

| 变量 | 用途 | 使用者 |
|---|---|---|
| `MCD_INGEST_ID` | Ingestion key ID (scope=Ingestion) | push 脚本 |
| `MCD_INGEST_TOKEN` | Ingestion key secret | push 脚本 |
| `MCD_ID` | GraphQL API key ID | 验证脚本 |
| `MCD_TOKEN` | GraphQL API key secret | 验证脚本 |
| `MCD_RESOURCE_UUID` | 仓库资源 UUID | 所有脚本 |

## 此技能可以为你构建什么

告诉 Claude 你的仓库或数据平台以及 Monte Carlo 资源 UUID，此技能将生成一个可直接运行的 Python 脚本，它会：
- 使用该平台的惯用驱动程序连接到你的仓库
- 发现数据库、schema 和表
- 提取正确的列 — 名称、类型、行数、字节数、最后修改时间、描述
- 构建正确的 pycarlo `RelationalAsset`、`LineageEvent` 或 `QueryLogEntry` 对象
- 推送到 Monte Carlo 并保存包含 `invocation_id` 的输出 manifest 用于追踪

常见仓库（Snowflake、BigQuery、BigQuery Iceberg、Databricks、Redshift、Hive）均有可用模板。对于任何其他平台，Claude 将从仓库的系统目录或元数据 API 推导出合适的收集查询，并生成等效脚本。

### 可直接运行的示例

基于这些模板构建的生产就绪示例脚本已发布在 [mcd-public-resources](https://github.com/monte-carlo-data/mcd-public-resources) 仓库中：

- **[BigQuery Iceberg (BigLake) 表](https://github.com/monte-carlo-data/mcd-public-resources/tree/main/examples/push-ingestion/bigquery/push-iceberg-tables)** —
  为对 Monte Carlo 标准 pull collector（使用 `__TABLES__`）不可见的 BigQuery Iceberg 表收集元数据和查询日志。包含 `--only-freshness-and-volume` 标志，用于在初始完整元数据推送后进行快速定期推送，跳过 schema/fields 查询 — 适用于每小时的 cron 作业。

## 参考文档 — 何时加载

| 参考文件 | 加载时机… |
|---|---|
| `references/prerequisites.md` | 客户首次设置、遇到认证错误或需要帮助创建 API key |
| `references/push-metadata.md` | 构建或调试元数据收集脚本 |
| `references/push-lineage.md` | 构建或调试血缘关系收集脚本 |
| `references/push-query-logs.md` | 构建或调试查询日志收集脚本 |
| `references/custom-lineage.md` | 客户需要通过 GraphQL 创建自定义血缘节点或边 |
| `references/validation.md` | 验证推送的数据、运行 GraphQL 检查或删除 push-ingested 表 |
| `references/direct-http-api.md` | 客户想通过 curl/HTTP 直接调用 push API，不使用 pycarlo |
| `references/anomaly-detection.md` | 客户询问为什么新鲜度或数据量检测器未触发 |

## 前置条件 — 先读这个

→ 加载 `references/prerequisites.md`

需要两个单独的 API key。这是最常见的设置障碍：
- **Ingestion key** (scope=Ingestion) — 用于推送数据
- **GraphQL API key** — 用于验证查询

两者使用相同的 `x-mcd-id` / `x-mcd-token` 头，但指向不同的端点。

## 可以推送的内容

| 流程 | pycarlo 方法 | Push 端点 | 类型字段 | 过期时间 |
|---|---|---|---|---|
| 表元数据 | `send_metadata()` | `/ingest/v1/metadata` | `resource_type`（如 `"data-lake"`） | **永不过期** |
| 表血缘 | `send_lineage()` | `/ingest/v1/lineage` | `resource_type`（与元数据相同） | **永不过期** |
| 列血缘 | `send_lineage()`（事件包含 `fields`） | `/ingest/v1/lineage` | `resource_type`（与元数据相同） | **10 天后过期** |
| 查询日志 | `send_query_logs()` | `/ingest/v1/querylogs` | **`log_type`**（不是 `resource_type`！） | 与 pulled 相同 |
| 自定义血缘 | GraphQL mutations | `api.getmontecarlo.com/graphql` | 不适用 — 使用 GraphQL API key | 默认 7 天；设置 `expireAt: "9999-12-31"` 为永久 |

**重要**：查询日志使用 `log_type` 而不是 `resource_type`。这是唯一一个字段名称不同的 push 端点。有关支持的 `log_type` 值的完整列表，请参阅 `references/push-query-logs.md`。

pycarlo SDK 是可选的 — 你也可以通过 HTTP/curl 直接调用 push API。有关示例，请参阅 `references/direct-http-api.md`。

每次推送都会返回一个 `invocation_id` — 保存它。这是你在所有下游系统中的主要调试句柄。

## 步骤 1 — 生成收集脚本

让 Claude 为你的仓库构建脚本：

> "为 Snowflake 构建一个元数据收集脚本。我的 MC 资源 UUID 是 `abc-123`。"

`**/push-ingestion/scripts/templates/` 中的脚本模板（Snowflake、BigQuery、BigQuery Iceberg、Databricks、Redshift、Hive）是脚本生成的**强制起点** — 它们包含正确的 pycarlo 导入、模型构造器和 SDK 调用。**它们不是详尽的列表。** 如果客户的仓库未列出，请以模板作为指南，并确定适用于其平台的适当查询或文件收集方法。对于基于文件的源（如 Hive Metastore 日志），请提供检索文件、解析文件并将其转换为 push API 所需格式的命令。无论数据源是什么，push 格式和 SDK 调用都是相同的；只有收集查询会改变。

**批处理**：对于大型负载，将事件拆分为批次。每次 push 调用使用 **50 个资产**的批次大小。pycarlo HTTP 客户端有一个硬编码的 10 秒读取超时，无法覆盖（`Session` 和 `Client` 不接受 `timeout` 参数）— 较大的批次（200+）在拥有数千个表的仓库上会超时。压缩的请求体也不能超过 **1MB**（Kinesis 限制）。所有 push 端点都支持批处理。

**推送频率**：最多**每小时推送一次**。低于一小时的推送会产生不可预测的异常检测器行为，因为训练管道会聚合到小时桶中。

**每个流程，请参阅：**
- 元数据（schema + 数据量 + 新鲜度）：`references/push-metadata.md`
- 表和列血缘：`references/push-lineage.md`
- 查询日志：`references/push-query-logs.md`

## 步骤 2 — 验证推送的数据

推送后，使用 GraphQL API（GraphQL API key）验证数据在 Monte Carlo 中是否可见。

→ `references/validation.md` — 所有验证查询（getTable、getMetricsV4、getTableLineage、getDerivedTablesPartialLineage、getAggregatedQueries）

时间预期：
- **元数据**：几分钟内可见
- **表血缘**：几秒到几分钟内可见（通过快速直接路径到 Neo4j）
- **列血缘**：几分钟
- **查询日志**：至少 **15-20 分钟**（异步处理管道）

## 步骤 3 — 异常检测（可选）

如果你想让 Monte Carlo 的新鲜度和数据量检测器对推送的数据触发，你需要持续推送 — 检测器需要历史数据来训练。

→ `references/anomaly-detection.md` — 推荐的推送频率、最小样本数、训练窗口，以及如何回答客户询问检测器未激活的问题

## 自定义血缘节点和边

对于非仓库资产（dbt 模型、Airflow DAG、自定义 ETL 管道）或跨资源血缘，直接使用 GraphQL mutations：

→ `references/custom-lineage.md` — `createOrUpdateLineageNode`、`createOrUpdateLineageEdge`、`deleteLineageNode`，以及关键的 `expireAt: "9999-12-31"` 规则

## 删除 push-ingested 表

Push 表被排除在正常的基于 pull 的删除流程之外（这是有意为之的）。要显式删除它们，请使用 `deletePushIngestedTables` — 在 `references/validation.md` 的"表管理操作"部分中有说明。

## 可用的斜杠命令

客户可以显式调用这些命令，而不是用散文描述他们的意图：

| 命令 | 用途 |
|---|---|
| `/mc-build-metadata-collector` | 生成元数据收集脚本 |
| `/mc-build-lineage-collector` | 生成血缘关系收集脚本 |
| `/mc-build-query-log-collector` | 生成查询日志收集脚本 |
| `/mc-validate-metadata` | 通过 GraphQL API 验证推送的元数据 |
| `/mc-validate-lineage` | 通过 GraphQL API 验证推送的血缘关系 |
| `/mc-validate-query-logs` | 通过 GraphQL API 验证推送的查询日志 |
| `/mc-create-lineage-node` | 创建自定义血缘节点 |
| `/mc-create-lineage-edge` | 创建自定义血缘边 |
| `/mc-delete-lineage-node` | 删除自定义血缘节点 |
| `/mc-delete-push-tables` | 删除 push-ingested 表 |

## 调试检查点

当推送的数据未出现时，按顺序检查以下五个检查点：

1. **SDK 是否返回了 `202` 和 `invocation_id`？**
   如果没有，网关拒绝了请求 — 检查认证头和 `resource.uuid`。

2. **集成 key 类型是否正确？**
   必须是 scope `Ingestion`，通过 `montecarlo integrations create-key --scope Ingestion` 创建。
   标准 GraphQL API key 不适用于 push。

3. **`resource.uuid` 是否正确且已授权？**
   key 可以限定到特定的仓库 UUID。如果 UUID 不匹配，会返回 `403`。

4. **标准化器是否处理了它？**
   使用 `invocation_id` 在 CloudWatch 日志中搜索相关的 Lambda。对于查询日志，检查 `log_type` — Hive 需要 `"hive-s3"`，而不是 `"hive"`。

5. **下游系统是否接收到了？**
   - 元数据：在 GraphQL 中查询 `getTable`
   - 表血缘：在几秒到几分钟内检查 Neo4j（通过 PushLineageProcessor 的快速路径）
   - 查询日志：等待至少 15-20 分钟；检查 `getAggregatedQueries`

## 已知注意事项

- **`log_type` 与 `resource_type`**：元数据和血缘使用 `resource_type`（如 `"data-lake"`）；查询日志使用 **`log_type`** — 这是唯一一个字段名称不同的端点。错误的值 → `Unsupported ingest query-log log_type` 错误。
- **必须保存 `invocation_id`**：每个输出 manifest 都应包含它 — 这是请求离开 SDK 后唯一的追踪句柄。
- **查询日志异步延迟**：至少 15-20 分钟。`getAggregatedQueries` 在处理完成前会返回 0 — 这是预期行为，不是 bug。
- **自定义血缘 `expireAt` 默认为 7 天**：除非你设置 `expireAt: "9999-12-31"`，否则节点会静默消失。
- **Push 表永远不会自动删除**：定期清理作业默认排除它们（`exclude_push_tables=True`）。通过 `deletePushIngestedTables` 显式删除它们（每次调用最多 1,000 个 MCON；同时删除血缘节点和所有接触这些节点的边）。
- **异常检测器需要历史数据**：仅推送一次是不够的。新鲜度需要在约 2 周内进行 7 次以上的推送；数据量需要在约 42 天内进行 10-48 次样本。最多每小时推送一次。
- **大型负载需要批处理**：压缩的请求体不得超过 1MB。将大型事件列表拆分为批次。
- **列血缘在 10 天后过期**：与表元数据和表血缘（永不过期）不同，列血缘有 10 天的 TTL，与 pulled 列血缘相同。
- **在仓库查询中引用 SQL 标识符**：数据库、schema 和表名必须被引用以处理混合大小写或特殊字符。引用语法因仓库而异 — Snowflake 和 Redshift 使用双引号（`"{db}"`），BigQuery/Databricks/Hive 使用反引号（`` `db` ``）。模板已经为每个仓库正确处理了这一点 — 调整时遵循相同的引用模式。

## 内存安全

生成的脚本必须包含启动内存检查。收集阶段会将查询历史行加载到内存中进行解析 — 在具有长回溯窗口的大型仓库上，这可能会耗尽可用 RAM 并导致进程被静默终止（SIGKILL / exit 137），没有回溯信息。

在每个生成的脚本的顶部（导入之后）添加此模式：

```python
import os

def _check_available_memory(min_gb: float = 2.0) -> None:
    """Warn if available memory is below the threshold."""
    try:
        if hasattr(os, "sysconf"):  # Linux / macOS
            page_size = os.sysconf("SC_PAGE_SIZE")
            avail_pages = os.sysconf("SC_AVPHYS_PAGES")
            avail_gb = (page_size * avail_pages) / (1024 ** 3)
        else:
            return  # Windows — skip check
    except (ValueError, OSError):
        return
    if avail_gb < min_gb:
        print(
            f"WARNING: Only {avail_gb:.1f} GB of memory available "
            f"(minimum recommended: {min_gb:.1f} GB). "
            f"Consider reducing the lookback window or increasing available memory."
        )
```

在连接到仓库之前调用 `_check_available_memory()`。

此外，在获取查询历史时：
- 尽可能使用 `cursor.fetchmany(batch_size)` 循环而不是 `cursor.fetchall()`
- 对于非常大的结果集，考虑添加 LIMIT 子句并分窗口处理

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。