---
name: competitor-analysis
description: "通过 Browserbase 发现、富集通道、截图、对比矩阵和 HTML 报告来研究竞品。触发词：竞品分析、competitor analysis、市场调研、竞争情报、竞品监控"
license: MIT
compatibility: Requires the browse CLI (npm install -g browse) and BROWSERBASE_API_KEY env var
allowed-tools: Bash Agent AskUserQuestion
metadata:
  author: browserbase
  version: "0.2.0"
category: "marketing"
risk: "safe"
source: "official"
source_repo: "browserbase/skills"
source_type: "official"
date_added: "2026-06-19"
author: "Browserbase"
license_source: "https://github.com/browserbase/skills/blob/main/skills/competitor-analysis/LICENSE.txt"
tags:
  - competitor-analysis
  - browserbase
  - market-research
  - browser-automation
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 竞品分析

## 何时使用

当用户需要结构化的竞品研究，包含 Browserbase 发现、富集通道、截图、对比矩阵以及最终的 HTML 报告时使用。

_来源：[browserbase/skills](https://github.com/browserbase/skills) (MIT)。_

分析用户的竞品。使用 Browserbase Search API 进行发现，并采用 4 通道 Plan→Research→Synthesize 模式进行富集——输出包含概览、每个竞品的深度分析、并排的功能/定价矩阵以及按时间顺序排列的提及动态的 HTML 报告。

**前置条件**：需要 `BROWSERBASE_API_KEY` 环境变量以及安装好的 `browse` CLI（`npm install -g browse`）。

**首次运行设置**：首次运行时，系统会提示你批准 `browse cloud fetch`、`browse cloud search`、`cat`、`mkdir`、`sed` 等命令。请为每条命令选择 **"Yes, and don't ask again for: browse cloud fetch:\*"**（或等效选项）。要永久批准，请将这些命令添加到你的 `~/.claude/settings.json` 中 `permissions.allow` 字段下：
```json
"Bash(browse:*)", "Bash(bunx:*)", "Bash(bun:*)", "Bash(node:*)",
"Bash(cat:*)", "Bash(mkdir:*)", "Bash(sed:*)", "Bash(head:*)", "Bash(tr:*)", "Bash(rm:*)"
```

**路径规则**：在 Bash 中始终使用完整的字面路径——不要使用 `~` 或 `$HOME`。先解析一次主目录并全程使用。构建子代理提示时，请将 `{SKILL_DIR}` 替换为完整的字面路径。

**输出目录**：所有输出都放到 `~/Desktop/{company_slug}_competitors_{YYYY-MM-DD}/`。该目录包含每个竞品一个 `.md` 文件以及生成的 HTML 视图和 CSV。

**关键——工具限制（适用于主代理及所有子代理）**：
- 所有网页搜索：使用 `browse cloud search`。禁止使用 WebSearch。
- 所有页面抓取：使用 `browse cloud fetch --allow-redirects`（默认返回 markdown；如果需要原始 HTML，请添加 `--format raw`，然后通过 `sed ... | tr -s ' \n'` 管道提取文本）。禁止使用 WebFetch。1 MB 的响应上限——对于重 JS 页面，回退到 `browse get markdown`（在 `browse open <url> --remote` 之后）。
- 所有研究输出：子代理使用 bash heredoc **为每个竞品编写一个 markdown 文件**到 `{OUTPUT_DIR}/{competitor-slug}.md`。禁止使用 Write 工具或 `python3 -c`。文件格式参见 `references/example-research.md`。
- 报告编译：使用 `node {SKILL_DIR}/scripts/compile_report.mjs {OUTPUT_DIR} --user-company "{user_company}" --open`——一步生成 `index.html`、`competitors/*.html`、`matrix.html`、`mentions.html`、`results.csv` 并打开概览。
- URL 去重：`node {SKILL_DIR}/scripts/list_urls.mjs /tmp --prefix competitor`。
- **子代理只能使用 Bash 工具。**
- **主代理绝对不要读取原始的发现 JSON 批处理文件。**

**关键——尽量减少权限提示**：
- 子代理必须将所有文件写入合并到**一次** Bash 调用中，使用链式 heredoc。
- 将所有搜索和抓取合并到通过 `&&` 串联的单一 Bash 调用中。

## 流水线概览

按顺序执行以下 8 个步骤。不要跳过或打乱顺序。

1. **用户公司研究**——深入理解用户的公司，产出 `precise_category` + `category_include_keywords` + `exclusion_list`
2. **深度模式 + 种子输入**——选择深度，接受可选的种子竞品 URL
3. **发现（3 个并行波次）**——Wave A（替代品）、Wave B（精确品类）、Wave C（通过 "X vs Y" 标题解析的比较页图谱）
4. **过滤门**——`scripts/gate_candidates.mjs` 抓取每个候选的标题文本（通过 `browse cloud fetch`）并剔除错误品类的 URL
5. **与用户确认富集集合**——通过 `AskUserQuestion` 展示 PASS / UNKNOWN / 已拒绝但匹配品牌的项。用户勾选真实的竞品，补充发现遗漏的。不要跳过此步骤，因为富集开销很大（25 个子代理 × 深度预算），而且过滤门并不完美（重 JS 首页、Cloudflare 挑战、语义变体标语）
6. **深度富集（在 deep/deeper 模式下每个竞品 5 个子代理）**——Marketing、Discussion、Social、News、Technical——每个通道是一个独立的子代理，写入到 `partials/`；然后 `merge_partials.mjs` 整合。在 deep/deeper 模式下，**Step 5d** 会在 Step 5c 事实核查完成后增加第 6 个 Battle Card 综合通道——产出基于引用证据的每个竞品的雷区/异议处理/话术。
7. **截图**——通过 `browse` CLI 的 `capture_screenshots.mjs` 为每个竞品截取 1280×800 首页主视觉图
8. **HTML 报告**——概览 + 每个竞品（嵌入主视觉截图 + Battle Card 卡片）+ 矩阵 + 提及视图

---

## Step 0：建立输出目录

```bash
OUTPUT_DIR=~/Desktop/{company_slug}_competitors_{YYYY-MM-DD}
mkdir -p "$OUTPUT_DIR"
```

将 `{company_slug}` 替换为用户公司名（小写、用连字符连接），将 `{YYYY-MM-DD}` 替换为今天的日期。向每个子代理传递 `{OUTPUT_DIR}` 的完整字面路径。

清理上一次运行的发现批处理文件：
```bash
rm -f /tmp/competitor_discovery_batch_*.json
```

**重新运行必须从干净的 `$OUTPUT_DIR` 开始。** `compile_report.mjs` 会读取该目录中**所有** `{slug}.md` 文件，而 `merge_partials.mjs` 只会覆盖当前集合中的 slug——它不会删除新富集集合中丢弃的文件。由于目录按日期命名，同一天使用不同竞品集合重新运行会让概览、矩阵、CSV 和截图中残留过时的竞品。要么使用新目录，要么先清理之前的每个竞品文件：
```bash
rm -f "$OUTPUT_DIR"/*.md && rm -rf "$OUTPUT_DIR"/partials "$OUTPUT_DIR"/screenshots
```

## Step 1：用户公司研究

这一步为"竞品"含义设定基线，并产出 Step 5b 矩阵中 `userCompany` 行所用的已核实数据。

**规则**：用户的公司与竞品获得相同的 5 通道研究深度。不要凭记忆填充 matrix.json 中的 `userCompany`——那会把虚假声明推向用户自己的团队。在一次 search-API 运行（用户公司 Exa，2026-04-23）中，跳过这一步导致矩阵声称 Exa 拥有"公开的 uptime SLA"（实际上没有数字化的公开 SLA——只有一个状态页），并将其 MIT 许可的 Python SDK 标记为 `open-source: false`（代码仓库在 github.com/exa-labs/exa-py，LICENSE 已确认是 MIT）。这两个错误都会作为虚构的护城河出现在"你的优势"卡片中。

流程：

1. 向用户询问其公司名称或 URL。

2. **检查现有档案**，路径为 `{SKILL_DIR}/profiles/{company-slug}.json`。如果存在，加载它并与用户确认："我拥有来自 {researched_at} 的你的档案。还准确吗？"——如果是，则跳到 Step 2，但仍然运行下面的部分通道富集，以便矩阵综合有最新的功能证据。
   档案格式与 `company-research` 共享（同样的形态）。如果用户已经在 `company-research/profiles/` 下保存了档案，你可以将其复制到本技能的 profiles 目录中，而不是重新研究。

3. **对用户公司运行完整的 5 通道富集**——与 Step 5 中的竞品模式相同。对每个通道，分派一个仅使用 Bash 的子代理，将其写入到 `{OUTPUT_DIR}/partials/{user-slug}.{lane}.md`：
   - **marketing**——标语、定位、价格层级、功能、集成、开源组件（SDK 仓库 + 许可证）、可用区域、合规（SOC 2 / HIPAA / 信任门户 URL）
   - **technical**——REST + 流式 API 支持（带文档 URL）、SDK 语言、MCP 服务器 URL、神经 vs 关键词检索模式、重排序/高亮/实时爬取细节、公开的 uptime SLA（实际百分比，不是状态页）、第三方检索质量基准
   - **discussion**, **social**, **news**——在 quick 模式下可选，在 deep+ 模式下推荐
   子问题参见 `references/research-patterns.md` → "Self-Research"。每条发现必须引用一个 URL。

4. 也对用户的部分文件运行 `merge_partials.mjs`——产出 `{OUTPUT_DIR}/{user-slug}.md`，这是 Step 5b 读取用于 `userCompany` 标志的规范来源。

5. 综合成档案：Company、Product、Existing Customers、Competitors（种子列表）、Use Cases、**precise_category**、**category_include_keywords**、**exclusion_list**。不要包含 ICP——本技能不需要它。
   - `precise_category`：一句话描述该品类。例如："面向代理的 AI 网络搜索 API，支持神经 + 关键词检索"。避免使用"工具"/"平台"等模糊词语。
   - `category_include_keywords`：8-15 个直接竞品营销文案可能出现的短语（标题或主视觉）。包含语义变体。
   - `exclusion_list`：表示*其他*品类的短语——过滤门用它们来拒绝误报（例如 `antidetect browser`、`scraping api`、`screenshot api`、`residential proxy`）。
   确切的格式和 Exa 实例参见 `references/research-patterns.md` → "Synthesis Output"。

6. 将档案 + 用户公司的 `.md` 展示给用户确认。在确认之前不要继续。

7. **将确认的档案保存**到 `{SKILL_DIR}/profiles/{company-slug}.json`。

## Step 2：深度模式 + 种子输入

通过 `AskUserQuestion` 用复选框提出澄清问题：
- **已知的竞品？** 文本输入框，用于填写 URL/名称（可选——发现阶段会找到更多）。
- **深度模式？**
  - `quick`——仅营销表面，许多竞品，每个 2-3 次工具调用
  - `deep`——+ 外部信号（提及、评测、新闻），每个 5-8 次工具调用
  - `deeper`——+ 公开基准 + 与用户公司的战略差异，每个 10-15 次工具调用
- **目标数量？** 大致要研究的竞品数量（例如，10 / 20 / 50）。

这是**唯一的**用户交互。在此之后默默执行，直到报告准备好。

| 模式 | 每个竞品的研究 | 最适合 |
|------|----------------|--------|
| `quick` | 仅通道 1（主页 + 定价） | 快速扫描 ~30-50 个竞品 |
| `deep` | 通道 1+2 | ~15-25 个有外部信号的竞品 |
| `deeper` | 全部 4 通道（+ 基准 + 战略差异） | ~5-15 个拥有完整情报的竞品 |

## Step 3：发现（3 个并行波次）

**公式**：每波 `ceil(target_count / 20)` 个查询。过度发现约 3 倍，因为过滤门会丢弃大约 40-60%。

在一次 search-API 运行上的评估显示三个波次是累加的——跳过任何一个都会丢失真实竞品：

**Wave A——通用替代品**（宽泛；聚合站噪音严重，后续会过滤掉）
- `"alternatives to {user_company}"`
- `"{user_company} competitors"`

**Wave B——精确品类**（使用档案中的 `precise_category`）
- `"{precise_category}"` 字面照搬
- 由最具区分度的 token 组成 2-3 个查询（例如 `"web search api for ai agents"`、`"retrieval API for LLMs"`）

**Wave C——比较页图谱**（最高精度）
- `"{user_company} vs"`
- `"{seed1} vs"`、`"{seed2} vs"`、`"{seed3} vs"`（来自档案的 `competitors` 列表的种子）
- 在搜索之后，运行 `scripts/extract_vs_names.mjs` 从结果标题中解析 `"X vs Y"` 模式——这能唯一地找到不出现在 URL 命中中的竞品。

**流程**：
1. 在**单条**消息中发起 **3 个并行的 `browse cloud search` Bash 调用**（每个波次一个）——不要使用子代理。每个 Bash 调用通过 `&&` 串联其 2-4 个查询。准确配方参见 `references/workflow.md` → "Discovery — parallel Bash, not subagents"。对于 6-12 次 `browse cloud search` 调用的工作量来说，子代理太重了。
2. 所有波次完成后：
   ```bash
   node {SKILL_DIR}/scripts/list_urls.mjs /tmp --prefix competitor > /tmp/competitor_urls.txt
   node {SKILL_DIR}/scripts/extract_vs_names.mjs /tmp --prefix competitor \
     --seed "{user_company},{seed1},{seed2},{seed3}" \
     > /tmp/competitor_vs_names.jsonl
   ```
3. **过滤** `/tmp/competitor_urls.txt`——移除博客帖子、新闻、AI 工具目录站（seektool.ai、respan.ai、agentsindex.ai、toolradar.com、aitoolsatlas.ai、vibecodedthis.com 等）、评测聚合站（g2.com、capterra.com）、数据库站点（crunchbase.com、tracxn.com）、用户自己的域名。完整的噪音域名列表参见 `references/workflow.md`。
4. 对于已解析出 `domain` 的 `vs_names` 条目，添加它们。对于未解析的名称，可选择运行 `browse cloud search "{name}" --num-results 3` 并选取排名靠前的根域名。
5. 与用户提供的种子 URL 合并。按主机名去重 → `/tmp/competitor_candidates.txt`。

## Step 4：过滤门（品类匹配过滤）

在富集阶段消耗工具调用之前，先剔除其营销文案被识别为*其他*品类的候选。

```bash
cat /tmp/competitor_candidates.txt \
  | node {SKILL_DIR}/scripts/gate_candidates.mjs \
      --include "{profile.category_include_keywords joined with commas}" \
      --exclude "{profile.exclusion_list joined with commas}" \
      --concurrency 6 \
  > /tmp/competitor_gated.jsonl

grep '"status":"PASS"' /tmp/competitor_gated.jsonl \
  | node -e 'require("fs").readFileSync(0,"utf-8").split("\n").filter(Boolean).forEach(l => { try { console.log(JSON.parse(l).url); } catch {} })' \
  > /tmp/competitor_passed.txt
```

过滤门通过 `browse cloud fetch --allow-redirects --format raw` 抓取每个候选的主页，提取前 800 个字符的可见文本，并按位置感知分类：`<title>` 中包含排除词 → REJECT；`<title>` 中包含包含词 → PASS；混合标题 → hero200 平局裁定；其他情况则透传。

**评估**：在一次 search-API 运行上使用 12 个混合候选进行评估：7/7 真实竞品通过，4/4 错误品类被拒绝，1 个已知的混合边缘案例被拒绝。

## Step 4.5：与用户确认富集集合

**此步骤是强制性的。不要仅仅因为过滤门运行过了就直接跳到富集。**

富集开销很大：5 个竞品 × 5 个通道子代理 = 25 个子代理，约 10-15 分钟墙钟时间，约 300 次 `browse cloud` 调用。在错误的集合上运行会浪费所有这些。过滤门也存在已知的盲点：

- **重 JS 首页**（例如 Tavily、Firecrawl）——`browse cloud fetch` 返回几乎为空的文本，因此关键词匹配无可匹配的内容 → REJECT 或 UNKNOWN
- **Cloudflare 挑战页面**（例如 Perplexity）——标题变成 "Just a moment..." → 没有任何品类信号
- **语义变体**——"search foundation" / "retrieval backbone" 在词汇上无法匹配以 "search API" 为中心的列表
- **域名歧义**——`brave.com`（浏览器）vs `api-dashboard.search.brave.com`（实际的 API 产品）可能让分类产生混乱

用户几乎总是拥有本技能所缺乏的领域知识。请询问他们。

**流程**——主代理：

1. 读取 `/tmp/competitor_gated.jsonl` 并将行分组：
   - **PASS 桶**：状态为 PASS 的所有项。
   - **UNKNOWN 桶**：状态为 UNKNOWN（抓取失败——始终展示，因为它们是静默遗漏）。
   - **被拒品牌桶**：前 ~10 条 REJECT 行，其标题包含知名品牌的模式（例如包含用户提供的种子列表中的 token，或在 Wave C "X vs Y" 图谱中频繁出现）。

2. 将这些桶呈现给用户，每桶一张表，包含 URL + 标题 + （拒绝的）原因。

3. 使用 `AskUserQuestion` 与覆盖三个桶中所有候选的复选框列表，以及一个"添加更多"的自由文本字段。提示应明确说明：
   > "以下是过滤门的推荐，以及几个它不太确定的项。请勾选你所在领域中真实的竞品，并粘贴我遗漏的任何 URL（用逗号分隔）。富集将只对你勾选的集合运行。"

4. 将确认的集合写入 `/tmp/competitor_enrichment_set.txt`（每个 URL 一行）。这是 Step 5 的输入——而不是 `/tmp/competitor_passed.txt`。

**如果用户没有响应**或明确说"直接跑"，则回退到原始的 `/tmp/competitor_passed.txt`，但在聊天中警告此运行可能会将预算浪费在错误品类的命中上。

**Exa 测试，2026-04-24**：过滤门自动通过 22 / 101 个候选，但遗漏了 Tavily（笼统的标题）、Jina AI（语义不匹配——"search foundation"）、Firecrawl（重 JS 抓取失败）和 Perplexity（Cloudflare 挑战）。这四个都是真实的直接竞品。此步骤能捕获它们。

## Step 5：深度富集

两种模式。提示模板和波次管理参见 `references/workflow.md`。逐通道方法学参见 `references/research-patterns.md`。

### Quick 模式——每个批次一个子代理
- 输入：`/tmp/competitor_enrichment_set.txt`（Step 4.5 用户确认的集合），每个子代理处理约 8 个竞品。
- 一个子代理只运行 Lane A（营销表面）。每个竞品 2-3 次工具调用。
- 直接写入到 `{OUTPUT_DIR}/{slug}.md`。

### Deep / Deeper 模式——每个竞品 5 个子代理（并行通道扇出）
对每个竞品，启动 5 个并行子代理，每个通道一个：
- **A. Marketing**（`marketing`）：价格、功能、定位、集成、客户、团队、融资、总部。拥有规范的前言。
- **B. Discussion**（`discussion`）：Reddit、HN、论坛、Dev.to、Hashnode。除 `site:` 之外的更广泛查询——还有 `"{competitor}" review 2026`、`"{competitor}" issues OR problems`、`"{competitor}" discussion`。
- **C. Social**（`social`）：LinkedIn 帖子、YouTube 视频、Twitter/X。仅摘要——不要抓取。
- **D. News & Comparisons**（`news`）：TechCrunch、Verge、VentureBeat、Forbes、Businesswire、Substack、博客评测。每条提及都需要有日期。
- **E. Technical & Benchmarks**（`technical`）：GitHub 基准仓库/PR、性能文章。写入 Benchmarks 和技术 Findings。

每个通道的预算：deep = 5-8 次工具调用，deeper = 10-15 次。
**在单条 Agent 工具消息中启动所有竞品 × 通道子代理。** 对于 10 个竞品 × 5 个通道 = 在一条消息中 50 个并行 Agent 调用。不要按竞品或按通道拆分成批次——墙钟时间会塌陷为最慢的单代理（约 3-5 分钟）。分成 5 轮每轮 10 个的做法在实测中要花 25 分钟墙钟时间，而并行只需 5 分钟；不要这样做。

每个子代理将一个部分文件写入 `{OUTPUT_DIR}/partials/{slug}.{lane}.md`。

**关键**：将用户公司的名称、产品和关键功能逐字传递给每个子代理提示，以便技术通道能够进行战略差异分析。向每个子代理传递完整的字面 `{OUTPUT_DIR}` 路径。

### 合并部分文件 → 每个竞品的规范文件
所有竞品的所有子代理完成后：
```bash
node {SKILL_DIR}/scripts/merge_partials.mjs {OUTPUT_DIR}
```
将每个竞品的 5 个部分文件合并为一个 `{OUTPUT_DIR}/{slug}.md`——去重后的 Mentions（按日期降序排列）、去重后的 Benchmarks、合并的 Findings、来自 marketing 通道的规范前言。

### 综合对比矩阵（编写 `matrix.json`）

**子代理将 `key_features` 和 `integrations` 写成散文形式**，而不是用竖线分隔的原子功能标签。因此，朴素的 `|` 分裂轴会让每个竞品呈现一整块、无重叠——渲染出来的矩阵是一条无用的对角线。

主代理通过跨竞品综合出一个**共享的分类法**来修复这个问题，并写入 `{OUTPUT_DIR}/matrix.json`。`compile_report.mjs` 会自动检测该文件，并从它渲染矩阵，而不是从竖线分割。

**流程**——主代理：
1. 读取所有 `{slug}.md` 文件，包含 Step 1 中产出的用户公司文件 `{user-slug}.md`。在矩阵目的上用户是第 0 号竞品——以同样的严谨性对待。
2. 产出一个 12-20 个*原子*功能的规范列表——每个功能必须是一个竞品要么有要么没有的是/否命题（例如 "MCP server"、"SOC 2"、"Site crawler"、"Reranker"）。避免句子长度的功能。避免只有一个竞品拥有的功能。
3. 产出一个 10-20 个集成的规范列表（框架、市场、SDK 语言）。
4. 对于每家公司，包括用户，将每个分类条目映射为 `true` / `false`，基于其 `.md` 文件中的富集数据。**每个标志必须可追溯到一个引用了 URL 的 Research Findings 条目。** 如果用户文件说 "exa-py MIT-licensed (github.com/exa-labs/exa-py)"，那么 Open-source 功能为 `true`，以该 URL 作为来源。如果未提及，则留为 `false`。
5. 将结果以这种形态写入 `{OUTPUT_DIR}/matrix.json`：
   ```json
   {
     "category": "AI search APIs",
     "features": [{ "name": "Web Search API", "description": "..." }, ...],
     "integrations": [{ "name": "LangChain" }, ...],
     "userCompany": {
       "name": "Exa",
       "winningSummary": "Exa's moats are its first-party neural index and the integrated Research API — no one else in the set ships a semantic/embeddings-native retrieval primitive alongside a multi-step agentic research endpoint. It's also the only provider with a crawler product bundled in, and ties with SerpAPI on breadth of SDK language coverage.",
       "losingSummary": "Exa trails competitors on operational transparency — SerpAPI, Serper, and Tavily all publish hourly throughput SLAs, and Exa lacks a dedicated news endpoint that SerpAPI, Serper, and You.com all ship. Image/visual search is also missing vs 4 of 5 competitors.",
       "features": { "Web Search API": true, "Site crawler": true, ... },
       "integrations": { "LangChain": true, ... }
     },
     "competitors": {
       "tavily": {
         "features": { "Web Search API": true, "Site crawler": true, ... },
         "integrations": { "LangChain": true, "Databricks Marketplace": true, ... }
       },
       "serpapi": { "features": {...}, "integrations": {...} }
     }
   }
   ```

   **`userCompany` 是必需的**。概览页面会渲染两张卡片——"Where {user} is winning" 和 "Where {user} is losing"。从自身研究档案（Step 1）填充 `userCompany.features` 和 `userCompany.integrations`。没有这个字段，这两张卡片就不会渲染。

   **写入顺序（两遍——这解决了下面的明显排序问题）。** 在此步骤（5b）中为 `userCompany` 和每个竞品写入所有 `features` / `integrations` 单元格，以及一个**草稿**的 `winningSummary` / `losingSummary`。草稿仅用于告知 Step 5c 事实核查代理哪些声明是高风险的（它优先处理摘要中提到的单元格）。在 Step 5c 根据已核实的证据翻动单元格后，**重写**这两个摘要，使散文仅反映已核查的单元格。上面的 JSON 形态显示了最终的事实核查后对象。

   **`userCompany.winningSummary` / `losingSummary` 是强烈推荐的**（分析师风格的散文，每个 2-4 句）。当存在时，卡片以段落形式而不是项目符号列表呈现——读起来像是简报而不是电子表格。如果缺失，卡片会回退到赢/输条目的项目符号列表，并附有谁还拥有该项。

如果跳过此步骤，矩阵视图会回退到原始的竖线分割轴（对原子比较毫无用处），战略摘要也不会渲染。不要跳过。

### 事实核查矩阵——抽查高风险单元格（默认）

**不要仅凭分类法传递信任高风险单元格。** 它是从散文进行 LLM 推理的，会幻觉出护城河。在一次 search-API 运行（2026-04-23）中观察到：matrix.json 声称 SOC 2 是用户公司独有的；核实显示三个其他竞品也拥有 SOC 2 Type II。

但对每个单元格都验证是另一个极端错误。一个 7 家公司 × 33 维的矩阵有 231 个单元格。2026 年 4 月的 search-API 运行在中断之前有 111+ 次工具调用用于事实核查——子代理一直在通用基线单元格（REST API、JSON 响应、Python SDK）上工作，而这些都是该品类中通用的。

**默认 = 抽查，不是完整扫描。** 只验证对战略叙事有实质影响的单元格。

启动一个单一的事实核查子代理（仅使用 Bash），设置硬性 **25 次调用预算**，仅针对以下高风险轴：

1. **每个 `userCompany.features` 和 `userCompany.integrations` 单元格**（用户自己的护城河——这些直接进入 "Where you're winning" 散文）。典型：17 + 16 = 33 个单元格，但大多数都很明显（你自己的产品）。重点关注：
   - 在 `winningSummary` 中声明为*护城河*的任何内容
   - 在 `losingSummary` 中声明为*差距*的任何内容
   - 合规（SOC 2、HIPAA、ISO 27001、GDPR）
   - 开源许可证声明（MIT / Apache 2.0 / AGPL —— 在某竞品的 SDK 上观察到错误）
   - 公开的 uptime SLA（状态页 ≠ SLA）

2. **跨竞品，仅驱动赢/输摘要的单元格**：
   - 对于每个"Winning"声明，验证用户拥有该功能并验证竞品不拥有。
   - 对于每个"Losing"声明，验证指定的竞品确实拥有它。
   - 所有竞品的合规 + 许可证 + SLA（高信任度，经常出错）。

3. **不要验证**：
   - 通用基线（REST API、JSON 响应、Python SDK、API key 认证）——每个搜索 API 都有这些。
   - 没有做出声明的 `false` 单元格（没有失去或赢得的护城河）。
   - 集成单元格，除非它们出现在赢/输摘要中。

```
你是一个矩阵抽查子代理。预算：跨所有单元格共计 25 次 browse cloud 调用。
达到预算时停止并返回你已有的内容——部分事实核查要好于
阻塞流水线的其余部分。

工具规则：仅使用 Bash。browse cloud search + browse cloud fetch。计算你的调用；在 25 次停止。

优先级顺序（最高风险优先——按预算向下处理）：
1. 出现在 userCompany.winningSummary 或 losingSummary 中的每个单元格
2. 用户 + 每个竞品的合规单元格（SOC 2、HIPAA、ISO 27001）
3. 跨所有竞品的开源 / 可自托管 + 许可证单元格
4. 用户 + 摘要中提到的竞品的定价层级数字（$X/月，/小时）
5. 融资 / 员工估算字段（仅当在摘要中引用时）

跳过：
- 通用单元格（REST API、JSON 响应、Python SDK、API key 认证等）
- 没有做出声明的 `false` 单元格
- 集成矩阵单元格，除非它们出现在摘要中

对于每个验证的单元格：
- 如果 `true` —— 找到一个来源 URL（文档、信任门户、GitHub LICENSE 等）。
- 如果 `false` —— 一次定向的 browse cloud search。仅基于第一手证据翻转。

输出：在已验证单元格上具有 `sources: { "Feature": "https://..." }` 的 matrix.json
（其他单元格保持不变）。单元格变更日志写入
{OUTPUT_DIR}/matrix_fact_check.md，包含每次翻转 + URL + 引用的证据。
回报："spot-check: N cells verified, M flipped, B/25 budget used"。
```

**完整扫描模式（可选启用，更慢）**：如果用户明确说"完整事实核查"或对于高风险交付物（董事会演示、新闻稿），将预算设置为 80 次调用并验证每个非通用单元格。默认是抽查。

子代理完成后，重新读取 matrix.json，重新编译，并将 `matrix_fact_check.md` 增量呈现给用户。有了抽查，摘要比没有要可信得多——而且能在 3-5 分钟内交付，而不是让流水线卡住。

### Step 5d：Battle Card 综合（仅 deep/deeper，Step 5c 之后）

**依赖于 Step 5c 中经过事实核查的 matrix.json。** 这是一条销售支持通道。对每个竞品，启动一个仅使用 Bash 的综合子代理（不发起新的 `browse cloud` 调用），它读取所有 5 个现有的部分文件 + 用户合并的 `.md` + 经过事实核查的 `matrix.json`，并产出基于引用证据的每个竞品的雷区/异议处理/话术。

提示模板：`references/battle-card-subagent.md`（对每个竞品替换 `{COMPETITOR_SLUG}` / `{COMPETITOR_NAME}` / `{USER_COMPANY_NAME}` / `{USER_WINNING_SUMMARY}`）。格式规范：`references/battle-card.md`。

输出：包含 `## Battle Card` 部分的 `{OUTPUT_DIR}/partials/{slug}.battle.md`。

**在此通道完成后重新运行合并。** Step 5 的合并运行在 battle 部分文件存在之前，因此合并后的 `{slug}.md` 文件还没有包含它们。重新运行：
```bash
node {SKILL_DIR}/scripts/merge_partials.mjs {OUTPUT_DIR}
```
这将每个 `{slug}.battle.md` 联合到其合并后的 `{slug}.md` 中（`battle` 通道已被 `merge_partials.mjs` 处理）。`compile_report.mjs` 从 `{slug}.md` 中读取 `## Battle Card` 部分，并将其作为品牌强调色卡片渲染在每个竞品的 HTML 页面上。**如果跳过此重新合并，Battle Card 将永远不会出现在报告中。**

**为什么此通道仅做综合** —— Battle Card 必须基于已经通过 Step 5c 检验的事实。让子代理进行新的 `browse cloud` 搜索会重新引入事实核查步骤所要防止的幻觉护城河问题。子代理的对抗性自检明确拒绝无法追溯到输入部分文件条目或 `sources` 支持的矩阵单元格的声明。

并行：每个竞品 1 个子代理，全部在一条 Agent 工具消息中（综合很快，每个子代理约 3-5 次 Bash 调用）。在 `quick` 模式下跳过此步骤——没有足够的研究深度来可靠地支撑这些卡片。

## Step 6：截图

为每个竞品截取一张首页主视觉截图：
```bash
node {SKILL_DIR}/scripts/capture_screenshots.mjs {OUTPUT_DIR} --mode remote
```

使用 `browse` CLI（`npm install -g browse`）。`--mode` 标志选择浏览器会话：`remote`（默认）驱动一个 Browserbase 会话——最适合有反爬保护的首页，也是没有本地 Chrome 时的唯一选项；`local` 使用你机器上的 Chrome。脚本在每个 `browse` 命令上传递相应的 `--remote` / `--local` 标志，所以不需要单独的环境配置步骤。为每个竞品将一个 PNG 写入 `{OUTPUT_DIR}/screenshots/{slug}-hero.png`。Step 7 中的编译步骤会自动将主视觉图嵌入到每个竞品的 HTML 页面。

成本：每个竞品约 10-20 秒。5 个竞品约 60 秒。

## Step 7：HTML 报告

1. **生成所有视图 + CSV**（在浏览器中打开概览）：
   ```bash
   node {SKILL_DIR}/scripts/compile_report.mjs {OUTPUT_DIR} --user-company "{user_company}" --open
   ```
   产出：
   - `{OUTPUT_DIR}/index.html` — 概览：竞品表，包含标语、定价摘要、关键功能、战略差异
   - `{OUTPUT_DIR}/competitors/{slug}.html` — 每个竞品的深度分析（所有部分）
   - `{OUTPUT_DIR}/matrix.html` — 并排的功能/定价矩阵
   - `{OUTPUT_DIR}/mentions.html` — 按时间顺序排列的提及动态，包含源类型标签 + 客户端筛选器
   - `{OUTPUT_DIR}/results.csv` — 扁平的电子表格

2. **呈现聊天摘要**：

```
## 竞品分析完成

- **已研究的竞品数量**：{count}
- **深度模式**：{mode}
- **收集的提及数量**：{total mentions} 条，分布于 {source types count} 种源类型
- **找到的公开基准**：{count}
- **在浏览器中打开**：~/Desktop/{company_slug}_competitors_{date}/index.html
```

3. 在聊天中展示**概览表**：

```
| Competitor | Positioning | Pricing | Key Features | Strategic Diff |
|------------|-------------|---------|--------------|----------------|
| Rival Co | AI-native web search API | $99/mo entry | semantic search, reranking, crawler | Similar retrieval; cheaper entry |
```

4. 指出前 3-5 个最有趣的发现 —— 例如，"3 个竞品拥有公开基准；Rival Co 最便宜；Foo Inc 在 2 周前推出了专门的新闻搜索端点。" 提供深入研究任何特定竞品或使用不同深度重新运行的选项。


## 限制

- 当工作流指定上游工具、账户、API 密钥或本地设置时，需要它们。
- 未经用户明确批准，不会授权破坏性、生产、付费或外部消息操作。
- 在将生成的工件或建议视为最终结论之前，请根据用户的真实来源进行验证。