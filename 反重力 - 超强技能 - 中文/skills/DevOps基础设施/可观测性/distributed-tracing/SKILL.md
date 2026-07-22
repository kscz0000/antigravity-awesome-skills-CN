---
name: distributed-tracing
description: "使用 Jaeger 和 Tempo 实现分布式追踪，实现微服务间请求流的可见性。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 分布式追踪

使用 Jaeger 和 Tempo 实现分布式追踪，实现微服务间请求流的可见性。

## 何时不使用此技能

- 任务与分布式追踪无关
- 需要此范围之外的其他领域或工具

## 说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 目的

跨分布式系统追踪请求，以了解延迟、依赖关系和故障点。

## 使用此技能的场景

- 调试延迟问题
- 理解服务依赖关系
- 识别瓶颈
- 追踪错误传播
- 分析请求路径

## 分布式追踪概念

### Trace 结构
```
Trace (Request ID: abc123)
  ↓
Span (frontend) [100ms]
  ↓
Span (api-gateway) [80ms]
  ├→ Span (auth-service) [10ms]
  └→ Span (user-service) [60ms]
      └→ Span (database) [40ms]
```

### 核心组件
- **Trace** - 端到端请求旅程
- **Span** - trace 中的单个操作
- **Context** - 服务间传播的元数据
- **Tags** - 用于过滤的键值对
- **Logs** - span 内的时间戳事件

## Jaeger 设置

### Kubernetes 部署

```bash
# 部署 Jaeger Operator
kubectl create namespace observability
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.51.0/jaeger-operator.yaml -n observability

# 部署 Jaeger 实例
kubectl apply -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
  namespace: observability
spec:
  strategy: production
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
  ingress:
    enabled: true
EOF
```

### Docker Compose

```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"  # UI
      - "14268:14268"  # Collector
      - "14250:14250"  # gRPC
      - "9411:9411"    # Zipkin
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
```

**参考：** 参见 `references/jaeger-setup.md`

## 应用程序埋点

### OpenTelemetry（推荐）

#### Python (Flask)
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

# 初始化 tracer
resource = Resource(attributes={SERVICE_NAME: "my-service"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# 埋点 Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route('/api/users')
def get_users():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("get_users") as span:
        span.set_attribute("user.count", 100)
        # 业务逻辑
        users = fetch_users_from_db()
        return {"users": users}

def fetch_users_from_db():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("database_query") as span:
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.statement", "SELECT * FROM users")
        # 数据库查询
        return query_database()
```

#### Node.js (Express)
```javascript
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');

// 初始化 tracer
const provider = new NodeTracerProvider({
  resource: { attributes: { 'service.name': 'my-service' } }
});

const exporter = new JaegerExporter({
  endpoint: 'http://jaeger:14268/api/traces'
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

// 埋点库
registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
  ],
});

const express = require('express');
const app = express();

app.get('/api/users', async (req, res) => {
  const tracer = trace.getTracer('my-service');
  const span = tracer.startSpan('get_users');

  try {
    const users = await fetchUsers();
    span.setAttributes({ 'user.count': users.length });
    res.json({ users });
  } finally {
    span.end();
  }
});
```

#### Go
```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
)

func initTracer() (*sdktrace.TracerProvider, error) {
    exporter, err := jaeger.New(jaeger.WithCollectorEndpoint(
        jaeger.WithEndpoint("http://jaeger:14268/api/traces"),
    ))
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("my-service"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func getUsers(ctx context.Context) ([]User, error) {
    tracer := otel.Tracer("my-service")
    ctx, span := tracer.Start(ctx, "get_users")
    defer span.End()

    span.SetAttributes(attribute.String("user.filter", "active"))

    users, err := fetchUsersFromDB(ctx)
    if err != nil {
        span.RecordError(err)
        return nil, err
    }

    span.SetAttributes(attribute.Int("user.count", len(users)))
    return users, nil
}
```

**参考：** 参见 `references/instrumentation.md`

## Context 传播

### HTTP 头
```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
tracestate: congo=t61rcWkgMzE
```

### HTTP 请求中的传播

#### Python
```python
from opentelemetry.propagate import inject

headers = {}
inject(headers)  # 注入 trace context

response = requests.get('http://downstream-service/api', headers=headers)
```

#### Node.js
```javascript
const { propagation } = require('@opentelemetry/api');

const headers = {};
propagation.inject(context.active(), headers);

axios.get('http://downstream-service/api', { headers });
```

## Tempo 设置（Grafana）

### Kubernetes 部署

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tempo-config
data:
  tempo.yaml: |
    server:
      http_listen_port: 3200

    distributor:
      receivers:
        jaeger:
          protocols:
            thrift_http:
            grpc:
        otlp:
          protocols:
            http:
            grpc:

    storage:
      trace:
        backend: s3
        s3:
          bucket: tempo-traces
          endpoint: s3.amazonaws.com

    querier:
      frontend_worker:
        frontend_address: tempo-query-frontend:9095
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tempo
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: tempo
        image: grafana/tempo:latest
        args:
          - -config.file=/etc/tempo/tempo.yaml
        volumeMounts:
        - name: config
          mountPath: /etc/tempo
      volumes:
      - name: config
        configMap:
          name: tempo-config
```

**参考：** 参见 `assets/jaeger-config.yaml.template`

## 采样策略

### 概率采样
```yaml
# 采样 1% 的 trace
sampler:
  type: probabilistic
  param: 0.01
```

### 限速采样
```yaml
# 每秒最多采样 100 个 trace
sampler:
  type: ratelimiting
  param: 100
```

### 自适应采样
```python
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

# 基于 trace ID 采样（确定性）
sampler = ParentBased(root=TraceIdRatioBased(0.01))
```

## Trace 分析

### 查找慢请求

**Jaeger 查询：**
```
service=my-service
duration > 1s
```

### 查找错误

**Jaeger 查询：**
```
service=my-service
error=true
tags.http.status_code >= 500
```

### 服务依赖图

Jaeger 自动生成服务依赖图，显示：
- 服务关系
- 请求速率
- 错误率
- 平均延迟

## 最佳实践

1. **合理采样**（生产环境 1-10%）
2. **添加有意义的标签**（user_id、request_id）
3. **跨所有服务边界传播 context**
4. **在 span 中记录异常**
5. **使用一致的命名**规范操作
6. **监控追踪开销**（CPU 影响 <1%）
7. **设置 trace 错误告警**
8. **实现分布式 context**（baggage）
9. **使用 span 事件**标记重要里程碑
10. **文档化埋点**标准

## 与日志集成

### 关联日志
```python
import logging
from opentelemetry import trace

logger = logging.getLogger(__name__)

def process_request():
    span = trace.get_current_span()
    trace_id = span.get_span_context().trace_id

    logger.info(
        "Processing request",
        extra={"trace_id": format(trace_id, '032x')}
    )
```

## 故障排查

**没有 trace 出现：**
- 检查 collector 端点
- 验证网络连接
- 检查采样配置
- 查看应用程序日志

**延迟开销过高：**
- 降低采样率
- 使用批量 span 处理器
- 检查 exporter 配置

## 参考文件

- `references/jaeger-setup.md` - Jaeger 安装
- `references/instrumentation.md` - 埋点模式
- `assets/jaeger-config.yaml.template` - Jaeger 配置

## 相关技能

- `prometheus-configuration` - 用于指标
- `grafana-dashboards` - 用于可视化
- `slo-implementation` - 用于延迟 SLO

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
