---
name: container-security-hardening
description: >
  使用安全的基础镜像、非 root 用户、CVE 扫描、SBOM/签名、seccomp/AppArmor 以及
  Kubernetes Pod 安全控制来加固 Docker/容器镜像与运行时部署。用于 Dockerfile 安全审查、
  容器 CVE、镜像扫描、distroless 镜像或生产环境加固。
  触发词：Docker 安全、容器安全加固、Dockerfile 安全审查、容器漏洞、镜像扫描、非 root 用户、
  最小攻击面、Cosign 签名、SBOM、seccomp、AppArmor、Pod 安全加固、容器 CVE 修复。
category: security
risk: safe
source: community
date_added: "2026-05-30"
---

# 容器安全加固技能

一份面向生产环境的指南，介绍如何安全地构建、扫描和运行容器 —— 从 Dockerfile 编写到运行时强制执行以及供应链完整性。

---

## 何时使用本技能

- 用户提及 Docker 安全、容器加固或 Dockerfile 安全审查
- 用户询问 distroless 镜像、非 root 容器或只读文件系统
- 用户希望使用 Trivy、Grype 或 Snyk 扫描镜像中的 CVE
- 用户提及 seccomp、AppArmor、Linux capabilities 或运行时安全
- 用户询问「我的 Dockerfile 是否安全？」或「如何减小镜像的攻击面？」
- 用户希望使用 Cosign 对镜像进行签名/校验或生成 SBOM
- 用户询问 Kubernetes Pod 安全、NetworkPolicy 或 RBAC 加固
- 用户表示「修复容器 CVE」或「为生产环境加固我的容器」

## 何时不使用本技能

- 用户主要询问 GitHub Actions CI/CD → 推荐 `github-actions-advanced`
- 用户需要常规的 Docker 使用帮助（非安全相关） → 推荐 `docker-expert`
- 用户正在处理安全以外的 Kubernetes 编排 → 推荐 `kubernetes-architect`
- 用户需要应用层安全（SQL 注入、XSS） → 推荐 `api-security-best-practices`

---

## 步骤 1：先理解上下文再回答

被调用时，首先检测当前状态：

```bash
# 查找项目中的 Dockerfile
find . -name "Dockerfile*" -not -path "*/node_modules/*" | head -10

# 检查现有安全工具
ls .trivyignore .hadolint.yaml .snyk docker-compose*.yml 2>/dev/null

# 检查当前正在使用的基础镜像
grep -r "^FROM" $(find . -name "Dockerfile*") 2>/dev/null

# 检查是否存在 Kubernetes 清单
find . -name "*.yaml" -path "*/k8s/*" -o -name "*.yaml" -path "*/manifests/*" | head -10
```

然后根据以下因素调整建议：
- 技术栈（Node、Python、Go、Java —— 影响基础镜像选择）
- 是仅 Docker 部署还是部署到 Kubernetes
- 使用的 CI 平台（用于集成扫描器）
- 现有基础镜像与最佳实践之间的差距

---

## 容器安全的五个层级

```
1. 镜像构建         → 最小基础镜像、无密钥、非 root、只读文件系统
2. 镜像扫描         → CVE 扫描、SBOM、密钥检测、Dockerfile lint
3. 运行时安全       → capabilities、seccomp、AppArmor、资源限制
4. 供应链           → 已签名镜像、固定 digest、可信镜像仓库
5. Kubernetes 层    → Pod Security Admission、NetworkPolicy、RBAC、Kyverno
```

> 按顺序逐层处理 —— 先加固镜像能获得最大的杠杆效应。
> 完整的体积/CVE 权衡表请参阅 `references/base-image-comparison.md`。

---

## 第 1 层：Dockerfile 加固

### 1.1 使用最小基础镜像

```dockerfile
# ❌ 避免使用 —— 攻击面巨大（典型 100–200 个 CVE）
FROM ubuntu:latest
FROM node:20

# ✅ 更好的选择 —— slim 变体（glibc，更小的 apt 占用）
FROM node:20-slim
FROM python:3.12-slim

# ✅ 最佳 —— distroless（无 shell、无包管理器、内置 nonroot 用户）
FROM gcr.io/distroless/nodejs20-debian12
FROM gcr.io/distroless/python3-debian12
FROM gcr.io/distroless/static-debian12   # Go/Rust 完全静态二进制

# ✅ 同样优秀 —— Alpine（musl libc；请先验证应用兼容性）
FROM alpine:3.20

# ✅ 零攻击面 —— 仅用于完全静态的二进制
FROM scratch
```

完整的权衡矩阵请参阅 `references/base-image-comparison.md`。

### 1.2 多阶段构建 —— 将构建与运行时分离

切勿在生产镜像中携带构建工具、编译器或开发依赖。

```dockerfile
# syntax=docker/dockerfile:1

# ── 阶段 1：安装与构建 ──────────────────────────────
FROM node:20-slim AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci                          # 安装所有依赖（包括 devDeps）
COPY . .
RUN npm run build && npm prune --production

# ── 阶段 2：运行时 —— 最小化，无构建工具 ────────────
FROM gcr.io/distroless/nodejs20-debian12@sha256:<digest>
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.revision="${BUILD_SHA}"
LABEL org.opencontainers.image.licenses="MIT"
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /build/dist        ./dist
COPY --from=builder --chown=nonroot:nonroot /build/node_modules ./node_modules
USER nonroot:nonroot                # UID 65532 —— distroless 内置
EXPOSE 3000
CMD ["dist/server.js"]
```

**Go / Rust 静态二进制模式：**
```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /build
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o app .

FROM scratch                        # 零攻击面
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /build/app /app
USER 65532:65532
ENTRYPOINT ["/app"]
```

### 1.3 以非 root 用户运行

```dockerfile
# 对于基于 debian/ubuntu 的镜像 —— 创建专用用户
RUN groupadd -r appgroup --gid 10001 && \
    useradd -r -g appgroup --uid 10001 --no-log-init appuser

COPY --chown=appuser:appgroup . /app

USER appuser    # 在 CMD/ENTRYPOINT 之前切换 —— 切勿以 root 运行

# ─────────────────────────────────────────────────────────
# 对于基于 Alpine 的镜像
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

# 对于 distroless —— 已内置 nonroot（UID 65532）
USER nonroot:nonroot
```

### 1.4 将基础镜像固定到 Digest

```dockerfile
# ❌ 不安全 —— tag 是可变的；镜像可能被静默覆盖（供应链攻击）
FROM node:20-slim

# ✅ 安全 —— SHA256 digest 在密码学上不可变
FROM node:20-slim@sha256:a1b2c3d4e5f6789abcdef0123456789abcdef0123456789abcdef0123456789ab
```

**获取当前 digest：**
```bash
docker pull node:20-slim
docker inspect node:20-slim --format='{{index .RepoDigests 0}}'
```

**使用 Renovate 或 Dependabot 自动化 digest 固定：**
```json
// .renovaterc.json
{
  "extends": ["config:base"],
  "dockerfile": { "enabled": true },
  "pinDigests": true
}
```

### 1.5 切勿将密钥烘焙到镜像中

```dockerfile
# ❌ 切勿 —— 在 ENV 或 RUN 中使用密钥；在 `docker history` 和层缓存中可见
ENV AWS_SECRET_ACCESS_KEY=supersecret
RUN curl -H "Authorization: Bearer $TOKEN" https://api.example.com > config.json
ARG API_KEY                         # 同样不安全 —— 在构建参数历史中可见

# ✅ 正确 —— BuildKit secret 挂载（永远不会持久化到任何层）
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=api_token \
    curl -H "Authorization: Bearer $(cat /run/secrets/api_token)" \
    https://api.example.com/config > config.json
```

构建命令：`docker build --secret id=api_token,src=./token.txt .`

**检查镜像中是否泄露了密钥：**
```bash
docker history --no-trunc myapp:latest | grep -iE "secret|key|password|token"
trivy image --scanners secret myapp:latest
```

### 1.6 只读文件系统与禁止提权

```dockerfile
# 在 Dockerfile 中 —— 使用 exec 形式（无 shell 解析）
ENTRYPOINT ["node", "server.js"]    # ✅ exec 形式
# ENTRYPOINT /bin/sh -c "node..."  # ❌ shell 形式 —— 会产生额外进程

# 定义 HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["node", "-e", "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"]
```

在运行时强制只读（请参阅第 3 层）。

### 1.7 最小化的 .dockerignore

```dockerignore
# 始终将这些排除在构建上下文之外
.git
.github
.env
.env.*
*.pem
*.key
node_modules
__pycache__
.pytest_cache
coverage/
dist/
*.log
.DS_Store
Dockerfile*
docker-compose*
README.md
docs/
tests/
```

### 1.8 完整的加固 Dockerfile 示例

```dockerfile
# syntax=docker/dockerfile:1

# ── 构建阶段 ───────────────────────────────────────────
FROM node:20-slim AS builder
WORKDIR /build
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN npm run build && npm prune --production

# ── 运行时阶段 ─────────────────────────────────────────
FROM gcr.io/distroless/nodejs20-debian12@sha256:<pin-digest-here>

LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.revision="${BUILD_SHA}"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /build/dist        ./dist
COPY --from=builder --chown=nonroot:nonroot /build/node_modules ./node_modules

USER nonroot:nonroot
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["node", "-e", "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode===200?0:1))"]

CMD ["dist/server.js"]
```

---

## 第 2 层：镜像扫描

### 2.1 Trivy（推荐 —— 快速、全面）

```bash
# 安装
brew install trivy                              # macOS
apt install trivy                               # Debian/Ubuntu
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
  -o "$tmpdir/trivy-install.sh"
sed -n '1,160p' "$tmpdir/trivy-install.sh"
sh "$tmpdir/trivy-install.sh"

# 扫描镜像中的 CVE
trivy image myapp:latest

# 在 HIGH/CRITICAL 严重级别时使 CI 失败
trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest

# 扫描 Dockerfile 中的错误配置
trivy config ./Dockerfile

# 扫描整个仓库（漏洞 + 密钥 + 错误配置）
trivy fs --scanners vuln,secret,misconfig .

# 生成 SBOM（CycloneDX 或 SPDX）
trivy image --format cyclonedx --output sbom.json myapp:latest
trivy image --format spdx-json  --output sbom.spdx.json myapp:latest

# 忽略特定 CVE（添加说明注释）
trivy image --ignorefile .trivyignore myapp:latest
```

**.trivyignore 示例：**
```
# CVE-2023-1234 —— 仅通过 X 功能可利用，本应用未使用该功能
CVE-2023-1234

# CVE-2023-5678 —— 修复尚不可用；已在 issue #42 中跟踪
CVE-2023-5678
```

### 2.2 Grype（Anchore 替代方案）

```bash
# 安装
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh \
  -o "$tmpdir/grype-install.sh"
sed -n '1,160p' "$tmpdir/grype-install.sh"
sh "$tmpdir/grype-install.sh"

# 扫描镜像
grype myapp:latest

# 在 critical 级别时失败
grype myapp:latest --fail-on critical

# 输出 SARIF 供 GitHub Security 选项卡使用
grype myapp:latest -o sarif > results.sarif

# 与 Syft 配合生成 SBOM
syft myapp:latest -o cyclonedx-json > sbom.json
grype sbom:sbom.json                            # 直接扫描 SBOM
```

### 2.3 Hadolint —— Dockerfile Lint

```bash
# 直接运行
docker run --rm -i hadolint/hadolint < Dockerfile

# 使用配置文件
hadolint --config .hadolint.yaml --failure-threshold warning Dockerfile
```

**.hadolint.yaml：**
```yaml
failure-threshold: warning
ignore:
  - DL3008   # 在 apt-get 中固定版本（基础层允许浮动）
trustedRegistries:
  - gcr.io
  - ghcr.io
  - public.ecr.aws
```

### 2.4 镜像中的密钥扫描

```bash
# Trivy 也覆盖密钥扫描
trivy image --scanners secret myapp:latest

# 专业工具：TruffleHog
trufflehog docker --image myapp:latest

# 使用 git-secrets 防止提交密钥
git secrets --scan
```

### 2.5 CI 集成（GitHub Actions —— SHA 固定）

```yaml
permissions:
  contents: read
  security-events: write      # 上传 SARIF 所必需

jobs:
  security-scan:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - name: 构建镜像
        run: docker build -t myapp:${{ github.sha }} .

      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@54c9adbab1582c2ef04b2016b760714a4bfde3cf  # v3.1.0
        with:
          dockerfile: Dockerfile
          failure-threshold: warning

      - name: 使用 Trivy 扫描
        uses: aquasecurity/trivy-action@6e7b7d1fd3e4fef0c5fa8cce1229c54b2c9bd0d8  # v0.28.0
        with:
          image-ref: myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: HIGH,CRITICAL
          exit-code: '1'

      - name: 将结果上传到 GitHub Security 选项卡
        uses: github/codeql-action/upload-sarif@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1
        if: always()          # 即使扫描发现问题也上传
        with:
          sarif_file: trivy-results.sarif
```

---

## 第 3 层：运行时安全

### 3.1 docker run 加固标志

```bash
docker run \
  --read-only \                              # 只读根文件系统
  --tmpfs /tmp:noexec,nosuid,size=100m \     # 仅 /tmp 启用可写 tmpfs
  --tmpfs /var/run \                         # 如需存放 PID 文件
  --user 10001:10001 \                       # 非 root UID:GID
  --cap-drop ALL \                           # 移除所有 Linux capabilities
  --cap-add NET_BIND_SERVICE \               # 仅添加确实需要的
  --security-opt no-new-privileges:true \    # 通过 setuid 阻止提权
  --security-opt seccomp=seccomp.json \      # 自定义 seccomp 配置
  --security-opt apparmor=docker-default \   # AppArmor 配置
  --pids-limit 100 \                         # 防止 fork 炸弹
  --memory 512m \                            # OOM 保护
  --memory-swap 512m \                       # 禁用 swap
  --cpus 1.0 \                               # CPU 限制
  --network none \                           # 无网络（如不需要）
  --health-cmd "curl -f http://localhost:3000/health || exit 1" \
  --health-interval 30s \
  myapp:latest
```

### 3.2 Linux Capabilities —— 移除与保留

移除所有 capabilities，然后仅显式添加应用所需的能力：

| Capability | 用途 | 是否保留 |
|---|---|---|
| `NET_BIND_SERVICE` | 绑定 < 1024 的端口 | 仅当需要绑定特权端口时 |
| `CHOWN` | 更改文件所有权 | 否 —— 在构建时设置所有权 |
| `SETUID` / `SETGID` | 切换用户身份 | 否 —— 始终移除 |
| `SYS_ADMIN` | 广泛的特权操作 | 否 —— 最危险的 capability |
| `NET_ADMIN` | 配置网络接口 | 否（仅限网络工具） |
| `SYS_PTRACE` | 调试/跟踪进程 | 否（仅限调试器容器） |
| `DAC_OVERRIDE` | 覆盖文件权限 | 否 —— 以正确用户身份运行 |
| `NET_RAW` | 原始套接字（ping） | 否（默认 seccomp 已阻止） |

> **大多数 Web 应用不需要任何 capability。** 仅使用 `--cap-drop ALL` 通常就足够了。

### 3.3 Docker Compose 加固

```yaml
services:
  app:
    image: myapp:latest
    read_only: true
    user: "10001:10001"
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
      - /var/run:noexec,nosuid,size=10m
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE    # 仅当绑定 < 1024 端口时
    security_opt:
      - no-new-privileges:true
      - seccomp:./references/seccomp-profile-template.json
    pids_limit: 100
    mem_limit: 512m
    memswap_limit: 512m
    cpus: 1.0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    networks:
      - backend
    # 仅在确实需要时才对外暴露
    # ports: ["8080:8080"]
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

networks:
  backend:
    driver: bridge
    internal: true    # 无需时无外部连通性
```

### 3.4 Seccomp 配置

Docker 默认的 seccomp 配置阻止约 44 个危险的系统调用。若需更严格的控制：

```bash
# 步骤 1：审计应用实际使用的系统调用
docker run --security-opt seccomp=unconfined \
  --name audit-run myapp:latest &

# 使用 strace 捕获
strace -c -p $(docker inspect --format '{{.State.Pid}}' audit-run)

# 或使用 sysdig（对容器更友好）
sysdig -p "%syscall.type" container.name=audit-run | sort -u

# 步骤 2：基于 references/seccomp-profile-template.json 构建自定义配置
# 步骤 3：应用它
docker run --security-opt seccomp=references/seccomp-profile-template.json myapp:latest
```

针对典型 Web 服务器的最小起始白名单请参阅 `references/seccomp-profile-template.json`。

### 3.5 AppArmor 配置（Linux 主机）

```bash
# 加载 Docker 默认的 AppArmor 配置
sudo apparmor_parser -r /etc/apparmor.d/docker-default

# 在运行时应用
docker run --security-opt apparmor=docker-default myapp:latest

# 生成自定义配置
aa-genprof myapp   # 交互式 —— 先在 aa-complain 模式下运行应用
```

---

## 第 4 层：供应链安全

### 4.1 使用 Cosign 对镜像进行签名（Sigstore —— 无密钥）

```bash
# 安装 cosign
brew install cosign    # macOS
# 或：https://github.com/sigstore/cosign/releases

# 推送后签名 —— 通过 OIDC 无密钥（无需长期密钥）
cosign sign ghcr.io/org/myapp:latest

# 部署前校验
cosign verify ghcr.io/org/myapp:latest \
  --certificate-identity-regexp="https://github.com/org/repo" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com"
```

**GitHub Actions —— 签名与校验流水线：**
```yaml
permissions:
  id-token: write     # OIDC 无密钥签名所必需
  packages: write

steps:
  - uses: sigstore/cosign-installer@dc72c7d5c4d10cd6bcb8cf6e3fd625a9e5e537da  # v3.7.0

  - name: 签名镜像（通过 OIDC 无密钥）
    run: |
      cosign sign --yes \
        ghcr.io/${{ github.repository }}:${{ github.sha }}
    env:
      COSIGN_EXPERIMENTAL: "true"

  - name: 附加 SBOM 证明
    run: |
      cosign attest --yes \
        --predicate sbom.json \
        --type cyclonedx \
        ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### 4.2 SBOM 生成与证明

```bash
# 使用 Syft 生成 SBOM
syft myapp:latest -o cyclonedx-json > sbom.json
syft myapp:latest -o spdx-json > sbom.spdx.json

# 作为证明附加到镜像
cosign attest --predicate sbom.json --type cyclonedx ghcr.io/org/myapp:latest

# 部署前校验 SBOM 证明
cosign verify-attestation \
  --type cyclonedx \
  --certificate-identity-regexp="https://github.com/org/repo" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  ghcr.io/org/myapp:latest
```

### 4.3 使用可信镜像仓库并启用仓库扫描

| 镜像仓库 | 内置扫描 | 说明 |
|---|---|---|
| GHCR (GitHub Container Registry) | 否（在 CI 中使用 Trivy） | 适合开源、OIDC 认证 |
| AWS ECR | 是（通过 Inspector 增强扫描） | 按仓库启用 |
| GCP Artifact Registry | 是（Container Analysis） | 默认启用 |
| Azure ACR | 是（Defender for Containers） | 高级层级 |
| Docker Hub | 是（免费层有限制） | 避免用于私有镜像 |

```bash
# 启用 ECR 增强扫描
aws ecr put-registry-scanning-configuration \
  --scan-type ENHANCED \
  --rules '[{"repositoryFilters":[{"filter":"*","filterType":"WILDCARD"}],"scanFrequency":"CONTINUOUS_SCAN"}]'
```

### 4.4 准入控制 —— 阻止未签名/未扫描的镜像

```yaml
# Kyverno 策略 —— 在准入前要求镜像签名
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-image-signature
      match:
        resources:
          kinds: [Pod]
      verifyImages:
        - imageReferences:
            - "ghcr.io/org/*"
          attestors:
            - entries:
                - keyless:
                    subject: "https://github.com/org/repo/.github/workflows/*"
                    issuer: "https://token.actions.githubusercontent.com"
```

---

## 第 5 层：Kubernetes Pod 安全

> 完整参考：`references/kubernetes-pod-security.md`

### 5.1 Pod 安全上下文

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  template:
    spec:
      # ── Pod 级安全上下文 ─────────────────────
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
        fsGroupChangePolicy: OnRootMismatch
        seccompProfile:
          type: RuntimeDefault    # 使用 containerd/runc 默认 seccomp
        supplementalGroups: []

      automountServiceAccountToken: false   # 除非需要，否则禁用

      # ── 容器级安全上下文 ──────────────
      containers:
        - name: app
          image: ghcr.io/org/myapp@sha256:<digest>   # 始终使用 digest
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
              add: []              # 除非绝对必要，否则不添加任何东西
            runAsNonRoot: true
            runAsUser: 10001
            seccompProfile:
              type: RuntimeDefault

          # ── 资源限制（restricted PSA 必需） ──
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"

          # ── 可写 tmpfs 挂载 ──────────────────────
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: varrun
              mountPath: /var/run

      volumes:
        - name: tmp
          emptyDir:
            medium: Memory
            sizeLimit: 100Mi
        - name: varrun
          emptyDir:
            medium: Memory
            sizeLimit: 10Mi
```

### 5.2 Pod Security Admission（K8s 1.25+）

```bash
# 在强制执行前审计现有工作负载
kubectl label namespace production \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/audit-version=latest

# 在 staging 中告警，在 production 中强制
kubectl label namespace staging \
  pod-security.kubernetes.io/warn=restricted

kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest
```

| PSA 级别 | 阻止的内容 |
|---|---|
| `privileged` | 无限制 |
| `baseline` | 阻止 hostNetwork、hostPID、特权容器、hostPath |
| `restricted` | 还要求非 root、只读文件系统、移除 capabilities、seccomp |

### 5.3 NetworkPolicy —— 零信任网络

```yaml
# 步骤 1：在命名空间中默认拒绝所有入站和出站流量
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]

---
# 步骤 2：仅选择性地允许所需流量
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes: [Ingress, Egress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - port: 3000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
    - to:                 # 仅允许集群 DNS
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
```

### 5.4 RBAC —— 最小权限

```yaml
# 创建最小角色 —— 切勿使用通配符
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    resourceNames: ["myapp-config"]    # 锁定到特定资源名称
    verbs: ["get"]                     # 切勿使用 ["*"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-reader-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: myapp-sa
    namespace: production
roleRef:
  kind: Role
  name: app-reader
  apiGroup: rbac.authorization.k8s.io
```

```bash
# 审计 ServiceAccount 拥有的权限
kubectl auth can-i --list --as=system:serviceaccount:production:myapp-sa

# 查找过度宽松的集群角色
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name == "cluster-admin") | .subjects'
```

### 5.5 Kyverno 策略示例

```yaml
# 要求容器以非 root 运行
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
        message: "容器不得以 root 运行（必须设置 runAsNonRoot: true）"
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true

---
# 要求固定镜像 digest
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
        message: "镜像必须固定到 SHA256 digest，而不仅仅是 tag"
        pattern:
          spec:
            containers:
              - image: "*@sha256:*"

---
# 阻止特权容器
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
        message: "不允许特权容器"
        pattern:
          spec:
            containers:
              - =(securityContext):
                  =(privileged): "false"
```

---

## 常见陷阱与修复

| 问题 | 根本原因 | 修复 |
|---|---|---|
| 镜像以 root 运行 | 没有 `USER` 指令 | 添加 `RUN useradd ...` 和 `USER appuser` |
| 密钥出现在 `docker history` 中 | `ENV` 或 `RUN curl -H "Bearer $TOKEN"` | 使用 `RUN --mount=type=secret` |
| 镜像体积大且包含大量 CVE | 完整基础镜像（`node:20`、`ubuntu`） | 切换到 `node:20-slim` 或 `distroless` |
| 应用在 `--read-only` 下崩溃 | 向 `/tmp` 或应用目录写入 | 添加 `--tmpfs /tmp` 以提供可写临时空间 |
| Trivy 扫描因无法修复的 CVE 阻塞 CI | 没有忽略文件 | 添加 `.trivyignore` 并附上合理说明 |
| 容器需要 `SYS_ADMIN` | 缺少 `--cap-drop` 的语境 | 调查原因 —— 几乎总是可以避免的 |
| 基于 tag 的镜像随时间漂移 | 可变 tag | 固定到 `@sha256:` digest；使用 Renovate 自动更新 |
| K8s Pod 被 PSA 拒绝 | 缺少安全上下文字段 | 添加 `runAsNonRoot`、`readOnlyRootFilesystem`、`allowPrivilegeEscalation: false` |
| 应用无法写入文件系统 | `readOnlyRootFilesystem: true` | 为可写路径挂载 `emptyDir` 卷 |

---

## 安全清单

### Dockerfile
- [ ] 最小基础镜像（distroless、slim 或 alpine —— 而非完整 debian/ubuntu）
- [ ] 多阶段构建 —— 运行时镜像中不包含构建工具、devDependencies 或编译器
- [ ] 在 `CMD`/`ENTRYPOINT` 之前声明非 root `USER`
- [ ] 基础镜像固定到 `@sha256:...` digest（不仅仅是 tag）
- [ ] 在 `ENV`、`ARG` 或 `RUN` 命令中没有密钥
- [ ] 定义了 `HEALTHCHECK`
- [ ] 包含 OCI 标签（`org.opencontainers.image.*`）
- [ ] `.dockerignore` 排除 `.git`、`.env`、密钥、测试
- [ ] `ENTRYPOINT` 使用 exec 形式而非 shell 形式

### 镜像扫描
- [ ] CI 中使用 Trivy 或 Grype 扫描（在 HIGH/CRITICAL 时失败）
- [ ] Hadolint 无警告通过
- [ ] 对镜像运行密钥扫描（`trivy --scanners secret`）
- [ ] 已生成并存储 SBOM
- [ ] `.trivyignore` 中包含已接受 CVE 的合理说明条目

### 运行时
- [ ] `--read-only` 文件系统
- [ ] `--cap-drop ALL`（仅在文档明确要求时才添加回来）
- [ ] `--security-opt no-new-privileges:true`
- [ ] 应用 `--security-opt seccomp=<profile>`
- [ ] 设置资源限制（`--memory`、`--cpus`、`--pids-limit`）
- [ ] 使用 Cosign 对镜像签名；部署前校验

### Kubernetes
- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: false`
- [ ] `runAsNonRoot: true` 并显式指定 UID
- [ ] `capabilities.drop: ["ALL"]`
- [ ] 定义资源 `requests` 和 `limits`
- [ ] `automountServiceAccountToken: false`
- [ ] 命名空间 PSA 在 `restricted` 级别强制执行
- [ ] 应用 `NetworkPolicy` 默认拒绝
- [ ] RBAC 使用特定资源名称和最小 verbs

---

## 参考文件

- `references/base-image-comparison.md` —— 体积、CVE 数量、shell/包管理器权衡：distroless vs alpine vs slim vs scratch
- `references/seccomp-profile-template.json` —— 典型 Web 服务器的最小系统调用白名单；从这里开始并按需扩展
- `references/kubernetes-pod-security.md` —— NetworkPolicy、RBAC、OPA/Kyverno 策略、ServiceAccount 加固、PSA

## 相关技能

- `docker-expert` —— 常规 Docker 使用、Compose 编排、镜像优化
- `gha-security-review` —— GitHub Actions 工作流的安全审计
- `github-actions-advanced` —— 包括扫描器集成的 CI 流水线模式
- `kubernetes-architect` —— 完整 Kubernetes 架构，而不仅仅是安全
- `api-security-best-practices` —— 应用层安全（注入、认证、OWASP）
- `k8s-security-policies` —— 扩展的 Kubernetes 安全策略

## 局限性

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为针对特定环境的渗透测试或正式安全审计的替代品。
- Seccomp 配置和 AppArmor 仅适用于 Linux；macOS/Windows 上的 Docker Desktop 使用不同的机制。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。