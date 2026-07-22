# 验证

建议中的声明如何机械地验证，以及在通过率较低时推荐器何时重新运行。

## 目录

- [Why mechanical verification](#why-mechanical-verification)
- [Claim types](#claim-types)
- [Dispositions](#dispositions)
- [Re-gen trigger and accept criteria](#re-gen-trigger-and-accept-criteria)
- [Verifier implementation](#verifier-implementation)

## 为何采用机械验证

推荐器是 LLM。LLM 会对计数产生幻觉、错误计算文件出现次数，并在外观相似的文件之间混淆代码片段。机械验证——grep + 文件系统读取 + 针对 `signals.json` 和 `references/docs-library.json` 的 JSON 检查——在客户看到之前捕获这些失败。

契约：验证每个数字声明、文件引用、代码片段、引用 URL 和与其他声明的矛盾。不要求 LLM 判断自己的输出是否正确。

## 声明类型

验证器从 `why`、`fix`、`currentBehavior`、`desiredBehavior` 和 `verify` 字段提取声明。每个匹配的声明都会通过以下某个处理器运行：

| # | 声明类型 | 建议中的模式 | 验证 |
|---|---|---|---|
| 1 | `pattern_count` | "N fetch() calls in file X" | 在 X 中 grep/ast-grep，精确计数匹配 |
| 2 | `pattern_exists` | "uses JSON.parse(JSON.stringify())" | grep，布尔值 |
| 3 | `pattern_absent` | "no Cache-Control header" | grep，验证不存在（带保护——见下文） |
| 4 | `file_exists` | "app/not-found.tsx exists" | fs.access |
| 5 | `finding_count` | "2 unoptimized images" | 发现计数与 `verifiedFindings.json` 对比 |
| 6 | `contradiction` | 声明 A vs 声明 B | 子串冲突检查 |
| 7 | `code_snippet` | 标记为 "Before:" 的代码围栏 | 在引用的文件中进行子串搜索 |
| 8 | `arithmetic` | "20% of 100K = 20K" | 数学检查 |
| 9 | `repo_count` | "11 unstable_cache usages across 8 files" | grep 仓库，统计不同文件 |
| 10 | `cited_count_literal` | "60+ icons in packages/ui/src/icons" | glob 目录，按扩展名计数 |
| 11 | `citation_in_library` | `citations[]` 中的任何 URL | URL ∈ `references/docs-library.json` |
| 12 | `citation_applies_to_version` | `citations[]` 中的任何 URL | URL 的 `applicableFrameworks` 与 `signals.json.stack.framework@frameworkVersion` 匹配 |
| 13 | `cache_vary_matches_dynamic_inputs` | CDN 缓存建议涉及读取 Vercel 地理位置的路由文件 | 除非建议通过粗粒度的 Vercel 地理位置头（如 `X-Vercel-IP-Country`、`X-Vercel-IP-Country-Region` 或 `X-Vercel-IP-City`）进行 Vary，否则失败 |
| 13a | `cache_vary_cardinality_safe` | CDN 缓存建议对请求特定的地理位置设置 `Vary` | 在高基数 `X-Vercel-IP-Latitude` / `X-Vercel-IP-Longitude` / `X-Vercel-IP-Postal-Code` 上失败 |
| 14 | `next_cached_not_found_causal_support` | 建议声称 `'use cache'` 中的 `notFound()` 导致了 5xx | 除非有 Next 特定文档或运行时栈证据支持，否则失败 |
| 15 | `next_stable_cache_api_for_version` | Next.js 16 缓存建议包含代码示例 | 在 `unstable_cacheLife` / `unstable_cacheTag` 或单参数 `revalidateTag()` 上失败 |
| 16 | `next_cache_components_runtime_cache_preference` | Next.js 建议在 `cacheComponents=true` 时使用 Runtime Cache API | 除非使用 `use cache: remote` 或将 Runtime Cache 框定为回退，否则失败 |
| 17 | `next_cache_components_route_segment_config` | Next.js 16 建议在 `cacheComponents=true` 时建议已移除的路由段配置 | 在 `dynamicParams`、`dynamic`、`revalidate` 或 `fetchCache` 建议上失败 |
| 17a | `next_route_revalidate_static_prereq` | 建议为 Next.js page/layout 路由建议路由级 `export const revalidate` | 当路由链包含请求时 API 或可能强制动态渲染的常见鉴权辅助函数时失败 |
| 18 | `next_cache_lifetime_freshness_supported` | 建议使用 `cacheLife()` 延长带标签的 Cache Components 生命周期 | 除非每个受影响的 `cacheTag()` 都有匹配的 `revalidateTag()` / `updateTag()` 证据，否则失败 |
| 19 | `next_cache_life_cdn_header_semantics` | 建议声称 `cacheLife()` 发出 CDN/Cache-Control 头或缺少 `cacheLife()` 单独使路由按请求运行 | 除非重写为已记录的 Cache Components 生命周期行为或由生产头证据支持，否则失败 |
| 20 | `next_cache_tag_invalidation_supported` | 缓存生命周期建议声称存在标签失效 | 除非每个声称为 `cacheTag()` 都有匹配的 `revalidateTag()` / `updateTag()` 证据，否则失败 |
| 21 | `cache_rec_not_error_dominated_or_acknowledged` | CDN 缓存建议针对具有函数 5xx 指标的路由 | 除非建议排除或承认错误流量，否则失败 |
| 22 | `cache_control_header_syntax` | CDN 缓存建议包含 `Cache-Control`、`CDN-Cache-Control` 或 `Vercel-CDN-Cache-Control` 值 | 在空指令（如尾随逗号）上失败 |
| 23 | `cache_policy_positive_or_no_ready_rec` | 缓存候选发出就绪建议 | 除非命名正面的缓存策略，否则失败；仅 no-store 属于无改动/观察输出 |
| 24 | `cache_404_long_ttl_safety` | CDN 缓存建议提及 404 或 not-found 分支 | 除非建议将 404/not-found 分支保持未缓存、短生命期或显式分开，否则失败 |
| 25 | `immutable_dynamic_route_safety` | 动态路由建议使用浏览器 `immutable` 缓存 | 除非 URL 是字节版本化的或将指令限定到 Vercel 的 CDN，否则失败 |
| 26 | `auth_guard_parallelization_safety` | 并行化建议涉及私有/鉴权/所有权数据 | 如果私有数据可以在鉴权或所有权保护之前被获取，则失败 |
| 27 | `parallelization_impact_not_overclaimed` | 并行化建议承诺助手大小的延迟下降 | 除非助手/跨度时间被测量过，否则失败 |
| 28 | `parallelization_not_cpu_bound_work` | 并行化建议针对 CPU 或编译工作 | 除非测得的等待/I/O 时间证明存在独立工作可以重叠，否则失败 |
| 29 | `runtime_error_cause_supported` | 路由错误建议命名运行时异常/根本原因 | 除非运行时日志或栈证据支持该原因，否则失败 |
| 30 | `turbo_build_cache_safety` | 建议启用 Turbo 构建缓存 | 当 package 构建脚本具有迁移副作用或 Turbo 输出缺少框架构建输出时失败 |

验证器保护：

- **`snippet_in_wrong_file`**：找到代码片段，但在与引用路径不同的文件中 → 处理为 `unsupported`（不要使建议失败；LLM 接近正确，但源文件声明是错误的）。
- **`line-number-as-count`**：针对 `pattern_count` 声明匹配 "filename:42" → 跳过；这是行号，不是计数。
- **`prose-of-absence`**："no cache headers" 没有显式的 grep 确认 → `unsupported`；缺失声明需要证据。
- **`pattern_count` for abstracted DB calls**：`db.method()` 出现在带有 DB 导入 + await 辅助函数但字面计数为 0 的文件中 → `unsupported`（导入链解析超出范围）。

## 处理结果

每个已验证的声明解析为以下四种状态之一：

| 处理结果 | 含义 | 是否计入 `passRate`？ |
|---|---|---|
| `verified` | 声明与现实匹配 | 是（计为通过） |
| `failed` | 声明与现实矛盾 | 是（计为失败） |
| `unsupported` | 声明无法机械检查（见上述保护） | 否 |
| `unverifiable` | 超出范围（例如，外部 API 行为、仅运行时） | 否 |

`passRate = verified / (verified + failed)`。Unsupported 和 unverifiable 不计入。

## 重生成触发与接受标准

验证后：

| 条件 | 动作 |
|---|---|
| `passRate < 0.8 AND verifiableClaimCount >= 2` | 重跑第 3.3 步（推荐器），并以 `topFailures` 作为反馈注入 |
| 项目配置矛盾、缓存安全失败或框架语义失败 | 硬性重跑。客户报告扣留原始建议，直到重新生成修复或弃权 |
| `passRate >= 0.8` 或 `verifiableClaimCount < 2` | 接受运行，继续第 4 步 |

_(基线在 2026 年 5 月审计中从 5 降至 2：一条带 1/1 失败声明的建议与 1/5 一样糟糕，而旧基线让许多小建议完全逃脱重新生成。)_

重新生成接受标准：

- `regenPassRate >= originalPassRate` 且
- 建议数量未被大量削减（重新生成未丢弃超过 50% 的建议）且
- 发现仍被引用（无建议孤立）

如果重新生成使情况更糟，则保留原始输出，除非触发器是硬安全性（`project_config_contradiction`、`cache_vary_safety` 或 `semantic_safety`）。硬安全失败绝不能发布到客户报告。

## 验证器实现

`scripts/verify-and-regen.mjs` 为每个可验证的声明调用进程内的 `lib/extract-claims.mjs` 和 `lib/verify-claim.mjs`。纯函数，无网络，无 LLM——确定性。

对于 `citation_in_library` 和 `citation_applies_to_version`，脚本使用 `lib/citations.mjs` 的 `isKnownUrl()` 和 `sanitizeCitations()` 辅助函数（已经过测试）。对于其他所有情况，它通过 execFile 调用 grep + ast-grep。