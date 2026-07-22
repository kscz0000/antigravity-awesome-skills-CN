---
title: 使用流处理实时数据
impact: MEDIUM
impactDescription: 支持实时进度和 LLM 流式输出
tags: streaming, write_stream, read_stream, realtime
---

## 使用流处理实时数据

工作流可以向客户端实时流式传输数据。适用于 LLM 响应、进度上报或长时间运行的结果。

**错误（在结尾一次性返回所有数据）：**

```python
@DBOS.workflow()
def llm_workflow(prompt):
    # 客户端必须等待整个响应
    response = call_llm(prompt)
    return response
```

**正确（流式返回结果）：**

```python
@DBOS.workflow()
def llm_workflow(prompt):
    for chunk in call_llm_streaming(prompt):
        DBOS.write_stream("response", chunk)
    DBOS.close_stream("response")
    return "complete"

# 客户端读取流
@app.get("/stream/{workflow_id}")
def stream_response(workflow_id: str):
    def generate():
        for value in DBOS.read_stream(workflow_id, "response"):
            yield value
    return StreamingResponse(generate())
```

流的特点：
- 流是不可变的，仅追加
- 工作流中的写入保证精确一次
- 步骤中的写入保证至少一次（重试时可能重复）
- 工作流终止时流自动关闭

完成后显式关闭流：

```python
@DBOS.workflow()
def producer():
    DBOS.write_stream("data", {"step": 1})
    DBOS.write_stream("data", {"step": 2})
    DBOS.close_stream("data")  # 表示写入完成
```

参考：[工作流流式传输](https://docs.dbos.dev/python/tutorials/workflow-communication#workflow-streaming)
