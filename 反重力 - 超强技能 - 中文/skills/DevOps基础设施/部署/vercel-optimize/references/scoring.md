## 第 4 步 — 评分与报告

本参考涵盖了建议草拟之后的所有内容：质量底线、影响框架、排序顺序、面向客户的报告模板以及剧本选择矩阵。

## 目录

- [Quality floor and prune rules](#quality-floor-and-prune-rules)
- [Impact framing — the magnitude rule](#impact-framing--the-magnitude-rule)
- [`impactLabel` schema](#impactlabel-schema)
- [Sort order and platform-rec cap](#sort-order-and-platform-rec-cap)
- [The customer-facing report template](#the-customer-facing-report-template)
- [Playbook selection matrix](#playbook-selection-matrix)

## 质量底线与裁剪规则

| 规则 | 值 | 原因 |
|---|---|---|
| 丢弃 `quality.overall < 0.55` 的建议 | 硬截止（自 2026 年 5 月审计从 0.4 提高） | 差等级的建议侵蚀信任的速度快于它们带来的帮助。0.55 对应 Poor/Fair 等级边界；低于此的建议是"Poor"，不应发布。 |
| 发现项的裁剪上限 | 输入的 30% | 当 LLM 价值评分噪声大时，阻止裁剪器擦除整个报告 |
| 平台建议上限 | 3 | 账户级建议（Fluid、Bot Protection、Speed Insights）只为前三名留出空间 |
| Quick-wins 定义 | `effort === 'low' AND priority > 40` | 浮现用户能在单个 PR 中发布的修复 |
| 节省下限（仅内部排序） | $5/月等价值 | 低于此，即使"高"层级影响也意味着"negligible"量级 |

## 影响框架 — 量级规则

**性能：精确。** 使用观察到的数字。例如：

> "Reduce /api/products p95 from 850ms toward ~250-400ms; cache hit would lift from 0% toward ~60% based on similar cached routes."

性能数字来自 `signals.json.metrics.*`——它们是被观察到的，不是外推的。引用精确路由 + 指标值。

**美元成本：永远不精确。** 通过 `lib/impact-magnitude.mjs` 的 `impactMagnitude({currentCost, impactTier})` 使用量级桶：

| 估算削减（美元） | 量级 | 面向客户的短语 |
|---|---|---|
| < $5 | `negligible` | "small cost impact at current traffic" |
| $5 – $50 | `small` | "low-tens of dollars per month at current traffic" |
| $50 – $500 | `medium` | "hundreds of dollars per month at current traffic" |
| $500 – $5,000 | `large` | "low-thousands of dollars per month at current traffic" |
| > $5,000 | `very-large` | "thousands+ of dollars per month at current traffic" |

削减按 `currentCost × fraction` 计算，其中 `fraction = {high: 0.4, medium: 0.2, low: 0.1}[impactTier]`。该分数刻意保守——我们宁愿保守承诺也不误导。

### 可折扣 vs 不可折扣 SKU

当项目在 Flex Commit 上、报告针对合同消耗框定节省时，请在措辞前对支出分段。现场原则（2026 年 5 月）：Flex 折扣滑块仅适用于一部分 SKU。

| 可折扣（滑块适用） | 不可折扣（原始费率） |
|---|---|
| Seats | Build CPU Minutes |
| Edge Requests | Fluid Active CPU |
| Fast Data Transfer | Fluid Provisioned Memory |
| Fast Origin Transfer | Raw Flex top-up |
| Image Optimization | |
| ISR Reads / Writes | |
| Observability Events | |

针对不可折扣 SKU 的建议绝不应将节省框定为合同百分比；仅框定为绝对量级。相反，可折扣 SKU 的建议可以在量级短语中浮现"applies to contract burndown"。

**为什么用量级：**

- 流量变化。"edge requests 减少 20%"在今天的流量下精确，下一季度就毫无意义。
- 定价变化。Vercel 的计费费率会变化；精确的美元投影会腐烂。
- 用户很聪明。他们宁愿看到带有真实指标支撑的"每月数百美元"，也不愿看到背后是含糊其辞的 `$340/mo`。
- `$-strip` 清理器在输出时强制执行此规则。任何混入面向客户字段的 `$N` 字面量，在渲染之前都被替换为 "the billed cost"。

## `impactLabel` schema

```ts
type ImpactLabel = {
  // PRECISE: performance recs
  performance?: string;
  // MAGNITUDE: cost recs
  costMagnitude?: 'negligible' | 'small' | 'medium' | 'large' | 'very-large';
  costPhrase?: string;
  billingDimension?: string;   // 'Edge Requests' | 'Function Duration' | ...
  fractionReduced?: number;    // 0.2 = ~20% — internal only, NOT rendered
};
```

成本建议渲染 `costPhrase`。性能建议渲染 `performance`。可靠性建议将影响框定为观察到的错误/超时减少（例如，"Cuts 5xx rate from 0.4% to <0.1% based on current traffic"）。

当一条建议跨越桶——例如同时降低成本和延迟的缓存修复——渲染两行。

## 排序顺序与平台建议上限

内部排序键（从不渲染）：`priority = currentDimensionCost × fractionReduced × confidence`。

客户看到的建议列表按此优先级排序。平台建议部分的上限为 3，按相同方式排序。

## 面向客户的报告模板

代理将其渲染为第 4 步的最终输出。形状是固定的；内容来自合并的信号 + 已验证的建议 + 来自第 2 步的 `gated[]` 列表。

```markdown
# Vercel Optimization Report — {projectName}

**Stack**: {framework}@{frameworkVersion} | {router} | {orm}
**Plan**: {plan.plan} ({plan.reason})
**Period**: {usage.period.from} → {usage.period.to}
**Observability**: {observability status}

## Cost breakdown

| Service | Usage | Billed Cost |
|---|---|---|
| (non-zero rows from usage.services, sorted by billedCost desc) |

Total billed: {usage.totals.billedCost} (we render the precise current cost — we just don't project future precise savings)

Omit zero-cost service rows from the table at the same cent precision shown to customers. If every row has `$0.00` billed cost but `effectiveCost` / USD `pricingQuantity` is non-zero, explain that net billed cost is `$0.00` after included credits or allotments and show the effective usage cost table instead. If both billed and effective costs are `$0.00`, replace the table with a concise note that `vercel usage` returned a billing payload but every reported service cost was `$0.00` for the window.

If `vercel usage` was queried and unavailable, the cost breakdown is replaced by an observability-derived cost ranking from `metrics.fnGbHrByRoute` + `metrics.fnCpuMsByRoute` + `metrics.fdtByRoute` when those metrics exist. These don't translate directly to dollars — they show *which routes consume the billable units* so the user knows what to attack first. If `usageError` is `NOT_COLLECTED_OBSERVABILITY_BLOCKED` or another `NOT_COLLECTED_*` value, say usage was not collected; do not describe it as a billing-plan or Costs-feature finding.

Render Observability status from the actual collection state:
- `Observability Plus enabled — per-route metrics included` when `observabilityPlusUsable=true`.
- `Per-route metrics unavailable — audit paused before metric-backed route ranking` when an Observability Plus blocker stopped the run before billing/scanner collection.
- `Per-route metrics unavailable — analysis based on billing + scanner findings` when the user accepted a limited audit and billing/scanner signals were collected.
- `Per-route metrics unavailable — limited analysis based on scanner findings` when the user accepted a limited audit but billing usage was queried and unavailable.
- `Not checked — audit paused at unsupported-framework preflight` when framework support stopped the run before the Observability Plus check.
- `Not enabled — analysis based on billing + scanner findings` only for legacy/limited reports where Observability Plus is known false and billing/scanner signals exist.

## Highest-impact recommendations

For each high-priority rec, in order:
1. **{route or file}** — {o11ySignal}
1. **{readable candidate label}** — {readable metric labels}
   - **What to do**: {rec.what}
   - **Impact**: {impactLabel.performance ?? impactLabel.costPhrase}
   - **Effort**: {rec.effort}
   - **Citations**: {rec.citations}

## Recommendations

### High impact

| # | Bucket | What | Impact | Effort | Citations |
|---|---|---|---|---|---|

### Medium impact
### Low impact

## Platform recommendations

(account-level recs from gate, capped at 3)

## Observations from investigation

Non-recommendation findings from reconciliation or investigation: deployment regressions, route-error storms, metric mismatches, and other real signals that should not become speculative performance recommendations.

Observations must not contain implementation-grade actions. If the suggested action says to enable, add, wrap, apply, move, configure, challenge, deny, or otherwise change code or project settings, the renderer must hold it back until it passes the ready-to-apply recommendation evidence bar. Customer-visible observations can ask for narrower evidence collection: inspect logs, compare deployments, check headers, or confirm cacheability.

## Investigated, no change recommended

Candidates that were checked but did not produce a supported recommendation. Use plain reasons; do not use "abstain" in customer-facing copy.

| Candidate | Why no recommendation shipped |
|---|---|
| Slow route on /docs | Detailed metrics did not support a code change |

## Not investigated in this run

This section earns the user's trust. For every metric signal we considered but didn't act on, group by candidate type and reason:

| Candidate type | Why not investigated | Targets | Count |
|---|---|---|---:|
| Low cache-hit route | hitRate 0.65 above threshold | /api/orders | 1 |
| Slow route | left for a larger run | /api/docs<br>/api/learn | 2 |

## Strengths

(what the project is doing right — caching is healthy on routes X/Y/Z; Fluid Compute is enabled; etc.)

## Data gaps

(what we couldn't measure — Observability Plus disabled means no per-route latency, etc.)
```

Common data gaps to call out when the underlying metric returned empty rows. If the metric query failed (`ok=false`), say the metric was not usable with the code; do not convert failed queries into "no measurements" or "not used" claims.

- **Core Web Vitals empty.** The Speed Insights metric returned no measurements for the 14-day window. The `cwv_poor` gate stayed dormant; no claims about LCP/INP/CLS are made.
- **ISR empty.** Project doesn't use Incremental Static Regeneration. The `isr_overrevalidation` gate stayed dormant.
- **Middleware empty.** No `middleware.ts` (or matcher excludes all observed traffic). The `middleware_heavy` gate stayed dormant.
- **Image transformations empty.** No `next/image` usage or no images served in the window.
- **BotID checks empty.** BotID is disabled — see the `platform_bot_protection` recommendation for the toggle.
- **Cold-start data near-zero.** Fluid Compute may already be enabled, or the project's traffic pattern keeps warm instances available; the `cold_start` gate evaluates the data but emits no candidate.

The "Not investigated in this run" section is critical. It comes directly from `gate.json` produced by the gate. It tells the user we considered everything; we didn't just pick the easy targets.

## 剧本选择矩阵

推荐器根据项目的 `stack.applicationProfile`（从框架 + 依赖推断）和顶部计费维度选择 0-2 个剧本。

| 应用画像 | 可能的顶部维度 | 应用剧本 |
|---|---|---|
| `ai-application`（AI SDK、AI Gateway、Sandbox 使用） | AI Gateway、Sandbox Active Compute、Function Duration | `playbooks/ai-application.md` |
| `ecommerce`（Stripe、Shopify、购物车组件） | Edge Requests、Function Duration | `playbooks/ecommerce.md` |
| `saas`（鉴权、仪表板、多租户） | Function Duration、Bandwidth | `playbooks/saas.md` |
| `api-service`（大部分是 API 路由，没有 UI） | Function Duration、Edge Requests | `playbooks/api-service.md` |
| `content-site`（博客、文档、大部分静态） | Edge Requests、Image Optimization | `playbooks/content-site.md` |
| `marketing`（落地页、A/B 测试） | Edge Requests、ISR Reads | `playbooks/marketing.md` |

`ai-application` 在 `inferPlaybook()` 中首先检查——AI 重的客户常常与 SaaS/ecommerce 表面共享路由，但成本杠杆（AI Gateway 主导）和修复集合（提供者故障转移、sandbox 复用、OIDC 无密钥）属于该画像。

剧本塑造建议的措辞和排序。它们从不捏造声明——每条建议仍必须追溯到已验证的发现。
