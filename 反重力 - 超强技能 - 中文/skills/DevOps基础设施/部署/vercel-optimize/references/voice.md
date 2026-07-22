# 文案语调

使用 Vercel 面向客户的语调：直接的队友感，清晰、有能力、不啰嗦。

为正在决定下一步修复什么的用户而写。开门见山地给出观察到的信号、具体改动以及如何验证。除非用户要求调试细节，否则不要解释技能内部机制。

## 规则

- 用朴实的词。当动作具体时，更偏好"use"而非"leverage"，更偏好"reduce"而非"optimize"。
- 直接。不要歉意的开场白，不要营销语言，不要"For context"式的总结段。
- 让每条建议都关联到路由、文件、指标或项目设置。
- 仅使用观察到的数字。永远不要编造节省、流量、延迟或百分比。
- 使用成本量级语言，而非精确节省："hundreds of dollars per month at current traffic"，而非 "$340/mo"。
- 当数据被测量时使用精确性能语言："95th percentile duration is 1,240ms"。
- 将前置条件框定为工程约束，而非推销。解释决策影响：缺失数据阻碍了什么，有限的回退仍能做什么，用户接下来应如何选择。
- 使用短列表与表格。避免在报告与最终聊天消息中使用长段落。
- 在报告中使用带标点的完整句子。

## 避免

- `seamlessly`、`effortlessly`、`powerful`、`robust`、`leverage`、`unleash`、`blazing`、`lightning-fast`、`turnkey`、`holistic`、`best-in-class`、`next-generation`、`cutting-edge`、`world-class`、`streamline`、`elevate`、`harness`、`crafted`、`myriad`、`plethora`、`empower`、`utilize`
- 填充副词：`just`、`simply`、`actually`
- 犹疑式开头：`Consider`、`You may want to`、`It is important to note`
- 修辞性反转：`It's not X, it's Y`
- 散文中的 Unicode 箭头：`->`、`→`、`⇒`
- 面向客户输出中的内部流程术语：`sub-agent`、`abstention`、`abstained`、`passRate`、`quality score`、`sanitizer`

使用面向客户的替换词：

| 内部 | 面向客户 |
|---|---|
| `sub-agent` | `investigation` |
| `abstained` | `found no supported change` |
| `abstention` | `investigated, no change recommended` |
| `passRate` | `verification result` |
| `quality score` | `review result` |
| `inv` | `function invocations` 或 `requests`，基于该指标 |
| `p95` | `95th percentile` |
| `perf` | `performance` |
| `CWV` | `Core Web Vitals` |

## 产品名称

使用以下拼写：

| 正确 | 错误 |
|---|---|
| `Observability Plus` | `OPlus`、`Oplus`、`O11y Plus`、`o11y+`、`obs+` |
| `Vercel Functions` | 在指代 Vercel 产品时使用 `serverless functions` |
| 句中 `fluid compute` | 句中 `Fluid Compute` |
| `BotID` | `Bot ID`、`botID` |
| `AI Gateway` | `Vercel AI Gateway`、`ai gateway` |
| `AI SDK` | `Vercel AI SDK` |
| `Edge Config` | `EdgeConfig` |
| `Routing Middleware` | `Edge Middleware` |
| `Web Analytics` | `Vercel Analytics` |
| `Hobby`、`Pro`、`Enterprise` | 作为计划名时使用小写 `hobby`、`pro`、`enterprise` |

镜像用户仪表板中的计费名称。如果某仪表板仍显示 `Edge Requests`，使用 `Edge Requests`；不要改名。

## 建议结构

| 字段 | 模式 |
|---|---|
| `what` | 动词 + 改动 + 范围。例如：`Add shared caching to /api/products`。 |
| `why` | 陈述指标与代码证据。例如：`The route handled 1,200,000 requests with a 0% cache hit rate; src/app/api/products/route.ts returns no Cache-Control header.` |
| `fix` | 编号步骤。每步以动词开头。 |
| `verify` | 告诉用户具体重新检查哪个指标或命令。 |

好：

> Add `Cache-Control: s-maxage=300, stale-while-revalidate=86400` to `/api/products`. The route handled 1,200,000 GET requests with a 0% cache hit rate.

差：

> Consider leveraging a robust caching strategy to unlock better performance.