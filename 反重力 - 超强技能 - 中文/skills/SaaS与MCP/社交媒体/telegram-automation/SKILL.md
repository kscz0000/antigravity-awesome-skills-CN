---
name: telegram-automation
description: "通过 Rube MCP（Composio）自动化 Telegram 任务：发送消息、管理聊天、分享图片/文档、处理机器人命令。始终先搜索工具以获取当前 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Telegram 自动化

通过 Rube MCP 调用 Composio 的 Telegram 工具包，自动化 Telegram 操作。

## 前置条件

- Rube MCP 已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `telegram` 工具包建立活跃的 Telegram 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema
- 需要 Telegram Bot Token（通过 @BotFather 创建）

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 响应以验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包选择 `telegram`
3. 如果连接状态不是 ACTIVE，按返回的授权链接配置 Telegram 机器人
4. 运行任何工作流前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 发送消息

**适用场景**：用户想向 Telegram 聊天发送文本消息

**工具调用顺序**：
1. `TELEGRAM_GET_ME` - 验证机器人身份和连接 [前置条件]
2. `TELEGRAM_GET_CHAT` - 获取聊天详情并验证访问权限 [可选]
3. `TELEGRAM_SEND_MESSAGE` - 发送文本消息 [必需]

**关键参数**：
- `chat_id`：数字聊天 ID 或频道用户名（如 '@channelname'）
- `text`：消息文本内容
- `parse_mode`：'HTML' 或 'MarkdownV2' 用于格式化
- `disable_notification`：静默发送，不发出通知声音
- `reply_to_message_id`：要回复的消息 ID

**注意事项**：
- 机器人必须是聊天/群组成员才能发送消息
- MarkdownV2 需要转义特殊字符：`_*[]()~>#+-=|{}.!`
- HTML 模式支持有限的标签：`<b>`、`<i>`、`<code>`、`<pre>`、`<a>`
- 消息有 4096 字符限制；较长内容需分段发送

### 2. 发送图片和文档

**适用场景**：用户想在 Telegram 聊天中分享图片或文件

**工具调用顺序**：
1. `TELEGRAM_SEND_PHOTO` - 发送图片 [可选]
2. `TELEGRAM_SEND_DOCUMENT` - 发送文件/文档 [可选]

**关键参数**：
- `chat_id`：目标聊天 ID
- `photo`：图片 URL 或 file_id（用于 SEND_PHOTO）
- `document`：文档 URL 或 file_id（用于 SEND_DOCUMENT）
- `caption`：媒体的可选说明文字

**注意事项**：
- 图片说明有 1024 字符限制
- 文档说明同样有 1024 字符限制
- 通过 Bot API 可发送最大 50MB 的文件
- Telegram 会压缩图片；如需未压缩图片请使用 SEND_DOCUMENT

### 3. 管理聊天

**适用场景**：用户想获取聊天信息或管理聊天设置

**工具调用顺序**：
1. `TELEGRAM_GET_CHAT` - 获取详细聊天信息 [必需]
2. `TELEGRAM_GET_CHAT_ADMINISTRATORS` - 列出聊天管理员 [可选]
3. `TELEGRAM_GET_CHAT_MEMBERS_COUNT` - 获取成员数量 [可选]
4. `TELEGRAM_EXPORT_CHAT_INVITE_LINK` - 生成邀请链接 [可选]

**关键参数**：
- `chat_id`：目标聊天 ID 或用户名

**注意事项**：
- 机器人必须是管理员才能导出邀请链接
- GET_CHAT 对私聊、群组和频道返回不同字段
- 超大群组的成员数可能为近似值
- 管理员列表不包含普通成员

### 4. 编辑和删除消息

**适用场景**：用户想修改或删除之前发送的消息

**工具调用顺序**：
1. `TELEGRAM_EDIT_MESSAGE` - 编辑已发送的消息 [可选]
2. `TELEGRAM_DELETE_MESSAGE` - 删除消息 [可选]

**关键参数**：
- `chat_id`：消息所在的聊天
- `message_id`：要编辑或删除的消息 ID
- `text`：新的文本内容（用于编辑）

**注意事项**：
- 机器人只能编辑自己发送的消息
- 消息只能在发送后 48 小时内删除
- 在群组中，具有删除权限的机器人可以删除任何消息
- 编辑消息会移除其"已编辑"时间戳历史

### 5. 转发消息和获取更新

**适用场景**：用户想转发消息或获取最近的更新

**工具调用顺序**：
1. `TELEGRAM_FORWARD_MESSAGE` - 将消息转发到另一个聊天 [可选]
2. `TELEGRAM_GET_UPDATES` - 获取最近的机器人更新/消息 [可选]
3. `TELEGRAM_GET_CHAT_HISTORY` - 获取聊天消息历史 [可选]

**关键参数**：
- `from_chat_id`：转发的源聊天
- `chat_id`：转发的目标聊天
- `message_id`：要转发的消息
- `offset`：GET_UPDATES 的更新偏移量
- `limit`：要获取的更新数量

**注意事项**：
- 转发的消息会显示原始发送者归属
- GET_UPDATES 返回最近更新的有限窗口
- 聊天历史访问可能受机器人权限和聊天类型限制
- 使用 offset 避免重复处理同一更新

### 6. 管理机器人命令

**适用场景**：用户想设置或更新机器人命令菜单

**工具调用顺序**：
1. `TELEGRAM_SET_MY_COMMANDS` - 设置机器人的命令列表 [必需]
2. `TELEGRAM_ANSWER_CALLBACK_QUERY` - 响应内联按钮点击 [可选]

**关键参数**：
- `commands`：包含 `command` 和 `description` 的命令对象数组
- `callback_query_id`：要响应的回调查询 ID

**注意事项**：
- 命令必须以 '/' 开头且为小写
- 命令描述有 256 字符限制
- 回调查询必须在 10 秒内响应，否则会过期
- 设置命令会替换整个命令列表

## 常用模式

### Chat ID 解析

**从用户名获取**：
```
1. Use '@username' format as chat_id (for public channels/groups)
2. For private chats, numeric chat_id is required
3. Call GET_CHAT with username to retrieve numeric ID
```

**从 GET_UPDATES 获取**：
```
1. Call TELEGRAM_GET_UPDATES
2. Extract chat.id from message objects
3. Use numeric chat_id in subsequent calls
```

### 消息格式化

- 使用 `parse_mode: 'HTML'` 实现 `<b>bold</b>`、`<i>italic</i>`、`<code>code</code>`
- 使用 `parse_mode: 'MarkdownV2'` 实现 `*bold*`、`_italic_`、`` `code` ``
- MarkdownV2 中转义特殊字符：`_ * [ ] ( ) ~ > # + - = | { } . !`
- 省略 parse_mode 以发送纯文本（无格式）

## 已知注意事项

**机器人权限**：
- 机器人必须被添加到群组/频道才能交互
- 以下操作需要管理员权限：删除消息、导出邀请链接、管理成员
- 机器人不能主动发起对话；用户必须先启动对话

**速率限制**：
- 同一群组每秒最多 30 条消息
- 群组中同一用户每分钟最多 20 条消息
- 批量操作应在调用之间添加延迟
- 超出限制时 API 返回 429 Too Many Requests

**聊天类型**：
- 私聊：与机器人一对一聊天
- 群组：多用户聊天（需添加机器人）
- 超级群组：具有管理员功能的增强群组
- 频道：仅广播（机器人必须是管理员才能发布）

**消息限制**：
- 文本消息：最多 4096 字符
- 说明文字：最多 1024 字符
- 文件上传：通过 Bot API 最大 50MB
- 内联键盘按钮：每行最多 8 个

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 验证机器人 | TELEGRAM_GET_ME | （无） |
| 发送消息 | TELEGRAM_SEND_MESSAGE | chat_id, text, parse_mode |
| 发送图片 | TELEGRAM_SEND_PHOTO | chat_id, photo, caption |
| 发送文档 | TELEGRAM_SEND_DOCUMENT | chat_id, document, caption |
| 编辑消息 | TELEGRAM_EDIT_MESSAGE | chat_id, message_id, text |
| 删除消息 | TELEGRAM_DELETE_MESSAGE | chat_id, message_id |
| 转发消息 | TELEGRAM_FORWARD_MESSAGE | chat_id, from_chat_id, message_id |
| 获取聊天信息 | TELEGRAM_GET_CHAT | chat_id |
| 获取聊天管理员 | TELEGRAM_GET_CHAT_ADMINISTRATORS | chat_id |
| 获取成员数量 | TELEGRAM_GET_CHAT_MEMBERS_COUNT | chat_id |
| 导出邀请链接 | TELEGRAM_EXPORT_CHAT_INVITE_LINK | chat_id |
| 获取更新 | TELEGRAM_GET_UPDATES | offset, limit |
| 获取聊天历史 | TELEGRAM_GET_CHAT_HISTORY | chat_id |
| 设置机器人命令 | TELEGRAM_SET_MY_COMMANDS | commands |
| 响应回调 | TELEGRAM_ANSWER_CALLBACK_QUERY | callback_query_id |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
