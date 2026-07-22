---
name: linkerd-patterns
description: "Linkerd 服务网格生产级模式——Kubernetes 轻量级安全优先的服务网格。当用户要求'配置 Linkerd'、'服务网格'、'mTLS'、'金丝雀部署流量分割'、'ServiceProfile'、'多集群服务网格'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

<!-- security-allowlist: curl-pipe-bash -->

# Linkerd 模式

Linkerd 服务网格生产级模式——Kubernetes 轻量级安全优先的服务网格。

## 不使用此技能的情况

- 任务与 Linkerd 模式无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和必要输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 使用此技能的情况

- 搭建轻量级服务网格
- 实现自动 mTLS
- 配置金丝雀部署的流量分割
- 配置 ServiceProfile 获取逐路由指标
- 实现重试和超时
- 多集群服务网格

## 核心概念

### 1. Linkerd 架构

```
┌─────────────────────────────────────────────┐
│                Control Plane                 │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ destiny │ │ identity │ │ proxy-inject │ │
│  └─────────┘ └──────────┘ └──────────────┘ │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────┐
│                 Data Plane                   │
│  ┌─────┐    ┌─────┐    ┌─────┐             │
│  │proxy│────│proxy│────│proxy│             │
│  └─────┘    └─────┘    └─────┘             │
│     │           │           │               │
│  ┌──┴──┐    ┌──┴──┐    ┌──┴──┐            │
│  │ app │    │ app │    │ app │            │
│  └─────┘    └─────┘    └─────┘            │
└─────────────────────────────────────────────┘
```

### 2. 关键资源

| 资源 | 用途 |
|------|------|
| **ServiceProfile** | 逐路由指标、重试、超时 |
| **TrafficSplit** | 金丝雀部署、A/B 测试 |
| **Server** | 定义服务端策略 |
| **ServerAuthorization** | 访问控制策略 |

## 模板

### 模板 1：Mesh 安装

```bash
# Install CLI
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh

# Validate cluster
linkerd check --pre

# Install CRDs
linkerd install --crds | kubectl apply -f -

# Install control plane
linkerd install | kubectl apply -f -

# Verify installation
linkerd check

# Install viz extension (optional)
linkerd viz install | kubectl apply -f -
```

### 模板 2：命名空间注入

```yaml
# Automatic injection for namespace
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
  annotations:
    linkerd.io/inject: enabled
---
# Or inject specific deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  annotations:
    linkerd.io/inject: enabled
spec:
  template:
    metadata:
      annotations:
        linkerd.io/inject: enabled
```

### 模板 3：带重试的 ServiceProfile

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: my-service.my-namespace.svc.cluster.local
  namespace: my-namespace
spec:
  routes:
    - name: GET /api/users
      condition:
        method: GET
        pathRegex: /api/users
      responseClasses:
        - condition:
            status:
              min: 500
              max: 599
          isFailure: true
      isRetryable: true
    - name: POST /api/users
      condition:
        method: POST
        pathRegex: /api/users
      # POST not retryable by default
      isRetryable: false
    - name: GET /api/users/{id}
      condition:
        method: GET
        pathRegex: /api/users/[^/]+
      timeout: 5s
      isRetryable: true
  retryBudget:
    retryRatio: 0.2
    minRetriesPerSecond: 10
    ttl: 10s
```

### 模板 4：流量分割（金丝雀）

```yaml
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: my-service-canary
  namespace: my-namespace
spec:
  service: my-service
  backends:
    - service: my-service-stable
      weight: 900m  # 90%
    - service: my-service-canary
      weight: 100m  # 10%
```

### 模板 5：服务端授权策略

```yaml
# Define the server
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  name: my-service-http
  namespace: my-namespace
spec:
  podSelector:
    matchLabels:
      app: my-service
  port: http
  proxyProtocol: HTTP/1
---
# Allow traffic from specific clients
apiVersion: policy.linkerd.io/v1beta1
kind: ServerAuthorization
metadata:
  name: allow-frontend
  namespace: my-namespace
spec:
  server:
    name: my-service-http
  client:
    meshTLS:
      serviceAccounts:
        - name: frontend
          namespace: my-namespace
---
# Allow unauthenticated traffic (e.g., from ingress)
apiVersion: policy.linkerd.io/v1beta1
kind: ServerAuthorization
metadata:
  name: allow-ingress
  namespace: my-namespace
spec:
  server:
    name: my-service-http
  client:
    unauthenticated: true
    networks:
      - cidr: 10.0.0.0/8
```

### 模板 6：HTTPRoute 高级路由

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: my-route
  namespace: my-namespace
spec:
  parentRefs:
    - name: my-service
      kind: Service
      group: core
      port: 8080
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api/v2
        - headers:
            - name: x-api-version
              value: v2
      backendRefs:
        - name: my-service-v2
          port: 8080
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: my-service-v1
          port: 8080
```

### 模板 7：多集群配置

```bash
# On each cluster, install with cluster credentials
linkerd multicluster install | kubectl apply -f -

# Link clusters
linkerd multicluster link --cluster-name west \
  --api-server-address https://west.example.com:6443 \
  | kubectl apply -f -

# Export a service to other clusters
kubectl label svc/my-service mirror.linkerd.io/exported=true

# Verify cross-cluster connectivity
linkerd multicluster check
linkerd multicluster gateways
```

## 监控命令

```bash
# Live traffic view
linkerd viz top deploy/my-app

# Per-route metrics
linkerd viz routes deploy/my-app

# Check proxy status
linkerd viz stat deploy -n my-namespace

# View service dependencies
linkerd viz edges deploy -n my-namespace

# Dashboard
linkerd viz dashboard
```

## 调试

```bash
# Check injection status
linkerd check --proxy -n my-namespace

# View proxy logs
kubectl logs deploy/my-app -c linkerd-proxy

# Debug identity/TLS
linkerd identity -n my-namespace

# Tap traffic (live)
linkerd viz tap deploy/my-app --to deploy/my-backend
```

## 最佳实践

### 应该做
- **全面启用 mTLS** — Linkerd 自动完成
- **使用 ServiceProfile** — 获取逐路由指标和重试能力
- **设置重试预算** — 防止重试风暴
- **监控黄金指标** — 成功率、延迟、吞吐量

### 不应该做
- **不要跳过 check** — 每次变更后务必运行 `linkerd check`
- **不要过度配置** — Linkerd 默认值已经合理
- **不要忽略 ServiceProfile** — 它们解锁高级功能
- **不要忘记超时** — 为每条路由设置合适的超时值

## 资源

- [Linkerd 文档](https://linkerd.io/2.14/overview/)
- [ServiceProfile](https://linkerd.io/2.14/features/service-profiles/)
- [授权策略](https://linkerd.io/2.14/features/server-policy/)

## 局限性
- 仅在任务明确符合上述范围时使用此技能
- 输出不能替代针对具体环境的验证、测试或专家评审
- 若缺少必要输入、权限、安全边界或成功标准，应停下来询问确认
