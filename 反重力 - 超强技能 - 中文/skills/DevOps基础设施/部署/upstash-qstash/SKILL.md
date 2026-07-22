---
name: upstash-qstash
description: Upstash QStash 无服务器消息队列专家，支持定时任务和可靠的 HTTP 任务投递，无需管理基础设施。触发词：qstash、upstash queue、serverless cron、scheduled http、message queue serverless、vercel cron、delayed message
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Upstash QStash

Upstash QStash 无服务器消息队列专家，支持定时任务和可靠的 HTTP 任务投递，无需管理基础设施。

## 原则

- HTTP 即接口——能处理 HTTPS，就能处理 QStash
- 端点必须公开——QStash 从云端调用你的 URL
- 永远验证签名——不要信任未验证的 webhook
- 定时任务是开箱即忘的——QStash 处理 cron
- 重试是内置的——但要根据场景配置
- 延迟投递免费——从几秒到几天都可以调度
- 回调完成闭环——知道投递何时成功或失败
- 消息去重防止重复处理——使用消息 ID

## 能力范围

- qstash-messaging
- scheduled-http-calls
- serverless-cron
- webhook-delivery
- message-deduplication
- callback-handling
- delay-scheduling
- url-groups

## 边界

- complex-workflows -> inngest
- redis-queues -> bullmq-specialist
- event-sourcing -> event-architect
- workflow-orchestration -> temporal-craftsman

## 工具链

### 核心

- qstash-sdk
- upstash-console

### 框架

- nextjs
- cloudflare-workers
- vercel-functions
- aws-lambda
- netlify-functions

### 模式

- scheduled-jobs
- delayed-messages
- webhook-fanout
- callback-verification

### 相关

- upstash-redis
- upstash-kafka

## 模式

### 基础消息发布

将消息发送到指定端点

**使用场景**：需要可靠的异步 HTTP 调用

import { Client } from '@upstash/qstash';

const qstash = new Client({
  token: process.env.QSTASH_TOKEN!,
});

// 发送简单消息到端点
await qstash.publishJSON({
  url: 'https://myapp.com/api/process',
  body: {
    userId: '123',
    action: 'welcome-email',
  },
});

// 带延迟（1 小时后处理）
await qstash.publishJSON({
  url: 'https://myapp.com/api/reminder',
  body: { userId: '123' },
  delay: 60 * 60,  // 秒
});

// 指定投递时间
await qstash.publishJSON({
  url: 'https://myapp.com/api/scheduled',
  body: { report: 'daily' },
  notBefore: Math.floor(Date.now() / 1000) + 86400,  // 明天
});

### 定时 Cron 任务

设置周期性定时任务

**使用场景**：需要无基础设施的周期性后台任务

import { Client } from '@upstash/qstash';

const qstash = new Client({
  token: process.env.QSTASH_TOKEN!,
});

// 创建定时任务
const schedule = await qstash.schedules.create({
  destination: 'https://myapp.com/api/cron/daily-report',
  cron: '0 9 * * *',  // 每天 UTC 9 点
  body: JSON.stringify({ type: 'daily' }),
  headers: {
    'Content-Type': 'application/json',
  },
});

console.log('Schedule created:', schedule.scheduleId);

// 列出所有定时任务
const schedules = await qstash.schedules.list();

// 删除定时任务
await qstash.schedules.delete(schedule.scheduleId);

### 签名验证

在端点中验证 QStash 消息签名

**使用场景**：任何接收 QStash 消息的端点（必须！）

// app/api/webhook/route.ts (Next.js App Router)
import { Receiver } from '@upstash/qstash';
import { NextRequest, NextResponse } from 'next/server';

const receiver = new Receiver({
  currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY!,
  nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY!,
});

export async function POST(req: NextRequest) {
  const signature = req.headers.get('upstash-signature');
  const body = await req.text();

  // 必须验证签名
  const isValid = await receiver.verify({
    signature: signature!,
    body,
    url: req.url,
  });

  if (!isValid) {
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 401 }
    );
  }

  // 安全处理
  const data = JSON.parse(body);
  await processMessage(data);

  return NextResponse.json({ success: true });
}

### 投递状态回调

获取消息投递成功或失败的通知

**使用场景**：需要追踪关键消息的投递状态

import { Client } from '@upstash/qstash';

const qstash = new Client({
  token: process.env.QSTASH_TOKEN!,
});

// 带回调发布
await qstash.publishJSON({
  url: 'https://myapp.com/api/critical-task',
  body: { taskId: '456' },
  callback: 'https://myapp.com/api/qstash-callback',
  failureCallback: 'https://myapp.com/api/qstash-failed',
});

// 回调端点接收投递状态
// app/api/qstash-callback/route.ts
export async function POST(req: NextRequest) {
  // 先验证签名！
  const data = await req.json();

  // data 包含：
  // - sourceMessageId: 原始消息 ID
  // - url: 目标 URL
  // - status: HTTP 状态码
  // - body: 响应体

  if (data.status >= 200 && data.status < 300) {
    await markTaskComplete(data.sourceMessageId);
  }

  return NextResponse.json({ received: true });
}

### URL 组（扇出）

同时向多个端点发送消息

**使用场景**：需要通知多个服务某个事件

import { Client } from '@upstash/qstash';

const qstash = new Client({
  token: process.env.QSTASH_TOKEN!,
});

// 创建 URL 组
await qstash.urlGroups.addEndpoints({
  name: 'order-processors',
  endpoints: [
    { url: 'https://inventory.myapp.com/api/process' },
    { url: 'https://shipping.myapp.com/api/process' },
    { url: 'https://analytics.myapp.com/api/track' },
  ],
});

// 发布到组——所有端点都会收到消息
await qstash.publishJSON({
  urlGroup: 'order-processors',
  body: {
    orderId: '789',
    event: 'order.placed',
  },
});

### 消息去重

防止重复消息处理

**使用场景**：幂等性至关重要（支付、通知）

import { Client } from '@upstash/qstash';

const qstash = new Client({
  token: process.env.QSTASH_TOKEN!,
});

// 通过自定义 ID 去重（在去重窗口内）
await qstash.publishJSON({
  url: 'https://myapp.com/api/charge',
  body: { orderId: '123', amount: 5000 },
  deduplicationId: 'charge-order-123',  // 窗口内不会重复发送
});

// 基于内容的去重
await qstash.publishJSON({
  url: 'https://myapp.com/api/notify',
  body: { userId: '456', message: 'Hello' },
  contentBasedDeduplication: true,  // 使用消息体哈希作为 ID
});

## 关键陷阱

### 未验证 QStash webhook 签名

严重程度：CRITICAL

场景：端点接受任意 POST 请求。攻击者发现你的回调 URL。伪造消息涌入系统。恶意负载被当作可信数据处理。

症状：
- webhook 处理器中没有导入 Receiver
- 缺少 upstash-signature 头检查
- 验证前就处理请求

原因：
QStash 端点是公开 URL。没有签名验证，任何人都能发送请求。这是未授权消息处理和潜在数据篡改的直接路径。

修复方案：

# 始终用两个密钥验证签名：
```typescript
import { Receiver } from '@upstash/qstash';

const receiver = new Receiver({
  currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY!,
  nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY!,
});

export async function POST(req: NextRequest) {
  const signature = req.headers.get('upstash-signature');
  const body = await req.text();  // 必须是原始请求体

  const isValid = await receiver.verify({
    signature: signature!,
    body,
    url: req.url,
  });

  if (!isValid) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  // 安全处理
}
```

# 为什么需要两个密钥？
- QStash 会轮换签名密钥
- 轮换时 nextSigningKey 变成 current
- 两个都检查才能无缝轮换

### 回调端点响应太慢

严重程度：HIGH

场景：webhook 处理器执行大量处理，耗时超过 30 秒。QStash 超时。标记为失败。重试。开始重复处理。

症状：
- QStash 仪表板显示 webhook 超时
- 消息标记为失败后重试
- 同一消息重复处理

原因：
QStash 对回调有 30 秒超时。如果端点未及时响应，QStash 认为失败并重试。长时间运行的处理器会导致重复处理和浪费重试。

修复方案：

# 设计为快速确认：
```typescript
export async function POST(req: NextRequest) {
  // 1. 先验证签名（快）
  // 2. 解析和验证消息（快）
  // 3. 排队异步处理（快）

  const message = await parseMessage(req);

  // 不要这样做：
  // await processHeavyWork(message);  // 可能超时！

  // 应该这样做：
  await db.jobs.create({ data: message, status: 'pending' });
  // 或用另一个 QStash 消息处理重活

  return NextResponse.json({ queued: true });  // 快速响应
}
```

# 替代方案：用 QStash 处理重活
```typescript
// Webhook 接收触发
await qstash.publishJSON({
  url: 'https://myapp.com/api/heavy-process',
  body: { jobId: message.id },
});
return NextResponse.json({ delegated: true });
```

# Vercel：考虑用 Edge 运行时加速冷启动

### 意外触发 QStash 速率限制

严重程度：HIGH

场景：突发事件触发大量消息发布。QStash 速率限制被触发。消息被拒绝。用户没收到通知。关键任务延迟。

症状：
- QStash 返回 429 错误
- 消息未投递
- 高峰时段处理量骤降

原因：
QStash 有基于计划的速率限制。免费版：500 条/天。专业版：更高但有限。突发流量会快速耗尽限制。没有监控，你只能等到用户投诉才知道。

修复方案：

# 检查计划限制：
- 免费版：500 条/天
- 按量付费：查看仪表板
- 专业版：更高限制，查看仪表板

# 实现速率限制处理：
```typescript
try {
  await qstash.publishJSON({ url, body });
} catch (error) {
  if (error.message?.includes('rate limit')) {
    // 本地排队稍后重试
    await localQueue.add('qstash-retry', { url, body });
  }
  throw error;
}
```

# 尽量批量发送消息：
```typescript
// 而不是 100 次单独发布
await qstash.batchJSON({
  messages: items.map(item => ({
    url: 'https://myapp.com/api/process',
    body: { itemId: item.id },
  })),
});
```

# 在仪表板监控：
Upstash Console 显示使用量和限制

### 关键操作未使用去重

严重程度：HIGH

场景：发布时网络抖动。SDK 重试。同一消息发送两次。客户被重复扣款。邮件重复发送。数据损坏。

症状：
- 重复扣款或邮件
- 同一事件重复处理
- 用户投诉重复

原因：
网络故障和重试会发生。没有去重，同一逻辑消息可能被发送多次。QStash 提供去重，但你必须在关键操作中使用。

修复方案：

# 关键消息使用去重：
```typescript
// 自定义 ID（最适合业务操作）
await qstash.publishJSON({
  url: 'https://myapp.com/api/charge',
  body: { orderId: '123', amount: 5000 },
  deduplicationId: `charge-${orderId}`,  // 相同 ID = 相同消息
});

// 基于内容（适合通知）
await qstash.publishJSON({
  url: 'https://myapp.com/api/notify',
  body: { userId: '456', type: 'welcome' },
  contentBasedDeduplication: true,  // 消息体哈希
});
```

# 去重窗口：
- 默认：60 秒
- 窗口内相同 ID 的消息被去重
- 在重试逻辑中考虑这一点

# 同时让端点幂等：
处理前检查操作是否已完成

### 期望 QStash 能访问私有/本地端点

严重程度：CRITICAL

场景：开发时用本地服务器正常。部署到生产环境用内部 URL。QStash 无法访问。所有消息静默失败。没有处理发生。

症状：
- 消息在 QStash 仪表板显示"failed"
- 本地正常但"生产"失败
- 使用 http:// 而非 https://

原因：
QStash 运行在 Upstash 云端。只能访问公开的互联网 URL。localhost、内网 IP 和私有网络不可达。这是架构要求，不是配置问题。

修复方案：

# 生产环境要求：
- URL 必须公开可访问
- 必须 HTTPS（HTTP 会失败）
- 不要 localhost、127.0.0.1 或私有 IP

# 本地开发选项：

# 选项 1：ngrok/localtunnel
```bash
ngrok http 3000
# 用 ngrok URL 测试 QStash
```

# 选项 2：QStash 本地开发模式
```typescript
// 开发时跳过 QStash 直接调用
if (process.env.NODE_ENV === 'development') {
  await fetch('http://localhost:3000/api/process', {
    method: 'POST',
    body: JSON.stringify(data),
  });
} else {
  await qstash.publishJSON({ url, body: data });
}
```

# 选项 3：使用 Vercel 预览 URL
预览部署提供公开 URL 用于测试

### 所有消息类型使用默认重试行为

严重程度：MEDIUM

场景：关键支付 webhook 使用默认值。3 次重试在几分钟内。支付处理商临时宕机 15 分钟。消息标记为失败。支付对账需要手动处理。

症状：
- 关键消息标记为失败
- 重试需要手动干预
- 临时中断导致永久失败

原因：
默认重试行为（3 次尝试，短退避）适合很多场景但不是全部。某些端点需要更多尝试、更长退避或不同策略。没有万能方案。

修复方案：

# 按消息配置重试：
```typescript
// 关键操作：更多重试、更长退避
await qstash.publishJSON({
  url: 'https://myapp.com/api/payment-webhook',
  body: { paymentId: '123' },
  retries: 5,
  // 退避：10s、30s、1m、5m、30m
});

// 非关键通知：更少重试
await qstash.publishJSON({
  url: 'https://myapp.com/api/analytics',
  body: { event: 'pageview' },
  retries: 1,  // 快速失败，不关键
});
```

# 考虑端点恢复时间：
- 数据库宕机：可能需要 5+ 分钟
- 第三方 API：可能需要几小时
- 内部服务：通常很快

# 使用失败回调进行死信处理：
```typescript
await qstash.publishJSON({
  url: 'https://myapp.com/api/critical',
  body: data,
  failureCallback: 'https://myapp.com/api/dead-letter',
});
```

### 发送大负载而非引用

严重程度：MEDIUM

场景：消息包含整个文档（5MB）。QStash 拒绝——消息体太大。即使接受，传输也很慢。成本高。浪费带宽。

症状：
- 消息发布失败
- 消息投递慢
- 高带宽成本

原因：
QStash 有消息大小限制（约 500KB 消息体）。大负载拖慢投递、增加成本，可能完全失败。消息应该是轻量触发器，不是数据载体。

修复方案：

# 发送引用，不发送数据：
```typescript
// 不好：大负载
await qstash.publishJSON({
  url: 'https://myapp.com/api/process',
  body: { document: largeDocumentContent },  // 5MB！
});

// 好：只发引用
await qstash.publishJSON({
  url: 'https://myapp.com/api/process',
  body: { documentId: 'doc_123' },  // 在处理器中获取
});
```

# 在处理器中：
```typescript
export async function POST(req: NextRequest) {
  const { documentId } = await req.json();
  const document = await storage.get(documentId);  // 获取实际数据
  await processDocument(document);
}
```

# 大数据存储选项：
- S3/R2/Blob 存储用于文件
- 数据库用于结构化数据
- Redis 用于临时数据（Upstash Redis 是好搭档）

### 关键流程未使用 callback/failureCallback

严重程度：MEDIUM

场景：重要任务已发布。QStash 投递了。端点处理了。但你的系统不知道成功了。用户卡在等待。没有反馈循环。

症状：
- 消息投递不可见
- 用户等待已完成的操作
- 失败没有告警

原因：
QStash 默认是开箱即忘的。没有回调，你不知道消息是否成功投递。关键流程需要反馈循环来更新状态和处理失败。

修复方案：

# 关键操作使用回调：
```typescript
await qstash.publishJSON({
  url: 'https://myapp.com/api/send-email',
  body: { userId: '123', template: 'welcome' },
  callback: 'https://myapp.com/api/email-callback',
  failureCallback: 'https://myapp.com/api/email-failed',
});
```

# 处理回调：
```typescript
// app/api/email-callback/route.ts
export async function POST(req: NextRequest) {
  // 先验证签名！
  const data = await req.json();

  // data.sourceMessageId - 原始消息
  // data.status - HTTP 状态码
  // data.body - 端点响应

  await db.emailLogs.update({
    where: { messageId: data.sourceMessageId },
    data: { status: 'delivered' },
  });

  return NextResponse.json({ received: true });
}
```

# 失败回调用于告警：
```typescript
// app/api/email-failed/route.ts
export async function POST(req: NextRequest) {
  const data = await req.json();
  await alerting.notify(`Email failed: ${data.sourceMessageId}`);
  await db.emailLogs.update({
    where: { messageId: data.sourceMessageId },
    data: { status: 'failed', error: data.body },
  });
}
```

### Cron 调度使用错误时区

严重程度：MEDIUM

场景：定时每日报告设在"9 点"。但哪个时区的 9 点？QStash 用 UTC。报告在本地时间凌晨 4 点运行。用户困惑。提交工单。

症状：
- 调度在意外时间运行
- 夏令时时差一小时
- 用户投诉报告时间

原因：
QStash cron 调度在 UTC 运行。如果你按本地时间配置但用 UTC，调度会在意外时间运行。夏令时切换时尤其麻烦。

修复方案：

# QStash 使用 UTC：
```typescript
// 这在 UTC 9 点运行，不是本地时间
await qstash.schedules.create({
  destination: 'https://myapp.com/api/daily-report',
  cron: '0 9 * * *',  // UTC 9 点
});
```

# 转换为 UTC：
- EST 9 点 = UTC 14 点（冬令时）/ UTC 13 点（夏令时）
- PST 9 点 = UTC 17 点（冬令时）/ UTC 16 点（夏令时）

# 在调度名称中记录时区：
```typescript
await qstash.schedules.create({
  destination: 'https://myapp.com/api/daily-report',
  cron: '0 14 * * *',  // EST 9 点（UTC 14:00）
  body: JSON.stringify({
    timezone: 'America/New_York',
    localTime: '9:00 AM',
  }),
});
```

# 如需处理夏令时：
夏令时变更时更新调度，或接受 UTC 时间

### URL 组包含失效或过时端点

严重程度：MEDIUM

场景：URL 组有 5 个端点。一个服务已弃用数月。消息仍然扇出到它。仪表板显示失败。浪费尝试。投递变慢。

症状：
- URL 组投递失败
- 向弃用服务发送消息
- 超时导致扇出变慢

原因：
URL 组会持续存在直到显式更新。服务变更时端点变得过时。QStash 尝试向失效 URL 投递，浪费重试，失败噪音掩盖真正问题。

修复方案：

# 定期审计 URL 组：
```typescript
const groups = await qstash.urlGroups.list();
for (const group of groups) {
  console.log(`Group: ${group.name}`);
  for (const endpoint of group.endpoints) {
    // 检查端点是否仍然有效
    try {
      await fetch(endpoint.url, { method: 'HEAD' });
      console.log(`  OK: ${endpoint.url}`);
    } catch {
      console.log(`  DEAD: ${endpoint.url}`);
    }
  }
}
```

# 服务变更时更新组：
```typescript
// 移除失效端点
await qstash.urlGroups.removeEndpoints({
  name: 'order-processors',
  endpoints: [{ url: 'https://old-service.myapp.com/api/process' }],
});
```

# 在 CI/CD 中自动化：
部署时检查 URL 组健康状态

## 验证检查

### Webhook 签名验证

严重程度：CRITICAL

消息：QStash webhook 处理器必须使用 Receiver 验证签名

修复操作：添加签名验证：const receiver = new Receiver({ currentSigningKey, nextSigningKey }); await receiver.verify({ signature, body, url })

### 配置两个签名密钥

严重程度：CRITICAL

消息：QStash Receiver 必须有 currentSigningKey 和 nextSigningKey 以支持密钥轮换

修复操作：配置两个密钥：new Receiver({ currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY, nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY })

### QStash token 硬编码

严重程度：CRITICAL

消息：QStash token 不得硬编码——使用环境变量

修复操作：使用 process.env.QSTASH_TOKEN

### QStash 签名密钥硬编码

严重程度：CRITICAL

消息：QStash 签名密钥不得硬编码

修复操作：使用 process.env.QSTASH_CURRENT_SIGNING_KEY 和 process.env.QSTASH_NEXT_SIGNING_KEY

### QStash 发布使用 localhost URL

严重程度：CRITICAL

消息：QStash 无法访问 localhost——端点必须公开可访问

修复操作：使用公开 URL（如部署域名或测试用 ngrok）

### 使用 HTTP 而非 HTTPS

严重程度：ERROR

消息：QStash 要求 HTTPS URL 以确保安全

修复操作：将 http:// 改为 https://

### QStash 发布无错误处理

严重程度：ERROR

消息：QStash 发布调用应有速率限制和失败的错误处理

修复操作：用 try/catch 包裹并适当处理错误

### 签名验证使用解析后的 JSON

严重程度：CRITICAL

消息：签名验证需要原始请求体（req.text()），不是解析后的 JSON

修复操作：使用 await req.text() 获取原始请求体用于验证

### 回调端点无签名验证

严重程度：CRITICAL

消息：回调端点也必须验证签名——它们也接收 QStash 请求

修复操作：为回调处理器添加 Receiver 签名验证

### 调度无目标 URL

严重程度：ERROR

消息：QStash 调度需要目标 URL

修复操作：在调度选项中添加 destination: 'https://your-app.com/api/endpoint'

## 协作

### 委托触发器

- complex workflow|multi-step|state machine -> inngest（需要带检查点的持久化步骤函数）
- redis queue|worker process|job priority -> bullmq-specialist（需要带 worker 的传统队列）
- ai background|long running ai|model inference -> trigger-dev（需要 AI 专用后台处理）
- deploy|vercel|production|environment -> vercel-deployment（需要 QStash 部署配置）
- database|persistence|state|sync -> supabase-backend（需要任务状态数据库）
- auth|user context|session -> nextjs-supabase-auth（需要消息处理器中的用户上下文）

### 无服务器后台任务

技能：upstash-qstash、nextjs-app-router、vercel-deployment

工作流：

```
1. 定义 API 路由处理器 (nextjs-app-router)
2. 配置 QStash 集成 (upstash-qstash)
3. 用环境变量部署 (vercel-deployment)
```

### 可靠 Webhook

技能：upstash-qstash、stripe-integration、supabase-backend

工作流：

```
1. 接收 Stripe webhook (stripe-integration)
2. 排队可靠处理 (upstash-qstash)
3. 持久化状态到数据库 (supabase-backend)
```

### 定时报告

技能：upstash-qstash、email-systems、supabase-backend

工作流：

```
1. 配置 cron 调度 (upstash-qstash)
2. 查询报告数据 (supabase-backend)
3. 通过邮件系统发送 (email-systems)
```

### 扇出通知

技能：upstash-qstash、email-systems、slack-bot-builder

工作流：

```
1. 发布到 URL 组 (upstash-qstash)
2. 邮件处理器接收 (email-systems)
3. Slack 处理器接收 (slack-bot-builder)
```

### 渐进迁移到工作流

技能：upstash-qstash、inngest

工作流：

```
1. 从简单 QStash 消息开始 (upstash-qstash)
2. 识别多步骤模式
3. 将复杂流程迁移到 Inngest (inngest)
4. 简单调度保留在 QStash
```

## 相关技能

配合良好：`vercel-deployment`、`nextjs-app-router`、`redis-specialist`、`email-systems`、`supabase-backend`、`cloudflare-workers`

## 使用场景
- 用户提到或暗示：qstash
- 用户提到或暗示：upstash queue
- 用户提到或暗示：serverless cron
- 用户提到或暗示：scheduled http
- 用户提到或暗示：message queue serverless
- 用户提到或暗示：vercel cron
- 用户提到或暗示：delayed message

## 限制
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为特定环境验证、测试或专家审查的替代品
- 如果缺少必需输入、权限、安全边界或成功标准，停止并请求澄清