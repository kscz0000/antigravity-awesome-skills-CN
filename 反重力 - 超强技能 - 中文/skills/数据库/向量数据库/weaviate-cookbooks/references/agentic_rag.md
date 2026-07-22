# Agentic RAG Cookbook

使用 Weaviate 构建由 RAG 驱动的 AI Agent。

请先阅读：
- Basic Agent cookbook，务必先以此为基础。必读：[Basic Agent Cookbook](./basic_agent.md)

如需参考的文档：
- Weaviate 中的搜索模式与基础：https://docs.weaviate.io/weaviate/search/basics
- Weaviate 中的过滤器：https://docs.weaviate.io/weaviate/search/filters
- 混合检索：https://docs.weaviate.io/weaviate/search/hybrid
- Weaviate Query Agent：https://docs.weaviate.io/agents/query/usage
- Elysia：https://weaviate.github.io/elysia/


## 核心规则

请先实现[此处](./basic_agent.md)中的基础 Agent，再按本指南进行改造。

- 使用 `venv` 创建虚拟环境。
- 使用 `uv` 进行 Python 项目与依赖管理。
- 不要手动编写 `pyproject.toml` 或 `uv.lock`；由 `uv` 生成/更新。
- 使用的安装命令为：`uv add weaviate-client python-dotenv dspy`
- 使用 Query Agent 时，额外安装 `weaviate-agents`：`uv add "weaviate-client[agents]"`
- 使用 Elysia 时，额外安装 `elysia-ai`：`uv add elysia-ai`
- 依据用户规格定制本 cookbook；未给出时主动向用户询问细节。

假设用户已具备可用数据，除非用户要求，否则不要生成测试数据。

在沿用本 cookbook 之前，必须先询问用户是否更倾向于使用 Weaviate Query Agent 或 Elysia。若用户选择其中之一，请直接跳到对应章节。

- Query Agent 文档：https://docs.weaviate.io/agents/query/usage
- Elysia 文档：https://weaviate.github.io/elysia/

## 环境变量规则

必填：
- 一项 LLM 服务商 API 密钥（例如 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`GEMINI_API_KEY`）
- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`

外部服务商密钥：
- 仅填写目标 Weaviate 集合配置实际使用的密钥。


## Agentic RAG 概览

* 朴素 RAG 工具：*以单一工具的形式为 RouterAgent 提供基础检索*
* 分层 RAG：*由 LLM 生成过滤器与搜索参数，作为子 Agent 工具*
* 向量数据库记忆：*使用 Weaviate 在跨会话间存取事实*
* Query Agent：*Weaviate 自带的预构建 agentic RAG 服务*
* Elysia：*内置查询工具的开源 agentic 框架*


## 朴素 RAG 工具

一个简单的检索工具，可供 RouterAgent 调用。将其作为工具传入 [basic agent cookbook](./basic_agent.md) 中的 RouterAgent。

```python
from weaviate import connect_to_weaviate_cloud
import os

def retrieve_data(query: str):
    """
    Given a query (free text), return the most relevant documents from the vector database using hybrid search.
    """
    client = connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL", ""),
        auth_credentials=os.getenv("WEAVIATE_API_KEY", ""),
    )
    collection = client.collections.use("<collection_name>")
    response = collection.query.hybrid(query=query, limit=5)
    client.close()
    return f"{[obj.properties for obj in response.objects]}"
```

可根据用例定制检索类型（`hybrid`、`near_text`、`bm25`）、`limit` 与返回字段。


## 分层 RAG（LLM 生成的过滤器）

相比朴素检索，使用 LLM 子 Agent 来构造过滤器与搜索参数，使工具本身成为一个 Agent。

1. 用于过滤器的结构化响应模型：

```python
from pydantic import BaseModel, Field
from typing import Literal, Any

class SearchFilter(BaseModel):
    field: str = Field(description="The field to be filtered on.")
    operator: Literal["=", "!=", ">", "<"] = Field(description="The operator to be used in conjunction with the value.")
    value: Any = Field(description="The value to be used in conjunction with the operator.")

class Search(BaseModel):
    query: str = Field(description="The search query to be used in the vector database.")
    filters: list[SearchFilter] = Field(description="The filters to be used in the vector database.")
    limit: int = Field(description="The number of results to return from the vector database.")

class SearchCreation(dspy.Signature):
    """
    Create a search query for a vector database.
    """
    user_prompt: str = dspy.InputField()
    schema: list[dict] = dspy.InputField(desc="Schema of the collection to be searched.")
    search: Search = dspy.OutputField(
        desc=(
            "Your search query and filters, this should be a valid JSON object. "
            "This should be constructed so that it matches the goal of the user prompt."
        )
    )
```

2. 辅助函数：将结构化过滤器转换为 Weaviate 过滤器：

```python
from weaviate.classes.query import Filter

def format_filters(search_filters: list[SearchFilter]):
    filters = []
    for search_filter in search_filters:
        base_filter = Filter.by_property(search_filter.field)
        if search_filter.operator == "=":
            filters.append(base_filter.equal(search_filter.value))
        elif search_filter.operator == "!=":
            filters.append(base_filter.not_equal(search_filter.value))
        elif search_filter.operator == ">":
            filters.append(base_filter.greater_than(search_filter.value))
        elif search_filter.operator == "<":
            filters.append(base_filter.less_than(search_filter.value))
    return Filter.all_of(filters) if filters else None
```

3. 分层查询工具（用于替换朴素检索工具）：

```python
def query_agent_tool(collection_name: str, user_prompt: str):
    """
    Given a query (free text), return the most relevant documents from the vector database using hybrid search with LLM-generated filters.
    """
    client = connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL", ""),
        auth_credentials=os.getenv("WEAVIATE_API_KEY", ""),
    )
    collection = client.collections.use(collection_name)
    config = collection.config.get()
    schema = [{"name": p.name, "type": p.data_type[:]} for p in config.properties]

    query_model = dspy.ChainOfThought(SearchCreation)
    query_output = query_model(
        user_prompt=user_prompt,
        schema=schema,
        lm=dspy.LM("<subtask_model_name>")
    )

    response = collection.query.hybrid(
        query=query_output.search.query,
        filters=format_filters(query_output.search.filters),
        limit=query_output.search.limit
    )
    client.close()
    return f"{[obj.properties for obj in response.objects]}"
```

为了让 LLM 能够构造过滤器，必须提供 Schema 信息。可通过 `collection.config.get()` 动态获取；若 Schema 稳定，也可手动提供。可考虑附加样本数据或枚举值以提升过滤准确率。


## 向量数据库记忆

使用 Weaviate 在跨会话间存取事实。仅当需要跨会话持久化时才添加此能力。

1. 记忆创建签名：

```python
class MemoryCreation(dspy.Signature):
    user_prompt: str = dspy.InputField()
    assistant_response: str = dspy.InputField()
    memory: str = dspy.OutputField(
        description="A single string representing the most pertinent fact from the user/agent interaction."
    )
```

2. 为 `AgentResponse` 增加 `memories` 输入字段：

```python
class AgentResponse(dspy.Signature):

    # Input Fields
    history: dspy.History = dspy.InputField()
    user_prompt: str = dspy.InputField()
    available_tools: str = dspy.InputField()
    memories: list[str] = dspy.InputField(
        desc="A list of memories from previous conversations, you can use these to inform your response."
    )

    # Output Fields
    response: str = dspy.OutputField(
        description="The response to the user's prompt whilst the tool is running. Update the user on the progress of their request (if a tool is picked), or the final response to the user (if no tool is picked)."
    )
    tool: str | None = dspy.OutputField(
        description="The tool that needs to be used. Return None if no tool is needed."
    )
    tool_inputs: Dict[str, Any] | None = dspy.OutputField(
        description=(
            "The inputs for the tool. Return an empty dictionary (still include the field) if no inputs are needed. "
            "The key is the name of the input, the value is the value of the input."
        )
    )
```

3. 为 `RouterAgent` 增加 `create_memory` 与 `retrieve_memories` 方法：

```python
from weaviate import connect_to_weaviate_cloud
from weaviate.classes.config import Configure

class RouterAgent:
    def __init__(self, model: str, memory_model: str | None = None, tools: List[Callable] = []):
        self.tools: list[Callable] = tools
        self.model = dspy.LM(model)
        self.memory_model = dspy.LM(memory_model) if memory_model else dspy.LM(model)
        self.agent = dspy.ChainOfThought(AgentResponse)
        self.memory_agent = dspy.Predict(MemoryCreation)
        self.conversation_history = dspy.History(messages=[])
        self.weaviate_client = connect_to_weaviate_cloud(
            cluster_url=os.getenv("WEAVIATE_URL", ""),
            auth_credentials=os.getenv("WEAVIATE_API_KEY", ""),
        )

    # ... existing methods from basic_agent.md (add_conversation_history, get_tools_and_descriptions) ...

    def create_memory(self, user_prompt: str, assistant_response: str, tool_result: str):
        if tool_result:
            assistant_response += "\n" + tool_result

        result = self.memory_agent(
            history=self.conversation_history,
            user_prompt=user_prompt,
            assistant_response=assistant_response,
            lm=self.memory_model,
        )
        if not self.weaviate_client.collections.exists("Agent_Memory"):
            self.weaviate_client.collections.create(
                "Agent_Memory",
                vector_config=Configure.Vectors.text2vec_weaviate()
            )

        collection = self.weaviate_client.collections.use("Agent_Memory")
        collection.data.insert({"user_prompt": user_prompt, "memory": result.memory})
        return result.memory

    def retrieve_memories(self, user_prompt: str):
        if not self.weaviate_client.collections.exists("Agent_Memory"):
            return []
        collection = self.weaviate_client.collections.use("Agent_Memory")
        query = collection.query.near_text(query=user_prompt, limit=5)
        return [memory.properties["memory"] for memory in query.objects]
```

在每次交互开始时调用 `retrieve_memories`，将结果传入 `AgentResponse` 的 `memories` 字段；每次交互结束后调用 `create_memory`。

可考虑为记忆创建使用更便宜的模型（例如 `memory_model="<cheap_model_name>"`）。


## Weaviate Query Agent

跳过自建实现，直接使用 Weaviate 预构建的 Query Agent 来完成 agentic RAG。它会自动处理集合选择、过滤器构造与查询优化。

```python
from weaviate.agents.query import QueryAgent

# import client here

qa = QueryAgent(
    client=client, collections=["<collection_name>"]
)
response = qa.search("<user query here>")  # retrieval only
response = qa.ask("<user query here>")     # retrieval + text response via response.final_answer
```

Query Agent 每月前 1000 次请求免费。文档：https://docs.weaviate.io/agents/query/usage


## Elysia

Elysia 是一个开源的 agentic 框架，内置查询工具、决策树、错误处理与自动重试。

初始化：

```python
import elysia
from elysia.tools.text import FakeTextResponse as TextResponseTool

elysia.configure(
    base_model="<model_name>",
    base_provider="<provider>",  # e.g. "anthropic", "openai"
    logging_level="ERROR"
)
```

配合自定义工具：

```python
tree = elysia.Tree("empty", use_elysia_collections=False)
tree.add_tool(TextResponseTool)

@elysia.tool
async def your_tool(param: str):
    """Tool description."""
    return {"result"}

tree.add_tool(your_tool)
response, _ = tree("user query here")
```

配合内置的 Weaviate 查询工具（需先进行预处理）：

```python
from elysia import preprocess
preprocess("<collection_name>")

tree = elysia.Tree()
response, _ = tree(
    "user query here",
    collection_names=["<collection_name>"]
)
```

Elysia 内置错误处理、自愈与自动重试。同时也提供带前端 UI 的独立应用版本：https://github.com/weaviate/elysia


## 可定制点

**何时使用哪种方案：**

| 用例 | 推荐方案 |
|----------|---------------------|
| 单集合、查询简单 | 朴素 RAG 工具 |
| 需要过滤器或操作符 | 分层 RAG 或 Query Agent |
| 多步任务、多数据源 | 带 agentic 循环的顺序 Agent |
| 跨会话个性化 | 加入向量数据库记忆层 |
| 生产部署且需要错误处理 | 使用 Elysia 或 Query Agent |

**不要为简单检索任务实现多 Agent 架构。**

**LLM 框架**

本指南使用 DSPy。请遵循[此处](./basic_agent.md)中的指引，但你很可能需要支持结构化响应的 LLM 框架。


## 故障排查

- Weaviate 启动主机错误：确认 `WEAVIATE_URL` 是完整的 `https://...` URL。
- DSPy 签名中关于缺失字段的告警：在使用 followup Agent 而未传入所有字段时可能触发；请确保可选字段已被妥善处理。
- 其他问题：请查阅官方库/包文档，并充分利用网络搜索进行排查。

## 完成标准

- 编写测试脚本，使用测试数据分别验证每个函数是否独立工作。验证完成后清理临时测试，或使用 pytest 构建正式测试套件（需安装）。
- 用户已完成应用规格的确认。