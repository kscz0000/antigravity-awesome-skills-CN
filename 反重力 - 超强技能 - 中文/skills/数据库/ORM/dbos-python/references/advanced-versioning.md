---
title: 使用版本管理进行蓝绿部署
impact: LOW
impactDescription: 通过版本标记安全地部署新代码
tags: versioning, blue-green, deployment, recovery
---

## 使用版本管理进行蓝绿部署

DBOS 对工作流进行版本管理，以防止不安全的恢复。请使用蓝绿部署安全地升级。

**错误（部署破坏性变更时未使用版本管理）：**

```python
# 直接部署新代码会终止正在执行的工作流
# 因为它们的检查点与新代码不匹配

# 旧代码
@DBOS.workflow()
def workflow():
    step_a()
    step_b()

# 新代码立即替换旧代码——破坏恢复！
@DBOS.workflow()
def workflow():
    step_a()
    step_c()  # 变更了步骤——旧工作流无法恢复
```

**正确（使用版本管理配合蓝绿部署）：**

```python
# 在配置中显式设置版本
config: DBOSConfig = {
    "name": "my-app",
    "application_version": "2.0.0",  # 新版本
}
DBOS(config=config)

# 并行部署新旧版本
# 新流量进入 v2.0.0，旧工作流在 v1.0.0 上排空

# 退役 v1.0.0 之前检查是否还有旧工作流
old_workflows = DBOS.list_workflows(
    app_version="1.0.0",
    status=["PENDING", "ENQUEUED"]
)

if len(old_workflows) == 0:
    # 可以安全退役旧版本
    pass
```

将工作流分叉到新版本运行：

```python
# 将工作流从第 5 步分叉到 2.0.0 版本
new_handle = DBOS.fork_workflow(
    workflow_id="old-workflow-id",
    start_step=5,
    application_version="2.0.0"
)
```

参考：[Versioning](https://docs.dbos.dev/python/tutorials/upgrading-workflows#versioning)
