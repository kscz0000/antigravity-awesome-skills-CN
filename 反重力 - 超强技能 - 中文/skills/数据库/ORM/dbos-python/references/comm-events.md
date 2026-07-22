---
title: 使用事件发布工作流状态
impact: MEDIUM
impactDescription: 实时监控工作流状态
tags: events, set_event, get_event, status
---

## 使用事件发布工作流状态

工作流可以发布键值对事件，客户端可以读取这些事件。事件是持久化的，适合用来更新状态。

**错误（无法监控进度）：**

```python
@DBOS.workflow()
def long_workflow():
    step_one()
    step_two()  # 客户端看不到进度
    step_three()
    return "done"
```

**正确（发布事件）：**

```python
@DBOS.workflow()
def long_workflow():
    DBOS.set_event("status", "starting")

    step_one()
    DBOS.set_event("status", "step_one_complete")

    step_two()
    DBOS.set_event("status", "step_two_complete")

    step_three()
    DBOS.set_event("status", "finished")
    return "done"

# 读取事件的客户端代码
@app.post("/start")
def start_workflow():
    handle = DBOS.start_workflow(long_workflow)
    return {"workflow_id": handle.get_workflow_id()}

@app.get("/status/{workflow_id}")
def get_status(workflow_id: str):
    status = DBOS.get_event(workflow_id, "status", timeout_seconds=0) or "not started"
    return {"status": status}
```

获取工作流的所有事件：

```python
all_events = DBOS.get_all_events(workflow_id)
# 返回：{"status": "finished", "other_key": "value"}
```

事件可以由工作流或步骤通过 `set_event` 调用。

参考：[工作流事件](https://docs.dbos.dev/python/tutorials/workflow-communication#workflow-events)
