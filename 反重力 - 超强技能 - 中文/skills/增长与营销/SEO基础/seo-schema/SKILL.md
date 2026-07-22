---
name: seo-schema
description: >
  检测、验证和生成 Schema.org 结构化数据。优先使用 JSON-LD 格式。
  当用户提到"schema"、"结构化数据"、"富媒体搜索结果"、"JSON-LD"、"标记"、"schema标记"、
  "结构化标记"、"rich results"、"markup"时使用。
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# Schema 标记分析与生成

## 使用场景
- 检测、验证或生成 Schema.org 结构化数据时使用。
- 用户询问 JSON-LD、富媒体搜索结果或标记优化机会时使用。
- 当 schema 验证是主要任务（而非更广泛的 SEO 审计）时使用。

## 检测

1. 扫描页面源码中的 JSON-LD `<script type="application/ld+json">`
2. 检查 Microdata（`itemscope`、`itemprop`）
3. 检查 RDFa（`typeof`、`property`）
4. 始终推荐 JSON-LD 作为首选格式（Google 明确声明偏好）

## 验证

- 检查每种 schema 类型的必需属性
- 对照 Google 支持的富媒体搜索结果类型进行验证
- 测试常见错误：
  - 缺少 @context
  - 无效的 @type
  - 数据类型错误
  - 占位符文本
  - 相对 URL（应为绝对 URL）
  - 无效的日期格式
- 标记已弃用的类型（见下方）

## Schema 类型状态（截至 2026 年 2 月）

完整列表请阅读 `references/schema-types.md`。关键规则：

### 活跃（可自由推荐）：
Organization, LocalBusiness, SoftwareApplication, WebApplication, Product（自 2025 年 4 月起支持 Certification 标记）, ProductGroup, Offer, Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage, ContactPage, VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting

### 视频与专业类型（可自由推荐）：
BroadcastEvent, Clip, SeekToAction, SoftwareSourceCode

这些类型的即用型 JSON-LD 模板见 `schema/templates.json`。

> **JSON-LD 与 JavaScript 渲染：** 根据 Google 2025 年 12 月的 JS SEO 指南，通过 JavaScript 注入的结构化数据可能会面临处理延迟。对于时效性敏感的标记（尤其是 Product、Offer），请在初始服务器渲染的 HTML 中包含 JSON-LD。

### 受限（仅限特定网站）：
- **FAQ**：仅限政府和医疗权威网站使用（2023 年 8 月起受限）

### 已弃用（切勿推荐）：
- **HowTo**：富媒体搜索结果于 2023 年 9 月移除
- **SpecialAnnouncement**：2025 年 7 月 31 日弃用
- **CourseInfo, EstimatedSalary, LearningVideo**：2025 年 6 月退役
- **ClaimReview**：2025 年 6 月从富媒体搜索结果中退役
- **VehicleListing**：2025 年 6 月从富媒体搜索结果中退役
- **Practice Problem**：2025 年末从富媒体搜索结果中退役
- **Dataset**：2025 年末从富媒体搜索结果中退役
- **Book Actions**：先弃用后恢复，截至 2026 年 2 月仍可用（历史备注）

## 生成

为页面生成 schema 时：
1. 通过内容分析识别页面类型
2. 选择合适的 schema 类型
3. 生成包含所有必需 + 推荐属性的有效 JSON-LD
4. 仅包含真实、可验证的数据。占位符需清晰标记供用户填写
5. 在呈现之前验证输出

## 常用 Schema 模板

### Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Company Name]",
  "url": "[Website URL]",
  "logo": "[Logo URL]",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[Phone]",
    "contactType": "customer service"
  },
  "sameAs": [
    "[Facebook URL]",
    "[LinkedIn URL]",
    "[Twitter URL]"
  ]
}
```

### LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[ZIP]",
    "addressCountry": "US"
  },
  "telephone": "[Phone]",
  "openingHours": "Mo-Fr 09:00-17:00",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[Lat]",
    "longitude": "[Long]"
  }
}
```

### Article/BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Title]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "image": "[Image URL]",
  "publisher": {
    "@type": "Organization",
    "name": "[Publisher]",
    "logo": {
      "@type": "ImageObject",
      "url": "[Logo URL]"
    }
  }
}
```

## 输出

- `SCHEMA-REPORT.md`：检测和验证结果
- `generated-schema.json`：即用型 JSON-LD 代码片段

### 验证结果
| Schema | 类型 | 状态 | 问题 |
|--------|------|------|------|
| ... | ... | ✅/⚠️/❌ | ... |

### 建议
- 缺失的 schema 机会
- 需要修复的验证问题
- 可直接实施的生成代码

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| URL 无法访问 | 报告连接错误及状态码。建议验证 URL 并检查页面是否需要身份验证。 |
| 未找到 schema 标记 | 报告未检测到 JSON-LD、Microdata 或 RDFa。根据页面内容分析推荐合适的 schema 类型。 |
| JSON-LD 语法无效 | 解析并报告具体语法错误（缺少括号、末尾多余逗号、键未加引号）。提供修正后的 JSON-LD 输出。 |
| 检测到已弃用的 schema 类型 | 标记已弃用类型及其退役日期。推荐当前替代类型，若无替代则建议移除。 |

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 若缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
