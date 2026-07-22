# 基础 RAG Cookbook

使用 Weaviate 构建基础 RAG 功能。
如需进阶策略，请参阅[此处](./advanced_rag.md)。



如需参考的文档：
- Weaviate 中的搜索模式与基础：https://docs.weaviate.io/weaviate/search/basics
- Weaviate 中的过滤器：https://docs.weaviate.io/weaviate/search/filters
- 向量检索：https://docs.weaviate.io/weaviate/search/similarity
- 关键词检索：https://docs.weaviate.io/weaviate/search/bm25
- 混合检索：https://docs.weaviate.io/weaviate/search/hybrid
- 图像检索：https://docs.weaviate.io/weaviate/search/image

## 核心规则

- 使用 `venv` 创建虚拟环境。
- 使用 `uv` 进行 Python 项目与依赖管理。
- 不要手动编写 `pyproject.toml` 或 `uv.lock`；由 `uv` 生成/更新。
- 使用的安装命令为：`uv add weaviate-client python-dotenv dspy`
- 依据用户规格定制本 cookbook；未给出时主动向用户询问细节。

假设用户已具备可用数据，除非用户要求，否则不要生成测试数据。

## 环境变量规则

必填：
- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`

外部服务商密钥：
- 仅填写目标 Weaviate 集合配置实际使用的密钥。


## Weaviate 客户端

```python
import os
from weaviate import connect_to_weaviate_cloud

client = connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL", ""),
    auth_credentials=os.getenv("WEAVIATE_API_KEY", ""),
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    },
)
```

若用户的集合需要向量器服务商的密钥，请设置 `environment_requirements.md` 中列出的对应密钥。

客户端使用完毕后必须关闭。请用 `try/finally` 包裹，并在其中调用 `client.close()`（如需重连可调用 `client.connect()`）。


## 多租户

多租户信息可通过以下方式检查：

```python
config = await collection.config.get()
config.multi_tenancy_config.enabled # bool
```

例如：

```python

base_collection = client.collections.use(collection_name)

config = collection.config.get()
if config.multi_tenancy_config.enabled:
    collection = base_collection.with_tenant("<tenant_name>")
else:
    collection = base_collection
```

可通过以下方式获取所有租户名：

```python
all_tenants = list(collection.tenants.get().keys())
```

## 基础检索

通过以下方式使用集合：

```python
collection = client.collections.use("<collection_name>")
```

Weaviate 支持向量、关键词或混合检索。

```python
collection.query.near_text # semantic (text)
collection.query.bm25 # keyword
collection.query.hybrid # blend of keyword and semantic
```

也支持图像检索：

```python
collection.query.near_image(
    near_image = ... # base 64 representation of image or Path object to image
)
```

## 核心代码块

RAG 应当具备 4 项核心功能：

1. 检索前处理
2. 检索
3. 检索后处理
4. 生成

这些功能都应拆分为独立函数，再合并到一个函数中，便于后续修改或用户自行调整，同时保持代码清晰可读。

## 检索前处理

将用户问题转换为向量数据库风格的查询（一个或一组）。基础 RAG 不提供额外的查询转换。

```python
def query_transformation(query: str) -> list[str]:
    return [query]
```

## 检索

```python
def retrieve(
    query: str, 
    limit: int = 10,  # optional
    filters = [] # optional
    # additional arguments if required can go here and passed down to the search strategy
) -> list[dict]:
    
    # import client logic here

    collection = client.collections.use("<collection_name>")

    response = collection.query.near_text( # or hybrid, bm25, near_image
        query=query,
        limit=limit,
        filters=filters if filters else None
    )
    
    return [
        {
            **obj.properties,
            "uuid": obj.uuid
        } 
        for obj in response.objects
    ]
```

## 检索后处理

修改 `retrieve` 的输出。基础 RAG 不做额外的后处理。但可以考虑加入去重检查、属性裁剪格式化等逻辑。

```python
def process_retrieval_results(objects: list[dict]) -> list[dict]:
    return objects
```


## 生成

该步骤依赖你所使用的 LLM 框架，[详见下文](#user-specific-customisations)。以 DSPy 为例：

```python
import dspy
def generate(query: str, context: list[dict]) -> str:
    lm = dspy.LM("<model_name>") # e.g. gpt-5.2, gpt-5-mini, claude-sonnet-4-5, etc.
    answer = dspy.Predict("context, query -> answer") # inputs: context, query. outputs: answer
    pred = answer(context=context, query=query, lm=lm)
    return pred.answer # answer is then an attribute of pred
```

## 用户特定定制

若未明确说明，请在实施对应策略前就以下要点向用户确认：

**LLM 框架**

可使用 DSPy（兼容所有 LiteLLM 服务商）或 LiteLLM 本身。

- DSPy：https://dspy.ai/learn/programming/language_models/
- LiteLLM：https://docs.litellm.ai/docs/

或者，用户也可以使用单一模型服务商。用户将使用哪家服务商？

- OpenAI（https://platform.openai.com/docs/libraries）
- Anthropic（https://platform.claude.com/docs/）
- Google GenAI（https://ai.google.dev/gemini-api/docs/libraries）
- 其他（如本地托管模型），请自行合理判断

这些可能需要额外的安装步骤。

**集合**

集合是否已存在？名称是什么？用户希望查询单个集合还是多个集合？是否需要可配置？

数据是什么格式？图像、文本还是其他？集合配置的是哪种向量器？需要哪些 API 密钥？

**检索策略**

用户希望使用语义检索、关键词检索还是混合检索？

混合检索有一个 `alpha` 参数，用于控制关键词与语义权重之间的权衡。`alpha=1` 表示纯语义检索，`alpha=0` 表示纯关键词检索。


## 故障排查

- Weaviate 启动主机错误：确认 `WEAVIATE_URL` 是完整的 `https://...` URL。
- 其他问题：请查阅官方库/包文档，并充分利用网络搜索进行排查。

## 完成标准

- 编写测试脚本，使用测试数据分别验证每个函数是否独立工作。验证完成后清理临时测试，或使用 pytest 构建正式测试套件（需安装）。
- 用户已完成应用规格的确认。