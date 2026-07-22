---
name: llm-prompt-optimizer
description: "优化任意 LLM 的提示词。运用成熟的提示词工程技术提升输出质量、减少幻觉、降低 token 用量。当用户要求'优化提示词'、'改进 prompt'、'提升 LLM 输出质量'、'减少幻觉'、'压缩提示词'时使用。"
risk: safe
source: community
date_added: "2026-03-04"
---

# LLM Prompt Optimizer

## 概述

本技能将薄弱、模糊或不一致的提示词转化为精准工程化的指令，使任何 LLM（Claude、Gemini、GPT-4、Llama 等）都能稳定产出高质量输出。它系统性地运用提示词工程框架——从 zero-shot 到 few-shot、chain-of-thought 和结构化输出模式。

## 适用场景

- 提示词返回不一致、模糊或幻觉结果时
- 需要从 LLM 稳定获取结构化/JSON 输出时
- 为 AI agent 或聊天机器人设计 system prompt 时
- 想在不牺牲质量的前提下降低 token 用量时
- 为复杂任务实现 chain-of-thought 推理时
- 提示词在一个模型上有效但在另一个模型上失败时

## 分步指南

### 1. 诊断薄弱提示词

优化之前，先识别问题模式：

| 问题 | 症状 | 修复方法 |
|------|------|----------|
| 过于模糊 | 泛泛而谈、无用的回答 | 添加角色 + 上下文 + 约束 |
| 缺乏结构 | 无格式、难以解析的输出 | 明确指定输出格式 |
| 幻觉 | 自信地给出错误答案 | 添加"不确定时说不知道" |
| 不一致 | 每次运行答案不同 | 添加 few-shot 示例 |
| 过长 | 冗长、注水的回复 | 添加长度约束 |

### 2. 应用 RSCIT 框架

每个优化后的提示词都应包含：

- **R** — **Role（角色）**：AI 在这次交互中扮演谁？
- **S** — **Situation（情境）**：它需要什么上下文？
- **C** — **Constraints（约束）**：规则和限制是什么？
- **I** — **Instructions（指令）**：具体要做什么？
- **T** — **Template（模板）**：输出应该长什么样？

**优化前（薄弱提示词）：**
```

Explain machine learning.
```

**优化后（优化提示词）：**
```

You are a senior ML engineer explaining concepts to a junior developer.

Context: The developer has 1 year of Python experience but no ML background.

Task: Explain supervised machine learning in simple terms.

Constraints:
- Use an analogy from everyday life
- Maximum 200 words
- No mathematical formulas
- End with one actionable next step

Format: Plain prose, no bullet points.
```

### 3. Chain-of-Thought (CoT) 模式

对于推理任务，指示模型逐步思考：

```

Solve this problem step by step, showing your work at each stage.
Only provide the final answer after completing all reasoning steps.

Problem: [your problem here]

Thinking process:
Step 1: [identify what's given]
Step 2: [identify what's needed]
Step 3: [apply logic or formula]
Step 4: [verify the answer]

Final Answer:
```

### 4. Few-Shot 示例模式

提供 2-3 个示例来建立模式：

```

Classify the sentiment of customer reviews as POSITIVE, NEGATIVE, or NEUTRAL.

Examples:
Review: "This product exceeded my expectations!" -> POSITIVE
Review: "It arrived broken and support was useless." -> NEGATIVE  
Review: "Product works as described, nothing special." -> NEUTRAL

Now classify:
Review: "[your review here]" ->
```

### 5. 结构化 JSON 输出模式

```

Extract the following information from the text below and return it as valid JSON only.
Do not include any explanation or markdown — just the raw JSON object.

Schema:
{
  "name": string,
  "email": string | null,
  "company": string | null,
  "role": string | null
}

Text: [input text here]
```

### 6. 减少幻觉模式

```

Answer the following question based ONLY on the provided context.
If the answer is not contained in the context, respond with exactly: "I don't have enough information to answer this."
Do not make up or infer information not present in the context.

Context:
[your context here]

Question: [your question here]
```

### 7. 提示词压缩技巧

在不损失效果的前提下减少 token 数量：

```

# Verbose (expensive)
"Please carefully analyze the following code and provide a detailed explanation of 
what it does, how it works, and any potential issues you might find."

# Compressed (efficient, same quality)
"Analyze this code: explain what it does, how it works, and flag any issues."
```

## 最佳实践

- ✅ **务必：** 始终指定输出格式（JSON、markdown、纯文本、列表）
- ✅ **务必：** 使用分隔符（`、---）将指令与内容分开
- ✅ **务必：** 用边界情况测试提示词（空输入、异常数据）
- ✅ **务必：** 在版本控制中管理 system prompt
- ✅ **务必：** 数学、逻辑或多步骤任务添加"think step by step"
- ❌ **不要：** 只用否定指令（"不要冗长"）——加上正面替代方案
- ❌ **不要：** 假设模型了解你的代码库上下文——始终显式提供
- ❌ **不要：** 未经测试就在不同模型上使用同一提示词——它们的行为差异很大

## 提示词审计清单

在生产环境中使用提示词之前：

- [ ] 是否有明确的角色/人设？
- [ ] 输出格式是否明确定义？
- [ ] 边界情况是否处理（空输入、模糊数据）？
- [ ] 长度是否合适（不过长/过短）？
- [ ] 是否在 5+ 种不同输入上测试过？
- [ ] 事实性任务是否已处理幻觉风险？

## 故障排除

**问题：** 模型忽略格式指令
**解决方案：** 将格式指令移到提示词末尾，放在示例之后。使用强语气："You MUST return only valid JSON."

**问题：** 多次运行结果不一致
**解决方案：** 降低 temperature 设置（事实性任务用 0.0-0.3）。增加更多 few-shot 示例。

**问题：** 提示词在 playground 有效但在生产环境失败
**解决方案：** 检查 system prompt 是否正确发送。确认未超出 token 限制（使用 token 计数器）。

**问题：** 输出过长
**解决方案：** 添加明确的字数/句数限制："Respond in exactly 3 bullet points, each under 20 words."

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，停下来请求澄清。