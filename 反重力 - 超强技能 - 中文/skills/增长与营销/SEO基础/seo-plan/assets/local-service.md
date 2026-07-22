<!-- Updated: 2026-02-07 -->
# 本地服务企业SEO策略模板

## 行业特征

- 地理定位搜索
- 高意图、快速决策
- 评价严重影响决策
- 电话是主要转化方式
- 移动优先用户行为
- 紧急/急迫服务需求

## 推荐网站架构

```
/
├── Home
├── /services
│   ├── /service-1
│   ├── /service-2
│   └── ...
├── /locations
│   ├── /city-1
│   │   ├── /service-1-city-1
│   │   └── ...
│   ├── /city-2
│   └── ...
├── /about
├── /reviews
├── /gallery (or /portfolio)
├── /blog
├── /contact
├── /emergency (if applicable)
└── /faq
```

## 质量门控

### 位置页面限制
- ⚠️ 30+位置页面时**警告**
- 🛑 50+位置页面时**硬性停止**

### 独特内容要求
| 页面类型 | 最低字数 | 独特% |
|----------|---------|-------|
| 主要位置页 | 600 | 60%+ |
| 服务区域页 | 500 | 40%+ |
| 服务页面 | 800 | 100% |

### 什么使位置页面独特
- 当地地标和社区
- 该位置提供的特定服务
- 当地团队成员
- 特定位置的客户评价
- 社区参与
- 当地法规或注意事项

## Schema推荐

| 页面类型 | Schema类型 |
|----------|-----------|
| 首页 | LocalBusiness, Organization |
| 服务页面 | Service, LocalBusiness |
| 位置页面 | LocalBusiness（含地理坐标） |
| 联系 | ContactPage, LocalBusiness |
| 评价 | LocalBusiness（含AggregateRating） |

### LocalBusiness Schema示例
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345"
  },
  "telephone": "+1-555-555-5555",
  "openingHours": "Mo-Fr 08:00-18:00",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  },
  "areaServed": ["City 1", "City 2"],
  "priceRange": "$$"
}
```

## Google Business Profile集成

- 确保NAP一致性（名称、地址、电话）
- 同步服务类别
- 定期发布更新
- 照片上传
- 评价回复策略

### Google Business Profile更新（2025-2026）

- **视频验证**现已成为标准：明信片验证已基本淘汰。准备好展示营业地点或服务区域的短视频验证流程。
- **WhatsApp集成**替代了Google Business Chat（已弃用）。商家可以连接WhatsApp作为主要消息渠道。
- **问答功能从Maps中移除**：由AI生成的答案替代。确保您的GBP描述、服务和网站FAQ全面完整，因为Google AI会使用它们来回答查询。
- **营业时间是前5大排名因素**："搜索时营业中"首次被列为顶级独立因素（Whitespark 2026年本地搜索排名因素报告）。保持营业时间准确；如可行，考虑延长营业时间。
- **评价"Stories"格式**：Google Maps现在在移动端以可滑动的Stories格式显示评价摘要。鼓励带有照片的详细、描述性评价。

### 服务区域商家（SAB）更新（2025年6月）

Google更新了SAB指南，**不允许**将整个州或国家作为服务区域。SAB必须指定：城市、邮政编码或社区。如果您服务整个都市区，请列出其中的主要城市而非整个州。

### 本地商家的AI可见性

AI Overviews仅出现在约0.14%的本地关键词中（2025年3月数据），本地SEO面临的AI干扰远少于其他领域。然而，ChatGPT和Perplexity越来越多地用于本地推荐。

针对AI本地可见性优化：
- 确保出现在专家策划的"最佳"列表中（Whitespark 2026年报告中排名第1的AI可见性因素）
- 在所有平台保持一致的NAP（名称、地址、电话）
- 建立真实的评价数量和质量
- 使用包含完整属性的LocalBusiness Schema（geo、openingHours、priceRange、areaServed）

## 内容优先级

### 高优先级
1. 包含清晰服务区域的首页
2. 核心服务页面
3. 主要城市页面
4. 包含所有位置的联系方式页面

### 中优先级
1. 服务+位置组合页面
2. FAQ页面
3. 关于/团队页面
4. 评价/客户推荐页面

### 博客主题
- 季节性维护技巧
- 如何选择[服务提供商]
- [问题]的警示信号
- DIY vs 专业服务对比
- 当地法规和许可

## 关键追踪指标

- 本地包排名
- 自然搜索电话量
- 导航请求
- Google Business Profile洞察
- 评价数量和评分

## 本地业务的生成式引擎优化（GEO）

- [ ] 包含清晰、可引用的服务描述和价格范围
- [ ] 使用包含完整geo、openingHours和areaServed的LocalBusiness Schema
- [ ] 在策划的"最佳"和本地目录列表中建立存在
- [ ] 在所有平台（Google、Yelp、Apple Maps）保持一致的NAP
- [ ] 包含工作、团队和位置的原创照片
- [ ] 为常见本地服务问题组织FAQ内容
- [ ] 监控ChatGPT和Perplexity本地推荐中的AI引用
