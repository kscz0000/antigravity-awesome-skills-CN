---
name: advanced-evaluation
description: 当用户要求"实现 LLM-as-judge"、"比较模型输出"、"创建评估评分标准"、"缓解评估偏差"，或提及直接评分、成对比较、位置偏差、评估流水线、自动化质量评估时使用此技能。触发词：LLM评估、模型输出比较、评估标准、评分标准、偏差缓解、直接评分、成对比较、位置偏差、评估流水线、自动化评估、质量评估、LLM-as-Judge、模型评判。
risk: safe
source: community
date_added: 2026-03-18
---

# 高级评估

本技能涵盖使用 LLM 作为评判者来评估 LLM 输出的生产级技术。它将学术论文、行业实践和实际实施经验中的研究成果综合为构建可靠评估系统的可操作模式。

**核心洞察**：LLM-as-a-Judge 不是单一技术，而是一系列方法的集合，每种方法适用于不同的评估场景。选择正确的方法并缓解已知偏差是本技能培养的核心能力。

## 何时使用

在以下情况下激活此技能：

- 为 LLM 输出构建自动化评估流水线
- 比较多个模型响应以选择最佳方案
- 在评估团队间建立一致的质量标准
- 调试显示不一致结果的评估系统
- 为提示词或模型变更设计 A/B 测试
- 为人工或自动化评估创建评分标准
- 分析自动化评估与人工判断之间的相关性

## 核心概念

### 评估分类体系

评估方法分为两大主要类别，具有不同的可靠性特征：

**直接评分（Direct Scoring）**：单个 LLM 在定义的量表上对一个响应进行评分。
- 最适用于：客观标准（事实准确性、指令遵循、毒性）
- 可靠性：对于定义明确的标准为中等到高
- 失败模式：分数校准漂移、量表解释不一致

**成对比较（Pairwise Comparison）**：LLM 比较两个响应并选择更好的一个。
- 最适用于：主观偏好（语气、风格、说服力）
- 可靠性：对于偏好评估高于直接评分
- 失败模式：位置偏差、长度偏差

MT-Bench 论文（Zheng et al., 2023）的研究表明，对于基于偏好的评估，成对比较比直接评分与人工评判者的一致性更高，而直接评分仍然适用于具有明确基准真相的客观标准。

### 偏差全景

LLM 评判者表现出必须主动缓解的系统性偏差：

**位置偏差（Position Bias）**：在成对比较中，第一位置的响应获得优待。缓解方法：交换位置评估两次，使用多数投票或一致性检查。

**长度偏差（Length Bias）**：较长的响应无论质量如何都被评为更高。缓解方法：明确提示忽略长度、长度归一化评分。

**自我增强偏差（Self-Enhancement Bias）**：模型对自己输出的评分更高。缓解方法：生成和评估使用不同模型，或承认此限制。

**冗长偏差（Verbosity Bias）**：详细的解释即使不必要也会获得更高分数。缓解方法：针对特定标准的评分标准，惩罚不相关的细节。

**权威偏差（Authority Bias）**：自信、权威的语气无论准确性如何都被评为更高。缓解方法：要求引用证据、事实核查层。

### 指标选择框架

根据评估任务结构选择指标：

| 任务类型 | 主要指标 | 次要指标 |
|----------|----------|----------|
| 二元分类（通过/失败） | Recall, Precision, F1 | Cohen's κ |
| 序数量表（1-5 评分） | Spearman's ρ, Kendall's τ | Cohen's κ（加权） |
| 成对偏好 | 一致率、位置一致性 | 置信度校准 |
| 多标签 | Macro-F1, Micro-F1 | 每标签 precision/recall |

关键洞察：系统性的不一致模式比绝对一致性更重要。一个在特定标准上持续与人类不一致的评判者比有随机噪声的评判者更有问题。

## 评估方法

### 直接评分实现

直接评分需要三个组件：明确的标准、校准的量表和结构化的输出格式。

**标准定义模式**：
```
Criterion: [Name]
Description: [What this criterion measures]
Weight: [Relative importance, 0-1]
```

**量表校准**：
- 1-3 量表：带中性选项的二元，认知负荷最低
- 1-5 量表：标准李克特量表，粒度与可靠性的良好平衡
- 1-10 量表：高粒度但难以校准，仅在有详细评分标准时使用

**直接评分提示词结构**：
```
You are an expert evaluator assessing response quality.

## Task
Evaluate the following response against each criterion.

## Original Prompt
{prompt}

## Response to Evaluate
{response}

## Criteria
{for each criterion: name, description, weight}

## Instructions
For each criterion:
1. Find specific evidence in the response
2. Score according to the rubric (1-{max} scale)
3. Justify your score with evidence
4. Suggest one specific improvement

## Output Format
Respond with structured JSON containing scores, justifications, and summary.
```

**思维链要求**：所有评分提示词必须在分数之前要求论证。研究表明，与先给分数的方法相比，这可将可靠性提高 15-25%。

### 成对比较实现

成对比较对于基于偏好的评估本质上更可靠，但需要偏差缓解。

**位置偏差缓解协议**：
1. 第一轮：响应 A 在第一位置，响应 B 在第二位置
2. 第二轮：响应 B 在第一位置，响应 A 在第二位置
3. 一致性检查：如果两轮不一致，返回 TIE 并降低置信度
4. 最终裁决：一致的获胜者，置信度取平均

**成对比较提示词结构**：
```
You are an expert evaluator comparing two AI responses.

## Critical Instructions
- Do NOT prefer responses because they are longer
- Do NOT prefer responses based on position (first vs second)
- Focus ONLY on quality according to the specified criteria
- Ties are acceptable when responses are genuinely equivalent

## Original Prompt
{prompt}

## Response A
{response_a}

## Response B
{response_b}

## Comparison Criteria
{criteria list}

## Instructions
1. Analyze each response independently first
2. Compare them on each criterion
3. Determine overall winner with confidence level

## Output Format
JSON with per-criterion comparison, overall winner, confidence (0-1), and reasoning.
```

**置信度校准**：置信度分数应反映位置一致性：
- 两轮一致：置信度 = 各轮置信度的平均值
- 两轮不一致：置信度 = 0.5，裁决 = TIE

### 评分标准生成

与开放式评分相比，定义明确的评分标准可将评估方差降低 40-60%。

**评分标准组件**：
1. **级别描述**：每个分数级别的清晰边界
2. **特征**：定义每个级别的可观察特征
3. **示例**：每个级别的代表性文本（可选但有价值）
4. **边缘情况**：模糊情况的指导
5. **评分指南**：一致应用的一般原则

**严格度校准**：
- **宽松**：通过分数门槛较低，适合鼓励迭代
- **平衡**：公平，生产使用的典型期望
- **严格**：高标准，适合安全关键或高风险评估

**领域适配**：评分标准应使用领域特定术语。"代码可读性"评分标准提及变量、函数和注释。"医学准确性"评分标准引用临床术语和证据标准。

## 实践指导

### 评估流水线设计

生产评估系统需要多层结构：

```
┌─────────────────────────────────────────────────┐
│                 Evaluation Pipeline              │
├─────────────────────────────────────────────────┤
│                                                   │
│  Input: Response + Prompt + Context               │
│           │                                       │
│           ▼                                       │
│  ┌─────────────────────┐                         │
│  │   Criteria Loader   │ ◄── Rubrics, weights    │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Primary Scorer    │ ◄── Direct or Pairwise  │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Bias Mitigation   │ ◄── Position swap, etc. │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │ Confidence Scoring  │ ◄── Calibration         │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  Output: Scores + Justifications + Confidence     │
│                                                   │
└─────────────────────────────────────────────────┘
```

### 常见反模式

**反模式：无论证的评分**
- 问题：分数缺乏依据，难以调试或改进
- 解决方案：始终要求基于证据的论证，然后再给分数

**反模式：单轮成对比较**
- 问题：位置偏差破坏结果
- 解决方案：始终交换位置并检查一致性

**反模式：过载标准**
- 问题：测量多个事物的标准不可靠
- 解决方案：一个标准 = 一个可测量方面

**反模式：缺少边缘情况指导**
- 问题：评估者对模糊情况处理不一致
- 解决方案：在评分标准中包含边缘情况及明确指导

**反模式：忽略置信度校准**
- 问题：高置信度的错误判断比低置信度更糟糕
- 解决方案：根据位置一致性和证据强度校准置信度

### 决策框架：直接评分 vs 成对比较

使用此决策树：

```
Is there an objective ground truth?
├── Yes → Direct Scoring
│   └── Examples: factual accuracy, instruction following, format compliance
│
└── No → Is it a preference or quality judgment?
    ├── Yes → Pairwise Comparison
    │   └── Examples: tone, style, persuasiveness, creativity
    │
    └── No → Consider reference-based evaluation
        └── Examples: summarization (compare to source), translation (compare to reference)
```

### 扩展评估

对于高容量评估：

1. **LLM 评审团（PoLL）**：使用多个模型作为评判者，聚合投票
   - 减少单个模型的偏差
   - 成本更高但对高风险决策更可靠

2. **分层评估**：快速廉价模型用于筛选，昂贵模型用于边缘情况
   - 对大批量具有成本效益
   - 需要校准筛选阈值

3. **人在回路**：自动化评估处理明确案例，人工审查低置信度案例
   - 关键应用的最佳可靠性
   - 设计反馈循环以改进自动化评估

## 示例

### 示例 1：准确性的直接评分

**输入**：
```
Prompt: "What causes seasons on Earth?"
Response: "Seasons are caused by Earth's tilted axis. As Earth orbits the Sun, 
different hemispheres receive more direct sunlight at different times of year."
Criterion: Factual Accuracy (weight: 1.0)
Scale: 1-5
```

**输出**：
```json
{
  "criterion": "Factual Accuracy",
  "score": 5,
  "evidence": [
    "Correctly identifies axial tilt as primary cause",
    "Correctly explains differential sunlight by hemisphere",
    "No factual errors present"
  ],
  "justification": "Response accurately explains the cause of seasons with correct 
scientific reasoning. Both the axial tilt and its effect on sunlight distribution 
are correctly described.",
  "improvement": "Could add the specific tilt angle (23.5°) for completeness."
}
```

### 示例 2：带位置交换的成对比较

**输入**：
```
Prompt: "Explain machine learning to a beginner"
Response A: [Technical explanation with jargon]
Response B: [Simple analogy-based explanation]
Criteria: ["clarity", "accessibility"]
```

**第一轮（A 在前）**：
```json
{ "winner": "B", "confidence": 0.8 }
```

**第二轮（B 在前）**：
```json
{ "winner": "A", "confidence": 0.6 }
```
（注意：获胜者是 A 因为 B 在第一位置）

**映射后的第二轮**：
```json
{ "winner": "B", "confidence": 0.6 }
```

**最终结果**：
```json
{
  "winner": "B",
  "confidence": 0.7,
  "positionConsistency": {
    "consistent": true,
    "firstPassWinner": "B",
    "secondPassWinner": "B"
  }
}
```

### 示例 3：评分标准生成

**输入**：
```
criterionName: "Code Readability"
criterionDescription: "How easy the code is to understand and maintain"
domain: "software engineering"
scale: "1-5"
strictness: "balanced"
```

**输出**（缩略）：
```json
{
  "levels": [
    {
      "score": 1,
      "label": "Poor",
      "description": "Code is difficult to understand without significant effort",
      "characteristics": [
        "No meaningful variable or function names",
        "No comments or documentation",
        "Deeply nested or convoluted logic"
      ]
    },
    {
      "score": 3,
      "label": "Adequate",
      "description": "Code is understandable with some effort",
      "characteristics": [
        "Most variables have meaningful names",
        "Basic comments present for complex sections",
        "Logic is followable but could be cleaner"
      ]
    },
    {
      "score": 5,
      "label": "Excellent",
      "description": "Code is immediately clear and maintainable",
      "characteristics": [
        "All names are descriptive and consistent",
        "Comprehensive documentation",
        "Clean, modular structure"
      ]
    }
  ],
  "edgeCases": [
    {
      "situation": "Code is well-structured but uses domain-specific abbreviations",
      "guidance": "Score based on readability for domain experts, not general audience"
    }
  ]
}
```

## 指南

1. **始终在分数前要求论证** - 思维链提示词可将可靠性提高 15-25%

2. **始终在成对比较中交换位置** - 单轮比较被位置偏差破坏

3. **将量表粒度与评分标准特异性匹配** - 没有详细级别描述不要使用 1-10

4. **分离客观和主观标准** - 客观用直接评分，主观用成对比较

5. **包含置信度分数** - 根据位置一致性和证据强度校准

6. **明确定义边缘情况** - 模糊情况导致最多的评估方差

7. **使用领域特定评分标准** - 通用评分标准产生通用（不太有用）的评估

8. **根据人工判断验证** - 自动化评估只有与人工评估相关才有价值

9. **监控系统性偏差** - 按标准、响应类型、模型追踪不一致模式

10. **为迭代设计** - 评估系统通过反馈循环改进

## 集成

此技能与以下技能集成：

- **context-fundamentals** - 评估提示词需要有效的上下文结构
- **tool-design** - 评估工具需要适当的 schema 和错误处理
- **context-optimization** - 评估提示词可以针对 token 效率进行优化
- **evaluation**（基础） - 此技能扩展了基础评估概念

## 参考文献

内部参考：
- LLM-as-Judge Implementation Patterns
- Bias Mitigation Techniques
- Metric Selection Guide

外部研究：
- [Eugene Yan: Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/)
- [Judging LLM-as-a-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [G-Eval: NLG Evaluation using GPT-4 (Liu et al., 2023)](https://arxiv.org/abs/2303.16634)
- [Large Language Models are not Fair Evaluators (Wang et al., 2023)](https://arxiv.org/abs/2305.17926)

本集合中的相关技能：
- evaluation - 基础评估概念
- context-fundamentals - 评估提示词的上下文结构
- tool-design - 构建评估工具

---

## 技能元数据

**Created**: 2024-12-24
**Last Updated**: 2024-12-24
**Author**: Muratcan Koylan
**Version**: 1.0.0

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，停止并请求澄清。
