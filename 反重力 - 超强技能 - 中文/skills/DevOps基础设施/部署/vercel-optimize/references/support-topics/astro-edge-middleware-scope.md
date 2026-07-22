---
id: astro-edge-middleware-scope
title: Astro edge middleware scope
status: active
candidateKinds: ["middleware_heavy"]
frameworks: ["astro@*"]
priority: 88
citations: ["https://vercel.com/docs/frameworks/frontend/astro", "https://docs.astro.build/en/guides/integrations-guide/vercel/"]
maxBriefChars: 800
---

## 调查简报
Astro 中间件可以在边缘为广泛的请求集运行。如果中间件量很高，证明哪些路径实际上需要拦截。

## 需要检查的证据
使用中间件调用份额和热门路径。检查 adapter 中间件模式、中间件源、鉴权/重定向逻辑，以及静态资产、预渲染页面或公共页面是否正在被拦截。

## 何时不建议
不要绕过必需的鉴权、区域、头或路由逻辑。当当前范围已经是最小时，不要将全局中间件工作移到每个页面。

## 验证
命名中间件份额、主要路径、当前中间件模式以及要收窄的确切源或配置行。