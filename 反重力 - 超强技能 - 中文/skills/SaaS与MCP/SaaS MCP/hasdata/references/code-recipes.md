# 代码模板 —— 将 HasData 集成到您的代码中

## 基本规则

- **Base URL：** `https://api.hasdata.com`。每个请求都带 `x-api-key` 头。
- **方法：** Scraper API 为 `GET`；网页抓取为 `POST`；Scraper Jobs 使用 `POST`（提交）+ `GET`（状态/结果）+ `DELETE`（停止）。
- **密钥处理：** 从环境变量读取（`HASDATA_API_KEY`）。绝不硬编码，绝不打日志。
- **超时：** **客户端超时 ≥ 300 秒。** HasData 的截止时间是 300 秒；客户端更短会产生幻影失败，同时仍会计费。
- **重试：** 仅对 `429` 和 `5xx` 使用指数退避 + 抖动重试。绝不要重试 `4xx`。
- **并发：** 限制在套餐限额内。免费套餐 = 1。
- **成功信号：** 同步 API 要求 `body.requestMetadata.status === "ok"`。仅 HTTP 200 并不足够。

## 状态码

| 状态码 | 含义 | 操作 |
|---|---|---|
| 200 + `status:"ok"` | 成功 | 使用 body |
| 401 | 密钥错误或缺失 | 修复 —— 不要重试 |
| 403 | 配额耗尽 | 不要重试 |
| 429 | 并发上限 | 退避 + 重试 |
| 500 | 服务器错误 | 重试 |

## Python —— 最简客户端

```python
import os, requests

class HasData:
    BASE = "https://api.hasdata.com"

    def __init__(self, api_key=None, timeout=300):
        self.s = requests.Session()
        self.s.headers["x-api-key"] = api_key or os.environ["HASDATA_API_KEY"]
        self.timeout = timeout

    def get(self, path, **params):
        r = self.s.get(f"{self.BASE}{path}", params=params, timeout=self.timeout)
        r.raise_for_status()
        body = r.json()
        if body.get("requestMetadata", {}).get("status") != "ok":
            raise RuntimeError(f"hasdata not-ok: {body.get('requestMetadata')}")
        return body

    def post(self, path, body):
        r = self.s.post(f"{self.BASE}{path}", json=body, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

hd = HasData()
serp = hd.get("/scrape/google/serp", q="coffee", num=20)["organicResults"]
md   = hd.post("/scrape/web", {"url": "https://example.com", "outputFormat": ["markdown"]})["markdown"]
```

## Python —— 重试 + 有界并发

```python
import time, random
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import HTTPError

def with_retry(fn, attempts=5, base=1.0, cap=60.0):
    for i in range(attempts):
        try:
            return fn()
        except HTTPError as e:
            code = e.response.status_code
            if code == 429 or 500 <= code < 600:
                time.sleep(min(cap, base * 2 ** i) + random.random())
                continue
            raise
    raise RuntimeError("retry exhausted")

def scrape_many(urls, workers=5):
    out = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(lambda u=u: hd.post("/scrape/web", {"url": u, "outputFormat": ["markdown"]})): u
                for u in urls}
        for f in as_completed(futs):
            try:
                out[futs[f]] = f.result().get("markdown")
            except Exception as e:
                out[futs[f]] = e
    return out
```

将 `workers` 限制在您套餐的并发上限内 —— 超过只会产生 `429`。

## TypeScript —— 最简客户端

```typescript
const BASE = "https://api.hasdata.com";
const KEY  = process.env.HASDATA_API_KEY!;

async function get<T = any>(path: string, params: Record<string, string | number> = {}): Promise<T> {
  const qs = new URLSearchParams(Object.entries(params).map(([k, v]) => [k, String(v)]));
  const r = await fetch(`${BASE}${path}?${qs}`, {
    headers: { "x-api-key": KEY },
    signal:  AbortSignal.timeout(300_000),
  });
  if (!r.ok) throw new Error(`HasData ${r.status} ${await r.text()}`);
  const body = await r.json() as any;
  if (body?.requestMetadata?.status && body.requestMetadata.status !== "ok") {
    throw new Error(`HasData not-ok: ${JSON.stringify(body.requestMetadata)}`);
  }
  return body as T;
}

async function post<T = any>(path: string, body: unknown): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method:  "POST",
    headers: { "x-api-key": KEY, "Content-Type": "application/json" },
    body:    JSON.stringify(body),
    signal:  AbortSignal.timeout(300_000),
  });
  if (!r.ok) throw new Error(`HasData ${r.status} ${await r.text()}`);
  return r.json() as Promise<T>;
}

// Bounded concurrency, no deps
async function pool<T, R>(items: T[], n: number, fn: (x: T) => Promise<R>) {
  const out: R[] = []; let i = 0;
  await Promise.all(Array.from({ length: n }, async () => {
    while (i < items.length) { const k = i++; out[k] = await fn(items[k]); }
  }));
  return out;
}
```

## 分页速查表

| 端点系列 | 分页 |
|---|---|
| Google SERP / Light SERP / Bing | `start` + `num`（最大 100） |
| Google Maps Search | `start`（步长 20） |
| Yelp Search | `start`（步长 10） |
| Google Maps Reviews / Glassdoor / Airbnb | `nextPageToken` |
| Indeed / YellowPages / Amazon Search | `start` 或 `page` |
| Shopify Products | `page`（配合 `limit` ≤ 250） |
| Scraper-Job results | `page` + `limit`（最大 100），直到 `meta.currentPage >= meta.lastPage` |

## 上线前检查清单

- [ ] 密钥从环境变量读取，从不记录。
- [ ] 所有 HTTP 超时 ≥ 300 秒。
- [ ] 每个同步响应都检查 `requestMetadata.status === "ok"`。
- [ ] 对 429 + 5xx 进行退避；不对 4xx 退避。
- [ ] 并发限制在套餐上限内。
- [ ] 任务的 `id`（来自提交响应）已立即持久化到持久存储。
- [ ] Webhook 配合轮询回退。
- [ ] 结果文件在 `scraper.job.finished` 时立即下载。