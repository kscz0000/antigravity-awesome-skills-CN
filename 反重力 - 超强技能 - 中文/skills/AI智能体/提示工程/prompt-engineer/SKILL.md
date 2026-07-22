---
name: prompt-engineer
description: "将用户提示词转化为优化后的提示词，支持多种框架（RTF、RISEN、Chain of Thought、RODES、Chain of Density、RACE、RISE、STAR、SOAP、CLEAR、GROW）。触发词：提示词优化、prompt优化、提示词工程、prompt engineering、优化提示词、改进提示词、提示词框架、写更好的提示词"
category: automation
risk: safe
source: community
tags: "[prompt-engineering, optimization, frameworks, ai-enhancement]"
date_added: "2026-02-27"
---

## 用途

本技能将原始、无结构的用户提示词转化为高度优化的提示词，使用成熟的提示词工程框架。它分析用户意图、识别任务复杂度，并智能选择最合适的框架来最大化 Claude/ChatGPT 的输出质量。

技能以"魔法模式"运行——在后台静默工作，仅在确实需要澄清时才与用户交互。用户会收到打磨好的、可直接使用的提示词，无需了解技术解释或框架术语。

这是一个**通用技能**，适用于任何终端环境，不限于 Obsidian vault 或特定项目结构。

## 使用时机
当出现以下情况时调用本技能：

- 用户提供了模糊或笼统的提示词（如"帮我写 Python 代码"）
- 用户有复杂想法但难以清晰表达
- 用户的提示词缺乏结构、上下文或具体要求
- 任务需要逐步推理（调试、分析、设计）
- 用户需要某个 AI 任务的提示词但不了解提示词框架
- 用户想提升现有提示词的效果
- 用户问"怎么让 AI 做..."或"帮我写一个提示词..."之类的变体

## 工作流程

### 第一步：分析意图

**目标：** 理解用户真正想完成什么。

**操作：**
1. 读取用户提供的原始提示词
2. 检测任务特征：
   - **类型：** 编码、写作、分析、设计、学习、规划、决策、创意等
   - **复杂度：** 简单（单步）、中等（多步）、复杂（需要推理/设计）
   - **清晰度：** 意图明确 vs. 模糊/含糊
   - **领域：** 技术、商业、创意、学术、个人等
3. 识别隐含需求：
   - 用户需要示例吗？
   - 指定了输出格式吗？
   - 有约束条件（时间、资源、范围）吗？
   - 这是探索性的还是执行导向的？

**检测模式：**
- **简单任务：** 短提示词（<50字符），单一动词，无上下文
- **复杂任务：** 长提示词（>200字符），多个需求，有条件逻辑
- **模糊任务：** 通用动词（"帮助"、"改进"），缺少对象/上下文
- **结构化任务：** 提及步骤、阶段、交付物、利益相关者


### 第二步：澄清提问（条件触发）

**目标：** 仅在对框架选择或提示词质量至关重要时才收集缺失信息。

**触发条件** — 仅在以下情况提问：
- 任务类型完全模糊（无法判断是编码、写作还是分析）
- 目标受众未知且会实质性影响输出
- 范围未定义，选错范围会使提示词失效
- 要求的输出格式冲突或缺失且无法推断

**提问限制：**
- 每次调用最多 3 个问题
- 尽可能将相关问题合并为一个
- 如果上下文已足够，完全跳过此步骤（大多数情况如此）

**澄清对话示例：**

```
用户："帮我搞搞 AI"

第二步（触发 — 任务类型模糊）：
"为了写出最好的提示词，我需要快速确认一下：
1. 你想用 AI 做什么——构建东西、学习它，还是用 AI 工具完成某个任务？"
```

**关键规则：** 拿不准时，跳过澄清，用已有上下文生成最佳提示词。过度提问会破坏"魔法模式"体验。


### 第三步：选择框架

**目标：** 将任务特征映射到最优的提示词框架。

**框架映射逻辑：**

| 任务类型 | 推荐框架 | 选择理由 |
|-----------|-------------------------|-----------|
| **角色扮演任务**（扮演专家、顾问） | **RTF** (Role-Task-Format) | 清晰的角色定义 + 任务 + 输出格式 |
| **逐步推理**（调试、证明、逻辑） | **Chain of Thought** | 鼓励显式推理步骤 |
| **结构化项目**（多阶段、交付物） | **RISEN** (Role, Instructions, Steps, End goal, Narrowing) | 为复杂工作提供全面结构 |
| **复杂设计/分析**（系统、架构） | **RODES** (Role, Objective, Details, Examples, Sense check) | 平衡细节与验证 |
| **总结归纳**（压缩、综合） | **Chain of Density** | 迭代提炼到核心信息 |
| **沟通表达**（报告、演示、叙事） | **RACE** (Role, Audience, Context, Expectation) | 受众感知的消息传递 |
| **调查分析**（研究、诊断） | **RISE** (Research, Investigate, Synthesize, Evaluate) | 系统化分析方法 |
| **情境化场景**（带背景的问题解决） | **STAR** (Situation, Task, Action, Result) | 丰富上下文的问题框架 |
| **文档记录**（医疗、技术、档案） | **SOAP** (Subjective, Objective, Assessment, Plan) | 结构化信息捕获 |
| **目标设定**（OKR、目标、指标） | **CLEAR** (Collaborative, Limited, Emotional, Appreciable, Refinable) | 目标清晰且可执行 |
| **辅导发展**（指导、成长） | **GROW** (Goal, Reality, Options, Will) | 发展性对话结构 |

**混合策略：**
- 当任务跨越多种类型时，**组合 2-3 个框架**
- 示例：复杂技术项目 → **RODES + Chain of Thought**（结构 + 推理）
- 示例：领导力决策 → **CLEAR + GROW**（目标清晰 + 发展）

**选择标准：**
- 主框架 = 与核心任务类型最佳匹配
- 辅助框架 = 处理额外的复杂度维度
- 避免过度工程化：简单任务用简单框架

**关键规则：** 框架选择在**后台静默完成**——不要向用户解释框架选择。

Role: You are a senior software architect. [RTF - Role]

Objective: Design a microservices architecture for [system]. [RODES - Objective]

Approach this step-by-step: [Chain of Thought]
1. Analyze current monolithic constraints
2. Identify service boundaries
3. Design inter-service communication
4. Plan data consistency strategy

Details: [RODES - Details]
- Expected traffic: [X]
- Data volume: [Y]
- Team size: [Z]

Output Format: [RTF - Format]
Provide architecture diagram description, service definitions, and migration roadmap.

Sense Check: [RODES - Sense check]
Validate that services are loosely coupled, independently deployable, and aligned with business domains.
```

**4.5. 语言适配**
- 如果原始提示词是葡萄牙语，生成葡萄牙语提示词
- 如果原始提示词是英语，生成英语提示词
- 如果是混合语言，默认英语（对 AI 模型更通用）

**4.6. 质量检查**
最终输出前，验证：
- [ ] 提示词自包含（不需要外部上下文）
- [ ] 任务具体且可衡量
- [ ] 输出格式清晰
- [ ] 无模糊表述
- [ ] 细节程度与任务复杂度匹配


## 关键规则

### **绝对不要：**

- ❌ 假设未提供的信息——关键细节缺失时务必提问
- ❌ 解释选择了哪个框架或为什么（魔法模式——保持不可见）
- ❌ 生成通用的、一刀切的提示词——始终根据上下文定制
- ❌ 在最终提示词中使用技术术语（除非用户领域是技术性的）
- ❌ 提问超过 3 个澄清问题（避免用户疲劳）
- ❌ 在输出中包含元评论（"这个提示词使用了..."、"注意..."）
- ❌ 不用代码块格式展示输出
- ❌ 语言使用不一致（如果用户用中文写，就用中文回复）

### **务必做到：**

- ✅ 生成前先分析意图（第一步是强制的）
- ✅ 关键信息模糊时提出澄清问题（第二步条件触发）
- ✅ 根据任务类型和复杂度选择框架（第三步映射）
- ✅ 当能提升提示词质量时混合多个框架
- ✅ 提示词长度适配原始输入复杂度（简单 → 简短，复杂 → 详细）
- ✅ 在生成的提示词中包含输出格式规范
- ✅ 用整洁的 Markdown 代码块展示最终提示词
- ✅ 让提示词自包含（不依赖外部上下文）
- ✅ 在复杂提示词中使用示例来说明预期输出
- ✅ 展示前验证提示词完整性（第四步 4.6 的质量检查）


### **示例 2：复杂明确提示 → RODES + Chain of Thought（无需澄清）**

**用户输入：**
```
copilot> create prompt for: I need to build a product recommendation system considering purchase history, user preferences, and market trends
```

**技能内部处理：**
1. **分析：** 意图明确，复杂任务（ML 系统设计），技术领域
2. **澄清：** 跳过（信息充分）
3. **选择：** RODES（复杂设计）+ Chain of Thought（需要推理）

**技能输出：**

````markdown
```
Role: You are a senior machine learning engineer specializing in recommendation systems.

Objective: Design a product recommendation system that combines user purchase history, preferences, and market trends.

Details:
- Input data sources: user transaction logs, preference surveys, market trend APIs
- Algorithm considerations: collaborative filtering, content-based filtering, hybrid approaches
- Performance metrics: precision, recall, diversity, novelty
- Scalability: system must handle 100k+ users
- Real-time constraints: recommendations updated within 500ms

Approach step-by-step:
1. Analyze the three data sources and their relationships
2. Propose 2-3 algorithm approaches with trade-offs analysis
3. Design data pipeline architecture (ingestion, processing, serving)
4. Define evaluation metrics and A/B testing strategy
5. Outline implementation roadmap with phases

Examples:
- Show pseudocode for core recommendation logic
- Illustrate data flow diagram
- Provide sample API response structure

Sense Check: Validate that the proposed solution balances personalization with discovery, scales to production load, and incorporates real-time market trends effectively.

Output format: Technical design document with architecture diagrams, algorithm justification, and implementation roadmap.
```
````


### **示例 4：代码调试 → Chain of Thought**

**用户输入：**
```
copilot> optimize prompt: my Python code isn't working, needs debugging
```

**技能内部处理：**
1. **分析：** 调试任务，需要逐步推理
2. **澄清：** 跳过（用户稍后会提供代码上下文）
3. **选择：** Chain of Thought

**技能输出：**

````markdown
```
You are an expert Python debugger.

Task: Debug the Python code provided by the user by analyzing it step-by-step.

Debugging approach:
1. Read and understand the code's intended purpose
2. Identify the error or unexpected behavior
3. Trace variable states at each execution step
4. Locate the root cause of the issue
5. Propose fix with explanation
6. Suggest preventive measures to avoid similar bugs

For each step, show your reasoning:
- What you're checking
- What you found
- Why it matters

Output format:
- **Issue identified:** [Describe the bug]
- **Root cause:** [Why it's happening]
- **Fix:** [Corrected code with comments]
- **Prevention:** [Best practices to avoid this in the future]

Include a working example to verify the fix.
```
````


## 备注

本技能**平台无关**，适用于任何可用 GitHub Copilot CLI 的终端环境。不依赖于：
- Obsidian vault 结构
- 特定项目配置
- 外部文件或模板

技能完全自包含，仅基于用户输入和框架知识运行。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
