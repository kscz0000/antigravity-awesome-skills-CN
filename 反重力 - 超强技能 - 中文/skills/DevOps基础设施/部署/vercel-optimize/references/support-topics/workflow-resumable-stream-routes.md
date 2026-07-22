---
id: workflow-resumable-stream-routes
title: Workflow resumable stream routes
status: active
candidateKinds: ["slow_route"]
frameworks: ["*"]
routePatterns: ["(^|/)api/.*/stream/?$", "(^|/)chat/.*/stream/?$", "\\[id\\].*/stream"]
priority: 98
citations: ["https://workflow-sdk.dev/docs/ai/resumable-streams", "https://workflow-sdk.dev/docs/foundations/streaming", "https://vercel.com/docs/workflow"]
maxBriefChars: 850
---

## 调查简报
流式路由可能是 Workflow SDK 重连接端点。长墙钟持续时间可能是实时客户端连接。

## 需要检查的证据
查找 `WorkflowChatTransport`、`getRun`、`run.getReadable`、`startIndex`、`x-workflow-run-id`、`x-workflow-stream-tail-index`、`getWritable` 或 `createUIMessageStreamResponse`。比较 CPU、TTFB、墙钟。检查完整重放、缺失的尾索引、未释放的锁或未关闭的流。

## 何时不建议
不要缓存流端点或删除可恢复性。当 CPU 低、TTFB 健康且路由仅保持客户端连接时，不要将高持续时间称为 bug。

## 验证
命名路由是启动还是重连接运行，然后引用确切的浪费：重放、缺失的尾索引、锁泄漏、未关闭的流、高 CPU 或可避免的首字节前工作。