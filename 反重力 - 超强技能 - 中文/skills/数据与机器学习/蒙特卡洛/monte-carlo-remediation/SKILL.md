---
name: monte-carlo-remediation
description: 使用 Monte Carlo MCP 工具调查和修复数据质量告警。运行根因分析、评估影响范围、发现可用工具（MCP/CLI/API），提出并执行修复方案，或在不确定时携带完整上下文升级。触发词：数据质量修复、告警修复、数据质量告警、Monte Carlo 修复、remediation、根因修复
risk: unknown
source: https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/remediation
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/monte-carlo-data/mc-agent-toolkit/blob/main/LICENSE
---

# Monte Carlo 修复技能

本技能教你调查和修复 Monte Carlo 检测到的数据质量问题。你将使用 MC MCP 工具了解告警上下文、运行根因分析、评估影响范围，然后利用用户已连接的外部工具执行合适的修复操作。

> **Monte Carlo 工具路由（必读）：** 始终通过本插件捆绑的服务器调用 Monte Carlo MCP 工具，
> 其全限定工具名为 `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__<tool>`（例如
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__get_alerts`）。本技能中使用的裸工具名
>（`get_alerts`、`search`、`get_table`、……）均指该捆绑服务器。如果会话中还有
> 单独配置的 `monte-carlo-mcp` 服务器，**不要**路由到它——它可能指向不同的端点或凭证。

参考文件位于本技能文件旁边。**使用 Read 工具**（而非 MCP 资源）访问它们：

- 常见修复模式和示例：`references/patterns.md`（相对于本文件）
- 如何在运行时发现可用工具：`references/tool-discovery.md`（相对于本文件）
- 安全护栏和升级标准：`references/safety.md`（相对于本文件）

## 何时激活本技能

当用户执行以下操作时激活：

- 要求修复、处理或响应数据质量告警或事件
- 提到特定的告警 ID、事件或希望解决的数据质量问题
- 说类似"修复 X 的新鲜度问题"、"处理这个告警"、"应对这个事件"
- 要求同时分诊和修复告警（仅分诊无修复意图→改用 prevent 技能的工作流 3）
- 希望自动化响应反复出现的数据质量问题
- 问"这个告警我该怎么办？"或"怎么修复这个？"

## 何时不激活本技能

当用户只是以下情况时不激活：

- 仅分诊或调查告警，无修复意图（使用 prevent 技能的工作流 3）
- 创建或配置监控器（使用 monitoring-advisor 技能）
- 在代码变更前运行变更影响评估（使用 prevent 技能的工作流 4）
- 询问一般性数据质量最佳实践，无具体事件
- 探索表健康度或血缘关系，无待修复的活跃问题

---

## 可用工具

### Monte Carlo MCP 服务器（调查 + 修复后）

Monte Carlo MCP 服务器（`monte-carlo-mcp`）提供以下工作流中使用的调查工具。工作流按名称引用关键工具（如 `get_alerts`、`run_troubleshooting_agent`、`get_asset_lineage`），但**使用任何有帮助的 Monte Carlo 工具**——该服务器还有工作流未明确列出的额外工具。探索可用的工具。

> **工具调用示例说明：** 下面的代码块展示了关键参数作为指引。请始终查看工具自身的描述以获取完整参数列表和精确参数名——它们是权威来源。

### 外部工具（修复执行）

修复操作通过所有可用工具执行——MCP 服务器、CLI 工具或 API。参见工作流 2（能力发现）和 `references/tool-discovery.md` 了解如何检测和使用它们。用什么管用就用什么，不要局限于预设列表。

---

## 核心工作流

按顺序执行以下工作流。每个工作流建立在前一个工作流收集的上下文之上。

### 工作流 1：调查

**目标：** 了解发生了什么、为什么发生、影响了什么。

在提出任何修复操作之前，你必须完成此调查。不要跳过步骤——不完整的上下文会导致错误的修复。

#### 步骤 1：获取告警上下文

```
get_alerts(
  alert_ids=["<alert_id>"],
)
```

如果用户提供的是表名而非告警 ID：
```
search(query="<table_name>")
→ extract MCON
get_alerts(
  table_mcons=["<mcon>"],
  created_after="<7 days ago>",
  created_before="<now>",
  order_by="-createdTime",
  statuses=["NOT_ACKNOWLEDGED", "WORK_IN_PROGRESS"]
)
```

从告警中提取：`alert_type`（Freshness、Volume、Schema Changes 等）、`severity`、受影响的表 MCON、`created_time`。

#### 步骤 2：评估分诊优先级

```
alert_assessment(
  incident_id="<alert_uuid>"
)
```

返回 `incident_likelihood`（HIGH/MEDIUM/LOW）、`alert_impact`（HIGH/MEDIUM/LOW）和摘要。用于判断紧急程度：

- **HIGH 影响 + HIGH 事件可能性** → 立即进入 TSA 分析
- **LOW 影响或 LOW 事件可能性** → 仍需运行 TSA，但告知用户这可能不需要立即修复

#### 步骤 3：根因分析（TSA）

**始终使用异步模式。** TSA 分析需要 4-8 分钟——同步模式会超时。

```
run_troubleshooting_agent(
  incident_id="<alert_uuid>",
  async_mode=true
)
```

**TSA 运行期间，并行执行步骤 4-6**——在等待时收集血缘、表上下文和查询数据。然后轮询 TSA 结果：

```
get_troubleshooting_agent_results(
  incident_id="<alert_uuid>"
)
```

状态值：
- `not_found` → TSA 尚未触发
- `running` → 仍在分析（先等 30 秒，然后每 60 秒轮询一次）
- `success` → 结果可用
- `failed` → 查看 `full_response` 中的错误；转为手动调查

**TSA 成功后，同时阅读 `tldr` 和验证部分。** `tldr` 总结了根因——这是你选择修复操作的主要依据。`full_response` 包含"确认根因的验证"部分，其中有具体检查（要运行的查询、要比较的内容、要检查的上游系统）。这些验证本身往往是可执行的修复步骤——用它们指导下一步操作，或作为具体后续步骤呈现给用户。

#### 步骤 4：评估影响范围

```
get_asset_lineage(
  mcons=["<affected_table_mcon>"],
  direction="DOWNSTREAM"
)
```

获取 BI 报表覆盖：
```
get_downstream_bi_reports(
  mcon="<affected_table_mcon>"
)
```

然后进行上游调查：
```
get_asset_lineage(
  mcons=["<affected_table_mcon>"],
  direction="UPSTREAM"
)
```

注意：`has_relationships=false` 表示未跟踪依赖关系——不要假设缺失的关系。

#### 步骤 5：收集表上下文

```
get_table(
  mcon="<affected_table_mcon>",
  include_fields=true,
  include_table_capabilities=true
)
```

提取：最近活动时间戳、行数、schema、监控状态、重要性评分。

对于步骤 4 中识别的关键下游表，也获取其详情：
```
get_table(mcon="<downstream_mcon>")
```

#### 步骤 6：检查告警上下文、监控和近期查询

```
get_monitors(mcons=["<affected_table_mcon>"])
```

对于 **Custom SQL** 或 **Validation** 告警，还需获取监控器配置以了解违反的具体规则：
```
get_monitors(
  monitor_ids=["<monitor_id_from_alert>"],
  include_fields=["config"]
)
```
配置包含 SQL 查询或验证条件——告诉你监控器检查的确切内容，这对理解出了什么问题以及如何修复至关重要。

```
get_queries_for_table(
  mcon="<affected_table_mcon>",
  query_type="destination",
  limit=10
)
```

使用 `query_type="destination"` 查找写入此表的查询（管道查询）。这有助于识别哪个管道或作业负责该数据。

#### 调查摘要

**等待 TSA 完成后再呈现发现。** 不要呈现部分结果——TSA 根因分析及其验证部分对选择正确修复操作至关重要。如果 TSA 仍在运行，继续轮询；同时收集步骤 4-6 的信息。

所有步骤完成后，将发现综合为清晰的摘要：

1. **发生了什么：** 告警类型、触发时间、严重程度
2. **根因：** TSA 发现（或 TSA 失败时的最佳判断）
3. **TSA 验证：** TSA `full_response` 中可确认根因或作为修复步骤的具体检查
4. **影响范围：** N 个下游消费者、受影响的关键资产
5. **管道上下文：** 哪些查询/作业写入此表、上次运行时间
6. **监控：** 存在哪些监控器、有何缺口。注意反复出现的模式（例如"30 天内 16 次事件"表明是长期问题，而非偶发）

在进入修复阶段之前，将此摘要呈现给用户。

---

### 工作流 2：能力发现

**目标：** 根据可用工具确定哪些修复操作是可行的。

在尝试任何修复操作之前，你必须了解可以使用哪些工具。需要检查三个类别：

1. **MCP 服务器** — 扫描工具列表中的 `mcp__*__*` 模式（如 `mcp__airflow__trigger_dag_run`）
2. **CLI 工具** — 你有 shell 访问权限；通过 `which <tool>` 检查 `gh`、`dbt`、`airflow`、`curl` 等工具
3. **API** — 任何有 REST API 的服务都可以通过 `curl` 访问（前提是有正确的凭证）

不要假设任何特定工具可用。但也不要假设 MCP 是唯一选项——通过 CLI 执行 `gh pr create` 和使用 GitHub MCP 工具同样有效。

关于所有三个类别的发现详细指引，请阅读 `references/tool-discovery.md`。

#### 能力评估

检查后，总结可用内容：

**示例：**
> "对于本次修复，我可以：
> - ✅ 通过 Monte Carlo 调查（MCP 已连接）
> - ✅ 重启 Airflow DAG（Airflow MCP 已连接）
> - ✅ 创建代码修复（`gh` CLI 可用）
> - ❌ 重新运行 dbt 作业（未找到 dbt Cloud MCP 或 `dbt` CLI）"

#### 优雅降级

当需要的操作没有可用工具（MCP、CLI 或 API）时：

1. **始终产出修复计划** — 逐步描述需要做什么
2. **提供可执行的命令** — 给用户可以手动运行的确切命令（如 `airflow dags trigger <dag_id>`、`dbt run --select <model>`）
3. **呈现发现并询问后续步骤** — 告诉用户你发现了什么、你的建议，询问他们希望如何继续
4. **记录到告警** — 使用 `create_or_update_alert_comment` 记录诊断和推荐修复

---

### 工作流 3：修复执行

**目标：** 在安全护栏下，采取合适操作修复根因。

阅读 `references/patterns.md` 获取常见修复模式的详细示例。

#### 步骤 1：选择修复操作

根据 TSA 根因和可用工具，确定操作：

| 根因信号（来自 TSA） | 典型修复方式 | 所需能力 |
| ---------------------------- | ------------------- | ------------------- |
| 管道/DAG 失败或延迟 | 重启失败的管道或任务 | 管道编排 |
| dbt 模型失败 | 重新运行失败的 dbt 作业 | dbt 操作 |
| Schema 变更（上游） | 评估影响，更新下游模型或回滚 | 代码变更 |
| 数据量异常（数据缺失） | 检查上游管道，触发回填 | 管道编排 + 数据仓库 |
| 数据量异常（数据重复） | 识别并移除重复数据，修复管道 | 数据仓库 + 代码变更 |
| 权限/访问错误 | 呈现发现，建议用户升级至数据平台团队 | 无（用户决定） |
| 基础设施问题 | 呈现发现，建议用户升级至平台/运维团队 | 无（用户决定） |
| 未知或复杂根因 | 呈现完整上下文，询问用户后续步骤 | 无（用户决定） |

**如果根因映射到多个可能操作**，向用户展示各选项及权衡，让他们选择。

**如果根因未清晰映射到任何模式**，阅读 `references/patterns.md` 中的"未知/复杂"模式，该模式侧重于向用户呈现完整上下文并征求指示。

#### 步骤 2：呈现修复计划

**在执行任何操作之前**，向用户呈现计划：

> "基于调查结果：
>
> **根因：** [TSA 摘要]
> **提议操作：** [你要做什么]
> **理由：** [为什么此操作能解决根因]
> **风险：** [可能出什么问题、影响范围]
> **回滚方案：** [如果修复导致新问题，如何撤销]"

#### 步骤 3：执行（带安全护栏）

执行前，阅读 `references/safety.md` 获取完整安全协议。要点：

- **先解释再执行** — 绝不在未告知用户做什么和为什么的情况下采取行动
- **确认破坏性操作** — 等待用户明确批准
- **不确定时询问用户** — 不要猜测修复方案
- **一次一个操作** — 执行一个操作，然后决定下一步
- **记录一切** — 通过 `create_or_update_alert_comment` 在告警上记录每个操作

---

### 工作流 4：修复后

**目标：** 正确关闭事件——更新状态、记录文档、防止复发。

#### 步骤 1：更新告警

询问用户要设置什么状态：

- `FIXED` — 根因已识别并修复
- `EXPECTED` — 告警基于预期行为触发（如计划维护）
- `NO_ACTION_NEEDED` — 问题自行解决或无需操作

然后调用 `update_alert(alert_id="<alert_uuid>", status="<chosen_status>")`。

#### 步骤 2：记录修复

```
create_or_update_alert_comment(
  alert_id="<alert_uuid>",
  comment="## Remediation Summary\n\n**Root cause:** [TSA findings]\n**Action taken:** [what was done]\n**Result:** [outcome]\n**Remediated by:** AI agent via remediation skill\n**Timestamp:** [ISO timestamp]"
)
```

#### 步骤 3：考虑预防

修复后，简要评估此问题是否可能复发：

- **如果根因是系统性的**（如不稳定的管道、缺失的监控器）：建议添加监控器或创建工单以解决根本问题
- **如果是偶发的**（如基础设施抖动、手动操作失误）：记录后继续

不要自动创建监控器或工单——提出建议，让用户决定。

---

## 常见错误

- **绝不在未先呈现计划的情况下执行修复操作。** 用户必须了解你即将做什么。
- **绝不跳过调查阶段。** 错误的诊断导致错误的修复——更糟的是，修复本身可能引发新问题。
- **绝不假设外部 MCP 工具可用。** 始终先检查。缺少工具不是错误——向用户呈现发现并询问后续步骤。
- **绝不在未验证每个操作的情况下链式执行多个修复操作。** 一次一个操作。
- **绝不在无用户明确确认且无明确回滚方案的情况下直接修改数据**（DELETE、UPDATE、DROP）。
- **绝不在未验证修复效果的情况下将告警标记为 FIXED。** 检查底层状况是否确实改善。
- **绝不静默修复。** 始终通过 `create_or_update_alert_comment` 记录所做操作。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代针对特定环境的测试、安全审查，或用户对破坏性或高成本操作的批准。
