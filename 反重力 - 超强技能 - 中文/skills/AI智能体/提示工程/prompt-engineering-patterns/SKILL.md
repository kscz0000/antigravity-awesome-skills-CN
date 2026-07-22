---
name: prompt-engineering-patterns
description: "掌握高级提示词工程技术，最大化 LLM 的性能、可靠性和可控性。触发词：提示词工程、prompt engineering、提示词模式、提示词优化、few-shot、chain-of-thought、提示词模板、系统提示词、prompt patterns"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Prompt Engineering Patterns

掌握高级提示词工程技术，最大化 LLM 的性能、可靠性和可控性。

## 不适用场景

- 任务与提示词工程模式无关
- 需要超出此范围的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 为生产级 LLM 应用设计复杂提示词
- 优化提示词性能和一致性
- 实现结构化推理模式（Chain-of-Thought、Tree-of-Thought）
- 构建带动态示例选择的 Few-Shot Learning 系统
- 创建带变量插值的可复用提示词模板
- 调试和优化产生不一致输出的提示词
- 为专用 AI 助手实现 System Prompt

## 核心能力

### 1. Few-Shot Learning
- 示例选择策略（语义相似度、多样性采样）
- 在示例数量与上下文窗口约束间取得平衡
- 用输入-输出对构建有效的示范
- 从知识库动态检索示例
- 通过策略性示例选择处理边界情况

### 2. Chain-of-Thought Prompting
- 逐步推理引导
- Zero-Shot CoT（使用 "Let's think step by step"）
- Few-Shot CoT（附带推理轨迹）
- Self-Consistency 技术（采样多条推理路径）
- 验证和确认步骤

### 3. Prompt 优化
- 迭代式精炼工作流
- A/B 测试提示词变体
- 衡量提示词性能指标（准确率、一致性、延迟）
- 在保持质量的同时减少 token 用量
- 处理边界情况和失败模式

### 4. 模板系统
- 变量插值和格式化
- 条件性提示词段落
- 多轮对话模板
- 基于角色的提示词组合
- 模块化提示词组件

### 5. System Prompt 设计
- 设置模型行为和约束
- 定义输出格式和结构
- 确立角色和专业领域
- 安全准则和内容策略
- 上下文设置和背景信息

## 快速开始

```python
from prompt_optimizer import PromptTemplate, FewShotSelector

# Define a structured prompt template
template = PromptTemplate(
    system="You are an expert SQL developer. Generate efficient, secure SQL queries.",
    instruction="Convert the following natural language query to SQL:\n{query}",
    few_shot_examples=True,
    output_format="SQL code block with explanatory comments"
)

# Configure few-shot learning
selector = FewShotSelector(
    examples_db="sql_examples.jsonl",
    selection_strategy="semantic_similarity",
    max_examples=3
)

# Generate optimized prompt
prompt = template.render(
    query="Find all users who registered in the last 30 days",
    examples=selector.select(query="user registration date filter")
)
```

## 关键模式

### 渐进式披露
从简单提示词开始，仅在需要时增加复杂度：

1. **Level 1**：直接指令
   - "Summarize this article"

2. **Level 2**：添加约束
   - "Summarize this article in 3 bullet points, focusing on key findings"

3. **Level 3**：添加推理
   - "Read this article, identify the main findings, then summarize in 3 bullet points"

4. **Level 4**：添加示例
   - 包含 2-3 个带输入-输出对的示例摘要

### 指令层级
```
[System Context] → [Task Instruction] → [Examples] → [Input Data] → [Output Format]
```

### 错误恢复
构建能优雅处理失败的提示词：
- 包含回退指令
- 请求置信度分数
- 不确定时要求提供替代解释
- 指定如何表示信息缺失

## 最佳实践

1. **具体明确**：模糊的提示词会产生不一致的结果
2. **用示例说话**：示例比描述更有效
3. **充分测试**：在多样化、有代表性的输入上评估
4. **快速迭代**：小改动可能带来大影响
5. **监控性能**：在生产环境中跟踪指标
6. **版本控制**：像对待代码一样对提示词进行版本管理
7. **记录意图**：解释提示词为何如此组织

## 常见陷阱

- **过度工程**：还没试简单提示词就从复杂的开始
- **示例污染**：使用与目标任务不匹配的示例
- **上下文溢出**：用过多示例超出 token 限制
- **指令模糊**：给多种解释留出空间
- **忽略边界情况**：未在异常或边界输入上测试

## 集成模式

### 与 RAG 系统集成
```python
# Combine retrieved context with prompt engineering
prompt = f"""Given the following context:
{retrieved_context}

{few_shot_examples}

Question: {user_question}

Provide a detailed answer based solely on the context above. If the context doesn't contain enough information, explicitly state what's missing."""
```

### 与验证系统集成
```python
# Add self-verification step
prompt = f"""{main_task_prompt}

After generating your response, verify it meets these criteria:
1. Answers the question directly
2. Uses only information from provided context
3. Cites specific sources
4. Acknowledges any uncertainty

If verification fails, revise your response."""
```

## 性能优化

### Token 效率
- 去除冗余的词语和短语
- 首次定义后一致使用缩写
- 合并相似指令
- 将稳定内容移至 System Prompt

### 延迟优化
- 在不牺牲质量的前提下最小化提示词长度
- 对长文本输出使用 streaming
- 缓存常见的提示词前缀
- 尽可能批量处理相似请求

## 资源

- **references/few-shot-learning.md**：示例选择与构建的深入指南
- **references/chain-of-thought.md**：高级推理引导技术
- **references/prompt-optimization.md**：系统化精炼工作流
- **references/prompt-templates.md**：可复用模板模式
- **references/system-prompts.md**：系统级提示词设计
- **assets/prompt-template-library.md**：经过实战检验的提示词模板
- **assets/few-shot-examples.json**：精选示例数据集
- **scripts/optimize-prompt.py**：自动化提示词优化工具

## 成功指标

跟踪以下提示词 KPI：
- **准确率**：输出的正确性
- **一致性**：相似输入间的可复现性
- **延迟**：响应时间（P50、P95、P99）
- **Token 用量**：每次请求的平均 token 数
- **成功率**：有效输出的百分比
- **用户满意度**：评分和反馈

## 后续步骤

1. 查阅提示词模板库，了解常见模式
2. 为你的具体用例实验 Few-Shot Learning
3. 实现提示词版本管理和 A/B 测试
4. 搭建自动化评估流水线
5. 记录你的提示词工程决策和经验

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
