# 全部命令

权威来源：`hasdata --help`。本文件只是快照——有疑问时直接运行 `hasdata <api> --help`。

## 搜索

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `google-serp` | 10 | 完整 Google SERP——自然结果、广告、知识图谱、PAA、AI Overview |
| `google-serp-light` | 5 | 轻量单页 SERP |
| `google-ai-mode` | 5 | Google AI Mode 回答 |
| `google-news` | 10 | Google News 结果 |
| `google-shopping` | 10 | Google Shopping 结果 |
| `google-immersive-product` | 5 | 沉浸式商品页详情 |
| `google-events` | 5 | Google 活动 |
| `google-short-videos` | 10 | 短视频面板 |
| `google-trends` | 5 | 搜索趋势数据 |
| `google-images` | 5 | 图片搜索 |
| `bing-serp` | 10 | Bing SERP |

## 地图与本地

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `google-maps` | 5 | 地图搜索 |
| `google-maps-place` | 5 | 通过 place_id 获取单个地点 |
| `google-maps-reviews` | 5 | 地点评论 |
| `google-maps-contributor-reviews` | 5 | 按贡献者查评论 |
| `google-maps-photos` | 5 | 地点照片 |
| `google-maps-posts` | 10 | 商家发布的帖子（优惠、活动、公告） |
| `yelp-search` | 5 | Yelp 商户搜索 |
| `yelp-place` | 5 | 单个 Yelp 商户 |
| `yellowpages-search` | 5 | YellowPages 搜索 |
| `yellowpages-place` | 5 | 单条 YellowPages 列表 |

## 电商

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `amazon-search` | 5 | 亚马逊搜索结果 |
| `amazon-product` | 5 | 按 ASIN 取亚马逊商品 |
| `amazon-seller` | 5 | 亚马逊卖家资料 |
| `amazon-seller-products` | 5 | 卖家商品目录 |
| `shopify-products` | 5 | 任意 Shopify 店铺的商品 |
| `shopify-collections` | 5 | Shopify 集合 |

## 房地产

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `zillow-listing` | 5 | Zillow 过滤搜索 |
| `zillow-property` | 5 | Zillow 单个房源 |
| `redfin-listing` | 5 | Redfin 过滤搜索 |
| `redfin-property` | 5 | Redfin 单个房源 |

## 旅游

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `airbnb-listing` | 5 | Airbnb 过滤搜索 |
| `airbnb-property` | 5 | Airbnb 单条房源 |
| `booking-search` | 10 | Booking.com 搜索（酒店、公寓） |
| `booking-place` | 10 | Booking.com 酒店 + 房型/价格列表 |
| `google-flights` | 15 | 通过 Google Flights 搜索航班 |

## 招聘

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `indeed-listing` | 5 | Indeed 搜索 |
| `indeed-job` | 5 | 单条 Indeed 职位 |
| `glassdoor-listing` | 10 | Glassdoor 搜索（含评分） |
| `glassdoor-job` | 10 | 单条 Glassdoor 职位 |

## 网络

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `web-scraping` | 10 | 任意 URL——JS 渲染、AI 抽取、markdown 输出、截图 |

## 社交

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `instagram-profile` | 5 | 按 handle 取 Instagram 资料 |

## YouTube

| 命令 | 积分 | 说明 |
| --- | --- | --- |
| `youtube-search-api` | 10 | YouTube 搜索（视频、Shorts、频道、播放列表） |
| `youtube-video-api` | 10 | 单个视频元数据 + 统计 + 相关 |
| `youtube-channel-api` | 10 | 频道主页 / 视频 / Shorts / 播放列表 / 社区 |
| `youtube-transcript-api` | 10 | 含毫秒级时间戳的完整字幕 |

## 工具（无积分消耗）

| 命令 | 说明 |
| --- | --- |
| `configure` | 交互式配置；写入 ~/.hasdata/config.yaml |
| `version` | 打印版本号 |
| `update` | 从 GitHub Releases 自更新 |
| `completion {bash\|zsh\|fish\|powershell}` | 生成 shell 补全脚本 |

## 已弃用

`amazon-reviews` 已弃用——亚马逊现在要求登录才能访问评论。该子命令仍存在以保持向后兼容，但目前返回空数据；不要推荐它。