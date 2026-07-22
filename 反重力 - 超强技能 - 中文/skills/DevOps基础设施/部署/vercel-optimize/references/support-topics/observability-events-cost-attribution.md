---
id: observability-events-cost-attribution
title: Observability Events cost attribution
status: active
candidateKinds: ["observability_events_attribution"]
frameworks: ["*"]
priority: 92
citations: ["https://vercel.com/docs/observability/observability-plus", "https://vercel.com/docs/alerts"]
maxBriefChars: 900
---

## 调查简报
Observability Events 是 Observability Plus 下的计量 SKU。当当前账单显示大量 Observability Events 份额时，事件量就是杠杆。减少上游：提高缓存命中率、收窄中间件匹配器、减少不必要的自定义 span 基数。

## 需要检查的证据
从 `usage.services` 验证份额。交叉引用 `requestsByRouteCache`、`middlewareCount`、外部 API span 计数和第三方跟踪（`tracesSampleRate=1`）。

## 何时不建议
在低于 15% 份额时跳过。当热门路由的缓存命中率已经 >90% 时跳过——杠杆在其他地方。除非特定的计量信号有记录的采样控件，否则不要提出采样。

## 验证
命名份额、上游驱动因素以及每个驱动因素的具体修复，而不是通用的"减少事件"。