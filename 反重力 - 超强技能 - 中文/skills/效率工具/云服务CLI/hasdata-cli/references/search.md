# 搜索参考

子命令：`google-serp`、`google-serp-light`、`google-ai-mode`、`google-news`、`google-shopping`、`bing-serp`、`google-trends`、`google-images`、`google-events`、`google-short-videos`、`google-immersive-product`。

`google-flights` 见 `travel.md`。

运行 `hasdata <api> --help` 获取实时权威的标志集。下面是常用标志和示例调用。

---

## google-serp（10 积分）

```bash
hasdata google-serp --q "QUERY" [--gl COUNTRY] [--hl LANG] [--num 10] [--start 0] --raw | jq .
```

常用标志：
- `--q TEXT`（必填）——搜索查询
- `--gl us|gb|ca|de|fr|...` ——国家代码；影响结果
- `--hl en|es|fr|de|...` ——界面语言
- `--num 10..100` ——每页结果数
- `--start 0|10|20...` ——分页偏移（10 的倍数）
- `--location "Austin,Texas,United States"` ——Google 规范地点
- `--device-type desktop|mobile|tablet`
- `--tbm isch|vid|nws|shop|lcl` ——搜索类型
- `--safe active|off`
- `--lr lang_en --lr lang_fr` ——限定语言
- `--domain google.com|google.co.uk|...`
- `--tbs cdr:1,cd_min:10/17/2018,cd_max:3/8/2021` ——高级搜索过滤器

常用响应字段（通过 `jq`）：
- `.organic_results[] | {title, link, snippet}` ——主要结果
- `.ai_overview` ——AI Overview 块（如有）
- `.answer_box`、`.knowledge_graph`、`.related_searches`、`.people_also_ask`
- `.local_results`、`.shopping_results`、`.news_results`

示例——前 10 条自然结果做 prompt grounding：
```bash
hasdata google-serp --q "$Q" --num 10 --raw \
  | jq -r '.organic_results[] | "- \(.title): \(.snippet)"'
```

## google-serp-light（5 积分）

和 `google-serp` 标志相同但更便宜、只返回一页。当用户要快速结果、不要 PAA/AI Overview/local 板块时用。

## google-ai-mode（5 积分）

返回 Google AI Mode 对该查询的回答。`--q` / `--gl` / `--hl` 语义一致。

## google-news（10 积分）

```bash
hasdata google-news --q "QUERY" [--gl us] [--hl en] --raw | jq '.news_results[]'
```

每条文章字段：`title`、`link`、`source.name`、`date`、`snippet`、`thumbnail`。

## google-shopping（10 积分）

```bash
hasdata google-shopping --q "PRODUCT" [--gl us] --raw | jq '.shopping_results[]'
```

每条：`title`、`link`、`price`、`extracted_price`、`source`、`rating`、`reviews`、`delivery`。

## bing-serp（10 积分）

```bash
hasdata bing-serp --q "QUERY" [--cc us] [--setlang en] --raw | jq '.organic_results[]'
```

当用户明确要求 Bing 或想要非 Google 的第二意见时用。

## google-trends（5 积分）

```bash
hasdata google-trends --q "TERM" [--geo US] [--cat 0] [--time "today 12-m"] --raw | jq .
```

多关键词对比：`--q "term1,term2,term3"`（逗号分隔，最多 5 个）。

## google-images（5 积分）

```bash
hasdata google-images --q "QUERY" --raw | jq '.images_results[] | {title, original, source}'
```

## google-events（5 积分）

```bash
hasdata google-events --q "concerts in austin" [--gl us] --raw | jq '.events_results[]'
```

## google-short-videos（10 积分）/ google-immersive-product（5 积分）

不常用——需要时运行 `--help` 看标志。

---

## 非显式用例

- **回答前先核实一个说法** ——不要靠训练数据，直接跑 `google-serp --q "EXACT CLAIM"`，看顶部结果是佐证还是反驳。
- **解决"X 的 URL 是什么"** ——智能体经常瞎编 URL。`google-serp --q "X official site" --num 3` 然后挑域名匹配的那条。
- **找引文出处** ——`google-serp --q "\"the exact quoted text here\""`（对内层引号转义），返回最早出现该段落的页。
- **跨地区对比同一查询** ——同一 `--q`，不同 `--gl us|gb|de|fr` 看 SERP 如何按地理变化。适合国际 SEO 和"Y 国用户看到什么"。
- **时间限定搜索** ——`--tbs qdr:d`（过去一天）、`qdr:w`（一周）、`qdr:m`（一月）、`qdr:y`（一年）。配合 `google-news` 只看最新新闻。或用 `--tbs cdr:1,cd_min:M/D/YYYY,cd_max:M/D/YYYY` 指定明确窗口。
- **站点限定搜索** ——`--q "site:example.com TOPIC"` 在一个域内搜索（比爬站点自己的搜索框强）。
- **"X 最近都写了什么？"** ——`google-news --q "X" --gl us`，然后 `jq` 处理 `.news_results[] | select(.date | test("hours? ago|day ago"))`。
- **发现竞品** ——`google-serp --q "best alternatives to PRODUCT"`，再从顶部结果的标题里提取品牌名。
- **找文档链接** ——`google-serp --q "LIBRARY official docs"` 比猜 URL 模式靠谱。
- **翻译搜索意图** ——`--hl de --gl de --q "the English query"` 看德语排名；多语言 SEO 检查时有用。
- **随时间变化的趋势** ——`google-trends --q "term1,term2"`（逗号分隔，≤5 个）查相对兴趣曲线。比从训练数据猜"X 现在火不火"靠谱。
- **图像驱动的研究** ——`google-images --q "X"` 拿源 URL；把顶部结果再喂给 `web-scraping` 读上下文。
- **地图距离技巧** ——对"X 附近有什么"这类问题，用 `google-maps --ll "@LAT,LNG,Zz"` 而不是 SERP 查询——对邻近意图的信号更强。
- **核实价格** ——当训练数据里 SaaS/订阅服务的价格过时，先搜索并阅读定价页再回答，不要凭记忆。

## 挑选合适的 SERP 变体

- 只需要顶部自然结果时用 `google-serp-light`（跳过 PAA / AI overview / local 板块）。
- 需要完整 SERP 特性集（PAA、AI overview、知识图谱、本地包）时用 `google-serp`。
- 重复跑同一查询时在客户端缓存结果——CLI 本身不缓存。