# 招聘 API —— Indeed 与 Glassdoor

| 端点 | 返回 |
|---|---|
| `/scrape/indeed/listing` | Indeed 搜索结果 |
| `/scrape/indeed/job` | 单个 Indeed 职位详情 |
| `/scrape/glassdoor/listing` | Glassdoor 搜索结果 |
| `/scrape/glassdoor/job` | 单个 Glassdoor 职位（含薪资区间、公司简介） |

全部为同步 `GET`。

## Indeed Listing

```python
import requests

resp = requests.get(
    "https://api.hasdata.com/scrape/indeed/listing",
    headers={"x-api-key": API_KEY},
    params={
        "keyword":  "software engineer",
        "location": "New York, NY",
        "sort":     "date",
        "domain":   "www.indeed.com",
        "start":    0,
    },
    timeout=300,
)
```

| 参数 | 说明 |
|---|---|
| `keyword` | **必填。** |
| `location` | **必填。** |
| `sort` | `date`、`relevance`（默认）。 |
| `domain` | 国家站点 —— `www.indeed.com`、`uk.indeed.com`、`de.indeed.com`。 |
| `start` | 偏移量，**步长 10**。 |

响应：`jobs` 数组包含 `title`、`company`、`location`、`salary`、`description`、`postedAt`、`link`、`jobKey`。薪资是自由格式的字符串 —— 需用正则解析。

## Indeed Job

传入 `jobKey`（来自 listing）→ 返回完整描述、要求、福利、公司 URL。

## Glassdoor Listing & Job

```python
params = {"keyword": "software engineer", "location": "New York, NY", "sort": "recent"}
# pagination: pass back nextPageToken
```

| 参数 | 说明 |
|---|---|
| `keyword`、`location` | **必填。** |
| `sort` | `recent`（默认）、`relevant`。 |
| `domain` | 国家站点。 |
| `nextPageToken` | 游标分页。 |

## 模式

### 薪资区间

```python
import re, statistics

def salary_band(role, location):
    page = requests.get(
        "https://api.hasdata.com/scrape/indeed/listing",
        headers={"x-api-key": API_KEY},
        params={"keyword": role, "location": location}, timeout=300,
    ).json()
    nums = [int(m.replace(",", ""))
            for j in page.get("jobs", [])
            for m in re.findall(r"\$([\d,]+)", j.get("salary") or "")]
    if not nums: return None
    return {"n": len(nums), "median": statistics.median(nums)}
```

### 按公司统计招聘速度

```python
from collections import Counter

page = indeed_listing(role, loc, sort="date")
Counter(j.get("company") for j in page.get("jobs", []))
```

每周运行一次；持续的增长往往先于财报/PR 信号出现。

### 分页方式不同

```python
# Indeed: numeric start
for p in range(10):
    page = indeed_listing(kw, loc, start=p * 10)

# Glassdoor: cursor token
out, token = [], None
while True:
    page = glassdoor_listing(kw, loc, next_token=token)
    out.extend(page.get("jobs", []))
    token = page.get("nextPageToken")
    if not token: break
```

## 陷阱

- **薪资是自由格式字符串。** 务必使用正则解析。
- **Indeed = 数字 start（10），Glassdoor = token。** 不要混用。
- **非美国地区 `domain` 很重要。** `uk.indeed.com`、`ca.indeed.com` 等。
- **批量场景优先使用 API + 分页。** 只有在您希望跨多个关键字 × 地点组合通过 Webhook 驱动扇出，而不想自己管理轮询循环时，才使用对应的 Scraper Job。