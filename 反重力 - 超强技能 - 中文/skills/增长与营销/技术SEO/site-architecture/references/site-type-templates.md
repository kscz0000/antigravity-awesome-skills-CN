# 网站类型模板

针对常见网站类型的完整页面层级模板，包含 ASCII 树、URL 映射和导航建议。

---

## SaaS 营销网站

### 页面层级

```
Homepage (/)
├── Features (/features)
│   ├── Feature A (/features/feature-a)
│   ├── Feature B (/features/feature-b)
│   └── Feature C (/features/feature-c)
├── Pricing (/pricing)
├── Customers (/customers)
│   ├── Case Study 1 (/customers/company-name)
│   └── Case Study 2 (/customers/company-name-2)
├── Resources (/resources)
│   ├── Blog (/blog)
│   │   └── [Posts] (/blog/post-slug)
│   ├── Templates (/resources/templates)
│   │   └── [Template] (/resources/templates/template-slug)
│   └── Guides (/resources/guides)
│       └── [Guide] (/resources/guides/guide-slug)
├── Integrations (/integrations)
│   └── [Integration] (/integrations/integration-name)
├── Docs (/docs)
│   ├── Getting Started (/docs/getting-started)
│   ├── Guides (/docs/guides)
│   └── API Reference (/docs/api)
├── About (/about)
│   ├── Careers (/about/careers)
│   └── Contact (/contact)
├── Compare (/compare)
│   └── [Competitor] (/compare/competitor-name)
├── Privacy (/privacy)
└── Terms (/terms)
```

### URL 映射

| 页面 | URL | 导航位置 | 优先级 |
|------|-----|----------|--------|
| 首页 | `/` | 页头 (logo) | 关键 |
| 功能 | `/features` | 页头 | 高 |
| 功能页面 | `/features/{slug}` | 页头下拉菜单 | 中 |
| 定价 | `/pricing` | 页头 | 关键 |
| 客户 | `/customers` | 页头 | 中 |
| 案例研究 | `/customers/{slug}` | 客户下拉菜单 | 中 |
| 博客 | `/blog` | 页头 (Resources) | 高 |
| 博客文章 | `/blog/{slug}` | — | 中 |
| 集成 | `/integrations` | 页头 | 中 |
| 文档 | `/docs` | 页头 | 中 |
| 比较 | `/compare/{slug}` | 页脚 | 高 (SEO) |
| 关于 | `/about` | 页脚 | 低 |
| 定价 CTA | `/pricing` | 页头 (CTA 按钮) | 关键 |

### 导航

**页头 (6 个项目 + CTA)**: Features | Pricing | Customers | Resources | Integrations | Docs | [Get Started]

**页脚列**:
- Product: Features, Pricing, Integrations, Changelog, Security
- Resources: Blog, Templates, Guides, Case Studies
- Company: About, Careers, Contact, Press
- Legal: Privacy, Terms, Security

---

## 内容 / 博客网站

### 页面层级

```
Homepage (/)
├── Blog (/blog)
│   ├── [Category: Topic A] (/blog/category/topic-a)
│   ├── [Category: Topic B] (/blog/category/topic-b)
│   ├── [Category: Topic C] (/blog/category/topic-c)
│   └── [Posts] (/blog/post-slug)
├── Newsletter (/newsletter)
├── Resources (/resources)
│   ├── Guides (/resources/guides)
│   │   └── [Guide] (/resources/guides/guide-slug)
│   └── Tools (/resources/tools)
│       └── [Tool] (/resources/tools/tool-slug)
├── About (/about)
├── Contact (/contact)
├── Privacy (/privacy)
└── Terms (/terms)
```

### URL 映射

| 页面 | URL | 导航位置 | 优先级 |
|------|-----|----------|--------|
| 首页 | `/` | 页头 (logo) | 关键 |
| 博客索引 | `/blog` | 页头 | 高 |
| 分类 | `/blog/category/{slug}` | 页头下拉菜单 | 中 |
| 文章 | `/blog/{slug}` | — | 中 |
| Newsletter | `/newsletter` | 页头 (CTA) | 高 |
| 指南 | `/resources/guides` | 页头 | 中 |
| 关于 | `/about` | 页头 | 低 |

### 导航

**页头 (4 个项目 + CTA)**: Blog | Resources | About | Contact | [Subscribe]

**侧边栏** (在博客上): 分类、热门文章、Newsletter 注册

---

## 电商网站

### 页面层级

```
Homepage (/)
├── Shop (/shop)
│   ├── Category A (/shop/category-a)
│   │   ├── Subcategory (/shop/category-a/subcategory)
│   │   │   └── [Product] (/shop/category-a/subcategory/product-slug)
│   │   └── [Product] (/shop/category-a/product-slug)
│   ├── Category B (/shop/category-b)
│   │   └── [Product] (/shop/category-b/product-slug)
│   └── Category C (/shop/category-c)
│       └── [Product] (/shop/category-c/product-slug)
├── Collections (/collections)
│   └── [Collection] (/collections/collection-slug)
├── Sale (/sale)
├── Blog (/blog)
│   └── [Posts] (/blog/post-slug)
├── About (/about)
│   └── Our Story (/about/our-story)
├── Help (/help)
│   ├── FAQ (/help/faq)
│   ├── Shipping (/help/shipping)
│   ├── Returns (/help/returns)
│   └── Contact (/contact)
├── Cart (/cart)
├── Account (/account)
├── Privacy (/privacy)
└── Terms (/terms)
```

### URL 映射

| 页面 | URL | 导航位置 | 优先级 |
|------|-----|----------|--------|
| 首页 | `/` | 页头 (logo) | 关键 |
| 商店 | `/shop` | 页头 | 关键 |
| 分类 | `/shop/{category}` | 页头大型菜单 | 高 |
| 产品 | `/shop/{category}/{product}` | — | 高 |
| 系列 | `/collections/{slug}` | 页头 | 中 |
| 促销 | `/sale` | 页头 (高亮) | 高 |
| 购物车 | `/cart` | 页头 (图标) | 关键 |
| 账户 | `/account` | 页头 (图标) | 中 |

### 导航

**页头 (5 个项目 + 购物车/账户)**: Shop (大型菜单) | Collections | Sale | Blog | Help | [Cart icon] [Account icon]

**Shop 下的大型菜单**: 带有特色产品/图片的分类列

---

## 文档网站

### 页面层级

```
Docs Home (/docs)
├── Getting Started (/docs/getting-started)
│   ├── Installation (/docs/getting-started/installation)
│   ├── Quick Start (/docs/getting-started/quick-start)
│   └── Configuration (/docs/getting-started/configuration)
├── Guides (/docs/guides)
│   ├── Guide A (/docs/guides/guide-a)
│   ├── Guide B (/docs/guides/guide-b)
│   └── Guide C (/docs/guides/guide-c)
├── API Reference (/docs/api)
│   ├── Authentication (/docs/api/authentication)
│   ├── Endpoints (/docs/api/endpoints)
│   └── Webhooks (/docs/api/webhooks)
├── Examples (/docs/examples)
│   └── [Example] (/docs/examples/example-slug)
├── Changelog (/docs/changelog)
└── FAQ (/docs/faq)
```

### URL 映射

| 页面 | URL | 导航位置 | 优先级 |
|------|-----|----------|--------|
| 文档首页 | `/docs` | 页头 | 高 |
| 快速开始 | `/docs/getting-started` | 侧边栏 (顶部) | 关键 |
| 指南 | `/docs/guides` | 侧边栏 | 高 |
| API 参考 | `/docs/api` | 侧边栏 | 高 |
| 更新日志 | `/docs/changelog` | 侧边栏 (底部) | 低 |

### 导航

**页头**: Docs | API | Blog | Community | GitHub | [Dashboard]

**侧边栏** (持久，左侧): Getting Started, Guides, API Reference, Examples, Changelog — 带有可展开的子部分

**页面内**: 每个文档页面底部的上一页/下一页导航

---

## 混合 SaaS + 内容

### 页面层级

```
Homepage (/)
├── Product (/product)
│   ├── Feature A (/product/feature-a)
│   ├── Feature B (/product/feature-b)
│   └── Feature C (/product/feature-c)
├── Solutions (/solutions)
│   ├── By Use Case (/solutions/use-case-slug)
│   └── By Industry (/solutions/industry-slug)
├── Pricing (/pricing)
├── Blog (/blog)
│   ├── [Category] (/blog/category/slug)
│   └── [Posts] (/blog/post-slug)
├── Resources (/resources)
│   ├── Guides (/resources/guides)
│   ├── Templates (/resources/templates)
│   ├── Webinars (/resources/webinars)
│   └── Case Studies (/resources/case-studies)
├── Docs (/docs)
│   ├── Getting Started (/docs/getting-started)
│   └── API (/docs/api)
├── Integrations (/integrations)
│   └── [Integration] (/integrations/slug)
├── Compare (/compare)
│   └── [Competitor] (/compare/competitor-slug)
├── About (/about)
│   ├── Careers (/about/careers)
│   └── Contact (/contact)
├── Privacy (/privacy)
└── Terms (/terms)
```

### 导航

**页头 (7 个项目 + CTA)**: Product | Solutions | Pricing | Resources | Blog | Docs | Integrations | [Start Free Trial]

为 Product（功能列表）、Solutions（使用场景 + 行业）和 Resources（博客、指南、模板、网络研讨会、案例研究）使用大型菜单。

---

## 小型企业 / 本地业务

### 页面层级

```
Homepage (/)
├── Services (/services)
│   ├── Service A (/services/service-a)
│   ├── Service B (/services/service-b)
│   └── Service C (/services/service-c)
├── About (/about)
├── Testimonials (/testimonials)
├── Blog (/blog)
│   └── [Posts] (/blog/post-slug)
├── Contact (/contact)
├── Privacy (/privacy)
└── Terms (/terms)
```

### URL 映射

| 页面 | URL | 导航位置 | 优先级 |
|------|-----|----------|--------|
| 首页 | `/` | 页头 (logo) | 关键 |
| 服务 | `/services` | 页头 | 高 |
| 服务页面 | `/services/{slug}` | 页头下拉菜单 | 高 |
| 关于 | `/about` | 页头 | 中 |
| 客户评价 | `/testimonials` | 页头 | 中 |
| 博客 | `/blog` | 页头 | 中 |
| 联系我们 | `/contact` | 页头 (CTA) | 高 |

### 导航

**页头 (5 个项目 + CTA)**: Services | About | Testimonials | Blog | [Contact Us]

保持简单。小型企业网站应该是扁平的（最多 1-2 层级）。每个页面都应该可以从页头访问。