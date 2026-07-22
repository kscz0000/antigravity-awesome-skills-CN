---
id: function-region-misconfiguration-ttfb
title: Function region misconfiguration (TTFB)
status: active
candidateKinds: ["region_misconfig"]
frameworks: ["*"]
scannerPatterns: ["region-pin-in-config"]
priority: 85
citations: ["https://vercel.com/docs/functions/configuring-functions/region", "https://vercel.com/docs/regions"]
maxBriefChars: 950
---

## 调查简报
单个函数区域被固定。每区域 TTFB 数据今天不可用（`evidence.dataGap`）；将其视为审计提示——在推荐更改之前对照用户地理和数据源位置验证固定的区域。

## 需要检查的证据
扫描器子类型（`vercel-json-single`、`segment-preferred`）和固定的区域。交叉检查 Speed Insights TTFB 和按国家的流量分析。定位数据源——在缓存未命中的路径上，靠近它通常获胜。

## 何时不建议
如果各国的 TTFB 是健康的，则跳过。如果是有意为之以保持数据接近性，则跳过。在小型项目（<20 路由）上跳过。在不确认数据层可在无跨区域出口的情况下访问之前，不要提出多区域。

## 验证
命名固定的区域、流量地理、数据源位置以及具体调用：迁移、扩展或保留并使用 TTFB 监控器。