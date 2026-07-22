---
name: product-marketing-context
description: "创建或更新可复用的产品营销上下文文档，涵盖定位、受众、ICP、用例和消息传递。在项目开始时使用，避免在多个任务中重复阐述核心营销信息。触发词：产品营销、营销上下文、产品定位、ICP、受众画像、营销文档、产品消息传递。"
risk: unknown
source: "https://github.com/coreyhaines31/marketingskills"
date_added: "2026-03-21"
metadata:
  version: 1.1.0
---

# 产品营销上下文

帮助用户创建和维护产品营销上下文文档。该文档记录基础定位和消息传递信息，供其他营销技能引用，避免用户反复说明相同内容。

## 使用场景
- 需要创建可复用的产品、受众和定位上下文文件时使用。
- 在营销项目开始时、使用更专业的营销技能之前使用。
- 用户不想反复解释 ICP、消息传递和产品基础信息时使用。

文档存储在 `.agents/product-marketing-context.md`。

## 工作流程

### 步骤一：检查已有上下文

首先检查 `.agents/product-marketing-context.md` 是否已存在。同时检查 `.claude/product-marketing-context.md` 是否有旧版本——如果在后者找到但前者没有，主动提出迁移。

**如果已存在：**
- 读取并总结已有内容
- 询问用户想更新哪些章节
- 只收集相关章节的信息

**如果不存在，提供两个选项：**

1. **从代码库自动生成**（推荐）：分析仓库——README、落地页、营销文案、package.json 等——然后草拟 V1 版上下文文档。用户审阅、修正、补充。这比从零开始快得多。

2. **从零开始**：按章节逐一引导对话，逐个收集信息。

大多数用户会选择选项 1。展示草稿后问："哪些需要修正？哪些还缺？"

### 步骤二：收集信息

**如果自动生成：**
1. 阅读代码库：README、落地页、营销文案、关于页面、meta 描述、package.json、已有文档
2. 根据发现草拟所有章节
3. 展示草稿，询问需要修正或补充的内容
4. 迭代直到用户满意

**如果从零开始：**
按下方章节逐一引导对话，每次只处理一个章节。不要一次性抛出所有问题。

每个章节：
1. 简要说明要收集什么
2. 提出相关问题
3. 确认准确性
4. 继续下一章节

尽量收集客户的原话——精确的措辞比润色后的描述更有价值，因为它反映了客户真实的思考和表达方式，能让文案更有共鸣。

---

## 需要收集的章节

### 1. 产品概述
- 一句话描述
- 产品功能（2-3 句话）
- 产品类别（放在哪个"货架"上——客户怎么搜索你）
- 产品类型（SaaS、平台、电商、服务等）
- 商业模式和定价

### 2. 目标受众
- 目标公司类型（行业、规模、阶段）
- 目标决策者（角色、部门）
- 主要用例（你解决的核心问题）
- 待完成任务（客户"雇用"你完成的 2-3 件事）
- 具体用例或场景

### 3. 用户画像（仅 B2B）
如果购买涉及多个利益相关方，为每个角色收集：
- 用户、推动者、决策者、财务决策者、技术影响者
- 每个角色关心什么、面临什么挑战、你承诺给他们什么价值

### 4. 问题与痛点
- 客户找到你之前面临的核心挑战
- 现有方案为何不足
- 付出的代价（时间、金钱、机会）
- 情绪张力（压力、恐惧、疑虑）

### 5. 竞争格局
- **直接竞品**：相同方案，相同问题（如 Calendly vs SavvyCal）
- **次要竞品**：不同方案，相同问题（如 Calendly vs Superhuman scheduling）
- **间接竞品**：冲突的方式（如 Calendly vs 个人助理）
- 每个竞品对客户来说不足在哪里

### 6. 差异化
- 关键差异点（竞品缺少的能力）
- 你的解决方式有何不同
- 为什么更好（收益）
- 客户为什么选择你而不是竞品

### 7. 异议与反画像
- 销售中最常听到的 3 个异议及应对方式
- 哪些人不适合（反画像）

### 8. 转换动力
JTBD 四力模型：
- **推力**：什么不满驱使他们离开现有方案
- **拉力**：什么吸引他们选择你
- **惯性**：什么让他们留在现有方案
- **焦虑**：他们对转换有什么顾虑

### 9. 客户语言
- 客户如何描述问题（原话）
- 客户如何描述你的方案（原话）
- 应该使用的词/短语
- 应该避免的词/短语
- 产品专有术语表

### 10. 品牌语调
- 语气（专业、随意、活泼等）
- 沟通风格（直接、对话式、技术型）
- 品牌个性（3-5 个形容词）

### 11. 信任证据
- 可引用的关键指标或成果
- 知名客户/Logo
- 客户证言片段
- 核心价值主题及支撑证据

### 12. 目标
- 主要业务目标
- 关键转化动作（你希望用户做什么）
- 当前指标（如已知）

---

## 步骤三：创建文档

收集完信息后，创建 `.agents/product-marketing-context.md`，结构如下：

```markdown
# Product Marketing Context

*Last updated: [date]*

## Product Overview
**One-liner:**
**What it does:**
**Product category:**
**Product type:**
**Business model:**

## Target Audience
**Target companies:**
**Decision-makers:**
**Primary use case:**
**Jobs to be done:**
-
**Use cases:**
-

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| | | | |

## Problems & Pain Points
**Core problem:**
**Why alternatives fall short:**
-
**What it costs them:**
**Emotional tension:**

## Competitive Landscape
**Direct:** [Competitor] — falls short because...
**Secondary:** [Approach] — falls short because...
**Indirect:** [Alternative] — falls short because...

## Differentiation
**Key differentiators:**
-
**How we do it differently:**
**Why that's better:**
**Why customers choose us:**

## Objections
| Objection | Response |
|-----------|----------|
| | |

**Anti-persona:**

## Switching Dynamics
**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Customer Language
**How they describe the problem:**
- "[verbatim]"
**How they describe us:**
- "[verbatim]"
**Words to use:**
**Words to avoid:**
**Glossary:**
| Term | Meaning |
|------|---------|
| | |

## Brand Voice
**Tone:**
**Style:**
**Personality:**

## Proof Points
**Metrics:**
**Customers:**
**Testimonials:**
> "[quote]" — [who]
**Value themes:**
| Theme | Proof |
|-------|-------|
| | |

## Goals
**Business goal:**
**Conversion action:**
**Current metrics:**
```

---

## 步骤四：确认并保存

- 展示完成的文档
- 询问是否需要调整
- 保存到 `.agents/product-marketing-context.md`
- 告知用户："其他营销技能现在会自动使用这个上下文。随时运行 `/product-marketing-context` 来更新它。"

---

## 技巧

- **具体化**：问"是什么样的挫败感让他们来找你？"而不是"他们要解决什么问题？"
- **收集原话**：客户的真实语言比润色后的描述更有力量
- **要例子**："能举个例子吗？"能引出更好的回答
- **边做边确认**：每个章节总结一遍再继续
- **跳过不适用的**：不是每个产品都需要所有章节（比如 B2C 不需要用户画像）

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清。
