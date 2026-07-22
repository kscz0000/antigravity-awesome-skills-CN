# 搜索与 SERP API

为 Google、AI 模式、Bing 以及专用的 Google 面板提供预解析 JSON。同步 `GET`，位于 `https://api.hasdata.com`。

| 端点 | 返回 |
|---|---|
| `/scrape/google/serp` | 完整 SERP —— 自然结果 + 每一个富摘要块 |
| `/scrape/google-light/serp` | 仅自然结果 |
| `/scrape/google/ai-mode` | Gemini 答案 + 引用 |
| `/scrape/google/ai-overview` | AI Overview 块 |
| `/scrape/google/news` | 新闻文章 |
| `/scrape/google/shopping` | 购物轮播 |
| `/scrape/google/images` | 图片搜索 |
| `/scrape/google/events` | 本地活动 |
| `/scrape/google/short-videos` | 短视频面板 |
| `/scrape/google/immersive-product` | 展开的商品弹窗 |
| `/scrape/google-trends/search` | Trends + 相关查询 |
| `/scrape/bing/serp` | Bing SERP |

有关 `/scrape/google/flights`，请参见 `travel.md`。

## Google SERP

```python
import requests

resp = requests.get(
    "https://api.hasdata.com/scrape/google/serp",
    headers={"x-api-key": API_KEY},
    params={"q": "coffee beans", "gl": "us", "hl": "en", "num": 100},
    timeout=300,
)
for hit in resp.json().get("organicResults", []):
    print(hit["position"], hit["title"], hit["link"])
```

### 查询参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `q` | — | **必填。** |
| `location` | — | 规范名称，如 `"Austin,Texas,United States"`。超本地化。 |
| `uule` | — | 预编码的位置（与 `location` 互斥）。 |
| `domain` | `google.com` | `google.co.uk`、`google.de` 等。 |
| `gl` | — | 2 字母国家代码（`us`、`de`、`jp`）。 |
| `hl` | — | 2 字母界面语言。 |
| `lr` | — | 内容语言过滤（`lang_en`）。 |
| `tbs` | — | 过滤器 —— `qdr:d|w|m|y` 用于时间范围，`li:1` 表示精确匹配，排序，图片类型。 |
| `safe` | — | `active` / `off`。 |
| `start` | `0` | 分页偏移量。 |
| `num` | `10` | 每页结果数。**最大 100** |
| `tbm` | — | `isch` 图片，`vid`，`nws`，`shop`，`lcl`。 |
| `deviceType` | — | `desktop`、`mobile`、`tablet`。 |

### 响应键

```
requestMetadata, searchInformation, organicResults, knowledgeGraph, answerBox,
aiOverview, topStories, newsResults, localResults, inlineShoppingResults,
inlineVideos, inlineImages, recipesResults, perspectives, discussionsAndForums,
relatedQuestions, relatedSearches, adResults, pagination
```

富摘要键**仅在 SERP 显示该块时出现** —— 始终使用 `data.get(key, default)`。

### 提示

- `gl`/`hl` 改变的是排名，而不仅仅是本地化。使用相同的 `q` 配合不同的 `gl` 来研究地理偏差。
- `location="Austin,Texas,United States"` 产生与单独使用 `gl=us` 不同的超本地化结果。

## Google Light SERP

与完整 SERP 参数相同，但响应被精简到少数几个键 —— 通常包括 `requestMetadata`、`searchInformation`、`organicResults`、`relatedSearches` 以及可能存在的 `pagination`。当您不需要更重的富摘要块时，可用于爬虫种子和链接发现。

## Google AI Mode

```python
resp = requests.get(
    "https://api.hasdata.com/scrape/google/ai-mode",
    headers={"x-api-key": API_KEY},
    params={"q": "is coffee good for health?", "location": "Austin,Texas,United States"},
    timeout=300,
)
```

参数：`q`（必填）、`location`、`uule`、`gl`。响应：

```json
{
  "requestMetadata": {...},
  "textBlocks": [
    {"type":"heading","snippet":"..."},
    {"type":"paragraph","snippet":"...","snippetHighlightedWords":["..."]},
    {"type":"list","list":[{"snippet":"..."}]},
    {"type":"table","table":{...}},
    {"type":"code","code":"..."}
  ],
  "references": [{"index":1,"link":"...","title":"...","snippet":"...","source":"..."}]
}
```

实践中观察到的块类型：`heading`、`paragraph`、`list`、`table`、`code`。始终基于 `type` 进行判断，而不要假设固定的集合。

模式：AI 模式获取答案 → 对每个 `references[].link` 调用 `/scrape/web`（markdown）→ 得到带引用的 RAG 上下文。

## Google News / Shopping / Bing

相同的结构：`q` + `gl`/`hl`/`location`。News 支持 `tbs=qdr:d|w|m|y` 指定时间窗口。Bing 返回与 Google SERP 相同的键集合 —— 可用于跨引擎达成共识（不一致 = 存在争议的话题）。

## 模式

### 分页

```python
def all_organic(q, target=300):
    out, start = [], 0
    while len(out) < target:
        page = requests.get(
            "https://api.hasdata.com/scrape/google-light/serp",
            headers={"x-api-key": API_KEY},
            params={"q": q, "num": 100, "start": start},
            timeout=300,
        ).json().get("organicResults", [])
        if not page:
            break
        out.extend(page)
        start += 100
    return out[:target]
```

### 反向查找（邮箱 / 电话 / 域名 → 身份）

```python
requests.get(
    "https://api.hasdata.com/scrape/google/serp",
    headers={"x-api-key": API_KEY},
    params={"q": f'"{literal}"', "num": 20},
    timeout=300,
).json().get("organicResults", [])
```

带引号的字面量（邮箱、电话、错误字符串）通常会呈现规范的提及位置。

### 索引检查

```python
def is_indexed(url):
    r = requests.get(
        "https://api.hasdata.com/scrape/google-light/serp",
        headers={"x-api-key": API_KEY},
        params={"q": f"site:{url}", "num": 1}, timeout=300,
    )
    return bool(r.json().get("organicResults"))
```