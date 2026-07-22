---
name: grafana-dashboards
description: "创建和管理生产级 Grafana 仪表盘，实现全面的系统可观测性。适用于创建 Grafana 仪表盘、监控面板、可视化 Prometheus 指标、SLO 仪表盘、监控看板等场景。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Grafana Dashboards

创建和管理生产级 Grafana 仪表盘，实现全面的系统可观测性。

## 不适用场景

- 任务与 Grafana 仪表盘无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束条件和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，请打开 `resources/implementation-playbook.md`

## 目的

设计高效的 Grafana 仪表盘，用于监控应用、基础设施和业务指标。

## 适用场景

- 可视化 Prometheus 指标
- 创建自定义仪表盘
- 实现 SLO 仪表盘
- 监控基础设施
- 追踪业务 KPI

## 仪表盘设计原则

### 1. 信息层次
```
┌─────────────────────────────────────┐
│  Critical Metrics (Big Numbers)     │
├─────────────────────────────────────┤
│  Key Trends (Time Series)           │
├─────────────────────────────────────┤
│  Detailed Metrics (Tables/Heatmaps) │
└─────────────────────────────────────┘
```

### 2. RED 方法（服务）
- **Rate** - 每秒请求数
- **Errors** - 错误率
- **Duration** - 延迟/响应时间

### 3. USE 方法（资源）
- **Utilization** - 资源忙碌时间百分比
- **Saturation** - 队列长度/等待时间
- **Errors** - 错误计数

## 仪表盘结构

### API 监控仪表盘

```json
{
  "dashboard": {
    "title": "API Monitoring",
    "tags": ["api", "production"],
    "timezone": "browser",
    "refresh": "30s",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "Error Rate %",
        "type": "graph",
        "targets": [
          {
            "expr": "(sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))) * 100",
            "legendFormat": "Error Rate"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [5], "type": "gt"},
              "operator": {"type": "and"},
              "query": {"params": ["A", "5m", "now"]},
              "type": "query"
            }
          ]
        },
        "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "P95 Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 8, "w": 24, "h": 8}
      }
    ]
  }
}
```

**参考：** 参见 `assets/api-dashboard.json`

## 面板类型

### 1. Stat 面板（单值）
```json
{
  "type": "stat",
  "title": "Total Requests",
  "targets": [{
    "expr": "sum(http_requests_total)"
  }],
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"]
    },
    "orientation": "auto",
    "textMode": "auto",
    "colorMode": "value"
  },
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": 0, "color": "green"},
          {"value": 80, "color": "yellow"},
          {"value": 90, "color": "red"}
        ]
      }
    }
  }
}
```

### 2. 时间序列图
```json
{
  "type": "graph",
  "title": "CPU Usage",
  "targets": [{
    "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
  }],
  "yaxes": [
    {"format": "percent", "max": 100, "min": 0},
    {"format": "short"}
  ]
}
```

### 3. 表格面板
```json
{
  "type": "table",
  "title": "Service Status",
  "targets": [{
    "expr": "up",
    "format": "table",
    "instant": true
  }],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {"Time": true},
        "indexByName": {},
        "renameByName": {
          "instance": "Instance",
          "job": "Service",
          "Value": "Status"
        }
      }
    }
  ]
}
```

### 4. 热力图
```json
{
  "type": "heatmap",
  "title": "Latency Heatmap",
  "targets": [{
    "expr": "sum(rate(http_request_duration_seconds_bucket[5m])) by (le)",
    "format": "heatmap"
  }],
  "dataFormat": "tsbuckets",
  "yAxis": {
    "format": "s"
  }
}
```

## 变量

### 查询变量
```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_pod_info, namespace)",
        "refresh": 1,
        "multi": false
      },
      {
        "name": "service",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_service_info{namespace=\"$namespace\"}, service)",
        "refresh": 1,
        "multi": true
      }
    ]
  }
}
```

### 在查询中使用变量
```
sum(rate(http_requests_total{namespace="$namespace", service=~"$service"}[5m]))
```

## 仪表盘告警

```json
{
  "alert": {
    "name": "High Error Rate",
    "conditions": [
      {
        "evaluator": {
          "params": [5],
          "type": "gt"
        },
        "operator": {"type": "and"},
        "query": {
          "params": ["A", "5m", "now"]
        },
        "reducer": {"type": "avg"},
        "type": "query"
      }
    ],
    "executionErrorState": "alerting",
    "for": "5m",
    "frequency": "1m",
    "message": "Error rate is above 5%",
    "noDataState": "no_data",
    "notifications": [
      {"uid": "slack-channel"}
    ]
  }
}
```

## 仪表盘配置管理

**dashboards.yml:**
```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'General'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/dashboards
```

## 常用仪表盘模式

### 基础设施仪表盘

**核心面板：**
- 各节点 CPU 利用率
- 各节点内存使用量
- 磁盘 I/O
- 网络流量
- 各命名空间 Pod 数量
- 节点状态

**参考：** 参见 `assets/infrastructure-dashboard.json`

### 数据库仪表盘

**核心面板：**
- 每秒查询数
- 连接池使用率
- 查询延迟（P50、P95、P99）
- 活跃连接数
- 数据库大小
- 复制延迟
- 慢查询

**参考：** 参见 `assets/database-dashboard.json`

### 应用仪表盘

**核心面板：**
- 请求速率
- 错误率
- 响应时间（百分位）
- 活跃用户/会话
- 缓存命中率
- 队列长度

## 最佳实践

1. **从模板开始**（Grafana 社区仪表盘）
2. **使用一致的命名**规范面板和变量
3. **按行分组相关指标**
4. **设置合适的时间范围**（默认：最近 6 小时）
5. **使用变量**提高灵活性
6. **添加面板描述**提供上下文
7. **正确配置单位**
8. **设置有意义的阈值**用于颜色标识
9. **跨仪表盘使用一致的颜色**
10. **用不同时间范围测试**

## 仪表盘即代码

### Terraform 配置

```hcl
resource "grafana_dashboard" "api_monitoring" {
  config_json = file("${path.module}/dashboards/api-monitoring.json")
  folder      = grafana_folder.monitoring.id
}

resource "grafana_folder" "monitoring" {
  title = "Production Monitoring"
}
```

### Ansible 配置

```yaml
- name: Deploy Grafana dashboards
  copy:
    src: "{{ item }}"
    dest: /etc/grafana/dashboards/
  with_fileglob:
    - "dashboards/*.json"
  notify: restart grafana
```

## 参考文件

- `assets/api-dashboard.json` - API 监控仪表盘
- `assets/infrastructure-dashboard.json` - 基础设施仪表盘
- `assets/database-dashboard.json` - 数据库监控仪表盘
- `references/dashboard-design.md` - 仪表盘设计指南

## 相关技能

- `prometheus-configuration` - 用于指标采集
- `slo-implementation` - 用于 SLO 仪表盘

## 限制
- 仅在任务明确符合上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家评审。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
