---
name: microsoft-teams-automation
description: "通过 Rube MCP (Composio) 自动化 Microsoft Teams 任务：发送消息、管理频道、创建会议、处理聊天和搜索消息。始终先搜索工具获取最新 schema。当用户要求'自动化 Teams 操作'、'发送 Teams 消息'、'管理 Teams 频道'、'创建 Teams 会议'、'搜索 Teams 消息'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Microsoft Teams

通过 Composio 的 Microsoft Teams 工具包和 Rube MCP 自动化 Microsoft Teams 操作。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立有效的 Microsoft Teams 连接，toolkit 设为 `microsoft_teams`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 能正常响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `microsoft_teams`
3. 若连接状态非 ACTIVE，按返回的认证链接完成 Microsoft OAuth
4. 确认连接状态为 ACTIVE 后再执行任何工作流

## 核心工作流

### 1. 发送频道消息

**适用场景**：向 Teams 频道发送消息

**工具调用顺序**：
1. `MICROSOFT_TEAMS_TEAMS_LIST` - 列出团队以找到目标团队 [前置]
2. `MICROSOFT_TEAMS_TEAMS_LIST_CHANNELS` - 列出团队中的频道 [前置]
3. `MICROSOFT_TEAMS_TEAMS_POST_CHANNEL_MESSAGE` - 发送消息 [必需]

**关键参数**：
- `team_id`：团队 UUID（来自 TEAMS_LIST）
- `channel_id`：频道 ID（来自 LIST_CHANNELS，格式：'19:...@thread.tacv2'）
- `content`：消息文本或 HTML
- `content_type`：'text' 或 'html'

**注意事项**：
- team_id 必须为有效的 UUID 格式
- channel_id 必须为 thread 格式（如 '19:abc@thread.tacv2'）
- TEAMS_LIST 可能分页（约 100 项/页）；按 @odata.nextLink 获取全部团队
- LIST_CHANNELS 在用户无权访问团队时返回 403
- 消息超过约 28KB 可能触发 400/413 错误；需拆分长内容
- 限流可能返回 429；使用指数退避（1s/2s/4s）

### 2. 发送聊天消息

**适用场景**：发送一对一或群组聊天消息

**工具调用顺序**：
1. `MICROSOFT_TEAMS_CHATS_GET_ALL_CHATS` - 列出现有聊天 [可选]
2. `MICROSOFT_TEAMS_LIST_USERS` - 查找用户以创建新聊天 [可选]
3. `MICROSOFT_TEAMS_TEAMS_CREATE_CHAT` - 创建新聊天 [可选]
4. `MICROSOFT_TEAMS_TEAMS_POST_CHAT_MESSAGE` - 发送消息 [必需]

**关键参数**：
- `chat_id`：聊天 ID（来自 GET_ALL_CHATS 或 CREATE_CHAT）
- `content`：消息内容
- `content_type`：'text' 或 'html'
- `chatType`：'oneOnOne' 或 'group'（用于 CREATE_CHAT）
- `members`：成员对象数组（用于 CREATE_CHAT）

**注意事项**：
- CREATE_CHAT 要求已认证用户必须是成员之一
- 两个用户之间若已存在一对一聊天，oneOnOne 会返回已有聊天
- 群组聊天至少需要一个 'owner' 角色的成员
- 成员的 user_odata_bind 必须使用完整的 Microsoft Graph URL 格式
- 聊天筛选支持非常有限；需要时在客户端筛选

### 3. 创建在线会议

**适用场景**：安排 Microsoft Teams 会议

**工具调用顺序**：
1. `MICROSOFT_TEAMS_LIST_USERS` - 查找参与者用户 ID [可选]
2. `MICROSOFT_TEAMS_CREATE_MEETING` - 创建会议 [必需]

**关键参数**：
- `subject`：会议标题
- `start_date_time`：ISO 8601 开始时间（如 '2024-08-15T10:00:00Z'）
- `end_date_time`：ISO 8601 结束时间（必须晚于开始时间）
- `participants`：包含 user_id 和 role 的用户对象数组

**注意事项**：
- end_date_time 必须严格晚于 start_date_time
- 参与者需要有效的 Microsoft user_id（GUID），而非邮箱
- 创建的是独立会议，不关联日历事件
- 需要关联日历的会议，请使用 OUTLOOK_CALENDAR_CREATE_EVENT 并设 is_online_meeting=true

### 4. 管理团队和频道

**适用场景**：列出、创建或管理团队和频道

**工具调用顺序**：
1. `MICROSOFT_TEAMS_TEAMS_LIST` - 列出所有可访问的团队 [必需]
2. `MICROSOFT_TEAMS_GET_TEAM` - 获取特定团队详情 [可选]
3. `MICROSOFT_TEAMS_TEAMS_LIST_CHANNELS` - 列出团队中的频道 [可选]
4. `MICROSOFT_TEAMS_GET_CHANNEL` - 获取频道详情 [可选]
5. `MICROSOFT_TEAMS_TEAMS_CREATE_CHANNEL` - 创建新频道 [可选]
6. `MICROSOFT_TEAMS_LIST_TEAM_MEMBERS` - 列出团队成员 [可选]
7. `MICROSOFT_TEAMS_ADD_MEMBER_TO_TEAM` - 添加团队成员 [可选]

**关键参数**：
- `team_id`：团队 UUID
- `channel_id`：thread 格式的频道 ID
- `filter`：OData 筛选字符串（如 "startsWith(displayName,'Project')"）
- `select`：逗号分隔的返回属性

**注意事项**：
- TEAMS_LIST 分页：大型租户需按 @odata.nextLink 翻页
- 私有/共享频道在权限不匹配时可能被省略
- team_id 或 channel_id 错误时 GET_CHANNEL 返回 404
- 始终从列表操作获取 ID，不要猜测 ID 格式

### 5. 搜索消息

**适用场景**：在 Teams 聊天和频道中查找消息

**工具调用顺序**：
1. `MICROSOFT_TEAMS_SEARCH_MESSAGES` - 使用 KQL 语法搜索 [必需]

**关键参数**：
- `query`：KQL 搜索查询（支持 from:、sent:、attachments、布尔逻辑）

**注意事项**：
- 新发送的消息可能需要 30-60 秒才能出现在搜索结果中
- 搜索为最终一致性；不要依赖它确认即时送达
- 需要实时消息验证时，使用消息列表工具

## 常用模式

### 团队和频道 ID 解析

```
1. Call MICROSOFT_TEAMS_TEAMS_LIST
2. Find team by displayName
3. Extract team id (UUID format)
4. Call MICROSOFT_TEAMS_TEAMS_LIST_CHANNELS with team_id
5. Find channel by displayName
6. Extract channel id (19:...@thread.tacv2 format)
```

### 用户解析

```
1. Call MICROSOFT_TEAMS_LIST_USERS
2. Filter by displayName or email
3. Extract user id (UUID format)
4. Use for meeting participants, chat members, or team operations
```

### 分页

- Teams/Users：按 @odata.nextLink URL 获取下一页
- Chats：自动分页至 limit 上限；用 top 控制页大小（最大 50）
- 使用 `top` 参数控制页大小
- 持续翻页直到 @odata.nextLink 不再出现

## 已知注意事项

**认证与权限**：
- 不同操作需要不同的 Microsoft Graph 权限
- 403 错误表示权限不足或无团队访问权
- 部分操作需要 Azure AD 租户管理员同意

**ID 格式**：
- Team ID：UUID 格式（如 '87b0560f-fc0d-4442-add8-b380ca926707'）
- Channel ID：Thread 格式（如 '19:abc123@thread.tacv2'）
- Chat ID：多种格式（如 '19:meeting_xxx@thread.v2'）
- User ID：UUID 格式
- 禁止猜测 ID；始终从列表操作中解析

**速率限制**：
- Microsoft Graph 强制限流
- 429 响应包含 Retry-After 头
- 请求频率控制在每秒数次
- 批量操作有助于减少总请求数

**消息格式**：
- HTML content_type 支持富文本格式
- Adaptive Cards 需要额外处理
- 消息大小上限约 28KB
- 长内容需拆分为多条消息

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出团队 | MICROSOFT_TEAMS_TEAMS_LIST | filter, select, top |
| 获取团队详情 | MICROSOFT_TEAMS_GET_TEAM | team_id |
| 列出频道 | MICROSOFT_TEAMS_TEAMS_LIST_CHANNELS | team_id, filter |
| 获取频道 | MICROSOFT_TEAMS_GET_CHANNEL | team_id, channel_id |
| 创建频道 | MICROSOFT_TEAMS_TEAMS_CREATE_CHANNEL | team_id, displayName |
| 发送频道消息 | MICROSOFT_TEAMS_TEAMS_POST_CHANNEL_MESSAGE | team_id, channel_id, content |
| 列出聊天 | MICROSOFT_TEAMS_CHATS_GET_ALL_CHATS | user_id, limit |
| 创建聊天 | MICROSOFT_TEAMS_TEAMS_CREATE_CHAT | chatType, members, topic |
| 发送聊天消息 | MICROSOFT_TEAMS_TEAMS_POST_CHAT_MESSAGE | chat_id, content |
| 创建会议 | MICROSOFT_TEAMS_CREATE_MEETING | subject, start_date_time, end_date_time |
| 列出用户 | MICROSOFT_TEAMS_LIST_USERS | filter, select, top |
| 列出团队成员 | MICROSOFT_TEAMS_LIST_TEAM_MEMBERS | team_id |
| 添加团队成员 | MICROSOFT_TEAMS_ADD_MEMBER_TO_TEAM | team_id, user_id |
| 搜索消息 | MICROSOFT_TEAMS_SEARCH_MESSAGES | query |
| 获取聊天消息 | MICROSOFT_TEAMS_GET_CHAT_MESSAGE | chat_id, message_id |
| 列出已加入团队 | MICROSOFT_TEAMS_LIST_USER_JOINED_TEAMS | (无) |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 若缺少必要的输入、权限、安全边界或成功标准，应停止并请求澄清。
