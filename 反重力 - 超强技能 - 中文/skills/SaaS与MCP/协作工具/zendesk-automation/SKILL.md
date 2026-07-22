---
name: zendesk-automation
description: "通过 Rube MCP（Composio）自动化 Zendesk 任务：工单、用户、组织、回复。始终先搜索工具以获取最新的 schema。触发词：Zendesk 自动化、工单管理、Zendesk 集成、Zendesk MCP、Rube MCP、客服支持、用户管理、组织管理"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Zendesk 自动化

通过 Rube MCP，使用 Composio 的 Zendesk 工具集自动化 Zendesk 操作。

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具集 `zendesk` 保持 Zendesk 活动连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取最新的工具 schema

## 配置

**获取 Rube MCP**：在你的客户端配置中，将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具集 `zendesk` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是 ACTIVE 状态，请按照返回的授权链接完成 Zendesk 认证
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出与搜索工单

**使用场景**：用户希望查看、筛选或搜索支持工单

**工具调用顺序**：
1. `ZENDESK_LIST_ZENDESK_TICKETS` - 分页列出所有工单 [必需]
2. `ZENDESK_GET_ZENDESK_TICKET_BY_ID` - 获取指定工单详情 [可选]

**关键参数**：
- `page`：页码（从 1 开始）
- `per_page`：每页结果数（最多 100）
- `sort_by`：排序字段（'created_at'、'updated_at'、'priority'、'status'）
- `sort_order`：'asc' 或 'desc'
- `ticket_id`：用于获取单个工单的工单 ID

**注意事项**：
- LIST 使用 `page`/`per_page` 分页，而非基于 offset 的分页；请检查响应中的 `next_page`
- 每页最多 100 条结果；使用页码迭代直到 `next_page` 为 null
- LIST 不会返回已删除的工单；使用 GET_BY_ID 时会返回状态 'deleted'
- 工单的评论和审计日志包含在 GET_BY_ID 中，但不在 LIST 响应中

### 2. 创建与更新工单

**使用场景**：用户希望创建新工单或修改现有工单

**工具调用顺序**：
1. `ZENDESK_SEARCH_ZENDESK_USERS` - 查找请求者/受理人 [前置]
2. `ZENDESK_CREATE_ZENDESK_TICKET` - 创建新工单 [必需]
3. `ZENDESK_UPDATE_ZENDESK_TICKET` - 更新工单字段 [可选]
4. `ZENDESK_DELETE_ZENDESK_TICKET` - 删除工单 [可选]

**关键参数**：
- `subject`：工单主题
- `description`：工单正文（用于创建；将成为第一条评论）
- `priority`：'urgent'、'high'、'normal'、'low'
- `status`：'new'、'open'、'pending'、'hold'、'solved'、'closed'
- `type`：'problem'、'incident'、'question'、'task'
- `assignee_id`：要分配的客服用户 ID
- `requester_id`：请求者用户 ID
- `tags`：标签字符串数组
- `ticket_id`：工单 ID（用于更新/删除）

**注意事项**：
- UPDATE 上的 tags 会完全替换现有 tags；需与当前 tags 合并以保留旧标签
- 使用带 `updated_stamp` 的 `safe_update` 以防止并发修改冲突
- DELETE 是永久性的且不可逆；工单无法恢复
- `description` 仅在创建时使用；创建后请使用 `REPLY_ZENDESK_TICKET` 添加评论
- 已关闭的工单无法更新；请改用创建后续工单

### 3. 回复工单

**使用场景**：用户希望向工单添加评论或回复

**工具调用顺序**：
1. `ZENDESK_GET_ZENDESK_TICKET_BY_ID` - 获取当前工单状态 [前置]
2. `ZENDESK_REPLY_ZENDESK_TICKET` - 添加回复/评论 [必需]

**关键参数**：
- `ticket_id`：要回复的工单 ID
- `body`：回复文本内容
- `public`：布尔值；true 表示公开回复，false 表示内部备注
- `author_id`：作者用户 ID（默认为已认证用户）

**注意事项**：
- 对仅客服可见的内部备注，设置 `public: false`
- 默认为公开回复，会向请求者发送邮件
- 正文中支持 HTML
- 回复时也可以同时更新工单状态

### 4. 管理用户

**使用场景**：用户希望查找或创建 Zendesk 用户（客服、终端用户）

**工具调用顺序**：
1. `ZENDESK_SEARCH_ZENDESK_USERS` - 搜索用户 [必需]
2. `ZENDESK_CREATE_ZENDESK_USER` - 创建新用户 [可选]
3. `ZENDESK_GET_ABOUT_ME` - 获取已认证用户信息 [可选]

**关键参数**：
- `query`：搜索字符串（匹配姓名、邮箱、电话等）
- `name`：用户全名（创建时必需）
- `email`：用户邮箱
- `role`：'end-user'、'agent' 或 'admin'
- `verified`：邮箱是否已验证

**注意事项**：
- 用户搜索是模糊匹配；可能返回部分匹配结果
- 使用已存在邮箱创建用户将返回该现有用户（upsert 行为）
- agent 和 admin 角色可能需要特定套餐功能

### 5. 管理组织

**使用场景**：用户希望列出、创建或管理组织

**工具调用顺序**：
1. `ZENDESK_GET_ALL_ZENDESK_ORGANIZATIONS` - 列出所有组织 [必需]
2. `ZENDESK_GET_ZENDESK_ORGANIZATION` - 获取指定组织 [可选]
3. `ZENDESK_CREATE_ZENDESK_ORGANIZATION` - 创建组织 [可选]
4. `ZENDESK_UPDATE_ZENDESK_ORGANIZATION` - 更新组织 [可选]
5. `ZENDESK_COUNT_ZENDESK_ORGANIZATIONS` - 获取总数 [可选]

**关键参数**：
- `name`：组织名称（唯一，创建时必需）
- `organization_id`：用于获取/更新的组织 ID
- `details`：组织详情文本
- `notes`：内部备注
- `domain_names`：关联域名数组
- `tags`：标签字符串数组

**注意事项**：
- 组织名称必须唯一；重名会导致创建错误
- UPDATE 上的 tags 会替换现有 tags（与工单行为相同）
- 域名可用于自动关联用户

## 常用模式

### 分页

**列表端点**：
- 使用 `page`（从 1 开始）和 `per_page`（最多 100）
- 检查响应中的 `next_page` URL；为 null 表示最后一页
- `count` 字段给出总结果数

### 工单生命周期

```
new -> open -> pending -> solved -> closed
                  |          ^
                  v          |
                hold --------+
```

- `new`：未分配的工单
- `open`：已分配，正在处理
- `pending`：等待客户回复
- `hold`：等待内部操作
- `solved`：已解决，可以重新打开
- `closed`：永久关闭，无法修改

### 用于分配的用户搜索

```
1. 使用 query（姓名或邮箱）调用 ZENDESK_SEARCH_ZENDESK_USERS
2. 从结果中提取用户 ID
3. 在创建/更新工单时将用户 ID 用作 assignee_id
```

## 已知陷阱

**Tags 行为**：
- 更新时的 tags 会替换所有现有 tags
- 始终先获取当前 tags 并在更新前进行合并
- tags 应为小写、无空格（使用下划线）

**安全更新**：
- 使用 `safe_update: true` 配合 `updated_stamp`（ISO 8601）防止冲突
- 如果工单自该时间戳后被修改，将返回 409

**删除**：
- 工单删除是永久性的且不可逆
- 建议将状态设置为 'closed' 而非删除
- 已删除的工单无法通过 API 恢复

**速率限制**：
- 默认：每分钟 400 次请求
- 随套餐等级而变化
- 429 响应包含 Retry-After 头

## 快速参考

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| 列出工单 | ZENDESK_LIST_ZENDESK_TICKETS | page, per_page, sort_by |
| 获取工单 | ZENDESK_GET_ZENDESK_TICKET_BY_ID | ticket_id |
| 创建工单 | ZENDESK_CREATE_ZENDESK_TICKET | subject, description, priority |
| 更新工单 | ZENDESK_UPDATE_ZENDESK_TICKET | ticket_id, status, tags |
| 回复工单 | ZENDESK_REPLY_ZENDESK_TICKET | ticket_id, body, public |
| 删除工单 | ZENDESK_DELETE_ZENDESK_TICKET | ticket_id |
| 搜索用户 | ZENDESK_SEARCH_ZENDESK_USERS | query |
| 创建用户 | ZENDESK_CREATE_ZENDESK_USER | name, email |
| 我的资料 | ZENDESK_GET_ABOUT_ME | (none) |
| 列出组织 | ZENDESK_GET_ALL_ZENDESK_ORGANIZATIONS | page, per_page |
| 获取组织 | ZENDESK_GET_ZENDESK_ORGANIZATION | organization_id |
| 创建组织 | ZENDESK_CREATE_ZENDESK_ORGANIZATION | name |
| 更新组织 | ZENDESK_UPDATE_ZENDESK_ORGANIZATION | organization_id, name |
| 统计组织 | ZENDESK_COUNT_ZENDESK_ORGANIZATIONS | (none) |

## 何时使用
本技能适用于执行上述概览中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 请勿将输出视为针对特定环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下并请求澄清。
