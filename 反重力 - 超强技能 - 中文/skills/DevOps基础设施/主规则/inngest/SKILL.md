---
name: inngest
description: Inngest 专家，专注无服务器优先的后台任务、事件驱动工作流和持久化执行，无需管理队列或工作进程。触发词：inngest、无服务器后台任务、事件驱动工作流、step function、持久化执行、vercel 后台任务、定时函数、fan out
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Inngest 集成

Inngest 专家，专注无服务器优先的后台任务、事件驱动工作流和持久化执行，无需管理队列或工作进程。

## 核心原则

- 事件是原语——一切由事件触发，而非队列
- 步骤即检查点——每个步骤的结果都会被持久化存储
- Sleep 不是取巧——Inngest 的 sleep 是真正的休眠，不是阻塞线程
- 重试是自动的——但策略由你掌控
- 函数只是 HTTP 处理器——可部署到任何提供 HTTP 服务的平台
- 并发是一等公民——保护下游服务
- 幂等键防止重复——关键操作务必使用
- 扇出是内置的——一个事件可触发多个函数

## 能力

- inngest-functions
- event-driven-workflows
- step-functions
- serverless-background-jobs
- durable-sleep
- fan-out-patterns
- concurrency-control
- scheduled-functions

## 范围

- redis-queues -> bullmq-specialist
- workflow-orchestration -> temporal-craftsman
- message-streaming -> event-architect
- infrastructure -> infra-architect

## 工具

### 核心

- inngest
- inngest-cli

### 框架

- nextjs
- express
- hono
- remix
- sveltekit

### 部署

- vercel
- cloudflare-workers
- netlify
- railway
- fly-io

### 模式

- step-functions
- event-fan-out
- scheduled-cron
- webhook-handling

## 模式

### 基础函数设置

Next.js 中带类型事件的 Inngest 函数

**何时使用**：在任何 Next.js 项目中开始使用 Inngest

// lib/inngest/client.ts
import { Inngest } from 'inngest';

export const inngest = new Inngest({
  id: 'my-app',
  schemas: new EventSchemas().fromRecord<Events>(),
});

// 用类型定义你的事件
type Events = {
  'user/signed.up': { data: { userId: string; email: string } };
  'order/placed': { data: { orderId: string; total: number } };
};

// lib/inngest/functions.ts
import { inngest } from './client';

export const sendWelcomeEmail = inngest.createFunction(
  { id: 'send-welcome-email' },
  { event: 'user/signed.up' },
  async ({ event, step }) => {
    // 步骤 1：获取用户详情
    const user = await step.run('get-user', async () => {
      return await db.users.findUnique({ where: { id: event.data.userId } });
    });

    // 步骤 2：发送欢迎邮件
    await step.run('send-email', async () => {
      await resend.emails.send({
        to: user.email,
        subject: 'Welcome!',
        template: 'welcome',
      });
    });

    // 步骤 3：等待 24 小时后发送使用技巧
    await step.sleep('wait-for-tips', '24h');

    await step.run('send-tips', async () => {
      await resend.emails.send({
        to: user.email,
        subject: 'Getting Started Tips',
        template: 'tips',
      });
    });
  }
);

// app/api/inngest/route.ts (Next.js App Router)
import { serve } from 'inngest/next';
import { inngest } from '@/lib/inngest/client';
import { sendWelcomeEmail } from '@/lib/inngest/functions';

export const { GET, POST, PUT } = serve({
  client: inngest,
  functions: [sendWelcomeEmail],
});

### 多步骤工作流

带并行步骤和错误处理的复杂工作流

**何时使用**：涉及多个服务或需要长时间等待的处理场景

export const processOrder = inngest.createFunction(
  {
    id: 'process-order',
    retries: 3,
    concurrency: { limit: 10 },  // 最多同时处理 10 个订单
  },
  { event: 'order/placed' },
  async ({ event, step }) => {
    const { orderId } = event.data;

    // 并行步骤——两者同时运行
    const [inventory, payment] = await Promise.all([
      step.run('check-inventory', () => checkInventory(orderId)),
      step.run('validate-payment', () => validatePayment(orderId)),
    ]);

    if (!inventory.available) {
      // 发送事件而非直接调用（扇出模式）
      await step.sendEvent('notify-backorder', {
        name: 'order/backordered',
        data: { orderId, items: inventory.missing },
      });
      return { status: 'backordered' };
    }

    // 扣款
    const charge = await step.run('charge-payment', async () => {
      return await stripe.charges.create({
        amount: event.data.total,
        customer: payment.customerId,
      });
    });

    // 发货
    await step.run('ship-order', () => fulfillment.ship(orderId));

    return { status: 'completed', chargeId: charge.id };
  }
);

### 定时/Cron 函数

按计划定时运行的函数

**何时使用**：每日报告、清理作业等周期性任务

export const dailyDigest = inngest.createFunction(
  { id: 'daily-digest' },
  { cron: '0 9 * * *' },  // 每天 UTC 上午 9 点
  async ({ step }) => {
    // 获取所有需要摘要的用户
    const users = await step.run('get-users', async () => {
      return await db.users.findMany({
        where: { digestEnabled: true },
      });
    });

    // 向每个用户发送（创建子事件）
    await step.sendEvent(
      'send-digests',
      users.map(user => ({
        name: 'digest/send',
        data: { userId: user.id },
      }))
    );

    return { sent: users.length };
  }
);

// 独立函数处理单个摘要发送
export const sendDigest = inngest.createFunction(
  { id: 'send-digest', concurrency: { limit: 50 } },
  { event: 'digest/send' },
  async ({ event, step }) => {
    // ... 发送单个摘要
  }
);

### 带幂等性的 Webhook 处理器

安全处理带去重的 webhook

**何时使用**：处理 Stripe、GitHub 等平台的 webhook

export const handleStripeWebhook = inngest.createFunction(
  {
    id: 'stripe-webhook',
    // 按 Stripe 事件 ID 去重
    idempotency: 'event.data.stripeEventId',
  },
  { event: 'stripe/webhook.received' },
  async ({ event, step }) => {
    const { type, data } = event.data;

    switch (type) {
      case 'checkout.session.completed':
        await step.run('fulfill-order', async () => {
          await fulfillOrder(data.session.id);
        });
        break;

      case 'customer.subscription.deleted':
        await step.run('cancel-subscription', async () => {
          await cancelSubscription(data.subscription.id);
        });
        break;
    }
  }
);

### 长时间处理的 AI 管道

带分块工作的多步骤 AI 处理

**何时使用**：可能需要数分钟才能完成的 AI 工作流

export const processDocument = inngest.createFunction(
  {
    id: 'process-document',
    retries: 2,
    concurrency: { limit: 5 },  // 限制 API 调用量
  },
  { event: 'document/uploaded' },
  async ({ event, step }) => {
    // 步骤 1：提取文本（可能耗时较长）
    const text = await step.run('extract-text', async () => {
      return await extractTextFromPDF(event.data.fileUrl);
    });

    // 步骤 2：分块用于嵌入
    const chunks = await step.run('chunk-text', async () => {
      return chunkText(text, { maxTokens: 500 });
    });

    // 步骤 3：生成嵌入（受 API 速率限制）
    const embeddings = await step.run('generate-embeddings', async () => {
      return await openai.embeddings.create({
        model: 'text-embedding-3-small',
        input: chunks,
      });
    });

    // 步骤 4：存入向量数据库
    await step.run('store-vectors', async () => {
      await vectorDb.upsert({
        vectors: embeddings.data.map((e, i) => ({
          id: `${event.data.documentId}-${i}`,
          values: e.embedding,
          metadata: { chunk: chunks[i] },
        })),
      });
    });

    return { chunks: chunks.length, status: 'indexed' };
  }
);

## 验证检查

### Inngest serve 处理器已就位

严重级别：CRITICAL

消息：Inngest 需要 serve 处理器才能接收事件

修复操作：创建 app/api/inngest/route.ts 并导出 serve()

### 函数已注册到 serve

严重级别：ERROR

消息：确保所有 Inngest 函数都在 serve() 调用中注册

修复操作：将函数添加到 serve() 的 functions 数组中

### Step.run 有描述性名称

严重级别：WARNING

消息：步骤名称应使用 kebab-case 并具有描述性

修复操作：使用描述性步骤名称，如 'fetch-user' 或 'send-email'

### waitForEvent 设置了超时

严重级别：ERROR

消息：waitForEvent 应设置超时以防止无限等待

修复操作：添加 timeout 选项：{ timeout: '24h' }

### 函数设有并发限制

严重级别：WARNING

消息：建议添加并发限制以保护下游服务

修复操作：在函数配置中添加 concurrency: { limit: 10 }

### 事件类型已定义

严重级别：WARNING

消息：Inngest 客户端应定义事件模式以确保类型安全

修复操作：添加 schemas: new EventSchemas().fromRecord<Events>()

### 函数拥有唯一 ID

严重级别：CRITICAL

消息：每个 Inngest 函数必须有唯一 ID

修复操作：在函数配置中添加 id: 'my-function-name'

### Sleep 使用时长字符串

严重级别：WARNING

消息：step.sleep 应使用时长字符串如 '1h' 或 '30m'，而非毫秒数

修复操作：使用时长字符串：step.sleep('wait', '1h')

### 重试策略已配置

严重级别：WARNING

消息：建议配置重试策略以应对失败场景

修复操作：添加 retries: 3 或 retries: { attempts: 3, backoff: { ... } }

### 支付函数设有幂等键

严重级别：ERROR

消息：支付相关函数应使用幂等键

修复操作：在函数配置中添加 idempotency: 'event.data.orderId'

## 协作

### 委托触发器

- redis|queue infrastructure|bullmq -> bullmq-specialist（需要基于 Redis 的队列和现有基础设施）
- saga|compensation|rollback|long-running workflow -> temporal-craftsman（需要带补偿的复杂工作流编排）
- event sourcing|event store|cqrs -> event-architect（需要事件溯源模式）
- vercel|deploy|production -> vercel-deployment（需要部署配置）
- database|schema|data model -> supabase-backend（需要用于事件数据的数据库）
- api|endpoint|route -> backend（需要 API 来触发事件）

### Vercel 后台任务

技能：inngest, nextjs-app-router, vercel-deployment

工作流：

```
1. 定义 Inngest 函数 (inngest)
2. 在 Next.js 中设置 serve 处理器 (nextjs-app-router)
3. 配置函数超时 (vercel-deployment)
4. 部署并测试 (vercel-deployment)
```

### AI 管道

技能：inngest, ai-agents-architect, supabase-backend

工作流：

```
1. 设计 AI 工作流步骤 (ai-agents-architect)
2. 用 Inngest 持久化能力实现 (inngest)
3. 将结果存入数据库 (supabase-backend)
4. 处理 API 失败的重试 (inngest)
```

### Webhook 处理

技能：inngest, stripe-integration, backend

工作流：

```
1. 接收 webhook (backend)
2. 带幂等性发送到 Inngest (inngest)
3. 处理支付逻辑 (stripe-integration)
4. 更新应用状态 (backend)
```

### 邮件自动化

技能：inngest, email-systems, supabase-backend

工作流：

```
1. 从用户操作触发事件 (inngest)
2. 用 step.sleep 安排滴灌邮件 (inngest)
3. 带重试发送邮件 (email-systems)
4. 跟踪邮件状态 (supabase-backend)
```

### 定时任务

技能：inngest, backend, analytics-architecture

工作流：

```
1. 定义 cron 触发器 (inngest)
2. 实现处理逻辑 (backend)
3. 聚合并报告数据 (analytics-architecture)
4. 带告警处理失败 (inngest)
```

## 相关技能

配合使用效果良好：`nextjs-app-router`, `vercel-deployment`, `supabase-backend`, `email-systems`, `ai-agents-architect`, `stripe-integration`

## 何时使用

- 用户提到或暗示：inngest
- 用户提到或暗示：无服务器后台任务
- 用户提到或暗示：事件驱动工作流
- 用户提到或暗示：step function
- 用户提到或暗示：持久化执行
- 用户提到或暗示：vercel 后台任务
- 用户提到或暗示：定时函数
- 用户提到或暗示：fan out

## 限制

- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
