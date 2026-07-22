---
title: 列出和检查工作流
impact: MEDIUM
impactDescription: 支持对工作流执行的监控与调试
tags: workflow, list, inspect, status, monitoring
---

## 列出和检查工作流

使用 `dbos.ListWorkflows` 按状态、名称、时间范围等条件查询工作流执行。

**错误示例（无法监控工作流状态）：**

```go
// 启动工作流但之后无法检查
dbos.RunWorkflow(ctx, processTask, "data")
// 如果出现问题，没有办法找到或调试它
```

**正确示例（列出和检查工作流）：**

```go
// 按状态列出工作流
erroredWorkflows, err := dbos.ListWorkflows(ctx,
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusError}),
)

for _, wf := range erroredWorkflows {
	fmt.Printf("Workflow %s: %s - %v\n", wf.ID, wf.Name, wf.Error)
}
```

使用多个过滤条件列出工作流：

```go
workflows, err := dbos.ListWorkflows(ctx,
	dbos.WithName("processOrder"),
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusSuccess}),
	dbos.WithLimit(100),
	dbos.WithSortDesc(),
	dbos.WithLoadOutput(true),
)
```

列出工作流步骤：

```go
steps, err := dbos.GetWorkflowSteps(ctx, workflowID)
for _, step := range steps {
	fmt.Printf("Step %d: %s\n", step.StepID, step.StepName)
	if step.Error != nil {
		fmt.Printf("  Error: %v\n", step.Error)
	}
	if step.ChildWorkflowID != "" {
		fmt.Printf("  Child: %s\n", step.ChildWorkflowID)
	}
}
```

工作流状态值：`WorkflowStatusPending`、`WorkflowStatusEnqueued`、`WorkflowStatusSuccess`、`WorkflowStatusError`、`WorkflowStatusCancelled`、`WorkflowStatusMaxRecoveryAttemptsExceeded`

为优化性能，在不需要时避免加载输入/输出（默认不会加载）。

参考：[Workflow Management](https://docs.dbos.dev/golang/tutorials/workflow-management#listing-workflows)
