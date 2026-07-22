# 构建数据探索应用

## 概述

基于 FastAPI 构建一个面向 Weaviate 集合的全栈数据探索应用。

请先阅读：
- Weaviate 中的搜索模式与基础：https://docs.weaviate.io/weaviate/search/basics
- Weaviate 中的过滤器：https://docs.weaviate.io/weaviate/search/filters

## 操作指引

### 核心规则

- 使用 `venv` 创建虚拟环境。
- 使用 `uv` 进行 Python 项目与依赖管理。
- 不要手动编写 `pyproject.toml` 或 `uv.lock`；由 `uv` 生成/更新。
- 后端安装依赖使用以下命令：
  - `uv add fastapi 'uvicorn[standard]' weaviate-client pydantic-settings python-dotenv`
- 根据用户需求：可考虑将该应用与 [Query Agent Chatbot](./query_agent_chatbot.md) 合并。
  - 若用户明确只需要数据查看/探索器，则独立构建本应用。
  - 若用户希望同时具备聊天与数据探索的完整功能，则合并两个应用。
  - 若没有明确指示，先询问用户偏好再继续。
  - 详见 [Next Steps](#next-steps) 章节。

### 快速初始化命令

项目引导：

```bash
uv init data_explorer
cd data_explorer
uv venv
uv add fastapi 'uvicorn[standard]' weaviate-client pydantic-settings python-dotenv
```

### 工作流约定

1. 一次性完成后端与前端构建。
2. 基于 `environment_requirements.md` 中的官方模板创建 `.env`，随后添加应用专属字段（例如 `CORS_ORIGINS`）。
3. 在要求用户填写环境变量之前，先进行不依赖真实凭据的本地非密钥自检（导入/编译/启动形态检查）。
4. 要求用户填写真实的环境变量值：
   - 必填：`WEAVIATE_URL`、`WEAVIATE_API_KEY`
   - 可选：仅其集合配置真正需要的服务商密钥
5. 用户确认后，验证后端能无错误启动，并提供可在终端运行的精确命令。

不要问那些可以通过上下文自行解决的回避性问题。

### 目录结构

采用模块化布局，例如：

```text
data_explorer/
  backend/
    app/
      main.py
      config.py
      lifespan.py
      dependencies.py
      routers/
      services/
      models/
    .env  # local file, never committed
```

保持以下边界：

- routers：仅处理 HTTP
- services：业务/Query Agent 逻辑
- models：请求/响应模型
- config/lifespan：装配与启动/关闭

### 后端要求

- FastAPI 异步应用，使用 lifespan 管理生命周期。
- 在 lifespan 中初始化异步 Weaviate 客户端，并在关闭时关闭连接。
- 确保没有会阻塞事件循环的同步操作。
- 并非完整的 CRUD 实现 —— 本应用仅用于查看 Weaviate 集合中的数据。
- 接口：
  - `GET /health`
  - `GET /env_check`：返回缺失的 API 密钥（若有），用于在应用启动时校验
  - `GET /collections`：返回可用的集合
  - `GET /data/{collection_name}?xx=xx&yy=yy`：按需返回数据，支持后续扩展参数与分页
- Pydantic settings 从进程环境读取；本地开发时可选加载本地 `.env`。
- 对话历史需映射为 Weaviate 聊天消息格式。

### 环境变量规则

必填：
- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`

外部服务商密钥：
- 包含目标集合所需的全部服务商密钥。
- 未使用的服务商密钥留空或注释掉。

CORS：

- 默认 `CORS_ORIGINS` 应包含：
  - `http://localhost:3000`
  - `http://127.0.0.1:3000`
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`

### FastAPI 规范

1. 不要使用硬编码的状态值，使用 FastAPI 的 `status`，例如：

```python
from fastapi import status
status.HTTP_200_OK # code 200
status.HTTP_404_NOT_FOUND # code 404
# and more
```

2. 对于所有需要 `request` 或 `response_model` 的接口，使用 Pydantic `BaseModel`，通过模式校验减少 API 用户输入错误。

3. GET 接口应使用路径参数与查询参数，而非请求体，例如：

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}
```

```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

4. 按照最佳实践进行错误处理：采用 early return 并在必要时给出正确的状态码。

5. 使用规范的日志记录 API 调用，不要使用简单的 print。

### FastAPI 接口

接口的基础结构。可按用户偏好或适配情况进行定制，不要机械照搬，仅作为参考。

同时请遵循标准 FastAPI 流程，例如全局错误处理、日志、依赖注入。配置一个异步客户端管理器，在启动时通过 lifespan 连接，在应用退出时优雅关闭，并通过依赖注入将客户端注入到相关接口。

#### GET /health

标准的健康检查接口，例如：

```python
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

@app.get("/health", tags=["health"], response_model=HealthResponse)
async def health_check() -> HealthResponse:
    logger.info("Health check requested")
    return HealthResponse(status="healthy")
```

#### GET /env_check

检查后端可访问哪些环境变量，用于确认用户的 Weaviate 配置是否正确，例如：

```python
import os
from pydantic import BaseModel

class EnvCheckResponse(BaseModel):
    weaviate_url: bool
    weaviate_api_key: bool

@app.get("/env_check", tags=["health"])
async def env_check() -> EnvCheckResponse:
    logger.info("Environment check requested")
    return EnvCheckResponse(
        weaviate_url = os.getenv("WEAVIATE_URL") is not None,
        weaviate_api_key = os.getenv("WEAVIATE_API_KEY") is not None,
    )
```

### GET /collections

查看可用的集合，例如：

```python
from pydantic import BaseModel
from weaviate.client import WeaviateAsyncClient

class CollectionsResponse(BaseModel):
    collections: list[str]

@app.get("/collections", tags=["collections"])
async def collections() -> CollectionsResponse:

    # include client management to import async client here

    logger.info("Collections requested")
    collections = await client.collections.list_all()
    return CollectionsResponse(
        collections = list(collections.keys())
    )
```

提示：可考虑扩展该接口，附带集合的描述与配置。`await client.collections.list_all()` 返回 `dict[str, _CollectionConfigSimple]`，其中 `_CollectionConfigSimple` 包含如下属性：

- `description`：`str`
- `properties`：`list[Property]`，`Property` 含 `.name`、`.description` 与 `.data_type`（可通过 `.data_type[:]` 获取数据类型名称字符串）
- `vector_config`：`dict[str, _NamedVectorConfig]`，`_NamedVectorConfig` 含属性 `.vectorizer.vectorizer`（不是笔误），可通过 `.vectorizer.vectorizer[:]` 获取向量器名称字符串。

多租户信息可通过以下方式检查：

```python
config = await collection.config.get()
config.multi_tenancy_config.enabled # bool
```

该信息在 `_CollectionConfigSimple` 中不可用，必须通过 `collection.config.get()` 获取。

#### GET /data/{collection_name}

通过分页、排序与过滤器从集合中获取数据。

```python
from weaviate.collections import CollectionAsync
from fastapi import Query
from pydantic import BaseModel
from typing import Any

async def get_collection_data_types(collection: CollectionAsync) -> dict[str, str]:
    config = await collection.config.get()
    properties = config.properties
    return {prop.name: prop.data_type[:] for prop in properties}

class GetDataResponse(BaseModel):
    data_types: dict[str, str]
    items: list[dict[str, Any]]

@router.post("/data/{collection_name}")
async def get_data(
    collection_name: str,
    page_size: int = Query(default=10, ge=1, le=100),
    page_number: int = Query(default=1, ge=1),
    query: str = Query(default=""),
    sort_on: str = Query(default=None),
    ascending: bool = Query(default=True),
) -> GetDataResponse:

    # include client management to import async client here

    collection = await client.collections.use(collection_name)
    data_types = await async_get_collection_data_types(collection)

    if query != "":
        response = await collection.query.bm25(
            query=query,
            limit=page_size,
            offset=page_size * (page_number - 1),
        )
    elif sort_on is not None:
        response = await collection.query.fetch_objects(
            sort=Sort.by_property(name=sort_on, ascending=ascending),
            limit=page_size,
            offset=page_size * (page_number - 1),
        )
    else:
        response = await collection.query.fetch_objects(
            limit=page_size,
            offset=page_size * (page_number - 1),
        )

    return GetDataResponse(data_types = data_types, items = [obj.properties for obj in response.objects])
```

提示：部分集合可能启用多租户。可考虑在 `get_data` 中将 tenant 作为可选查询参数，例如：

```python
async def get_data(
    ... # existing args
    tenant: str | None = Query(default=None)
):
    base_collection = await client.collections.use(collection_name)
    data_types = await async_get_collection_data_types(collection)

    config = await collection.config.get()
    if config.multi_tenancy_config.enabled and tenant and tenant.strip():
        collection = base_collection.with_tenant(tenant)
    else:
        collection = base_collection

    # ...existing code
```

### 环境变量填写后的引导（必需）

在用户确认所需环境变量已设置后，提供用于运行后端的终端命令：

```bash
cd data_explorer/backend
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

随后：

- 请用户启动终端。
- 自行对运行中的服务执行冒烟测试。
- 用简洁语言报告通过/失败，并修复阻塞问题。

除非用户明确要求，不要将详细测试步骤推给用户。

## 故障排查

- Weaviate 启动主机错误：确认 `WEAVIATE_URL` 是完整的 `https://...` URL。
- 其他问题：请查阅官方库/包文档并结合网络搜索定位。

## 完成标准

- 后端健康检查通过。
- 所有接口正常工作。
- 用户可在终端使用提供的命令运行服务。

## 后续步骤

本应用当前仅是一个数据探索后端。可根据用户偏好，提议将其与 [Query Agent Chatbot](./query_agent_chatbot.md) 集成。

若用户选择合并两个应用，按以下方式实现集成：

- 创建或使用 `/routes` 目录，分别承载 Query Agent 聊天与数据探索功能。在 `main.py` 中导入这些路由。
- 若需要前端，则根据设计选择使用多页面/多标签页，以区分数据探索与聊天。
- 考虑功能间的交叉联动，例如从数据查看器/集合查看器提供聊天按钮，跳转后自动选中对应集合进入聊天。
- 运行快速测试，确保集成顺畅，用户可以无障碍地使用聊天机器人和数据探索功能。

### 前端

仅当用户明确要求前端时，使用以下指引：

- [Frontend Interface](frontend_interface.md)：构建 Next.js 前端以对接 Weaviate 后端。