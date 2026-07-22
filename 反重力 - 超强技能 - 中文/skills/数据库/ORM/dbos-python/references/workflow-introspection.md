---
title: 列出和检视工作流
impact: MEDIUM
impactDescription: 支持监控和管理工作流状态
tags: workflow, list, introspection, status, monitoring
---

## 列出和检视工作流

使用 `DBOS.list_workflows()` 按状态、名称、队列或其他条件查询工作流。

**错误（加载不必要的数据）：**

```python
# 在不需要时加载输入/输出会很慢
workflows = DBOS.list_workflows(status="PENDING")
for w in workflows:
    print(w.workflow_id)  # 只使用了 ID
```

**正确（用 load 参数优化）：**

```python
# 关闭输入/输出加载以获得更好的性能
workflows = DBOS.list_workflows(
    status="PENDING",
    load_input=False,
    load_output=False
)
for w in workflows:
    print(f"{w.workflow_id}: {w.status}")
```

常见查询：

```python
# 查找失败的工作流
failed = DBOS.list_workflows(status="ERROR", limit=100)

# 按名称查找工作流
processing = DBOS.list_workflows(
    name="process_task",
    status=["PENDING", "ENQUEUED"]
)

# 查找特定队列上的工作流
queued = DBOS.list_workflows(queue_name="high_priority")

# 只查询已入队的工作流（简写）
queued = DBOS.list_queued_workflows(queue_name="task_queue")

# 查找旧版本的工作流以便蓝绿部署
old = DBOS.list_workflows(
    app_version="1.0.0",
    status=["PENDING", "ENQUEUED"]
)

# 获取工作流的步骤
steps = DBOS.list_workflow_steps(workflow_id)
for step in steps:
    print(f"Step {step['function_id']}: {step['function_name']}")
```

WorkflowStatus 字段：`workflow_id`、`status`、`name`、`queue_name`、`created_at`、`input`、`output`、`error`

状态值：`ENQUEUED`、`PENDING`、`SUCCESS`、`ERROR`、`CANCELLED`、`MAX_RECOVERY_ATTEMPTS_EXCEEDED`

参考：[工作流管理](https://docs.dbos.dev/python/tutorials/workflow-management)
