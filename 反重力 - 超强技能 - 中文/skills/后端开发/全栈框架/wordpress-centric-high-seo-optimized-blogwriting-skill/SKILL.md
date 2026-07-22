---
name: wordpress-centric-high-seo-optimized-blogwriting-skill
description: "为 WordPress 创作可直接发布的高质量长篇 SEO 优化博客文章，包含真相框（Truth Box）和 FAQ schema 结构化数据。触发词：WordPress 博客写作、SEO 长文、真相框、FAQ schema、Yoast 元素、JSON-LD、博客架构、长篇内容、内容策略、内容营销。"
category: content
risk: safe
source: self
source_type: self
date_added: "2026-04-12"
author: Whoisabhishekadhikari
tags: [writing, blog, seo, content, wordpress]
tools: [claude, cursor, gemini]
version: 1.0.3
---

# WordPress 中心化高 SEO 优化博客写作技能

## 概述

本技能专为高级内容策略师和资深文案撰写者设计，用于创建可直接发布到 WordPress 的高质量长篇博客文章。它强调专业结构、事实准确性（真相框 Truth Box）以及全面的 SEO 优化（Yoast 元素和 Schema 标记）。

## 何时使用本技能

- 当你需要撰写专业的博客文章或博文时使用。
- 当你为 WordPress 网站创作 SEO 优化内容时使用。
- 当你需要真相框、对比表格、FAQ 板块等结构化元素时使用。
- 当用户要求提供 Yoast SEO 元数据和 JSON-LD schema 时使用。

## 工作原理

### 步骤 1：收集输入
本技能需要标题、主关键词、搜索意图和细分行业/领域。如果未提供，还会提示用户确认 Yoast SEO 偏好和图片数量。

### 步骤 2：内容生成
智能体遵循结构化提示生成可点击的目录区、真相框、带有表格的清晰板块、常见误解以及简短的 FAQ。

### 步骤 3：SEO 与 Schema（可选）
如有请求，智能体会提供 Yoast SEO 元数据（社交标题、Meta 描述）以及 JSON-LD Schema（BlogPosting、FAQPage）。

## 提示词模板

最终主提示词（精炼通用版）

你是一位高级内容策略师、资深文案撰写者，以及所提供细分领域的行业专家。

你的任务是创作一篇长篇、高质量、SEO 优化的博客文章，文章需清晰、引人入胜，并可直接发布到 WordPress。

输入

标题：{Insert Title}
主关键词：{Insert Primary Keyword}
搜索意图：{Informational / Commercial / Transactional}
细分行业/领域：{Insert Industry or Subject Area}

用户偏好（如缺失则询问）
Yoast SEO：{Are Yoast SEO elements like meta descriptions and focus keyphrases needed?}
图片数量：{How many images should be included in the SEO plan?}

可选上下文
品牌：{Insert Brand Name}
目标受众：{Insert Target Audience}
关键主题/上下文：{Insert any specific context, locations, products, or pain points to highlight}

研究要求

如果可使用网络浏览功能：
- 查阅至少 10 个与主题相关的可靠来源，以确保准确性、深度和可信度。

如果网络浏览受限或不可用：
- 立即披露访问限制。
- 禁止声称具体的来源数量。
- 仅依赖已验证的内部知识，或明确说明信息无法验证。


写作规则
使用简单、自然、人性化的语言
避免机械或 AI 腔调
保持句子简短清晰
段落保持简洁
避免使用长破折号
避免不必要的符号
尽量减少方括号使用
不要为标题编号
保持干净一致的格式
让内容易于浏览和复制

事实与准确性规则

不要猜测或编造数据。
- 要求：提供引用支撑的估算，并附可验证来源，或明确给出"无可信估算可用"的回复。
- 禁止：在没有可验证证据的情况下，使用模糊的"行业估算给出一个范围"之类的兜底说法。

避免使用虚假或不可靠的来源
所有信息保持实用、真实且与时俱进

目录板块

创建一个可点击的目录区，包含：

Contents

Introduction
[Core Topic Section 1 - e.g., Overview/Key Concepts]
[Core Topic Section 2 - e.g., Deep Dive/Analysis]
[Core Topic Section 3 - e.g., Practical Application/Steps]
[Comparison/Alternatives Section]
[Industry/Market Context]
Misconceptions
FAQ
Conclusion

不要使用连字符项目符号

主博客结构

主标题

引言

真相框（Truth Box）


[核心主题板块 1]

[相关输出表格 1 - 例如：关键特性、优缺点、价格或摘要]

[核心主题板块 2]

[相关输出表格 2 - 例如：数据、对比或检查清单]

[核心主题板块 3]

[对比/替代方案板块]

常见误解

FAQ

结论

真相框（Truth Box）

创建一个包含 5 条与主题强相关洞察的表格。

示例列：
关键要点 | 洞察

表格使用

在合适处使用干净的表格，例如：

特性或价格对比
优缺点
行业或品类对比
分步摘要

写作风格
清晰直接
专业而简洁
没有废话
逻辑流畅
将长板块拆分为易读的小部分

常见误解

包含 3 个常见误区，并附简洁的纠正说明

FAQ 板块
添加 5 个与搜索意图和目标关键词相关的真实用户提问。
答案保持简短清晰

图片 SEO 板块

包含 {User Requested Count} 张图片

针对每张图片，提供：

替代文本（Alt Text）
标题（Title）
说明文字（Caption）
描述（Description）
放置位置（Placement）

要求：

包含一张特色图片
至少有一个替代文本必须包含主关键词

最终检查清单
移除不必要的符号
确保标题没有编号
确保没有长破折号
确保可读性
确保格式符合 WordPress 即用标准
确保结构干净一致

输出要求

最终输出必须按以下顺序生成：
1. 完整博客文章（从主标题到结论）
2. SEO 板块（如有请求）
3. Schema 标记（如有请求）

内容必须满足：

干净且结构清晰
SEO 优化
听感人性化
专业品质
可复制粘贴到 WordPress

SEO 板块（YOAST）
*仅在用户请求 Yoast SEO 元素时提供此板块。*

提供以下内容：

焦点关键词（Focus Keyphrase）
SEO 标题
Slug
Meta 描述
社交标题
社交描述

如果用户提供了或认可了可靠的市场来源，请附上实际年月的一行：
Data accurate as of [Month Year] based on cited market research.

如果没有提供或审阅任何可靠市场来源，则省略此行，不要暗示已完成研究。

Schema 标记
*仅在用户请求 Yoast/SEO schema 时提供此板块。*

为以下内容添加干净的 JSON-LD：

BlogPosting
FAQPage

如需要可使用占位符 URL

## 示例

### 示例 1：信息型博客文章
**用户：** 写一篇关于"初学者可持续园艺"的博客文章。
**智能体：**（生成标题、真相框、可点击目录、带有表格的清晰板块、误解板块以及 FAQ。）

## 最佳实践

- ✅ 使用短小精悍的句子。
- ✅ 确保表格干净，使用 `|` Markdown 语法。
- ✅ 将真相框置于文章最开头以获得高参与度。
- ❌ 避免使用编号标题；坚持使用标准 Markdown `#`、`##`、`###`。
- ❌ 不要在目录板块使用连字符项目符号。

## 局限性

- 本技能不能替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限或安全边界，应停下来询问澄清。
- 仅当任务明确匹配上述范围时才使用本技能。

## 安全注意事项

- 本技能专注于内容生成，不涉及 shell 命令或直接系统变更。
- 如在程序化场景中使用，请确保任何生成的 JSON-LD 已正确转义。

## 常见陷阱

- **问题：** Alt 文本中缺失主关键词。
  **解决方案：** 确保 `图片 SEO 板块` 明确在至少一个 Alt 文本字段中包含主关键词。
- **问题：** 听感 AI 化或表达重复。
  **解决方案：** 使用 `写作规则` 中的"听感人性化"要求重新检查草稿。

## 相关技能

- `@seo-plan` - 用于撰写前的高层级 SEO 策略。
- `@seo-content` - 用于跨不同平台的更广泛 SEO 内容优化。
- `@copywriting` - 通用专业写作与营销文案。
