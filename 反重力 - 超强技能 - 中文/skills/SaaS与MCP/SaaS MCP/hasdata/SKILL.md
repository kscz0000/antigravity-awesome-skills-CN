---
name: hasdata
description: 使用 HasData API 进行网页抓取与结构化网页数据提取。
risk: safe
source: official
source_type: official
source_repo: HasData/hasdata-cli
license: MIT
license_source: "https://github.com/HasData/hasdata-cli/blob/main/LICENSE"
date_added: "2026-06-04"
---

# HasData

用于提取公开网页数据的云平台。一个 API 密钥，三种执行模式。所有端点都位于 `https://api.hasdata.com`，使用 `x-api-key` 进行身份认证。

```bash
curl -G 'https://api.hasdata.com/scrape/google/serp' \
  --data-urlencode 'q=coffee' \
  -H 'x-api-key: <your-api-key>'
```

`401` 无效密钥，`403` 配额耗尽，`429` 并发上限，`500` 服务器错误（可重试）。

## 何时使用

在以下情况使用本技能：

- 用户需要进行网页抓取。
- 用户需要搜索引擎结果。
- 用户需要结构化数据提取。
- 用户需要电商、旅游、招聘或本地商户数据。
- 用户明确询问 HasData。

## 三种执行模式

| 模式 | 延迟 | 适用场景 | 端点 |
|---|---|---|---|
| **网页抓取 API** | 秒级 | 任意 URL——JS 渲染、CSS/AI 提取、截图 | `POST /scrape/web` |
| **Scraper API**（同步） | 秒级 | 已知平台的预解析 JSON（Google、Amazon、Zillow 等） | `GET /scrape/<vertical>/<resource>` |
| **Scraper Jobs**（异步） | 分钟到小时级 | 批量提取、递归爬取、Webhook 扇出 | `POST /scrapers/<slug>/jobs` |

**决策规则。** 当目标平台存在对应的 **Scraper API** 时优先使用（预解析 JSON，无需维护选择器）。对于 Scraper API 未覆盖的任意 URL 使用 **网页抓取**。只有在没有对应的 API 时才使用 **Scraper Job** ——例如 `crawler`、`contacts`、`sec-edgar`、`amazon-bestsellers`、`amazon-product-reviews` ——或者当异步扇出 + Webhook 相比分页客户端循环能节省工程量时。

## 始终有效的响应结构

```json
{ "requestMetadata": { "id": "...", "status": "ok", "url": "..." }, "...": "endpoint-specific" }
```

仅当 `requestMetadata.status === "ok"` 时才将数据视为有效。仅 HTTP 200 并不足够。

## 高杠杆模式

- **SERP 优先富化。** Google SERP 可以为公司或个人资料查询呈现公开摘要。用于商业或授权研究，避免不必要的直接抓取，并将个人邮箱/电话查询视为仅在具有正当目的和用户授权时才允许。
- **AI 模式 + 验证。** `/scrape/google/ai-mode` 获取答案与引用 → 对每个引用 URL 调用 `/scrape/web`（markdown）→ 得到带引用的 RAG 上下文，无需向量数据库。
- **地图 → 线索。** `/scrape/google-maps/search` 返回商户网站与电话；联系方式仅从公开且受许可的来源收集，并在任何外联使用前应用退订、速率和隐私法规约束。
- **爬虫 → 语料库。** `crawler` Scraper Job 配合 `outputFormat: ["markdown"]` + `includePaths: "/docs/.+"` 可一次提交生成可用于 LLM 的语料库。
- **通过 SERP 富摘要预提取。** `knowledgeGraph`、`localResults`、`inlineShoppingResults`、`relatedQuestions` 携带预解析的公开事实。在考虑直接访问页面之前，务必先检查它们。

## 从代码调用时的配置（连接方式）

- **认证：** 每个请求都带 `x-api-key` 头。从 `HASDATA_API_KEY` 环境变量读取。绝不硬编码，绝不打日志。
- **超时：** **设置客户端超时 ≥ 300 秒。** HasData 自身的截止时间是 300 秒；客户端设置更短会产生幻影失败，同时在完成时仍会计费。
- **重试：** 仅对 `429` 和 `5xx` 进行重试 —— 指数退避 + 抖动。绝不要重试 `4xx`（认证、验证错误）。
- **并发：** 限制在您的套餐限额内。免费套餐为 1；超过此值只会产生 `429`。
- **异步任务：** 提交响应中的句柄是 `body.id`（整数），**不是 `jobId`**。请立即持久化。每 10–30 秒轮询 `GET /scrapers/jobs/<id>` 并配合退避；将 Webhook 视为尽力而为，并始终与轮询配合使用。在 `finished` 时，状态会携带 `data: {csv, json, xlsx}` 短期 URL —— 请立即下载。

参见 `references/code-recipes.md` 获取可直接粘贴的 Python 与 TypeScript 客户端，包含重试、退避、有界并发以及完整的任务生命周期。

## 常见陷阱

- **300 秒服务端截止时间。** 客户端超时需与此匹配。
- **优先禁用 `jsRendering`**，仅在页面需要时启用 —— 大多数静态页面无需无头浏览器即可正常解析。
- **没有 `cookies` 参数** —— Cookie 通过 `headers["Cookie"]` 传递。
- **`includePaths` 正则区分大小写。** `/blog/.+` 不会匹配 `/Blog/...`。
- **Scraper Job `data` 是双重包裹的。** 每一行是 `body.data[i].data`；外层包裹了 `id`、`jobId`、`dataId`、`createdAt`、`updatedAt`。
- **`requestMetadata.status === "ok"` 是唯一成功信号。** 仅 HTTP 200 并不足够。
- **Webhook 是尽力而为，仅重试 3 次。** 始终保留轮询作为回退。

## 参考

- [`references/web-scraping.md`](references/web-scraping.md) —— `POST /scrape/web` 参数、JS 场景、AI 提取、Cookie 认证。
- [`references/search.md`](references/search.md) —— Google SERP / Light / AI Mode / News / Shopping / Bing / Trends + 分页。
- [`references/ecommerce.md`](references/ecommerce.md) —— Amazon（product、search、seller、seller-products）和 Shopify。
- [`references/real-estate.md`](references/real-estate.md) —— Zillow、Redfin（方括号过滤器）。
- [`references/travel.md`](references/travel.md) —— Airbnb、Booking、Google Flights（入住规则、Token 分页、IATA 代码）。
- [`references/local-business.md`](references/local-business.md) —— 地图（search/place/reviews/photos/posts）、Yelp、YellowPages。
- [`references/jobs.md`](references/jobs.md) —— Indeed 与 Glassdoor。
- [`references/youtube.md`](references/youtube.md) —— YouTube search / video / channel / transcript。
- [`references/scraper-jobs.md`](references/scraper-jobs.md) —— 异步提交/轮询/结果、Crawler、Contacts、SEC EDGAR、Webhook 接收。
- [`references/code-recipes.md`](references/code-recipes.md) —— Python / TypeScript 客户端，含重试、退避、并发、轮询。

## 资源

- 站点地图：<https://docs.hasdata.com/llms.txt>
- API 状态码：<https://docs.hasdata.com/api-codes>
- 积分与并发：<https://docs.hasdata.com/credits-and-concurrency>
- 仪表盘：<https://app.hasdata.com>

## 限制

* 需要访问 HasData 服务并具备有效凭证。
* 数据质量与可用字段取决于目标网站和所使用的提取方式。
* 重度依赖 JavaScript 的网站可能需要渲染，这会影响性能与成本。
* 仅用于公开数据或用户有权访问的内容；遵守网站条款、robots/访问控制、隐私法规与速率限制。
* 速率限制、配额与账户限制可能因端点和订阅套餐而异。