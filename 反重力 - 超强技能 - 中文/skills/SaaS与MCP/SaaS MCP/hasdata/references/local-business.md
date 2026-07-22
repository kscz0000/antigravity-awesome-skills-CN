# 本地商户 API —— Google Maps、Yelp、YellowPages

| 端点 | 返回 |
|---|---|
| `/scrape/google-maps/search` | 视口内的搜索结果 |
| `/scrape/google-maps/place` | 单个地点详情 |
| `/scrape/google-maps/reviews` | 地点的评价，支持分页 |
| `/scrape/google-maps/photos` | 照片画廊 |
| `/scrape/google-maps/posts` | 商家发布的帖子（优惠、活动、公告） |
| `/scrape/google-maps/contributor-reviews` | 某位 Google 评论者的所有评价 |
| `/scrape/yelp/search` | Yelp 搜索 |
| `/scrape/yelp/place` | Yelp 商户详情 |
| `/scrape/yellowpages/search` | YellowPages 搜索 |
| `/scrape/yellowpages/place` | YellowPages 商户详情 |

全部为同步 `GET`。

## Google Maps Search

```python
import requests

resp = requests.get(
    "https://api.hasdata.com/scrape/google-maps/search",
    headers={"x-api-key": API_KEY},
    params={"q": "Pizza", "ll": "@40.7455,-74.0083,14z"},
    timeout=300,
)
```

| 参数 | 说明 |
|---|---|
| `q` | **必填。** 自由格式查询。 |
| `ll` | `@LAT,LNG,ZOOMz` 视口 —— **经纬度 + 缩放级别，不是城市名**。进行精确分页时必填。 |
| `domain`、`gl`、`hl` | 标准参数。 |
| `start` | 分页偏移量，**步长 20**。 |

响应：`localResults` —— 每个条目包含 `position`、`title`、`placeId`、`dataId`、`kgmid`、`thumbnail`、`phone`、`address`、`website`、`description`、`workingHours`（含 `timezone` + `days[]` 的对象）、`openState`、`rating`、`reviews`、`type` + `types[]`（分类）、`price`、`priceDescription`、`gpsCoordinates`、`serviceOptions[]`、`extensions`（服务、无障碍、支付等）、`menu`。将 `placeId`/`dataId` 传入 `/place` 和 `/reviews`。

## Google Maps Place

```python
params = {"placeId": "ChIJFU2bda4SM4cRKSCRyb6pOB8"}
```

返回完整的地点详情 —— 坐标、每日营业时间、电话、网站、热门时段、属性（外带、堂食）、照片摘要。

## Google Maps Reviews

```python
def reviews(place_id=None, data_id=None, sort_by="newestFirst", token=None):
    params = {}
    if place_id: params["placeId"] = place_id
    if data_id:  params["dataId"]  = data_id
    if sort_by:  params["sortBy"]  = sort_by
    if token:    params["nextPageToken"] = token
    return requests.get(
        "https://api.hasdata.com/scrape/google-maps/reviews",
        headers={"x-api-key": API_KEY},
        params=params, timeout=300,
    ).json()
```

| 参数 | 说明 |
|---|---|
| `placeId` / `dataId` | 二选一。`dataId` 是 Maps 结果中的十六进制对。 |
| `sortBy` | `newestFirst`、`highestRating`、`lowestRating`、`mostRelevant`。 |
| `topicId` | 按评价主题过滤。 |
| `nextPageToken` | 游标分页。 |

## Google Maps Posts

```python
resp = requests.get(
    "https://api.hasdata.com/scrape/google-maps/posts",
    headers={"x-api-key": API_KEY},
    params={"placeId": "ChIJ..."},      # or dataId="0x...:0x..."
    timeout=300,
)
for p in resp.json().get("posts", []):
    print(p["postedAt"], p["description"][:120], p.get("cta", {}).get("url"))
```

`placeId` **或** `dataId` 二者必填其一。可选参数：`hl`（界面语言）、`nextPageToken`（游标分页）。每次调用消耗 10 积分。

每条帖子的字段（实时验证）：`postId`、`locationId`、`title`、`description`、`image`、`cta`（`label` + `url`）、`createdAt`（ISO）、`postedAt`（人类可读）、`shareUrl`、`postUrl`。响应顶层：`posts`、`pagination`、`source`、`requestMetadata`。

帖子展示商家当前正在推广的优惠、节日营业时间、活动和产品发布。比抓取首页更便宜的信号源，且 `cta.url` 是规范的落地页。

## Yelp 与 YellowPages

```python
# Yelp
params = {"keyword": "McDonald's", "location": "New York, NY", "start": 0}  # steps of 10
# YellowPages
params = {"keyword": "Plumbers", "location": "New York, NY", "page": 1}
```

YellowPages 仅限美国 —— 在欧盟/亚太地区搜索将返回无效结果。

## 模式

### 通过邮件获取潜在客户（Maps + 网页抓取）

Maps 结果包含网站和电话，**但不包含邮箱**。结合网页抓取 API 的 `extractEmails`，仅用于公开商户联系页面、合法的外联以及遵守退订、隐私法规、速率和服务条款约束的工作流：

```python
leads = []
for biz in maps_results.get("localResults", []):
    site = biz.get("website")
    if not site: continue
    page = requests.post(
        "https://api.hasdata.com/scrape/web",
        headers={"x-api-key": API_KEY},
        json={"url": site, "extractEmails": True},
        timeout=300,
    ).json()
    leads.append({
        "name":    biz["title"],
        "phone":   biz.get("phone"),
        "website": site,
        "emails":  page.get("extractedEmails") or [],
    })
```

对于更高量级的需求，仅在您具有合法目的、合规的外联流程以及速率/退订控制时，才切换到 `contacts` Scraper Job（参见 `scraper-jobs.md`）。

### 新店发现

按评价数量 `< 5` 过滤 Maps 结果 —— 通常意味着新开业。

```python
new = [b for b in localResults if (b.get("reviews") or 0) < 5]
```

### 多门店连锁映射

搜索品牌名；每个 `localResults` 条目就是一家分店。

## 陷阱

- **`ll` 是视口，不是城市名称。** `@lat,lng,zoom`。直接粘贴"Brooklyn"会失败。
- **分页步长不同。** Maps `start` = +20，Yelp `start` = +10，Maps Reviews 使用 `nextPageToken`。
- **`placeId` vs `dataId`** —— Place 优先使用 `placeId`；Reviews 接受两者。
- **YellowPages 仅限美国。**