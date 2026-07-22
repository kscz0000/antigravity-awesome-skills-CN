---
name: github-actions-advanced
description: >
  设计、调试和加固 GitHub Actions CI/CD 工作流，涵盖可复用工作流、矩阵构建、自托管运行器、OIDC 认证、缓存策略、环境、密钥和发布自动化。触发词：GitHub Actions、工作流、CI/CD 流水线、矩阵构建、可复用工作流、自托管运行器、OIDC、缓存、密钥管理、发布自动化。
category: devops
risk: safe
source: community
date_added: "2026-05-30"
---

# GitHub Actions 进阶技能

针对设计、编写、调试和保护**生产级** GitHub Actions 工作流的专家级指南。

---

## 适用场景

- 用户提到 GitHub Actions、`.github/workflows`、CI/CD 流水线、运行器、作业、步骤或操作
- 需要通过 GitHub 自动化构建、测试、部署或发布
- 涉及矩阵构建、可复用工作流、组合操作或自托管运行器
- 需要 OIDC 认证、缓存策略或密钥管理方面的帮助
- 用户说"GitHub 流水线挂了"或"给我的仓库搭 CI"
- 涉及工作流安全加固、环境保护规则

## 不适用场景

- 使用 GitLab CI/CD → 推荐 `gitlab-ci-patterns`
- 使用 CircleCI、Jenkins 或其他 CI 平台
- 纯 Docker 镜像构建（无 GitHub 上下文）→ 推荐 `docker-expert`
- Kubernetes 部署配置 → 推荐 `kubernetes-architect`

---

## 步骤 1：回复前先了解上下文

调用此技能时，先收集上下文：

```bash
# Discover existing workflows in the repo
find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null | head -20

# Check for composite actions
find .github/actions -name "action.yml" 2>/dev/null

# Detect tech stack (influences runner OS, language setup actions)
ls package.json requirements.txt Gemfile go.mod Cargo.toml pom.xml 2>/dev/null
```

然后根据以下因素调整建议：
- 仓库中已有的工作流模式
- 技术栈和语言运行时
- 是否为 monorepo 或单项目仓库
- 使用自托管还是 GitHub 托管的运行器

---

## 工作流结构参考

```yaml
name: Workflow Name

on:                          # Triggers (see Triggers section)
  push:
    branches: [main]

permissions:                 # Always declare — principle of least privilege
  contents: read

env:                         # Workflow-level env vars
  NODE_VERSION: '20'

concurrency:                 # Prevent duplicate runs
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true   # Cancel older runs for same branch

jobs:
  job-id:
    name: Human-readable name
    runs-on: ubuntu-24.04    # Pin OS version — never use -latest in prod
    timeout-minutes: 15      # Always set — prevents runaway jobs
    environment: production  # Links to GitHub Environment (approvals/secrets)

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - name: Step name
        run: echo "hello"
```

---

## 触发器（`on:`）

### 常用模式

```yaml
on:
  push:
    branches: [main, 'release/**']
    paths-ignore: ['**.md', 'docs/**']   # Skip docs-only changes

  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]

  workflow_dispatch:                      # Manual trigger with inputs
    inputs:
      environment:
        description: 'Deploy target'
        required: true
        type: choice
        options: [staging, production]
      dry-run:
        description: 'Dry run only?'
        type: boolean
        default: false

  schedule:
    - cron: '0 2 * * 1'                 # Monday 2am UTC

  workflow_call:                          # Called by other workflows (reusable)
    inputs:
      image-tag:
        type: string
        required: true
    secrets:
      deploy-token:
        required: true

  release:
    types: [published]                   # Trigger only on published releases

  pull_request_target:                   # Runs with repo secrets — use with care!
    types: [labeled]                     # Gate with label + author_association check
```

> **安全警告：** `pull_request_target` 会使用仓库密钥运行。仅在维护者为 PR 添加标签后才可使用。未经明确沙箱化，绝不要检出 fork 代码。

---

## 可复用工作流

将大型流水线拆分为存储在 `.github/workflows/` 中的可组合单元。

**约定：** 内部/可复用工作流以 `_` 为前缀（如 `_build.yml`）。

### 调用方（`.github/workflows/deploy.yml`）

```yaml
jobs:
  call-build:
    uses: ./.github/workflows/_build.yml        # Same-repo reusable
    # uses: org/repo/.github/workflows/build.yml@main  # Cross-repo
    with:
      image-tag: ${{ github.sha }}
    secrets: inherit                             # Pass all caller secrets down
  
  call-test:
    uses: ./.github/workflows/_test.yml
    with:
      node-version: '20'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}       # Explicit secret passing
```

### 可复用工作流（`.github/workflows/_build.yml`）

```yaml
on:
  workflow_call:
    inputs:
      image-tag:
        type: string
        required: true
      push:
        type: boolean
        default: false
    secrets:
      registry-token:
        required: false
    outputs:
      digest:
        description: "Image digest"
        value: ${{ jobs.build.outputs.digest }}

jobs:
  build:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - id: build
        uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75  # v6.9.0
        with:
          push: ${{ inputs.push }}
          tags: myapp:${{ inputs.image-tag }}
```

---

## 矩阵构建

```yaml
jobs:
  test:
    strategy:
      fail-fast: false           # Don't cancel others if one fails
      max-parallel: 4            # Limit concurrent runners
      matrix:
        os: [ubuntu-24.04, windows-2022, macos-14]
        node: ['18', '20', '22']
        exclude:
          - os: windows-2022
            node: '18'
        include:
          - os: ubuntu-24.04
            node: '22'
            experimental: true   # Custom matrix variable

    runs-on: ${{ matrix.os }}
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
        continue-on-error: ${{ matrix.experimental == true }}
```

### 通过脚本动态生成矩阵

```yaml
jobs:
  generate-matrix:
    runs-on: ubuntu-24.04
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - id: set-matrix
        run: |
          SERVICES=$(find services -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | jq -R -s -c 'split("\n")[:-1]')
          printf 'matrix={"service":%s}\n' "$SERVICES" >> "$GITHUB_OUTPUT"

  build:
    needs: generate-matrix
    strategy:
      matrix: ${{ fromJson(needs.generate-matrix.outputs.matrix) }}
    runs-on: ubuntu-24.04
    steps:
      - env:
          SERVICE: ${{ matrix.service }}
        run: echo "Building $SERVICE"
```

---

## 缓存策略

### 语言安装操作（优先选择——无需额外步骤）

```yaml
# Node.js
- uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
  with:
    node-version: '20'
    cache: 'npm'           # or 'yarn' or 'pnpm'

# Python
- uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b  # v5.3.0
  with:
    python-version: '3.12'
    cache: 'pip'

# Go
- uses: actions/setup-go@3041bf56c941b39c61721a86cd11f3bb1338122a  # v5.2.0
  with:
    go-version: '1.23'
    cache: true

# Java / Gradle / Maven
- uses: actions/setup-java@7a6d8a8234af8eb26422e24052f73b12b0e46a27  # v4.6.0
  with:
    distribution: 'temurin'
    java-version: '21'
    cache: 'maven'        # or 'gradle'
```

### 手动缓存（任意工具）

```yaml
- uses: actions/cache@6849a6489940f00c2f30c0fb92c6274307ccb58a  # v4.1.2
  id: cache-deps
  with:
    path: |
      ~/.cache/pip
      .venv
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
      ${{ runner.os }}-pip-

- name: Install deps (only on cache miss)
  if: steps.cache-deps.outputs.cache-hit != 'true'
  run: pip install -r requirements.txt
```

### Docker 层缓存

```yaml
- uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75  # v6.9.0
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
    # For registry-backed cache (cross-branch):
    # cache-from: type=registry,ref=ghcr.io/myorg/myapp:buildcache
    # cache-to: type=registry,ref=ghcr.io/myorg/myapp:buildcache,mode=max
```

---

## OIDC 认证（无密钥云认证）

**绝不将长期有效的云凭证存储为密钥。** 使用 OIDC 获取自动过期的短期令牌。

### AWS

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4.0.2
    with:
      role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
      aws-region: us-east-1
      role-session-name: GitHubActions-${{ github.run_id }}

  # Trust policy on the IAM role must include:
  # "token.actions.githubusercontent.com" as OIDC provider
  # Condition: "repo:org/repo:ref:refs/heads/main" (restrict to branch)
```

### GCP（Workload Identity Federation）

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: google-github-actions/auth@6fc4af4b145ae7821d527454aa9bd537d1f2dc5f  # v2.1.7
    with:
      workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider
      service_account: github-actions@my-project.iam.gserviceaccount.com
      token_format: access_token   # or 'id_token'
```

### Azure（联合身份验证）

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: azure/login@a65d910e8af852a8061c627c456678983e180302  # v2.2.0
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      # No client secret needed! Uses OIDC federated credentials
```

---

## 环境与部署保护

```yaml
jobs:
  deploy-staging:
    environment:
      name: staging
      url: https://staging.myapp.com
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    steps:
      - run: ./scripts/deploy.sh staging

  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://myapp.com      # Shown in the GitHub UI deployment panel
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    steps:
      - run: ./scripts/deploy.sh production
```

**在 Settings → Environments 中配置：**
- **必需审阅者** — 运行前的人工审批关卡
- **等待计时器** — 审批后延迟（如 10 分钟缓冲）
- **分支/标签限制** — 仅 `main` 或 `v*` 标签可部署到生产环境
- **环境专用密钥** — 按环境覆盖仓库级密钥
- **部署分支** — 白名单允许哪些分支部署到此环境

---

## 密钥管理

```yaml
# Access repo/org/environment secrets
env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}

# Auto-provided token — no setup needed
- uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea  # v7.0.1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}

# Hierarchy (most specific wins):
# environment secret > repo secret > org secret
```

### 动态值掩码

```yaml
- name: Generate and mask dynamic token
  run: |
    TOKEN=$(./scripts/generate-token.sh)
    echo "::add-mask::$TOKEN"          # Mask in all subsequent logs
    echo "DEPLOY_TOKEN=$TOKEN" >> $GITHUB_ENV
```

### 组合操作中的密钥

```yaml
# Secrets cannot be passed as inputs to composite actions
# Pass them as env vars instead:
- uses: ./.github/actions/my-action
  env:
    SECRET_VALUE: ${{ secrets.MY_SECRET }}
```

---

## 组合操作

将可复用的步骤序列打包为本地操作。无需启动容器，也无需单独的工作流文件。

### 操作定义（`.github/actions/setup-app/action.yml`）

```yaml
name: Setup App
description: Install and configure application dependencies

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'
  install-flags:
    description: 'Additional npm install flags'
    required: false
    default: ''

outputs:
  cache-hit:
    description: 'Whether the dependency cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: composite
  steps:
    - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
      with:
        node-version: ${{ inputs.node-version }}
        cache: npm

    - id: cache
      uses: actions/cache@6849a6489940f00c2f30c0fb92c6274307ccb58a  # v4.1.2
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ inputs.node-version }}-${{ hashFiles('package-lock.json') }}

    - name: Install dependencies
      if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      env:
        INSTALL_FLAGS: ${{ inputs.install-flags }}
      run: |
        args=()
        case "$INSTALL_FLAGS" in
          "") ;;
          "--ignore-scripts") args+=(--ignore-scripts) ;;
          *) echo "Unsupported install flags" >&2; exit 1 ;;
        esac
        npm ci "${args[@]}"

    - name: Build
      shell: bash
      run: npm run build
```

### 在工作流中使用

```yaml
steps:
  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
  - uses: ./.github/actions/setup-app
    with:
      node-version: '22'
      install-flags: '--ignore-scripts'
```

---

## 自托管运行器

```yaml
jobs:
  build-gpu:
    runs-on: [self-hosted, linux, x64, gpu]    # Label matching
    timeout-minutes: 60

  build-arm:
    runs-on: [self-hosted, linux, arm64]
```

### 运行器最佳实践

| 实践 | 说明 |
|---|---|
| **临时运行器** | 在 Kubernetes 上使用 Actions Runner Controller (ARC)，每个作业获得全新运行器 |
| **隔离** | 绝不在生产运行器上运行不可信的 fork PR 工作流 |
| **清理钩子** | 设置 `ACTIONS_RUNNER_HOOK_JOB_COMPLETED` 以重置环境 |
| **运行器组** | 使用组限制哪些仓库/工作流可以访问哪些运行器 |
| **标签** | 使用自定义标签（如 `gpu`、`high-memory`）实现精确匹配 |
| **安全** | 在 Settings 中禁止 fork PR 访问自托管运行器 |

```bash
# Actions Runner Controller (Kubernetes) — recommended for ephemeral runners
helm install arc \
  --namespace arc-systems \
  --create-namespace \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```

---

## 条件执行与流程控制

```yaml
# Condition on branch + event
- run: ./scripts/deploy.sh
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'

# Continue on error (non-blocking steps)
- run: ./scripts/lint.sh
  continue-on-error: true

# Job dependency and conditional execution
jobs:
  test:
    runs-on: ubuntu-24.04
    outputs:
      result: ${{ steps.run-tests.outcome }}

  deploy:
    needs: [test, build]
    if: |
      needs.test.result == 'success' &&
      needs.build.result == 'success' &&
      github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04

  notify-failure:
    needs: [test, deploy]
    if: failure()          # Runs even if earlier jobs fail
    runs-on: ubuntu-24.04
    steps:
      - run: ./scripts/notify-slack.sh "Pipeline failed!"
```

### 在作业间传递数据

```yaml
jobs:
  prepare:
    runs-on: ubuntu-24.04
    outputs:
      version: ${{ steps.get-version.outputs.version }}
      should-deploy: ${{ steps.check.outputs.deploy }}

    steps:
      - id: get-version
        run: |
          VERSION=$(tr -d '\r\n' < VERSION)
          case "$VERSION" in
            ""|*[!0-9A-Za-z._-]*) echo "Invalid VERSION" >&2; exit 1 ;;
          esac
          printf 'version=%s\n' "$VERSION" >> "$GITHUB_OUTPUT"

      - id: check
        run: |
          if git log -1 --pretty=%B | grep -q '\[deploy\]'; then
            echo "deploy=true" >> $GITHUB_OUTPUT
          else
            echo "deploy=false" >> $GITHUB_OUTPUT
          fi

  build:
    needs: prepare
    if: needs.prepare.outputs.should-deploy == 'true'
    runs-on: ubuntu-24.04
    steps:
      - env:
          VERSION: ${{ needs.prepare.outputs.version }}
        run: echo "Building version $VERSION"
```

---

## 安全加固

### 1. 始终声明权限（最小权限原则）

```yaml
# Workflow-level default — restrict everything
permissions:
  contents: read

jobs:
  publish:
    # Job-level override — only expand what's needed
    permissions:
      contents: write        # Only for release/publish jobs
      packages: write        # Only for container push jobs
      pull-requests: write   # Only for PR comment jobs
      id-token: write        # Only for OIDC auth jobs
```

### 2. 将第三方操作锁定到完整 commit SHA

```yaml
# ❌ UNSAFE — tag can be mutated or hijacked
- uses: actions/checkout@v4

# ✅ SAFE — commit SHA is immutable
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# Tool to automate SHA pinning:
# npx pin-github-action .github/workflows/*.yml
# or: pip install ratchet && ratchet pin .github/workflows/
```

### 3. 防止脚本注入

```yaml
# ❌ UNSAFE — attacker controls PR title, which gets expanded in shell
- run: echo "${{ github.event.pull_request.title }}"

# ✅ SAFE — pass through environment variable (shell doesn't evaluate it)
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "$PR_TITLE"

# ✅ SAFE — expressions in if: conditions are evaluated by Actions, not shell
- if: github.event.pull_request.draft == false
  run: echo "Not a draft"
```

当值可能来自 PR 元数据、工作流输入、仓库文件、矩阵 JSON 或上游作业输出时，绝不将 `${{ ... }}` 直接放在 `run:` 中。先放入 `env:`，尽可能验证白名单值，然后用引号引用 shell 变量。

### 4. 限制 `pull_request_target` 的使用

```yaml
# Only run when a maintainer adds a specific label — prevents untrusted execution
on:
  pull_request_target:
    types: [labeled]

jobs:
  validate:
    # Double-guard: check label name AND author_association
    if: |
      github.event.label.name == 'safe-to-test' &&
      (github.event.pull_request.author_association == 'COLLABORATOR' ||
       github.event.pull_request.author_association == 'MEMBER' ||
       github.event.pull_request.author_association == 'OWNER')
```

### 5. 使用 StepSecurity 加固

```yaml
# Add to every workflow — hardens runner, monitors outbound traffic
- uses: step-security/harden-runner@4d991eb9995541a0b71d1b66f1f98a5f1bef422c  # v2.11.0
  with:
    egress-policy: audit          # Start with 'audit', move to 'block' after confirming allowlist
    allowed-endpoints: >
      api.github.com:443
      registry.npmjs.org:443
      objects.githubusercontent.com:443
```

---

## 调试技巧

```yaml
# Enable runner diagnostic logging via repo secrets:
# ACTIONS_RUNNER_DEBUG = true
# ACTIONS_STEP_DEBUG = true

# Dump full GitHub context for inspection
- name: Debug — dump github context
  if: runner.debug == '1'
  env:
    GITHUB_CONTEXT: ${{ toJson(github) }}
  run: echo "$GITHUB_CONTEXT" | jq '.'

# Dump all available contexts
- name: Debug — dump all contexts
  if: runner.debug == '1'
  run: |
    echo "github: ${{ toJson(github) }}"
    echo "env: ${{ toJson(env) }}"
    echo "vars: ${{ toJson(vars) }}"
    echo "runner: ${{ toJson(runner) }}"

# SSH into a failing runner for interactive debugging
- uses: mxschmitt/action-tmate@7b04f3521e6b0a9fc56fa8f9f50da4bcfb5fc7b5  # v3.19.0
  if: failure() && runner.debug == '1'
  with:
    limit-access-to-actor: true    # Only the workflow triggerer can SSH in
    timeout-minutes: 30

# Check what's pre-installed on GitHub-hosted runners
- run: |
    echo "=== Tool Versions ===" 
    node --version
    python3 --version
    go version
    docker --version
    echo "=== Disk Space ==="
    df -h
    echo "=== Memory ==="
    free -h
```

---

## 完整流水线模式

### 模式 1：构建 → 测试 → 推送 → 部署

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

permissions:
  contents: read

jobs:
  # ── Build & Test ──────────────────────────────────────
  build-test:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    permissions:
      contents: read
      checks: write        # For test result reporting

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run test -- --coverage
      - run: npm run build

      - uses: actions/upload-artifact@b4b15b8c7c6ac21ea08fcf65892d2ee8f75cf882  # v4.4.3
        with:
          name: build-artifacts
          path: dist/
          retention-days: 7

  # ── Push Image (main branch only) ─────────────────────
  push-image:
    needs: build-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    permissions:
      contents: read
      packages: write
      id-token: write      # For OIDC
    outputs:
      image-digest: ${{ steps.push.outputs.digest }}

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - uses: docker/setup-buildx-action@c47758b77c9736f4b2ef4073d4d51994fabfe349  # v3.7.1

      - uses: docker/login-action@9780b0c442fbb1117ed29e0efdff1e18412f7567  # v3.3.0
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@70b2cdc6480c1a8b86edf1777157f8f437de2166  # v5.5.1
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha,format=long
            type=raw,value=latest

      - id: push
        uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75  # v6.9.0
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true    # SLSA provenance attestation
          sbom: true          # Software Bill of Materials

  # ── Deploy Staging ────────────────────────────────────
  deploy-staging:
    needs: push-image
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    environment:
      name: staging
      url: https://staging.myapp.com
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - env:
          IMAGE_DIGEST: ${{ needs.push-image.outputs.image-digest }}
        run: ./scripts/deploy.sh staging "$IMAGE_DIGEST"

  # ── Deploy Production (manual approval required) ──────
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    environment:
      name: production
      url: https://myapp.com
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - env:
          IMAGE_DIGEST: ${{ needs.push-image.outputs.image-digest }}
        run: ./scripts/deploy.sh production "$IMAGE_DIGEST"
```

### 模式 2：带更新日志的自动发布

```yaml
name: Release

on:
  push:
    tags: ['v[0-9]+.[0-9]+.[0-9]+']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-24.04
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          fetch-depth: 0    # Full history needed for changelog generation

      - uses: softprops/action-gh-release@e7a8f85e1c67a31e6ed99a94b41bd0b71bbee6b8  # v2.0.9
        with:
          generate_release_notes: true    # Auto-generates from PR titles and commits
          make_latest: true
          fail_on_unmatched_files: true
          files: |
            dist/**/*.tar.gz
            dist/**/*.zip
```

### 模式 3：依赖自动更新并创建 PR

```yaml
name: Dependency Updates

on:
  schedule:
    - cron: '0 9 * * 1'    # Every Monday at 9am UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  update-deps:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af  # v4.1.0
        with:
          node-version: '20'

      - run: npx npm-check-updates -u
      - run: npm install

      - uses: peter-evans/create-pull-request@5e914681df9dc83aa4e4905692ca88beb2f9e91f  # v7.0.5
        with:
          commit-message: 'chore: update npm dependencies'
          title: 'chore: update npm dependencies'
          branch: 'chore/npm-updates'
          delete-branch: true
          body: |
            Automated dependency updates generated by the dependency update workflow.
            Please review and test before merging.
```

### 模式 4：安全扫描流水线

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'    # Daily at 6am UTC

permissions:
  contents: read
  security-events: write    # For uploading SARIF results

jobs:
  codeql:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    permissions:
      security-events: write
      actions: read
      contents: read
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: github/codeql-action/init@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1
        with:
          languages: javascript-typescript
      - uses: github/codeql-action/autobuild@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1
      - uses: github/codeql-action/analyze@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1

  container-scan:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: aquasecurity/trivy-action@6e7b7d1fd3e4fef0c5fa8cce1229c54b2c9bd0d8  # v0.28.0
        with:
          scan-type: 'fs'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      - uses: github/codeql-action/upload-sarif@4f3212b61783c3c68e8309a0f18a699764811cda  # v3.27.1
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## 常见问题与修复

| 问题 | 原因 | 修复 |
|---|---|---|
| Fork 的 PR 不触发工作流 | Fork PR 使用受限的 `GITHUB_TOKEN` | 使用 `pull_request` 而非 `pull_request_target`；避免在 fork 上下文中使用仓库密钥 |
| 密钥在日志中显示 `***` 但实际已泄露 | 动态值未被掩码 | 在使用前执行 `echo "::add-mask::$VALUE"` |
| 缓存在分支间从不命中 | 缓存键过于具体 | 添加不含分支或哈希段的 `restore-keys` 回退 |
| 矩阵作业静默失败 | `fail-fast: true`（默认值）取消了同级作业 | 调试时设置 `fail-fast: false` |
| 作业无限挂起 | 未设置 `timeout-minutes` | 始终为每个作业设置 `timeout-minutes` |
| `$GITHUB_OUTPUT` 未设置 | 使用了旧的 `set-output` 命令 | 使用 `echo "key=value" >> $GITHUB_OUTPUT` |
| OIDC 令牌请求失败 | 缺少 `id-token: write` 权限 | 在作业级 `permissions` 块中添加 |
| 可复用工作流无法访问调用方密钥 | 未使用 `secrets: inherit` | 添加 `secrets: inherit` 或显式传递密钥 |

---

## GitHub Actions 表达式参考

```yaml
# Context objects available in expressions
${{ github.sha }}                           # Commit SHA
${{ github.ref }}                           # Branch/tag ref
${{ github.ref_name }}                      # Short branch/tag name
${{ github.event_name }}                    # Event name (push, pull_request, etc.)
${{ github.actor }}                         # Username who triggered the run
${{ github.repository }}                    # org/repo
${{ github.run_id }}                        # Unique run ID
${{ runner.os }}                            # Linux, Windows, macOS

# Built-in functions
${{ toJson(github) }}                       # Serialize context to JSON
${{ fromJson(needs.job.outputs.matrix) }}   # Parse JSON string
${{ hashFiles('**/package-lock.json') }}    # Hash file(s) for cache keys
${{ format('{0}/{1}', var1, var2) }}        # String formatting
${{ join(matrix.items, ',') }}              # Join array

# Status functions (use in if: conditions)
${{ success() }}    # All previous steps succeeded
${{ failure() }}    # Any previous step failed
${{ cancelled() }}  # Workflow was cancelled
${{ always() }}     # Always runs (success OR failure OR cancelled)
```

---

## 生产就绪检查清单

将任何工作流合并到 `main` 之前，请验证：

### 安全
- [ ] 所有第三方操作已锁定到完整 commit SHA
- [ ] 在工作流和作业级声明了 `permissions:`（最小权限）
- [ ] `run:` 块中没有直接的 `${{ }}` 表达式（使用环境变量）
- [ ] 云凭证使用 OIDC（不存储长期密钥）
- [ ] `pull_request_target` 已用标签检查 + author_association 守卫做门控
- [ ] 密钥从不被回显或记录到日志

### 可靠性
- [ ] 每个作业都设置了 `timeout-minutes`
- [ ] 用于调试的矩阵构建设置了 `fail-fast: false`
- [ ] 配置了 `concurrency` 以取消过期运行
- [ ] 不稳定的外部调用有重试逻辑
- [ ] 制品保留策略已适当设置

### 性能
- [ ] 依赖缓存已配置（setup-* cache 或 actions/cache）
- [ ] Docker 层缓存已启用（`type=gha`）
- [ ] `push`/`pull_request` 上配置了路径过滤以跳过无关变更
- [ ] 矩阵并行度适当（不会耗尽运行器池）

### 可维护性
- [ ] 重复模式使用了可复用工作流
- [ ] 重复步骤序列使用了组合操作
- [ ] 工作流名称和步骤名称可读
- [ ] 内部/可复用工作流文件使用 `_` 前缀
- [ ] `production` 环境已配置环境保护规则

---

## 相关技能

- `gha-security-review` — 对现有工作流文件进行深度安全审计
- `github-actions-templates` — 可直接复制使用的工作流模板
- `docker-expert` — 容器构建优化和 Dockerfile 最佳实践
- `kubernetes-architect` — 从 GitHub Actions 部署到 Kubernetes
- `gitlab-ci-patterns` — GitLab CI/CD 等效模式

## 局限性

- 仅当任务明确符合上述范围时才使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 合并到 main 之前，始终在功能分支中测试可复用工作流。
- 如果缺少必要的输入、权限、安全边界或成功标准，停下来询问澄清。
