---
name: seo-technical
description: "审计技术SEO，涵盖可爬取性、可索引性、安全性、URL结构、移动端优化、Core Web Vitals、结构化数据、JavaScript渲染及robots.txt和AI爬虫访问等平台信号。触发词：技术SEO、技术SEO审计、可爬取性、可索引性、Core Web Vitals、结构化数据、JavaScript SEO、robots.txt、AI爬虫、移动端优化、URL结构、安全头、IndexNow"
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
---

# 技术 SEO 审计

## 何时使用
- 当用户需要针对可爬取性、可索引性、性能或渲染的技术SEO审查时使用。
- 当审计 robots.txt、规范化、JavaScript SEO、Core Web Vitals 或 AI 爬虫访问时使用。
- 当任务面向基础设施和实现而非内容时使用。

## 审计类别

### 1. 可爬取性
- robots.txt：是否存在、是否有效、是否阻止了重要资源
- XML 站点地图：是否存在、是否在 robots.txt 中引用、格式是否有效
- Noindex 标签：有意设置还是意外添加
- 爬取深度：重要页面距首页不超过3次点击
- JavaScript 渲染：检查关键内容是否依赖 JS 执行
- 爬取预算：对于大型网站（>1万页面），效率很重要

#### AI 爬虫管理

截至2025-2026年，AI公司积极爬取网络以训练模型和驱动AI搜索。通过 robots.txt 管理这些爬虫是技术SEO的关键考量。

**已知 AI 爬虫：**

| 爬虫 | 公司 | robots.txt 令牌 | 用途 |
|------|------|----------------|------|
| GPTBot | OpenAI | `GPTBot` | 模型训练 |
| ChatGPT-User | OpenAI | `ChatGPT-User` | 实时浏览 |
| ClaudeBot | Anthropic | `ClaudeBot` | 模型训练 |
| PerplexityBot | Perplexity | `PerplexityBot` | 搜索索引 + 训练 |
| Bytespider | ByteDance | `Bytespider` | 模型训练 |
| Google-Extended | Google | `Google-Extended` | Gemini 训练（非搜索） |
| CCBot | Common Crawl | `CCBot` | 开放数据集 |

**关键区别：**
- 屏蔽 `Google-Extended` 可阻止 Gemini 训练使用，但不会影响 Google 搜索索引或 AI Overviews（它们使用 `Googlebot`）
- 屏蔽 `GPTBot` 可阻止 OpenAI 训练，但不会阻止 ChatGPT 通过浏览（`ChatGPT-User`）引用你的内容
- 约3-5%的网站现在使用针对AI的 robots.txt 规则

**示例，选择性屏蔽 AI 爬虫：**
```
# Allow search indexing, block AI training crawlers
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

# Allow all other crawlers (including Googlebot for search)
User-agent: *
Allow: /
```

**建议：** 在屏蔽之前考虑你的 AI 可见性策略。被 AI 系统引用可以提升品牌知名度和引荐流量。交叉参考 `seo-geo` 技能以获取完整的 AI 可见性优化方案。

### 2. 可索引性
- Canonical 标签：自引用，与 noindex 无冲突
- 重复内容：近似重复、参数URL、www 与非 www
- 薄内容：低于各类型最低字数要求的页面
- 分页：rel=next/prev 或加载更多模式
- Hreflang：多语言/多地区网站是否正确配置
- 索引膨胀：不必要的页面消耗爬取预算

### 3. 安全性
- HTTPS：是否强制、SSL证书是否有效、是否存在混合内容
- 安全头：
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
- HSTS 预加载：检查高安全要求网站是否加入预加载列表

### 4. URL 结构
- 简洁URL：描述性强、使用连字符、内容页无查询参数
- 层级：反映网站架构的逻辑文件夹结构
- 重定向：无链式重定向（最多1跳），永久移动使用301
- URL长度：标记超过100个字符的URL
- 尾部斜杠：使用是否一致

### 5. 移动端优化
- 响应式设计：viewport meta 标签、响应式 CSS
- 触控目标：最小 48x48px，间距 8px
- 字体大小：基准最小 16px
- 无水平滚动
- 移动优先索引：Google 索引移动版本。**移动优先索引已于2024年7月5日100%完成。** Google 现在仅使用移动端 Googlebot 用户代理来爬取和索引所有网站。

### 6. Core Web Vitals
- **LCP**（最大内容绘制）：目标 <2.5s
- **INP**（下次绘制交互）：目标 <200ms
  - INP 于2024年3月12日取代了 FID。FID 已于2024年9月9日从所有 Chrome 工具（CrUX API、PageSpeed Insights、Lighthouse）中完全移除。请勿在任何地方引用 FID。
- **CLS**（累积布局偏移）：目标 <0.1
- 评估使用真实用户数据的第75百分位
- 如有 MCP 可用，使用 PageSpeed Insights API 或 CrUX 数据

### 7. 结构化数据
- 检测方式：JSON-LD（首选）、Microdata、RDFa
- 根据 Google 支持的类型进行验证
- 完整分析请参见 seo-schema 技能

### 8. JavaScript 渲染
- 检查内容在初始 HTML 中是否可见还是需要 JS
- 识别客户端渲染（CSR）与服务端渲染（SSR）
- 标记可能导致索引问题的 SPA 框架（React、Vue、Angular）
- 如适用，验证动态渲染设置

#### JavaScript SEO：Canonical 与索引指南（2025年12月）

Google 于2025年12月更新了其 JavaScript SEO 文档，提供了关键说明：

1. **Canonical 冲突：** 如果原始 HTML 中的 canonical 标签与 JavaScript 注入的不同，Google 可能使用其中任何一个。确保服务端渲染 HTML 和 JS 渲染输出中的 canonical 标签完全一致。
2. **JavaScript 中的 noindex：** 如果原始 HTML 包含 `<meta name="robots" content="noindex">` 但 JavaScript 移除了它，Google 可能仍会遵循原始 HTML 中的 noindex。请在初始 HTML 响应中提供正确的 robots 指令。
3. **非200状态码：** Google 不会对返回非200 HTTP 状态码的页面渲染 JavaScript。在错误页面上通过 JS 注入的任何内容或 meta 标签对 Googlebot 不可见。
4. **JavaScript 中的结构化数据：** 通过 JS 注入的 Product、Article 等结构化数据可能面临延迟处理。对于时效性结构化数据（尤其是电商 Product 标记），请在初始服务端渲染 HTML 中包含。

**最佳实践：** 在初始服务端渲染 HTML 中提供关键 SEO 元素（canonical、meta robots、结构化数据、title、meta description），而非依赖 JavaScript 注入。

### 9. IndexNow 协议
- 检查网站是否支持 Bing、Yandex、Naver 的 IndexNow
- 由 Google 以外的搜索引擎支持
- 建议实施以加快非 Google 引擎的索引速度

## 输出

### 技术评分：XX/100

### 类别细分
| 类别 | 状态 | 评分 |
|------|------|------|
| 可爬取性 | pass/warn/fail | XX/100 |
| 可索引性 | pass/warn/fail | XX/100 |
| 安全性 | pass/warn/fail | XX/100 |
| URL 结构 | pass/warn/fail | XX/100 |
| 移动端 | pass/warn/fail | XX/100 |
| Core Web Vitals | pass/warn/fail | XX/100 |
| 结构化数据 | pass/warn/fail | XX/100 |
| JS 渲染 | pass/warn/fail | XX/100 |
| IndexNow | pass/warn/fail | XX/100 |

### 严重问题（立即修复）
### 高优先级（1周内修复）
### 中优先级（1月内修复）
### 低优先级（待办积压）

## DataForSEO 集成（可选）

如果 DataForSEO MCP 工具可用，使用 `on_page_instant_pages` 进行实时页面分析（状态码、页面计时、断链、页面检查），使用 `on_page_lighthouse` 进行 Lighthouse 审计（性能、无障碍、SEO 评分），使用 `domain_analytics_technologies_domain_technologies` 进行技术栈检测。

## 错误处理

| 场景 | 操作 |
|------|------|
| URL 无法访问 | 报告连接错误及状态码。建议验证 URL、检查 DNS 解析并确认网站可公开访问。 |
| 未找到 robots.txt | 注明根域名未检测到 robots.txt。建议创建包含适当指令的文件。继续审计其余类别。 |
| 未配置 HTTPS | 标记为严重问题。报告 HTTP 是否无重定向、是否存在混合内容或 SSL 证书缺失/过期。 |
| Core Web Vitals 数据不可用 | 注明 CrUX 数据不可用（低流量网站常见）。建议使用 Lighthouse 实验室数据作为替代，并建议增加流量后重新测试。 |

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
