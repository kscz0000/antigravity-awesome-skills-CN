---
name: workflow-automation
description: 工作流自动化是让 AI 智能体可靠运行的基础设施。在 10 步支付流程中若没有持久执行，一次网络抖动就意味着资金损失和客户投诉；有了持久执行，工作流就能精确地从中断处恢复。触发词：workflow、automation、n8n、temporal、inngest、step function、background job、durable execution、event-driven、scheduled task、job queue、cron、trigger
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 工作流自动化

工作流自动化是让 AI 智能体可靠运行的基础设施。在 10 步支付流程中若没有持久执行，一次网络抖动就意味着资金损失和客户投诉；有了持久执行，工作流就能精确地从中断处恢复。

本技能涵盖将脆弱脚本转变为生产级自动化所需的平台（n8n、Temporal、Inngest）和模式（顺序、并行、编排器-工作者）。

关键洞见：各平台有不同的取舍。n8n 侧重易用性，Temporal 侧重正确性、Inngest 侧重开发者体验。依据实际需求选择，而不是追逐热度。

## 原则

- 对于涉及资金或状态关键的工作流，持久执行不可妥协
- 事件是工作流触发器的通用语言
- 步骤即检查点——每一步都应能独立重试
- 从简单开始，仅在可靠性要求时才增加复杂度
- 可观测性不是可选项——你需要看到工作流在哪里失败
- 工作流与智能体协同演进——为两者同时设计

## 能力

- workflow-automation
- workflow-orchestration
- durable-execution
- event-driven-workflows
- step-functions
- job-queues
- background-jobs
- scheduled-tasks

## 范围

- multi-agent-coordination → multi-agent-orchestration
- ci-cd-pipelines → devops
- data-pipelines → data-engineer
- api-design → api-designer

## 工具

### 平台

- n8n - 适用场景：低代码自动化、快速原型、非技术用户 备注：可自托管，400+ 集成，适合可视化工作流
- Temporal - 适用场景：关键任务工作流、金融交易、微服务 备注：最强大的持久性保证，学习曲线较陡
- Inngest - 适用场景：事件驱动的无服务器架构、TypeScript 代码库、AI 工作流 备注：最佳开发者体验，兼容任何托管环境
- AWS Step Functions - 适用场景：AWS 原生技术栈、已有 Lambda 函数 备注：与 AWS 深度集成，基于 JSON 的工作流定义
- Azure Durable Functions - 适用场景：Azure 技术栈、.NET 或 TypeScript 备注：良好的 AI 智能体支持，支持检查点与重放

## 模式

### 顺序工作流模式

步骤按序执行，前一步的输出成为后一步的输入

**适用场景**：内容流水线、数据处理、有序操作

# 顺序工作流：

"""
步骤 1 → 步骤 2 → 步骤 3 → 输出
  ↓         ↓         ↓
（每一步的检查点）
"""

## Inngest 示例（TypeScript）
"""
import { inngest } from "./client";

export const processOrder = inngest.createFunction(
  { id: "process-order" },
  { event: "order/created" },
  async ({ event, step }) => {
    // Step 1: Validate order
    const validated = await step.run("validate-order", async () => {
      return validateOrder(event.data.order);
    });

    // Step 2: Process payment (durable - survives crashes)
    const payment = await step.run("process-payment", async () => {
      return chargeCard(validated.paymentMethod, validated.total);
    });

    // Step 3: Create shipment
    const shipment = await step.run("create-shipment", async () => {
      return createShipment(validated.items, validated.address);
    });

    // Step 4: Send confirmation
    await step.run("send-confirmation", async () => {
      return sendEmail(validated.email, { payment, shipment });
    });

    return { success: true, orderId: event.data.orderId };
  }
);
"""

## Temporal 示例（TypeScript）
"""
import { proxyActivities } from '@temporalio/workflow';
import type * as activities from './activities';

const { validateOrder, chargeCard, createShipment, sendEmail } =
  proxyActivities<typeof activities>({
    startToCloseTimeout: '30 seconds',
    retry: {
      maximumAttempts: 3,
      backoffCoefficient: 2,
    }
  });

export async function processOrderWorkflow(order: Order): Promise<void> {
  const validated = await validateOrder(order);
  const payment = await chargeCard(validated.paymentMethod, validated.total);
  const shipment = await createShipment(validated.items, validated.address);
  await sendEmail(validated.email, { payment, shipment });
}
"""

## n8n 模式
"""
[Webhook: order.created]
    ↓
[HTTP Request: Validate Order]
    ↓
[HTTP Request: Process Payment]
    ↓
[HTTP Request: Create Shipment]
    ↓
[Send Email: Confirmation]

Configure each node with retry on failure.
Use Error Trigger for dead letter handling.
"""

### 并行工作流模式

独立步骤同时运行，汇总结果

**适用场景**：多个独立分析、来自多个来源的数据

# 并行工作流：

"""
        ┌→ 步骤 A ─┐
输入 ──┼→ 步骤 B ─┼→ 汇总 → 输出
        └→ 步骤 C ─┘
"""

## Inngest 示例
"""
export const analyzeDocument = inngest.createFunction(
  { id: "analyze-document" },
  { event: "document/uploaded" },
  async ({ event, step }) => {
    // Run analyses in parallel
    const [security, performance, compliance] = await Promise.all([
      step.run("security-analysis", () =>
        analyzeForSecurityIssues(event.data.document)
      ),
      step.run("performance-analysis", () =>
        analyzeForPerformance(event.data.document)
      ),
      step.run("compliance-analysis", () =>
        analyzeForCompliance(event.data.document)
      ),
    ]);

    // Aggregate results
    const report = await step.run("generate-report", () =>
      generateReport({ security, performance, compliance })
    );

    return report;
  }
);
"""

## AWS Step Functions（Amazon States Language）
"""
{
  "Type": "Parallel",
  "Branches": [
    {
      "StartAt": "SecurityAnalysis",
      "States": {
        "SecurityAnalysis": {
          "Type": "Task",
          "Resource": "arn:aws:lambda:...:security-analyzer",
          "End": true
        }
      }
    },
    {
      "StartAt": "PerformanceAnalysis",
      "States": {
        "PerformanceAnalysis": {
          "Type": "Task",
          "Resource": "arn:aws:lambda:...:performance-analyzer",
          "End": true
        }
      }
    }
  ],
  "Next": "AggregateResults"
}
"""

### 编排器-工作者模式

中央协调器将任务分派给专门的工作者

**适用场景**：需要不同专业能力的复杂任务、动态子任务创建

# 编排器-工作者模式：

"""
┌─────────────────────────────────────┐
│            编排器                   │
│  - 分析任务                          │
│  - 创建子任务                        │
│  - 分派给工作者                      │
│  - 汇总结果                          │
└─────────────────────────────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌───────┐  ┌───────┐  ┌───────┐
│工作者1│  │工作者2│  │工作者3│
│创建   │  │修改   │  │删除   │
└───────┘  └───────┘  └───────┘
"""

## Temporal 示例
"""
export async function orchestratorWorkflow(task: ComplexTask) {
  // Orchestrator decides what work needs to be done
  const plan = await analyzeTask(task);

  // Dispatch to specialized worker workflows
  const results = await Promise.all(
    plan.subtasks.map(subtask => {
      switch (subtask.type) {
        case 'create':
          return executeChild(createWorkerWorkflow, { args: [subtask] });
        case 'modify':
          return executeChild(modifyWorkerWorkflow, { args: [subtask] });
        case 'delete':
          return executeChild(deleteWorkerWorkflow, { args: [subtask] });
      }
    })
  );

  // Aggregate results
  return aggregateResults(results);
}
"""

## Inngest 与 AI 编排
"""
export const aiOrchestrator = inngest.createFunction(
  { id: "ai-orchestrator" },
  { event: "task/complex" },
  async ({ event, step }) => {
    // AI decides what needs to be done
    const plan = await step.run("create-plan", async () => {
      return await llm.chat({
        messages: [
          { role: "system", content: "Break this task into subtasks..." },
          { role: "user", content: event.data.task }
        ]
      });
    });

    // Execute each subtask as a durable step
    const results = [];
    for (const subtask of plan.subtasks) {
      const result = await step.run(`execute-${subtask.id}`, async () => {
        return executeSubtask(subtask);
      });
      results.push(result);
    }

    // Final synthesis
    return await step.run("synthesize", async () => {
      return synthesizeResults(results);
    });
  }
);
"""

### 事件驱动触发模式

工作流由事件触发，而非按计划触发

**适用场景**：响应式系统、用户操作、Webhook 集成

# 事件驱动触发：

## Inngest 基于事件
"""
// Define events with TypeScript types
type Events = {
  "user/signed.up": {
    data: { userId: string; email: string };
  };
  "order/completed": {
    data: { orderId: string; total: number };
  };
};

// Function triggered by event
export const onboardUser = inngest.createFunction(
  { id: "onboard-user" },
  { event: "user/signed.up" },  // Trigger on this event
  async ({ event, step }) => {
    // Wait 1 hour, then send welcome email
    await step.sleep("wait-for-exploration", "1 hour");

    await step.run("send-welcome", async () => {
      return sendWelcomeEmail(event.data.email);
    });

    // Wait 3 days for engagement check
    await step.sleep("wait-for-engagement", "3 days");

    const engaged = await step.run("check-engagement", async () => {
      return checkUserEngagement(event.data.userId);
    });

    if (!engaged) {
      await step.run("send-nudge", async () => {
        return sendNudgeEmail(event.data.email);
      });
    }
  }
);

// Send events from anywhere
await inngest.send({
  name: "user/signed.up",
  data: { userId: "123", email: "user@example.com" }
});
"""

## n8n Webhook 触发
"""
[Webhook: POST /api/webhooks/order]
    ↓
[Switch: event.type]
    ↓ order.created
[处理新订单子工作流]
    ↓ order.cancelled
[处理取消子工作流]
"""

### 重试与恢复模式

自动重试并配合退避策略，处理死信

**适用场景**：任何涉及外部依赖的工作流

# 重试与恢复：

## Temporal 重试配置
"""
const activities = proxyActivities<typeof activitiesType>({
  startToCloseTimeout: '30 seconds',
  retry: {
    initialInterval: '1 second',
    backoffCoefficient: 2,
    maximumInterval: '1 minute',
    maximumAttempts: 5,
    nonRetryableErrorTypes: [
      'ValidationError',      // Don't retry validation failures
      'InsufficientFunds',    // Don't retry payment failures
    ]
  }
});
"""

## Inngest 重试配置
"""
export const processPayment = inngest.createFunction(
  {
    id: "process-payment",
    retries: 5,  // Retry up to 5 times
  },
  { event: "payment/initiated" },
  async ({ event, step, attempt }) => {
    // attempt is 0-indexed retry count

    const result = await step.run("charge-card", async () => {
      try {
        return await stripe.charges.create({...});
      } catch (error) {
        if (error.code === 'card_declined') {
          // Don't retry card declines
          throw new NonRetriableError("Card declined");
        }
        throw error;  // Retry other errors
      }
    });

    return result;
  }
);
"""

## 死信处理
"""
// n8n: Use Error Trigger node
[错误触发器]
    ↓
[记录到错误数据库]
    ↓
[向 Slack 发送告警]
    ↓
[在 Jira 创建工单]

// Inngest: Handle in onFailure
export const myFunction = inngest.createFunction(
  {
    id: "my-function",
    onFailure: async ({ error, event, step }) => {
      await step.run("alert-team", async () => {
        await slack.postMessage({
          channel: "#errors",
          text: `Function failed: ${error.message}`
        });
      });
    }
  },
  { event: "..." },
  async ({ step }) => { ... }
);
"""

### 定时工作流模式

基于时间的触发器，用于周期性任务

**适用场景**：日报、周期同步、批处理

# 定时工作流：

## Inngest Cron
"""
export const dailyReport = inngest.createFunction(
  { id: "daily-report" },
  { cron: "0 9 * * *" },  // Every day at 9 AM
  async ({ step }) => {
    const data = await step.run("gather-metrics", async () => {
      return gatherDailyMetrics();
    });

    await step.run("generate-report", async () => {
      return generateAndSendReport(data);
    });
  }
);

export const syncInventory = inngest.createFunction(
  { id: "sync-inventory" },
  { cron: "*/15 * * * *" },  // Every 15 minutes
  async ({ step }) => {
    await step.run("sync", async () => {
      return syncWithSupplier();
    });
  }
);
"""

## Temporal Cron 工作流
"""
// Schedule workflow to run on cron
const handle = await client.workflow.start(dailyReportWorkflow, {
  taskQueue: 'reports',
  workflowId: 'daily-report',
  cronSchedule: '0 9 * * *',  // 9 AM daily
});
"""

## n8n 定时触发
"""
[定时触发器：每天上午 9:00]
    ↓
[HTTP Request: 获取指标]
    ↓
[代码节点：生成报告]
    ↓
[发送邮件：报告]
"""

## 锐边

### 持久工作流中非幂等的步骤

严重程度：CRITICAL

场景：编写修改外部状态的工作流步骤

症状：
客户被重复扣款。邮件被发送多次。数据库记录被多次创建。工作流重试导致重复副作用。

失败原因：
持久执行在重启时会从开头重放工作流。如果第 3 步崩溃且工作流恢复，第 1 步和第 2 步会再次执行。没有幂等键，外部服务无法识别这些是重试。

推荐修复：

# 务必为外部调用使用幂等键：

## Stripe 示例：
await stripe.paymentIntents.create({
  amount: 1000,
  currency: 'usd',
  idempotency_key: `order-${orderId}-payment`  # 关键！
});

## 邮件示例：
await step.run("send-confirmation", async () => {
  const alreadySent = await checkEmailSent(orderId);
  if (alreadySent) return { skipped: true };
  return sendEmail(customer, orderId);
});

## 数据库示例：
await db.query(`
  INSERT INTO orders (id, ...) VALUES ($1, ...)
  ON CONFLICT (id) DO NOTHING
`, [orderId]);

# 从稳定的输入生成幂等键，而不是随机值

### 工作流连续运行数小时/数天而无检查点

严重程度：HIGH

场景：步骤稀疏的长时间运行工作流

症状：
内存占用持续增长。工作者超时。崩溃后进度丢失。出现"工作流超出最大时长"错误。

失败原因：
工作流在检查点前将状态保存在内存中。一个工作流如果每 24 小时只执行一步，状态就会累积 24 小时。工作者存在内存限制，函数存在执行时长限制。

推荐修复：

# 将长时间工作流拆分为带检查点的步骤：

## 错误 - 一个长步骤：
await step.run("process-all", async () => {
  for (const item of thousandItems) {
    await processItem(item);  // 数小时工作，仅一个检查点
  }
});

## 正确 - 许多小步骤：
for (const item of thousandItems) {
  await step.run(`process-${item.id}`, async () => {
    return processItem(item);  // 每项之后检查点
  });
}

## 对于很长的等待，使用 sleep：
await step.sleep("wait-for-trial", "14 days");
// 等待期间不消耗资源

## 考虑为长流程使用子工作流：
await step.invoke("process-batch", {
  function: batchProcessor,
  data: { items: batch }
});

### 活动未配置超时

严重程度：HIGH

场景：在工作流活动中调用外部服务

症状：
工作流无限期挂起。工作者池耗尽。死工作流既不完成也不失败。需要人工介入来终止卡住的工作流。

失败原因：
外部 API 可能永远挂起。没有超时，工作流会永远等待。与 HTTP 客户端不同，工作流活动在大多数平台中没有默认超时。

推荐修复：

# 务必为活动设置超时：

## Temporal：
const activities = proxyActivities<typeof activitiesType>({
  startToCloseTimeout: '30 seconds',  # 必填！
  scheduleToCloseTimeout: '5 minutes',
  heartbeatTimeout: '10 seconds',  # 用于长活动
  retry: {
    maximumAttempts: 3,
    initialInterval: '1 second',
  }
});

## Inngest：
await step.run("call-api", { timeout: "30s" }, async () => {
  return fetch(url, { signal: AbortSignal.timeout(25000) });
});

## AWS Step Functions：
{
  "Type": "Task",
  "TimeoutSeconds": 30,
  "HeartbeatSeconds": 10,
  "Resource": "arn:aws:lambda:..."
}

# 规则：活动超时 < 工作流超时

### 步骤/活动边界外的副作用

严重程度：CRITICAL

场景：编写在工作流重放期间运行的代码

症状：
重放时随机失败。"工作流已损坏"错误。重放与首次运行行为不同。非确定性错误。

失败原因：
工作流代码在每次重放时都会执行。如果在工作流代码中生成随机 ID，每次重放会得到不同的 ID。如果读取当前时间，每次会得到不同的时间。这会破坏确定性。

推荐修复：

# 错误 - 在工作流代码中产生副作用：
export async function orderWorkflow(order) {
  const orderId = uuid();  // 每次重放都不同！
  const now = new Date();  // 每次重放都不同！
  await activities.process(orderId, now);
}

# 正确 - 在活动中产生副作用：
export async function orderWorkflow(order) {
  const orderId = await activities.generateOrderId();  # 已记录
  const now = await activities.getCurrentTime();       # 已记录
  await activities.process(orderId, now);
}

# 同样正确 - Temporal 的 workflow.now() 与 sideEffect：
import { sideEffect } from '@temporalio/workflow';

const orderId = await sideEffect(() => uuid());
const now = workflow.now();  # 确定性重放安全的时间

# 在工作流代码中安全的副作用：
# - 读取函数参数
# - 简单计算（无随机性）
# - 日志记录（通常）

### 重试配置缺少指数退避

严重程度：MEDIUM

场景：为失败步骤配置重试行为

症状：
压垮失败的服务。触发限流。级联失败。重试风暴导致宕机。被外部 API 封禁。

失败原因：
当服务挣扎时，立即重试只会让情况更糟。100 个工作流同时立即重试 = 100 个请求砸向已经失败的服务。退避给服务恢复的时间。

推荐修复：

# 务必使用指数退避：

## Temporal：
const activities = proxyActivities({
  retry: {
    initialInterval: '1 second',
    backoffCoefficient: 2,       # 1s, 2s, 4s, 8s, 16s...
    maximumInterval: '1 minute',  # 退避上限
    maximumAttempts: 5,
  }
});

## Inngest（内置退避）：
{
  id: "my-function",
  retries: 5,  # 默认使用指数退避
}

## 手动退避：
const backoff = (attempt) => {
  const base = 1000;
  const max = 60000;
  const delay = Math.min(base * Math.pow(2, attempt), max);
  const jitter = delay * 0.1 * Math.random();
  return delay + jitter;
};

# 增加抖动以避免惊群效应

### 在工作流状态中存储大数据

严重程度：HIGH

场景：在工作流步骤间传递大型负载

症状：
工作流执行缓慢。内存错误。"负载过大"错误。存储成本高昂。重放缓慢。

失败原因：
工作流状态被持久化并重放。10MB 负载会在每一步被存储、序列化和反序列化。这会增加延迟和成本。某些平台有硬性限制（例如 Step Functions 256KB）。

推荐修复：

# 错误 - 工作流中保存大数据：
await step.run("fetch-data", async () => {
  const largeDataset = await fetchAllRecords();  // 100MB！
  return largeDataset;  // 存储在工作流状态中
});

# 正确 - 存储引用而非数据：
await step.run("fetch-data", async () => {
  const largeDataset = await fetchAllRecords();
  const s3Key = await uploadToS3(largeDataset);
  return { s3Key };  // 仅返回引用
});

const processed = await step.run("process-data", async () => {
  const data = await downloadFromS3(fetchResult.s3Key);
  return processData(data);
});

# 对于 Step Functions，使用 S3 存储大负载：
{
  "Type": "Task",
  "Resource": "arn:aws:states:::s3:putObject",
  "Parameters": {
    "Bucket": "my-bucket",
    "Key.$": "$.outputKey",
    "Body.$": "$.largeData"
  }
}

### 缺少死信队列或失败处理器

严重程度：HIGH

场景：耗尽所有重试次数的工作流

症状：
失败的工作流悄然消失。故障时无告警。客户问题数天后才发现。无法手动恢复。

失败原因：
即使有重试，某些工作流仍会永久失败。没有死信处理，你就不知道它们失败了。客户永远在等待，你浑然不知，也没有可调试的数据。

推荐修复：

# Inngest onFailure 处理器：
export const myFunction = inngest.createFunction(
  {
    id: "process-order",
    onFailure: async ({ error, event, step }) => {
      // Log to error tracking
      await step.run("log-error", () =>
        sentry.captureException(error, { extra: { event } })
      );

      // Alert team
      await step.run("alert", () =>
        slack.postMessage({
          channel: "#alerts",
          text: `Order ${event.data.orderId} failed: ${error.message}`
        })
      );

      // Queue for manual review
      await step.run("queue-review", () =>
        db.insert(failedOrders, { orderId, error, event })
      );
    }
  },
  { event: "order/created" },
  async ({ event, step }) => { ... }
);

# n8n 错误触发器：
[错误触发器]  →  [记录到 DB]  →  [Slack 告警]  →  [创建工单]

# Temporal：使用 workflow.failed 或 workflow signals

### n8n 工作流缺少错误触发器

严重程度：MEDIUM

场景：构建生产级 n8n 工作流

症状：
工作流静默失败。错误仅在执行日志中可见。无告警、无恢复、无可见性，直到有人注意到。

失败原因：
n8n 默认不在失败时通知。没有连接告警的错误触发器节点，失败仅在 UI 中可见。生产环境的失败会被忽略。

推荐修复：

# 每个生产 n8n 工作流都需要：

1. 错误触发器节点
   - 捕获工作流中任意节点的失败
   - 提供错误详情与上下文

2. 连接的错误处理：
   [错误触发器]
       ↓
   [Set: 提取错误详情]
       ↓
   [HTTP: 记录到错误服务]
       ↓
   [Slack/Email: 告警团队]

3. 考虑死信模式：
   [错误触发器]
       ↓
   [Redis/Postgres: 存储失败任务]
       ↓
   [独立恢复工作流]

# 同时使用：
- 节点失败重试（内置）
- 节点超时设置
- 工作流超时

### 长时间运行的 Temporal 活动缺少心跳

严重程度：MEDIUM

场景：运行超过数秒的活动

症状：
活动正常推进却超时。工作者重启时工作丢失。无法取消长时间运行的活动。

失败原因：
Temporal 通过心跳检测卡住的活动。没有心跳，Temporal 无法判断活动是在工作还是卡住。长时间活动看似挂起，可能超时，也无法被优雅取消。

推荐修复：

# 对任何 > 10 秒的活动，添加心跳：

import { heartbeat, activityInfo } from '@temporalio/activity';

export async function processLargeFile(fileUrl: string): Promise<void> {
  const chunks = await downloadChunks(fileUrl);

  for (let i = 0; i < chunks.length; i++) {
    // Check for cancellation
    const { cancelled } = activityInfo();
    if (cancelled) {
      throw new CancelledFailure('Activity cancelled');
    }

    await processChunk(chunks[i]);

    // Report progress
    heartbeat({ progress: (i + 1) / chunks.length });
  }
}

# 配置心跳超时：
const activities = proxyActivities({
  startToCloseTimeout: '10 minutes',
  heartbeatTimeout: '30 seconds',  # 必须每 30 秒一次心跳
});

# 如果 30 秒无心跳，活动被视为卡住

## 验证检查

### 外部调用缺少幂等键

严重程度：ERROR

Stripe/支付调用应使用幂等键

消息：支付调用缺少 idempotency_key。请添加幂等键以防止重试时重复扣款。

### 邮件发送缺少去重

严重程度：WARNING

工作流中的邮件发送应检查是否已发送

消息：工作流中的邮件发送缺少去重检查。重试可能发送重复邮件。

### Temporal 活动缺少超时

严重程度：ERROR

所有 Temporal 活动都需要超时配置

消息：proxyActivities 缺少超时。请添加 startToCloseTimeout 以防止无限挂起。

### Inngest 步骤调用外部 API 缺少超时

严重程度：WARNING

外部 API 调用应有超时

消息：步骤中的外部 API 调用缺少超时。请添加超时以防止工作流挂起。

### 工作流代码中的随机值

严重程度：ERROR

随机值会在重放时破坏确定性

消息：工作流代码中存在随机值。请移至活动/步骤中或使用 sideEffect。

### 工作流代码中的 Date.now()

严重程度：ERROR

当前时间会在重放时破坏确定性

消息：工作流代码中存在当前时间。请使用 workflow.now() 或移至活动/步骤中。

### Inngest 函数缺少 onFailure 处理器

严重程度：WARNING

生产函数应有失败处理器

消息：Inngest 函数缺少 onFailure 处理器。请添加失败处理以保证生产可靠性。

### 步骤缺少错误处理

严重程度：WARNING

步骤应优雅处理错误

消息：步骤缺少 try/catch。请考虑处理特定错误情形。

### 步骤返回可能过大的数据

严重程度：INFO

工作流状态中的大数据会拖慢执行

消息：步骤返回的数据可能过大。请考虑存储在 S3/DB 中并返回引用。

### 重试缺少退避配置

严重程度：WARNING

重试应使用指数退避

消息：重试配置缺少退避。请添加 backoffCoefficient 和 initialInterval。

## 协作

### 委派触发器

- 用户需要多智能体协调 -> multi-agent-orchestration（工作流提供基础设施，编排提供模式）
- 用户需要为工作流构建工具 -> agent-tool-builder（工作流可调用的工具）
- 用户需要 Zapier/Make 集成 -> zapier-make-patterns（无代码自动化平台）
- 用户需要在工作流中进行浏览器自动化 -> browser-automation（Playwright/Puppeteer 活动）
- 用户需要在工作流中进行计算机控制 -> computer-use-agents（桌面自动化活动）
- 用户需要 LLM 集成到工作流中 -> llm-architect（AI 驱动的工作流步骤）

## 相关技能

可与以下技能配合使用：`multi-agent-orchestration`、`agent-tool-builder`、`backend`、`devops`

## 何时使用
- 用户提及或暗示：workflow
- 用户提及或暗示：automation
- 用户提及或暗示：n8n
- 用户提及或暗示：temporal
- 用户提及或暗示：inngest
- 用户提及或暗示：step function
- 用户提及或暗示：background job
- 用户提及或暗示：durable execution
- 用户提及或暗示：event-driven
- 用户提及或暗示：scheduled task
- 用户提及或暗示：job queue
- 用户提及或暗示：cron
- 用户提及或暗示：trigger

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将本输出视为环境特定验证、测试或专家审查的替代品。
- 若缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
