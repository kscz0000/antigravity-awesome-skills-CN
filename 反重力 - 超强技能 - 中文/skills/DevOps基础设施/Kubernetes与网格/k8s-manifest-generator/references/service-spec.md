# Kubernetes Service 规范参考

Kubernetes Service 资源的综合参考，涵盖 Service 类型、网络、负载均衡和服务发现模式。

## 概述

Service 为访问 Pod 提供稳定的网络端点。Service 通过提供服务发现和负载均衡，实现微服务之间的松耦合。

## Service 类型

### 1. ClusterIP（默认）

在集群内部 IP 上暴露 Service，仅可从集群内部访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  sessionAffinity: None
```

**适用场景：**
- 内部微服务通信
- 数据库服务
- 内部 API
- 消息队列

### 2. NodePort

在每个 Node 的 IP 上以静态端口（30000-32767 范围）暴露 Service。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - name: http
    port: 80
    targetPort: 8080
    nodePort: 30080  # Optional, auto-assigned if omitted
    protocol: TCP
```

**适用场景：**
- 开发/测试环境的外部访问
- 无负载均衡器的小型部署
- 需要直接访问 Node 的场景

**局限性：**
- 端口范围有限（30000-32767）
- 需自行处理 Node 故障
- 无内置跨 Node 负载均衡

### 3. LoadBalancer

使用云提供商的负载均衡器暴露 Service。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: public-api
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  loadBalancerSourceRanges:
  - 203.0.113.0/24
```

**云平台专用注解：**

**AWS：**
```yaml
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: "nlb"  # or "external"
  service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
  service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
  service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
  service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
```

**Azure：**
```yaml
annotations:
  service.beta.kubernetes.io/azure-load-balancer-internal: "true"
  service.beta.kubernetes.io/azure-pip-name: "my-public-ip"
```

**GCP：**
```yaml
annotations:
  cloud.google.com/load-balancer-type: "Internal"
  cloud.google.com/backend-config: '{"default": "my-backend-config"}'
```

### 4. ExternalName

将 Service 映射到外部 DNS 名称（CNAME 记录）。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.external.example.com
  ports:
  - port: 5432
```

**适用场景：**
- 访问外部服务
- 服务迁移场景
- 多集群服务引用

## 完整 Service 规范

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: production
  labels:
    app: my-app
    tier: backend
  annotations:
    description: "Main application service"
    prometheus.io/scrape: "true"
spec:
  # Service type
  type: ClusterIP

  # Pod selector
  selector:
    app: my-app
    version: v1

  # Ports configuration
  ports:
  - name: http
    port: 80           # Service port
    targetPort: 8080   # Container port (or named port)
    protocol: TCP      # TCP, UDP, or SCTP

  # Session affinity
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800

  # IP configuration
  clusterIP: 10.0.0.10  # Optional: specific IP
  clusterIPs:
  - 10.0.0.10
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack

  # External traffic policy
  externalTrafficPolicy: Local

  # Internal traffic policy
  internalTrafficPolicy: Local

  # Health check
  healthCheckNodePort: 30000

  # Load balancer config (for type: LoadBalancer)
  loadBalancerIP: 203.0.113.100
  loadBalancerSourceRanges:
  - 203.0.113.0/24

  # External IPs
  externalIPs:
  - 80.11.12.10

  # Publishing strategy
  publishNotReadyAddresses: false
```

## 端口配置

### 命名端口

在 Pod 中使用命名端口以获得灵活性：

**Deployment：**
```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        ports:
        - name: http
          containerPort: 8080
        - name: metrics
          containerPort: 9090
```

**Service：**
```yaml
spec:
  ports:
  - name: http
    port: 80
    targetPort: http  # References named port
  - name: metrics
    port: 9090
    targetPort: metrics
```

### 多端口

```yaml
spec:
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  - name: grpc
    port: 9090
    targetPort: 9090
    protocol: TCP
```

## 会话亲和性

### None（默认）

随机将请求分发到各个 Pod。

```yaml
spec:
  sessionAffinity: None
```

### ClientIP

将来自同一客户端 IP 的请求路由到同一 Pod。

```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours
```

**适用场景：**
- 有状态应用
- 基于会话的应用
- WebSocket 连接

## 流量策略

### 外部流量策略

**Cluster（默认）：**
```yaml
spec:
  externalTrafficPolicy: Cluster
```
- 跨所有 Node 进行负载均衡
- 可能增加额外网络跳数
- 源 IP 被屏蔽

**Local：**
```yaml
spec:
  externalTrafficPolicy: Local
```
- 流量仅发送到接收 Node 上的 Pod
- 保留客户端源 IP
- 更好的性能（无额外跳数）
- 可能导致负载不均

### 内部流量策略

```yaml
spec:
  internalTrafficPolicy: Local  # or Cluster
```

控制集群内部客户端的流量路由。

## Headless Service

无集群 IP 的 Service，用于直接访问 Pod。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database
spec:
  clusterIP: None  # Headless
  selector:
    app: database
  ports:
  - port: 5432
    targetPort: 5432
```

**适用场景：**
- StatefulSet Pod 发现
- Pod 间直接通信
- 自定义负载均衡
- 数据库集群

**DNS 返回：**
- 各个 Pod 的 IP 而非 Service IP
- 格式：`<pod-name>.<service-name>.<namespace>.svc.cluster.local`

## 服务发现

### DNS

**ClusterIP Service：**
```
<service-name>.<namespace>.svc.cluster.local
```

示例：
```bash
curl http://backend-service.production.svc.cluster.local
```

**同一 Namespace 内：**
```bash
curl http://backend-service
```

**Headless Service（返回 Pod IP）：**
```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

### 环境变量

Kubernetes 将 Service 信息注入 Pod：

```bash
# Service host and port
BACKEND_SERVICE_SERVICE_HOST=10.0.0.100
BACKEND_SERVICE_SERVICE_PORT=80

# For named ports
BACKEND_SERVICE_SERVICE_PORT_HTTP=80
```

**注意：** Pod 必须在 Service 创建之后创建，环境变量才会被注入。

## 负载均衡

### 算法

Kubernetes 默认使用随机选择。高级负载均衡方案：

**Service Mesh（Istio 示例）：**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-destination-rule
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST  # or ROUND_ROBIN, RANDOM, PASSTHROUGH
    connectionPool:
      tcp:
        maxConnections: 100
```

### 连接限制

使用 Pod 干扰预算和资源限制：

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-app
```

## Service Mesh 集成

### Istio Virtual Service

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: my-service
        subset: v2
  - route:
    - destination:
        host: my-service
        subset: v1
      weight: 90
    - destination:
        host: my-service
        subset: v2
      weight: 10
```

## 常见模式

### 模式 1：内部微服务

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: backend
  labels:
    app: user-service
    tier: backend
spec:
  type: ClusterIP
  selector:
    app: user-service
  ports:
  - name: http
    port: 8080
    targetPort: http
    protocol: TCP
  - name: grpc
    port: 9090
    targetPort: grpc
    protocol: TCP
```

### 模式 2：带负载均衡器的公共 API

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  selector:
    app: api-gateway
  ports:
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  loadBalancerSourceRanges:
  - 0.0.0.0/0
```

### 模式 3：StatefulSet 配合 Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cassandra
spec:
  clusterIP: None
  selector:
    app: cassandra
  ports:
  - port: 9042
    targetPort: 9042
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cassandra
spec:
  serviceName: cassandra
  replicas: 3
  selector:
    matchLabels:
      app: cassandra
  template:
    metadata:
      labels:
        app: cassandra
    spec:
      containers:
      - name: cassandra
        image: cassandra:4.0
```

### 模式 4：外部服务映射

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-database
spec:
  type: ExternalName
  externalName: prod-db.cxyz.us-west-2.rds.amazonaws.com
---
# Or with Endpoints for IP-based external service
apiVersion: v1
kind: Service
metadata:
  name: external-api
spec:
  ports:
  - port: 443
    targetPort: 443
    protocol: TCP
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-api
subsets:
- addresses:
  - ip: 203.0.113.100
  ports:
  - port: 443
```

### 模式 5：带监控指标的多端口 Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
spec:
  type: ClusterIP
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: metrics
    port: 9090
    targetPort: 9090
```

## NetworkPolicy

控制 Service 的流量：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

## 最佳实践

### Service 配置

1. **使用命名端口** 以获得灵活性
2. **根据暴露需求设置合适的 Service 类型**
3. **在 Deployment 和 Service 之间保持标签和选择器一致**
4. **为有状态应用配置会话亲和性**
5. **为保留源 IP 设置外部流量策略为 Local**
6. **为 StatefulSet 使用 Headless Service**
7. **实施 NetworkPolicy** 以保障安全
8. **添加监控注解** 以实现可观测性

### 生产检查清单

- [ ] Service 类型适合使用场景
- [ ] 选择器匹配 Pod 标签
- [ ] 使用命名端口以增强可读性
- [ ] 已按需配置会话亲和性
- [ ] 流量策略设置恰当
- [ ] 负载均衡器注解已配置（如适用）
- [ ] 源 IP 范围已限制（针对公共 Service）
- [ ] 健康检查配置已验证
- [ ] 监控注解已添加
- [ ] NetworkPolicy 已定义

### 性能调优

**高流量场景：**
```yaml
spec:
  externalTrafficPolicy: Local
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

**WebSocket/长连接场景：**
```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 86400  # 24 hours
```

## 故障排查

### Service 不可访问

```bash
# Check service exists
kubectl get service <service-name>

# Check endpoints (should show pod IPs)
kubectl get endpoints <service-name>

# Describe service
kubectl describe service <service-name>

# Check if pods match selector
kubectl get pods -l app=<app-name>
```

**常见问题：**
- 选择器不匹配 Pod 标签
- 无运行中的 Pod（端点为空）
- 端口配置错误
- NetworkPolicy 阻断流量

### DNS 解析失败

```bash
# Test DNS from pod
kubectl run debug --rm -it --image=busybox -- nslookup <service-name>

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### 负载均衡器问题

```bash
# Check load balancer status
kubectl describe service <service-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Verify cloud provider configuration
kubectl describe node
```

## 相关资源

- [Kubernetes Service API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#service-v1-core)
- [Service Networking](https://kubernetes.io/docs/concepts/services-networking/service/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
