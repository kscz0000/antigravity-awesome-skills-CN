---
name: sendblue-api
description: "通过 Sendblue HTTP API 从应用代码发送和接收 iMessage、SMS 和 RCS——支持文本、媒体、群消息、发送样式、表态、正在输入提示、状态回执和入站 Webhook。"
category: api-integration
risk: critical
source: community
source_type: official
date_added: "2026-05-22"
author: AnthonyFirth
tags: [sendblue, imessage, sms, rcs, messaging, api, webhooks]
tools: [claude, cursor, gemini]
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Sendblue API

## 概述

Sendblue 是一款 REST API，可从已开通的电话号码发送 iMessage（蓝色气泡）、SMS 和 RCS。一切都是基于 HTTPS 的纯 JSON——无需 SDK。该 API 涵盖出站一对一和群组发送、iMessage 特效、表态、正在输入提示、状态回执以及入站 Webhook。

## 适用场景

- 当编写作为长跑服务一部分发送 Sendblue 消息的应用代码（服务器、Worker，函数）时。
- 当通过 Webhook 接收入站消息时。
- 当你需要 CLI 未提供的功能时：发送样式、表态、群组消息、正在输入提示、状态回执、媒体上传，或超出基础 CRUD 的联系人 API。
- 在 Shell 上下文做一次性出站时（一次性脚本、定时任务、智能体钩子、"X 发生时通知我"工作流），请改用 [[sendblue-cli]]。

## 工作原理

### 步骤 1：认证

```
https://api.sendblue.com
```

每个请求都需要两个 Header：

```
sb-api-key-id: <YOUR_API_KEY_ID>
sb-api-secret-key: <YOUR_API_SECRET>
Content-Type: application/json
```

两个值都应保留在服务端——切勿发送到浏览器或移动客户端。

### 步骤 2：发送消息

```bash
curl -X POST https://api.sendblue.com/api/send-message \
  -H "sb-api-key-id: $KEY_ID" \
  -H "sb-api-secret-key: $SECRET" \
  -H 'Content-Type: application/json' \
  -d '{
    "number": "+15551234567",
    "from_number": "+1YOUR_SENDBLUE_NUMBER",
    "content": "Hello from the API!"
  }'
```

电话号码必须是 E.164 格式。`from_number` 必须是属于你的线路——可通过 `GET /api/lines` 列出你的号码。

### 步骤 3：追踪投递

同步响应包含 `message_handle`（Apple GUID——务必持久化，发起表态和回复时需要它）和一个 `status`（取值来自 `REGISTERED`、`PENDING`、`QUEUED`、`ACCEPTED`、`SENT`、`DELIVERED`、`DECLINED`、`ERROR`）。只有 `DELIVERED` 才表示真正送达。请使用 `status_callback` 而非轮询 `/api/status`。

### 步骤 4：接收入站消息

在控制台或通过 `POST /api/account/webhooks` 配置 Webhook URL。Sendblue 会向你的端点 POST JSON。请及时返回 2xx——非 2xx 会触发重试和重复投递。事件类型包括：`receive`、`outbound`、`typing_indicator`、`call_log`、`line_blocked`、`line_assigned`、`contact_created`。

## 核心端点

| Method | Path | 用途 |
|--------|------|---------|
| POST | `/api/send-message` | 发送一对一消息（文本和/或媒体）|
| POST | `/api/send-group-message` | 发送给多个收件人 |
| POST | `/api/create-group` | 创建命名群组会话 |
| POST | `/api/send-reaction` | 发送 tapback 表态（love/like/dislike/laugh/emphasize/question）|
| POST | `/api/send-typing-indicator` | 在收件人会话中显示"正在输入…"|
| POST | `/api/mark-read` | 发送已读回执 |
| POST | `/api/upload-file` / `/api/upload-media-object` | 上传媒体（直接上传或从 URL）|
| GET | `/api/status` | 轮询消息的投递状态 |
| GET | `/api/evaluate-service` | 检查某个号码是否在 iMessage 上 |
| GET | `/api/v2/messages` / `/api/v2/messages/:id` | 读取消息历史 |
| GET / POST / PUT / DELETE | `/api/v2/contacts[...]` | 管理联系人 |
| GET | `/api/lines` | 列出你的 Sendblue 电话号码 |
| POST | `/api/account/webhooks` | 对 Webhook 订阅做 CRUD |

## 示例

### 示例 1：发送带媒体、特效和状态回执的消息

```json
POST /api/send-message
{
  "number": "+15551234567",
  "from_number": "+1YOUR_SENDBLUE_NUMBER",
  "content": "Optional text",
  "media_url": "https://example.com/img.jpg",
  "send_style": "celebration",
  "status_callback": "https://yourapp.com/sendblue/status"
}
```

`content` 和/或 `media_url` 必填。`send_style` 仅适用于 iMessage——有效取值为：`celebration`、`shooting_star`、`fireworks`、`lasers`、`love`、`confetti`、`balloons`、`spotlight`、`echo`、`invisible`、`gentle`、`loud`、`slam`。SMS 上忽略此字段。文本上限 18,996 字符；媒体在 iMessage 上限 100 MB，SMS 上限 5 MB。

### 示例 2：群发消息

```json
POST /api/send-group-message
{
  "numbers": ["+15551234567", "+15557654321"],
  "from_number": "+1YOUR_SENDBLUE_NUMBER",
  "content": "Hey team"
}
```

响应会返回一个 `group_id`——请持久化它，以便在同一个会话中发送后续消息，而不是每次都新建会话。

### 示例 3：对消息表态

```json
POST /api/send-reaction
{
  "from_number": "+1YOUR_SENDBLUE_NUMBER",
  "message_handle": "<message_handle from prior send>",
  "reaction": "love"
}
```

表态仅在 iMessage 上生效，且需要原消息的 `message_handle`。有效取值为：`love`、`like`、`dislike`、`laugh`、`emphasize`、`question`。

### 示例 4：入站 Webhook 负载（`receive`）

```json
{
  "accountEmail": "you@example.com",
  "content": "Reply text",
  "media_url": "https://...",
  "is_outbound": false,
  "number": "+15551234567",
  "from_number": "+1YOUR_SENDBLUE_NUMBER",
  "service": "iMessage",
  "group_id": "...",
  "date_sent": "2024-01-01T12:00:00Z"
}
```

状态回执负载（`outbound`）与 send-message 响应结构一致，并随消息在 `SENT` → `DELIVERED`（或 `ERROR`）之间流转而更新。

## 最佳实践

- ✅ **每次发送都持久化 `message_handle`。** 表态、回复以及关联状态回执都需要它。
- ✅ **使用 `status_callback` 而非轮询。** 比 `GET /api/status` 成本更低且更准确。
- ✅ **Webhook 快速返回 2xx**，然后异步处理。非 2xx 会触发重复投递。
- ✅ **在依赖 iMessage 专属功能前**，先用 `/api/evaluate-service` 检查收件人线路。
- ✅ **收到入站媒体后重新托管**——媒体 URL 约 30 天后过期。
- ❌ **切勿将 `sb-api-key-id` / `sb-api-secret-key` 发给客户端。** 它们是服务端凭据。
- ❌ **不要把 `/api/send-message` 返回 200 当作已送达。** 它只表示"已接受"。

## 限制

- 同步发送响应仅反映是否被接受，并不代表已送达。最终状态通过 `status_callback` 或 `GET /api/status` 到达。
- `send_style` 在 SMS（绿气泡收件人）上静默无效。
- 入站媒体 URL 约 30 天后过期。
- 单线路有速率限制；从同一号码突发大量发送可能触发 Apple 的垃圾消息启发式——请控制节奏或分散到多条线路。
- 表态和特效仅适用于 iMessage。

## 安全注意事项

- 将 `sb-api-key-id` 和 `sb-api-secret-key` 保留在服务端。它们出现在浏览器、移动端或 CI 日志中都不安全。
- 将每次出站发送、联系人/Webhook 修改、已读回执、表态或正在输入提示视为状态变更操作。请先预览收件人、发件线路、内容和回执/Webhook 变更，等待用户明确确认后再发送。
- Webhook 端点应启用 HTTPS 并具备幂等性——同一个 `message_handle` 可能多次到达。
- 消息内容中的敏感数据会显示在收件人设备的锁屏预览里。不要嵌入密钥、Token 或完整的 PII——改为链接到带身份认证的仪表盘或精简后的负载。
- 若任一凭据泄露，请在 Sendblue 控制台轮换 API Key；轮换后旧密钥对立即失效。

## 常见陷阱

- **仅限 E.164 格式。** `5551234567` 或 `(555) 123-4567` 会失败——务必发送 `+15551234567`。
- **`from_number` 必须属于你的线路之一。** 使用伪造或未开通的号码会返回错误。
- **`send_style` 在 SMS 上静默无效。** 如果收件人是绿气泡，特效不会渲染——必要时先用 `/api/evaluate-service` 检查线路。
- **务必存储 `message_handle`。** 表态、回复以及将状态回执关联回你的记录都需要它。
- **媒体 URL 约 30 天后过期。** 如果需要从入站 Webhook 中长期保留媒体，请在收到时下载并重新托管。
- **状态是异步的。** `/api/send-message` 返回 200 只表示已接受，并不代表已送达。请使用 `status_callback` 而不是阻塞等待同步响应。
- **非 2xx 会触发 Webhook 重试。** 即使你决定忽略某个事件，也要返回 200；否则将出现重复投递。
- **按线路生效速率限制。** 从同一号码突发大量发送会触发 Apple 的垃圾消息启发式——请控制节奏或分散到多条线路。

## 相关技能

- `@sendblue-cli`——Shell 上下文的封装器（脚本、定时任务、智能体钩子）。当你不需要完整的 HTTP 集成时使用。
- `@sendblue-notify`——在 API 或 CLI 之上构建的出站"X 完成时发短信通知我"消息的文案与模式。

## 链接

- 完整参考：<https://docs.sendblue.com/>
- Sendblue：<https://sendblue.com>
- 此处未文档化的实用功能：轮播（`/api/send-carousel`）、FaceTime/联系人卡片分享、高级 Webhook 过滤、超出基础 CRUD 的联系人 API——请参见文档站点。