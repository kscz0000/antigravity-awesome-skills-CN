---
name: ai-agent-development
description: "AI 智能体开发工作流，用于构建自主智能体、多智能体系统和智能体编排，支持 CrewAI、LangGraph 和自定义智能体。触发词：AI智能体开发、智能体构建、多智能体系统、agent开发、自主智能体、智能体编排、CrewAI、LangGraph、agent workflow"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# AI 智能体开发工作流

## 概述

用于构建 AI 智能体的专项工作流，包括单一自主智能体、多智能体系统、智能体编排、工具集成和人机协作模式。

## 何时使用此工作流

在以下情况下使用此工作流：
- 构建自主 AI 智能体
- 创建多智能体系统
- 实现智能体编排
- 为智能体添加工具集成
- 设置智能体记忆系统

## 工作流阶段

### 阶段 1：智能体设计

#### 调用的技能
- `ai-agents-architect` - 智能体架构
- `autonomous-agents` - 自主模式

#### 操作
1. 定义智能体用途
2. 设计智能体能力
3. 规划工具集成
4. 设计记忆系统
5. 定义成功指标

#### 复制粘贴提示词
```
Use @ai-agents-architect to design AI agent architecture
```

### 阶段 2：单一智能体实现

#### 调用的技能
- `autonomous-agent-patterns` - 智能体模式
- `autonomous-agents` - 自主智能体

#### 操作
1. 选择智能体框架
2. 实现智能体逻辑
3. 添加工具集成
4. 配置记忆系统
5. 测试智能体行为

#### 复制粘贴提示词
```
Use @autonomous-agent-patterns to implement single agent
```

### 阶段 3：多智能体系统

#### 调用的技能
- `crewai` - CrewAI 框架
- `multi-agent-patterns` - 多智能体模式

#### 操作
1. 定义智能体角色
2. 设置智能体通信
3. 配置编排机制
4. 实现任务委托
5. 测试协调能力

#### 复制粘贴提示词
```
Use @crewai to build multi-agent system with roles
```

### 阶段 4：智能体编排

#### 调用的技能
- `langgraph` - LangGraph 编排
- `workflow-orchestration-patterns` - 编排模式

#### 操作
1. 设计工作流图
2. 实现状态管理
3. 添加条件分支
4. 配置持久化
5. 测试工作流

#### 复制粘贴提示词
```
Use @langgraph to create stateful agent workflows
```

### 阶段 5：工具集成

#### 调用的技能
- `agent-tool-builder` - 工具构建
- `tool-design` - 工具设计

#### 操作
1. 识别工具需求
2. 设计工具接口
3. 实现工具
4. 添加错误处理
5. 测试工具使用

#### 复制粘贴提示词
```
Use @agent-tool-builder to create agent tools
```

### 阶段 6：记忆系统

#### 调用的技能
- `agent-memory-systems` - 记忆架构
- `conversation-memory` - 对话记忆

#### 操作
1. 设计记忆结构
2. 实现短期记忆
3. 设置长期记忆
4. 添加实体记忆
5. 测试记忆检索

#### 复制粘贴提示词
```
Use @agent-memory-systems to implement agent memory
```

### 阶段 7：评估

#### 调用的技能
- `agent-evaluation` - 智能体评估
- `evaluation` - AI 评估

#### 操作
1. 定义评估标准
2. 创建测试场景
3. 测量智能体性能
4. 测试边界情况
5. 迭代改进

#### 复制粘贴提示词
```
Use @agent-evaluation to evaluate agent performance
```

## 智能体架构

```
User Input -> Planner -> Agent -> Tools -> Memory -> Response
              |          |        |        |
         Decompose   LLM Core  Actions  Short/Long-term
```

## 质量门控

- [ ] 智能体逻辑正常运行
- [ ] 工具已集成
- [ ] 记忆系统可用
- [ ] 编排已测试
- [ ] 评估通过

## 相关工作流包

- `ai-ml` - AI/ML 开发
- `rag-implementation` - RAG 系统
- `workflow-automation` - 工作流模式

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
