---
title: 正确配置和启动 DBOS
impact: CRITICAL
impactDescription: 没有正确配置时应用将无法运行
tags: configuration, launch, setup, initialization
---

## 正确配置和启动 DBOS

每个 DBOS 应用都必须在 main 函数中配置并启动 DBOS。

**错误（在模块顶层配置）：**

```python
from dbos import DBOS, DBOSConfig

# 不要在模块顶层配置！
config: DBOSConfig = {
    "name": "my-app",
}
DBOS(config=config)

@DBOS.workflow()
def my_workflow():
    pass

if __name__ == "__main__":
    DBOS.launch()
    my_workflow()
```

**正确（在 main 中配置）：**

```python
import os
from dbos import DBOS, DBOSConfig

@DBOS.workflow()
def my_workflow():
    pass

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
    my_workflow()
```

对于仅定时任务的应用（没有 HTTP 服务器），需要阻塞主线程：

```python
import os
import threading
from dbos import DBOS, DBOSConfig

@DBOS.scheduled("* * * * *")
@DBOS.workflow()
def scheduled_task(scheduled_time, actual_time):
    pass

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
    threading.Event().wait()  # 永久阻塞
```

参考：[DBOS 配置](https://docs.dbos.dev/python/reference/configuration)
