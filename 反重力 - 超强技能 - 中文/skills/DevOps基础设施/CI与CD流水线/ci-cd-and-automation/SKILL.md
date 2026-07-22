---
name: ci-cd-and-automation
description: 自动化 CI/CD 流水线配置。用于搭建或修改构建与部署流水线时、需要自动化质量门禁、在 CI 中配置测试运行器，或建立部署策略时使用。触发词：CI/CD、流水线、自动化、部署、质量门禁、GitHub Actions
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/ci-cd-and-automation
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# CI/CD 与自动化

## 概述

自动化质量门禁，确保任何变更在通过测试、lint、类型检查与构建之前都无法进入生产环境。CI/CD 是所有其他技能的强制执行机制——它能一致地捕获人类与智能体忽略的问题，对每一次变更都一视同仁。

**左移原则：** 尽可能在流水线早期发现问题。在 lint 阶段捕获一个 bug 只需几分钟；在生产环境捕获同样的 bug 则要耗费数小时。将检查环节前置——静态分析先于测试，测试先于预发布，预发布先于生产。

**更快即更安全：** 更小的批次与更频繁的发布降低风险，而非增加风险。一次包含 3 处变更的部署，远比一次包含 30 处变更的部署易于调试。频繁发布能建立对发布流程本身的信心。

## 使用场景

- 为新项目搭建 CI 流水线
- 新增或修改自动化检查
- 配置部署流水线
- 当某次变更应当触发自动化校验时
- 调试 CI 失败

## 质量门禁流水线

每次变更在合并前都必须通过以下门禁：

```
Pull Request Opened
    │
    ▼
┌─────────────────┐
│   LINT CHECK     │  eslint, prettier
│   ↓ pass         │
│   TYPE CHECK     │  tsc --noEmit
│   ↓ pass         │
│   UNIT TESTS     │  jest/vitest
│   ↓ pass         │
│   BUILD          │  npm run build
│   ↓ pass         │
│   INTEGRATION    │  API/DB tests
│   ↓ pass         │
│   E2E (optional) │  Playwright/Cypress
│   ↓ pass         │
│   SECURITY AUDIT │  npm audit
│   ↓ pass         │
│   BUNDLE SIZE    │  bundlesize check
└─────────────────┘
    │
    ▼
  Ready for review
```

**任何门禁都不可跳过。** lint 失败就去修复 lint——不要禁用规则；测试失败就去修复代码——不要跳过测试。

## GitHub Actions 配置

### 基础 CI 流水线

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Test
        run: npm test -- --coverage

      - name: Build
        run: npm run build

      - name: Security audit
        run: npm audit --audit-level=high
```

### 包含数据库集成测试

```yaml
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Run migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
      - name: Integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
```

> **注意：** 即使是仅供 CI 使用的测试数据库，也应通过 GitHub Secrets 管理凭据，而非硬编码。这样能养成良好习惯，避免测试凭据在其它场景下被意外复用。

### E2E 测试

```yaml
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps chromium
      - name: Build
        run: npm run build
      - name: Run E2E tests
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## 将 CI 失败反馈给智能体

AI 智能体使用 CI 的关键在于反馈闭环。当 CI 失败时：

```
CI fails
    │
    ▼
Copy the failure output
    │
    ▼
Feed it to the agent:
"The CI pipeline failed with this error:
[粘贴具体错误]
Fix the issue and verify locally before pushing again."
    │
    ▼
Agent fixes → pushes → CI runs again
```

**关键模式：**

```
Lint failure → Agent runs `npm run lint --fix` and commits
Type error  → Agent reads the error location and fixes the type
Test failure → Agent follows debugging-and-error-recovery skill
Build error → Agent checks config and dependencies
```

## 部署策略

### 预览部署

每个 PR 都应获得一个预览部署，用于人工测试：

```yaml
# Deploy preview on PR (Vercel/Netlify/etc.)
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - name: Deploy preview
      run: npx vercel --token=${{ secrets.VERCEL_TOKEN }}
```

### 功能开关

功能开关将部署与发布解耦。把尚未完成或存在风险的功能部署在开关之后，以便：

- **发布代码但不启用。** 尽早合并到 main，准备就绪后再启用。
- **无需重新部署即可回滚。** 关闭开关即可，不必回退代码。
- **灰度新功能。** 先对 1% 用户开启，再到 10%，最终全量。
- **运行 A/B 测试。** 对比功能开启与关闭时的行为差异。

```typescript
// 简单的功能开关模式
if (featureFlags.isEnabled('new-checkout-flow', { userId })) {
  return renderNewCheckout();
}
return renderLegacyCheckout();
```

**开关生命周期：** 创建 → 启用测试 → 灰度 → 全量发布 → 移除开关及死代码。永久存在的开关将变成技术债——在创建时设定清理日期。

### 分阶段发布

```
PR merged to main
    │
    ▼
  Staging deployment (auto)
    │ Manual verification
    ▼
  Production deployment (manual trigger or auto after staging)
    │
    ▼
  Monitor for errors (15-minute window)
    │
    ├── Errors detected → Rollback
    └── Clean → Done
```

### 回滚方案

每次部署都应可逆：

```yaml
# 手动回滚工作流
name: Rollback
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        run: |
          # Deploy the specified previous version
          npx vercel rollback ${{ inputs.version }}
```

## 环境管理

```
.env.example       → Committed (template for developers)
.env                → NOT committed (local development)
.env.test           → Committed (test environment, no real secrets)
CI secrets          → Stored in GitHub Secrets / vault
Production secrets  → Stored in deployment platform / vault
```

CI 永远不应持有生产环境的密钥。CI 测试应使用独立的密钥。

## CI 之外的自动化

### Dependabot / Renovate

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

### 构建守护人角色

指定专人负责保持 CI 处于通过状态。当构建失败时，构建守护人的职责是修复或回退——而不是由引发故障的变更作者本人处理。这能避免在所有人都指望别人修复时，破损的构建不断累积。

### PR 检查

- **强制评审：** 合并前至少 1 个审批
- **强制状态检查：** 合并前必须通过 CI
- **分支保护：** main 分支禁止强制推送
- **自动合并：** 若所有检查通过且已获批准，则自动合并

## CI 优化

当流水线超过 10 分钟时，按以下影响顺序应用这些策略：

```
Slow CI pipeline?
├── Cache dependencies
│   └── Use actions/cache or setup-node cache option for node_modules
├── Run jobs in parallel
│   └── Split lint, typecheck, test, build into separate parallel jobs
├── Only run what changed
│   └── Use path filters to skip unrelated jobs (e.g., skip e2e for docs-only PRs)
├── Use matrix builds
│   └── Shard test suites across multiple runners
├── Optimize the test suite
│   └── Remove slow tests from the critical path, run them on a schedule instead
└── Use larger runners
    └── GitHub-hosted larger runners or self-hosted for CPU-heavy builds
```

**示例：缓存与并行**
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
```

## 常见借口

| 借口 | 现实 |
|---|---|
| "CI 太慢了" | 优化流水线（见下方 CI 优化），而不是跳过它。5 分钟的流水线能省下数小时的调试。 |
| "这次改动很小，跳过 CI 吧" | 微小的改动同样会破坏构建。况且 CI 对微小变更本身也很快。 |
| "测试只是 flaky，重跑一下" | 不稳定的测试掩盖真实 bug，浪费所有人的时间。务必修复不稳定性。 |
| "以后再加 CI" | 没有 CI 的项目会累积破损的状态。从第一天就搭建好。 |
| "手动测试就够了" | 手动测试不可扩展，也不可重复。能自动化的就自动化。 |

## 危险信号

- 项目中没有 CI 流水线
- CI 失败被忽略或压制
- 在 CI 中禁用测试以让流水线通过
- 不经过预发布验证就直接生产部署
- 没有回滚机制
- 密钥存储在代码或 CI 配置文件中（而非密钥管理工具）
- CI 耗时过长却没有任何优化动作

## 校验

完成 CI 搭建或修改后：

- [ ] 所有质量门禁均已就位（lint、类型、测试、构建、审计）
- [ ] 流水线在每次 PR 与 main 分支推送时都会运行
- [ ] 失败会阻止合并（已配置分支保护）
- [ ] CI 结果会反馈到开发闭环中
- [ ] 密钥存放在密钥管理工具中，而非代码中
- [ ] 部署具备回滚机制
- [ ] 测试套件的流水线在 10 分钟内完成

## 局限

- 仅当任务与上游来源及本地项目上下文明确匹配时才使用本技能。
- 在应用变更前，请校验命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作特定环境测试、安全审查或对破坏性/高成本操作的授权替代。