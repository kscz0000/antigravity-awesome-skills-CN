---
name: monte-carlo-storage-cost-analysis
description: 通过 analyze_storage_costs MCP 工具分析数据仓库中的过期、未使用或冗余表。分类浪费模式和表类别，计算安全层级，并处理类别下钻和血缘追踪。触发词：存储成本分析、仓库清理、僵尸表、过期表、存储优化、成本缩减
risk: unknown
source: https://github.com/monte-carlo-data/mc-agent-toolkit/tree/main/skills/storage-cost-analysis
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/monte-carlo-data/mc-agent-toolkit/blob/main/LICENSE
---

# Monte Carlo 存储成本分析技能

本技能分析数据仓库中可移除以降低存储成本的过期表。它将分类、安全评分和格式化工作委托给 `analyze_storage_costs` MCP 工具，然后原样呈现预格式化结果，并处理后续问题（类别下钻、血缘检查）。

> **Monte Carlo 工具路由（必读）：** 始终通过本插件绑定的 MCP 服务器调用 Monte Carlo 工具，
> 其完整工具名为 `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__<tool>`
> （例如 `mcp__plugin_mc-agent-toolkit_monte-carlo-mcp__get_alerts`）。本技能中使用的裸工具名
> （`get_alerts`、`search`、`get_table` 等）均指向该绑定服务器。如果当前会话还配置了
> 独立的 `monte-carlo-mcp` 服务器，**不要**路由到该服务器——它可能指向不同的端点或凭据。

参考文件（使用 Read 工具访问）：

- 输出契约和类别关键词：`references/output-structure.md`

## 何时激活此技能

当用户出现以下情况时激活：

- 询问存储成本、浪费或清理机会
- 想要查找未使用、未读取或过期的表
- 询问"哪些表可以删除？"或"什么在花钱？"
- 提及存储优化、成本缩减或仓库清理
- 想要识别僵尸表、死端管道或临时/归档表

## 何时不激活此技能

当用户出现以下情况时不激活：

- 仅查询数据或探索表内容
- 创建或修改监控器（使用 monitoring-advisor 技能）
- 调查数据质量事件（使用 prevent 技能）
- 查看管道性能或查询成本（使用 performance-diagnosis 技能）

## 前置条件

以下 MCP 工具必须可用（连接到 Monte Carlo 的 MCP 服务器）：

- `analyze_storage_costs` -- 运行完整分析管道并返回预格式化输出
- `get_asset_lineage` -- 仅用于后续血缘检查

`analyze_storage_costs` 工具仅支持 **Snowflake、BigQuery、Redshift 和 Databricks** 数据仓库。其他仓库类型不在范围内。

## 工作流程

**重要：** 以下步骤是给你的内部指令。不要向用户暴露步骤编号、步骤名称或流程结构。自然执行即可。

### 步骤 1：确定数据仓库

需要指定数据仓库才能继续。

- **如果用户已指定仓库**（按名称或 UUID），直接使用。
- **如果未指定：** 不带 `warehouse_id` 参数调用 `analyze_storage_costs`。当仅存在一个受支持仓库时工具会自动选择，否则返回受支持仓库列表——让用户选择一个，然后使用选定的 `warehouse_id` 再次调用工具。

### 步骤 2：运行分析

使用以下参数调用 `analyze_storage_costs`：

- `warehouse_id`：仓库 UUID

工具获取候选表，将其分类为浪费模式（Unread、Write-only、Dead-end、Static waste、Zombie、Other stale）和表类别（Temporary、Archive/Snapshot、Production、Other），计算安全层级，并返回格式化分析结果。

- 如果工具返回错误，向用户报告并停止。
- 如果未找到候选表，告知用户并停止。

### 步骤 3：呈现初始摘要

工具输出包含两个区域：

1. `<!-- PRESENT_AS_IS -->` 块，包含精简摘要、Top-N 表和下钻提示。
2. `<!-- CATEGORY_DETAILS -->` 块，包含用 `<!-- CATEGORY:<key> -->` 标记包裹的各类别表。暂时不要呈现这些内容。

仅呈现 `<!-- PRESENT_AS_IS -->` 块——逐字复制，保留每一列、每一行和每个值。如需要可添加简短引导语，然后原样粘贴该块。用户将看到摘要和排名靠前的表，然后选择类别进行下钻。

**关键——`analyze_storage_costs` 成功后不要调用任何其他工具。** 不要调用 `search`、`get_table`，不要启动排错代理，不要交叉验证。分析结果就是最终答案；你剩下的工作只是原样呈现 `<!-- PRESENT_AS_IS -->` 块。

**关键——原样保留 markdown 链接中的 MCON。** 预格式化表格已包含正确链接的 MCON（例如 `` [`db:schema.table`](https://getmontecarlo.com/assets/MCON++...) ``）。绝不要将裸 MCON 字符串作为纯文本输出。

### 步骤 4：处理后续请求

**类别下钻。** 当用户询问特定类别时（"显示临时表"、"生产表呢？"、"告诉我更多关于归档的信息"）：

1. 在对话中已有的 `analyze_storage_costs` 结果中找到匹配的 `<!-- CATEGORY:<key> -->` 部分。**不要重新调用 `analyze_storage_costs`**——数据已存在。
2. 原样呈现该部分内容——每一列、每一行和每个值。
3. 呈现后，提醒用户尚未探索的剩余类别。

类别关键词（完整列表见 `references/output-structure.md`）：

- "temporary"、"staging"、"tmp"、"stg" → `CATEGORY:temporary`
- "archive"、"snapshot"、"backup"、"old" → `CATEGORY:archive_snapshot`
- "uncategorized"、"other"、"unknown" → `CATEGORY:other`
- "production"、"prod"、"critical"、"important" → `CATEGORY:production`

如果用户说"显示所有"或"全部类别"，按以下顺序呈现所有类别部分：temporary → archive → uncategorized → production。

**血缘检查。** 当用户询问某个特定表的消费方时（"检查 X 的血缘"、"删除 Y 安全吗？"、"这个表被谁依赖？"）：

1. 使用 `mcons: [<table mcon>]` 和 `direction: "DOWNSTREAM"` 调用 `get_asset_lineage`。
2. 如果 `has_relationships: false` → 该表的消费方可能是 BI 仪表盘或工具（而非其他表）。提及这一点——移除可能仍然安全，但用户应与仪表盘所有者确认。
3. 如果存在下游表且同样过期 → 建议同时删除。
4. 如果下游表处于活跃状态 → 标记为高风险，不要建议删除。

**注意：** Usage & Risk 列中的 `N consumers` 标志统计所有消费方，包括 BI 仪表盘（Looker、Tableau、Power BI）和其他非表资产。血缘工具仅返回表到表的边，因此血缘结果可能显示的消费方数量少于该计数。出现这种情况时，向用户解释差异。

## 读取 Usage & Risk 列

每行末尾的 `Usage & Risk` 单元格将读取端活动与风险标志组合在一起。格式：

```
{activity}                          # 无标志触发
{activity}; {flag1, flag2, ...}     # 一个或多个标志触发
```

**活动值**（始终存在）：

- `No reads` -- 无已记录的读取
- `180d · 0 reads` -- 距上次读取 N 天，零总读取
- `2d · 580 reads / 14 users` -- 近期有读取，总读取数和不同读取用户数

较低的"距上次读取天数"仅在配合读取计数时才有意义——单次备份作业或安全扫描可能让冷表看起来像"1d"。始终将过期程度与读取次数和用户数综合权衡。

**风险标志**（当任何标志触发时按此固定顺序追加在 `; ` 之后）：

- `high criticality` / `medium criticality` -- 预计算的关键性
- `N consumers` -- 存在活跃消费方（表、视图或 BI 仪表盘）；删除前需验证
- `high importance score` -- `is_important` 是 Databricks 上游计算的阈值化 `importance_score ≥ 0.6`，**不是**用户应用的标签
- `has monitors` -- 正被 Monte Carlo 监控

## 表类别

表会自动分类以优先审查：

- **Temporary/Staging** -- 短生命周期 ETL/测试表（删除最安全）
- **Archive/Snapshot** -- 历史副本、带日期后缀的表（需验证保留策略）
- **Production** -- 被监控、关键或血缘重要的表（风险最高）
- **Other** -- 无明确信号（需人工审查）

## 范围限制

- 仅限**存储**成本——不涉及计算、查询优化或计费
- 每次分析一个仓库
- 仅支持 **Snowflake、BigQuery、Redshift 和 Databricks**
- 仅提供建议——绝不执行 DROP TABLE 或破坏性操作

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例替代特定环境的测试、安全审查或用户对破坏性/高成本操作的批准。
