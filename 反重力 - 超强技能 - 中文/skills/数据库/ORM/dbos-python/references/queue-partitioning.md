---
title: 为队列分区以实现按实体限流
impact: HIGH
impactDescription: 支持按用户或按实体的流控
tags: queue, partition, per-user, flow-control
---

## 为队列分区以实现按实体限流

分区队列按分区（而非全局）应用流控限制。适用于按用户或按实体的并发限制。

**错误（全局限制影响所有用户）：**

```python
queue = Queue("user_tasks", concurrency=1)  # 全局只有 1 个任务

def handle_user_task(user_id, task):
    # 一个用户会阻塞所有其他用户！
    queue.enqueue(process_task, task)
```

**正确（通过分区实现按用户限流）：**

```python
from dbos import Queue, SetEnqueueOptions

# 分区队列，每个分区并发为 1
queue = Queue("user_tasks", partition_queue=True, concurrency=1)

@DBOS.workflow()
def process_task(task):
    pass

def handle_user_task(user_id: str, task):
    # 每个用户拥有自己的“子队列”，并发为 1
    with SetEnqueueOptions(queue_partition_key=user_id):
        queue.enqueue(process_task, task)
```

同时需要按分区和全局限制时，使用两层队列：

```python
# 全局上限 5 个并发任务
global_queue = Queue("global_queue", concurrency=5)
# 按用户上限 1 个并发任务
user_queue = Queue("user_queue", partition_queue=True, concurrency=1)

def handle_task(user_id: str, task):
    with SetEnqueueOptions(queue_partition_key=user_id):
        user_queue.enqueue(concurrency_manager, task)

@DBOS.workflow()
def concurrency_manager(task):
    # 强制执行全局限制
    return global_queue.enqueue(process_task, task).get_result()

@DBOS.workflow()
def process_task(task):
    pass
```

参考：[队列分区](https://docs.dbos.dev/python/tutorials/queue-tutorial#partitioning-queues)
