# 数据增强

用公开数据丰富化公司、域名或经授权的联系人列表。仅在经许可的商业调研、用户授权的联系人增强场景下使用，并遵守站点条款、robots/访问控制、隐私法、退出订阅义务和速率限制。

## SERP 优先。Web-scraping 是最后手段。

`google-serp` 是首选的数据增强工具。理由：

- **Google 已经抽好了你要的结构化字段。** `.knowledge_graph` 包含总部、创始人、成立年份、母公司、员工数、行业。`.organic_results[]` 的标题和摘要携带人 → 职位 → 雇主的映射（LinkedIn 标题就是 `Name — Role at Company`）。`.local_results[]` 携带电话/地址/营业时间。
- **避免不必要的直接访问。** 许多目标站点限制、限速或禁止爬取。Google 摘要就能回答公开的高层问题，不必渲染目标页。
- **覆盖面广的公开索引。** 带引号的查询（`--q '"info@example.com"'`、`--q '"+1 555 123 4567"'`、`--q '"Acme Corp"'`）能找到公开索引的商业联系人或公司信息。

优先使用 `google-serp`（新闻时效用 `google-news`，地点用 `google-maps`，商品用 `google-shopping`）。只在以下情况回落到 `web-scraping`：
- 你需要的具体字段不在任何 SERP 摘要里，并且
- 目标页能通过服务端或可被爬虫处理的 JS 渲染该字段，并且
- 用户明确需要，并有访问权限（别在 SERP 能回答 N-0 个的情况下做 N 次 web-scraping）。

下面的模式展示完整链路，便于理解何时该升级。真实 CSV 大多数行在第 1 或第 2 步就停了。

---

## 个人信息增强

### 第 1 步 —— 用 SERP 查职位、雇主、LinkedIn URL

```bash
hasdata google-serp --q '"Jane Doe" linkedin' --num 5 --raw \
  | jq -c '.organic_results[] | select(.link | contains("linkedin.com/in/")) |
           {title, snippet, link}'
```

结果通常长这样：

```json
{
  "title": "Jane Doe — Senior Engineer at Acme Corp | LinkedIn",
  "snippet": "San Francisco, CA · 500+ connections · Engineering @ Acme. Previously...",
  "link": "https://www.linkedin.com/in/janedoe"
}
```

到这里你已经有了职位、雇主、地点、LinkedIn URL 和人脉数提示——什么都没爬。**除非确实需要额外字段，否则就停在这里。**

### 第 2 步 —— 用定向 SERP 查询精炼

若第 1 步还缺字段，可以更精准地问 Google：

```bash
# Disambiguate by company
hasdata google-serp --q '"Jane Doe" "Acme Corp"' --num 10 --raw \
  | jq -c '.organic_results[] | {title, snippet, link}'

# Other social profiles
hasdata google-serp --q '"Jane Doe" site:twitter.com OR site:x.com' --num 3 --raw
hasdata google-serp --q '"Jane Doe" site:github.com' --num 3 --raw

# Past employers / bio paragraphs
hasdata google-serp --q '"Jane Doe" bio OR background OR experience' --num 5 --raw \
  | jq -r '.organic_results[].snippet'
```

### 第 3 步 —— Web-scraping（仅在 SERP 不足时）

当 SERP 摘要截断了你需要的字段，或用户明确想要完整的资料内容时，先确认该资料页是公开的或用户有访问授权：

```bash
hasdata web-scraping --url "https://www.linkedin.com/in/janedoe" \
  --output-format markdown --no-screenshot --no-block-resources \
  --raw | jq -r .markdown
```

或者用 AI 抽取结构化字段：

```bash
hasdata web-scraping --url "https://www.linkedin.com/in/janedoe" \
  --ai-extract-rules-json '{
    "headline":   {"type": "string"},
    "location":   {"type": "string"},
    "company":    {"type": "string"},
    "role":       {"type": "string"},
    "followers":  {"type": "number"},
    "experience": {"type": "list", "output": {
      "company":  {"type": "string"},
      "role":     {"type": "string"},
      "duration": {"type": "string"}
    }}
  }' --raw | jq .
```

LinkedIn 有时会拦截公开预览；若如此，回退到第 2 步（综合 SERP 摘要）——几乎总是够用。

### 邮箱查找

三角验证，不要做承诺。仅用于商业联系人发现、用户授权的增强或其他正当用途。SERP 优先，爬取殿后；永远不要把模式猜测的个人邮箱当成已验证结果。

```bash
# 1. Has Google already indexed the email anywhere?
hasdata google-serp --q '"jane.doe@acme.com"' --num 10 --raw \
  | jq -c '.organic_results[] | {title, snippet, link}'

# 2. What email format does the company use? Look for any indexed @company.com address.
hasdata google-serp --q 'site:acme.com "@acme.com"' --num 10 --raw \
  | jq -r '.organic_results[].snippet' \
  | grep -oE '[A-Za-z0-9._-]+@acme\.com' | sort -u

# 3. Pattern-guess + SERP-verify
for guess in "jane.doe" "jdoe" "jane" "j.doe" "janed"; do
  count=$(hasdata google-serp --q "\"$guess@acme.com\"" --num 1 --raw \
            | jq -r '.organic_results | length')
  [ "$count" -gt 0 ] && echo "$guess@acme.com  (appears in SERP)"
done

# 4. Last resort — scrape the company's public contact / about / team pages for emails
hasdata web-scraping --url "https://acme.com/about" --extract-emails --raw \
  | jq -r '.emails // [] | .[]'
```

务必告诉用户某个邮箱是模式猜测还是经 SERP/爬取确认的；用户无授权时避免收集个人联系信息。

---

## 公司信息增强

### 第 1 步 —— SERP knowledge_graph

```bash
hasdata google-serp --q "Acme Corp" --num 5 --raw | jq '.knowledge_graph // {}'
```

`.knowledge_graph` 通常包含：founder、founded（年份）、headquarters、parent_organization、ceo、employees（区间）、revenue、stock_price、industry、products。**对大部分公司增强请求，这一通调用就是全部答案。**

### 第 2 步 —— 用定向 SERP 查具体字段

```bash
# Headquarters
hasdata google-serp --q '"Acme Corp" headquarters' --num 5 --raw \
  | jq -r '.organic_results[].snippet'

# Funding / acquisition signals
hasdata google-serp --q '"Acme Corp" raises OR acquires OR acquired OR ipo OR funding' --num 10 --raw \
  | jq -c '.organic_results[] | {title, snippet, link}'

# Recent news
hasdata google-news --q "Acme Corp" --gl us --raw \
  | jq -c '.news_results[] | {title, source: .source.name, date, link}'

# LinkedIn company page
hasdata google-serp --q '"Acme Corp" site:linkedin.com/company' --num 3 --raw \
  | jq -c '.organic_results[] | {title, snippet, link}'

# Employee profiles in a specific function/region
hasdata google-serp \
  --q 'site:linkedin.com/in "Acme Corp" engineer' --gl us --num 25 --raw \
  | jq -r '.organic_results[] | "\(.title)\t\(.link)"'
```

### 第 3 步 —— Web-scraping（仅在 SERP 无法填充特定字段时）

```bash
# Company About page → AI-extract structured fields
hasdata web-scraping --url "https://acme.com/about" \
  --ai-extract-rules-json '{
    "name":         {"type": "string"},
    "founded":      {"type": "number"},
    "headquarters": {"type": "string"},
    "employees":    {"type": "string"},
    "industry":     {"type": "string"},
    "description":  {"type": "string"},
    "products":     {"type": "list"}
  }' --raw | jq .
```

仅当用户要的是 SERP 无法提供的东西（例如逐字使命陈述、完整产品分类、领导团队页面解析成行）时才使用。

---

## CSV 行级增强

对 N 行名单，每行做一到两次 SERP 扇出。除非某行确实需要，否则不要把 web-scraping 加进来。

```bash
# Input: people.csv with one column "name"
while IFS=, read -r name; do
  result=$(hasdata google-serp --q "\"$name\" linkedin" --num 1 --raw)
  linkedin=$(echo "$result" | jq -r '.organic_results[0].link // ""')
  title=$(echo "$result"    | jq -r '.organic_results[0].title // ""')
  snippet=$(echo "$result"  | jq -r '.organic_results[0].snippet // ""')
  printf '%s\t%s\t%s\t%s\n' "$name" "$title" "$snippet" "$linkedin"
done < people.csv > enriched.tsv
```

就这样。每行一次 SERP，从标题和摘要提取职位/雇主/LinkedIn。只有当某行首个结果不匹配时再补一次 SERP（用 `select(.title | test("\(name)"; "i"))` 做置信度过滤）。

---

## 反向查询

总是 SERP 优先，把字面值带引号。仅在用户授权的调查、商业联系人核实或其他正当用途时使用反向查询；不要用于人肉搜索、骚扰或收集私人个人信息。

```bash
# Business email → public identity signal
hasdata google-serp --q '"jane@example.com"' --num 10 --raw \
  | jq -c '.organic_results[] | {title, snippet, link}'

# Business phone → owner / business
hasdata google-serp --q '"+1 555 123 4567"' --num 10 --raw
# Combine with yelp-search / yellowpages-search if it's a business number.

# Domain → company
hasdata google-serp --q "site:example.com" --num 5 --raw \
  | jq '.organic_results[0].title'
hasdata google-serp --q "Acme Corp" --num 5 --raw | jq '.knowledge_graph // {}'
```

只有当你特别需要首页正文时才爬域名（`web-scraping --url "https://example.com"`）。

---

## 可靠增强的技巧

- **始终把姓名等多 token 字符串加引号** ——`"Jane Doe"` 精确匹配该人；`Jane Doe` 会混入噪声。
- **善用 `site:`** ——`site:linkedin.com/in/`、`site:linkedin.com/company/`、`site:github.com`、`site:crunchbase.com`。Google 的 `site:` 是限定增强搜索最便宜的方式。
- **先读 `.knowledge_graph`** ——对公司信息增强，先看这一项；如果有内容，常常已经完成了。
- **用 AI 抽取代替 CSS 选择器** ——若必须爬，LinkedIn / Crunchbase / About 页的标记经常变；用带字段名和描述的 AI 抽取能扛住布局变动。
- **跨源验证** ——不要只从一个来源增强。若 LinkedIn 标题写 "Acme Corp" 且 `--q '"Jane Doe" "Acme Corp"'` 的 SERP 有多条结果佐证，置信度就高。
- **标注猜测** ——模式猜的邮箱、推断的地点、单一来源的职位应当作为未验证标记给用户。
- **尊重隐私和授权** ——没有正当目的和用户授权，不要收集或推断个人联系方式。