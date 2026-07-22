<!-- Updated: 2026-02-07 -->
# 电商SEO策略模板

## 行业特征

- 高交易意图
- 产品比较行为
- 价格敏感
- 视觉优先决策
- 季节性需求模式
- 竞争性市场平台列表

## 推荐网站架构

```
/
├── Home
├── /collections (or /categories)
│   ├── /category-1
│   │   ├── /subcategory-1
│   │   └── ...
│   ├── /category-2
│   └── ...
├── /products
│   ├── /product-1
│   ├── /product-2
│   └── ...
├── /brands
│   ├── /brand-1
│   └── ...
├── /sale (or /deals)
├── /new-arrivals
├── /best-sellers
├── /gift-guide
├── /blog
│   ├── /buying-guides
│   ├── /how-to
│   └── /trends
├── /about
├── /contact
├── /shipping
├── /returns
└── /faq
```

## Schema推荐

| 页面类型 | Schema类型 |
|----------|-----------|
| 产品页 | Product, Offer, AggregateRating, Review, BreadcrumbList |
| 分类页 | CollectionPage, ItemList, BreadcrumbList |
| 品牌页 | Brand, Organization |
| 博客 | Article, BlogPosting |

### 额外电商Schema（2025）

- **ProductGroup**：用于有变体（尺码、颜色）的产品。用 `variesBy` 和 `hasVariant` 属性包裹单个Product条目。参见 `schema/templates.json`。
- **Certification**：用于产品认证（Energy Star、安全、有机）。已替代EnergyConsumptionDetails（2025年4月）。在Product上使用 `hasCertification`。
- **OfferShippingDetails**：包含运费、处理时间和运输时间。对Merchant Center资格至关重要。

> **Google Merchant Center免费列表：** 产品可以免费出现在Google Shopping中。确保Product结构化数据在初始服务器渲染的HTML中（而非JavaScript注入），并包含必需属性：`name`、`image`、`price`、`priceCurrency`、`availability`。

> **JS渲染注意：** Product结构化数据应在初始服务器渲染的HTML中：不要通过JavaScript动态注入（根据2025年12月Google JS SEO指南）。

### Product Schema示例
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": ["https://example.com/product.jpg"],
  "description": "Product description",
  "sku": "SKU123",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "price": "99.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/product"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "42"
  }
}
```

## 内容要求

### 产品页面（最少400字）
- 独特的产品描述（非制造商文案）
- 功能亮点
- 使用场景/适用人群
- 规格表格
- 尺码/合身指南（服装类）
- 保养说明
- 客户评价

### 分类页面（最少400字）
- 分类介绍
- 购买指南摘要
- 精选产品
- 子分类链接
- 筛选/排序选项

## 技术考量

### 分页
- 使用rel="next"/rel="prev"或加载更多
- 确保所有产品可被抓取
- 规范链接指向主分类页

### 分面导航
- 对创建重复内容的筛选组合使用noindex
- 适当使用canonical标签
- 确保热门筛选可被索引

### 产品变体
- 父产品及变体使用单一URL
- 或使用独立URL并canonical指向父产品
- 所有变体都需结构化数据

## 内容优先级

### 高优先级
1. 分类页面（顶级）
2. 畅销产品页面
3. 首页
4. 主要分类的购买指南

### 中优先级
1. 子分类页面
2. 品牌页面
3. 对比内容
4. 季节性落地页

### 博客主题
- 购买指南（"如何选择……"）
- 产品对比
- 趋势报告
- 使用场景和灵感
- 保养和维护指南

## 关键追踪指标

- 自然搜索收入
- 产品页面排名
- 分类页面排名
- 点击率（富媒体结果）
- 自然流量平均订单价值

## 电商的生成式引擎优化（GEO）

AI搜索平台越来越多地直接回答产品查询。针对AI引用进行优化：

- [ ] 以结构化格式包含清晰的产品规格、尺寸、材质
- [ ] 对变体产品使用ProductGroup Schema
- [ ] 提供原创产品摄影，配有描述性alt文本
- [ ] 包含真实客户评价内容（AggregateRating Schema）
- [ ] 在所有平台（网站、Amazon、Merchant Center）保持一致的产品实体数据
- [ ] 以AI可解析的清晰功能表格组织对比内容
- [ ] 为常见产品问题添加详细的FAQ内容
