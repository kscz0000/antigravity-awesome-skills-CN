# 本地商户 / 地图参考

子命令：`google-maps`、`google-maps-place`、`google-maps-reviews`、`google-maps-contributor-reviews`、`google-maps-photos`、`google-maps-posts`、`yelp-search`、`yelp-place`、`yellowpages-search`、`yellowpages-place`。每个 5 积分（`google-maps-posts` 和 YellowPages 是 10 积分）。

---

## google-maps

```bash
hasdata google-maps --q "coffee" --ll "@30.2672,-97.7431,14z" --raw | jq '.local_results[]'
```

必填：`--q TEXT`。其他常用标志：
- `--ll "@LAT,LNG,ZOOMz"` ——中心点和缩放（Google 的 `ll` 参数）
- `--gl us|gb|...` ——国家
- `--hl en|es|...` ——语言
- `--type search|place` ——搜索或特定地点查询
- `--data` / `--cid` / `--fid` ——Google 标识（高级）

每条结果：`title`、`place_id`、`rating`、`reviews`、`address`、`phone`、`website`、`types[]`、`gps_coordinates`。

## google-maps-place

```bash
hasdata google-maps-place --place-id "ChIJ..." --raw | jq .
```

单个地点：完整详情、营业时间、人流高峰时段、属性。

## google-maps-reviews

```bash
hasdata google-maps-reviews --place-id "ChIJ..." [--sort newest|highest|lowest] --raw \
  | jq '.reviews[] | {author, rating, date, snippet}'
```

分页：响应里包含 `next_page_token`——通过 `--next-page-token` 传入。

## google-maps-contributor-reviews

按 `--contributor-id` 查特定 Google 贡献者写的评论。适用于本地向导分析。

## google-maps-photos

```bash
hasdata google-maps-photos --place-id "ChIJ..." --raw
```

按类别返回照片 URL（室内、室外、菜品等）。

## google-maps-posts（10 积分）

```bash
hasdata google-maps-posts --place-id "ChIJ..." [--hl en] [--next-page-token TOKEN] --raw \
  | jq '.posts[] | {postedAt, description, cta, postUrl}'
```

posts 是 Maps 商家页面上由商家自己发布的帖子：优惠、活动、节假日营业时间、公告。`--place-id` **或** `--data-id` 必填其一。

每条 post 字段（已实测）：`postId`、`locationId`、`title`、`description`、`image`、`cta`（含 `label` + `url`）、`createdAt`（ISO）、`postedAt`（人类可读）、`shareUrl`、`postUrl`。更早的帖子用 `pagination.nextPageToken`。

---

## yelp-search

```bash
hasdata yelp-search --query "italian" --location "Brooklyn, NY" [--page 1] --raw \
  | jq '.businesses[] | {name, rating, review_count, price, categories}'
```

## yelp-place

```bash
hasdata yelp-place --url "https://www.yelp.com/biz/SLUG" --raw | jq .
```

单个商户：完整详情、营业时间、热门评论、照片、属性。

## yellowpages-search

```bash
hasdata yellowpages-search --search-terms "plumber" --geo-location-terms "Atlanta, GA" --raw
```

## yellowpages-place

```bash
hasdata yellowpages-place --url "https://www.yellowpages.com/atlanta-ga/mip/..." --raw
```

---

## 非显式用例

- **销售线索研究** ——`google-maps --q "INDUSTRY" --ll "@LAT,LNG,12z"` 枚举商户，再 `xargs` 喂给 `google-maps-place` 拿公开电话/网站。收集邮箱仅用于正当的商业外联，并遵守退出订阅、隐私法和速率限制。
- **口碑监控** ——`google-maps-reviews --place-id X --sort lowest` 把最差评论排前；能快速发现危机信号。每周跑一次，捕获新增的 1 星差评。
- **"这家店还开着吗？"** ——`google-maps-place --place-id X --raw | jq '.hours'` 看当前营业时间；也会给出 `permanently_closed` 状态。
- **验证用户给的地址** ——`google-maps --q "BUSINESS NAME, CITY" --raw | jq '.local_results[0].address'`。高风险动作（寄件、付款）不要轻信用户提供的地址。
- **公开商户联系方式查询** ——`google-maps-place` 包含电话和网站；`web-scraping --url WEBSITE --extract-emails` 从首页解析邮箱。仅用于公开商户联系方式，并注明不确定性。
- **竞争密度地图** ——在不同缩放级别跑 `google-maps --q "coffee shop" --ll "@LAT,LNG,Zz"`；把 `.local_results[]` 聚合到带地址+评分的 CSV，找出供给不足的区域。
- **服务范围验证** ——用 `yelp-search --location "CITY"` 跨几个城市串起来验证同名商家是否覆盖。
- **找最近开业的商户** ——`google-maps-place` 返回 `description.years_in_business` 和 posts/更新时间戳；按时间排。
- **差评样本用于产品分析** ——`yelp-place --url X --raw | jq '.reviews[] | select(.rating <= 2)'`；可作为"客户都在抱怨什么"摘要的输入。
- **可视化素材用的图片挖掘** ——`google-maps-photos --place-id X` 返回分类图片 URL（室内、菜品、外景）。当用户要图又不依赖 `google-images` 时很有用。
- **本地向导可信度** ——`google-maps-contributor-reviews --contributor-id X` 展示某位评论者写过的全部内容，可用于过滤水军/可疑账号。
- **YellowPages 用于 B2B 细分** ——服务类商户（水管工、电工、律师）通常 YellowPages 索引比 Yelp 更好；一边搜不到时两边都试。
- **跨平台口碑差异** ——同商户名+城市分别用 `yelp-search` 和 `google-maps` 查，比较评分差异（差距大往往意味着某一边有刷评）。
- **促销/活动监控** ——`google-maps-posts --place-id X` 抓取当前优惠、节假日营业时间和限时活动。信号比爬官网便宜，且 `cta.url` 通常指向官方落地页。
- **识别即将重开/换牌的商户** ——沉寂多月突然爆发新 `google-maps-posts` 通常预示重新开业或换老板。

## 常见模式

```bash
# Build a directory: search → fan out to per-place details
hasdata google-maps --q "yoga studios" --ll "@30.27,-97.74,12z" --raw \
  | jq -r '.local_results[].place_id' \
  | head -10 \
  | xargs -I{} hasdata google-maps-place --place-id {} --raw

# Sentiment / review analysis
hasdata google-maps-reviews --place-id "$PID" --sort lowest --raw \
  | jq '.reviews[] | {rating, snippet}'
```