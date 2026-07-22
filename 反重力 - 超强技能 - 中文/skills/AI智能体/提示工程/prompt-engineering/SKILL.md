---
name: prompt-engineering
description: "关于提示词工程模式、最佳实践和优化技术的专业指南。当用户想要改进提示词、学习提示策略或调试智能体行为时使用。触发词：提示词工程、prompt engineering、提示词优化、调试智能体。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 提示词工程模式

高级提示词工程技术，用于最大化 LLM 的性能、可靠性和可控性。

## 核心能力

### 1. 少样本学习

通过展示示例而非解释规则来教导模型。包含 2-5 个输入-输出对，演示所需行为。当需要一致的格式、特定的推理模式或处理边界情况时使用。更多示例可提高准确性但会消耗 token——根据任务复杂度权衡。

**示例：**

```markdown
Extract key information from support tickets:

Input: "My login doesn't work and I keep getting error 403"
Output: {"issue": "authentication", "error_code": "403", "priority": "high"}

Input: "Feature request: add dark mode to settings"
Output: {"issue": "feature_request", "error_code": null, "priority": "low"}

Now process: "Can't upload files larger than 10MB, getting timeout"
```

### 2. 思维链提示

在最终答案前请求逐步推理。添加"让我们逐步思考"（零样本）或包含示例推理轨迹（少样本）。用于需要多步逻辑、数学推理的复杂问题，或需要验证模型思考过程时。可将分析任务的准确性提高 30-50%。

**示例：**

```markdown
Analyze this bug report and determine root cause.

Think step by step:

1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently that could cause this?
4. What components are involved?
5. What is the most likely root cause?

Bug: "Users can't save drafts after the cache update deployed yesterday"
```

### 3. 提示词优化

通过测试和迭代系统性地改进提示词。从简单开始，衡量性能（准确性、一致性、token 使用量），然后迭代。在包括边界情况的多样输入上测试。使用 A/B 测试比较变体。对于一致性和成本至关重要的生产提示词至关重要。

**示例：**

```markdown
Version 1 (Simple): "Summarize this article"
→ Result: Inconsistent length, misses key points

Version 2 (Add constraints): "Summarize in 3 bullet points"
→ Result: Better structure, but still misses nuance

Version 3 (Add reasoning): "Identify the 3 main findings, then summarize each"
→ Result: Consistent, accurate, captures key information
```

### 4. 模板系统

构建可复用的提示词结构，包含变量、条件部分和模块化组件。用于多轮对话、基于角色的交互，或相同模式应用于不同输入时。减少重复并确保类似任务的一致性。

**示例：**

```python
# Reusable code review template
template = """
Review this {language} code for {focus_area}.

Code:
{code_block}

Provide feedback on:
{checklist}
"""

# Usage
prompt = template.format(
    language="Python",
    focus_area="security vulnerabilities",
    code_block=user_code,
    checklist="1. SQL injection\n2. XSS risks\n3. Authentication"
)
```

### 5. 系统提示词设计

设置贯穿对话的全局行为和约束。定义模型的角色、专业水平、输出格式和安全指南。系统提示词用于不应逐轮变化的稳定指令，从而为用户消息释放 token 空间用于可变内容。

**示例：**

```markdown
System: You are a senior backend engineer specializing in API design.

Rules:

- Always consider scalability and performance
- Suggest RESTful patterns by default
- Flag security concerns immediately
- Provide code examples in Python
- Use early return pattern

Format responses as:

1. Analysis
2. Recommendation
3. Code example
4. Trade-offs
```

## 关键模式

### 渐进式披露

从简单提示词开始，仅在需要时增加复杂性：

1. **级别 1**：直接指令

   - "总结这篇文章"

2. **级别 2**：添加约束

   - "用 3 个要点总结这篇文章，重点关注关键发现"

3. **级别 3**：添加推理

   - "阅读这篇文章，识别主要发现，然后用 3 个要点总结"

4. **级别 4**：添加示例
   - 包含 2-3 个输入-输出对的示例摘要

### 指令层次结构

```
[System Context] → [Task Instruction] → [Examples] → [Input Data] → [Output Format]
```

### 错误恢复

构建能优雅处理失败的提示词：

- 包含回退指令
- 请求置信度分数
- 不确定时请求替代解释
- 指定如何表示缺失信息

## 最佳实践

1. **具体明确**：模糊的提示词会产生不一致的结果
2. **展示而非讲述**：示例比描述更有效
3. **广泛测试**：在多样、有代表性的输入上评估
4. **快速迭代**：微小改变可能产生重大影响
5. **监控性能**：在生产环境中跟踪指标
6. **版本控制**：像对待代码一样对提示词进行版本管理
7. **记录意图**：解释提示词为何如此结构

## 常见陷阱

- **过度工程化**：在尝试简单提示词之前就使用复杂提示词
- **示例污染**：使用与目标任务不匹配的示例
- **上下文溢出**：过多示例超出 token 限制
- **指令模糊**：为多种解释留下空间
- **忽略边界情况**：未在异常或边界输入上测试

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。