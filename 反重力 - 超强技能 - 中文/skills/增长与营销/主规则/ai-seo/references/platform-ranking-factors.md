# 各 AI 平台如何选择来源

每个 AI 搜索平台都有自己的搜索索引、排名逻辑和内容偏好。本指南涵盖在每个平台上获得引用的关键要点。

引用来源：Princeton GEO 研究 (KDD 2024)、SE Ranking 域名权威度研究、ZipTie 内容-答案匹配分析。

---

## 基础要素

每个 AI 平台都有三个基准要求：

1. **你的内容必须在其索引中**——每个平台使用不同的搜索后端（Google、Bing、Brave 或自己的）。如果你未被索引，就无法被引用。
2. **你的内容必须可爬取**——AI 机器人需要通过 robots.txt 访问。阻止机器人，就失去引用。
3. **你的内容必须可提取**——AI 系统提取段落，而非页面。清晰的结构和独立的段落胜出。

在这些基础之上，每个平台对不同的信号赋予不同权重。以下是各平台的关键要点。

---

## Google AI Overviews

Google AI Overviews 从 Google 自己的索引中提取，并高度依赖 E-E-A-T 信号（经验、专业性、权威性、可信度）。它们出现在约 45% 的 Google 搜索中。

**Google AI Overviews 的独特之处：**它们已经拥有你的传统 SEO 信号——反向链接、页面权威度、主题相关性。额外的 AI 层增加了对带引用来源和结构化数据内容的偏好。研究表明，在内容中包含权威引用与 132% 的可见性提升相关，以权威（非推销）语气写作可再增加 89%。

**重要的是，AI Overviews 不会简单重复传统 Top 10。**只有约 15% 的 AI Overview 来源与传统自然结果重叠。在传统搜索中无法进入第一页的页面，如果有强大的结构化数据和清晰、可提取的答案，仍然可以被引用。

**重点关注：**
- Schema 标记是最大的杠杆——Article、FAQPage、HowTo 和 Product Schema 为 AI Overviews 提供结构化上下文（30-40% 可见性提升）
- 通过强内部链接的内容集群建立主题权威
- 在内容中包含具名、有来源的引用（不仅是主张）
- 带真实资历的作者简介很重要——E-E-A-T 权重很高
- 尽可能进入 Google 知识图谱（准确的 Wikipedia 条目有帮助）
- 针对"如何"和"什么是"查询模式——这些最常触发 AI Overviews

---

## ChatGPT

ChatGPT 的网络搜索从基于 Bing 的索引中提取。它结合训练知识生成答案，然后引用所依赖的网络来源。

**ChatGPT 的独特之处：**域名权威度在这里比其他 AI 平台更重要。SE Ranking 对 129,000 个域名的分析发现，权威度和可信度信号约占决定引用因素的 40%，内容质量约 35%，平台信任度 25%。引用域名数量极高（35 万+）的网站平均每次响应 8.4 次引用，而信任分数稍低（91-96 vs 97-100）的网站从 8.4 降至 6 次引用。

**新鲜度是主要区分因素。**过去 30 天内更新的内容被引用的频率比旧内容高约 3.2 倍。ChatGPT 明显偏好近期信息。

**最重要的信号是内容-答案匹配**——ZipTie 对 40 万页面的分析发现，你的内容风格和结构与 ChatGPT 自身响应格式的匹配程度约占引用可能性的 55%。这远比域名权威度（12%）或页面结构（14%）单独重要。以 ChatGPT 回答问题的方式写作，你更可能成为它引用的来源。

**ChatGPT 在你网站之外查找的地方：**Wikipedia 占所有 ChatGPT 引用的 7.8%，Reddit 占 1.8%，Forbes 占 1.1%。品牌官方网站经常被引用，但第三方提及也很有分量。

**重点关注：**
- 投资反向链接和域名权威度——这是最强的基础信号
- 至少每月更新竞争性内容
- 以 ChatGPT 构建答案的方式构建内容（对话式、直接、组织良好）
- 包含带具名来源的可验证统计数据
- 清晰的标题层级（H1 > H2 > H3）配描述性标题

---

## Perplexity

Perplexity 始终引用来源并提供可点击链接，使其成为最透明的 AI 搜索平台。它结合自己的索引与 Google 的，并通过多次重排序——初始相关性检索、传统排名因子评分、基于机器学习的质量评估，如果不符合质量阈值可丢弃整个结果集。

**Perplexity 的独特之处：**它是最"研究导向"的 AI 搜索引擎，其引用行为反映了这一点。Perplexity 维护权威域名（Amazon、GitHub、主要学术网站）的精选列表，这些域名获得固有的排名提升。它使用时间衰减算法快速评估新内容，给新发布者真正的引用机会。

**Perplexity 有独特的内容偏好：**
- **FAQ Schema (JSON-LD)**——带 FAQ 结构化数据的页面被引用明显更频繁
- **PDF 文档**——公开可访问的 PDF（白皮书、研究报告）被优先考虑。如果你有权威 PDF 内容在表单后受限，考虑公开一个版本。
- **发布频率**——发布频率比关键词定位更重要
- **独立段落**——Perplexity 偏好可以干净提取的原子化、语义完整的段落

**重点关注：**
- 在 robots.txt 中允许 PerplexityBot
- 在任何有问答内容的页面实现 FAQPage Schema
- 公开托管 PDF 资源（白皮书、指南、报告）
- 添加带发布和修改时间戳的 Article Schema
- 以清晰、独立的段落写作，可作为独立答案
- 在你的特定领域建立深度主题权威

---

## Microsoft Copilot

Copilot 嵌入在 Microsoft 生态系统中——Edge、Windows、Microsoft 365 和 Bing 搜索。它完全依赖 Bing 的索引，所以如果 Bing 没有索引你的内容，Copilot 就无法引用它。

**Copilot 的独特之处：**Microsoft 生态系统连接创造了独特的优化机会。LinkedIn 和 GitHub 上的提及和内容提供其他平台不提供的排名提升。Copilot 也更重视页面速度——2 秒以下的加载时间是一个明显阈值。

**重点关注：**
- 将网站提交到 Bing Webmaster Tools（许多网站只提交 Google Search Console）
- 使用 IndexNow 协议加快新内容和更新内容的索引
- 优化页面速度至 2 秒以下
- 编写清晰的实体定义——当你的内容定义术语或概念时，使定义明确且可提取
- 在 LinkedIn（发布文章、维护公司页面）和 GitHub（如相关）建立存在
- 确保 Bingbot 有完全的爬取访问权限

---

## Claude

Claude 在启用网络搜索时使用 Brave Search 作为搜索后端——不是 Google，不是 Bing。这是一个完全不同的索引，这意味着你的 Brave Search 可见性直接决定 Claude 能否找到并引用你。

**Claude 的独特之处：**Claude 对引用什么非常挑剔。虽然它处理大量内容，但引用率很低——它在寻找给定主题上最事实准确、来源良好的内容。带具体数字和清晰归属的数据丰富内容明显优于通用内容。

**重点关注：**
- 验证你的内容出现在 Brave Search 结果中（在 search.brave.com 搜索你的品牌和关键术语）
- 在 robots.txt 中允许 ClaudeBot 和 anthropic-ai 用户代理
- 最大化事实密度——具体数字、具名来源、带日期的统计数据
- 使用清晰、可提取的结构配描述性标题
- 在内容中引用权威来源
- 力求成为你主题上最事实准确的来源——Claude 奖励精确性

---

## 在 robots.txt 中允许 AI 机器人

如果你的 robots.txt 阻止了 AI 机器人，该平台就无法引用你的内容。以下是需要允许的用户代理：

```
User-agent: GPTBot           # OpenAI — 驱动 ChatGPT 搜索
User-agent: ChatGPT-User     # ChatGPT 浏览模式
User-agent: PerplexityBot    # Perplexity AI 搜索
User-agent: ClaudeBot        # Anthropic Claude
User-agent: anthropic-ai     # Anthropic Claude（备用）
User-agent: Google-Extended   # Google Gemini 和 AI Overviews
User-agent: Bingbot          # Microsoft Copilot（通过 Bing）
Allow: /
```

**训练 vs 搜索：**一些 AI 机器人同时用于模型训练和搜索引用。如果你想被引用但不希望内容用于训练，你的选择有限——GPTBot 为 OpenAI 处理两者。但是，你可以安全地阻止 **CCBot**（Common Crawl）而不影响任何 AI 搜索引用，因为它只用于训练数据集收集。

---

## 从哪里开始

如果你是第一次为 AI 搜索优化，将精力集中在你的受众实际所在的地方：

**从 Google AI Overviews 开始**——它们覆盖最多用户（45%+ 的 Google 搜索），你可能已有 Google SEO 基础。添加 Schema 标记，在内容中包含引用来源，加强 E-E-A-T 信号。

**然后处理 ChatGPT**——它是技术和商业受众最常用的独立 AI 搜索工具。专注于新鲜度（每月更新内容）、域名权威度，以及将内容结构匹配 ChatGPT 格式化响应的方式。

**然后扩展到 Perplexity**——如果你的受众包括研究人员、早期采用者或技术专业人士，特别有价值。添加 FAQ Schema，发布 PDF 资源，以清晰、独立的段落写作。

**Copilot 和 Claude 优先级较低**，除非你的受众偏向企业/Microsoft（Copilot）或开发者/分析师（Claude）。但基础要素——结构化内容、引用来源、Schema 标记——对所有平台都有帮助。

**到处都有帮助的行动：**
1. 在 robots.txt 中允许所有 AI 机器人
2. 实现 Schema 标记（至少 FAQPage、Article、Organization）
3. 在内容中包含带具名来源的统计数据
4. 定期更新内容——竞争性主题每月
5. 使用清晰的标题结构（H1 > H2 > H3）
6. 保持页面加载时间在 2 秒以下
7. 添加带资历的作者简介
