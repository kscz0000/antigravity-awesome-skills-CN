# 导航模式

针对不同网站类型和上下文的详细导航模式。

---

## 页头导航

### 简单页头（4-6 个项目）

最适合：小型企业、简单 SaaS、个人作品集。

```
[Logo]   Features   Pricing   Blog   About   [CTA Button]
```

规则：
- Logo 始终链接到首页
- CTA 按钮在最右侧，视觉上突出（填充按钮、对比色）
- 项目按优先级排序（访问量最多的在前）
- 当前页面获得视觉指示器（下划线、加粗、颜色）

### 大型菜单页头

最适合：功能丰富的 SaaS、带分类的电商、大型内容网站。

```
[Logo]   Product ▾   Solutions ▾   Resources ▾   Pricing   Docs   [CTA]
```

当悬停/点击 "Product" 时：

```
┌─────────────────────────────────────────────────┐
│  Features           Platform        Integrations │
│  ─────────          ─────────       ──────────── │
│  Analytics           Security       Slack         │
│  Automation          API            HubSpot       │
│  Reporting           Compliance     Salesforce    │
│  Dashboards                         Zapier        │
│                                                   │
│  [See all features →]                             │
└─────────────────────────────────────────────────┘
```

大型菜单规则：
- 最多 2-4 列
- 按逻辑分组项目（按功能区域、使用场景或受众）
- 底部包含"查看全部"链接
- 不要在大型菜单内嵌套下拉菜单
- 当标签本身不够清晰时，为项目显示描述

### 分割导航

最适合：同时具有营销和产品导航的应用。

```
[Logo]   Features   Pricing   Blog        [Login]   [Sign Up]
├── Marketing nav (left) ──────┘          └── Auth nav (right) ──┤
```

右侧处理身份验证操作。左侧处理页面导航。

---

## 页脚导航

### 基于列的页脚（标准）

最适合：大多数网站。将链接组织成 3-5 个主题列。

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Product          Resources        Company       Legal   │
│  ─────────        ──────────       ─────────     ─────   │
│  Features         Blog             About         Privacy │
│  Pricing          Guides           Careers       Terms   │
│  Integrations     Templates        Contact       GDPR    │
│  Changelog        Case Studies     Press                 │
│  Security         Webinars         Partners              │
│                                                          │
│  [Logo]  © 2026 Company Name                             │
│  Social: [Twitter] [LinkedIn] [GitHub]                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 极简页脚

最适合：简单网站、落地页。

```
┌──────────────────────────────────────────────────────────┐
│  [Logo]                                                  │
│  © 2026 Company  ·  Privacy  ·  Terms  ·  Contact        │
└──────────────────────────────────────────────────────────┘
```

### 扩展页脚

最适合：使用页脚进行 SEO 的网站（比较页面、位置页面、资源链接）。

```
┌──────────────────────────────────────────────────────────┐
│  Product     Resources    Compare         Use Cases      │
│  Features    Blog         vs Competitor A  For Startups  │
│  Pricing     Guides       vs Competitor B  For Enterprise│
│  API         Templates    vs Competitor C  For Agencies  │
│                                                          │
│  Integrations             Popular Posts                  │
│  Slack       Zapier       How to Do X                    │
│  HubSpot     Salesforce   Guide to Y                     │
│                           Template: Z                    │
│                                                          │
│  [Logo]  © 2026  ·  Privacy  ·  Terms  ·  Security      │
└──────────────────────────────────────────────────────────┘
```

---

## 侧边栏导航

### 文档侧边栏

持久的左侧边栏，带有可折叠的部分。

```
Getting Started
  ├── Installation
  ├── Quick Start
  └── Configuration

Guides
  ├── Authentication
  ├── Data Models
  └── Deployment

API Reference
  ├── REST API
  │   ├── Users
  │   ├── Projects
  │   └── Webhooks
  └── GraphQL

Examples
  ├── Next.js
  ├── Rails
  └── Python

Changelog
```

规则：
- 当前页面高亮显示
- 部分可折叠（活动部分默认展开）
- 侧边栏顶部有搜索
- 内容区域底部有"上一页/下一页"页面导航
- 滚动时固定（不会滚走）

### 博客分类侧边栏

```
Categories
  ├── SEO (24)
  ├── CRO (18)
  ├── Content (15)
  ├── Paid Ads (12)
  └── Analytics (9)

Popular Posts
  ├── How to Improve SEO
  ├── Landing Page Guide
  └── Analytics Setup

Newsletter
  └── [Email signup form]
```

---

## 面包屑导航

### 标准格式

```
Home > Features > Analytics
Home > Blog > SEO Category > How to Do Keyword Research
Home > Docs > API Reference > Authentication
```

规则：
- 分隔符：`>` 或 `/`（保持一致）
- 除当前页面外，每个段都是链接
- 当前页面是纯文本（不链接）
- 如果标题已作为 H1 可见，则不包含当前页面

### 带 Schema 标记

```html
<nav aria-label="Breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/"><span itemprop="name">Home</span></a>
      <meta itemprop="position" content="1" />
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/features"><span itemprop="name">Features</span></a>
      <meta itemprop="position" content="2" />
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">Analytics</span>
      <meta itemprop="position" content="3" />
    </li>
  </ol>
</nav>
```

或使用 JSON-LD（推荐）：

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Features", "item": "https://example.com/features" },
    { "@type": "ListItem", "position": 3, "name": "Analytics" }
  ]
}
```

---

## 移动端导航

### 汉堡菜单

移动端标准。所有导航项折叠到一个菜单图标中。

规则：
- 汉堡图标（三条线）在右上角或左上角
- 全屏或滑出面板
- CTA 按钮无需打开菜单即可可见（粘性页头）
- 搜索可从移动菜单访问
- 嵌套项目使用手风琴模式

### 底部标签栏

最适合：Web 应用、PWA、移动优先产品。

```
┌──────────────────────────────────────┐
│                                      │
│           [Page Content]             │
│                                      │
├──────────────────────────────────────┤
│  Home    Search    Create    Profile │
│   🏠       🔍        ➕       👤    │
└──────────────────────────────────────┘
```

规则：
- 最多 3-5 个项目
- 图标 + 标签（不只是图标）
- 活动状态清晰指示
- 最重要的操作在中间

---

## 反模式

### 需要避免的事项

- **页头项目过多**（8+）：导致决策瘫痪，导航在较小屏幕上变得不可读
- **下拉菜单嵌套**：下拉菜单内嵌套下拉菜单再嵌套下拉菜单
- **神秘图标**：没有标签的图标——用户不知道它们是什么意思
- **隐藏主要导航**：在桌面上将重要页面埋在汉堡菜单中
- **页面间导航不一致**：导航应在整个网站保持一致（应用与营销除外）
- **不考虑移动端**：桌面导航无法转化为移动端
- **页脚作为站点地图转储**：页脚中有 50 多个链接没有组织
- **面包屑与 URL 不匹配**：面包屑显示"Products > Widget"但 URL 是 `/shop/widget-pro`

### 常见修复

| 问题 | 修复方案 |
|------|----------|
| 导航项过多 | 分组到下拉菜单或大型菜单中 |
| 用户找不到页面 | 添加搜索，改进标签 |
| 导航跳出率高 | 简化选择，使用更清晰的标签 |
| SEO 页面未链接 | 添加到页脚或资源部分 |
| 移动导航损坏 | 在真实设备上测试，使用汉堡模式 |

---

## SEO 导航

导航中的内部链接传递 PageRank。战略性地使用这一点：

- **页头导航链接最强** — 将最重要的页面放在这里
- **页脚链接传递的价值较低** — 适合比较页面、位置页面
- **侧边栏链接**有助于部分级别的权威性 — 适合博客类别、文档部分
- **面包屑**为搜索引擎提供结构信号 — 使用 schema 标记实现
- **不要使用纯 JavaScript 导航** — 搜索引擎需要可爬取的 HTML 链接
- **使用描述性锚文本** — "Analytics Features"而不只是"Features"