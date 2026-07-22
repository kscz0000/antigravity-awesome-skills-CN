---
name: trigger-dev
description: Trigger.dev 专家，专注于后台任务、AI 工作流和可靠的异步执行，
  提供卓越的开发者体验和 TypeScript 优先设计。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Trigger.dev 集成

Trigger.dev 专家，专注于后台任务、AI 工作流和可靠的异步执行，提供卓越的开发者体验和 TypeScript 优先设计。

## 核心原则

- 任务是构建块 - 每个任务可独立重试
- 运行具有持久性 - 状态在崩溃和重启后保留
- 集成是一等公民 - 使用内置 API 封装确保可靠性
- 日志是调试生命线 - 在任务中大量记录
- 并发保护资源 - 始终设置限制
- 延迟和调度内置 - 无需外部 cron
- AI 就绪设计 - 长时间运行的 AI 任务开箱即用
- 本地开发与生产一致 - 使用 CLI

## 能力范围

- trigger-dev-tasks
- ai-background-jobs
- integration-tasks
- scheduled-triggers
- webhook-handlers
- long-running-tasks
- task-queues
- batch-processing

## 边界

- redis-queues -> bullmq-specialist
- pure-event-driven -> inngest
- workflow-orchestration -> temporal-craftsman
- infrastructure -> infra-architect

## 工具链

### 核心

- trigger-dev-sdk
- trigger-cli

### 框架

- nextjs
- remix
- express
- hono

### 集成

- openai
- anthropic
- resend
- stripe
- slack
- supabase

### 部署

- trigger-cloud
- self-hosted
- docker

## 模式

### 基础任务配置

在 Next.js 项目中配置 Trigger.dev

**适用场景**：在任何项目中开始使用 Trigger.dev

// trigger.config.ts
import { defineConfig } from '@trigger.dev/sdk/v3';

export default defineConfig({
  project: 'my-project',
  runtime: 'node',
  logLevel: 'log',
  retries: {
    enabledInDev: true,
    default: {
      maxAttempts: 3,
      minTimeoutInMs: 1000,
      maxTimeoutInMs: 10000,
      factor: 2,
    },
  },
});

// src/trigger/tasks.ts
import { task, logger } from '@trigger.dev/sdk/v3';

export const helloWorld = task({
  id: 'hello-world',
  run: async (payload: { name: string }) => {
    logger.log('Processing hello world', { payload });

    // Simulate work
    await new Promise(resolve => setTimeout(resolve, 1000));

    return { message: `Hello, ${payload.name}!` };
  },
});

// Triggering from your app
import { helloWorld } from '@/trigger/tasks';

// Fire and forget
await helloWorld.trigger({ name: 'World' });

// Wait for result
const handle = await helloWorld.trigger({ name: 'World' });
const result = await handle.wait();

### 集成 OpenAI 的 AI 任务

使用内置 OpenAI 集成实现自动重试

**适用场景**：构建 AI 驱动的后台任务

import { task, logger } from '@trigger.dev/sdk/v3';
import { openai } from '@trigger.dev/openai';

// Configure OpenAI with Trigger.dev
const openaiClient = openai.configure({
  id: 'openai',
  apiKey: process.env.OPENAI_API_KEY,
});

export const generateContent = task({
  id: 'generate-content',
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: { topic: string; style: string }) => {
    logger.log('Generating content', { topic: payload.topic });

    // Uses Trigger.dev's OpenAI integration - handles retries automatically
    const completion = await openaiClient.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        {
          role: 'system',
          content: `You are a ${payload.style} writer.`,
        },
        {
          role: 'user',
          content: `Write about: ${payload.topic}`,
        },
      ],
    });

    const content = completion.choices[0].message.content;
    logger.log('Generated content', { length: content?.length });

    return { content, tokens: completion.usage?.total_tokens };
  },
});

### 定时任务（Cron）

按计划运行的任务

**适用场景**：定期任务，如报告、清理或同步

import { schedules, task, logger } from '@trigger.dev/sdk/v3';

export const dailyCleanup = schedules.task({
  id: 'daily-cleanup',
  cron: '0 2 * * *',  // 2 AM daily
  run: async () => {
    logger.log('Starting daily cleanup');

    // Clean up old records
    const deleted = await db.logs.deleteMany({
      where: {
        createdAt: { lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) },
      },
    });

    logger.log('Cleanup complete', { deletedCount: deleted.count });

    return { deleted: deleted.count };
  },
});

// Weekly report
export const weeklyReport = schedules.task({
  id: 'weekly-report',
  cron: '0 9 * * 1',  // Monday 9 AM
  run: async () => {
    const stats = await generateWeeklyStats();
    await sendReportEmail(stats);
    return stats;
  },
});

### 批量处理

分批处理大型数据集

**适用场景**：需要带速率限制处理大量项目

import { task, logger, wait } from '@trigger.dev/sdk/v3';

export const processBatch = task({
  id: 'process-batch',
  queue: {
    concurrencyLimit: 5,  // Only 5 running at once
  },
  run: async (payload: { items: string[] }) => {
    const results = [];

    for (const item of payload.items) {
      logger.log('Processing item', { item });

      const result = await processItem(item);
      results.push(result);

      // Respect rate limits
      await wait.for({ seconds: 1 });
    }

    return { processed: results.length, results };
  },
});

// Trigger batch processing
export const startBatchJob = task({
  id: 'start-batch',
  run: async (payload: { datasetId: string }) => {
    const items = await fetchDataset(payload.datasetId);

    // Split into chunks of 100
    const chunks = chunkArray(items, 100);

    // Trigger parallel batch tasks
    const handles = await Promise.all(
      chunks.map(chunk => processBatch.trigger({ items: chunk }))
    );

    logger.log('Started batch processing', {
      totalItems: items.length,
      batches: chunks.length,
    });

    return { batches: handles.length };
  },
});

### Webhook 处理器

可靠处理 Webhook 并实现去重

**适用场景**：处理来自 Stripe、GitHub 等的 Webhook

import { task, logger, idempotencyKeys } from '@trigger.dev/sdk/v3';

export const handleStripeEvent = task({
  id: 'handle-stripe-event',
  run: async (payload: {
    eventId: string;
    type: string;
    data: any;
  }) => {
    // Idempotency based on Stripe event ID
    const idempotencyKey = await idempotencyKeys.create(payload.eventId);

    if (idempotencyKey.isNew === false) {
      logger.log('Duplicate event, skipping', { eventId: payload.eventId });
      return { skipped: true };
    }

    logger.log('Processing Stripe event', {
      type: payload.type,
      eventId: payload.eventId,
    });

    switch (payload.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(payload.data);
        break;
      case 'customer.subscription.updated':
        await handleSubscriptionUpdate(payload.data);
        break;
    }

    return { processed: true, type: payload.type };
  },
});

## 关键问题

### 任务超时导致执行终止且无明确错误

严重程度：CRITICAL

场景：长时间运行的 AI 任务或批处理突然停止，日志中无错误。任务在仪表板中显示失败但无堆栈跟踪，数据部分处理。

症状：
- 任务失败且无错误消息
- 数据部分处理
- 本地正常，生产环境失败
- 仪表板显示"Task timed out"

原因：
Trigger.dev 有执行超时限制（默认值因计划而异）。超时后任务会被强制终止。如果未记录进度，将无法知道停在哪里。这在可能耗时数分钟的 AI 任务中尤为常见。

修复建议：

# 配置显式超时：
```typescript
export const processDocument = task({
  id: 'process-document',
  machine: {
    preset: 'large-2x',  // More resources = longer allowed time
  },
  run: async (payload) => {
    logger.log('Starting document processing', { docId: payload.id });

    // Log progress at each step
    logger.log('Step 1: Extracting text');
    const text = await extractText(payload.fileUrl);

    logger.log('Step 2: Generating embeddings', { textLength: text.length });
    const embeddings = await generateEmbeddings(text);

    logger.log('Step 3: Storing vectors', { count: embeddings.length });
    await storeVectors(embeddings);

    logger.log('Completed successfully');
    return { processed: true };
  },
});
```

# 对于超长任务，拆分为子任务：
- 使用 triggerAndWait 处理顺序步骤
- 每个子任务有独立超时
- 进度在仪表板中可见

### 不可序列化载荷导致任务静默失败

严重程度：CRITICAL

场景：在载荷中传递 Date 对象、类实例或循环引用。任务入队但从未运行，或运行时值为 undefined/null。

症状：
- 任务中载荷值为 undefined
- Date 对象变为字符串
- 类方法不可用
- "Converting circular structure to JSON"

原因：
Trigger.dev 将载荷序列化为 JSON。Date 变为字符串，类实例丢失方法，函数消失，循环引用抛出异常。任务看到的数据与发送的不同。

修复建议：

# 始终使用普通对象：
```typescript
// WRONG - Date becomes string
await myTask.trigger({ createdAt: new Date() });

// RIGHT - ISO string
await myTask.trigger({ createdAt: new Date().toISOString() });

// WRONG - Class instance
await myTask.trigger({ user: new User(data) });

// RIGHT - Plain object
await myTask.trigger({ user: { id: data.id, email: data.email } });

// WRONG - Circular reference
const obj = { parent: null };
obj.parent = obj;
await myTask.trigger(obj);  // Throws!
```

# 在任务中按需重组：
```typescript
run: async (payload: { createdAt: string }) => {
  const date = new Date(payload.createdAt);
  // ...
}
```

### 环境变量未同步到 Trigger.dev 云

严重程度：CRITICAL

场景：任务本地正常但生产环境失败。Vercel 中存在的环境变量在 Trigger.dev 中未定义。API 调用失败，数据库连接失败。

症状：
- "Environment variable not found"
- 生产任务中 API 调用返回 401
- 开发环境正常，生产环境失败
- 任务中数据库连接错误

原因：
Trigger.dev 在其独立云中运行任务，与 Vercel/Railway 部署分离。环境变量必须在两处配置，不会自动同步。

修复建议：

# 同步环境变量到 Trigger.dev：
1. 进入 Trigger.dev 仪表板
2. Project Settings > Environment Variables
3. 添加所有必需的环境变量

# 或使用 CLI：
```bash
# Create .env.trigger file
DATABASE_URL=postgres://...
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_live_...

# Push to Trigger.dev
npx trigger.dev@latest env push
```

# 常见缺失变量：
- DATABASE_URL
- OPENAI_API_KEY / ANTHROPIC_API_KEY
- STRIPE_SECRET_KEY
- 服务 API 密钥
- 内部服务 URL

# 在预发布环境测试：
Trigger.dev 有独立环境 - 也要配置预发布环境

### SDK 版本在 CLI 和包之间不匹配

严重程度：HIGH

场景：更新了 @trigger.dev/sdk 但忘记更新 CLI，或反之。任务注册失败，出现奇怪的类型错误，开发服务器崩溃。

症状：
- 任务未出现在仪表板
- trigger.config.ts 中出现类型错误
- "Failed to register task"
- 开发服务器启动时崩溃

原因：
Trigger.dev SDK 和 CLI 必须使用兼容版本。版本间的破坏性变更会导致注册失败。CLI 生成的类型必须与 SDK 匹配。

修复建议：

# 始终一起更新：
```bash
# Update both SDK and CLI
npm install @trigger.dev/sdk@latest
npx trigger.dev@latest dev

# Or pin to same version
npm install @trigger.dev/sdk@3.3.0
npx trigger.dev@3.3.0 dev
```

# 检查版本：
```bash
npx trigger.dev@latest --version
npm list @trigger.dev/sdk
```

# 在 CI/CD 中：
```yaml
- run: npm install @trigger.dev/sdk@${{ env.TRIGGER_VERSION }}
- run: npx trigger.dev@${{ env.TRIGGER_VERSION }} deploy
```

### 任务重试导致重复副作用

严重程度：HIGH

场景：任务发送邮件后下一步失败。重试时再次发送邮件。客户收到 3 封相同邮件，或 3 次 Stripe 扣款，或 3 条 Slack 消息。

症状：
- 重试时邮件重复
- 同一订单多次扣款
- Webhook 重复投递
- 数据重复插入

原因：
Trigger.dev 从头开始重试失败的任务。如果任务在失败点之前有副作用，这些副作用会再次执行。没有幂等性就会产生重复。

修复建议：

# 使用幂等键：
```typescript
import { task, idempotencyKeys } from '@trigger.dev/sdk/v3';

export const sendOrderEmail = task({
  id: 'send-order-email',
  run: async (payload: { orderId: string }) => {
    // Check if already sent
    const key = await idempotencyKeys.create(`email-${payload.orderId}`);

    if (!key.isNew) {
      logger.log('Email already sent, skipping');
      return { skipped: true };
    }

    await sendEmail(payload.orderId);
    return { sent: true };
  },
});
```

# 替代方案：在数据库中跟踪
```typescript
const existing = await db.emailLogs.findUnique({
  where: { orderId_type: { orderId, type: 'order_confirmation' } }
});

if (existing) {
  logger.log('Already sent');
  return;
}

await sendEmail(orderId);
await db.emailLogs.create({ data: { orderId, type: 'order_confirmation' } });
```

### 高并发压垮下游服务

严重程度：HIGH

场景：突发 1000 个任务同时触发，全部同时请求 OpenAI API。触发速率限制，全部失败。重试，再次触发限制。恶性循环。

症状：
- 速率限制错误 (429)
- 数据库连接池耗尽
- API 返回"too many requests"
- 大量任务失败

原因：
Trigger.dev 可扩展处理大量并发任务，但下游 API（OpenAI、数据库、外部服务）有速率限制。没有并发控制会压垮它们。

修复建议：

# 设置队列并发限制：
```typescript
export const callOpenAI = task({
  id: 'call-openai',
  queue: {
    concurrencyLimit: 10,  // Only 10 running at once
  },
  run: async (payload) => {
    // Protected by concurrency limit
    return await openai.chat.completions.create(payload);
  },
});
```

# 对于有速率限制的 API：
```typescript
export const callRateLimitedAPI = task({
  id: 'call-api',
  queue: {
    concurrencyLimit: 5,
  },
  retry: {
    maxAttempts: 5,
    minTimeoutInMs: 5000,  // Wait before retry
    factor: 2,  // Exponential backoff
  },
  run: async (payload) => {
    // Add delay between calls
    await wait.for({ milliseconds: 200 });
    return await externalAPI.call(payload);
  },
});
```

# 保守起步：
- 外部 API：5-10
- 数据库：20-50
- 根据监控逐步增加

### trigger.config.ts 不在项目根目录

严重程度：HIGH

场景：运行 npx trigger.dev dev 但 CLI 找不到配置，或配置存在但位置错误（monorepo 问题）。

症状：
- "Could not find trigger.config.ts"
- 任务未被发现
- 仪表板任务列表为空
- 某个包正常，其他包不行

原因：
CLI 在当前工作目录查找 trigger.config.ts。在 monorepo 中，必须从包目录运行，而非根目录。位置错误 = 任务未被发现。

修复建议：

# 配置必须在包根目录：
```
my-app/
├── trigger.config.ts  <- Here
├── package.json
├── src/
│   └── trigger/
│       └── tasks.ts
```

# 在 monorepo 中：
```
monorepo/
├── apps/
│   └── web/
│       ├── trigger.config.ts  <- Here, not at monorepo root
│       ├── package.json
│       └── src/trigger/

# Run from package directory
cd apps/web && npx trigger.dev dev
```

# 指定配置位置：
```bash
npx trigger.dev dev --config ./apps/web/trigger.config.ts
```

### 循环中使用 wait.for 导致内存问题

严重程度：MEDIUM

场景：处理数千个项目时在每项之间使用 wait.for。任务内存增长，最终因内存不足被终止。

症状：
- 任务因内存被终止
- 任务执行缓慢
- 状态 blob 过大错误
- 小批量正常，大批量失败

原因：
每次 wait.for 创建检查点状态。在数千次迭代的循环中，状态会累积。任务的状态 blob 增长直到达到内存限制。

修复建议：

# 批量处理而非逐个等待：
```typescript
// WRONG - Wait per item
for (const item of items) {
  await processItem(item);
  await wait.for({ milliseconds: 100 });  // 1000 waits = bloated state
}

// RIGHT - Batch processing
const chunks = chunkArray(items, 50);
for (const chunk of chunks) {
  await Promise.all(chunk.map(processItem));
  await wait.for({ milliseconds: 500 });  // Only 20 waits
}
```

# 对于超大数据集，使用子任务：
```typescript
export const processAll = task({
  id: 'process-all',
  run: async (payload: { items: string[] }) => {
    const chunks = chunkArray(payload.items, 100);

    // Each chunk is a separate task
    await Promise.all(
      chunks.map(chunk =>
        processChunk.triggerAndWait({ items: chunk })
      )
    );
  },
});
```

### 使用原始 SDK 而非 Trigger.dev 集成

严重程度：MEDIUM

场景：直接使用 OpenAI SDK。API 调用失败，无自动重试。未处理速率限制，需手动实现所有容错。

症状：
- 任务中包含手动重试逻辑
- 未处理速率限制错误
- API 调用无自动日志
- 错误处理不一致

原因：
Trigger.dev 集成封装了 SDK，提供自动重试、速率限制处理和适当的日志记录。使用原始 SDK 意味着失去这些功能，需自行实现。

修复建议：

# 使用可用的集成：
```typescript
// WRONG - Raw SDK
import OpenAI from 'openai';
const openai = new OpenAI();

// RIGHT - Trigger.dev integration
import { openai } from '@trigger.dev/openai';

const openaiClient = openai.configure({
  id: 'openai',
  apiKey: process.env.OPENAI_API_KEY,
});

// Now has automatic retries and rate limiting
export const generateContent = task({
  id: 'generate-content',
  run: async (payload) => {
    const response = await openaiClient.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [{ role: 'user', content: payload.prompt }],
    });
    return response;
  },
});
```

# 可用集成：
- @trigger.dev/openai
- @trigger.dev/anthropic
- @trigger.dev/resend
- @trigger.dev/slack
- @trigger.dev/stripe

### 未运行开发服务器时触发任务

严重程度：MEDIUM

场景：调用 task.trigger() 但无任何响应，也没有错误。任务消失在虚无中，开发服务器未运行。

症状：
- 触发器不运行
- 仪表板无任务
- 无错误，静默
- 生产环境正常，开发环境不行

原因：
开发环境中，任务通过本地开发服务器（npx trigger.dev dev）运行。如果未运行，触发器会排队或静默失败，取决于配置。生产环境行为不同。

修复建议：

# 开发期间始终运行开发服务器：
```bash
# Terminal 1: Your app
npm run dev

# Terminal 2: Trigger.dev dev server
npx trigger.dev dev
```

# 检查开发服务器已连接：
- 应显示 "Connected to Trigger.dev"
- 任务应出现在控制台
- 仪表板显示任务注册

# 在 package.json 中：
```json
{
  "scripts": {
    "dev": "next dev",
    "trigger:dev": "trigger.dev dev",
    "dev:all": "concurrently \"npm run dev\" \"npm run trigger:dev\""
  }
}
```

## 验证检查

### 任务无日志

严重程度：WARNING

消息：任务无日志。添加 logger.log() 调用以便在生产环境中调试。

修复操作：从 '@trigger.dev/sdk/v3' 导入 { logger } 并添加日志语句

### 任务无错误处理

严重程度：ERROR

消息：任务缺少显式错误处理。未处理的错误可能导致不明确的失败。

修复操作：用 try/catch 包装任务逻辑并记录带上下文的错误

### 任务无并发限制

严重程度：WARNING

消息：任务无并发限制。高负载可能压垮下游服务。

修复操作：添加 queue: { concurrencyLimit: 10 } 保护 API 和数据库

### 触发载荷中的 Date 对象

严重程度：ERROR

消息：Date 对象会被序列化为字符串。请改用 ISO 字符串格式。

修复操作：使用 date.toISOString() 替代 new Date()

### 触发载荷中的类实例

严重程度：ERROR

消息：类实例在序列化时丢失方法。请使用普通对象。

修复操作：触发前将类实例转换为普通对象

### 任务无显式 ID

严重程度：ERROR

消息：任务必须有显式 id 属性才能注册。

修复操作：在任务定义中添加 id: 'my-task-name'

### Trigger.dev API 密钥硬编码

严重程度：CRITICAL

消息：Trigger.dev API 密钥不应硬编码 - 请使用 TRIGGER_SECRET_KEY 环境变量

修复操作：移除硬编码密钥并使用 process.env.TRIGGER_SECRET_KEY

### 使用原始 OpenAI SDK 而非集成

严重程度：WARNING

消息：考虑使用 @trigger.dev/openai 实现自动重试和速率限制

修复操作：替换为：import { openai } from '@trigger.dev/openai'

### 使用原始 Anthropic SDK 而非集成

严重程度：WARNING

消息：考虑使用 @trigger.dev/anthropic 实现自动重试和速率限制

修复操作：替换为：import { anthropic } from '@trigger.dev/anthropic'

### 循环内使用 wait.for

严重程度：WARNING

消息：循环中的 wait.for 会创建大量检查点。考虑改用批量处理。

修复操作：批量处理项目并减少等待次数，或拆分为子任务

## 协作

### 委派触发条件

- redis|bullmq|traditional queue -> bullmq-specialist（需要 Redis 支持的队列而非托管服务）
- vercel|deployment|serverless -> vercel-deployment（Trigger.dev 需要部署配置）
- database|postgres|supabase -> supabase-backend（任务需要数据库访问）
- openai|anthropic|ai model|llm -> llm-architect（任务需要 AI 模型集成）
- event-driven|event sourcing|fan out -> inngest（需要纯事件驱动模型）

### AI 后台处理

技能：trigger-dev, llm-architect, nextjs-app-router, supabase-backend

工作流：

```
1. User triggers via UI (nextjs-app-router)
2. Task queued (trigger-dev)
3. AI processing (llm-architect)
4. Results stored (supabase-backend)
```

### Webhook 处理流水线

技能：trigger-dev, stripe-integration, email-systems, supabase-backend

工作流：

```
1. Webhook received (stripe-integration)
2. Task triggered (trigger-dev)
3. Database updated (supabase-backend)
4. Notification sent (email-systems)
```

### 批量数据处理

技能：trigger-dev, supabase-backend, backend

工作流：

```
1. Batch job triggered (backend)
2. Data chunked and processed (trigger-dev)
3. Results aggregated (supabase-backend)
```

### 定时报告

技能：trigger-dev, supabase-backend, email-systems

工作流：

```
1. Cron triggers task (trigger-dev)
2. Data aggregated (supabase-backend)
3. Report generated and sent (email-systems)
```

## 相关技能

适用场景：`nextjs-app-router`, `vercel-deployment`, `ai-agents-architect`, `llm-architect`, `email-systems`, `stripe-integration`

## 触发词

- 用户提及或暗示：trigger.dev
- 用户提及或暗示：trigger dev
- 用户提及或暗示：background task
- 用户提及或暗示：ai background job
- 用户提及或暗示：long running task
- 用户提及或暗示：integration task
- 用户提及或暗示：scheduled task

## 限制

- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家评审的替代品
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来寻求澄清