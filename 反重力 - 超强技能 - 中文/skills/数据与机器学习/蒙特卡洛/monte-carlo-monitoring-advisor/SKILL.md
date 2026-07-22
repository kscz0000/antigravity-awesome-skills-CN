---
name: monte-carlo-monitoring-advisor
description: 分析数据覆盖率，为仓库表和AI智能体创建监控。覆盖范围包括覆盖率缺口、用例分析、数据监控创建及智能体可观测性。
risk: unknown
source: https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/monitoring-advisor
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/monte-carlo-data/mc-agent-toolkit/blob/main/LICENSE
---

# Monte Carlo 监控顾问技能

本技能处理所有监控请求——覆盖率分析、数据监控创建和AI智能体监控。根据用户意图路由到对应的参考文件。

> **Monte Carlo 工具路由（必需）：** 始终通过此插件捆绑的服务器调用 Monte Carlo MCP 工具，其完全限定工具名称为
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__<tool>`（例如
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__get_alerts`）。本技能中使用的裸工具名
>（`get_alerts`、`search`、`get_table` 等）均指该捆绑服务器。如果会话中还有单独配置的
> `monte-carlo-mcp` 服务器，**不要**路由到它——它可能指向不同的端点或凭证。

参考文件位于本技能文件旁。**使用 Read 工具**（而非 MCP 资源）访问它们：

- 数据监控创建流程：`references/data-monitor-creation.md`（相对于本文件）
- 智能体监控创建流程：`references/agent-monitor-creation.md`（相对于本文件）
- 各类型参考：`references/data-*.md` 和 `references/agent-*.md`（相对于本文件）

## 何时激活本技能

当用户出现以下情况时激活：

- 询问监控覆盖率、数据覆盖率或覆盖率缺口
- 想了解仓库中哪些被监控、哪些未被监控
- 询问用例、用例关键性或用例分析
- 想探索数据资产并找出需要监控的内容
- 说类似"我应该监控什么？""我的覆盖率缺口在哪里？""给我看看我的用例"
- 询问具有异常的未监控表或基于重要性的优先级排序
- 要求创建、添加或设置监控（例如"给……添加监控""在……上创建新鲜度检查""为……设置验证"）
- 提到监控特定的表、字段或指标
- 想检查数据质量规则或实施数据契约
- 询问表或数据集的监控选项
- 请求监控即代码 YAML 生成
- 想在新的转换逻辑之后添加监控（当预防技能未激活时）
- 询问监控AI智能体、智能体延迟、智能体令牌用量或智能体质量
- 想对智能体行为或执行模式设置告警
- 询问调查智能体追踪或对话
- 说类似"监控我的智能体""追踪智能体延迟""对智能体错误发出告警"
- 询问智能体评估监控、轨迹监控或验证监控
- 提到智能体可观测性或智能体监控

## 何时不激活本技能

当用户出现以下情况时不激活：

- 仅查询数据或浏览表内容
- 分类或响应活跃告警（使用预防技能的工作流3）
- 在代码变更前运行影响评估（使用预防技能的工作流4）
- 询问现有监控配置（直接使用 `get_monitors`）
- 编辑或删除现有监控

---

## 前提条件

- **必需：** Monte Carlo MCP 服务器（`monte-carlo-mcp`）必须已配置并通过认证
- **可选：** 数据库 MCP 服务器（Snowflake、BigQuery、Redshift、Databricks）用于对表使用模式进行 SQL 分析

---

## 可用 MCP 工具

所有工具通过 `monte-carlo-mcp` MCP 服务器可用。

### 覆盖率与发现工具

| 工具 | 用途 |
| --- | --- |
| `get_warehouses` | 列出可访问的仓库（需首先调用——`get_use_cases` 需要 `warehouse_id`） |
| `get_use_cases` | 列出用例及其关键性、描述、表数量、预计算标签名 |
| `get_use_case_table_summary` | 某用例的关键性分布（HIGH/MEDIUM/LOW 表数量） |
| `get_use_case_tables` | 分页表列表，含关键性、金表状态、MCON |
| `get_monitors` | 通过 `mcons` 过滤器检查特定表的监控状态 |
| `get_asset_lineage` | 表的上游/下游依赖关系（接受 MCON + 方向参数） |
| `get_audiences` | 列出通知受众 |
| `get_unmonitored_tables_with_anomalies` | 具有已静默的 OOTB 异常但无监控的表（接受 ISO 8601 时间范围） |
| `search` | 按名称查找表；支持 `is_monitored` 过滤 |
| `get_table` | 表详情、字段、统计信息、域成员关系 |
| `get_queries_for_table` | 某表的查询日志（源/目标） |
| `get_field_metric_definitions` | 某仓库中各字段类型可用的指标 |
| `get_domains` | 列出 Monte Carlo 域 |
| `get_validation_predicates` | 可用的验证规则类型 |

### 数据监控创建工具

全部五个工具遵循**两次调用预览-确认模式**：第一次调用（使用默认的 `dry_run=True`）返回渲染后的 MaC YAML 供审阅；第二次调用（`dry_run=False`）部署监控并返回其深度链接。在任一调用中传入 `monitor_uuid` 可原地更新现有监控而非创建新监控。完整流程见 `references/data-monitor-creation.md`。

| 工具 | 用途 |
| --- | --- |
| `create_or_update_table_monitor` | 创建或更新表监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |
| `create_or_update_metric_monitor` | 创建或更新指标监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |
| `create_or_update_validation_monitor` | 创建或更新验证监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |
| `create_or_update_sql_monitor` | 创建或更新自定义 SQL 监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |
| `create_or_update_comparison_monitor` | 创建或更新比较监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |

### 智能体监控工具

| 工具 | 用途 |
| --- | --- |
| `get_agent_metadata` | 列出AI智能体——返回智能体名称、`agentReference` 值（创建监控时的 `agent` 参数）、追踪表 MCON、源类型 |
| `get_agent_conversation` | 获取某智能体最近的 LLM 交互/对话 |
| `get_agent_trace` | 检查执行追踪和跨度树 |
| `create_or_update_agent_metric_monitor` | 创建或更新定量跨度级指标的监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |
| `create_or_update_agent_evaluation_monitor` | 创建或更新 LLM 评估质量指标的监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |
| `create_or_update_agent_trajectory_monitor` | 创建或更新执行模式告警的轨迹监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |
| `create_or_update_agent_validation_monitor` | 创建或更新逻辑断言的验证监控（`dry_run=True` 时预览 YAML，`dry_run=False` 时部署） |

---

## 路由

当用户请求到达时，确定应遵循哪个工作流：

| 用户意图 | 工作流 |
| --- | --- |
| 覆盖率分析、用例探索、"我应该监控什么？" | **覆盖率工作流**（如下） |
| 为已知表创建特定数据监控 | **阅读 `references/data-monitor-creation.md`** 并遵循其流程 |
| 监控AI智能体、智能体延迟、智能体质量、智能体追踪 | **阅读 `references/agent-monitor-creation.md`** 并遵循其流程 |
| 覆盖率分析导向监控创建 | 完成覆盖率工作流后，**阅读 `references/data-monitor-creation.md`** 进行创建 |

读取参考文件时，始终使用 **Read 工具**，路径相对于本技能文件。

---

## 覆盖率工作流

当用户询问监控覆盖率、覆盖率缺口或应该监控什么时，使用此主流程。

### 步骤1：发现仓库

调用 `get_warehouses` 列出所有可访问的仓库。

- 如果只有**一个**仓库：自动选择，进入步骤2。
- 如果有**多个**仓库：展示仓库名称（绝不展示 UUID），询问用户要探索哪一个。

### 步骤2：发现用例

调用 `get_use_cases(warehouse_id=<选定的>)` 发现所选仓库的用例。

- 如果**存在用例** --> 进入**用例探索**（如下）。
- 如果**无用例** --> 进入**基于重要性的回退方案**（如下）。

### 步骤3：检查数据库 MCP（可选）

通过查找工具列表中包含 `snowflake`、`bigquery`、`redshift` 或 `databricks` 的工具，检查用户是否有可用的数据库 MCP 服务器。如果有，记录下来以备后续 SQL 分析步骤。如果没有，跳过 SQL 分析。

---

## 用例探索

当用例已定义时，使用此主流程。

### 展示用例

- 按关键性排序：**HIGH** 在前，**MEDIUM** 次之，**LOW** 在后。
- 对每个用例，展示其描述，并解释其关键性等级的理由，让用户理解其重要性。
- 调用 `get_use_case_tables`（`golden_tables_only=true`）并提及具体的金表名称作为实例。金表是仓库中的最后一层——它们供给 ML 模型、仪表盘和报表。适时解释这一点。
- 使用 `get_asset_lineage` 解释用例中表的连接关系以及某些表为何重要（例如具有许多上游依赖的金表）。

### "创建用例"请求

你**无法**创建用例——它们由 Monte Carlo 自动生成（包括其关键性），没有工具可以手动创建。当用户要求"创建""设置"或"定义"用例时：简要说明这一点，不要静默替换为监控部署。然后提供你对所提及的表**能做**的事——查找现有用例/关键性、推荐字段监控、生成监控预览或分析覆盖率缺口——并对可执行部分采取行动，不要扩展到兄弟表。

### 分析覆盖率

1. 调用 `get_use_case_table_summary` 展示该用例在各关键性级别（HIGH/MEDIUM/LOW）有多少表。
2. 调用 `get_use_case_tables` 获取表的 MCON，然后调用 `get_monitors(mcons=[...])` 报告已监控与未监控的数量。
3. **默认范围为 HIGH + MEDIUM 关键性。** 这覆盖了最重要的表，不会让用户不堪重负。不要询问用户使用哪个范围——直接执行。如果他们想包含 LOW 关键性的表，他们会提出。
4. 你可以在一次会话中建议覆盖**多个**用例。
5. **倾向行动而非提问。** 当范围明确时（选定用例的 HIGH + MEDIUM），直接为所有推荐的监控生成预览。以"退出"而非"加入"的方式呈现："我将为全部 N 个监控生成预览——告诉我是否要跳过任何。"不要逐个询问"你想创建哪个？"——批量处理。

### 利用异常数据识别覆盖率缺口

使用 `get_unmonitored_tables_with_anomalies` 发现**未被监控**但已有静默 OOTB 异常的表。这揭示了真正的覆盖率缺口——Monte Carlo 检测到了数据问题但没有配置监控来通知任何人。

- 使用最近的时间窗口（如最近 7-30 天），传入 ISO 8601 时间戳。
- 结果按**重要性分数**排序——最关键的缺口排在前面。
- 每个结果包含异常事件样本，展示检测到的问题类型（新鲜度、数据量、模式变更）。
- 利用此功能**优先排序**应首先覆盖的未监控表——有近期异常的表比无活动的表更值得监控。
- 与用例数据交叉引用：如果具有异常的未监控表属于关键用例，提升其优先级。

---

## 基于重要性的回退方案

当未定义用例时，回退到基于重要性的表发现。

1. **查找未监控表：** 使用 `search(query="", is_monitored=false)` 查找按重要性排序的未监控表。
2. **查找有异常的表：** 使用 `get_unmonitored_tables_with_anomalies`（最近 14-30 天时间窗口）查找有近期异常但无监控的表。
3. **检查顶级候选：** 使用 `get_table` 检查最重要的未监控表的详情、字段和统计信息。
4. **通过血缘理解关键性：** 使用 `get_asset_lineage`（`direction="DOWNSTREAM"`）了解哪些表连接最多——下游依赖多的表更值得监控。
5. **优先排序：** 按重要性分数和异常活动对候选排序。向用户展示顶级候选并附理由。

### 重要提示

- **不要将重要性分数呈现为业务关键性。** 始终解释重要性分数是计算得出的指标（查询频率、下游依赖、使用模式），而非业务定义的关键性。
- 告知用户其账户**尚未**有用例数据——用例由 Monte Carlo 从仓库元数据自动生成并作为资产标签展示；它们不是通过 UI 手动配置的。
- 在此模式下，你仍可为单个表创建指标监控、验证监控和自定义 SQL 监控——只是不会使用基于标签的表监控，因为没有用例标签。

---

## SQL 分析（可选）

如果在覆盖率工作流的步骤3中检测到数据库 MCP 服务器：

1. 调用 `get_queries_for_table` 查看候选表上的近期查询模式。
2. 使用数据库 MCP 工具（如 `snowflake_query`、`bigquery_query`）分析表使用情况——识别哪些表查询最频繁，哪些列用于 JOIN 和 WHERE 子句。
3. 利用此信息优化监控建议——查询频繁但无监控的表是高优先级缺口。

如果没有可用的数据库 MCP，完全跳过此步骤。不要要求用户配置一个。

---

## 创建前上下文（覆盖率驱动）

当覆盖率分析导向监控创建时，在读取创建参考文件之前收集以下上下文：

1. **先去重。** 在生成用例标签监控之前，调用 `get_monitors`（使用与监控 `asset_selection.filters` 中相同的标签对，`monitor_types=["TABLE"]`）。如果已有监控覆盖该 `(tag, domain)` 范围，展示它（描述、uuid）并询问是更新它（传入其 `monitor_uuid`）、添加一个不同范围的监控，还是跳过——不要静默重新创建。后端对表监控按 `(description, domain)` 进行 upsert，因此相同描述的定义会静默覆盖先前监控的设置。
2. 调用 `get_audiences` 列出通知受众。建议一个或多个相关受众（按团队或用例上下文匹配）并询问用户选择哪些——可以选**一个或多个**。这是生成前需要询问的**唯一**问题；不要同时询问草稿/激活状态或调度。默认为**草稿**（`is_draft=True`）；用户看到预览后可切换为激活。
3. 传入 `audiences` 或 `failure_audiences` 时，使用受众的**名称/标签**（而非 UUID），以列表形式——每个选定的受众一个条目。
4. **绝不编造信用成本。** 不要给出通用的每监控或每字段 MC 信用费率——成本随具体规格（分段、调度、字段数量）而变化。如果预览响应包含后端估算（如 `estimated_credits.credits_per_day`），则报告该值；否则拒绝估算，并提供预览特定监控或用例以获取真实估算。

### 用例标签监控

覆盖率分析最常见的输出是通过 `create_or_update_table_monitor` 创建的**按用例标签限定范围的表监控**。`asset_selection` 参数使用以下结构：

```json
{
  "databases": ["<database_name>"],
  "schemas": ["<schema_name>"],
  "filters": [
    {
      "type": "TABLE_TAG",
      "tableTags": ["<tag_key>:<criticality>"],
      "tableTagsOperator": "HAS_ANY"
    }
  ]
}
```

规则：
- 过滤器 `type` 对于用例监控**始终**为 `TABLE_TAG`。
- `tableTagsOperator` 应为 `HAS_ANY`。
- `tableTags` 中的每个条目为 `"<tag_key>:<value>"`，其中标签键是 `get_use_cases` 输出中的预计算标签名，值为小写的关键性级别（`high`、`medium`、`low`）。
- 仅监控 HIGH 关键性表：`["tag_name:high"]`
- 监控 MEDIUM + HIGH：`["tag_name:high", "tag_name:medium"]`
- 监控全部：`["tag_name:high", "tag_name:medium", "tag_name:low"]`

### 监控标题（`description`）和理由（`notes`）

保持二者区分——创建工具都接受这两个字段。后端自动生成监控的 `name` slug；`description` 是用户看到的标题。

- **`description`——标题。** 简短且可扫描（约 80 字符以内），纯文本，命名资产/用例和关键性范围。不要在此塞入理由。
- **`notes`——理由。** 1-3 句话回答"为什么要这个监控？"，基于关键性、范围和下游影响。

用例标签监控示例：

- **不好的 description**（这是理由，不是标题）：`"监控 Revenue Reporting 用例中的 HIGH 关键性表，以在问题影响仪表盘和财务报表之前发现它们。"`
- **好的 description：** `"Revenue Reporting 覆盖率 -- HIGH + MEDIUM 关键性表"`
- **好的 notes**（配套）：`"覆盖 Revenue Reporting 用例中 HIGH/MEDIUM 关键性的表。在新鲜度、数据量和模式问题到达仪表盘和财务报表之前发现它们。"`

---

## 临时表和截断重载表

某些表在直接查询时显示 0 行，但在 Monte Carlo 元数据中有近期的写入活动。这些是**临时表**——每次管道运行时完全替换（截断重载模式）。及早识别此模式可避免浪费时间查询空表。

临时表的特征：
- `get_table` 显示近期的 `last_write` 时间戳和较高的读/写活动
- 直接 SQL 查询返回 0 行或全为 NULL 的时间戳列
- Monte Carlo 检测到新鲜度异常（表在两次加载之间保持空的时间超过预期）

---

## 优雅降级

优雅地处理缺失或不可用的工具：

| 场景 | 行为 |
| --- | --- |
| 未定义用例 | 回退到基于重要性的发现 |
| 无可用的数据库 MCP | 跳过 SQL 分析，仅依赖 MC 工具 |
| `get_unmonitored_tables_with_anomalies` 返回空 | 说明未发现近期异常；继续基于用例或重要性的优先排序 |
| `get_use_case_tables` 返回无表 | 说明该用例无表；建议探索其他用例 |
| `get_audiences` 返回空 | 告知用户未配置受众；仍可创建监控但不进行通知路由 |
| 用户无仓库 | 告知用户无可访问的仓库；可能需要检查其 Monte Carlo 权限 |

绝不因某个工具返回空结果就报错或中断对话。解释发生了什么并提供次优路径。

---

## 规则

- **绝不向用户暴露 UUID、MCON 或内部标识符**——始终使用人类可读的名称表示仓库、受众、用例和表。仅在工具调用中使用内部标识符。
- 当用户询问表之间的关系时，使用 `get_asset_lineage` 获取上游/下游连接并解释数据流。
- 简洁但全面。使用项目符号和表格以求清晰。
- 在工具调用中始终使用 **ISO 8601** 格式的日期时间值。
- 绝不重新格式化创建工具返回的 YAML 值。
- 向监控创建工具传入 `audiences` 或 `failure_audiences` 时，使用受众的**名称/标签**（而非 UUID）。API 接受受众名称。

## 局限性

- 仅当任务明确匹配其上游源和本地项目上下文时使用本技能。
- 在应用变更前验证命令、生成的代码、依赖、凭证和外部服务行为。
- 不要将示例替代特定环境的测试、安全审查或用户对破坏性或高成本操作的审批。
