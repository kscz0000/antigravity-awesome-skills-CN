---
name: observability-and-instrumentation
description: 为代码添加埋点，使生产环境行为可见可诊断。添加日志、指标、链路追踪或告警时使用。发布任何在生产环境运行的功能且需要证据证明其正常工作时使用。生产问题报告后无法判断发生了什么时使用。触发词：可观测性、埋点、日志、指标、链路追踪、告警、遥测、observability、instrumentation、tracing、metrics。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/observability-and-instrumentation
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 可观测性与埋点

## 概述

无法观测的代码就是无法运维的代码。可观测性是指从外部借助代码发出的遥测数据回答"系统在做什么、为什么这样做"的能力。埋点不是上线后的补丁——它应该和功能一起编写，就像测试一样。如果一个功能上线时没有遥测，第一个用户报告的 bug 就变成了考古而非查询。

## 何时使用

- 构建任何将在生产环境运行的功能
- 添加新服务、端点、后台任务或外部集成
- 生产故障诊断耗时过长（"我们无法判断发生了什么"）
- 设置或审查告警规则
- 审查添加了 I/O、重试、队列或跨服务调用的 PR

**不适用于：**
- 诊断正在发生的故障——使用 `debugging-and-error-recovery` 技能（可观测性是让该技能下次更快的手段）
- 分析和优化已测量的性能瓶颈——使用 `performance-optimization` 技能
- 上线日的监控清单和回滚触发器——参见 `shipping-and-launch` 技能；本技能覆盖的是为其提供数据的埋点

## 流程

### 1. 埋点前先定义"正常"

没有问题的遥测就是噪音。添加任何埋点之前，写下值班的工程师关于这个功能会问的 2–4 个问题：

```
FEATURE: checkout payment retry
QUESTIONS ON-CALL WILL ASK:
1. What fraction of payments succeed on first attempt vs after retry?
2. When a payment fails permanently, why? (provider error? timeout? validation?)
3. Is the payment provider slower than usual?
→ Every signal below must help answer one of these.
```

如果你说不出这些问题，说明还没准备好做埋点——你会记录一切却什么也学不到。

### 2. 为每个问题选择正确的信号

| 信号 | 回答的问题 | 成本特征 | 示例 |
|---|---|---|---|
| **结构化日志** | "这个具体案例发生了什么？" | 按事件计；随流量增长 | `payment_failed` 附带提供商错误码 |
| **指标** | "总体上多频繁/多快？" | 每个序列固定成本；查询便宜 | 提供商调用的 p99 延迟 |
| **链路追踪** | "跨服务的时间花在哪了？" | 按请求计；通常采样 | 一个慢结账，按跳分解 |

经验法则：指标告诉你**出了问题**，链路追踪告诉你**在哪出的问题**，日志告诉你**为什么出问题**。

### 3. 结构化日志

记录事件，而非叙述。每条日志都是一个 JSON 对象，包含稳定的事件名和机器可读的字段：

```typescript
// BAD: string interpolation — unqueryable, inconsistent
logger.info(`Payment ${id} failed for user ${userId} after ${n} retries`);

// GOOD: stable event name + structured fields
logger.warn({
  event: 'payment_failed',
  paymentId: id,
  provider: 'stripe',
  errorCode: err.code,
  attempt: n,
}, 'payment failed');
```

**日志级别——保持一致使用：**

| 级别 | 含义 | 值班动作 |
|---|---|---|
| `error` | 不变量被打破；可能需要有人介入 | 排查 |
| `warn` | 退化但已处理（重试成功、回退已用） | 关注趋势 |
| `info` | 重要的业务事件（下单、任务完成） | 无 |
| `debug` | 诊断细节 | 生产环境默认关闭 |

**关联 ID 是强制性的。** 在系统边界生成（或接收）请求 ID，并附加到每条日志、每个 span 和每个出站调用。没有它，你无法从交织的日志中重建单个请求：

```typescript
// Express: child logger per request, ID propagated downstream
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] ?? crypto.randomUUID();
  req.log = logger.child({ requestId: req.id });
  res.setHeader('x-request-id', req.id);
  next();
});
```

**绝不记录密钥、令牌、密码或完整 PII。** 这是 `security-and-hardening` 技能的硬性规则——遥测管道是经典的数据泄露路径。使用字段白名单；不要记录完整请求体。

### 4. 指标

对于请求驱动的服务，在每个端点和每个外部依赖上埋点 **RED**：**R**ate（请求/秒）、**E**rrors（失败率）、**D**uration（延迟直方图，而非平均值）。对于资源（队列、池、主机），使用 **USE**：**U**tilization（利用率）、**S**aturation（饱和度）、**E**rrors（错误）。

与链路追踪一样，厂商中立的路径是 OpenTelemetry 指标 API（与步骤 5 相同的 SDK 和上下文）。下面的示例使用 Prometheus 的 `prom-client`——一种常见的后端选择，但不是唯一选择；RED/USE 和基数规则在两种情况下完全相同。

```typescript
import { Histogram } from 'prom-client';

const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route', 'status_class'],  // '2xx', not '200'
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
});
```

**基数是失败模式。** 每个唯一的标签组合都是一个独立的时间序列。标签必须来自小的固定集合（路由模板、状态类、提供商名称）。绝不使用用户 ID、原始 URL、错误消息或其他无界值作为标签——它们属于日志和链路追踪。

```
OK as label:    route="/api/tasks/:id"   status_class="5xx"   provider="stripe"
NEVER a label:  user_id, email, request_id, full URL, error message text
```

永远不要追踪平均值，始终追踪百分位数：平均值会掩盖那 1% 体验极差的用户。使用直方图，读取 p50/p95/p99。

### 5. 分布式链路追踪

使用 OpenTelemetry——它是厂商中立的标准，自动埋点几乎零代码即可覆盖 HTTP、gRPC 和常见数据库客户端：

```typescript
// tracing.ts — must be imported before anything else
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  serviceName: 'checkout-service',
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
```

仅在有意义的工作单元周围添加手动 span（例如 `applyDiscounts`、`chargeProvider`），并附加值班人员会用来过滤的属性。在每个异步边界——HTTP 头、队列消息元数据——传播上下文，否则链路追踪会在间隙处断裂。默认以低比率进行头部采样；如果后端支持尾部采样，保留 100% 的错误。

### 6. 告警

对**用户能感受到的症状**告警，而非对原因告警：

```
SYMPTOM (page-worthy):           CAUSE (dashboard, not a page):
error rate > 1% for 5 min        CPU at 85%
p99 latency > 2s                 one pod restarted
queue age > 10 min               disk at 70%
```

基于原因的告警会在一切正常时触发，却会遗漏你未预见到的故障。基于症状的告警恰好在用户受损时触发，无论原因是什么。

每条告警必须遵循以下规则：

1. **必须可执行。** 如果响应是"忽略它，它会自愈"，删除该告警。
2. **必须链接到运维手册**——哪怕只有三行：含义、首个查询、升级路径。
3. **必须有阈值和持续时间**，由 SLO 或历史数据论证，而非猜测。
4. 仅使用两个严重级别：**页面**（面向用户，立即行动）和**工单**（退化，本周处理）。第三级会变成噪音，让人习惯性忽略一切。

### 7. 验证遥测本身

埋点就是代码；它可能出错。在宣布完成之前，触发路径并查看实际输出：

- 在预发环境强制产生错误 → 通过 `requestId` 在日志中找到它，确认字段是结构化的（而非 `[object Object]`）
- 发送测试流量 → 确认指标序列出现，带预期标签且值合理
- 在链路追踪 UI 中跨服务跟踪单个请求 → 无断裂的 span
- 触发每条新告警一次（临时降低阈值）→ 确认它到达正确的渠道且运维手册链接有效

## 常见自我辩解

| 辩解 | 现实 |
|---|---|
| "等跑通了再加日志" | "之后"会变成"第一次故障之后"，那正是发现你什么都看不见的最昂贵时刻。边构建边埋点。 |
| "日志越多=可观测性越好" | 非结构化噪音让故障排查更慢而非更快。三个可查询的事件胜过三百行叙述文本。 |
| "console.log 暂时够用" | 非结构化输出无法过滤、关联或告警。结构化日志器只多花五分钟，一次就好。 |
| "出问题时看仪表盘就行" | 没有明确问题而建的仪表盘什么都展示了，唯独没有答案。从值班问题出发。 |
| "重要的都告警，之后再调" | 嘈杂的寻呼机会让人习惯性忽略。调整永远不会发生；被漏掉的真实告警会。 |
| "用户 ID 做指标标签方便调试" | 它也会让你的指标后端崩溃。高基数查询属于日志和链路追踪。 |
| "链路追踪对我们两个服务来说杀鸡用牛刀" | 两个服务已经意味着存在日志无法回答的跨服务延迟问题。自动埋点让成本微不足道。 |

## 危险信号

- 功能 PR 包含重试、队列或外部调用，却没有新增遥测
- 日志行由字符串拼接构建，而非结构化字段
- 没有关联/请求 ID——每条日志行都是孤立的
- 指标标签使用用户 ID、原始 URL 或错误消息文本（基数炸弹）
- 延迟追踪为平均值，没有百分位数
- 告警每天触发却被无操作地确认
- 对原因（CPU、内存）告警并呼叫值班人员，面向用户的错误率却无人监控
- 密钥、令牌或完整请求体出现在日志中
- "在我机器上能跑"是生产功能健康的唯一证据

## 验证清单

埋点功能后，确认：

- [ ] 该功能的值班问题已记录，且每个信号映射到其中一个
- [ ] 所有日志输出是结构化的（JSON），有稳定的事件名和每行都有的关联 ID
- [ ] 没有密钥、令牌或未脱敏 PII 出现在任何日志行中（抽查实际输出）
- [ ] 每个新端点和每个外部依赖都有 RED 指标，标签集合有界
- [ ] 延迟是直方图；p95/p99 可查询
- [ ] 单个请求可在链路追踪 UI 中端到端跟踪，无断裂 span
- [ ] 每条新告警基于症状，有运维手册链接，并测试触发过一次
- [ ] 在预发环境诱导的故障仅通过遥测定位，无需阅读源码

简明版本清单（含上线前埋点门控）参见 `references/observability-checklist.md`。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用更改之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定测试、安全审查或用户对破坏性或高成本操作的批准。
