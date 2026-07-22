---
id: middleware-proxy-edge-cost
title: Middleware edge cost
status: active
candidateKinds: ["middleware_heavy"]
frameworks: ["next@>=12.0.0"]
priority: 90
citations: ["https://nextjs.org/docs/app/building-your-application/routing/middleware", "https://vercel.com/docs/routing-middleware"]
maxBriefChars: 850
---

## 调查简报
中间件建议应减少不必要的拦截，而不是删除必需的请求处理。

## 需要检查的证据
使用 `topMiddlewarePaths` 和 matcher 配置。确认哪些路径需要鉴权、重写、头或区域处理。检查静态资产、图像或不需要中间件的路由是否被匹配。

## 何时不建议
不要以绕过必需的鉴权或路由行为的方式收窄 matcher。当当前 matcher 已经收窄时，不要将中间件工作移到每个路由。

## 验证
说明当前中间件份额、主要匹配路径以及要更改的确切 matcher 行。