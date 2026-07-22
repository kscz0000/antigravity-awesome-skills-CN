---
title: 创建定时工作流
impact: MEDIUM
impactDescription: 在每个时间间隔内工作流只执行一次
tags: scheduled, cron, recurring, timer
---

## 创建定时工作流

使用 `@DBOS.scheduled` 按计划运行工作流。每个间隔内工作流恰好执行一次。

**错误（手动调度）：**

```python
# 不要使用外部 cron 或手动定时器
import schedule
schedule.every(1).minute.do(my_task)
```

**正确（DBOS 定时工作流）：**

```python
@DBOS.scheduled("* * * * *")  # 每分钟
@DBOS.workflow()
def run_every_minute(scheduled_time, actual_time):
    print(f"Running at {scheduled_time}")
    do_maintenance_task()

@DBOS.scheduled("0 */6 * * *")  # 每 6 小时
@DBOS.workflow()
def periodic_cleanup(scheduled_time, actual_time):
    cleanup_old_records()
```

定时工作流要求：
- 必须使用 `@DBOS.scheduled` 装饰器并配合 crontab 语法
- 必须接受两个参数：`scheduled_time` 和 `actual_time`（均为 `datetime`）
- 主线程必须保持存活以运行定时工作流

对于仅有定时工作流的应用（没有 HTTP 服务器）：

```python
import threading

if __name__ == "__main__":
    DBOS.launch()
    threading.Event().wait()  # 永久阻塞
```

Crontab 格式：`分 时 日 月 周`
- `* * * * *` = 每分钟
- `0 * * * *` = 每小时
- `0 0 * * *` = 每天零点
- `0 0 * * 0` = 每周日

参考：[定时工作流](https://docs.dbos.dev/python/tutorials/scheduled-workflows)
