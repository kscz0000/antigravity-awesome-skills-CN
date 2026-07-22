---
title: 在后台启动工作流
impact: CRITICAL
impactDescription: 后台工作流在崩溃和重启后依然存活
tags: workflow, background, start_workflow, handle
---

## 在后台启动工作流

使用 `DBOS.start_workflow` 在后台运行工作流。它返回一个句柄，用于监控或获取结果。

**错误（使用线程）：**

```python
import threading

@DBOS.workflow()
def long_task(data):
    # 长时间运行的工作
    pass

# 不要用线程来运行 DBOS 工作流！
thread = threading.Thread(target=long_task, args=(data,))
thread.start()
```

**正确（使用 start_workflow）：**

```python
from dbos import DBOS, WorkflowHandle

@DBOS.workflow()
def long_task(data):
    # 长时间运行的工作
    return "done"

# 在后台启动工作流
handle: WorkflowHandle = DBOS.start_workflow(long_task, data)

# 稍后获取结果
result = handle.get_result()

# 或者检查状态
status = handle.get_status()
```

可以稍后通过 ID 重新获取工作流句柄：

```python
# 获取工作流 ID
workflow_id = handle.get_workflow_id()

# 稍后重新获取句柄
handle = DBOS.retrieve_workflow(workflow_id)
result = handle.get_result()
```

参考：[启动工作流](https://docs.dbos.dev/python/tutorials/workflow-tutorial#starting-workflows-in-the-background)
