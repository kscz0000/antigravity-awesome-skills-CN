---
title: 控制队列并发
impact: HIGH
impactDescription: 通过并发上限防止资源耗尽
tags: queue, concurrency, worker_concurrency, limits
---

## 控制队列并发

队列支持 worker 级别和全局的并发限制，以防止资源耗尽。

**错误（没有并发控制）：**

```python
queue = Queue("heavy_tasks")  # 没有限制——可能耗尽内存

@DBOS.workflow()
def memory_intensive_task(data):
    # 占用大量内存
    pass
```

**正确（worker 并发）：**

```python
# 每个进程从该队列最多运行 5 个任务
queue = Queue("heavy_tasks", worker_concurrency=5)

@DBOS.workflow()
def memory_intensive_task(data):
    pass
```

**正确（全局并发）：**

```python
# 跨所有进程最多同时运行 10 个任务
queue = Queue("limited_tasks", concurrency=10)
```

**顺序处理（串行）：**

```python
# 同时只处理一个任务——保证顺序
queue = Queue("sequential_queue", concurrency=1)

@DBOS.step()
def process_event(event):
    pass

def handle_event(event):
    queue.enqueue(process_event, event)
```

大多数情况下推荐使用 worker 并发。全局并发需要谨慎使用，因为等待中的工作流会计入限制。

参考：[管理并发](https://docs.dbos.dev/python/tutorials/queue-tutorial#managing-concurrency)
