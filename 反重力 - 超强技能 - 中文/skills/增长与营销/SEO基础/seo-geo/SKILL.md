---
name: seo-geo
description: "优化内容以适配 AI Overviews、ChatGPT、Perplexity 等 AI 搜索系统。用于提升 GEO、AI 引用、llms.txt 就绪度、爬虫可访问性和段落级可引用性。触发词：GEO优化、AI搜索优化、AI引用、llms.txt、AI爬虫、生成式引擎优化、AI可见性、AI Overviews优化"
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

# AI 搜索 / GEO 优化（2026年2月）

## 何时使用
- 在提升 AI Overviews、ChatGPT、Perplexity 或类似 AI 搜索系统中的可见性时使用。
- 在评估 llms.txt 就绪度、AI 爬虫访问权限或面向引用的内容结构时使用。
- 当用户询问 GEO、AI SEO、LLM 可见性或 AI 引用时使用。

## 关键数据

| 指标 | 数值 | 来源 |
|--------|-------|--------|
| AI Overviews 覆盖范围 | 每月 15 亿用户，覆盖 200+ 个国家 | Google |
| AI Overviews 查询覆盖率 | 所有查询的 50%+ | 行业数据 |
| AI 引荐会话增长 | 527%（2025年1-5月） | SparkToro |
| ChatGPT 周活跃用户 | 9 亿 | OpenAI |
| Perplexity 月查询量 | 5 亿+ | Perplexity |

## 关键洞察：品牌提及 > 反向链接

**品牌提及与 AI 可见性的相关性是反向链接的 3 倍。**
（Ahrefs 2025年12月对 75,000 个品牌的研究）

| 信号 | 与 AI 引用的相关性 |
|--------|------------------------------|
| YouTube 提及 | ~0.737（最强） |
| Reddit 提及 | 高 |
| Wikipedia 存在 | 高 |
| LinkedIn 存在 | 中等 |
| 域名评级（反向链接） | ~0.266（弱） |

**仅有 11% 的域名**同时被 ChatGPT 和 Google AI Overviews 在同一查询中引用，因此针对各平台的优化至关重要。

---

## GEO 分析标准（已更新）

### 1. 可引用性评分（25%）

**最佳段落长度：134-167 词**，适合 AI 引用。

**强信号：**
- 含具体事实/统计数据的清晰、可引用句子
- 自包含的回答块（无需上下文即可提取）
- 章节前 40-60 词内直接给出答案
- 附有具体来源的论断
- 遵循"X 是……"或"X 指的是……"模式的定义
- 其他地方找不到的独特数据点

**弱信号：**
- 模糊、笼统的陈述
- 无证据支撑的观点
- 被掩盖的结论
- 没有具体数据点

### 2. 结构可读性（20%）

**92% 的 AI Overview 引用来自排名前 10 的页面**，但 47% 来自排名低于第 5 位的页面，表明其选择逻辑有所不同。

**强信号：**
- 清晰的 H1->H2->H3 标题层级
- 基于问题的标题（匹配查询模式）
- 短段落（2-4 句）
- 用于对比数据的表格
- 用于步骤或多项目内容的有序/无序列表
- 具有清晰问答格式的 FAQ 章节

**弱信号：**
- 无结构的文字墙
- 不一致的标题层级
- 没有列表或表格
- 信息埋没在段落中

### 3. 多模态内容（15%）

包含多模态元素的内容的**选择率高出 156%**。

**检查项：**
- 文本 + 相关图片
- 视频内容（嵌入或链接）
- 信息图和图表
- 交互元素（计算器、工具）
- 支持媒体的结构化数据

### 4. 权威与品牌信号（20%）

**强信号：**
- 附带资质信息的作者署名
- 发布日期和最后更新日期
- 对一手来源的引用（研究、官方文档、数据）
- 组织资质和隶属关系
- 带归属的专家引言
- 在 Wikipedia、Wikidata 中的实体存在
- 在 Reddit、YouTube、LinkedIn 上的提及

**弱信号：**
- 匿名作者
- 无日期
- 无来源引用
- 跨平台无品牌存在

### 5. 技术可访问性（20%）

**AI 爬虫不会执行 JavaScript。** 服务端渲染至关重要。

**检查项：**
- 服务端渲染（SSR）vs 仅客户端内容
- robots.txt 中的 AI 爬虫访问权限
- llms.txt 文件的存在和配置
- RSL 1.0 许可条款

---

## AI 爬虫检测

检查 `robots.txt` 中的以下 AI 爬虫：

| 爬虫 | 所属方 | 用途 |
|---------|-------|---------|
| GPTBot | OpenAI | ChatGPT 网页搜索 |
| OAI-SearchBot | OpenAI | OpenAI 搜索功能 |
| ChatGPT-User | OpenAI | ChatGPT 浏览 |
| ClaudeBot | Anthropic | Claude 网页功能 |
| PerplexityBot | Perplexity | Perplexity AI 搜索 |
| CCBot | Common Crawl | 训练数据（常被屏蔽） |
| anthropic-ai | Anthropic | Claude 训练 |
| Bytespider | ByteDance | TikTok/抖音 AI |
| cohere-ai | Cohere | Cohere 模型 |

**建议：** 允许 GPTBot、OAI-SearchBot、ClaudeBot、PerplexityBot 以获得 AI 搜索可见性。如需要可屏蔽 CCBot 和训练爬虫。

---

## llms.txt 标准

新兴的 **llms.txt** 标准为 AI 爬虫提供结构化内容指引。

**位置：** `/llms.txt`（域名根目录）

**格式：**
```
# Title of site
> Brief description

## Main sections
- `Page title -> https://example.com/page`: Description
- `Another page -> https://example.com/another-page`: Description

## Optional: Key facts
- Fact 1
- Fact 2
```

**检查项：**
- `/llms.txt` 是否存在
- 结构化内容指引
- 关键页面亮点
- 联系/权威信息

---

## RSL 1.0（Really Simple Licensing）

面向机器可读 AI 许可条款的新标准（2025年12月）。

**支持方：** Reddit、Yahoo、Medium、Quora、Cloudflare、Akamai、Creative Commons

**检查项：** RSL 实现及适当的许可条款。

---

## 平台专属优化

| 平台 | 主要引用来源 | 优化重点 |
|----------|---------------------|-------------------|
| **Google AI Overviews** | 排名前 10 的页面（92%） | 传统 SEO + 段落优化 |
| **ChatGPT** | Wikipedia（47.9%）、Reddit（11.3%） | 实体存在、权威来源 |
| **Perplexity** | Reddit（46.7%）、Wikipedia | 社区验证、讨论 |
| **Bing Copilot** | Bing 索引、权威站点 | Bing SEO、IndexNow |

---

## 输出

生成 `GEO-ANALYSIS.md`，包含：

1. **GEO 就绪评分：XX/100**
2. **平台细分**（Google AIO、ChatGPT、Perplexity 评分）
3. **AI 爬虫访问状态**（哪些爬虫被允许/屏蔽）
4. **llms.txt 状态**（存在、缺失、建议）
5. **品牌提及分析**（在 Wikipedia、Reddit、YouTube、LinkedIn 上的存在）
6. **段落级可引用性**（识别出的 134-167 词最佳段落块）
7. **服务端渲染检查**（JavaScript 依赖分析）
8. **前 5 项最高影响变更**
9. **Schema 建议**（用于 AI 可发现性）
10. **内容重排建议**（需要重写的具体段落）

---

## 快速见效

1. 在前 60 词内添加"[主题]是什么？"的定义
2. 创建 134-167 词的自包含回答块
3. 添加基于问题的 H2/H3 标题
4. 包含带来源的具体统计数据
5. 添加发布/更新日期
6. 为作者实现 Person schema
7. 在 robots.txt 中允许关键 AI 爬虫

## 中等投入

1. 创建 `/llms.txt` 文件
2. 添加带资质信息 + Wikipedia/LinkedIn 链接的作者简介
3. 确保关键内容的服务端渲染
4. 在 Reddit、YouTube 上建立实体存在
5. 添加带数据的对比表格
6. 实现 FAQ 章节（结构化，商业站点不使用 schema）

## 高影响

1. 创建原创研究/调查（独特可引用性）
2. 为品牌/关键人物建立 Wikipedia 存在
3. 建立含内容提及的 YouTube 频道
4. 实现全面的实体链接（跨平台 sameAs）
5. 开发独特工具或计算器

## DataForSEO 集成（可选）

如果 DataForSEO MCP 工具可用，使用 `ai_optimization_chat_gpt_scraper` 检查 ChatGPT 网页搜索对目标查询的返回结果（真实 GEO 可见性检查），使用 `ai_opt_llm_ment_search` 配合 `ai_opt_llm_ment_top_domains` 进行跨 AI 平台的 LLM 提及追踪。

## 错误处理

| 场景 | 操作 |
|----------|--------|
| URL 不可达（DNS 失败、连接被拒绝） | 清晰报告错误。不要猜测网站内容。建议用户验证 URL 后重试。 |
| AI 爬虫被 robots.txt 屏蔽 | 精确报告哪些爬虫被屏蔽、哪些被允许。提供具体的 robots.txt 指令以启用 AI 搜索可见性。 |
| 未找到 llms.txt | 注明缺失，并根据网站内容结构提供即用型 llms.txt 模板。 |
| 未检测到结构化数据 | 报告缺口并提供具体的 schema 建议（Article、Organization、Person）以提升 AI 可发现性。 |

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
