# 电商 API —— Amazon 与 Shopify

| 端点 | 返回 |
|---|---|
| `/scrape/amazon/product` | 单个商品（价格、评分、变体、其他卖家、A+） |
| `/scrape/amazon/search` | 搜索结果（推广 + 自然） |
| `/scrape/amazon/seller` | 卖家资料 |
| `/scrape/amazon/seller-products` | 卖家商品目录 |
| `/scrape/shopify/products` | 任意 Shopify 商店的商品 |
| `/scrape/shopify/collections` | 任意 Shopify 商店的商品集合 |

全部为同步 `GET`。

## Amazon Product

```python
import requests

resp = requests.get(
    "https://api.hasdata.com/scrape/amazon/product",
    headers={"x-api-key": API_KEY},
    params={"asin": "B0DHJ7SBDR", "domain": "www.amazon.com", "otherSellers": "true"},
    timeout=300,
)
```

| 参数 | 说明 |
|---|---|
| `asin` | **必填。** |
| `domain` | `www.amazon.com`（默认）、`.co.uk`、`.de`、`.co.jp` 等。 |
| `language` | 每个 domain 对应的语言环境。 |
| `deliveryZip` | 影响配送与可用性字段。 |
| `shippingLocation` | 2 字母国家代码。 |
| `otherSellers` | `true`（默认）以包含其他卖家模块。 |

响应：顶层 `requestMetadata` + `product`。`product` 对象的键（实时验证）：`asin`、`url`、`title`、`brand`、`isAvailable`、`primaryFeatures`、`features`、`featureBullets`、`description`、`badges`、`breadcrumbs`、`whatIsInTheBox`、`variants`、`totalImages`、`primaryImage`、`images`、`descriptionImages`、`totalVideos`、`primaryVideo`、`videos`、`specification`、`reviewsInfo`（评分 + 数量 + 示例评论在此处，不在根级别）。价格字段通过 `variants` 和 `specification` 提供。

## Amazon Search

```python
params = {"q": "mechanical keyboard", "domain": "www.amazon.com", "page": 1}
```

参数：`q`（必填）、`domain`、`language`、`page`、`deliveryZip`、`shippingLocation`、`sortBy`。

## Amazon Seller / Seller Products

```python
profile = requests.get(
    "https://api.hasdata.com/scrape/amazon/seller",
    headers={"x-api-key": API_KEY},
    params={"sellerId": "A1MNOPQR", "domain": "www.amazon.com"},
    timeout=300,
).json()

catalog = requests.get(
    "https://api.hasdata.com/scrape/amazon/seller-products",
    headers={"x-api-key": API_KEY},
    params={"sellerId": "A1MNOPQR", "page": 1},
    timeout=300,
).json()
```

使用场景：假货检测、MAP 价格合规、竞品目录镜像。

## Shopify Products

适用于**任何** Shopify 店面，无需身份认证。

```python
def shopify_all(store_url):
    page, out = 1, []
    while True:
        batch = requests.get(
            "https://api.hasdata.com/scrape/shopify/products",
            headers={"x-api-key": API_KEY},
            params={"url": store_url, "page": page, "limit": 250},
            timeout=300,
        ).json().get("products", [])
        if not batch:
            return out
        out.extend(batch)
        page += 1
```

| 参数 | 说明 |
|---|---|
| `url` | **必填。** 店面 URL。 |
| `limit` | 1–250，默认 `1`。目录工作时**调到 250**。 |
| `page` | 从 1 开始计数。 |
| `collection` | 商品集合 handle 过滤器。 |

`/scrape/shopify/collections` 具有相同的结构，返回商品集合列表。

## 模式

### 跨商家价格比较

```python
a = requests.get("https://api.hasdata.com/scrape/amazon/search",
                 headers={"x-api-key": API_KEY},
                 params={"q": query}, timeout=300).json()
g = requests.get("https://api.hasdata.com/scrape/google/shopping",
                 headers={"x-api-key": API_KEY},
                 params={"q": query, "gl": "us"}, timeout=300).json()
```

### 评价与畅销榜通过 Scraper Jobs 处理

Product API 仅包含部分评价。如需全部评价，请使用 `amazon-product-reviews` Scraper Job。如需畅销榜排名，请使用 `amazon-bestsellers` —— 没有对应的同步 API。参见 `scraper-jobs.md`。

## 陷阱

- **相同的 ASIN 在不同 `domain` 下并非同一商品。** `.com` 与 `.co.uk` 可能不同。
- **`deliveryZip` 会改变可用性。** 当库存重要时传入；若只抓规格则可省略。
- **Shopify `limit` 默认值为 1** —— 进行目录抓取时务必设为 250。