---
name: weaviate-cookbooks
description: "基于官方 cookbook 蓝图构建 Weaviate AI 应用，覆盖 RAG、Agentic RAG、数据探索、多模态 PDF 检索、异步客户端与前端界面。涉及 RAG、agentic RAG、cookbook、Weaviate blueprint、异步客户端、Next.js 前端时使用。"
category: ai
risk: safe
source: community
source_repo: weaviate/agent-skills
source_type: official
date_added: "2026-06-29"
author: Weaviate
tags: [weaviate, rag, agents, vector-database, ai-apps]
tools: [python, weaviate, nextjs]
license: "BSD-3-Clause"
license_source: "https://github.com/weaviate/agent-skills/blob/main/LICENSE"
---

# Weaviate Cookbooks

## 概述

本技能提供一份实施指南与基础需求清单的索引，用于构建基于 Weaviate 的 AI 应用。可参考其中的引用快速搭建全栈应用，并遵循连接管理、环境配置和应用架构的最佳实践。

## 适用场景

- 用户希望构建基于 Weaviate 的 RAG、Agentic RAG、聊天机器人、数据探索或多模态文档检索应用时使用。
- 在编写全栈 Weaviate 应用之前，需要在 cookbook 模式之间进行选型时使用。
- 项目需要 Weaviate 环境、配置、异步客户端或前端指引时使用。
- 用户希望使用 Weaviate 官方蓝图，而非通用向量数据库方案时使用。

### Weaviate Cloud 实例

如果用户尚无实例，可引导其前往 Cloud 控制台注册并创建免费沙箱。通过 [Weaviate Cloud](https://console.weaviate.cloud/signin?utm_source=github&utm_campaign=agent_skills) 创建 Weaviate 实例。

## 构建任何 Cookbook 之前的准备

在生成任何 cookbook 应用前，请遵循以下通用指引：

- [Project Setup Contract](references/project_setup.md)
- [Environment Requirements](references/environment_requirements.md)

随后再进入下方具体的 cookbook 引用。

## Cookbook 索引

- [Query Agent Chatbot](references/query_agent_chatbot.md)：使用 Weaviate Query Agent 构建支持流式响应与聊天历史记录的全栈聊天机器人。
- [Data Explorer](references/data_explorer.md)：构建全栈数据探索应用，涵盖排序、关键词检索与 Weaviate 数据的表格视图。
- [Multimodal RAG: Building Document Search](references/pdf_multimodal_rag.md)：使用 Weaviate Embeddings（ModernVBERT/colmodernvbert）以及 Ollama + Qwen3-VL 作为生成端，构建多模态 RAG 系统。
- [Basic RAG](references/basic_rag.md)：使用 Weaviate 实现基础检索与生成。适用于大多数从 Weaviate 集合中检索数据的场景。
- [Advanced RAG](references/advanced_rag.md)：在基础 RAG 之上加入重排序、查询分解、查询改写、LLM 过滤器选择等增强能力。
- [Basic Agent](references/basic_agent.md)：使用 DSPy 构建具备结构化输出的工具调用型 AI Agent。涵盖 AgentResponse 签名、RouterAgent、工具设计与顺序多步循环。
- [Agentic RAG](references/agentic_rag.md)：构建由 RAG 驱动的 Weaviate AI Agent。涵盖朴素 RAG 工具、带 LLM 生成过滤器的分层 RAG、向量数据库记忆、Weaviate Query Agent 与 Elysia 集成。

## 前端界面（可选）

仅在用户明确要求为其 Weaviate 后端搭建前端时使用。

- [Frontend Interface](references/frontend_interface.md)：构建 Next.js 前端以对接 Weaviate 后端。

## 客户端用法

- [Async Client](references/async_client.md)：生产环境（FastAPI、异步框架）下使用 Weaviate Python 异步客户端的指引。涵盖连接模式、生命周期管理、常见陷阱与多集群配置。

## 局限性

- Cookbook 蓝图仍需结合用户的数据模型、嵌入服务提供方、鉴权模型、部署平台与时延/成本目标进行适配。
- 除非用户提供并确认相关环境，否则本技能不会校验实时 Weaviate 凭据、云配额或模型可用性。
- 生成的应用在上线前应就安全、数据隐私、提示注入风险与生产可观测性进行审查。