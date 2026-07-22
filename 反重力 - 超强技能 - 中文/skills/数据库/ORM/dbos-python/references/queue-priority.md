---
title: 为工作流设置队列优先级
impact: HIGH
impactDescription: 确保重要的工作优先执行
tags: queue, priority, ordering, scheduling
---

## 为工作流设置队列优先级

使用优先级控制哪些工作流先运行。数字越小，优先级越高。

**错误（没有优先级控制）：**

```python
queue = Queue("tasks")

# 所有任务同等对待——紧急任务可能需要等待
for task in tasks:
    queue.enqueue(process_task, task)
```

**正确（使用优先级）：**

```python
from dbos import Queue, SetEnqueueOptions

# 必须在队列上启用优先级
queue = Queue("tasks", priority_enabled=True)

@DBOS.workflow()
def process_task(task):
    pass

def enqueue_task(task, is_urgent: bool):
    # 优先级 1 = 最高，先于优先级 10 执行
    priority = 1 if is_urgent else 10
    with SetEnqueueOptions(priority=priority):
        queue.enqueue(process_task, task)
```

优先级行为：
- 范围：1 到 2,147,483,647（越小优先级越高）
- 没有指定优先级的工作流具有最高优先级（最先执行）
- 相同优先级按 FIFO 顺序执行
- 必须在队列上设置 `priority_enabled=True`

多优先级示例：

```python
queue = Queue("jobs", priority_enabled=True)

PRIORITY_CRITICAL = 1
PRIORITY_HIGH = 10
PRIORITY_NORMAL = 100
PRIORITY_LOW = 1000

def enqueue_job(job, level):
    with SetEnqueueOptions(priority=level):
        queue.enqueue(process_job, job)
```

参考：[队列优先级](https://docs.dbos.dev/python/tutorials/queue-tutorial#priority)
