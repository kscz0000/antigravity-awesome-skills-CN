---
name: youtube-automation
description: "通过 Rube MCP（Composio）自动化 YouTube 任务：上传视频、管理播放列表、搜索内容、获取分析数据和处理评论。始终先搜索工具以获取最新 schema。触发词：YouTube自动化、YouTube视频上传、YouTube播放列表、YouTube评论、YouTube分析、Rube MCP、Composio"
risk: critical
source: community
date_added: "2026-02-27"
---

# YouTube 自动化（通过 Rube MCP）

通过 Rube MCP 经由 Composio 的 YouTube 工具包自动化 YouTube 操作。

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `youtube` 建立活跃的 YouTube 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API key，只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用工具包 `youtube` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的授权链接完成 Google OAuth
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 上传与管理视频

**使用时机**：用户想要上传视频或更新视频元数据

**工具序列**：
1. `YOUTUBE_UPLOAD_VIDEO` - 上传新视频 [必选]
2. `YOUTUBE_UPDATE_VIDEO` - 更新标题、描述、标签、隐私设置 [可选]
3. `YOUTUBE_UPDATE_THUMBNAIL` - 设置自定义缩略图 [可选]

**关键参数**：
- `title`：视频标题（最多 100 个字符）
- `description`：视频描述（最多 5000 字节）
- `tags`：关键词标签数组
- `categoryId`：YouTube 类别 ID（例如，'22' 代表人物与博客）
- `privacyStatus`：'public'、'private' 或 'unlisted'
- `videoFilePath`：包含 `{name, mimetype, s3key}` 的视频文件对象

**注意事项**：
- `UPLOAD_VIDEO` 消耗大量配额；仅修改元数据时优先使用 `UPDATE_VIDEO`
- `videoFilePath` 必须是包含 `s3key` 的对象，不能是裸文件路径或 URL
- 标签总长度（含分隔符）不得超过 500 个字符
- 标签中的尖括号 `< >` 会被自动去除
- 描述长度限制为 5000 字节，而非字符（多字节字符计数更多）

### 2. 搜索 YouTube 内容

**使用时机**：用户想要查找视频、频道或播放列表

**工具序列**：
1. `YOUTUBE_SEARCH_YOU_TUBE` - 搜索内容 [必选]
2. `YOUTUBE_VIDEO_DETAILS` - 获取指定视频的完整详情 [可选]
3. `YOUTUBE_GET_VIDEO_DETAILS_BATCH` - 获取多个视频的详情 [可选]

**关键参数**：
- `q`：搜索查询（支持精确短语、排除词、频道 handle）
- `type`：'video'、'channel' 或 'playlist'
- `maxResults`：每页结果数（1-50）
- `pageToken`：用于分页

**注意事项**：
- 搜索接口仅返回 'snippet' 部分；统计数据请使用 `VIDEO_DETAILS`
- 搜索结果总数上限为 500 条
- 搜索配额消耗较高（100 单位），而列表接口仅 1 单位
- 批量视频详情的实际限制为每次约 50 个 ID；更大的集合需分块处理

### 3. 管理播放列表

**使用时机**：用户想要创建播放列表或管理播放列表内容

**工具序列**：
1. `YOUTUBE_LIST_USER_PLAYLISTS` - 列出用户现有播放列表 [可选]
2. `YOUTUBE_CREATE_PLAYLIST` - 创建新播放列表 [可选]
3. `YOUTUBE_ADD_VIDEO_TO_PLAYLIST` - 向播放列表添加视频 [可选]
4. `YOUTUBE_LIST_PLAYLIST_ITEMS` - 列出播放列表中的视频 [可选]

**关键参数**：
- `playlistId`：播放列表 ID（用户创建的为 'PL...'，上传列表的为 'UU...'）
- `part`：包含的资源部分（例如，'snippet,contentDetails'）
- `maxResults`：每页条目数（1-50）
- `pageToken`：上一次响应中的分页令牌

**注意事项**：
- 不要将频道 ID（'UC...'）作为播放列表 ID 传递；上传列表需将 'UC' 转换为 'UU'
- 大型播放列表需要通过 `pageToken` 分页；跟踪 `nextPageToken` 直到不再出现
- `items[].id` 不是 `videoId`；请使用 `items[].snippet.resourceId.videoId`
- 允许创建重名的播放列表；请先检查现有播放列表

### 4. 获取频道和视频分析

**使用时机**：用户想要分析频道表现或视频指标

**工具序列**：
1. `YOUTUBE_GET_CHANNEL_ID_BY_HANDLE` - 将 handle 解析为频道 ID [前置]
2. `YOUTUBE_GET_CHANNEL_STATISTICS` - 获取频道订阅者/观看/视频计数 [必选]
3. `YOUTUBE_LIST_CHANNEL_VIDEOS` - 列出频道的所有视频 [可选]
4. `YOUTUBE_GET_VIDEO_DETAILS_BATCH` - 获取每个视频的统计数据 [可选]
5. `YOUTUBE_GET_CHANNEL_ACTIVITIES` - 获取频道近期动态 [可选]

**关键参数**：
- `channelId`：频道 ID（'UC...'）、handle（'@handle'）或 'me'
- `forHandle`：频道 handle（例如，'@Google'）
- `id`：用于批量详情的以逗号分隔的视频 ID
- `parts`：包含的资源部分（例如，'snippet,statistics'）

**注意事项**：
- 频道统计数据是累计总数，而非按周期统计
- 由于私密/已删除视频，批量视频详情可能返回的条目少于请求数量
- 响应数据可能嵌套在 `data` 或 `data_preview` 下；需进行防御性解析
- `contentDetails.duration` 使用 ISO 8601 格式（例如，'PT4M13S'）

### 5. 管理订阅和评论

**使用时机**：用户想要订阅频道或查看视频评论

**工具序列**：
1. `YOUTUBE_SUBSCRIBE_CHANNEL` - 订阅频道 [可选]
2. `YOUTUBE_UNSUBSCRIBE_CHANNEL` - 取消订阅频道 [可选]
3. `YOUTUBE_LIST_USER_SUBSCRIPTIONS` - 列出订阅 [可选]
4. `YOUTUBE_LIST_COMMENT_THREADS` - 列出视频的评论 [可选]

**关键参数**：
- `channelId`：订阅/取消订阅的频道
- `videoId`：用于评论线程的视频 ID
- `maxResults`：每页结果数
- `pageToken`：分页令牌

**注意事项**：
- 订阅已订阅的频道可能返回错误
- 评论线程返回顶层评论，每条最多包含 5 条回复
- 部分视频可能禁用了评论
- 取消订阅需要订阅 ID，而非频道 ID

## 常见模式

### 频道 ID 解析

**Handle 转频道 ID**：
```
1. 使用 '@handle' 调用 YOUTUBE_GET_CHANNEL_ID_BY_HANDLE
2. 从响应中提取 channelId
3. 用于后续的频道操作
```

**上传列表**：
```
1. 获取频道 ID（以 'UC' 开头）
2. 将 'UC' 前缀替换为 'UU' 以获得上传列表 ID
3. 与 LIST_PLAYLIST_ITEMS 配合使用，枚举所有视频
```

### 分页

- 设置 `maxResults`（每页最多 50）
- 在响应中检查 `nextPageToken`
- 将该令牌作为下一次请求的 `pageToken` 传递
- 持续迭代，直到 `nextPageToken` 不再出现

### 批量视频详情

- 从搜索或播放列表中收集视频 ID
- 按约 50 个 ID 一组进行分块
- 对每个块调用 `GET_VIDEO_DETAILS_BATCH`
- 合并各块的结果

## 已知陷阱

**配额管理**：
- YouTube API 有每日配额限制（默认 10,000 单位）
- 上传 = 1600 单位；搜索 = 100 单位；列表 = 1 单位
- 尽可能优先使用列表接口而非搜索
- 监控配额使用以避免触及每日上限

**ID 格式**：
- 视频 ID：11 字符的字母数字字符串
- 频道 ID：以 'UC' 开头，后跟 22 个字符
- 播放列表 ID：以 'PL'（用户）或 'UU'（上传）开头
- 不要混淆频道 ID 和播放列表 ID

**缩略图**：
- 自定义缩略图需要频道完成手机验证
- 必须为 JPG、PNG 或 GIF 格式；小于 2MB
- 推荐：1280x720 分辨率（16:9 宽高比）

**响应解析**：
- 统计值以字符串形式返回，而非整数；参与计算前需转换类型
- 时长使用 ISO 8601 格式（PT#H#M#S）
- 批量响应可能将数据包装在不同的键下

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 上传视频 | YOUTUBE_UPLOAD_VIDEO | title, description, tags, categoryId, privacyStatus, videoFilePath |
| 更新视频 | YOUTUBE_UPDATE_VIDEO | video_id, title, description, tags |
| 设置缩略图 | YOUTUBE_UPDATE_THUMBNAIL | videoId, thumbnailUrl |
| 搜索 YouTube | YOUTUBE_SEARCH_YOU_TUBE | q, type, maxResults |
| 视频详情 | YOUTUBE_VIDEO_DETAILS | id, part |
| 批量视频详情 | YOUTUBE_GET_VIDEO_DETAILS_BATCH | id, parts |
| 列出播放列表 | YOUTUBE_LIST_USER_PLAYLISTS | maxResults, pageToken |
| 创建播放列表 | YOUTUBE_CREATE_PLAYLIST | （参见 schema） |
| 添加到播放列表 | YOUTUBE_ADD_VIDEO_TO_PLAYLIST | （参见 schema） |
| 列出播放列表条目 | YOUTUBE_LIST_PLAYLIST_ITEMS | playlistId, maxResults |
| 频道统计 | YOUTUBE_GET_CHANNEL_STATISTICS | id/forHandle/mine |
| 列出频道视频 | YOUTUBE_LIST_CHANNEL_VIDEOS | channelId, maxResults |
| 通过 handle 获取频道 ID | YOUTUBE_GET_CHANNEL_ID_BY_HANDLE | channel_handle |
| 订阅 | YOUTUBE_SUBSCRIBE_CHANNEL | channelId |
| 列出订阅 | YOUTUBE_LIST_USER_SUBSCRIPTIONS | （参见 schema） |
| 列出评论 | YOUTUBE_LIST_COMMENT_THREADS | videoId |
| 频道动态 | YOUTUBE_GET_CHANNEL_ACTIVITIES | （参见 schema） |

## 使用时机
本技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为可替代特定环境验证、测试或专家审查的产物。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下并请求澄清。
