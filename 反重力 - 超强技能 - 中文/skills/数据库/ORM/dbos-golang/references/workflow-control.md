---
title: 取消、恢复和分叉工作流
impact: MEDIUM
impactDescription: 支持对长时间运行工作流的运维控制
tags: workflow, cancel, resume, fork, management
---

## 取消、恢复和分叉工作流

DBOS 提供取消、恢复和分叉工作流的函数，以进行运维控制。

**错误示例（无法处理卡住或失败的工作流）：**

```go
// 工作流卡住或失败 - 没有恢复机制
handle, _ := dbos.RunWorkflow(ctx, processTask, "data")
// 如果工作流失败，没有办法重试或恢复
```

**正确示例（使用 cancel、resume、fork）：**

```go
// 取消工作流 - 在下一步停止
err := dbos.CancelWorkflow(ctx, workflowID)

// 从最后完成的步骤恢复
handle, err := dbos.ResumeWorkflowstring
result, err := handle.GetResult()
```

取消操作将工作流状态设置为 `CANCELLED`，并在下一步开始时抢占执行。取消操作也会取消所有子工作流。

Resume 从最后完成的步骤重启工作流。适用于已取消或超出最大恢复尝试次数的工作流。也可以用于立即启动一个已入队的工作流，跳过其队列。

从特定步骤分叉工作流：

```go
// 列出步骤以找到正确的步骤 ID
steps, err := dbos.GetWorkflowSteps(ctx, workflowID)

// 从特定步骤分叉
forkHandle, err := dbos.ForkWorkflowstring
result, err := forkHandle.GetResult()
```

分叉会创建一个带新 ID 的工作流，复制原工作流的输入和截至所选步骤的步骤输出。

参考：[Workflow Management](https://docs.dbos.dev/golang/tutorials/workflow-management)
