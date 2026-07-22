---
name: frontend-lighthouse
description: "为生产前端构建添加一个可移植的 Lighthouse CI 质量门，含 Core Web Vitals 预算、类别分数下限、中位数运行与 CI 制品。触发词：Lighthouse CI、性能门、Core Web Vitals、CWV、LCP、CLS、INP、TBT。"
category: frontend
risk: safe
source: community
source_repo: stareezy-1/frontend-architecture-skill
source_type: community
date_added: "2026-06-29"
author: stareezy-1
tags: [frontend, lighthouse, performance, core-web-vitals, ci]
tools: [lighthouse, node, github-actions]
license: "MIT"
license_source: "https://github.com/stareezy-1/frontend-architecture-skill/blob/main/LICENSE"
---

# Frontend Lighthouse（可移植的性能门）

> 可移植技能 —— 可被 Claude Code、OpenCode、Codex、Cursor、Windsurf 等读取。
> 本技能描述的是一个 **CI 性能门** —— 一份 Lighthouse CI 配置加上一条工作流 —— 而不是组件库或视觉样式。它与 **frontend-seo** 和 **frontend-architecture** 技能配合使用：SEO 负责写元数据，Lighthouse 负责证明它加载得足够快。

目标：每个 pull request 都 **被拦截，除非生产构建满足明确的 Core Web Vitals 预算与类别分数下限**。预算集中存放在 **唯一** 的 `lighthouserc.cjs` 中，运行采用 **N 次中位数** 以避免门控抖动，且同一份配置在本地与 CI 中行为一致。

## 何时使用本技能

- 在为 Web 应用添加 Lighthouse CI 性能门时使用。
- 在为 LCP、CLS 与 TBT（作为 INP 的实验室代理）设定 Core Web Vitals 预算时使用。
- 在为 performance、SEO、accessibility、best-practices 配置类别分数下限时使用。
- 在排查 Lighthouse 抖动运行、或将报告以 CI 制品形式对外可见时使用。

---

## 0. 五大核心思想

1. **一份配置，一个真理来源。** 所有预算与断言都集中在单一 `lighthouserc.cjs` 中。每个预算都用具名常量 —— 不要在断言对象里埋魔法数字。
2. **门控生产构建，绝不门控 dev。** Lighthouse 对 `build` + `start`（真实的、已优化的产物）运行。dev 服务器上的数字对预算毫无意义。
3. **N 次中位数消除抖动。** 运行 3 次以上并以中位运行作为断言依据，使单次抖动（冷缓存、CI 噪声）永远不会把一个健康的构建误标为红灯。
4. **预算对应 Google 的"良好"阈值。** LCP ≤ 2500 ms、INP ≤ 200 ms（通过 TBT 实验室代理门控）、CLS ≤ 0.1 —— 这些是能拿到绿色分数的值，不是"有待改进"。
5. **在 CI 中拦截，以制品形式可见。** GitHub Action 在每个触碰应用的 PR 上运行门控并上传 HTML/JSON 报告，让失败可被调试。

---

## 1. 本技能新增的文件

```
apps/web/                          (or your app root)
├── lighthouserc.cjs               ← the gate: budgets + assertions + collect settings
├── package.json                   ← "lhci": "lhci autorun --config=./lighthouserc.cjs"
└── .github/workflows/lighthouse.yml  ← PR-blocking CI job (build → start → lhci → upload)
```

外加一个开发依赖：`@lhci/cli`。

```bash
pnpm add -D @lhci/cli        # or npm i -D / yarn add -D
```

---

## 2. 配置文件（`lighthouserc.cjs`）

使用 `.cjs`（CommonJS），这样无需 ESM/TS 转译即可加载。每个预算都是 **具名常量**，并附有说明阈值的注释 —— 绝不裸露数字。

```js
/**
 * Lighthouse CI configuration — Core Web Vitals budgets for the marketing surface.
 *
 * Enforces Google's mobile "good" CWV thresholds:
 *   - Largest Contentful Paint (LCP) ≤ 2500 ms
 *   - Cumulative Layout Shift (CLS)  ≤ 0.1
 *   - Interaction to Next Paint (INP) ≤ 200 ms
 *
 * INP is a *field* metric with no direct lab audit, so in the lab we gate on
 * Total Blocking Time (TBT) — Lighthouse's recommended lab proxy — at the same
 * budget, and assert the experimental INP audit directly as a warning where the
 * build exposes it.
 *
 * Collection runs against the *production* server (build + start) on Lighthouse's
 * default mobile (Moto G4 / slow 4G) emulation.
 */

/** The fixed port the production server is started on for the audit. */
const PORT = 3100;
const BASE_URL = `http://localhost:${PORT}`;

/** Pages whose budgets are enforced in CI. */
const MARKETING_URLS = [`${BASE_URL}/`];

/**
 * Core Web Vitals budgets on mobile — Google's "good" thresholds.
 * These are the values that earn the best Lighthouse scores.
 */
const LCP_BUDGET_MS = 2500; // good
const INP_BUDGET_MS = 200; // good (TBT lab proxy)
const CLS_BUDGET = 0.1; // good

module.exports = {
  ci: {
    collect: {
      // Build is run separately in CI; here we only serve the production output.
      startServerCommand: `pnpm start --port ${PORT}`,
      startServerReadyPattern: "Ready in", // framework's "server ready" log line
      startServerReadyTimeout: 120000,
      url: MARKETING_URLS,
      // Median of multiple runs keeps the gate stable against per-run jitter.
      numberOfRuns: 3,
      settings: {
        // Default mobile emulation; opt into desktop via env for a second run.
        preset:
          process.env.LHCI_FORM_FACTOR === "desktop" ? "desktop" : undefined,
        // Only gate the categories we care about; skip PWA category noise.
        onlyCategories: [
          "performance",
          "seo",
          "accessibility",
          "best-practices",
        ],
      },
    },
    assert: {
      // Median across runs is the value compared against each budget.
      aggregationMethod: "median-run",
      assertions: {
        // --- Core Web Vitals budgets (the contract) ---------------------
        "largest-contentful-paint": [
          "error",
          { maxNumericValue: LCP_BUDGET_MS },
        ],
        "cumulative-layout-shift": ["error", { maxNumericValue: CLS_BUDGET }],
        "total-blocking-time": ["error", { maxNumericValue: INP_BUDGET_MS }],
        // Direct INP audit where the Lighthouse build exposes it (else ignored).
        "interaction-to-next-paint": [
          "warn",
          { maxNumericValue: INP_BUDGET_MS },
        ],

        // --- Category floors (target top Lighthouse scores) -------------
        "categories:performance": ["error", { minScore: 0.9 }],
        "categories:seo": ["error", { minScore: 0.95 }],
        "categories:accessibility": ["error", { minScore: 0.95 }],
        "categories:best-practices": ["error", { minScore: 0.9 }],
      },
    },
    upload: {
      // Keep reports in the CI run's filesystem; no external LHCI server.
      target: "filesystem",
      outputDir: "./.lighthouseci",
    },
  },
};
```

**硬性规则：**

- 每个预算都是具名常量，名字里带单位（`LCP_BUDGET_MS`），并附注释。
- `aggregationMethod: "median-run"` 不可妥协 —— 单次门控会持续抖动。
- `numberOfRuns` ≥ 3（奇数能得到干净的中位数）。
- 在实验室中以 TBT 断言 INP；将实验性的 `interaction-to-next-paint` 审计视为 `warn` 而非 `error`（它并非在每个 Lighthouse 版本中都存在）。
- 让 `onlyCategories` 严格限定你实际门控的类别 —— 更少的审计、更快、更少噪声。

---

## 3. 选择预算严重度与阈值

| Audit / category            | Severity | Threshold | Why                                                   |
| --------------------------- | -------- | --------- | ----------------------------------------------------- |
| `largest-contentful-paint`  | `error`  | ≤ 2500 ms | Google "good" LCP                                     |
| `cumulative-layout-shift`   | `error`  | ≤ 0.1     | Google "good" CLS                                     |
| `total-blocking-time`       | `error`  | ≤ 200 ms  | INP lab proxy                                         |
| `interaction-to-next-paint` | `warn`   | ≤ 200 ms  | not in all builds; don't hard-fail on a missing audit |
| `categories:performance`    | `error`  | ≥ 0.9     | top (green) band                                      |
| `categories:seo`            | `error`  | ≥ 0.95    | SEO is cheap to keep perfect                          |
| `categories:accessibility`  | `error`  | ≥ 0.95    | a11y regressions must block                           |
| `categories:best-practices` | `error`  | ≥ 0.9     | green band                                            |

对必须成立的契约使用 `error`，对依赖环境或属于愿景性的审计使用 `warn`。**起步要严，只在有书面记录的原因下才放宽** —— 一个你为了过 CI 而不断上调的预算，已经不再保护任何东西。

---

## 4. npm 脚本

```jsonc
// package.json
{
  "scripts": {
    "lhci": "lhci autorun --config=./lighthouserc.cjs"
  }
}
```

`lhci autorun` 会依次执行 `collect` → `assert` → `upload`。在推送前于本地运行，以精确复现 CI 的行为：

```bash
pnpm build && pnpm lhci
# desktop form factor:
LHCI_FORM_FACTOR=desktop pnpm build && LHCI_FORM_FACTOR=desktop pnpm lhci
```

---

## 5. GitHub Actions 工作流

在触碰应用或工作流自身的 PR 上运行。构建生产产物、运行门控，并 **始终** 上传报告（即使失败也照传），以便红灯可被调试。

```yaml
name: Lighthouse CWV

on:
  pull_request:
    branches: [main]
    paths:
      - "apps/web/**"
      - ".github/workflows/lighthouse.yml"

permissions:
  contents: read

jobs:
  lighthouse:
    name: Lighthouse CWV (marketing pages)
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/web
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4 # version comes from root package.json packageManager

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm

      - name: Install dependencies
        working-directory: .
        run: pnpm install --frozen-lockfile

      - name: Build web app
        run: pnpm build

      # build + start the production server, run Lighthouse on mobile emulation,
      # fail the job if any budget in lighthouserc.cjs is exceeded.
      - name: Run Lighthouse CI
        run: pnpm lhci

      - name: Upload Lighthouse reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: lighthouse-reports
          path: apps/web/.lighthouseci
          if-no-files-found: ignore
```

**硬性规则：**

- 触发器同时覆盖应用路径 **和工作流自身** 文件，使配置变更能自测。
- 上传步骤必须配 `if: always()` —— 门控失败时你最需要这份报告。
- 基于 **生产** 构建（先 `pnpm build`，再在 `collect` 中启动 `start` 服务）。
- 让 CI 中 Node/pnpm 版本与仓库锁定的版本一致，避免 lockfile 漂移。

---

## 6. 框架适配器

除 `startServerCommand` 和 `startServerReadyPattern` 外，配置与框架无关。

| Framework     | `startServerCommand`                                              | `startServerReadyPattern`                   |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------- |
| **Next.js**   | `pnpm start --port 3100` (after `next build`)                     | `"Ready in"`                                |
| **Remix**     | `pnpm start` (serve the built app)                                | server's listening log line                 |
| **Astro**     | `node ./dist/server/entry.mjs` (SSR) or `npx serve dist` (static) | the adapter's ready line / serve's URL line |
| **SvelteKit** | `node build` (node adapter)                                       | `"Listening on"`                            |
| **Vite SPA**  | `npx vite preview --port 3100`                                    | `"Local:"`                                  |

对于纯静态产物，你可以跳过服务器，改用 `collect.staticDistDir` 指向构建目录 —— Lighthouse 会自行托管。

---

## 7. 排查失败或抖动的运行

- **LCP/TBT 抖动** → 提升 `numberOfRuns`（如到 5），确认使用 `median-run`，并确认 runner 上没有其他进程抢占 CPU。
- **`interaction-to-next-paint` 报错** → 应为 `warn` 而非 `error`；该审计在某些 Lighthouse 版本中缺失。
- **"server not ready" 超时** → 修正 `startServerReadyPattern` 以匹配框架的实际就绪日志，并提升 `startServerReadyTimeout`。
- **真正的回归** → 打开上传的报告制品，查看失败审计的 "Opportunities"/"Diagnostics"，定位并修复根因（图片过大、阻塞渲染的 JS、未设定尺寸导致的布局抖动）—— 不要直接放宽预算。
- **桌面与移动端差异** → 同时跑两种 form factor；移动端是更严的门，应作为默认。

---

## 8. 约定清单（评审中强制）

- [ ] 所有预算都是具名常量，带单位与注释 —— 断言中无魔法数字。
- [ ] 门控基于 **生产** 构建运行，绝不使用 dev 服务器。
- [ ] `aggregationMethod: "median-run"`，`numberOfRuns` ≥ 3。
- [ ] CWV 预算采用 Google "良好" 阈值（LCP ≤ 2500、TBT ≤ 200、CLS ≤ 0.1）。
- [ ] 通过 TBT 门控 INP（`error`）；实验性 INP 审计为 `warn`。
- [ ] 类别分数下限设为 `error`（perf ≥ 0.9，SEO/a11y ≥ 0.95，best-practices ≥ 0.9）。
- [ ] `onlyCategories` 严格列出门控的类别。
- [ ] CI 同时基于应用路径 **和工作流文件** 触发；报告以 `if: always()` 上传。
- [ ] 本地 `pnpm lhci` 能复现 CI 运行。
- [ ] 预算随时间收紧，仅在有书面原因时才放宽。

---

## 9. 如何应用本技能

**为项目添加门控：** 安装 `@lhci/cli`，放入一份带你的 URL 与 `startServerCommand` 的 `lighthouserc.cjs`，添加 `lhci` 脚本和工作流。先在本地执行 `pnpm build && pnpm lhci` 确认通过，再发起 PR。

**为门控新增页面：** 把对应 URL 追加到 `MARKETING_URLS`（或第二个 URL 数组）。每个 URL 都会独立按同一套预算进行审计。

**调优预算：** 改具名常量，不要改断言。在注释中记录原因。优先修复回归，而非上调预算。

**评审性能：** 按 §8 的清单走一遍。最高价值的发现是基于 dev 服务器运行的门控（数字无意义）和单次断言（长期抖动）。

---

## 发布 / 安装本技能

本技能遵循 Anthropic 的 `SKILL.md` 格式，可在多 Agent 间移植。

1. 将其放在公开 GitHub 仓库的 `skills/frontend-lighthouse/SKILL.md` 下。
2. 保留 frontmatter 的 `name` 与高信号的 `description` —— 发现索引会匹配它们。
3. 安装方式：`npx skills add <org>/<repo> --skill "frontend-lighthouse"`。
4. 非 `SKILL.md` 的 Agent 可通过 `AGENTS.md` / `CLAUDE.md` 指向本技能；Kiro 可将其镜像为 steering 文件。

## 局限性

- Lighthouse CI 是实验室信号，无法替代来自真实用户指标的业务侧监控。
- 预算必须结合实际的应用路由、托管平台与设备/网络假设来调优。
- 通过 Lighthouse 门控并不意味着业务关键流程、视觉正确性或后端可用性已得到验证。