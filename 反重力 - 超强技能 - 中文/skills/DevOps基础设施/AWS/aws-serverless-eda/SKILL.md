---
name: aws-serverless-eda
description: 基于 AWS Well-Architected Framework 的无服务器与事件驱动架构专家。适用于构建无服务器 API、Lambda 函数、REST API、微服务或异步工作流。涵盖基于 TypeScript/Python 的 Lambda、API Gateway（REST/HTTP）、DynamoDB、Step Functions 等内容。触发词：无服务器、事件驱动、Lambda、API Gateway、DynamoDB、Step Functions、EventBridge、SQS、SNS、微服务、Saga、Well-Architected
risk: unknown
source: https://github.com/zxkane/aws-skills/tree/main/plugins/serverless-eda/skills/aws-serverless-eda
source_repo: zxkane/aws-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zxkane/aws-skills/blob/main/LICENSE
---

# AWS 无服务器与事件驱动架构

本技能基于 Well-Architected Framework 原则，为在 AWS 上构建无服务器应用与事件驱动架构提供全面指导。

## AWS 文档要求

回答前务必使用 MCP 工具（`mcp__aws-mcp__*` 或 `mcp__*awsdocs*__*`）核实 AWS 相关事实。`aws-mcp-setup` 依赖项会自动加载；若 MCP 工具不可用，请引导用户按该技能的设置流程进行配置。

## 无服务器 MCP 服务器

本技能借助 CDK MCP 服务器（通过 `aws-cdk-development` 依赖项提供）以及 AWS 文档 MCP 获取无服务器相关指导。

> **注意**：以下 AWS MCP 服务器需通过 Full AWS MCP Server 单独获取（参见 `aws-mcp-setup` 技能），并未随本插件捆绑：
> - AWS Serverless MCP —— SAM CLI 生命周期（init、deploy、local test）
> - AWS Lambda Tool MCP —— 直接调用 Lambda
> - AWS Step Functions MCP —— 工作流编排
> - Amazon SNS/SQS MCP —— 消息传递与队列管理

## 使用场景

在以下情况下使用本技能：

- 使用 Lambda 构建无服务器应用
- 设计事件驱动架构
- 实现微服务模式
- 创建异步处理工作流
- 编排多服务事务
- 构建实时数据处理管道
- 为分布式事务实现 Saga 模式
- 为可扩展性与弹性进行设计

## AWS Well-Architected 无服务器设计原则

### 1. 快速、简洁、单一职责

**函数应简洁且职责单一**

```typescript
// ✅ GOOD - Single purpose, focused function
export const processOrder = async (event: OrderEvent) => {
  // Only handles order processing
  const order = await validateOrder(event);
  await saveOrder(order);
  await publishOrderCreatedEvent(order);
  return { statusCode: 200, body: JSON.stringify({ orderId: order.id }) };
};

// ❌ BAD - Function does too much
export const handleEverything = async (event: any) => {
  // Handles orders, inventory, payments, shipping...
  // Too many responsibilities
};
```

**保持函数运行高效且具备成本意识**：
- 最小化冷启动时间
- 优化内存分配
- 仅在需要时使用预置并发
- 利用连接复用

### 2. 关注并发请求而非总请求数

**按并发而非按总量进行设计**

Lambda 横向扩展 —— 设计时应聚焦以下要点：
- 并发执行限制
- 下游服务的限流
- 共享资源争用
- 连接池规模

```typescript
// Consider concurrent Lambda executions accessing DynamoDB
const table = new dynamodb.Table(this, 'Table', {
  billingMode: dynamodb.BillingMode.PAY_PER_REQUEST, // Auto-scales with load
});

// Or with provisioned capacity + auto-scaling
const table = new dynamodb.Table(this, 'Table', {
  billingMode: dynamodb.BillingMode.PROVISIONED,
  readCapacity: 5,
  writeCapacity: 5,
});

// Enable auto-scaling for concurrent load
table.autoScaleReadCapacity({ minCapacity: 5, maxCapacity: 100 });
table.autoScaleWriteCapacity({ minCapacity: 5, maxCapacity: 100 });
```

### 3. 无共享状态

**函数运行时环境是短暂的**

```typescript
// ❌ BAD - Relying on local file system
export const handler = async (event: any) => {
  fs.writeFileSync('/tmp/data.json', JSON.stringify(data)); // Lost after execution
};

// ✅ GOOD - Use persistent storage
export const handler = async (event: any) => {
  await s3.putObject({
    Bucket: process.env.BUCKET_NAME,
    Key: 'data.json',
    Body: JSON.stringify(data),
  });
};
```

**状态管理**：
- 使用 DynamoDB 存储持久化状态
- 使用 Step Functions 管理流程状态
- 使用 ElastiCache 存储会话状态
- 使用 S3 进行文件存储

### 4. 假设无硬件亲和性

**应用必须与硬件无关**

基础设施可能随时变更：
- Lambda 函数可能运行在不同硬件上
- 容器实例可能被替换
- 不应对底层基础设施做任何假设

**为可移植性而设计**：
- 使用环境变量进行配置
- 避免针对特定硬件的优化
- 在不同环境中进行测试

### 5. 使用状态机而非函数链进行编排

**使用 Step Functions 进行编排**

```typescript
// ❌ BAD - Lambda function chaining
export const handler1 = async (event: any) => {
  const result = await processStep1(event);
  await lambda.invoke({
    FunctionName: 'handler2',
    Payload: JSON.stringify(result),
  });
};

// ✅ GOOD - Step Functions orchestration
const stateMachine = new stepfunctions.StateMachine(this, 'OrderWorkflow', {
  definition: stepfunctions.Chain
    .start(validateOrder)
    .next(processPayment)
    .next(shipOrder)
    .next(sendConfirmation),
});
```

**Step Functions 的优势**：
- 可视化的工作流呈现
- 内置的错误处理与重试
- 执行历史与调试能力
- 支持并行与顺序执行
- 无需编写代码的服务集成

### 6. 使用事件触发事务

**事件驱动优于同步请求/响应**

```typescript
// Pattern: Event-driven processing
const bucket = new s3.Bucket(this, 'DataBucket');

bucket.addEventNotification(
  s3.EventType.OBJECT_CREATED,
  new s3n.LambdaDestination(processFunction),
  { prefix: 'uploads/' }
);

// Pattern: EventBridge integration
const rule = new events.Rule(this, 'OrderRule', {
  eventPattern: {
    source: ['orders'],
    detailType: ['OrderPlaced'],
  },
});

rule.addTarget(new targets.LambdaFunction(processOrderFunction));
```

**优势**：
- 服务间松耦合
- 异步处理
- 更好的容错能力
- 独立扩展

### 7. 为失败与重复而设计

**操作必须是幂等的**

```typescript
// ✅ GOOD - Idempotent operation
export const handler = async (event: SQSEvent) => {
  for (const record of event.Records) {
    const orderId = JSON.parse(record.body).orderId;

    // Check if already processed (idempotency)
    const existing = await dynamodb.getItem({
      TableName: process.env.TABLE_NAME,
      Key: { orderId },
    });

    if (existing.Item) {
      console.log('Order already processed:', orderId);
      continue; // Skip duplicate
    }

    // Process order
    await processOrder(orderId);

    // Mark as processed
    await dynamodb.putItem({
      TableName: process.env.TABLE_NAME,
      Item: { orderId, processedAt: Date.now() },
    });
  }
};
```

**使用指数退避实现重试逻辑**：
```typescript
async function withRetry<T>(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
    }
  }
  throw new Error('Max retries exceeded');
}
```

## 架构模式

如需查看含完整代码示例的详细实现模式，请参阅参考文档：

### 事件驱动架构模式
**文件**：`references/eda-patterns.md`
- 基于 EventBridge 的事件路由（自定义事件总线、Schema 注册表、基于规则的路由）
- 基于 SQS 的队列处理（标准/FIFO、DLQ、Lambda 消费者）
- 基于 SNS + SQS 的发布订阅扇出（多消费者、过滤）
- 基于 Step Functions 的 Saga 模式（分布式事务、补偿动作）
- 基于 DynamoDB Streams 的事件溯源（仅追加事件存储、投影）

### 无服务器架构模式
**文件**：`references/serverless-patterns.md`
- API 驱动的微服务（REST API + Lambda 后端）
- 基于 Kinesis 的流处理（实时、批处理窗口、错误二分）
- 基于 SQS 的异步任务处理（后台作业、并发控制）
- 基于 EventBridge 的定时任务（cron/rate 调度）
- Webhook 处理（签名验证、异步队列转发）

> **重要提示**：使用 references 中的 CDK 代码示例时，避免硬编码资源名称（如 `restApiName`、`eventBusName`）。让 CDK 自动生成唯一名称，以便支持复用与并行部署。详见 `aws-cdk-development` 技能。

## 最佳实践

### 错误处理

**实现全面的错误处理**：

```typescript
export const handler = async (event: SQSEvent) => {
  const failures: SQSBatchItemFailure[] = [];

  for (const record of event.Records) {
    try {
      await processRecord(record);
    } catch (error) {
      console.error('Failed to process record:', record.messageId, error);
      failures.push({ itemIdentifier: record.messageId });
    }
  }

  // Return partial batch failures for retry
  return { batchItemFailures: failures };
};
```

### 死信队列

**始终为错误处理配置 DLQ**：

```typescript
const dlq = new sqs.Queue(this, 'DLQ', {
  retentionPeriod: Duration.days(14),
});

const queue = new sqs.Queue(this, 'Queue', {
  deadLetterQueue: {
    queue: dlq,
    maxReceiveCount: 3,
  },
});

// Monitor DLQ depth
new cloudwatch.Alarm(this, 'DLQAlarm', {
  metric: dlq.metricApproximateNumberOfMessagesVisible(),
  threshold: 1,
  evaluationPeriods: 1,
  alarmDescription: 'Messages in DLQ require attention',
});
```

### 可观测性

**启用链路追踪与监控**：

```typescript
new NodejsFunction(this, 'Function', {
  entry: 'src/handler.ts',
  tracing: lambda.Tracing.ACTIVE, // X-Ray tracing
  environment: {
    POWERTOOLS_SERVICE_NAME: 'order-service',
    POWERTOOLS_METRICS_NAMESPACE: 'MyApp',
    LOG_LEVEL: 'INFO',
  },
});
```

## 高效使用 MCP 服务器

构建无服务器基础设施时，可通过 CDK MCP 服务器（即 `aws-cdk-development` 依赖项）获取构件推荐与 CDK 专项指导。

实现前，使用 AWS 文档 MCP 核实服务功能、区域可用性与 API 规格。

## 附加资源

本技能包含基于 AWS 最佳实践的全面参考文档：

- **无服务器模式**：`references/serverless-patterns.md`
  - 核心无服务器架构与 API 模式
  - 数据处理与集成模式
  - 使用 Step Functions 的编排
  - 需要规避的反模式

- **事件驱动架构模式**：`references/eda-patterns.md`
  - 事件路由与处理模式
  - 事件溯源与 Saga 模式
  - 幂等性与错误处理
  - 消息顺序与去重

- **安全最佳实践**：`references/security-best-practices.md`
  - 共享责任模型
  - IAM 最小权限模式
  - 数据保护与加密
  - 基于 VPC 的网络安全

- **可观测性最佳实践**：`references/observability-best-practices.md`
  - 三大支柱：指标、日志、链路追踪
  - 使用 Lambda Powertools 进行结构化日志
  - X-Ray 分布式链路追踪
  - CloudWatch 告警与仪表盘

- **性能优化**：`references/performance-optimization.md`
  - 冷启动优化技巧
  - 内存与 CPU 优化
  - 包体积缩减
  - 预置并发模式

- **部署最佳实践**：`references/deployment-best-practices.md`
  - CI/CD 流水线设计
  - 测试策略（单元、集成、负载）
  - 部署策略（金丝雀、蓝绿）
  - 回滚与安全机制

**外部资源**：
- **AWS Well-Architected Serverless Lens**：https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/
- **ServerlessLand.com**：预构建的无服务器模式
- **AWS Serverless Workshops**：https://serverlessland.com/learn?type=Workshops

如需了解详细的实现模式、反模式与代码示例，请参阅技能目录中的完整参考资料。

## 使用限制

- 仅当任务与本技能的上游来源及本地项目上下文明确匹配时使用。
- 在应用变更前，请核实命令、生成的代码、依赖项、凭证及外部服务行为。
- 切勿将示例视为可替代环境专项测试、安全审查，或用户对破坏性/高成本操作的批准。