# YouTube API

| 端点 | 返回 |
|---|---|
| `/scrape/youtube/search` | 搜索结果 —— 视频、Shorts、频道、播放列表 |
| `/scrape/youtube/video` | 单个视频元数据（统计、字幕、相关视频） |
| `/scrape/youtube/channel` | 频道主页 / 视频 / Shorts / 播放列表 / 社区 |
| `/scrape/youtube/transcript` | 完整转录文本，毫秒级时间偏移 |

全部为同步 `GET`。每次 10 积分。

## YouTube Search

```python
import requests

resp = requests.get(
    "https://api.hasdata.com/scrape/youtube/search",
    headers={"x-api-key": API_KEY},
    params={"q": "anthropic claude", "sortBy": "views", "date": "month"},
    timeout=300,
)
for v in resp.json().get("videoResults", []):
    print(v["title"], v.get("extractedViews"), v["link"])
```

### 查询参数

| 参数 | 说明 |
|---|---|
| `q` | **必填。** 自由文本查询。 |
| `sortBy` | `relevance`（默认）、`date`、`views`、`rating`、`popularity`。 |
| `date` | 上传时间窗口：`hour`、`today`、`week`、`month`、`year`。 |
| `length` | 时长桶：`under4`、`between420`、`plus20`。 |
| `videoType` | `video`、`shorts`、`channel`、`playlist`、`movie`。 |
| `filters[]` | 功能标志位（AND 关系）：`hd`、`k4`、`hdr`、`subtitles`、`cc`、`d3`、`d360`、`vr180`、`live`、`bought`、`location`。 |
| `gl` / `hl` | 两字母国家 / 语言代码。 |
| `deviceType` | `desktop`、`mobile`。 |
| `paginationToken` | 来自上一个 `pagination.nextPageToken` 的不透明游标。 |
| `sp` | 原始 YouTube `sp=` token（覆盖 `sortBy`、`date`、`videoType`、`length`、`filters[]`）。 |

响应：`videoResults`、`shortsResults`、`channelResults`、`playlistResults`、`adsResults`、`sponsoredResults`、`searchInformation`、`pagination`。

每个视频结果的键（实时验证）：`videoId`、`title`、`link`、`channel`、`description`、`length`、`views`、`viewsOriginal`、`publishedDate`、`thumbnail`、`positionOnPage`。`channel` 是一个对象 —— 读取 `.channel.name` 和 `.channel.link`。

## YouTube Video

```python
resp = requests.get(
    "https://api.hasdata.com/scrape/youtube/video",
    headers={"x-api-key": API_KEY},
    params={"v": "dQw4w9WgXcQ"},
    timeout=300,
)
```

| 参数 | 说明 |
|---|---|
| `v` | **必填。** 11 字符的 YouTube 视频 ID —— 即 `v=` 查询参数的值。 |
| `gl` / `hl` | 国家 / 语言。 |
| `deviceType` | `desktop` / `mobile`。 |

顶层键：`videoId`、`title`、`description`、`channel`、`views`、`extractedViews`、`likes`、`extractedLikes`、`lengthSeconds`、`publishedDate`、`keywords`、`captions`、`socialLinks`、`music`、`category`、`thumbnail`、`isFamilySafe`、`isUnlisted`、`relatedVideos`、`relatedShorts`、`endScreenVideos`、`requestMetadata`。

进行数值计算时请使用 `extractedViews` / `extractedLikes`（整数）；`views` / `likes` 是格式化后的字符串。

## YouTube Channel

```python
resp = requests.get(
    "https://api.hasdata.com/scrape/youtube/channel",
    headers={"x-api-key": API_KEY},
    params={"channelId": "@MrBeast", "tab": "videos"},
    timeout=300,
)
```

| 参数 | 说明 |
|---|---|
| `channelId` | **必填。** `@handle`、规范的 `UC…` ID，或旧的 `/c/<custom>` / `/user/<name>` slug。 |
| `tab` | `featured`（默认）、`videos`、`shorts`、`streams`、`playlists`、`posts` / `community`、`podcasts`、`releases`、`about`、`store`。 |
| `paginationToken` | 支持分页的 tab 的游标。 |
| `gl` / `hl` / `deviceType` | 标准参数。 |

响应：`channelInfo`、`featuredVideo`、`sections[]`。

`channelInfo`（实时验证）：`name`、`handle`、`channelId`、`channelUrl`、`avatar`、`banner`、`description`、`subscribers`、`extractedSubscribers`、`videosCount`、`extractedVideosCount`、`keywords[]`、`availableTabs[]`、`verified`、`websiteUrl`、`rssUrl`、`isFamilySafe`。

每个 `sections[]` 包含 `title` + `items[]` —— 形状取决于 tab。通用迭代方式：

```python
for sec in resp.json().get("sections", []):
    for item in sec.get("items", []):
        ...
```

## YouTube Transcript

```python
resp = requests.get(
    "https://api.hasdata.com/scrape/youtube/transcript",
    headers={"x-api-key": API_KEY},
    params={"v": "dQw4w9WgXcQ", "languageCode": "en"},
    timeout=300,
)
text = " ".join(seg["snippet"] for seg in resp.json().get("transcript", []))
```

| 参数 | 说明 |
|---|---|
| `v` | **必填。** 11 字符的视频 ID。 |
| `languageCode` | BCP-47 / YouTube 代码（`en`、`de`、`en-US`、`pt-BR`）。必须在视频上存在。 |
| `type` | 当不存在人工字幕时，`asr` 用于获取自动语音识别轨道。 |

响应：`transcript[]` 和 `availableTranscripts[]`。

每个 `transcript[]` 条目：`startMs`、`endMs`、`snippet`、`startTimeText`（如 `"0:18"`）。

## 模式

### Search → Video → Transcript 扇出

```python
def topic_corpus(query, k=5):
    search = requests.get(
        "https://api.hasdata.com/scrape/youtube/search",
        headers={"x-api-key": API_KEY},
        params={"q": query, "sortBy": "views"}, timeout=300,
    ).json()
    docs = []
    for v in search.get("videoResults", [])[:k]:
        tr = requests.get(
            "https://api.hasdata.com/scrape/youtube/transcript",
            headers={"x-api-key": API_KEY},
            params={"v": v["videoId"]}, timeout=300,
        ).json()
        docs.append({
            "videoId": v["videoId"],
            "title":   v["title"],
            "url":     v["link"],
            "text":    " ".join(s["snippet"] for s in tr.get("transcript", [])),
        })
    return docs
```

### 频道发布速度

```python
def channel_velocity(handle):
    page = requests.get(
        "https://api.hasdata.com/scrape/youtube/channel",
        headers={"x-api-key": API_KEY},
        params={"channelId": handle, "tab": "videos"}, timeout=300,
    ).json()
    return [
        {"date": it.get("publishedDate"),
         "views": it.get("extractedViews"),
         "title": it.get("title")}
        for sec in page.get("sections", [])
        for it in sec.get("items", [])
    ]
```

### 在转录文本中按时间戳搜索

```python
def mentions(video_id, needle):
    tr = requests.get(
        "https://api.hasdata.com/scrape/youtube/transcript",
        headers={"x-api-key": API_KEY},
        params={"v": video_id}, timeout=300,
    ).json()
    return [(s["startTimeText"], s["snippet"])
            for s in tr.get("transcript", [])
            if needle.lower() in s["snippet"].lower()]
```

## 陷阱

- **`v` 是 11 字符的 ID，不是 URL。** 请先提取 `v=` 的值。
- **`languageCode` 必须在视频上存在。** 如果获取失败，请检查 `availableTranscripts[]` 后重试。
- **当不存在人工字幕轨道时，必须使用 `type=asr`。** 否则 API 会在仅有自动字幕的视频上报错。
- **`@handle` 解析为与规范 `UC…` ID 相同的频道。** 为可读性优先使用 handle。
- **分页 token 是不透明的** —— 通过 `paginationToken` 原样传回。
- **`extractedViews` / `extractedLikes`** 是整数；`views` / `likes` 是格式化的字符串。进行算术运算时请使用整数字段。
- **`channelInfo.rssUrl`** 是该频道的规范 RSS 源 —— 可在播客客户端中订阅而无需抓取。