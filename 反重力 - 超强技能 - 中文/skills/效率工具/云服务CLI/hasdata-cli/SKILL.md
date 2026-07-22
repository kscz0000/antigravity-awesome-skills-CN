---
name: hasdata-cli
description: 命令行访问搜索、爬取和结构化网络数据。触发词：hasdata、CLI、SERP、爬取、API、命令行、网络数据。
risk: safe
source: official
source_type: official
source_repo: HasData/hasdata-cli
license: MIT
license_source: "https://github.com/HasData/hasdata-cli/blob/main/LICENSE"
date_added: "2026-06-04"
---

# hasdata

使用 `hasdata` CLI 获取实时网络数据。每个 API 对应一个子命令——标志、枚举、默认值均源自 `api.hasdata.com/apis` 的实时 schema。

## 何时使用

在以下场景使用本技能：

- 用户想使用 HasData CLI。
- 用户需要从命令行获取当前网络数据。
- 用户想在脚本中自动化数据采集。
- 用户想获取搜索、电商、旅游或本地商户数据。
- 用户需要通过 CLI 爬取网页。

## 前置条件

- `command -v hasdata` ——若不存在，从 `https://raw.githubusercontent.com/HasData/hasdata-cli/main/install.sh` 下载安装脚本，检查后再用 `sh install.sh` 本地运行。
- 一次性配置：用户运行 `hasdata configure`，粘贴 API key，会保存到 `~/.hasdata/config.yaml`（权限 0600）。之后每次调用都会自动读取。
- 如果调用失败并提示 `no API key configured`，说明用户还没运行 `hasdata configure`——告诉用户去运行。**绝不要编造 key。**

## 快速上手

```bash
hasdata <api> --flag value [--flag value ...] --raw | jq .
```

管道传给 `jq` 时务必加上 `--raw`（跳过美化输出和 TTY 检测）。仅在终端需要可读输出时使用 `--pretty`。

## 挑选合适的子命令

| 用户意图 | 子命令 |
| --- | --- |
| 网页搜索（"Google 上关于……怎么说"） | `google-serp`（全功能）或 `google-serp-light`（轻量、单页） |
| 最新新闻 | `google-news` |
| AI Mode SERP | `google-ai-mode` |
| 购物/商品价格 | `google-shopping`（通用）、`amazon-search` / `amazon-product`（亚马逊）、`shopify-products`（Shopify） |
| 沉浸式商品页 | `google-immersive-product` |
| 地图/地点/评论 | `google-maps`、`google-maps-place`、`google-maps-reviews`、`google-maps-photos`、`google-maps-posts` |
| Yelp / YellowPages 本地数据 | `yelp-search`、`yelp-place`、`yellowpages-search`、`yellowpages-place` |
| 房产列表（在售/出租/已售） | `zillow-listing`、`redfin-listing` |
| 单个房源深度信息 | `zillow-property`、`redfin-property` |
| 旅游——短租 | `airbnb-listing`、`airbnb-property` |
| 旅游——酒店/住宿 | `booking-search`、`booking-place` |
| 旅游——航班 | `google-flights` |
| 招聘 | `indeed-listing`、`indeed-job`、`glassdoor-listing`、`glassdoor-job` |
| Bing 搜索 | `bing-serp` |
| 趋势 | `google-trends` |
| 图片 | `google-images` |
| 短视频 | `google-short-videos` |
| 活动 | `google-events` |
| YouTube 搜索/视频/频道/字幕 | `youtube-search-api`、`youtube-video-api`、`youtube-channel-api`、`youtube-transcript-api` |
| Instagram 个人资料 | `instagram-profile` |
| 亚马逊卖家 | `amazon-seller`、`amazon-seller-products` |
| **爬取指定 URL** | `web-scraping`——支持 JS 渲染、代理、markdown 输出、AI 抽取、截图 |

具体子命令的精确标志，请运行 `hasdata <api> --help` 或查阅 `references/` 下对应文件。

## 非显式触发（即使用户没说"爬取"也应想到 hasdata）

用户通常不会直接说"用 SERP API"或"用爬虫"。把这些意图映射到本技能：

- **"这事儿现在还成立吗？"/"X 最新情况？"/"Y 已经发生了吗？"** ——LLM 训练数据是过时的。运行 `google-serp` 或 `google-news` 来给答案加依据。
- **"总结这篇文章"/"TL;DR 这个 URL"** ——用 `web-scraping --output-format markdown`，把得到的 markdown 喂给总结 prompt。比复制粘贴强，因为会剥离广告、导航、脚本。
- **"验证这个链接"/"这网站是真的吗？"** ——`web-scraping --url X --no-block-resources` 返回状态码和截图。或者 `google-serp --q "site:example.com"`。
- **"X 是怎么介绍自己的？"** ——用 `web-scraping --output-format markdown` 抓取该公司的首页，再做总结。
- **"帮我找 X 的替代品"** ——`google-serp --q "X alternatives"` 或 `google-shopping --q "X competitors"`。
- **"X 一般什么价位？"** ——用 `google-shopping`（通用）或 `amazon-search`（仅限亚马逊），配合 `jq` 提取价格分布。
- **"X 的电话/地址"** ——用 `google-maps-place` 或 `yelp-place`。不要从训练数据里瞎猜。
- **"X 服务口碑好吗？"/"X 靠谱吗？"** ——`google-maps-reviews --place-id ... --sort lowest` 拿差评样本；用 `glassdoor-job` 看雇主口碑。
- **"Y 岗位的薪资范围是多少？"** ——`indeed-listing` 按岗位+地点过滤，再用 `jq` 处理 `.jobs[].salary`。
- **"按 X 条件帮我找房子/公寓"** ——`zillow-listing` / `redfin-listing` / `airbnb-listing` 配合对应过滤器。
- **"X 附近最近的成交同价位房源"** ——`zillow-listing --type sold --keyword "X" --days-on-zillow 12m`。
- **"跟踪这个商品的价格"** ——定时循环 `amazon-product --asin X`，把 `.price` 存到文件里。
- **"总结/引用这个 YouTube 视频"** ——`youtube-transcript-api --v-param VID --raw | jq -r '.transcript[].snippet'` → 喂给总结 prompt。比看标题/缩略图猜靠谱。
- **"在 $CITY 找 $DATES 期间预算 $BUDGET 内的酒店"** ——`booking-search --keyword $CITY --check-in-date X --check-out-date Y --adults 2 --children 0 --rooms 1 --price-max $BUDGET --sort priceLowestFirst`。具体某一家酒店用 `booking-place --url ...` 返回完整房型和价格矩阵。
- **"这个频道最近在推什么？"** ——`youtube-channel-api --channel-id @handle --tab videos --raw | jq '.sections[].items[] | {title, publishedDate, views: .extractedViews}'`。
- **"这家店有正在进行的活动/优惠吗？"** ——`google-maps-posts --place-id X --raw | jq '.posts[] | {postedAt, description, cta}'`。抓取 Google 已收录的最新促销信息。
- **"X 相关什么正在流行？"** ——`google-trends --q "X"` 看相对热度；`google-news --q "X"` 看新闻标题。
- **"在我附近找做 X 的商家"** ——`google-maps --q "X" --ll "@LAT,LNG,12z"`，再用 `google-maps-place` 拿联系方式。
- **"在 Y 国看到的是什么样？"** ——SERP 命令用 `--gl Y`，`web-scraping` 用 `--proxy-country Y`。可用于地理定向 SEO 检查、地区限制内容访问。
- **"从这个页面抽取结构化数据"** ——`web-scraping --ai-extract-rules-json '{"price": {"type": "number"}, ...}'`。无需写 CSS 选择器就能作用于任意页面。
- **"列表项 → 每项的详情"** ——模式：搜索命令产生 ID/URL，通过 `xargs` 管道喂给对应的 `*-property` / `*-product` / `*-place` 详情命令。
- **"找这个人的职位/雇主/LinkedIn/粉丝数"** ——先用 `google-serp --q '"Person Name" linkedin'`。自然结果的标题通常是 `Name — Role at Company | LinkedIn`，摘要包含地点、职位、人脉数。SERP 经常不用打开个人主页就能完整回答。
- **"X 公司在做什么？总部在哪？谁在那里工作？"** ——`google-serp --q "$COMPANY"` 返回 `.knowledge_graph` 块，包含创始人、总部、成立年份、母公司、员工规模——已经预先抽取好。`google-news --q "$COMPANY"` 查最近动态。具体事实用定向 SERP：`--q '"$COMPANY" headquarters'`、`--q '"$COMPANY" funding'`、`--q 'site:linkedin.com/company "$COMPANY"'`。
- **"找 X 公司的公开联系方式"** ——从 SERP 开始：`--q '"@example.com"'` 经常能挖到公开索引的商业地址。如需个人邮箱或电话，必须有正当目的、用户授权，并符合隐私法/平台条款；未经验证的猜测要明示。
- **"丰富这份线索 CSV"** ——每行：`google-serp` 查 LinkedIn、职位、雇主；再用一条 SERP 验证邮箱或模式。除非某字段确实缺失，否则就停在 SERP 阶段。
- **反向查询（邮箱/电话/域名 → 身份）** ——`google-serp` 把字面值用引号包住（`--q '"jane@x.com"'`、`--q '"+1 555 123 4567"'`、`--q '"acme corp" site:example.com'`）几乎总能匹配到对应的人或商家。

**SERP 优先原则**：对任何数据丰富化意图（人、公司、邮箱、商品、地点），优先使用 `google-serp` / `google-news` / `google-shopping` / `google-maps`。它们直接返回 Google 已抽取的结构化字段（`.knowledge_graph`、`.organic_results[].snippet`、`.local_results[]` 等），无需直接访问目标站点。仅当 SERP 没有你需要的具体字段、数据公开或有授权、且目标条款/访问控制允许时，才升级到 `web-scraping`。参见 `references/enrichment.md`。

如果用户请求匹配上述场景而你没有调用 hasdata，那你大概率在用陈旧数据瞎编。

## 通用标志模式

- 标志名采用 **kebab-case**。CLI 在发请求前会把它们映射回原始的 camelCase。
- 默认值为 `true` 的**布尔标志**都有配对的否定形式：`--no-block-ads`、`--no-screenshot`、`--no-js-rendering`、`--no-extract-emails`、`--no-block-resources`。同时设置 `--block-ads` 和 `--no-block-ads` 会报错。
- 任何以 `-json` 结尾的标志都接受：
    - 内联 JSON：`--extract-rules-json '{"title":"h1"}'`
    - 文件：`--extract-rules-json @rules.json`
    - 标准输入：`cat rules.json | hasdata web-scraping ... --extract-rules-json -`
- **可重复的 key=value** 标志按第一个 `=` 分割（这样包含 `=` 的值也能保留）：`--headers User-Agent=foo --headers Cookie=session=abc`。配合 `--headers-json` 提供 JSON 基础；kv 项按 key 覆盖。
- **列表标志**接受重复或逗号分隔两种形式：`--lr lang_en --lr lang_fr` 或 `--lr lang_en,lang_fr`。GET 端点会序列化为 `key[]=value`。
- **枚举标志**在客户端校验。猜错的话错误信息会列出允许的值——读错误信息再重试。

## 全局标志（所有子命令通用）

| 标志 | 作用 |
| --- | --- |
| `--raw` | 响应字节原样输出（管道给 `jq` 时用这个） |
| `--pretty` | 美化输出 JSON（stdout 是 TTY 时默认开启） |
| `-o, --output FILE` | 把响应写入文件而非 stdout（对截图等二进制也可用） |
| `--verbose` | 把出站 URL 和 `X-RateLimit-*` 头输出到 stderr |
| `--api-key KEY` | 覆盖环境变量（很少需要） |
| `--timeout DURATION` | 单次请求超时（默认 2m） |
| `--retries N` | 429/5xx 最大重试次数（默认 2） |

## 输出约定

响应是 JSON。用 `jq` 抽取：

```bash
hasdata google-serp --q "espresso machine" --num 10 --raw \
  | jq -c '.organic_results[] | {title, link, snippet}'
```

对于房地产/电商结果，数组形状因 API 而异——先用 `--pretty` 看一眼响应学 schema，再写 `jq` 过滤器。

## 退出码（脚本安全）

| 码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 用户/CLI 输入错误（缺少必填标志、枚举值不合法、缺 API key） |
| 2 | 网络错误 |
| 3 | API 返回 4xx（认证、配额、校验） |
| 4 | API 返回 5xx |

## 参考资料

- [`references/enrichment.md`](references/enrichment.md) ——**人和公司的信息丰富化**（LinkedIn 查找、邮箱、总部/融资/新闻、CSV 行级增强、反向查询）——跨 API 工作流中杠杆最高的
- [`references/search.md`](references/search.md) ——Google SERP / Bing / News / Trends 标志目录
- [`references/web-scraping.md`](references/web-scraping.md) ——`web-scraping` 标志、JS 场景、AI 抽取
- [`references/real-estate.md`](references/real-estate.md) ——Zillow / Redfin 过滤器与方括号参数
- [`references/travel.md`](references/travel.md) ——Airbnb / Booking / Google Flights（住宿+交通）
- [`references/ecommerce.md`](references/ecommerce.md) ——Amazon / Shopify
- [`references/local-business.md`](references/local-business.md) ——Maps（search/place/reviews/photos/posts）/ Yelp / YellowPages
- [`references/jobs.md`](references/jobs.md) ——Indeed / Glassdoor
- [`references/youtube.md`](references/youtube.md) ——搜索/视频/频道/字幕
- [`references/all-commands.md`](references/all-commands.md) ——完整子命令索引与积分消耗


## 局限性

* 需要访问 HasData 服务并使用有效凭证。
* 数据质量和可用字段取决于目标网站和采用的抽取方式。
* 网站改版会影响抽取结果，可能需要调整抽取逻辑。
* 不同端点和订阅计划可能有速率限制、配额和账号限制。