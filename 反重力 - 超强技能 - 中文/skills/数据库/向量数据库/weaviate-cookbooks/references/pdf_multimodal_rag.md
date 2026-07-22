# 多向量 RAG：基于 Weaviate 构建多模态文档检索系统

## 概述

本 cookbook 提供使用 Weaviate Embeddings 多模态模型进行嵌入、Ollama 运行视觉语言模型（VLM）进行生成的 PDF 文档多模态 RAG（Retrieval-Augmented Generation）系统实施指南。

Weaviate Embeddings 在服务端完成全部嵌入生成 —— 无需本地 GPU 或下载模型。只需将文档图像以 base64 Blob 形式上传，Weaviate 即可自动生成多向量嵌入。

### 架构

一个多模态 RAG 系统包含两条主流程：

**数据写入流程：**
- 将文档（PDF、图像）转换为页面图像
- 将图像以 base64 Blob 形式上传到 Weaviate
- Weaviate Embeddings 使用 `ModernVBERT/colmodernvbert` 在服务端生成多向量嵌入
- 嵌入自动存入向量索引

**查询流程：**
- 将文本查询发送到 Weaviate，由其在服务端完成嵌入
- 使用相似度检索（MaxSim）拉取相关文档
- 将检索到的文档图像连同查询一起送入运行在 Ollama 上的视觉语言模型（VLM）
- VLM 基于视觉与文本上下文生成自然语言回复



**环境要求：**
- Weaviate Cloud 实例（Weaviate Embeddings 仅支持云端）
- Python 3.11 或更高版本
- `uv` 包管理器（[安装指南](https://docs.astral.sh/uv/getting-started/installation/)）
- 本地安装 [Ollama](https://ollama.com/) 用于 VLM 生成

## 操作流程

### 第 1 步：初始化项目并安装依赖

#### 项目引导

使用 `uv` 初始化新项目：

```bash
uv init multimodal-rag
cd multimodal-rag
uv venv
```

**如需安装 uv：**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh -o /tmp/uv-install.sh
less /tmp/uv-install.sh
sh /tmp/uv-install.sh

# Or with pip
pip install uv

# Or with Homebrew
brew install uv
```

#### 安装核心依赖

使用 `uv` 安装所需库：

```bash
uv add weaviate-client
```

**包说明：**
- `weaviate-client`：Weaviate 向量数据库（v4.x）的 Python 客户端 —— 全部嵌入生成由 Weaviate Embeddings 负责

#### 其他依赖（按需安装）

```bash
# For loading Hugging Face datasets
uv add datasets

# For PDF processing (pdf2image requires poppler to be installed!)
uv add pdf2image pillow

# For VLM generation via Ollama
uv add ollama
```

### 第 2 步：准备文档数据集

#### 方案 A：加载已有数据集
若使用已有数据集：
- 使用 Hugging Face `datasets` 库
- 确保数据集中含文档图像或可转换为图像
- 校验图像格式兼容（JPEG、PNG）

#### 方案 B：处理自有文档
对于自定义文档集合：
1. 将文档转换为图像（若不是图像）
   - PDF：使用 `pdf2image` 或类似库
   - Office 文档：先转换为 PDF，再转换为图像
2. 附带元数据（文档 ID、页码、标题等）
3. 以适合批处理的格式存储

**推荐结构：**
```python
{
    "document_id": str,
    "page_number": int,
    "image": PIL.Image,
    "metadata": dict  # title, author, date, etc.
}
```

### 第 3 步：配置 Weaviate 集合

#### 连接 Weaviate

```python
import os
import weaviate
from weaviate.classes.init import Auth

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)
```

#### 创建集合 Schema

定义一个使用 `multi2vec_weaviate` 向量器的集合，以自动生成多模态嵌入：

```python
from weaviate.classes.config import Configure, Property, DataType

collection_name = "PDFDocuments"  # Use a descriptive name for your use case

collection = client.collections.create(
    name=collection_name,
    properties=[
        Property(name="doc_page", data_type=DataType.BLOB),
        Property(name="page_id", data_type=DataType.INT),
        Property(name="document_id", data_type=DataType.TEXT),
        Property(name="page_number", data_type=DataType.INT),
        Property(name="title", data_type=DataType.TEXT),
        # Add other metadata properties as needed
    ],
    vector_config=[
        Configure.MultiVectors.multi2vec_weaviate(
            name="doc_vector"
            image_field="doc_page",
            model="ModernVBERT/colmodernvbert",
            encoding=Configure.VectorIndex.MultiVector.Encoding.muvera(
                ksim=4,
                dprojections=16,
                repetitions=20,
            ),
        )
    ],
)
```

**关键配置项：**
- **`doc_page`**：保存 base64 编码页面图像的 BLOB 属性 —— 向量器读取该字段
- **`image_field`**：必须与 BLOB 属性名一致（`"doc_page"`）
- **`model`**：`ModernVBERT/colmodernvbert` —— 2.5 亿参数的 late-interaction 视觉-语言编码器，针对视觉文档检索做了微调
- **MUVERA 编码**：将多向量压缩为高效的单向量，同时保持检索质量
  - `ksim`：纳入考虑的相似向量数量（默认：4）
  - `dprojections`：投影维度数（默认：16）
  - `repetitions`：编码重复次数（默认：20）
- **属性**：添加你希望用于过滤或展示的全部元数据

**不使用 MUVERA 编码**（占用更多内存，但保留完整的多向量表示）：
```python
vector_config=[
    Configure.MultiVectors.multi2vec_weaviate(
        name="doc_vector",
        image_field="doc_page",
        model="ModernVBERT/colmodernvbert",
    )
],
```

### 第 4 步：索引文档

#### 将图像转换为 Base64

```python
import base64
from io import BytesIO

def image_to_base64(image):
    """Convert a PIL Image to a base64-encoded string.

    Args:
        image: PIL.Image object

    Returns:
        Base64-encoded string of the JPEG image
    """
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
```

#### 批量导入

Weaviate Embeddings 在导入过程中在服务端生成嵌入 —— 无需本地模型：

```python
collection = client.collections.get(collection_name)

with collection.batch.dynamic() as batch:
    for idx, document in enumerate(your_document_dataset):
        # Convert image to base64
        img_base64 = image_to_base64(document["image"])

        # Add object to batch — Weaviate generates embeddings automatically
        batch.add_object(
            properties={
                "doc_page": img_base64,
                "page_id": document["page_id"],
                "document_id": document["document_id"],
                "page_number": document["page_number"],
                "title": document.get("title", ""),
                # Add other properties from your dataset
            },
        )

        # Progress tracking
        if idx % 25 == 0:
            print(f"Indexed {idx+1}/{len(your_document_dataset)} documents")

# Clean up dataset if memory is limited
del your_document_dataset

print(f"Total documents indexed: {len(collection)}")
```

**性能提示：**
- **批大小**：`dynamic()` 模式下 Weaviate 自动管理批大小
- **无需本地 GPU**：Weaviate Embeddings 在服务端运行
- **图像格式**：推荐 JPEG 以获得更小的载荷
- **大型数据集**：分块处理，及时删除中间变量以释放内存

### 第 5 步：实现检索

#### 基础查询函数

Weaviate 自动完成查询嵌入 —— 只需传入文本：

```python
from weaviate.classes.query import MetadataQuery

def search_documents(query_text, limit=3):
    """Search for documents using Weaviate Embeddings multimodal model.

    Args:
        query_text: Natural language query string
        limit: Number of results to return (default: 3)

    Returns:
        List of dicts with document properties, similarity scores, and base64 images
    """
    collection = client.collections.get(collection_name)

    # Search — Weaviate embeds the query server-side
    # Include doc_page in return_properties to get the base64-encoded image blob
    response = collection.query.near_text(
        query=query_text,
        limit=limit,
        return_properties=["page_id", "document_id", "page_number", "title", "doc_page"],
        return_metadata=MetadataQuery(distance=True),
    )

    # Process and format results
    results = []
    for i, obj in enumerate(response.objects):
        props = obj.properties
        results.append({
            "rank": i + 1,
            "page_id": props["page_id"],
            "document_id": props["document_id"],
            "page_number": props["page_number"],
            "title": props["title"],
            "distance": obj.metadata.distance,
            "image_base64": props["doc_page"],  # Already base64-encoded
        })

    return results

# Example usage
query = "How does DeepSeek-V2 compare against the LLaMA family of LLMs?"
results = search_documents(query, limit=3)

for result in results:
    print(f"{result['rank']}) Distance: {result['distance']:.4f}, "
          f"Title: \"{result['title']}\", Page: {result['page_number']}")
```

**查询参数：**
- **`limit`**：返回结果数（推荐 1-10，需考虑 VLM 的内存限制）
- **`return_metadata`**：设置 `distance=True` 以返回相似度评分
- **过滤器**：使用 `filters=` 进行元数据过滤（见下文）

**在结果中访问图像字段：**
作为 `multi2vec_weaviate` 向量器 `image_field` 属性的 BLOB（例如 `doc_page`）默认不会返回。必须通过 `return_properties` 显式指定（见上文 `search_documents()` 示例）。返回的 Blob 是 base64 编码的。Ollama Python SDK 的 `images` 键接受原始 `bytes` 或路径类字符串（不接受 base64 字符串），因此在传入 Ollama 之前需用 `base64.b64decode()` 解码（见下文 `OllamaVLM.generate_answer()` 示例）。

#### 元数据过滤

添加过滤器以按文档属性缩小检索范围：

```python
import weaviate.classes.config as wc

# Example: Filter by document ID
response = collection.query.near_text(
    query="query text",
    limit=5,
    filters=wc.Filter.by_property("document_id").equal("paper_123"),
)

# Example: Filter by page range
response = collection.query.near_text(
    query="query text",
    limit=5,
    filters=wc.Filter.by_property("page_number").less_than(10),
)

# Example: Combine multiple filters
from weaviate.classes.query import Filter

response = collection.query.near_text(
    query="query text",
    limit=5,
    filters=(
        Filter.by_property("document_id").equal("paper_123") &
        Filter.by_property("page_number").less_than(10)
    ),
)
```

#### 混合检索

将向量检索与 BM25 关键词检索结合：

```python
# Hybrid search: vector + keyword (Weaviate handles embedding)
response = collection.query.hybrid(
    query="query text",
    alpha=0.7,  # 0.0=keyword only, 0.5=balanced, 1.0=vector only
    limit=5,
)
```

**何时使用混合检索：**
- 需要精确关键词匹配（例如搜索特定术语、ID）
- 希望结合语义理解与精确文本匹配（BM25）
- 根据对语义与关键词匹配的不同侧重调整 `alpha`

### 第 6 步：扩展为完整的 VLM RAG

#### 关于 Ollama

[Ollama](https://ollama.com/) 让你通过一条命令即可在本地运行视觉语言模型，无需手动下载模型、配置 GPU 或管理依赖。

**Ollama 上推荐的 VLM 模型：**
- `qwen3-vl:4b`：约 4 GB，适合硬件受限的环境
- `qwen3-vl:8b`：约 8 GB，质量更佳
- `qwen3-vl:32b`：约 32 GB，最高质量
- `gemma3`：Google 多模态模型，提供 4B/12B/27B 三种规格
- `llava`：LLaVA 模型，轻量且快速

#### 安装 Ollama 并拉取模型

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh -o /tmp/ollama-install.sh
less /tmp/ollama-install.sh
sh /tmp/ollama-install.sh

# Or on macOS with Homebrew
brew install ollama

# Pull a vision language model
ollama pull qwen3-vl:4b
```

校验模型是否可用：
```bash
ollama list
```

#### 实现 Ollama VLM 封装

```python
import base64
import ollama

class OllamaVLM:
    def __init__(self, model_name="qwen3-vl:4b"):
        """Initialize with an Ollama vision model name.

        Args:
            model_name: Ollama model tag (must support vision)
        """
        self.model_name = model_name

    def generate_answer(self, query, images_base64, max_tokens=128):
        """Generate text response based on query and retrieved document images.

        Args:
            query: String text query
            images_base64: List of base64-encoded image strings (as returned by Weaviate)
            max_tokens: Maximum tokens to generate (default: 128)

        Returns:
            Generated text answer as string
        """
        # The Ollama SDK "images" key accepts bytes or path-like strings,
        # so decode the base64 strings from Weaviate into raw bytes
        images_bytes = [base64.b64decode(img) for img in images_base64]

        response = ollama.chat(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": query,
                "images": images_bytes,
            }],
            options={"num_predict": max_tokens},
        )

        return response["message"]["content"]

# Instantiate the VLM
vlm = OllamaVLM(model_name="qwen3-vl:4b")
```

#### 完整 RAG 流水线

```python
def multimodal_rag(query, num_documents=3, max_tokens=128):
    """Complete multimodal RAG pipeline using Weaviate Embeddings + Ollama VLM.

    Args:
        query: Natural language question
        num_documents: Number of documents to retrieve (1-3 recommended)
        max_tokens: Maximum tokens for VLM response

    Returns:
        Dict with query, answer, sources, and metadata
    """
    # Step 1: Retrieve relevant documents (Weaviate handles embedding)
    print(f"Searching for: {query}")
    retrieved_docs = search_documents(query, limit=num_documents)

    # Display retrieved sources
    print(f"\nRetrieved {len(retrieved_docs)} documents:")
    for doc in retrieved_docs:
        print(f"  - {doc['title']}, Page {doc['page_number']} "
              f"(Distance: {doc['distance']:.4f})")

    # Step 2: Extract base64 images from results
    context_images = [doc["image_base64"] for doc in retrieved_docs]

    # Step 3: Generate answer using Ollama VLM
    print(f"\nGenerating answer...")
    answer = vlm.generate_answer(query, context_images, max_tokens=max_tokens)

    # Step 4: Return structured response
    return {
        "query": query,
        "answer": answer,
        "sources": retrieved_docs,
        "num_sources": len(retrieved_docs)
    }

# Example usage
query = "How does DeepSeek-V2 compare against the LLaMA family of LLMs?"
result = multimodal_rag(query, num_documents=1, max_tokens=128)

print(f"\nQuery: {result['query']}")
print(f"Answer: {result['answer']}")
print(f"\nBased on {result['num_sources']} source(s)")
```

#### 引用来源

在生成的答案中附带来源标注：

```python
def generate_with_citations(query, retrieved_docs, max_tokens=256):
    """Generate answer with source citations.

    Args:
        query: User question
        retrieved_docs: List of documents from search_documents()
        max_tokens: Maximum response length

    Returns:
        Answer string with embedded citations
    """
    # Build source references
    sources_text = "\n".join([
        f"Source {i+1}: \"{doc['title']}\", Page {doc['page_number']}"
        for i, doc in enumerate(retrieved_docs)
    ])

    # Enhanced prompt with citation instructions
    enhanced_query = f"""{query}

Available sources:
{sources_text}

Instructions: Answer the question based on the provided document images.
Cite sources in your answer using [Source N] notation."""

    # Generate answer with citations
    answer = vlm.generate_answer(
        enhanced_query,
        [doc["image_base64"] for doc in retrieved_docs],
        max_tokens=max_tokens
    )

    return answer, retrieved_docs

# Example usage
query = "What is the architecture of GPT-4?"
answer, sources = generate_with_citations(query, search_documents(query, limit=3))
print(f"Answer: {answer}\n")
print("Sources:")
for src in sources:
    print(f"  - {src['title']}, Page {src['page_number']}")
```

## 故障排查

### 环境变量缺失
```
Error: WEAVIATE_URL environment variable is not set
```
**解决方案：** 设置 `WEAVIATE_URL` 和 `WEAVIATE_API_KEY` 环境变量。参见 `environment_requirements.md`。

### 连接错误
```
WeaviateConnectionError: Failed to connect to Weaviate
```
**解决方案：** 确认 `WEAVIATE_URL` 正确，且网络可达 Weaviate Cloud 实例。

### Ollama 连接错误
```
ConnectionError: Failed to connect to Ollama
```
**解决方案：** 确认 Ollama 已启动。使用以下命令启动：
```bash
ollama serve
```

### Ollama 模型未找到
```
ollama._types.ResponseError: model 'qwen3-vl:4b' not found
```
**解决方案：** 先拉取模型：
```bash
ollama pull qwen3-vl:4b
```

### VLM 生成过程中内存不足（OOM）
**症状：** 生成答案时出现 OOM 错误。

**解决方案：**
- 减少 `num_documents` —— 检索更少的文档（即使 1 个也能工作良好）
- 减少 `max_tokens` —— 更短的回复占用更少内存
- 使用更小的模型规格（如 `qwen3-vl:4b` 替代 `8b`）
- 使用基于 API 的 VLM（GPT-4V、Claude、Gemini）以完全规避本地资源需求

### BLOB 属性未随查询结果返回
**症状：** 查询结果中缺少 `doc_page` 字段。

**解决方案：** 在 `multi2vec_weaviate` 中作为 `image_field` 使用的 BLOB 属性默认不返回。需显式指定：
```python
response = collection.query.near_text(
    query=query_text,
    limit=limit,
    return_properties=["page_id", "document_id", "page_number", "title", "doc_page"],
)
```

### 未安装 Poppler（PDF 处理）
```
Exception: Unable to get page count. Is poppler installed and in PATH?
```
**解决方案：** 为 `pdf2image` 安装 poppler：
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

### TypeError: unexpected keyword argument 'image_fields'
```
TypeError: _MultiVectors.multi2vec_weaviate() got an unexpected keyword argument 'image_fields'
```
**原因：** 参数为单数而非复数。

**解决方案：** 使用 `image_field`（单数）而非 `image_fields`：
```python
Configure.MultiVectors.multi2vec_weaviate(
    name="doc_vector",
    image_field="doc_page",
    ...
)
```

## 完成标准

实现完成的标志：
- [ ] 项目已通过 `uv` 初始化并安装所有依赖
- [ ] 文档图像已转换并上传到使用 `multi2vec_weaviate` 向量器的 Weaviate 集合
- [ ] 集合使用 `ModernVBERT/colmodernvbert` 模型并配置了 MUVERA 编码
- [ ] `search_documents()` 能为文本查询返回带相似度评分的排序结果
- [ ] Ollama 与视觉语言模型可基于检索到的文档图像生成自然语言答案
- [ ] 完整的 `multimodal_rag()` 流水线可端到端地检索文档并生成答案

## 后续步骤

- **添加元数据过滤**：按文档 ID、页码范围或其他属性缩小检索范围
- **实现混合检索**：将向量相似度与 BM25 关键词匹配结合以提升精度
- **添加答案引用**：使用 `generate_with_citations()` 将答案归因到来源文档
- **扩大数据集规模**：通过批处理分块与内存管理处理更大的文档集合
- **切换为基于 API 的 VLM**（GPT、Claude、Gemini）或其他 Ollama 视觉模型（`gemma3`、`llava`）
- **评估检索质量**：使用已知相关文档测试查询，并调优 MUVERA 参数