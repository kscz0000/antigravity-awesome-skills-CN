---
name: brave-man
description: "在动手构建之前，针对新的项目需求运行结构化的澄清式访谈。不直接编写代码，而是产出一份完整规范的 prompt.md，交由一个全新的智能体会话去执行，从而避免代价高昂的错误。触发词：brave-man、新项目澄清访谈、构建前需求澄清、prompt.md 模板生成、避免构建失误。"
risk: critical
source: community
date_added: "2026-06-16"
---

# 勇者先问后战

## 概述

大多数人在描述一个项目时（包括"凭感觉写代码的人"），往往只给出片面或粗略的描述。没人能在一开始就把一切都讲清楚——人脑本来就不是按完整规范去思考的；即便想做到，也会遗漏那些细枝末节，而这些细节一旦项目做大了就会变成真正的麻烦。如果智能体拿着一份稀薄的描述就开始动工，它会用沉默的猜测去填补空白，而等到这些猜测被证明是错的时候，返工的成本已经极其高昂。

本技能的做法是反过来：**先把事情问透，再动手建造**。本技能中智能体的职责并不是写代码、搭建脚手架或产出实施计划。它唯一的工作，是运行一场结构化的访谈，直到把项目完全理解清楚，然后把这份理解写成一份单一、整洁、自包含的 `prompt.md` 文件，供之后一个全新的智能体会话去执行。

## 适用场景

- 当用户表达想要搭建网站、应用、软件、工具或任何类型的项目时使用。
- 当用户的请求里出现类似"帮我做个网站"、"我想做一个能 XXX 的应用"、"做一个能做 Y 的工具"这样的表述时使用。
- 在为新的构建请求写下任何代码或实施计划之前使用。

## 分步指南

1. **分流（Triage）**——用几个简短的快速问题摸清项目的体量，让提问的深度匹配项目的复杂度。
2. **分阶段访谈**——按顺序逐个推进下面列出的相关阶段，每一阶段以一批问题为单位进行。
3. **跟踪完成情况**——维护一份可见的检查清单；在所有相关阶段都被关闭（已回答或已显式使用默认值）之前，不要进入综合环节。
4. **综合**——写出最终的 `prompt.md`。本技能内不要生成实施计划的产物，不要搭建仓库脚手架，也不要写任何应用代码。
5. **交接**——告诉用户开启一个新聊天，附上 `prompt.md`，让新的智能体去执行它。

永远不要因为请求"听起来很简单"就直接跳过分流直奔开发。即便再简单的请求也要先走分流——分流决定的是访谈可以多短，而不是要不要访谈。

## 阶段 0：分流

在开始之前，先问 2–3 个快速问题，以校准深度：

- 这是只给你自己用，还是会有其他人也使用/依赖它？
- 在你脑子里，这件事大致有多大——一个单页/小脚本？一个带几个功能的小应用？还是一个有诸多组件（账号、支付、多种用户角色等）的项目？
- 你是否已有强烈偏好（语言、框架、托管、现有代码库），还是一切都开放？

依据回答来判断下面哪些阶段需要完整展开，哪些只需要一两道快速问题，哪些可以完全跳过并给出明确默认值（例如：一个纯静态单页就直接跳过"集成与认证"阶段，而不是去问它）。

## 阶段说明

按顺序一次推进一个阶段。在一个阶段内，问题以"一批"为单位提出（3–5 个），而不是逐个抛出。对分流判定为不相关的阶段，请明确说出来（比如"因为没有账号需求，跳过认证"），而不是悄悄丢掉。

### 阶段 1 — 目的与用户
- 这是给谁用的？它必须能让他们做到的、绝对不能少的那件事是什么？
- 成功是什么样——怎样的状态会让你说出"没错，这正是我想要的"？
- 是否存在一个你正在对照的现有应用/网站/工具？或者有你想刻意避开的某些东西？

### 阶段 2 — 核心功能与流程
- 请一步步走一遍用户的使用路径：从打开它，到从中获得价值。
- 在你提到的所有内容里，第一版必须有的功能是什么？哪些可以放到以后再说？
- 是否有某些功能你认为"显而易见"，但其实还没说出口？

### 阶段 3 — 数据与内容模型
- 这个应用主要管理的"东西"是什么（例如：帖子、订单、用户、文件）？它们彼此之间是什么关系？
- 数据需要永久保存吗？还是有些只是临时的/会话级的？
- 同样的数据是否需要被不同的用户以不同方式看到（例如：私有的 vs 共享的）？还是所有人都以同样的方式看到？

### 阶段 4 — 技术栈与环境
- 是否有必须使用的语言/框架？还是让智能体挑最合适的？
- 它将运行在哪里——某个具体的托管平台、仅本地、移动端、桌面端，还是浏览器？
- 这是要嵌入到现有代码库/仓库里，还是从零开始？

### 阶段 5 — 集成与认证
*（如果分流显示没有账号/外部服务的需求，则完全跳过——明确说出来，而不是去问）*
- 是否需要用户账号/登录？如果需要，是简单的邮箱+密码，还是通过 Google/Apple/其它方式登录？
- 是否需要与某些外部服务对接（支付、邮件发送、地图、AI 接口等）？
- 是否存在多种类型的用户，并拥有不同的权限（例如：管理员 vs 普通用户）？

### 阶段 6 — 非功能性需求
- 大约会有多少人同时使用——几个人、几百人、还是远超于此？
- 是否涉及敏感数据（个人信息、支付、健康数据），需要额外的保护？
- 是否存在硬性约束——必须能离线使用？必须即时加载？必须在老旧手机上能用？

### 阶段 7 — 边界情况与错误状态
- 当事情出错时应该怎么办——错误输入、连接丢失、空状态（例如：还没有数据）？
- 用户是否会做出某些风险较高或难以撤回的操作（删除东西、发送东西、支付购买）？应用应该在确认环节上做到多谨慎？

### 阶段 8 — 完成定义
- 如果把这件事交给别人去测试，他们要检查哪些点才能确认它运行正确？
- 第一版明确不在范围内的东西是什么——以免被顺手做进去，或者做到一半搁置。

## 最佳实践

- ✅ **要做：** 批量提问，不要挤牙膏。每个阶段以"主题轮"为单位，而不是没完没了的一问一答。
- ✅ **要做：** 用平实语言，少用术语。除非用户已经表现出技术熟练度，否则请围绕现实后果来提问。
- ✅ **要做：** 当一道题只有少数合理答案时，尽可能给出选项。
- ❌ **不要：** 问那些前面已经回答过、或可直接推断出来的重复问题。
- ✅ **要做：** 当用户说"我不知道"时，落落大方地给出一个命名清晰的默认值，并明确把它作为一项假设声明出来。
- ❌ **不要：** 除非用户自然地主动提供信息，否则不要跨阶段跳跃或合并阶段。
- ✅ **要做：** 尊重"你自己看着办"这种回答，但仍要求在阶段 3（数据）和阶段 5（认证/集成）至少走一遍"默认值 + 确认"的流程。

## 完成检查清单

用下面的格式持续维护一份可见的各相关阶段状态，并在每个阶段关闭时展示给用户：

```
[x] Purpose & users — confirmed
[x] Core features & flows — confirmed
[~] Data & content model — defaulted (assumed simple per-user storage, no sharing)
[ ] Tech stack & environment — open
[-] Integrations & auth — skipped (no accounts needed)
...
```

只要还有任何相关阶段处于 `[ ]` 未完成，就不要进入综合环节。`[x]` 已确认 与 `[~]` 已默认并被接受 这两种状态都视为已关闭。

## 综合：写出 prompt.md

一旦所有相关阶段都已关闭，立即停止提问。不要产出实施计划，不要搭建项目，不要写应用代码。改为：在项目根目录写下一个名为 `prompt.md` 的文件，里面装下完整、提炼过的规范说明，直接面向将读到它的下一个智能体。结构如下：

```markdown
# Project Brief: <name>

You are building the following project. Treat this file as the complete
specification — everything needed to build it correctly is below.
Do not re-ask the questions that produced this brief unless something
here is genuinely ambiguous or missing.

## Overview
<one paragraph: what it is, who it's for, what success looks like>

## Core Features (prioritized)
<must-have list, then nice-to-have list>

## User Flows
<step-by-step walkthroughs from Phase 2>

## Data Model
<entities, relationships, persistence rules from Phase 3>

## Tech Stack & Environment
<language/framework, hosting/platform, repo constraints from Phase 4>

## Integrations & Auth
<or "None — no accounts or external services required">

## Non-Functional Requirements
<scale, sensitive data handling, hard constraints from Phase 6>

## Edge Cases & Error Handling
<from Phase 7>

## Assumptions & Defaults Used
<every default that was proposed and accepted during the interview,
listed plainly so the user can spot anything they want to override later>

## Definition of Done
<acceptance criteria and explicit out-of-scope items from Phase 8>

## Suggested Build Order
<a short, sensible milestone sequence — not a full implementation plan>
```

保持紧凑和完整，不要注水——每一节都应当承载真实决策，而不是凑字数的填充。其中"已使用的假设与默认值"这一节最为重要：它是用户原本没法在一开始就讲清楚的所有空白的纸面记录。

## 交接

写完 `prompt.md` 之后，直白地告诉用户：

> 你的项目规范已保存为 `prompt.md`。为获得最佳效果，请开一个**新聊天**，把这份文件带上，然后让新的智能体去执行它。从零开始可以保证构建对话不被这次来回反复的澄清过程所污染——新的智能体只需要这份提炼过的简报，而不是完整的访谈过程，这样速度更快，也避免在一个它并不需要的对话上消耗上下文。

即便用户在当前会话内紧接着请求立即实现，也不要开始实现——请指引他们走"新聊天"交接流程，因为把访谈与执行分开正是本技能的核心理念。

## 示例

### 示例 1：用户说"帮我做一个待办应用"
```markdown
1. **Triage:** Is this just for you? How big is it? Any preferred stack?
2. **Phase 1 (Purpose):** What is the one thing it absolutely must let you do?
3. **Synthesis:** Outputs `prompt.md` with React/Firebase stack based on interview.
```

## 故障排除

### 问题：用户因问题过多而不耐烦
**症状：** 用户回复"直接做就行了"或"我不在乎"。
**解决办法：** 停止提问，对剩余关键阶段（数据、认证）提出默认值，并综合出 `prompt.md`。

## 相关技能

- `@brainstorming` - 用于探索抽象想法，而不是收集构建规范时使用。

## 局限性

- **不生成代码：** 本技能刻意不写任何应用代码，也不搭建仓库脚手架。
- **需要新会话：** 生成的 `prompt.md` 必须在全新的智能体会话中执行，以保证上下文干净。
- **依赖用户输入：** 规范的质量在很大程度上取决于用户是否愿意回答访谈中的问题。