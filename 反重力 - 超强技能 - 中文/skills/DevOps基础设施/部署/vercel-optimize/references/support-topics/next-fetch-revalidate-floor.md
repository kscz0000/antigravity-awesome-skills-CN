---
id: next-fetch-revalidate-floor
title: Next.js fetch revalidation floor
status: active
candidateKinds: ["uncached_route", "isr_overrevalidation"]
frameworks: ["next@>=13.0.0"]
priority: 88
citations: ["https://nextjs.org/docs/app/api-reference/functions/fetch", "https://nextjs.org/docs/app/building-your-application/caching"]
maxBriefChars: 850
---

## 调查简报
Next.js `fetch` 选项可以设置路由的有效缓存下限。低 `revalidate`、`revalidate: 0` 或 `cache: 'no-store'` 可以解释未缓存流量和过多的 ISR 工作。

## 需要检查的证据
检查路由树的 `fetch` 调用。比较路由重新验证与每 fetch 的 `cache`、`next.revalidate`、标签、动态 API 以及具有冲突选项的重复 URL。

## 何时不建议
除非源证明陈旧读取是可接受的，否则不要为定价、库存、鉴权、草稿或用户特定的数据提高新鲜度窗口。

## 验证
命名观察到的缓存或 ISR 信号、控制路由的最低缓存设置以及要更改的确切 fetch 行。