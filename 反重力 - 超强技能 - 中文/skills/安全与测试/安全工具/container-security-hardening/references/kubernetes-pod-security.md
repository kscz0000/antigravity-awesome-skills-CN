# Kubernetes Pod 安全参考

在 Kubernetes 中加固工作负载的完整参考 —— 涵盖 NetworkPolicy、RBAC、Pod Security Admission、准入控制器（Kyverno/OPA）以及 Service Account 加固。

## 目录

1. [Pod Security Admission (PSA)](#pod-security-admission)
2. [NetworkPolicy —— 零信任网络](#networkpolicy--零信任网络)
3. [RBAC —— 最小权限](#rbac--最小权限)
4. [准入控制器（Kyverno / OPA Gatekeeper）](#准入控制器)
5. [Service Account 加固](#service-account-加固)
6. [运行时安全 —— Falco](#运行时安全--falco)
7. [K8s 中的 Secret 管理](#k8s-中的-secret-管理)

---

## Pod Security Admission

K8s 1.25+ 内置的策略引擎（取代了已弃用的 PodSecurityPolicy）。

### 三个内置策略级别

| 级别 | 拦截的内容 |
|---|---|
| `privileged` | 无任何限制（集群默认） |
| `baseline` | 拦截 hostNetwork、hostPID、hostIPC、特权容器、危险卷类型与 hostPath |
| `restricted` | 在 baseline 基础上额外要求非 root、只读文件系统、丢弃 capabilities、要求 seccomp |

### 每个级别的三种模式

| 模式 | 行为 |
|---|---|
| `enforce` | 拒绝违反策略的 Pod |
| `audit` | 允许运行，但在审计日志中记录违规 |
| `warn` | 允许运行，但向用户返回警告 |

### 应用 PSA 标签

```bash
# 强制执行前先审计 —— 找出可能失败的工作负载
kubectl label namespace production \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/audit-version=latest

# 渐进式上线：预发布环境用 warn，生产环境用 enforce
kubectl label namespace staging \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/warn-version=latest

kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest
```

### 强制执行前先检查可能失败的内容

```bash
# 针对命名空间进行 dry-run 检查
kubectl --dry-run=server apply -f manifests/ --namespace production

# 检查具体的 Pod 规格
kubectl run test-pod --image=nginx --dry-run=server -n production
```

### 满足 `restricted` 级别的最小 Pod 规格

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault     # 或使用自定义配置的 Localhost
  containers:
    - name: app
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
      # restricted PSA 强制要求设置资源限制
      resources:
        requests:
          memory: "64Mi"
          cpu: "50m"
        limits:
          memory: "256Mi"
          cpu: "250m"
```

---

## NetworkPolicy —— 零信任网络

默认情况下，集群中所有 Pod 之间都可以通过任意端口互通。请使用 NetworkPolicy 收紧访问控制。

> **前置条件：** 你的 CNI 插件必须支持 NetworkPolicy（Calico、Cilium、Weave Net 等 —— 但 Flannel 默认不支持）。

### 步骤 1：默认拒绝一切

为承载工作负载的每个命名空间应用默认拒绝策略：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}               # 选中该命名空间内的所有 Pod
  policyTypes:
    - Ingress
    - Egress
```

### 步骤 2：仅放行必要的流量

```yaml
# 允许来自 nginx ingress controller 的入站流量，允许到 postgres 与 DNS 的出站流量
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-myapp
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 3000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
          namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: production
      ports:
        - protocol: TCP
          port: 5432
    - to:                       # 仅允许向集群 DNS 发起 DNS 解析
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

### 允许访问外部服务（例如云 API）

```yaml
egress:
  - to:
      - ipBlock:
          cidr: 0.0.0.0/0        # 所有外部 IP
          except:
            - 10.0.0.0/8         # 但排除内部集群网段
            - 172.16.0.0/12
            - 192.168.0.0/16
    ports:
      - protocol: TCP
        port: 443                 # 仅 HTTPS
```

### 使用 Cilium 或 Calico CLI 验证 NetworkPolicy

```bash
# Cilium —— 测试 Pod 之间的连通性
cilium connectivity test

# Calico —— 列出已生效的策略
kubectl exec -it deploy/myapp -- calicoctl get networkpolicy -n production
```

---

## RBAC —— 最小权限

### 原则：缩小范围、避免通配符

```yaml
# ❌ 危险 —— 对所有对象授予所有权限
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: full-admin
subjects:
  - kind: ServiceAccount
    name: myapp-sa
    namespace: production
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io

---
# ✅ 正确 —— 限定在命名空间内的最小角色，并指定具体资源名
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["myapp-config"]    # 锁定到具体的命名资源
    verbs: ["get", "list"]             # 绝不要使用 ["*"]
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["myapp-db-creds"]
    verbs: ["get"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: myapp-rolebinding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: myapp-sa
    namespace: production
roleRef:
  kind: Role
  name: myapp-role
  apiGroup: rbac.authorization.k8s.io
```

### 审计 RBAC

```bash
# Service Account 能做什么？
kubectl auth can-i --list \
  --as=system:serviceaccount:production:myapp-sa \
  -n production

# 查找所有 cluster-admin 绑定（安全反模式）
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin") | {name:.metadata.name, subjects:.subjects}'

# 查找过度宽松的通配符权限
kubectl get roles,clusterroles -A -o json | \
  jq '.items[] | select(.rules[]?.verbs[]? == "*") | .metadata.name'

# 使用 rbac-tool 进行完整审计
kubectl rbac-tool who-can get secrets -n production
```

---

## 准入控制器

### Kyverno（以 Kubernetes 资源形式表达策略）

Kyverno 可用于校验、变更和生成资源 —— 无需掌握 Rego。

```bash
# 安装 Kyverno
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
```

**核心策略：**

```yaml
# 1. 要求容器以非 root 身份运行
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-run-as-non-root
      match:
        resources:
          kinds: [Pod]
      validate:
        message: "runAsNonRoot: true is required"
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true

---
# 2. 要求镜像使用摘要钉版
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-image-digest
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-digest
      match:
        resources:
          kinds: [Pod]
      validate:
        message: "Images must use @sha256: digest, not floating tags"
        pattern:
          spec:
            containers:
              - image: "*@sha256:*"

---
# 3. 禁止特权容器
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-privileged
      match:
        resources:
          kinds: [Pod]
      validate:
        message: "Privileged containers are not allowed"
        pattern:
          spec:
            containers:
              - =(securityContext):
                  =(privileged): "false"

---
# 4. 要求设置资源限制（避免资源争抢）
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-limits
      match:
        resources:
          kinds: [Pod]
      validate:
        message: "Resource limits (memory and cpu) must be set"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"

---
# 5. 自动变更：若未设置则自动添加 drop ALL capabilities
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: drop-all-capabilities
spec:
  rules:
    - name: add-drop-all
      match:
        resources:
          kinds: [Pod]
      mutate:
        patchStrategicMerge:
          spec:
            containers:
              - (name): "*"
                securityContext:
                  capabilities:
                    drop: ["ALL"]
```

### OPA Gatekeeper（以 Rego 表达策略）

```bash
# 安装 Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.17/deploy/gatekeeper.yaml
```

```yaml
# ConstraintTemplate —— 定义 Rego 策略
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }

---
# Constraint —— 应用该策略
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-app-label
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["app", "version", "owner"]
```

---

## Service Account 加固

```yaml
# 为每个工作负载创建专用 Service Account（切勿使用 'default'）
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
  annotations:
    # EKS —— IAM Roles for Service Accounts（IRSA）
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/myapp-role
    # GKE —— Workload Identity
    iam.gke.io/gcp-service-account: myapp@my-project.iam.gserviceaccount.com
automountServiceAccountToken: false    # 除非应用需要调用 K8s API，否则禁用

---
# 在 Pod 规格中 —— 同时禁用 token 自动挂载
spec:
  serviceAccountName: myapp-sa
  automountServiceAccountToken: false
```

**为何在云凭证场景下应使用 Workload Identity 而非 K8s Secret？**
- 凭证短时有效（1 小时）且自动轮换
- 无需担心 Secret 泄露、轮换或存储问题
- 审计轨迹与工作负载身份绑定，而非共用密钥

---

## 运行时安全 —— Falco

Falco 用于检测运行时的异常行为（意外的 syscall、网络连接、文件读取）。

```bash
# 通过 Helm 安装
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set falco.grpc.enabled=true \
  --set falco.grpcOutput.enabled=true
```

**规则示例：**

```yaml
# 检测容器内启动的 shell
- rule: Terminal shell in container
  desc: A shell was spawned in a container with an attached terminal
  condition: >
    spawned_process and container
    and shell_procs and proc.tty != 0
    and container_entrypoint
  output: >
    Shell spawned in a container (user=%user.name container=%container.name
    shell=%proc.name parent=%proc.pname)
  priority: WARNING

# 检测敏感文件被读取
- rule: Read sensitive file untrusted
  desc: An attempt to read a sensitive file by a non-trusted program
  condition: >
    open_read and sensitive_files
    and not proc.name in (trusted_programs)
  output: >
    Sensitive file opened for reading (file=%fd.name user=%user.name
    container=%container.name)
  priority: WARNING
```

---

## K8s 中的 Secret 管理

**Kubernetes Secret 默认只是 base64 编码，并未加密。** 请选用以下方案之一：

| 方案 | 机制 | 适用场景 |
|---|---|---|
| **External Secrets Operator** | 从 AWS Secrets Manager / GCP Secret Manager / Vault 同步 | 生产环境 —— Secret 永远不会落入 etcd |
| **Sealed Secrets（Bitnami）** | 在 Git 中对 Secret 进行非对称加密 | GitOps 工作流 |
| **HashiCorp Vault** | 动态 Secret、PKI、租约管理 | 复杂的多云环境 |
| **SOPS + Age/GPG** | 在 Git 中存放加密的 Secret 文件 | 小型团队、简单流程 |

```yaml
# External Secrets Operator —— 从 AWS Secrets Manager 同步
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-db-creds
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: myapp-db-creds
    creationPolicy: Owner
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: production/myapp/db
        property: password
```

```bash
# 启用 etcd 静态加密（K8s）
# 在 kube-apiserver 中：--encryption-provider-config=encryption-config.yaml
# encryption-config.yaml：
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources: [secrets]
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-key>
      - identity: {}
```