---
id: cache-components-suspense-dedupe-pitfall
title: Cache Components Suspense dedupe pitfall
status: active
candidateKinds: ["cache_components_suspense_dedupe"]
frameworks: ["next@>=16.0.0"]
scannerPatterns: ["cache-components-suspense-dedupe"]
priority: 87
citations: ["https://nextjs.org/docs/app/api-reference/directives/use-cache", "https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents", "https://nextjs.org/docs/app/guides/migrating-to-cache-components"]
maxBriefChars: 900
---

## 调查简报
默认的 `'use cache'` 不会在同一次渲染中跨独立 `<Suspense>` 边界对相同调用去重。每个边界重新调用缓存函数，会成倍增加函数时长和 ISR 写入抖动。

## 需要检查的证据
确认扫描器发现的重复 fetch URL 或辅助函数名称。验证调用站点在同一路由段内并位于不同的 `<Suspense>` 边界中。交叉引用 `fnDurationP95ByRoute` 和 `isrWritesByRoute` 以获取所属路由。

## 何时不建议
如果重复调用是有意的（不同参数、不同意图），跳过。如果重复位于已经应用请求内记忆化的单个组件主体中，跳过。

## 验证
命名重复的调用、计数，以及：(a) 要提升的页面级 promise，或 (b) 要移动到 `'use cache: remote'` 的函数。