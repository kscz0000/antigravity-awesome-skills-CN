# 错误分析与解决实施手册

本文件包含本技能引用的详细模式、检查清单和代码示例。

## 错误检测与分类

### 错误分类法

将错误分类为以下类别，以指导调试策略：

**按严重程度：**
- **严重（Critical）**：系统宕机、数据丢失、安全漏洞、完整服务不可用
- **高（High）**：主要功能故障、重大用户影响、数据损坏风险
- **中（Medium）**：部分功能降级、有可用的变通方案、性能问题
- **低（Low）**：次要 bug、界面问题、影响极小的边缘情况

**按类型：**
- **运行时错误**：异常、崩溃、段错误、空指针解引用
- **逻辑错误**：行为错误、计算错误、状态转换非法
- **集成错误**：API 失败、网络超时、外部服务问题
- **性能错误**：内存泄漏、CPU 激增、慢查询、资源耗尽
- **配置错误**：环境变量缺失、设置无效、版本不匹配
- **安全错误**：身份验证失败、授权违规、注入攻击尝试

**按可观测性：**
- **确定性（Deterministic）**：在已知输入下可一致复现
- **间歇性（Intermittent）**：零星出现，通常与时序或竞态条件相关
- **环境性（Environmental）**：仅在特定环境或配置下出现
- **负载相关（Load-dependent）**：在高流量或资源压力下出现

### 错误检测策略

实施多层错误检测：

1. **应用层埋点**：使用错误跟踪 SDK（Sentry、DataDog Error Tracking、Rollbar）自动捕获未处理异常及其完整上下文
2. **健康检查端点**：监控 `/health` 和 `/ready` 端点，在影响用户前检测服务降级
3. **综合监控（Synthetic Monitoring）**：对生产环境运行自动化测试，主动发现问题
4. **真实用户监控（RUM）**：跟踪真实用户体验和前端错误
5. **日志模式分析**：使用 SIEM 工具识别错误峰值和异常模式
6. **APM 阈值告警**：对错误率上升、延迟峰值或吞吐量下降设置告警

### 错误聚合与模式识别

将相关错误分组以识别系统性问题：

- **指纹（Fingerprinting）**：按堆栈跟踪相似度、错误类型和受影响代码路径对错误分组
- **趋势分析**：跟踪错误频率随时间变化，检测回归或新出现的问题
- **相关性分析**：将错误与部署、配置变更或外部事件关联
- **用户影响评分**：按受影响用户数和会话数排定优先级
- **地理/时间模式**：识别特定区域或基于时间的错误集群

## 根因分析技术

### 系统化调查流程

针对每个错误遵循以下结构化方法：

1. **复现错误**：创建最小复现步骤。如为间歇性问题，需识别触发条件
2. **定位失败点**：缩小到产生失败的确切代码行或组件
3. **分析调用链**：从错误反向追踪，理解系统如何进入失败状态
4. **检查变量状态**：检查失败时及前序步骤中的值
5. **审查近期变更**：检查 git 历史中受影响代码路径的近期修改
6. **验证假设**：形成关于原因的猜想并通过针对性实验进行验证

### 五个为什么法（Five Whys）

反复追问"为什么"以深入挖掘根因：

```
错误：数据库连接 30 秒后超时

为什么？数据库连接池耗尽
为什么？所有连接都被长时间运行的查询占用
为什么？新功能引入了 N+1 查询模式
为什么？ORM 懒加载配置不正确
为什么？代码审查未发现该性能回归
```

根因：数据库查询模式的代码审查流程不充分。

### 分布式系统调试

针对微服务和分布式系统中的错误：

- **追踪请求路径**：使用关联 ID 跨服务边界跟踪请求
- **检查服务依赖**：识别涉及哪些上游/下游服务
- **分析级联失败**：判断是否为其他服务失败的衍生症状
- **审查熔断器状态**：检查保护机制是否被触发
- **检查消息队列**：查找背压、死信或处理延迟
- **时间线重建**：使用分布式追踪构建跨所有服务的事件时间线

## 堆栈跟踪分析

### 解读堆栈跟踪

从堆栈跟踪中提取最大信息量：

**关键元素：**
- **错误类型**：发生了什么类型的异常/错误
- **错误消息**：关于失败的上下文信息
- **起源点**：抛出错误的最深层栈帧
- **调用链**：导致错误的函数调用序列
- **框架代码 vs 应用代码**：区分库代码与你的代码
- **异步边界**：识别异步操作在哪里打断了追踪链

**分析策略：**
1. 从堆栈顶部（错误起源）开始
2. 定位应用代码中的第一个栈帧（非框架/库）
3. 检查该栈帧的上下文：输入参数、局部变量、状态
4. 沿调用函数反向追踪，理解无效状态是如何产生的
5. 寻找规律：是否在循环中？在回调内？异步操作之后？

### 堆栈跟踪增强

现代错误跟踪工具提供增强的堆栈跟踪：

- **源代码上下文**：查看每个栈帧周围的代码行
- **局部变量值**：检查每帧的变量状态（使用 Sentry 的 debug 模式）
- **Breadcrumbs**：查看导致错误的事件序列
- **发布追踪**：将错误链接到具体部署和提交
- **Source Maps**：对于压缩 JavaScript，映射回原始源码
- **内联注释**：为栈帧添加上下文信息的注释

### 常见堆栈跟踪模式

**模式：框架代码深处的空指针异常**
```
NullPointerException
  at java.util.HashMap.hash(HashMap.java:339)
  at java.util.HashMap.get(HashMap.java:556)
  at com.myapp.service.UserService.findUser(UserService.java:45)
```
根因：应用层向框架代码传入了 null。应聚焦于 UserService.java:45。

**模式：长时间等待后超时**
```
TimeoutException: Operation timed out after 30000ms
  at okhttp3.internal.http2.Http2Stream.waitForIo
  at com.myapp.api.PaymentClient.processPayment(PaymentClient.java:89)
```
根因：外部服务缓慢/无响应。需要重试逻辑和熔断器。

**模式：并发代码中的竞态条件**
```
ConcurrentModificationException
  at java.util.ArrayList$Itr.checkForComodification
  at com.myapp.processor.BatchProcessor.process(BatchProcessor.java:112)
```
根因：迭代过程中集合被修改。需要线程安全的数据结构或同步机制。

## 日志聚合与模式匹配

### 结构化日志实现

实现基于 JSON 的结构化日志，使日志可被机器读取：

**标准日志模式：**
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
- `trace_id` 和 `span_id`：用于分布式追踪的 OpenTelemetry 标识
- `service`：生成该日志的微服务
- `environment`：dev、staging、production
- `error.fingerprint`：用于对相似错误分组的稳定标识

### 关联 ID 模式

实现关联 ID 以跨分布式系统跟踪请求：

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

# 带有关联 ID 的结构化日志
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
2. **日志采集器**：Fluentd/Fluent Bit/Vector 从容器中采集日志
3. **日志聚合器**：Elasticsearch/Loki/DataDog 接收并索引日志
4. **可视化**：Kibana/Grafana/DataDog UI 用于查询和仪表盘
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

// 按指纹分组错误以找出最常见问题
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

使用日志分析识别模式：

- **错误率峰值**：将当前错误率与历史基线比较（例如 >3 个标准差）
- **新错误类型**：在出现之前未见过的错误指纹时告警
- **级联失败**：检测一个服务中的错误是否触发了依赖服务中的错误
- **用户影响模式**：识别哪些用户/群体受到不成比例的影响
- **地理模式**：发现特定区域问题（例如 CDN 问题、数据中心宕机）
- **时间模式**：查找基于时间的问题（例如批处理任务、定时任务、时区 bug）

## 调试工作流

### 交互式调试

针对开发环境中的确定性错误：

**调试器设置：**
1. 在错误发生前设置断点
2. 逐行跟踪代码执行
3. 检查变量值和对象状态
4. 在调试控制台中计算表达式
5. 观察意外的状态变化
6. 修改变量以测试猜想

**现代调试工具：**
- **VS Code 调试器**：针对 JavaScript、Python、Go、Java、C++ 的集成调试
- **Chrome DevTools**：前端调试，涵盖网络、性能和内存分析
- **pdb/ipdb（Python）**：支持事后分析的交互式调试器
- **dlv（Go）**：Go 程序的 Delve 调试器
- **lldb（C/C++）**：底层调试器，支持反向调试

### 生产环境调试

针对生产环境中无法使用调试器的错误：

**安全的生产环境调试技术：**

1. **增强日志**：在疑似失败点周围添加策略性日志语句
2. **特性开关（Feature Flags）**：为特定用户/请求启用详细日志
3. **采样**：对一定比例的请求记录详细上下文
4. **APM 事务追踪**：使用 DataDog APM 或 New Relic 查看详细的事务流
5. **分布式追踪**：利用 OpenTelemetry trace 理解跨服务交互
6. **性能分析**：使用持续性能分析器（DataDog Profiler、Pyroscope）识别热点
7. **堆转储**：捕获内存快照以分析内存泄漏
8. **流量镜像**：在预发布环境重放生产流量以安全调查

**远程调试（谨慎使用）：**
- 仅在非关键服务上将调试器附加到运行中的进程
- 使用只读断点，不暂停执行
- 严格限定调试会话时间
- 始终准备好回滚计划

### 内存与性能调试

**内存泄漏检测：**
```javascript
// Node.js 堆快照对比
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(filename) {
  const snapshot = v8.writeHeapSnapshot(filename);
  console.log(`Heap snapshot written to ${snapshot}`);
}

// 按间隔获取快照
takeHeapSnapshot('heap-before.heapsnapshot');
// ... 运行可能泄漏的操作 ...
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
    stats.print_stats(20)  # 打印耗时最多的前 20 个函数
```

## 错误预防策略

### 输入验证与类型安全

**防御性编程：**
```typescript
// TypeScript：利用类型系统实现编译期安全
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

  // 现在可以安全处理
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
    HALF_OPEN = "half_open"  # 测试服务是否已恢复

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
        # 优雅降级：排队稍后处理
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
        throw error; // 不可重试的错误直接抛出
      }

      if (attempt < options.maxAttempts - 1) {
        const delay = Math.min(
          options.baseDelayMs * Math.pow(options.exponentialBase, attempt),
          options.maxDelayMs
        );

        // 添加抖动以避免惊群效应
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
- **指标**：Prometheus + Grafana 或 DataDog
- **日志**：Elasticsearch/Loki + Fluentd 或 DataDog Logs
- **追踪**：OpenTelemetry + Jaeger/Tempo 或 DataDog APM
- **错误**：Sentry 或 DataDog Error Tracking
- **前端**：Sentry Browser SDK 或 DataDog RUM
- **综合监控（Synthetics）**：DataDog Synthetics 或 Checkly

### Sentry 集成

**Node.js/Express 配置：**
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

// 路由定义在此 ...

// 错误处理器（必须放在最后）
app.use(Sentry.Handlers.errorHandler());

// 手动捕获错误并附带上下文
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

**Python/Flask 配置：**
```python
from ddtrace import patch_all, tracer
from ddtrace.contrib.flask import TraceMiddleware
import logging

# 自动埋点常用库
patch_all()

app = Flask(__name__)

# 初始化追踪
TraceMiddleware(app, tracer, service='payment-service')

# 自定义 span 以实现详细追踪
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

**智能化告警策略：**

```yaml
# DataDog Monitor 配置
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

**阶段一：检测与分诊（0-5 分钟）**
1. 确认告警/事故
2. 检查事故严重程度和用户影响
3. 指定事故指挥官
4. 创建事故频道（#incident-2025-10-11-payment-errors）
5. 如面向客户则更新状态页

**阶段二：调查（5-30 分钟）**
1. 收集可观测性数据：
   - 来自 Sentry/DataDog 的错误率
   - 显示失败请求的追踪
   - 事故开始时间前后的日志
   - 显示资源使用、延迟、吞吐量的指标
2. 与近期变更关联：
   - 近期部署（检查 CI/CD 管道）
   - 配置变更
   - 基础设施变更
   - 外部依赖状态
3. 形成关于根因的初始假设
4. 在事故日志中记录发现

**阶段三：缓解（即时）**
1. 基于假设实施即时修复：
   - 回滚近期部署
   - 扩容资源
   - 禁用有问题的功能（功能开关）
   - 故障切换到备份系统
   - 应用热修复
2. 验证缓解措施是否生效（错误率下降）
3. 监控 15-30 分钟确保稳定

**阶段四：恢复与验证**
1. 验证所有系统运行正常
2. 检查数据一致性
3. 处理排队/失败的请求
4. 更新状态页：事故已解决
5. 通知相关方

**阶段五：事故后复盘**
1. 48 小时内安排复盘会
2. 创建详细的事件时间线
3. 识别根因（可能与初始假设不同）
4. 记录促成因素
5. 为以下事项创建行动项：
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

# 查找错误与部署的相关性（DataDog）
# 使用部署跟踪在错误图表上叠加部署标记
# 查询：sum:trace.express.request.errors{service:payment-service} by {version}

# 识别受影响用户（Sentry）
# 导航到 issue → User Impact 标签
# 显示：受影响用户总数、新用户 vs 回访用户、地理分布

# 追踪特定失败请求（OpenTelemetry/Jaeger）
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

针对每个错误分析，提供：

1. **错误摘要**：发生了什么、何时发生、影响范围
2. **根因**：错误发生的根本原因
3. **证据**：支持诊断结论的堆栈跟踪、日志、指标
4. **即时修复**：解决该问题的代码变更
5. **测试策略**：如何验证修复有效
6. **预防措施**：如何防止未来出现类似错误
7. **监控建议**：未来需要监控/告警的指标
8. **Runbook**：处理类似事故的分步指南

优先考虑可执行的建议，以提升系统可靠性并降低未来事故的 MTTR（平均恢复时间）。