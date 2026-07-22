---
title: 遵循工作流约束
impact: CRITICAL
impactDescription: 违反约束会导致失败或行为异常
tags: workflow, step, constraints, rules
---

## 遵循工作流约束

DBOS 工作流和步骤有一些必须遵守的特定约束，才能保证正确运行。

**错误（在步骤中调用 start_workflow）：**

```python
@DBOS.step()
def my_step():
    # 切勿在步骤中启动工作流！
    DBOS.start_workflow(another_workflow)
```

**错误（修改全局状态）：**

```python
results = []  # 全局变量

@DBOS.workflow()
def my_workflow():
    # 不要在工作流中修改全局变量！
    results.append("done")
```

**错误（在工作流之外调用 recv）：**

```python
@DBOS.step()
def my_step():
    # recv 只能从工作流中调用！
    msg = DBOS.recv("topic")
```

**正确（遵守约束）：**

```python
@DBOS.workflow()
def parent_workflow():
    result = my_step()
    # 从工作流而非步骤中启动子工作流
    handle = DBOS.start_workflow(child_workflow, result)
    # 在工作流中使用 recv
    msg = DBOS.recv("topic")
    return handle.get_result()

@DBOS.step()
def my_step():
    # 步骤只负责完成自己的工作并返回
    return process_data()

@DBOS.workflow()
def child_workflow(data):
    return transform(data)
```

关键约束：
- 不要在步骤中调用 `DBOS.start_workflow`
- 不要在步骤中调用 `DBOS.recv`
- 不要在工作流之外调用 `DBOS.set_event`
- 不要在工作流或步骤中修改全局变量
- 不要使用线程来启动工作流

参考：[DBOS 工作流](https://docs.dbos.dev/python/tutorials/workflow-tutorial)
