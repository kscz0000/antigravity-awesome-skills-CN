---
title: 使用补丁安全地升级工作流
impact: LOW
impactDescription: 在不中断进行中工作流的前提下部署破坏性变更
tags: patching, upgrade, versioning, migration
---

## 使用补丁安全地升级工作流

使用 `DBOS.patch()` 安全地部署破坏性的工作流变更。破坏性变更会改变运行的步骤或其顺序。

**错误（无补丁的破坏性变更）：**

```python
# 原始
@DBOS.workflow()
def workflow():
    foo()
    bar()

# 更新后——破坏正在执行的工作流！
@DBOS.workflow()
def workflow():
    baz()  # 替换了 foo()——检查点不匹配
    bar()
```

**正确（使用补丁）：**

```python
# 在配置中启用补丁
config: DBOSConfig = {
    "name": "my-app",
    "enable_patching": True,
}
DBOS(config=config)

@DBOS.workflow()
def workflow():
    if DBOS.patch("use-baz"):
        baz()  # 新工作流使用 baz
    else:
        foo()  # 旧工作流继续使用 foo
    bar()
```

所有旧工作流完成后弃用补丁：

```python
# 步骤 1：弃用（所有工作流都运行，但停止插入标记）
@DBOS.workflow()
def workflow():
    DBOS.deprecate_patch("use-baz")
    baz()
    bar()

# 步骤 2：完全移除（所有已弃用的工作流完成后）
@DBOS.workflow()
def workflow():
    baz()
    bar()
```

`DBOS.patch(name)` 的返回值：
- 新工作流返回 `True`（补丁部署后启动）
- 旧工作流返回 `False`（补丁部署前启动）

参考：[Patching](https://docs.dbos.dev/python/tutorials/upgrading-workflows#patching)
