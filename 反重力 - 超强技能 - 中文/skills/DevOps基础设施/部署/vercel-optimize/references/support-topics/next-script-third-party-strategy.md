---
id: next-script-third-party-strategy
title: Next.js third-party script strategy
status: active
candidateKinds: ["cwv_poor"]
frameworks: ["next@*"]
metrics: ["LCP", "INP"]
priority: 85
citations: ["https://nextjs.org/docs/app/api-reference/components/script", "https://web.dev/articles/optimize-inp"]
maxBriefChars: 850
---

## 调查简报
第三方脚本仅当它们与不佳的指标和路由一致时才是可操作的。对于 LCP 或 INP，证明特定脚本阻塞关键渲染、水合或交互。

## 需要检查的证据
检查 `next/script`、原始 `<script>`、标签管理器、聊天小部件、分析和同意代码。检查 `beforeInteractive`、`afterInteractive`、`lazyOnload` 以及脚本是路由本地还是全局。

## 何时不建议
不要在没有产品证据的情况下将必需的 bot 检测、同意、鉴权或支付脚本移到后面。不要为 App Router 推荐 `worker`。

## 验证
命名不佳的指标、脚本源、当前策略以及要更改的确切路由或布局行。