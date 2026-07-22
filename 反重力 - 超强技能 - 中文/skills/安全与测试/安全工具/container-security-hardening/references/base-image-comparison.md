# 基础镜像对比参考

容器基础镜像选型快速决策指南 —— 在安全性、兼容性、体积、可调试性之间取得平衡。

---

## 快速决策矩阵

| 运行时 / 需求 | 最佳选择 | 备选方案 |
|---|---|---|
| Go / Rust —— 完全静态二进制 | `scratch` | `gcr.io/distroless/static-debian12` |
| Go / Rust —— 带 CGO 或动态库 | `gcr.io/distroless/base-debian12` | `alpine:3.20` |
| Node.js 应用（生产） | `gcr.io/distroless/nodejs20-debian12` | `node:20-slim` |
| Python 应用（生产） | `gcr.io/distroless/python3-debian12` | `python:3.12-slim` |
| Java 应用（生产） | `gcr.io/distroless/java21-debian12` | `eclipse-temurin:21-jre-alpine` |
| 需要 Shell 脚本 | `alpine:3.20` | `debian:12-slim` |
| musl 兼容性问题 | `node:20-slim`（glibc） | `debian:12-slim` |
| 在预发布环境调试 | distroless `:debug` 变体 | `ubuntu:24.04`（临时） |

---

## 体积与 CVE 对比

> 2025 年中前后的近似数值。请运行 `trivy image <name>` 获取最新统计。

| 镜像 | 压缩后体积 | 典型 CVE 数量 | Shell | 包管理器 | libc |
|---|---|---|---|---|---|
| `scratch` | 0 MB | 0 | 无 | 无 | 无 |
| `gcr.io/distroless/static-debian12` | ~2 MB | 0–2 | 无 | 无 | 无 |
| `gcr.io/distroless/base-debian12` | ~20 MB | 0–3 | 无 | 无 | glibc |
| `gcr.io/distroless/nodejs20-debian12` | ~55 MB | 0–5 | 无 | 无 | glibc |
| `gcr.io/distroless/python3-debian12` | ~50 MB | 0–5 | 无 | 无 | glibc |
| `gcr.io/distroless/java21-debian12` | ~220 MB | 0–5 | 无 | 无 | glibc |
| `alpine:3.20` | ~3.5 MB | 0–5 | 有（ash） | 有（apk） | musl |
| `node:20-alpine` | ~65 MB | 5–20 | 有 | 有 | musl |
| `python:3.12-alpine` | ~55 MB | 5–20 | 有 | 有 | musl |
| `node:20-slim` | ~90 MB | 15–40 | 有 | 有（精简 apt） | glibc |
| `python:3.12-slim` | ~60 MB | 15–40 | 有 | 有（精简 apt） | glibc |
| `eclipse-temurin:21-jre-alpine` | ~180 MB | 5–20 | 有 | 有 | musl |
| `node:20`（完整版） | ~370 MB | 80–200 | 有 | 有（完整 apt） | glibc |
| `ubuntu:24.04` | ~30 MB | 20–60 | 有 | 有（完整 apt） | glibc |
| `ubuntu:24.04`（完整软件包） | ~200 MB+ | 50–150 | 有 | 有 | glibc |

---

## 详细权衡分析

### `scratch`
**适用场景：** Go、Rust 或任何以 `CGO_ENABLED=0` 构建的完全静态二进制

- ✅ 零攻击面 —— 完全空白
- ✅ 体积最小的可能镜像
- ✅ 没有可供利用的包管理器
- ❌ 无 libc、无 shell、无 CA 证书、无时区数据 —— 必须自行 `COPY` 进去
- ❌ 无法 exec 进入进行调试（完全没有 shell）

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /build
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w -extldflags=-static" \
    -o app .

FROM scratch
# 复制 CA 证书以支持 HTTPS 调用
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
# 如需时区数据则一并复制
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /build/app /app
USER 65532:65532
ENTRYPOINT ["/app"]
```

---

### `gcr.io/distroless`（Google）
**适用场景：** 生产环境 Node.js、Python、Java、Go（带 CGO）

- ✅ 无 shell、无包管理器 —— 攻击面大幅缩小
- ✅ 默认包含 CA 证书与 tzdata
- ✅ 内置 `nonroot` 用户（UID 65532）
- ✅ 基于 Debian —— glibc 兼容（不存在 musl 问题）
- ✅ 由 Google 定期打补丁
- ❌ 无法通过 `docker exec -it` 进入（无 shell）—— 预发布环境请使用 `:debug` 变体

```bash
# 可用的 distroless 变体
gcr.io/distroless/static-debian12       # 无 libc —— 适用于完全静态二进制
gcr.io/distroless/base-debian12         # glibc + openssl —— 适用于动态 Go/Rust
gcr.io/distroless/nodejs20-debian12     # Node.js 20 运行时
gcr.io/distroless/nodejs22-debian12     # Node.js 22 运行时
gcr.io/distroless/python3-debian12      # Python 3 运行时
gcr.io/distroless/java21-debian12       # JRE 21
gcr.io/distroless/cc-debian12           # C/C++ 运行时

# Debug 变体 —— 预发布环境专用，包含 busybox shell
gcr.io/distroless/nodejs20-debian12:debug
gcr.io/distroless/python3-debian12:debug
```

**调试 distroless 容器（仅限预发布环境）：**
```bash
# 使用 sidecar 调试容器，不要修改生产镜像
kubectl debug -it deploy/myapp \
  --image=busybox \
  --target=app \
  --copy-to=debug-pod
```

---

### `alpine`
**适用场景：** 需要 Shell 的镜像，或将镜像体积作为首要考量时

- ✅ 体积非常小（约 3.5 MB）
- ✅ 自带 shell（ash）和包管理器（apk）—— 调试友好
- ✅ 定期更新，社区活跃
- ⚠️ 使用 **musl libc** —— 某些 Python C 扩展、Node.js 原生模块或依赖 glibc 的二进制可能失败
- ❌ CVE 数量多于 distroless（因为包含更多软件包）

**musl 兼容性检查：**
```bash
# 提交前在 alpine 上测试你的应用
docker run -it --rm -v $(pwd):/app node:20-alpine sh -c "cd /app && npm ci && npm test"
```

**常见的 musl 问题：**
- `bcrypt`、`node-gyp`、`sharp`、`canvas` 等原生模块 → 可能需要构建工具
- 带 `numpy`、`scipy`、`pandas` 的 Python → 改用 `python:3.12-slim`
- Java 应用 → 通常无碍，但请充分测试

---

### `slim` 变体（基于 Debian）
**适用场景：** 依赖 glibc 但又无法使用 distroless 的应用

- ✅ glibc 兼容 —— 不存在 musl 问题
- ✅ 熟悉的 `apt` 生态
- ✅ 比完整镜像更小（约 60–90 MB 对比 300–400 MB）
- ❌ CVE 数量多于 distroless（包含 apt、shell 与更多系统库）
- ❌ 体积大于 alpine

```dockerfile
FROM node:20-slim
# 仅安装必要软件，并在同一层清理缓存
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libssl3 \
    && rm -rf /var/lib/apt/lists/*
```

---

### 完整镜像（`node:20`、`ubuntu:24.04`、`python:3.12`）
**仅适用于：** 开发、CI 构建阶段或调试 —— 绝不能作为生产运行时

- ❌ 攻击面巨大（50–200+ CVE）
- ❌ 包含编译器、构建工具、包管理器 —— 运行时无需这些
- ❌ 体积庞大导致拉取耗时与存储成本增加

仅用作构建阶段：
```dockerfile
FROM node:20 AS builder     # 完整镜像用于构建
FROM node:20-slim AS runtime  # 精简镜像用于生产
```

---

## 保持基础镜像更新

**容器 CVE 最常见的来源就是过时的基础镜像。**

### 手动检查
```bash
# 拉取最新版并查看摘要
docker pull node:20-slim
docker inspect node:20-slim --format='{{index .RepoDigests 0}}'

# 更新前检查当前基础镜像的 CVE
trivy image node:20-slim --severity HIGH,CRITICAL
```

### 使用 Renovate 自动化（推荐）
```json
// .renovaterc.json
{
  "extends": ["config:base"],
  "dockerfile": {
    "enabled": true,
    "pinDigests": true
  },
  "packageRules": [
    {
      "matchDatasources": ["docker"],
      "matchPackagePatterns": ["^gcr.io/distroless"],
      "automerge": true,
      "automergeType": "branch"
    }
  ]
}
```

### 使用 Dependabot 自动化
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

---

## Distroless 摘要钉版参考

务必使用摘要钉版。可在此处查询当前摘要：
- `gcr.io/distroless/nodejs20-debian12` → `docker pull gcr.io/distroless/nodejs20-debian12 && docker inspect gcr.io/distroless/nodejs20-debian12 --format='{{index .RepoDigests 0}}'`
- 最新版本请访问 [Google 的 distroless tags 页面](https://github.com/GoogleContainerTools/distroless/blob/main/README.md)

---

## 镜像体积精简清单

当镜像体积过大时：

- [ ] 已切换到 distroless 或 alpine 运行时阶段？
- [ ] 通过多阶段构建分离构建与运行时？
- [ ] `npm ci --only=production` / `pip install --no-dev`？
- [ ] 在同一 `RUN` 层清理构建缓存（`rm -rf /var/lib/apt/lists/*`、`npm cache clean --force`）？
- [ ] `.dockerignore` 已排除 `node_modules`、`.git`、`tests/`、`docs/`？
- [ ] 使用 `--mount=type=cache` 复用包管理器缓存（BuildKit）？
- [ ] 仅将必要文件 `COPY` 到运行时阶段？
- [ ] 生产镜像中没有调试工具？

```bash
# 分析镜像各层占用，找出体积膨胀的位置
docker history --no-trunc myapp:latest
dive myapp:latest    # 交互式镜像分层浏览器：https://github.com/wagoodman/dive
```