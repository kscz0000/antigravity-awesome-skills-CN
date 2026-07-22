---
name: mixpanel-automation
description: "通过 Rube MCP (Composio) 自动化 Mixpanel 任务：事件、分群分析、漏斗、用户群组、用户画像、JQL 查询。始终先搜索工具获取最新 schema。当用户要求'自动化 Mixpanel'、'查询 Mixpanel 数据'、'Mixpanel 事件分析'、'Mixpanel 漏斗分析'、'Mixpanel 用户分群'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Mixpanel

通过 Composio 的 Mixpanel 工具包和 Rube MCP 自动化 Mixpanel 产品分析。

## 前置条件

- Rube MCP 已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `mixpanel` 建立活跃的 Mixpanel 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 可响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `mixpanel`
3. 若连接状态非 ACTIVE，按返回的认证链接完成 Mixpanel 认证
4. 确认连接状态为 ACTIVE 后再执行任何工作流

## 核心工作流

### 1. 聚合事件数据

**适用场景**：统计事件数量、获取总量或追踪事件趋势

**工具调用顺序**：
1. `MIXPANEL_GET_ALL_PROJECTS` — 列出项目以获取项目 ID [前置]
2. `MIXPANEL_AGGREGATE_EVENT_COUNTS` — 获取事件计数和聚合结果 [必需]

**关键参数**：
- `event`：事件名称或事件名称数组
- `from_date` / `to_date`：日期范围，格式 'YYYY-MM-DD'
- `unit`：时间粒度（'minute'、'hour'、'day'、'week'、'month'）
- `type`：聚合类型（'general'、'unique'、'average'）
- `where`：事件属性过滤表达式

**注意事项**：
- 日期格式必须为 'YYYY-MM-DD'，其他格式会报错
- 事件名称区分大小写，须使用 Mixpanel 项目中的精确名称
- `where` 过滤器使用 Mixpanel 表达式语法（如 `properties["country"] == "US"`）
- 最大日期范围可能受 Mixpanel 套餐限制

### 2. 运行分群查询

**适用场景**：按属性拆分事件进行详细分析

**工具调用顺序**：
1. `MIXPANEL_QUERY_SEGMENTATION` — 运行分群分析 [必需]

**关键参数**：
- `event`：要分群的事件名称
- `from_date` / `to_date`：日期范围，格式 'YYYY-MM-DD'
- `on`：分群依据的属性（如 `properties["country"]`）
- `unit`：时间粒度
- `type`：计数类型（'general'、'unique'、'average'）
- `where`：过滤表达式
- `limit`：返回的最大分群数

**注意事项**：
- `on` 参数使用 Mixpanel 属性表达式语法
- 属性引用必须使用 `properties["prop_name"]` 格式
- 对高基数属性分群时结果会被截断，请使用 `limit`
- 结果按分群属性和时间单位分组

### 3. 分析漏斗

**适用场景**：追踪转化漏斗并定位流失环节

**工具调用顺序**：
1. `MIXPANEL_LIST_FUNNELS` — 列出已保存的漏斗以获取漏斗 ID [前置]
2. `MIXPANEL_QUERY_FUNNEL` — 执行漏斗分析 [必需]

**关键参数**：
- `funnel_id`：要查询的已保存漏斗 ID
- `from_date` / `to_date`：日期范围
- `unit`：时间粒度
- `where`：过滤表达式
- `on`：漏斗分群属性
- `length`：转化窗口（天数）

**注意事项**：
- `funnel_id` 为必填项，须先通过 LIST_FUNNELS 获取
- 漏斗须先在 Mixpanel UI 中创建，API 仅查询已有漏斗
- 转化窗口（`length`）默认值不固定，应显式设置以确保准确性
- 大日期范围配合分群可能产生非常大的响应

### 4. 管理用户画像

**适用场景**：查询或更新 Mixpanel 中的用户画像

**工具调用顺序**：
1. `MIXPANEL_QUERY_PROFILES` — 搜索和筛选用户画像 [必需]
2. `MIXPANEL_PROFILE_BATCH_UPDATE` — 批量更新用户画像 [可选]

**关键参数**：
- `where`：画像属性过滤表达式（如 `properties["plan"] == "premium"`）
- `output_properties`：结果中包含的属性名数组
- `page`：分页页码
- `session_id`：保持分页一致性的会话 ID（来自首次响应）
- 批量更新：包含 `$distinct_id` 和属性操作的画像更新数组

**注意事项**：
- 画像查询返回分页结果，使用首次响应的 `session_id` 保持分页一致
- `where` 使用 Mixpanel 表达式语法操作画像属性
- BATCH_UPDATE 对画像执行操作（`$set`、`$unset`、`$add`、`$append`）
- 批量更新有单次请求最大画像数限制，大批量需分块处理
- 画像属性名区分大小写

### 5. 管理用户群组

**适用场景**：列出或分析用户群组

**工具调用顺序**：
1. `MIXPANEL_COHORTS_LIST` — 列出所有已保存的群组 [必需]

**关键参数**：
- 无必填参数，返回所有可访问的群组
- 响应包含群组 `id`、`name`、`description`、`count`

**注意事项**：
- 群组在 Mixpanel UI 中创建和管理，API 仅提供读取权限
- 群组 ID 为数字，须使用列表结果中的精确 ID
- 超大群组的计数可能为近似值
- 群组可通过 `where` 表达式作为其他查询的过滤条件

### 6. 运行 JQL 和 Insight 查询

**适用场景**：运行自定义 JQL 查询或 Insight 分析

**工具调用顺序**：
1. `MIXPANEL_JQL_QUERY` — 执行自定义 JQL（JavaScript Query Language）查询 [可选]
2. `MIXPANEL_QUERY_INSIGHT` — 运行已保存的 Insight 查询 [可选]

**关键参数**：
- JQL：`script`，包含 JQL JavaScript 代码
- Insight：`bookmark_id`，已保存 Insight 的 ID
- `project_id`：查询的项目上下文

**注意事项**：
- JQL 使用 Mixpanel 专用的类 JavaScript 语法
- JQL 查询有执行时间限制，需优化效率
- Insight `bookmark_id` 须引用已保存的 Insight
- JQL 为遗留功能，请查阅 Mixpanel 文档确认当前可用性

## 常用模式

### ID 解析

**项目名称 → 项目 ID**：
```
1. Call MIXPANEL_GET_ALL_PROJECTS
2. Find project by name in results
3. Extract project id
```

**漏斗名称 → 漏斗 ID**：
```
1. Call MIXPANEL_LIST_FUNNELS
2. Find funnel by name
3. Extract funnel_id
```

### Mixpanel 表达式语法

用于 `where` 和 `on` 参数：
- 属性引用：`properties["property_name"]`
- 等值判断：`properties["country"] == "US"`
- 比较运算：`properties["age"] > 25`
- 布尔值：`properties["is_premium"] == true`
- 包含判断：`"search_term" in properties["name"]`
- AND/OR：`properties["country"] == "US" and properties["plan"] == "pro"`

### 分页

- 事件查询：通过调整日期范围实现基于日期的分页
- 画像查询：使用 `page` 页码和 `session_id` 保持结果一致
- 漏斗/群组列表：通常返回完整结果，无需分页

## 已知注意事项

**日期格式**：
- 始终使用 'YYYY-MM-DD' 格式
- 日期范围两端均为包含
- 数据新鲜度取决于 Mixpanel 数据摄入延迟（通常为数分钟）

**表达式语法**：
- 属性引用始终使用 `properties["name"]` 格式
- 字符串值须加引号：`properties["status"] == "active"`
- 数值不加引号：`properties["count"] > 10`
- 布尔值：`true` / `false`（小写）

**速率限制**：
- Mixpanel API 按项目设有限速
- 大规模分群查询可能超时，应缩小日期范围或减少分群数
- 尽量使用批量操作以减少 API 调用

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 事件数据通常按日期和分群分组
- 数值可能以字符串形式返回，需显式解析
- 空日期范围返回空对象，而非空数组

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出项目 | MIXPANEL_GET_ALL_PROJECTS | (无) |
| 聚合事件 | MIXPANEL_AGGREGATE_EVENT_COUNTS | event, from_date, to_date, unit |
| 分群查询 | MIXPANEL_QUERY_SEGMENTATION | event, on, from_date, to_date |
| 列出漏斗 | MIXPANEL_LIST_FUNNELS | (无) |
| 查询漏斗 | MIXPANEL_QUERY_FUNNEL | funnel_id, from_date, to_date |
| 查询画像 | MIXPANEL_QUERY_PROFILES | where, output_properties, page |
| 批量更新画像 | MIXPANEL_PROFILE_BATCH_UPDATE | (画像更新对象) |
| 列出群组 | MIXPANEL_COHORTS_LIST | (无) |
| JQL 查询 | MIXPANEL_JQL_QUERY | script |
| 查询 Insight | MIXPANEL_QUERY_INSIGHT | bookmark_id |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，应停止并请求澄清。
