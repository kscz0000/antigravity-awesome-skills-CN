# 落地页 SEO 清单

## 概述

本清单确保落地页在保持转化导向的同时，获得搜索引擎可见性优化。发布任何落地页前都应逐项检查。

## Meta 标签

- [ ] **Title 标签**：60 字符以内，包含主关键词，末尾为品牌名
- [ ] **Meta description**：150-160 字符，包含 CTA 语言，每页唯一
- [ ] **Canonical URL**：已设置，防止重复内容问题
- [ ] **Robots meta**：确保页面可索引（`index, follow`），除非有意设为 noindex
- [ ] **Open Graph 标签**：og:title、og:description、og:image、og:url，用于社交分享
- [ ] **Twitter Card 标签**：twitter:card、twitter:title、twitter:description、twitter:image
- [ ] **Viewport meta**：`<meta name="viewport" content="width=device-width, initial-scale=1">`

## 结构化数据

- [ ] **Organization schema**：公司名称、Logo、社交主页
- [ ] **Product schema**：名称、描述、价格、可用性（产品页适用）
- [ ] **FAQ schema**：含 FAQ 区块的页面（富摘要机会）
- [ ] **Breadcrumb schema**：深层页面的导航路径
- [ ] **Review schema**：有证言时使用聚合评分（谨慎使用，遵守规范）
- [ ] **验证**：用 Google Rich Results Test 测试所有结构化数据

## Core Web Vitals 指标

### 最大内容绘制（LCP）— 目标：< 2.5s
- [ ] 优化首屏图片（WebP 格式，合适尺寸）
- [ ] 预加载关键资源（`<link rel="preload">`）
- [ ] 静态资源使用 CDN
- [ ] 减少阻塞渲染的 CSS 和 JavaScript

### 首次输入延迟（FID）/ 交互到下次绘制（INP）— 目标：< 200ms
- [ ] 延迟非关键 JavaScript
- [ ] 拆分长任务（>50ms）
- [ ] 减少第三方脚本影响
- [ ] 视觉更新使用 `requestAnimationFrame`

### 累积布局偏移（CLS）— 目标：< 0.1
- [ ] 图片和视频设置明确的 width/height
- [ ] 为动态内容（广告、嵌入）预留空间
- [ ] Web 字体使用 `font-display: swap`
- [ ] 避免在已有内容上方插入新内容

## 关键词布局

- [ ] **H1 标签**：包含主关键词，每页仅一个
- [ ] **H2 标签**：自然融入次关键词
- [ ] **首段**：主关键词出现在前 100 词内
- [ ] **正文**：自然关键词密度（1-2%），不堆砌
- [ ] **图片 alt 文本**：描述性文字，适当位置包含关键词
- [ ] **URL slug**：简短、含关键词、连字符分隔
- [ ] **CTA 文案**：自然处可考虑融入关键词

## 内链策略

- [ ] 链接到相关产品/功能页面
- [ ] 链接到支撑页面主题的博客内容
- [ ] 使用描述性锚文本（不用"点击这里"）
- [ ] 确保落地页在主导航或 sitemap 中有链接
- [ ] 如适用，链接到定价页面
- [ ] 限制链接数量避免稀释页面权重（最多 15-20 个）

## 图片优化

- [ ] **格式**：使用 WebP，JPEG/PNG 作回退
- [ ] **压缩**：照片用有损压缩，图形用无损压缩
- [ ] **尺寸**：按实际显示尺寸提供（不做 CSS 缩放）
- [ ] **Alt 文本**：描述性，最多 125 字符，自然融入关键词
- [ ] **文件名**：描述性，连字符分隔（如 `product-dashboard-screenshot.webp`）
- [ ] **懒加载**：首屏以下图片使用 `loading="lazy"`
- [ ] **响应式图片**：不同视口尺寸使用 `srcset`

## Canonical URL

- [ ] 每页设置自引用 canonical
- [ ] 协议（https）和尾部斜杠用法保持一致
- [ ] Canonical 指向首选 URL 版本（www 与非 www）
- [ ] Canonical URL 中排除 UTM 参数
- [ ] 分页用 rel="next"/"prev" 处理，或使用单页 canonical

## 移动端适配

- [ ] **移动友好测试**：通过 Google Mobile-Friendly Test
- [ ] **触控目标**：最小 44x44px，目标间距 8px
- [ ] **字号**：基础字号最小 16px，无需双指缩放
- [ ] **内容对等**：所有关键内容在移动端可访问
- [ ] **水平滚动**：任何视口宽度下均无水平滚动
- [ ] **表单可用性**：使用合适的输入类型（email、tel），添加 autocomplete 属性
- [ ] **媒体查询**：断点至少覆盖 480px、768px、1024px、1200px

## 技术 SEO

- [ ] **HTTPS**：SSL 证书有效且已激活
- [ ] **页面速度**：移动端加载时间 < 3s（用 PageSpeed Insights 测试）
- [ ] **XML sitemap**：页面已包含在 sitemap.xml 中
- [ ] **Robots.txt**：页面未被 robots.txt 阻止
- [ ] **404 处理**：自定义 404 页面含导航
- [ ] **重定向链**：不超过 1 次重定向跳转
- [ ] **Hreflang**：多语言落地页需设置

## 内容质量信号

- [ ] **原创内容**：与其他页面无重复内容
- [ ] **内容深度**：话题覆盖充分（SEO 页面建议 500+ 词）
- [ ] **可读性**：面向大众受众的阅读等级 6-8 级
- [ ] **时效性**：最后修改日期反映近期更新
- [ ] **E-E-A-T 信号**：作者专业度、公司权威性、信任指标
