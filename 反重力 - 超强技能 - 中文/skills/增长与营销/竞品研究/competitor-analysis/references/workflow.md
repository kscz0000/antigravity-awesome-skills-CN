# 竞品分析 — 工作流参考

## 目录
- [Discovery Batch JSON Schema](#discovery-batch-json-schema) — browse cloud search 输出格式
- [竞品研究 Markdown 格式](#竞品研究-markdown-格式) — frontmatter + 正文章节规范
- [提取页面文本](#提取页面文本) — browse cloud fetch（默认 markdown；HTML 用 --format raw）
- [Discovery — 并行 Bash，而非子代理](#discovery--并行-bash而非子代理) — Wave A/B/C 配方
- [Enrichment 扇出 — 每个竞品 5 个子代理](#enrichment-扇出--每个竞品-5-个子代理deepdeeper-模式) — 5-lane 划分
- [遗留：单子代理模板](#遗留单子代理模板quick-模式) — 仅 quick 模式
- [波次管理](#波次管理) — 并行规则、gate 阶段、规模公式
- [报告编译](#报告编译) — compile_report.mjs 调用

## Discovery Batch JSON Schema

文件：`/tmp/competitor_discovery_batch_{N}.json`

`browse cloud search --output` 写入一个 JSON 对象：

```json
{
  "requestId": "abc123",
  "query": "alternatives to acme",
  "results": [
    { "id": "...", "url": "https://example.com", "title": "Example Corp", "image": null, "favicon": null }
  ]
}
```

`list_urls.mjs` 脚本（使用 `--prefix competitor` 运行）跨 batch 去重。

## 竞品研究 Markdown 格式

文件：`{OUTPUT_DIR}/{competitor-slug}.md` — 完整模板见 `references/example-research.md`。

**YAML frontmatter 字段**（`compile_report.mjs` 使用）：
- `competitor_name`（必需）
- `website`（必需）
- `tagline`
- `positioning`
- `product_description`
- `target_customer`
- `pricing_model`
- `pricing_tiers`（管道分隔：`Free | Pro $99 | Enterprise Contact`）
- `key_features`（管道分隔）
- `integrations`（管道分隔）
- `headquarters`
- `founded`
- `employee_estimate`
- `funding_info`
- `strategic_diff`（概览表用的单行；仅 deeper 模式）

**正文章节**（按此顺序 — `compile_report.mjs` 按标题解析）：
- `## Product`
- `## Pricing`
- `## Features`
- `## Positioning`
- `## Comparison vs {user_company}`（仅 deeper）
- `## Mentions`
- `## Benchmarks`（仅 deeper）
- `## Research Findings`

**Mentions 行格式**（被解析进 mentions feed）：
```
- **[SourceType]** Title | Snippet (source: URL, YYYY-MM-DD)
```
`SourceType` ∈ `Benchmark | Comparison | News | Reddit | HN | LinkedIn | YouTube | Review | Podcast | X`。日期可选但推荐。

## 提取页面文本

`browse cloud fetch --allow-redirects` 默认返回干净的 **markdown** — 无需剥离 HTML。只需限制长度：

```bash
browse cloud fetch --allow-redirects "https://rivalco.com/pricing" | head -c 3000
```

若需要原始 HTML（例如读取 `<title>` 标签或解析标记），加上 `--format raw` 并剥离标签：

```bash
browse cloud fetch --allow-redirects --format raw "https://rivalco.com/pricing" | sed 's/<script[^>]*>.*<\/script>//g; s/<style[^>]*>.*<\/style>//g; s/<[^>]*>//g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&nbsp;/ /g; s/&#[0-9]*;//g' | tr -s ' \n' | head -c 3000
```

每页限制约 3000 字符以保持子代理上下文可控。对于 JS 重度（客户端渲染定价表）的页面，若 Fetch API 返回内容稀薄，使用浏览器会话打开：`browse open "{url}" --remote` 然后 `browse get markdown`。

## Discovery — 并行 Bash，而非子代理

主代理将 discovery 作为 **3 个并行 `browse cloud search` Bash 调用**（每波一个）在**单条消息**中执行。没有子代理层。每波用 `&&` 链接其 2-4 个查询，并将结果写入 `/tmp/competitor_discovery_batch_{wave}{N}.json`。

示例 — 主代理在一条消息中并行发起以下三个 Bash 工具调用：

```bash
# Wave A — alternatives
browse cloud search "alternatives to {user_company}" --num-results 12 --output /tmp/competitor_discovery_batch_A1.json && \
browse cloud search "{user_company} competitors" --num-results 12 --output /tmp/competitor_discovery_batch_A2.json && \
echo "A done"
```

```bash
# Wave B — precise category
browse cloud search "{precise_category}" --num-results 12 --output /tmp/competitor_discovery_batch_B1.json && \
browse cloud search "{compose 3 distinctive tokens}" --num-results 12 --output /tmp/competitor_discovery_batch_B2.json && \
browse cloud search "{primary_noun} for ai agents" --num-results 12 --output /tmp/competitor_discovery_batch_B3.json && \
echo "B done"
```

```bash
# Wave C — comparison-page graph
browse cloud search "{user_company} vs" --num-results 12 --output /tmp/competitor_discovery_batch_C1.json && \
browse cloud search "{seed1} vs" --num-results 12 --output /tmp/competitor_discovery_batch_C2.json && \
browse cloud search "{seed2} vs" --num-results 12 --output /tmp/competitor_discovery_batch_C3.json && \
echo "C done"
```

为什么直接用 Bash 而非子代理：每波仅 2-4 次 `browse cloud search` 调用 —— 代理冷启动 + 工具推理开销大于实际工作。使用并行 Bash 可每次运行节省约 1-2 分钟且无质量损失。

### Discovery 查询模式

Discovery 使用**三个并行波**（已评估 —— 三波均具增量价值）：

**Wave A — 通用替代品**（宽网，噪声多）：
- `"alternatives to {user_company}"`
- `"{user_company} competitors"`

**Wave B — 精确品类查询**（使用自身研究中的 `precise_category`）：
- `"{precise_category}"` 字面
- `"{precise_category_2_3_keywords}"` — 挑选 3 个最具区分度的 token
- 与 "API"、"cloud"、"for agents" 组合：`"cloud {primary_noun} for ai agents"`、`"{primary_noun} infrastructure API"`

**Wave C — 对比页面图**（单波最高精度）：
- `"{user_company} vs"`
- 对用户画像中每个种子竞品，也运行 `"{seed} vs"`
- 搜索后，`scripts/extract_vs_names.mjs` 解析所有 Wave C 结果中的 `"X vs Y"` 标题，挖掘未作为 URL 出现的候选名称。

**评估结果**（在一次 search-API 运行中测试）：Wave A 返回约 10% 的真实竞品（多为 AI 工具目录聚合）。Wave B 返回约 35%。Wave C 通过标题解析独占地挖掘出 A 和 B 都没找到的具名品牌。三波都用。

## Enrichment 扇出 — 每个竞品 5 个子代理（deep/deeper 模式）

对每个通过 gate 的竞品，并行启动**五个子代理**，每个负责一条赛道。每个子代理将 *partial* 写入 `{OUTPUT_DIR}/partials/{slug}.{lane}.md`。所有子代理完成后，`scripts/merge_partials.mjs` 将 partials 合并为每个竞品一份的标准 `{OUTPUT_DIR}/{slug}.md`（按 URL 去重 mentions，按日期降序排列）。

5 条赛道：

| 赛道 | Slug | 范围 |
|------|------|-------|
| **A. Marketing** | `marketing` | 拥有规范 frontmatter。定价、功能、定位、集成、客户、目标、团队、融资、总部。首页 + sitemap 驱动的页面发现。 |
| **B. Discussion** | `discussion` | Reddit、HN、论坛、dev.to、hashnode。超出 `site:` 限制的更宽查询 — 还有 `"{competitor}" discussion`、`"{competitor}" review 2026`、`"{competitor}" issues OR problems`。写入带日期的 Mentions 条目。 |
| **C. Social** | `social` | LinkedIn 帖子、YouTube 视频、Twitter/X 线程。仅搜索摘要 — 不获取（认证墙）。 |
| **D. News & Comparisons** | `news` | 对比页面（"X vs Y"）、TechCrunch / Verge / Forbes / VentureBeat / Businesswire、独立博客评论、Substack。每条 mention 必须包含日期。 |
| **E. Technical & Benchmarks** | `technical` | GitHub 基准仓库/PR、性能博客、独立测试。写入 Benchmarks 条目以及关于技术细节的 Findings（检索模式、延迟、速率限制、SDK）。 |

**波次管理 — 在单条消息中启动所有子代理**：对 N 个竞品 × 5 赛道 = 5N 个子代理，全部塞进单条 Agent 工具消息。挂钟时间则等于最慢的单个子代理（约 3-5 分钟），而非 `批次数 × 单批最慢`。在真实的 10 竞品运行中，我们测得自我限速到每消息 10 个浪费了 25 分钟 —— Agent 工具可并行跑 50+ 个；不要因"礼貌"而分批。唯一限制是每个子代理仍须将自身的 Bash 操作批处理为一次调用。

**合并步骤**（所有 partials 都就位后）：
```bash
node {SKILL_DIR}/scripts/merge_partials.mjs {OUTPUT_DIR}
```
产出每个竞品一份 `{OUTPUT_DIR}/{slug}.md`，含去重后的 Mentions（按日期降序）、Benchmarks 和 Findings。

## 遗留：单子代理模板（仅 quick 模式）

`quick` 模式下，每个竞品批保留一个单子代理（无扇出 —— 仅赛道 1，每个 2-3 次调用预算）。

```
You are a competitor enrichment subagent. For each competitor URL, run the 4-lane research
pattern and write a single markdown file per competitor.

CONTEXT:
- User's company: {user_company}
- User's product: {user_product}
- User's key features: {user_key_features}
- Depth mode: {depth_mode}   (quick | deep | deeper)
- Output directory: {OUTPUT_DIR}   ← write files HERE, as a full literal path

COMPETITOR URLS TO PROCESS:
{url_list}

TOOL RULES — CRITICAL, FOLLOW EXACTLY:
1. You may ONLY use the Bash tool. No exceptions.
2. All searches: Bash → browse cloud search "..." --num-results 10
3. All page fetches: Bash → browse cloud fetch --allow-redirects "..."
   browse cloud fetch returns clean markdown by default — just `| head -c 3000`, no HTML stripping.
   If you need the raw HTML, add --format raw and pipe through:
   sed 's/<script[^>]*>.*<\/script>//g; s/<style[^>]*>.*<\/style>//g; s/<[^>]*>//g' | tr -s ' \n' | head -c 3000
   If a page returns thin content or "enable JavaScript", use `browse open "{url}" --remote` then `browse get markdown`.
4. BATCH all file writes: Write ALL markdown files in a SINGLE Bash call using chained heredocs.
5. BANNED TOOLS: WebFetch, WebSearch, Write, Read, Glob, Grep — ALL BANNED.
6. NEVER use ~ or $HOME in paths — use full literal paths.

RESEARCH PATTERN (per competitor — lanes are depth-gated):

LANE 1 — Marketing Surface (always run):
  a. Fetch competitor homepage
  b. Discover via sitemap: /sitemap.xml — find /pricing, /features, /integrations, /customers
  c. Fetch 2-4 most relevant pages
  d. Extract: tagline, positioning, product_description, target_customer,
     pricing_model, pricing_tiers, key_features, integrations

LANE 2 — External Signal (deep + deeper):
  Run these searches:
    browse cloud search "{competitor} vs"
    browse cloud search "{competitor} alternatives review"
    browse cloud search "site:reddit.com {competitor}"
    browse cloud search "site:news.ycombinator.com {competitor}"
    browse cloud search "site:linkedin.com/posts {competitor}"
    browse cloud search "site:youtube.com {competitor}"
    browse cloud search "{competitor} G2 OR Capterra"
    browse cloud search "{competitor} launch OR funding 2025 OR 2026"

  For each search result, classify source type from URL:
    reddit.com → Reddit
    news.ycombinator.com → HN
    linkedin.com → LinkedIn
    youtube.com/youtu.be → YouTube
    twitter.com/x.com → X (or Twitter — either works)
    dev.to → DevTo
    hashnode.dev, hashnode.com → Hashnode
    *.substack.com → Substack
    spotify.com/episode, transistor.fm, simplecast.com → Podcast
    g2.com/capterra.com/trustradius.com → Review
    url or title contains "vs" → Comparison
    techcrunch/theverge/venturebeat/forbes/businesswire/wired/fortune → News
    other blog domain → Blog

  Record each as a Mentions line with title + one-line snippet + URL + **date**. Always include
  the date when available. If a `browse cloud search` result carries a date field, prefer it.
  If absent, parse the year from title/URL (e.g. "2026" or `/2025/11/` in a news URL).
  For LinkedIn and YouTube — use search snippet only, do NOT fetch the page.

LANE 3 — Public Benchmarks (deeper only):
  Run these searches:
    browse cloud search "{competitor} benchmark"
    browse cloud search "site:github.com {competitor} benchmark"
    browse cloud search "{category} benchmark {competitor}"

  Record each hit in ## Benchmarks with: title, source, URL, one-line key finding.
  Also append to ## Mentions with type Benchmark.

LANE 4 — Strategic Diff vs {user_company} (deeper only):
  Using Lane 1-3 findings + the user's company profile, write:
  ## Comparison vs {user_company}
  - Overlaps: ...
  - Gaps: ...
  - Where they win: ...
  - Where you win: ...
  Also fill the `strategic_diff` frontmatter field with a one-line summary.

HARD TOOL-CALL CAP — count your browse cloud calls and STOP at the cap. Partial output beats blocking the pipeline.
  quick mode:   3 browse cloud calls max per competitor
  deep mode:    8 browse cloud calls max per competitor
  deeper mode:  12 browse cloud calls max per competitor

ENFORCEMENT — at the start of every Bash call, prepend a comment like
  # browse call N/8 (deep mode)
After hitting the cap, write the output file with WHAT YOU HAVE — even if a section is thin.
NEVER do a 9th call in deep mode "to be thorough". The pipeline budgets time on this assumption.

Observed cost of overshoot (Apr 25 search-API run): two lanes hit 29-30 calls each, drove
wall-clock for the whole 30-agent fan-out from 5 min → 12 min. Don't do this.

OUTPUT — write ALL competitor files in a SINGLE Bash call using chained heredocs directly to {OUTPUT_DIR}:

cat << 'COMPETITOR_MD' > {OUTPUT_DIR}/{slug1}.md
---
competitor_name: {name}
website: {url}
tagline: {tagline}
positioning: {positioning}
product_description: {description}
target_customer: {audience}
pricing_model: {model}
pricing_tiers: {tier1} | {tier2} | {tier3}
key_features: {f1} | {f2} | {f3}
integrations: {i1} | {i2}
headquarters: {hq}
founded: {year}
employee_estimate: {estimate}
funding_info: {funding}
strategic_diff: {one line — deeper only}
---

## Product
{paragraph}

## Pricing
{bullets per tier}

## Features
{bullets}

## Positioning
{paragraph}

## Comparison vs {user_company}    ← deeper only
- Overlaps: ...
- Gaps: ...
- Where they win: ...
- Where you win: ...

## Mentions
- **[SourceType]** Title | Snippet (source: URL, YYYY-MM-DD)

## Benchmarks                       ← deeper only
- Title | Source | URL | Key finding

## Research Findings
- **[confidence]** Fact (source: URL)
COMPETITOR_MD
cat << 'COMPETITOR_MD' > {OUTPUT_DIR}/{slug2}.md
...
COMPETITOR_MD

Use 'COMPETITOR_MD' (quoted) as the heredoc delimiter to prevent shell variable expansion.

Report back ONLY: "Batch {batch_id}: {succeeded}/{total} competitors researched, {mentions_count} mentions, {benchmarks_count} benchmarks."
Do NOT return raw data to the main conversation.
```

## 波次管理

### 关键原则：最大化并行，最小化提示
**在一条消息中启动该阶段所需的所有子代理。** 没有"每消息最多 6 个"的限制 — Agent 工具并行跑它们，所以挂钟时间 = 最慢的单代理，与数量无关。在 10 竞品 × 5 赛道 = 50 子代理 enrichment 中，分成 5 批每批 10 个比单批 50 个多花 20 分钟挂钟时间（2026 年 4 月实测）。每个子代理仍必须将其自身的 Bash 操作批处理为一次调用。

### Discovery 阶段
- **将 discovery 作为并行 `browse cloud search` Bash 调用运行，而非子代理。** 子代理开销（冷启动 + 工具推理）大于工作量。三次 Bash 工具调用在一条消息中 —— 每波一次 — 用 `&&` 链接每波的搜索。
- 每波的 bash 调用将输出写入 `/tmp/competitor_discovery_batch_{wave}{N}.json`
- 所有波完成后，按顺序运行：
  ```bash
  # 1. Dedup URLs from all batches
  node {SKILL_DIR}/scripts/list_urls.mjs /tmp --prefix competitor > /tmp/competitor_urls.txt

  # 2. Extract candidate names from "X vs Y" titles (Wave C output)
  node {SKILL_DIR}/scripts/extract_vs_names.mjs /tmp --prefix competitor \
    --seed "{user_company},{seed1},{seed2},{seed3}" \
    > /tmp/competitor_vs_names.jsonl
  ```
- **过滤 URL**：移除博客文章、新闻文章、AI 工具目录（seektool.ai、respan.ai、agentsindex.ai、toolradar.com、aitoolsatlas.ai、aidirectory.com、vibecodedthis.com、aichief.com、openalternative.co、cbinsights.com、saasworthy.com、softwareworld.com）、评测聚合（g2.com、capterra.com、trustradius.com）、数据库（crunchbase.com、tracxn.com）以及用户自己的域名。只保留候选公司首页。
- 对于来自 `extract_vs_names.mjs` 但未解析到域名的名称，可选地运行 `browse cloud search "{name}" --num-results 3` 解析顶级域名；若歧义则跳过。
- **合并**：过滤后的 URL 列表 ∪ 已解析的 `vs_names` 域名 ∪ 用户提供的种子 URL。按 hostname 去重到 `/tmp/competitor_candidates.txt`。

### 用户确认阶段（在 gate 与 enrichment 之间 — 强制）

在 gate 写入 `/tmp/competitor_gated.jsonl` 之后，主代理**必须**询问用户确认 enrichment 集合，然后再启动子代理。Enrichment 是每个竞品 25 子代理 × 深度预算 — 在猜测上跑太贵了。

向用户呈现三个桶：
1. **PASS** — status=PASS 的行及标题
2. **UNKNOWN** — status=UNKNOWN（获取失败；总是一种静默漏失风险 — JS 重度首页、Cloudflare 挑战）
3. **被拒绝的品牌匹配** — 约 10 行标题中含种子 token 或在 Wave C "X vs Y" 图中反复出现的 REJECT 行

然后使用 `AskUserQuestion` 弹出复选框列表 + 自由文本"添加更多"。将确认的集合写入 `/tmp/competitor_enrichment_set.txt`（每行一个 URL）。那个文件 — 而非 `/tmp/competitor_passed.txt` — 是 enrichment 子代理的输入。

需主动暴露的已知 gate 盲点：
- JS 重度落地页返回几乎为空的 hero 文本 → gate 的关键词匹配器无内容可咬
- Cloudflare 挑战标题（"Just a moment..."） → 明显的假阴性
- "Search foundation" / "retrieval backbone" / "agent runtime" — 品类的语义变体不在词法上匹配
- 顶级域 vs 产品子域（如浏览器 `brave.com` vs 实际 API 产品 `api-dashboard.search.brave.com`）

### Gate 阶段（在 discovery 和 enrichment 之间）

在 enrichment 烧掉工具调用之前，先剔除错误品类的候选。

```bash
cat /tmp/competitor_candidates.txt \
  | node {SKILL_DIR}/scripts/gate_candidates.mjs \
      --include "{category_include_keywords_csv}" \
      --exclude "{exclusion_list_csv}" \
      --concurrency 6 \
  > /tmp/competitor_gated.jsonl

# Extract PASS-only URLs for enrichment
grep '"status":"PASS"' /tmp/competitor_gated.jsonl \
  | node -e 'require("fs").readFileSync(0,"utf-8").split("\n").filter(Boolean).forEach(l => { try { console.log(JSON.parse(l).url); } catch {} })' \
  > /tmp/competitor_passed.txt
```

**关键词来源**：
- `--include` ← 画像中的 `category_include_keywords`（逗号连接）。
- `--exclude` ← 画像中的 `exclusion_list`。

**Gate 逻辑**（位置感知）：若 `<title>` 中含 exclude 词则 REJECT；若 `<title>` 中含 include 词则 PASS；对于同时包含两者的混合标题（例如 "Browser Automation & Web Scraping API"），以前 200 字符的 hero 文本决胜负；否则回退到整段 hero 宽检。默认保守。

**审视输出** — 主代理应抽查两个列表，并可手动重新纳入自己识别出的已知直接竞品的 REJECT（其自身营销对品类而言是歧义的）。

**在某 search-API 运行上的评估**（12 个候选）：7/7 真实竞品 PASS；4/4 错误品类（向量数据库、抓取/ETL 平台、分析工具、内部 KB 搜索）REJECT。一例分裂身份边缘情况（一个搜索供应商同时也卖抓取套件）被拒绝 — 可接受。

### Enrichment 阶段

两种模式：

- **`quick` 模式** — 每个竞品批一个单子代理。仅赛道 A（marketing）。每子代理约 8 个竞品，每个 2-3 次工具调用。直接写入 `{OUTPUT_DIR}/{slug}.md`。
- **`deep` / `deeper` 模式** — 每个竞品 5 子代理扇出。每个子代理拥有**一条**赛道（marketing / discussion / social / news / technical）。写入 `{OUTPUT_DIR}/partials/{slug}.{lane}.md`。预算：deep 每个子代理 5-8 次调用，deeper 10-15 次。所有赛道完成后，运行 `scripts/merge_partials.mjs` 合并。
- **在单条 Agent 工具消息中启动所有竞品 × 赛道子代理。** 对 10 竞品 × 5 赛道 = 50 个并行代理在一条消息中。**不要**拆批 — 挂钟时间变成最慢单代理（约 3-5 分钟）而非批次 × 批最大（约 25 分钟在 10 竞品拆成 5 轮 10 个的情况下）。

### Screenshots 阶段（merge 之后、compile 之前）

为每个竞品截取首页 hero 截图：
```bash
node {SKILL_DIR}/scripts/capture_screenshots.mjs {OUTPUT_DIR} --mode remote --concurrency 1
```
需要 `browse` CLI（`npm install -g browse`）。`--mode remote` 驱动 Browserbase 会话（脚本在每个 `browse` 命令上加 `--remote`）；本地 Chrome 用 `--mode local`。将每个竞品一个 PNG 写入 `{OUTPUT_DIR}/screenshots/{slug}-hero.png`。`compile_report.mjs` 在存在时自动将 hero 嵌入每个竞品的 HTML 页面。

成本：每竞品约 10-20 秒（串行）。5 个竞品总计约 60 秒。

### 规模公式
```
search_queries = ceil(requested_competitors / 20)   # discovery is narrower than lead gen
discovery_subagents = ceil(search_queries / 3)
expected_urls = search_queries * 15

quick:   research_subagents = ceil(expected_urls / 8)
deep:    research_subagents = ceil(expected_urls / 4)
deeper:  research_subagents = ceil(expected_urls / 2)
```

### 错误处理
- 若子代理失败，记录并继续剩余批次
- 若某波 >50% 子代理失败，暂停并告知用户
- 若 `browse cloud fetch --allow-redirects` 失败，尝试 `browse open "{url}" --remote` + `browse get markdown` 作为后备，或跳过该页

## 报告编译

所有 enrichment 子代理完成后，一次性编译所有 HTML 视图：

```bash
node {SKILL_DIR}/scripts/compile_report.mjs {OUTPUT_DIR} --user-company "{user_company}" --open
```

脚本：
- 读取 `{OUTPUT_DIR}` 中的所有 `.md` 文件
- 解析 YAML frontmatter + 正文章节
- 按归一化的竞品名称去重
- 生成 `{OUTPUT_DIR}/index.html` — 概览表（名称、tagline、定价、关键功能、strategic diff）
- 生成 `{OUTPUT_DIR}/competitors/{slug}.html` — 每个竞品的深度页面
- 生成 `{OUTPUT_DIR}/matrix.html` — 跨竞品的并排功能/定价网格
- 生成 `{OUTPUT_DIR}/mentions.html` — 带来源类型徽章 + 客户端过滤的按时间排序的信息流
- 生成 `{OUTPUT_DIR}/results.csv` — 平面电子表格
- 在默认浏览器中打开 `index.html`（`--open` 标志）
- 将 JSON 摘要打印到 stderr