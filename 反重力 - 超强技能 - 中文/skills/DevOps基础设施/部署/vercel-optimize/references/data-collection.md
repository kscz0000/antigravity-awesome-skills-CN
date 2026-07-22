# 数据收集

本技能在第 1 步收集的内容、每个信号的来源，以及在某个能力缺失时的降级方式。

此处所有结构都由 `packages/vercel-optimize-tests/test/fixtures/real-cli-output/` 中的脱敏 CLI 固定数据覆盖。

## 目录

- [The `signals.json` shape](#the-signalsjson-shape)
- [Per-signal source matrix](#per-signal-source-matrix)
- [Error states and fallbacks](#error-states-and-fallbacks)
- [Real JSON shapes](#real-json-shapes)
- [Why we avoid stderr grep](#why-we-avoid-stderr-grep)

## `signals.json` 的结构

`node scripts/collect-signals.mjs` 输出 Vercel 侧的信号文档。`node scripts/scan-codebase.mjs <repo-root>` 输出本地代码库扫描。`node scripts/merge-signals.mjs vercel-signals.json codebase.json --out signals.json` 将二者合并为闸门、深入调查、验证器和渲染器消费的产物。合并步骤还会为扫描器发现标注路由级可观测性、`COLD-PATH` 或 `NO-ROUTE-MAPPING`；扫描器闸门拒绝不带这些确定性标注之一的、与流量无关的发现。

合并后的 `signals.json` 具有以下顶层结构：

```json
{
  "schemaVersion": "1.2",
  "collectedAt": "2026-05-12T20:48:44.123Z",
  "timeWindow": "14d",
  "projectId": "prj_xxx",
  "orgId": "team_xxx",
  "projectIdSource": "repo.json" | "project.json" | "arg" | "env" | "arg+repo.json" | "arg+project.json" | "env+repo.json" | "env+project.json",
  "commandScope": {
    "ok": true,
    "cliScope": "team-slug-or-username",
    "source": "team-api" | "whoami-current-team" | "whoami-user" | "linked-org-scope" | "missing-org-scope",
    "required": true,
    "detail": "..."
  },
  "frameworkSupport": {
    "ok": true,
    "status": "supported" | "limited" | "unsupported",
    "blocker": null | "unsupported_framework",
    "framework": "next",
    "label": "Next.js",
    "detail": "..."
  },
  "frameworkSupportBlocker": null | "unsupported_framework",
  "frameworkSupportDetail": "...",
  "observabilityPlus": true | false | null,
  "observabilityPlusPreflight": { /* CLI/API configuration probe result */ },
  "observabilityPlusUsable": true | false | null,
  "observabilityPlusBlocker": null | "no_oplus_probe" | "project_disabled" | "payment_required" | "forbidden" | "daily_quota_exceeded" | "project_not_found" | "not_linked" | "all_failed_other" | "no_traffic",
  "observabilityPlusBlockerDetail": "...",
  "plan": { "plan": "hobby" | "pro" | "enterprise" | "uncertain", "reason": "..." },
  "project": { /* /v9/projects/:id response; team-owned projects include ?teamId */ },
  "contract": { "context": "...", "commitments": [], "totalCommitments": 0 },
  "usage": { /* vercel usage --format json --breakdown daily, or null */ },
  "usageError": null | "USAGE_UNAVAILABLE" | "USAGE_CONTEXT_MISMATCH" | "NOT_COLLECTED_OBSERVABILITY_BLOCKED" | "NOT_COLLECTED_UNSUPPORTED_FRAMEWORK" | "EXIT_<n>" | "UNKNOWN",
  "stack": { /* framework + version + router + ORM + monorepo */ },
  "codebase": { /* scan-codebase output: stack + routes + findings */ },
  "metrics": { /* per-metric query results (only when observabilityPlus=true) */ },
  "metricsSchema": [ /* array of {id, description} */ ]
}
```

所有指标查询都使用相同的 `timeWindow` 常量（`14d`）——定义为 [lib/queries.mjs](../lib/queries.mjs) 中的 `TIME_WINDOW`，由仓库测试套件覆盖。混合窗口会静默产生不兼容的汇总；切勿在单个查询上钉住 `since`。

所有接受 scope 的 Vercel CLI 命令都必须使用 `commandScope.cliScope`（`--scope <team-slug-or-username>`）。已链接的项目文件通常包含原始的 `team_...` 或 `usr_...` ID，但一些 CLI 子命令会在 `--scope` 收到原始账户 ID 时静默回退到当前团队。`collect-signals.mjs` 在运行 `vercel metrics`、`vercel usage` 或 `vercel contract` 之前将原始团队 ID 解析为 slug，将原始用户 ID 解析为用户名；`deep-dive.mjs` 为后续指标查询复用相同 scope。如果项目链接缺少所有者账户或无法解析 CLI 安全的 scope，请停止并询问用户希望审计哪个 Vercel 项目和团队/个人 scope。不要从当前的 `vercel whoami` 团队推断 scope。

下游消费者按字面路径引用 `signals.<field>`。当任何被消费的路径被重命名或删除时，必须递增 `schemaVersion`。

## 每信号来源矩阵

| 信号 | CLI 命令 | 必需于 | 缺失时的回退 |
|---|---|---|---|
| 认证 | `vercel whoami` | 一切 | 退出并提示"run `vercel login`" |
| CLI 版本 | `vercel --version` | 一切 | 退出并提示"upgrade to v53+"——v53 是本技能的兼容基线 |
| Project ID + Org ID | `.vercel/repo.json`（较新）或 `.vercel/project.json`（旧版）→ `VERCEL_PROJECT_ID` + `VERCEL_ORG_ID` → argv。当用户传入 project ID 且多项目 `repo.json` 恰好包含一个匹配条目时，收集器使用该条目的所有者账户。 | 一切 | 退出并提示"run `vercel link` or pass projectId"。多项目 `repo.json` 没有明确匹配的项目 ID，或任何项目 ID 没有所有者账户范围，都是歧义；请用户澄清预期的项目/账户 |
| 框架支持 | 本地 `package.json` 经 `detectStack()` + `classifyFrameworkSupport()` | 基于代码的路由建议 | 在指标展开之前对不支持的框架停止，除非用户选择 `--continue-unsupported-framework` |
| CLI 命令 scope | `vercel whoami --format json`，然后当已链接的 `team_...` ID 必须转换为 slug 时调用 `vercel api /v2/teams/:orgId` | 让 `vercel metrics`、`vercel usage` 和 `vercel contract` 保持在已链接项目的账户上，而不是用户的当前/个人 scope | `PROJECT_SCOPE_UNRESOLVED` 或 `SCOPE_UNRESOLVED`；停止并询问用户澄清预期的项目/账户，然后在预期团队或个人账户下重新链接 |
| 项目/scope 验证 | `vercel api /v9/projects/:id?teamId=<orgId>`（对团队所属项目）；对 `usr_...` 用户所属项目省略 `teamId` | 在得出 Observability Plus 或计费结论之前，证明已解析账户能读取已解析项目 | `PROJECT_SCOPE_MISMATCH`；停止并要求用户确认精确的 Vercel 项目和团队/个人 scope。在通过此检查之前，不要报告 Observability Plus 缺失 |
| Observability Plus 配置 | Vercel CLI/API 探测加一次指标访问检查；用户所属项目跳过团队配置端点，依靠限定 scope 的指标探测 | 所有 `metrics.*` 信号 | 当账户缺少 Observability Plus 或本项目被禁用时尽早停止 |
| Observability Plus 指标访问 | 一次金丝雀 `vercel metrics vercel.request.count --since 14d --limit 1`，仅在成功后才进行完整扇出 | 所有 `metrics.*` 信号 | 将 `observabilityPlusUsable=false` 与 blocker 详情一起设置；在项目/scope 验证之后、计费收集之前发出 blocker 文档，除非传入 `--continue-without-observability` |
| 项目配置 | 项目/scope 验证的已验证项目 API 响应 | Fluid Compute、BotID、Speed Insights、安全标志 | 在所有权不匹配时停止；否则需要缺失可选字段的闸门跳过 |
| 计划等级 | `vercel api /v2/teams/:orgId`（或用户所属项目的 `/v2/user`）→ `billing.plan`，然后回退到限定 scope 的 `vercel contract --format json` → `inferPlan()` | 仅成本上下文框架 | `plan="uncertain"`；成本量级仍然根据 `usage.services[].billedCost` 计算 |
| 计费 usage | 限定 scope 的 `vercel usage --format json --from <14d> --to <today>`，在安装的 CLI 支持时尽力做项目分组 | 成本量级框架、计费驱动的候选 | 查询且不可用时为 `null` + `usageError` 已设置；预检停止发生在计费收集之前时为 `NOT_COLLECTED_*` |
| 栈 | 本地 `package.json` + 目录扫描 | 版本感知引用过滤、扫描器分流 | "unknown" framework → 所有框架特定的引用被过滤 |
| `metrics.fnDurationP95ByRoute` | `vercel metrics vercel.function_invocation.function_duration_ms -a p95 --group-by route --since 14d` | `slow_route`、`platform_fluid_compute` 闸门 | `{ok:false}`；闸门不输出候选 |
| `metrics.requestsByRouteCache` | `vercel metrics vercel.request.count --group-by route --group-by cache_result --since 14d` | `uncached_route`、流量总量计算 | `{ok:false}` |
| `metrics.fnStatusByRoute` | `vercel metrics vercel.function_invocation.count --group-by route --group-by http_status --since 14d` | 用于 `route_errors` 和 `slow_route` 错误取消资格的规范函数级 5xx 来源 | `{ok:false}`；仅对较旧固定数据回退到 `requestsByRouteStatus` |
| `metrics.requestsByRouteStatus` | `vercel metrics vercel.request.count --group-by route --group-by http_status --since 14d` | 请求级状态的兼容性回退 | `{ok:false}` |
| `metrics.externalApiP75` | `vercel metrics vercel.external_api_request.request_duration_ms -a p75 --group-by origin_hostname --since 14d` | `external_api_slow` 闸门 | `{ok:false}` |
| `metrics.fnStartTypeByRoute` | `vercel metrics vercel.function_invocation.count -a sum --group-by route --group-by function_start_type --since 14d` | `cold_start`、`platform_fluid_compute` | `{ok:false}`；闸门休眠。**`function_start_type` ∈ {cold,hot,prewarmed}** 是在 CLI v53.4.0+ 上读取冷启动率的公开方式（取代了旧的"无法推导"缺口）。 |
| `metrics.fnGbHrByRoute` | `vercel metrics vercel.function_invocation.function_duration_gbhr -a sum --group-by route --since 14d` | 成本排序/报告分解 | `{ok:false}` |
| `metrics.fnCpuMsByRoute` | `vercel metrics vercel.function_invocation.function_cpu_time_ms -a sum --group-by route --since 14d` | 活跃 CPU 排序（Fluid Compute 计费单位） | `{ok:false}` |
| `metrics.fnPeakMemoryByRoute` | `vercel metrics vercel.function_invocation.peak_memory_mb -a max --group-by route --since 14d` | `oversized_memory` 闸门 | `{ok:false}` |
| `metrics.fnProvisionedMemoryByRoute` | `vercel metrics vercel.function_invocation.provisioned_memory_mb -a max --group-by route --since 14d` | `oversized_memory` 闸门 | `{ok:false}` |
| `metrics.fnTtfbP95ByRoute` | `vercel metrics vercel.function_invocation.ttfb_ms -a p95 --group-by route --since 14d` | 慢路由的 TTFB 交叉检查 | `{ok:false}` |
| `metrics.fdtByRoute` | `vercel metrics vercel.request.fdt_total_bytes -a sum --group-by route --since 14d` | 带宽成本排序 | `{ok:false}` |
| `metrics.fdtByBot` | `vercel metrics vercel.request.fdt_total_bytes -a sum --group-by bot_category --since 14d` | 通过观察到的 bot 带宽份额加强 `platform_bot_protection` | `{ok:false}`；闸门回退到仅配置信号 |
| `metrics.fdtByCache` | `vercel metrics vercel.request.fdt_total_bytes -a sum --group-by cache_result --since 14d` | 未缓存带宽叙事 | `{ok:false}` |
| `metrics.middlewareCount` | `vercel metrics vercel.middleware_invocation.count -a sum --group-by request_path --since 14d` | `middleware_heavy` 闸门 | `{ok:false}`；闸门休眠 |
| `metrics.middlewareDurationP95` | `vercel metrics vercel.middleware_invocation.duration_ms -a p95 --group-by request_path --since 14d` | 中间件延迟叙事 | `{ok:false}` |
| `metrics.isrReadsByRoute` | `vercel metrics vercel.isr_operation.read_units -a sum --group-by route --since 14d` | `isr_overrevalidation` 闸门（分母） | `{ok:false}` |
| `metrics.isrWritesByRoute` | `vercel metrics vercel.isr_operation.write_units -a sum --group-by route --since 14d` | `isr_overrevalidation` 闸门（分子） | `{ok:false}` |

**ISR 读写比注意事项。** `isrReadsByRoute` 只暴露**源层**的读数。CDN 层读取（区域缓存命中，从不到达 ISR 源）目前未单独呈现，且可能主导总读取量。在将"写 > 读"标记为倒挂之前，闸门和报告必须 (a) 承认 CDN 层读取未包含在内，(b) 在告警之前用 `requestsByRouteCache` 的 `cache_result=HIT` 份额来佐证。仅较高的源写率并不代表病理性的过度重新验证，如果 CDN 正在吸收稳态读取流量。
| `metrics.imageCount`、`imageByHost`、`imageSourceBytes` | `vercel metrics vercel.image_transformation.*` | 图像优化叙事 | `{ok:false}` |
| `metrics.cwvLcpByRoute`、`cwvInpByRoute`、`cwvClsByRoute`、`cwvTtfbByRoute`、`cwvCount`、`cwvCountByRoute` | `vercel metrics vercel.speed_insights_metric.*`（vitals 用 `p75`，计数用 `sum`）`--since 14d` | `cwv_poor` 闸门 | 在 14 天窗口 Speed Insights 没有测量返回时为空——闸门休眠；除非另一个信号证明，否则不要推断为禁用或无流量 |
| `metrics.firewallByAction` | `vercel metrics vercel.firewall_action.count -a sum --group-by waf_action --since 14d` | Bot 保护叙事；显示现有托管规则活动 | `{ok:false}` |
| `metrics.botIdChecks` | `vercel metrics vercel.bot_id_check.count -a sum --since 14d` | 确认 BotID 是否正在运行 | `{ok:false}` |
| `metrics.externalApiCount`、`externalApiBytes` | `vercel metrics vercel.external_api_request.*` 按 `origin_hostname` 分组 | 外部依赖成本叙事 | `{ok:false}` |

## 错误状态与回退

`lib/vercel.mjs` 中的 `runVercelJson()` 首先将 stdout 解析为 JSON（最可靠的信号——CLI 即使在退出码非零时也会发出结构化错误负载），仅在 JSON 解析失败时回退到 stderr 子串匹配：

| 代码 | 含义 | 技能行为 |
|---|---|---|
| `unsupported_framework` | 检测到的框架无法可靠地将 Vercel 路由指标映射回源文件 | 在指标展开之前停止；询问是否继续有限的平台/扫描器审计 |
| `PROJECT_SCOPE_UNRESOLVED` | 找到项目但没有所有者账户，或 `.vercel/repo.json` 包含多个已链接项目且未提供明确匹配的项目 ID | 在 `vercel metrics`、`vercel usage` 或 `vercel contract` 之前停止；询问用户希望审计哪个 Vercel 项目和团队/个人 scope |
| `SCOPE_UNRESOLVED` | 已链接项目属于特定团队/用户，但收集器无法解析 CLI 安全的 `--scope` 值 | 在 `vercel metrics`、`vercel usage` 或 `vercel contract` 之前停止；询问用户使用正确团队切换/重新链接 |
| `PROJECT_SCOPE_MISMATCH` | 已解析的团队/个人账户无法读取已解析的项目，或项目 API 返回不同的所有者/项目 | 在 Observability Plus、指标、usage 或合同检查之前停止；询问用户确认精确的 Vercel 项目和团队/个人 scope |
| `no_oplus_probe` | 团队上未启用 Observability Plus | 在完整指标扇出之前停止；询问是否启用 Observability Plus 或仅运行扫描器 |
| `project_disabled` | 团队上启用了 Observability Plus 但项目上禁用 | 在完整指标扇出之前停止；询问用户为该项目启用 Observability Plus 或继续仅扫描器 |
| `daily_quota_exceeded` | 当天的 Observability Plus 查询配额已用尽 | 在完整指标扇出之前停止；告知用户在下一个 UTC 午夜重置后重试，或询问是否继续仅扫描器 |
| `USAGE_UNAVAILABLE` | 在实际查询计费 usage 后，`vercel usage` 未返回 Costs 负载 | `usage=null`；成本层闸门输出较低优先级候选；报告的计费部分显示确切的 usage 错误 |
| `PROJECT_NOT_FOUND` | `vercel api /v9/projects/<id>` 404（通常是错误的 scope） | `project={error}`；依赖项目配置的平台闸门跳过；报告标记数据缺口 |
| `invalid_filter_dimension` / `invalid_dimension` | 指标查询使用了该指标不支持的维度 | 指标返回 `{ok:false, code, allowedValues}`；消费者可以自省并调整 |
| `NOT_LINKED` | 应用目录未按 `vercel metrics` 要求的方式链接 | 运行 `vercel link --yes --project <project-name-or-id> --cwd <app-dir>`；团队已知时添加 `--team <team-id-or-slug>`。如果 cwd 未链接，仅传 `VERCEL_PROJECT_ID` 对路由指标是不够的 |
| `NOT_AUTH` | 会话已过期 | 调用方退出并提示"run `vercel login`" |
| `FORBIDDEN` | 403——角色缺少权限 | 跳过该端点；继续降级信号；在报告中浮现 |
| `RATE_LIMIT` | 来自 API 的 429 | 视为"缺失数据"（尚未实现重试） |
| `EXIT_N` | 其他情况 | 视为缺失数据；继续 |

本技能从不会因为单个端点失败而使整个收集崩溃。每个 catch 块使用 `?? null` 或 `?? {}`，因此 JSON 输出始终结构良好。

## 真实的 JSON 结构

### `vercel metrics <id> --format json`

```jsonc
{
  "query": {
    "metric": "vercel.request.count",
    "aggregation": "sum",
    "groupBy": ["route"],
    "startTime": "2026-04-13T04:00:00.000Z",
    "endTime": "2026-05-13T08:00:00.000Z",
    "granularity": { "hours": 4 }
  },
  "summary": [
    { "route": "/dashboard/[sessionId]", "vercel_request_count_sum": 4923 },
    { "route": "/sw.js",               "vercel_request_count_sum": 872 }
  ],
  "data": [
    { "timestamp": "2026-04-13T04:00:00.000Z", "vercel_request_count_sum": 0, "route": "/dashboard/[sessionId]" }
    /* ... */
  ],
  "statistics": { "bytesRead": 10267, "rowsRead": 947, "dbTimeSeconds": 0 }
}
```

字段命名规则：指标 ID 的点变成下划线，并附加聚合后缀——`vercel.request.count` + `sum` → `vercel_request_count_sum`。`lib/vercel.mjs::normalizeSummary()` 将 `summary[]` 扁平化为 `[{<dim>: v, ..., value: <n>}]`。

### `vercel metrics schema --format json`

`{id, description}` 条目的数组——不是对象。早期文档中的许多指标 ID 不存在：没有 `vercel.function.cold_starts`，也没有 `vercel.cache.hits`。缓存状态是 `vercel.request.count` 上的 `cache_result` 维度。

### `vercel metrics <id> --filter "<bad>"`

```jsonc
{
  "error": {
    "code": "invalid_filter_dimension",
    "message": "Filter uses invalid dimension \"status\" for metric \"vercel.request.count\".",
    "allowedValues": [ "asn_id", ..., "http_status", ..., "route" ]
  }
}
```

状态过滤使用 `http_status`（而不是 `status`）。`http_status eq '500'` 和 `http_status ge 500` 都有效。

### `vercel api /v9/projects/<id>` / `?teamId=<orgId>`

与本技能相关的顶层键（真实的、已验证）：
- `framework`（字符串，例如 `"nextjs"`）
- `resourceConfig.fluid`（布尔值）——**Fluid Compute 开关**
- `defaultResourceConfig.fluid`——新函数的模板
- `security.botIdEnabled`（布尔值）——**BotID 开关**
- `security.managedRules.bot_filter`（`{active, action}`）——防火墙规则
- `speedInsights`（`{id, hasData}`）
- `webAnalytics`（`{id}`）——已安装但 `features.webAnalytics` 表示启用状态
- `nodeVersion`（例如 `"22.x"`）

在不属于用户的 `currentTeam` 的团队所属项目上，不带 `?teamId=` 的调用将返回 404。对于用户所属项目（`orgId` 以 `usr_` 开头），省略 `teamId` 并让 CLI 使用已认证的用户上下文。

### `vercel contract --format json`

```jsonc
{ "context": "example-team", "commitments": [], "totalCommitments": 0 }
```

直接的账户计费记录是主要的计划信号：来自 `vercel api /v2/teams/:orgId` 或 `vercel api /v2/user` 的 `billing.plan` 预期为 `hobby`、`pro` 或 `enterprise`。

`vercel contract` 仅作为回退。`commitments[]` 字段名不稳定，因此 `inferPlan()` 尝试 `category`、`commitmentCategory` 和 `type`；类别 `Spend` 表示 Pro，`Usage` 表示 Enterprise。空的 commitments 不再单独表示 Hobby。

### `vercel usage --format json`

可能返回 `Error: Costs not found (404)`。将该查询错误视为 `USAGE_UNAVAILABLE` 并降级——本技能仍可以从指标 + 扫描器生成有用的报告。当 `usageError` 是 `NOT_COLLECTED_OBSERVABILITY_BLOCKED` 或另一个 `NOT_COLLECTED_*` 值时不要使用此解释；那意味着审计在 `vercel usage` 运行之前停止。

## 为何避免 stderr grep

CLI 错误消息字符串不是稳定的契约——它们可能在版本之间变化。通过 grep `stderr.includes('Observability Plus')` 来检测 `OPLUS_REQUIRED` 会在 Vercel 重新措辞该消息的瞬间失效。

因此 `runVercelJson()`：
1. 始终首先尝试**将 stdout 解析为 JSON**。大多数失败会发出确定性的 `{error:{code,message,allowedValues}}` 负载。
2. 仅在 stdout 不可解析为 JSON 时回退到小写 stderr 子串匹配。
3. 将任何无法识别的内容归类为 `EXIT_N` 并视为"缺失数据，继续"。

即使没有精确的类别检测，本技能也是正确的。类别存在是为了给用户提供更好的错误消息，而不是驱动控制流。
