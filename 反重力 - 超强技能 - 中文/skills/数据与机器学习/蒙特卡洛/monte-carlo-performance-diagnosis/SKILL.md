---
name: monte-carlo-performance-diagnosis
description: "使用 Monte Carlo 跨平台可观测性诊断数据管道性能问题——慢作业、昂贵查询、延迟趋势。采用分层调查方法：发现问题、桥接到受影响表、然后深入根因。当用户提到慢管道、性能回归、延迟上升、昂贵查询、管道变慢、计算消耗大时激活"
risk: unknown
source: https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/performance-diagnosis
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/monte-carlo-data/mc-agent-toolkit/blob/main/LICENSE
---

# Monte Carlo 性能诊断技能

本技能帮助使用 Monte Carlo 的跨平台可观测性数据诊断数据管道性能问题。它支持 Airflow、dbt、Databricks 和仓库查询引擎，用于发现瓶颈、检测回归和定位根因。

> **Monte Carlo 工具路由（必需）：** 始终通过本插件捆绑的服务器调用 Monte Carlo MCP 工具，其全限定工具名为
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__<tool>`（例如
> `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__get_alerts`）。本技能中使用的裸工具名
>（`get_alerts`、`search`、`get_table`、…）均指向该捆绑服务器。如果会话中还配置了单独的
> `monte-carlo-mcp` 服务器，**不要**路由到它——它可能指向不同的端点或凭证。

参考文件位于本技能文件旁边。**使用 Read 工具**（而非 MCP 资源）访问它们：

- 分层调查方法：`references/investigation-tiers.md`（相对于本文件）
- 查询分析模式：`references/query-analysis.md`（相对于本文件）

## 何时激活本技能

当用户出现以下情况时激活：

- 询问慢管道、慢作业或慢查询
- 想要查找昂贵或高成本的查询
- 提及性能回归或性能下降
- 询问"为什么这个管道慢？"或"什么在消耗最多计算资源？"
- 想要对比不同时间段的性能或发现瓶颈任务
- 询问失败或无效的查询模式

## 何时不激活本技能

当用户出现以下情况时不激活：

- 调查数据质量问题（使用 prevent 技能）
- 查看存储成本（使用 storage-cost-analysis 技能）
- 创建监控（使用 monitoring-advisor 技能）
- 仅仅是查询数据或浏览表内容

## 前置条件

以下 MCP 工具必须可用（连接到 Monte Carlo 的 MCP 服务器）：

**发现工具（第1层）：**
- `get_jobs_performance` -- 跨 Airflow、dbt、Databricks 查找慢作业/失败作业
- `get_top_slow_queries` -- 按总运行时间查找最慢的查询组

**桥接工具：**
- `get_tables_for_job` -- 将作业 MCON 转换为表 MCON

**诊断工具（第2层）：**
- `get_tasks_performance` -- 深入查看作业中的各个任务
- `get_change_timeline` -- 统一展示查询变更、数据量变化、Airflow/dbt 失败的时间线
- `get_query_rca` -- 对失败/无效查询进行根因分析
- `get_query_latency_distribution` -- 延迟随时间的变化趋势
- `get_asset_lineage` -- 追踪上游/下游影响

**辅助工具：**
- `get_warehouses` -- 列出可用的仓库

## 工作流程

### 步骤1：确定调查范围

确定用户想要调查的内容：
- **特定作业/管道**：用户提到了作业名或管道名
- **特定表**：用户提到某张表更新很慢
- **通用发现**：用户想要找出哪里慢

调用 `get_warehouses` 列出可用仓库。将用户的上下文匹配到对应仓库。

### 步骤2：第1层——发现

如果没有具体的 MCON 需要调查，从发现阶段开始：

1. **查找慢作业**：调用 `get_jobs_performance`，如果用户指定了平台，可选传入 `integration_type` 过滤器（AIRFLOW、DATABRICKS、DBT）。
   - 结果包含：作业名、平均耗时、趋势（7天）、运行次数、失败率
   - 关注：高 `avgDuration`、负 `runDurationTrend7d`、高失败率

2. **查找昂贵查询**：调用 `get_top_slow_queries`，可选传入 `warehouse_id` 和 `query_type`（"read" 对应 SELECT，"write" 对应 INSERT/CREATE/MERGE）。
   - 结果包含：查询哈希、总运行时间、平均运行时间、运行次数
   - 关注：总运行时间高或单次执行时间高的查询

在深入调查前，先将主要发现呈现给用户。一次典型调查只需要 3-7 次工具调用。

**如果两个发现工具都没有返回结果：** 告诉用户在当前时间窗口内未发现性能问题。建议扩大范围（换一个仓库、更长的时间范围、或不同的平台过滤器）。

### 步骤3：桥接——从作业到表

第1层识别出问题作业后，将其转换为表 MCON：

使用作业性能结果中的 `integration_type`，调用 `get_tables_for_job(job_mcon=..., integration_type=...)`。

这样你就获得了第2层调查所需的表 MCON。

### 步骤4：第2层——诊断

现在使用发现阶段或桥接阶段获得的 MCON 深入分析根因：

1. **任务瓶颈**：调用 `get_tasks_performance` 找出作业中哪个具体任务是瓶颈。

2. **什么变了？** 调用 `get_change_timeline`——这是你最强的工具。它返回统一的时间线：
   - 查询文本变更（模式修改、新增 JOIN、过滤条件变更）
   - 数据量变化（行数激增/骤降）
   - Airflow 任务失败
   - dbt 模型失败
   全部在一次调用中获取。寻找关联性："查询在第 X 天变更，运行时间在第 X+1 天翻倍。"

3. **查询为什么失败？** 调用 `get_query_rca` 获取根因分析：
   - **失败（Failed）**查询：错误、超时、权限问题
   - **无效（Futile）**查询：运行了但没有产生有用输出的查询
   - 模式是预计算的——工具按原因分组失败

4. **延迟在恶化吗？** 调用 `get_query_latency_distribution` 查看趋势：
   - 对比 p50 与 p95——如果 p95 远大于 p50（>5倍），问题在于离群查询
   - 寻找延迟的阶跃变化（突然增长 = 回归）
   - 对于阶跃变化/回归时间定位场景，传入 `bucket="1h"`。默认在窗口 ≥ 3 天时降采样到天级别，这会隐藏小时级别的阶跃。

5. **追踪影响**：调用 `get_asset_lineage`，传 `direction="DOWNSTREAM"` 查看慢表影响了什么，或传 `direction="UPSTREAM"` 查看是什么在供给它。

### 步骤5：呈现结果

按以下结构组织回复：

1. **问题摘要**：什么慢、慢多少（附带工具返回的精确数据）
2. **根因**：发生了什么变更或什么导致了问题
3. **影响**：哪些下游系统受到影响
4. **建议**：解决问题的具体措施

### 重要规则

- **精确引用工具返回的数字。** 如果工具返回"1282 runs, avg 22.5s"，就原样说。绝不四舍五入、估算或编造数字。
- **始终与基线对比。** 使用 7 天趋势数据（`runDurationTrend7d`）区分回归和正常波动。如果趋势数据的置信度低于 0.1 则标记说明。
- **找到根因就停下。** 3-7 次工具调用是典型情况。超过 10 次说明你在过度调查。
- **读查询与写查询**：当用户问"读"或"读查询"时，用 `query_type="read"` 过滤。问"写"时用 `query_type="write"`。不要混用。
- **不要向用户暴露 MCON、UUID 或内部标识符。** 使用人类可读的名称。
- **跨平台**：本技能支持 Airflow、dbt 和 Databricks。标注每个发现来自哪个平台。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定测试、安全审查或用户对破坏性/高成本操作的审批。
