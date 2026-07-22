---
name: agent-memory-systems
description: "记忆是智能体的基石。没有记忆，每次交互都从零开始。本技能涵盖智能体记忆架构：短期记忆（上下文窗口）、长期记忆（向量存储）以及组织它们的认知架构。触发词：智能体记忆、agent memory、长期记忆、短期记忆、记忆系统、向量存储、记忆检索、episodic memory、semantic memory、LangMem、MemGPT、记忆架构"
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 智能体记忆系统

记忆是智能体的基石。没有记忆，每次交互都从零开始。本技能涵盖智能体记忆架构：短期记忆（上下文窗口）、长期记忆（向量存储）以及组织它们的认知架构。

核心洞见：记忆不只是存储——更是检索。如果找不到正确的记忆，存储百万条事实毫无意义。分块（chunking）、嵌入（embedding）和检索策略决定了你的智能体是记住还是遗忘。

该领域术语碎片化且不一致。我们采用 CoALA 认知架构框架：语义记忆（事实）、情景记忆（经历）和程序记忆（方法知识）。

## 原则

- 记忆质量 = 检索质量，而非存储数量
- 为检索分块，而非为存储分块
- 上下文隔离是记忆的敌人
- 正确的信息类型使用正确的记忆类型
- 衰减旧记忆——不是所有内容都应永久保存
- 上线前测试检索准确率
- 后台记忆形成优于实时处理

## 能力

- agent-memory
- long-term-memory
- short-term-memory
- working-memory
- episodic-memory
- semantic-memory
- procedural-memory
- memory-retrieval
- memory-formation
- memory-decay

## 范围

- vector-database-operations → data-engineer
- rag-pipeline-architecture → llm-architect
- embedding-model-selection → ml-engineer
- knowledge-graph-design → knowledge-engineer

## 工具

### 记忆框架

- LangMem (LangChain) - 适用场景：带持久记忆的 LangGraph 智能体 备注：支持语义、情景、程序三种记忆类型
- MemGPT / Letta - 适用场景：虚拟上下文管理，操作系统式记忆 备注：分层记忆层级，自动分页
- Mem0 - 适用场景：用户记忆层，用于个性化 备注：专为用户偏好和历史设计

### 向量存储

- Pinecone - 适用场景：托管式，企业级规模（十亿级向量） 备注：最佳查询性能，最高成本
- Qdrant - 适用场景：复杂元数据过滤，开源 备注：Rust 实现，过滤能力出色
- Weaviate - 适用场景：混合搜索，知识图谱功能 备注：GraphQL 接口，适合关系数据
- ChromaDB - 适用场景：原型开发，中小型应用 备注：开发者友好，10万向量时 p50 约 20ms
- pgvector - 适用场景：已使用 PostgreSQL，简化部署 备注：适合百万级以下向量，工具链熟悉

### 嵌入模型

- OpenAI text-embedding-3-large - 适用场景：最佳质量，3072 维 备注：$0.13/百万 tokens
- OpenAI text-embedding-3-small - 适用场景：平衡选择，1536 维 备注：$0.02/百万 tokens，便宜 5 倍
- nomic-embed-text-v1.5 - 适用场景：开源，本地部署 备注：768 维，质量良好
- all-MiniLM-L6-v2 - 适用场景：轻量级，快速本地嵌入 备注：384 维，延迟最低

## 模式

### 记忆类型架构

为不同信息选择正确的记忆类型

**适用场景**：设计智能体记忆系统

# 记忆类型架构（CoALA 框架）：

"""
三种记忆类型，各司其职：

1. 语义记忆（Semantic Memory）：事实和知识
   - 你对世界的认知
   - 用户偏好、领域知识
   - 存储在配置文件（结构化）或集合（非结构化）中

2. 情景记忆（Episodic Memory）：经历和事件
   - 发生了什么（带时间戳的事件）
   - 过去对话、任务结果
   - 用于从经验中学习

3. 程序记忆（Procedural Memory）：如何做事
   - 规则、技能、工作流
   - 通常以少样本示例实现
   - "我之前是怎么解决这个问题的？"
"""

## LangMem 实现
"""
from langmem import MemoryStore
from langgraph.graph import StateGraph

# 初始化记忆存储
memory = MemoryStore(
    connection_string=os.environ["POSTGRES_URL"]
)

# 语义记忆：用户画像
await memory.semantic.upsert(
    namespace="user_profile",
    key=user_id,
    content={
        "name": "Alice",
        "preferences": ["dark mode", "concise responses"],
        "expertise_level": "developer",
    }
)

# 情景记忆：过往交互
await memory.episodic.add(
    namespace="conversations",
    content={
        "timestamp": datetime.now(),
        "summary": "Helped debug authentication issue",
        "outcome": "resolved",
        "key_insights": ["Token expiry was root cause"],
    },
    metadata={"user_id": user_id, "topic": "debugging"}
)

# 程序记忆：习得模式
await memory.procedural.add(
    namespace="skills",
    content={
        "task_type": "debug_auth",
        "steps": ["Check token expiry", "Verify refresh flow"],
        "example_interaction": few_shot_example,
    }
)
"""

## 运行时记忆检索
"""
async def prepare_context(user_id, query):
    # 获取用户画像（语义）
    profile = await memory.semantic.get(
        namespace="user_profile",
        key=user_id
    )

    # 查找相关过往经历（情景）
    similar_experiences = await memory.episodic.search(
        namespace="conversations",
        query=query,
        filter={"user_id": user_id},
        limit=3
    )

    # 查找相关技能（程序）
    relevant_skills = await memory.procedural.search(
        namespace="skills",
        query=query,
        limit=2
    )

    return {
        "profile": profile,
        "past_experiences": similar_experiences,
        "relevant_skills": relevant_skills,
    }
"""

### 向量存储选择模式

为你的用例选择正确的向量数据库

**适用场景**：搭建持久记忆存储

# 向量存储选择：

"""
决策矩阵：

|            | Pinecone | Qdrant | Weaviate | ChromaDB | pgvector |
|------------|----------|--------|----------|----------|----------|
| 规模       | 十亿级   | 1亿+   | 1亿+     | 百万级   | 百万级   |
| 托管       | 是       | 两者皆可| 两者皆可 | 自托管   | 自托管   |
| 过滤       | 基础     | 最佳   | 良好     | 基础     | SQL      |
| 混合搜索   | 否       | 是     | 最佳     | 否       | 是       |
| 成本       | 高       | 中     | 中       | 免费     | 免费     |
| 延迟       | 5ms      | 7ms    | 10ms     | 20ms     | 15ms     |
"""

## Pinecone（企业级规模）
"""
from pinecone import Pinecone

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("agent-memory")

# 带元数据插入
index.upsert(
    vectors=[
        {
            "id": f"memory-{uuid4()}",
            "values": embedding,
            "metadata": {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "type": "episodic",
                "content": memory_text,
            }
        }
    ],
    namespace=namespace
)

# 带过滤查询
results = index.query(
    vector=query_embedding,
    filter={"user_id": user_id, "type": "episodic"},
    top_k=5,
    include_metadata=True
)
"""

## Qdrant（复杂过滤）
"""
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition

client = QdrantClient(url="http://localhost:6333")

# Qdrant 复杂过滤
results = client.search(
    collection_name="agent_memory",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="user_id", match={"value": user_id}),
            FieldCondition(key="type", match={"value": "semantic"}),
        ],
        should=[
            FieldCondition(key="topic", match={"any": ["auth", "security"]}),
        ]
    ),
    limit=5
)
"""

## ChromaDB（原型开发）
"""
import chromadb

client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection("agent_memory")

# 原型开发简单快速
collection.add(
    ids=[str(uuid4())],
    embeddings=[embedding],
    documents=[memory_text],
    metadatas=[{"user_id": user_id, "type": "episodic"}]
)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={"user_id": user_id}
)
"""

### 分块策略模式

将文档拆分为可检索的块

**适用场景**：处理文档以存入记忆

# 分块策略：

"""
分块困境：
- 太大：向量失去特异性
- 太小：丢失上下文

最优分块大小取决于：
- 文档类型（代码 vs 散文 vs 数据）
- 查询模式（事实性 vs 探索性）
- 嵌入模型（每个都有最佳区间）

通用建议：大多数场景 256-512 tokens
"""

## 固定大小分块（基线）
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 字符数
    chunk_overlap=50,    # 重叠防止截断句子
    separators=["\n\n", "\n", ". ", " ", ""]  # 优先级顺序
)

chunks = splitter.split_text(document)
"""

## 语义分块（更高质量）
"""
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# 基于语义相似度分割
splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95
)

chunks = splitter.split_text(document)
"""

## 结构感知分块（层级文档）
"""
from langchain.text_splitter import MarkdownHeaderTextSplitter

# 尊重文档结构
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
)

chunks = splitter.split_text(markdown_doc)
# 每个块带有标题元数据作为上下文
"""

## 上下文分块（Anthropic 方法）
"""
# 嵌入前为每个块添加上下文
# 检索失败率降低 35%

def add_context_to_chunk(chunk, document_summary):
    context_prompt = f'''
    Document summary: {document_summary}

    The following is a chunk from this document:
    {chunk}
    '''
    return context_prompt

# 嵌入上下文化后的块，而非原始块
for chunk in chunks:
    contextualized = add_context_to_chunk(chunk, summary)
    embedding = embed(contextualized)
    store(chunk, embedding)  # 存储原始内容，嵌入上下文化版本
"""

## 代码专用分块
"""
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter

# 语言感知分割
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=1000,
    chunk_overlap=200
)

# 尊重函数/类边界
chunks = python_splitter.split_text(python_code)
"""

### 后台记忆形成

异步处理记忆以获得更高质量

**适用场景**：希望提高召回率而不拖慢交互

# 后台记忆形成：

"""
实时记忆提取会拖慢对话并增加智能体工具调用的复杂性。
对话结束后在后台处理能产生更高质量的记忆。

模式：潜意识记忆形成
"""

## LangGraph 后台处理
"""
from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver

async def background_memory_processor(thread_id: str):
    # 对话结束或空闲后运行
    conversation = await load_conversation(thread_id)

    # 无时间压力地提取洞察
    insights = await llm.invoke('''
        Analyze this conversation and extract:
        1. Key facts learned about the user
        2. User preferences revealed
        3. Tasks completed or pending
        4. Patterns in user behavior

        Be thorough - this runs in background.

        Conversation:
        {conversation}
    ''')

    # 存入长期记忆
    for insight in insights:
        await memory.semantic.upsert(
            namespace="user_insights",
            key=generate_key(insight),
            content=insight,
            metadata={"source_thread": thread_id}
        )

# 对话结束或空闲超时时触发
@on_conversation_idle(timeout_minutes=5)
async def process_conversation(thread_id):
    await background_memory_processor(thread_id)
"""

## 记忆整合（类似睡眠）
"""
# 定期整合和去重记忆

async def consolidate_memories(user_id: str):
    # 获取用户所有记忆
    memories = await memory.semantic.list(
        namespace="user_insights",
        filter={"user_id": user_id}
    )

    # 找到相似记忆（潜在重复）
    clusters = cluster_by_similarity(memories, threshold=0.9)

    # 合并相似记忆
    for cluster in clusters:
        if len(cluster) > 1:
            merged = await llm.invoke(f'''
                Consolidate these related memories into one:
                {cluster}

                Preserve all important information.
            ''')
            await memory.semantic.upsert(
                namespace="user_insights",
                key=generate_key(merged),
                content=merged
            )
            # 删除原始记忆
            for old in cluster:
                await memory.semantic.delete(old.id)
"""

### 记忆衰减模式

遗忘旧的、无关的记忆

**适用场景**：记忆增长过大，检索变慢

# 记忆衰减：

"""
不是所有记忆都应永久保存：
- 旧偏好可能已过时
- 任务细节失去相关性
- 冲突的记忆混淆检索

基于以下因素实现智能衰减：
- 新近度（何时创建/访问？）
- 频率（被检索多频繁？）
- 重要性（是核心事实还是细节？）
"""

## 基于时间的衰减
"""
from datetime import datetime, timedelta

async def decay_old_memories(namespace: str, max_age_days: int):
    cutoff = datetime.now() - timedelta(days=max_age_days)

    old_memories = await memory.episodic.list(
        namespace=namespace,
        filter={"last_accessed": {"$lt": cutoff.isoformat()}}
    )

    for mem in old_memories:
        # 软删除（标记为已归档）
        await memory.episodic.update(
            id=mem.id,
            metadata={"archived": True, "archived_at": datetime.now()}
        )
"""

## 基于效用的衰减（MIRIX 方法）
"""
def calculate_memory_utility(memory):
    '''
    受认知科学启发的综合效用评分：
    - 新近度：上次访问是什么时候？
    - 频率：被访问多频繁？
    - 重要性：此信息有多关键？
    '''
    now = datetime.now()

    # 新近度评分（72小时半衰期的指数衰减）
    hours_since_access = (now - memory.last_accessed).total_seconds() / 3600
    recency_score = 0.5 ** (hours_since_access / 72)

    # 频率评分
    frequency_score = min(memory.access_count / 10, 1.0)

    # 重要性（来自元数据或启发式）
    importance = memory.metadata.get("importance", 0.5)

    # 加权组合
    utility = (
        0.4 * recency_score +
        0.3 * frequency_score +
        0.3 * importance
    )

    return utility

async def prune_low_utility_memories(threshold=0.2):
    all_memories = await memory.list_all()
    for mem in all_memories:
        if calculate_memory_utility(mem) < threshold:
            await memory.archive(mem.id)
"""

## 常见陷阱

### 分块将信息与其上下文隔离

严重程度：严重

场景：处理文档以存入向量存储

症状：
检索找到的块单独看没有意义。智能体的回答缺乏全局视角。
检索到"该函数返回 X"却不知道是哪个函数。引用"这个"却不知道"这个"指什么。

为何出错：
当我们为 AI 处理分块时，我们切断了连接，将整体叙事简化为孤立片段，
往往丢失全局视角。一个关于"配置"的块，如果不知道是什么系统的配置，
几乎毫无用处。

推荐修复：

## 上下文分块（Anthropic 方法）
# 嵌入前为每个块添加文档上下文
# 检索失败率降低 35%

def contextualize_chunk(chunk, document):
    summary = summarize(document)

    # LLM 为块生成上下文
    context = llm.invoke(f'''
        Document summary: {summary}

        Generate a brief context statement for this chunk
        that would help someone understand what it refers to:

        {chunk}
    ''')

    return f"{context}\n\n{chunk}"

# 嵌入上下文化版本
for chunk in chunks:
    contextualized = contextualize_chunk(chunk, full_doc)
    embedding = embed(contextualized)
    # 存储原始块，嵌入上下文化版本
    store(original=chunk, embedding=embedding)

## 层级分块
# 以多种粒度存储
chunks_small = split(doc, size=256)
chunks_medium = split(doc, size=512)
chunks_large = split(doc, size=1024)

# 根据查询以适当粒度检索

### 分块大小与查询模式不匹配

严重程度：高

场景：为记忆存储配置分块

症状：
高质量文档产生低质量检索。简单问题找不到相关信息。复杂问题只得到片段而非完整答案。

为何出错：
最优分块大小取决于查询模式：
- 事实性查询需要小的、具体的块
- 概念性查询需要更大的上下文
- 代码需要函数级边界

最佳区间因文档类型和嵌入模型而异。默认的 1000 字符对任何特定场景都不适用。

推荐修复：

## 测试不同大小
from sklearn.metrics import recall_score

def evaluate_chunk_size(documents, test_queries, chunk_size):
    chunks = split_documents(documents, size=chunk_size)
    index = build_index(chunks)

    correct_retrievals = 0
    for query, expected_chunk in test_queries:
        results = index.search(query, k=5)
        if expected_chunk in results:
            correct_retrievals += 1

    return correct_retrievals / len(test_queries)

# 测试多种大小
for size in [256, 512, 768, 1024]:
    recall = evaluate_chunk_size(docs, test_queries, size)
    print(f"Size {size}: Recall@5 = {recall:.2%}")

## 按内容类型推荐大小
CHUNK_SIZES = {
    "documentation": 512,   # 完整概念
    "code": 1000,          # 函数级
    "conversation": 256,   # 轮次级
    "articles": 768,       # 段落级
}

## 使用重叠防止边界问题
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,  # 10% 重叠
)

### 语义搜索返回无关结果

严重程度：高

场景：查询记忆获取上下文

症状：
智能体检索到看似相关但无用的记忆。"告诉我用户的偏好"返回关于一般偏好的对话，
而非此用户的偏好。错误内容获得高相似度分数。

为何出错：
语义相似度不等于相关性。"用户喜欢 Python"和"Python 是编程语言"语义相似，
但信息类型截然不同。没有元数据过滤，检索只是词匹配。

推荐修复：

## 始终先按元数据过滤
# 不要仅依赖语义相似度

# 错误：仅语义搜索
results = index.query(
    vector=query_embedding,
    top_k=5
)

# 正确：先过滤再搜索
results = index.query(
    vector=query_embedding,
    filter={
        "user_id": current_user.id,
        "type": "preference",
        "created_after": cutoff_date,
    },
    top_k=5
)

## 使用混合搜索（语义 + 关键词）
from qdrant_client import QdrantClient

client = QdrantClient(...)

# 融合混合搜索
results = client.search(
    collection_name="memories",
    query_vector=semantic_embedding,
    query_text=query,  # 同时关键词匹配
    fusion={"method": "rrf"},  # Reciprocal Rank Fusion
)

## 使用交叉编码器重排序
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# 初始检索（面向召回）
candidates = index.query(query_embedding, top_k=20)

# 重排序（面向精确）
pairs = [(query, c.text) for c in candidates]
scores = reranker.predict(pairs)
reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

### 旧记忆覆盖当前信息

严重程度：高

场景：用户偏好或事实随时间变化

症状：
智能体使用过时偏好。6 个月前的"用户偏好深色模式"覆盖了最近的"切换到浅色模式"请求。
智能体自信地使用陈旧数据。

为何出错：
向量存储默认没有时间感知。一年前的记忆与今天的记忆检索权重相同。
对于偏好和可变事实，近期信息通常应覆盖旧信息。

推荐修复：

## 添加时间评分
from datetime import datetime, timedelta

def time_decay_score(memory, half_life_days=30):
    age = (datetime.now() - memory.created_at).days
    decay = 0.5 ** (age / half_life_days)
    return decay

def retrieve_with_recency(query, user_id):
    # 获取候选
    candidates = index.query(
        vector=embed(query),
        filter={"user_id": user_id},
        top_k=20
    )

    # 应用时间衰减
    for candidate in candidates:
        time_score = time_decay_score(candidate)
        candidate.final_score = candidate.similarity * 0.7 + time_score * 0.3

    # 按最终分数重排序
    return sorted(candidates, key=lambda x: x.final_score, reverse=True)[:5]

## 偏好更新而非追加
async def update_preference(user_id, category, value):
    # 删除旧偏好
    await memory.delete(
        filter={"user_id": user_id, "type": "preference", "category": category}
    )

    # 存储新偏好
    await memory.upsert(
        id=f"pref-{user_id}-{category}",
        content={"category": category, "value": value},
        metadata={"updated_at": datetime.now()}
    )

## 事实显式版本控制
await memory.upsert(
    id=f"fact-{fact_id}-v{version}",
    content=new_fact,
    metadata={
        "version": version,
        "supersedes": previous_id,
        "valid_from": datetime.now()
    }
)

### 矛盾记忆被同时检索

严重程度：中

场景：用户改变偏好或提供冲突信息

症状：
智能体检索到"用户偏好深色模式"和"用户偏好浅色模式"在同一上下文中。给出不一致的回答。
对用户显得困惑或健忘。

为何出错：
没有冲突解决，新旧信息共存。语义搜索可能同时返回两者，因为它们关于同一主题（偏好）。
智能体无法知道哪个是当前的。

推荐修复：

## 存储时检测冲突
async def store_with_conflict_check(memory, user_id):
    # 查找潜在冲突记忆
    similar = await index.query(
        vector=embed(memory.content),
        filter={"user_id": user_id, "type": memory.type},
        threshold=0.9,  # 非常相似
        top_k=5
    )

    for existing in similar:
        if is_contradictory(memory.content, existing.content):
            # 请求解决
            resolution = await resolve_conflict(memory, existing)
            if resolution == "replace":
                await index.delete(existing.id)
            elif resolution == "version":
                await mark_superseded(existing.id, memory.id)

    await index.upsert(memory)

## 冲突检测启发式
def is_contradictory(new_content, old_content):
    # 使用 LLM 检测矛盾
    result = llm.invoke(f'''
        Do these two statements contradict each other?

        Statement 1: {old_content}
        Statement 2: {new_content}

        Respond with just YES or NO.
    ''')
    return result.strip().upper() == "YES"

## 定期整合
async def consolidate_memories(user_id):
    all_memories = await index.list(filter={"user_id": user_id})
    clusters = cluster_by_topic(all_memories)

    for cluster in clusters:
        if has_conflicts(cluster):
            resolved = await llm.invoke(f'''
                These memories may conflict. Create one consolidated
                memory that represents the current truth:
                {cluster}
            ''')
            await replace_cluster(cluster, resolved)

### 检索的记忆超出上下文窗口

严重程度：中

场景：一次检索过多记忆

症状：
Token 限制错误。智能体截断重要信息。系统提示被截断。检索的记忆与用户查询竞争空间。

为何出错：
检索通常返回 top-k 结果。如果 k 太大或块太大，检索的上下文会淹没窗口。
关键信息（系统提示、近期消息）被挤出。

推荐修复：

## 为不同记忆类型分配 token 预算
TOKEN_BUDGET = {
    "system_prompt": 500,
    "user_profile": 200,
    "recent_messages": 2000,
    "retrieved_memories": 1000,
    "current_query": 500,
    "buffer": 300,  # 安全边际
}

def budget_aware_retrieval(query, context_limit=4000):
    remaining = context_limit - TOKEN_BUDGET["system_prompt"] - TOKEN_BUDGET["buffer"]

    # 优先近期消息
    recent = get_recent_messages(limit=TOKEN_BUDGET["recent_messages"])
    remaining -= count_tokens(recent)

    # 然后用户画像
    profile = get_user_profile(limit=TOKEN_BUDGET["user_profile"])
    remaining -= count_tokens(profile)

    # 最后用剩余预算检索记忆
    memories = retrieve_memories(query, max_tokens=remaining)

    return build_context(profile, recent, memories)

## 基于块大小动态调整 k
def retrieve_with_budget(query, max_tokens=1000):
    avg_chunk_tokens = 150  # 根据你的数据
    max_k = max_tokens // avg_chunk_tokens

    results = index.query(query, top_k=max_k)

    # 如果仍超预算则裁剪
    total_tokens = 0
    filtered = []
    for result in results:
        tokens = count_tokens(result.text)
        if total_tokens + tokens <= max_tokens:
            filtered.append(result)
            total_tokens += tokens
        else:
            break

    return filtered

### 查询和文档嵌入来自不同模型

严重程度：中

场景：升级嵌入模型或混用提供商

症状：
检索质量突然下降。相关文档找不到。返回随机结果。新文档正常，旧文档失败。

为何出错：
嵌入模型产生不同的向量空间。用 text-embedding-3 嵌入的查询无法匹配用 text-ada-002 嵌入的文档。
混用模型产生垃圾相似度分数。

推荐修复：

## 在元数据中跟踪嵌入模型
await index.upsert(
    id=doc_id,
    vector=embedding,
    metadata={
        "embedding_model": "text-embedding-3-small",
        "embedding_version": "2024-01",
        "content": content
    }
)

## 检索时按模型版本过滤
results = index.query(
    vector=query_embedding,
    filter={"embedding_model": current_model},
    top_k=10
)

## 模型升级迁移策略
async def migrate_embeddings(old_model, new_model):
    # 获取所有旧模型文档
    old_docs = await index.list(filter={"embedding_model": old_model})

    for doc in old_docs:
        # 用新模型重新嵌入
        new_embedding = await embed(doc.content, model=new_model)

        # 原地更新
        await index.update(
            id=doc.id,
            vector=new_embedding,
            metadata={"embedding_model": new_model}
        )

## 迁移期间使用独立集合
# 旧集合：生产查询
# 新集合：重新嵌入进行中
# 完成后切换

## 验证检查

### 生产代码中使用内存存储

严重程度：错误

内存存储在重启时丢失数据

消息：检测到内存存储。生产环境请使用持久存储（Postgres、Qdrant、Pinecone）。

### 向量插入不带元数据

严重程度：警告

向量应有元数据以便过滤

消息：向量插入无元数据。添加 user_id、type、timestamp 以便正确过滤。

### 查询不带用户过滤

严重程度：错误

查询应按用户过滤以防止数据泄露

消息：向量查询无用户过滤。始终按 user_id 过滤以防止数据泄露。

### 硬编码分块大小无理由

严重程度：信息

分块大小应测试并有理由

消息：硬编码分块大小。针对你的内容类型测试不同大小并测量检索准确率。

### 分块无重叠

严重程度：警告

分块重叠防止边界问题

消息：文本分割无重叠。添加 chunk_overlap（10-20%）以防止边界问题。

### 语义搜索无过滤

严重程度：警告

纯语义搜索常返回无关结果

消息：纯语义搜索。添加元数据过滤（用户、类型、时间）以提高相关性。

### 检索无结果限制

严重程度：警告

无界检索可能溢出上下文

消息：检索无限制。设置 top_k 以防止上下文溢出。

### 嵌入无模型版本跟踪

严重程度：警告

跟踪嵌入模型以处理迁移

消息：在元数据中存储嵌入模型版本以处理模型迁移。

### 文档和查询嵌入使用不同模型

严重程度：错误

文档和查询必须使用相同嵌入模型

消息：确保索引和查询使用相同嵌入模型。

## 协作

### 委派触发条件

- 用户需要大规模向量数据库 -> data-engineer（生产向量存储运维）
- 用户需要嵌入模型优化 -> ml-engineer（自定义嵌入、微调）
- 用户需要知识图谱 -> knowledge-engineer（基于图的记忆结构）
- 用户需要 RAG 管道 -> llm-architect（端到端检索增强生成）
- 用户需要多智能体共享记忆 -> multi-agent-orchestration（智能体间记忆共享）

## 相关技能

配合良好：`autonomous-agents`、`multi-agent-orchestration`、`llm-architect`、`agent-tool-builder`

## 使用时机

- 用户提及或暗示：智能体记忆
- 用户提及或暗示：长期记忆
- 用户提及或暗示：记忆系统
- 用户提及或暗示：跨会话记忆
- 用户提及或暗示：记忆检索
- 用户提及或暗示：情景记忆
- 用户提及或暗示：语义记忆
- 用户提及或暗示：向量存储
- 用户提及或暗示：rag
- 用户提及或暗示：langmem
- 用户提及或暗示：memgpt
- 用户提及或暗示：对话历史

## 局限性

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
