---
name: istio-traffic-management
description: "生产级服务网格部署的 Istio 流量管理全面指南。触发词：Istio流量管理、服务网格、VirtualService、DestinationRule、Gateway、canary部署、circuit breaker、流量镜像、故障注入、流量路由"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Istio Traffic Management

生产级服务网格部署的 Istio 流量管理全面指南。

## 不使用此技能的情况

- 任务与 Istio 流量管理无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 使用此技能的情况

- 配置服务间路由
- 实施 Canary 或 Blue-Green 部署
- 设置 Circuit Breaker 和重试策略
- 负载均衡配置
- 流量镜像用于测试
- 故障注入用于混沌工程

## 核心概念

### 1. 流量管理资源

| 资源 | 用途 | 作用范围 |
|------|------|----------|
| **VirtualService** | 将流量路由到目标 | 基于 Host |
| **DestinationRule** | 定义路由后的策略 | 基于 Service |
| **Gateway** | 配置入站/出站流量 | 集群边缘 |
| **ServiceEntry** | 添加外部服务 | 全网格 |

### 2. 流量流向

```
Client → Gateway → VirtualService → DestinationRule → Service
                   (routing)        (policies)        (pods)
```

## 模板

### 模板 1：基础路由

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-route
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - match:
        - headers:
            end-user:
              exact: jason
      route:
        - destination:
            host: reviews
            subset: v2
    - route:
        - destination:
            host: reviews
            subset: v1
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews-destination
  namespace: bookinfo
spec:
  host: reviews
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
    - name: v3
      labels:
        version: v3
```

### 模板 2：Canary 部署

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service-canary
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: stable
          weight: 90
        - destination:
            host: my-service
            subset: canary
          weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-service-dr
spec:
  host: my-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
  subsets:
    - name: stable
      labels:
        version: stable
    - name: canary
      labels:
        version: canary
```

### 模板 3：Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: circuit-breaker
spec:
  host: my-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
```

### 模板 4：重试与超时

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ratings-retry
spec:
  hosts:
    - ratings
  http:
    - route:
        - destination:
            host: ratings
      timeout: 10s
      retries:
        attempts: 3
        perTryTimeout: 3s
        retryOn: connect-failure,refused-stream,unavailable,cancelled,retriable-4xx,503
        retryRemoteLocalities: true
```

### 模板 5：流量镜像

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: mirror-traffic
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: v1
      mirror:
        host: my-service
        subset: v2
      mirrorPercentage:
        value: 100.0
```

### 模板 6：故障注入

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: fault-injection
spec:
  hosts:
    - ratings
  http:
    - fault:
        delay:
          percentage:
            value: 10
          fixedDelay: 5s
        abort:
          percentage:
            value: 5
          httpStatus: 503
      route:
        - destination:
            host: ratings
```

### 模板 7：Ingress Gateway

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: my-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: my-tls-secret
      hosts:
        - "*.example.com"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-vs
spec:
  hosts:
    - "api.example.com"
  gateways:
    - my-gateway
  http:
    - match:
        - uri:
            prefix: /api/v1
      route:
        - destination:
            host: api-service
            port:
              number: 8080
```

## 负载均衡策略

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: load-balancing
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN  # or LEAST_CONN, RANDOM, PASSTHROUGH
---
# Consistent hashing for sticky sessions
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: sticky-sessions
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: x-user-id
        # or: httpCookie, useSourceIp, httpQueryParameterName
```

## 最佳实践

### 推荐做法
- **从简单开始** — 逐步增加复杂度
- **使用 Subset** — 为服务明确版本标识
- **设置超时** — 始终配置合理的超时时间
- **启用重试** — 但需配合退避策略和次数限制
- **监控可观测性** — 使用 Kiali 和 Jaeger 获取流量可见性

### 避免做法
- **不要过度重试** — 可能导致级联故障
- **不要忽略异常检测** — 务必启用 Circuit Breaker
- **不要镜像到生产环境** — 应镜像到测试环境
- **不要跳过 Canary** — 先用小比例流量验证

## 调试命令

```bash
# Check VirtualService configuration
istioctl analyze

# View effective routes
istioctl proxy-config routes deploy/my-app -o json

# Check endpoint discovery
istioctl proxy-config endpoints deploy/my-app

# Debug traffic
istioctl proxy-config log deploy/my-app --level debug
```

## 参考资源

- [Istio Traffic Management](https://istio.io/latest/docs/concepts/traffic-management/)
- [Virtual Service Reference](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
- [Destination Rule Reference](https://istio.io/latest/docs/reference/config/networking/destination-rule/)

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出内容不能替代针对具体环境的验证、测试或专家评审。
- 当所需输入、权限、安全边界或成功标准不明确时，应停下来请求澄清。
