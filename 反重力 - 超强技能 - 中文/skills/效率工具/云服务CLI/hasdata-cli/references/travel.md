# 旅游参考

子命令：
- `airbnb-listing`、`airbnb-property`（各 5 积分）——短租。
- `booking-search`、`booking-place`（各 10 积分）——Booking.com 上的酒店和其他住宿。
- `google-flights`（15 积分）——通过 Google Flights 查机票价格和行程。

`*-listing` / `*-search` 是过滤搜索；`*-property` / `*-place` 是单个房源/酒店的深入查询。

目的地的活动用 `google-events`（在 `search.md`）；地面交通用 `web-scraping` 爬运营商站点。

---

## airbnb-listing

```bash
hasdata airbnb-listing --location "Lisbon, Portugal" \
  --check-in 2026-06-15 --check-out 2026-06-22 \
  --adults 2 --price-max 200 --raw
```

运行 `--help` 查看完整过滤器（房型、设施、即时预订等）。

## airbnb-property

```bash
hasdata airbnb-property --url "https://www.airbnb.com/rooms/12345678" --raw
```

## booking-search（10 积分）

```bash
hasdata booking-search \
  --keyword "Lisbon" \
  --check-in-date 2026-07-10 --check-out-date 2026-07-13 \
  --adults 2 --children 0 --rooms 1 \
  [--price-min 50 --price-max 250] [--rating 4 --rating 5] \
  [--review-score reviewScoreVeryGood --review-score reviewScoreSuperb] \
  [--property-type hotels --property-type apartments] \
  [--meals breakfastIncluded] [--facilities freeParking --facilities pool] \
  [--sort priceLowestFirst|ratingHighToLow|topReviewed|...] \
  [--page 2] [--currency USD] [--language en-us] \
  --raw | jq '.results[]'
```

必填（生产环境无默认值，即使 `--help` 显示有）：`--keyword`、`--check-in-date`、`--check-out-date`、`--adults`、`--children`、`--rooms`。没有小孩时显式传 `--children 0`。

当 `--children > 0` 时，**还要传 `--children-ages-json '[5,7]'`**，每个小孩一个年龄（0–17）。否则 Booking 会拒绝请求。

方括号价格过滤器（`--price-min` / `--price-max`）要求 `>= 10` / `>= 20`；按价格过滤时这两个至少要传一个。

顶层响应：`results`、`searchInformation`、`pagination`、`requestMetadata`。每条结果键（已实测）：`hotelId`、`roomId`、`title`、`url`、`location`、`rating`、`reviews`、`price`、`room`、`beds`、`bedTypes`、`policies`、`photo`。

```bash
# Cheap-first filtered search
hasdata booking-search --keyword "Paris" \
  --check-in-date 2026-08-01 --check-out-date 2026-08-04 \
  --adults 2 --children 0 --rooms 1 \
  --review-score reviewScoreVeryGood \
  --sort priceLowestFirst --raw \
  | jq -c '.results[] | {title, price: .price.total, rating, url}'
```

## booking-place（10 积分）

```bash
hasdata booking-place \
  --url "https://www.booking.com/hotel/fr/le-bristol-paris.html" \
  --check-in-date 2026-07-10 --check-out-date 2026-07-13 \
  --adults 2 --children 0 --rooms 1 \
  [--currency USD] [--language en-us] \
  --raw | jq .
```

必填：`--url`（必须在 `booking.com` / `www.booking.com` 上）、入住日期、`--adults`、`--children`、`--rooms`。

响应：`overview`、`bookingDetails`、`rooms[]`、`facilities`、`houseRules`、`ratings`、`reviews`、`restaurants`、`breadcrumbs`、`questionsAndAnswers`。`overview` 含 `id`、`title`、`address`、`description`、`propertyType`、`photos`、`highlights`、`mostPopularFacilities`。每个 `rooms[i]` 含 `roomId`、`name`、`bedTypes`、`beds`、`facilities`、`otherFacilities`、`variants[]`（每个套餐的价格/可订情况）。

## google-flights（15 积分）

```bash
hasdata google-flights \
  --departure-id "JFK" --arrival-id "LAX" \
  --outbound-date 2026-06-15 --return-date 2026-06-22 \
  --currency USD --raw | jq .
```

往返 vs 单程由是否传 `--return-date` 控制。运行 `--help` 查看完整标志集（舱位、限经停、偏好航司等）。

---

## 非显式用例

- **酒店 vs 民宿套利** ——同日期、同人数分别跑 `booking-search` 和 `airbnb-listing`；按分位数对比每晚成本。哪个平台便宜在不同城市不一定一样。
- **会场房价审计** ——在已知会议窗口 vs 空闲周用 `booking-search --keyword "$CITY" --check-in-date $START --check-out-date $END --sort priceHighestFirst`，差值就是会议溢价。
- **家庭友好过滤** ——`--children-ages-json '[5,9]' --children 2 --rooms 1 --travel-group family`，Booking 只会返回能容纳该人数且床型合适的房源。
- **忠诚计划组合** ——`booking-search --keyword "$CITY" --raw | jq '.results[] | select(.title | test("Marriott|Hilton|Hyatt"))'` 过滤出你有积分的连锁品牌。
- **Airbnb 价格套利检查** ——同日期、同区域，两次 `airbnb-listing` 用不同的 `--adults` 数量，挖出那些不按人头加价的房源。有时差价就是机会。
- **短租 vs 长租可行性** ——同区域用 `airbnb-listing` 取夜间价，配 `zillow-listing --type forSale`（见 `real-estate.md`）取买房价；客户端计算毛收益。
- **不用旅游 API 查航班** ——用 `google-flights` 加 `--departure-id`、`--arrival-id`、日期和 `--currency` 临时查价，对照 Skyscanner 等。
- **多段成本规划** ——串行 `google-flights` 调用查每段，把 `.best_flights[].price` 累加；一次性行程比 round-trip 价格机器人 SaaS 便宜。
- **行程成本预览** ——把 `google-flights`（交通）+ `booking-search` / `airbnb-listing`（住宿）+ `google-events`（活动，见 `search.md`）合成一份目的地报价，再决定要不要去。