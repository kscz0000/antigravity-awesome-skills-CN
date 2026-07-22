---
name: ai-ml
description: "AI与机器学习工作流，涵盖LLM应用开发、RAG实现、智能体架构、ML管道和AI功能开发。触发词：当用户要求'AI工作流'、'机器学习管道'、'LLM开发'、'RAG系统'、'AI智能体'、'ML工程'时使用"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# AI/ML 工作流套件

## 概述

用于构建LLM应用、实现RAG系统、创建AI智能体和开发机器学习管道的综合AI/ML工作流。此套件编排生产级AI开发所需的各项技能。

## 何时使用此工作流

在以下场景使用此工作流：
- 构建LLM驱动的应用程序
- 实现RAG（检索增强生成）
- 创建AI智能体
- 开发ML管道
- 为应用添加AI功能
- 设置AI可观测性

## 工作流阶段

### 阶段1：AI应用设计

#### 调用技能
- `ai-product` - AI产品开发
- `ai-engineer` - AI工程
- `ai-agents-architect` - 智能体架构
- `llm-app-patterns` - LLM模式

#### 操作
1. 定义AI用例
2. 选择合适的模型
3. 设计系统架构
4. 规划数据流
5. 定义成功指标

#### 复制粘贴提示词
```
Use @ai-product to design AI-powered features
```

```
Use @ai-agents-architect to design multi-agent system
```

### 阶段2：LLM集成

#### 调用技能
- `llm-application-dev-ai-assistant` - AI助手开发
- `llm-application-dev-langchain-agent` - LangChain智能体
- `llm-application-dev-prompt-optimize` - 提示词工程
- `gemini-api-dev` - Gemini API

#### 操作
1. 选择LLM提供商
2. 设置API访问
3. 实现提示词模板
4. 配置模型参数
5. 添加流式支持
6. 实现错误处理

#### 复制粘贴提示词
```
Use @llm-application-dev-ai-assistant to build conversational AI
```

```
Use @llm-application-dev-langchain-agent to create LangChain agents
```

```
Use @llm-application-dev-prompt-optimize to optimize prompts
```

### 阶段3：RAG实现

#### 调用技能
- `rag-engineer` - RAG工程
- `rag-implementation` - RAG实现
- `embedding-strategies` - 嵌入选择
- `vector-database-engineer` - 向量数据库
- `similarity-search-patterns` - 相似度搜索
- `hybrid-search-implementation` - 混合搜索

#### 操作
1. 设计数据管道
2. 选择嵌入模型
3. 设置向量数据库
4. 实现分块策略
5. 配置检索
6. 添加重排序
7. 实现缓存

#### 复制粘贴提示词
```
Use @rag-engineer to design RAG pipeline
```

```
Use @vector-database-engineer to set up vector search
```

```
Use @embedding-strategies to select optimal embeddings
```

### 阶段4：AI智能体开发

#### 调用技能
- `autonomous-agents` - 自主智能体模式
- `autonomous-agent-patterns` - 智能体模式
- `crewai` - CrewAI框架
- `langgraph` - LangGraph
- `multi-agent-patterns` - 多智能体系统
- `computer-use-agents` - 计算机使用智能体

#### 操作
1. 设计智能体架构
2. 定义智能体角色
3. 实现工具集成
4. 设置记忆系统
5. 配置编排
6. 添加人机协作

#### 复制粘贴提示词
```
Use @crewai to build role-based multi-agent system
```

```
Use @langgraph to create stateful AI workflows
```

```
Use @autonomous-agents to design autonomous agent
```

### 阶段5：ML管道开发

#### 调用技能
- `ml-engineer` - ML工程
- `mlops-engineer` - MLOps
- `machine-learning-ops-ml-pipeline` - ML管道
- `ml-pipeline-workflow` - ML工作流
- `data-engineer` - 数据工程

#### 操作
1. 设计ML管道
2. 设置数据处理
3. 实现模型训练
4. 配置评估
5. 设置模型注册表
6. 部署模型

#### 复制粘贴提示词
```
Use @ml-engineer to build machine learning pipeline
```

```
Use @mlops-engineer to set up MLOps infrastructure
```

### 阶段6：AI可观测性

#### 调用技能
- `langfuse` - Langfuse可观测性
- `manifest` - Manifest遥测
- `evaluation` - AI评估
- `llm-evaluation` - LLM评估

#### 操作
1. 设置追踪
2. 配置日志
3. 实现评估
4. 监控性能
5. 追踪成本
6. 设置告警

#### 复制粘贴提示词
```
Use @langfuse to set up LLM observability
```

```
Use @evaluation to create evaluation framework
```

### 阶段7：AI安全

#### 调用技能
- `prompt-engineering` - 提示词安全
- `security-scanning-security-sast` - 安全扫描

#### 操作
1. 实现输入验证
2. 添加输出过滤
3. 配置速率限制
4. 设置访问控制
5. 监控滥用行为
6. 实现审计日志

## AI开发检查清单

### LLM集成
- [ ] API密钥已安全存储
- [ ] 速率限制已配置
- [ ] 错误处理已实现
- [ ] 流式传输已启用
- [ ] Token使用已追踪

### RAG系统
- [ ] 数据管道正常运行
- [ ] 嵌入已生成
- [ ] 向量搜索已优化
- [ ] 检索准确性已测试
- [ ] 缓存已实现

### AI智能体
- [ ] 智能体角色已定义
- [ ] 工具已集成
- [ ] 记忆系统正常工作
- [ ] 编排已测试
- [ ] 错误处理健壮

### 可观测性
- [ ] 追踪已启用
- [ ] 指标已收集
- [ ] 评估正在运行
- [ ] 告警已配置
- [ ] 仪表板已创建

## 质量门控

- [ ] 所有AI功能已测试
- [ ] 性能基准已达标
- [ ] 安全措施已到位
- [ ] 可观测性已配置
- [ ] 文档已完成

## 相关工作流套件

- `development` - 应用开发
- `database` - 数据管理
- `cloud-devops` - 基础设施
- `testing-qa` - AI测试

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
