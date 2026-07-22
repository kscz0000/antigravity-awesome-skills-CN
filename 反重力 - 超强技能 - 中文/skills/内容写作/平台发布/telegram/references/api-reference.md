# Telegram Bot API - 完整参考

## 目录
1. [身份验证](#autenticacao)
2. [发送方法](#envio)
3. [编辑方法](#edicao)
4. [聊天方法](#chat)
5. [成员方法](#membros)
6. [更新和 Webhook](#updates)
7. [机器人配置](#config)
8. [主要类型](#tipos)
9. [解析模式](#parse-modes)
10. [错误代码](#erros)

---

## 身份验证

**Base URL:** `https://api.telegram.org/bot<TOKEN>/<METHOD>`
**File URL:** `https://api.telegram.org/file/bot<TOKEN>/<file_path>`
**方法:** GET 和 POST

发送参数的方式：
- Query string: `?chat_id=123&text=hello`
- JSON body: `Content-Type: application/json`
- Form data: `Content-Type: application/x-www-form-urlencoded`
- Multipart: `Content-Type: multipart/form-data`（上传文件时必需）

---

## 发送方法

| 方法 | 描述 | 必需参数 |
|------|------|----------|
| `sendMessage` | 文本 | `chat_id`, `text` |
| `sendPhoto` | 照片 | `chat_id`, `photo` |
| `sendVideo` | 视频 | `chat_id`, `video` |
| `sendAnimation` | GIF | `chat_id`, `animation` |
| `sendAudio` | 音频/音乐 | `chat_id`, `audio` |
| `sendDocument` | 文档 | `chat_id`, `document` |
| `sendVoice` | 语音消息 | `chat_id`, `voice` |
| `sendVideoNote` | 圆形视频 | `chat_id`, `video_note` |
| `sendSticker` | 贴纸 | `chat_id`, `sticker` |
| `sendLocation` | 位置 | `chat_id`, `latitude`, `longitude` |
| `sendVenue` | 地点 | `chat_id`, `latitude`, `longitude`, `title`, `address` |
| `sendContact` | 联系人 | `chat_id`, `phone_number`, `first_name` |
| `sendPoll` | 投票 | `chat_id`, `question`, `options` |
| `sendDice` | 动画骰子 | `chat_id` |
| `sendMediaGroup` | 媒体组 | `chat_id`, `media` |
| `sendChatAction` | 输入动作 | `chat_id`, `action` |
| `sendInvoice` | 发票/支付 | `chat_id`, `title`, `description`, `payload`, `currency`, `prices` |

### 所有发送方法的通用参数

| 参数 | 类型 | 描述 |
|------|------|------|
| `chat_id` | Integer/String | 聊天 ID 或 @用户名 |
| `message_thread_id` | Integer | 话题 ID（在论坛中） |
| `parse_mode` | String | `HTML`, `MarkdownV2`, `Markdown` |
| `reply_parameters` | Object | 用于回复消息 |
| `reply_markup` | Object | InlineKeyboard 或 ReplyKeyboard |
| `disable_notification` | Boolean | 静默发送 |
| `protect_content` | Boolean | 禁止转发 |
| `effect_id` | String | 消息视觉效果 |

### sendChatAction - 可用动作

`typing`, `upload_photo`, `record_video`, `upload_video`, `record_voice`, `upload_voice`, `upload_document`, `find_location`, `record_video_note`, `upload_video_note`, `choose_sticker`

---

## 编辑方法

| 方法 | 描述 |
|------|------|
| `editMessageText` | 编辑文本 |
| `editMessageCaption` | 编辑说明 |
| `editMessageMedia` | 编辑媒体 |
| `editMessageReplyMarkup` | 编辑按钮 |
| `deleteMessage` | 删除消息 |
| `deleteMessages` | 删除多条 |
| `forwardMessage` | 转发 |
| `forwardMessages` | 转发多条 |
| `copyMessage` | 复制（无"转发自"标记） |
| `copyMessages` | 复制多条 |

---

## 聊天方法

| 方法 | 描述 |
|------|------|
| `getChat` | 聊天完整信息 |
| `getChatMemberCount` | 成员数量 |
| `getChatAdministrators` | 管理员列表 |
| `setChatTitle` | 修改标题 |
| `setChatDescription` | 修改描述 |
| `setChatPhoto` | 修改头像 |
| `deleteChatPhoto` | 删除头像 |
| `setChatPermissions` | 默认权限 |
| `setChatStickerSet` | 贴纸集 |
| `pinChatMessage` | 置顶消息 |
| `unpinChatMessage` | 取消置顶 |
| `unpinAllChatMessages` | 取消所有置顶 |
| `leaveChat` | 退出聊天 |
| `exportChatInviteLink` | 生成链接 |
| `createChatInviteLink` | 创建自定义链接 |
| `editChatInviteLink` | 编辑链接 |
| `revokeChatInviteLink` | 撤销链接 |

---

## 成员方法

| 方法 | 描述 |
|------|------|
| `getChatMember` | 成员信息 |
| `banChatMember` | 封禁 |
| `unbanChatMember` | 解封 |
| `restrictChatMember` | 限制 |
| `promoteChatMember` | 提升为管理员 |
| `setChatAdministratorCustomTitle` | 自定义头衔 |
| `approveChatJoinRequest` | 批准入群 |
| `declineChatJoinRequest` | 拒绝入群 |

---

## 更新和 Webhook

| 方法 | 描述 |
|------|------|
| `getUpdates` | 长轮询 |
| `setWebhook` | 注册 webhook |
| `deleteWebhook` | 删除 webhook |
| `getWebhookInfo` | webhook 状态 |

### 更新类型

`message`, `edited_message`, `channel_post`, `edited_channel_post`, `inline_query`, `chosen_inline_result`, `callback_query`, `shipping_query`, `pre_checkout_query`, `poll`, `poll_answer`, `my_chat_member`, `chat_member`, `chat_join_request`, `message_reaction`, `message_reaction_count`

---

## 机器人配置

| 方法 | 描述 |
|------|------|
| `getMe` | 机器人信息 |
| `setMyCommands` | 设置命令 |
| `getMyCommands` | 列出命令 |
| `deleteMyCommands` | 删除命令 |
| `setMyName` | 修改名称 |
| `setMyDescription` | 修改描述 |
| `setMyShortDescription` | 简短描述 |
| `setMyDefaultAdministratorRights` | 默认权限 |
| `setChatMenuButton` | 菜单按钮 |
| `setMyProfilePhoto` | 头像 |

---

## 主要类型

### Update
```json
{
  "update_id": 123,
  "message": { ... },
  "callback_query": { ... },
  "inline_query": { ... }
}
```

### Message
```json
{
  "message_id": 1,
  "from": { "id": 123, "first_name": "用户" },
  "chat": { "id": 123, "type": "private" },
  "date": 1709000000,
  "text": "你好",
  "entities": [{ "type": "bot_command", "offset": 0, "length": 6 }]
}
```

### CallbackQuery
```json
{
  "id": "query123",
  "from": { "id": 123 },
  "message": { ... },
  "data": "callback_data_string"
}
```

### InlineKeyboardMarkup
```json
{
  "inline_keyboard": [
    [{ "text": "按钮", "callback_data": "data" }],
    [{ "text": "链接", "url": "https://example.com" }]
  ]
}
```

### ReplyKeyboardMarkup
```json
{
  "keyboard": [
    [{ "text": "选项 1" }, { "text": "选项 2" }],
    [{ "text": "发送位置", "request_location": true }]
  ],
  "resize_keyboard": true,
  "one_time_keyboard": true
}
```

---

## 解析模式

### HTML
```html
<b>粗体</b>
<i>斜体</i>
<u>下划线</u>
<s>删除线</s>
<tg-spoiler>剧透</tg-spoiler>
<code>行内代码</code>
<pre>预格式化</pre>
<pre><code class="language-python">python 代码</code></pre>
<a href="https://example.com">链接</a>
<a href="tg://user?id=123">用户提及</a>
<blockquote>引用</blockquote>
```

### MarkdownV2
```
*粗体*
_斜体_
__下划线__
~删除线~
||剧透||
`行内代码`
```预格式化块```
```python
python 代码
```
[链接](https://example\.com)
[用户](tg://user?id=123)
>引用
```

**MarkdownV2 需转义的字符:** `_ * [ ] ( ) ~ ` > # + - = | { } . !`

---

## 错误代码

| 代码 | 描述 | 操作 |
|------|------|------|
| 400 | Bad Request - 参数无效 | 检查参数 |
| 401 | Unauthorized - 令牌无效 | 检查令牌 |
| 403 | Forbidden - 机器人被封禁 | 用户已封禁机器人 |
| 404 | Not Found - 方法无效 | 检查方法名 |
| 409 | Conflict - webhook 和轮询冲突 | 只使用一种方式 |
| 429 | Too Many Requests - 速率限制 | 等待 `retry_after` 秒 |

### 常见错误消息

- `"chat not found"` - 聊天 ID 无效或机器人未启动
- `"bot was blocked by the user"` - 用户已封禁机器人
- `"message to edit not found"` - 消息已删除
- `"query is too old"` - 回调查询已过期（需在 10 秒内响应）
- `"message is not modified"` - 文本与之前相同
- `"BUTTON_DATA_INVALID"` - callback_data 超过 64 字节
- `"have no rights to send a message"` - 机器人在群组中无权限
