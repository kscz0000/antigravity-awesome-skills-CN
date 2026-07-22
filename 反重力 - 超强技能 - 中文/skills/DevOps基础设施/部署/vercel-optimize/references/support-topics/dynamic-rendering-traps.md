---
id: dynamic-rendering-traps
title: Dynamic rendering traps
status: active
candidateKinds: ["rendering_candidate"]
frameworks: ["next@>=13.0.0"]
priority: 90
citations: ["https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config", "https://nextjs.org/docs/app/api-reference/functions/generate-static-params", "https://nextjs.org/docs/app/building-your-application/rendering/partial-prerendering"]
maxBriefChars: 850
---

## 调查简报
只有当动态行为是偶然的，渲染候选才是可操作的。首先证明路由可以是静态、ISR 或部分静态的。

## 需要检查的证据
检查 `dynamic`、`revalidate`、`generateStaticParams`、路由参数以及动态 API（如请求头或 cookies）。检查动态调用是否在布局中，因为这可能影响更大的路由树。

## 何时不建议
不要为鉴权、个性化、草稿模式、每请求重定向或请求特定数据删除动态渲染。

## 验证
建议必须引用动态触发器，并解释为什么目标路由可以容忍静态或 ISR 行为。