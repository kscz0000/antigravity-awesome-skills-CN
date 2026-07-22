---
name: llm-ops
description: "LLM 运维 —— RAG、嵌入、向量数据库、微调、高级提示工程、LLM 成本、质量评估和生产级 AI 架构。触发词：LLM运维、RAG、向量数据库、embeddings、微调、提示工程、语义缓存、LLM成本优化"
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- llm
- rag
- embeddings
- vector-db
- fine-tuning
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# LLM-OPS —— 生产级 AI

## 概述

LLM 运维 —— RAG、嵌入、向量数据库、微调、高级提示工程、LLM 成本、质量评估和生产级 AI 架构。适用于：实现 RAG、创建嵌入流水线、Pinecone/Chroma/pgvector、微调、提示工程、降低 LLM 成本、评估、语义缓存、流式输出、智能体。

## 何时使用此技能

- 当你需要该领域的专业帮助时

## 何时不使用此技能

- 任务与 LLM 运维无关
- 更简单、更具体的工具可以处理该请求
- 用户需要的是无领域专业知识的通用帮助

## 工作原理

> AI 原型与 AI 产品之间的区别在于可运维性。
> LLM-Ops 是让 AI 可靠、可扩展、经济的工程实践。

---

## 完整 RAG 架构

[文档] -> [分块] -> [嵌入] -> [向量数据库]
                                              |
    [查询] -> [嵌入查询] -> [语义搜索] -> [Top K 分块]
                                                          |
                                           [LLM + 上下文] -> [回答]

## 索引流水线

from anthropic import Anthropic
    import chromadb

    client = Anthropic()
    chroma = chromadb.PersistentClient(path="./chroma_db")

    def chunk_text(text, chunk_size=500, overlap=50):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk: chunks.append(chunk)
        return chunks

    def index_document(doc_id, content_text, metadata=None):
        chunks = chunk_text(content_text)
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        collection.upsert(ids=ids, documents=chunks)
        return len(chunks)

## RAG 查询流水线

def rag_query(query, top_k=5, system=None):
        results = collection.query(
            query_texts=[query], n_results=top_k,
            include=["documents", "metadatas", "distances"])
        context_parts = []
        for doc, meta, dist in zip(results["documents"][0],
                                    results["metadatas"][0],
                                    results["distances"][0]):
            if dist < 1.5:
                src = meta.get("source", "doc")
                context_parts.append(f"[来源: {src}]
{doc}")
        context = "

---

".join(context_parts)
        response = client.messages.create(
            model="claude-opus-4-20250805", max_tokens=1024,
            system=system or "根据上下文回答。",
            messages=[{"role": "user", "content": f"上下文:
{context}

{query}"}])
        return response.content[0].text

---

## 向量数据库选择

| 数据库 | 最佳场景 | 托管方式 | 成本 |
|----|------------|---------|-------|
| Chroma | 开发、本地 | 自托管 | 免费 |
| pgvector | 已使用 PostgreSQL | 自托管/云 | 免费 |
| Pinecone | 托管生产环境 | 云端 | 70美元+/月 |
| Weaviate | 多模态 | 自托管/云 | 免费+ |
| Qdrant | 高性能 | 自托管/云 | 免费+ |

## pgvector

CREATE EXTENSION IF NOT EXISTS vector;
    CREATE TABLE knowledge_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        content TEXT NOT NULL,
        embedding vector(1536),
        metadata JSONB,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX ON knowledge_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
    SELECT content, 1 - (embedding <=> QUERY_VECTOR) AS similarity
    FROM knowledge_embeddings ORDER BY similarity DESC LIMIT 5;

---

## 精英提示结构

Auri 系统提示组件：

- 身份：名称 (Auri)、语调（自然、温暖、直接）、平台 (Amazon Alexa)
- 规则：最多 3 个短段落、无 markdown、对话式语言
- 能力：商业分析、数据驱动建议、创造力
- 限制：无实时互联网、无金融交易
- 个性化：{user_name}、{user_preferences}、{relevant_history}

## 思维链

def cot_analysis(problem: str) -> str:
        steps = [
            "1. 具体要求是什么？",
            "2. 解决问题需要哪些关键信息？",
            "3. 有哪些可行的方案？",
            "4. 哪个方案最好，为什么？",
            "5. 存在哪些风险或限制？",
        ]
        prompt = f"逐步分析：

问题: {problem}

"
        prompt += "
".join(steps) + "

最终回答（简洁，适合语音）："
        return call_claude(prompt)

---

## 语义缓存

class SemanticCache:
        def __init__(self, similarity_threshold=0.95):
            self.threshold = similarity_threshold
            self.cache = {}

        def get_cached(self, query, embedding):
            for cached_emb, (response, _) in self.cache.items():
                if cosine_similarity(embedding, cached_emb) >= self.threshold:
                    return response
            return None

        def set_cache(self, query, embedding, response):
            self.cache[tuple(embedding)] = (response, query)

## Claude 成本估算

PRICING = {
        "claude-opus-4-20250805": {"input": 15.00, "output": 75.00},
        "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
        "claude-haiku-3-5": {"input": 0.80, "output": 4.00},
    }

    def estimate_monthly_cost(model, avg_input, avg_output, req_per_day):
        p = PRICING[model]
        daily = (avg_input + avg_output) * req_per_day / 1e6
        monthly = daily * p["input"] * 30
        return {"model": model, "monthly_cost": "USD %.2f" % monthly}

---

## 评估框架

from anthropic import Anthropic
    client = Anthropic()

    def evaluate_response(question, expected, actual, criteria):
        criteria_text = "
".join(f"- {c}" for c in criteria)
        eval_prompt = (
            f"评估 AI 助手的回答。

"
            f"问题: {question}
期望回答: {expected}
"
            f"实际回答: {actual}

评估标准:
{criteria_text}

"
            "每个标准打分 0-10 并给出理由。JSON 格式。"
        )
        response = client.messages.create(
            model="claude-haiku-3-5", max_tokens=1024,
            messages=[{"role": "user", "content": eval_prompt}]
        )
        import json
        return json.loads(response.content[0].text)

    AURI_EVALS = [
        {
            "question": "现在创业的主要风险有哪些？",
            "criteria": ["事实准确性", "相关性", "语音清晰度"]
        },
    ]

---

## 命令

| 命令 | 操作 |
|---------|------|
| /rag-setup | 配置完整 RAG 流水线 |
| /embed-docs | 将文档索引到向量数据库 |
| /prompt-optimize | 优化提示以提升质量和降低成本 |
| /cost-estimate | 估算 LLM 月度成本 |
| /eval-run | 运行质量评估套件 |
| /cache-setup | 配置语义缓存 |
| /model-select | 为用例选择理想模型 |

## 最佳实践

- 提供清晰、具体的项目上下文和需求
- 在将建议应用到生产代码前进行审查
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其领域专业范围之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为特定环境验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
