---
name: seo-aeo-blog-writer
description: "撰写长篇博客文章，包含 TL;DR 摘要块、定义句、对比表格和 5 问 FAQ，用于 SEO 排名和 AEO 引用。当用户需要写博客文章、长篇指南或内容创作时触发。触发词：写博客、撰写文章、长篇内容、SEO 文章、AEO 内容、blog writer、SEO 写作"
risk: safe
source: community
date_added: "2026-04-01"
---

# SEO-AEO 博客写手

## 概述

撰写结构化的长篇博客文章（800–3000 词），同时满足 SEO 排名信号和 AEO 引用要求。每篇文章包含一个 TL;DR 直答块、一句定义、结构化的 H2/H3 层级、相关对比表格，以及恰好 5 个为 AI 提取而设计的 FAQ 条目。

属于 [SEO-AEO Engine](https://github.com/mrprewsh/seo-aeo-engine) 的一部分。

## 使用场景

- 从内容集群地图中撰写集群文章时使用
- 创建长篇指南以建立主题权威时使用
- 需要可被 Perplexity 或 ChatGPT 等 AI 引擎引用的内容时使用
- 需要遵循一致、可审计结构的博客文章时使用

## 工作原理

### 步骤 1：先写 TL;DR 块
用 2–3 句话直接回答文章的核心问题。将其放在 H1 之后的引用块中。这是 AI 引擎首先尝试提取的内容块。

### 步骤 2：构建标题骨架
在撰写正文之前先设定 H1、H2（4–6 个）和 H3。第一个 H2 必须是"什么是"章节，以简洁的定义句开头。

### 步骤 3：撰写正文
按以下章节顺序：什么是 → 为什么重要 → 工作原理（含 H3 子概念）→ 实操步骤 → 常见错误 → FAQ → 结论。

### 步骤 4：撰写 5 个 FAQ 条目
使用长尾关键词和次要关键词作为问题。每个回答不超过 50 词且自成一体 — 无需上下文即可独立阅读。

### 步骤 5：运行 AEO 和 SEO 检查清单
在输出前验证 TL;DR 是否存在、定义句、FAQ 数量、关键词放置和标题结构。

## 示例

### 示例：TL;DR 块
How to Manage a Remote Engineering Team

TL;DR: Managing a remote engineering team requires async
communication tools, clear documentation standards, and
timezone-aware sprint planning. Teams that nail these three
areas ship consistently regardless of where members are located.


### 示例：FAQ 章节
Q: What is the biggest challenge of remote engineering teams?
A: Async communication. Without shared hours, decisions slow down
and context gets lost. Teams that document decisions in writing
and use structured standup tools close this gap fastest.
Q: How do you run a daily standup with a remote team?
A: Use async video or text standups posted at the start of each
member's day. Tools like Loom or Slack threads work well.
Avoid live calls across more than 2 timezones.

## 最佳实践

- ✅ **推荐：** 先写 TL;DR 块再写其他内容 — 它锚定整篇文章
- ✅ **推荐：** 让"什么是"的定义句可以独立提取 — 一句干净的话
- ✅ **推荐：** 用次要关键词作为 FAQ 问题以捕获长尾流量
- ❌ **避免：** FAQ 回答超过 50 词 — AI 引擎会跳过过长的回答
- ❌ **避免：** 在文章中使用重复的 H2 标题
- ❌ **避免：** 如果主题涉及方案对比，不要省略对比表格

## 常见陷阱

- **问题：** TL;DR 块过于模糊，无法作为直接回答提取
  **解决方案：** TL;DR 必须用 2–3 句话回答文章的核心问题。如果没有回答具体问题，请重写。

- **问题：** FAQ 回答引用了"如上所述"或其他上下文
  **解决方案：** 每个 FAQ 回答必须完全独立 — 不引用文章其他部分。

## 相关技能

- `@seo-aeo-content-cluster` — 为本文提供主题和关键词
- `@seo-aeo-content-quality-auditor` — 审计完成文章的 SEO 和 AEO 信号
- `@seo-aeo-internal-linking` — 映射本文与相关页面之间的链接

## 附加资源

- [SEO-AEO Engine 仓库](https://github.com/mrprewsh/seo-aeo-engine)
- [完整 Blog Writer SKILL.md](https://github.com/mrprewsh/seo-aeo-engine/blob/main/.agent/skills/blog-writer/SKILL.md)

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
