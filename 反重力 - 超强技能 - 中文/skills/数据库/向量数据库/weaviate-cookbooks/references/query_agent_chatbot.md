# 构建 Weaviate Query Agent 聊天机器人

## 概述

以最少来回沟通构建一个全栈 Query Agent 聊天机器人。

请先阅读：
- Weaviate Query Agent 用法：https://docs.weaviate.io/agents/query/usage

## 操作指引

### 核心规则

- 使用 `uv` 进行 Python 项目与依赖管理。
- 不要手动编写 `pyproject.toml` 或 `uv.lock`；由 `uv` 生成/更新。
- 后端安装依赖使用以下命令：
  - `uv add fastapi 'uvicorn[standard]' weaviate-client weaviate-agents pydantic-settings sse-starlette python-dotenv`
- 若环境无 `uv`，可创建 `requirements.txt` 通过 pip 安装。
- 根据用户需求：可考虑将该应用与 Data Explorer 合并。
  - 若用户明确只需要聊天机器人，则独立构建本应用。
  - 若用户希望同时具备聊天与数据探索的完整功能，则合并两个应用。
  - 若没有明确指示，先询问用户偏好再继续。
  - 详见 [Next Steps](#next-steps) 章节。

### 快速初始化命令

项目引导：

```bash
uv init chatbot
cd chatbot
uv venv
uv add fastapi 'uvicorn[standard]' weaviate-client weaviate-agents pydantic-settings sse-starlette python-dotenv
```

### 工作流约定

1. 一次性完成后端构建。
2. 基于 `environment_requirements.md` 中的官方模板创建 `.env`，随后添加应用专属字段（例如 `COLLECTIONS`）。
3. 在要求用户填写环境变量之前，先进行不依赖真实凭据的本地非密钥自检（导入/编译/启动形态检查）。
4. 要求用户填写真实的环境变量值：
   - 必填：`WEAVIATE_URL`、`WEAVIATE_API_KEY`、`COLLECTIONS`
   - 可选：仅其集合配置真正需要的服务商密钥
5. 用户确认后，验证后端能无错误启动，并提供可在终端运行的精确命令。

不要问那些可以通过上下文自行解决的回避性问题。

### 目录结构

采用模块化布局，例如：

```text
chatbot/
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
- Query Agent 服务层（`ask` + `ask_stream`）。
- 对于异步 FastAPI 后端，使用 `AsyncQueryAgent`（而非 `QueryAgent`），以保证 `await agent.ask(...)` 和 `async for ... in agent.ask_stream(...)` 可正常工作。
- 接口：
  - `GET /health`
  - `POST /chat`
  - `POST /chat/stream`（SSE）
- Pydantic settings 从进程环境读取；本地开发时可选加载本地 `.env`。
- 对话历史需映射为 Weaviate 聊天消息格式。

### 来源处理

- 对每个 ask 响应，将输出标准化为：
  - `answer`：`response.final_answer` 中的文本（兜底为 `""`）
  - `sources`：由 `response.sources` 构造的 `{ "collection": ..., "object_id": ... }` 列表
  - `source_count`：`len(sources)`
- `POST /chat` 必须返回 `answer`、`sources`、`source_count`。
- `POST /chat/stream` 的最终 SSE 事件必须包含同样的字段。
- 若没有来源，返回 `sources: []` 与 `source_count: 0`。

### 环境变量规则

必填：
- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`
- `COLLECTIONS`

外部服务商密钥：
- 包含目标集合所需的全部服务商密钥。
- 未使用的服务商密钥留空或注释掉。

CORS：

- 默认 `CORS_ORIGINS` 应包含：
  - `http://localhost:3000`
  - `http://127.0.0.1:3000`
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`

### 环境变量填写后的引导（必需）

在用户确认所需环境变量已设置后，提供用于运行后端的终端命令：

```bash
cd chatbot/backend
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

随后：

- 请用户启动终端。
- 自行对运行中的服务执行冒烟测试。
- 用简洁语言报告通过/失败，并修复阻塞问题。

除非用户明确要求，不要将详细测试步骤推给用户。

## 故障排查

- `OPTIONS /chat/stream 400`：修正 CORS 来源不匹配问题（`localhost` 与 `127.0.0.1`）。
- Weaviate 启动主机错误：确认 `WEAVIATE_URL` 是完整的 `https://...` URL。
- 其他问题：请查阅官方库/包文档并结合网络搜索定位。

## 完成标准

- 后端健康检查通过。
- `/chat` 可用。
- `/chat/stream` 可输出进度/token/最终结果。
- `/chat` 与 `/chat/stream` 的最终响应均包含 `sources` 与 `source_count`。
- 用户可在终端使用提供的命令运行服务。

## 后续步骤

本应用当前仅是一个聊天机器人后端。可根据用户偏好，提议将其与 [Data Explorer](./data_explorer.md) 集成。

若用户选择合并两个应用，按以下方式实现集成：

- 创建或使用 `/routes` 目录，分别承载 Query Agent 聊天与数据探索功能。在 `main.py` 中导入这些路由。
- 若需要前端，则根据设计选择使用多页面/多标签页，以区分数据探索与聊天。
- 考虑功能间的交叉联动，例如从数据查看器/集合查看器提供聊天按钮，跳转后自动选中对应集合进入聊天。
- 运行快速测试，确保集成顺畅，用户可以无障碍地使用聊天机器人和数据探索功能。

### 前端

仅当用户明确要求前端时，使用以下指引：

- [Frontend Interface](frontend_interface.md)：构建 Next.js 前端以对接 Weaviate 后端。
- 在聊天响应 UI 中渲染 `sources` 与 `source_count` 的来源引用。