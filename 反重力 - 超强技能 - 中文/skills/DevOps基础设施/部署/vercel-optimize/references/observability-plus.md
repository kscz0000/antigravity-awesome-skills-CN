# Observability Plus 停止并询问

仅当 `signals.observabilityPlusBlocker` 已设置时使用此文件。除非用户选择该路径，否则不要静默继续到仅扫描器模式。

## 为何存在此检查

这是数据依赖，而不是升级推销。本技能通过观察到的路由行为来排序工作，以便将热门、昂贵的路径与仅看起来可疑的代码分开。这些闸门需要每路由指标：

| 闸门 | 必需信号 |
|---|---|
| `slow_route` | 各路由的函数时长与调用次数 |
| `uncached_route` | 各路由的缓存结果与请求次数 |
| `cold_start` | 各路由的函数启动类型 |
| `route_errors` | 各路由的函数状态 |
| `isr_overrevalidation` | 各路由的 ISR 读写 |
| `middleware_heavy` | 中间件调用与时长 |
| `cwv_poor` | 各路由的 Core Web Vitals |
| `platform_bot_protection` | 按 bot 类别的 Fast Data Transfer |

仅扫描器模式仍然能捕获与流量无关的代码问题，但无法对最热门的路由排序或证明成本影响。在继续之前明确说明该权衡。

## 用户模板

首先渲染此模板，然后等待用户的选择。仅替换 `<detail>`。不要加开场白；标题就是开场行。

```md
**Per-route metrics are unavailable.**

<detail>

This audit needs route-level metrics to rank fixes by observed latency, cache hit rate, error rate, cold-start rate, and Incremental Static Regeneration reads and writes. Without them, I can run a scanner-only audit for traffic-independent code issues, but I cannot tell which routes matter most or prove cost impact.

Docs: https://vercel.com/docs/observability/observability-plus

Choose one:
1. Enable Observability Plus, then re-run the metric-backed audit.
2. Continue in scanner-only mode for a limited audit.
```

如果宿主支持结构化问题工具，请使用此精确的面向客户文案。不要重写它。

```json
{
  "question": "Enable Observability Plus and re-run, or continue with a limited scanner-only audit?",
  "header": "Observability Plus",
  "options": [
    {
      "label": "Enable and re-run",
      "description": "Use route-level metrics to rank the routes that matter most for cost and performance."
    },
    {
      "label": "Run scanner-only",
      "description": "Check traffic-independent code patterns without route ranking or proven cost impact."
    }
  ]
}
```

在该问题中使用完整产品名称。不要在面向客户的 blocker 文案中缩写产品名称或指标。

## 用户选择之后

如果用户选择 **Enable and re-run**，在此简短响应之后停止：

```md
Enable Observability Plus from the Vercel dashboard's Observability tab, then tell me to rerun. I'll restart the metric-backed audit once route-level metrics are available.
```

不要包含原始团队 ID、组织 ID、项目 ID、定价语言、仪表板截图或额外的说服内容。blocker 消息中的文档链接已涵盖可用性和计费细节。

如果用户选择 **Run scanner-only**，请继续下面的仅扫描器步骤。

## Blocker 文案

| Blocker | 详情 |
|---|---|
| `payment_required` | `Detected: route-level metrics were recognized for this team, but these metric queries are not usable.` |
| `no_oplus_probe` | `Detected: this team does not expose the route-level metrics this audit needs.` |
| `not_linked` | `Detected: this app directory is not linked to a Vercel project.` |
| `forbidden` | `Detected: the Vercel CLI is authenticated to a team that cannot read this project.` |
| `project_not_found` | `Detected: the project ID is not visible to the authenticated team.` |
| `project_disabled` | `Detected: route-level metrics are enabled for the team but disabled for this project.` |
| `all_failed_other` | `Detected: every per-route metric query failed. Error code: <code>.` |

对于 `not_linked`，不要使用 Observability Plus 模板。先链接应用目录：

```bash
vercel link --yes --project <project-name-or-id> --cwd <app-dir>
```

团队已知时添加 `--team <team-id-or-slug>`。如果用户同时提供了应用路径和项目名称，请运行 link 命令而不是询问用户该做什么。

对于 `forbidden` 和 `project_not_found`，在呈现 Observability Plus 选择之前，要求用户确认精确的 Vercel 项目和团队/个人 scope。

对于 `project_disabled`，不要将其呈现为团队订阅问题。要求用户为该项目启用 Observability Plus，然后重跑。

对于 `no_traffic`，不要使用此模板。告诉用户该项目在 14 天窗口内没有有意义的流量，然后询问是在流量积累后立即运行仅扫描器模式还是稍后再来。

## 仅扫描器模式

如果用户选择仅扫描器模式：

1. 如果当前 `signals.json` 在快速 blocker 处停止（`usageError=NOT_COLLECTED_OBSERVABILITY_BLOCKED` 或 `project=null`），则重新运行 `node scripts/collect-signals.mjs [projectId] --continue-without-observability > "$RUN_DIR/vercel-signals.json" 2> "$RUN_DIR/collect.stderr"`。
2. 运行代码扫描器。
3. 仅启动与流量无关的发现。
4. 呈现清晰的数据缺口：由于 Observability Plus 数据不可用，每路由指标闸门被跳过。

不要暗示仅扫描器报告是一次完整的优化审计。