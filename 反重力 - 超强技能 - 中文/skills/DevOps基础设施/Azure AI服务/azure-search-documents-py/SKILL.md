---
name: azure-search-documents-py
description: Azure AI Search Python SDK，用于向量搜索、混合搜索、语义排序、索引和技能集。当用户要求'Azure搜索''向量搜索''混合搜索''语义排序''Azure AI Search''索引管理'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI Search SDK for Python

全文搜索、向量搜索和混合搜索，具备 AI 增强能力。

## 安装

```bash
pip install azure-search-documents
```

## 环境变量

```bash
AZURE_SEARCH_ENDPOINT=https://<service-name>.search.windows.net
AZURE_SEARCH_API_KEY=<your-api-key>
AZURE_SEARCH_INDEX_NAME=<your-index-name>
```

## 身份验证

### API Key

```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"])
)
```

### Entra ID（推荐）

```python
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
    credential=DefaultAzureCredential()
)
```

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `SearchClient` | 搜索和文档操作 |
| `SearchIndexClient` | 索引管理、同义词映射 |
| `SearchIndexerClient` | 索引器、数据源、技能集 |

## 创建带向量字段的索引

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SearchableField,
    SimpleField
)

index_client = SearchIndexClient(endpoint, AzureKeyCredential(key))

fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="title", type=SearchFieldDataType.String),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="my-vector-profile"
    )
]

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(name="my-hnsw")
    ],
    profiles=[
        VectorSearchProfile(
            name="my-vector-profile",
            algorithm_configuration_name="my-hnsw"
        )
    ]
)

index = SearchIndex(
    name="my-index",
    fields=fields,
    vector_search=vector_search
)

index_client.create_or_update_index(index)
```

## 上传文档

```python
from azure.search.documents import SearchClient

client = SearchClient(endpoint, "my-index", AzureKeyCredential(key))

documents = [
    {
        "id": "1",
        "title": "Azure AI Search",
        "content": "Full-text and vector search service",
        "content_vector": [0.1, 0.2, ...]  # 1536 dimensions
    }
]

result = client.upload_documents(documents)
print(f"Uploaded {len(result)} documents")
```

## 关键词搜索

```python
results = client.search(
    search_text="azure search",
    select=["id", "title", "content"],
    top=10
)

for result in results:
    print(f"{result['title']}: {result['@search.score']}")
```

## 向量搜索

```python
from azure.search.documents.models import VectorizedQuery

# Your query embedding (1536 dimensions)
query_vector = get_embedding("semantic search capabilities")

vector_query = VectorizedQuery(
    vector=query_vector,
    k_nearest_neighbors=10,
    fields="content_vector"
)

results = client.search(
    vector_queries=[vector_query],
    select=["id", "title", "content"]
)

for result in results:
    print(f"{result['title']}: {result['@search.score']}")
```

## 混合搜索（向量 + 关键词）

```python
from azure.search.documents.models import VectorizedQuery

vector_query = VectorizedQuery(
    vector=query_vector,
    k_nearest_neighbors=10,
    fields="content_vector"
)

results = client.search(
    search_text="azure search",
    vector_queries=[vector_query],
    select=["id", "title", "content"],
    top=10
)
```

## 语义排序

```python
from azure.search.documents.models import QueryType

results = client.search(
    search_text="what is azure search",
    query_type=QueryType.SEMANTIC,
    semantic_configuration_name="my-semantic-config",
    select=["id", "title", "content"],
    top=10
)

for result in results:
    print(f"{result['title']}")
    if result.get("@search.captions"):
        print(f"  Caption: {result['@search.captions'][0].text}")
```

## 筛选器

```python
results = client.search(
    search_text="*",
    filter="category eq 'Technology' and rating gt 4",
    order_by=["rating desc"],
    select=["id", "title", "category", "rating"]
)
```

## 分面导航

```python
results = client.search(
    search_text="*",
    facets=["category,count:10", "rating"],
    top=0  # Only get facets, no documents
)

for facet_name, facet_values in results.get_facets().items():
    print(f"{facet_name}:")
    for facet in facet_values:
        print(f"  {facet['value']}: {facet['count']}")
```

## 自动补全与建议

```python
# Autocomplete
results = client.autocomplete(
    search_text="sea",
    suggester_name="my-suggester",
    mode="twoTerms"
)

# Suggest
results = client.suggest(
    search_text="sea",
    suggester_name="my-suggester",
    select=["title"]
)
```

## 索引器与技能集

```python
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexer,
    SearchIndexerDataSourceConnection,
    SearchIndexerSkillset,
    EntityRecognitionSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry
)

indexer_client = SearchIndexerClient(endpoint, AzureKeyCredential(key))

# Create data source
data_source = SearchIndexerDataSourceConnection(
    name="my-datasource",
    type="azureblob",
    connection_string=connection_string,
    container={"name": "documents"}
)
indexer_client.create_or_update_data_source_connection(data_source)

# Create skillset
skillset = SearchIndexerSkillset(
    name="my-skillset",
    skills=[
        EntityRecognitionSkill(
            inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
            outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")]
        )
    ]
)
indexer_client.create_or_update_skillset(skillset)

# Create indexer
indexer = SearchIndexer(
    name="my-indexer",
    data_source_name="my-datasource",
    target_index_name="my-index",
    skillset_name="my-skillset"
)
indexer_client.create_or_update_indexer(indexer)
```

## 最佳实践

1. **使用混合搜索**以获得最佳相关性，结合向量和关键词
2. **启用语义排序**用于自然语言查询
3. **批量索引**每次 100-1000 个文档以提高效率
4. **使用筛选器**在排序前缩小结果范围
5. **配置向量维度**以匹配你的 embedding 模型
6. **使用 HNSW 算法**用于大规模向量搜索
7. **在创建索引时创建建议器**（之后无法添加）

## 参考文件

| 文件 | 内容 |
|------|------|
| references/vector-search.md | HNSW 配置、集成向量化、多向量查询 |
| references/semantic-ranking.md | 语义配置、标题、答案、混合模式 |
| scripts/setup_vector_index.py | 创建向量搜索索引的 CLI 脚本 |


---

## 更多 Azure AI Search 模式

# Azure AI Search Python SDK

使用 `azure-search-documents` 编写简洁、惯用的 Python 代码。

## 安装

```bash
pip install azure-search-documents azure-identity
```

## 环境变量

```bash
AZURE_SEARCH_ENDPOINT=https://<search-service>.search.windows.net
AZURE_SEARCH_INDEX_NAME=<index-name>
# For API key auth (not recommended for production)
AZURE_SEARCH_API_KEY=<api-key>
```

## 身份验证

**DefaultAzureCredential（首选）**：
```python
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

credential = DefaultAzureCredential()
client = SearchClient(endpoint, index_name, credential)
```

**API Key**：
```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

client = SearchClient(endpoint, index_name, AzureKeyCredential(api_key))
```

## 客户端选择

| 客户端 | 用途 |
|--------|------|
| `SearchClient` | 查询索引、上传/更新/删除文档 |
| `SearchIndexClient` | 创建/管理索引、知识源、知识库 |
| `SearchIndexerClient` | 管理索引器、技能集、数据源 |
| `KnowledgeBaseRetrievalClient` | 带 LLM 问答的智能体检索 |

## 索引创建模式

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, VectorSearch, VectorSearchProfile,
    HnswAlgorithmConfiguration, AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters, SemanticSearch,
    SemanticConfiguration, SemanticPrioritizedFields, SemanticField
)

index = SearchIndex(
    name=index_name,
    fields=[
        SearchField(name="id", type="Edm.String", key=True),
        SearchField(name="content", type="Edm.String", searchable=True),
        SearchField(name="embedding", type="Collection(Edm.Single)",
                   vector_search_dimensions=3072,
                   vector_search_profile_name="vector-profile"),
    ],
    vector_search=VectorSearch(
        profiles=[VectorSearchProfile(
            name="vector-profile",
            algorithm_configuration_name="hnsw-algo",
            vectorizer_name="openai-vectorizer"
        )],
        algorithms=[HnswAlgorithmConfiguration(name="hnsw-algo")],
        vectorizers=[AzureOpenAIVectorizer(
            vectorizer_name="openai-vectorizer",
            parameters=AzureOpenAIVectorizerParameters(
                resource_url=aoai_endpoint,
                deployment_name=embedding_deployment,
                model_name=embedding_model
            )
        )]
    ),
    semantic_search=SemanticSearch(
        default_configuration_name="semantic-config",
        configurations=[SemanticConfiguration(
            name="semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                content_fields=[SemanticField(field_name="content")]
            )
        )]
    )
)

index_client = SearchIndexClient(endpoint, credential)
index_client.create_or_update_index(index)
```

## 文档操作

```python
from azure.search.documents import SearchIndexingBufferedSender

# Batch upload with automatic batching
with SearchIndexingBufferedSender(endpoint, index_name, credential) as sender:
    sender.upload_documents(documents)

# Direct operations via SearchClient
search_client = SearchClient(endpoint, index_name, credential)
search_client.upload_documents(documents)      # Add new
search_client.merge_documents(documents)       # Update existing
search_client.merge_or_upload_documents(documents)  # Upsert
search_client.delete_documents(documents)      # Remove
```

## 搜索模式

```python
# Basic search
results = search_client.search(search_text="query")

# Vector search
from azure.search.documents.models import VectorizedQuery

results = search_client.search(
    search_text=None,
    vector_queries=[VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=5,
        fields="embedding"
    )]
)

# Hybrid search (vector + keyword)
results = search_client.search(
    search_text="query",
    vector_queries=[VectorizedQuery(vector=embedding, k_nearest_neighbors=5, fields="embedding")],
    query_type="semantic",
    semantic_configuration_name="semantic-config"
)

# With filters
results = search_client.search(
    search_text="query",
    filter="category eq 'technology'",
    select=["id", "title", "content"],
    top=10
)
```

## 智能体检索（知识库）

用于带答案合成的 LLM 问答，参见 references/agentic-retrieval.md。

核心概念：
- **Knowledge Source**：指向搜索索引
- **Knowledge Base**：包装知识源 + LLM，用于查询规划和合成
- **输出模式**：`EXTRACTIVE_DATA`（原始分块）或 `ANSWER_SYNTHESIS`（LLM 生成的答案）

## 异步模式

```python
from azure.search.documents.aio import SearchClient

async with SearchClient(endpoint, index_name, credential) as client:
    results = await client.search(search_text="query")
    async for result in results:
        print(result["title"])
```

## 最佳实践

1. **使用环境变量**存储端点、密钥和部署名称
2. **生产环境优先使用 `DefaultAzureCredential`** 而非 API Key
3. **使用 `SearchIndexingBufferedSender`** 进行批量上传（自动处理分批和重试）
4. **始终定义语义配置**用于智能体检索索引
5. **使用 `create_or_update_index`** 实现幂等的索引创建
6. **使用上下文管理器或显式 `close()`** 关闭客户端

## 字段类型参考

| EDM 类型 | Python | 说明 |
|----------|--------|------|
| `Edm.String` | str | 可搜索文本 |
| `Edm.Int32` | int | 整数 |
| `Edm.Int64` | int | 长整数 |
| `Edm.Double` | float | 浮点数 |
| `Edm.Boolean` | bool | 布尔值 |
| `Edm.DateTimeOffset` | datetime | ISO 8601 |
| `Collection(Edm.Single)` | List[float] | 向量嵌入 |
| `Collection(Edm.String)` | List[str] | 字符串数组 |

## 错误处理

```python
from azure.core.exceptions import (
    HttpResponseError,
    ResourceNotFoundError,
    ResourceExistsError
)

try:
    result = search_client.get_document(key="123")
except ResourceNotFoundError:
    print("Document not found")
except HttpResponseError as e:
    print(f"Search error: {e.message}")
```

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
