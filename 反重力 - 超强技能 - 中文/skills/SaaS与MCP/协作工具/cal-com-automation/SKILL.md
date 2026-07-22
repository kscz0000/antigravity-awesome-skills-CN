---
name: cal-com-automation
description: "通过 Rube MCP (Composio) 自动化 Cal.com 任务：管理预订、查看可用时间、配置 webhook 和处理团队。当用户要求'管理 Cal.com 预订'、'查看日程可用时间'、'配置 Cal.com webhook'或'管理 Cal.com 团队'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Cal.com 自动化（通过 Rube MCP）

通过 Composio 的 Cal 工具包和 Rube MCP 自动化 Cal.com 日程安排操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 连接 Cal.com，工具包为 `cal`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API key — 添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 响应正常，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，指定工具包 `cal`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Cal.com 认证
4. 确认连接状态显示 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 管理预订

**适用场景**：用户想要列出、创建或查看预订

**工具调用顺序**：
1. `CAL_FETCH_ALL_BOOKINGS` - 列出所有预订（支持筛选）[必需]
2. `CAL_POST_NEW_BOOKING_REQUEST` - 创建新预订 [可选]

**列出预订的关键参数**：
- `status`：按预订状态筛选（'upcoming', 'recurring', 'past', 'cancelled', 'unconfirmed'）
- `afterStart`：筛选此日期之后的预订（ISO 8601）
- `beforeEnd`：筛选此日期之前的预订（ISO 8601）

**创建预订的关键参数**：
- `eventTypeId`：预订的事件类型 ID
- `start`：预订开始时间（ISO 8601）
- `end`：预订结束时间（ISO 8601）
- `name`：参会者姓名
- `email`：参会者邮箱
- `timeZone`：参会者时区（IANA 格式）
- `language`：参会者语言代码
- `metadata`：附加元数据对象

**注意事项**：
- 日期筛选使用带时区的 ISO 8601 格式（如 '2024-01-15T09:00:00Z'）
- `eventTypeId` 必须引用有效且活跃的事件类型
- 创建预订需要匹配可用时段；请先检查可用性
- 时区必须是有效的 IANA 时区字符串（如 'America/New_York'）
- 状态筛选值为特定字符串；无效值会返回空结果

### 2. 检查可用性

**适用场景**：用户想要查找空闲/忙碌时间或可用预订时段

**工具调用顺序**：
1. `CAL_RETRIEVE_CALENDAR_BUSY_TIMES` - 获取忙碌时间段 [必需]
2. `CAL_GET_AVAILABLE_SLOTS_INFO` - 获取具体可用时段 [必需]

**关键参数**：
- `dateFrom`：可用性检查开始日期（YYYY-MM-DD）
- `dateTo`：可用性检查结束日期（YYYY-MM-DD）
- `eventTypeId`：要检查时段的事件类型
- `timeZone`：可用性响应的时区
- `loggedInUsersTz`：请求用户的时区

**注意事项**：
- 忙碌时间显示用户不可用的时间段
- 可用时段取决于事件类型的时长和配置
- 日期范围应合理（不要提前数月），以获得准确结果
- 时区影响时段显示方式；务必明确指定
- 可用性反映日历集成（Google Calendar、Outlook 等）

### 3. 配置 Webhook

**适用场景**：用户想要设置或管理预订事件的 webhook 通知

**工具调用顺序**：
1. `CAL_RETRIEVE_WEBHOOKS_LIST` - 列出现有 webhook [必需]
2. `CAL_GET_WEBHOOK_BY_ID` - 获取特定 webhook 详情 [可选]
3. `CAL_UPDATE_WEBHOOK_BY_ID` - 更新 webhook 配置 [可选]
4. `CAL_DELETE_WEBHOOK_BY_ID` - 删除 webhook [可选]

**关键参数**：
- `id`：GET/UPDATE/DELETE 操作的 webhook ID
- `subscriberUrl`：Webhook 端点 URL
- `eventTriggers`：触发事件类型数组
- `active`：Webhook 是否激活
- `secret`：Webhook 签名密钥

**注意事项**：
- Webhook URL 必须是公开可访问的 HTTPS 端点
- 事件触发器包括：'BOOKING_CREATED'、'BOOKING_RESCHEDULED'、'BOOKING_CANCELLED' 等
- 非激活状态的 webhook 不会触发；切换 `active` 来启用/禁用
- Webhook 密钥用于负载签名验证

### 4. 管理团队

**适用场景**：用户想要创建、查看或管理团队及团队事件类型

**工具调用顺序**：
1. `CAL_GET_TEAMS_LIST` - 列出所有团队 [必需]
2. `CAL_GET_TEAM_INFORMATION_BY_TEAM_ID` - 获取特定团队详情 [可选]
3. `CAL_CREATE_TEAM_IN_ORGANIZATION` - 创建新团队 [可选]
4. `CAL_RETRIEVE_TEAM_EVENT_TYPES` - 列出团队的事件类型 [可选]

**关键参数**：
- `teamId`：团队标识符
- `name`：团队名称（创建时）
- `slug`：URL 友好的团队标识符

**注意事项**：
- 创建团队可能需要组织级别权限
- 团队事件类型与个人事件类型是分开的
- 团队 slug 必须是 URL 安全的，且在组织内唯一

### 5. 组织管理

**适用场景**：用户想要查看组织详情

**工具调用顺序**：
1. `CAL_GET_ORGANIZATION_ID` - 获取组织 ID [必需]

**关键参数**：（无需参数）

**注意事项**：
- 创建团队和执行组织级操作需要组织 ID
- 并非所有 Cal.com 账户都有组织；个人计划可能返回错误

## 常用模式

### 预订创建流程

```
1. 调用 CAL_GET_AVAILABLE_SLOTS_INFO 查找可用时段
2. 向用户展示可用时间
3. 调用 CAL_POST_NEW_BOOKING_REQUEST 创建预订
4. 确认预订创建响应
```

### ID 解析

**团队名称 -> 团队 ID**：
```
1. 调用 CAL_GET_TEAMS_LIST
2. 在响应中按名称查找团队
3. 提取 id 字段
```

### Webhook 设置

```
1. 调用 CAL_RETRIEVE_WEBHOOKS_LIST 检查现有 webhook
2. 创建或更新 webhook，设置所需触发器
3. 通过测试预订验证 webhook 是否触发
```

## 已知注意事项

**日期/时间格式**：
- 预订时间：带时区的 ISO 8601（如 '2024-01-15T09:00:00Z'）
- 可用性日期：YYYY-MM-DD 格式
- 始终明确指定时区以避免混淆

**事件类型**：
- 事件类型 ID 是数字整数
- 事件类型定义时长、地点和预订规则
- 已禁用的事件类型无法接受新预订

**权限**：
- 团队操作需要团队成员身份或管理员权限
- 组织操作需要组织级别权限
- Webhook 管理需要相应的访问级别

**速率限制**：
- Cal.com API 对每个 API key 有速率限制
- 收到 429 响应时实现退避策略

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出预订 | CAL_FETCH_ALL_BOOKINGS | status, afterStart, beforeEnd |
| 创建预订 | CAL_POST_NEW_BOOKING_REQUEST | eventTypeId, start, end, name, email |
| 获取忙碌时间 | CAL_RETRIEVE_CALENDAR_BUSY_TIMES | dateFrom, dateTo |
| 获取可用时段 | CAL_GET_AVAILABLE_SLOTS_INFO | eventTypeId, dateFrom, dateTo |
| 列出 webhook | CAL_RETRIEVE_WEBHOOKS_LIST | (none) |
| 获取 webhook | CAL_GET_WEBHOOK_BY_ID | id |
| 更新 webhook | CAL_UPDATE_WEBHOOK_BY_ID | id, subscriberUrl, eventTriggers |
| 删除 webhook | CAL_DELETE_WEBHOOK_BY_ID | id |
| 列出团队 | CAL_GET_TEAMS_LIST | (none) |
| 获取团队 | CAL_GET_TEAM_INFORMATION_BY_TEAM_ID | teamId |
| 创建团队 | CAL_CREATE_TEAM_IN_ORGANIZATION | name, slug |
| 团队事件类型 | CAL_RETRIEVE_TEAM_EVENT_TYPES | teamId |
| 获取组织 ID | CAL_GET_ORGANIZATION_ID | (none) |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
