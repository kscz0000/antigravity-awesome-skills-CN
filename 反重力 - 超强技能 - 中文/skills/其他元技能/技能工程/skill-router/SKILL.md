---
name: skill-router
description: "当用户不确定该用哪个技能或从哪里开始时使用。通过针对性问题访谈用户，并从已安装的技能库中推荐最适合其目标的技能。触发词：不知道用哪个技能、从哪里开始、该用什么、帮我选技能、skill router"
risk: safe
source: self
---

# 技能路由器

## 使用场景
在以下情况下使用此技能：
- 用户说"我不知道从哪里开始"或"我该用哪个技能"
- 用户有模糊的目标但没有明确的方法
- 用户问"我应该用什么来……"或"我不确定该怎么处理这个"
- 用户刚接触技能库，需要引导

## 目标

帮助不确定自己想做什么或该用哪个技能的用户。
通过简短的结构化对话进行访谈，然后从已安装的技能库中推荐最相关的技能——并清晰解释每个技能为何适合，以及如何精确调用它。

---

## 指引

### 第一步 — 热情回应并开启访谈

热情地回复用户，告诉他们你会问几个快速问题来找到合适的技能。此时**不要**推荐任何技能。

开场示例：
> "没问题——让我问你几个快速问题，这样我就能为你找到最合适的技能。"

---

### 第二步 — 按顺序逐一提问漏斗问题

只问必要的问题。如果前面的回答让后面的问题变得无关，就跳过。

**问题一 — 任务的大致领域是什么？**
以编号选项呈现：
1. 构建/编码某样东西（应用、功能、组件、脚本）
2. 修复或调试某个已损坏的东西
3. 安全、渗透测试或漏洞评估
4. AI 智能体、LLM 或自动化流水线
5. 营销、SEO、内容或增长
6. DevOps、基础设施、部署或 git
7. 设计、UI/UX 或创意输出
8. 规划、策略或文档
9. 其他（请用户描述）

**问题二 — 任务的具体程度如何？**
1. 我有明确的规格说明/我确切知道要构建什么
2. 我有一个大致的想法，但需要帮助来完善它
3. 我完全是零基础，没有明确的方向

**问题三 — 涉及什么技术栈或领域？**（仅在相关时询问）
例如：React / Next.js、Node.js、Python、AWS、Stripe、AI/LLM、无代码等。
如果用户说"不确定"或"都行"，没问题——继续。

**问题四 — 你想自主执行（智能体全权处理）还是协作进行（你保持参与）？**
1. 完全自主——直接开干
2. 协作——我想审核/批准每个步骤
3. 还不确定

---

### 第三步 — 推荐技能

根据用户的回答，推荐 **1 个主要技能** 和最多 **2 个辅助技能**。严格按照以下格式推荐：

**✅ 主要技能：`@skill-name`**
*原因：* [1-2 句话解释为什么这最适合他们描述的需求]
*调用方式：*
```
@skill-name [在此粘贴用户的目标]
```

**🔁 也可以考虑：**
- `@skill-name-2` — [一句话说明何时搭配使用]
- `@skill-name-3` — [一句话说明何时搭配使用]

---

### 第四步 — 提供现成的提示词

推荐之后，主动提出为用户撰写一个可以直接粘贴使用的提示词。询问：

> "需要我为你写好完整的提示词，这样你直接粘贴就行？"

如果用户同意，使用推荐的技能和访谈中了解到的所有信息，撰写一个完整、具体的提示词。

---

## 示例交互

```
用户：@skill-router 我想构建一些东西，但不知道从哪里开始

智能体：没问题——让我问几个快速问题。
       任务的大致领域是什么？
       (1) 构建  (2) 调试  (3) 安全  (4) AI/LLM
       (5) 营销  (6) DevOps  (7) 设计  (8) 规划

用户：1 - 构建一些东西

智能体：任务的具体程度如何？
       (1) 明确的规格  (2) 大致想法  (3) 从零开始

用户：2 - 大致想法

智能体：用什么技术栈？（React、Node、Python 等——或者"不确定"）

用户：Next.js

智能体：✅ 主要技能：@brainstorming
       原因：你有一个大致的想法，需要在构建之前先梳理清楚。
       头脑风暴会提出结构化问题并产出清晰的规格说明。

       @brainstorming 帮我设计一个 [你的应用想法]，使用 Next.js

       🔁 也可以考虑：
       - @plan-writing — 头脑风暴产出规格后，将其分解为任务
       - @senior-fullstack — 当你准备好开始构建时

       需要我为你写好完整的提示词吗？
```

---

## 技能路由参考

### 从零构建完整产品或应用
- 主要：`@app-builder`
- 如果想先规划：`@brainstorming` → `@plan-writing` → `@app-builder`
- 如果想要完全自主：`@loki-mode`

### 构建特定的前端功能/界面
- 主要：`@senior-fullstack` 或 `@frontend-design`
- 技术栈相关：`@react-patterns`、`@nextjs-best-practices`、`@tailwind-patterns`
- 如果需要完整的设计系统：`@ui-ux-pro-max` + `@core-components`

### 构建后端 API 或服务
- 主要：`@backend-dev-guidelines`
- 技术栈相关：`@nodejs-best-practices`、`@python-patterns`、`@nestjs-expert`
- API 设计：`@api-patterns`
- 数据库：`@database-design` + `@prisma-expert`

### 调试已损坏的东西
- 主要：`@systematic-debugging`
- 如果测试失败：`@test-fixing`
- 如果是代码质量问题：`@clean-code`

### 编写测试 / TDD
- 主要：`@tdd`
- Playwright/浏览器测试：`@playwright-skill`
- Jest 模式：`@testing-patterns`

### 集成第三方服务
- 支付：`@stripe-integration`
- 认证：`@clerk-auth` 或 `@nextjs-supabase-auth`
- 数据库：`@neon-postgres` 或 `@firebase`
- 消息：`@twilio-communications`
- 机器人：`@slack-bot-builder`、`@discord-bot-architect`、`@telegram-bot-builder`
- 文件存储：`@file-uploads`
- 分析：`@analytics-tracking`

### AI / LLM / 智能体
- 架构：`@ai-agents-architect`
- RAG 流水线：`@rag-engineer`
- 提示词：`@prompt-engineer`
- 多智能体：`@langgraph` 或 `@crewai`
- 可观测性：`@langfuse`
- 语音：`@voice-agents`

### 安全/渗透测试
- 入门：`@ethical-hacking-methodology` + `@pentest-checklist`
- Web 应用测试：`@burp-suite-testing`、`@sql-injection-testing`、`@xss-html-injection`
- 网络/基础设施：`@aws-penetration-testing`、`@linux-privilege-escalation`
- 参考：`@top-web-vulnerabilities`

### DevOps / 基础设施 / 部署
- Docker：`@docker-expert`
- 云：`@aws-serverless`、`@gcp-cloud-run`、`@vercel-deployment`
- Git 工作流：`@git-pushing`、`@using-git-worktrees`、`@github-workflow-automation`
- 脚本：`@linux-shell-scripting`

### 营销/增长/SEO
- 文案：`@copywriting`
- 落地页：`@page-cro`
- SEO：`@seo-fundamentals` + `@seo-audit`
- 邮件：`@email-sequence`
- 广告：`@paid-ads`
- 发布：`@launch-strategy`

### 规划/架构/策略
- 快速规划：`@concise-planning`
- 完整规划：`@plan-writing` → `@executing-plans`
- 架构：`@software-architecture` 或 `@senior-architect`
- 产品策略：`@product-manager-toolkit`

### 创意/设计/视觉
- UI：`@frontend-design`
- 数据可视化：`@claude-d3js-skill`
- 生成艺术：`@algorithmic-art`
- 演示文稿：`@pptx-official`

### 完全自主/并行执行
- 完整启动模式：`@loki-mode`
- 独立并行任务：`@dispatching-parallel-agents`
- 先规划后执行：`@subagent-driven-development`

### 文档创建
- Word 文档：`@docx-official`
- PDF：`@pdf-official`
- 电子表格：`@xlsx-official`
- 演示文稿：`@pptx-official`

---

## 约束

- 每次推荐不超过 1 个主要技能和 2 个辅助技能。
- 始终包含精确的 `@invoke` 语法，方便用户复制粘贴。
- 如果用户的目标跨越多个类别，选择最上游的技能（例如在 `@senior-fullstack` 之前选 `@brainstorming`）。
- 不要用完整的技能列表淹没用户。只推荐与他们具体回答相关的技能。
- 如果用户完全不知所措，对开放式目标默认推荐 `@brainstorming`，对涉及构建的目标默认推荐 `@app-builder`。
- 推荐后，始终主动提出为用户撰写现成的提示词。

---

## 局限性

- 仅推荐已安装库中的技能。如果某个技能未安装，推荐可能无法使用。
- 路由基于自然语言匹配。高度模糊的目标可能需要进一步澄清。
- 不执行推荐的技能——仅负责推荐。用户需要自行调用技能。
- 路由参考涵盖了最常见的技能，但不包含库中的每个技能。
