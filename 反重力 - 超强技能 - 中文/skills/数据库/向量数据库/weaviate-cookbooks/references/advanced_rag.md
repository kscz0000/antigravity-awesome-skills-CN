# 进阶 RAG Cookbook

使用 Weaviate 构建进阶 RAG 功能。

请先阅读：
- Basic RAG cookbook，务必先以此为基础。必读：[Basic RAG Cookbook](./basic_rag.md)

如需参考的文档：
- Weaviate 中的搜索模式与基础：https://docs.weaviate.io/weaviate/search/basics
- Weaviate 中的过滤器：https://docs.weaviate.io/weaviate/search/filters
- 向量检索：https://docs.weaviate.io/weaviate/search/similarity
- 关键词检索：https://docs.weaviate.io/weaviate/search/bm25
- 混合检索：https://docs.weaviate.io/weaviate/search/hybrid
- 图像检索：https://docs.weaviate.io/weaviate/search/image


## 核心规则

请先实现[此处](./basic_rag.md)中的基础策略，再按本指南进行改造。

- 使用 `venv` 创建虚拟环境。
- 使用 `uv` 进行 Python 项目与依赖管理。
- 不要手动编写 `pyproject.toml` 或 `uv.lock`；由 `uv` 生成/更新。
- 使用的安装命令为：`uv add weaviate-client python-dotenv dspy weaviate-agents`
- 依据用户规格定制本 cookbook；未给出时主动向用户询问细节。

假设用户已具备可用数据，除非用户要求，否则不要生成测试数据。

在沿用本 cookbook 之前，必须先询问用户是否更倾向于使用 Weaviate Query Agent。若用户选择 Query Agent，则本指南的全部步骤都可以交由 Query Agent 直接完成（它开箱即支持进阶 RAG）。

Query Agent 文档：https://docs.weaviate.io/agents/query/usage

## 环境变量规则

必填：
- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`

外部服务商密钥：
- 仅填写目标 Weaviate 集合配置实际使用的密钥。

## 进阶 RAG 概览

* Query 改写（Query Re-writer）：*使用 LLM 将用户输入文本改写为查询文本*
* Query 分解（Query Decomposition）：*将查询拆分为多个子查询，每个子查询均由 LLM 改写*
* 过滤（Filtering）：*使用 LLM 在集合上定义过滤器*
* 重排序（Re-ranking）：*使用更强大的模型对最终结果打分*
* 提示工程（Prompt Engineering）：*加入思维链、思维树、ReAct 等*

## Query 改写

```python
class QueryRewriter(dspy.Signature):
    """
    Rewrite the user's query into a more relevant search term that is a more relevant search term for searching a database.
    """
    input_query: str = dspy.InputField(description="The original user query")
    rewritten_query: str = dspy.OutputField(
        description=(
            "A single search term that is more relevant to the user's query. "
            "Include only relevant information, it does not need to be a full sentence or question "
        )
    )
```

修改 `query_transformation` 函数：

```python
def query_transformation(query: str) -> list[str]:
    lm = dspy.LM(subtask_model_name)
    answer = dspy.Predict(QueryRewriter)
    pred = answer(input_query=query, lm=lm)
    return [pred.rewritten_query]
```

## Query 分解

```python
class QueryRewriter(dspy.Signature):
    """
    Rewrite the user's query into a more relevant search terms that are more relevant search term for searching a database.
    """
    input_query: str = dspy.InputField(description="The original user query")
    rewritten_queries: list[str] = dspy.OutputField(
        description=(
            "A list of search terms that are more relevant to the user's query. "
            "Each entry should include only relevant information, it does not need to be a full sentence or question "
            "Split independent searches into different entries "
            "Each entry should be relevant independently that capture a different required search aspect "
            "Do not repeat similar search terms, each one should have a unique meaning "
            "Be sparse, do not duplicate search terms "
        )
    )

def query_transformation(query: str) -> list[str]:
    lm = dspy.LM(subtask_model_name)
    answer = dspy.Predict(QueryRewriter)
    pred = answer(input_query=query, lm=lm)
    return pred.rewritten_queries
```

## 由 LLM 生成的过滤器

过滤器既可以由用户指定（例如针对特定用例），也可以让 LLM 自动生成。编写过滤器需要掌握集合的 Schema，可通过进阶方法获取，或采用下面的简易版本。

简易版本：

1. 首先用结构化响应来格式化过滤器

```python
from pydantic import BaseModel, Field
from typing import Literal, Any

class SearchFilter(BaseModel):
    field: str = Field(description="The field to be filtered on.")
    operator: Literal["=", "!=", ">", "<"] = Field(description="The operator to be used in conjunction with the value. These are strict operators.")
    value: Any = Field(description="The value to be used in conjunction with the operator.")

class Search(BaseModel):
    filters: list[SearchFilter] = Field(description="The filters to be used in the vector database. This is an AND operation.")

class SearchCreation(dspy.Signature):
    """
    Create filters and search parameters for a search query in a database.
    """
    query: str = dspy.InputField()
    schema: list[dict] = dspy.InputField(desc="Schema of the collection to be searched.")
    data_sample: list[dict] = dspy.InputField(desc="A sample of the data in the collection to be searched.")
    search: Search = dspy.OutputField(
        desc=(
            "Your filters and search parameters, this should be a valid JSON object. "
            "This should be constructed so that it matches the goal of the user prompt."
        )
    )
```
此方案要求在 LLM 调用 `SearchCreation` 时提供 `schema` 与 `data_sample` 作为输入字段。

2. 辅助函数：将结构化响应转换为 Weaviate 过滤器

```python
def _format_filters(search_filters: list[SearchFilter]):
    filters = []
    for search_filter in search_filters:
        base_filter = Filter.by_property(search_filter.field)
        if search_filter.operator == "=":
            filter = base_filter.equal(search_filter.value)
        elif search_filter.operator == "!=":
            filter = base_filter.not_equal(search_filter.value)
        elif search_filter.operator == ">":
            filter = base_filter.greater_than(search_filter.value)
        elif search_filter.operator == "<":
            filter = base_filter.less_than(search_filter.value)
        filters.append(filter)
    return Filter.all_of(filters) if filters else None
```

3. 组合使用

```python
def create_filters(query: str):
    
    # import client here

    collection = client.collections.use("<collection_name>")

    # Get collection schema (for field names etc.). can replace this with more advanced configuration (like aggregating for unique groups)
    config = collection.config.get()
    schema = [{"name": p.name, "type": p.data_type[:]} for p in config.properties]

    # Get a sample of the data in the collection to be searched
    data_sample = collection.query.fetch_objects(limit=5)

    # Create search parameters
    search_parameters = dspy.ChainOfThought(SearchCreation)
    search_parameters_output = search_parameters(query=query, schema=schema, data_sample=data_sample, lm=dspy.LM(subtask_model_name))
    
    return _format_filters(search_parameters_output.search.filters)
```

这些过滤器可以传入 `collection.query.near_text`（或等价的检索函数）。

## 重排序

除非用户明确要求，否则不要改动其集合。重排序要求在集合上配置重排序器，例如：

```python
collection = client.collections.use("<collection_name>")
collection.config.update(
    reranker_config=Reconfigure.Reranker.cohere()  
)
```
（这需要提供 Cohere API 密钥。）

修改 `retrieve` 函数：

```python
from weaviate.classes.query import Rerank

def retrieve(query: str, limit: int | None = None, filters = []) -> list[dict]:

    # ...existing code
    
    response = collection.query.hybrid(
        query=query,
        limit=limit,
        rerank=Rerank(
            prop="content", # what field to re-rank on
            query=query # what the search term for the re-ranker should be (same as original in this case)
        ),
        filters=filters if filters else None
    )
    
    # ...existing code
```

## 提示工程

该步骤取决于所使用的 LLM 框架。可以手动要求 LLM 在给出最终答案前先进行推理，例如在结构化响应中加入一个 reasoning 子字段；也可以在 DSPy 中指定使用 chain-of-thought。

```python
class Generator(dspy.Signature):
    """
    Answer the question based on the context.
    Do not include any information from external sources, only use the information provided in the context.
    If you cannot answer the question based on the information provided, say "I don't know".
    """
    context: str | list[dict] =  dspy.InputField(desc="The context to answer the question.")
    query: str = dspy.InputField(desc="The question to answer.")
    answer: str = dspy.OutputField(desc="The single answer to the question with no additional communication")
```

修改 `generate` 函数：

```python
def generate(query: str, context: list[dict]) -> str:
    lm = dspy.LM(generation_model_name)
    answer = dspy.Predict(Generator)
    pred = answer(context=context, query=query, lm=lm)
    return pred.answer
```

如有需要，可考虑其他提示工程技术，例如 ReAct（一般属于过度设计）、few-shot 学习（需要更精细的设定）等。

## Query Agent

直接跳过本指南，使用 Weaviate Query Agent。

```python
from weaviate.agents.query import QueryAgent

# import client here

qa = QueryAgent(
    client=client, collections=["Example_Communications_Raw"]
)
response = qa.search("<user query here>") # just search with no text response
response = qa.ask("<user query here>") # search with text response accessible via response.final_answer
```

## 可定制点

**LLM 框架**

本指南使用 DSPy。请遵循[此处](./basic_rag.md)中的指引，但你很可能需要支持结构化响应的 LLM 框架。

## 故障排查

- Weaviate 启动主机错误：确认 `WEAVIATE_URL` 是完整的 `https://...` URL。
- 其他问题：请查阅官方库/包文档，并充分利用网络搜索进行排查。

## 完成标准

- 编写测试脚本，使用测试数据分别验证每个函数是否独立工作。验证完成后清理临时测试，或使用 pytest 构建正式测试套件（需安装）。
- 用户已完成应用规格的确认。