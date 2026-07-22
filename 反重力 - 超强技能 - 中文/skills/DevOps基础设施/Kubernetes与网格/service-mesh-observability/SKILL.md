---
name: service-mesh-observability
description: "Istio、Linkerd 和服务网格部署的可观测性模式完整指南。触发词：服务网格可观测性、分布式追踪、网格指标、Prometheus、Grafana、Jaeger、Kiali、OpenTelemetry、SLO、网格监控、链路追踪"
risk: critical
source: community
date_added: "2026-02-27"
---

# 服务网格可观测性

Istio、Linkerd 和服务网格部署的可观测性模式完整指南。

## 不适用场景

- 任务与服务网格可观测性无关
- 需要本范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 运用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 搭建跨服务的分布式追踪
- 实现服务网格指标和仪表盘
- 调试延迟和错误问题
- 定义服务通信的 SLO
- 可视化服务依赖关系
- 排查网格连接问题

## 核心概念

### 1. 可观测性三大支柱

```
┌─────────────────────────────────────────────────────┐
│                  Observability                       │
├─────────────────┬─────────────────┬─────────────────┤
│     Metrics     │     Traces      │      Logs       │
│                 │                 │                 │
│ • Request rate  │ • Span context  │ • Access logs   │
│ • Error rate    │ • Latency       │ • Error details │
│ • Latency P50   │ • Dependencies  │ • Debug info    │
│ • Saturation    │ • Bottlenecks   │ • Audit trail   │
└─────────────────┴─────────────────┴─────────────────┘
```

### 2. 网格黄金指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| **延迟** | 请求耗时 P50、P99 | P99 > 500ms |
| **流量** | 每秒请求数 | 异常检测 |
| **错误** | 5xx 错误率 | > 1% |
| **饱和度** | 资源利用率 | > 80% |

## 模板

### 模板 1：Istio + Prometheus & Grafana

```yaml
# Install Prometheus
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus
  namespace: istio-system
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'istio-mesh'
        kubernetes_sd_configs:
          - role: endpoints
            namespaces:
              names:
                - istio-system
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_name]
            action: keep
            regex: istio-telemetry
---
# ServiceMonitor for Prometheus Operator
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-mesh
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: istiod
  endpoints:
    - port: http-monitoring
      interval: 15s
```

### 模板 2：关键 Istio 指标查询

```promql
# 按服务统计请求速率
sum(rate(istio_requests_total{reporter="destination"}[5m])) by (destination_service_name)

# 错误率 (5xx)
sum(rate(istio_requests_total{reporter="destination", response_code=~"5.."}[5m]))
  / sum(rate(istio_requests_total{reporter="destination"}[5m])) * 100

# P99 延迟
histogram_quantile(0.99,
  sum(rate(istio_request_duration_milliseconds_bucket{reporter="destination"}[5m]))
  by (le, destination_service_name))

# TCP 连接数
sum(istio_tcp_connections_opened_total{reporter="destination"}) by (destination_service_name)

# 请求大小
histogram_quantile(0.99,
  sum(rate(istio_request_bytes_bucket{reporter="destination"}[5m]))
  by (le, destination_service_name))
```

### 模板 3：Jaeger 分布式追踪

```yaml
# Jaeger installation for Istio
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    enableTracing: true
    defaultConfig:
      tracing:
        sampling: 100.0  # 100% in dev, lower in prod
        zipkin:
          address: jaeger-collector.istio-system:9411
---
# Jaeger deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
        - name: jaeger
          image: jaegertracing/all-in-one:1.50
          ports:
            - containerPort: 5775   # UDP
            - containerPort: 6831   # Thrift
            - containerPort: 6832   # Thrift
            - containerPort: 5778   # Config
            - containerPort: 16686  # UI
            - containerPort: 14268  # HTTP
            - containerPort: 14250  # gRPC
            - containerPort: 9411   # Zipkin
          env:
            - name: COLLECTOR_ZIPKIN_HOST_PORT
              value: ":9411"
```

### 模板 4：Linkerd Viz 仪表盘

```bash
# 安装 Linkerd viz 扩展
linkerd viz install | kubectl apply -f -

# 访问仪表盘
linkerd viz dashboard

# CLI 可观测性命令
# Top 请求
linkerd viz top deploy/my-app

# 按路由的指标
linkerd viz routes deploy/my-app --to deploy/backend

# 实时流量检查
linkerd viz tap deploy/my-app --to deploy/backend

# 服务边（依赖关系）
linkerd viz edges deployment -n my-namespace
```

### 模板 5：Grafana 仪表盘 JSON

```json
{
  "dashboard": {
    "title": "Service Mesh Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(istio_requests_total{reporter=\"destination\"}[5m])) by (destination_service_name)",
            "legendFormat": "{{destination_service_name}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "sum(rate(istio_requests_total{response_code=~\"5..\"}[5m])) / sum(rate(istio_requests_total[5m])) * 100"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"value": 0, "color": "green"},
                {"value": 1, "color": "yellow"},
                {"value": 5, "color": "red"}
              ]
            }
          }
        }
      },
      {
        "title": "P99 Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, sum(rate(istio_request_duration_milliseconds_bucket{reporter=\"destination\"}[5m])) by (le, destination_service_name))",
            "legendFormat": "{{destination_service_name}}"
          }
        ]
      },
      {
        "title": "Service Topology",
        "type": "nodeGraph",
        "targets": [
          {
            "expr": "sum(rate(istio_requests_total{reporter=\"destination\"}[5m])) by (source_workload, destination_service_name)"
          }
        ]
      }
    ]
  }
}
```

### 模板 6：Kiali 服务网格可视化

```yaml
# Kiali installation
apiVersion: kiali.io/v1alpha1
kind: Kiali
metadata:
  name: kiali
  namespace: istio-system
spec:
  auth:
    strategy: anonymous  # or openid, token
  deployment:
    accessible_namespaces:
      - "**"
  external_services:
    prometheus:
      url: http://prometheus.istio-system:9090
    tracing:
      url: http://jaeger-query.istio-system:16686
    grafana:
      url: http://grafana.istio-system:3000
```

### 模板 7：OpenTelemetry 集成

```yaml
# OpenTelemetry Collector for mesh
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      zipkin:
        endpoint: 0.0.0.0:9411

    processors:
      batch:
        timeout: 10s

    exporters:
      jaeger:
        endpoint: jaeger-collector:14250
        tls:
          insecure: true
      prometheus:
        endpoint: 0.0.0.0:8889

    service:
      pipelines:
        traces:
          receivers: [otlp, zipkin]
          processors: [batch]
          exporters: [jaeger]
        metrics:
          receivers: [otlp]
          processors: [batch]
          exporters: [prometheus]
---
# Istio Telemetry v2 with OTel
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: istio-system
spec:
  tracing:
    - providers:
        - name: otel
      randomSamplingPercentage: 10
```

## 告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: mesh-alerts
  namespace: istio-system
spec:
  groups:
    - name: mesh.rules
      rules:
        - alert: HighErrorRate
          expr: |
            sum(rate(istio_requests_total{response_code=~"5.."}[5m])) by (destination_service_name)
            / sum(rate(istio_requests_total[5m])) by (destination_service_name) > 0.05
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate for {{ $labels.destination_service_name }}"

        - alert: HighLatency
          expr: |
            histogram_quantile(0.99, sum(rate(istio_request_duration_milliseconds_bucket[5m]))
            by (le, destination_service_name)) > 1000
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High P99 latency for {{ $labels.destination_service_name }}"

        - alert: MeshCertExpiring
          expr: |
            (certmanager_certificate_expiration_timestamp_seconds - time()) / 86400 < 7
          labels:
            severity: warning
          annotations:
            summary: "Mesh certificate expiring in less than 7 days"
```

## 最佳实践

### 推荐做法
- **合理采样** - 开发环境 100%，生产环境 1-10%
- **使用链路上下文** - 一致地传播 header
- **设置告警** - 针对黄金指标
- **关联指标与链路** - 使用 exemplar
- **分层存储** - 热/冷存储策略

### 避免做法
- **不要过度采样** - 存储成本会累积
- **不要忽视基数** - 限制标签值
- **不要跳过仪表盘** - 可视化依赖关系
- **不要忽略成本** - 监控可观测性本身的开销

## 参考资源

- [Istio 可观测性](https://istio.io/latest/docs/tasks/observability/)
- [Linkerd 可观测性](https://linkerd.io/2.14/features/dashboard/)
- [OpenTelemetry](https://opentelemetry.io/)
- [Kiali](https://kiali.io/)

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不可将输出内容替代针对特定环境的验证、测试或专家评审。
- 当所需输入、权限、安全边界或成功标准缺失时，请停下来请求澄清。
