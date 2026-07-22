# RBAC 模式与最佳实践

## 常见 RBAC 模式

### 模式 1：只读访问
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-only
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
```

### 模式 2：命名空间管理员
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: namespace-admin
  namespace: production
rules:
- apiGroups: ["", "apps", "batch", "extensions"]
  resources: ["*"]
  verbs: ["*"]
```

### 模式 3：Deployment 管理员
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

### 模式 4：Secret 读取（ServiceAccount）
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["app-secrets"]  # 仅限特定 Secret
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-secret-reader
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: production
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### 模式 5：CI/CD 流水线访问
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cicd-deployer
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["services", "configmaps"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

## ServiceAccount 最佳实践

### 创建专用 ServiceAccount
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: production
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      serviceAccountName: my-app
      automountServiceAccountToken: false  # 不需要时禁用
```

### 最小权限 ServiceAccount
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get"]
  resourceNames: ["my-app-config"]
```

## 安全最佳实践

1. 尽可能**使用 Role 而非 ClusterRole**
2. 通过 **resourceNames** 实现细粒度访问控制
3. 生产环境中**避免通配符权限**（`*`）
4. 为每个应用**创建专用 ServiceAccount**
5. 不需要时**禁用 Token 自动挂载**
6. **定期审计 RBAC**，移除未使用的权限
7. **使用组**管理用户
8. **实施命名空间隔离**
9. 通过审计日志**监控 RBAC 使用情况**
10. 在元数据中**记录 Role 用途**

## RBAC 故障排查

### 检查用户权限
```bash
kubectl auth can-i list pods --as john@example.com
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-app
```

### 查看有效权限
```bash
kubectl describe clusterrole cluster-admin
kubectl describe rolebinding -n production
```

### 调试访问问题
```bash
kubectl get rolebindings,clusterrolebindings --all-namespaces -o wide | grep my-user
```

## 常见 RBAC 动词

- `get` - 读取特定资源
- `list` - 列出某类型的所有资源
- `watch` - 监听资源变更
- `create` - 创建新资源
- `update` - 更新现有资源
- `patch` - 部分更新资源
- `delete` - 删除资源
- `deletecollection` - 批量删除资源
- `*` - 所有动词（生产环境中避免使用）

## 资源作用域

### 集群范围资源
- Nodes
- PersistentVolumes
- ClusterRoles
- ClusterRoleBindings
- Namespaces

### 命名空间范围资源
- Pods
- Services
- Deployments
- ConfigMaps
- Secrets
- Roles
- RoleBindings
