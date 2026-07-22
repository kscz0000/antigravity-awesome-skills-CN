# 房地产参考

子命令：`zillow-listing`、`zillow-property`、`redfin-listing`、`redfin-property`——各 5 积分。

短租（Airbnb）、酒店（Booking）和航班见 `travel.md`。

`*-listing` 用于过滤搜索；`*-property` 是单个房源的深入查询。

---

## zillow-listing

```bash
hasdata zillow-listing --keyword "Austin, TX" --type forSale [filters] --raw | jq '.results[]'
```

必填：
- `--keyword "City, ST"`（默认：`New York, NY`）
- `--type forSale|forRent|sold`（默认：`forSale`）

价格 / 面积（成对区间，保留为浮点）：
- `--price-min N --price-max N`
- `--beds-min N --beds-max N`
- `--baths-min N --baths-max N`
- `--square-feet-min N --square-feet-max N`
- `--lot-size-min N --lot-size-max N`
- `--year-built-min N --year-built-max N`
- `--hoa N` ——最高 HOA 费
- `--parking-spots-min N`

数组过滤器（枚举校验，小写 camelCase 值）：
- `--home-types house|townhome|multiFamily|condo|lot|apartment|manufactured`（可重复）
- `--pets allowsLargeDogs|allowsSmallDogs|allowsCats`（可重复）
- `--other-amenities ac|pool|waterfront|onsiteParking|inUnitLaundry|acceptZillowApplications|incomeRestricted|apartmentCommunity`（可重复）
- `--views city|mountain|park|water`（可重复）
- `--basement finished|unfinished`（可重复）
- `--property-status comingSoon|acceptingBackupOffers|pendingAndUnderContract`（可重复）
- `--listing-publish-options ownerPosted|agentListed|newConstruction|foreclosures|auctions|foreclosed|preForeclosures`（可重复）
- `--tours open|3d`（可重复）

布尔：
- `--must-have-garage` ——只要带车库的房源
- `--single-story-only`
- `--hide55plus-communities`

其他：
- `--listing-type byAgent|byOwner`
- `--days-on-zillow 1|7|14|30|90|6m|12m|24m|36m`
- `--keywords "open floor plan"` ——精炼关键词（在描述里匹配）
- `--move-in-date 2026-06-01`
- `--page N` ——分页
- `--sort verifiedSource|homesForYou|priceHighToLow|priceLowToHigh|paymentHighToLow|paymentLowToHigh|newest|bedrooms|bathrooms|squareFeet|lotSize`

### 示例

```bash
# Family home, mid-market, sorted cheapest first
hasdata zillow-listing \
  --keyword "Austin, TX" --type forSale \
  --price-min 400000 --price-max 900000 \
  --beds-min 3 --beds-max 5 --baths-min 2 \
  --home-types house --home-types townhome \
  --sort priceLowToHigh --raw | jq '.results[] | {address, price, beds, baths}'

# Pet-friendly rental
hasdata zillow-listing \
  --keyword "Seattle, WA" --type forRent \
  --price-max 4000 \
  --pets allowsSmallDogs --pets allowsCats \
  --parking-spots-min 1 --must-have-garage \
  --raw

# Recently sold comps
hasdata zillow-listing \
  --keyword "Miami, FL" --type sold \
  --square-feet-min 1500 --square-feet-max 4000 \
  --year-built-min 2000 --year-built-max 2020 \
  --days-on-zillow 12m --sort newest --raw
```

方括号查询参数（`price[max]`、`homeTypes[]`、`yearBuilt[min]`）由 CLI 处理——传上面展示的 kebab-case 标志，而不是原始 API 名字。

## zillow-property

```bash
hasdata zillow-property --url "https://www.zillow.com/homedetails/.../123_zpid/" --raw | jq .
```

也可以用 `--zpid <ID>`。返回完整房源详情（照片、历史、学校、税费、出行评分等）。

## redfin-listing

形态和 `zillow-listing` 类似，但 Redfin 的枚举不同。运行 `hasdata redfin-listing --help` 查看完整列表。常用模式：

```bash
hasdata redfin-listing --location "San Francisco, CA" --status forSale \
  --min-price 800000 --max-price 1500000 \
  --min-beds 2 --raw
```

## redfin-property

```bash
hasdata redfin-property --url "https://www.redfin.com/CA/San-Francisco/.../home/12345" --raw
```

---

## 非显式用例

- **投资筛选** ——组合 `--type sold` + `--days-on-zillow 12m` + `--year-built-min` + `--lot-size-min` 挖出 flip / 增值候选房源。再 `xargs` 喂给 `zillow-property` 做 ARV 分析。
- **房产税申诉可比房源** ——`--type sold --keyword "ZIP CODE" --days-on-zillow 12m` 过滤到与你家 beds/baths/sqft 同区间的近期成交，这是评估员用的。用 `jq -r '.results[] | [.address, .price, .beds, .baths, .squareFootage, .soldDate] | @csv'` 导出 CSV。
- **评估员拉成交** ——同一招，缩窄面积和同年代建成区间。
- **急售信号** ——`--type forSale --days-on-zillow 90` 返回挂了很久的房源，常常愿意谈价。
- **搬家前街区扫描** ——同一 `--type forRent` 过滤器跑 5–10 个街区，用 `jq '.results[].price'` 导出租金分布，看实地考察前的成本差异。
- **短租 vs 长租可行性** ——同区域用 `airbnb-listing`（见 `travel.md`）取夜间价，配 `zillow-listing --type forSale` 取买房价；客户端计算毛收益。
- **HOA 过滤** ——`--hoa N` 限制物业费上限；对月供上限有要求的买家有用。
- **学区导向找房** ——`zillow-property` 返回学校评分；遍历 `zillow-listing` 结果保留评分 ≥ X 的房源。
- **本周末开放日** ——Zillow 给开放日房源打标签；查 `.results[].openHouseTimes` 找即将到来的时段。
- **只看 3D 看房 / 虚拟看房** ——`--tours 3d` 只保留带虚拟看房的房源。适合异地/海外买家。
- **大量宠物友好租房** ——`--pets allowsLargeDogs --pets allowsCats` 适合多宠家庭。配合 `--keyword` 锁定具体街区。
- **法拍/预法拍线索** ——`--listing-publish-options foreclosures --listing-publish-options preForeclosures`。
- **非传统房源类型** ——`--listing-type byOwner` 找 FSBO；`--listing-type byAgent` 找经纪人挂牌（默认混合）。
- **入住日期约束** ——`--move-in-date YYYY-MM-DD` 用于租房搜索有硬性时间要求时。
- **批量地址验证** ——把一组房源 URL 管道给 `zillow-property` 确认可解析，并拉取 Zillow 用的标准地址。
- **验证 Redfin/Zillow 房源真实性** ——`redfin-property --url X --raw | jq .status` 确认它没被下架。