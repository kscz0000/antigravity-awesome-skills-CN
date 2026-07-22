---
name: dbos-python
description: "使用 DBOS 持久化工作流构建可靠、容错 Python 应用的指南。触发词：DBOS、持久化工作流、Python 工作流、容错应用、DBOS 队列、工作流步骤、DBOSClient。当添加 DBOS 到现有 Python 代码、创建工作流和步骤、使用队列进行并发控制时使用。"
risk: safe
source: "https://docs.dbos.dev/"
date_added: "2026-02-27"
---

# DBOS Python 最佳实践

使用 DBOS 持久化工作流构建可靠、容错 Python 应用的指南。

## 使用场景

在以下情况下参考这些指南：
- 将 DBOS 添加到现有 Python 代码
- 创建工作流和步骤
- 使用队列进行并发控制
- 实现工作流通信（事件、消息、流）
- 配置和启动 DBOS 应用
- 从外部应用使用 DBOSClient
- 测试 DBOS 应用

## 按优先级分类的规则

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | Lifecycle | CRITICAL | `lifecycle-` |
| 2 | Workflow | CRITICAL | `workflow-` |
| 3 | Step | HIGH | `step-` |
| 4 | Queue | HIGH | `queue-` |
| 5 | Communication | MEDIUM | `comm-` |
| 6 | Pattern | MEDIUM | `pattern-` |
| 7 | Testing | LOW-MEDIUM | `test-` |
| 8 | Client | MEDIUM | `client-` |
| 9 | Advanced | LOW | `advanced-` |

## 关键规则

### DBOS 配置与启动

DBOS 应用必须在其 main 函数内配置并启动 DBOS：

```python
import os
from dbos import DBOS, DBOSConfig

@DBOS.workflow()
def my_workflow():
    pass

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
```

### 工作流与步骤结构

工作流由步骤组成。任何执行复杂操作或访问外部服务的函数必须是步骤：

```python
@DBOS.step()
def call_external_api():
    return requests.get("https://api.example.com").json()

@DBOS.workflow()
def my_workflow():
    result = call_external_api()
    return result
```

### 关键约束

- 不要在步骤中调用 `DBOS.start_workflow` 或 `DBOS.recv`
- 不要使用线程启动工作流 - 使用 `DBOS.start_workflow` 或队列
- 工作流必须是确定性的 - 非确定性操作放在步骤中
- 不要在工作流或步骤中创建/更新全局变量

## 使用方法

阅读各个规则文件以获取详细说明和示例：

```
references/lifecycle-config.md
references/workflow-determinism.md
references/queue-concurrency.md
```

## 参考资料

- https://docs.dbos.dev/
- https://github.com/dbos-inc/dbos-transact-py

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
