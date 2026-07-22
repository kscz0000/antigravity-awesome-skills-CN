---
title: 使用工作流 ID 实现幂等性
impact: MEDIUM
impactDescription: 防止关键操作的重复执行
tags: idempotency, workflow-id, deduplication, exactly-once
---

## 使用工作流 ID 实现幂等性

设置工作流 ID 以让操作具备幂等性。具有相同 ID 的工作流只执行一次。

**错误（可能产生重复支付）：**

```python
@app.post("/pay/{order_id}")
def process_payment(order_id: str):
    # 多次点击 = 多次支付！
    handle = DBOS.start_workflow(payment_workflow, order_id)
    return handle.get_result()
```

**正确（通过工作流 ID 实现幂等性）：**

```python
from dbos import SetWorkflowID

@app.post("/pay/{order_id}")
def process_payment(order_id: str):
    # 相同的 order_id = 相同的工作流 ID = 只执行一次
    with SetWorkflowID(f"payment-{order_id}"):
        handle = DBOS.start_workflow(payment_workflow, order_id)
    return handle.get_result()

@DBOS.workflow()
def payment_workflow(order_id: str):
    charge_customer(order_id)
    send_confirmation(order_id)
    return "success"
```

在工作流内部访问工作流 ID：

```python
@DBOS.workflow()
def my_workflow():
    current_id = DBOS.workflow_id
    DBOS.logger.info(f"Running workflow {current_id}")
```

工作流 ID 必须全局唯一。重复的 ID 会返回已有工作流的结果而不会重新执行。

参考：[工作流 ID 与幂等性](https://docs.dbos.dev/python/tutorials/workflow-tutorial#workflow-ids-and-idempotency)
