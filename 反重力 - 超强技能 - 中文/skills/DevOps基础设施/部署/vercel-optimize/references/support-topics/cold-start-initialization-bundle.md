---
id: cold-start-initialization-bundle
title: Cold-start initialization and bundle weight
status: active
candidateKinds: ["cold_start"]
frameworks: ["*"]
priority: 92
citations: ["https://vercel.com/docs/functions/debug-slow-functions", "https://vercel.com/docs/functions/limitations", "https://vercel.com/docs/functions/runtimes"]
maxBriefChars: 850
---

## 调查简报
冷启动候选需要代码路径检查，而不仅仅是项目设置检查。首先证明冷请求是否为导入、模块作用域设置、运行时选择或依赖项权重付费。

## 需要检查的证据
使用 `startTypeSplit`、`coldVsWarmLatencyP95` 和 `coldByDeployment`。在源代码中，检查模块作用域 SDK 设置、数据库/客户端构造、顶层网络调用、重型依赖、运行时导出和部署局部更改。

## 何时不建议
当温热请求同样缓慢时，不要归咎于冷启动。在证明初始化或运行时压力之前，不要推荐保活流量或更多内存。

## 验证
命名冷启动份额、冷热对比 gap，以及解释它的确切初始化、依赖项或运行时行。