---
name: arrowspace
description: "基于图拉普拉斯特征结构的谱向量检索。当余弦/L2 相似度在你的嵌入中遗漏了潜在结构时使用。触发词：谱向量搜索、图拉普拉斯、λτ 评分、潜在结构、嵌入谱分析、谱检索、RAG 谱感知。"
category: data
risk: safe
source: community
source_repo: Genefold/arrowspace-skills
source_type: community
date_added: "2026-06-25"
author: Genefold AI
license: Apache-2.0
license_source: "https://github.com/Genefold/arrowspace-skills/blob/main/LICENSE"
tags: [vector-search, spectral-analysis, graph-laplacian, embeddings, lambda-tau]
tools: [claude, cursor, codex, gemini, opencode]
---

# ArrowSpace 技能

谱向量检索，使用图拉普拉斯特征来增强最近邻搜索。它在物品图上计算拉普拉斯算子，并利用瑞利商（Rayleigh quotient）为每个物品生成一个 λτ（lambda-tau）评分，从而实现既尊重语义相似性又兼顾结构角色的检索。

## 何时使用本技能

- 余弦或 L2 相似度在你的嵌入中遗漏了潜在结构
- 你希望构建具有谱感知能力的基于图的检索
- 你需要刻画某个嵌入空间的谱特性
- 你正在搭建 RAG 流水线，其中上下文角色与语义内容同等重要

## 工作原理

### 步骤 1：安装与导入

```bash
pip install arrowspace
```

```python
from arrowspace import ArrowSpaceBuilder
import numpy as np
```

### 步骤 2：准备数据

传入一个 (N, d) 的 float64 NumPy 嵌入向量数组：

```python
items = np.array([[0.1, 0.2, 0.3],
                  [0.0, 0.5, 0.1],
                  [0.9, 0.1, 0.0]], dtype=np.float64)
```

### 步骤 3：配置图参数

```python
graph_params = {"eps": 0.2, "k": 6, "topk": 3, "p": 2.0, "sigma": 1.0}
builder = ArrowSpaceBuilder(items, graph_params=graph_params)
aspace = builder.build()
```

### 步骤 4：查询

```python
lambdas = aspace.lambdas()           # 按插入顺序索引的数组
sorted_res = aspace.lambdas_sorted()  # (分数, 索引) 对，按升序排列
```

更高的 λτ 值表示该物品在语义上更接近且在结构上更中心。

## 示例

### 示例 1：基础谱检索

```python
items = np.random.randn(100, 64).astype(np.float64)
builder = ArrowSpaceBuilder(items, graph_params={"eps": 0.5, "k": 10, "topk": 5, "p": 2.0, "sigma": None})
aspace = builder.build()
scores = aspace.lambdas()
top_indices = np.argsort(scores)[-5:]
```

### 示例 2：对比谱排序与余弦排序

```python
from sklearn.metrics.pairwise import cosine_similarity
cos_sim = cosine_similarity(items)
cosine_order = np.argsort(cos_sim[0])[::-1]
spectral_order = np.argsort(aspace.lambdas())[::-1]
```

## 最佳实践

- ✅ 在传入 ArrowSpace 之前将嵌入归一化到单位范数
- ✅ 初始 eps 与 1/sqrt(dim) 成比例，再从此处开始调优
- ✅ 根据数据集大小将 k 设在 3 到 25 之间（经验法则：N/50）
- ✅ 设置 sigma=None 以根据距离分布自动选择核宽度
- ❌ 不要在少于 10 个物品的情况下使用（图结构没有意义）
- ❌ 不要用于实时流式数据（ArrowSpace 是面向批处理的）

## 局限性

- 本技能不能替代特定环境的验证、测试或专家评审。
- ArrowSpace 是面向批处理的，并非为流式数据的实时索引而设计。

## 常见陷阱

- **问题：** eps 过小，导致图不连通
  **解决方案：** 增大 eps，或将其设置为与 1/sqrt(embedding_dim) 成比例

- **问题：** k 过大，产生过密的图，导致谱特征被稀释
  **解决方案：** 对大多数数据集保持 k ≤ 25

## 相关技能

- `vector-database-engineer` — 通用的向量数据库专业知识
- `embedding-strategies` — 嵌入模型选择与分块
- `similarity-search-patterns` — 语义搜索实现模式
- `hybrid-search-implementation` — 语义搜索与关键词搜索的组合