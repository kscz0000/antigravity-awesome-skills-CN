---
title: 对队列中的工作流去重
impact: HIGH
impactDescription: 防止重复工作和资源浪费
tags: queue, deduplication, duplicate, idempotent
---

## 对队列中的工作流去重

使用 deduplication ID 确保一个队列中同时只有一个具有给定 ID 的工作流处于活跃状态。

**错误（可能产生重复工作流）：**

```python
queue = Queue("user_tasks")

@app.post("/process/{user_id}")
def process_for_user(user_id: str):
    # 多次请求 = 同一用户的多个工作流！
    queue.enqueue(process_workflow, user_id)
```

**正确（按用户去重）：**

```python
from dbos import Queue, SetEnqueueOptions
from dbos import error as dboserror

queue = Queue("user_tasks")

@app.post("/process/{user_id}")
def process_for_user(user_id: str):
    with SetEnqueueOptions(deduplication_id=user_id):
        try:
            handle = queue.enqueue(process_workflow, user_id)
            return {"workflow_id": handle.get_workflow_id()}
        except dboserror.DBOSQueueDeduplicatedError:
            return {"status": "already processing"}
```

去重行为：
- 如果具有相同 deduplication ID 的工作流处于 `ENQUEUED` 或 `PENDING` 状态，新的入队会抛出 `DBOSQueueDeduplicatedError`
- 工作流完成后，相同 ID 的新工作流可以再次入队
- 去重是按队列进行的（相同 ID 可以存在于不同队列中）

使用场景：
- 每个用户同时只有一个活跃任务
- 防止重复的作业提交
- 按实体进行速率限制

参考：[队列去重](https://docs.dbos.dev/python/tutorials/queue-tutorial#deduplication)
