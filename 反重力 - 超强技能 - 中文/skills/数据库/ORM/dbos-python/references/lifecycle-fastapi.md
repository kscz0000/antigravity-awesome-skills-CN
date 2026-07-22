---
title: 将 DBOS 与 FastAPI 集成
impact: CRITICAL
impactDescription: 正确集成可确保工作流在服务器重启后存活
tags: fastapi, http, server, integration
---

## 将 DBOS 与 FastAPI 集成

将 DBOS 与 FastAPI 一起使用时，需要在启动 uvicorn 之前，在 main 函数中配置和启动 DBOS。

**错误（在模块顶层配置）：**

```python
from fastapi import FastAPI
from dbos import DBOS, DBOSConfig

app = FastAPI()

# 不要在模块顶层配置！
config: DBOSConfig = {"name": "my-app"}
DBOS(config=config)

@app.get("/")
@DBOS.workflow()
def endpoint():
    return {"status": "ok"}

if __name__ == "__main__":
    DBOS.launch()
    uvicorn.run(app)
```

**正确（在 main 中配置）：**

```python
import os
from fastapi import FastAPI
from dbos import DBOS, DBOSConfig
import uvicorn

app = FastAPI()

@DBOS.step()
def process_data():
    return "processed"

@app.get("/")
@DBOS.workflow()
def endpoint():
    result = process_data()
    return {"result": result}

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

工作流装饰器可以与 FastAPI 路由装饰器组合使用。FastAPI 装饰器应放在最外层。

参考：[DBOS 与 FastAPI](https://docs.dbos.dev/python/tutorials/workflow-tutorial)
