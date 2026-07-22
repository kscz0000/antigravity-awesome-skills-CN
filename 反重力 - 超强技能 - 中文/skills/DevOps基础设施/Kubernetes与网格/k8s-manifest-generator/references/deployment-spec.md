# Kubernetes Deployment 规范参考

Kubernetes Deployment 资源的综合参考，涵盖所有关键字段、最佳实践和常见模式。

## 概述

Deployment 为 Pod 和 ReplicaSet 提供声明式更新。它管理应用的期望状态，处理滚动更新、回滚和扩缩容操作。

## 完整 Deployment 规范

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: my-system
  annotations:
    description: "Main application deployment"
    contact: "backend-team@example.com"
spec:
  # Replica management
  replicas: 3
  revisionHistoryLimit: 10

  # Pod selection
  selector:
    matchLabels:
      app: my-app
      version: v1

  # Update strategy
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  # Minimum time for pod to be ready
  minReadySeconds: 10

  # Deployment will fail if it doesn't progress in this time
  progressDeadlineSeconds: 600

  # Pod template
  template:
    metadata:
      labels:
        app: my-app
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      # Service account for RBAC
      serviceAccountName: my-app

      # Security context for the pod
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      # Init containers run before main containers
      initContainers:
      - name: init-db
        image: busybox:1.36
        command: ['sh', '-c', 'until nc -z db-service 5432; do sleep 1; done']
        securityContext:
          allowPrivilegeEscalation: false
          runAsNonRoot: true
          runAsUser: 1000

      # Main containers
      containers:
      - name: app
        image: myapp:1.0.0
        imagePullPolicy: IfNotPresent

        # Container ports
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP

        # Environment variables
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url

        # ConfigMap and Secret references
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets

        # Resource requests and limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Liveness probe
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
            httpHeaders:
            - name: Custom-Header
              value: Awesome
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3

        # Readiness probe
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3

        # Startup probe (for slow-starting containers)
        startupProbe:
          httpGet:
            path: /health/startup
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 30

        # Volume mounts
        volumeMounts:
        - name: data
          mountPath: /var/lib/app
        - name: config
          mountPath: /etc/app
          readOnly: true
        - name: tmp
          mountPath: /tmp

        # Security context for container
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL

        # Lifecycle hooks
        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", "echo Container started > /tmp/started"]
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

      # Volumes
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: app-data
      - name: config
        configMap:
          name: app-config
      - name: tmp
        emptyDir: {}

      # DNS configuration
      dnsPolicy: ClusterFirst
      dnsConfig:
        options:
        - name: ndots
          value: "2"

      # Scheduling
      nodeSelector:
        disktype: ssd

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - my-app
              topologyKey: kubernetes.io/hostname

      tolerations:
      - key: "app"
        operator: "Equal"
        value: "my-app"
        effect: "NoSchedule"

      # Termination
      terminationGracePeriodSeconds: 30

      # Image pull secrets
      imagePullSecrets:
      - name: regcred
```

## 字段参考

### 元数据字段

#### 必填字段
- `apiVersion`：`apps/v1`（当前稳定版本）
- `kind`：`Deployment`
- `metadata.name`：Namespace 内唯一名称

#### 推荐元数据
- `metadata.namespace`：目标 Namespace（默认为 `default`）
- `metadata.labels`：用于组织的键值对
- `metadata.annotations`：非标识性元数据

### Spec 字段

#### 副本管理

**`replicas`**（整数，默认：1）
- 期望的 Pod 实例数量
- 最佳实践：生产环境使用 3 个以上副本实现高可用
- 可手动扩缩容或通过 HorizontalPodAutoscaler 自动扩缩容

**`revisionHistoryLimit`**（整数，默认：10）
- 保留用于回滚的旧 ReplicaSet 数量
- 设为 0 禁用回滚能力
- 减少长期运行部署的存储开销

#### 更新策略

**`strategy.type`**（字符串）
- `RollingUpdate`（默认）：逐步替换 Pod
- `Recreate`：先删除所有 Pod 再创建新的

**`strategy.rollingUpdate.maxSurge`**（整数或百分比，默认：25%）
- 更新期间超出期望副本数的最大 Pod 数
- 示例：3 副本且 maxSurge=1 时，更新期间最多 4 个 Pod

**`strategy.rollingUpdate.maxUnavailable`**（整数或百分比，默认：25%）
- 更新期间低于期望副本数的最大 Pod 数
- 设为 0 实现零停机部署
- maxSurge 为 0 时不能设为 0

**最佳实践：**
```yaml
# Zero-downtime deployment
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0

# Fast deployment (can have brief downtime)
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 2
    maxUnavailable: 1

# Complete replacement
strategy:
  type: Recreate
```

#### Pod 模板

**`template.metadata.labels`**
- 必须包含与 `spec.selector.matchLabels` 匹配的标签
- 添加版本标签以支持蓝绿部署
- 包含标准 Kubernetes 标签

**`template.spec.containers`**（必填）
- 容器规格数组
- 至少需要一个容器
- 每个容器需要唯一名称

#### 容器配置

**镜像管理：**
```yaml
containers:
- name: app
  image: registry.example.com/myapp:1.0.0
  imagePullPolicy: IfNotPresent  # or Always, Never
```

镜像拉取策略：
- `IfNotPresent`：未缓存时拉取（带标签镜像的默认值）
- `Always`：始终拉取（:latest 的默认值）
- `Never`：从不拉取，未缓存则失败

**端口声明：**
```yaml
ports:
- name: http      # Named for referencing in Service
  containerPort: 8080
  protocol: TCP   # TCP (default), UDP, or SCTP
  hostPort: 8080  # Optional: Bind to host port (rarely used)
```

#### 资源管理

**请求 vs 限制：**

```yaml
resources:
  requests:
    memory: "256Mi"  # Guaranteed resources
    cpu: "250m"      # 0.25 CPU cores
  limits:
    memory: "512Mi"  # Maximum allowed
    cpu: "500m"      # 0.5 CPU cores
```

**QoS 类别（自动判定）：**

1. **Guaranteed**：所有容器的 requests = limits
   - 最高优先级
   - 最后被驱逐

2. **Burstable**：requests < limits 或仅设置了 requests
   - 中等优先级
   - 在 Guaranteed 之前被驱逐

3. **BestEffort**：未设置 requests 或 limits
   - 最低优先级
   - 最先被驱逐

**最佳实践：**
- 生产环境始终设置 requests
- 设置 limits 防止资源垄断
- 内存 limits 应为 requests 的 1.5-2 倍
- 突发工作负载的 CPU limits 可以更高

#### 健康检查

**探针类型：**

1. **startupProbe** - 用于慢启动应用
   ```yaml
   startupProbe:
     httpGet:
       path: /health/startup
       port: 8080
     initialDelaySeconds: 0
     periodSeconds: 10
     failureThreshold: 30  # 5 minutes to start (10s * 30)
   ```

2. **livenessProbe** - 重启不健康的容器
   ```yaml
   livenessProbe:
     httpGet:
       path: /health/live
       port: 8080
     initialDelaySeconds: 30
     periodSeconds: 10
     timeoutSeconds: 5
     failureThreshold: 3  # Restart after 3 failures
   ```

3. **readinessProbe** - 控制流量路由
   ```yaml
   readinessProbe:
     httpGet:
       path: /health/ready
       port: 8080
     initialDelaySeconds: 5
     periodSeconds: 5
     failureThreshold: 3  # Remove from service after 3 failures
   ```

**探针机制：**

```yaml
# HTTP GET
httpGet:
  path: /health
  port: 8080
  httpHeaders:
  - name: Authorization
    value: Bearer token

# TCP Socket
tcpSocket:
  port: 3306

# Command execution
exec:
  command:
  - cat
  - /tmp/healthy

# gRPC (Kubernetes 1.24+)
grpc:
  port: 9090
  service: my.service.health.v1.Health
```

**探针时序参数：**

- `initialDelaySeconds`：首次探测前的等待时间
- `periodSeconds`：探测间隔
- `timeoutSeconds`：探测超时时间
- `successThreshold`：标记为健康所需的成功次数（liveness/startup 为 1）
- `failureThreshold`：采取行动前的失败次数

#### 安全上下文

**Pod 级安全上下文：**
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    fsGroupChangePolicy: OnRootMismatch
    seccompProfile:
      type: RuntimeDefault
```

**容器级安全上下文：**
```yaml
containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 1000
    capabilities:
      drop:
      - ALL
      add:
      - NET_BIND_SERVICE  # Only if needed
```

**安全最佳实践：**
- 始终以非 root 运行（`runAsNonRoot: true`）
- 丢弃所有权限，仅添加需要的
- 尽可能使用只读根文件系统
- 启用 seccomp 配置
- 禁用权限提升

#### 卷

**卷类型：**

```yaml
volumes:
# PersistentVolumeClaim
- name: data
  persistentVolumeClaim:
    claimName: app-data

# ConfigMap
- name: config
  configMap:
    name: app-config
    items:
    - key: app.properties
      path: application.properties

# Secret
- name: secrets
  secret:
    secretName: app-secrets
    defaultMode: 0400

# EmptyDir (ephemeral)
- name: cache
  emptyDir:
    sizeLimit: 1Gi

# HostPath (avoid in production)
- name: host-data
  hostPath:
    path: /data
    type: DirectoryOrCreate
```

#### 调度

**Node 选择：**

```yaml
# Simple node selector
nodeSelector:
  disktype: ssd
  zone: us-west-1a

# Node affinity (more expressive)
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/arch
          operator: In
          values:
          - amd64
          - arm64
```

**Pod 亲和性/反亲和性：**

```yaml
# Spread pods across nodes
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: my-app
      topologyKey: kubernetes.io/hostname

# Co-locate with database
affinity:
  podAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: database
        topologyKey: kubernetes.io/hostname
```

**容忍度：**

```yaml
tolerations:
- key: "node.kubernetes.io/unreachable"
  operator: "Exists"
  effect: "NoExecute"
  tolerationSeconds: 30
- key: "dedicated"
  operator: "Equal"
  value: "database"
  effect: "NoSchedule"
```

## 常见模式

### 高可用 Deployment

```yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: my-app
            topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: my-app
```

### Sidecar 容器模式

```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log
      - name: log-forwarder
        image: fluent-bit:2.0
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log
          readOnly: true
      volumes:
      - name: shared-logs
        emptyDir: {}
```

### 依赖等待的 Init Container

```yaml
spec:
  template:
    spec:
      initContainers:
      - name: wait-for-db
        image: busybox:1.36
        command:
        - sh
        - -c
        - |
          until nc -z database-service 5432; do
            echo "Waiting for database..."
            sleep 2
          done
      - name: run-migrations
        image: myapp:1.0.0
        command: ["./migrate", "up"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
      containers:
      - name: app
        image: myapp:1.0.0
```

## 最佳实践

### 生产检查清单

- [ ] 设置资源请求和限制
- [ ] 实现三种探针（startup、liveness、readiness）
- [ ] 使用明确的镜像标签（不使用 :latest）
- [ ] 配置安全上下文（非 root、只读文件系统）
- [ ] 副本数 >= 3 实现高可用
- [ ] 配置 Pod 反亲和性以分散部署
- [ ] 设置合适的更新策略（maxUnavailable: 0 实现零停机）
- [ ] 使用 ConfigMap 和 Secret 管理配置
- [ ] 添加标准标签和注解
- [ ] 配置优雅关闭（preStop 钩子、terminationGracePeriodSeconds）
- [ ] 设置 revisionHistoryLimit 以支持回滚
- [ ] 使用最小 RBAC 权限的 ServiceAccount

### 性能调优

**快速启动：**
```yaml
spec:
  minReadySeconds: 5
  strategy:
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**零停机更新：**
```yaml
spec:
  minReadySeconds: 10
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**优雅关闭：**
```yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: app
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15 && kill -SIGTERM 1"]
```

## 故障排查

### 常见问题

**Pod 无法启动：**
```bash
kubectl describe deployment <name>
kubectl get pods -l app=<app-name>
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**ImagePullBackOff：**
- 检查镜像名称和标签
- 验证 imagePullSecrets
- 检查镜像仓库凭据

**CrashLoopBackOff：**
- 检查容器日志
- 验证存活探针是否过于激进
- 检查资源限制
- 验证应用依赖

**Deployment 卡住：**
- 检查 progressDeadlineSeconds
- 验证就绪探针
- 检查资源可用性

## 相关资源

- [Kubernetes Deployment API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#deployment-v1-apps)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
