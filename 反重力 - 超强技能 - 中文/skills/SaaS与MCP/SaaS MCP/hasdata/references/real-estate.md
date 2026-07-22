# 房地产 API —— Zillow、Redfin

| 端点 | 返回 |
|---|---|
| `/scrape/zillow/listing` | 按区域 + 过滤器的搜索结果 |
| `/scrape/zillow/property` | 单个房源（历史、经纪人、学校、税费） |
| `/scrape/redfin/listing` | Redfin 搜索结果 |
| `/scrape/redfin/property` | 单个 Redfin 房源 |

全部为同步 `GET`。每次 5 积分。

有关短租（Airbnb）、酒店（Booking）和机票，请参见 `travel.md`。

## Zillow Listing

过滤器参数使用**方括号**键名（`price[min]`、`beds[max]`）。

```python
import requests

def zillow_search(keyword, listing_type="forSale", **filters):
    r = requests.get(
        "https://api.hasdata.com/scrape/zillow/listing",
        headers={"x-api-key": API_KEY},
        params={"keyword": keyword, "type": listing_type, **filters},
        timeout=300,
    )
    return r.json()

zillow_search("Brooklyn, NY", price={"min": 800000, "max": 2000000})
zillow_search("33321", "sold", daysOnZillow="6m")  # recent comps
```

`requests` + `axios` 会自动将嵌套字典序列化为 `price[min]=…&price[max]=…`。若使用原生 `URLSearchParams`，需自行构造方括号键名。

| 参数 | 说明 |
|---|---|
| `keyword` | **必填。** 区域字符串（"New York, NY"、邮编、街区）。 |
| `type` | **必填。** `forSale`、`forRent`、`sold`。 |
| `price[min/max]`、`beds[min/max]`、`baths[min/max]`、`sqft[min/max]` | 范围过滤器。 |
| `daysOnZillow` | `24h`、`7d`、`14d`、`30d`、`90d`、`6m`、`12m`。 |
| `page` | 分页。 |

响应：`requestMetadata`、`searchInformation`、**`properties`**（房源数组 —— 而非 `listings`）、`pagination`。

## Zillow Property

```python
requests.get(
    "https://api.hasdata.com/scrape/zillow/property",
    headers={"x-api-key": API_KEY},
    params={"url": url, "extractAgentEmails": "true"},
    timeout=300,
)
```

接受完整的 Zillow URL（而非 zpid）。返回地址、地块/面积/卧室/浴室、价格与税费历史、学校、经纪人模块、照片。经纪人邮箱为尽力而为。

## Redfin

```python
# Listing
params = {"keyword": "33321", "type": "forSale", "page": 1}
# Property
params = {"url": "https://www.redfin.com/FL/Tamarac/9...html"}
```

与 Zillow 相同的方括号 `price[min]`、`beds[min]` 等。使用邮编作为 `keyword` 效果最好。

## 模式

### 用于 ROI 计算的成交可比

```python
sold = zillow_search(zip_code, "sold", daysOnZillow="6m").get("properties", [])
ppsf = [(l["price"] / l["livingArea"]) for l in sold if l.get("livingArea")]
```

## 陷阱

- **方括号查询键** —— 适用于 `requests`/`axios`，不适用于原生 `URLSearchParams`。
- **`type=sold` + `daysOnZillow` = 可比房源配方。** 没有 `daysOnZillow`，历史数据是无界的。
- **Property 端点接受 URL**，而非 ID。
- **经纪人邮箱是尽力而为。**