---
name: monte-carlo-monitor-creation
description: "通过 MCP 工具引导创建 Monte Carlo 监控器，生成 monitors-as-code YAML 用于 CI/CD 部署。当用户要求'创建监控器'、'添加监控'、'设置数据质量检查'或'生成 monitors-as-code YAML'时使用。"
category: data
risk: safe
source: community
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: "2026-04-08"
author: monte-carlo-data
tags: [data-observability, monitoring, monte-carlo, monitors-as-code]
tools: [claude, cursor, codex]
---

# Monte Carlo 监控器创建技能

本技能教你通过 MCP 正确创建 Monte Carlo 监控器。每个创建工具都以**试运行模式**运行，返回 monitors-as-code (MaC) YAML。不会直接创建监控器——用户通过 Monte Carlo CLI 或 CI/CD 应用 YAML。

参考文件位于本技能文件旁边。**使用 Read 工具**（而非 MCP 资源）访问它们：

- 指标监控器详情：`references/metric-monitor.md`（相对于本文件）
- 验证监控器详情：`references/validation-monitor.md`（相对于本文件）
- 自定义 SQL 监控器详情：`references/custom-sql-monitor.md`（相对于本文件）
- 比较监控器详情：`references/comparison-monitor.md`（相对于本文件）
- 表监控器详情：`references/table-monitor.md`（相对于本文件）

## 何时激活本技能

涉及以下场景时激活：

- 创建、添加或设置监控器（如"为...添加监控器"、"创建新鲜度检查"、"设置验证"）
- 监控特定表、字段或指标
- 检查数据质量规则或实施数据契约
- 了解表或数据集的监控选项
- 生成 monitors-as-code YAML
- 在新增转换逻辑后添加监控（当 prevent 技能未激活时）

## 何时不激活本技能

以下场景不激活：

- 仅查询数据或浏览表内容
- 分流或响应活跃告警（使用 prevent 技能的工作流 3）
- 在代码变更前运行影响评估（使用 prevent 技能的工作流 4）
- 查询已有监控器配置（直接使用 `getMonitors`）
- 编辑或删除已有监控器

---

## 可用 MCP 工具

所有工具通过 `monte-carlo` MCP 服务器提供。

| 工具                         | 用途                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| `testConnection`             | 开始前验证认证和连接               |
| `search`                     | 按名称查找表/资产；使用 `include_fields` 获取列信息 |
| `getTable`                   | Schema、统计信息、元数据、域归属、能力   |
| `getValidationPredicates`    | 列出仓库可用的验证规则类型       |
| `getDomains`                 | 列出 MC 域（仅当表无域信息时需要）  |
| `createMetricMonitorMac`     | 生成指标监控器 YAML（试运行）                     |
| `createValidationMonitorMac` | 生成验证监控器 YAML（试运行）                 |
| `createComparisonMonitorMac` | 生成比较监控器 YAML（试运行）                 |
| `createCustomSqlMonitorMac`  | 生成自定义 SQL 监控器 YAML（试运行）                 |
| `createTableMonitorMac`      | 生成表监控器 YAML（试运行）                      |

---

## 监控器类型

| 类型           | 工具                         | 适用场景                                                                                                                                |
| -------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Metric**     | `createMetricMonitorMac`     | 追踪字段上的统计指标（空值率、唯一计数、数值统计）或行数随时间的变化。需要时间戳字段用于聚合。 |
| **Validation** | `createValidationMonitorMac` | 行级数据质量检查，带条件（如"字段 X 不为空"、"状态在允许集合内"）。对无效数据告警。       |
| **Custom SQL** | `createCustomSqlMonitorMac`  | 运行任意 SQL 返回单个数值，按阈值告警。最灵活；其他类型不适用时使用。                     |
| **Comparison** | `createComparisonMonitorMac` | 比较两张表之间的指标（如开发环境 vs 生产环境、源表 vs 目标表）。                                                               |
| **Table**      | `createTableMonitorMac`      | 监控一组表的新鲜度、Schema 变更和数据量。在数据库/Schema 级别使用资产选择。                      |

---

## 操作流程

按顺序执行以下步骤。不要跳过步骤。

### 验证阶段（步骤 1-3）—— 必须在任何创建工具调用前完成

最常见的错误模式是智能体跳过验证，用猜测或不完整的参数调用创建工具。**创建调用中的每个字段都必须基于此阶段检索到的数据。** 在步骤 1-3 完全满足之前，不要进入步骤 4。

#### 步骤 1：理解请求

自问：
- 用户想监控什么？（特定表、指标、数据质量规则、跨表一致性、Schema 级别的新鲜度/数据量）
- 哪种监控器类型适合？参考上面的监控器类型表。
- 用户是否具备所有细节，还是需要引导？

如果用户意图不明确，先提出针对性问题再继续。

#### 步骤 2：识别表和列

如果没有表的 MCON：
1. 使用 `search` 加表名和 `include_fields: ["field_names"]` 查找 MCON 并获取列名。
2. 如果用户提供了完整表 ID 如 `database:schema.table`，搜索它。
3. 获取 MCON 后，调用 `getTable` 并传入 `include_fields: true` 和 `include_table_capabilities: true` 验证能力并获取域信息。

如果已有 MCON：
1. 使用 MCON 调用 `getTable`，传入 `include_fields: true` 和 `include_table_capabilities: true`。

**关键：必须使用 `getTable` 结果中的实际列名。绝不要猜测或编造列名。** 这是监控器创建失败的最常见原因。

对于需要时间戳列的监控器类型（指标监控器），查看列名并识别可能的时间戳候选项。如有歧义，向用户展示。

#### 步骤 3：处理域分配

监控器必须分配到包含被监控表的域。`getTable` 响应包含 `domains` 列表，含 `uuid` 和 `name`。

1. 如果 `domains` 为空：跳过域分配。
2. 如果 `domains` 恰好有一个条目：默认 `domain_id` 为该域的 UUID。
3. 如果 `domains` 有多个条目：仅展示这些域，让用户选择。

不要将所有账户域作为选项展示——只有包含该表的域才是有效的。

**始终在调用任何创建工具前检查表的 `domains`。**

---

### 创建阶段（步骤 4-8）

仅在验证阶段完成且拥有 MCP 工具返回的真实数据后才进入此阶段。

#### 步骤 4：加载子技能参考

根据监控器类型，阅读详细参考获取参数指导：

- **Metric** —— 阅读详细参考：`references/metric-monitor.md`（相对于本文件）
- **Validation** —— 阅读详细参考：`references/validation-monitor.md`（相对于本文件）
- **Custom SQL** —— 阅读详细参考：`references/custom-sql-monitor.md`（相对于本文件）
- **Comparison** —— 阅读详细参考：`references/comparison-monitor.md`（相对于本文件）
- **Table** —— 阅读详细参考：`references/table-monitor.md`（相对于本文件）

#### 步骤 5：询问调度

**表监控器跳过此步骤。** 表监控器不支持 MaC YAML 中的 `schedule` 字段——添加它会导致 `montecarlo monitors apply` 验证错误。表监控器的调度由 Monte Carlo 自动管理。

对于其他所有监控器类型，创建工具默认为每 60 分钟运行的固定调度。展示以下选项：

1. **固定间隔** —— `interval_minutes` 为任意整数（30、60、90、120、360、720、1440 等）
2. **动态** —— MC 根据表更新模式自动确定运行时间。
3. **宽松** —— 每天运行一次。

MaC YAML 中的调度格式：
- 固定：`schedule: { type: fixed, interval_minutes: <N> }`
- 动态：`schedule: { type: dynamic }`
- 宽松：`schedule: { type: loose, start_time: "00:00" }`

#### 步骤 6：与用户确认

调用创建工具前，用自然语言展示监控器配置：
- 监控器类型
- 目标表（及适用时的列）
- 检查内容 / 触发告警的条件
- 域分配
- 调度

询问："配置是否正确？我将生成监控器配置。"

**绝不在未经用户确认的情况下调用创建工具。**

#### 步骤 7：创建监控器

使用前几步构建的参数调用相应的创建工具。尽可能传入 MCON。如果只有表名，同时传入 warehouse。

#### 步骤 8：展示结果

**关键：始终在响应中包含 YAML。** 用户需要可直接复制的 YAML。

1. 如果选择了非默认调度，在展示前修改 YAML 中的调度部分。
2. 将 YAML 包裹在完整 MaC 结构中（见下方"MaC YAML 格式"部分）。
3. 始终在 ```yaml 代码块中展示完整 YAML。
4. 说明存放位置和应用方式（见下方）。
5. 始终使用 ISO 8601 格式表示日期时间值。
6. 绝不重新格式化创建工具返回的 YAML 值。

---

## MaC YAML 格式

创建工具返回的 YAML 是监控器定义。必须包裹在标准 MaC 结构中才能应用：

```yaml
montecarlo:
  <monitor_type>:
    - <returned yaml>
```

例如，指标监控器如下：

```yaml
montecarlo:
  metric:
    - <yaml returned by createMetricMonitorMac>
```

**重要：** `montecarlo.yml`（不带目录路径）是一个独立的 Monte Carlo 项目配置文件——它与监控器定义文件不同。监控器定义放在各自的 `.yml` 文件中，通常在 `monitors/` 目录下或 dbt 模型 Schema 文件旁。

告知用户：
- 将 YAML 保存到 `.yml` 文件（如 `monitors/<table_name>.yml` 或放在 dbt Schema 中）
- 通过 Monte Carlo CLI 应用：`montecarlo monitors apply --namespace <namespace>`
- 或集成到 CI/CD 中实现合并时自动部署

---

## 常见错误

- **绝不猜测列名。** 始终从 `getTable` 获取。
- **绝不跳过确认步骤**（步骤 6）。
- 指标监控器的 `aggregate_time_field` 必须是表中的真实时间戳列。
- 验证监控器的条件匹配无效数据，而非有效数据。
- 尽可能传入 MCON。如果只有表名，同时传入 warehouse。
- **始终在调用任何创建工具前检查表的 `domains`。**
- 始终使用 ISO 8601 格式表示日期时间值。
- 绝不重新格式化创建工具返回的 YAML 值。
- 在验证阶段完成前不要调用创建工具。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少必要输入、权限、安全边界或成功标准，停下来请求澄清。
