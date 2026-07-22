# Kubernetes Manifest Generator 实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# Kubernetes Manifest Generator

逐步指导创建生产级 Kubernetes 清单文件，涵盖 Deployment、Service、ConfigMap、Secret 和 PersistentVolumeClaim。

## 目的

本技能提供全面指导，用于生成结构良好、安全且生产就绪的 Kubernetes 清单，遵循云原生最佳实践和 Kubernetes 规范。

## 何时使用此技能

在以下场景使用此技能：
- 创建新的 Kubernetes Deployment 清单
- 定义 Service 资源以实现网络连通
- 生成 ConfigMap 和 Secret 资源进行配置管理
- 为有状态工作负载创建 PersistentVolumeClaim 清单
- 遵循 Kubernetes 最佳实践与命名规范
- 实现资源限制、健康检查和安全上下文
- 设计多环境部署的清单文件

## 分步工作流

### 1. 收集需求

**了解工作负载：**
- 应用类型（无状态/有状态）
- 容器镜像及版本
- 环境变量和配置需求
- 存储需求
- 网络暴露需求（内部/外部）
- 资源需求（CPU、内存）
- 扩缩容需求
- 健康检查端点

**需要确认的问题：**
- 应用名称和用途是什么？
- 使用什么容器镜像和标签？
- 应用是否需要持久化存储？
- 应用暴露哪些端口？
- 是否需要 Secret 或配置文件？
- CPU 和内存需求是多少？
- 应用是否需要对外暴露？

### 2. 创建 Deployment 清单

**遵循以下结构：**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
    version: <version>
spec:
  replicas: 3
  selector:
    matchLabels:
      app: <app-name>
  template:
    metadata:
      labels:
        app: <app-name>
        version: <version>
    spec:
      containers:
      - name: <container-name>
        image: <image>:<tag>
        ports:
        - containerPort: <port>
          name: http
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: ENV_VAR
          value: "value"
        envFrom:
        - configMapRef:
            name: <app-name>-config
        - secretRef:
            name: <app-name>-secret
```

**应遵循的最佳实践：**
- 始终设置资源请求和限制
- 同时实现存活探针和就绪探针
- 使用明确的镜像标签（绝不使用 `:latest`）
- 为非 root 用户应用安全上下文
- 使用标签进行组织和选择
- 根据可用性需求设置合适的副本数

**参考：** 详见 `references/deployment-spec.md` 了解 Deployment 的详细选项

### 3. 创建 Service 清单

**选择合适的 Service 类型：**

**ClusterIP（仅内部访问）：**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
spec:
  type: ClusterIP
  selector:
    app: <app-name>
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
```

**LoadBalancer（外部访问）：**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app: <app-name>
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
```

**参考：** 详见 `references/service-spec.md` 了解 Service 类型和网络配置

### 4. 创建 ConfigMap

**用于应用配置：**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: <app-name>-config
  namespace: <namespace>
data:
  APP_MODE: production
  LOG_LEVEL: info
  DATABASE_HOST: db.example.com
  # For config files
  app.properties: |
    server.port=8080
    server.host=0.0.0.0
    logging.level=INFO
```

**最佳实践：**
- ConfigMap 仅用于非敏感数据
- 将相关配置组织在一起
- 为键使用有意义的名称
- 考虑每个组件使用一个 ConfigMap
- 变更时对 ConfigMap 进行版本管理

**参考：** 详见 `assets/configmap-template.yaml` 获取示例

### 5. 创建 Secret

**用于敏感数据：**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <app-name>-secret
  namespace: <namespace>
type: Opaque
stringData:
  DATABASE_PASSWORD: "changeme"
  API_KEY: "secret-api-key"
  # For certificate files
  tls.crt: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
  tls.key: |
    -----BEGIN PRIVATE KEY-----
    ...
    -----END PRIVATE KEY-----
```

**安全注意事项：**
- 绝不将明文 Secret 提交到 Git
- 使用 Sealed Secrets、External Secrets Operator 或 Vault
- 定期轮换 Secret
- 使用 RBAC 限制 Secret 访问
- 对于 TLS Secret，考虑使用 Secret 类型：`kubernetes.io/tls`

### 6. 创建 PersistentVolumeClaim（如需要）

**用于有状态应用：**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <app-name>-data
  namespace: <namespace>
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: gp3
  resources:
    requests:
      storage: 10Gi
```

**在 Deployment 中挂载：**
```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        volumeMounts:
        - name: data
          mountPath: /var/lib/app
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: <app-name>-data
```

**存储注意事项：**
- 根据性能需求选择合适的 StorageClass
- 单 Pod 访问使用 ReadWriteOnce
- 多 Pod 共享存储使用 ReadWriteMany
- 考虑备份策略
- 设置合适的保留策略

### 7. 应用安全最佳实践

**为 Deployment 添加安全上下文：**

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

**安全检查清单：**
- [ ] 以非 root 用户运行
- [ ] 丢弃所有权限
- [ ] 使用只读根文件系统
- [ ] 禁用权限提升
- [ ] 设置 seccomp 配置
- [ ] 使用 Pod Security Standards

### 8. 添加标签和注解

**标准标签（推荐）：**

```yaml
metadata:
  labels:
    app.kubernetes.io/name: <app-name>
    app.kubernetes.io/instance: <instance-name>
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: <system-name>
    app.kubernetes.io/managed-by: kubectl
```

**常用注解：**

```yaml
metadata:
  annotations:
    description: "Application description"
    contact: "team@example.com"
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

### 9. 组织多资源清单

**文件组织方式：**

**方式 1：使用 `---` 分隔符的单文件**
```yaml
# app-name.yaml
---
apiVersion: v1
kind: ConfigMap
...
---
apiVersion: v1
kind: Secret
...
---
apiVersion: apps/v1
kind: Deployment
...
---
apiVersion: v1
kind: Service
...
```

**方式 2：独立文件**
```
manifests/
├── configmap.yaml
├── secret.yaml
├── deployment.yaml
├── service.yaml
└── pvc.yaml
```

**方式 3：Kustomize 结构**
```
base/
├── kustomization.yaml
├── deployment.yaml
├── service.yaml
└── configmap.yaml
overlays/
├── dev/
│   └── kustomization.yaml
└── prod/
    └── kustomization.yaml
```

### 10. 验证与测试

**验证步骤：**

```bash
# Dry-run validation
kubectl apply -f manifest.yaml --dry-run=client

# Server-side validation
kubectl apply -f manifest.yaml --dry-run=server

# Validate with kubeval
kubeval manifest.yaml

# Validate with kube-score
kube-score score manifest.yaml

# Check with kube-linter
kube-linter lint manifest.yaml
```

**测试检查清单：**
- [ ] 清单通过 dry-run 验证
- [ ] 所有必填字段已填写
- [ ] 资源限制合理
- [ ] 健康检查已配置
- [ ] 安全上下文已设置
- [ ] 标签遵循规范
- [ ] Namespace 已存在或已创建

## 常见模式

### 模式 1：简单无状态 Web 应用

**适用场景：** 标准 Web API 或微服务

**所需组件：**
- Deployment（3 副本实现高可用）
- ClusterIP Service
- ConfigMap（配置）
- Secret（API 密钥）
- HorizontalPodAutoscaler（可选）

**参考：** 详见 `assets/deployment-template.yaml`

### 模式 2：有状态数据库应用

**适用场景：** 数据库或持久化存储应用

**所需组件：**
- StatefulSet（而非 Deployment）
- Headless Service
- PersistentVolumeClaim 模板
- ConfigMap（数据库配置）
- Secret（凭据）

### 模式 3：后台任务或定时任务

**适用场景：** 定时任务或批处理

**所需组件：**
- CronJob 或 Job
- ConfigMap（任务参数）
- Secret（凭据）
- ServiceAccount（配合 RBAC）

### 模式 4：多容器 Pod

**适用场景：** 带有 Sidecar 容器的应用

**所需组件：**
- 包含多个容器的 Deployment
- 容器间共享卷
- Init 容器（初始化）
- Service（如需要）

## 模板

以下模板位于 `assets/` 目录：

- `deployment-template.yaml` - 遵循最佳实践的标准 Deployment
- `service-template.yaml` - Service 配置（ClusterIP、LoadBalancer、NodePort）
- `configmap-template.yaml` - 不同数据类型的 ConfigMap 示例
- `secret-template.yaml` - Secret 示例（应生成而非提交）
- `pvc-template.yaml` - PersistentVolumeClaim 模板

## 参考文档

- `references/deployment-spec.md` - 详细的 Deployment 规范
- `references/service-spec.md` - Service 类型和网络详情

## 最佳实践总结

1. **始终设置资源请求和限制** - 防止资源饥饿
2. **实现健康检查** - 确保 Kubernetes 能管理你的应用
3. **使用明确的镜像标签** - 避免不可预测的部署
4. **应用安全上下文** - 以非 root 运行，丢弃权限
5. **使用 ConfigMap 和 Secret** - 将配置与代码分离
6. **为一切打标签** - 便于筛选和组织
7. **遵循命名规范** - 使用标准 Kubernetes 标签
8. **应用前先验证** - 使用 dry-run 和验证工具
9. **版本管理清单** - 存入 Git 进行版本控制
10. **用注解记录信息** - 为其他开发者添加上下文

## 故障排查

**Pod 无法启动：**
- 检查镜像拉取错误：`kubectl describe pod <pod-name>`
- 验证资源可用性：`kubectl get nodes`
- 检查事件：`kubectl get events --sort-by='.lastTimestamp'`

**Service 不可访问：**
- 验证选择器是否匹配 Pod 标签：`kubectl get endpoints <service-name>`
- 检查 Service 类型和端口配置
- 从集群内测试：`kubectl run debug --rm -it --image=busybox -- sh`

**ConfigMap/Secret 未加载：**
- 验证 Deployment 中的名称是否匹配
- 检查 Namespace
- 确认资源存在：`kubectl get configmap,secret`

## 后续步骤

创建清单后：
1. 存入 Git 仓库
2. 搭建 CI/CD 流水线进行部署
3. 考虑使用 Helm 或 Kustomize 进行模板化
4. 使用 ArgoCD 或 Flux 实现 GitOps
5. 添加监控和可观测性

## 相关技能

- `helm-chart-scaffolding` - 模板化与打包
- `gitops-workflow` - 自动化部署
- `k8s-security-policies` - 高级安全配置
