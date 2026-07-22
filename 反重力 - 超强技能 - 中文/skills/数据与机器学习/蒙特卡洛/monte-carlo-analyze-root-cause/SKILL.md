---
name: monte-carlo-analyze-root-cause
description: "调查数据事件并使用 Monte Carlo 的可观测性数据定位根因。引导智能体进行系统性排查：告警查询、血缘追踪、ETL 检查、查询分析和数据画像。当用户询问数据问题、事件、告警、异常时激活。"
risk: unknown
source: https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/analyze-root-cause
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/monte-carlo-data/mc-agent-toolkit/blob/main/LICENSE
---

# Monte Carlo 根因分析技能

本技能帮助调查数据事件——新鲜度延迟、数据量异常、Schema 变更、字段指标漂移以及 ETL 失败——通过引导智能体使用 Monte Carlo 的 MCP 工具进行系统性排查。它将可观测性元数据与可选的直接数据查询相结合，定位根因。

> **Monte Carlo 工具路由（必须遵守）：** 始终通过本插件绑定的服务器调用 Monte Carlo MCP 工具，
> 其完全限定工具名为
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__<tool>`（例如
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__get_alerts`）。本技能中使用的裸工具名
> （`get_alerts`、`search`、`get_table`、……）均指该绑定服务器。如果会话中还有
> 单独配置的 `monte-carlo-mcp` 服务器，**不要**路由到它——它可能指向不同的端点或凭证。

参考文件位于本技能文件旁边。**使用 Read 工具**（而非 MCP 资源）访问它们：

- 按问题类型的排查手册：`references/<type>-investigation.md`
- 数据探索模式：`references/data-exploration.md`
- 无事件 ID 时的接诊流程：`references/intake-no-incident.md`
- 常见根因目录：`references/common-root-causes.md`

## 何时激活本技能

当用户出现以下情况时激活：

- 提到 Monte Carlo 告警、事件或异常
- 问"为什么这张表不更新了？"或"为什么行数下降了？"
- 想调查数据质量问题
- 询问新鲜度、数据量或 Schema 问题
- 提到管道失败（Airflow、dbt、Databricks）
- 说"调试这个告警"、"调查这个事件"、"根因分析"等

## 何时不激活本技能

当用户处于以下情况时不激活：

- 创建监控（使用 monitoring-advisor 技能）
- 在代码变更前做影响评估（使用 prevent 技能）
- 查看存储成本（使用 storage-cost-analysis 技能）
- 在没有具体事件的情况下探索管道性能（使用 performance-diagnosis 技能）

## 前提条件

**必需：** Monte Carlo MCP 服务器（`integrations.getmontecarlo.com/mcp`）必须已配置并完成认证。

**可选但推荐：**
- **数据库 MCP 服务器**（Snowflake、BigQuery、Redshift、Databricks）——支持直接 SQL 查询以进行更深入的数据调查。没有它，本技能仍可使用 MC 的元数据工具进行分析，但无法对实际数据进行画像。
- **GitHub MCP 服务器**——支持搜索可能导致问题的近期 PR。没有它，本技能回退到 MC 的查询变更检测。

## 使用的 MCP 工具

### 来自 Monte Carlo MCP 服务器

| 工具 | 用途 |
|------|------|
| `get_alerts` | 获取事件/告警详情 |
| `search` | 按名称或关键词查找表 |
| `get_table` | 表元数据和字段 |
| `get_asset_lineage` | 表级上下游血缘 |
| `get_field_lineage` | 字段级血缘（追踪问题数据到源列） |
| `get_table_freshness` | 表更新/新鲜度历史 |
| `get_table_size_history` | 行数和大小历史 |
| `get_queries_for_table` | 读写查询历史 |
| `get_query_changes` | 检测 SQL 文本变更 |
| `get_query_rca` | 失败/无效/遗漏查询的根因分析 |
| `get_etl_issues` | ETL 管道问题——传入 `platform`（"airflow"、"dbt"或"databricks"） |
| `get_etl_jobs` | 查找写入特定表的 ETL 作业——传入 `platform` 参数 |
| `get_github_prs` | 账户 MC GitHub 集成的近期 PR |
| `get_jobs_performance` | 作业运行时统计、失败率、7 天趋势 |
| `get_change_timeline` | 统一时间线：查询变更 + 数据量 + ETL 失败 |
| `get_current_time` | 当前时间戳，用于相对时间范围 |
| `alert_assessment` | 可选的约 2 分钟事件分诊——返回 HIGH/MEDIUM/LOW 置信度和影响。适合在决定升级到 TSA 之前快速判断。 |
| `run_troubleshooting_agent` | 对事件启动排查智能体（TSA）。默认异步；幂等（返回已有结果，除非传入 `force_rerun=True`）。当存在事件 UUID 时在步骤 1.5 自动调用。 |
| `get_troubleshooting_agent_results` | 轮询事件的 TSA 结果（`status` 为 `not_found` / `running` / `success` / `failed`）。用于检查步骤 1.5 启动的异步运行。 |

> **额度消耗：** `alert_assessment` 和 `run_troubleshooting_agent` 消耗 Monte Carlo 额度，与在 Monte Carlo UI 中启动排查智能体的方式相同。每次新的 `run_troubleshooting_agent` 调用都是一次计费运行；通过内置幂等性复用（除非用户明确要求重新分析，否则不要传入 `force_rerun=True`）。

### 可选的外部 MCP 工具

| 工具 | 用途 |
|------|------|
| 数据库 MCP（Snowflake、BigQuery 等） | 运行 SQL 查询进行数据画像 |
| GitHub MCP | 搜索近期 PR（MC 的 `get_github_prs` 的替代——适用于账户未配置 MC GitHub 集成的情况） |

---

## 工作流

### 步骤 1：理解问题（接诊）

**如果用户提供了告警或事件 ID：**
1. 使用告警 ID 调用 `get_alerts` 获取详情。
2. 确认：受影响的表、问题类型（新鲜度、数据量、Schema、字段指标）、开始时间。
3. 进入步骤 2。

**如果用户描述了问题但没有事件 ID：**
阅读 `references/intake-no-incident.md` 了解完整的接诊流程。简要流程：
1. 提出澄清问题：哪张表？哪里不对？什么时候开始的？
2. 搜索表：`search(query="table_name")`
3. 搜索相关告警：在近期时间范围内调用 `get_alerts`
4. 检查表健康状态：`get_table_freshness`、`get_table_size_history`
5. 缩小问题类型范围，进入步骤 2。

### 步骤 1.5：自动调用 TSA（适用时）

当接诊产生了 Monte Carlo **事件 UUID** 时，在继续步骤 2 之前启动排查智能体（TSA）。TSA 运行与 Monte Carlo UI 相同的根因分析；在此处与手动排查并行运行，通常比单独走任一路径效果更好。

**以下情况跳过 TSA：**

1. **无事件 UUID。** `run_troubleshooting_agent` 需要 UUID。无事件接诊路径（`references/intake-no-incident.md`）不会触发 TSA。如果该路径后续识别出匹配的告警，带着告警的事件 UUID 返回步骤 1——步骤 1.5 将正常执行。
2. **窄范围检查。** 用户只需要一个事实，而非调查。例如："`analytics.orders` 现在不更新了吗？"、"X 的行数是多少？"、"给我看 Y 的 Schema"、"这个查询今天运行了吗？"。用相关工具回答问题后停止。TSA 对这些场景过于重量级。
3. **用户明确选择退出。** 用户说"跳过 TSA"、"不要运行 TSA"、"仅手动排查"、"你自己来"等类似表述。遵从选择，直接进入步骤 2，不调用 TSA。

**默认调用方式（异步、并行）：**

```
run_troubleshooting_agent(incident_id="<uuid>", async_mode=True)
```

- 该工具默认**幂等**：如果此事件已有先前成功的 TSA 运行，它会立即返回那些结果。**不要**传入 `force_rerun=True`，除非用户明确要求重新分析（每次新运行都会消耗 Monte Carlo 额度）。
- 如果首次调用时状态为 `success`，说明已有结果——直接将其纳入步骤 7 的综合分析，同时继续步骤 2–6 进行交叉验证。
- 如果状态为 `queued` 或 `running`，立即继续步骤 2。TSA 通常在 4–8 分钟内完成；后续通过 `get_troubleshooting_agent_results` 轮询结果（见步骤 4 和步骤 7）。
- 如果状态为 `failed`，记录错误，仅继续手动排查——不要自动重新运行。

告知用户："我已对此事件启动了排查智能体——通常 4–8 分钟完成。在它运行的同时，我会继续手动排查，这样无论哪条路径先出结果我们都有发现。"

### 步骤 2：映射影响范围

> **TSA 并行运行：** 如果你在步骤 1.5 启动了 TSA，它在此步骤期间在后台运行。不要阻塞等待它。

1. 调用 `get_asset_lineage(mcons=[table_mcon], direction="UPSTREAM")`——什么在给这张表提供数据？
2. 调用 `get_asset_lineage(mcons=[table_mcon], direction="DOWNSTREAM")`——这张表在给什么提供数据？
3. 如果问题涉及特定字段，调用 `get_field_lineage` 追踪哪些上游字段在给受影响的列提供数据。

向用户报告："这张表由 X 个上游源提供数据，并向 Y 个下游消费者提供数据。以下是可能受影响的内容。"

**询问方向：** 在深入排查之前，先问用户想先调查什么。他们可能已有预感（"我觉得是 Airflow 作业的问题"或"看看是不是有人改了 SQL"）。跟随他们的指引——不要盲目运行所有排查路径。如果他们没有偏好，根据问题类型选择最可能的路径继续。

### 步骤 3：按问题类型排查

阅读对应的参考文件并遵循其排查手册：

| 问题类型 | 参考文件 |
|---------|---------|
| 表未按计划更新 | `references/freshness-investigation.md` |
| 行数意外变化 | `references/volume-investigation.md` |
| 列被添加、删除或类型变更 | `references/schema-investigation.md` |
| Airflow/dbt/Databricks 管道失败 | `references/etl-failure-investigation.md` |
| SQL 修改导致数据变化 | `references/query-change-investigation.md` |
| 字段级指标漂移（空值率、均值等） | `references/field-anomaly-investigation.md` |

### 步骤 4：检查上游原因

数据问题通常源于上游。沿血缘链向上追溯：

1. 对步骤 2 中的每个直接上游表：
   - 检查新鲜度：`get_table_freshness`——上游表也不更新了吗？
   - 检查大小：`get_table_size_history`——上游表的数据量有变化吗？
   - 检查 ETL 状态：使用相关 `platform` 调用 `get_etl_issues`
2. 使用 `get_field_lineage` 追踪有问题的数据字段到其源头。
3. 检查哪些上游字段值与异常相关（如果有数据库连接器——见步骤 5）。

**TSA 轮询 #1。** 如果你在步骤 1.5 启动了 TSA 且尚未返回 `success`，在此处调用一次 `get_troubleshooting_agent_results(incident_id=...)`（步骤 1.5 后约 30 秒）。如果状态为 `success`，保留结果到步骤 7。如果仍为 `running`，继续——步骤 7 之前会再次轮询。不要阻塞等待。

### 步骤 5：数据画像（如果有数据库 MCP）

如果用户连接了数据库 MCP 服务器（Snowflake、BigQuery、Redshift、Databricks 等），阅读 `references/data-exploration.md` 了解 SQL 排查模式，包括：
- 事件时间附近的样本行
- 空值率和分布检查
- 与上游表的值关联
- 前后对比

**如果没有数据库 MCP：** 告知用户："我无法直接查询数据仓库——要进行更深入的数据调查，请连接数据库 MCP 服务器。我仍可使用 Monte Carlo 的元数据和可用工具进行分析。"仅使用 MC 工具继续排查。

### 步骤 6：检查代码变更

使用问题开始前后时间范围调用 `get_github_prs`，从账户的 Monte Carlo GitHub 集成中查找近期 PR。寻找修改了 dbt 模型、SQL 文件或影响受影响表的管道配置的 PR。

如果账户没有 GitHub 集成（工具返回空），或用户有他们偏好的本地 GitHub MCP 服务器，改用那个。

同时使用受影响的表 MCON 调用 `get_query_changes` 检测 SQL 文本变更，调用 `get_change_timeline` 获取所有变更（查询修改 + 数据量变化 + ETL 失败）的统一视图。

### 步骤 7：综合分析与呈现

**TSA 轮询 #2。** 如果你在步骤 1.5 启动了 TSA 但尚未获得结果，再调用一次 `get_troubleshooting_agent_results(incident_id=...)`（轮询 #1 后约 60–90 秒）。`success` 或 `failed` 时停止；如果此轮询后仍为 `running`，先呈现手动排查结果，并告知用户 TSA 仍在运行（"TSA 仍在此事件上运行——如果你需要，我可以在它完成后将结果纳入，或者你可以让我稍后再查"）。

阅读 `references/common-root-causes.md` 将发现与已知模式匹配。呈现：

1. **根因**——发生了什么、何时发生，附工具证据
2. **证据链**——哪些工具确认了故事的每一部分
3. **影响**——哪些下游表/消费者受影响（来自步骤 2）
4. **修复建议**——解决问题的具体行动
5. **预防措施**——建议监控以便下次更早发现

**合并 TSA 发现：**

- **TSA 成功且与手动排查一致**——以统一的根因为主；同时引用 TSA 的证据链和交叉验证的手动发现。
- **TSA 成功但与手动排查矛盾**——同时呈现两者。展示 TSA 的结论，展示手动排查的发现，解释分歧（例如"TSA 认为是上游 Airflow 作业的问题，但该表的 `get_table_freshness` 显示健康"）。询问用户想追踪哪条线索。
- **TSA 成功但输出信号弱**（例如"无明确根因"）——以手动排查发现为主；将 TSA 作为佐证的空结果引用。
- **TSA 失败或超时**——仅呈现手动排查发现；简要提及 TSA 失败，让用户知道已经尝试过。

---

## 重要规则

- **绝不编造数据。** 只引用工具返回的数字和事实。如果工具返回了空数据，如实说明。
- **跟随证据。** 如果上游血缘未显示问题，问题可能在表自身的 ETL。不要追逐虚幻的上游原因。
- **检查时间线。** 最常见的模式是："X 在时间 T 发生了变更，异常在时间 T+1 开始。"使用 `get_change_timeline` 进行此检查。
- **明确说明无法检查的内容。** 如果没有数据库连接器，解释有了它可以做哪些额外排查。
- **不要向用户暴露 MCON、UUID 或内部标识符。** 使用人类可读的表名。
- **跨平台意识。** ETL 问题可能来自 Airflow、dbt 或 Databricks。检查所有相关平台。
- **没有事件 UUID 时不要调用 TSA。** `run_troubleshooting_agent` 需要 UUID。如果接诊走的是无事件路径，完全跳过 TSA，直到/除非识别出告警。
- **遵从用户的明确选择退出。** 如果用户说"跳过 TSA"、"仅手动排查"或类似表述，不要调用 `run_troubleshooting_agent` 或 `alert_assessment`——仅进行手动排查。

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性或高成本操作的审批。
