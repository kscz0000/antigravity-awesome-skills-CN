---
name: examprep-ai
description: "备考助手，可将教学大纲、往年试题或笔记转化为按优先级排序的高分路线图。涵盖理论、计算题、选择题、编程题和实验备考，按 易→中→难 排序。用于最后冲刺复习、重点梳理和考点预测。触发词：考试备考、高分路线、考点预测、复习冲刺、刷题、考前突击。"
risk: safe
source: community
date_added: "2026-06-05"
allowed-tools: Read, Glob, Grep
author: WHOISABHISHEKADHIKARI
user-invokable: true
tags:
  - education
  - exam-prep
  - study-guide
  - question-prediction
  - syllabus-analysis
  - revision
  - students
---

# 考试备考 AI

## 适用场景

在以下情况下使用此技能：
- 将教学大纲、往年试题或学习笔记转化为按优先级排序的路线图。
- 聚焦特定类型的考试题（理论、计算题、选择题、编程题、实验题）。
- 创建记忆卡片、预测试卷，或检查整体备考情况。
- 进行最后冲刺复习，或深入钻研重要考点。

## 🎯 选择性阅读规则 — 仅阅读与请求匹配的章节

| 学生提问内容 | 跳转目标 |
|--------------------------|---------|
| 完整路线图 / "该学什么" / 已上传教学大纲 + 往年试题 | [完整路线图模式](#完整路线图模式) |
| 仅理论题 / 定义 / 解释 | [理论笔记](#理论笔记) |
| 计算题 / 推导题 | [计算笔记](#计算笔记) |
| 选择题 / 判断题 / 客观题练习 | [选择题笔记](#选择题笔记) |
| 编程题 / 算法 / 跟踪 / 调试 | [编程笔记](#编程笔记) |
| 实验题 / 实践 / 口试备考 | [实验笔记](#实验笔记) |
| 仅需要记忆卡片 | [记忆卡片](#记忆卡片) |
| 模拟试卷 | [预测试卷](#预测试卷) |
| 备考情况检查 / 分数预估 | [考试就绪度仪表板](#考试就绪度仪表板) |

**规则：** 阅读匹配的章节以及 [共享基础](#共享基础) 块。
跳过其余内容。对于聚焦型请求，不要加载所有章节。

---

## 共享基础

> 每个请求都要加载此块。它体量小且始终需要。

### 难度量表（通用）

| 级别 | 关键词 | 学习目标 |
|-------|-------------|--------------|
| 🟩 易 | 定义、陈述、列举、命名、识别、什么是 | 保底分 — 优先攻克 |
| 🟨 中 | 解释、描述、比较、计算、实现、跟踪 | 试卷中段分 |
| 🟥 难 | 推导、证明、优化、分析、评价、设计、为什么 | 拉开差距的题 — 最后攻克 |

**顺序规则：** 始终按 易→中→难 呈现。绝不可颠倒。

### 收集信息（只问一次，然后继续）

1. 至少收集以下一项：教学大纲、往年试题、笔记，或科目名 + 高校名称。
2. 若 OCR 置信度 < 80%，需确认课程代码：*"我识别到 [X] — 是否正确？"*
3. 询问可用时间。若无回答 → 默认 **标准模式（6–12 小时）** 并说明假设。

### 学习模式

| 模式 | 时间 | 负载 |
|------|------|------|
| 🚨 应急模式 | 1–2 小时 | 仅 🟩 易，TOP 10 题 |
| ⚡ 冲刺模式 | 3–5 小时 | 🟩 + 🟨，TOP 25 题 |
| 📚 标准模式 *（默认）* | 6–12 小时 | 全难度，完整路线图 |
| 🗓️ 提前模式 | 数天以上 | 每日计划 + 模拟卷 |

### 教学大纲护栏

- 将每道题映射到教学大纲的某个单元（≥ 70% 匹配 → `[IN SYLLABUS]`）。
- 绝不为教学大纲中未涉及的主题生成内容。
- 超出大纲范围的内容 → 标记，并在加入前询问学生。

### 概率分数

```
Score = (Frequency × 0.40) + (Recency × 0.30) + (Unit Weight × 0.20) + (Marks × 0.10)
```
- Frequency（频次）：出现次数 ÷ 最大出现次数 × 100
- Recency（时效）：近 2 年 = 100 · 3–4 年 = 60 · 更早 = 30
- Unit Weight（单元权重）：核心 = 100 · 选修 = 50
- Marks（分值）：10+ = 100 · 5–9 = 60 · 2–4 = 30 · 选择题 = 20

## 局限性

- 本技能支持学习规划和复习，但不能保证考试题、
  分数、评分结果或教师的预期。
- 概率分数是基于所提供教学大纲、笔记和往年
  试题得出的启发式估计；输入稀疏、过时或不完整会降低可靠性。
- 本技能不应捏造大纲覆盖。若原始资料
  缺失、含糊或超出范围，应在添加预测内容之前请学生确认。
- 它不能替代官方课程指导、无障碍
  便利措施、学术诚信政策或教师反馈。
- 除当前复习任务所需的学习资料外，
  不得请求或处理学生的私人记录。

---

## 完整路线图模式

> 适用场景：学生上传教学大纲 + 往年试题，或询问"我该学什么？"

**步骤 1 — 抽取。** 提取所有题目；标注每题的年份/来源。
确认：*"已从 [M] 份试卷中为 [课程] 抽取 [N] 道题。统计：📝[A] 🔢[B] 🔘[C] 💻[D] 🧪[E]。是否继续？"*

**步骤 2 — 分类 + 难度标注。** 使用五类题型表：

| 题型 | 识别依据 |
|------|------------|
| 📝 理论 | 定义、解释、讨论、比较、辨析 |
| 🔢 计算 | 计算、求解、推导、证明、题目中有数字 |
| 🔘 选择/判断 | 列出选项、"对或错"、"下列哪项" |
| 💻 编程 | 编写程序、实现、跟踪输出、算法、流程图 |
| 🧪 实验 | 实验、步骤、现象、目的、器材、口试 |

**步骤 3 — 构建排序表（每类一张）：**

```
| # | Question | Times | Marks | Difficulty | Unit | Priority |
|---|----------|-------|-------|------------|------|----------|
| 1 | [question text] | [N]× | [X] | 🟩/🟨/🟥 | Unit [X] | 🔥 Must / ✅ Do |
```

**步骤 4 — 生成笔记** 使用下方匹配的题型章节。
顺序：先完成所有题型的"易"，再"中"，再"难"。

**步骤 5 — 覆盖追踪器：**
```
Unit 1: [Name]  →  📝✅  🔢✅  🔘⚠️ PREDICTED  💻—  🧪—
Legend: ✅ past paper  ⚠️ predicted  — not applicable
```
对于任何空白：生成一道预测题 + 笔记，标记 `[PREDICTED — not from past papers]`。

**步骤 6 — 提供选择：** *"您需要 (a) 记忆卡片，(b) 预测试卷，还是 (c) 就绪度仪表板？"*

---

## 理论笔记

> 适用场景：学生询问定义、解释、简答题。

**🟩 易 — 定义 / 列举（30 秒）**
```
📝🟩 [Question] | [N]× | [X] marks
─────────────────────────────────
ANSWER: [2–4 bullets max]
KEY TERM: [single most important word]
MEMORY HOOK: [one-liner trick]
```

**🟨 中 — 解释 / 比较（2 分钟）**
```
📝🟨 [Question] | [N]× | [X] marks
─────────────────────────────────
DEFINITION: [1 sentence]
MAIN POINTS: • P1 • P2 • P3 • P4
DIAGRAM: [text description — student sketches from this]
EXAM TIP: [what examiner rewards]
```

**🟥 难 — 讨论 / 评价（5 分钟阅读 · 10 分钟作答）**
```
📝🟥 [Question] | [N]× | [X] marks | Unit [X]
─────────────────────────────────────────────
INTRO: [2–3 sentences]
SECTION 1 — [subtopic]: • point • point
SECTION 2 — [subtopic]: • point • point
SECTION 3 — [subtopic]: • point • point
DIAGRAM: [sketch description]
CONCLUSION: [1–2 lines]
MARKS HINT: Intro ~2 · each section ~3 · diagram ~2 · conclusion ~1
MEMORY: [acronym or order trick]
```

---

## 计算笔记

> 适用场景：学生询问计算题、推导题、公式。

**🟩 易 — 直接套公式**
```
🔢🟩 [Problem Type] | [N]× | [X] marks
──────────────────────────────────────
FORMULA:        [clearly written]
GIVEN → FIND:   [what's given / what to find]
WORKED EXAMPLE:
  Step 1: [substitute]
  Step 2: [calculate]
  Answer: [result + unit]
COMMON MISTAKE: [the one error students make]
MEMORY HOOK:    [how to remember formula]
```

**🟨 中 — 多步带条件**
```
🔢🟨 [Problem Type] | [N]× | [X] marks
──────────────────────────────────────
FORMULA(S): [all needed]
APPROACH:   [which formula when — decision rule]
WORKED EXAMPLE:
  Step 1: [setup / draw table]
  Step 2: [apply condition]
  Step 3: [calculate]
  Step 4: [verify / interpret]
  Answer: [result]
WATCH OUT:  [condition that trips students]
EXAM TIP:   [show working — marks for method too]
```

**🟥 难 — 推导 / 证明**
```
🔢🟥 [Problem / Derivation] | [N]× | [X] marks
───────────────────────────────────────────────
PREREQUISITES: [what student must know first]
DERIVATION:
  Step 1: [first principles]
  Step 2: [key transformation]
  ...Final: [result / QED]
WORKED EXAMPLE: [concrete numbers applied]
MARKS BREAKDOWN: [method marks vs answer marks]
COMMON ERRORS: [2–3 errors that lose marks]
```

---

## 选择题笔记

> 适用场景：学生需要选择题练习、判断题、客观题。

**🟩 易 — 记忆**
```
🔘🟩 [Question] | [N]×
──────────────────────
CORRECT: [option + text]
WHY CORRECT: [one sentence]
WHY OTHERS WRONG: • A: ... • B: ... • C: ...
KEY FACT: [the one thing this tests]
```

**🟨 中 — 应用**
```
🔘🟨 [Question] | [N]×
──────────────────────
CORRECT: [option + text]
REASONING: [identify concept] → [apply rule] → [eliminate wrong]
TRAP: [why students pick the wrong answer]
```

**🟥 难 — 陷阱 / 边界情况**
```
🔘🟥 [Question] | [N]×
──────────────────────
CORRECT: [option + text]
WHY TRICKY: [what assumption is exploited]
ELIMINATE: • Drop [A]: [reason] • Drop [B]: [reason] • Keep [C]: [reason]
RULE: [the precise rule that settles this type]
```

---

## 编程笔记

> 适用场景：学生需要编写程序、跟踪输出、实现算法、调试。

**🟩 易 — 语法 / 模式回忆**
```
💻🟩 [Task] | [N]× | [X] marks
────────────────────────────────
PATTERN:     [algorithm/structure name]
TEMPLATE:    [minimal working skeleton — pseudocode or language-specific]
KEY LINES:   [1–2 lines examiner looks for]
MEMORY HOOK: [how to recall under pressure]
```

**🟨 中 — 逻辑构建**
```
💻🟨 [Task] | [N]× | [X] marks
────────────────────────────────
APPROACH:
  1. [sub-tasks]  2. [data structures]  3. [step-by-step logic]
ANNOTATED CODE: [code with inline comments]
EDGE CASES:  [inputs needing special handling]
EXAM TIP:    [comment code — examiners reward clarity]
```

**🟥 难 — 优化 / 跟踪 / 调试**
```
💻🟥 [Task] | [N]× | [X] marks | TYPE: [Optimize / Trace / Debug]
──────────────────────────────────────────────────────────────────
TRACE →   Input | Trace Table (Iter · VarA · VarB · Output) | Final Output
OPTIMIZE → Naive O(?) → Optimized O(?) | Key Insight: [what enables it]
DEBUG →   Bug Location | Bug Type | Fix | Why it works
```

---

## 实验笔记

> 适用场景：学生询问实验、步骤、现象、口试备考。

**🟩 易 — 命名 / 识别**
```
🧪🟩 [Experiment] | [N]×
─────────────────────────
AIM:      [one sentence]
APPARATUS: [bullet list]
RESULT:   [expected outcome to state]
KEY TERM: [most important term]
```

**🟨 中 — 编写步骤**
```
🧪🟨 [Experiment] | [N]×
─────────────────────────
AIM / APPARATUS: [brief]
PROCEDURE: Step 1 → Step 2 → Step 3 → Step 4
OBS TABLE: [column headers + example row]
RESULT:    [how to state conclusion]
PRECAUTIONS: [2–3 points examiners look for]
```

**🟥 难 — 分析 / 口试**
```
🧪🟥 [Experiment] | [N]×
─────────────────────────
ANALYSIS: • result in context • formula used • source of error
VIVA:
  Q1: [question]  A: [2–3 sentence answer]
  Q2: [question]  A: [2–3 sentence answer]
  Q3: [question]  A: [2–3 sentence answer]
EXAM TIP: [what viva examiner always asks]
```

---

## 记忆卡片

> 适用场景：学生需要记忆卡片或快速回忆卡。

每个题目一张卡：
```
[TYPE EMOJI][DIFFICULTY EMOJI]
Q: [question]
A: [answer in 1–2 lines]
Key: [formula / term / pattern — if applicable]
```

---

## 预测试卷

> 适用场景：学生需要模拟卷或练习测试。

生成一份涵盖所有题型的试卷。每道题标注题型 + 难度。

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI PREDICTION — Not official. For practice only.
Course: [Name]  |  Total Marks: [X]  |  Time: [X] hrs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECTION A — Short / Objective  [🟩 Easy]
  [MCQ / T-F / 1-mark definitions]

SECTION B — Medium Answer      [🟨 Medium]
  [Theory explanations + medium numericals]

SECTION C — Long Answer        [🟥 Hard]
  [Long theory + derivations + coding]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 考试就绪度仪表板

> 适用场景：学生询问分数预估或就绪度检查。

```
📊 EXAM READINESS
──────────────────────────────────────────────────────
TYPE          EASY    MEDIUM   HARD    OVERALL
📝 Theory     [X]%    [X]%     [X]%    [X]%
🔢 Numerical  [X]%    [X]%     [X]%    [X]%
🔘 MCQ/T-F    [X]%    [X]%     [X]%    [X]%
💻 Coding     [X]%    [X]%     [X]%    [X]%
🧪 Lab        [X]%    [X]%     [X]%    [X]%
──────────────────────────────────────────────────────
PREPAREDNESS  : [X]%
MARKS RANGE   : [Low]–[High] out of [Total]
──────────────────────────────────────────────────────
STRONG        : [types + topics]
WEAK → FOCUS  : [types + topics]
──────────────────────────────────────────────────────
Confidence: [High/Medium/Low]  |  Based on: [N] papers
```

---

## 应用示例

> 演示技能的具体前后效果。

**输入：**
> "我明天有操作系统考试。这是教学大纲 [粘贴] 和 3 份往年试题 [上传]。我有 4 小时。"

**技能路由：** 完整路线图模式 → 冲刺模式（3–5 小时）

**输出顺序：**
1. 抽取确认：*"已从 3 份试卷中为操作系统（CSC-207）抽取 47 道题。统计：📝18 🔢12 🔘10 💻7 🧪0。是否继续？"*
2. 所有题型的排序表，仅 易→中（冲刺模式跳过 难，每单元最多 1 道）
3. TOP 25 题的笔记 — 先做所有题型的 易，再做 中
4. 覆盖追踪器，显示已覆盖的单元
5. 提供：记忆卡片、模拟卷或仪表板

---

## 质量检查（每次输出前运行）

| 检查项 | 规则 |
|-------|------|
| 大纲符合性 | 每条笔记对应大纲的某个单元 |
| 难度顺序 | 易 在 中 之前，中 在 难 之前 — 绝不可颠倒 |
| 计算准确性 | 例题计算结果正确 |
| 代码有效性 | 代码片段语法正确 |
| 笔记长度 | 每条笔记可在 ≤ 2–5 分钟内阅读完毕 |
| 无幻觉 | 不包含所上传资料中未涉及的事实 |
| 课程代码已确认 | OCR 识别出的代码已由学生核实 |

---

## 错误响应

| 情况 | 回应 |
|-----------|-----|
| 无教学大纲 | "没有教学大纲我无法保证笔记紧扣考点。请将单元列表以文本形式粘贴？" |
| 仅 1 份往年试题 | "只有 1 份试卷 = 预测置信度较低。试卷越多 = 准确度越高。" |
| OCR 失败 | "部分图片无法识别。能否重新输入这些题目？" |
| 超出大纲范围的题目 | "这与您的教学大纲不匹配 — 已跳过。需要我强制纳入吗？" |
| 混合科目 | "发现来自两个科目的题目。是否分开处理？" |
| 未提供时间 | "默认采用标准模式（6–12 小时）。若有更少时间请告知。" |
| 未找到计算题/编程题 | "未找到计算题/编程题。如果您的考试包含这些题型，请提供含有它们的试卷。"