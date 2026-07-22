<!-- Updated: 2026-02-07 -->
# 代理机构/咨询公司SEO策略模板

## 行业特征

- 服务型、高价值交易
- 专业性和信任至关重要
- 长考虑周期
- 作品集/案例研究驱动决策
- 关系型销售
- 利基专业化优势

## 推荐网站架构

```
/
├── Home
├── /services
│   ├── /service-1
│   │   ├── /sub-service-1
│   │   └── ...
│   └── /service-2
├── /industries
│   ├── /industry-1
│   ├── /industry-2
│   └── ...
├── /work (or /case-studies)
│   ├── /case-study-1
│   ├── /case-study-2
│   └── ...
├── /about
│   ├── /team
│   │   ├── /team-member-1
│   │   └── ...
│   ├── /culture
│   └── /careers
├── /insights (or /blog)
│   ├── /articles
│   ├── /guides
│   ├── /webinars
│   └── /podcasts
├── /contact
├── /process
└── /faq
```

## Schema推荐

| 页面类型 | Schema类型 |
|----------|-----------|
| 首页 | Organization, ProfessionalService |
| 服务页面 | Service, ProfessionalService |
| 案例研究 | Article, Organization（客户） |
| 团队成员 | Person, ProfilePage |
| 博客 | Article, BlogPosting |

### ProfessionalService Schema示例
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Agency Name",
  "description": "What the agency does",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Agency St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345"
  },
  "telephone": "+1-555-555-5555",
  "areaServed": "National",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Service 1"
        }
      }
    ]
  }
}
```

## E-E-A-T要求

### 团队页面必须包含
- 专业头像
- 含资质的详细简介
- 行业经验
- 演讲活动
- 发表作品
- 社交资料

### 案例研究必须包含
- 客户名称（经许可）或行业
- 挑战/问题陈述
- 方法/方法论
- 含具体指标的结果
- 时间线
- 客户评价引述

## 内容优先级

### 高优先级
1. 服务页面（详细、具体）
2. 行业页面（垂直专业）
3. 3-5个详细案例研究
4. 团队/领导层页面

### 中优先级
1. 方法论/流程页面
2. 思想领导力博客
3. 对比内容（vs 替代方案）
4. FAQ页面

### 思想领导力主题
- 行业趋势分析
- 操作指南（非竞争性）
- 原创研究/调查
- 活动回顾和洞察
- 专家访谈
- 工具/技术评测

## 内容策略

### 服务页面（最少800字）
- 清晰的价值主张
- 方法论概览
- 交付物清单
- 相关案例研究
- 提供该服务的团队成员
- 预约咨询CTA

### 行业页面（最少800字）
- 行业特定挑战
- 您如何以不同方式解决
- 相关案例研究
- 行业资质/经验
- 客户Logo（经许可）

### 案例研究（最少1,000字）
- 执行摘要
- 客户背景
- 挑战详情
- 解决方案方法
- 实施过程
- 可衡量结果
- 客户评价
- 相关服务/CTA

## 关键追踪指标

- 服务页面的自然流量
- 案例研究页面浏览量
- 自然搜索的联系表单提交
- 关键内容的页面停留时间
- 博客→服务页面转化

## 代理机构的生成式引擎优化（GEO）

- [ ] 发布包含具体、可引用指标和结果的原创案例研究
- [ ] 为所有团队成员使用含sameAs链接的Person Schema（建立实体权威）
- [ ] 为团队成员页面使用ProfilePage Schema
- [ ] 在服务页面描述中包含清晰、可引用的专业性声明
- [ ] 产出AI系统可引用的原创行业研究和调查
- [ ] 以清晰的标题和可提取的洞察组织思想领导力内容
- [ ] 在目录、社交资料和行业网站中保持一致的机构实体信息
- [ ] 监控ChatGPT、Perplexity和Google AI Overviews中品牌和关键服务术语的AI引用
