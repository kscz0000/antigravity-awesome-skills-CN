---
id: next-image-lcp-preload-sizes
title: Next.js image LCP preload and sizes
status: active
candidateKinds: ["cwv_poor"]
frameworks: ["next@*"]
metrics: ["LCP"]
priority: 86
citations: ["https://nextjs.org/docs/app/api-reference/components/image", "https://web.dev/articles/optimize-lcp"]
maxBriefChars: 850
---

## 调查简报
对于不佳的 LCP，在触及不相关的 JavaScript 之前，确定 LCP 元素是否为图像。Hero 图像需要正确的尺寸、优先级行为和源缓存卫生。

## 需要检查的证据
检查首屏媒体的 `next/image`、没有 `sizes` 的 `fill`、Next.js 16 上已弃用的 `priority`、缺少 `preload` 或 `fetchPriority`、过大的尺寸以及远程图像的 TTL/源行为。

## 何时不建议
不要预加载多个可能的 LCP 图像或将微小图标/SVG UI 资产路由到图像优化。不要在未检查源更新语义的情况下更改质量或 TTL。

## 验证
命名 LCP 值、图像元素或组件、当前属性/配置以及要更改的确切行。