# YouTube 参考

子命令：`youtube-search-api`、`youtube-video-api`、`youtube-channel-api`、`youtube-transcript-api`。各 10 积分。

`*-search-api` 按关键词驱动；其他命令定位特定视频、频道或字幕。大部分工作流是 search → video → transcript 串起来。

---

## youtube-search-api

```bash
hasdata youtube-search-api --q "QUERY" [--sort-by relevance|date|views|rating|popularity] \
  [--length under4|between420|plus20] [--date hour|today|week|month|year] \
  [--video-type video|shorts|channel|playlist|movie] \
  [--gl us] [--hl en] [--device-type desktop|mobile] \
  [--pagination-token TOKEN] --raw | jq .
```

常用标志：
- `--q TEXT`（必填）
- `--sort-by relevance|date|views|rating|popularity`
- `--date hour|today|week|month|year` ——上传时间窗口
- `--length under4|between420|plus20` ——时长桶（`<4m`、`4–20m`、`>20m`）
- `--video-type video|shorts|channel|playlist|movie`
- `--filters hd,k4,hdr,subtitles,cc,d3,d360,vr180,live,bought,location` ——特性标志 AND 组合
- `--gl`、`--hl` ——国家/语言
- `--pagination-token` ——从上一次响应的 `pagination.nextPageToken` 拷贝
- `--sp` ——原始 YouTube `sp=` 过滤 token（覆盖 `sort-by` / `date` / `video-type` / `length` / `filters`）

顶层响应键：`videoResults`、`shortsResults`、`channelResults`、`playlistResults`、`adsResults`、`sponsoredResults`、`searchInformation`、`pagination`。

每条视频结果：`videoId`、`title`、`link`、`channel`、`description`、`length`、`views`、`viewsOriginal`、`publishedDate`、`thumbnail`、`positionOnPage`。

```bash
# Latest videos for a topic
hasdata youtube-search-api --q "$Q" --sort-by date --date week --raw \
  | jq -c '.videoResults[] | {title, channel: .channel.name, views, publishedDate, link}'
```

## youtube-video-api

```bash
hasdata youtube-video-api --v-param VIDEO_ID [--gl us] [--hl en] --raw | jq .
```

- `--v-param`（必填）——11 位视频 ID（watch URL 中的 `v=` 部分）
- `--device-type desktop|mobile`
- `--gl`、`--hl`

顶层字段：`videoId`、`title`、`description`、`channel`、`views`、`extractedViews`、`likes`、`extractedLikes`、`lengthSeconds`、`publishedDate`、`keywords[]`、`captions`、`socialLinks`、`music`、`category`、`thumbnail`、`isFamilySafe`、`isUnlisted`、`relatedVideos[]`、`relatedShorts[]`、`endScreenVideos[]`。

```bash
# Quick stats
hasdata youtube-video-api --v-param "$VID" --raw \
  | jq '{title, views: .extractedViews, likes: .extractedLikes, length: .lengthSeconds, published: .publishedDate, channel: .channel.name}'
```

## youtube-channel-api

```bash
hasdata youtube-channel-api --channel-id "@HANDLE_OR_UCID" \
  [--tab featured|videos|shorts|streams|playlists|posts|community|podcasts|releases|about|store] \
  [--gl us] [--hl en] [--pagination-token TOKEN] --raw | jq .
```

- `--channel-id`（必填）——`@handle`、`UC…` 规范 ID，或旧的 `/c/<custom>` / `/user/<name>` URL slug
- `--tab` ——要抓哪个 tab；默认 `featured`（主页）
- `--pagination-token` ——用于分页 tab（`videos`、`shorts` 等）

顶层响应：`channelInfo`、`featuredVideo`、`sections[]`。

`channelInfo` 含：`name`、`handle`、`channelId`、`channelUrl`、`avatar`、`banner`、`description`、`subscribers`、`extractedSubscribers`、`videosCount`、`extractedVideosCount`、`keywords[]`、`availableTabs[]`、`verified`、`websiteUrl`、`rssUrl`、`isFamilySafe`。

```bash
# All uploads (paginated)
hasdata youtube-channel-api --channel-id "@MrBeast" --tab videos --raw \
  | jq -c '.sections[].items[]? | {title, videoId, views, publishedDate}'
```

## youtube-transcript-api

```bash
hasdata youtube-transcript-api --v-param VIDEO_ID [--language-code en] [--type asr] --raw | jq .
```

- `--v-param`（必填）——11 位视频 ID
- `--language-code` ——BCP-47 / YouTube 代码（`en`、`de`、`en-US`、`pt-BR`）；必须匹配视频实际拥有的字幕轨道
- `--type asr` ——取自动语音识别轨道（不传则取人工上传的）

响应：`transcript[]` 和 `availableTranscripts[]`。

每条 `transcript[]` 元素：`startMs`、`endMs`、`snippet`、`startTimeText`。把 `snippet` 串起来还原全文。

```bash
# Flatten to plain text
hasdata youtube-transcript-api --v-param "$VID" --raw \
  | jq -r '.transcript[].snippet' | tr '\n' ' '
```

---

## 非显式用例

- **"这个视频到底讲了什么？"** ——`youtube-transcript-api --v-param X --raw | jq -r '.transcript[].snippet'` → 喂给 LLM 做真正的总结，不要凭缩略图/标题猜。
- **在简报里引用 YouTube 内容** ——字幕 + 时间戳支持你以 `(02:14)` 精度引用。创作者没上传字幕时用 `--type asr` 顶上。
- **频道增长审计** ——`youtube-channel-api --channel-id @X --tab videos` 分页；`jq '.sections[].items[] | {publishedDate, views: .extractedViews}'` 给出速度随时间变化的表。
- **趋势发现** ——`youtube-search-api --q "TOPIC" --sort-by views --date month` 返回过去一个月播放量最高的视频——在它登上 Google News 之前预判文化趋势。
- **竞品内容地图** ——`youtube-channel-api --channel-id @competitor --tab videos --raw | jq -r '.sections[].items[].title'` 列出所有发布过的标题，用于内容缺口分析。
- **品牌安全扫描** ——`youtube-search-api --q "BRAND" --sort-by date --date week --raw | jq '.videoResults[] | select(.title | test("BRAND"; "i"))'` 在新提及病毒化前抓出来。
- **网红尽调** ——组合 `youtube-channel-api` 拿粉丝/视频数 + `youtube-video-api` 看头部视频（互动率 ≈ `likes / views`）。
- **"找到他们说 X 的那一段"** ——`youtube-transcript-api`，然后 `jq -r '.transcript[] | select(.snippet | test("X"; "i")) | "\(.startTimeText): \(.snippet)"'`，返回每次提到的时间戳。
- **音乐授权查询** ——`youtube-video-api --v-param X --raw | jq .music` 在 YouTube Content ID 匹配时返回识别到的曲目（艺人、标题）。
- **翻译/重新本地化视频** ——用 `youtube-transcript-api` 拉英文字幕，通过 LLM 翻译，重新生成字幕。比重新转录音频便宜。
- **给频道建播客/RSS feed** ——`youtube-channel-api --raw | jq -r .channelInfo.rssUrl` 返回官方 RSS URL；订阅到任意播客 app。
- **检测已删除视频** ——`youtube-video-api --v-param X` 对被下架视频返回错误；在归档流水线中可用于捕获下架。
- **批量研究 → 字幕链** ——`youtube-search-api --q "$Q" --raw | jq -r '.videoResults[].videoId' | xargs -I{} hasdata youtube-transcript-api --v-param {} --raw`，从话题搜索构建研究语料。
- **只看 Shorts / 只看长视频 feed** ——`--video-type shorts` vs `--length plus20` 偏向其中一种。
- **直播发现** ——`--filters live` 只返回当前正在直播；配合 `--sort-by date` 拿最新直播。

## 流水线

```bash
# Search → top 5 video transcripts as a corpus
hasdata youtube-search-api --q "$Q" --sort-by views --raw \
  | jq -r '.videoResults[:5][].videoId' \
  | while read -r vid; do
      echo "=== $vid ==="
      hasdata youtube-transcript-api --v-param "$vid" --raw \
        | jq -r '.transcript[].snippet'
    done > corpus.txt

# Channel → CSV of all videos
hasdata youtube-channel-api --channel-id "@$HANDLE" --tab videos --raw \
  | jq -r '.sections[].items[]? | [.videoId, .title, (.extractedViews // 0), .publishedDate] | @csv' \
  > channel_videos.csv
```

## 注意事项

- **`--v-param` 恰好 11 个字符** ——不是完整 watch URL。提取 `v=` 部分或用上次搜索的 `jq -r '.videoResults[0].videoId'`。
- **`--language-code` 必须是视频上确实存在的。** 传 `availableTranscripts[]` 里列出的代码之一，或不传取默认轨道。
- **没有人工字幕时需要 `--type asr`。** 不传的话 API 返回默认的人工轨道，没有就报错。
- **`@handle` 比 `UC…` 优先** ——更易读，结果一样。旧 `/c/` 和 `/user/` slug 也能解析。
- **`pagination.nextPageToken` 是不透明的** ——原样通过 `--pagination-token` 回传，不要试图解码。
- **`views` vs `extractedViews`** ——`views` 是格式化字符串（`"1.2M views"`），`extractedViews` 是整数。计算用整数。