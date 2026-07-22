---
name: seo-aeo-schema-generator
description: "为 10 种 schema 类型生成有效的 JSON-LD 结构化数据，包含富媒体搜索结果资格验证和可直接使用的脚本模块。当用户需要为任何页面生成 schema 标记、JSON-LD 或结构化数据时激活。触发词：schema生成、JSON-LD、结构化数据、schema标记、富媒体结果、FAQ schema、产品schema、面包屑schema"
risk: safe
source: community
date_added: "2026-04-01"
---

# SEO-AEO Schema 生成器

## 概述

为 10 种 schema 类型（包括 FAQPage、Article、Product、HowTo 和 BreadcrumbList）生成可直接使用的 JSON-LD schema 标记。根据 Google 富媒体搜索结果资格规则验证所有必需字段，标记缺失字段并给出具体修复指令，每种 schema 类型输出一个干净的 `<script>` 模块，可直接粘贴到页面 `<head>` 中。

本技能是 [SEO-AEO Engine](https://github.com/mrprewsh/seo-aeo-engine) 的一部分。

## 使用场景

- 为新落地页或博客文章添加结构化数据时
- 页面需要在搜索中展示 FAQ 富媒体结果或产品星级评分时
- 验证现有 schema 是否符合 Google 富媒体搜索结果资格时
- 内容质量审计标记缺少 schema 时

## 支持的 Schema 类型

| 类型 | 可解锁的富媒体结果 |
|------|---------------------|
| FAQPage | SERP 中的 FAQ 折叠面板 — AEO 关键 |
| Article | 文章富媒体结果、热门新闻 |
| Product | SERP 中的价格、库存、评分 |
| HowTo | 分步操作富媒体结果 |
| Review | SERP 中的星级评分 |
| AggregateRating | 带评论数的星级评分 |
| BreadcrumbList | SERP URL 中的面包屑路径 |
| Organization | 品牌知识面板信号 |
| WebPage | 增强页面理解 |
| WebSite | 站点链接搜索框 |

## 工作原理

### 第一步：推荐 Schema 类型
如果未指定 schema 类型，根据页面类型推荐合适的类型。落地页使用 FAQPage + Product + BreadcrumbList。博客文章使用 Article + FAQPage + BreadcrumbList。

### 第二步：使用内置 Schema 模板
运用对 schema.org 和 Google 富媒体搜索结果要求的了解，为每种请求的 schema 类型构建 JSON-LD 模板。使用 Google 富媒体搜索结果文档中该类型列出的必需和推荐字段。

### 第三步：填充字段
将所有页面数据映射到模板占位符。根据富媒体搜索结果资格规则检查每个必需字段。

### 第四步：验证
将缺失的必需字段标记为严重问题。将缺失的推荐字段标记为警告。不要输出缺少必需字段的 schema。

### 第五步：输出脚本模块
每种 schema 类型输出一个 `<script type="application/ld+json">` 模块。附带实施说明和测试工具链接。

## 示例

### 示例：FAQPage Schema 输出
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "什么是 Syncro？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Syncro 是面向分布式工程团队的远程优先项目管理平台。它将任务追踪、异步沟通和冲刺规划整合在一个工具中。"
      }
    }
  ]
}
</script>
```

## 最佳实践

- ✅ **应该做：** 任何有 FAQ 板块的页面都要包含 FAQPage schema——这是最强的 AEO 信号
- ✅ **应该做：** 每种 schema 类型用一个 `<script>` 模块——不要合并多种类型
- ✅ **应该做：** 部署前用 Google 的富媒体搜索结果测试工具测试每个输出
- ❌ **不应该做：** schema 中不要使用相对 URL——所有 URL 必须以 `https://` 开头
- ❌ **不应该做：** 部署前不要在任何字段中留有占位文本
- ❌ **不应该做：** 不要在 JSON-LD 字符串值中使用 HTML 标签

## 常见陷阱

- **问题：** Schema 通过了验证但搜索中未显示富媒体结果
  **解决：** 富媒体结果可能在部署后需要数周才会出现。添加 schema 后立即在 Google Search Console 中请求重新索引。

- **问题：** 产品 schema 缺少星级评分显示
  **解决：** 添加包含 ratingValue、reviewCount、bestRating 和 worstRating 的 AggregateRating 对象——四个字段都是必需的。

## 相关技能

- `@seo-aeo-landing-page-writer` — 提供用于 schema 填充的 FAQ 和产品数据
- `@seo-aeo-content-quality-auditor` — 在审计中标记 schema 缺失

## 相关资源

- [SEO-AEO Engine 仓库](https://github.com/mrprewsh/seo-aeo-engine)
- [完整版 Schema 生成器 SKILL.md](https://github.com/mrprewsh/seo-aeo-engine/blob/main/.agent/skills/schema-generator/SKILL.md)

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
