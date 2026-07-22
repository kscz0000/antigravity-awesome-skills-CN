---
name: embedding-strategies
description: "向量搜索应用中选择和优化嵌入模型的指南。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 嵌入策略

向量搜索应用中选择和优化嵌入模型的指南。

## 不使用此技能的情况

- 任务与嵌入策略无关
- 你需要此范围之外的其他领域或工具

## 说明

- 明确目标、约束条件和所需输入。
- 应用相关的最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如果需要详细示例，请打开 `resources/implementation-playbook.md`。

## 使用此技能的情况

- 为 RAG 选择嵌入模型
- 优化分块策略
- 为特定领域微调嵌入
- 比较嵌入模型性能
- 降低嵌入维度
- 处理多语言内容

## 核心概念

### 1. 嵌入模型对比

| 模型 | 维度 | 最大 Token 数 | 最佳用途 |
|-------|------------|------------|----------|
| **text-embedding-3-large** | 3072 | 8191 | 高精度 |
| **text-embedding-3-small** | 1536 | 8191 | 性价比高 |
| **voyage-2** | 1024 | 4000 | 代码、法律 |
| **bge-large-en-v1.5** | 1024 | 512 | 开源 |
| **all-MiniLM-L6-v2** | 384 | 256 | 快速、轻量 |
| **multilingual-e5-large** | 1024 | 512 | 多语言 |

### 2. 嵌入流水线

```
文档 → 分块 → 预处理 → 嵌入模型 → 向量
                ↓
        [重叠, 大小]  [清洗, 归一化]  [API/本地]
```

## 模板

### 模板 1：OpenAI 嵌入

```python
from openai import OpenAI
from typing import List
import numpy as np

client = OpenAI()

def get_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: int = None
) -> List[List[float]]:
    """从 OpenAI 获取嵌入。"""
    # 处理大批量的分批
    batch_size = 100
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        kwargs = {"input": batch, "model": model}
        if dimensions:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)
        embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(embeddings)

    return all_embeddings


def get_embedding(text: str, **kwargs) -> List[float]:
    """获取单个嵌入。"""
    return get_embeddings([text], **kwargs)[0]


# 使用 OpenAI 进行维度缩减
def get_reduced_embedding(text: str, dimensions: int = 512) -> List[float]:
    """获取缩减维度的嵌入（Matryoshka）。"""
    return get_embedding(
        text,
        model="text-embedding-3-small",
        dimensions=dimensions
    )
```

### 模板 2：使用 Sentence Transformers 的本地嵌入

```python
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np

class LocalEmbedder:
    """使用 sentence-transformers 的本地嵌入。"""

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
        device: str = "cuda"
    ):
        self.model = SentenceTransformer(model_name, device=device)

    def embed(
        self,
        texts: List[str],
        normalize: bool = True,
        show_progress: bool = False
    ) -> np.ndarray:
        """嵌入文本，可选归一化。"""
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """使用 BGE 风格前缀嵌入查询。"""
        # BGE 模型受益于查询前缀
        if "bge" in self.model.get_sentence_embedding_dimension():
            query = f"Represent this sentence for searching relevant passages: {query}"
        return self.embed([query])[0]

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """嵌入文档用于索引。"""
        return self.embed(documents)


# 带指令的 E5 模型
class E5Embedder:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, query: str) -> np.ndarray:
        return self.model.encode(f"query: {query}")

    def embed_document(self, document: str) -> np.ndarray:
        return self.model.encode(f"passage: {document}")
```

### 模板 3：分块策略

```python
from typing import List, Tuple
import re

def chunk_by_tokens(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    tokenizer=None
) -> List[str]:
    """按 Token 数量分块文本。"""
    import tiktoken
    tokenizer = tokenizer or tiktoken.get_encoding("cl100k_base")

    tokens = tokenizer.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end - chunk_overlap

    return chunks


def chunk_by_sentences(
    text: str,
    max_chunk_size: int = 1000,
    min_chunk_size: int = 100
) -> List[str]:
    """按句子分块文本，遵守大小限制。"""
    import nltk
    sentences = nltk.sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)

        if current_size + sentence_size > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(sentence)
        current_size += sentence_size

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_by_semantic_sections(
    text: str,
    headers_pattern: str = r'^#{1,3}\s+.+$'
) -> List[Tuple[str, str]]:
    """按标题分块 Markdown，保留层级结构。"""
    lines = text.split('\n')
    chunks = []
    current_header = ""
    current_content = []

    for line in lines:
        if re.match(headers_pattern, line, re.MULTILINE):
            if current_content:
                chunks.append((current_header, '\n'.join(current_content)))
            current_header = line
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        chunks.append((current_header, '\n'.join(current_content)))

    return chunks


def recursive_character_splitter(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: List[str] = None
) -> List[str]:
    """LangChain 风格的递归分割器。"""
    separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(text: str, separators: List[str]) -> List[str]:
        if not text:
            return []

        separator = separators[0]
        remaining_separators = separators[1:]

        if separator == "":
            # 字符级分割
            return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]

        splits = text.split(separator)
        chunks = []
        current_chunk = []
        current_length = 0

        for split in splits:
            split_length = len(split) + len(separator)

            if current_length + split_length > chunk_size and current_chunk:
                chunk_text = separator.join(current_chunk)

                # 如果仍然太大，递归分割
                if len(chunk_text) > chunk_size and remaining_separators:
                    chunks.extend(split_text(chunk_text, remaining_separators))
                else:
                    chunks.append(chunk_text)

                # 带重叠开始新块
                overlap_splits = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length + len(s) <= chunk_overlap:
                        overlap_splits.insert(0, s)
                        overlap_length += len(s)
                    else:
                        break
                current_chunk = overlap_splits
                current_length = overlap_length

            current_chunk.append(split)
            current_length += split_length

        if current_chunk:
            chunks.append(separator.join(current_chunk))

        return chunks

    return split_text(text, separators)
```

### 模板 4：领域特定嵌入流水线

```python
class DomainEmbeddingPipeline:
    """领域特定嵌入的流水线。"""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        preprocessing_fn=None
    ):
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.preprocess = preprocessing_fn or self._default_preprocess

    def _default_preprocess(self, text: str) -> str:
        """默认预处理。"""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    async def process_documents(
        self,
        documents: List[dict],
        id_field: str = "id",
        content_field: str = "content",
        metadata_fields: List[str] = None
    ) -> List[dict]:
        """处理文档以存入向量存储。"""
        processed = []

        for doc in documents:
            content = doc[content_field]
            doc_id = doc[id_field]

            # 预处理
            cleaned = self.preprocess(content)

            # 分块
            chunks = chunk_by_tokens(
                cleaned,
                self.chunk_size,
                self.chunk_overlap
            )

            # 创建嵌入
            embeddings = get_embeddings(chunks, self.embedding_model)

            # 创建记录
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                record = {
                    "id": f"{doc_id}_chunk_{i}",
                    "document_id": doc_id,
                    "chunk_index": i,
                    "text": chunk,
                    "embedding": embedding
                }

                # 添加元数据
                if metadata_fields:
                    for field in metadata_fields:
                        if field in doc:
                            record[field] = doc[field]

                processed.append(record)

        return processed


# 代码专用流水线
class CodeEmbeddingPipeline:
    """代码嵌入的专用流水线。"""

    def __init__(self, model: str = "voyage-code-2"):
        self.model = model

    def chunk_code(self, code: str, language: str) -> List[dict]:
        """按函数/类分块代码。"""
        import tree_sitter

        # 使用 tree-sitter 解析
        # 提取函数、类、方法
        # 返回带上下文的块
        pass

    def embed_with_context(self, chunk: str, context: str) -> List[float]:
        """嵌入带周围上下文的代码。"""
        combined = f"Context: {context}\n\nCode:\n{chunk}"
        return get_embedding(combined, model=self.model)
```

### 模板 5：嵌入质量评估

```python
import numpy as np
from typing import List, Tuple

def evaluate_retrieval_quality(
    queries: List[str],
    relevant_docs: List[List[str]],  # 每个查询的相关文档 ID 列表
    retrieved_docs: List[List[str]],  # 每个查询的检索文档 ID 列表
    k: int = 10
) -> dict:
    """评估嵌入的检索质量。"""

    def precision_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        retrieved_k = retrieved[:k]
        relevant_retrieved = len(set(retrieved_k) & relevant)
        return relevant_retrieved / k

    def recall_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        retrieved_k = retrieved[:k]
        relevant_retrieved = len(set(retrieved_k) & relevant)
        return relevant_retrieved / len(relevant) if relevant else 0

    def mrr(relevant: set, retrieved: List[str]) -> float:
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                return 1 / (i + 1)
        return 0

    def ndcg_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        dcg = sum(
            1 / np.log2(i + 2) if doc in relevant else 0
            for i, doc in enumerate(retrieved[:k])
        )
        ideal_dcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
        return dcg / ideal_dcg if ideal_dcg > 0 else 0

    metrics = {
        f"precision@{k}": [],
        f"recall@{k}": [],
        "mrr": [],
        f"ndcg@{k}": []
    }

    for relevant, retrieved in zip(relevant_docs, retrieved_docs):
        relevant_set = set(relevant)
        metrics[f"precision@{k}"].append(precision_at_k(relevant_set, retrieved, k))
        metrics[f"recall@{k}"].append(recall_at_k(relevant_set, retrieved, k))
        metrics["mrr"].append(mrr(relevant_set, retrieved))
        metrics[f"ndcg@{k}"].append(ndcg_at_k(relevant_set, retrieved, k))

    return {name: np.mean(values) for name, values in metrics.items()}


def compute_embedding_similarity(
    embeddings1: np.ndarray,
    embeddings2: np.ndarray,
    metric: str = "cosine"
) -> np.ndarray:
    """计算嵌入集之间的相似度矩阵。"""
    if metric == "cosine":
        # 归一化
        norm1 = embeddings1 / np.linalg.norm(embeddings1, axis=1, keepdims=True)
        norm2 = embeddings2 / np.linalg.norm(embeddings2, axis=1, keepdims=True)
        return norm1 @ norm2.T
    elif metric == "euclidean":
        from scipy.spatial.distance import cdist
        return -cdist(embeddings1, embeddings2, metric='euclidean')
    elif metric == "dot":
        return embeddings1 @ embeddings2.T
```

## 最佳实践

### 应该做的
- **模型匹配用例** - 代码 vs 散文 vs 多语言
- **深思熟虑地分块** - 保留语义边界
- **归一化嵌入** - 用于余弦相似度
- **批量请求** - 比逐个更高效
- **缓存嵌入** - 避免重复计算

### 不应该做的
- **不要忽略 Token 限制** - 截断会丢失信息
- **不要混用嵌入模型** - 空间不兼容
- **不要跳过预处理** - 垃圾进，垃圾出
- **不要过度分块** - 丢失上下文

## 资源

- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers](https://www.sbert.net/)
- [MTEB Benchmark](https://huggingface.co/spaces/mteb/leaderboard)

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
