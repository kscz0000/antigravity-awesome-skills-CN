---
title: 保持工作流的确定性
impact: CRITICAL
impactDescription: 非确定性工作流无法正确恢复
tags: workflow, determinism, recovery, reliability
---

## 保持工作流的确定性

工作流函数必须是确定性的：在相同输入和步骤返回值的前提下，必须以相同顺序调用相同的步骤。非确定性操作必须放到步骤中。

**错误（非确定性工作流）：**

```python
import random

@DBOS.workflow()
def example_workflow():
    # 在工作流中使用随机数会破坏恢复！
    choice = random.randint(0, 1)
    if choice == 0:
        step_one()
    else:
        step_two()
```

**正确（将非确定性操作放在步骤中）：**

```python
import random

@DBOS.step()
def generate_choice():
    return random.randint(0, 1)

@DBOS.workflow()
def example_workflow():
    # 随机数在步骤中生成——结果会被保存
    choice = generate_choice()
    if choice == 0:
        step_one()
    else:
        step_two()
```

必须放在步骤中的非确定性操作：
- 生成随机数
- 获取当前时间
- 访问外部 API
- 读取文件
- 数据库查询（使用事务或步骤）

参考：[工作流确定性](https://docs.dbos.dev/python/tutorials/workflow-tutorial#determinism)
