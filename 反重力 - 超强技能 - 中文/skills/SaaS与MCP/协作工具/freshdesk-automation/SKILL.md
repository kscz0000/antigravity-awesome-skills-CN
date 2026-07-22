---
name: freshdesk-automation
description: "通过 Rube MCP (Composio) 自动化 Freshdesk 服务台操作，包括工单、联系人、公司、备注和回复。当用户要求'Freshdesk 自动化'、'工单管理'、'客服工单操作'、'Freshdesk API'时使用。始终先搜索工具以获取当前架构。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Freshdesk 自动化

通过 Composio 的 Freshdesk 工具包自动化 Freshdesk 客户支持工作流，包括工单管理、联系人和公司操作、备注、回复以及工单搜索。

## 前提条件

- 必须连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `freshdesk` 建立活跃的 Freshdesk 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具架构

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `freshdesk` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Freshdesk 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和管理工单

**何时使用**：用户想要创建新的支持工单、更新现有工单或查看工单详情。

**工具序列**：
1. `FRESHDESK_SEARCH_CONTACTS` - 通过邮箱查找请求者以获取 requester_id [可选]
2. `FRESHDESK_LIST_TICKET_FIELDS` - 检查可用的自定义字段和状态 [可选]
3. `FRESHDESK_CREATE_TICKET` - 创建包含主题、描述、请求者信息的新工单 [必需]
4. `FRESHDESK_UPDATE_TICKET` - 修改工单状态、优先级、负责人或其他字段 [可选]
5. `FRESHDESK_VIEW_TICKET` - 通过 ID 检索完整工单详情 [可选]

**FRESHDESK_CREATE_TICKET 的关键参数**：
- `subject`：工单主题（必需）
- `description`：工单的 HTML 内容（必需）
- `email`：请求者邮箱（至少需要一个请求者标识符）
- `requester_id`：请求者的用户 ID（邮箱的替代选项）
- `status`：2=Open, 3=Pending, 4=Resolved, 5=Closed（默认 2）
- `priority`：1=Low, 2=Medium, 3=High, 4=Urgent（默认 1）
- `source`：1=Email, 2=Portal, 3=Phone, 7=Chat（默认 2）
- `responder_id`：分配工单的客服 ID
- `group_id`：分配工单的组
- `tags`：标签字符串数组
- `custom_fields`：包含 `cf_<field_name>` 键的对象

**注意事项**：
- 至少需要一个请求者标识符：`requester_id`、`email`、`phone`、`facebook_id`、`twitter_id` 或 `unique_external_id`
- 如果提供了 `phone` 但未提供 `email`，则 `name` 变为必填
- `description` 支持 HTML 格式
- `attachments` 字段需要 multipart/form-data 格式，而非文件路径或 URL
- 自定义字段键必须以 `cf_` 为前缀（例如 `cf_reference_number`）
- 状态和优先级是整数，而非字符串

### 2. 搜索和筛选工单

**何时使用**：用户想要按状态、优先级、日期范围、客服或自定义字段查找工单。

**工具序列**：
1. `FRESHDESK_GET_TICKETS` - 使用简单筛选器列出工单（状态、优先级、客服）[必需]
2. `FRESHDESK_GET_SEARCH` - 使用查询语法进行高级工单搜索 [必需]
3. `FRESHDESK_VIEW_TICKET` - 从结果中获取特定工单的完整详情 [可选]
4. `FRESHDESK_LIST_TICKET_FIELDS` - 检查可用于搜索查询的字段 [可选]

**FRESHDESK_GET_TICKETS 的关键参数**：
- `status`：按状态整数筛选（2=Open, 3=Pending, 4=Resolved, 5=Closed）
- `priority`：按优先级整数筛选（1-4）
- `agent_id`：按分配的客服筛选
- `requester_id`：按请求者筛选
- `email`：按请求者邮箱筛选
- `created_since`：ISO 8601 时间戳
- `page` / `per_page`：分页（默认每页 30 条）
- `sort_by` / `sort_order`：排序字段和方向

**FRESHDESK_GET_SEARCH 的关键参数**：
- `query`：查询字符串，如 `"status:2 AND priority:3"` 或 `"(created_at:>'2024-01-01' AND tag:'urgent')"`
- `page`：页码（1-10，最多 300 条总结果）

**注意事项**：
- `FRESHDESK_GET_SEARCH` 查询必须用双引号括起
- 查询字符串限制为 512 个字符
- 搜索端点最多 10 页（300 条结果）
- 查询中的日期字段使用 UTC 格式 YYYY-MM-DD
- 使用 `null` 关键字查找字段为空的工单（例如 `"agent_id:null"`）
- `FRESHDESK_LIST_ALL_TICKETS` 不接受参数并返回所有工单（使用 GET_TICKETS 进行筛选）

### 3. 回复工单和添加备注

**何时使用**：用户想要向客户发送回复、添加内部备注或查看对话历史。

**工具序列**：
1. `FRESHDESK_VIEW_TICKET` - 验证工单存在并检查当前状态 [前置条件]
2. `FRESHDESK_REPLY_TO_TICKET` - 向请求者发送公开回复 [必需]
3. `FRESHDESK_ADD_NOTE_TO_TICKET` - 添加私有或公开备注 [必需]
4. `FRESHDESK_LIST_ALL_TICKET_CONVERSATIONS` - 查看工单上的所有消息和备注 [可选]
5. `FRESHDESK_UPDATE_CONVERSATIONS` - 编辑现有备注 [可选]

**FRESHDESK_REPLY_TO_TICKET 的关键参数**：
- `ticket_id`：工单 ID（整数，必需）
- `body`：回复内容，支持 HTML（必需）
- `cc_emails` / `bcc_emails`：额外收件人（to/cc/bcc 总共最多 50 人）
- `from_email`：如果配置了多个支持邮箱，覆盖发件人邮箱
- `user_id`：代表其回复的客服 ID

**FRESHDESK_ADD_NOTE_TO_TICKET 的关键参数**：
- `ticket_id`：工单 ID（整数，必需）
- `body`：备注内容，支持 HTML（必需）
- `private`：true 表示仅客服可见，false 表示公开（默认 true）
- `notify_emails`：仅接受客服邮箱地址，不接受外部联系人

**注意事项**：
- 有两个回复工具：`FRESHDESK_REPLY_TO_TICKET`（功能更多）和 `FRESHDESK_REPLY_TICKET`（更简单）；两者都可用
- `FRESHDESK_ADD_NOTE_TO_TICKET` 默认为私有（仅客服可见）；设置 `private: false` 为公开备注
- 备注中的 `notify_emails` 仅接受客服邮箱，不接受客户邮箱
- 只有备注可以通过 `FRESHDESK_UPDATE_CONVERSATIONS` 编辑；收到的回复无法编辑

### 4. 管理联系人和公司

**何时使用**：用户想要创建、搜索或管理客户联系人及公司记录。

**工具序列**：
1. `FRESHDESK_SEARCH_CONTACTS` - 通过邮箱、电话或公司搜索联系人 [必需]
2. `FRESHDESK_GET_CONTACTS` - 使用筛选器列出联系人 [可选]
3. `FRESHDESK_IMPORT_CONTACT` - 从 CSV 批量导入联系人 [可选]
4. `FRESHDESK_SEARCH_COMPANIES` - 通过自定义字段搜索公司 [必需]
5. `FRESHDESK_GET_COMPANIES` - 列出所有公司 [可选]
6. `FRESHDESK_CREATE_COMPANIES` - 创建新公司 [可选]
7. `FRESHDESK_UPDATE_COMPANIES` - 更新公司详情 [可选]
8. `FRESHDESK_LIST_COMPANY_FIELDS` - 检查可用的公司字段 [可选]

**FRESHDESK_SEARCH_CONTACTS 的关键参数**：
- `query`：搜索字符串，如 `"email:'user@example.com'"`（必需）
- `page`：分页（1-10，每页最多 30 条）

**FRESHDESK_CREATE_COMPANIES 的关键参数**：
- `name`：公司名称（必需）
- `domains`：域名字符串数组，用于与联系人自动关联
- `health_score`："Happy"、"Doing okay" 或 "At risk"
- `account_tier`："Basic"、"Premium" 或 "Enterprise"
- `industry`：标准行业分类

**注意事项**：
- `FRESHDESK_SEARCH_CONTACTS` 需要精确匹配；不支持部分/正则搜索
- `FRESHDESK_SEARCH_COMPANIES` 无法通过标准 `name` 字段搜索；使用自定义字段或 `created_at`
- 公司自定义字段不使用 `cf_` 前缀（与工单自定义字段不同）
- 公司上的 `domains` 可通过邮箱域名实现联系人与公司的自动关联
- 联系人搜索查询需要在双引号括起的查询内用单引号括起字符串值

## 常见模式

### ID 解析
在操作前始终将显示值解析为 ID：
- **请求者邮箱 -> requester_id**：使用 `"email:'user@example.com'"` 调用 `FRESHDESK_SEARCH_CONTACTS`
- **公司名称 -> company_id**：调用 `FRESHDESK_GET_COMPANIES` 并按名称匹配（不支持按名称搜索）
- **客服姓名 -> agent_id**：不直接可用；使用工单响应中的 agent_id 或管理员配置

### 分页
Freshdesk 使用基于页码的分页：
- `FRESHDESK_GET_TICKETS`：`page`（从 1 开始）和 `per_page`（最多 100）
- `FRESHDESK_GET_SEARCH`：`page`（1-10，每页 30 条结果，最多 300 条总计）
- `FRESHDESK_SEARCH_CONTACTS`：`page`（1-10，每页 30 条）
- `FRESHDESK_LIST_ALL_TICKET_CONVERSATIONS`：`page` 和 `per_page`（最多 100）

## 已知注意事项

### ID 格式
- 工单 ID、联系人 ID、公司 ID、客服 ID 和组 ID 都是整数
- Freshdesk 中没有基于字符串的 ID

### 速率限制
- Freshdesk 根据套餐等级对每个账户强制执行 API 速率限制
- 批量操作应控制节奏以避免 429 响应
- 搜索端点限制为总共 300 条结果（10 页，每页 30 条）

### 参数特性
- 状态值：2=Open, 3=Pending, 4=Resolved, 5=Closed（整数，非字符串）
- 优先级值：1=Low, 2=Medium, 3=High, 4=Urgent（整数，非字符串）
- 来源值：1=Email, 2=Portal, 3=Phone, 7=Chat, 9=Feedback Widget, 10=Outbound Email
- 工单自定义字段使用 `cf_` 前缀；公司自定义字段不使用
- 工单中的 `description` 支持 HTML 格式
- 搜索查询字符串必须用双引号括起，字符串值用单引号括起
- `FRESHDESK_LIST_ALL_TICKETS` 返回所有工单，无筛选参数

### 响应结构
- 工单详情包含请求者、负责人和对话数据的嵌套对象
- 搜索结果分页，最多 300 条结果分布在 10 页中
- 对话列表按时间顺序包含回复和备注

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 创建工单 | `FRESHDESK_CREATE_TICKET` | `subject`, `description`, `email`, `priority` |
| 更新工单 | `FRESHDESK_UPDATE_TICKET` | `ticket_id`, `status`, `priority` |
| 查看工单 | `FRESHDESK_VIEW_TICKET` | `ticket_id` |
| 列出工单 | `FRESHDESK_GET_TICKETS` | `status`, `priority`, `page`, `per_page` |
| 列出所有工单 | `FRESHDESK_LIST_ALL_TICKETS` | (无) |
| 搜索工单 | `FRESHDESK_GET_SEARCH` | `query`, `page` |
| 回复工单 | `FRESHDESK_REPLY_TO_TICKET` | `ticket_id`, `body`, `cc_emails` |
| 回复（简单） | `FRESHDESK_REPLY_TICKET` | `ticket_id`, `body` |
| 添加备注 | `FRESHDESK_ADD_NOTE_TO_TICKET` | `ticket_id`, `body`, `private` |
| 列出对话 | `FRESHDESK_LIST_ALL_TICKET_CONVERSATIONS` | `ticket_id`, `page` |
| 更新备注 | `FRESHDESK_UPDATE_CONVERSATIONS` | `conversation_id`, `body` |
| 搜索联系人 | `FRESHDESK_SEARCH_CONTACTS` | `query`, `page` |
| 列出联系人 | `FRESHDESK_GET_CONTACTS` | `email`, `company_id`, `page` |
| 导入联系人 | `FRESHDESK_IMPORT_CONTACT` | `file`, `name_column_index`, `email_column_index` |
| 创建公司 | `FRESHDESK_CREATE_COMPANIES` | `name`, `domains`, `industry` |
| 更新公司 | `FRESHDESK_UPDATE_COMPANIES` | `company_id`, `name`, `domains` |
| 搜索公司 | `FRESHDESK_SEARCH_COMPANIES` | `query`, `page` |
| 列出公司 | `FRESHDESK_GET_COMPANIES` | `page` |
| 列出工单字段 | `FRESHDESK_LIST_TICKET_FIELDS` | (无) |
| 列出公司字段 | `FRESHDESK_LIST_COMPANY_FIELDS` | (无) |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
