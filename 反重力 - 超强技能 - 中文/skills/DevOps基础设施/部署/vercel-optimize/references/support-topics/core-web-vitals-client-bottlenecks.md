---
id: core-web-vitals-client-bottlenecks
title: Core Web Vitals client bottlenecks
status: active
candidateKinds: ["cwv_poor"]
frameworks: ["*"]
priority: 90
citations: ["https://vercel.com/docs/speed-insights", "https://web.dev/articles/vitals", "https://web.dev/articles/optimize-lcp", "https://web.dev/articles/optimize-inp", "https://web.dev/articles/optimize-cls"]
maxBriefChars: 850
---

## 调查简报
Core Web Vitals 候选需要针对指标的调查。LCP、INP 和 CLS 通常具有不同的原因和修复方法。

## 需要检查的证据
首先在深入调查中使用不佳的指标。对于 LCP，检查服务器响应和关键媒体。对于 INP，检查重型客户端 JavaScript 和交互处理程序。对于 CLS，检查尺寸、字体和注入的内容。

## 何时不建议
不要发出通用的"改进 Web Vitals"建议。不要针对该路由未不佳的指标进行优化。

## 验证
命名不佳的 p75 指标、其值，以及该指标背后的确切源机制。