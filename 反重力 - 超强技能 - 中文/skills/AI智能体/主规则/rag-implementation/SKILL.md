---
name: rag-implementation
description: "RAG（检索增强生成）实现工作流，涵盖 Embedding 选型、向量数据库搭建、分块策略和检索优化。触发词：RAG实现、检索增强生成、向量数据库、Embedding选型、分块策略、检索优化、知识库问答、语义搜索、RAG工程"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# RAG 实现工作流

## 概述

用于实现 RAG（检索增强生成）系统的专项工作流，包括 Embedding 模型选型、向量数据库搭建、分块策略、检索优化和评估。

## 适用场景

以下情况使用本工作流：
- 构建 RAG 驱动的应用
- 实现语义搜索
- 创建知识增强的 AI 系统
- 搭建文档问答系统
- 优化检索质量

## 工作流阶段

### 阶段一：需求分析

#### 调用技能
- `ai-product` - AI 产品设计
- `rag-engineer` - RAG 工程

#### 执行步骤
1. 定义使用场景
2. 识别数据源
3. 设定精度要求
4. 确定延迟目标
5. 规划评估指标

#### 即用提示词
```
Use @ai-product to define RAG application requirements
```

### 阶段二：Embedding 选型

#### 调用技能
- `embedding-strategies` - Embedding 选型
- `rag-engineer` - RAG 模式

#### 执行步骤
1. 评估 Embedding 模型
2. 测试领域相关性
3. 衡量 Embedding 质量
4. 考虑成本/延迟
5. 选定模型

#### 即用提示词
```
Use @embedding-strategies to select optimal embedding model
```

### 阶段三：向量数据库搭建

#### 调用技能
- `vector-database-engineer` - 向量数据库
- `similarity-search-patterns` - 相似度搜索

#### 执行步骤
1. 选择向量数据库
2. 设计 Schema
3. 配置索引
4. 建立连接
5. 测试查询

#### 即用提示词
```
Use @vector-database-engineer to set up vector database
```

### 阶段四：分块策略

#### 调用技能
- `rag-engineer` - 分块策略
- `rag-implementation` - RAG 实现

#### 执行步骤
1. 选择分块大小
2. 实现分块逻辑
3. 添加重叠处理
4. 创建元数据
5. 测试检索质量

#### 即用提示词
```
Use @rag-engineer to implement chunking strategy
```

### 阶段五：检索实现

#### 调用技能
- `similarity-search-patterns` - 相似度搜索
- `hybrid-search-implementation` - 混合搜索

#### 执行步骤
1. 实现向量搜索
2. 添加关键词搜索
3. 配置混合搜索
4. 搭建重排序
5. 优化延迟

#### 即用提示词
```
Use @similarity-search-patterns to implement retrieval
```

```
Use @hybrid-search-implementation to add hybrid search
```

### 阶段六：LLM 集成

#### 调用技能
- `llm-application-dev-ai-assistant` - LLM 集成
- `llm-application-dev-prompt-optimize` - Prompt 优化

#### 执行步骤
1. 选择 LLM 供应商
2. 设计 Prompt 模板
3. 实现上下文注入
4. 添加引用处理
5. 测试生成质量

#### 即用提示词
```
Use @llm-application-dev-ai-assistant to integrate LLM
```

### 阶段七：缓存

#### 调用技能
- `prompt-caching` - Prompt 缓存
- `rag-engineer` - RAG 优化

#### 执行步骤
1. 实现响应缓存
2. 搭建 Embedding 缓存
3. 配置 TTL
4. 添加缓存失效机制
5. 监控命中率

#### 即用提示词
```
Use @prompt-caching to implement RAG caching
```

### 阶段八：评估

#### 调用技能
- `llm-evaluation` - LLM 评估
- `evaluation` - AI 评估

#### 执行步骤
1. 定义评估指标
2. 创建测试数据集
3. 衡量检索准确率
4. 评估生成质量
5. 迭代优化

#### 即用提示词
```
Use @llm-evaluation to evaluate RAG system
```

## RAG 架构

```
User Query -> Embedding -> Vector Search -> Retrieved Docs -> LLM -> Response
                |              |              |              |
            Model         Vector DB     Chunk Store    Prompt + Context
```

## 质量门禁

- [ ] Embedding 模型已选定
- [ ] 向量数据库已配置
- [ ] 分块已实现
- [ ] 检索正常工作
- [ ] LLM 已集成
- [ ] 评估通过

## 相关工作流包

- `ai-ml` - AI/ML 开发
- `ai-agent-development` - AI 智能体
- `database` - 向量数据库

## 限制条件
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清。