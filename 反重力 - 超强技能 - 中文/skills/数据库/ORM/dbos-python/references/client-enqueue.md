---
title: 从外部应用将工作流加入队列
impact: HIGH
impactDescription: 通过分离的 API 与 worker 服务实现解耦架构
tags: client, enqueue, workflow, external
---

## 从外部应用将工作流加入队列

使用 `client.enqueue()` 从 DBOS 应用外部提交工作流。必须显式指定工作流名称和队列名称。

**错误（缺少必需选项）：**

```python
from dbos import DBOSClient

client = DBOSClient(system_database_url=db_url)

# 缺少 workflow_name 和 queue_name！
handle = client.enqueue({}, task_data)
```

**正确（带上必需选项）：**

```python
from dbos import DBOSClient, EnqueueOptions

client = DBOSClient(system_database_url=db_url)

options: EnqueueOptions = {
    "workflow_name": "process_task",  # 必填
    "queue_name": "task_queue",       # 必填
}
handle = client.enqueue(options, task_data)
result = handle.get_result()
client.destroy()
```

带上可选参数：

```python
options: EnqueueOptions = {
    "workflow_name": "process_task",
    "queue_name": "task_queue",
    "workflow_id": "custom-id-123",
    "workflow_timeout": 300,
    "deduplication_id": "user-123",
    "priority": 1,
}
```

限制：无法将作为 Python 类方法的工作流加入队列。

参考：[DBOSClient.enqueue](https://docs.dbos.dev/python/reference/client#enqueue)
