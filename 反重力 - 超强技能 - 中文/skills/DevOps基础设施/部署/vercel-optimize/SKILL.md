---
name: vercel-optimize
description: "使用指标、项目配置、代码扫描和版本感知建议，审计已部署的 Vercel 应用的成本与性能问题。"
risk: safe
source: "https://github.com/vercel-labs/agent-skills"
date_added: "2026-06-02"
---

# Vercel Optimize

运行一次以可观测性为先的 Vercel 优化审计。在 `signals.json` 存在、且确定性闸门指向某个路由、文件或项目设置之前，不要检查源文件。

核心原则：若任何规则不清楚，请阅读 [references/doctrine.md](references/doctrine.md)。

- 指标优先。建议从 Vercel 生产信号出发，而不是全仓库 grep。
- 确定性闸门。`scripts/gate-investigations.mjs` 决定哪些值得调查。
- 候选绑定范围。只读取由候选或路由本地导入链命名的文件。
- 版本感知引用。仅使用 `references/docs-library.json`；无效或版本不匹配的引用会被剥离。
- 客户文案。在撰写报告文本或聊天输出之前，请阅读 [references/voice.md](references/voice.md)。

## 适用场景
- 当任务与以下描述匹配时使用此技能：使用指标、项目配置、代码扫描和版本感知建议，审计已部署的 Vercel 应用的成本与性能问题。

## 前置条件

- Vercel CLI v53+，包含 `vercel metrics`、`vercel usage`、`vercel contract` 和 `vercel api`。
- 已认证的 CLI 会话：`vercel login`。
- 已链接的应用目录：`vercel link`。`VERCEL_PROJECT_ID` 可帮助解析项目配置，但 `vercel metrics` 仍要求目录已链接。该链接或环境必须包含预期的项目 org/team/user 范围，以便收集器能解析一个 CLI 安全的 `--scope`，并让 `vercel metrics`、`vercel usage` 和 `vercel contract` 保持在同一账户下。
- Node.js 20+。
- 用于路由级指标支持建议的 Observability Plus。

绝不要将认证令牌放入 shell 命令中。不要在可能被回显到聊天里的命令中键入 `VERCEL_TOKEN=...`、`--token ...` 或 `Authorization: Bearer ...`。

## 框架支持

预检会读取 `package.json` 并在指标展开之前设置期望。

| 框架 | 状态 | 备注 |
|---|---|---|
| Next.js App Router | supported | 最强的路由映射、扫描器、剧本和引用 |
| Next.js Pages Router | supported | 限定为 Pages Router 习惯用法（检测时） |
| SvelteKit | supported | `src/routes` 文件的路由映射与 SvelteKit 扫描器 |
| Nuxt | supported | 路由映射加通用/平台检查；框架特定建议较少 |
| Astro | limited | 路由映射加通用检查；框架特定建议较少 |
| Hono / Remix / unknown | blocked by default | 仅当用户接受有限的平台/仅代码审计时才继续 |

如果不支持，则停止并在扫描或分流之前询问：

```text
This project uses <framework>. Vercel Optimize supports metric-backed code recommendations for Next.js, SvelteKit, and Nuxt. Astro support is limited. For <framework>, I can still run a limited platform/scanner audit, but route-level Vercel metrics may not map back to source files.

Do you want me to continue with the limited audit, or stop here?
```

如果用户选择继续，使用 `--continue-unsupported-framework` 重新运行收集。

## 运行目录

每次审计都使用全新的运行目录。不要跨运行复用简报、子代理输出或报告。

```bash
RUN_DIR="$(mktemp -d -t vercel-optimize-XXXXXX)"
```

## 流水线

### 1. 收集、扫描与合并信号

从已链接的应用目录运行，或在脚本支持时传入 `--cwd`。将 stdout JSON 与 stderr 日志分开保存。不要合并流。

```bash
node scripts/collect-signals.mjs [projectId] > "$RUN_DIR/vercel-signals.json" 2> "$RUN_DIR/collect.stderr"
node -e 'JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"))' "$RUN_DIR/vercel-signals.json"

node scripts/scan-codebase.mjs <repo-root> > "$RUN_DIR/codebase.json"
node scripts/merge-signals.mjs "$RUN_DIR/vercel-signals.json" "$RUN_DIR/codebase.json" --out "$RUN_DIR/signals.json"
```

收集细节、schema、指标 ID 与降级行为见 [references/data-collection.md](references/data-collection.md)。指标注册表位于 [lib/queries.mjs](lib/queries.mjs)；所有查询保持共享的 14 天窗口。

`collect-signals.mjs` 将已链接项目的所有者解析为 `commandScope.cliScope`，并在检查 Observability Plus 之前验证解析后的账户能否读取解析后的项目。下游脚本对每个接受 `--scope` 的 Vercel CLI 命令复用此 scope。不要在没有相同 scope 的情况下手动运行 `vercel usage`、`vercel metrics` 或 `vercel contract`；未限定的 usage 可能报告用户的个人组织，而路由指标来自团队项目。

如果项目或 scope 解析存在歧义，停止并询问用户希望审计哪个 Vercel 项目和团队/个人 scope。不要从当前的 `vercel whoami` 团队推断预期 scope；在链接、在 `.vercel/repo.json` 中精确匹配项目，或使用 `VERCEL_PROJECT_ID` + `VERCEL_ORG_ID` 标识预期账户之前，不要继续进行指标、usage 或合同收集。

对 `PROJECT_SCOPE_UNRESOLVED`、`SCOPE_UNRESOLVED` 或 `PROJECT_SCOPE_MISMATCH` 使用此提示：

```text
I can't safely identify the Vercel project and account for this audit yet.

Please confirm the Vercel project name or ID and the team slug/name, or tell me it's under your personal account. Once confirmed, I'll relink or rerun collection against that exact scope before checking metrics.
```

### 1.1 遇到阻塞即停止

在分流之前检查阻塞：

```bash
jq '{frameworkSupportBlocker, observabilityPlus, observabilityPlusUsable, observabilityPlusBlocker, observabilityPlusBlockerDetail}' "$RUN_DIR/signals.json"
```

所需动作：

- `frameworkSupportBlocker === "unsupported_framework"`：使用上面的不支持框架提示。
- `PROJECT_SCOPE_UNRESOLVED`、`SCOPE_UNRESOLVED` 或 `PROJECT_SCOPE_MISMATCH`：停止并询问用户希望审计哪个 Vercel 项目和团队/个人 scope。对于团队项目，在 `vercel link --yes --project <project-name-or-id> --team <team-slug>` 后重新运行；对于个人项目，在预期用户账户下重新链接或同时设置 `VERCEL_PROJECT_ID` 和 `VERCEL_ORG_ID` 后重新运行。
- `observabilityPlusBlocker === null`：继续。
- `no_traffic`：告诉用户路由指标很稀疏；只有在用户接受有限输出时才继续。
- `payment_required` 或 `no_oplus_probe`：逐字渲染 [references/observability-plus.md](references/observability-plus.md) 并询问。
- `project_disabled`：告诉用户为该项目启用 Observability Plus 或接受有限审计。
- `daily_quota_exceeded`：停止并告诉用户 Observability 查询配额已用尽；在下一个 UTC 午夜重置后重试，或询问是否继续有限的仅代码审计。
- `not_linked`：链接应用目录，然后重跑第 1 步。如果应用路径和项目已知：

```bash
vercel link --yes --project <project-name-or-id> --cwd <app-dir>
# add --team <team-id-or-slug> when known
```

- `forbidden` 或 `project_not_found`：修复认证/团队 scope。不要推销 Observability Plus。
- `all_failed_other`：显示原始错误代码并询问是否继续仅代码模式。

不要静默回退到仅代码模式。如果用户接受有限审计，使用以下命令重新运行收集：

```bash
node scripts/collect-signals.mjs [projectId] --continue-without-observability > "$RUN_DIR/vercel-signals.json" 2> "$RUN_DIR/collect.stderr"
```

然后再次扫描和合并。

### 2. 候选分流

```bash
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" > "$RUN_DIR/gate.json"
```

输出结构：

- `toLaunch`：待调查的代码范围候选。
- `platform`：项目/账户范围的建议。
- `gated`：跳过、已覆盖或不合格的候选，仍需出现在报告中。
- `budget`：候选预算与选择模式。

默认预算是 6 个代码范围候选，并配有多样性保护。要扩大预算：

```bash
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" --max-candidates 12 > "$RUN_DIR/gate.json"
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" --max-candidates all > "$RUN_DIR/gate.json"
```

生成的候选文档：[references/candidates.md](references/candidates.md)。

### 2.1 必要时询问审计范围

在深入调查之前，运行：

```bash
node scripts/budget-summary.mjs "$RUN_DIR/gate.json" --format json > "$RUN_DIR/budget-summary.json"
```

如果 `shouldAsk` 为 false，继续。

如果 `shouldAsk` 为 true：

1. 按返回值原样打印 `exactChatMessage.body`。不要总结、截断、重排或重写。
2. 然后当宿主支持结构化问题时，用 `questionPayload` 询问 `questionText`。
3. 如果用户选择了不同数量，使用 `--max-candidates <choice>` 重新运行分流。

切勿将长预览放进问题字段。预览和问题分属不同界面。

### 2.2 深入调查与协调

```bash
node scripts/deep-dive.mjs "$RUN_DIR/signals.json" "$RUN_DIR/gate.json" --cwd <project-dir> > "$RUN_DIR/investigation-evidence.json"

node scripts/reconcile-candidates.mjs "$RUN_DIR/investigation-evidence.json" \
  --gate "$RUN_DIR/gate.json" \
  --out "$RUN_DIR/reconciled-investigation.json"
```

`--cwd` 必须是已链接的项目目录，以便 `deep-dive.mjs` 验证同一项目链接，并复用 `signals.json.commandScope.cliScope` 进行后续任何 `vercel metrics` 调用。

协调会在任何源调查之前，将被驳倒的候选确定性转换为观察项：

- `metric_mismatch`
- `error_storm`
- `deployment_regression`
- `scanner_only_no_metric`

### 2.3 生成简报并调查

列出工作：

```bash
node scripts/prepare-investigation-brief.mjs "$RUN_DIR/signals.json" "$RUN_DIR/reconciled-investigation.json" --list > "$RUN_DIR/briefs-manifest.json"
```

为 `briefs-manifest.json.briefs` 中的每个条目生成一个简报。`group` 可以是 `toLaunch` 或 `platform`；不要只生成 `toLaunch` 简报。

```bash
mkdir -p "$RUN_DIR/briefs" "$RUN_DIR/sub-agent-outputs"
node scripts/prepare-investigation-brief.mjs "$RUN_DIR/signals.json" "$RUN_DIR/reconciled-investigation.json" \
  --group <brief.group> --index <brief.index> --out "$RUN_DIR/briefs/<brief.group>-<brief.index>.md"
```

对可见的 worker 名称使用 `briefs-manifest.json.briefs[].label`，例如 `Low cache-hit route on /docs/llm-digest/[...slug]`，而不是 `toLaunch-7`。

扇出规则：

- 1-2 个简报：内联调查。
- 3+ 个简报：当宿主支持时，每个简报生成一个子代理。
- 不支持子代理的宿主：内联串行运行。

子代理契约：

- 简报就是全部提示词。
- 只读取简报中列出的文件，以及需要的路由本地导入。
- 使用 [references/recommendations.md](references/recommendations.md) 输出一条 JSON 建议或一条 JSON "无改动" 发现。
- 不要引用所提供引用子集之外的 URL。
- 不要推荐在检测到的版本中不可用的框架功能。

如果子代理试图进行全仓库 grep，则该候选格式错误；丢弃或弃权，而不是扩大范围。

### 2.4 收集输出

将每个原始调查结果保存到 `$RUN_DIR/sub-agent-outputs/`，然后收集：

```bash
node scripts/collect-sub-agent-outputs.mjs \
  --manifest "$RUN_DIR/briefs-manifest.json" \
  --out "$RUN_DIR/recommendations.json" \
  "$RUN_DIR/sub-agent-outputs/"
```

收集器提取 JSON、添加已预先解析的记录、强制清单顺序，并在缺失、重复、未知或 `candidateRef` 不匹配时失败。

### 3. 验证建议

```bash
node scripts/verify-and-regen.mjs "$RUN_DIR/recommendations.json" \
  --signals "$RUN_DIR/signals.json" \
  --repo-root <project-dir> \
  --out "$RUN_DIR/verify.json"
```

该脚本提取声明、验证文件/引用/版本匹配、评定质量、应用清理器、发出 `verifiedRecommendations`、`withheldRecommendations`、`renderableRecommendations`，并为失败或不安全的建议创建 `regenPlan`。

建议 schema、编写规则、清理器顺序与评分规则：[references/recommendations.md](references/recommendations.md)。验证规则：[references/verification.md](references/verification.md)。

对每个 `regenPlan` 条目，使用包含 `topFailures` 列表的 `Previous attempt failed these checks` 部分重跑相同简报。仅当验证改善且未大幅削减引用时，才保留重新生成的输出。

### 4. 渲染报告与最终消息

```bash
node scripts/render-report.mjs "$RUN_DIR/verify.json" "$RUN_DIR/gate.json" "$RUN_DIR/signals.json" \
  --project <name> \
  --out "$RUN_DIR/report.md" \
  --message-out "$RUN_DIR/final-message.json"
```

仅在开发本技能时使用 `--debug-out "$RUN_DIR/debug.json"`。客户 Markdown 与聊天输出不得暴露 `passRate`、`quality`、清理器跟踪、原始子代理名称或其他实现字段。

渲染后，按字面打印 `final-message.json.body` 并停止。不要添加高亮、调试说明、原始计数、子代理摘要或额外解释。渲染时的去重、平台上限与硬安全丢弃会改变面向客户的计数，因此切勿从原始 `verify.json` 进行总结。

报告结构与影响框架：[references/scoring.md](references/scoring.md)。

## 建议规则

每条建议都必须：

- 追溯到某个已启动的候选、平台候选、预先解析的观察项，或经过验证的与流量无关的扫描器发现。
- 包含来自 `signals.json` 或 `evidence.deepDive` 的可观察指标证据。
- 在涉及代码时，引用带行号的已验证文件。
- 至少包含一条适用于检测到的框架/版本的有效引用。
- 使用精确的可观察性能数字。
- 仅使用成本量级短语；永远不要面向客户写 `$N` 节省。
- 不要对 Vercel Workflow 运行时端点（`/.well-known/workflow/v1/*`）建议缩短时长。这些是为持久步骤/流执行生成的编排路由，应在调查之前硬性屏蔽。
- Workflow 建议必须命名正在变更的边界。有效示例：入队持久工作并返回运行 ID 而不是等待完成、修复流重放/关闭/锁，或减少已验证的多余 Workflow 步骤/存储。不要从 Workflow 端点的墙钟时长推断成本节省。
- 对于流式、SSE、可恢复聊天或其他有意长生命周期的路由，不要将墙钟函数时长本身当作问题。需要有可避免的首字节前工作、高活跃 CPU、重复调用或可移出用户可见路径的响应后工作的证据。
- 在建议缓存时，指定具体的缓存策略。
- 除非证据证明它们可安全缓存，否则保持不安全响应为动态：鉴权敏感路径、错误、回退响应、缺失内容、无效请求、地理位置/设备变化的输出，以及未版本化的动态 URL。

切勿为 `signals.project` 中已经存在的事实（如 Fluid compute 状态、内存层、区域、函数内并发、超时）建议"确认 X 是否已开启"。

## 扫描器规则

扫描器发现是补充性的。除非扫描器声明 `metadata.trafficIndependent === true`，否则丢弃标记为 `COLD-PATH` 或 `NO-ROUTE-MAPPING` 的发现。

与流量无关的示例：middleware matcher、source maps、React Compiler 配置、构建设置。路由本地缓存或数据获取模式需要路由级流量证据。

扫描器文档：[references/scanner-patterns.md](references/scanner-patterns.md)。

## 面向客户的最终术语

使用：

- `recommendations ready`
- `observations from investigation`
- `investigated, no change recommended`
- `not investigated in this run`

避免：

- `sub-agent`
- `abstention`
- `passRate`
- `quality score`
- `gate`
- `LLM`

## 失败文案

请使用以下消息，不要添加销售文案或流程细节。

**过去 14 天无流量：**

> This project has no meaningful traffic in the last 14 days, so route-level metrics are sparse. I can still check traffic-independent scanner findings and project settings, but I cannot rank route fixes until traffic accumulates.

**路由级指标不可用：**

> Use the verbatim choice template in [references/observability-plus.md](references/observability-plus.md). Do not silently fall back to code-only mode; present the two-path choice: enable Observability Plus and rerun the metric-backed audit, or accept a limited code-only run.

**项目未链接：**

> This worktree is not linked to a Vercel project. Run `vercel link --yes --project <project-name-or-id> --cwd <app-dir>` and rerun the audit. If the team is known, add `--team <team-id-or-slug>`.

**大多数路由到文件的映射失败：**

> The route inventory matched fewer than half of the routes we saw in observability. This is common in monorepos with custom routing. I've surfaced what I can match; the rest appear in the "Not investigated in this run" section.

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果必需的输入、权限、安全边界或成功标准缺失，请停止并请求澄清。