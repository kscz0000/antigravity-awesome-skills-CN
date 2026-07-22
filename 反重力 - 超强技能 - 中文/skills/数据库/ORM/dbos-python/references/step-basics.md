---
title: 使用步骤处理外部操作
impact: HIGH
impactDescription: 步骤通过检查点结果支持恢复
tags: step, external, api, checkpoint
---

## 使用步骤处理外部操作

任何执行复杂操作、访问外部 API 或具有副作用的函数都应当作为步骤。步骤结果会被检查点化，从而支持工作流恢复。

**错误（在工作流中直接调用外部接口）：**

```python
import requests

@DBOS.workflow()
def my_workflow():
    # 在工作流中直接调用外部 API——不会检查点化！
    response = requests.get("https://api.example.com/data")
    return response.json()
```

**正确（在步骤中调用外部接口）：**

```python
import requests

@DBOS.step()
def fetch_data():
    response = requests.get("https://api.example.com/data")
    return response.json()

@DBOS.workflow()
def my_workflow():
    # 步骤结果会被检查点化以支持恢复
    data = fetch_data()
    return data
```

步骤要求：
- 输入和输出必须是可序列化的
- 不应修改全局状态
- 失败时可重试（可配置）

何时使用步骤：
- 调用外部服务的 API
- 文件系统操作
- 生成随机数
- 获取当前时间
- 任何非确定性操作

参考：[DBOS 步骤](https://docs.dbos.dev/python/tutorials/step-tutorial)
