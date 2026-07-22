---
title: 控制 worker 监听的队列
impact: HIGH
impactDescription: 支持异构 worker 池（CPU/GPU）
tags: queue, listen, worker, heterogeneous
---

## 控制 worker 监听的队列

使用 `DBOS.listen_queues()` 让进程只处理特定的队列。适用于 CPU 与 GPU worker 分离的场景。

**错误（所有 worker 处理所有队列）：**

```python
cpu_queue = Queue("cpu_tasks")
gpu_queue = Queue("gpu_tasks")

# 每个 worker 同时处理两个队列
# GPU 任务可能运行在只有 CPU 的机器上！
if __name__ == "__main__":
    DBOS(config=config)
    DBOS.launch()
```

**正确（worker 只监听指定队列）：**

```python
from dbos import DBOS, DBOSConfig, Queue

cpu_queue = Queue("cpu_queue")
gpu_queue = Queue("gpu_queue")

@DBOS.workflow()
def cpu_task(data):
    pass

@DBOS.workflow()
def gpu_task(data):
    pass

if __name__ == "__main__":
    worker_type = os.environ.get("WORKER_TYPE")  # "cpu" 或 "gpu"
    config: DBOSConfig = {"name": "worker"}
    DBOS(config=config)

    if worker_type == "gpu":
        DBOS.listen_queues([gpu_queue])
    elif worker_type == "cpu":
        DBOS.listen_queues([cpu_queue])

    DBOS.launch()
```

要点：
- 必须在 `DBOS.launch()` **之前**调用 `DBOS.listen_queues()`
- Worker 仍然可以**入队**到任何队列，只是不会从其他队列**出队**
- 默认情况下，worker 监听所有已声明的队列

使用场景：
- CPU 与 GPU worker
- 内存密集型与轻量型任务
- 按地域路由任务

参考：[显式队列监听](https://docs.dbos.dev/python/tutorials/queue-tutorial#explicit-queue-listening)
