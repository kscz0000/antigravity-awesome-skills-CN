# 建议

建议如何成形、编写、清理和评分。

## 目录

- [Schema](#schema)
- [Writing rules](#writing-rules)
- [The 12 sanitizers](#the-12-sanitizers)
- [Envelope-unwrap recovery](#envelope-unwrap-recovery)
- [Grading rubric](#grading-rubric)
- [Next.js version awareness](#nextjs-version-awareness)

## Schema

每条建议都是一个匹配以下 TypeScript 结构的 JSON 对象：

```ts
interface Recommendation {
  // Customer-facing
  what: string;              // 1 line, lead with impact. Max 80 chars when feasible.
  why: string;               // 1-2 sentences. Root cause. Cites codebase findings + counts.
  fix: string;               // Step-by-step. Includes before/after code fences. Specific enough to implement.
  bucket: 'cost' | 'performance' | 'reliability';
  effort: 'low' | 'medium' | 'high';
  affectedFiles: string[];   // Verified file paths, from candidate.files
  currentBehavior: string;   // What the code does now (with snippet)
  desiredBehavior: string;   // Target state (with snippet)
  risk?: string;             // Optional: e.g., "Removing force-dynamic may serve stale data on /admin"
  verify: string;            // How to confirm the fix worked. e.g., "Re-run `vercel metrics …` and watch p95"

  // Impact (computed from impact-magnitude.mjs in Step 4)
  impactLabel: {
    performance?: string;    // PRECISE: "Reduce /api/products p95 from 850ms toward ~250-400ms"
    costMagnitude?: 'negligible' | 'small' | 'medium' | 'large' | 'very-large';
    costPhrase?: string;     // "hundreds of dollars per month at current traffic"
    billingDimension?: string;
    fractionReduced?: number;
  };
  impactTier: 'high' | 'medium' | 'low';
  billingDimension?: 'edge-requests' | 'function-duration' | 'image-optimization' | 'isr-reads' | 'isr-writes' | 'bandwidth' | 'data-cache-reads' | 'cron-invocations' | string;

  // Grounding
  citations: string[];       // From references/docs-library.json allow-list. Required: ≥1 entry.
  candidateRef?: string;     // The gate candidate this rec traces to (e.g., "uncached_route:/api/products")
  findingRefs?: string[];    // File:line markers from verifiedFindings.json
  appliesAlsoTo?: Array<{     // Added by dedup when matching recs collapse into one customer-facing item.
    candidateRef?: string;
    affectedFiles?: string[];
    o11ySignal?: string;
    what?: string;
  }>;
  corroborationCount?: number; // Number of matching verified recs folded into this item, including itself.

  // Verifier output (computed in Step 3.6)
  verification?: {
    passRate: number;
    failed: Array<{ type: string; text: string; reason: string }>;
  };

  // Sanitizer audit trail (computed in Step 3.4)
  sanitizerTrail?: string[]; // ["$-strip:2", "version-mismatch:next@15+:1", ...]
  needsReview?: boolean;     // Set when a sanitizer caught a hazard

  // Grading (Step 3.5)
  quality: {
    specificity: number;     // 0-1
    actionability: number;
    grounding: number;
    evidence: number;
    overall: number;
    grade: 'Excellent' | 'Good' | 'Fair' | 'Poor';
  };
}
```

## 编写规则

推荐器提示词明确告知代理遵循这些规则。清理器在生成之后强制执行它们。

**语音与语气**由 [`references/voice.md`](./voice.md) 约束。在编写建议文本之前阅读它；它使报告保持直接、以指标为基础，并避免内部流程术语。

### 以影响开头

`what` 字段以动词 + 改动开头，而不是框定。对比：

- ❌ "Consider enabling caching on the /api/products route"（实质之前的填充）
- ✅ "Add Cache-Control with s-maxage to /api/products"（动词优先，范围明确）

### 用行号引用代码库发现

`why` 必须引用 `verifiedFindings.json` 中已验证的发现：

- ❌ "The route is uncached"（可能适用于任何地方）
- ✅ "src/app/api/products/route.ts:22 returns Response without Cache-Control; observability shows 0% cache hit on 1.2M invocations/mo"

### 面向客户字段中不含 $ 字面量

用户强制规则。`what`/`why`/`fix`/`impact`/`currentBehavior`/`desiredBehavior` 不得包含 `$N` 货币字面量。使用 `impact-magnitude.mjs` 中的量级框架。

- ❌ "Save $340/mo by adding s-maxage"
- ✅ "Hundreds of dollars per month at current traffic"
- ✅ （精确性能）"Move 1.2M monthly invocations to the CDN; expect p95 to drop from 850ms toward ~50ms on cache hits"

`$-strip` 清理器在输出时强制执行此规则，但提示词也应指示 LLM 一开始就不要发出美元字面量。

### 必须有 before/after 代码围栏

`currentBehavior` 显示有问题的片段。`desiredBehavior` 显示目标。语言标记的代码围栏。两者均保持在约 20 行以内。

### 至少引用库中的一个 URL

`citations[]` 必须至少包含 `references/docs-library.json` 中的一条。`missing-citation` 清理器丢弃未引用的建议。`unknown-citation` 和 `version-mismatch` 清理器剥离无效引用。

### 匹配用户的框架版本

不要向 Next 13 用户推荐 `'use cache'`（Next 15+）。推荐器提示词只接收用户栈有效的引用子集——但 LLM 仍可能产生幻觉。`version-mismatch` 清理器捕获漏网之鱼。

## 12 个清理器

每个清理器在变更字段时将其动作记录到 `rec.sanitizerTrail` 中。标签格式：`tag:detail`。标签在词法上是稳定的——下游消费者按 grep 使用它们。

| # | 清理器 | 触发 | 动作 | 跟踪标签 |
|---|---|---|---|---|
| 1 | `$-strip` | 面向客户字段中的货币字面量正则 | 替换为 "the billed cost" | `$-strip:N` |
| 2 | `vercel-directive-strip` | cache-control 中的 `stale-if-error` / `proxy-revalidate` | 剥离指令（Vercel CDN 不识别） | `vercel-directive-strip:directive` |
| 3 | `rate-limit` | 并发 × 延迟 > 已知的提供者速率限制 | 预先添加 caveat，设置 needsReview | `rate-limit:provider:prescribed/limit` |
| 4 | `pre-release` | 修复启用了 `-rc`/`-beta`/`-canary` 功能 | 追加 "requires pre-release version" caveat | `pre-release:pkg@version` |
| 5 | `middleware-conflict` | 建议针对由 middleware matcher 覆盖的路由 | 追加 "Middleware {matcher} may intercept" caveat | `middleware-conflict:matcher` |
| 6 | `undeclared-dep` | 修复导入了 package.json 中不存在的包 | 预先添加 "Add dependency first: npm i {pkg}" | `undeclared-dep:pkg` |
| 7 | `count-correct` | 引用计数 > 已验证计数，ground-truth 已知 | 重写为 "~N" 并附已验证计数 | `count-correct:token:cited→actual` |
| 8 | `count-strip` | 引用计数 > 已验证计数，无 ground truth | 重写为 "a number of" | `count-strip:token` |
| 9 | `rendering-mode-mislabel` | 建议将 ISR/SSR 归咎于静态页面 | 追加警告，设置 needsReview | `rendering-mode-mislabel` |
| 10 | `unknown-citation` | URL 不在 `references/docs-library.json` 中 | 剥离 URL，如果全部剥离则设置 needsReview | `unknown-citation:url` |
| 11 | `version-mismatch` | URL 的 `applicableFrameworks` 与栈不匹配 | 剥离 URL，如果全部剥离则设置 needsReview | `version-mismatch:url` |
| 12 | `missing-citation` | 在其他清理器之后 `citations.length === 0` | 完全丢弃建议 | （建议不发出；在最后计数） |

清理器顺序很重要：dollar-strip 首先运行（便宜、确定性），然后是内容清理器，最后是引用清理器。这保证了引用计数是针对最终状态计算的。

`recordSanitizer(rec, tag)` 辅助函数是单一入口——清理器必须在变更字段之前调用它。否则审计跟踪会腐烂。

### 提供者速率限制

由清理器 #3 使用。这些提供者限制是公开的契约值：

| 提供者 | 限制 | 文档 URL |
|---|---|---|
| Notion | 3 rps | https://developers.notion.com/reference/request-limits |
| OpenAI | 30 rps | https://platform.openai.com/docs/guides/rate-limits |
| Stripe | 100 rps | https://docs.stripe.com/rate-limits |
| Anthropic | 10 rps | https://docs.anthropic.com/en/api/rate-limits |

层级/计划不同；这些是首层默认。如果推荐建议更高并发，清理器会预先添加 caveat。

## 信封解包恢复

不是清理器——而是恢复步骤。LLM 偶尔将其 JSON 输出包装在信封中：

```json
{ "data": { "recommendations": [...] } }
{ "result": { "recommendations": [...] } }
{ "insights": { "recommendations": [...] } }
```

`attemptManualRecovery` 在 schema 验证之前剥去一个包装层。递增 `hygieneCounters.envelopeUnwraps`。将解包记录到运行日志。

这是本技能所做的唯一"创造性"解析。任何其他无法通过 schema 验证的内容将被拒绝。

## 评分标准

每条建议在四个轴上评分，每个 0-1。取平均值 → 等级：

| 轴 | 衡量内容 | 强（1.0）信号 |
|---|---|---|
| Specificity | 具体文件、行号、代码片段 | 三反引号代码围栏或内联代码 ≥10 个字符 + 已验证文件路径 |
| Actionability | 清晰的"先做这个再做那个"步骤 | 编号步骤；每步含动词；没有 "consider"/"might" |
| Grounding | 声明追溯到发现或指标数据 | `sourceIndex` 匹配某发现或建议有 affectedFiles + 代码围栏（推定为有证据） |
| Evidence | 数值化、被观察到的声明 | 计数词（错误、查询、调用）+ 单位（% / ms / s / K / M） |

等级阈值：
- `Excellent` ≥ 0.85
- `Good` 0.70 – 0.85
- `Fair` 0.55 – 0.70
- `Poor` < 0.55 → 在第 4 步的质量底线处丢弃

## Next.js 版本感知

推荐器的引用库按 `signals.json.stack.framework@frameworkVersion` 过滤。在选择要推荐的 API 时，代理仍应自检版本：

| 功能 | 可用版本 | 备注 |
|---|---|---|
| App Router | Next ≥ 13.0 | 自 14 起为默认 |
| `generateStaticParams` | Next ≥ 13.0 | 在 App Router 中取代 getStaticPaths |
| Fetch `next: { revalidate }` | Next ≥ 13.0 | 注意：默认 fetch 缓存在 Next 15 中反转 |
| `unstable_cache` | Next 14-15 | 在 16 中被 `'use cache'` 取代 |
| `'use cache'` 指令 | Next ≥ 15.0 | 持久缓存原语 |
| `cacheLife()`、`cacheTag()` | Next ≥ 15.0 | 与 `'use cache'` 配合使用 |
| `after()` | Next ≥ 15.0 | 非阻塞响应后工作 |
| 部分预渲染 | Next ≥ 15.0 | 稍后稳定目标——按发布验证 |
| `revalidateTag` / `revalidatePath` | Next ≥ 13.4 | 基于标签的按需失效 |
| `cookies()` / `headers()` async | Next ≥ 15.0 | 15+ 中的异步模式 |

本技能精心策划的引用库通过 `applicableFrameworks` 对这些约束进行编码。如果贡献者添加新的 Next.js 功能 URL，他们必须在 `references/docs-library.json` 中设置正确的 semver 范围。
