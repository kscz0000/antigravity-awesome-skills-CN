---
name: google-analytics-automation
description: "通过 Rube MCP (Composio) 自动化 Google Analytics 任务：运行报告、列出账号/媒体资源、漏斗、透视表、关键事件。始终先搜索工具获取当前 schema。当用户要求'Google Analytics 自动化'、'GA4 报告'、'运行 GA 报告'、'列出 GA 账号'、'GA 漏斗分析'、'GA 透视表'或'GA 关键事件'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Google Analytics 自动化

通过 Composio 的 Google Analytics 工具包和 Rube MCP 自动化 Google Analytics 4 (GA4) 报告和媒体资源管理。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 工具包 `google_analytics` 建立活跃的 Google Analytics 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 响应以验证 Rube MCP 可用
2. 使用工具包 `google_analytics` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Google OAuth
4. 在运行任何工作流前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出账号和媒体资源

**何时使用**：用户想要发现可用的 GA4 账号和媒体资源

**工具调用顺序**：
1. `GOOGLE_ANALYTICS_LIST_ACCOUNTS` - 列出所有可访问的 GA4 账号 [必需]
2. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - 列出账号下的媒体资源 [必需]

**关键参数**：
- `pageSize`：每页结果数量
- `pageToken`：上一次响应的分页标记
- `filter`：媒体资源过滤表达式（例如 `parent:accounts/12345`）

**注意事项**：
- 媒体资源 ID 是带有 'properties/' 前缀的数字字符串（例如 'properties/123456'）
- 账号 ID 带有 'accounts/' 前缀（例如 'accounts/12345'）
- 始终先列出账号，再列出每个账号下的媒体资源
- 拥有大量媒体资源的组织需要分页处理

### 2. 运行标准报告

**何时使用**：用户想要从 GA4 数据中查询指标和维度

**工具调用顺序**：
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - 获取媒体资源 ID [前置条件]
2. `GOOGLE_ANALYTICS_GET_METADATA` - 发现可用的维度和指标 [可选]
3. `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` - 验证维度/指标兼容性 [可选]
4. `GOOGLE_ANALYTICS_RUN_REPORT` - 执行报告查询 [必需]

**关键参数**：
- `property`：媒体资源 ID（例如 'properties/123456'）
- `dateRanges`：包含 `startDate` 和 `endDate` 的日期范围对象数组
- `dimensions`：包含 `name` 字段的维度对象数组
- `metrics`：包含 `name` 字段的指标对象数组
- `dimensionFilter` / `metricFilter`：过滤表达式
- `orderBys`：排序配置
- `limit`：返回的最大行数
- `offset`：分页行偏移量

**注意事项**：
- 日期格式为 'YYYY-MM-DD' 或相对值如 'today'、'yesterday'、'7daysAgo'、'30daysAgo'
- 并非所有维度和指标都兼容；先使用 CHECK_COMPATIBILITY 验证
- 使用 GET_METADATA 发现有效的维度和指标名称
- 每个报告请求最多 9 个维度
- 行数限制默认值各异；大数据集需显式设置
- `offset` 用于结果分页，而非日期分页

### 3. 运行批量报告

**何时使用**：用户需要在一次调用中从同一媒体资源获取多个不同的报告

**工具调用顺序**：
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - 获取媒体资源 ID [前置条件]
2. `GOOGLE_ANALYTICS_BATCH_RUN_REPORTS` - 一次执行多个报告 [必需]

**关键参数**：
- `property`：媒体资源 ID（必需）
- `requests`：单个报告请求对象数组（结构与 RUN_REPORT 相同）

**注意事项**：
- 每次批量调用最多 5 个报告请求
- 批量中的所有报告必须针对同一媒体资源
- 每个单独报告的维度/指标限制与 RUN_REPORT 相同
- 批量错误可能影响所有报告；检查各个报告响应

### 4. 运行透视报告

**何时使用**：用户想要交叉表数据（行 vs 列），类似透视表

**工具调用顺序**：
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - 获取媒体资源 ID [前置条件]
2. `GOOGLE_ANALYTICS_RUN_PIVOT_REPORT` - 执行透视报告 [必需]

**关键参数**：
- `property`：媒体资源 ID（必需）
- `dateRanges`：日期范围对象
- `dimensions`：透视中使用的所有维度
- `metrics`：要聚合的指标
- `pivots`：透视定义数组，包含 `fieldNames`、`limit` 和 `orderBys`

**注意事项**：
- 透视中使用的维度也必须列在顶层 `dimensions` 中
- 透视的 `fieldNames` 引用顶层列表中的维度名称
- 包含多个维度的复杂透视可能产生非常大的结果集
- 每个透视有独立的 `limit` 和 `orderBys`

### 5. 运行漏斗报告

**何时使用**：用户想要分析转化漏斗和流失率

**工具调用顺序**：
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - 获取媒体资源 ID [前置条件]
2. `GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT` - 执行漏斗分析 [必需]

**关键参数**：
- `property`：媒体资源 ID（必需）
- `dateRanges`：日期范围对象
- `funnel`：包含 `steps` 数组的漏斗定义
- `funnelBreakdown`：可选，用于细分漏斗的维度

**注意事项**：
- 漏斗步骤是有序的；每个步骤定义用户必须满足的条件
- 步骤使用类似维度/指标过滤器的过滤表达式
- 开放漏斗允许在任意步骤进入；封闭漏斗要求顺序推进
- 漏斗报告处理时间可能比标准报告更长

### 6. 管理关键事件

**何时使用**：用户想要查看或管理 GA4 中的转化事件（关键事件）

**工具调用顺序**：
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - 获取媒体资源 ID [前置条件]
2. `GOOGLE_ANALYTICS_LIST_KEY_EVENTS` - 列出媒体资源的所有关键事件 [必需]

**关键参数**：
- `parent`：媒体资源资源名称（例如 'properties/123456'）
- `pageSize`：每页结果数量
- `pageToken`：分页标记

**注意事项**：
- 关键事件在 GA4 中以前称为"转化"
- 媒体资源必须配置有关键事件才能返回结果
- 关键事件名称对应 GA4 事件名称

## 常见模式

### ID 解析

**账号名称 -> 账号 ID**：
```
1. Call GOOGLE_ANALYTICS_LIST_ACCOUNTS
2. Find account by displayName
3. Extract name field (e.g., 'accounts/12345')
```

**媒体资源名称 -> 媒体资源 ID**：
```
1. Call GOOGLE_ANALYTICS_LIST_PROPERTIES with filter
2. Find property by displayName
3. Extract name field (e.g., 'properties/123456')
```

### 维度/指标发现

```
1. Call GOOGLE_ANALYTICS_GET_METADATA with property ID
2. Browse available dimensions and metrics
3. Call GOOGLE_ANALYTICS_CHECK_COMPATIBILITY to verify combinations
4. Use verified dimensions/metrics in RUN_REPORT
```

### 分页

- 报告：使用 `offset` 和 `limit` 进行行分页
- 账号/媒体资源：使用响应中的 `pageToken`
- 持续获取直到 `pageToken` 不存在或达到 `rowCount`

### 常用维度和指标

**维度**：`date`、`city`、`country`、`deviceCategory`、`sessionSource`、`sessionMedium`、`pagePath`、`pageTitle`、`eventName`

**指标**：`activeUsers`、`sessions`、`screenPageViews`、`eventCount`、`conversions`、`totalRevenue`、`bounceRate`、`averageSessionDuration`

## 已知注意事项

**媒体资源 ID**：
- 始终使用完整资源名称格式：'properties/123456'
- 仅使用数字 ID 会导致错误
- 通过 LIST_PROPERTIES 将媒体资源名称解析为 ID

**日期范围**：
- 格式：'YYYY-MM-DD' 或相对值（'today'、'yesterday'、'7daysAgo'、'30daysAgo'）
- 数据处理延迟意味着今日数据可能不完整
- 最大日期范围因媒体资源配置而异

**兼容性**：
- 并非所有维度都能与所有指标配合使用
- 复杂报告前始终用 CHECK_COMPATIBILITY 验证
- 自定义维度/指标有特定的命名模式

**响应解析**：
- 报告数据嵌套在 `rows` 数组中，包含 `dimensionValues` 和 `metricValues`
- 值以字符串形式返回；需显式解析数字
- 空报告不返回 `rows` 键（而非空数组）

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出账号 | GOOGLE_ANALYTICS_LIST_ACCOUNTS | pageSize, pageToken |
| 列出媒体资源 | GOOGLE_ANALYTICS_LIST_PROPERTIES | filter, pageSize |
| 获取元数据 | GOOGLE_ANALYTICS_GET_METADATA | property |
| 检查兼容性 | GOOGLE_ANALYTICS_CHECK_COMPATIBILITY | property, dimensions, metrics |
| 运行报告 | GOOGLE_ANALYTICS_RUN_REPORT | property, dateRanges, dimensions, metrics |
| 批量报告 | GOOGLE_ANALYTICS_BATCH_RUN_REPORTS | property, requests |
| 透视报告 | GOOGLE_ANALYTICS_RUN_PIVOT_REPORT | property, dateRanges, pivots |
| 漏斗报告 | GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT | property, dateRanges, funnel |
| 列出关键事件 | GOOGLE_ANALYTICS_LIST_KEY_EVENTS | parent, pageSize |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需输入、权限、安全边界或成功标准，请停止并请求澄清。
