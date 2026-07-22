# 错误分析与解决实施手册

本文件包含该技能所引用的详细模式、检查清单和代码示例。

## 错误检测与分类

### 错误分类法

将错误归入以下类别，以指导你的调试策略：

**按严重程度：**
- **严重（Critical）**：系统宕机、数据丢失、安全泄露、服务完全不可用
- **高（High）**：主要功能损坏、重大用户影响、数据损坏风险
- **中（Medium）**：部分功能降级、有变通方案、性能问题
- **低（Low）**：次要缺陷、界面问题、影响极小的边界情况

**按类型：**
- **运行时错误**：异常、崩溃、段错误、空指针解引用
- **逻辑错误**：行为不正确、计算错误、状态转换无效
- **集成错误**：API 失败、网络超时、外部服务问题
- **性能错误**：内存泄漏、CPU 飙升、慢查询、资源耗尽
- **配置错误**：缺少环境变量、配置无效、版本不匹配
- **安全错误**：身份验证失败、授权违规、注入攻击尝试

**按可观察性：**
- **确定性**：使用已知输入可稳定复现
- **间歇性**：零星出现，通常与时序或竞态条件相关
- **环境性**：仅在特定环境或配置下发生
- **负载相关**：在高流量或资源压力下出现

### 错误检测策略

实施多层次的错误检测：

1. **应用层插桩**：使用错误跟踪 SDK（Sentry、DataDog Error Tracking、Rollbar）自动捕获未处理异常并附带完整上下文
2. **健康检查端点**：监控 `/health` 和 `/ready` 端点，在影响用户之前检测服务降级
3. **合成监控**：对生产环境运行自动化测试，主动发现问题
4. **真实用户监控（RUM）**：跟踪真实用户体验和前端错误
5. **日志模式分析**：使用 SIEM 工具识别错误峰值和异常模式
6. **APM 阈值告警**：在错误率上升、延迟飙升或吞吐量下降时告警

### 错误聚合与模式识别

对相关错误进行分组以识别系统性问题：

- **指纹识别**：按堆栈跟踪相似性、错误类型和受影响的代码路径对错误分组
- **趋势分析**：跟踪错误频率随时间的变化，以检测回归或新出现的问题
- **相关性分析**：将错误与部署、配置变更或外部事件关联起来
- **用户影响评分**：根据受影响用户和会话的数量排定优先级
- **地理/时间模式**：识别特定区域或基于时间的错误集群

## 根因分析技术

### 系统化调查流程

针对每个错误遵循以下结构化方法：

1. **复现错误**：创建最小复现步骤。如果属于间歇性错误，识别触发条件
2. **隔离故障点**：缩小到发生故障的精确代码行或组件
3. **分析调用链**：从错误反向追踪，了解系统如何进入失败状态
4. **检查变量状态**：检查失败点及其前置步骤的值
5. **审查近期变更**：查看 git 历史记录中受影响代码路径的近期修改
6. **验证假设**：形成原因理论并通过针对性实验进行验证

### 五个"为什么"分析法

反复追问"为什么"以深入到根本原因：

```
错误：30 秒后数据库连接超时

为什么？数据库连接池耗尽
为什么？所有连接都被长时间运行的查询占用
为什么？新功能引入了 N+1 查询模式
为什么？ORM 懒加载未正确配置
为什么？代码审查未能发现该性能回归
```

根本原因：针对数据库查询模式的代码审查流程不足。

### 分布式系统调试

针对微服务和分布式系统中的错误：

- **追踪请求路径**：使用关联 ID 跟踪跨服务边界的请求
- **检查服务依赖**：识别涉及哪些上游/下游服务
- **分析级联失败**：判断这是否是另一个服务失败的表征
- **审查熔断器状态**：检查保护机制是否已触发
- **检查消息队列**：查看背压、死信或处理延迟
- **时间线重建**：使用分布式追踪构建跨所有服务的事件时间线

## 堆栈跟踪分析

### 解读堆栈跟踪

从堆栈跟踪中提取最大化的信息：

**关键元素：**
- **错误类型**：发生了哪种异常/错误
- **错误消息**：关于失败的上下文信息
- **原始抛出点**：抛出错误的最深层帧
- **调用链**：导致错误的函数调用序列
- **框架代码与应用代码**：区分库代码和你的代码
- **异步边界**：识别异步操作中断跟踪的位置

**分析策略：**
1. 从堆栈顶部（错误源）开始
2. 识别你的应用代码中的第一帧（非框架/库）
3. 检查该帧的上下文：输入参数、局部变量、状态
4. 通过调用函数反向追踪，了解无效状态是如何产生的
5. 寻找模式：这是否在循环中？在回调中？在异步操作之后？

### 堆栈跟踪增强

现代错误跟踪工具提供增强的堆栈跟踪：

- **源代码上下文**：查看每帧周围的代码行
- **局部变量值**：检查每帧的变量状态（使用 Sentry 的调试模式）
- **面包屑（Breadcrumbs）**：查看导致错误的事件序列
- **发布版本追踪**：将错误关联到特定的部署和提交
- **Source Map**：对于压缩的 JavaScript，映射回原始源代码
- **内联注释**：为堆栈帧添加上下文信息

### 常见的堆栈跟踪模式

**模式：框架代码深层的空指针异常**
```
NullPointerException
  at java.util.HashMap.hash(HashMap.java:339)
  at java.util.HashMap.get(HashMap.java:556)
  at com.myapp.service.UserService.findUser(UserService.java:45)
```
根本原因：应用将 null 传递给了框架代码。重点关注 UserService.java:45。

**模式：长时间等待后超时**
```
TimeoutException: Operation timed out after 30000ms
  at okhttp3.internal.http2.Http2Stream.waitForIo
  at com.myapp.api.PaymentClient.processPayment(PaymentClient.java:89)
```
根本原因：外部服务缓慢/无响应。需要重试逻辑和熔断器。

**模式：并发代码中的竞态条件**
```
ConcurrentModificationException
  at java.util.ArrayList$Itr.checkForComodification
  at com.myapp.processor.BatchProcessor.process(BatchProcessor.java:112)
```
根本原因：迭代过程中集合被修改。需要线程安全的数据结构或同步机制。

## 日志聚合与模式匹配

### 结构化日志实现

实施基于 JSON 的结构化日志，以获得机器可读的日志：

**标准日志架构：**
```json
{
  "timestamp": "2025-10-11T14:23:45.123Z",
  "level": "ERROR",
  "correlation_id": "req-7f3b2a1c-4d5e-6f7g-8h9i-0j1k2l3m4n5o",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "service": "payment-service",
  "environment": "production",
  "host": "pod-payment-7d4f8b9c-xk2l9",
  "version": "v2.3.1",
  "error": {
    "type": "PaymentProcessingException",
    "message": "Failed to charge card: Insufficient funds",
    "stack_trace": "...",
    "fingerprint": "payment-insufficient-funds"
  },
  "user": {
    "id": "user-12345",
    "ip": "203.0.113.42",
    "session_id": "sess-abc123"
  },
  "request": {
    "method": "POST",
    "path": "/api/v1/payments/charge",
    "duration_ms": 2547,
    "status_code": 402
  },
  "context": {
    "payment_method": "credit_card",
    "amount": 149.99,
    "currency": "USD",
    "merchant_id": "merchant-789"
  }
}
```

**始终包含的关键字段：**
- `timestamp`：UTC 的 ISO 8601 格式
- `level`：ERROR、WARN、INFO、DEBUG、TRACE
- `correlation_id`：整个请求链的唯一 ID
- `trace_id` 和 `span_id`：用于分布式追踪的 OpenTelemetry 标识符
- `service`：生成此日志的微服务
- `environment`：dev、staging、production
- `error.fingerprint`：用于对相似错误进行分组的稳定标识符

### 关联 ID 模式

实施关联 ID 以跟踪分布式系统中的请求：

**Node.js/Express 中间件：**
```javascript
const { v4: uuidv4 } = require('uuid');
const asyncLocalStorage = require('async-local-storage');

// 用于生成/传递关联 ID 的中间件
function correlationIdMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id'] || uuidv4();
  req.correlationId = correlationId;
  res.setHeader('x-correlation-id', correlationId);

  // 存储到异步上下文中，以便在嵌套调用中访问
  asyncLocalStorage.run(new Map(), () => {
    asyncLocalStorage.set('correlationId', correlationId);
    next();
  });
}

// 向下游服务传递
function makeApiCall(url, data) {
  const correlationId = asyncLocalStorage.get('correlationId');
  return axios.post(url, data, {
    headers: {
      'x-correlation-id': correlationId,
      'x-source-service': 'api-gateway'
    }
  });
}

// 包含在所有日志语句中
function log(level, message, context = {}) {
  const correlationId = asyncLocalStorage.get('correlationId');
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    correlation_id: correlationId,
    message,
    ...context
  }));
}
```

**Python/Flask 实现：**
```python
import uuid
import logging
from flask import request, g
import json

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = g.get('correlation_id', 'N/A')
        return True

@app.before_request
def setup_correlation_id():
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    g.correlation_id = correlation_id

@app.after_request
def add_correlation_header(response):
    response.headers['X-Correlation-ID'] = g.correlation_id
    return response

# 带关联 ID 的结构化日志
logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.addFilter(CorrelationIdFilter())

def log_structured(level, message, **context):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'level': level,
        'correlation_id': g.correlation_id,
        'service': 'payment-service',
        'message': message,
        **context
    }
    logger.log(getattr(logging, level), json.dumps(log_entry))
```

### 日志聚合架构

**集中式日志管道：**
1. **应用**：将结构化 JSON 日志输出到 stdout/stderr
2. **日志采集器**：Fluentd/Fluent Bit/Vector 从容器收集日志
3. **日志聚合器**：Elasticsearch/Loki/DataDog 接收并索引日志
4. **可视化**：Kibana/Grafana/DataDog UI 用于查询和仪表板
5. **告警**：基于错误模式和阈值触发告警

**日志查询示例（Elasticsearch DSL）：**
```json
// 查找特定关联 ID 的所有错误
{
  "query": {
    "bool": {
      "must": [
        { "match": { "correlation_id": "req-7f3b2a1c-4d5e-6f7g" }},
        { "term": { "level": "ERROR" }}
      ]
    }
  },
  "sort": [{ "timestamp": "asc" }]
}

// 查找过去一小时内错误率峰值
{
  "query": {
    "bool": {
      "must": [
        { "term": { "level": "ERROR" }},
        { "range": { "timestamp": { "gte": "now-1h" }}}
      ]
    }
  },
  "aggs": {
    "errors_per_minute": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1m"
      }
    }
  }
}

// 按指纹对错误分组以查找最常见的问题
{
  "query": {
    "term": { "level": "ERROR" }
  },
  "aggs": {
    "error_types": {
      "terms": {
        "field": "error.fingerprint",
        "size": 10
      },
      "aggs": {
        "affected_users": {
          "cardinality": { "field": "user.id" }
        }
      }
    }
  }
}
```

### 模式检测与异常识别

使用日志分析来识别模式：

- **错误率峰值**：将当前错误率与历史基线进行比较（例如，超过 3 个标准差）
- **新错误类型**：在出现以前未见过的错误指纹时告警
- **级联失败**：检测一个服务中的错误何时触发依赖服务中的错误
- **用户影响模式**：识别哪些用户/细分群体受到不成比例的影响
- **地理模式**：发现区域性问题（例如，CDN 问题、数据中心宕机）
- **时间模式**：发现基于时间的问题（例如，批处理作业、计划任务、时区缺陷）

## 调试工作流

### 交互式调试

针对开发环境中的确定性错误：

**调试器设置：**
1. 在错误发生之前设置断点
2. 逐行单步执行代码
3. 检查变量值和对象状态
4. 在调试控制台中计算表达式
5. 观察意外的状态变化
6. 修改变量以测试假设

**现代调试工具：**
- **VS Code 调试器**：JavaScript、Python、Go、Java、C++ 的集成调试
- **Chrome DevTools**：带网络、性能和内存分析的前端调试
- **pdb/ipdb（Python）**：支持事后分析的交互式调试器
- **dlv（Go）**：Go 程序的 Delve 调试器
- **lldb（C/C++）**：具有反向调试功能的低级调试器

### 生产环境调试

针对生产环境中无法使用调试器的错误：

**安全的生产环境调试技术：**

1. **增强日志记录**：在疑似故障点周围添加策略性日志语句
2. **特性开关**：为特定用户/请求启用详细日志
3. **采样**：为一定比例的请求记录详细上下文
4. **APM 事务追踪**：使用 DataDog APM 或 New Relic 查看详细的事务流
5. **分布式追踪**：利用 OpenTelemetry 追踪来理解跨服务交互
6. **性能分析**：使用持续分析器（DataDog Profiler、Pyroscope）识别热点
7. **堆转储**：捕获内存快照以分析内存泄漏
8. **流量镜像**：在预发布环境中重放生产流量以进行安全调查

**远程调试（谨慎使用）：**
- 仅在非关键服务上将调试器附加到运行中的进程
- 使用不会暂停执行的只读断点
- 严格限定调试会话的时间
- 始终准备好回滚计划

### 内存和性能调试

**内存泄漏检测：**
```javascript
// Node.js 堆快照对比
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(filename) {
  const snapshot = v8.writeHeapSnapshot(filename);
  console.log(`Heap snapshot written to ${snapshot}`);
}

// 间隔地拍摄快照
takeHeapSnapshot('heap-before.heapsnapshot');
// ... 运行可能导致泄漏的操作 ...
takeHeapSnapshot('heap-after.heapsnapshot');

// 在 Chrome DevTools 内存分析器中分析
// 查找保留大小持续增长的对象
```

**性能分析：**
```python
# 使用 cProfile 进行 Python 性能分析
import cProfile
import pstats
from pstats import SortKey

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()

    # 你的代码
    process_large_dataset()

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(20)  # 耗时最多的前 20 个函数
```

## 错误预防策略

### 输入验证与类型安全

**防御性编程：**
```typescript
// TypeScript：利用类型系统实现编译时安全
interface PaymentRequest {
  amount: number;
  currency: string;
  customerId: string;
  paymentMethodId: string;
}

function processPayment(request: PaymentRequest): PaymentResult {
  // 对外部输入进行运行时验证
  if (request.amount <= 0) {
    throw new ValidationError('Amount must be positive');
  }

  if (!['USD', 'EUR', 'GBP'].includes(request.currency)) {
    throw new ValidationError('Unsupported currency');
  }

  // 对复杂验证使用 Zod 或 Yup
  const schema = z.object({
    amount: z.number().positive().max(1000000),
    currency: z.enum(['USD', 'EUR', 'GBP']),
    customerId: z.string().uuid(),
    paymentMethodId: z.string().min(1)
  });

  const validated = schema.parse(request);

  // 现在可以安全地处理
  return chargeCustomer(validated);
}
```

**Python 类型提示与验证：**
```python
from typing import Optional
from pydantic import BaseModel, validator, Field
from decimal import Decimal

class PaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, le=1000000)
    currency: str
    customer_id: str
    payment_method_id: str

    @validator('currency')
    def validate_currency(cls, v):
        if v not in ['USD', 'EUR', 'GBP']:
            raise ValueError('Unsupported currency')
        return v

    @validator('customer_id', 'payment_method_id')
    def validate_ids(cls, v):
        if not v or len(v) < 1:
            raise ValueError('ID cannot be empty')
        return v

def process_payment(request: PaymentRequest) -> PaymentResult:
    # Pydantic 在实例化时自动验证
    # 类型提示提供 IDE 支持和静态分析
    return charge_customer(request)
```

### 错误边界与优雅降级

**React 错误边界：**
```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';
import * as Sentry from '@sentry/react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // 记录到错误跟踪服务
    Sentry.captureException(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack
        }
      }
    });

    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div role="alert">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.message}</pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

**熔断器模式：**
```python
from datetime import datetime, timedelta
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"      # 正常运行
    OPEN = "open"          # 失败中，拒绝请求
    HALF_OPEN = "half_open"  # 测试服务是否恢复

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self):
        return (datetime.now() - self.last_failure_time) > timedelta(seconds=self.timeout)

# 使用示例
payment_circuit = CircuitBreaker(failure_threshold=5, timeout=60)

def process_payment_with_circuit_breaker(payment_data):
    try:
        result = payment_circuit.call(external_payment_api.charge, payment_data)
        return result
    except CircuitBreakerOpenError:
        # 优雅降级：排队等待后续处理
        payment_queue.enqueue(payment_data)
        return {"status": "queued", "message": "Payment will be processed shortly"}
```

### 带指数退避的重试逻辑

```typescript
// TypeScript 重试实现
interface RetryOptions {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  exponentialBase: number;
  retryableErrors?: string[];
}

async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {
    maxAttempts: 3,
    baseDelayMs: 1000,
    maxDelayMs: 30000,
    exponentialBase: 2
  }
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < options.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // 检查错误是否可重试
      if (options.retryableErrors &&
          !options.retryableErrors.includes(error.name)) {
        throw error; // 不重试不可重试的错误
      }

      if (attempt < options.maxAttempts - 1) {
        const delay = Math.min(
          options.baseDelayMs * Math.pow(options.exponentialBase, attempt),
          options.maxDelayMs
        );

        // 增加随机抖动以防止雷暴群效应
        const jitter = Math.random() * 0.1 * delay;
        const actualDelay = delay + jitter;

        console.log(`Attempt ${attempt + 1} failed, retrying in ${actualDelay}ms`);
        await new Promise(resolve => setTimeout(resolve, actualDelay));
      }
    }
  }

  throw lastError!;
}

// 使用示例
const result = await retryWithBackoff(
  () => fetch('https://api.example.com/data'),
  {
    maxAttempts: 3,
    baseDelayMs: 1000,
    maxDelayMs: 10000,
    exponentialBase: 2,
    retryableErrors: ['NetworkError', 'TimeoutError']
  }
);
```

## 监控与告警集成

### 现代可观测性技术栈（2025）

**推荐架构：**
- **指标（Metrics）**：Prometheus + Grafana 或 DataDog
- **日志（Logs）**：Elasticsearch/Loki + Fluentd 或 DataDog Logs
- **追踪（Traces）**：OpenTelemetry + Jaeger/Tempo 或 DataDog APM
- **错误（Errors）**：Sentry 或 DataDog Error Tracking
- **前端（Frontend）**：Sentry Browser SDK 或 DataDog RUM
- **合成（Synthetics）**：DataDog Synthetics 或 Checkly

### Sentry 集成

**Node.js/Express 设置：**
```javascript
const Sentry = require('@sentry/node');
const { ProfilingIntegration } = require('@sentry/profiling-node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.GIT_COMMIT_SHA,

  // 性能监控
  tracesSampleRate: 0.1, // 10% 的事务
  profilesSampleRate: 0.1,

  integrations: [
    new ProfilingIntegration(),
    new Sentry.Integrations.Http({ tracing: true }),
    new Sentry.Integrations.Express({ app }),
  ],

  beforeSend(event, hint) {
    // 脱敏敏感数据
    if (event.request) {
      delete event.request.cookies;
      delete event.request.headers?.authorization;
    }

    // 添加自定义上下文
    event.tags = {
      ...event.tags,
      region: process.env.AWS_REGION,
      instance_id: process.env.INSTANCE_ID
    };

    return event;
  }
});

// Express 中间件
app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

// 路由在此处...

// 错误处理（必须放在最后）
app.use(Sentry.Handlers.errorHandler());

// 带上下文的手动错误捕获
function processOrder(orderId) {
  try {
    const order = getOrder(orderId);
    chargeCustomer(order);
  } catch (error) {
    Sentry.captureException(error, {
      tags: {
        operation: 'process_order',
        order_id: orderId
      },
      contexts: {
        order: {
          id: orderId,
          status: order?.status,
          amount: order?.amount
        }
      },
      user: {
        id: order?.customerId
      }
    });
    throw error;
  }
}
```

### DataDog APM 集成

**Python/Flask 设置：**
```python
from ddtrace import patch_all, tracer
from ddtrace.contrib.flask import TraceMiddleware
import logging

# 自动插桩常用库
patch_all()

app = Flask(__name__)

# 初始化追踪
TraceMiddleware(app, tracer, service='payment-service')

# 用于详细追踪的自定义 span
@app.route('/api/v1/payments/charge', methods=['POST'])
def charge_payment():
    with tracer.trace('payment.charge', service='payment-service') as span:
        payment_data = request.json

        # 添加自定义标签
        span.set_tag('payment.amount', payment_data['amount'])
        span.set_tag('payment.currency', payment_data['currency'])
        span.set_tag('customer.id', payment_data['customer_id'])

        try:
            result = payment_processor.charge(payment_data)
            span.set_tag('payment.status', 'success')
            return jsonify(result), 200
        except InsufficientFundsError as e:
            span.set_tag('payment.status', 'insufficient_funds')
            span.set_tag('error', True)
            return jsonify({'error': 'Insufficient funds'}), 402
        except Exception as e:
            span.set_tag('payment.status', 'error')
            span.set_tag('error', True)
            span.set_tag('error.message', str(e))
            raise
```

### OpenTelemetry 实现

**使用 OpenTelemetry 的 Go 服务：**
```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/trace"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
)

func initTracer() (*sdktrace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(
        context.Background(),
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("payment-service"),
            semconv.ServiceVersionKey.String("v2.3.1"),
            attribute.String("environment", "production"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func processPayment(ctx context.Context, paymentReq PaymentRequest) error {
    tracer := otel.Tracer("payment-service")
    ctx, span := tracer.Start(ctx, "processPayment")
    defer span.End()

    // 添加属性
    span.SetAttributes(
        attribute.Float64("payment.amount", paymentReq.Amount),
        attribute.String("payment.currency", paymentReq.Currency),
        attribute.String("customer.id", paymentReq.CustomerID),
    )

    // 调用下游服务
    err := chargeCard(ctx, paymentReq)
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }

    span.SetStatus(codes.Ok, "Payment processed successfully")
    return nil
}

func chargeCard(ctx context.Context, paymentReq PaymentRequest) error {
    tracer := otel.Tracer("payment-service")
    ctx, span := tracer.Start(ctx, "chargeCard")
    defer span.End()

    // 模拟外部 API 调用
    result, err := paymentGateway.Charge(ctx, paymentReq)
    if err != nil {
        return fmt.Errorf("payment gateway error: %w", err)
    }

    span.SetAttributes(
        attribute.String("transaction.id", result.TransactionID),
        attribute.String("gateway.response_code", result.ResponseCode),
    )

    return nil
}
```

### 告警配置

**智能告警策略：**

```yaml
# DataDog 监控配置
monitors:
  - name: "High Error Rate - Payment Service"
    type: metric
    query: "avg(last_5m):sum:trace.express.request.errors{service:payment-service} / sum:trace.express.request.hits{service:payment-service} > 0.05"
    message: |
      Payment service error rate is {{value}}% (threshold: 5%)

      This may indicate:
      - Payment gateway issues
      - Database connectivity problems
      - Invalid payment data

      Runbook: https://wiki.company.com/runbooks/payment-errors

      @slack-payments-oncall @pagerduty-payments

    tags:
      - service:payment-service
      - severity:high

    options:
      notify_no_data: true
      no_data_timeframe: 10
      escalation_message: "Error rate still elevated after 10 minutes"

  - name: "New Error Type Detected"
    type: log
    query: "logs(\"level:ERROR service:payment-service\").rollup(\"count\").by(\"error.fingerprint\").last(\"5m\") > 0"
    message: |
      New error type detected in payment service: {{error.fingerprint}}

      First occurrence: {{timestamp}}
      Affected users: {{user_count}}

      @slack-engineering

    options:
      enable_logs_sample: true

  - name: "Payment Service - P95 Latency High"
    type: metric
    query: "avg(last_10m):p95:trace.express.request.duration{service:payment-service} > 2000"
    message: |
      Payment service P95 latency is {{value}}ms (threshold: 2000ms)

      Check:
      - Database query performance
      - External API response times
      - Resource constraints (CPU/memory)

      Dashboard: https://app.datadoghq.com/dashboard/payment-service

      @slack-payments-team
```

## 生产事故响应

### 事故响应工作流

**阶段 1：检测与分流（0-5 分钟）**
1. 确认告警/事故
2. 检查事故严重程度和用户影响
3. 指定事故指挥官
4. 创建事故频道（#incident-2025-10-11-payment-errors）
5. 如果面向客户，则更新状态页

**阶段 2：调查（5-30 分钟）**
1. 收集可观测性数据：
   - 来自 Sentry/DataDog 的错误率
   - 显示失败请求的追踪
   - 事故开始时间附近的日志
   - 显示资源使用、延迟、吞吐量的指标
2. 与近期变更关联：
   - 最近的部署（检查 CI/CD 管道）
   - 配置变更
   - 基础设施变更
   - 外部依赖状态
3. 形成关于根本原因的初步假设
4. 在事故日志中记录发现

**阶段 3：缓解（即时）**
1. 根据假设实施即时修复：
   - 回滚最近的部署
   - 扩容资源
   - 禁用有问题的功能（特性开关）
   - 故障转移到备份系统
   - 应用热修复
2. 验证缓解措施是否有效（错误率下降）
3. 监控 15-30 分钟以确保稳定

**阶段 4：恢复与验证**
1. 验证所有系统正常运行
2. 检查数据一致性
3. 处理排队/失败的请求
4. 更新状态页：事故已解决
5. 通知利益相关方

**阶段 5：事后复盘**
1. 在 48 小时内安排事后总结会
2. 创建详细的事件时间线
3. 识别根本原因（可能与初步假设不同）
4. 记录促成因素
5. 创建以下行动项：
   - 防止类似事故
   - 改进检测时间
   - 改进缓解时间
   - 改进沟通

### 事故调查工具

**常见事故的查询模式：**

```
# 查找特定时间窗口内的所有错误（Elasticsearch）
GET /logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "level": "ERROR" }},
        { "term": { "service": "payment-service" }},
        { "range": { "timestamp": {
          "gte": "2025-10-11T14:00:00Z",
          "lte": "2025-10-11T14:30:00Z"
        }}}
      ]
    }
  },
  "sort": [{ "timestamp": "asc" }],
  "size": 1000
}

# 查找错误与部署之间的相关性（DataDog）
# 使用部署追踪在错误图表上叠加部署标记
# 查询：sum:trace.express.request.errors{service:payment-service} by {version}

# 识别受影响的用户（Sentry）
# 导航到问题 → 用户影响选项卡
# 显示：受影响的总用户数、新用户与回访用户、地理分布

# 追踪特定的失败请求（OpenTelemetry/Jaeger）
# 按 trace_id 或 correlation_id 搜索
# 可视化跨服务的完整请求路径
# 识别哪个服务/span 失败
```

### 沟通模板

**初始事故通知：**
```
🚨 INCIDENT: Payment Processing Errors

Severity: High
Status: Investigating
Started: 2025-10-11 14:23 UTC
Incident Commander: @jane.smith

Symptoms:
- Payment processing error rate: 15% (normal: <1%)
- Affected users: ~500 in last 10 minutes
- Error: "Database connection timeout"

Actions Taken:
- Investigating database connection pool
- Checking recent deployments
- Monitoring error rate

Updates: Will provide update every 15 minutes
Status Page: https://status.company.com/incident/abc123
```

**缓解措施通知：**
```
✅ INCIDENT UPDATE: Mitigation Applied

Severity: High → Medium
Status: Mitigated
Duration: 27 minutes

Root Cause: Database connection pool exhausted due to long-running queries
introduced in v2.3.1 deployment at 14:00 UTC

Mitigation: Rolled back to v2.3.0

Current Status:
- Error rate: 0.5% (back to normal)
- All systems operational
- Processing backlog of queued payments

Next Steps:
- Monitor for 30 minutes
- Fix query performance issue
- Deploy fixed version with testing
- Schedule postmortem
```

## 错误分析交付物

针对每次错误分析，提供：

1. **错误摘要**：发生了什么、何时发生、影响范围
2. **根本原因**：错误发生的根本原因
3. **证据**：支持诊断的堆栈跟踪、日志、指标
4. **即时修复**：解决问题的代码变更
5. **测试策略**：如何验证修复有效
6. **预防措施**：如何防止未来发生类似错误
7. **监控建议**：未来需要监控/告警什么
8. **运行手册**：处理类似事故的分步指南

优先考虑可操作的建议，以提高系统可靠性和减少未来事故的平均解决时间（MTTR）。