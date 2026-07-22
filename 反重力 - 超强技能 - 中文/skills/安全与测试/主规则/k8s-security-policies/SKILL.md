---
name: k8s-security-policies
description: "Kubernetes 中 NetworkPolicy、PodSecurityPolicy、RBAC 及 Pod Security Standards 的全面实施指南。触发词：K8s安全策略、NetworkPolicy、Pod安全标准、RBAC配置、网络策略、准入控制、集群安全"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Kubernetes 安全策略

Kubernetes 中 NetworkPolicy、PodSecurityPolicy、RBAC 及 Pod Security Standards 的全面实施指南。

## 以下情况不要使用此技能

- 任务与 Kubernetes 安全策略无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 目的

使用网络策略、Pod 安全标准和 RBAC，为 Kubernetes 集群实施纵深防御安全体系。

## 以下情况使用此技能

- 实施网络分段
- 配置 Pod 安全标准
- 设置最小权限 RBAC 访问控制
- 为合规要求创建安全策略
- 实施准入控制
- 保护多租户集群安全

## Pod 安全标准

### 1. Privileged（无限制）
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: privileged-ns
  labels:
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/audit: privileged
    pod-security.kubernetes.io/warn: privileged
```

### 2. Baseline（最小限制）
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: baseline-ns
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/warn: baseline
```

### 3. Restricted（最严格）
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: restricted-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## 网络策略

### 默认拒绝所有流量
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### 允许前端访问后端
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
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

### 允许 DNS 查询
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

**参考：** 参见 `assets/network-policy-template.yaml`

## RBAC 配置

### Role（命名空间范围）
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### ClusterRole（集群范围）
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

### RoleBinding
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: default
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**参考：** 参见 `references/rbac-patterns.md`

## Pod 安全上下文

### 受限 Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

## 使用 OPA Gatekeeper 实施策略

### ConstraintTemplate
```yaml
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
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("missing required labels: %v", [missing])
        }
```

### Constraint
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-app-label
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["app", "environment"]
```

## 服务网格安全（Istio）

### PeerAuthentication（mTLS）
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

### AuthorizationPolicy
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
```

## 最佳实践

1. 在命名空间级别**实施 Pod 安全标准**
2. 使用 NetworkPolicy 实现**网络分段**
3. 为所有 ServiceAccount **应用最小权限 RBAC**
4. **启用准入控制**（OPA Gatekeeper/Kyverno）
5. **以非 root 用户运行容器**
6. **使用只读根文件系统**
7. 除非必要，**丢弃所有 capabilities**
8. **实施资源配额**和限制范围
9. 为安全事件**启用审计日志**
10. **定期扫描**镜像安全漏洞

## 合规框架

### CIS Kubernetes Benchmark
- 使用 RBAC 授权
- 启用审计日志
- 使用 Pod 安全标准
- 配置网络策略
- 实施静态加密 Secret
- 启用节点认证

### NIST 网络安全框架
- 实施纵深防御
- 使用网络分段
- 配置安全监控
- 实施访问控制
- 启用日志和监控

## 故障排查

**NetworkPolicy 不生效：**
```bash
# 检查 CNI 是否支持 NetworkPolicy
kubectl get nodes -o wide
kubectl describe networkpolicy <name>
```

**RBAC 权限被拒绝：**
```bash
# 检查有效权限
kubectl auth can-i list pods --as system:serviceaccount:default:my-sa
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-sa
```

## 参考文件

- `assets/network-policy-template.yaml` - 网络策略示例
- `assets/pod-security-template.yaml` - Pod 安全策略
- `references/rbac-patterns.md` - RBAC 配置模式

## 相关技能

- `k8s-manifest-generator` - 用于创建安全清单
- `gitops-workflow` - 用于自动化策略部署

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代针对具体环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
