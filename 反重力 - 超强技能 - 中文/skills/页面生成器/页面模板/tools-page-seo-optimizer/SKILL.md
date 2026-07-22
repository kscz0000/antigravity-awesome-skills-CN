---
name: tools-page-seo-optimizer
description: "面向任何拥有多个工具、产品或功能页面的站点的、与框架无关的 SEO 工作流。涵盖重复内容、独一无二的 meta 标签、标题层级、内链、URL slug、E-E-A-T、用于扩展 50–500 个页面的内容注册表模式，以及针对排名 50–68 关键词的博客内容策略。"
category: seo
risk: safe
source: community
source_type: community
author: whoisabhishekadhikari
date_added: "2026-06-19"
tags: [seo, tools-pages, product-pages, duplicate-content, content-registry, meta-tags, internal-linking, url-slugs, e-e-a-t, framework-agnostic]
tools: [claude-code, cursor, codex-cli, gemini-cli, opencode]
version: 1.0.0
---

# 工具页 SEO 优化器

你是面向拥有大量工具、产品或功能页面的站点的技术 SEO 与内容策略专家。你的工作流与框架无关——适用于 Django、Rails、Laravel、Express、Next.js、Nuxt、Astro、WordPress 以及静态 HTML。

源自一次真实审计：发现 105 个工具页面中有 93 个共享完全相同的模板文案，平均排名在第 68 位。本技能就是修复这一问题的操作手册。

---

## 快速启动决策树

```
Full audit from scratch?              → Run all phases in order
All tool pages rank the same?         → Phase 2 (Content Registry) first
Meta titles/descriptions all generic? → Phase 1 (Meta Tags)
Tool pages buried / hard to navigate? → Phase 5 (Internal Linking)
Bad URL slugs?                        → Phase 6 (URL Slug Hygiene)
Site looks authorless to Google?      → Phase 7 (E-E-A-T)
Stuck at position 50–68 on keywords?  → Phase 9 (Blog Content Strategy)
Fixes deployed but unsure they're live? → Phase 10 (Live Verification)
```

---

## Phase 0 — 代码库侦察

**在动手写任何代码之前**，先在代码库中定位以下内容。名称因框架而异——请自行适配。

| 要找的内容 | 常见位置 |
|---|---|
| URL 路由 | `routes.rb`、`urls.py`、`routes/`、`pages/`、`app/` |
| Head / meta 模板 | `_head.html`、`layout.js`、`base.html`、`app.blade.php` |
| 工具/页面注册表 | 配置文件、数据库种子、JSON、`lib/guides.js`、`data/tools.js` |

**在动手写一行代码之前先回答这些问题：**

1. 工具页面是如何生成的——静态文件、数据库循环、配置注册表，还是 CMS？
2. 渲染 `<title>`、`<meta name="description">`、`<h1>` 的共享模板在哪里？
3. 每个工具是否有自己的内容字段，还是所有工具都回退到同一份模板文案？
4. 是否存在一个中心化的工具 slug 列表，可以以编程方式遍历？

---

## Phase 1 — Meta 标题与描述

### 核心问题

所有工具页面共享同一份 `<title>` 模板、只替换工具名，
是工具站点排名不佳的最常见原因。Google 会把几乎相同的标题
视为重复页面，并压低它们整体的排名。

### 标题标签公式

```
{Tool Name} | {Specific Outcome} — {Brand}
```

| ✅ 好 | ❌ 差 |
|---|---|
| `Meta Tag Generator \| Create Perfect SEO Titles Free — MySite` | `Meta Tag Generator - MySite Tools` |
| `Broken Link Finder \| Scan Any Page for Dead URLs — MySite` | `Broken Link Finder - Free Online Tool \| MySite` |

**规则：**
- 总长度 ≤ 60 个字符
- 主关键词出现在前 40 个字符以内
- 每个工具的标题都**独一无二**——不允许两个工具共用同一个标题
- 在准确的前提下包含“Free”——可显著提升 CTR

### Meta 描述公式

```
{What it does — one action sentence}. {Key differentiator}. {CTA}.
```

示例：`Scan any webpage for broken links in seconds. Checks internal and external URLs,
exports results as CSV. Free, no account needed.`

**规则：**
- 120–160 个字符
- 行动动词：Generate、Scan、Check、Analyze、Convert、Build、Find
- 每个工具都拥有**专属**描述——零模板填充

### 实现方式（任意框架）

```html
<!-- Generic template pattern -->
<title>{{ tool.meta_title | default(tool.name + " | " + site_name) }}</title>
<meta name="description" content="{{ tool.meta_description | default(tool.tagline) }}">
```

### 校验脚本——每次部署前运行

```python
# validate_meta.py
import json, sys

tools = json.load(open('data/tools.json'))
errors = []

for t in tools:
    slug  = t.get('slug', '?')
    title = t.get('meta_title', '')
    desc  = t.get('meta_description', '')
    if not title:          errors.append(f"MISSING TITLE: {slug}")
    elif len(title) > 60:  errors.append(f"TITLE TOO LONG ({len(title)}): {slug}")
    if not desc:           errors.append(f"MISSING DESC: {slug}")
    elif len(desc) < 120:  errors.append(f"DESC TOO SHORT ({len(desc)}): {slug}")
    elif len(desc) > 160:  errors.append(f"DESC TOO LONG ({len(desc)}): {slug}")

if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f"✅ All {len(tools)} tools passed meta validation")
```

---

## Phase 2 — 内容注册表（杠杆率最高的修复）

**工具站点排名差的根本原因：** 80–95% 的工具页面共享相同的模板文案。
Google 将其视为单薄、几乎重复的页面，任何一个都排不好。
在做任何其他事情之前，先修复这一点。

### 问题诊断

```bash
# Find shared prose in your templates — if these strings appear in a shared template
# file, you have the problem
D1=$(grep -rn "powerful tool that helps" templates/ src/ 2>/dev/null | head -5)
[ -n "$D1" ] && echo "  ✗ Shared template prose found" || echo "  ✓ No shared prose"
D2=$(grep -rn "easy to use" templates/ src/ 2>/dev/null | head -5)
[ -n "$D2" ] && echo "  ✗ Template filler found"
```

### 注册表条目结构（与框架无关）

```yaml
# data/tools/meta-tag-generator.yaml  (or JSON, DB columns, JS object — adapt to your stack)
slug: meta-tag-generator
name: Meta Tag Generator
meta_title: "Meta Tag Generator | Create Perfect SEO Titles & Descriptions Free"
meta_description: "Generate optimized title tags and meta descriptions with live character
  counters. Enforces Google's 60/160 char limits. Instant, free, no account needed."

introduction: >
  The meta tag generator creates the two most critical on-page SEO elements —
  your title tag and meta description — with live character counters that enforce
  Google's recommended limits before you publish. [80+ unique words minimum]

best_practices:
  - "Include your primary keyword within the first 40 characters of the title"
  - "Write a unique description per page — duplicate descriptions waste crawl budget"
  - "Use action verbs in descriptions: Generate, Find, Check, Analyze"

how_to_steps:
  - name: "Enter your page details"
    text: "Type your target keyword, page topic, and a brief summary of the content"
  - name: "Check the live character counters"
    text: "Keep title ≤60 chars and description ≤160 chars"
  - name: "Copy and paste the output"
    text: "Paste the generated tags into your HTML <head> section"

faqs:
  - q: "Does Google always use my meta description?"
    a: "No — Google rewrites descriptions ~63% of the time. Write them anyway for
       social shares and some SERPs."
  - q: "What happens if my title is over 60 characters?"
    a: "Google truncates it with an ellipsis, cutting off your message mid-sentence."

related_tools:
  - og-tag-generator
  - schema-markup-generator
  - heading-analyzer
```

### 每个工具最低限度必需的独特内容

| 字段 | 最低要求 | 优先级 |
|---|---|---|
| `meta_title` | 独一无二，≤ 60 字符 | 🔴 关键 |
| `meta_description` | 独一无二，120–160 字符 | 🔴 关键 |
| `introduction` | 80+ 个独一无二的词 | 🔴 关键 |
| `best_practices` | 3–5 条工具专属项 | 🟡 高 |
| `how_to_steps` | 3 个针对**该工具**的真实步骤 | 🟡 高 |
| `faqs` | 2 条工具专属问答 | 🟡 高 |
| `related_tools` | 2–4 条 slug 引用 | 🟢 中 |

**规则：在开始下一个工具之前，先把当前这一个工具完整填好。**

---

## Phase 3 — H1 与标题层级

### H1 公式

```
{Tool Name} | {Outcome Phrase}
```

**规则：**
- 每页仅一个 `<h1>`——只放工具名/标题
- 每页 H1 必须独一无二

### 标题层级

```
h1 — Tool name (one per page)
  h2 — Major sections: "How It Works", "Best Practices", "FAQs", "Related Tools"
    h3 — Subsections: individual FAQ items, feature callouts, step headers
```

绝不跨级。不允许 h1 → h3 跳过 h2。

```bash
# Audit heading hierarchy on a live page
curl -s "https://yourdomain.com/tools/meta-tag-generator" \
  | grep -oE '<h[1-6][^>]*>.*?</h[1-6]>'
```

---

## Phase 4 — 可访问性

可访问性故障会拉低 Core Web Vitals 分数——而 Core Web Vitals 是直接排名信号。

每个仅含图标的交互元素都需要 `aria-label`：

```html
<button aria-label="Copy to clipboard"><svg>...</svg></button>
<button aria-label="Go to next page">›</button>
<input type="search" aria-label="Search tools" placeholder="Search...">
```

```bash
# Find icon-only buttons missing aria-label
B=$(grep -rn "<button" templates/ 2>/dev/null | grep -v "aria-label" | grep -v ">[A-Za-z]" | head -5)
[ -n "$B" ] && echo "  ⚠ Icon buttons missing aria-label:" && echo "$B" || echo "  ✓ Buttons have aria-labels"
```

---

## Phase 5 — 内链

工具之间的内链是 PageRank 在站点内流动的方式。一个没有任何入站内链的工具，
即便内容再好，对 Google 而言实际上等同于隐形。

### Hub-and-Spoke 模型

```
Homepage
  └── Category: Keyword Tools
        ├── Keyword Density Checker  ←→  Keyword Suggestion Tool
        └── SERP Preview Tool        ←→  Meta Tag Generator
  └── Category: Technical SEO
        ├── XML Sitemap Visualizer   ←→  Robots.txt Creator
        └── Robots.txt Creator       ←→  Redirect Generator
```

### 规则

- 每个工具**链向**至少 2 个相关工具（使用注册表里的 `related_tools`）
- 每个工具**被链**至少 2 次（来自其他工具或分类页）
- 不允许孤立工具——任何工具都应在 3 次点击内从首页抵达

```bash
# Orphan detection — tools with too few inbound references
for slug in $(cat data/slugs.txt 2>/dev/null); do
  C=$(grep -rl "$slug" templates/ 2>/dev/null | wc -l | tr -d ' ')
  [ "$C" -lt 2 ] && echo "  ORPHAN RISK: $slug ($C refs)"
done
```

### 模板实现

```html
{% if tool.related_tools %}
<section>
  <h2>Related Tools</h2>
  {% for slug in tool.related_tools %}
  {% set rel = get_tool(slug) %}
  <a href="/tools/{{ slug }}">{{ rel.name }} — {{ rel.tagline }}</a>
  {% endfor %}
</section>
{% endif %}
```

---

## Phase 6 — URL Slug 卫生

| ✅ 好 | ❌ 差 | 问题 |
|---|---|---|
| `/tools/meta-tag-generator` | `/tools/tool-1` | 无关键词 |
| `/tools/keyword-density-checker` | `/tools/free-online-keyword-density-checker-tool-free` | 关键词堆砌 |
| `/tools/broken-link-finder` | `/tools/brokenLinkFinder` | 驼峰命名 |

**公式：** `{primary-keyword-phrase}`——全小写、连字符、无停用词、无 “free” / “online” / “tool” 等填充词。

```bash
# Audit — list longest slugs (likely stuffed)
curl -s "https://yourdomain.com/sitemap.xml" \
  | grep -oE '<loc>[^<]+' | sed 's/<loc>//' \
  | grep "/tools/" \
  | awk -F'/tools/' '{print length($2), $2}' | sort -n | tail -20
```

如果重命名 slug，务必对旧 → 新做 301 重定向，并更新所有内链。

---

## Phase 7 — E-E-A-T 信号

工具站点如果看起来既无作者也无日期，排名就会很差。

### 作者署名 + 日期（每个工具页都需要）

```html
<p class="tool-byline">
  Built by <a href="/about">Your Name</a>
  <time datetime="{{ tool.updated_at }}"> · Updated {{ tool.updated_at | date }}</time>
</p>
```

### 信任要点区域

```html
<section class="trust-pillars">
  <div>✅ <strong>100% Free</strong> — no account, no credit card</div>
  <div>🔒 <strong>Privacy First</strong> — your data never leaves your browser</div>
  <div>⚡ <strong>Instant Results</strong> — processed in under 1 second</div>
</section>
```

### 关于 / 作者页

创建 `/about` 页面，包含：真实姓名、资历、为什么构建这些工具、联系方式。
在每个工具页的署名处链接到该页。对于个人构建的工具站点，
这是影响最大的 E-E-A-T 修复。

---

## Phase 8 — 扩展到 100+ 工具

当内容注册表模式在 10–20 个工具上跑通后，下一个挑战是
在不损失质量、不引入重复的前提下扩展到 100+。

### 批量完成闸门

永远不要提交不完整的批次。每次涉及工具内容的提交之前：

```bash
# Count tools with introduction content vs total tools
python3 -c "
import json
tools = json.load(open('data/tools.json'))
total   = len(tools)
done    = sum(1 for t in tools if t.get('introduction','').strip())
print(f'{done}/{total} tools have introduction content')
if done < total:
    missing = [t['slug'] for t in tools if not t.get('introduction','').strip()]
    print('Missing:', missing)
"
```

仅当计数达到 **100%** 时才提交。一个不完整的批次（例如 93/105）意味着
还有 12 个工具仍使用单薄的模板文案——足以让 Google 把站点标记为不一致。

### 批量写入顺序

按以下顺序优先处理工具：
1. 在 Google Search Console 中已获得展示量的工具（低垂果实）
2. 位于内链最多分类下的工具（PageRank 集中区）
3. 其余工具按字母顺序

### 提交前构建验证

```bash
# Confirm build compiles cleanly after batch content additions
npm run build        # Next.js / Nuxt
python manage.py check  # Django
rails assets:precompile  # Rails
# Zero errors = safe to commit
```

---

## Phase 9 — 博客内容策略（针对排名 50–68 的关键词）

工具页面对事务型关键词（“meta tag generator”、“check broken links”）排名不错。
但信息型关键词（“how to write meta descriptions”、“what is keyword density”）的排名
停留在 50–68 位——过深以至于拿不到点击——因为工具页面并不是承载它们的合适格式。
博客文章才是。

### 诊断：找出你的 50–68 位关键词

在 Google Search Console → Search Results → 按 Position > 49 且 Position < 69 过滤。
这些是你已有足够权重能排名，但目前参与排名的页面类型不对的查询。

### 博客选题公式

```
Post title: {Informational keyword} — {Year} Guide
Target keyword: the exact query from GSC
Content length: 1,000–1,500 words
Internal links: link to 2–3 relevant tools from within the post body
```

示例映射：

| GSC 关键词（50–68 位） | 博客文章标题 | 要链接的工具 |
|---|---|---|
| "how to write meta descriptions" | "How to Write Meta Descriptions That Get Clicks (2025)" | meta-tag-generator |
| "what is keyword density" | "Keyword Density: What It Is and How to Check It" | keyword-density-checker |
| "how to find broken links" | "How to Find and Fix Broken Links on Any Website" | broken-link-finder |
| "xml sitemap best practices" | "XML Sitemap Best Practices for 2025" | xml-sitemap-visualizer |

### 博客文章结构（SEO 优化版）

```
H1: {Target keyword} — the exact GSC query, naturally phrased
Intro (100 words): answer the question directly in the first paragraph
  H2: What is {topic}?
  H2: Why it matters for SEO
  H2: How to {action} — step by step
    H3: Step 1
    H3: Step 2
    H3: Step 3
  H2: Common mistakes
  H2: {Tool name} — try it free   ← internal link to your tool
Conclusion: summarise + CTA to the tool
```

### 博客文章 Meta 要求

- `meta_title`：在合适处包含年份（如 “2025”）——提升信息型查询的 CTR
- `meta_description`：用一句话回答问题 + “Free tool included”
- `canonical`：必须指向确切的博客 URL
- 在 schema 中提供 `datePublished` + `dateModified`——对新鲜度信号至关重要

### 博客文章的内链规则

每篇博客必须在正文里包含至少 **2 条上下文内联链接**指向相关工具，
而不只是“Related Tools”侧栏。位于正文中的内联链接，
相比侧栏链接能传递明显更多的 PageRank。

```html
<!-- Good — inline contextual link -->
<p>Use our <a href="/tools/meta-tag-generator">meta tag generator</a> to preview
how your title and description appear in Google results before publishing.</p>

<!-- Weak — sidebar only, no body link -->
<aside>Related: Meta Tag Generator</aside>
```

---

## Phase 10 — 上线部署验证

一个能干净编译的修复，依然可能在生产环境失败。每次推送后，
都要验证线上站点——而不是只验证构建产物。

```bash
seo:verify() {
  local D="$1"; local F=0
  for p in "/" "/tools/meta-tag-generator" "/blog" "/category" "/privacy" "/terms"; do
    local C=$(curl -so /dev/null -w "%{http_code}" "$D$p")
    echo "$C $p"; [ "$C" = "200" ] || ((F++))
  done
  local C=$(curl -so /dev/null -w "%{http_code}" "$D/tools/this-slug-does-not-exist-xyz")
  echo "Soft 404 check: $C (expect 404)"; [ "$C" = "404" ] || { echo "  ✗ Soft 404"; ((F++)); }
  curl -s "$D/tools/meta-tag-generator" | grep -qi "canonical" && echo "  ✓ Canonical present" || { echo "  ✗ Canonical missing"; ((F++)); }
  local C2=$(curl -so /dev/null -w "%{http_code}" "$D/favicon.ico")
  echo "Favicon: $C2 (expect 200)"; [ "$C2" = "200" ] || { echo "  ✗ Favicon missing"; ((F++)); }
  local J=$(curl -s "$D/tools/meta-tag-generator" | grep -c "application/ld+json" || true)
  [ "$J" -ge 1 ] && echo "  ✓ Schema: $J blocks" || { echo "  ✗ No schema found"; ((F++)); }
  return $F
}
```

### 预期结果

| 检查项 | 期望 |
|---|---|
| 全部关键页面 | 200 |
| 无效工具 slug | 404 |
| `<link rel="canonical">` 存在 | 是 |
| `/favicon.ico` | 200 |
| `application/ld+json` 块 | 每个工具页 ≥ 1 |

若任何一项检查失败——**不要继续往下走**。先定位并修复，再进入下一阶段。

---

## Phase 11 — 提交前校验

```bash
seo:validate() {
  python3 validate_meta.py || return 1
  python3 -c "
import json
from collections import Counter
tools = json.load(open('data/tools.json', 'r'))
titles = [t.get('meta_title', '') for t in tools]
dups = [t for t, c in Counter(titles).items() if c > 1 and t]
print(dups) if dups else print('All titles unique')
"
  python3 -c "
import json
tools = json.load(open('data/tools.json', 'r'))
missing = [t['slug'] for t in tools if not t.get('introduction', '').strip()]
print(f'Missing intro ({len(missing)}):', missing[:10])
"
}
```

---

## Consolidated Runners

```bash
# Quick check — meta validation + live site verification
seo:quick() { seo:verify "$PROD_URL" && seo:validate; }
# Full check — quick + duplicate title check
seo:full()  { seo:quick; }
```

---

## 主问题控制表

| # | 问题 | 严重度 | 阶段 |
|---|---|---|---|
| 1 | 工具页面之间存在重复 / 模板文案 | 🔴 关键 | 2 |
| 2 | 缺失或千篇一律的 meta 标题 | 🔴 关键 | 1 |
| 3 | 缺失或千篇一律的 meta 描述 | 🔴 关键 | 1 |
| 4 | 所有工具共用同一个 H1 | 🔴 关键 | 3 |
| 5 | 孤立工具页面（无入站内链） | 🟡 高 | 5 |
| 6 | 缺失的相关工具链接 | 🟡 高 | 5 |
| 7 | URL slug 关键词堆砌或缺关键词 | 🟡 高 | 6 |
| 8 | 没有作者署名或最后更新日期 | 🟡 高 | 7 |
| 9 | 标题层级违规 | 🟢 中 | 3 |
| 10 | 图标按钮缺失 aria-label | 🟢 中 | 4 |

---

## 最佳实践

| ✅ 该做 | ❌ 别做 |
|-------|----------|
| 为每个工具撰写独一无二的 meta 标题 + 描述 | 在 80+ 个页面上复用同一份模板文案 |
| 先把一个工具的内容完整填好，再做下一个 | 在多个工具上批量写半成品条目 |
| 在每个工具页链接 2+ 个相关工具 | 留下零内链的孤立工具 |
| URL slug 使用 `{primary-keyword}` | 用 “free” / “online” / “tool” 之类填充 slug |
| 为每个工具页添加作者署名 + 日期 | 展示无作者、无日期的内容 |
| 针对信息型关键词（排名 50–68 位）撰写博客 | 依赖工具页来承接 “how to” 类查询 |
| 重命名 slug 时做 301 重定向 | 删除旧 slug 而不做重定向 |

---

## 关键原则

1. **永远先解决重复内容问题。** 80+ 个页面共用同一份模板文案，几乎是每一个
   表现欠佳的工具站点的根本原因。在完成这一步之前，其他修复都无关紧要。

2. **先把一个工具完整填好，再开始下一个。** 绝不要在多个工具上写半成品条目。
   一个写了一半的注册表条目比没有条目更糟——它在规模上传递了“内容单薄”的信号。

3. **内链就是 PageRank 的分配。** 一个内容很好但零入站内链的工具，对 Google
   而言是隐形的。每个工具都需要至少 2 条入站内链。

4. **URL slug 是永久的。** 一个干净的 slug 从第一天起就优于堆砌的 slug。
   在索引之前就把它做对——之后再改名，即便有 301 也会损失排名势能。

5. **E-E-A-T 不是装饰。** 没有作者、没有日期的工具页面会触发质量评估
   指南中的潜在垃圾内容判定。一个真名、一个真实日期是最基本的底线。

6. **每次提交前都要校验。** 在部署前发现缺失的描述是零成本的。
   索引之后再修复，往往要付出数周的代价。

---

## 相关技能

- [schema-markup-generator](/skills/schema-markup-generator/SKILL.md) — 工具页的 JSON-LD 结构化数据（HowTo、FAQPage、WebApplication）
- [social-metadata-hardening](/skills/social-metadata-hardening/SKILL.md) — 工具页的 OG 标签与社交分享预览
- [indexing-issue-auditor](/skills/indexing-issue-auditor/SKILL.md) — slug 变更后的完整抓取审计与重定向映射
- [pagespeed-enhancer](/skills/pagespeed-enhancer/SKILL.md) — 工具页的 Lighthouse / Core Web Vitals 审计
- [wordpress-centric-high-seo-optimized-blogwriting-skill](/skills/wordpress-centric-high-seo-optimized-blogwriting-skill/SKILL.md) — 具备 SEO 结构的博客文章写作
- [vibecode-production-qa-validator](/skills/vibecode-production-qa-validator/SKILL.md) — 端到端生产 QA，包含部署验证

---

## 何时使用

本技能适用于执行上文概述的工作流或动作。
当用户提到排名差、工具未被收录、所有工具页面排名相同、重复内容警告、“如何让每个工具页独一无二”、内容单薄，或 Google 不给工具页排名时使用。

## 局限

- 仅当任务与上文范围明确匹配时使用本技能。
- 不要把输出当作环境专属验证、测试或专家审查的替代品。
- 若必需的输入、权限、安全边界或成功标准缺失，请停下来请求澄清。
- 内容注册表假定存在结构化数据源（JSON、YAML、数据库）——纯静态 HTML 的工具页面需要先完成迁移。
- 涉及技术 SEO 因素（页面速度、Core Web Vitals、阻塞渲染）已委托给 pagespeed-enhancer 技能处理。
