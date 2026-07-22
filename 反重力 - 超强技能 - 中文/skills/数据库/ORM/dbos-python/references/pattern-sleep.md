---
title: 使用持久化 sleep 延迟执行
impact: MEDIUM
impactDescription: 在重启后依然有效，可跨越数天或数周
tags: sleep, delay, schedule, durable
---

## 使用持久化 sleep 延迟执行

使用 `DBOS.sleep()` 实现跨重启存活的持久化延迟。唤醒时间会持久化到数据库中。

**错误（普通 sleep）：**

```python
import time

@DBOS.workflow()
def delayed_task(delay_seconds, task):
    # 普通 sleep 在重启后会丢失！
    time.sleep(delay_seconds)
    run_task(task)
```

**正确（持久化 sleep）：**

```python
@DBOS.workflow()
def delayed_task(delay_seconds, task):
    # 持久化 sleep——跨重启存活
    DBOS.sleep(delay_seconds)
    run_task(task)
```

持久化 sleep 的使用场景：
- 将任务安排在未来执行
- 在重试之间等待
- 实现跨越数小时、数天或数周的延迟

示例：安排一个提醒：

```python
@DBOS.workflow()
def send_reminder(user_id: str, message: str, delay_days: int):
    # 睡眠数天——任何重启都能存活
    DBOS.sleep(delay_days * 24 * 60 * 60)
    send_notification(user_id, message)
```

对于异步工作流，使用 `DBOS.sleep_async()`：

```python
@DBOS.workflow()
async def async_delayed_task():
    await DBOS.sleep_async(60)
    await run_async_task()
```

参考：[持久化 sleep](https://docs.dbos.dev/python/tutorials/workflow-tutorial#durable-sleep)
