---
name: schema-markup-generator
description: "为 Web 应用、博客、FAQ 和 SaaS 站点生成并实现 JSON-LD 结构化数据。支持 WebSite、SoftwareApplication、BlogPosting、FAQPage、HowTo 等类型。触发词：schema、结构化数据、JSON-LD、rich results、富摘要、Schema.org、structured data"
category: seo
risk: safe
source: self
source_type: self
date_added: "2026-05-31"
author: Whoisabhishekadhikari
tags: [seo, schema, json-ld, structured-data, rich-results, nextjs, technical-seo]
tools: [claude, cursor, gemini, claude-code]
version: 1.0.0
---

# Schema 标记生成器技能

为页面添加 JSON-LD 结构化数据，解锁富摘要结果、提升 CTR，并向 Google 和 AI 系统传递页面上下文信号。

---

## 何时使用

- 在为网站、SaaS 应用、工具页、文章、FAQ、面包屑或组织页面添加或审计 JSON-LD schema 时使用。
- 当 schema 需要在 Next.js App Router 中实现，或需通过 Google Rich Results 和 Schema.org 工具验证时使用。
- 当页面内容质量高但缺少面向搜索引擎和富摘要资格的结构化数据时使用。

---

## 如何在 Next.js App Router 中添加 Schema

最干净的方式是创建一个可复用的 `JsonLd` 组件：

```jsx
// components/JsonLd.jsx
export function JsonLd({ data }) {
  const json = JSON.stringify(data).replace(/</g, '\\u003c');
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: json }}
    />
  );
}
```

在任意页面中使用：

```jsx
import { JsonLd } from '@/components/JsonLd';

export default function MyPage() {
  return (
    <>
      <JsonLd data={mySchemaObject} />
      {/* rest of page */}
    </>
  );
}
```

---

## 按页面类型选择 Schema 类型

### WebSite + Sitelinks Searchbox（仅首页）

```js
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "100 SEO Tools",
  "url": "https://www.100seotools.com",
  "description": "Free online SEO tools for keyword research, technical audits, and more.",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://www.100seotools.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

### SoftwareApplication（工具 / SaaS 应用页面）

```js
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Keyword Density Checker",
  "applicationCategory": "WebApplication",
  "operatingSystem": "Web",
  "url": "https://www.100seotools.com/tools/keyword-density-checker",
  "description": "Free keyword density checker tool. Analyze keyword frequency and optimize your content for SEO.",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "featureList": [
    "Analyze keyword frequency",
    "Detect over-optimization",
    "Export results as CSV"
  ],
  "provider": {
    "@type": "Organization",
    "name": "100 SEO Tools",
    "url": "https://www.100seotools.com"
  }
}
```

---

### Article / BlogPosting（博客文章）

```js
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How to Improve Your Core Web Vitals in 2025",
  "description": "A practical guide to improving LCP, FID, and CLS scores for better rankings.",
  "url": "https://www.100seotools.com/blog/improve-core-web-vitals",
  "datePublished": "2025-01-15",
  "dateModified": "2025-03-20",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "url": "https://www.100seotools.com/author/jane-smith"
  },
  "publisher": {
    "@type": "Organization",
    "name": "100 SEO Tools",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.100seotools.com/logo.png"
    }
  },
  "image": {
    "@type": "ImageObject",
    "url": "https://www.100seotools.com/images/blog/core-web-vitals.jpg",
    "width": 1200,
    "height": 630
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.100seotools.com/blog/improve-core-web-vitals"
  }
}
```

---

### FAQPage（FAQ 区域、工具帮助页面）

```js
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is keyword density?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Keyword density is the percentage of times a keyword appears in a piece of content relative to the total word count. A healthy keyword density is typically 1-3%."
      }
    },
    {
      "@type": "Question",
      "name": "Is this tool free to use?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, our keyword density checker is completely free with no registration required."
      }
    }
  ]
}
```

---

### HowTo（分步工具指南）

```js
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Check Keyword Density",
  "description": "Step-by-step guide to analyzing keyword density using our free tool.",
  "totalTime": "PT2M",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Paste your content",
      "text": "Copy your article or webpage content and paste it into the text area.",
      "image": "https://www.100seotools.com/images/how-to/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Enter your target keyword",
      "text": "Type the keyword you want to analyze in the keyword field."
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "Click Analyze",
      "text": "Press the Analyze button to get your keyword density report instantly."
    }
  ]
}
```

---

### BreadcrumbList（所有非首页页面）

```js
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.100seotools.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "SEO Tools",
      "item": "https://www.100seotools.com/tools"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Keyword Density Checker",
      "item": "https://www.100seotools.com/tools/keyword-density-checker"
    }
  ]
}
```

---

### Organization（关于页面、联系页面）

```js
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "100 SEO Tools",
  "url": "https://www.100seotools.com",
  "logo": "https://www.100seotools.com/logo.png",
  "sameAs": [
    "https://twitter.com/100seotools",
    "https://www.linkedin.com/company/100seotools"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "hello@100seotools.com"
  }
}
```

---

## 在同一页面组合多个 Schema

一个工具页面可以同时包含 BreadcrumbList + SoftwareApplication + FAQPage：

```jsx
export default function ToolPage() {
  return (
    <>
      <JsonLd data={breadcrumbSchema} />
      <JsonLd data={softwareApplicationSchema} />
      <JsonLd data={faqSchema} />
      {/* page content */}
    </>
  );
}
```

每个 schema 放在独立的 `<script>` 标签中 — 不要将它们合并为一个对象。

---

## 验证

部署前务必验证 schema：

1. **Google Rich Results Test** — https://search.google.com/test/rich-results
2. **Schema.org Validator** — https://validator.schema.org/
3. **Google Search Console** → 增强功能 → 部署后检查警告

```bash
# Quick check: schema appears in HTML
curl -s https://www.yourdomain.com/tools/keyword-density | grep -A 5 "application/ld+json"
```

---

## Schema 标记检查清单

- [ ] 首页有 `WebSite` schema
- [ ] 工具/应用页面有 `SoftwareApplication` schema
- [ ] 博客文章有 `BlogPosting` / `Article` schema
- [ ] FAQ 区域有 `FAQPage` schema
- [ ] 分步指南有 `HowTo` schema
- [ ] 所有非首页页面有 `BreadcrumbList`
- [ ] 关于/联系页面有 `Organization` schema
- [ ] schema 中所有 URL 均为绝对 HTTPS 地址
- [ ] 已通过 Google Rich Results Test 验证
- [ ] Google Search Console 中无 schema 错误

## 局限性

- 不保证富摘要资格或展示；Google 及其他消费者决定是否使用有效的 schema。
- 生成的示例必须根据网站的真实内容、法律实体详情、评分、定价和可用性进行适配。
- 务必验证部署后的 HTML，而非仅验证源代码，因为框架和渲染模式可能改变最终标记。