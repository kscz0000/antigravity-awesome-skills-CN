---
name: monte-carlo-asset-health
description: 使用 Monte Carlo 检查数据表/资产的健康状况。激活词："表X怎么样"、"检查X的健康"、"X健康吗"、"X的状态"、"查看X表"、"资产健康"、"数据表状态"、"表健康检查"，或任何关于数据资产健康/状态的问题。
risk: unknown
source: https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/asset-health
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/monte-carlo-data/mc-agent-toolkit/blob/main/LICENSE
---

# Monte Carlo 资产健康检查技能

本技能使用 Monte Carlo 可观测性平台检查数据资产的健康状况，生成结构化的健康报告，涵盖新鲜度、告警、监控覆盖、重要性和上游依赖健康情况。

> **Monte Carlo 工具路由（必需）：** 始终通过本插件绑定的服务器调用 Monte Carlo MCP 工具，其完全限定工具名为
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__<tool>`（例如
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__get_alerts`）。本技能中使用的裸工具名
>（`get_alerts`、`search`、`get_table`、…）均指该绑定服务器。如果会话中还有单独配置的 `monte-carlo-mcp` 服务器，请**不要**路由到它——它可能指向不同的端点或凭证。

## 必需：执行前阅读参考文件

**在发起任何 MCP 工具调用之前，必须使用 Read 工具阅读以下两个参考文件。** 这些文件是工具调用、参数和响应解读的权威来源。本文件仅定义激活时机和输出格式。

1. `references/workflows.md`（相对于本文件）—— 精确的工具调用、阶段和执行顺序
2. `references/parameters.md`（相对于本文件）—— 参数约定和字段详情

**在阅读完两个文件之前，不要发起任何 MCP 工具调用。**

## 何时激活本技能

当用户满足以下条件时激活：

- 询问健康状况："表 X 怎么样？"、"检查 X 的健康"、"X 健康吗？"
- 询问状态："X 的状态是什么？"、"orders 表的状态"
- 要求检查某张表："查看 X 表"、"关注一下 X"
- 询问特定资产的可靠性、新鲜度或质量
- 在事件分诊或变更规划的上下文中引用某张表

## 何时不激活本技能

- **分析或探索表数据**（行数、列统计、分布）→ 使用 `explore-table`
- **创建或建议监控器** → 使用 `monitoring-advisor`
- **活跃事件分诊**（调查正在触发的告警根因）→ 使用 prevent 技能的工作流 3

## 健康报告格式

**关键：仅报告 `references/workflows.md` 中定义的工具所返回的数据。不要调用额外工具，不要推断或编造指标。下方每行均明确指定了数据来源工具。**

**所有章节（活跃告警、监控器、上游问题、建议）必须始终显示其标题。** 永远不要省略任何章节——如果没有数据，显示下方定义的空状态文本。

**永远不要使用 emoji 短代码**（如 `:warning:` 或 `:arrow_up:`）。直接使用 Unicode emoji 字符（如 ⚠️）或纯文本。短代码在终端中会显示为原始文本。

**始终将 URL 显示为裸 URL**，而非 markdown 链接（例如，不要写成 `[text](https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/asset-health/url)`）。

**`{MC_WEBAPP_URL}` 在本模板中多处出现。** 每次出现都必须替换为调用 `get_mc_webapp_url()` 返回的实际值。永远不要硬编码或猜测此 URL——它因环境而异。

按以下结构呈现结果：

```
## Health Check: <table_name>

**Tags:** `tag1:value1`, `tag2:value2` (or "None" if no tags)
**Link:** {MC_WEBAPP_URL}/assets/{mcon}
**Warehouse:** snowflake-prod (Snowflake)
**Status: 🟢 Healthy / 🟡 Degraded / 🔴 Unhealthy** | **Importance:** 0.85 (key asset ⭐️)
**Avg Reads/Day:** ~538 | **Avg Writes/Day:** ~12

| Metric        | Value                          | Signal |
|---------------|--------------------------------|--------|
| Last Activity | Apr 6, 2025                    | 🟢 Recent    |
| Alerts        | 2 active                       | 🔴 Has alerts |
| Monitoring    | 3 active monitors              | 🟢 Monitored  |
| Upstream      | 1/3 sources unhealthy          | 🔴 Issues     |

### Active Alerts

| Date  | Type           | Priority | Status           | Link                                                    |
|-------|----------------|----------|------------------|---------------------------------------------------------|
| Apr 8 | Metric anomaly | P3       | Not acknowledged | {MC_WEBAPP_URL}/alerts/{alert_uuid} |
| Apr 7 | Freshness      | P2       | Acknowledged     | {MC_WEBAPP_URL}/alerts/{alert_uuid} |

If there are more than 5 active alerts, display only 5. Do NOT put the overflow
message inside the table as a row. Instead, put it as plain text on the line
immediately after the table:

There are N more alerts not shown for brevity

If there are zero active alerts, show:
No active alerts in the last 7 days.

### Monitors

| Type        | Name                                    | Incidents (7d) | Status              |
|-------------|-----------------------------------------|----------------|---------------------|
| TABLE       | Orders freshness and schema             | 3              | Running hourly      |
| METRIC      | Revenue row count                       | 0              | Never executed      |
| BULK_METRIC | Warehouse volume check                  | 21             | ⚠️ 1 table has errors |

If there are zero monitors, show:
No monitors configured for this table.

### Upstream Issues
- raw_orders — FRESHNESS alert: not updated in 8h
- raw_payments — healthy
- dim_customers — healthy

> Want me to check further upstream for **raw_orders**?

If there are no upstream dependencies, show:
No upstream dependencies found.

### Diagnosis

1-2 sentences summarizing what is causing the table to be unhealthy, or
confirming it is healthy. This should naturally lead into the recommendations.

Example (unhealthy):
Upstream table raw_orders has not been updated in 8 hours, which is likely
causing staleness in this table. There are also 2 unacknowledged alerts.

Example (healthy):
Table is healthy — no active alerts, monitored, and all upstream sources
are in good shape.

### Recommendations
- Investigate upstream raw_orders freshness — likely root cause of this table's staleness
- Acknowledge or investigate the 2 active alerts

If there are no recommendations, show:
No recommendations — table looks healthy.

```

### 指标定义 — 精确数据来源

每个指标行必须仅使用指定的数据来源。不要添加、推断或润色超出工具返回范围的值。

| 指标 | 数据来源 | 显示内容 | 信号 |
|------|---------|---------|------|
| **最后活动** | `get_table` → `last_activity` | 最后活动日期（如 "Apr 6, 2025"） | 🟢 近期（7天内）/ 🟡 过期（超过7天） |
| **告警** | `get_alerts` → 计数 | "N 个活跃" 或 "无活跃告警" | 🔴 有告警 / 🟢 无告警 |
| **监控** | `get_monitors` → `is_paused` 为 false 的计数 | "N 个活跃监控器" 或 "0 个活跃监控器（M 个已暂停）"。包含监控器字段中的相关详情（事件数、错误数、类型）。 | 🟢 已监控（≥1 个活跃）/ 🔴 未监控（0 个活跃） |
| **上游** | `get_asset_lineage`（上游）+ 阶段 3 检查 | "N/M 个上游源不健康" 或 "全部 N 个上游源健康" | 🔴 有问题（任何不健康）/ 🟢 健康（全部健康） |

**重要性**显示在状态行旁边（不在指标表中）。来源：`get_table` → `importance_score` + `is_important`。如果是关键资产或重要性 > 0.8，显示 "X.XX (关键资产 ⭐️)"，否则仅显示 "X.XX"。

**日均读取**和**日均写入**显示在状态行下方。来源：`get_table` → `table_stats.avg_reads_per_active_day` 和 `table_stats.avg_writes_per_active_day`。

**不要包含下游数据。** 本技能仅查询上游血缘。

### 状态判定

- **🔴 不健康：** 资产上有任何活跃告警（来自 `get_alerts`，状态为 `["NOT_ACKNOWLEDGED", "ACKNOWLEDGED", "WORK_IN_PROGRESS"]`——参见 `parameters.md`）
- **🟡 降级：** 无活跃告警，但高重要性资产（重要性 > 0.8 或关键资产）上没有活跃监控器
- **🟢 健康：** 无活跃告警且至少有 1 个活跃监控器

### 标签

显示 `search` 工具 `properties` 字段中的标签。以内联徽章形式显示：`key:value`。如果没有标签，显示 "None"。始终包含标签行。

### 数据仓库

显示 `search` 结果中的数据仓库名称和类型。始终包含此行。

### 建议

仅包含可从已收集数据推导出的建议：
- 可能是根因的上游健康问题
- 需要确认或调查的活跃告警
- 不要建议具体的监控器类型——这超出了本技能的范围

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代针对具体环境的测试、安全审查或用户对破坏性/高成本操作的批准。
