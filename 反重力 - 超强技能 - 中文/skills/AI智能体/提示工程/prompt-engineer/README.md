# 🎯 Prompt Engineer

**版本：** 1.0.1  
**状态：** ✨ 零配置 | 🌍 通用

将原始提示词转化为优化的、可直接使用的提示词，支持 11 种成熟的提示词框架。

---

## 📋 概览

**Prompt Engineer** 是一个智能 AI 技能，能分析你的意图并自动生成优化的提示词，适用于 Claude、ChatGPT 或任何其他 AI 模型。不用再纠结怎么措辞复杂请求——只需描述你想要什么，剩下的交给技能处理。

本技能以**"魔法模式"**运行——静默工作，仅在绝对必要时才提问。你提供一个粗略想法，它返回一个打磨好的、结构化的提示词，可以直接使用。

### ✨ 核心特性

- **🎯 意图分析：** 理解你想要完成什么
- **🧠 11 种框架：** RTF、Chain of Thought、RISEN、RODES、Chain of Density、RACE、RISE、STAR、SOAP、CLEAR、GROW
- **🔄 框架混合：** 需要时组合多个框架
- **❓ 智能澄清：** 仅在关键缺失时才提问
- **📏 自适应输出：** 提示词长度匹配任务复杂度
- **🌍 通用：** 适用于任何项目、任何终端环境
- **🪄 魔法模式：** 不做技术解释——只给结果

---

## 🚀 快速开始

### 调用技能

使用以下任一触发短语：

```bash
copilot> improve this prompt: [your rough prompt]
copilot> optimize prompt: [your idea]
copilot> refine prompt: [what you want]
copilot> prompt engineering for: [task description]
copilot> transform into prompt: [concept]
copilot> create prompt for: [goal]
```

### 示例 1：简单任务

**输入：**
```bash
copilot> improve this prompt: help me write Python code
```

**技能提问：**
```
What type of Python code do you need?
- [ ] Data analysis
- [ ] Web scraping
- [ ] Task automation
- [ ] API/backend development
```

**你选择：** "Web scraping"

**输出：**
````markdown
```
You are a Python developer expert in web scraping.

Task: Create a Python script to scrape data from [specify target website].

Requirements:
- Use BeautifulSoup or Scrapy
- Implement pagination and rate limiting
- Store data in structured format (CSV or JSON)
- Include error handling for network issues

Output format: Complete, commented Python code with usage examples.
```
````

---

### 示例 2：复杂任务（无需澄清）

**输入：**
```bash
copilot> create prompt for: product recommendation system with purchase history and market trends
```

**输出：**
````markdown
```
Role: You are a senior machine learning engineer specializing in recommendation systems.

Objective: Design a product recommendation system that combines user purchase history, preferences, and market trends.

Details:
- Input data sources: user transaction logs, preference surveys, market trend APIs
- Algorithm considerations: collaborative filtering, content-based filtering, hybrid approaches
- Performance metrics: precision, recall, diversity, novelty
- Scalability: system must handle 100k+ users

Approach step-by-step:
1. Analyze the three data sources and their relationships
2. Propose 2-3 algorithm approaches with trade-offs
3. Design data pipeline architecture
4. Define evaluation metrics
5. Outline implementation roadmap

Examples: Show pseudocode for core recommendation logic

Sense Check: Validate that the solution balances personalization with discovery and scales to production.

Output format: Technical design document with architecture diagrams and implementation roadmap.
```
````

---

### 示例 3：模糊任务（技能主动澄清）

**输入：**
```bash
copilot> transform into prompt: I want to improve my process
```

**技能提问：**
```
What process do you want to improve?
- [ ] Work/productivity process
- [ ] Learning process
- [ ] Technical process (development, deployment, etc.)
```

**你选择：** "Work process"

**技能提问：**
```
What specific aspect?
- [ ] Time management
- [ ] Team collaboration
- [ ] Decision making
```

**你选择：** "Decision making"

**输出：**
````markdown
```
Context: I struggle with making decisions quickly and effectively at work.

Objective: Develop a structured framework to improve decision speed and quality.

Current Reality:
- Decisions delayed by excessive analysis
- Lack of clear criteria
- Uncertainty about when to decide vs. gather information

Desired Outcome:
- Consistent decision-making framework
- Clear criteria for different decision types
- Reduced decision fatigue

Your task:
1. Assess current patterns and identify bottlenecks
2. Propose framework (Eisenhower Matrix, RAPID, Decision Tree)
3. Create decision criteria templates
4. Design tracking and iteration process

Output format: Practical playbook with templates, examples, and metrics.
```
````

---

## 📚 支持的框架

**Prompt Engineer** 技能使用 **11 种成熟框架**来优化你的提示词。技能会根据你的任务自动选择和混合这些框架——你无需了解或手动选择。

---

### 1. **RTF (Role-Task-Format)**

**结构：** 角色 → 任务 → 格式

**适用场景：** 需要特定专业视角的任务

**组成要素：**
- **角色：** "你是一位 [专家身份]"
- **任务：** "你的任务是 [具体操作]"
- **格式：** "输出格式：[结构/风格]"

**示例：**
```
You are a senior Python developer.
Task: Refactor this code for better performance.
Format: Provide refactored code with inline comments explaining changes.
```

---

### 2. **Chain of Thought**

**结构：** 问题 → 步骤 1 → 步骤 2 → ... → 解决方案

**适用场景：** 复杂推理、调试、数学问题、逻辑谜题

**组成要素：**
- 将问题拆分为顺序步骤
- 展示每个阶段的推理过程
- 逐步构建最终解决方案

**示例：**
```
Solve this problem step-by-step:
1. Identify the core issue
2. Analyze contributing factors
3. Propose solution approach
4. Validate solution against requirements
```

---

### 3. **RISEN**

**结构：** 角色、指令、步骤、最终目标、约束范围

**适用场景：** 有明确交付物和约束的多阶段项目

**组成要素：**
- **角色：** 专家身份
- **指令：** 做什么
- **步骤：** 顺序执行的操作
- **最终目标：** 期望结果
- **约束范围：** 限制和聚焦领域

**示例：**
```
Role: You are a DevOps architect.
Instructions: Design a CI/CD pipeline for microservices.
Steps: 1) Analyze requirements 2) Select tools 3) Design workflow 4) Document
End goal: Automated deployment with zero-downtime releases.
Narrowing: Focus on AWS, limit to 3 environments (dev/staging/prod).
```

---

### 4. **RODES**

**结构：** 角色、目标、细节、示例、合理性检查

**适用场景：** 复杂设计、系统架构、研究提案

**组成要素：**
- **角色：** 专家视角
- **目标：** 要达成什么
- **细节：** 上下文和需求
- **示例：** 具体说明
- **合理性检查：** 验证标准

**示例：**
```
Role: You are a system architect.
Objective: Design a scalable e-commerce platform.
Details: Handle 100k concurrent users, sub-200ms response time, multi-region.
Examples: Show database schema, caching strategy, load balancing.
Sense check: Validate solution meets latency and scalability requirements.
```

---

### 5. **Chain of Density**

**结构：** 第 1 次迭代（冗长）→ 第 2 次 → ... → 第 5 次迭代（最高密度）

**适用场景：** 总结、压缩、综合长内容

**流程：**
- 从冗长解释开始
- 迭代压缩，同时保留关键信息
- 以最高密度版本结束（每词信息量最大）

**示例：**
```
Compress this article into progressively denser summaries:
1. Initial summary (300 words)
2. Compressed (200 words)
3. Further compressed (100 words)
4. Dense (50 words)
5. Maximum density (25 words, all critical points)
```

---

### 6. **RACE**

**结构：** 角色、受众、上下文、期望

**适用场景：** 沟通表达、演示汇报、利益相关者更新、叙事

**组成要素：**
- **角色：** 沟通者身份
- **受众：** 你在对谁说（专业水平、关注点）
- **上下文：** 背景/情境
- **期望：** 受众需要知道或做什么

**示例：**
```
Role: You are a product manager.
Audience: Non-technical executives.
Context: Quarterly business review, product performance down 5%.
Expectation: Explain root causes and recovery plan in non-technical terms.
```

---

### 7. **RISE**

**结构：** 研究、调查、综合、评估

**适用场景：** 分析、调查、系统化探索、诊断工作

**流程：**
1. **研究：** 收集信息
2. **调查：** 深入分析发现
3. **综合：** 整合洞察
4. **评估：** 评估并提出建议

**示例：**
```
Analyze customer churn data using RISE:
Research: Collect churn metrics, exit surveys, support tickets.
Investigate: Identify patterns in churned users.
Synthesize: Combine findings into themes.
Evaluate: Recommend retention strategies based on evidence.
```

---

### 8. **STAR**

**结构：** 情境、任务、行动、结果

**适用场景：** 带丰富上下文的问题解决、案例研究、回顾复盘

**组成要素：**
- **情境：** 背景上下文
- **任务：** 具体挑战
- **行动：** 需要做什么
- **结果：** 期望产出

**示例：**
```
Situation: Legacy monolith causing deployment delays (2 weeks per release).
Task: Modernize architecture to enable daily deployments.
Action: Migrate to microservices, implement CI/CD, containerize.
Result: Deploy 10+ times per day with <5% rollback rate.
```

---

### 9. **SOAP**

**结构：** 主观、客观、评估、计划

**适用场景：** 结构化文档记录、医疗档案、技术日志、事故报告

**组成要素：**
- **主观：** 报告的信息（症状、投诉）
- **客观：** 可观察的事实（指标、数据）
- **评估：** 分析和诊断
- **计划：** 建议行动

**示例：**
```
Incident Report (SOAP):
Subjective: Users report slow page loads starting 10 AM.
Objective: Average response time increased from 200ms to 3s. CPU at 95%.
Assessment: Database connection pool exhausted due to traffic spike.
Plan: 1) Scale pool size 2) Add monitoring alerts 3) Review query performance.
```

---

### 10. **CLEAR**

**结构：** 协作性、有限性、情感性、可衡量性、可迭代性

**适用场景：** 目标设定、OKR、可衡量目标、团队对齐

**组成要素：**
- **协作性：** 谁参与
- **有限性：** 范围边界（时间、资源）
- **情感性：** 为什么重要（动力）
- **可衡量性：** 可量化的进度指标
- **可迭代性：** 如何迭代改进

**示例：**
```
Q1 Objective (CLEAR):
Collaborative: Engineering + Product teams.
Limited: Complete by March 31, budget $50k, 2 engineers allocated.
Emotional: Reduces customer support load by 30%, improves satisfaction.
Appreciable: Track weekly via tickets resolved, NPS score, deployment count.
Refinable: Bi-weekly retrospectives, adjust priorities based on feedback.
```

---

### 11. **GROW**

**结构：** 目标、现状、选项、意愿

**适用场景：** 辅导、个人发展、成长规划、导师指导

**组成要素：**
- **目标：** 要达成什么
- **现状：** 当前情况（优势、差距）
- **选项：** 可能的方法
- **意愿：** 行动承诺

**示例：**
```
Career Development (GROW):
Goal: Become senior engineer within 12 months.
Reality: Strong coding skills, weak in system design and leadership.
Options: 1) Take system design course 2) Lead a project 3) Find mentor.
Will: Commit to 5 hours/week study, lead Q2 project, find mentor by Feb.
```

---

### 框架选择逻辑

技能会分析你的输入并：

1. **检测任务类型**
   - 编码、写作、分析、设计、沟通等

2. **识别复杂度**
   - 简单（1-2 句话）→ 快速、最少结构
   - 中等（一个段落）→ 标准框架
   - 复杂（详细需求）→ 高级框架或混合

3. **选择主框架**
   - RTF → 角色扮演任务
   - Chain of Thought → 逐步推理
   - RISEN/RODES → 复杂项目
   - RACE → 沟通表达
   - STAR → 情境化问题
   - 以此类推...

4. **需要时混合辅助框架**
   - RODES + Chain of Thought → 复杂技术项目
   - CLEAR + GROW → 领导力目标
   - RACE + STAR → 策略性沟通

**你永远不需要手动选择框架** —— 技能在"魔法模式"下自动完成。

---

### 常见框架混合

| 任务类型 | 主框架 | 混合框架 | 效果 |
|-----------|------------------|--------------|--------|
| 复杂技术设计 | RODES | Chain of Thought | 结构化设计 + 逐步推理 |
| 领导力发展 | CLEAR | GROW | 可衡量目标 + 行动承诺 |
| 策略性沟通 | RACE | STAR | 受众感知叙事 + 上下文 |
| 事故调查 | RISE | SOAP | 系统化分析 + 结构化文档 |
| 项目规划 | RISEN | RTF | 多阶段交付 + 角色清晰 |

---

## 🎯 工作原理

```
用户输入（粗略提示词）
         ↓
┌────────────────────────┐
│ 1. 分析意图            │  用户想做什么？
│    - 任务类型           │  编码？写作？分析？设计？
│    - 复杂度             │  简单、中等、复杂？
│    - 清晰度             │  明确还是模糊？
└────────┬───────────────┘
         ↓
┌────────────────────────┐
│ 2. 澄清（可选）        │  仅在关键缺失时
│    - 提 2-3 个问题      │  尽量用选择题
│    - 补充缺失信息       │  
└────────┬───────────────┘
         ↓
┌────────────────────────┐
│ 3. 选择框架            │  静默选择
│    - 任务 → 框架映射
│    - 需要时混合         │
└────────┬───────────────┘
         ↓
┌────────────────────────┐
│ 4. 生成提示词          │  应用框架规则
│    - 添加角色/上下文    │  
│    - 结构化任务         │  
│    - 定义格式           │
│    - 添加示例           │
└────────┬───────────────┘
         ↓
┌────────────────────────┐
│ 5. 输出                │  整洁、可复制
│    Markdown 代码块      │  无解释
└────────────────────────┘
```

---

## 🎨 使用场景

### 编码

```bash
copilot> optimize prompt: create REST API in Python
```

→ 生成带角色、需求、输出格式、示例的结构化提示词

---

### 写作

```bash
copilot> create prompt for: write technical article about microservices
```

→ 生成带受众感知、结构、语气和内容指南的提示词

---

### 分析

```bash
copilot> refine prompt: analyze sales data and identify trends
```

→ 生成带可视化需求的逐步分析框架

---

### 决策

```bash
copilot> improve this prompt: I need to decide between technology A and B
```

→ 生成带标准、权衡和验证的决策框架

---

### 学习

```bash
copilot> transform into prompt: learn machine learning from zero
```

→ 生成带阶段、资源和里程碑的学习路径提示词

---

## ❓ 常见问题

### 问：这个技能在 Obsidian vault 之外能用吗？
**答：** 能！它是一个**通用技能**，适用于任何终端环境。不依赖 vault 结构、项目配置或外部文件。

---

### 问：我需要了解提示词框架吗？
**答：** 不需要。技能内置全部 11 种框架，会根据你的任务自动选择最佳的。

---

### 问：技能会告诉我它用了哪个框架吗？
**答：** 不会。它在"魔法模式"下运行——你直接拿到打磨好的提示词，没有技术解释。如果想知道，可以明确提问。

---

### 问：技能会问我几个问题？
**答：** 最多 2-3 个，且仅在信息关键缺失时才问。大多数时候，它会直接生成提示词。

---

### 问：我能自定义框架吗？
**答：** 技能使用标准框架定义，不能自定义。但你可以在输入中附加额外约束（如"写一个简短的提示词用于..."）。

---

### 问：支持英语以外的语言吗？
**答：** 支持。如果你用葡萄牙语输入，它会生成葡萄牙语提示词。英语或混合输入同理。

---

### 问：不满意生成的提示词怎么办？
**答：** 可以让技能进一步优化："写短一点"、"加更多示例"、"聚焦 X 方面"等。

---

### 问：能用于任何 AI 模型（Claude、ChatGPT、Gemini）吗？
**答：** 能。生成的提示词与模型无关，适用于任何对话式 AI。

---

## 🔧 安装（全局设置）

本技能设计为**全局**适用于你所有项目。

### 方式 1：从仓库使用

1. 克隆仓库：
   ```bash
   git clone https://github.com/eric.andrade/cli-ai-skills.git
   ```

2. 配置 Copilot 全局加载技能：
   ```bash
   # 添加到 ~/.copilot/config.json
   {
     "skills": {
       "directories": [
         "/path/to/cli-ai-skills/.github/skills"
       ]
     }
   }
   ```

### 方式 2：复制到全局技能目录

```bash
cp -r /path/to/cli-ai-skills/.github/skills/prompt-engineer ~/.copilot/global-skills/
```

然后配置：
```bash
# 添加到 ~/.copilot/config.json
{
  "skills": {
    "directories": [
      "~/.copilot/global-skills"
    ]
  }
}
```

---

## 📖 了解更多

- **技能开发指南** - 学习如何创建自己的技能
- **[SKILL.md](./SKILL.md)** - 本技能的完整技术规范
- **[仓库 README](../../README.md)** - 所有可用技能概览

---

## 📄 版本

**v1.0.1** | 零配置 | 通用  
*适用于任何项目、任何上下文、任何终端。*
