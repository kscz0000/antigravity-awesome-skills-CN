# 监控和可观测性设置实施手册

此文件包含技能引用的详细模式、检查清单和代码示例。

# 监控和可观测性设置

您是专注于实施全面监控解决方案的监控和可观测性专家。设置指标收集、分布式追踪、日志聚合，并创建提供系统健康和性能完整可视化的洞察性仪表板。

## 上下文
用户需要实施或改进监控和可观测性。重点关注可观测性的三大支柱（指标、日志、追踪）、设置监控基础设施、创建可操作的仪表板以及建立有效的告警策略。

## 需求
$ARGUMENTS

## 指令

### 1. Prometheus 和指标设置

**Prometheus 配置**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts/*.yml"
  - "recording_rules/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'application'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

**自定义指标实现**
```typescript
// metrics.ts
import { Counter, Histogram, Gauge, Registry } from 'prom-client';

export class MetricsCollector {
    private registry: Registry;
    private httpRequestDuration: Histogram<string>;
    private httpRequestTotal: Counter<string>;

    constructor() {
        this.registry = new Registry();
        this.initializeMetrics();
    }

    private initializeMetrics() {
        this.httpRequestDuration = new Histogram({
            name: 'http_request_duration_seconds',
            help: 'Duration of HTTP requests in seconds',
            labelNames: ['method', 'route', 'status_code'],
            buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5]
        });

        this.httpRequestTotal = new Counter({
            name: 'http_requests_total',
            help: 'Total number of HTTP requests',
            labelNames: ['method', 'route', 'status_code']
        });

        this.registry.registerMetric(this.httpRequestDuration);
        this.registry.registerMetric(this.httpRequestTotal);
    }

    httpMetricsMiddleware() {
        return (req: Request, res: Response, next: NextFunction) => {
            const start = Date.now();
            const route = req.route?.path || req.path;

            res.on('finish', () => {
                const duration = (Date.now() - start) / 1000;
                const labels = {
                    method: req.method,
                    route,
                    status_code: res.statusCode.toString()
                };

                this.httpRequestDuration.observe(labels, duration);
                this.httpRequestTotal.inc(labels);
            });

            next();
        };
    }

    async getMetrics(): Promise<string> {
        return this.registry.metrics();
    }
}
```

### 2. Grafana 仪表板设置

**仪表板配置**
```typescript
// dashboards/service-dashboard.ts
export const createServiceDashboard = (serviceName: string) => {
    return {
        title: `${serviceName} Service Dashboard`,
        uid: `${serviceName}-overview`,
        tags: ['service', serviceName],
        time: { from: 'now-6h', to: 'now' },
        refresh: '30s',

        panels: [
            // Golden Signals
            {
                title: 'Request Rate',
                type: 'graph',
                gridPos: { x: 0, y: 0, w: 6, h: 8 },
                targets: [{
                    expr: `sum(rate(http_requests_total{service="${serviceName}"}[5m])) by (method)`,
                    legendFormat: '{{method}}'
                }]
            },
            {
                title: 'Error Rate',
                type: 'graph',
                gridPos: { x: 6, y: 0, w: 6, h: 8 },
                targets: [{
                    expr: `sum(rate(http_requests_total{service="${serviceName}",status_code=~"5.."}[5m])) / sum(rate(http_requests_total{service="${serviceName}"}[5m]))`,
                    legendFormat: 'Error %'
                }]
            },
            {
                title: 'Latency Percentiles',
                type: 'graph',
                gridPos: { x: 12, y: 0, w: 12, h: 8 },
                targets: [
                    {
                        expr: `histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{service="${serviceName}"}[5m])) by (le))`,
                        legendFormat: 'p50'
                    },
                    {
                        expr: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service="${serviceName}"}[5m])) by (le))`,
                        legendFormat: 'p95'
                    },
                    {
                        expr: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="${serviceName}"}[5m])) by (le))`,
                        legendFormat: 'p99'
                    }
                ]
            }
        ]
    };
};
```

### 3. 分布式追踪

**OpenTelemetry 配置**
```typescript
// tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';

export class TracingSetup {
    private sdk: NodeSDK;

    constructor(serviceName: string, environment: string) {
        const jaegerExporter = new JaegerExporter({
            endpoint: process.env.JAEGER_ENDPOINT || 'http://localhost:14268/api/traces',
        });

        this.sdk = new NodeSDK({
            resource: new Resource({
                [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
                [SemanticResourceAttributes.SERVICE_VERSION]: process.env.SERVICE_VERSION || '1.0.0',
                [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: environment,
            }),

            traceExporter: jaegerExporter,
            spanProcessor: new BatchSpanProcessor(jaegerExporter),

            instrumentations: [
                getNodeAutoInstrumentations({
                    '@opentelemetry/instrumentation-fs': { enabled: false },
                }),
            ],
        });
    }

    start() {
        this.sdk.start()
            .then(() => console.log('Tracing initialized'))
            .catch((error) => console.error('Error initializing tracing', error));
    }

    shutdown() {
        return this.sdk.shutdown();
    }
}
```

### 4. 日志聚合

**Fluentd 配置**
```yaml
# fluent.conf
<source>
  @type tail
  path /var/log/containers/*.log
  pos_file /var/log/fluentd-containers.log.pos
  tag kubernetes.*
  <parse>
    @type json
    time_format %Y-%m-%dT%H:%M:%S.%NZ
  </parse>
</source>

<filter kubernetes.**>
  @type kubernetes_metadata
  kubernetes_url "#{ENV['KUBERNETES_SERVICE_HOST']}"
</filter>

<filter kubernetes.**>
  @type record_transformer
  <record>
    cluster_name ${ENV['CLUSTER_NAME']}
    environment ${ENV['ENVIRONMENT']}
    @timestamp ${time.strftime('%Y-%m-%dT%H:%M:%S.%LZ')}
  </record>
</filter>

<match kubernetes.**>
  @type elasticsearch
  host "#{ENV['FLUENT_ELASTICSEARCH_HOST']}"
  port "#{ENV['FLUENT_ELASTICSEARCH_PORT']}"
  index_name logstash
  logstash_format true
  <buffer>
    @type file
    path /var/log/fluentd-buffers/kubernetes.buffer
    flush_interval 5s
    chunk_limit_size 2M
  </buffer>
</match>
```

**结构化日志库**
```python
# structured_logging.py
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

class StructuredLogger:
    def __init__(self, name: str, service: str, version: str):
        self.logger = logging.getLogger(name)
        self.service = service
        self.version = version
        self.default_context = {
            'service': service,
            'version': version,
            'environment': os.getenv('ENVIRONMENT', 'development')
        }

    def _format_log(self, level: str, message: str, context: Dict[str, Any]) -> str:
        log_entry = {
            '@timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'message': message,
            **self.default_context,
            **context
        }

        trace_context = self._get_trace_context()
        if trace_context:
            log_entry['trace'] = trace_context

        return json.dumps(log_entry)

    def info(self, message: str, **context):
        log_msg = self._format_log('INFO', message, context)
        self.logger.info(log_msg)

    def error(self, message: str, error: Optional[Exception] = None, **context):
        if error:
            context['error'] = {
                'type': type(error).__name__,
                'message': str(error),
                'stacktrace': traceback.format_exc()
            }

        log_msg = self._format_log('ERROR', message, context)
        self.logger.error(log_msg)
```

### 5. 告警配置

**告警规则**
```yaml
# alerts/application.yml
groups:
  - name: application
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (service)
          / sum(rate(http_requests_total[5m])) by (service) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: SlowResponseTime
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow response time on {{ $labels.service }}"

  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: avg(rate(container_cpu_usage_seconds_total[5m])) by (pod) > 0.8
        for: 15m
        labels:
          severity: warning

      - alert: HighMemoryUsage
        expr: |
          container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.9
        for: 10m
        labels:
          severity: critical
```

**Alertmanager 配置**
```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '$SLACK_API_URL'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'

  routes:
    - match:
        severity: critical
      receiver: pagerduty
      continue: true

    - match_re:
        severity: critical|warning
      receiver: slack

receivers:
  - name: 'slack'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '$PAGERDUTY_SERVICE_KEY'
        description: '{{ .GroupLabels.alertname }}: {{ .Annotations.summary }}'
```

### 6. SLO 实现

**SLO 配置**
```typescript
// slo-manager.ts
interface SLO {
    name: string;
    target: number; // e.g., 99.9
    window: string; // e.g., '30d'
    burnRates: BurnRate[];
}

export class SLOManager {
    private slos: SLO[] = [
        {
            name: 'API Availability',
            target: 99.9,
            window: '30d',
            burnRates: [
                { window: '1h', threshold: 14.4, severity: 'critical' },
                { window: '6h', threshold: 6, severity: 'critical' },
                { window: '1d', threshold: 3, severity: 'warning' }
            ]
        }
    ];

    generateSLOQueries(): string {
        return this.slos.map(slo => this.generateSLOQuery(slo)).join('\n\n');
    }

    private generateSLOQuery(slo: SLO): string {
        const errorBudget = 1 - (slo.target / 100);

        return `
# ${slo.name} SLO
- record: slo:${this.sanitizeName(slo.name)}:error_budget
  expr: ${errorBudget}

- record: slo:${this.sanitizeName(slo.name)}:consumed_error_budget
  expr: |
    1 - (sum(rate(successful_requests[${slo.window}])) / sum(rate(total_requests[${slo.window}])))
        `;
    }
}
```

### 7. 基础设施即代码

**Terraform 配置**
```hcl
# monitoring.tf
module "prometheus" {
  source = "./modules/prometheus"

  namespace = "monitoring"
  storage_size = "100Gi"
  retention_days = 30

  external_labels = {
    cluster = var.cluster_name
    region  = var.region
  }
}

module "grafana" {
  source = "./modules/grafana"

  namespace = "monitoring"
  admin_password = var.grafana_admin_password

  datasources = [
    {
      name = "Prometheus"
      type = "prometheus"
      url  = "http://prometheus:9090"
    }
  ]
}

module "alertmanager" {
  source = "./modules/alertmanager"

  namespace = "monitoring"

  config = templatefile("${path.module}/alertmanager.yml", {
    slack_webhook = var.slack_webhook
    pagerduty_key = var.pagerduty_service_key
  })
}
```

## 输出格式

1. **基础设施评估**：当前监控能力分析
2. **监控架构**：完整监控栈设计
3. **实施计划**：分步部署指南
4. **指标定义**：全面的指标目录
5. **仪表板模板**：开箱即用的 Grafana 仪表板
6. **告警运行手册**：详细的告警响应流程
7. **SLO 定义**：服务级别目标和错误预算
8. **集成指南**：服务插桩说明

重点创建一个提供可操作洞察、减少 MTTR 并支持主动问题检测的监控系统。