---
id: astro-output-mode-and-isr
title: Astro output mode and ISR
status: active
candidateKinds: ["uncached_route", "rendering_candidate"]
frameworks: ["astro@*"]
priority: 90
citations: ["https://vercel.com/docs/frameworks/frontend/astro", "https://docs.astro.build/en/guides/on-demand-rendering/", "https://docs.astro.build/en/reference/configuration-reference/"]
maxBriefChars: 850
---

## 调查简报
Astro 默认是静态输出；`server` 输出使页面按需渲染，除非路由级预渲染改变这一点。首先决定热路由是否真正需要 SSR。

## 需要检查的证据
检查 `astro.config`、adapter 选项、`output`、路由级 `prerender`、动态参数、中间件，以及内容是否在访问者之间共享。比较路由缓存结果和请求量。

## 何时不建议
不要预渲染或缓存个性化、预览、购物车、结账或鉴权守护的页面。当一个路由级标志就足够时，不要为整个应用更改输出模式。

## 验证
命名 Astro 输出模式、路由级预渲染状态、观察到的路由信号，以及确切要更改的配置或页面行。