---
title: 取消、恢复和分叉工作流
impact: MEDIUM
impactDescription: 控制运行中的工作流并从故障中恢复
tags: workflow, cancel, resume, fork, control
---

## 取消、恢复和分叉工作流

使用这些方法来控制工作流的执行：停止失控的工作流、重试失败的工作流，或从某个特定步骤重新启动。

**错误（期待立即取消）：**

```python
DBOS.cancel_workflow(workflow_id)
# 错误：假设工作流已经立即停止
cleanup_resources()  # 可能与仍在执行当前步骤的工作流发生竞态
```

**正确（等待取消完成）：**

```python
DBOS.cancel_workflow(workflow_id)
# 取消发生在下一个步骤的开始处
# 等待工作流真正停止
handle = DBOS.retrieve_workflow(workflow_id)
status = handle.get_status()
while status.status == "PENDING":
    time.sleep(0.5)
    status = handle.get_status()
# 现在可以安全地清理资源
cleanup_resources()
```

### 取消

停止一个工作流并将其从队列中移除：

```python
DBOS.cancel_workflow(workflow_id)  # 取消工作流及其所有子工作流
```

### 恢复

从工作流上次完成的步骤重新启动已停止的工作流：

```python
# 恢复已取消或失败的工作流
handle = DBOS.resume_workflow(workflow_id)
result = handle.get_result()

# 也可以绕过队列直接恢复已入队的工作流
handle = DBOS.resume_workflow(enqueued_workflow_id)
```

### 分叉

从已有工作流的某个特定步骤开始一个新的工作流：

```python
# 获取步骤列表以找到正确的起点
steps = DBOS.list_workflow_steps(workflow_id)
for step in steps:
    print(f"Step {step['function_id']}: {step['function_name']}")

# 从第 3 步分叉（跳过第 1-2 步，复用它们已保存的结果）
new_handle = DBOS.fork_workflow(workflow_id, start_step=3)

# 分叉到新应用版本运行（便于修复 bug）
new_handle = DBOS.fork_workflow(
    workflow_id,
    start_step=3,
    application_version="2.0.0"
)
```

参考：[工作流管理](https://docs.dbos.dev/python/tutorials/workflow-management)
