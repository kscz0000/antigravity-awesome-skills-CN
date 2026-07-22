---
title: 正确使用异步工作流
impact: LOW
impactDescription: 在工作流中启用非阻塞 I/O
tags: async, coroutine, await, asyncio
---

## 正确使用异步工作流

协程（async）函数可以作为 DBOS 工作流。请使用异步专用方法和模式。

**错误（同步和异步混用）：**

```python
@DBOS.workflow()
async def async_workflow():
    # 不要在异步工作流中使用同步 sleep！
    DBOS.sleep(10)

    # 不要对异步工作流使用同步 start_workflow
    handle = DBOS.start_workflow(other_async_workflow)
```

**正确（异步模式）：**

```python
import asyncio
import aiohttp

@DBOS.step()
async def fetch_async():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com") as response:
            return await response.text()

@DBOS.workflow()
async def async_workflow():
    # 使用异步 sleep
    await DBOS.sleep_async(10)

    # await 异步步骤
    result = await fetch_async()

    # 使用异步 start_workflow
    handle = await DBOS.start_workflow_async(other_async_workflow)

    return result
```

### 并行运行异步步骤

只要按**确定性顺序**启动，就可以并行运行异步步骤：

**正确（确定性启动顺序）：**

```python
@DBOS.workflow()
async def parallel_workflow():
    # 按确定性顺序启动步骤，然后一起 await
    tasks = [
        asyncio.create_task(step1("arg1")),
        asyncio.create_task(step2("arg2")),
        asyncio.create_task(step3("arg3")),
    ]
    # 使用 return_exceptions=True 实现正确的错误处理
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

**错误（非确定性顺序）：**

```python
@DBOS.workflow()
async def bad_parallel_workflow():
    async def seq_a():
        await step1("arg1")
        await step2("arg2")  # 顺序取决于 step1 的耗时

    async def seq_b():
        await step3("arg3")
        await step4("arg4")  # 顺序取决于 step3 的耗时

    # step2 和 step4 可能以任意顺序执行——非确定性！
    await asyncio.gather(seq_a(), seq_b())
```

如果需要并发的执行序列，请使用子工作流而不是交错步骤。

异步工作流中的事务，请使用 `asyncio.to_thread`：

```python
@DBOS.transaction()
def sync_transaction(data):
    DBOS.sql_session.execute(...)

@DBOS.workflow()
async def async_workflow():
    result = await asyncio.to_thread(sync_transaction, data)
```

参考：[异步工作流](https://docs.dbos.dev/python/tutorials/workflow-tutorial#coroutine-async-workflows)
