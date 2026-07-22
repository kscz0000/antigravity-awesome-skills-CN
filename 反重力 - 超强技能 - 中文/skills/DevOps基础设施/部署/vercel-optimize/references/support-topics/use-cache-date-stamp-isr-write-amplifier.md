---
id: use-cache-date-stamp-isr-write-amplifier
title: "'use cache' date-stamp ISR write amplifier"
status: active
candidateKinds: ["use_cache_date_stamp"]
frameworks: ["next@>=15.0.0"]
scannerPatterns: ["use-cache-date-stamp"]
priority: 88
citations: ["https://nextjs.org/docs/app/api-reference/directives/use-cache", "https://nextjs.org/docs/app/api-reference/functions/cacheLife"]
maxBriefChars: 900
---

## 调查简报
`'use cache'` 按参数标识和预渲染输出进行键控。烘焙进缓存输出的 `new Date()`、`Date.now()` 或 `Math.random()` 即使数据未变，也会强制每次重新生成时进行新的 ISR 写入。

## 需要检查的证据
检查扫描器发现的 `subtype`：`module-scope`（模块级日期）或 `in-cache-fn`（在缓存体内）。交叉引用 `isrWritesByRoute`——针对低读取的稳定写入率是症状。

## 何时不建议
如果日期位于 `useEffect`/`useCallback`/`useMemo` 内，则跳过。如果 `'use cache'` 只是注释，则跳过。如果日期是预期的缓存键，则跳过。

## 验证
命名文件、特定的原始调用以及替代方案：构建时常量或客户端 `useEffect`。