---
id: database-egress-pooling-region
title: Database region and connection pressure
status: active
candidateKinds: ["slow_route"]
frameworks: ["*"]
priority: 60
citations: ["https://vercel.com/docs/regions", "https://vercel.com/docs/functions", "https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package", "https://vercel.com/docs/functions/limitations"]
maxBriefChars: 800
---

## 调查简报
仅当源和指标都指向下游 I/O 而非进程内计算时，才推荐数据库或区域更改。

## 需要检查的证据
比较 `cpu.p95` 与 `latency.p95`，然后检查数据库 await、查询扇出、连接创建、池生命周期处理以及项目文件中配置的区域。

## 何时不建议
除非仓库和项目配置证明适用，否则不要命名数据库提供者、池产品或区域更改。

## 验证
将发现与观察到的墙钟 gap 以及确切的查询、池或区域配置行相关联。