# Instagram Graph API — 端点参考

基础 URL：`https://graph.instagram.com/v21.0`

## 目录

1. [用户个人资料](#用户个人资料)
2. [媒体](#媒体)
3. [发布（两步法）](#发布)
4. [评论](#评论)
5. [媒体洞察](#媒体洞察)
6. [用户洞察](#用户洞察)
7. [话题标签](#话题标签)
8. [消息（私信）](#消息)
9. [提及](#提及)
10. [常见错误](#常见错误)

---

## 用户个人资料

### GET /{user-id}

返回个人资料信息。

**可用字段：**
- `id`, `username`, `name`, `account_type`
- `biography`, `followers_count`, `follows_count`, `media_count`
- `profile_picture_url`, `website`

**示例：**
```
GET /me?fields=id,username,name,account_type,biography,followers_count,follows_count,media_count&access_token=TOKEN
```

**响应：**
```json
{
  "id": "17841400000000",
  "username": "我的账号",
  "name": "我的名字",
  "account_type": "BUSINESS",
  "biography": "简介",
  "followers_count": 1500,
  "follows_count": 200,
  "media_count": 45
}
```

---

## 媒体

### GET /{user-id}/media

列出用户发布的媒体。

**参数：**
- `fields`: id, caption, media_type, media_url, permalink, timestamp, thumbnail_url
- `limit`: 1-100（默认 25）
- `after`/`before`: 分页游标

**媒体类型：** IMAGE, VIDEO, CAROUSEL_ALBUM

### GET /{media-id}

特定媒体的详情。

**额外字段：** `like_count`, `comments_count`, `is_shared_to_feed`

### GET /{media-id}/children

对于 CAROUSEL_ALBUM — 返回轮播项目。

---

## 发布

### 两步流程

**第 1 步 — 创建容器：**

```
POST /{user-id}/media
```

| 类型 | 必需参数 |
|------|------------------------|
| 照片 | `image_url`, `caption`（可选） |
| 视频 | `video_url`, `caption`, `media_type=VIDEO` |
| Reel | `video_url`, `caption`, `media_type=REELS` |
| Story（照片） | `image_url`, `media_type=STORIES` |
| Story（视频） | `video_url`, `media_type=STORIES` |
| 轮播项目 | `image_url` 或 `video_url`, `is_carousel_item=true` |
| 轮播容器 | `media_type=CAROUSEL`, `children=[id1,id2,...]`, `caption` |

**响应：** `{"id": "container_id"}`

**第 1.5 步 — 检查状态（视频）：**

```
GET /{container-id}?fields=status_code
```

状态：`IN_PROGRESS`, `FINISHED`, `ERROR`

等待 `FINISHED` 后再发布。每 5-10 秒轮询一次。

**第 2 步 — 发布：**

```
POST /{user-id}/media_publish
  creation_id={container_id}
```

**响应：** `{"id": "ig_media_id"}`

### 通过 API 定时发布

```
POST /{user-id}/media
  image_url=URL
  caption=文字
  published=false
  scheduled_publish_time=UNIX_TIMESTAMP
```

- 时间戳必须在 10 分钟到 75 天后的未来
- 仅 Business 账号支持（Creator 不支持原生定时）

---

## 评论

### GET /{media-id}/comments

列出媒体的评论。

**字段：** `id`, `text`, `username`, `timestamp`, `like_count`
**参数：** `limit`（最多 50），使用游标分页

### POST /{media-id}/comments

在帖子中回复（新的一级评论）。

**Body：** `message=文字`

### POST /{comment-id}/replies

回复特定评论。

**Body：** `message=文字`

### DELETE /{comment-id}

删除评论（仅限自己媒体上的评论或自己的评论）。

### POST /{comment-id}

隐藏/显示评论。

**Body：** `hide=true` 或 `hide=false`

---

## 媒体洞察

### GET /{media-id}/insights

**IMAGE/CAROUSEL 指标：**
- `impressions` — 媒体展示次数
- `reach` — 看到的唯一账号数
- `engagement` — 点赞 + 评论 + 收藏
- `saved` — 收藏次数

**VIDEO/REELS 额外指标：**
- `video_views` — 视频观看次数
- `plays` — reel 播放次数

**参数：**
```
metric=impressions,reach,engagement,saved
```

**响应：**
```json
{
  "data": [
    {
      "name": "impressions",
      "period": "lifetime",
      "values": [{"value": 250}],
      "title": "Impressions"
    }
  ]
}
```

---

## 用户洞察

### GET /{user-id}/insights

账号聚合指标。

**周期 `day` 的指标：**
- `impressions` — 总展示次数
- `reach` — 触达的唯一账号数
- `follower_count` — 粉丝总数（仅 `day`）
- `profile_views` — 个人资料查看次数

**周期 `week` / `days_28` 的指标：**
- `impressions`, `reach`

**参数：**
```
metric=impressions,reach,follower_count,profile_views
period=day
since=UNIX_TIMESTAMP
until=UNIX_TIMESTAMP
```

**限制：** 每次请求最多 30 天。`since` 和 `until` 必须与时区对齐。

---

## 话题标签

### GET /ig_hashtag_search

搜索话题标签 ID。

**参数：**
- `user_id`: 账号 ID
- `q`: 话题标签名称（不带 #）

**响应：** `{"data": [{"id": "17843853986012965"}]}`

**限制：** 每账号每周 30 个唯一话题标签（7 天滚动窗口）。

### GET /{hashtag-id}/recent_media

带有话题标签的最近帖子。

**字段：** `id`, `caption`, `media_type`, `media_url`, `permalink`, `timestamp`
**参数：** `user_id`（必需），`fields`, `limit`

### GET /{hashtag-id}/top_media

热门帖子（按热度排序）。

字段和参数与 `recent_media` 相同。

---

## 消息

### GET /{user-id}/conversations

列出 Instagram Messaging 对话。

**字段：** `id`, `participants`, `updated_time`
**需要：** 权限范围 `instagram_manage_messages`

### GET /{conversation-id}/messages

对话中的消息。

**字段：** `id`, `message`, `from`, `created_time`

### POST /me/messages

发送消息。

**Body：**
```json
{
  "recipient": {"id": "user_ig_scoped_id"},
  "message": {"text": "你好！"}
}
```

**限制：**
- 仅回复现有对话（在 24 小时窗口内）
- 或使用已批准的消息模板（需要 Meta 审批）

---

## 提及

### GET /{user-id}/tags

用户被提及/标记的媒体。

**字段：** `id`, `caption`, `media_type`, `media_url`, `permalink`, `timestamp`, `username`

---

## 常见错误

| 代码 | 子代码 | 含义 | 操作 |
|--------|-----------|-------------|------|
| 4 | - | 达到速率限制 | 退避 1 小时 |
| 10 | - | 权限被拒绝 | 检查权限范围 |
| 17 | - | 账号速率限制 | 等待指定时间 |
| 24 | - | Webhook 无效 | 检查 URL/证书 |
| 100 | - | 参数无效 | 检查请求 |
| 190 | - | 令牌过期/无效 | 刷新令牌 |
| 200 | - | 权限不足 | 检查 app review |
| 368 | - | 内容被阻止 | 内容政策 |

**标准错误格式：**
```json
{
  "error": {
    "message": "错误描述",
    "type": "OAuthException",
    "code": 190,
    "fbtrace_id": "AbCdEfG"
  }
}
```
