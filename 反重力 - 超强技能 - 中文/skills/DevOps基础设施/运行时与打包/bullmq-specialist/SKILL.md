---
name: bullmq-specialist
description: BullMQ 专家，专注于 Redis 支持的作业队列、后台处理和 Node.js/TypeScript 应用中的可靠异步执行。当用户要求'BullMQ'、'Redis队列'、'后台作业'、'作业调度'、'异步处理'时使用。
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# BullMQ Specialist

BullMQ 专家，专注于 Redis 支持的作业队列、后台处理和 Node.js/TypeScript 应用中的可靠异步执行。

## 原则

- 从生产者角度看，作业是即发即弃的——让队列负责投递
- 始终设置显式作业选项——默认值很少匹配你的场景
- 幂等性是你的责任——作业可能运行不止一次
- 退避策略防止惊群效应——指数退避优于线性退避
- 死信队列不是可选的——失败的作业需要归宿
- 并发限制保护下游服务——从保守值开始
- 作业数据应保持精简——传递 ID，而非完整负载
- 优雅关停防止孤立作业——正确处理 SIGTERM

## 能力

- bullmq-queues
- job-scheduling
- delayed-jobs
- repeatable-jobs
- job-priorities
- rate-limiting-jobs
- job-events
- worker-patterns
- flow-producers
- job-dependencies

## 范围

- redis-infrastructure -> redis-specialist
- serverless-queues -> upstash-qstash
- workflow-orchestration -> temporal-craftsman
- event-sourcing -> event-architect
- email-delivery -> email-systems

## 工具

### 核心

- bullmq
- ioredis

### 托管

- upstash
- redis-cloud
- elasticache
- railway

### 监控

- bull-board
- arena
- bullmq-pro

### 模式

- delayed-jobs
- repeatable-jobs
- job-flows
- rate-limiting
- sandboxed-processors

## 模式

### 基本队列配置

生产级 BullMQ 队列，配置完善

**何时使用**：开始任何新的队列实现

import { Queue, Worker, QueueEvents } from 'bullmq';
import IORedis from 'ioredis';

// Shared connection for all queues
const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null,  // Required for BullMQ
  enableReadyCheck: false,
});

// Create queue with sensible defaults
const emailQueue = new Queue('emails', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 1000,
    },
    removeOnComplete: { count: 1000 },
    removeOnFail: { count: 5000 },
  },
});

// Worker with concurrency limit
const worker = new Worker('emails', async (job) => {
  await sendEmail(job.data);
}, {
  connection,
  concurrency: 5,
  limiter: {
    max: 100,
    duration: 60000,  // 100 jobs per minute
  },
});

// Handle events
worker.on('failed', (job, err) => {
  console.error(`Job ${job?.id} failed:`, err);
});

### 延迟与定时作业

在特定时间或延迟后运行的作业

**何时使用**：调度未来任务、提醒或定时操作

// Delayed job - runs once after delay
await queue.add('reminder', { userId: 123 }, {
  delay: 24 * 60 * 60 * 1000,  // 24 hours
});

// Repeatable job - runs on schedule
await queue.add('daily-digest', { type: 'summary' }, {
  repeat: {
    pattern: '0 9 * * *',  // Every day at 9am
    tz: 'America/New_York',
  },
});

// Remove repeatable job
await queue.removeRepeatable('daily-digest', {
  pattern: '0 9 * * *',
  tz: 'America/New_York',
});

### 作业流与依赖

具有父子关系的复杂多步作业处理

**何时使用**：作业依赖其他作业先完成

import { FlowProducer } from 'bullmq';

const flowProducer = new FlowProducer({ connection });

// Parent waits for all children to complete
await flowProducer.add({
  name: 'process-order',
  queueName: 'orders',
  data: { orderId: 123 },
  children: [
    {
      name: 'validate-inventory',
      queueName: 'inventory',
      data: { orderId: 123 },
    },
    {
      name: 'charge-payment',
      queueName: 'payments',
      data: { orderId: 123 },
    },
    {
      name: 'notify-warehouse',
      queueName: 'notifications',
      data: { orderId: 123 },
    },
  ],
});

### 优雅关停

正确关闭 Worker 而不丢失作业

**何时使用**：部署或重启 Worker 时

const shutdown = async () => {
  console.log('Shutting down gracefully...');

  // Stop accepting new jobs
  await worker.pause();

  // Wait for current jobs to finish (with timeout)
  await worker.close();

  // Close queue connection
  await queue.close();

  process.exit(0);
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

### Bull Board 仪表盘

BullMQ 队列的可视化监控

**何时使用**：需要查看队列状态和作业状态

import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

createBullBoard({
  queues: [
    new BullMQAdapter(emailQueue),
    new BullMQAdapter(orderQueue),
  ],
  serverAdapter,
});

app.use('/admin/queues', serverAdapter.getRouter());

## 验证检查

### Redis 连接缺少 maxRetriesPerRequest

严重级别：ERROR

BullMQ 要求 maxRetriesPerRequest 设为 null 才能正确处理重连

消息：BullMQ 队列/Worker 创建时 Redis 连接未设置 maxRetriesPerRequest: null。这会导致 Redis 连接问题时 Worker 停止工作。

### 缺少停滞作业事件处理器

严重级别：WARNING

Worker 应处理 stalled 事件以检测崩溃的 Worker

消息：Worker 创建时未设置 'stalled' 事件处理器。停滞作业表明 Worker 崩溃，应被监控。

### 缺少失败作业事件处理器

严重级别：WARNING

Worker 应处理 failed 事件以便监控和告警

消息：Worker 创建时未设置 'failed' 事件处理器。失败作业应被记录和监控。

### 缺少优雅关停处理

严重级别：WARNING

Worker 应在 SIGTERM/SIGINT 时优雅关停

消息：Worker 文件缺少优雅关停处理。部署时作业可能变为孤立状态。

### 在请求处理器中 await queue.add

严重级别：INFO

请求处理器中的队列添加应为即发即弃

消息：在请求处理器中 await 了 queue.add。考虑使用即发即弃方式以加快响应。

### 作业负载中可能存在大数据

严重级别：WARNING

作业数据应保持精简——传递 ID 而非完整对象

消息：作业似乎包含大量内联数据。应传递 ID 而非完整对象，以降低 Redis 内存占用。

### 作业未配置超时

严重级别：INFO

作业应设置超时以防止无限执行

消息：添加作业时未设置显式超时。建议添加超时以防止作业卡死。

### 重试未配置退避策略

严重级别：WARNING

重试应使用指数退避以避免惊群效应

消息：作业设置了重试次数但未配置退避策略。应使用指数退避以防止惊群效应。

### 可重复作业未指定时区

严重级别：WARNING

可重复作业应指定时区以避免夏令时问题

消息：可重复作业未指定时区。将使用服务器本地时间，可能因夏令时偏移。

### Worker 并发度可能过高

严重级别：INFO

高并发可能压垮下游服务

消息：Worker 并发度较高。请确保下游服务能承受此负载（数据库连接、API 速率限制）。

## 协作

### 委派触发条件

- redis infrastructure|redis cluster|memory tuning -> redis-specialist（队列需要 Redis 基础设施）
- serverless queue|edge queue|no redis -> upstash-qstash（需要无需管理 Redis 的队列）
- complex workflow|saga|compensation|long-running -> temporal-craftsman（需要超越简单作业的工作流编排）
- event sourcing|CQRS|event streaming -> event-architect（需要事件驱动架构）
- deploy|kubernetes|scaling|infrastructure -> devops（队列需要基础设施）
- monitor|metrics|alerting|dashboard -> performance-hunter（队列需要监控）

### 邮件队列技术栈

技能：bullmq-specialist, email-systems, redis-specialist

工作流：

```
1. 收到邮件请求 (API)
2. 带速率限制地入队 (bullmq-specialist)
3. Worker 带退避策略处理 (bullmq-specialist)
4. 通过服务商发送邮件 (email-systems)
5. 在 Redis 中跟踪状态 (redis-specialist)
```

### 后台处理技术栈

技能：bullmq-specialist, backend, devops

工作流：

```
1. API 接收请求 (backend)
2. 长任务入队后台处理 (bullmq-specialist)
3. Worker 异步处理 (bullmq-specialist)
4. 存储结果/通知 (backend)
5. 按负载扩缩 Worker (devops)
```

### AI 处理流水线

技能：bullmq-specialist, ai-workflow-automation, performance-hunter

工作流：

```
1. 提交 AI 任务 (ai-workflow-automation)
2. 创建带依赖的作业流 (bullmq-specialist)
3. Worker 处理各阶段 (bullmq-specialist)
4. 性能监控 (performance-hunter)
5. 汇总结果 (ai-workflow-automation)
```

### 定时任务技术栈

技能：bullmq-specialist, backend, redis-specialist

工作流：

```
1. 定义可重复作业 (bullmq-specialist)
2. 带时区的 Cron 表达式 (bullmq-specialist)
3. 按计划执行作业 (bullmq-specialist)
4. 在 Redis 中管理状态 (redis-specialist)
5. 处理结果 (backend)
```

## 相关技能

配合使用：`redis-specialist`、`backend`、`nextjs-app-router`、`email-systems`、`ai-workflow-automation`、`performance-hunter`

## 何时使用
- 用户提及或暗示：bullmq
- 用户提及或暗示：bull queue
- 用户提及或暗示：redis queue
- 用户提及或暗示：background job
- 用户提及或暗示：job queue
- 用户提及或暗示：delayed job
- 用户提及或暗示：repeatable job
- 用户提及或暗示：worker process
- 用户提及或暗示：job scheduling
- 用户提及或暗示：async processing

## 局限
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代针对特定环境的验证、测试或专家评审。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
