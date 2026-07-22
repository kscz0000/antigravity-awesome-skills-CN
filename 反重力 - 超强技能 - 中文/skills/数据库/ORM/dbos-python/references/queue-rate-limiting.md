---
title: 对队列执行进行速率限制
impact: HIGH
impactDescription: 避免触发 API 速率限制
tags: queue, rate-limit, api, throttle
---

## 对队列执行进行速率限制

在对接有速率限制的 API（如 LLM API）时使用速率限制。限制是跨所有进程全局生效的。

**错误（没有速率限制）：**

```python
queue = Queue("llm_tasks")

@DBOS.step()
def call_llm(prompt):
    # 调用过多可能触发速率限制
    return openai.chat.completions.create(...)
```

**正确（加上速率限制）：**

```python
# 每个 30 秒最多启动 50 个任务
queue = Queue("llm_tasks", limiter={"limit": 50, "period": 30})

@DBOS.step()
def call_llm(prompt):
    return openai.chat.completions.create(...)

@DBOS.workflow()
def process_prompts(prompts):
    handles = []
    for prompt in prompts:
        # 队列强制执行速率限制
        handle = queue.enqueue(call_llm, prompt)
        handles.append(handle)
    return [h.get_result() for h in handles]
```

速率限制参数：
- `limit`：在该时间窗口内最多启动的函数数量
- `period`：时间窗口长度（秒）

速率限制可以与并发限制组合使用：

```python
queue = Queue("api_tasks",
    worker_concurrency=5,
    limiter={"limit": 100, "period": 60})
```

参考：[速率限制](https://docs.dbos.dev/python/tutorials/queue-tutorial#rate-limiting)
