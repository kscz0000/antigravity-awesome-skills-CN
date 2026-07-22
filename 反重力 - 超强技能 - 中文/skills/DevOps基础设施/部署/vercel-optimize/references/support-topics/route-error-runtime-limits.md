---
id: route-error-runtime-limits
title: Route errors and runtime limits
status: active
candidateKinds: ["route_errors"]
frameworks: ["*"]
priority: 90
citations: ["https://vercel.com/docs/functions", "https://vercel.com/docs/functions/limitations", "https://vercel.com/docs/cli/inspect"]
maxBriefChars: 850
---

## 调查简报
路由错误候选是具有成本影响的可靠性发现。确定失败是应用异常、超时、有效负载限制还是部署特定的回归。

## 需要检查的证据
使用 `errorStatusPattern`、`errorCodes` 和 `errorsByDeployment`。在源代码中，检查最有可能抛出、超时或超出平台限制的路径。

## 何时不建议
不要将高 5xx 量框定为性能调优问题。在证明路由需要更多余量之前，不要建议增加限制。

## 验证
命名错误类、如果存在则部署集中度以及触发或未能处理它的文件行。