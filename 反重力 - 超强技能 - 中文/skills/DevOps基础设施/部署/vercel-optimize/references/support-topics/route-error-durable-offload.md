---
id: route-error-durable-offload
title: Durable offload for timeout-heavy routes
status: active
candidateKinds: ["route_errors"]
frameworks: ["*"]
priority: 84
citations: ["https://vercel.com/docs/workflow", "https://workflow-sdk.dev/docs/foundations/starting-workflows", "https://workflow-sdk.dev/docs/foundations/workflows-and-steps", "https://vercel.com/docs/queues", "https://vercel.com/docs/functions/limitations"]
maxBriefChars: 850
---

## 调查简报
超时严重的路由通常需要作业边界，而不是更高的限制。Workflow 适用于在响应后可以继续的持久多步骤工作；返回运行 ID 而不是等待 `returnValue`。

## 需要检查的证据
使用 `errorStatusPattern`、`errorCodes` 和源流。查找扇出、轮询、批量工作、AI 作业、上传、休眠、审批、多步骤副作用。如果已使用 Workflow，检查路由是等待还是流式传输进度。

## 何时不建议
不要卸载必须在响应之前完成的工作。不要仅根据卸载声明节省：Workflow Steps/Storage 单独计费，调用的函数仍使用计算计费。

## 验证
命名超时/错误类、长时间运行的操作、入队后的响应契约以及保留语义的队列或工作流边界。