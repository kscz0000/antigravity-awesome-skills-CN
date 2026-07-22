---
title: 通过防抖避免工作流浪费执行
impact: MEDIUM
impactDescription: 在快速输入场景下减少冗余执行
tags: debounce, throttle, input, optimization
---

## 通过防抖避免工作流浪费执行

防抖会延迟工作流的执行，直到距离上一次触发经过了一定时间。常用于用户输入处理。

**错误（每次输入都处理）：**

```python
@DBOS.workflow()
def process_input(user_input):
    # 昂贵的处理
    analyze(user_input)

@app.post("/input")
def on_input(user_id: str, input: str):
    # 每次按键都触发处理！
    DBOS.start_workflow(process_input, input)
```

**正确（防抖处理）：**

```python
from dbos import Debouncer

@DBOS.workflow()
def process_input(user_input):
    analyze(user_input)

# 为该工作流创建防抖器
debouncer = Debouncer.create(process_input)

@app.post("/input")
def on_input(user_id: str, input: str):
    # 在最后一次输入后等待 5 秒再处理
    debounce_key = user_id  # 按用户防抖
    debounce_period = 5.0   # 秒
    handle = debouncer.debounce(debounce_key, debounce_period, input)
    return {"workflow_id": handle.get_workflow_id()}
```

带超时的防抖器（最长等待时间）：

```python
# 空闲 5 秒后处理，或最多等待 60 秒
debouncer = Debouncer.create(process_input, debounce_timeout_sec=60)

def on_input(user_id: str, input: str):
    debouncer.debounce(user_id, 5.0, input)
```

工作流实际执行时，使用传入 `debounce` 的**最后一组**参数。

参考：[工作流防抖](https://docs.dbos.dev/python/tutorials/workflow-tutorial#debouncing-workflows)
