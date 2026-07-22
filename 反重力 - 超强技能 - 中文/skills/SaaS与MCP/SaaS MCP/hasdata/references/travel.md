# 旅游 API —— Airbnb、Booking、Google Flights

| 端点 | 返回 |
|---|---|
| `/scrape/airbnb/listing` | Airbnb 搜索结果 |
| `/scrape/airbnb/property` | 单个 Airbnb 房源 |
| `/scrape/booking/search` | Booking.com 搜索结果（酒店、公寓） |
| `/scrape/booking/place` | 单个 Booking.com 物业，含房间/房价列表 |
| `/scrape/google/flights` | Google Flights 价格与行程 |

全部为同步 `GET`。Airbnb 5 积分；Booking 10 积分；Google Flights 15 积分。

有关目的地的活动，请参见 `/scrape/google/events`（位于 `search.md`）；有关地面交通，请使用 `POST /scrape/web` 抓取运营商网站。

## Airbnb

```python
import requests

def airbnb_search(location, check_in, check_out, **kwargs):
    return requests.get(
        "https://api.hasdata.com/scrape/airbnb/listing",
        headers={"x-api-key": API_KEY},
        params={"location": location, "checkIn": check_in, "checkOut": check_out, **kwargs},
        timeout=300,
    ).json()
```

| 参数 | 说明 |
|---|---|
| `location` | **必填。** 自由格式。 |
| `checkIn` | **必填。** `YYYY-MM-DD`。 |
| `checkOut`、`adults`、`children`、`infants`、`pets` | 可选。 |
| `nextPageToken` | 分页游标。 |

### Token 分页

```python
def airbnb_all(location, check_in, check_out):
    out, token = [], None
    while True:
        page = airbnb_search(location, check_in, check_out,
                             **({"nextPageToken": token} if token else {}))
        out.extend(page.get("listings", []))
        token = page.get("nextPageToken")
        if not token:
            return out
```

### Airbnb Property

```python
requests.get(
    "https://api.hasdata.com/scrape/airbnb/property",
    headers={"x-api-key": API_KEY},
    params={"url": "https://www.airbnb.com/rooms/12345678"},
    timeout=300,
)
```

## Booking Search

```python
import json, requests

def booking_search(keyword, check_in, check_out, *, adults=2, children=0,
                   children_ages=None, rooms=1, **filters):
    params = {
        "keyword":      keyword,
        "checkInDate":  check_in,
        "checkOutDate": check_out,
        "adults":       adults,
        "children":     children,
        "rooms":        rooms,
        **filters,
    }
    if children and children_ages:
        params["childrenAgesJson"] = json.dumps(children_ages)
    return requests.get(
        "https://api.hasdata.com/scrape/booking/search",
        headers={"x-api-key": API_KEY},
        params=params, timeout=300,
    ).json()
```

| 参数 | 说明 |
|---|---|
| `keyword` | **必填。** 城市、街区或物业名称。 |
| `checkInDate` / `checkOutDate` | **必填。** `YYYY-MM-DD`。 |
| `adults`、`children`、`rooms` | **必填。** 没有儿童时也需显式传入 `children=0`。 |
| `childrenAgesJson` | 当且仅当 `children > 0` 时必填 —— 年龄的 JSON 数组（0–17），每位儿童一个。 |
| `price[min]` / `price[max]` | `>= 10` / `>= 20`。方括号 —— `requests`/`axios` 会将嵌套字典序列化为 `price[min]=…`。 |
| `rating[]`、`reviewScore[]`、`propertyType[]`、`facilities[]`、`meals[]`、`bedPreference[]`、`roomFacilities[]`、`propertyAccessibility[]`、`roomAccessibility[]`、`distanceFromCenter[]`、`travelGroup[]`、`onlinePayment[]`、`reservationPolicy[]` | 多值过滤器（OR）。 |
| `bedrooms`、`bathrooms` | 最小数量。 |
| `sort` | `ourTopPicks`、`homesAndApartmentsFirst`、`priceLowestFirst`、`priceHighestFirst`、`bestReviewedAndLowestPrice`、`ratingHighToLow`、`ratingLowToHigh`、`ratingAndPrice`、`distanceFromDowntown`、`topReviewed`。 |
| `page` | 从 1 开始，每页 25 条结果。 |
| `currency` | ISO 代码或 `hotelCurrency` 以保持原币种。 |
| `language` | 界面语言环境。 |

顶层响应（实时验证）：`requestMetadata`、`searchInformation`、`pagination`、`results`。每个结果的键：`hotelId`、`roomId`、`title`、`url`、`location`、`rating`、`reviews`、`price`（含 `total` / `nightly` / `currency` 的对象）、`room`、`beds`、`bedTypes`、`policies`、`photo`。

## Booking Place

```python
resp = requests.get(
    "https://api.hasdata.com/scrape/booking/place",
    headers={"x-api-key": API_KEY},
    params={
        "url":           "https://www.booking.com/hotel/fr/le-bristol-paris.html",
        "checkInDate":   "2026-07-10",
        "checkOutDate":  "2026-07-13",
        "adults":         2,
        "children":       0,
        "rooms":          1,
    },
    timeout=300,
).json()
```

`url` 必须是 `booking.com` / `www.booking.com`。其余入住/客人参数与 `booking-search` 共享相同规则（包括 `children > 0` 时的 `childrenAgesJson`）。

响应顶层键：`requestMetadata`、`overview`、`bookingDetails`、`rooms`、`facilities`、`houseRules`、`ratings`、`reviews`、`restaurants`、`breadcrumbs`、`questionsAndAnswers`。

- `overview` → `id`、`title`、`address`、`description`、`propertyType`、`photos`、`highlights`、`mostPopularFacilities`。
- `rooms[i]` → `roomId`、`name`、`bedTypes`、`beds`、`facilities`、`otherFacilities`、`variants[]`（每个变体包含价格与可订状态）。变体是实际可购买的单元；`rooms[i]` 是户型平面图。

## Google Flights

```python
resp = requests.get(
    "https://api.hasdata.com/scrape/google/flights",
    headers={"x-api-key": API_KEY},
    params={
        "departureId":  "JFK",
        "arrivalId":    "LAX",
        "outboundDate": "2026-06-15",
        "returnDate":   "2026-06-22",     # omit for one-way
        "currency":     "USD",
    },
    timeout=300,
).json()
```

| 参数 | 说明 |
|---|---|
| `departureId` / `arrivalId` | **必填。** IATA 机场代码（`JFK`、`LAX`）。 |
| `outboundDate` | **必填。** `YYYY-MM-DD`。 |
| `returnDate` | 可选 —— 单程时省略。 |
| `currency` | ISO 代码。 |
| `gl`、`hl` | 国家 / 语言。 |
| `travelClass` | `1` 经济舱，`2` 超经舱，`3` 商务舱，`4` 头等舱。 |
| `stops` | `0` 任意，`1` 直飞，`2` ≤1 次中转，`3` ≤2 次中转。 |
| `adults`、`children`、`infantsInSeat`、`infantsOnLap` | 乘客数量。 |

## 模式

### 短租房收益率估算

```python
rentals = airbnb_search(area, ci, co).get("listings", [])           # Airbnb → "listings"
# pair with /scrape/zillow/listing (see real-estate.md) for purchase price
night   = sum(r.get("price", 0) for r in rentals) / max(len(rentals), 1)
```

### 酒店与短租房价差

```python
b = booking_search(city, ci, co, adults=2, children=0, rooms=1, sort="priceLowestFirst")
a = airbnb_search(city, ci, co, adults=2)
def median(xs): xs = sorted(xs); return xs[len(xs)//2] if xs else None
median_hotel = median([r["price"]["nightly"] for r in b.get("results", []) if r.get("price")])
median_str   = median([r["price"]            for r in a.get("listings", []) if r.get("price")])
```

### 全程旅行总费用

```python
flight = requests.get(
    "https://api.hasdata.com/scrape/google/flights",
    headers={"x-api-key": API_KEY},
    params={"departureId": origin, "arrivalId": dest_iata,
            "outboundDate": dep, "returnDate": ret, "currency": "USD"},
    timeout=300,
).json()
cheapest_flight = min((f["price"] for f in flight.get("best_flights", [])), default=None)

stay = booking_search(city, dep, ret, adults=2, children=0, rooms=1, sort="priceLowestFirst")
cheapest_stay = stay.get("results", [{}])[0].get("price", {}).get("total")

total = (cheapest_flight or 0) + (cheapest_stay or 0)
```

## 陷阱

- **Airbnb 需要 `checkIn`**，并使用 **token** 分页 —— 存储 `nextPageToken`，而不是页码。
- **Airbnb property 端点接受 URL**，而非 ID。
- **Booking 即使在没有儿童时也要求传入 `children`。** 传入 `children=0`。当 `children > 0` 时，还需传入恰好包含相应数量年龄的 `childrenAgesJson`。
- **Booking `price[min]` / `price[max]`** 是方括号 —— 在 `requests`/`axios` 中使用嵌套字典。
- **Booking `rooms[i].variants[]` 才是价格所在** —— 父级 `rooms[i]` 描述户型，variants 是带 `priceBreakdown` / `cancellationPolicy` / `mealPlan` 的可购买房价。
- **`bookingDetails` 携带已解析的入住上下文** —— 在持久化结果时回传它，以便后续比较使用相同的日期 / 入住人数。
- **Google Flights 使用 IATA 代码**，而非城市名。`JFK` 而非 `New York`。
- **往返 / 单程** 由 `returnDate` 是否存在决定 —— 往返传入，单程省略。