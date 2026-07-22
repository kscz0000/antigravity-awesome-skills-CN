---
title: 使用流式传输实时数据
impact: MEDIUM
impactDescription: 支持从长时间运行的工作流流式传输结果
tags: communication, stream, real-time, async-generator
---

## 使用流式传输实时数据

工作流可使用 `DBOS.writeStream`、`DBOS.closeStream` 和 `DBOS.readStream` 实时向客户端流式传输数据。适用于 LLM 输出流式传输或进度报告。

**错误（累积结果后在末尾返回）：**

```typescript
async function processWorkflowFn() {
  const results: string[] = [];
  for (const chunk of data) {
    results.push(await processChunk(chunk));
  }
  return results; // 客户端必须等待整个工作流完成
}
```

**正确（在结果可用时立即流式输出）：**

```typescript
async function processWorkflowFn() {
  for (const chunk of data) {
    const result = await DBOS.runStep(() => processChunk(chunk), { name: "process" });
    await DBOS.writeStream("results", result);
  }
  await DBOS.closeStream("results"); // 标记完成
}
const processWorkflow = DBOS.registerWorkflow(processWorkflowFn);

// 从外部读取流
const handle = await DBOS.startWorkflow(processWorkflow)();
for await (const value of DBOS.readStream<string>(handle.workflowID, "results")) {
  console.log(`Received: ${value}`);
}
```

关键行为：
- 一个工作流可以有任意数量的流，每个流以唯一键标识
- 流不可变，仅追加
- 来自工作流的写入精确一次
- 来自步骤的写入至少一次（重试的步骤可能写入重复数据）
- 工作流终止时流自动关闭
- `readStream` 返回异步生成器，产出值直到流关闭

也可以使用 `DBOSClient.readStream` 从 DBOS 应用外部读取流。

参考：[Workflow Streaming](https://docs.dbos.dev/typescript/tutorials/workflow-communication#workflow-streaming)
