---
name: slack-automation
description: "通过 Composio 的 Slack 工具包自动化 Slack 工作区操作，包括消息发送、搜索、频道管理和表情回应工作流。触发词：Slack自动化、Slack消息、Slack频道、Slack搜索、Slack机器人、slack automation、slack message、slack channel"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Slack 自动化

通过 Composio 的 Slack 工具包自动化 Slack 工作区操作，包括消息发送、搜索、频道管理和表情回应工作流。

## 前置条件

- 必须连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并使用工具包 `slack` 建立活跃的 Slack 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `slack` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 Slack OAuth
4. 在运行任何工作流之前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 向频道发送消息

**使用时机**：用户想要向 Slack 频道或私信发送消息

**工具调用顺序**：
1. `SLACK_FIND_CHANNELS` - 将频道名称解析为频道 ID [前置条件]
2. `SLACK_LIST_ALL_CHANNELS` - 当 FIND_CHANNELS 返回空/模糊结果时的备选方案 [备选]
3. `SLACK_FIND_USERS` - 解析用户用于私信或 @提及 [可选]
4. `SLACK_OPEN_DM` - 如果直接给用户发消息，打开/复用私信频道 [可选]
5. `SLACK_SEND_MESSAGE` - 使用解析后的频道 ID 发送消息 [必需]
6. `SLACK_UPDATES_A_SLACK_MESSAGE` - 如需更正已发送的消息则编辑 [可选]

**关键参数**：
- `channel`：频道 ID 或名称（不带 '#' 前缀）
- `markdown_text`：格式化消息的首选字段（支持标题、粗体、斜体、代码块）
- `text`：原始文本备选（已弃用，推荐使用 markdown_text）
- `thread_ts`：父消息的时间戳，用于在话题中回复
- `blocks`：Block Kit 布局块（已弃用，使用 markdown_text）

**注意事项**：
- `SLACK_FIND_CHANNELS` 需要 `query` 参数；缺少会报错 "Invalid request data provided"
- `SLACK_SEND_MESSAGE` 需要有效的频道以及 markdown_text/text/blocks/attachments 之一
- 无效的 block 载荷返回 error=invalid_blocks（最多 50 个块）
- 如果省略 `thread_ts`，回复会变成顶级帖子
- 保存 SEND_MESSAGE 返回的 `response.data.channel` 和 `response.data.message.ts`，用于编辑/话题操作

### 2. 搜索消息和对话

**使用时机**：用户想要在工作区中查找特定消息

**工具调用顺序**：
1. `SLACK_FIND_CHANNELS` - 使用 `in:#channel` 解析频道用于范围搜索 [可选]
2. `SLACK_FIND_USERS` - 使用 `from:@user` 解析用户用于作者过滤 [可选]
3. `SLACK_SEARCH_MESSAGES` - 在可访问的对话中运行关键词搜索 [必需]
4. `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` - 展开相关结果的话题 [必需]

**关键参数**：
- `query`：搜索字符串，支持修饰符（`in:#channel`、`from:@user`、`before:YYYY-MM-DD`、`after:YYYY-MM-DD`、`has:link`、`has:file`）
- `count`：每页结果数（最多 100），或设置 auto_paginate=true 获取全部
- `sort`：'score'（相关性）或 'timestamp'（时间顺序）
- `sort_dir`：'asc' 或 'desc'

**注意事项**：
- 如果 `query` 缺失/为空，验证会失败
- `ok=true` 仍可能表示没有匹配（`response.data.messages.total=0`）
- 匹配结果在 `response.data.messages.matches` 下（有时也在 `response.data_preview.messages.matches`）
- `match.text` 可能为空/截断；关键信息可能出现在 `matches[].attachments[]` 中
- 通过 FETCH_MESSAGE_THREAD 展开话题时，当 `response.data.has_more=true` 可能截断；通过 `response_metadata.next_cursor` 分页

### 3. 管理频道和用户

**使用时机**：用户想要列出频道、用户或工作区信息

**工具调用顺序**：
1. `SLACK_FETCH_TEAM_INFO` - 验证连接并获取工作区身份 [必需]
2. `SLACK_LIST_ALL_CHANNELS` - 枚举公开频道 [必需]
3. `SLACK_LIST_CONVERSATIONS` - 包含私有频道和私信 [可选]
4. `SLACK_LIST_ALL_USERS` - 列出工作区成员 [必需]
5. `SLACK_RETRIEVE_CONVERSATION_INFORMATION` - 获取频道详细元数据 [可选]
6. `SLACK_LIST_USER_GROUPS_FOR_TEAM_WITH_OPTIONS` - 列出用户组 [可选]

**关键参数**：
- `cursor`：来自 `response_metadata.next_cursor` 的分页游标
- `limit`：每页结果数（默认值不定；大型工作区请显式设置）
- `types`：频道类型过滤器（'public_channel'、'private_channel'、'im'、'mpim'）

**注意事项**：
- 工作区元数据嵌套在 `response.data.team` 下，不是顶层
- `SLACK_LIST_ALL_CHANNELS` 仅返回公开频道；使用 `SLACK_LIST_CONVERSATIONS` 获取私有/私信频道
- `SLACK_LIST_ALL_USERS` 可能触发 HTTP 429 速率限制；遵守 Retry-After 响应头
- 始终通过 `response_metadata.next_cursor` 分页直到为空；按 `id` 去重

### 4. 回应和话题消息

**使用时机**：用户想要添加表情回应或管理话题对话

**工具调用顺序**：
1. `SLACK_SEARCH_MESSAGES` 或 `SLACK_FETCH_CONVERSATION_HISTORY` - 查找目标消息 [前置条件]
2. `SLACK_ADD_REACTION_TO_AN_ITEM` - 添加表情回应 [必需]
3. `SLACK_FETCH_ITEM_REACTIONS` - 列出消息上的回应 [可选]
4. `SLACK_REMOVE_REACTION_FROM_ITEM` - 移除回应 [可选]
5. `SLACK_SEND_MESSAGE` - 使用 `thread_ts` 在话题中回复 [可选]
6. `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` - 读取完整话题 [可选]

**关键参数**：
- `channel`：消息所在频道 ID
- `timestamp` / `ts`：消息时间戳（唯一标识符，如 '1234567890.123456'）
- `name`：表情名称，不带冒号（如 'thumbsup'、'wave::skin-tone-3'）
- `thread_ts`：父消息时间戳，用于话题回复

**注意事项**：
- 回应需要精确的频道 ID + 消息时间戳对
- 表情名称使用 Slack 命名规范，不带冒号
- `SLACK_FETCH_CONVERSATION_HISTORY` 仅返回主频道时间线，不包含话题回复
- 使用 `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` 配合父消息的 `thread_ts` 获取话题回复

### 5. 定时发送消息

**使用时机**：用户想要定时发送消息

**工具调用顺序**：
1. `SLACK_FIND_CHANNELS` - 解析频道 ID [前置条件]
2. `SLACK_SCHEDULE_MESSAGE` - 使用 `post_at` 时间戳定时发送消息 [必需]

**关键参数**：
- `channel`：已解析的频道 ID
- `post_at`：发送时间的 Unix 时间戳（最多提前 120 天）
- `text` / `blocks`：消息内容

**注意事项**：
- 定时发送最多提前 120 天
- `post_at` 必须是 Unix 时间戳，不是 ISO 8601

## 常用模式

### ID 解析
操作前始终将显示名称解析为 ID：
- **频道名称 -> 频道 ID**：使用 `query` 参数调用 `SLACK_FIND_CHANNELS`
- **用户名称 -> 用户 ID**：使用 `search_query` 或 `email` 调用 `SLACK_FIND_USERS`
- **私信频道**：使用已解析的用户 ID 调用 `SLACK_OPEN_DM`

### 分页
大多数列表端点使用基于游标的分页：
- 跟随 `response_metadata.next_cursor` 直到为空
- 设置显式 `limit` 值（如 100-200）以可靠分页
- 跨页按 `id` 去重结果

### 消息格式化
- 格式化消息优先使用 `markdown_text` 而非 `text` 或 `blocks`
- 使用 `<@USER_ID>` 格式提及用户（不是 @用户名）
- 在 markdown_text 中使用 `\n` 换行

## 已知注意事项

- **频道解析**：如果频道是私有的且机器人未被邀请，`SLACK_FIND_CHANNELS` 可能返回空结果
- **速率限制**：`SLACK_LIST_ALL_USERS` 和其他列表端点可能触发 HTTP 429；遵守 Retry-After 响应头
- **嵌套响应**：在包装执行中，结果可能嵌套在 `response.data.results[0].response.data` 下
- **话题与频道**：`SLACK_FETCH_CONVERSATION_HISTORY` 仅返回主时间线；使用 `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` 获取话题回复
- **消息编辑**：需要 `channel` 和原始消息 `ts` 两者；从 SEND_MESSAGE 响应中保存这些值
- **搜索延迟**：最近发送的消息可能不会立即出现在搜索结果中
- **权限范围限制**：缺少 OAuth 权限范围可能导致 403 错误；使用 `SLACK_GET_APP_PERMISSION_SCOPES` 检查

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 查找频道 | `SLACK_FIND_CHANNELS` | `query` |
| 列出所有频道 | `SLACK_LIST_ALL_CHANNELS` | `limit`、`cursor`、`types` |
| 发送消息 | `SLACK_SEND_MESSAGE` | `channel`、`markdown_text` |
| 编辑消息 | `SLACK_UPDATES_A_SLACK_MESSAGE` | `channel`、`ts`、`markdown_text` |
| 搜索消息 | `SLACK_SEARCH_MESSAGES` | `query`、`count`、`sort` |
| 获取话题 | `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` | `channel`、`ts` |
| 添加回应 | `SLACK_ADD_REACTION_TO_AN_ITEM` | `channel`、`name`、`timestamp` |
| 查找用户 | `SLACK_FIND_USERS` | `search_query` 或 `email` |
| 列出用户 | `SLACK_LIST_ALL_USERS` | `limit`、`cursor` |
| 打开私信 | `SLACK_OPEN_DM` | 用户 ID |
| 定时发送消息 | `SLACK_SCHEDULE_MESSAGE` | `channel`、`post_at`、`text` |
| 获取频道信息 | `SLACK_RETRIEVE_CONVERSATION_INFORMATION` | 频道 ID |
| 频道历史 | `SLACK_FETCH_CONVERSATION_HISTORY` | `channel`、`oldest`、`latest` |
| 工作区信息 | `SLACK_FETCH_TEAM_INFO` | （无） |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果所需的输入、权限、安全边界或成功标准缺失，请停下来请求澄清。
