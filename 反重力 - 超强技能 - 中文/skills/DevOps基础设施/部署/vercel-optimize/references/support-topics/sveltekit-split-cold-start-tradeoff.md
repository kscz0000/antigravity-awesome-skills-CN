---
id: sveltekit-split-cold-start-tradeoff
title: SvelteKit split function cold-start tradeoff
status: active
candidateKinds: ["cold_start", "slow_route"]
frameworks: ["sveltekit@*"]
priority: 82
citations: ["https://vercel.com/docs/frameworks/full-stack/sveltekit", "https://svelte.dev/docs/kit/adapter-vercel"]
maxBriefChars: 800
---

## 调查简报
SvelteKit 默认将路由捆绑在一起以避免过度冷启动。将 `split: true` 视为有针对性的权衡，而不是包罗万象的优化。

## 需要检查的证据
使用冷启动份额、冷热延迟对比、部署集中度以及源 bundle 压力。检查 adapter 选项以及大型依赖项是属于一个路由还是整个应用。

## 何时不建议
不要在没有函数大小压力或路由本地初始化成本证据的情况下拆分每个路由。如果冷启动已经是主导问题，不要拆分。

## 验证
命名冷启动信号、激发拆分的路由或依赖项以及确切 adapter 配置行。