---
name: freshservice-automation
description: "通过 Rube MCP (Composio) 自动化 Freshservice ITSM 任务：创建/更新工单、批量操作、服务请求和外发邮件。始终先搜索工具以获取当前 schema。当用户要求'Freshservice 自动化'、'工单管理'、'ITSM 操作'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Freshservice 自动化

通过 Rube MCP 使用 Composio 的 Freshservice 工具包自动化 Freshservice IT 服务管理操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 激活 Freshservice 连接（toolkit 为 `freshservice`）
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用 toolkit `freshservice` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Freshservice 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出和搜索工单

**适用场景**：用户想要查找、列出或搜索工单

**工具调用顺序**：
1. `FRESHSERVICE_LIST_TICKETS` - 列出工单（支持过滤和分页）[必需]
2. `FRESHSERVICE_GET_TICKET` - 获取特定工单的详细信息 [可选]

**列出工单的关键参数**：
- `filter`：预定义过滤器（'all_tickets'、'deleted'、'spam'、'watching'）
- `updated_since`：ISO 8601 时间戳，获取此时间之后更新的工单
- `order_by`：排序字段（'created_at'、'updated_at'、'status'、'priority'）
- `order_type`：排序方向（'asc' 或 'desc'）
- `page`：页码（从 1 开始）
- `per_page`：每页结果数（1-100，默认 30）
- `include`：附加字段（'requester'、'stats'、'description'、'conversations'、'assets'）

**获取工单的关键参数**：
- `ticket_id`：唯一工单 ID 或 display_id
- `include`：要包含的附加字段

**注意事项**：
- 默认只返回过去 30 天内创建的工单
- 使用 `updated_since` 获取更早的工单
- 每个 `include` 值会消耗额外的 API 配额
- `page` 从 1 开始计数；最小值为 1
- `per_page` 最大值为 100；默认为 30
- 工单 ID 可以是内部 ID 或 UI 中显示的 display_id

### 2. 创建工单

**适用场景**：用户想要记录新的事件或请求

**工具调用顺序**：
1. `FRESHSERVICE_CREATE_TICKET` - 创建新工单 [必需]

**关键参数**：
- `subject`：工单标题（必需）
- `description`：工单的 HTML 描述（必需）
- `status`：工单状态 - 2（Open/开启）、3（Pending/待处理）、4（Resolved/已解决）、5（Closed/已关闭）（必需）
- `priority`：工单优先级 - 1（Low/低）、2（Medium/中）、3（High/高）、4（Urgent/紧急）（必需）
- `email`：请求者的邮箱地址（提供 email 或 requester_id 之一）
- `requester_id`：请求者的用户 ID
- `type`：工单类型（'Incident' 或 'Service Request'）
- `source`：渠道 - 1（Email）、2（Portal）、3（Phone）、4（Chat）、5（Twitter）、6（Facebook）
- `impact`：影响级别 - 1（Low/低）、2（Medium/中）、3（High/高）
- `urgency`：紧急程度 - 1（Low/低）、2（Medium/中）、3（High/高）、4（Critical/严重）

**注意事项**：
- `subject`、`description`、`status` 和 `priority` 都是必需的
- 必须提供 `email` 或 `requester_id` 之一来标识请求者
- 状态和优先级使用数字代码，而非字符串名称
- 描述支持 HTML 格式
- 如果邮箱不匹配现有联系人，会创建新联系人

### 3. 批量更新工单

**适用场景**：用户想要一次更新多个工单

**工具调用顺序**：
1. `FRESHSERVICE_LIST_TICKETS` - 查找要更新的工单 [前置步骤]
2. `FRESHSERVICE_BULK_UPDATE_TICKETS` - 批量更新工单 [必需]

**关键参数**：
- `ids`：要更新的工单 ID 数组（必需）
- `update_fields`：要更新的字段字典（必需）
  - 允许的键：'subject'、'description'、'status'、'priority'、'responder_id'、'group_id'、'type'、'tags'、'custom_fields'

**注意事项**：
- 批量更新内部执行顺序更新；大批量可能需要时间
- 所有指定工单接收相同的字段更新
- 如果一个工单更新失败，其他可能仍然成功；检查响应中的个别结果
- 无法在单次调用中选择性地为不同工单更新不同字段
- 自定义字段必须使用其内部字段名，而非显示名称

### 4. 通过外发邮件创建工单

**适用场景**：用户想要通过发送外发邮件通知来创建工单

**工具调用顺序**：
1. `FRESHSERVICE_CREATE_TICKET_OUTBOUND_EMAIL` - 创建工单并发送邮件通知 [必需]

**关键参数**：
- `email`：请求者的邮箱地址（必需）
- `subject`：邮件主题 / 工单标题（必需）
- `description`：HTML 邮件正文内容
- `status`：工单状态（2=Open、3=Pending、4=Resolved、5=Closed）
- `priority`：工单优先级（1=Low、2=Medium、3=High、4=Urgent）
- `cc_emails`：抄送邮箱地址数组
- `email_config_id`：发件人地址的邮件配置 ID
- `name`：请求者姓名

**注意事项**：
- 这会通过 /api/v2/tickets 端点创建标准工单，同时发送邮件
- 如果邮箱不匹配现有联系人，会使用提供的姓名创建新联系人
- `email_config_id` 决定通知显示来自哪个邮箱地址

### 5. 创建服务请求

**适用场景**：用户想要提交服务目录请求

**工具调用顺序**：
1. `FRESHSERVICE_CREATE_SERVICE_REQUEST` - 为目录项创建服务请求 [必需]

**关键参数**：
- `item_display_id`：目录项的 Display ID（必需）
- `email`：请求者的邮箱地址
- `quantity`：请求的项目数量（默认：1）
- `custom_fields`：服务项表单的自定义字段值
- `parent_ticket_id`：父工单的 Display ID（用于子请求）

**注意事项**：
- `item_display_id` 可在 Admin > Service Catalog > 项目 URL 中找到（例如 /service_catalog/items/1）
- 自定义字段的键必须与服务项表单字段名匹配
- 如果未指定，数量默认为 1
- 服务请求遵循为目录项定义的审批工作流

## 常用模式

### 状态码参考

| 代码 | 状态 |
|------|------|
| 2 | Open（开启） |
| 3 | Pending（待处理） |
| 4 | Resolved（已解决） |
| 5 | Closed（已关闭） |

### 优先级代码参考

| 代码 | 优先级 |
|------|--------|
| 1 | Low（低） |
| 2 | Medium（中） |
| 3 | High（高） |
| 4 | Urgent（紧急） |

### 分页

- 使用 `page`（从 1 开始）和 `per_page`（最大 100）参数
- 每次请求将 `page` 加 1
- 持续直到返回结果数 < `per_page`
- 默认页面大小为 30

### 按日期范围查找工单

```
1. 调用 FRESHSERVICE_LIST_TICKETS，参数 updated_since='2024-01-01T00:00:00Z'
2. 可选添加 order_by='updated_at' 和 order_type='desc'
3. 分页遍历结果
```

## 已知注意事项

**数字代码**：
- 状态和优先级使用数字值，而非字符串
- 来源渠道使用数字代码（1-6）
- 影响和紧急程度使用数字代码（1-3 或 1-4）

**日期过滤**：
- 默认只返回过去 30 天的工单
- 使用 `updated_since` 参数获取更早的工单
- 日期格式为 ISO 8601（例如 '2024-01-01T00:00:00Z'）

**速率限制**：
- Freshservice API 有按账户的速率限制
- 每个 `include` 选项消耗额外的 API 配额
- 遇到 429 响应时实现退避策略

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 使用回退模式进行防御性解析
- 工单 ID 是数字整数

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 列出工单 | FRESHSERVICE_LIST_TICKETS | filter, updated_since, page, per_page |
| 获取工单 | FRESHSERVICE_GET_TICKET | ticket_id, include |
| 创建工单 | FRESHSERVICE_CREATE_TICKET | subject, description, status, priority, email |
| 批量更新 | FRESHSERVICE_BULK_UPDATE_TICKETS | ids, update_fields |
| 外发邮件工单 | FRESHSERVICE_CREATE_TICKET_OUTBOUND_EMAIL | email, subject, description |
| 服务请求 | FRESHSERVICE_CREATE_SERVICE_REQUEST | item_display_id, email, quantity |

## 使用时机
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
