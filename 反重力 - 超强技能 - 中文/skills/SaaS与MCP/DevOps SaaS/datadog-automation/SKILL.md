---
name: datadog-automation
description: "通过 Rube MCP (Composio) 自动化 Datadog 任务：查询指标、搜索日志、管理监控器/仪表盘、创建事件和停机时间。始终先搜索工具以获取当前 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Datadog Automation via Rube MCP

通过 Composio 的 Datadog 工具包（经由 Rube MCP）自动化 Datadog 监控和可观测性操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Datadog 连接，工具包为 `datadog`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `datadog` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Datadog 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 查询和探索指标

**适用场景**：用户想要查询指标数据或列出可用指标

**工具序列**：
1. `DATADOG_LIST_METRICS` - 列出可用指标名称 [可选]
2. `DATADOG_QUERY_METRICS` - 查询指标时序数据 [必需]

**关键参数**：
- `query`: Datadog 指标查询字符串（例如 `avg:system.cpu.user{host:web01}`）
- `from`: 起始时间戳（Unix 纪元秒）
- `to`: 结束时间戳（Unix 纪元秒）
- `q`: 列出指标的搜索字符串

**注意事项**：
- 查询语法遵循 Datadog 指标查询格式：`aggregation:metric_name{tag_filters}`
- `from` 和 `to` 是 Unix 纪元时间戳，单位为秒而非毫秒
- 有效聚合函数：`avg`、`sum`、`min`、`max`、`count`
- 标签过滤器使用花括号：`{host:web01,env:prod}`
- 时间范围不应超过该指标类型的 Datadog 保留限制

### 2. 搜索和分析日志

**适用场景**：用户想要搜索日志条目或列出日志索引

**工具序列**：
1. `DATADOG_LIST_LOG_INDEXES` - 列出可用日志索引 [可选]
2. `DATADOG_SEARCH_LOGS` - 使用查询和过滤器搜索日志 [必需]

**关键参数**：
- `query`: 使用 Datadog 日志查询语法的搜索查询
- `from`: 起始时间（ISO 8601 或 Unix 时间戳）
- `to`: 结束时间（ISO 8601 或 Unix 时间戳）
- `sort`: 排序顺序（'asc' 或 'desc'）
- `limit`: 返回的日志条目数量

**注意事项**：
- 日志查询使用 Datadog 日志搜索语法：`service:web status:error`
- 搜索仅限于配置的保留期内的已保留日志
- 大结果集需要分页；检查是否有游标/页面令牌
- 日志索引控制路由和保留；如已知可按索引过滤

### 3. 管理监控器

**适用场景**：用户想要创建、更新、静音或检查监控器

**工具序列**：
1. `DATADOG_LIST_MONITORS` - 使用过滤器列出所有监控器 [必需]
2. `DATADOG_GET_MONITOR` - 获取特定监控器详情 [可选]
3. `DATADOG_CREATE_MONITOR` - 创建新监控器 [可选]
4. `DATADOG_UPDATE_MONITOR` - 更新监控器配置 [可选]
5. `DATADOG_MUTE_MONITOR` - 临时静音监控器 [可选]
6. `DATADOG_UNMUTE_MONITOR` - 重新启用已静音的监控器 [可选]

**关键参数**：
- `monitor_id`: 数字监控器 ID
- `name`: 监控器显示名称
- `type`: 监控器类型（'metric alert'、'service check'、'log alert'、'query alert' 等）
- `query`: 定义告警条件的监控器查询
- `message`: 带 @mentions 的通知消息
- `tags`: 标签字符串数组
- `thresholds`: 告警阈值（`critical`、`warning`、`ok`）

**注意事项**：
- 监控器 `type` 必须与查询类型匹配；不匹配会导致创建失败
- `message` 支持 @mentions 通知（例如 `@slack-channel`、`@pagerduty`）
- 阈值因监控器类型而异；指标监控器至少需要 `critical`
- 静音监控器会抑制通知，但监控器仍会评估
- 监控器 ID 是数字整数

### 4. 管理仪表盘

**适用场景**：用户想要列出、查看、更新或删除仪表盘

**工具序列**：
1. `DATADOG_LIST_DASHBOARDS` - 列出所有仪表盘 [必需]
2. `DATADOG_GET_DASHBOARD` - 获取完整仪表盘定义 [可选]
3. `DATADOG_UPDATE_DASHBOARD` - 更新仪表盘布局或组件 [可选]
4. `DATADOG_DELETE_DASHBOARD` - 删除仪表盘（不可逆）[可选]

**关键参数**：
- `dashboard_id`: 仪表盘标识符字符串
- `title`: 仪表盘标题
- `layout_type`: 'ordered'（网格）或 'free'（自由定位）
- `widgets`: 组件定义对象数组
- `description`: 仪表盘描述

**注意事项**：
- 仪表盘 ID 是字母数字字符串（例如 'abc-def-ghi'），不是数字
- `layout_type` 创建后无法更改；必须重新创建仪表盘
- 组件定义是复杂的嵌套对象；先获取现有仪表盘以了解结构
- DELETE 是永久性的；无法撤销

### 5. 创建事件和管理停机时间

**适用场景**：用户想要发布事件或安排维护停机时间

**工具序列**：
1. `DATADOG_LIST_EVENTS` - 列出现有事件 [可选]
2. `DATADOG_CREATE_EVENT` - 发布新事件 [必需]
3. `DATADOG_CREATE_DOWNTIME` - 安排维护停机时间 [可选]

**事件关键参数**：
- `title`: 事件标题
- `text`: 事件正文（支持 markdown）
- `alert_type`: 事件严重程度（'error'、'warning'、'info'、'success'）
- `tags`: 标签字符串数组

**停机时间关键参数**：
- `scope`: 停机时间的标签范围（例如 `host:web01`）
- `start`: 起始时间（Unix 纪元）
- `end`: 结束时间（Unix 纪元；省略表示无限期）
- `message`: 停机时间描述
- `monitor_id`: 要停机的特定监控器（可选，省略则基于范围）

**注意事项**：
- 事件 `text` 支持 Datadog 的 markdown 格式，包括 @mentions
- 停机时间 scope 使用标签语法：`host:web01`、`env:staging`
- 省略 `end` 会创建无限期停机时间；维护时始终设置结束时间
- 停机时间 `monitor_id` 缩小到单个监控器；scope 应用于所有匹配的监控器

### 6. 管理主机和追踪

**适用场景**：用户想要列出基础设施主机或检查分布式追踪

**工具序列**：
1. `DATADOG_LIST_HOSTS` - 列出所有上报的主机 [必需]
2. `DATADOG_GET_TRACE_BY_ID` - 获取特定分布式追踪 [可选]

**关键参数**：
- `filter`: 主机搜索过滤字符串
- `sort_field`: 按字段排序主机（例如 'name'、'apps'、'cpu'）
- `sort_dir`: 排序方向（'asc' 或 'desc'）
- `trace_id`: 分布式追踪 ID 用于追踪查找

**注意事项**：
- 主机列表包括在保留窗口内上报到 Datadog 的所有主机
- 追踪 ID 是长数字字符串；确保精确匹配
- 停止上报的主机会在配置的期间内保留，然后移除

## 常用模式

### 监控器查询语法

**指标告警**：
```
avg(last_5m):avg:system.cpu.user{env:prod} > 90
```

**日志告警**：
```
logs("service:web status:error").index("main").rollup("count").last("5m") > 10
```

### 标签过滤

- 标签使用 `key:value` 格式：`host:web01`、`env:prod`、`service:api`
- 多个标签：`{host:web01,env:prod}`（AND 逻辑）
- 通配符：`host:web*`

### 分页

- 根据端点使用 `page` 和 `page_size` 或基于偏移的分页
- 检查响应中的总计数以确定是否存在更多页面
- 持续获取直到检索完所有结果

## 已知注意事项

**时间戳**：
- 大多数端点使用 Unix 纪元秒（而非毫秒）
- 部分端点接受 ISO 8601；检查工具 schema
- 时间范围应合理（不要查询数年的数据）

**查询语法**：
- 指标查询：`aggregation:metric{tags}`
- 日志查询：`field:value` 对
- 监控器查询因类型而异；查阅 Datadog 文档

**速率限制**：
- Datadog API 有每个端点的速率限制
- 在 429 响应时实现退避
- 尽可能批量操作

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 查询指标 | DATADOG_QUERY_METRICS | query, from, to |
| 列出指标 | DATADOG_LIST_METRICS | q |
| 搜索日志 | DATADOG_SEARCH_LOGS | query, from, to, limit |
| 列出日志索引 | DATADOG_LIST_LOG_INDEXES | (无) |
| 列出监控器 | DATADOG_LIST_MONITORS | tags |
| 获取监控器 | DATADOG_GET_MONITOR | monitor_id |
| 创建监控器 | DATADOG_CREATE_MONITOR | name, type, query, message |
| 更新监控器 | DATADOG_UPDATE_MONITOR | monitor_id |
| 静音监控器 | DATADOG_MUTE_MONITOR | monitor_id |
| 取消静音监控器 | DATADOG_UNMUTE_MONITOR | monitor_id |
| 列出仪表盘 | DATADOG_LIST_DASHBOARDS | (无) |
| 获取仪表盘 | DATADOG_GET_DASHBOARD | dashboard_id |
| 更新仪表盘 | DATADOG_UPDATE_DASHBOARD | dashboard_id, title, widgets |
| 删除仪表盘 | DATADOG_DELETE_DASHBOARD | dashboard_id |
| 列出事件 | DATADOG_LIST_EVENTS | start, end |
| 创建事件 | DATADOG_CREATE_EVENT | title, text, alert_type |
| 创建停机时间 | DATADOG_CREATE_DOWNTIME | scope, start, end |
| 列出主机 | DATADOG_LIST_HOSTS | filter, sort_field |
| 获取追踪 | DATADOG_GET_TRACE_BY_ID | trace_id |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
