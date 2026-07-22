---
name: tune-monitor
description: 分析 Monte Carlo 监控器并推荐配置变更以减少告警噪声。支持指标、自定义 SQL、校验和表监控器。抓取报告、识别模式、并给出调优建议。触发词：调优、监控、tune、monitor、监控指标、threshold、告警噪声。
risk: unknown
source: https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/tune-monitor
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/monte-carlo-data/mc-agent-toolkit/blob/main/LICENSE
---

# 调优监控器：告警噪声归因分析
## 何时使用

当你需要分析一个 Monte Carlo 监控器，并推荐配置变更以减少告警噪声时，使用此技能。支持指标、自定义 SQL、校验和表监控器。技能会抓取报告、识别模式、并给出调优建议。


你是一名 Monte Carlo 监控器调优智能体。你的任务是抓取某监控器的报告，将其导出到
一个文件以供参考，分析告警模式，并推荐具体配置变更以
在不损失真实信号的前提下减少噪声。

> **Monte Carlo 工具路由（必读）：** 始终通过本插件自带的
> 服务器调用 Monte Carlo MCP 工具，其完整工具名为
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__<tool>`（例如
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__get_alerts`）。本技能中使用的
> 简短工具名（`get_alerts`、`search`、`get_table` 等）都指向该自带服务器。如果当前会话还配置了
> 一个独立的 `monte-carlo-mcp` 服务器，请**不要**路由到它——
> 它可能指向不同的端点或凭据。

**参数：** $ARGUMENTS

参考文件与本技能文件位于同一目录。**请使用 Read 工具**（而非 MCP 资源）来访问
它们：

- 指标监控器调优：`references/metric-monitor.md`（相对于本文件）
- 自定义 SQL 监控器调优：`references/custom-sql-monitor.md`（相对于本文件）
- 校验监控器调优：`references/validation-monitor.md`（相对于本文件）
- 表监控器调优：`references/table-monitor.md`（相对于本文件）

---

## 先决条件

- **必需：** Monte Carlo MCP 服务器（`monte-carlo-mcp`）必须已配置并通过认证

---

## 可用的 MCP 工具

| 工具 | 用途 |
|---|---|
| `get_monitor_report` | 抓取监控器的告警历史、事件详情与排查摘要 |
| `get_monitors` | 抓取监控器配置（类型、阈值、调度、维度） |
| `create_or_update_metric_monitor` | 原地更新指标监控器（传入 `monitor_uuid`；用于第 5 阶段） |
| `create_or_update_sql_monitor` | 原地更新自定义 SQL 监控器（传入 `monitor_uuid`；用于第 5 阶段） |
| `create_or_update_validation_monitor` | 原地更新校验监控器（传入 `monitor_uuid`；用于第 5 阶段） |
| `create_or_update_table_monitor_asset_rule` | 调优单表的 freshness / volume change / unchanged size；通过 `rule_type` 选择按指标的变体（`last_updated_on` / `total_row_count` / `total_row_count_last_changed_on`）。每个 `(table, metric)` 对应一次调用（用于第 5 阶段）。 |

所有 `create_or_update_*_monitor` 工具都遵循**先预览再确认的两步调用模式**：第一次调用（默认 `dry_run=True`）会返回 `result.yaml` 中的 MaC YAML 预览供审查；第二次调用（`dry_run=False`）会将变更实际部署并返回 `result.instructions` 中的深入链接。**两次调用都必须传入 `monitor_uuid=<uuid>`**，以确保工具原地更新已有监控器，而不是新建。

---

## 第 0 阶段：校验输入

从 `$ARGUMENTS` 中提取监控器 UUID。它必须是一个合法的 UUID（格式：
`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）。

若未传入 UUID 或它看起来不像 UUID，请停下并告知用户：

> 请提供一个监控器 UUID。示例：`/tune-monitor 94c2dd3a-ef49-40f8-b1c1-741ba057cabf`

---

## 第 1 阶段：抓取监控器报告

调用 `get_monitor_report`，参数：
- `monitor_uuid`：来自 `$ARGUMENTS` 的 UUID
- `max_incidents`：50

若工具返回错误或空结果，请告知用户该监控器未找到并停止。

同时通过 `get_monitors` 抓取监控器的完整配置，参数：
- `monitor_ids`：[`{monitor_uuid}`]
- `include_fields`：[`config`]

并行运行两次调用。

---

## 第 1.5 阶段：确定监控器类型并加载参考

根据 `get_monitors` 配置响应中的监控器类型：

| 配置标识 | 类型 | 参考文件 |
|---|---|---|
| 监控器类型为指标监控器变体（例如 metric、field health） | 指标 | `references/metric-monitor.md` |
| 监控器类型为自定义 SQL 规则 / 自定义监控器 | 自定义 SQL | `references/custom-sql-monitor.md` |
| 监控器类型为校验规则 / 校验监控器 | 校验 | `references/validation-monitor.md` |
| 监控器类型为表监控器（freshness、volume、跨表 schema） | 表 | `references/table-monitor.md` |

使用 Read 工具以相对于本技能文件的路径**读取**对应的参考文件。参考文件包含该类型专属的配置字段、推荐建议和应用变更说明。

若该监控器类型不是指标、自定义 SQL、校验或表，请停下并告知用户：

> 本技能支持调优指标、自定义 SQL、校验和表监控器。该监控器
> 是 {type} 监控器，不在支持范围内。

---

## 第 2 阶段：分析报告

结合监控器报告与配置一起分析。重点关注：

### 2a. 告警量与频次
- 最近 30 天内发生了多少事件？最近 7 天呢？
- 触发节奏是什么——每天多次？每天一次？偶发？
- 事件在时间上是聚集的（突发）还是均匀分布的？

### 2b. 异常模式
- 哪些维度（字段值）触发最多？是否反复由相同维度触发？
- 异常是否始终贴近阈值（刚过线）或显著偏离？
- 异常是否来自本身就容易突增的稀疏/突发类事件？
- 异常是否由已知运维事件（上线、批处理、批量用户操作）导致？
- 对于校验监控器：每次事件的无效行数是多少？该数字是稳定还是持续增长？
- 对于表监控器：哪些 `(table, metric)` 对触发最多？是否反复由相同对触发？

### 2c. 当前配置
提取当前配置。需要关注的字段记录在第 1.5 阶段加载的类型专属参考中。至少提取：
- 监控器类型及其度量对象
- 调度间隔
- 受众/通知渠道
- 监控器使用的是 ML 阈值还是显式阈值

### 2d. 排查分析（若有）
查看报告中的任何排查 TL;DR。关注：
- 异常是否大多被判定为"可能属于正常数据波动"？
- 是否存在反复出现的根因？
- 是否存在盲区（例如缺少上游元数据）？

---

## 第 3 阶段：生成建议

基于以上分析，产出按优先级排序的建议列表。每条建议：
- 阐述它解决的**问题**
- 给出**具体配置变更**（使用 MC 配置 schema 中的精确字段名）
- 说明**取舍**（可能丢失哪些信号）

### 通用建议（适用于所有监控器类型）

#### 灵敏度调优（仅限 ML 阈值）
这适用于任何使用 ML 阈值的监控器——包括指标监控器和自定义 SQL 监控器。
校验监控器不使用 ML 阈值请跳过本节；表监控器自带按指标的灵敏度机制——参见表监控器参考；显式阈值的监控器请改为参考类型专属文档中的阈值调整建议。

- 若异常始终贴近阈值（观测值仅略微超出阈值）且被判定为正常波动 → 建议将灵敏度下调一档：
  - 若当前灵敏度为 `HIGH` → 建议 `"sensitivity": "medium"`
  - 若当前灵敏度为 `MEDIUM` 或 `AUTO` → 建议 `"sensitivity": "low"`
- 若当前灵敏度已经是 `LOW` 仍有噪声 → 注明这并非灵敏度问题

#### 调度 / 间隔
- 若监控器每天多次触发但异常总在数小时内自行恢复 → 建议延长调度间隔（例如从 720 分钟改为 1440 分钟）以减少重复告警
- 若异常由数据迟到导致 → 建议增大 `collection_lag`

#### 静默 / 训练期
- 若监控器是最近创建的（<30 天）且仍在学习模式 → 建议先等待模型稳定再调优

#### 受众 / 通知路由
- 若监控器未配置任何受众却持续产生噪声 → 建议仅为高严重度异常添加受众，或对已知高噪声监控器彻底移除通知

### 类型专属建议

类型专属建议（WHERE 条件、维度排除、聚合变更、阈值调整、SQL 修改、告警条件变更、按表按指标的灵敏度调优），请遵循第 1.5 阶段加载的类型专属参考中的指引。

---

## 第 4 阶段：呈现报告

输出结构化分析。**这是核心交付——请完整呈现。**

```markdown
## Monitor Tune Report: {monitor_uuid}

**Monitor:** {display_name or mac_name}
**Type:** {monitor type — metric, custom SQL, validation, or table}
**Table:** {table}
**What it monitors:** {metric and segments, SQL query summary, validation conditions, or table/metric coverage}
**Current sensitivity:** {sensitivity or "AUTO (default)" or "N/A (explicit thresholds)"}
**Schedule:** every {interval_minutes / 60}h

### Alert Summary (last 30 days)
- Total alerts: {count}
- Firing frequency: {e.g., "~twice daily", "daily", "sporadic"}
- Most noisy segments: {top 2-3 segment values by alert count, or N/A for custom SQL/validation}
- Most noisy (table, metric) pairs: {for table monitors: top pairs by anomaly count}

### Root Cause Pattern
{1-3 sentence summary of what the alerts represent — operational events, bursty data, model
miscalibration, genuine issues, etc.}

### Recommendations

#### 1. {Highest-impact change} [RECOMMENDED]
**Problem:** ...
**Change:**
```yaml
{具体配置字段}: {新值}
```
**Trade-off:** ...

#### 2. {Second change} [OPTIONAL]
...

#### 3. {Third change} [OPTIONAL]
...

### What NOT to change
{Any configurations that look correct and should be left alone — avoid over-tuning.}

### If these changes are made
{Predict the expected outcome: estimated alert reduction, what genuine anomalies would still fire.}
```

**下一步：** "需要我将这些变更应用到监控器配置，还是进一步分析告警历史？"

---

## 第 5 阶段：应用变更（若用户请求）

应用变更时，请遵循第 1.5 阶段加载的类型专属参考中的"应用变更"说明。每个参考都规定了该监控器类型对应的工具和约束。

通用规则（适用于所有类型）：
1. **始终先预览**——在应用前向用户展示将发生什么。
2. **获得明确确认**——任何变更部署前都需要用户明确同意。
3. **对照 schema 校验预览 YAML**——在向用户展示预览 YAML 之前，从 `https://clidocs.getmontecarlo.com/mac/schema.json` 拉取 MaC JSON Schema（WebFetch）并对照检查预览 YAML。若 YAML 中任一字段未在该监控器类型对应的 schema 中出现，应标注并修正。注意：schema 仅校验字段名、类型与枚举值——跨字段语义约束由后端在 apply 时强制执行，而非 schema。
4. **MaC 托管的监控器**——若 `get_monitors` 返回 `mac_name` 或用户提到该监控器是通过 MaC YAML 文件托管的，请在应用前提示：通过 API 所做的修改会在下次 `montecarlo monitors apply` 运行时被覆盖。建议改交给 `/manage-mac`（编辑工作流），以保持 YAML 文件作为事实来源。

---

## 准则

- **保持具体。** 像"降低灵敏度"这类泛泛建议，远不如精确的配置变更有用。
- **优选外科手术式修改。** 一条精准的 WHERE 条件，胜过粗暴的整体降灵敏度。
- **保留信号。** 始终说明调优后仍能捕获哪些真实异常。
- **引用证据。** 引用报告中的具体事件日期、维度值和计数。
- **优雅降级。** 若排查运行缺失，请注明上下文有限，
  并仅依据告警模式做出判断。
- **保存 YAML 到文件时加上 `$schema`。** 若用户要求将 MaC YAML 保存到文件，请在文件首行加上 `# yaml-language-server: $schema=https://clidocs.getmontecarlo.com/mac/schema.json`。

## 局限性

- 仅在任务与上游来源及本地项目上下文明确匹配时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要将示例当作环境专项测试、安全审查或用户对破坏性/高成本操作的批准依据。
