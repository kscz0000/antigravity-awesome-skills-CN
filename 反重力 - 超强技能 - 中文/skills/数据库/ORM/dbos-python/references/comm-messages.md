---
title: 使用消息进行工作流通知
impact: MEDIUM
impactDescription: 让外部信号能够控制工作流执行
tags: messages, send, recv, notifications
---

## 使用消息进行工作流通知

向运行中的工作流发送消息以发出信号或通知。消息是持久化的，并按 topic 排队。

**错误（轮询外部状态）：**

```python
@DBOS.workflow()
def payment_workflow():
    # 轮询效率低下且非持久化
    while True:
        status = check_payment_status()
        if status == "paid":
            break
        time.sleep(1)
```

**正确（使用消息）：**

```python
PAYMENT_STATUS = "payment_status"

@DBOS.workflow()
def payment_workflow():
    # 处理订单...
    DBOS.set_event("payment_id", payment_id)

    # 等待支付通知（60 秒超时）
    payment_status = DBOS.recv(PAYMENT_STATUS, timeout_seconds=60)

    if payment_status == "paid":
        fulfill_order()
    else:
        cancel_order()

# 用于接收支付通知的 Webhook 端点
@app.post("/payment_webhook/{workflow_id}/{status}")
def payment_webhook(workflow_id: str, status: str):
    DBOS.send(workflow_id, status, PAYMENT_STATUS)
    return {"ok": True}
```

要点：
- `DBOS.recv()` 只能从工作流中调用
- 消息按 topic 排队
- 超时时 `recv()` 返回 `None`
- 消息持久化，可保证精确一次投递

参考：[工作流消息传递](https://docs.dbos.dev/python/tutorials/workflow-communication#workflow-messaging-and-notifications)
