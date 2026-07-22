---
title: 初始化 DBOSClient 以支持外部访问
impact: HIGH
impactDescription: 让外部应用能够与 DBOS 交互
tags: client, setup, initialization, external
---

## 初始化 DBOSClient 以支持外部访问

使用 `DBOSClient` 从外部应用（API 服务器、CLI 工具等）与 DBOS 交互。

**错误（没有清理）：**

```python
from dbos import DBOSClient

client = DBOSClient(system_database_url=db_url)
handle = client.enqueue(options, data)
# 连接泄漏——没有 destroy()！
```

**正确（带上清理）：**

```python
import os
from dbos import DBOSClient

client = DBOSClient(
    system_database_url=os.environ["DBOS_SYSTEM_DATABASE_URL"]
)

try:
    handle = client.enqueue(options, data)
    result = handle.get_result()
finally:
    client.destroy()
```

构造器参数：
- `system_database_url`：DBOS 系统数据库的连接字符串
- `serializer`：必须与 DBOS 应用的序列化器一致（默认：pickle）

## API 参考

除了 `enqueue`，DBOSClient 镜像了 DBOS 的 API。可使用其他参考文件中相同的模式：

| DBOSClient 方法 | 对应的 DBOS 方法 |
|-------------------|---------------------|
| `client.send()` | `DBOS.send()` — 添加 `idempotency_key` 以实现精确一次 |
| `client.get_event()` | `DBOS.get_event()` |
| `client.read_stream()` | `DBOS.read_stream()` |
| `client.list_workflows()` | `DBOS.list_workflows()` |
| `client.cancel_workflow()` | `DBOS.cancel_workflow()` |
| `client.resume_workflow()` | `DBOS.resume_workflow()` |
| `client.retrieve_workflow()` | `DBOS.retrieve_workflow()` |

参考：[DBOSClient](https://docs.dbos.dev/python/reference/client)
