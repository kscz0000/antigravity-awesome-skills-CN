<!-- Updated: 2026-02-07 -->
# 出版商/媒体SEO策略模板

## 行业特征

- 高内容量
- 时效性内容（新闻）
- 流量依赖广告收入
- 权威和信任至关重要
- 与社交平台竞争
- AI Overviews对流量的影响

## 推荐网站架构

```
/
├── Home
├── /news (or /latest)
├── /topics
│   ├── /topic-1
│   ├── /topic-2
│   └── ...
├── /authors
│   ├── /author-1
│   └── ...
├── /opinion
├── /reviews
├── /guides
├── /videos
├── /podcasts
├── /newsletter
├── /about
│   ├── /editorial-policy
│   ├── /corrections
│   └── /contact
└── /[year]/[month]/[slug] (article URLs)
```

## Schema推荐

| 页面类型 | Schema类型 |
|----------|-----------|
| 文章 | NewsArticle 或 Article, Person（作者）, Organization（出版商） |
| 作者页 | Person, ProfilePage |
| 主题页 | CollectionPage, ItemList |
| 首页 | WebSite, Organization |
| 视频 | VideoObject |
| 播客 | PodcastEpisode, PodcastSeries |

### NewsArticle Schema示例
```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "Article Headline",
  "datePublished": "2026-02-07T10:00:00Z",
  "dateModified": "2026-02-07T14:30:00Z",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/authors/author-name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publication Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "image": ["https://example.com/article-image.jpg"],
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article-url"
  }
}
```

## E-E-A-T要求

出版商面临最严格的E-E-A-T审查。

### 作者页面必须包含
- 全名和照片
- 简介和资质
- 专业领域
- 联系信息
- 社交资料（sameAs）
- 该作者的过往文章

### 编辑标准
- 明确的更正政策
- 透明的编辑流程
- 事实核查程序
- 利益冲突披露

## 内容优先级

### 高优先级
1. 突发新闻（速度至关重要）
2. 核心主题的常青指南
3. 含资质的作者页面
4. 主题中心/支柱页面

### 中优先级
1. 观点/分析文章
2. 视频内容
3. 互动内容
4. Newsletter落地页

### GEO考量
- 文章中包含清晰、可引用的事实
- 数据密集内容使用表格
- 带归属的专家引用
- 更新日期醒目显示
- 结构化标题（H2/H3）
- 第一方数据和原创研究被AI系统高度引用
- 确保作者实体通过Person Schema + sameAs链接清晰定义
- 监控Google AI Overviews、AI Mode、ChatGPT、Perplexity中的AI引用频率
- 将AI引用作为独立KPI与自然流量并列

### 出版商SEO更新（2025-2026）

- **Google News自动收录：** Google News不再接受手动申请（自2025年3月起）。收录完全基于Google的内容质量标准自动进行。重点关注Google News站点地图标记和一致的高质量发布节奏。
- **KPI转变：** 基于流量的KPI（会话数、页面浏览量）的相关性正在下降，因为AI Overviews降低了点击率。领先出版商正在转向：订阅者转化、页面停留时间、滚动深度、Newsletter注册、AI引用频率和每位访客收入。
- **网站声誉滥用风险：** 在其域名下托管第三方内容（优惠券、产品评论、联盟内容）的出版商面临高风险。Google在2024年底因此惩罚了Forbes、WSJ、Time和CNN。如果托管第三方内容，请确保强有力的编辑监督和明确的第一方参与。

## 技术考量

### Core Web Vitals
- 广告放置影响CLS
- 延迟加载首屏以下的广告和图片
- 优化主图以改善LCP
- 最小化渲染阻塞资源

### AMP（如使用）
- 考虑弃用AMP（Top Stories不再要求）
- 确保canonical设置正确
- 监控与非AMP版本的性能对比

### 分页
- 多页文章使用正确的分页
- 或使用带正确索引的无限滚动
- canonical指向第1页或完整文章

## 关键追踪指标

- 自然搜索页面浏览量
- 页面停留时间
- 每次会话浏览页数
- 自然搜索Newsletter注册
- Google News/Discover流量
- AI Overview出现次数
