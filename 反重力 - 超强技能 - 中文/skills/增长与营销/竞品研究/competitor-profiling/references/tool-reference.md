# 竞品画像 MCP 工具参考

竞品画像所用 Firecrawl 与 DataForSEO MCP 工具的快速参考。

## 目录
- Firecrawl 工具（站点抓取）
- DataForSEO 工具（SEO 与市场数据）
- 推荐执行顺序
- 错误处理

---

## Firecrawl 工具

### firecrawl_map
**用途**：发现竞品站点上的所有 URL，以识别关键页面。
**使用时机**：每个竞品的第一步——在抓取单个页面之前。
**关键输出**：URL 列表及其页面类型/路径。
**提示**：留意包含 `/pricing`、`/features`、`/about`、`/customers`、`/integrations`、`/blog`、`/changelog` 的路径。

### firecrawl_scrape
**用途**：以干净的 markdown 提取单个页面的内容。
**使用时机**：完成映射后，逐个抓取关键页面。
**关键输出**：markdown 格式的页面内容——标题、正文、结构化数据。
**提示**：先抓取首页——它能一次性呈现定位、受众与社交证明。

### firecrawl_search
**用途**：在网络上搜索关于某竞品的特定内容。
**使用时机**：查找其官方站点之外的评测页面、媒体报道或竞品提及。
**查询示例**：
- `"[竞品名称]" site:g2.com`
- `"[竞品名称]" 评测`
- `"[竞品名称]" 融资 OR 获得投资`

### firecrawl_crawl
**用途**：一次性抓取站点上的多个页面。
**使用时机**：深度画像中需分析大量页面时（例如所有功能页、所有博客文章）。成本更高——请有选择地使用。
**提示**：设置页面数量上限，避免抓取整个站点。锁定特定的 URL 模式。

### firecrawl_extract
**用途**：使用 schema 从页面提取结构化数据。
**使用时机**：当你需要以一致格式获取特定数据点时（如定价档位详情、功能列表）。
**提示**：明确定义要提取内容的 schema——比直接解析原始 markdown 更可靠。

---

## DataForSEO MCP 工具

### 域名级情报

#### backlinks_summary
**用途**：获取域名权重、总反向链接数、引荐域名数、垃圾分数。
**输入**：目标域名（如 `competitor.com`）
**关键指标**：`domain_rank`、`total_backlinks`、`referring_domains`、`backlinks_spam_score`

#### backlinks_referring_domains
**用途**：列出头部引荐域名——展示其链接权重来源。
**输入**：目标域名 + 限制数量
**关键指标**：按域名：`rank`、`backlinks`、域名 `domain`

#### dataforseo_labs_google_domain_rank_overview
**用途**：自然搜索概览——流量、关键词、流量价值。
**输入**：目标域名
**关键指标**：`organic_count`（关键词数）、`organic_traffic`（预估月流量）、`organic_cost`（流量价值，美元）

#### dataforseo_labs_google_ranked_keywords
**用途**：某域名所排名关键词及其位置。
**输入**：目标域名
**关键指标**：按关键词：`keyword`、`position`、`search_volume`、排名页 `url`
**提示**：按流量排序，找出其最高价值的关键词。

#### dataforseo_labs_google_keywords_for_site
**用途**：与某域名相关的关键词——范围比排名关键词更广，包含潜在机会。
**输入**：目标域名
**关键指标**：`keyword`、`search_volume`、`competition`、`cpc`

### 竞争分析

#### dataforseo_labs_google_competitors_domain
**用途**：按关键词重合度找出某域名最接近的自然搜索竞争对手。
**输入**：目标域名
**关键指标**：`domain`、`avg_position`、`intersections`（共有关键词）、`full_domain_rank`
**提示**：可能揭示用户尚未考虑到的竞争对手。

#### dataforseo_labs_google_domain_intersection
**用途**：找出两个域名同时排名的关键词——显示直接竞争。
**输入**：两个目标域名
**关键指标**：`keyword`、各域名排名 `position`、`search_volume`
**提示**：用于将用户域名与各竞品进行对比。

#### dataforseo_labs_google_relevant_pages
**用途**：按自然流量找出某域名最重要的页面。
**输入**：目标域名
**关键指标**：`page`、`metrics`（流量、每页关键词数）
**提示**：揭示其内容策略——哪些页面创造最多价值。

### 技术栈检测

#### domain_analytics_technologies_domain_technologies
**用途**：检测某域名所使用的技术栈。
**输入**：目标域名
**关键指标**：按类别分组的技术（CMS、分析、营销、支付等）

### 反向链接深挖

#### backlinks_backlinks
**用途**：列出指向某域名的逐条反向链接。
**输入**：目标域名 + 限制数量
**关键指标**：`url_from`、`url_to`、`anchor`、`domain_from_rank`、`is_new`

#### backlinks_bulk_ranks
**用途**：一次比较多个域名的权重。
**输入**：目标域名数组
**关键指标**：每域名 `domain_rank`
**提示**：用于汇总对比表。

---

## 推荐执行顺序

### 快速扫描（每个竞品）

```
1. firecrawl_map → 获取站点 URL
2. 并行：
   a. firecrawl_scrape → 首页
   b. firecrawl_scrape → 定价页
   c. dataforseo_labs_google_domain_rank_overview → 自然搜索指标
   d. backlinks_summary → 域名权重
3. 综合为精简档案
```

### 深度画像（每个竞品）

```
1. firecrawl_map → 获取站点 URL
2. 并行（批次 1 — 抓取）：
   a. firecrawl_scrape → 首页
   b. firecrawl_scrape → 定价页
   c. firecrawl_scrape → 功能页
   d. firecrawl_scrape → 关于页
   e. firecrawl_scrape → 客户/案例研究页
   f. firecrawl_scrape → 集成页
3. 并行（批次 2 — SEO 数据）：
   a. dataforseo_labs_google_domain_rank_overview
   b. dataforseo_labs_google_ranked_keywords
   c. backlinks_summary
   d. backlinks_referring_domains
   e. dataforseo_labs_google_relevant_pages
   f. dataforseo_labs_google_competitors_domain
4. 并行（批次 3 — 可选补充）：
   a. domain_analytics_technologies_domain_technologies
   b. firecrawl_search → G2/Capterra 评测
   c. dataforseo_labs_google_domain_intersection（对比用户域名）
5. 综合为完整档案
```

### 多竞品（3 个及以上）

```
1. 并行映射所有竞品站点
2. 并行抓取所有首页，再并行抓取所有定价页
3. 并行拉取所有域名的 domain_rank_overview
4. 一次性拉取所有域名的 backlinks_bulk_ranks
5. 依次构建档案（综合阶段需要专注）
6. 最后构建汇总对比
```

---

## 错误处理

| 问题 | 处理 |
|------|------|
| Firecrawl 抓取返回为空或被拦截 | 对 JS 较多的站点改用 `firecrawl_browser_create` |
| 在映射中未找到定价页 | 搜索 `/pricing`、`/plans`、`/packages`——部分站点使用不同路径 |
| DataForSEO 对该域名无数据 | 域名可能过新或过小——在档案中标注"数据不足" |
| 触及速率限制 | 拉长请求间隔；优先获取高价值数据 |
| 评测页面抓取被阻止 | 使用 `firecrawl_search` 寻找缓存或可替代的评测来源 |