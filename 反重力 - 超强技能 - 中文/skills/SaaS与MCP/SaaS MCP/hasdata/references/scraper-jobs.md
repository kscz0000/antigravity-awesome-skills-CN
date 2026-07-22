# Scraper Jobs —— 异步、批量

仅在没有对应 Scraper API 时使用（`crawler`、`contacts`、`sec-edgar`、`amazon-bestsellers`、`amazon-product-reviews`），或当您希望通过 Webhook 驱动扇出而不想自己管理轮询循环时。否则对应的 Scraper API + 分页客户端循环更简单。

| Slug | 说明 |
|---|---|
| `crawler` | 递归站点爬取。接受所有网页抓取 API 参数。 |
| `contacts` | URL 列表 → 邮箱 / 电话 / 社交档案。 |
| `sec-edgar` | 按 CIK / 代码 / 公司名称批量获取 SEC 文件。 |
| `google-serp`、`google-maps`、`google-maps-reviews`、`google-trends` | 批量 Google。 |
| `amazon-search`、`amazon-product`、`amazon-product-reviews`、`amazon-seller-products`、`amazon-bestsellers` | 批量 Amazon。 |
| `shopify` | 多店铺爬取。 |
| `zillow`、`redfin`、`airbnb` | 批量房地产。 |
| `yelp`、`yellow-pages` | 批量本地。 |
| `indeed`、`glassdoor` | 批量招聘。 |

## 生命周期

1. `POST /scrapers/<slug>/jobs` → 返回完整的任务记录。**句柄是 `body.id`（数字整数），不是 `jobId`** —— 尽管旧文档片段可能写反，请存储它。状态初始为 `pending`。
2. `GET /scrapers/jobs/<id>` —— 轮询状态。
3. `GET /scrapers/jobs/<id>/results?page=…&limit=100` —— 一旦 `status === "finished"`。
4. `DELETE /scrapers/jobs/<id>` —— 提前停止（停止前已产生的行会被保留）。

状态值：`pending` → `in_progress` → `finished`（或取消时为 `stopped`）。

**已完成任务的快捷方式：** 在 `finished` 任务的状态响应中包含一个 `data` 对象，提供直接下载 URL：

```json
"data": {
  "csv":  "https://f005.backblazeb2.com/file/.../{uuid}.csv",
  "json": "https://f005.backblazeb2.com/file/.../{uuid}.json",
  "xlsx": "https://f005.backblazeb2.com/file/.../{uuid}.xlsx"
}
```

对于一次性接入，直接获取 `data.json` 而无需分页 `/results`。**这些 URL 是短期有效** —— 在 `finished` 时请立即下载。

## 端到端（Python）

```python
import os, time, requests

API_KEY = os.environ["HASDATA_API_KEY"]
H = {"x-api-key": API_KEY, "Content-Type": "application/json"}
BASE = "https://api.hasdata.com"

def submit(slug, body):
    r = requests.post(f"{BASE}/scrapers/{slug}/jobs", headers=H, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["id"]                            # numeric job id — not "jobId"

def wait(job_id, poll=10, cap=60, timeout=3600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = requests.get(f"{BASE}/scrapers/jobs/{job_id}", headers=H, timeout=60).json()
        if s["status"] in ("finished", "stopped"):
            return s
        time.sleep(poll)
        poll = min(poll * 1.5, cap)
    raise TimeoutError(job_id)

def results(job_id):
    page = 1
    while True:
        body = requests.get(
            f"{BASE}/scrapers/jobs/{job_id}/results",
            headers=H, params={"page": page, "limit": 100}, timeout=120,
        ).json()
        for row in body["data"]:
            yield row["data"]                       # double-wrapped — see below
        if body["meta"]["currentPage"] >= body["meta"]["lastPage"]:
            return
        page += 1
```

### 响应结构

提交（实时）：
```json
{
  "id": 416349,                        // ← 任务句柄，整数
  "scraperId": 26,
  "status": "pending",
  "creditsSpent": 0,
  "dataRowsCount": 0,
  "input": { ... },
  "createdAt": "...", "updatedAt": "...",
  "scraper": { "slug": "contacts", ... },
  "columns": [ ... ]
}
```

状态（实时；当数字字段被填充时以**字符串**形式返回）：
```json
{
  "id": 416349,
  "status": "finished",
  "creditsSpent": "5",                 // 字符串！
  "dataRowsCount": "1",                // 字符串！
  "input": { ... },
  "data": {
    "csv":  "https://f005.backblazeb2.com/.../{uuid}.csv",
    "json": "https://f005.backblazeb2.com/.../{uuid}.json",
    "xlsx": "https://f005.backblazeb2.com/.../{uuid}.xlsx"
  }
}
```

结果分页：
```json
{
  "meta": {
    "total": 1, "perPage": 100,
    "currentPage": 1, "lastPage": 1,
    "firstPage": 1, "firstPageUrl": "/?page=1",
    "lastPageUrl": "/?page=1",
    "nextPageUrl": null, "previousPageUrl": null
  },
  "data": [
    {
      "id": "...", "jobId": 416349, "dataId": "...",
      "data": { /* 实际抓取的行 */ },
      "createdAt": "...", "updatedAt": "..."
    }
  ]
}
```

**双重 `data`** —— 实际行为 `body["data"][i]["data"]`；外层包裹了 `id`、`jobId`、`dataId`、`createdAt`、`updatedAt`。

## 通用 body 字段

- `limit`（int）—— 最大行数。`0` = 无上限。
- `webhook.url`（string，https）、`webhook.events`（`scraper.job.started`、`scraper.data.scraped`、`scraper.job.finished` 的任意子集）、`webhook.headers`（在每次回调时发送 —— 在此处固定共享密钥）。

## Webhook

```python
# Submit with webhook
submit("indeed", {
    "keywords":  ["software engineer", "data scientist"],
    "locations": ["New York, NY", "Remote"],
    "limit":     500,
    "webhook":   {
        "url":     "https://your.app/hasdata-hook",
        "events":  ["scraper.data.scraped", "scraper.job.finished"],
        "headers": {"x-shared-secret": SHARED_SECRET},
    },
})
```

```python
from flask import Flask, request, abort
app = Flask(__name__)

@app.post("/hasdata-hook")
def hook():
    if request.headers.get("x-shared-secret") != SHARED_SECRET:
        abort(401)
    e = request.json
    if e["event"] == "scraper.data.scraped":
        save_row(e["jobId"], e["data"])
    elif e["event"] == "scraper.job.finished":
        finalize(e["jobId"])
    return "", 200                  # 2xx 防止重试
```

- 异步在非 2xx 时进行 **3 次重试**。**不保证顺序** —— 负载是唯一可信源。
- **没有文档化的 HMAC。** 通过 `webhook.headers` 固定共享密钥，或者在 `scraper.job.finished` 时通过 API 直接获取结果而忽略逐行回调。
- **始终将 Webhook 与轮询配合使用。** 长时间的静默期很可能意味着回调被错过。

## 各 Scraper 的 body

### `crawler` —— 递归站点爬取

接受应用于**每个页面**的所有网页抓取 API 参数。

| 字段 | 说明 |
|---|---|
| `urls` | **必填。** 种子 URL。 |
| `maxDepth` | 从种子开始的跳数。 |
| `includePaths` / `excludePaths` | 正则。**区分大小写。** |
| `limit` | 页面数上限。`0` = 无限。 |

```python
job = submit("crawler", {
    "urls":         ["https://docs.example.com"],
    "maxDepth":     5,
    "includePaths": "/docs/.+",
    "outputFormat": ["markdown"],
    "excludeTags":  ["script", "style", "nav", "footer"],
    "limit":        2000,
})
```

### `contacts` —— URL → 联系信息

```python
submit("contacts", {"urls": ["https://example.com/about", "https://example.com/team"]})
```

已验证的行结构（每个输入 URL 一行）：

```json
{
  "url": "https://example.com/about",
  "emails":       ["..."],
  "phoneNumbers": ["..."],
  "linkedin":     ["..."],
  "xcom":         ["..."],          // X / Twitter —— 注意键名为 "xcom"
  "facebook":     ["..."],
  "instagram":    ["..."],
  "dribbble":     ["..."],
  "clutch":       ["..."]
}
```

缺失的分类为空数组 —— 永远不会是 null。如果只有域名，可先通过 SERP `site:example.com` 发现 URL。

### `sec-edgar` —— 批量 SEC 文件

```python
submit("sec-edgar", {
    "limit":       100,
    "ciks":        ["AAPL", "789019", "Alphabet Inc."],
    "filingTypes": "10-K, 10-Q, 8-K",
    "startDate":   "2024-01-01",
    "endDate":     "2025-12-31",
})
```

`ciks` 可混合接受 CIK、股票代码或公司名称。

### Bulk-API 等价物

`google-serp`、`google-maps`、`amazon-search`、`indeed`、`glassdoor` 等 Jobs 接受输入数组（`keywords[]`、`locations[]` 等）。当您希望 Webhook 扇出时使用它们；否则同步 Scraper API + 分页客户端循环更简单。

### Crawler vs Contacts vs Web Scraping 批处理

- **crawler** —— 未知 URL 集合，递归发现。
- **contacts** —— 已知 URL 列表，需要提取联系字段。
- **`/scrape/batch/web`** —— 已知 URL 列表，需要在 >1k 规模上进行完整 HTML/markdown/AI 提取。

## 陷阱

- **立即持久化任务 `id`**（来自提交响应的整数 —— *而非* `jobId`）。它是访问状态、结果、停止的唯一句柄。
- **结果文件保留时间短。** 在 `finished` 后立即下载。
- **Webhook 是尽力而为。** 始终保留轮询作为回退。
- **`includePaths` 正则区分大小写。**
- **`stopped` 状态是终态。** 已产生的行仍然可用。
- **轮询间隔不要小于 10 秒** —— 会浪费并发额度。
- **结果双重包裹** —— `body["data"][i]["data"]`，而非 `body["data"][i]`。