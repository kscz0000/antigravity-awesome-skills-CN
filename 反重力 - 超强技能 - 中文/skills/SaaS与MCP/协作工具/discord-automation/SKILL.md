---
name: discord-automation
description: "通过 Rube MCP (Composio) 自动化 Discord 任务：消息、频道、角色、webhook、反应。始终先搜索工具以获取当前 schema。当用户要求自动化 Discord 任务、发送消息、管理频道、角色、webhook 或反应时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Discord 自动化

通过 Composio 的 Discord/Discordbot 工具包，经由 Rube MCP 自动化 Discord 操作。

## 前置条件

- 必须连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 连接 Discord，使用 `discord` 和 `discordbot` 工具包
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `discordbot`（机器人操作）或 `discord`（用户操作）调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Discord 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 发送消息

**何时使用**：用户想要向频道或私信发送消息

**工具序列**：
1. `DISCORD_LIST_MY_GUILDS` - 列出机器人所属的服务器 [前置条件]
2. `DISCORDBOT_LIST_GUILD_CHANNELS` - 列出服务器中的频道 [前置条件]
3. `DISCORDBOT_CREATE_MESSAGE` - 发送消息 [必需]
4. `DISCORDBOT_UPDATE_MESSAGE` - 编辑已发送的消息 [可选]

**关键参数**：
- `channel_id`：频道 snowflake ID
- `content`：消息文本（最多 2000 个字符）
- `embeds`：富文本内容的 embed 对象数组
- `guild_id`：用于列出频道的服务器 ID

**注意事项**：
- 机器人必须在该频道拥有 SEND_MESSAGES 权限
- 高频发送可能触发按路由的速率限制；请遵守 Retry-After 响应头
- 只能编辑同一机器人发送的消息

### 2. 发送私信

**何时使用**：用户想要私信 Discord 用户

**工具序列**：
1. `DISCORDBOT_CREATE_DM` - 创建或获取私信频道 [必需]
2. `DISCORDBOT_CREATE_MESSAGE` - 向私信频道发送消息 [必需]

**关键参数**：
- `recipient_id`：私信用户的 snowflake ID
- `channel_id`：CREATE_DM 返回的私信频道 ID

**注意事项**：
- 无法私信已关闭私信或已屏蔽机器人的用户
- 如果私信频道已存在，CREATE_DM 会返回现有频道

### 3. 管理角色

**何时使用**：用户想要创建、分配或移除角色

**工具序列**：
1. `DISCORDBOT_CREATE_GUILD_ROLE` - 创建新角色 [可选]
2. `DISCORDBOT_ADD_GUILD_MEMBER_ROLE` - 为成员分配角色 [可选]
3. `DISCORDBOT_DELETE_GUILD_ROLE` - 删除角色 [可选]
4. `DISCORDBOT_GET_GUILD_MEMBER` - 获取成员详情 [可选]
5. `DISCORDBOT_UPDATE_GUILD_MEMBER` - 更新成员（角色、昵称等）[可选]

**关键参数**：
- `guild_id`：服务器 snowflake ID
- `user_id`：用户 snowflake ID
- `role_id`：角色 snowflake ID
- `name`：角色名称
- `permissions`：位运算权限值
- `color`：RGB 颜色整数值

**注意事项**：
- 角色分配需要 MANAGE_ROLES 权限
- 目标角色必须在层级上低于机器人的最高角色
- DELETE 会永久移除所有成员的该角色

### 4. 管理 Webhook

**何时使用**：用户想要创建或使用 webhook 进行外部集成

**工具序列**：
1. `DISCORDBOT_GET_GUILD_WEBHOOKS` / `DISCORDBOT_LIST_CHANNEL_WEBHOOKS` - 列出 webhook [可选]
2. `DISCORDBOT_CREATE_WEBHOOK` - 创建新 webhook [可选]
3. `DISCORDBOT_EXECUTE_WEBHOOK` - 通过 webhook 发送消息 [可选]
4. `DISCORDBOT_UPDATE_WEBHOOK` - 更新 webhook 设置 [可选]

**关键参数**：
- `webhook_id`：Webhook ID
- `webhook_token`：Webhook 密钥令牌
- `channel_id`：创建 webhook 的频道
- `name`：Webhook 名称
- `content`/`embeds`：执行时的消息内容

**注意事项**：
- Webhook 令牌是机密；请安全处理
- Webhook 可以在每条消息中使用自定义用户名和头像发布
- 创建需要 MANAGE_WEBHOOKS 权限

### 5. 管理反应

**何时使用**：用户想要查看或管理消息反应

**工具序列**：
1. `DISCORDBOT_LIST_MESSAGE_REACTIONS_BY_EMOJI` - 列出已反应的用户 [可选]
2. `DISCORDBOT_DELETE_ALL_MESSAGE_REACTIONS` - 移除所有反应 [可选]
3. `DISCORDBOT_DELETE_ALL_MESSAGE_REACTIONS_BY_EMOJI` - 移除特定表情反应 [可选]
4. `DISCORDBOT_DELETE_USER_MESSAGE_REACTION` - 移除特定用户的反应 [可选]

**关键参数**：
- `channel_id`：频道 ID
- `message_id`：消息 snowflake ID
- `emoji_name`：URL 编码的表情或自定义表情的 `name:id` 格式
- `user_id`：用于移除特定反应的用户 ID

**注意事项**：
- Unicode 表情必须进行 URL 编码（例如 '%F0%9F%91%8D' 表示点赞）
- 自定义表情使用 `name:id` 格式
- DELETE_ALL 需要 MANAGE_MESSAGES 权限

## 常见模式

### Snowflake ID

Discord 对所有实体使用 snowflake ID（以字符串表示的 64 位整数）：
- 服务器、频道、用户、角色、消息、webhook

### 权限位字段

权限使用位运算 OR 组合：
- SEND_MESSAGES = 0x800
- MANAGE_ROLES = 0x10000000
- MANAGE_MESSAGES = 0x2000
- ADMINISTRATOR = 0x8

### 分页

- 大多数列表端点支持 `limit`、`before`、`after` 参数
- 消息：每次请求最多 100 条
- 反应：每次请求最多 100 条，使用 `after` 进行分页

## 已知注意事项

**机器人令牌 vs 用户令牌**：
- `discordbot` 工具包使用机器人令牌；`discord` 使用用户 OAuth
- 自动化操作首选机器人操作

**速率限制**：
- Discord 强制执行按路由的速率限制
- 在 429 响应时遵守 `Retry-After` 响应头

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出服务器 | DISCORD_LIST_MY_GUILDS | (无) |
| 列出频道 | DISCORDBOT_LIST_GUILD_CHANNELS | guild_id |
| 发送消息 | DISCORDBOT_CREATE_MESSAGE | channel_id, content |
| 编辑消息 | DISCORDBOT_UPDATE_MESSAGE | channel_id, message_id |
| 获取消息 | DISCORDBOT_LIST_MESSAGES | channel_id, limit |
| 创建私信 | DISCORDBOT_CREATE_DM | recipient_id |
| 创建角色 | DISCORDBOT_CREATE_GUILD_ROLE | guild_id, name |
| 分配角色 | DISCORDBOT_ADD_GUILD_MEMBER_ROLE | guild_id, user_id, role_id |
| 删除角色 | DISCORDBOT_DELETE_GUILD_ROLE | guild_id, role_id |
| 获取成员 | DISCORDBOT_GET_GUILD_MEMBER | guild_id, user_id |
| 更新成员 | DISCORDBOT_UPDATE_GUILD_MEMBER | guild_id, user_id |
| 获取服务器 | DISCORDBOT_GET_GUILD | guild_id |
| 创建 webhook | DISCORDBOT_CREATE_WEBHOOK | channel_id, name |
| 执行 webhook | DISCORDBOT_EXECUTE_WEBHOOK | webhook_id, webhook_token |
| 列出 webhook | DISCORDBOT_GET_GUILD_WEBHOOKS | guild_id |
| 获取反应 | DISCORDBOT_LIST_MESSAGE_REACTIONS_BY_EMOJI | channel_id, message_id, emoji_name |
| 清除反应 | DISCORDBOT_DELETE_ALL_MESSAGE_REACTIONS | channel_id, message_id |
| 测试认证 | DISCORDBOT_TEST_AUTH | (无) |
| 获取频道 | DISCORDBOT_GET_CHANNEL | channel_id |

## 何时使用
当用户要求自动化 Discord 任务、发送消息、管理频道、角色、webhook 或反应时使用此技能。

## 限制
- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
