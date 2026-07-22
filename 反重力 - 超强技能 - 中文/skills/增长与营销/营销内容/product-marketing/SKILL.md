---
name: product-marketing
description: 当用户想要创建或更新产品营销上下文文档时使用。也在用户提到"产品上下文"、"营销上下文"、"设置上下文"、"定位"、"我的目标受众是谁"、"描述我的产品"、"ICP"、"理想客户画像"或想要……时使用
risk: unknown
source: https://github.com/coreyhaines31/marketingskills/tree/main/skills/product-marketing
source_repo: coreyhaines31/marketingskills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/coreyhaines31/marketingskills/blob/main/LICENSE
---

# 产品营销上下文
## 何时使用

当用户想要创建或更新其产品营销上下文文档时使用此技能。也在用户提到"产品上下文"、"营销上下文"、"设置上下文"、"定位"、"我的目标受众是谁"、"描述我的产品"、"ICP"、"理想客户画像"或想要……时使用。


你帮助用户创建和维护产品营销上下文文档。该文档捕获基础的定位和消息信息，供其他营销技能引用，从而避免用户重复输入。

文档存储在 `.agents/product-marketing.md`。

## 工作流

### 步骤 1：检查已有上下文

首先，检查 `.agents/product-marketing.md` 是否已存在。同时检查 `.claude/product-marketing.md` 和旧版文件名 `product-marketing-context.md`（位于 `.agents/` 或 `.claude/` 中）——如果在 `.agents/product-marketing.md` 之外的位置找到了，提议将其迁移到规范位置。

**如果已存在：**
- 读取并概述已捕获的内容
- 询问用户想更新哪些章节
- 仅收集这些章节的信息

**如果不存在，提供两个选项：**

1. **从代码库自动起草**（推荐）：你将研究仓库——README、落地页、营销文案、package.json 等——并起草上下文文档的 V1 版本。用户随后审阅、纠正并补充缺失部分。这比从零开始更快。

2. **从零开始**：以对话方式逐个章节收集信息。

大多数用户偏好选项 1。展示草稿后，询问："有什么需要纠正的？有什么遗漏的？"

### 步骤 2：收集信息

**如果是自动起草：**
1. 阅读代码库：README、落地页、营销文案、关于页面、meta 描述、package.json、任何已有文档
2. 根据发现的内容起草所有章节
3. 展示草稿并询问有什么需要纠正或遗漏的
4. 迭代直到用户满意

**如果从零开始：**
以对话方式逐个章节推进以下各节。不要一次性抛出所有问题。

对每个章节：
1. 简要说明你正在捕获什么
2. 提出相关问题
3. 确认准确性
4. 进入下一个

追问客户的原话表达——确切措辞比精炼描述更有价值，因为它们反映了客户实际的思维和表达方式，使文案更具共鸣。

---

## 需捕获的章节

### 1. 产品概览
- 一句话描述
- 产品功能（2-3 句话）
- 产品类别（你所在的"货架"——客户如何搜索你）
- 产品类型（SaaS、市场平台、电商、服务等）
- 商业模式和定价

### 2. 目标受众
- 目标公司类型（行业、规模、阶段）
- 目标决策者（角色、部门）
- 主要使用场景（你解决的核心问题）
- 待完成使命（客户"雇佣"你的 2-3 件事）
- 具体使用场景或场景描述

### 3. 人物画像（仅限 B2B）
如果涉及多个利益相关者参与购买，为每个角色捕获：
- 用户、推动者、决策者、财务审批者、技术影响者
- 每个角色关心什么、面临的挑战、你承诺的价值

### 4. 问题与痛点
- 客户在找到你之前面临的核心挑战
- 为什么现有方案不够好
- 代价是什么（时间、金钱、机会）
- 情绪压力（焦虑、恐惧、怀疑）

### 5. 竞争格局
- **直接竞争对手**：相同方案、相同问题（如 Calendly vs SavvyCal）
- **次级竞争对手**：不同方案、相同问题（如 Calendly vs Superhuman 排期功能）
- **间接竞争对手**：冲突的解决路径（如 Calendly vs 私人助理）
- 每个竞争对手对客户的不足之处

### 6. 差异化
- 关键差异化优势（竞品缺乏的能力）
- 你如何以不同方式解决问题
- 为什么这样更好（收益）
- 客户为什么选择你而非竞品

### 7. 异议与反画像
- 销售中听到的前 3 个异议及应对方式
- 谁不适合你（反画像）

### 8. 切换动态
JTBD 四力模型：
- **推力**：什么挫败感驱使他们离开当前方案
- **拉力**：什么吸引他们走向你
- **惯性**：什么让他们困在当前方案
- **焦虑**：什么让他们对切换感到担忧

### 9. 客户语言
- 客户如何描述问题（原话）
- 客户如何描述你的方案（原话）
- 应使用的词语/短语
- 应避免的词语/短语
- 产品专属术语表

### 10. 品牌语调
- 语气（专业、随和、俏皮等）
- 沟通风格（直接、对话式、技术性）
- 品牌个性（3-5 个形容词）

### 11. 证据要点
- 需引用的关键指标或结果
- 知名客户/品牌标识
- 客户评价摘录
- 核心价值主题及支撑证据

### 12. 目标
- 主要业务目标
- 关键转化行为（你希望用户做什么）
- 当前指标（如已知）

---

## 步骤 3：创建文档

收集信息后，创建 `.agents/product-marketing.md`，结构如下：

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

## 步骤 4：确认并保存

- 展示完成的文档
- 询问是否需要调整
- 保存到 `.agents/product-marketing.md`
- 告知用户："其他营销技能现在会自动使用此上下文。随时运行 `/product-marketing` 来更新它。"

---

## 提示

- **要具体**：问"什么挫折是让他们找到你的第一原因？"而不是"他们解决什么问题？"
- **捕获原话**：客户语言胜过精炼描述
- **追问示例**："能举个例子吗？"能解锁更好的回答
- **边做边验证**：每个章节完成后总结并确认再继续
- **跳过不适用的部分**：并非每个产品都需要所有章节（如 B2C 不需要人物画像）

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性/高成本操作的审批。
