---
name: seo-dataforseo
description: "使用 DataForSEO 获取实时 SERP、关键词指标、外链、竞争对手分析、页面检查和 AI 可见性数据。当用户需要真实 SEO 数据而非静态指导时触发。触发词：DataForSEO、SERP数据、关键词数据、外链分析、竞争对手数据、AI可见性"
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[command] [query]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# DataForSEO：实时 SEO 数据（扩展）

通过 DataForSEO MCP 服务器获取实时搜索数据。提供实时 SERP 结果、关键词指标、外链档案、页面分析、内容分析、商业列表、AI 可见性检查和 LLM 提及追踪，涵盖 9 个 API 模块和 79 个 MCP 工具。

## 适用场景
- 当用户需要实时 SEO 数据而非静态最佳实践指导时使用
- 用于 SERP 查询、关键词搜索量、外链检查、竞争对手数据或 AI 可见性追踪
- 仅在环境中已安装 DataForSEO 扩展时使用

## 前置条件

此技能需要安装 DataForSEO 扩展：
```bash
./extensions/dataforseo/install.sh
```

**检查可用性：** 使用任何 DataForSEO 工具前，先检查 MCP 服务器是否已连接，确认 `serp_organic_live_advanced` 或任何 DataForSEO 工具是否可用。如工具不可用，告知用户扩展未安装并提供安装说明。

## API 额度意识

DataForSEO 按 API 调用次数收费，请注意效率：
- 优先使用批量接口而非多次单次调用
- 使用默认参数（美国、英语），除非用户另有指定
- 在会话中缓存结果，不要重复获取相同数据
- 运行昂贵操作（完整外链抓取、大批量关键词列表）前先提醒用户

## 快速参考

| 命令 | 功能 |
|------|------|
| `/seo dataforseo serp <keyword>` | Google 自然 SERP 结果 |
| `/seo dataforseo serp-youtube <keyword>` | YouTube 搜索结果 |
| `/seo dataforseo youtube <video_id>` | YouTube 视频深度分析 |
| `/seo dataforseo keywords <seed>` | 关键词创意和建议 |
| `/seo dataforseo volume <keywords>` | 关键词搜索量 |
| `/seo dataforseo difficulty <keywords>` | 关键词难度评分 |
| `/seo dataforseo intent <keywords>` | 搜索意图分类 |
| `/seo dataforseo trends <keyword>` | Google Trends 数据 |
| `/seo dataforseo backlinks <domain>` | 完整外链档案 |
| `/seo dataforseo competitors <domain>` | 竞争对手域名分析 |
| `/seo dataforseo ranked <domain>` | 域名排名关键词 |
| `/seo dataforseo intersection <domains>` | 关键词/外链重叠分析 |
| `/seo dataforseo traffic <domains>` | 批量流量估算 |
| `/seo dataforseo subdomains <domain>` | 子域名及排名数据 |
| `/seo dataforseo top-searches <domain>` | 提及该域名的热门查询 |
| `/seo dataforseo onpage <url>` | 页面分析（Lighthouse + 解析） |
| `/seo dataforseo tech <domain>` | 技术栈检测 |
| `/seo dataforseo whois <domain>` | WHOIS 注册数据 |
| `/seo dataforseo content <keyword/url>` | 内容分析和趋势 |
| `/seo dataforseo listings <keyword>` | 商业列表搜索 |
| `/seo dataforseo ai-scrape <query>` | ChatGPT 网页抓取用于 GEO |
| `/seo dataforseo ai-mentions <keyword>` | LLM 提及追踪用于 GEO |

---

## SERP 分析

### `/seo dataforseo serp <keyword>`

获取实时 Google 自然搜索结果。

**MCP 工具：** `serp_organic_live_advanced`

**默认参数：** location_code=2840（美国），language_code=en，device=desktop，depth=100

**同时支持：** `serp_organic_live_advanced` 工具通过 `se` 参数支持 Google、Bing 和 Yahoo。指定 "bing" 或 "yahoo" 可切换搜索引擎。

**输出：** 排名、URL、标题、描述、域名、精选摘要、AI 概览引用、"人们还问"。

### `/seo dataforseo serp-youtube <keyword>`

获取 YouTube 搜索结果。对 GEO 很有价值。YouTube 提及与 AI 引用的相关性最强。

**MCP 工具：** `serp_youtube_organic_live_advanced`

**输出：** 视频标题、频道、播放量、上传日期、描述、URL。

### `/seo dataforseo youtube <video_id>`

对特定 YouTube 视频的深度分析：信息、评论和字幕。YouTube 提及与 AI 可见性的相关性最强（0.737），这对 GEO 分析至关重要。

**MCP 工具：** `serp_youtube_video_info_live_advanced`、`serp_youtube_video_comments_live_advanced`、`serp_youtube_video_subtitles_live_advanced`

**参数：** video_id（YouTube 视频 ID，例如 "dQw4w9WgXcQ"）

**输出：** 视频元数据（标题、频道、播放量、点赞数、描述）、热门评论及互动数据、字幕/转录文本。

---

## 关键词研究

### `/seo dataforseo keywords <seed>`

从种子关键词生成关键词创意、建议和相关词。

**MCP 工具：** `dataforseo_labs_google_keyword_ideas`、`dataforseo_labs_google_keyword_suggestions`、`dataforseo_labs_google_related_keywords`

**默认参数：** location_code=2840（美国），language_code=en，limit=50

**输出：** 关键词、搜索量、CPC、竞争程度、关键词难度、趋势。

### `/seo dataforseo volume <keywords>`

获取一组关键词的搜索量和指标。

**MCP 工具：** `kw_data_google_ads_search_volume`

**参数：** keywords（数组，逗号分隔）、location_code、language_code

**输出：** 关键词、月搜索量、CPC、竞争度、月度趋势数据。

### `/seo dataforseo difficulty <keywords>`

计算关键词难度评分以评估排名竞争力。

**MCP 工具：** `dataforseo_labs_bulk_keyword_difficulty`

**参数：** keywords（数组）、location_code、language_code

**输出：** 关键词、难度评分（0-100）、解读（Easy/Medium/Hard/Very Hard）。

### `/seo dataforseo intent <keywords>`

按用户搜索意图对关键词进行分类。

**MCP 工具：** `dataforseo_labs_search_intent`

**参数：** keywords（数组）、location_code、language_code

**输出：** 关键词、意图类型（informational、navigational、commercial、transactional）、置信度分数。

### `/seo dataforseo trends <keyword>`

使用 Google Trends 数据分析关键词随时间变化的趋势。

**MCP 工具：** `kw_data_google_trends_explore`

**参数：** keywords（数组）、location_code、date_from、date_to、language_code

**输出：** 关键词、时间序列数据、趋势方向、季节性信号。

---

## 域名与竞争对手分析

### `/seo dataforseo backlinks <domain>`

全面的外链档案分析。

**MCP 工具：** `backlinks_summary`、`backlinks_backlinks`、`backlinks_anchors`、`backlinks_referring_domains`、`backlinks_bulk_spam_score`、`backlinks_timeseries_summary`

**默认参数：** 每个子调用 limit=100

**输出：** 外链总数、引荐域名、域名排名、垃圾评分、热门锚文本、新增/丢失外链时间线、dofollow 比例、顶级引荐域名。

### `/seo dataforseo competitors <domain>`

识别竞争域名并估算流量。

**MCP 工具：** `dataforseo_labs_google_competitors_domain`、`dataforseo_labs_google_domain_rank_overview`、`dataforseo_labs_bulk_traffic_estimation`

**输出：** 竞争域名、关键词重叠率、估算流量、域名排名、共同关键词。

### `/seo dataforseo ranked <domain>`

列出域名排名的关键词及其排名位置和页面数据。

**MCP 工具：** `dataforseo_labs_google_ranked_keywords`、`dataforseo_labs_google_relevant_pages`

**默认参数：** limit=100，location_code=2840

**输出：** 关键词、排名位置、URL、搜索量、流量占比、SERP 特性。

### `/seo dataforseo intersection <domain1> <domain2> [...]`

查找 2-20 个域名之间的共享关键词和外链来源。

**MCP 工具：** `dataforseo_labs_google_domain_intersection`、`backlinks_domain_intersection`

**参数：** domains（2-20 个域名的数组）

**输出：** 共享关键词及各域名排名位置、共享外链来源、各域名独有关键词。

### `/seo dataforseo traffic <domains>`

估算一个或多个域名的自然搜索流量。

**MCP 工具：** `dataforseo_labs_bulk_traffic_estimation`

**参数：** domains（数组）

**输出：** 域名、估算自然流量、估算流量成本、热门关键词。

### `/seo dataforseo subdomains <domain>`

枚举子域名及其排名数据和流量估算。

**MCP 工具：** `dataforseo_labs_google_subdomains`

**参数：** target（域名）、location_code、language_code

**输出：** 子域名、排名关键词数、估算流量、自然搜索成本。

### `/seo dataforseo top-searches <domain>`

查找搜索结果中提及特定域名的最热门查询。

**MCP 工具：** `dataforseo_labs_google_top_searches`

**参数：** target（域名）、location_code、language_code

**输出：** 查询词、搜索量、域名排名位置、SERP 特性、流量占比。

---

## 技术/页面分析

### `/seo dataforseo onpage <url>`

运行页面分析，包括 Lighthouse 审计和内容解析。

**MCP 工具：** `on_page_instant_pages`、`on_page_content_parsing`、`on_page_lighthouse`

**用法：**
- `on_page_instant_pages`：快速页面分析（状态码、meta 标签、内容大小、页面计时、死链、页面检查）
- `on_page_content_parsing`：提取并解析页面内容（纯文本、字数、结构）
- `on_page_lighthouse`：完整 Lighthouse 审计（性能评分、无障碍性、最佳实践、SEO、Core Web Vitals）

**输出：** 已爬取页面数、状态码、meta 标签、标题、内容大小、加载时间、Lighthouse 评分、死链、资源分析。

### `/seo dataforseo tech <domain>`

检测域名使用的技术。

**MCP 工具：** `domain_analytics_technologies_domain_technologies`

**输出：** 技术名称、版本、类别（CMS、分析、CDN、框架等）。

### `/seo dataforseo whois <domain>`

获取 WHOIS 注册数据。

**MCP 工具：** `domain_analytics_whois_overview`

**输出：** 注册商、创建日期、到期日期、域名服务器、注册人信息（如公开）。

---

## 内容与商业数据

### `/seo dataforseo content <keyword/url>`

分析内容质量、按主题搜索内容并追踪短语趋势。

**MCP 工具：** `content_analysis_search`、`content_analysis_summary`、`content_analysis_phrase_trends`

**参数：** keyword（用于搜索/趋势）或 URL（用于摘要）

**输出：** 内容匹配及质量评分、情感分析、可读性指标、短语趋势数据。

### `/seo dataforseo listings <keyword>`

搜索商业列表用于本地 SEO 竞争分析。

**MCP 工具：** `business_data_business_listings_search`

**参数：** keyword、location（可选）

**输出：** 商家名称、描述、类别、地址、电话、域名、评分、评论数、认领状态。

---

## AI 可见性 / GEO

### `/seo dataforseo ai-scrape <query>`

抓取 ChatGPT 网页搜索对特定查询的返回结果。真正的 GEO 可见性检查：查看 ChatGPT 为你的目标关键词引用了哪些来源。

**MCP 工具：** `ai_optimization_chat_gpt_scraper`

**参数：** query、location_code（可选）、language_code（可选）。使用 `ai_optimization_chat_gpt_scraper_locations` 查询可用位置。

**输出：** ChatGPT 回复内容、引用来源/URL、引用域名。

### `/seo dataforseo ai-mentions <keyword>`

追踪 LLM 如何提及品牌、域名和主题。对 GEO 至关重要。衡量跨多个 LLM 平台的实际 AI 可见性。

**MCP 工具：** `ai_opt_llm_ment_search`、`ai_opt_llm_ment_top_domains`、`ai_opt_llm_ment_top_pages`、`ai_opt_llm_ment_agg_metrics`

**参数：** keyword、location_code（可选）、language_code（可选）。使用 `ai_opt_llm_ment_loc_and_lang` 查询可用位置/语言，使用 `ai_optimization_llm_models` 查询支持的 LLM 模型。

**工作流：**
1. 使用 `ai_opt_llm_ment_search` 搜索 LLM 提及（查找品牌/关键词在 LLM 回复中的提及）
2. 使用 `ai_opt_llm_ment_top_domains` 获取顶级引用域名（哪些域名在此主题上被引用最多）
3. 使用 `ai_opt_llm_ment_top_pages` 获取顶级引用页面（哪些具体页面被引用最多）
4. 使用 `ai_opt_llm_ment_agg_metrics` 获取聚合指标（总体提及量、趋势）

**输出：** LLM 提及次数、顶级引用域名及频率、顶级引用页面、提及趋势、跨平台可见性评分。

**高级用法：** 使用 `ai_opt_llm_ment_cross_agg_metrics` 进行跨模型比较（ChatGPT、Claude、Perplexity 等之间的提及差异）。

---

## 可用工具集

以下 DataForSEO 工具可供智能体内部使用，但没有专用命令：

- `serp_locations`：SERP 查询的位置代码查找
- `serp_youtube_locations`：YouTube 查询的位置代码查找
- `kw_data_google_ads_locations`：关键词数据的位置查找
- `kw_data_dfs_trends_demography`：趋势分析的人口统计数据
- `kw_data_dfs_trends_subregion_interests`：趋势的子区域兴趣数据
- `kw_data_dfs_trends_explore`：DFS 专有趋势数据
- `kw_data_google_trends_categories`：Google Trends 类别查找
- `dataforseo_labs_google_keyword_overview`：快速关键词指标概览
- `dataforseo_labs_google_historical_serp`：关键词的历史 SERP 结果
- `dataforseo_labs_google_serp_competitors`：特定 SERP 的竞争对手
- `dataforseo_labs_google_keywords_for_site`：网站排名的关键词（ranked 的替代方案）
- `dataforseo_labs_google_page_intersection`：页面级交叉分析
- `dataforseo_labs_google_historical_rank_overview`：历史域名排名数据
- `dataforseo_labs_google_historical_keyword_data`：历史关键词指标
- `dataforseo_labs_available_filters`：Labs 端点的可用过滤选项
- `backlinks_competitors`：查找具有相似外链档案的域名
- `backlinks_bulk_backlinks`：多目标的批量外链计数
- `backlinks_bulk_new_lost_referring_domains`：批量新增/丢失引荐域名
- `backlinks_bulk_new_lost_backlinks`：批量新增/丢失外链
- `backlinks_bulk_ranks`：多目标的批量排名概览
- `backlinks_bulk_referring_domains`：批量引荐域名计数
- `backlinks_domain_pages_summary`：域名页面摘要
- `backlinks_domain_pages`：域名页面列表及外链数据
- `backlinks_page_intersection`：页面级共享外链来源
- `backlinks_referring_networks`：引荐网络分析
- `backlinks_timeseries_new_lost_summary`：追踪新增/丢失外链时间线
- `backlinks_bulk_pages_summary`：批量页面摘要
- `backlinks_available_filters`：Backlinks 端点的可用过滤选项
- `domain_analytics_whois_available_filters`：WHOIS 过滤选项
- `domain_analytics_technologies_available_filters`：技术检测过滤选项
- `ai_opt_kw_data_loc_and_lang`：AI 优化关键词数据位置/语言
- `ai_optimization_keyword_data_search_volume`：AI 专属关键词搜索量数据
- `ai_optimization_llm_response`：直接 LLM 回复分析
- `ai_optimization_llm_mentions_filters`：LLM 提及的可用过滤器
- `ai_optimization_chat_gpt_scraper_locations`：ChatGPT 抓取器的可用位置

## 跨技能集成

当 DataForSEO MCP 工具可用时，其他 claude-seo 技能可以利用实时数据：

- **seo-audit**：生成 `seo-dataforseo` 智能体获取真实 SERP、外链、页面和列表数据
- **seo-technical**：使用 `on_page_instant_pages` / `on_page_lighthouse` 获取真实爬取数据，使用 `domain_analytics_technologies_domain_technologies` 进行技术栈检测
- **seo-content**：使用 `kw_data_google_ads_search_volume`、`dataforseo_labs_bulk_keyword_difficulty`、`dataforseo_labs_search_intent` 获取真实关键词指标，使用 `content_analysis_summary` 分析内容质量
- **seo-page**：使用 `serp_organic_live_advanced` 获取真实 SERP 排名，使用 `backlinks_summary` 获取链接数据
- **seo-geo**：使用 `ai_optimization_chat_gpt_scraper` 获取真实 ChatGPT 可见性，使用 `ai_opt_llm_ment_search` 进行 LLM 提及追踪
- **seo-plan**：使用 `dataforseo_labs_google_competitors_domain`、`dataforseo_labs_google_domain_intersection`、`dataforseo_labs_bulk_traffic_estimation` 获取真实竞争情报

## 错误处理

- **MCP 服务器未连接**：报告 DataForSEO 扩展未安装或 MCP 服务器不可达。建议运行 `./extensions/dataforseo/install.sh`
- **API 认证失败**：报告凭据无效。建议检查 MCP 配置中的 DataForSEO API 登录名/密码
- **超出速率限制**：报告已触发限制，建议等待后重试
- **无结果返回**：报告"未找到数据"而非猜测。建议扩大查询范围或检查位置/语言代码
- **无效位置代码**：报告错误并建议使用位置查找工具获取正确代码

## 输出格式

匹配现有 claude-seo 输出模式：
- 使用表格展示对比数据
- 按严重程度排序：Critical > High > Medium > Low
- 包含具体、可操作的建议
- 适用时以 XX/100 格式展示评分
- 注明数据来源为 "DataForSEO (live)" 以区别于静态分析

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家评审的替代品
- 如缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清
