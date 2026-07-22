---
name: mtls-configuration
description: "为零信任服务间通信配置双向 TLS（mTLS）。当用户要求实现零信任网络、证书管理或保护内部服务通信时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# mTLS 配置

实现双向 TLS 以进行零信任服务网格通信的综合指南。

## 不要使用此技能的场景

- 任务与 mTLS 配置无关
- 需要此范围之外的其他领域或工具

## 指导说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如果需要详细示例，请打开 `resources/implementation-playbook.md`。

## 使用此技能的场景

- 实现零信任网络
- 保护服务间通信
- 证书轮换和管理
- 调试 TLS 握手问题
- 合规要求（PCI-DSS、HIPAA）
- 多集群安全通信

## 核心概念

### 1. mTLS 流程

```
┌─────────┐                              ┌─────────┐
│ Service │                              │ Service │
│    A    │                              │    B    │
└────┬────┘                              └────┬────┘
     │                                        │
┌────┴────┐      TLS Handshake          ┌────┴────┐
│  Proxy  │◄───────────────────────────►│  Proxy  │
│(Sidecar)│  1. ClientHello             │(Sidecar)│
│         │  2. ServerHello + Cert      │         │
│         │  3. Client Cert             │         │
│         │  4. Verify Both Certs       │         │
│         │  5. Encrypted Channel       │         │
└─────────┘                              └─────────┘
```

### 2. 证书层级

```
Root CA (Self-signed, long-lived)
    │
    ├── Intermediate CA (Cluster-level)
    │       │
    │       ├── Workload Cert (Service A)
    │       └── Workload Cert (Service B)
    │
    └── Intermediate CA (Multi-cluster)
            │
            └── Cross-cluster certs
```

## 模板

### 模板 1：Istio mTLS（严格模式）

```yaml
# Enable strict mTLS mesh-wide
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
---
# Namespace-level override (permissive for migration)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: legacy-namespace
spec:
  mtls:
    mode: PERMISSIVE
---
# Workload-specific policy
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: payment-service
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment-service
  mtls:
    mode: STRICT
  portLevelMtls:
    8080:
      mode: STRICT
    9090:
      mode: DISABLE  # Metrics port, no mTLS
```

### 模板 2：Istio mTLS 目标规则

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: default
  namespace: istio-system
spec:
  host: "*.local"
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
---
# TLS to external service
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: external-api
spec:
  host: api.external.com
  trafficPolicy:
    tls:
      mode: SIMPLE
      caCertificates: /etc/certs/external-ca.pem
---
# Mutual TLS to external service
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: partner-api
spec:
  host: api.partner.com
  trafficPolicy:
    tls:
      mode: MUTUAL
      clientCertificate: /etc/certs/client.pem
      privateKey: /etc/certs/client-key.pem
      caCertificates: /etc/certs/partner-ca.pem
```

### 模板 3：Cert-Manager 与 Istio 集成

```yaml
# Install cert-manager issuer for Istio
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: istio-ca
spec:
  ca:
    secretName: istio-ca-secret
---
# Create Istio CA secret
apiVersion: v1
kind: Secret
metadata:
  name: istio-ca-secret
  namespace: cert-manager
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-ca-cert>
  tls.key: <base64-encoded-ca-key>
---
# Certificate for workload
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-service-cert
  namespace: my-namespace
spec:
  secretName: my-service-tls
  duration: 24h
  renewBefore: 8h
  issuerRef:
    name: istio-ca
    kind: ClusterIssuer
  commonName: my-service.my-namespace.svc.cluster.local
  dnsNames:
    - my-service
    - my-service.my-namespace
    - my-service.my-namespace.svc
    - my-service.my-namespace.svc.cluster.local
  usages:
    - server auth
    - client auth
```

### 模板 4：SPIFFE/SPIRE 集成

```yaml
# SPIRE Server configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: spire-server
  namespace: spire
data:
  server.conf: |
    server {
      bind_address = "0.0.0.0"
      bind_port = "8081"
      trust_domain = "example.org"
      data_dir = "/run/spire/data"
      log_level = "INFO"
      ca_ttl = "168h"
      default_x509_svid_ttl = "1h"
    }

    plugins {
      DataStore "sql" {
        plugin_data {
          database_type = "sqlite3"
          connection_string = "/run/spire/data/datastore.sqlite3"
        }
      }

      NodeAttestor "k8s_psat" {
        plugin_data {
          clusters = {
            "demo-cluster" = {
              service_account_allow_list = ["spire:spire-agent"]
            }
          }
        }
      }

      KeyManager "memory" {
        plugin_data {}
      }

      UpstreamAuthority "disk" {
        plugin_data {
          key_file_path = "/run/spire/secrets/bootstrap.key"
          cert_file_path = "/run/spire/secrets/bootstrap.crt"
        }
      }
    }
---
# SPIRE Agent DaemonSet (abbreviated)
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: spire-agent
  namespace: spire
spec:
  selector:
    matchLabels:
      app: spire-agent
  template:
    spec:
      containers:
        - name: spire-agent
          image: ghcr.io/spiffe/spire-agent:1.8.0
          volumeMounts:
            - name: spire-agent-socket
              mountPath: /run/spire/sockets
      volumes:
        - name: spire-agent-socket
          hostPath:
            path: /run/spire/sockets
            type: DirectoryOrCreate
```

### 模板 5：Linkerd mTLS（自动模式）

```yaml
# Linkerd enables mTLS automatically
# Verify with:
# linkerd viz edges deployment -n my-namespace

# For external services without mTLS
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  name: external-api
  namespace: my-namespace
spec:
  podSelector:
    matchLabels:
      app: my-app
  port: external-api
  proxyProtocol: HTTP/1  # or TLS for passthrough
---
# Skip TLS for specific port
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    config.linkerd.io/skip-outbound-ports: "3306"  # MySQL
```

## 证书轮换

```bash
# Istio - Check certificate expiry
istioctl proxy-config secret deploy/my-app -o json | \
  jq '.dynamicActiveSecrets[0].secret.tlsCertificate.certificateChain.inlineBytes' | \
  tr -d '"' | base64 -d | openssl x509 -text -noout

# Force certificate rotation
kubectl rollout restart deployment/my-app

# Check Linkerd identity
linkerd identity -n my-namespace
```

## 调试 mTLS 问题

```bash
# Istio - Check if mTLS is enabled
istioctl authn tls-check my-service.my-namespace.svc.cluster.local

# Verify peer authentication
kubectl get peerauthentication --all-namespaces

# Check destination rules
kubectl get destinationrule --all-namespaces

# Debug TLS handshake
istioctl proxy-config log deploy/my-app --level debug
kubectl logs deploy/my-app -c istio-proxy | grep -i tls

# Linkerd - Check mTLS status
linkerd viz edges deployment -n my-namespace
linkerd viz tap deploy/my-app --to deploy/my-backend
```

## 最佳实践

### 推荐做法
- **从 PERMISSIVE 模式开始** - 逐步迁移到 STRICT 模式
- **监控证书过期** - 设置告警
- **使用短期证书** - 工作负载使用 24 小时或更短期限
- **定期轮换 CA** - 规划 CA 轮换策略
- **记录 TLS 错误** - 用于调试和审计

### 避免做法
- **不要为了便利禁用 mTLS** - 生产环境中尤其如此
- **不要忽略证书过期** - 自动化轮换
- **不要使用自签名证书** - 使用正确的 CA 层级
- **不要跳过验证** - 验证完整证书链

## 资源

- [Istio Security](https://istio.io/latest/docs/concepts/security/)
- [SPIFFE/SPIRE](https://spiffe.io/)
- [cert-manager](https://cert-manager.io/)
- [Zero Trust Architecture (NIST)](https://www.nist.gov/publications/zero-trust-architecture)

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
