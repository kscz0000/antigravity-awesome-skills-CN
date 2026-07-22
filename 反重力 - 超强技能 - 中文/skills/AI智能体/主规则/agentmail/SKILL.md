---
name: agentmail
description: AI 智能体的邮件基础设施。通过 AgentMail API 创建账户、发送/接收邮件、管理 Webhook 以及检查 Karma 余额。触发词：agentmail、AI邮件、智能体邮件、AgentMail、邮件API、智能体邮箱、AI邮箱、agent mail、email for agents
risk: safe
source: community
---

# AgentMail — AI 智能体的邮件服务

AgentMail 为 AI 智能体提供真实的邮箱地址（`@theagentmail.net`），通过 REST API 进行管理。智能体可以发送和接收邮件、注册服务（GitHub、AWS、Slack 等）并获取验证码。Karma 系统可防止垃圾邮件，保持共享域名的良好声誉。

Base URL: `https://api.theagentmail.net`

## 何时使用

- AI 智能体需要真实的收件箱/发件箱，用于注册、验证流程或事务性通信。
- 你需要创建 AgentMail 账户、发送消息、读取收件箱内容或注册入站 Webhook。
- 你需要监控 Karma 使用情况或将邮件事件接入智能体自动化流程。

## 快速开始

所有请求都需要 `Authorization: Bearer am_...` 请求头（从控制面板获取 API 密钥）。

### 创建邮箱账户（-10 karma）

```bash
curl -X POST https://api.theagentmail.net/v1/accounts \
  -H "Authorization: Bearer am_..." \
  -H "Content-Type: application/json" \
  -d '{"address": "my-agent@theagentmail.net"}'
```

响应：`{"data": {"id": "...", "address": "my-agent@theagentmail.net", "displayName": null, "createdAt": 123}}`

### 发送邮件（-1 karma）

```bash
curl -X POST https://api.theagentmail.net/v1/accounts/{accountId}/messages \
  -H "Authorization: Bearer am_..." \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["recipient@example.com"],
    "subject": "Hello from my agent",
    "text": "Plain text body",
    "html": "<p>Optional HTML body</p>"
  }'
```

可选字段：`cc`、`bcc`（字符串数组），`inReplyTo`、`references`（用于邮件线程的字符串），`attachments`（`{filename, contentType, content}` 数组，其中 content 为 base64 编码）。

### 读取收件箱

```bash
# 列出消息
curl https://api.theagentmail.net/v1/accounts/{accountId}/messages \
  -H "Authorization: Bearer am_..."

# 获取完整消息（包含正文和附件）
curl https://api.theagentmail.net/v1/accounts/{accountId}/messages/{messageId} \
  -H "Authorization: Bearer am_..."
```

### 检查 Karma

```bash
curl https://api.theagentmail.net/v1/karma \
  -H "Authorization: Bearer am_..."
```

响应：`{"data": {"balance": 90, "events": [...]}}`

### 注册 Webhook（实时入站）

```bash
curl -X POST https://api.theagentmail.net/v1/accounts/{accountId}/webhooks \
  -H "Authorization: Bearer am_..." \
  -H "Content-Type: application/json" \
  -d '{"url": "https://my-agent.example.com/inbox"}'
```

Webhook 推送包含两个安全请求头：
- `X-AgentMail-Signature` — 请求体的 HMAC-SHA256 十六进制摘要，使用 Webhook 密钥签名
- `X-AgentMail-Timestamp` — 推送发送时的毫秒时间戳

验证签名并拒绝时间戳超过 5 分钟的请求，以防止重放攻击：

```typescript
import { createHmac } from "crypto";

const verifyWebhook = (body: string, signature: string, timestamp: string, secret: string) => {
  if (Date.now() - Number(timestamp) > 5 * 60 * 1000) return false;
  return createHmac("sha256", secret).update(body).digest("hex") === signature;
};
```

### 下载附件

```bash
curl https://api.theagentmail.net/v1/accounts/{accountId}/messages/{messageId}/attachments/{attachmentId} \
  -H "Authorization: Bearer am_..."
```

返回 `{"data": {"url": "https://signed-download-url..."}}`。

## 完整 API 参考

| Method | Path | Description | Karma |
|--------|------|-------------|-------|
| POST | `/v1/accounts` | 创建邮箱账户 | -10 |
| GET | `/v1/accounts` | 列出所有账户 | |
| GET | `/v1/accounts/:id` | 获取账户详情 | |
| DELETE | `/v1/accounts/:id` | 删除账户 | +10 |
| POST | `/v1/accounts/:id/messages` | 发送邮件 | -1 |
| GET | `/v1/accounts/:id/messages` | 列出消息 | |
| GET | `/v1/accounts/:id/messages/:msgId` | 获取完整消息 | |
| GET | `/v1/accounts/:id/messages/:msgId/attachments/:attId` | 获取附件 URL | |
| POST | `/v1/accounts/:id/webhooks` | 注册 Webhook | |
| GET | `/v1/accounts/:id/webhooks` | 列出 Webhook | |
| DELETE | `/v1/accounts/:id/webhooks/:whId` | 删除 Webhook | |
| GET | `/v1/karma` | 获取余额和事件 | |

## Karma 系统

每个操作都有 Karma 成本或奖励：

| 事件 | Karma | 原因 |
|---|---|---|
| `money_paid` | +100 | 购买积分 |
| `email_received` | +2 | 有人从受信任的域名回复 |
| `account_deleted` | +10 | 删除地址时返还 Karma |
| `email_sent` | -1 | 发送邮件消耗 Karma |
| `account_created` | -10 | 创建地址消耗 Karma |

**重要规则：**
- Karma 仅奖励来自受信任提供商的入站邮件（Gmail、Outlook、Yahoo、iCloud、ProtonMail、Fastmail、Hey 等）。来自未知/临时域名的邮件不会获得 Karma。
- 每个发件人仅获得一次 Karma，直到智能体回复。如果发件人 X 向你发送了 5 封邮件而你未回复，只有第一封获得 Karma。回复 X 后，X 的下一封邮件将再次获得 Karma。
- 删除账户会返还创建时消耗的 10 Karma。

当 Karma 降为 0 时，发送邮件和创建账户将返回 HTTP 402。在执行消耗 Karma 的操作前，务必检查余额。

## TypeScript SDK

```typescript
import { createClient } from "@agentmail/sdk";

const mail = createClient({ apiKey: "am_..." });

// 创建账户
const account = await mail.accounts.create({
  address: "my-agent@theagentmail.net",
});

// 发送邮件
await mail.messages.send(account.id, {
  to: ["human@example.com"],
  subject: "Hello",
  text: "Sent by an AI agent.",
});

// 读取收件箱
const messages = await mail.messages.list(account.id);
const detail = await mail.messages.get(account.id, messages[0].id);

// 附件
const att = await mail.attachments.getUrl(accountId, messageId, attachmentId);
// att.url 是签名下载 URL

// Webhook
await mail.webhooks.create(account.id, {
  url: "https://my-agent.example.com/inbox",
});

// Karma
const karma = await mail.karma.getBalance();
console.log(karma.balance);
```

## 错误处理

```typescript
import { AgentMailError } from "@agentmail/sdk";

try {
  await mail.messages.send(accountId, { to: ["a@b.com"], subject: "Hi", text: "Hey" });
} catch (e) {
  if (e instanceof AgentMailError) {
    console.log(e.status);   // 402, 404, 401 等
    console.log(e.code);     // "INSUFFICIENT_KARMA", "NOT_FOUND" 等
    console.log(e.message);
  }
}
```

## 常用模式

### 注册服务并读取验证邮件

```typescript
const account = await mail.accounts.create({
  address: "signup-bot@theagentmail.net",
});

// 使用该地址注册（浏览器自动化、API 等）

// 轮询验证邮件
for (let i = 0; i < 30; i++) {
  const messages = await mail.messages.list(account.id);
  const verification = messages.find(m =>
    m.subject.toLowerCase().includes("verify") ||
    m.subject.toLowerCase().includes("confirm")
  );
  if (verification) {
    const detail = await mail.messages.get(account.id, verification.id);
    // 从 detail.bodyText 或 detail.bodyHtml 解析验证链接/验证码
    break;
  }
  await new Promise(r => setTimeout(r, 2000));
}
```

### 发送邮件并等待回复

```typescript
const sent = await mail.messages.send(account.id, {
  to: ["human@company.com"],
  subject: "Question about order #12345",
  text: "Can you check the status?",
});

for (let i = 0; i < 60; i++) {
  const messages = await mail.messages.list(account.id);
  const reply = messages.find(m =>
    m.direction === "inbound" && m.timestamp > sent.timestamp
  );
  if (reply) {
    const detail = await mail.messages.get(account.id, reply.id);
    // 处理回复
    break;
  }
  await new Promise(r => setTimeout(r, 5000));
}
```

## 类型定义

```typescript
type Account = { id: string; address: string; displayName: string | null; createdAt: number };
type Message = { id: string; from: string; to: string[]; subject: string; direction: "inbound" | "outbound"; status: string; timestamp: number };
type MessageDetail = Message & { cc: string[] | null; bcc: string[] | null; bodyText: string | null; bodyHtml: string | null; inReplyTo: string | null; references: string | null; attachments: AttachmentMeta[] };
type AttachmentMeta = { id: string; filename: string; contentType: string; size: number };
type KarmaBalance = { balance: number; events: KarmaEvent[] };
type KarmaEvent = { id: string; type: string; amount: number; timestamp: number; metadata?: Record<string, unknown> };
```

## 限制

- 仅在任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
