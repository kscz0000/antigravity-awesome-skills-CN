<!-- 更新时间: 2026-02-07 -->
# Schema.org 类型：状态与建议（2026 年 2 月）

**Schema.org 版本：** 29.4（2025 年 12 月 8 日）

## 格式偏好
始终使用 **JSON-LD**（`<script type="application/ld+json">`）。
Google 文档明确推荐 JSON-LD 而非 Microdata 和 RDFa。

**AI 搜索说明：**具有正确 schema 的内容出现在 AI 生成答案中的概率约高 2.5 倍（Google 和 Microsoft 于 2025 年 3 月确认）。

---

## 活跃：自由推荐

| 类型 | 用例 | 关键属性 |
|------|----------|----------------|
| Organization | 公司信息 | name, url, logo, contactPoint, sameAs |
| LocalBusiness | 实体企业 | name, address, telephone, openingHours, geo, priceRange |
| SoftwareApplication | 桌面/移动应用 | name, operatingSystem, applicationCategory, offers, aggregateRating |
| WebApplication | 基于浏览器的 SaaS | name, applicationCategory, offers, browserRequirements, featureList |
| Product | 实体/数字产品 | name, image, description, sku, brand, offers, review |
| Offer | 定价 | price, priceCurrency, availability, url, validFrom |
| Service | 服务型企业 | name, provider, areaServed, description, offers |
| Article | 博客文章、新闻 | headline, author, datePublished, dateModified, image, publisher |
| BlogPosting | 博客内容 | 与 Article 相同 + 博客特定上下文 |
| NewsArticle | 新闻内容 | 与 Article 相同 + 新闻特定上下文 |
| Review | 个人评论 | reviewRating, author, itemReviewed, reviewBody |
| AggregateRating | 评分摘要 | ratingValue, reviewCount, bestRating, worstRating |
| BreadcrumbList | 导航 | itemListElement 包含 position, name, item |
| WebSite | 站点级别 | name, url, potentialAction（SearchAction 用于站点链接搜索） |
| WebPage | 页面级别 | name, description, datePublished, dateModified |
| Person | 作者/团队 | name, jobTitle, url, sameAs, image, worksFor |
| ContactPage | 联系页面 | name, url |
| VideoObject | 视频内容 | name, description, thumbnailUrl, uploadDate, duration, contentUrl |
| ImageObject | 图片内容 | contentUrl, caption, creator, copyrightHolder |
| Event | 活动 | name, startDate, endDate, location, organizer, offers |
| JobPosting | 职位列表 | title, description, datePosted, hiringOrganization, jobLocation |
| Course | 教育内容 | name, description, provider, hasCourseInstance |
| DiscussionForumPosting | 论坛帖子 | headline, author, datePublished, text, url |
| ProductGroup | 变体产品 | name, productGroupID, variesBy, hasVariant |
| ProfilePage | 作者/创作者资料 | mainEntity (Person), name, url, description, sameAs |

---

## 受限：仅限特定网站类型

| 类型 | 限制 | 自 |
|------|------------|-------|
| FAQPage | 仅限政府和医疗权威网站 | 2023 年 8 月 |

> Google 在 2023 年 8 月大幅限制了 FAQ 富媒体结果。只有权威来源（政府、健康组织）才能获得 FAQ 富媒体结果。
>
> **GEO 细节**：FAQPage schema 仍然有利于 AI/LLM 引用可见性（ChatGPT、Perplexity、Google AI Overviews），即使没有 Google 富媒体结果。
> - **商业网站上的现有 FAQPage**：标记为信息优先级，非 Critical。移除会失去 GEO 引用优势。
> - **添加新的 FAQPage**：不建议为 Google 收益添加；如果 AI 搜索可见性是优先事项，则可接受。

---

## 已弃用：永不推荐

| 类型 | 状态 | 自 | 备注 |
|------|--------|-------|-------|
| HowTo | 富媒体结果完全移除 | 2023 年 9 月 | Google 停止显示 how-to 富媒体结果 |
| SpecialAnnouncement | 已弃用 | 2025 年 7 月 31 日 | COVID 时代的 schema，不再处理 |
| CourseInfo | 从富媒体结果中移除 | 2025 年 6 月 | 合并到 Course |
| EstimatedSalary | 从富媒体结果中移除 | 2025 年 6 月 | 不再显示 |
| LearningVideo | 从富媒体结果中移除 | 2025 年 6 月 | 使用 VideoObject 代替 |
| ClaimReview | 从富媒体结果中移除 | 2025 年 6 月 | 事实核查标记不再生成富媒体结果 |
| VehicleListing | 从富媒体结果中移除 | 2025 年 6 月 | 车辆列表结构化数据已停用 |
| Book Actions | 弃用后撤销 | 2025 年 6 月 | **截至 2026 年 2 月仍有效**：仅作历史记录 |
| Practice Problem | 从富媒体结果中移除 | 2025 年末 | 教育练习题不再显示 |
| Dataset | 从富媒体结果中移除 | 2025 年末 | Dataset Search 功能已停用 |

---

## 近期新增（2024-2026）

| 类型/功能 | 添加时间 | 备注 |
|-------------|-------|-------|
| Product Certification 标记 | 2025 年 4 月 | 能源评级、安全认证。取代 EnergyConsumptionDetails。 |
| ProductGroup | 2025 年 | 电子商务产品变体，包含 variesBy、hasVariant 属性 |
| ProfilePage | 2025 年 | 作者/创作者资料页面，包含 mainEntity Person 用于 E-E-A-T |
| DiscussionForumPosting | 2024 年 | 用于论坛/社区内容 |
| Speakable | 2024 年更新 | 用于语音搜索优化 |
| LoyaltyProgram | 2025 年 6 月 | 会员定价、会员卡结构化数据 |
| 组织级别的运输/退货政策 | 2025 年 11 月 | 通过 Search Console 配置，无需 Merchant Center |
| ConferenceEvent | 2025 年 12 月 | Schema.org v29.4 新增 |
| PerformingArtsEvent | 2025 年 12 月 | Schema.org v29.4 新增 |

## 电子商务要求（更新）

| 要求 | 状态 | 自 |
|-------------|--------|-------|
| MerchantReturnPolicy 中的 `returnPolicyCountry` | **必需** | 2025 年 3 月 |
| 产品变体结构化数据 | 已扩展 | 2025 年，包括服装、化妆品、电子产品 |

> **注意：**Content API for Shopping 将于 2026 年 8 月 18 日停用。迁移到 Merchant API。

---

## 验证清单

对于任何 schema 块，验证：

1. ✅ `@context` 是 `"https://schema.org"`（非 http）
2. ✅ `@type` 是有效、未弃用的类型
3. ✅ 所有必需属性都存在
4. ✅ 属性值匹配预期的数据类型
5. ✅ 无占位符文本（如"[Business Name]"）
6. ✅ URL 是绝对的，非相对的
7. ✅ 日期采用 ISO 8601 格式
8. ✅ 图片具有有效 URL

## 测试工具

- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
