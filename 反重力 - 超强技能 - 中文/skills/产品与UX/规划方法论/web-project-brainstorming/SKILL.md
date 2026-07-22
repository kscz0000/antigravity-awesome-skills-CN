---
name: web-project-brainstorming
description: 用于头脑风暴网页开发项目与页面设计的大师级框架。梳理概念、UX 流程、视觉风格、技术架构与 SEO 等结构性阶段。涉及网页项目规划、产品定位、设计系统、UX 流程、技术选型与架构设计时使用。
category: consulting
risk: safe
source: self
source_type: self
date_added: "2026-06-26"
author: Rsmiyani
tags: [brainstorming, project-planning, web-development, product-scoping, design-system, architecture]
tools: [claude, cursor, gemini]
---

# 网页项目头脑风暴

## 概述

本技能为网页项目、Web 应用或单个页面设计在起步阶段提供一套结构化的大师级头脑风暴框架。它引导开发者和设计师完成核心产品概念的范围界定、用户流程梳理、视觉风格定义、技术栈选型，以及搜索引擎优化（SEO）与性能规划。

## 适用场景

- 任何新建网页开发项目或页面重设计的起步阶段。
- 梳理 Web 应用的功能集合、用户角色与交互模式时。
- 建立设计系统、颜色令牌与布局规范时。
- 评估技术栈时（例如 Next.js 与原生 JS 的对比、CSS Grid 与 Tailwind 的取舍）。

## 工作方式

按顺序执行网页项目头脑风暴，共分六个结构化阶段。每个阶段逐一向用户提问，保持专注并确保充分对齐。

### 阶段一：核心概念与范围界定
明确产品的核心价值主张与范围：
- **目标用户**：谁会使用这个网站或应用？
- **核心价值**：它为用户解决了什么问题？
- **关键功能**：排名前 3–5 的必备功能是什么？

### 阶段二：用户体验（UX）与信息架构
梳理用户的导航与交互路径：
- **页面层级**：站点地图与页面结构是怎样的？
- **用户旅程**：用户为完成关键目标会经历哪些分步流程？
- **响应式布局**：采用移动优先、桌面优先，还是均衡策略？

### 阶段三：视觉风格与设计系统
建立视觉规范与美学参数：
- **设计美学**：现代风、极简风、粗野风、玻璃拟态还是奢华风？
- **配色方案**：主色、辅色、点缀色分别是什么？（推荐使用可定制的 HSL/RGB 模型，而非静态颜色关键字。）
- **字体排版**：哪些 Google Fonts 或系统字体契合主题？（例如 Inter、Outfit、Syne。）
- **交互状态**：悬停、点击、过渡与加载状态如何呈现？

### 阶段四：技术栈与架构
选定技术与集成方案：
- **前端框架**：React、Next.js、Vite、Astro、Svelte，还是原生 HTML/JS？
- **样式方案**：原生 CSS、Tailwind CSS，还是 CSS Modules？
- **数据与后端**：REST API、GraphQL、tRPC、Firebase、Supabase，还是 SQLite？
- **状态管理**：Zustand、Context API、Redux，还是 React 本地状态？

### 阶段五：SEO、可访问性（A11y）与性能
规划可发现性与快速加载：
- **SEO 元素**：标题标签结构、meta 描述与语义化 HTML 标签层级。
- **可访问性**：ARIA 标签、语义化标签、键盘导航与颜色对比。
- **性能**：资源预加载、图片懒加载、服务端渲染（SSR）与 CDN 分发。

### 阶段六：MVP 范围与项目分阶段
将工作拆解为可管理的增量：
- **阶段一（MVP）**：可上线的最小可行产品。
- **阶段二（增强项）**：锦上添花的功能、微动效与高级集成。

## 示例

### 交互式问卷提示模板
在与客户或团队成员开启头脑风暴会话时，使用以下提示布局：

```markdown
👋 Let's brainstorm your new web project! We will walk through 6 quick phases.

---
### Phase 1: Core Concept & Scoping
1. What is the main title or working name of this project?
2. Who are the primary target users (e.g., tech-savvy professionals, shoppers, children)?
3. What are the 3 core tasks a user must be able to perform?
---
```

### 头脑风暴产出文档模板
所有阶段完成后，使用以下模板生成项目 Markdown 蓝图：

```markdown
# Project Blueprint: [Project Name]

## 1. Product Concept
- **Value Proposition**: [Summary]
- **Key Features**:
  1. [Feature 1]
  2. [Feature 2]

## 2. Information Architecture & UX
- **Pages**: `/index.html`, `/dashboard.html`
- **Primary User Flow**: User signs up -> completes onboarding -> views dashboard.

## 3. Styling & Aesthetics
- **Aesthetic**: Sleek Glassmorphism Dark Mode
- **Color Tokens**:
  - Background: `hsl(222, 47%, 11%)`
  - Accent/Primary: `hsl(217, 91%, 60%)`
- **Typography**: Inter (Body), Outfit (Headings)

## 4. Technical Architecture
- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **Database**: PostgreSQL with Prisma ORM

## 5. SEO & Performance
- **Primary Title**: "[Brand] | [Tagline]"
- **Performance Strategy**: Dynamic image optimization, caching pages via Cloudflare.

## 6. MVP vs Phase 2 Roadmap
- **MVP**: Authentication + core dashboard view.
- **Phase 2**: Real-time notifications and PDF reporting.
```

## 最佳实践

- ✅ 逐步提问——避免在单次回复中倾泻全部六个阶段，以免造成认知过载。
- ✅ 在用户犹豫时提出合理默认值（例如推荐响应式 Tailwind / CSS Grid 与标准语义化 HTML）。
- ✅ 从一开始就规划好语义化 HTML 布局层级（每页一个 `<h1>`，按序使用 `<section>`、`<article>`、`<header>`、`<footer>` 等元素）。
- ✅ 明确记录非目标，防止功能蔓延。

## 局限

- 本技能聚焦于概念梳理、架构与功能规划，不能替代实现代码或系统配置的编写。
- 头脑风暴成果应视为灵活的蓝图，在开发过程中随着技术约束的显现不断打磨。

## 安全注意事项

- 在阶段四（架构）中尽早标记任何安全需求（例如 SSL 证书、CORS 策略、安全的身份认证存储、环境变量保护）。
- 切勿在设计或蓝图文档中存储真实的 API 令牌、密码或凭证。

## 常见陷阱

- **问题**：范围蔓延（项目在构建 MVP 之前扩张过快）。
  **对策**：严格执行阶段六，将锦上添花的功能推入阶段二。
- **问题**：直到开发后期才考虑移动端设计。
  **对策**：在阶段三确定布局风格之前，先于阶段二梳理响应式模式。

## 相关技能

- `@writing-plans` — 组织结构化的分步工程计划。
- `@architecture-decision-records` — 记录架构决策。
- `@ux-flow` — 深入设计用户体验流程与交互细节。