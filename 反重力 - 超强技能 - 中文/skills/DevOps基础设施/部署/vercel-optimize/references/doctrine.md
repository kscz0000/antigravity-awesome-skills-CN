# 原则

四条不可妥协的规则，决定本技能的所有行为。如果未来某项改动与其中任何一条冲突，那么该改动是错误的。

## 规则 1：调查之前先观测

没有指向源文件的可观测信号，本技能绝不读取源文件。第 1 步（`node scripts/collect-signals.mjs`）始终是第一位的。在 `signals.json` 存在之前，任何内容都不会读取源代码。

**跳过这一步为何会失败：** 没有指标，本技能会退化为"在仓库中 grep 已知的反模式并抱怨"。这会产生噪声大、影响力低、与流量、成本或用户痛点无关的建议。指标先行的调查让本技能聚焦于实际观察到的流量、成本和可靠性信号。

### Enterprise 计划的首轮四项检查

当 `plan === 'enterprise'` 时，闸门运行必须在代码级建议之前浮现以下四项检查。现场工程师确认这些是所有续约审计中杠杆最大的账户级开关：

1. **是否启用了 Observability Plus？** 从 `signals.observabilityPlus` 读取。若为 false，整个审计降级；应作为报告顶部的事项浮现。
2. **前面是否有反向代理？** 从响应头/CNAME 链启发式判断（当已收集时）。Vercel ISR 之上叠一个非 Vercel CDN 通常是"哑管道"——浪费开支。
3. **WAF 规则是否启用？** 从 `signals.project.security` 读取。在带有 bot 证据的项目上若缺少 BotID + 托管规则，则是最常见的成本激增原因。
4. **ISR 读写比。** 从 `metrics.isrReadsByRoute` + `metrics.isrWritesByRoute` 读取。在标记"写 > 读"之前，先包含 CDN 层读取（参见 [data-collection.md](data-collection.md)）。

这些检查构成 Enterprise 计划报告开篇叙事的基础；代码级建议紧随其后。

## 规则 2：每次子代理调查之前的确定性闸门

`node scripts/gate-investigations.mjs` 是一个纯 JS、不依赖 LLM 的函数。它读取 `signals.json` 并输出 `{toLaunch, platform, gated}`。同样的输入总是产生字节级一致的输出（除 `appliedAt` 外）。

每一种候选（未缓存路由、慢路由、错误、冷启动、扫描器发现、平台级建议）的阈值表达式都被编码为 `lib/gates/<kind>.mjs` 中的 `gate(signals) → Candidate[]` 函数。

**失败的闸门在最终报告中浮现**，位于 "Not investigated in this run" 之下，并附带被扣留的准确原因。这是面向用户的信任机制：你能看到我们考虑过并选择跳过的事项，以及原因。

**为何重要：** 代理从不通过 LLM 判断"我应该看这个路由吗？"来决策。阈值是机械的。这消除了代理调查不该调查的路由（冷路径）并为不需要的路由建议修复的整个失败模式。

## 规则 3：候选绑定调查范围

当闸门输出带有 `files: ['src/app/api/products/route.ts']` 的候选时，代理只读取该文件（以及随链展开时的导入）。它不会 `grep -r` 整个仓库。

如果你发现自己想要 grep 整个代码库，停下来重读当前候选的 `question` 字段。如果该问题没有约束搜索范围，那么候选格式错误——将其记录为 `gated` 并跳过。不要用更宽的搜索来弥补。

**为何重要：** 代理的工作是验证并解释闸门发现的指标异常，而不是做通用代码审查。漫无目的的调查会产生漂移、幻觉以及与成本和性能数据脱节的建议。

### 扫描器发现（补充信号）

静态 AST-grep 扫描器与指标驱动的调查并行运行。它们的输出会用每文件可观测信号进行注释（若文件映射到热路由，则为 `function invocations: 1.2M; 95th percentile duration: 850ms; cache hit rate: 0%`；若映射到无流量的路由，则为 `COLD-PATH`；若未映射到任何路由，则为 `NO-ROUTE-MAPPING`）。

**默认规则：** 标记为 `COLD-PATH` 或 `NO-ROUTE-MAPPING` 文件的扫描器发现会被丢弃。它们只有在模式与流量无关时才会变成建议：构建配置、middleware matcher、生产中的 source map、原始 script 标签、React Compiler 配置。这些与流量无关——它们对每个请求同等影响，或影响构建本身。

与流量无关的白名单位于每个扫描器的 `metadata.trafficIndependent: boolean` 字段中。仅当你能够为该声明辩护时，才将其设置为 `true`。

## 规则 4：基于文档、版本感知的建议——杜绝幻觉

每条建议都必须至少带有一条来自 `references/docs-library.json` 的引用。其他任何内容都会在清理阶段被丢弃。

该库包含两部分：
- **URL** — Vercel docs、Next.js docs、SvelteKit docs 等。每条声明 `applicableFrameworks`（例如 `["next@>=15.0.0"]`）。
- **跨技能规则引用** — 仅按名称（`vercel-react-best-practices:async-parallel`）。由代理宿主解析。

三个清理器强制执行此规则：
- `missing-citation` — 丢弃 `citations[]` 为空的建议。
- `unknown-citation` — 剥离库中没有的 URL，将 `needsReview=true`。
- `version-mismatch` — 剥离 `applicableFrameworks` 与项目的 framework@version（从 `package.json` 解析）不匹配的 URL。

两条验证声明类型会检查它：`citation_in_library`（URL ∈ 白名单）和 `citation_applies_to_version`（semver 匹配）。

**为何重要：** LLM 会引用看起来合理但 404 的 URL，或向 Next 13 用户推荐 Next 15 功能。两者都是信任杀手。白名单关闭第一种失败模式；`applicableFrameworks` 字段关闭第二种。

### 性能引用引用观察到的数据

每条性能声明都引用 `signals.json` 中实际的可观测数据——例如 `functionRoutes[/api/products].p95Ms=850`。估算的改进以基于观察基线的区间形式呈现：`"Reduce /api/products 95th percentile duration from 850ms toward ~250-400ms based on similar cached routes."`。绝不给出无依据的声明。

### 成本框架使用量级，从不精确

类似 `$340/mo` 的成本声明是被禁止的。投影的美元噪声下限太高，无法证明精确性。`impactMagnitude({currentCost, impactTier})` 辅助函数映射到诸如 `"hundreds of dollars per month at current traffic"` 的短语（基于用户的实际 `vercel usage` 数据计算）。

`$-strip` 清理器在输出时强制执行此规则——面向客户字段中的任何 `$N` 字面量都会被剥离。

性能数字保持精确，因为它们是被观察到的，不是外推的。我们信任观察到的指标；不信任美元投影。

## 何谓良好

一次良好的运行产生：
- 少量（5-15）条建议。
- 每条建议都关联到具体路由或文件以及具体指标信号。
- 每条建议都带有 before/after 代码以及 ≥1 条匹配用户框架版本的引用。
- 成本框架使用量级短语。性能框架使用精确观察数字。
- "Not investigated in this run" 部分解释了我们看到的每一个其他信号以及为何选择不深入（缓存命中率低于阈值、95 分位延迟已经健康等）。
- 没有 `$N/mo` 字符串，没有杜撰的 URL，没有向 Next.js 13 用户推荐 Next.js 15 功能。

## 何谓不佳（我们不会发布的反模式）

- 在不检查流量的情况下通过 grep 仓库中已知反模式得出的建议。
- 没有冷启动信号就"启用 Fluid Compute"。
- 在路由使用 cookies() 且由鉴权守护时，"为 /api/users 添加缓存"。
- 因为 Workflow 步骤是长时间运行的，所以"减少 `/.well-known/workflow/v1/step` 的时长"。Workflow 运行时端点是生成的编排路由；那里的高墙钟时长是预期的，除非单独的可靠性/错误信号另有所指。
- "修复 `/api/chat/[id]/stream` 因为它时长很高"，而未证明该流做了可避免的首字节前工作、高活跃 CPU、重复调用，或可移动的响应后工作。
- "通过做 X 节省 $340/mo"——捏造的精确性。
- 引用不存在或描述了用户版本没有的 Next.js 功能的 URL。
- 用户无法执行的长建议列表；每条建议都需要证据链。

## 范围之外

本技能限定于 Vercel 托管项目的运行时成本与性能优化。以下是明确的非目标；若信号或扫描器发现涉及这些领域，将其路由出去：

- **孤立的部署产物大小。** 仅当它表现为运行时成本（冷启动、FDT）或性能（LCP、INP）时，bundle 大小才有意义。如果唯一的影响是".next 目录很大"，则不在范围内。
- **没有运行时影响的构建期问题。** 构建缓慢、构建缓存未命中、monorepo 构建扇出——只有当它们表现为 Build Minutes 计费压力时才会进入范围（然后它们走 `build-minutes-fanout` 闸门）。一个 6 分钟构建成功完成并交付一个小产物的，不是目标。
- **安全公告与凭据轮换。** `next-mdx-remote` 的 RCE、泄漏的 env 变量、OIDC 与显式密钥认证卫生——请参考安全技能，而不是本技能。例外：当某项安全设置同时也是记录在案的成本杠杆（BotID = bot 流量 = 边缘成本）时，它通过 `platform_bot_protection` 闸门进入。
- **商业/计费流程琐事。** 折扣滑块、席位协调、合同续约机制。本技能可以量化哪种 SKU 很贵，但不进行谈判。