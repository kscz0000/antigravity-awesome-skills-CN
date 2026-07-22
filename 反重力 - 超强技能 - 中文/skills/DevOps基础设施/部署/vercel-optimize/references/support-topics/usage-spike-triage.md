---
id: usage-spike-triage
title: Usage spike triage
status: active
candidateKinds: ["usage_spike_triage"]
frameworks: ["*"]
priority: 95
citations: ["https://vercel.com/docs/alerts", "https://vercel.com/docs/spend-management", "https://vercel.com/docs/bot-management"]
maxBriefChars: 950
---

## 调查简报
单日或单 SKU 峰值在修复之前需要原因。分支：可缓存路由上的 bot 或 AI 爬虫、病毒式时刻、定价模型迁移或代码回归。

## 需要检查的证据
从 `usage.breakdown.data` 确认 SKU 和日期。交叉检查防火墙/bot 数据、流量曲线、SKU 重命名时间以及峰值日期周围的部署日志。Spend Management 和 Alerts 是监控工具；它们不能替代查找流量或部署原因。

## 何时不建议
在识别分支之前不要提出代码修复。不要对病毒式时刻限速或针对第三方爬虫流量回滚部署。

## 验证
命名 SKU、日期、值、窗口均值、分支以及一项支持数据。