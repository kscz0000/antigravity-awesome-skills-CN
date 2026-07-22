---
title: 设置工作流超时
impact: CRITICAL
impactDescription: 防止失控工作流持续占用资源
tags: timeout, cancel, deadline, limits
---

## 设置工作流超时

使用 `SetWorkflowTimeout` 限制工作流的执行时间。超时的工作流将被取消。

**错误（没有超时）：**

```python
@DBOS.workflow()
def potentially_long_workflow():
    # 可能永远运行！
    while not done:
        process_next()
```

**正确（设置超时）：**

```python
from dbos import SetWorkflowTimeout

@DBOS.workflow()
def bounded_workflow():
    while not done:
        process_next()

# 工作流必须在 60 秒内完成
with SetWorkflowTimeout(60):
    bounded_workflow()

# 或与 start_workflow 一起使用
with SetWorkflowTimeout(60):
    handle = DBOS.start_workflow(bounded_workflow)
```

超时行为：
- 超时是**从开始到完成**的时间（不计算队列等待时间）
- 超时是**持久化**的（跨重启依然有效）
- 取消发生在**下一个步骤的开始处**
- **所有子工作流**也会被取消

与队列一起使用：

```python
queue = Queue("example_queue")

# 超时从出队开始计算，而不是从入队开始
with SetWorkflowTimeout(30):
    queue.enqueue(my_workflow)
```

由于超时存储在数据库中，因此可以支持较长的时长（小时、天、周）。

参考：[工作流超时](https://docs.dbos.dev/python/tutorials/workflow-tutorial#workflow-timeouts)
