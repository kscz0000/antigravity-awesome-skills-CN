---
title: 使用队列运行并发工作流
impact: HIGH
impactDescription: 队列提供托管的并发控制和流控
tags: queue, concurrency, enqueue, workflow
---

## 使用队列运行并发工作流

队列以托管的流控方式并发运行大量工作流。当你需要控制同时运行的工作流数量时，请使用队列。

**错误（不受控的并发）：**

```python
@DBOS.workflow()
def process_task(task):
    pass

# 不加控制地启动大量工作流
for task in tasks:
    DBOS.start_workflow(process_task, task)  # 可能压垮资源
```

**正确（使用队列）：**

```python
from dbos import Queue

queue = Queue("task_queue")

@DBOS.workflow()
def process_task(task):
    pass

@DBOS.workflow()
def process_all_tasks(tasks):
    handles = []
    for task in tasks:
        # 队列管理并发
        handle = queue.enqueue(process_task, task)
        handles.append(handle)
    # 等待所有任务完成
    return [h.get_result() for h in handles]
```

队列按 FIFO 顺序处理工作流。可以将工作流和步骤都加入队列。

```python
queue = Queue("example_queue")

@DBOS.step()
def my_step(data):
    return process(data)

# 将步骤加入队列
handle = queue.enqueue(my_step, data)
result = handle.get_result()
```

参考：[DBOS 队列](https://docs.dbos.dev/python/tutorials/queue-tutorial)
