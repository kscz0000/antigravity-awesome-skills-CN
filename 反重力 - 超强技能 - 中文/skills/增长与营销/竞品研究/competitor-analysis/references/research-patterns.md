# 竞品分析 — 研究模式

## 目录
- [概览](#概览) — 两种研究上下文（自身 vs 目标）
- [自身研究（用户公司）](#自身研究用户公司) — 子问题、页面发现、合成输出（precise_category、include keywords、exclusion list）
- [竞品研究 — 4 条研究赛道](#竞品研究--4-条研究赛道) — Marketing / External / Benchmarks / Strategic Diff
- [深度模式行为](#深度模式行为) — quick / deep / deeper 的预算与范围
- [Finding 格式（按赛道）](#finding-格式按赛道) — JSON 结构、置信度
- [研究循环规则](#研究循环规则) — 研究阶段的 7 条元规则
- [合成指令](#合成指令) — 将 findings 转化为矩阵单元格

## 概览

两种研究上下文：
1. **自身研究**（Step 1）— 深度研究用户公司，以便我们知道本次运行中"竞品"指什么。
2. **竞品研究**（Step 4）— 对每个发现/播种的竞品，运行下面的 4 条赛道 enrichment。

两者都使用 Plan → Research → Synthesize 模式。自身研究的结构与 `company-research` 中的完全一致，因此画像可在多个技能间复用。

## 自身研究（用户公司）

### 子问题
- "{company} 卖什么，具体解决什么问题？"
- "{company} 的现有客户是谁？涉及哪些行业、公司规模、使用场景？"
- "{company} 已知的竞品是谁？他们在哪个品类中竞争？"
- "{company} 使用什么定价模式？"
- "{company} 的营销强调哪些功能、集成和差异化优势？"

### 页面发现
通过 sitemap 动态发现 —— 不要硬编码 `/about` 或 `/pricing`：
1. `browse cloud fetch --allow-redirects "{company website}/sitemap.xml"` — 主要来源
2. 扫描包含关键词的 URL：`pricing`、`customer`、`compare`、`vs`、`about`、`features`、`integrations`
3. 可选地获取 `/llms.txt` 获取页面描述
4. 挑选 3-5 个最相关的 URL

### 外部研究
- `browse cloud search "{company} alternatives competitors vs"`
- `browse cloud search "{company} review comparison"`
- 获取 1-2 个最有信息量的第三方页面

### 合成输出
产出包含以下内容的画像：
- **Company**、**Product**、**Existing Customers**、**Competitors**（种子列表）、**Use Cases**
- **precise_category** — 用一句清晰的话描述该产品在哪个品类竞争。避免模糊的词如"工具"或"平台"。好的例子："面向智能体的 AI 网页搜索 API，具备神经 + 关键词检索"。差的例子："搜索工具"。这将成为发现查询和 gate 的锚点。
- **category_include_keywords** — 8-15 个*直接竞品*营销中极可能出现的短语（标题或 hero 中）。包括语义变体。例如对 Exa：`web search api`、`search api`、`neural search`、`semantic search`、`retrieval api`、`search for ai agents`、`search for llms`、`serp api`、`embeddings search`、`live crawling`、`answer api`、`research api`。
- **exclusion_list** — 表明属于*不同品类*的短语，供 gate 用于拒绝假阳性。例如 `vector database`、`enterprise search appliance`、`site search widget`、`observability`、`analytics platform`、`data warehouse`、`scraping platform`（完整 ETL/抓取套件，而非检索 API）、`internal knowledge base`。

使用 `company-research` 中相同的 `profiles/{company-slug}.json` 结构，并扩展上述三个新字段。`competitors` 数组成为种子列表，也是 Step 3 中对比图扩展的初始输入。

---

## 竞品研究 — 4 条研究赛道

对每个竞品运行以下四条赛道（按深度门控）：

### 赛道 1 — 营销表面（所有深度模式）
目标：从竞品自己的网站提取他们对自己的描述。

**子问题**：
- "{competitor} 卖什么，面向谁，如何定位？"
- "{competitor} 的价格层级和定价模式是什么？"
- "{competitor} 列出了哪些关键功能、集成和平台？"

**要获取的页面**（通过 sitemap 发现 —— 不要硬编码）：
1. 首页
2. `/pricing`（或 sitemap 中等价路径）
3. `/features`、`/product`、`/platform`、`/solutions`
4. `/integrations`、`/customers`、`/case-studies`

**提取到 frontmatter 字段**：`tagline`、`positioning`、`product_description`、`target_customer`、`pricing_model`、`pricing_tiers`、`key_features`、`integrations`。

### 赛道 2 — 外部信号（deep + deeper）
目标：互联网其他地方对他们的看法。

**子问题**：
- "有哪些第三方对比页面提到了 {competitor}？"
- "Reddit、HN、G2、Capterra 上用户怎么说？"
- "最近的新闻、发布或公告？"
- "谁在 LinkedIn 或 YouTube 上谈论他们？"

**搜索查询**：
```
"{competitor} vs"
"{competitor} alternatives"
"{competitor} review"
"{competitor} G2" / "{competitor} Capterra"
"site:reddit.com {competitor}"
"site:news.ycombinator.com {competitor}"
"site:linkedin.com/posts {competitor}"
"site:youtube.com {competitor}"
"{competitor} launch 2025 OR 2026"
"{competitor} funding announcement"
```

**提取规则**：从搜索结果中，将每个命中收集为 `Mentions` 条目。根据 URL 分类来源类型：
- `reddit.com` → `Reddit`
- `news.ycombinator.com` → `HN`
- `linkedin.com` → `LinkedIn`
- `youtube.com` / `youtu.be` → `YouTube`
- `g2.com` / `capterra.com` / `trustradius.com` → `Review`
- 路径或标题中包含 `*vs*` → `Comparison`
- 新闻域名（techcrunch、theverge、venturebeat、forbes、businesswire、globenewswire）→ `News`
- `twitter.com` / `x.com` → `X`
- `spotify.com/episode` / transistor / simplecast → `Podcast`

对于 LinkedIn 和 YouTube，`browse cloud search` 的摘要 + URL 已足够。**不要**试图深度获取单个 LinkedIn 帖子（认证墙）—— 用标题/摘要列出即可。

### 赛道 3 — 公开基准（仅 deeper）
目标：找到测量过该竞品的第三方基准。

**子问题**：
- "{competitor} 是否被纳入任何公开基准？"
- "是否有 GitHub 仓库、PR 或博客在某个测量维度（速度、准确性、成本、通过率）上直接对比 {competitor}？"

**搜索查询**：
```
"{competitor} benchmark"
"{competitor} performance test"
"site:github.com {competitor} benchmark"
"site:github.com {competitor} vs"
"{competitor} vs {seed_competitor} benchmark"   # pairwise, use another known competitor as the seed
"{category} benchmark {competitor}"             # e.g. "web search api benchmark {competitor}"
```

**提取**：将每个命中加入 `Benchmarks` 章节，包含：title、source、URL、关键发现（一行）。同时镜像到 `Mentions` 中，类型为 `Benchmark`。

**需直接检查的已知基准仓库**（若领域相关）：
- 公开检索质量排行榜（如 BEIR / MTEB 类仓库），前提是供应商公布了分数
- 通过第一波搜索发现的品类特定基准仓库

### 赛道 4 — 相对用户公司的战略差异（仅 deeper）
目标：明确地将该竞品与用户公司对比。

**输入**：`{user_company_profile}`（来自 Step 1）—— 特别是 `product`、`use_cases`、`key_features`（若可用）。

**子问题**：
- "{competitor} 有哪些 {user_company} 没有的功能？"
- "{user_company} 有哪些 {competitor} 没有的功能？"
- "{competitor} 服务了哪些 {user_company} 没有服务的客户（反之亦然）？"
- "在营销表面（价格、功能深度、DX、生态）上，谁胜一筹？"

此赛道**无需新的抓取** —— 这是基于赛道 1+2+3 的发现以及用户画像的合成步骤。写成：

```markdown
## Comparison vs {user_company}
- **Overlaps**: ...
- **Gaps**: ...
- **Where they win**: ...
- **Where you win**: ...
```

同时用单行摘要填充 `strategic_diff` frontmatter 字段，供概览表使用。

---

## 深度模式行为

### Quick 模式（竞品多、便宜）
- **赛道**：仅 1
- **预算**：每个竞品 2-3 次工具调用（首页 + 定价页）
- **填充字段**：tagline、product_description、pricing_tiers、key_features
- **Mentions / Benchmarks / Comparison**：跳过

### Deep 模式（均衡，默认）
- **赛道**：1 + 2
- **预算**：每个竞品 5-8 次工具调用
- **quick 中的全部** + 跨来源类型的 5-10 条 mentions

### Deeper 模式（完整情报）
- **赛道**：1 + 2 + 3 + 4
- **预算**：每个竞品 10-15 次工具调用
- **deep 中的全部** + benchmarks 章节 + strategic diff 章节

---

## Finding 格式（按赛道）

每个 finding 都是绑定来源的事实陈述：

```json
{
  "lane": "marketing | external | benchmark | strategic",
  "fact": "Rival Co charges $99/mo for 10K search requests",
  "sourceUrl": "https://rivalco.com/pricing",
  "confidence": "high"
}
```

**置信度**：
- `high`：直接出现在竞品自己的网站或官方新闻中
- `medium`：从第三方文章、评论或招聘信息推断
- `low`：推测性 / 来源过时

## 研究循环规则

1. **先跑赛道 1** — 总是从竞品自己的网站开始
2. **使用 sitemap 而非硬编码路径** — `/pricing` 可能是 `/plans` 或 `/pricing-plans`
3. **换关键词而非重试** — 若搜索返回泛化垃圾，换关键词
4. **有选择地获取** — 每个查询挑选 1-2 个最有希望的 URL
5. **LinkedIn/YouTube：仅搜索，不获取** — 摘要足够，避免认证墙
6. **遵守各深度模式的步骤预算**
7. **去重 mentions** — 同一 URL 在 `## Mentions` 中只能出现一次

## 合成指令

竞品的研究循环完成后：

1. 从赛道 1 的发现填充 frontmatter 字段
2. 撰写正文章节：Product、Pricing、Features、Positioning（均来自赛道 1）
3. 从赛道 2 分类的命中追加 `## Mentions`
4. 从赛道 3（仅 deeper）追加 `## Benchmarks`
5. 从赛道 4 的合成（仅 deeper）追加 `## Comparison vs {user_company}`
6. 追加 `## Research Findings` 作为带置信度标签的原始发现附录

不输出 ICP 分数。不输出威胁分数。只有情报。

若某字段没有支撑发现，留空而非猜测。