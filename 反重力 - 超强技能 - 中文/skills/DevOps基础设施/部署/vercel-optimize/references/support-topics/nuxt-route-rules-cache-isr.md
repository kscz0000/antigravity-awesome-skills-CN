---
id: nuxt-route-rules-cache-isr
title: Nuxt routeRules cache and ISR
status: active
candidateKinds: ["uncached_route", "isr_overrevalidation", "rendering_candidate"]
frameworks: ["nuxt@>=3.0.0"]
priority: 90
citations: ["https://vercel.com/docs/frameworks/full-stack/nuxt", "https://nuxt.com/docs/4.x/api/utils/define-route-rules", "https://nuxt.com/docs/4.x/guide/concepts/rendering"]
maxBriefChars: 850
---

## 调查简报
对于 Vercel 上的 Nuxt，路由级缓存通常属于 `routeRules`。将杠杆与路由匹配：静态页面预渲染、共享内容 ISR、请求特定视图 SSR。

## 需要检查的证据
检查 `nuxt.config`、内联路由规则、服务器路由、页面、鉴权/会话读取以及观察到的缓存或 ISR 读/写模式。验证路由是否应该是 Vercel 缓存支持的 ISR 而不是通用 SWR。

## 何时不建议
不要缓存已认证、购物车、结账、预览或每用户路由。不要在未证明路由是公共的且新鲜度窗口可接受的情况下添加 routeRules。

## 验证
命名观察到的路由信号、当前 routeRule 或缺少的规则、选择的缓存模式以及确切配置行。