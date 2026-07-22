# 异步客户端用法

在生产环境应用（FastAPI、异步框架）中使用 Weaviate Python 异步客户端的指引。

## 官方文档参考

**面向智能体：** 如果遇到本文未覆盖的问题，请查阅 Weaviate 官方文档：

- **主要参考**：[Weaviate Async API 文档](https://docs.weaviate.io/weaviate/client-libraries/python/async)
- **Python 客户端参考**：[Weaviate Python Client 文档](https://docs.weaviate.io/weaviate/client-libraries/python)
- **API 参考**：[ReadTheDocs - Python Client](https://weaviate-python-client.readthedocs.io/en/stable/)
- **故障排查**：[社区论坛](https://forum.weaviate.io/) | [GitHub Issues](https://github.com/weaviate/weaviate-python-client/issues)

> **注意：** 异步客户端（`WeaviateAsyncClient`）在 `weaviate-client` v4.7.0+ 中可用。

## 连接方式

提供三种实例化辅助函数（[文档](https://docs.weaviate.io/weaviate/client-libraries/python/async#instantiation)）：

### Weaviate Cloud（推荐）

```python
import weaviate
from weaviate.classes.init import Auth

# Use the official helper function for Weaviate Cloud
client = weaviate.use_async_with_weaviate_cloud(
    cluster_url="your-cluster.weaviate.cloud",  # Accepts hostname with or without https://
    auth_credentials=Auth.api_key("your-api-key"),
    headers={  # Note: parameter is "headers" not "additional_headers"
        "X-OpenAI-Api-Key": "sk-...",
        "X-Anthropic-Api-Key": "sk-ant-...",
    }
)

await client.connect()  # Required! Async helpers don't auto-connect
```

**参考**：[Weaviate Cloud Setup](https://docs.weaviate.io/weaviate/quickstart)

### 自托管

```python
# For local instances
client = weaviate.use_async_with_local()

# For custom endpoints
client = weaviate.use_async_with_custom(
    http_host="localhost",
    http_port=8080,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False,
)

await client.connect()
```

**参考**：[Connection Configuration](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html)

### 身份认证

支持多种认证方式（[文档](https://docs.weaviate.io/weaviate/client-libraries/python#authentication)）：

```python
from weaviate.classes.init import Auth

# API Key (most common for Weaviate Cloud)
auth = Auth.api_key("your-api-key")

# Bearer Token (with optional refresh token)
auth = Auth.bearer_token("access-token", refresh_token="refresh-token")

# Client Credentials (OIDC)
auth = Auth.client_credentials(client_secret="secret")

# Client Password (OIDC Resource Owner Password flow)
auth = Auth.client_password(username="user", password="pass")

# Usage
client = weaviate.use_async_with_weaviate_cloud(
    cluster_url="your-cluster.weaviate.cloud",
    auth_credentials=auth,
)
```

## 关键模式

### 连接生命周期

**重要**：与同步辅助函数不同，异步辅助函数**不会自动连接**（[文档](https://docs.weaviate.io/weaviate/client-libraries/python/async#instantiation)）。你必须显式调用 `.connect()` 与 `.close()`：

```python
# ❌ Wrong - client not connected
client = weaviate.use_async_with_weaviate_cloud(...)
collections = await client.collections.list_all()  # Will fail!

# ✅ Correct - explicit connect/close
client = weaviate.use_async_with_weaviate_cloud(...)
await client.connect()
collections = await client.collections.list_all()
await client.close()
```

### 同步 vs 异步方法

**关键区别**（[文档](https://docs.weaviate.io/weaviate/client-libraries/python/async#which-methods-are-async)）：涉及服务端请求的方法是异步的；本地操作是同步的。

```python
# Collection retrieval is SYNC (no await)
collection = client.collections.get("MyCollection")

# Operations on collections are ASYNC (need await)
config = await collection.config.get()
results = await collection.query.fetch_objects()
count = await collection.aggregate.over_all()
```

**规则：** 获取 collection 对象是同步；调用其方法是异步。

### 批量操作

**重要提示**（[文档](https://docs.weaviate.io/weaviate/client-libraries/python/async#bulk-import-operations)）：对于大规模数据导入，应使用**同步客户端**及其批处理操作。同步客户端的批方法已在内部处理并发，并针对批量操作做了优化。

```python
# ✅ For bulk imports, prefer sync client
import weaviate

with weaviate.connect_to_weaviate_cloud(...) as client:
    collection = client.collections.get("MyCollection")

    # Batch insert handles concurrency automatically
    with collection.batch.dynamic() as batch:
        for item in large_dataset:
            batch.add_object(properties=item)
```

异步客户端的使用场景：

- Web 应用（FastAPI、Starlette）
- 并发请求处理
- 交互式查询

不要将异步客户端用于：

- 批量数据导入（请改用同步客户端）

## 上下文管理器模式（推荐）

**最佳实践**（[文档](https://docs.weaviate.io/weaviate/client-libraries/python/async#using-the-async-context-manager)）：使用 `async with` 自动连接/断开：

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def get_weaviate_client(
    cluster_url: str,
    api_key: str,
    provider_headers: dict[str, str] | None = None,
) -> AsyncGenerator[weaviate.WeaviateAsyncClient, None]:
    """Connect to Weaviate Cloud with automatic cleanup."""
    # Remove scheme if present
    hostname = cluster_url.replace("https://", "").replace("http://", "")

    client = weaviate.use_async_with_weaviate_cloud(
        cluster_url=hostname,
        auth_credentials=Auth.api_key(api_key),
        headers=provider_headers,
    )

    try:
        await client.connect()
        yield client
    finally:
        await client.close()

# Usage
async def example():
    async with get_weaviate_client(
        cluster_url="your-cluster.weaviate.cloud",
        api_key="your-key",
    ) as client:
        collections = await client.collections.list_all()
```

> **注意：** 使用上下文管理器时，`.connect()` 与 `.close()` 会被自动调用。

## FastAPI 集成

**使用场景**（[文档](https://docs.weaviate.io/weaviate/client-libraries/python/async#use-cases)）：异步客户端在 FastAPI 等 Web 框架中处理并发请求时表现尤为出色。

使用 lifespan 管理在多个请求间共享的客户端：

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to Weaviate
    app.state.weaviate = weaviate.use_async_with_weaviate_cloud(
        cluster_url="your-cluster.weaviate.cloud",
        auth_credentials=Auth.api_key("your-key"),
    )
    await app.state.weaviate.connect()

    yield

    # Shutdown: close connection
    await app.state.weaviate.close()

app = FastAPI(lifespan=lifespan)

@app.get("/collections")
async def list_collections():
    collections = await app.state.weaviate.collections.list_all()
    return {"collections": list(collections.keys())}
```

**社区讨论**：[FastAPI 最佳实践](https://forum.weaviate.io/t/what-is-the-best-practice-to-use-v4-python-client-for-query-with-fastapi-or-other-async-python-framework/1245)

## 常见陷阱

### 1. 参数名混淆

```python
# ❌ Wrong - WeaviateAsyncClient() constructor uses different param
client = weaviate.use_async_with_weaviate_cloud(
    additional_headers={...}  # Wrong parameter name!
)

# ✅ Correct - use "headers" not "additional_headers"
client = weaviate.use_async_with_weaviate_cloud(
    headers={...}
)
```

### 2. URL 格式

两种格式都可被辅助函数接受：

```python
# ✅ Both accepted
client = weaviate.use_async_with_weaviate_cloud(
    cluster_url="https://cluster.weaviate.cloud"  # With scheme
)

client = weaviate.use_async_with_weaviate_cloud(
    cluster_url="cluster.weaviate.cloud"  # Without scheme
)
```

### 3. 同步 vs 异步函数名

```python
# ❌ Wrong - sync client (cannot use await)
client = weaviate.connect_to_weaviate_cloud(...)
await client.connect()  # TypeError!

# ✅ Correct - async client
client = weaviate.use_async_with_weaviate_cloud(...)
await client.connect()
```

**命名规则：**

- 同步：`connect_to_*`（例如 `connect_to_weaviate_cloud`）
- 异步：`use_async_with_*`（例如 `use_async_with_weaviate_cloud`）

### 4. 端口配置

```python
# ❌ Wrong - manual port config causes conflicts with Weaviate Cloud
client = WeaviateAsyncClient(
    connection_params=ConnectionParams.from_url(
        url="https://cluster.weaviate.cloud",
        grpc_port=443,  # Conflict!
    )
)

# ✅ Correct - use helper function (handles ports automatically)
client = weaviate.use_async_with_weaviate_cloud(
    cluster_url="cluster.weaviate.cloud"
)
```

**规则：** 对于 Weaviate Cloud，请始终使用 `use_async_with_weaviate_cloud()` —— 它能正确处理 HTTP（443）与 gRPC（50051）端口。

## 多集群示例

管理到多个 Weaviate 集群的连接：

```python
@asynccontextmanager
async def get_multi_cluster_clients(
    clusters: dict[str, dict[str, str]]
) -> AsyncGenerator[dict[str, weaviate.WeaviateAsyncClient], None]:
    """Connect to multiple Weaviate clusters.

    Args:
        clusters: Dict of {cluster_id: {"url": "...", "api_key": "..."}}
    """
    clients = {}

    try:
        # Connect to all clusters
        for cluster_id, config in clusters.items():
            client = weaviate.use_async_with_weaviate_cloud(
                cluster_url=config["url"],
                auth_credentials=Auth.api_key(config["api_key"]),
            )
            await client.connect()
            clients[cluster_id] = client

        yield clients

    finally:
        # Close all connections
        for client in clients.values():
            await client.close()

# Usage
async def example():
    clusters = {
        "prod": {"url": "prod.weaviate.cloud", "api_key": "key1"},
        "dev": {"url": "dev.weaviate.cloud", "api_key": "key2"},
    }

    async with get_multi_cluster_clients(clusters) as clients:
        prod_collections = await clients["prod"].collections.list_all()
        dev_collections = await clients["dev"].collections.list_all()
```

## 环境变量

关于服务商 API 密钥，请参阅 [Environment Requirements](environment_requirements.md)。

```python
import os

# Read from environment
cluster_url = os.environ["WEAVIATE_URL"]
api_key = os.environ["WEAVIATE_API_KEY"]

# Build provider headers
provider_headers = {}
if openai_key := os.getenv("OPENAI_API_KEY"):
    provider_headers["X-OpenAI-Api-Key"] = openai_key
if anthropic_key := os.getenv("ANTHROPIC_API_KEY"):
    provider_headers["X-Anthropic-Api-Key"] = anthropic_key

client = weaviate.use_async_with_weaviate_cloud(
    cluster_url=cluster_url,
    auth_credentials=Auth.api_key(api_key),
    headers=provider_headers or None,
)
```

## 测试异步代码

```python
import pytest

@pytest.mark.asyncio
async def test_weaviate_connection():
    async with get_weaviate_client(
        cluster_url="test-cluster.weaviate.cloud",
        api_key="test-key",
    ) as client:
        collections = await client.collections.list_all()
        assert isinstance(collections, dict)
```

## 速查表

| 任务             | 模式                                       | 是否 await  |
| ---------------- | --------------------------------------------- | ------- |
| Create client    | `weaviate.use_async_with_weaviate_cloud(...)` | 否      |
| Connect          | `client.connect()`                            | **是** |
| Get collection   | `client.collections.get("Name")`              | 否      |
| List collections | `client.collections.list_all()`               | **是** |
| Query data       | `collection.query.fetch_objects()`            | **是** |
| Get config       | `collection.config.get()`                     | **是** |
| Aggregate        | `collection.aggregate.over_all()`             | **是** |
| Close            | `client.close()`                              | **是** |

## 故障排查

### 常见问题

| 问题                                                 | 解决方案                                            | 参考                                                                         |
| ----------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------- |
| 连接长时间挂起                                 | 使用上下文管理器或确保正确调用 `.close()`     | [GitHub #753](https://github.com/weaviate/weaviate-python-client/issues/753)      |
| 多 worker 冲突（Gunicorn）                     | 使用 lifespan 管理，而非启动钩子          | [GitHub #1292](https://github.com/weaviate/weaviate-python-client/issues/1292)    |
| `TypeError: object NoneType can't be used in 'await'` | 使用 `use_async_with_*`，而非 `connect_to_*`           | [Async API Docs](https://docs.weaviate.io/weaviate/client-libraries/python/async) |
| 与 Weaviate Cloud 的端口冲突                    | 使用辅助函数，而非手写 `ConnectionParams` | 参见上方 "常见陷阱 #4"                                                    |

### 寻求帮助

**面向智能体：** 遇到错误时：

1. 查阅上文的 [Common Pitfalls](#common-pitfalls) 章节
2. 在 [Community Forum](https://forum.weaviate.io/) 搜索类似问题
3. 在 [GitHub Issues](https://github.com/weaviate/weaviate-python-client/issues) 查阅已知缺陷
4. 参考 [官方异步文档](https://docs.weaviate.io/weaviate/client-libraries/python/async)
5. 回顾 [Python 客户端最佳实践](https://docs.weaviate.io/weaviate/client-libraries/python/notes-best-practices)

## 补充资源

### 官方文档

- **主要参考**：[Weaviate Async API](https://docs.weaviate.io/weaviate/client-libraries/python/async)
- **Python 客户端**：[主文档](https://docs.weaviate.io/weaviate/client-libraries/python)
- **API 参考**：[ReadTheDocs](https://weaviate-python-client.readthedocs.io/en/stable/)
- **最佳实践**：[Notes and Best Practices](https://docs.weaviate.io/weaviate/client-libraries/python/notes-best-practices)

### 框架集成

- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [Python Async Context Managers](https://docs.python.org/3/reference/datamodel.html#asynchronous-context-managers)

### 社区

- [Weaviate Community Forum](https://forum.weaviate.io/)
- [Python Client GitHub](https://github.com/weaviate/weaviate-python-client)
- [Weaviate Blog](https://weaviate.io/blog)