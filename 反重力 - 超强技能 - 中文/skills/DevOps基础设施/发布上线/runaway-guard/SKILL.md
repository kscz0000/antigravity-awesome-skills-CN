---
name: runaway-guard
description: "付费 AI / 推理 API 的成本安全纪律：将 $ 成本视为与时间和空间并列的第三复杂度维度。在编写任何调用代码之前，强制要求写明每次运行的 $ 上限、每日 $ 上限、最大迭代次数限制、并发限制，以及在服务商仪表盘设置匹配的硬性上限。"
risk: safe
source: community
source_repo: morsechimwai/lemmaly
source_type: community
date_added: "2026-05-28"
author: morsechimwai
tags: [cost-safety, finops, ai-apis, agents, retries, concurrency, wallet-invariant, gateway]
tools: [claude-code, antigravity, cursor, gemini-cli, codex-cli]
license: "Apache-2.0"
license_source: "https://github.com/morsechimwai/lemmaly/blob/main/LICENSE"
---

# runaway-guard — $ 成本是第三复杂度维度

每个循环都有时间复杂度和空间复杂度。调用付费 API 的循环还有第三个：**每次执行的美元成本**。模型会自动追踪前两个，但不会追踪第三个，于是它产出的代码中——一个无上限的重试、一次流重连风暴、一个自我重新入队的智能体、一个触发同一作业两次的 webhook——只需一个 bug 就会静默地花掉真金白银。

典型案例：开发者写了一个 Fal.ai 图像生成循环。循环"显然会终止"，因为它遍历的是一个固定列表。但列表来自一个回调，该回调在每次 Inngest 重试时触发。每次重试列表翻倍。到天亮时，账单是 **$200**。测试通过了。代码审查也通过了。bug 不在循环体里。bug 在于**没有人声明钱包不变量**。

runaway-guard 修复了这个问题。声明最大调用次数。声明每次运行的最大美元数。声明每天的最大美元数。在服务商仪表盘设置同样的上限，使代码 bug 无法绕过它们。然后再写代码。

**违反这些规则的字面意思就是违反这个技能的精神。**"我只是在本地测试"正是导致 $200 账单的那个辩解——本地代码访问的付费 API 和生产环境是同一个。

## 何时使用此技能

在以下情况下使用 **runaway-guard**：

- 编写或审查在循环、队列、重试路径、智能体步骤、webhook 处理器或后台作业中调用付费 AI / 推理 API 的代码。
- 导入或封装任何付费推理 SDK：`@fal-ai/*`、`fal-client`、`@anthropic-ai/sdk`、`anthropic`、`openai`、`replicate`、`elevenlabs`、`together-ai`、`groq-sdk`、`cohere-ai`、`@mistralai/*`。
- 设计智能体循环、扇出管道、重试包装器、轮询作业、流重连或自调度作业，这些可能调用计费端点。
- 审计代码库 / PR 中是否存在无界扇出、无界重试、缺少幂等键或缺少服务商侧支出上限。
- 诊断意外账单、失控循环事件或意外的超额费用。

## 铁律

```text
NO CALL TO A PAID API WITHOUT A WRITTEN $-CAP AT BOTH THE CODE AND PROVIDER LEVEL
```

仅在代码中设上限可被该代码中的 bug 绕过。仅在服务商侧设上限会在正常使用时被触发并降低产品质量。两者缺一不可。如果你无法各用一句话陈述这两者，你就没有设计好调用点——你只是写了一个愿望。

## 不可协商的规则

1. **每个调用点都有一个一行成本合约。** 在编写任何付费 API 调用之前，用一句话声明：
   - **每次运行最大调用次数：** 此代码路径单次执行中调用次数的严格上限。
   - **每次运行最大 $ 数：** `max_calls × unit_cost` — 计算出来，不要估算。
   - **每天最大 $ 数：** 作为代码侧上限兜底的服务商侧硬性上限。

   示例：
   - "Fal flux-pro，$0.05/图像；每次作业最多 20 张图像；每次作业最多 $1；服务商 Spend Limit $50/天。"
   - "Anthropic Sonnet，约 $0.015/请求（缓存）；每次智能体运行最多 50 次请求；每次运行最多 $0.75；Workspace Budget 硬性上限 $30/天。"

   如果你无法填满这三个数字，你就没有设计好调用点。

2. **每个调用付费 API 的循环都有一个显式迭代上限，而不仅仅是终止论证。** `invariant-guard` 要求一个终止度量。runaway-guard 要求该上限是**代码中的具体整数**，而不仅仅是"最终会终止"：

   ```ts
   // ❌ Terminates in theory. Bills $200 in practice.
   while (job.status !== 'done') {
     await fal.run(...);
   }

   // ✅ Concrete bound — wallet invariant explicit.
   const MAX_CALLS = 20;
   for (let i = 0; i < MAX_CALLS && job.status !== 'done'; i++) {
     await fal.run(...);
   }
   if (job.status !== 'done') throw new Error('exceeded MAX_CALLS budget');
   ```

3. **每条重试路径都受尝试次数和总耗时成本限制，而不仅仅是时间。** 没有尝试次数上限的指数退避是对自己钱包的攻击。
   - 最大尝试次数：一个小整数（瞬态错误 3-5 次，4xx 错误 1 次）。
   - 在整个管道中计算上限，而不仅是一个库——Inngest 重试 × SDK 重试 × 你自己的重试包装器会相乘。
   - 4xx 错误不重试。句号。它们不会变成 2xx；它们只会再次计费。

4. **每条扇出路径都声明一个并发限制。** 并行调用按每秒挂钟时间成倍增加成本。在代码中、在队列层（Inngest `concurrency`）、以及在服务商（如支持）声明该限制：
   - Inngest：函数上的 `concurrency: { limit: N }`。
   - BullMQ / Sidekiq / Cloud Tasks：队列级并发。
   - 进程内：`p-limit`、信号量或分批 `Promise.all` 块 — 绝不在付费 API 上使用无界 `Promise.all(items.map(...))`。

5. **每个付费 API 都有一个匹配的服务商侧硬性上限，在带外配置。** 纵深防御：如果代码有 bug，服务商止住出血。在与调用点相同的文件中记录该上限，让未来的读者知道它存在。

   | 服务商 | 在哪里设置硬性上限 |
   |---|---|
   | **Fal.ai** | Dashboard → Billing → **Spend Limit**（如 $50/天）。超出即硬性停止。 |
   | **Anthropic** | Console → Workspaces → **Workspace Budget** 设硬性上限。按工作空间、按月。 |
   | **OpenAI** | Org → Settings → **Usage limits**（组织级硬性上限会阻止请求）。⚠️ 按*项目*的月度预算**仅是软阈值** — 它们只发告警但不阻止。真正的硬性上限请使用组织级 Usage limit、计费网关或你自己的 fail-closed 预算检查。 |
   | **Replicate** | Account → Billing → **Spend limit**。按账户。 |
   | **ElevenLabs** | Workspace → **Usage limits**，按工作空间 / API key。 |
   | **Together / Groq / Cohere / Mistral** | 各家都有带月度支出上限的计费仪表盘 — 在首次部署前设置，而不是事后。 |

   没有硬性上限，就没有调用点。在第一个请求之前设置上限，而不是在第一次事故之后。

6. **每个变更或计费调用都要有幂等键。** 触发两次的 webhook 应该只计费一次。没有幂等键，你无法看到的重试策略（负载均衡器、框架、网关）会静默地双重计费。

7. **将"放大器"模式显式化并默认禁止。** 这些是将小 bug 变成大账单的形状：
   - **自调度作业。** 一个没有递减度量就将自己重新入队的作业，就是一个多了几步的无界循环。
   - **调用产生 webhook 的 API 的 webhook 处理器。** 需要环检测，否则它会循环。
   - **基于 LLM 输出的递归。** 没有深度上限的"让模型决定下一步做什么"是以美元计量的无界深度递归。
   - **没有截止时间的轮询。** 没有 `maxWaitMs` 的 `while (!done) await poll()` 是钱包泄漏。
   - **流重连风暴。** 没有退避和尝试次数上限的 WebSocket / SSE 重连可以每分钟数千次地轰击计费端点。
   - **付费调用上的缓存未命中踩踏。** N 个对同一未缓存 key 的并发请求 → N 次计费调用。使用 `singleflight` / 请求合并。

## 写前协议

在产出调用付费 API 的代码之前，你的消息必须按此顺序包含：

1. **服务商 + 单位成本。** "Fal flux-pro：$0.05/图像，按成功计费。"
2. **每次运行最大调用次数。** 一个将作为常量出现在代码中的字面整数。
3. **每次运行最大 $ 数。** `max_calls × unit_cost`。计算出来。
4. **每天最大 $ 数（服务商硬性上限）。** 作为代码兜底的仪表盘设置。
5. **并发限制。** 在代码中、在队列层、在服务商侧。
6. **重试策略。** 最大尝试次数、哪些错误码重试、幂等键策略。
7. **放大器审计。** 走一遍规则 7 中的清单；声明"均不适用"或逐一处理每个适用的项。
8. **代码** — 在调用点上方的注释中包含成本合约。
9. **自检。** 一行："在最坏情况下，此代码计费 $X，服务商上限在 $Y 止住。"

如果 1-7 中有任何一项缺失，不要输出代码。

## 案例剖析 — Inngest + Fal 的 $200 之夜

这是典型案例。观察每条规则如何会捕获它。

**上线时的代码：**

```ts
// inngest function: generate images for a campaign
export const generateCampaign = inngest.createFunction(
  { id: 'gen-campaign' },                              // ❌ no concurrency limit
  { event: 'campaign/start' },
  async ({ event, step }) => {
    const prompts = await step.run('fetch', () => fetchPrompts(event.data.id));
    // ❌ unbounded fan-out, no per-run cap, no idempotency
    await Promise.all(prompts.map(p => fal.run('fal-ai/flux-pro', { input: { prompt: p } })));
  }
);
```

**出了什么问题。** `fetchPrompts` 有一个 bug：在瞬态数据库错误时，它返回部分列表*加上前一次运行的列表被追加*。Inngest 以其默认重试次数重试该函数（除初始尝试外还有多次尝试）。每次重试重新运行 `fetchPrompts`，每次重试列表翻倍（40 → 80 → 160 → 320 条 prompt）。`Promise.all` 将所有 320 条并发扇出。按 $0.05/图像：**$16/重试 × 夜间按计划重试的三角增长 ≈ 天亮时 $200。**

**为什么每条规则都能捕获它。**

| 规则 | 捕获方式 |
|---|---|
| 1. 成本合约 | 强制写明"每次运行最大调用次数"。数字 `prompts.length` 不是一个已知整数 → 规则不通过 → 写一个上限。 |
| 2. 具体迭代上限 | `Promise.all(prompts.map(...))` 没有整数上限 → 规则不通过 → 用 `MAX_IMAGES_PER_RUN` 包裹分块。 |
| 3. 重试策略 | Inngest 默认重试 × 无幂等键 = 双重计费的工作。规则强制要求每个 `(campaignId, promptHash)` 一个幂等键。 |
| 4. 并发限制 | `Promise.all` 是无界并发。规则强制 `p-limit(3)` 和 Inngest `concurrency: { limit: 3 }`。 |
| 5. 服务商硬性上限 | Fal Spend Limit $50/天会在 $50 而不是 $200 止住出血。 |
| 7. 放大器审计 | "自调度作业" — Inngest 的重试就是自调度。审计强制你考虑这一点。 |

**通过协议的修复：**

```ts
// cost contract:
//   provider: Fal flux-pro @ $0.05/image
//   max calls per run: 50
//   max $ per run: $2.50
//   provider hard cap: $50/day (set in Fal dashboard 2026-05-22)
//   concurrency: 3 (Inngest + p-limit, matching)
//   idempotency: key = `${campaignId}:${sha1(prompt)}` — provider-side dedup window 24h
const MAX_IMAGES_PER_RUN = 50;
const limit = pLimit(3);

export const generateCampaign = inngest.createFunction(
  {
    id: 'gen-campaign',
    concurrency: { limit: 3 },
    retries: 2,                                        // attempts = 1 + retries
  },
  { event: 'campaign/start' },
  async ({ event, step }) => {
    const prompts = await step.run('fetch', () => fetchPrompts(event.data.id));
    if (prompts.length > MAX_IMAGES_PER_RUN) {
      throw new NonRetriableError(
        `prompt count ${prompts.length} exceeds MAX_IMAGES_PER_RUN=${MAX_IMAGES_PER_RUN}`
      );
    }
    await Promise.all(prompts.map(p => limit(() => step.run(
      `img:${event.data.id}:${sha1(p)}`,               // idempotency key
      () => fal.run('fal-ai/flux-pro', { input: { prompt: p } })
    ))));
  }
);
```

注意：`fetchPrompts` 中的 bug 仍然存在。协议不修复那个 bug — 它让那个 bug 的成本从 **$200 变成 $2.50**，同时你去找到它。这就是纵深防御的全部意义。

## 常见失控模式及其钱包不变量

| 模式 | 要写入的钱包不变量 | 要设置的硬性上限 |
|---|---|---|
| 对项目列表的扇出 | `total_cost ≤ list_len × unit_cost ≤ MAX_$_PER_RUN` | 服务商每日支出上限 |
| 瞬态错误重试 | `total_cost ≤ attempts × unit_cost`，attempts ≤ 5 | 服务商每日支出上限；50% 时告警 |
| 智能体循环（"让模型决定下一步"） | `total_cost ≤ MAX_STEPS × per_step_cost`，depth ≤ MAX_DEPTH | 按智能体运行的成本天花板，kill-switch |
| 轮询等待作业完成 | `total_cost ≤ ceil(MAX_WAIT_MS / poll_interval) × poll_cost` | 绝对截止时间 + 告警 |
| Webhook 处理器 → API 调用 | 必须有幂等键；如果 webhook 由同一 API 触发则存在循环 | 服务商按 key 的速率限制 |
| 流重连 | `attempts ≤ MAX_RECONNECTS`，带上限的指数退避 | 服务商连接上限 |
| 缓存未命中踩踏 | singleflight → `cost ≤ 1 × unit_cost` 每 key 每窗口 | 不适用（代码中去重） |
| 自调度作业 | 递归深度由台账行限定，而非由代码 | 调度器级去重 + 每天最大运行次数 |
| 多服务商回退 | 跨服务商总和 ≤ MAX_$_PER_RUN | 每个服务商单独设硬性上限 |

## 各服务商速查表

在首次部署**之前**设置这些。它们都不需要代码更改。

### Fal.ai
- Dashboard → **Billing → Spend Limit**。每日和每月硬性上限。超出即硬性停止。
- 按**环境**（dev / staging / prod）使用 per-API-key，并在 dev 环境设置低上限。
- Webhook：投递是计费的；在你的侧限制重试。

### Anthropic
- Console → **Workspaces** → 按环境创建 Workspace。
- 每个 Workspace 设一个 **Budget**，包含**硬性上限**（阻止请求）和**软性上限**（邮件告警）。
- 使用按 Workspace 的 API key — 泄露的 dev key 无法超过 dev Workspace 预算。
- Prompt caching 对重复上下文可降低约 90% 成本；上限基于未混合成本，因此 caching 可延伸预算。

### OpenAI
- ⚠️ **按项目的月度预算仅是软性的。** OpenAI 帮助中心将项目预算记录为"软支出阈值"，只发送告警但**不**执行硬性上限。失控可以继续超过记录的项目预算。
- 真正的硬性上限，请使用以下之一：
  - **组织级 Usage limits**（Org → Settings → Limits）— 超出时阻止请求。
  - API 前面的计费网关/代理，执行 fail-closed 预算。
  - 你自己的 fail-closed 预算检查代码，拒绝超过已记账 $-cap 的调用。
- 按环境（dev/staging/prod）使用单独的项目以便归因和告警，但不要依赖项目预算作为硬性停止。

### Replicate
- Account → **Billing → Spend limit**。账户级硬性上限。
- 按环境使用单独 token；泄露时轮换。

### ElevenLabs
- Workspace → **Usage limits**。按 API key 设置。
- 语音克隆按字符计费；在代码中 AND 按 key 限制字符数。

### Inngest（队列层 — 不是付费 AI，但是倍增器）
- 每个调用付费 API 的函数上设 `concurrency: { limit: N }`。
- `retries: 2`（Inngest 默认是 **4 次重试**，即包含初始尝试最多 5 次 — 请对照当前 Inngest 文档确认）用于付费调用函数；幂等失败时更少尝试。最坏情况的钱包计算：`attempts = 1 + retries`，所以默认的 `step.run()` 可以计费 **5 倍**，而不是 4 倍。
- `NonRetriableError` 用于 4xx — 永远不要将 4xx 重试到付费 API。
- `idempotency: ...` 用于你无法在调用点去重的事件。

## 上线前要枚举的边界情况

| 场景 | 预期行为 |
|---|---|
| 空输入列表 | 0 次调用，0 成本，提前返回 — 甚至不要认证 |
| 输入列表超过 MAX | 以 NonRetriableError 拒绝，不部分处理 |
| 所有调用以 4xx 失败 | 每个尝试 1 次，不重试，暴露错误 |
| 所有调用以 5xx 失败 | 有界重试，总成本 ≤ attempts × unit，完全耗尽时告警 |
| 同一作业的并发调用 | 幂等键去重；第二次调用成本 $0 |
| 批处理中途网络分区 | 已计入部分成本；恢复时幂等键防止重复计费 |
| 服务商速率限制（429） | 遵守 `Retry-After`；不要在 SDK 内外乘以重试 |
| 服务商重试 webhook | 在处理器边界做幂等 |
| 本地 dev 意外指向 prod key | 按环境的 key + 按环境的上限使其成本为 $0.50，而不是 $50 |
| 上一次运行仍在执行时 Cron 触发 | 并发限制 = 1 或显式的重叠容忍设计 |

## 输出纪律

你产出的代码必须：

- 在每个调用点上方有一个 `// cost contract:` 块，包含四个数字（单位成本、最大调用次数、最大 $/运行、服务商硬性上限设置）。
- 使用命名常量（`MAX_IMAGES_PER_RUN`、`MAX_AGENT_STEPS`）作为上限 — 绝不在行内使用魔术数字。
- 将扇出包裹在 `p-limit` 或等效物中 — 绝不在付费 API 上使用原始 `Promise.all`。
- 为每个变更/计费调用传递幂等键。
- 在同一文件中设置队列级并发和重试，或将其文档化。
- 通过 `NonRetriableError` 或等效物拒绝 `4xx` 重试。
- 按名称引用服务商硬性上限设置（"Fal Spend Limit $50/天，设置于 2026-05-22"），让未来的读者知道它存在。

## 相关技能

- **invariant-guard** — 当调用付费 API 的循环或递归没有书面终止度量时。终止是钱包上限的前提条件；invariant-guard 建立它，runaway-guard 限定成本。
- **complexity-cuts** — 当失控已经上线且你正在诊断意外账单时。将意外扇出视为复杂度 bug，写一个特征测试，然后一次变换一步。
- **lemmaly** — 当设计扇出付费调用的新智能体循环或批量管道时。先选算法和数据结构；然后回到这里为每步设置钱包不变量。
- **mathguard** — 当成本驱动因素是次线性算法问题（向量搜索、sketching、FFT）上的计算而非按调用计费时；mathguard 设定决定每次调用工作量的算法下限。

## 需要警惕的辩解

| 借口 | 现实 |
|---|---|
| "我只是在本地测试。" | 本地访问的付费端点是同一个。测试代码中的重试 bug 花的是同样的美元。 |
| "列表很小，扇出没问题。" | 列表*今天*很小。下周它来自一个增长了 50 倍的表。上限是为下周准备的。 |
| "Inngest 已经重试了，所以我不需要重试策略。" | Inngest 重试 × 你的重试包装器 × SDK 重试 = 27 次尝试。每次都计费。 |
| "API 调用很便宜，$0.001。" | 10,000 次意外调用就是 $10 — 而这个数量恰恰是你没能限定的。 |
| "我稍后设服务商上限。" | bug 在"稍后"之前就上线了。花 60 秒设好上限；代码可以等。 |
| "幂等对此是小题大做。" | Webhook 会重试。负载均衡器会重试。浏览器会重试。没有幂等键，*总有什么东西*会重复。 |
| "我们有监控，会发现的。" | 监控在花掉 $200 后才发现。上限防止 $200 被花掉。 |
| "它显然会终止。" | $200/晚的事故也"显然会终止"。写下整数上限。 |

如果在思考过程中这些听起来很熟悉：停下来，写成本合约，设服务商上限，然后再写代码。

## 红旗 — 先停下来写成本合约

- 正要写 `await Promise.all(items.map(x => paidApi(x)))` 而没有 `p-limit`。
- 正要写 `while (!done) await paidApi(...)` 而没有整数上限。
- 正要写一个"让模型决定何时停止"的智能体循环。
- 正要写一个重试包装器，而调用已经被 Inngest / SDK / 框架重试了。
- 正要部署一个付费 API key 而没有先设服务商仪表盘上限。
- 正要将付费 API key 提交到跨环境共享的 `.env` 中。
- 正要处理一个调用产生该 webhook 的 API 的 webhook。
- "就今晚" — 夜间恰恰是失控循环计费最多的时候。

所有这些都意味着：停下来，写成本合约，设服务商上限，然后再写代码。

## 验证清单

在上线任何调用付费 API 的代码之前：

- [ ] 每个调用点上方存在成本合约注释，包含单位成本、最大调用次数/运行、最大 $/运行、服务商上限。
- [ ] 迭代/扇出上限是一个命名整数常量，不是隐含在列表长度中。
- [ ] 并发限制在代码中（`p-limit`）AND 在队列层（`Inngest concurrency`）都设置了。
- [ ] 重试策略是显式的：最大尝试次数、4xx → 不重试、每次调用的幂等键。
- [ ] 服务商仪表盘硬性上限已设置，且值记录在文件中。
- [ ] 按环境的 API key；dev key 的上限低于 prod。
- [ ] 已执行放大器审计（规则 7），要么"均不适用"要么逐一处理。
- [ ] 存在以下测试：空输入、超大输入被拒绝、4xx 不被重试、幂等键去重重复调用。
- [ ] 在最坏情况下代码计费 ≤ MAX_$_PER_RUN，即使有 bug 服务商上限也将损失止于 MAX_$_PER_DAY。

无法勾选每一项？代码只是示例正确的，不是账单正确的。要么填补差距，要么不连接已启用计费的 key。

## 局限性

- **不是计费系统。** runaway-guard 在代码编写时强制执行*意图*（上限、合约、审计）。它不在生产环境中计量支出 — 将其与服务商的硬性上限和可观测性（LLM 成本仪表盘、日志告警）配合使用以实现运行时执行。
- **服务商侧上限可能需要几分钟才能生效。** Anthropic Workspace Budget、OpenAI usage limits 和 Fal Spend Limits 的对账延迟以分钟而非毫秒计。单个窗口内的病态突发仍可能略微超过上限。
- **对新模型没有自动成本估算。** 成本合约数字（单位成本、$/运行）是作者必须查找的输入；该技能不维护按模型的价格表。
- **流式和按 token 计费。** 对于按 token 的 API（Anthropic、OpenAI），`max calls` 是一个代理 — 真正的上限是 `max input tokens × max output tokens × per-token rate`。调整协议：将 `max calls per run` 替换为 `max tokens per run`。
- **按计算计费的服务商。** 对于按秒计费的长时间运行 GPU 作业（训练、视频编码），将合约中的"调用"替换为"GPU-秒"；纪律相同但单位不同。
- **不替代事件响应。** 当账单已经到达时，升级到 `complexity-cuts` 进行纠正性重写 — runaway-guard 预防下一个，而不是当前的。

## 论点，一行总结

> **时间上限防止卡死。空间上限防止 OOM。美元上限防止 $200 的早晨。AI 助手默认执行前两个而忽略第三个。runaway-guard 让它们优先考虑钱包。**
