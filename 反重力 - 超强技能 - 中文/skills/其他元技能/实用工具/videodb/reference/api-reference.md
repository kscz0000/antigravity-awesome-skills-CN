# 完整 API 参考

## 连接

```python
import videodb

conn = videodb.connect(
    api_key="your-api-key",      # 或设置 VIDEO_DB_API_KEY 环境变量
    base_url=None,                # 自定义 API 端点（可选）
)
```

**返回：** `Connection` 对象

### Connection 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `conn.get_collection(collection_id="default")` | `Collection` | 获取集合（无 ID 时获取默认集合） |
| `conn.get_collections()` | `list[Collection]` | 列出所有集合 |
| `conn.create_collection(name, description, is_public=False)` | `Collection` | 创建新集合 |
| `conn.update_collection(id, name, description)` | `Collection` | 更新集合 |
| `conn.check_usage()` | `dict` | 获取账户使用统计 |
| `conn.upload(source, media_type, name, ...)` | `Video\|Audio\|Image` | 上传到默认集合 |
| `conn.record_meeting(meeting_url, bot_name, ...)` | `Meeting` | 录制会议 |
| `conn.create_capture_session(...)` | `CaptureSession` | 创建捕获会话（见 [capture-reference.md](capture-reference.md)） |
| `conn.youtube_search(query, result_threshold, duration)` | `list[dict]` | 搜索 YouTube |
| `conn.transcode(source, callback_url, mode, ...)` | `str` | 转码视频（返回作业 ID） |
| `conn.get_transcode_details(job_id)` | `dict` | 获取转码作业状态和详情 |
| `conn.connect_websocket(collection_id)` | `WebSocketConnection` | 连接 WebSocket（见 [capture-reference.md](capture-reference.md)） |

### 转码

从 URL 转码视频，支持自定义分辨率、质量和音频设置。处理在服务端进行——无需本地 ffmpeg。

```python
from videodb import TranscodeMode, VideoConfig, AudioConfig

job_id = conn.transcode(
    source="https://example.com/video.mp4",
    callback_url="https://example.com/webhook",
    mode=TranscodeMode.economy,
    video_config=VideoConfig(resolution=720, quality=23),
    audio_config=AudioConfig(mute=False),
)
```

#### transcode 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `source` | `str` | 必需 | 要转码的视频 URL（最好是可下载的 URL） |
| `callback_url` | `str` | 必需 | 转码完成时接收回调的 URL |
| `mode` | `TranscodeMode` | `TranscodeMode.economy` | 转码速度：`economy` 或 `lightning` |
| `video_config` | `VideoConfig` | `VideoConfig()` | 视频编码设置 |
| `audio_config` | `AudioConfig` | `AudioConfig()` | 音频编码设置 |

返回作业 ID（`str`）。使用 `conn.get_transcode_details(job_id)` 检查作业状态。

```python
details = conn.get_transcode_details(job_id)
```

#### VideoConfig

```python
from videodb import VideoConfig, ResizeMode

config = VideoConfig(
    resolution=720,              # 目标分辨率高度（如 480、720、1080）
    quality=23,                  # 编码质量（越低越好，默认 23）
    framerate=30,                # 目标帧率
    aspect_ratio="16:9",         # 目标宽高比
    resize_mode=ResizeMode.crop, # 适配方式：crop、fit 或 pad
)
```

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `resolution` | `int\|None` | `None` | 目标分辨率高度（像素） |
| `quality` | `int` | `23` | 编码质量（越低质量越高） |
| `framerate` | `int\|None` | `None` | 目标帧率 |
| `aspect_ratio` | `str\|None` | `None` | 目标宽高比（如 `"16:9"`、`"9:16"`） |
| `resize_mode` | `str` | `ResizeMode.crop` | 调整大小策略：`crop`、`fit` 或 `pad` |

#### AudioConfig

```python
from videodb import AudioConfig

config = AudioConfig(mute=False)
```

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `mute` | `bool` | `False` | 静音音频轨道 |

## 集合

```python
coll = conn.get_collection()
```

### Collection 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `coll.get_videos()` | `list[Video]` | 列出所有视频 |
| `coll.get_video(video_id)` | `Video` | 获取特定视频 |
| `coll.get_audios()` | `list[Audio]` | 列出所有音频 |
| `coll.get_audio(audio_id)` | `Audio` | 获取特定音频 |
| `coll.get_images()` | `list[Image]` | 列出所有图像 |
| `coll.get_image(image_id)` | `Image` | 获取特定图像 |
| `coll.upload(url=None, file_path=None, media_type=None, name=None)` | `Video\|Audio\|Image` | 上传媒体 |
| `coll.search(query, search_type, index_type, score_threshold, namespace, scene_index_id, ...)` | `SearchResult` | 跨集合搜索（仅语义搜索；关键词和场景搜索会抛出 `NotImplementedError`） |
| `coll.generate_image(prompt, aspect_ratio="1:1")` | `Image` | 用 AI 生成图像 |
| `coll.generate_video(prompt, duration=5)` | `Video` | 用 AI 生成视频 |
| `coll.generate_music(prompt, duration=5)` | `Audio` | 用 AI 生成音乐 |
| `coll.generate_sound_effect(prompt, duration=2)` | `Audio` | 生成音效 |
| `coll.generate_voice(text, voice_name="Default")` | `Audio` | 从文本生成语音 |
| `coll.generate_text(prompt, model_name="basic", response_type="text")` | `dict` | LLM 文本生成——通过 `["output"]` 访问结果 |
| `coll.dub_video(video_id, language_code)` | `Video` | 将视频配音到其他语言 |
| `coll.record_meeting(meeting_url, bot_name, ...)` | `Meeting` | 录制实时会议 |
| `coll.create_capture_session(...)` | `CaptureSession` | 创建捕获会话（见 [capture-reference.md](capture-reference.md)） |
| `coll.get_capture_session(...)` | `CaptureSession` | 获取捕获会话（见 [capture-reference.md](capture-reference.md)） |
| `coll.connect_rtstream(url, name, ...)` | `RTStream` | 连接到直播流（见 [rtstream-reference.md](rtstream-reference.md)） |
| `coll.make_public()` | `None` | 将集合设为公开 |
| `coll.make_private()` | `None` | 将集合设为私有 |
| `coll.delete_video(video_id)` | `None` | 删除视频 |
| `coll.delete_audio(audio_id)` | `None` | 删除音频 |
| `coll.delete_image(image_id)` | `None` | 删除图像 |
| `coll.delete()` | `None` | 删除集合 |

### Upload 参数

```python
video = coll.upload(
    url=None,            # 远程 URL（HTTP、YouTube）
    file_path=None,      # 本地文件路径
    media_type=None,     # "video"、"audio" 或 "image"（省略时自动检测）
    name=None,           # 媒体的自定义名称
    description=None,    # 描述
    callback_url=None,   # 异步通知的 Webhook URL
)
```

## Video 对象

```python
video = coll.get_video(video_id)
```

### Video 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `video.id` | `str` | 唯一视频 ID |
| `video.collection_id` | `str` | 父集合 ID |
| `video.name` | `str` | 视频名称 |
| `video.description` | `str` | 视频描述 |
| `video.length` | `float` | 时长（秒） |
| `video.stream_url` | `str` | 默认流 URL |
| `video.player_url` | `str` | 播放器嵌入 URL |
| `video.thumbnail_url` | `str` | 缩略图 URL |

### Video 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `video.generate_stream(timeline=None)` | `str` | 生成流 URL（可选时间线，格式为 `[(start, end)]` 元组列表） |
| `video.play()` | `str` | 在浏览器中打开流，返回播放器 URL |
| `video.index_spoken_words(language_code=None, force=False)` | `None` | 索引语音以供搜索。使用 `force=True` 跳过已索引的情况。 |
| `video.index_scenes(extraction_type, prompt, extraction_config, metadata, model_name, name, scenes, callback_url)` | `str` | 索引视觉场景（返回 scene_index_id） |
| `video.index_visuals(prompt, batch_config, ...)` | `str` | 索引视觉内容（返回 scene_index_id） |
| `video.index_audio(prompt, model_name, ...)` | `str` | 用 LLM 索引音频（返回 scene_index_id） |
| `video.get_transcript(start=None, end=None)` | `list[dict]` | 获取带时间戳的转录文本 |
| `video.get_transcript_text(start=None, end=None)` | `str` | 获取完整转录文本 |
| `video.generate_transcript(force=None)` | `dict` | 生成转录文本 |
| `video.translate_transcript(language, additional_notes)` | `list[dict]` | 翻译转录文本 |
| `video.search(query, search_type, index_type, filter, **kwargs)` | `SearchResult` | 在视频内搜索 |
| `video.add_subtitle(style=SubtitleStyle())` | `str` | 添加字幕（返回流 URL） |
| `video.generate_thumbnail(time=None)` | `str\|Image` | 生成缩略图 |
| `video.get_thumbnails()` | `list[Image]` | 获取所有缩略图 |
| `video.extract_scenes(extraction_type, extraction_config)` | `SceneCollection` | 提取场景 |
| `video.reframe(start, end, target, mode, callback_url)` | `Video\|None` | 重构视频宽高比 |
| `video.clip(prompt, content_type, model_name)` | `str` | 从提示词生成片段（返回流 URL） |
| `video.insert_video(video, timestamp)` | `str` | 在时间戳处插入视频 |
| `video.download(name=None)` | `dict` | 下载视频 |
| `video.delete()` | `None` | 删除视频 |

### 重构（Reframe）

将视频转换为不同的宽高比，可选智能对象跟踪。处理在服务端进行。

> **警告：** 重构是缓慢的服务端操作。对于长视频可能需要几分钟并可能超时。始终使用 `start`/`end` 限制片段，或传递 `callback_url` 进行异步处理。

```python
from videodb import ReframeMode

# 始终优先重构短片段以避免超时：
reframed = video.reframe(start=0, end=60, target="vertical", mode=ReframeMode.smart)

# 完整长度视频的异步重构（返回 None，结果通过 webhook）：
video.reframe(target="vertical", callback_url="https://example.com/webhook")

# 自定义尺寸
reframed = video.reframe(start=0, end=60, target={"width": 1080, "height": 1080})
```

#### reframe 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `start` | `float\|None` | `None` | 开始时间（秒）（None = 开头） |
| `end` | `float\|None` | `None` | 结束时间（秒）（None = 视频结尾） |
| `target` | `str\|dict` | `"vertical"` | 预设字符串（`"vertical"`、`"square"`、`"landscape"`）或 `{"width": int, "height": int}` |
| `mode` | `str` | `ReframeMode.smart` | `"simple"`（中心裁剪）或 `"smart"`（对象跟踪） |
| `callback_url` | `str\|None` | `None` | 异步通知的 Webhook URL |

当未提供 `callback_url` 时返回 `Video` 对象，否则返回 `None`。

## Audio 对象

```python
audio = coll.get_audio(audio_id)
```

### Audio 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `audio.id` | `str` | 唯一音频 ID |
| `audio.collection_id` | `str` | 父集合 ID |
| `audio.name` | `str` | 音频名称 |
| `audio.length` | `float` | 时长（秒） |

### Audio 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `audio.generate_url()` | `str` | 生成签名 URL 用于播放 |
| `audio.get_transcript(start=None, end=None)` | `list[dict]` | 获取带时间戳的转录文本 |
| `audio.get_transcript_text(start=None, end=None)` | `str` | 获取完整转录文本 |
| `audio.generate_transcript(force=None)` | `dict` | 生成转录文本 |
| `audio.delete()` | `None` | 删除音频 |

## Image 对象

```python
image = coll.get_image(image_id)
```

### Image 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `image.id` | `str` | 唯一图像 ID |
| `image.collection_id` | `str` | 父集合 ID |
| `image.name` | `str` | 图像名称 |
| `image.url` | `str\|None` | 图像 URL（生成的图像可能为 `None`——改用 `generate_url()`） |

### Image 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `image.generate_url()` | `str` | 生成签名 URL |
| `image.delete()` | `None` | 删除图像 |

## 时间线与编辑器

### Timeline

```python
from videodb.timeline import Timeline

timeline = Timeline(conn)
```

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `timeline.add_inline(asset)` | `None` | 在主轨道上顺序添加 `VideoAsset` |
| `timeline.add_overlay(start, asset)` | `None` | 在时间戳处叠加 `AudioAsset`、`ImageAsset` 或 `TextAsset` |
| `timeline.generate_stream()` | `str` | 编译并获取流 URL |

### 资产类型

#### VideoAsset

```python
from videodb.asset import VideoAsset

asset = VideoAsset(
    asset_id=video.id,
    start=0,              # 修剪起点（秒）
    end=None,             # 修剪终点（秒，None = 完整）
)
```

#### AudioAsset

```python
from videodb.asset import AudioAsset

asset = AudioAsset(
    asset_id=audio.id,
    start=0,
    end=None,
    disable_other_tracks=True,   # 为 True 时静音原始音频
    fade_in_duration=0,          # 秒（最大 5）
    fade_out_duration=0,         # 秒（最大 5）
)
```

#### ImageAsset

```python
from videodb.asset import ImageAsset

asset = ImageAsset(
    asset_id=image.id,
    duration=None,        # 显示时长（秒）
    width=100,            # 显示宽度
    height=100,           # 显示高度
    x=80,                 # 水平位置（距左侧像素）
    y=20,                 # 垂直位置（距顶部像素）
)
```

#### TextAsset

```python
from videodb.asset import TextAsset, TextStyle

asset = TextAsset(
    text="Hello World",
    duration=5,
    style=TextStyle(
        fontsize=24,
        fontcolor="black",
        boxcolor="white",       # 背景框颜色
        alpha=1.0,
        font="Sans",
        text_align="T",         # 框内文本对齐
    ),
)
```

#### CaptionAsset（编辑器 API）

CaptionAsset 属于编辑器 API，它有自己的 Timeline、Track 和 Clip 系统：

```python
from videodb.editor import CaptionAsset, FontStyling

asset = CaptionAsset(
    src="auto",                    # "auto" 或 base64 ASS 字符串
    font=FontStyling(name="Clear Sans", size=30),
    primary_color="&H00FFFFFF",
)
```

完整 CaptionAsset 用法见 [editor.md](editor.md#caption-overlays)。

## 视频搜索参数

```python
results = video.search(
    query="your query",
    search_type=SearchType.semantic,       # semantic、keyword 或 scene
    index_type=IndexType.spoken_word,      # spoken_word 或 scene
    result_threshold=None,                 # 最大结果数
    score_threshold=None,                  # 最小相关性分数
    dynamic_score_percentage=None,         # 动态分数百分比
    scene_index_id=None,                   # 目标特定场景索引（通过 **kwargs 传递）
    filter=[],                             # 场景搜索的元数据过滤器
)
```

> **注意：** `filter` 是 `video.search()` 的显式命名参数。`scene_index_id` 通过 `**kwargs` 传递给 API。

> **重要：** 当没有匹配结果时，`video.search()` 会抛出 `InvalidRequestError`，消息为 `"No results found"`。始终用 try/except 包装搜索调用。对于场景搜索，使用 `score_threshold=0.3` 或更高来过滤低相关性噪音。

对于场景搜索，使用 `search_type=SearchType.semantic` 配合 `index_type=IndexType.scene`。当目标特定场景索引时传递 `scene_index_id`。详见 [search.md](search.md)。

## SearchResult 对象

```python
results = video.search("query", search_type=SearchType.semantic)
```

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `results.get_shots()` | `list[Shot]` | 获取匹配片段列表 |
| `results.compile()` | `str` | 将所有片段编译为流 URL |
| `results.play()` | `str` | 在浏览器中打开编译后的流 |

### Shot 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `shot.video_id` | `str` | 源视频 ID |
| `shot.video_length` | `float` | 源视频时长 |
| `shot.video_title` | `str` | 源视频标题 |
| `shot.start` | `float` | 开始时间（秒） |
| `shot.end` | `float` | 结束时间（秒） |
| `shot.text` | `str` | 匹配的文本内容 |
| `shot.search_score` | `float` | 搜索相关性分数 |

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `shot.generate_stream()` | `str` | 流式传输此特定片段 |
| `shot.play()` | `str` | 在浏览器中打开片段流 |

## Meeting 对象

```python
meeting = coll.record_meeting(
    meeting_url="https://meet.google.com/...",
    bot_name="Bot",
    callback_url=None,          # 状态更新的 Webhook URL
    callback_data=None,         # 传递给回调的可选字典
    time_zone="UTC",            # 会议时区
)
```

### Meeting 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `meeting.id` | `str` | 唯一会议 ID |
| `meeting.collection_id` | `str` | 父集合 ID |
| `meeting.status` | `str` | 当前状态 |
| `meeting.video_id` | `str` | 录制的视频 ID（完成后） |
| `meeting.bot_name` | `str` | 机器人名称 |
| `meeting.meeting_title` | `str` | 会议标题 |
| `meeting.meeting_url` | `str` | 会议 URL |
| `meeting.speaker_timeline` | `dict` | 发言者时间线数据 |
| `meeting.is_active` | `bool` | 正在初始化或处理时为 True |
| `meeting.is_completed` | `bool` | 完成时为 True |

### Meeting 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `meeting.refresh()` | `Meeting` | 从服务器刷新数据 |
| `meeting.wait_for_status(target_status, timeout=14400, interval=120)` | `bool` | 轮询直到达到目标状态 |

## RTStream 与捕获

关于 RTStream（实时摄入、索引、转录），见 [rtstream-reference.md](rtstream-reference.md)。

关于捕获会话（桌面录制、CaptureClient、通道），见 [capture-reference.md](capture-reference.md)。

## 枚举与常量

### SearchType

```python
from videodb import SearchType

SearchType.semantic    # 自然语言语义搜索
SearchType.keyword     # 精确关键词匹配
SearchType.scene       # 视觉场景搜索（可能需要付费计划）
SearchType.llm         # LLM 驱动的搜索
```

### SceneExtractionType

```python
from videodb import SceneExtractionType

SceneExtractionType.shot_based   # 自动镜头边界检测
SceneExtractionType.time_based   # 固定时间间隔提取
SceneExtractionType.transcript   # 基于转录的场景提取
```

### SubtitleStyle

```python
from videodb import SubtitleStyle

style = SubtitleStyle(
    font_name="Arial",
    font_size=18,
    primary_colour="&H00FFFFFF",
    bold=False,
    # ... 详见 SubtitleStyle 了解所有选项
)
video.add_subtitle(style=style)
```

### SubtitleAlignment 与 SubtitleBorderStyle

```python
from videodb import SubtitleAlignment, SubtitleBorderStyle
```

### TextStyle

```python
from videodb import TextStyle
# 或：from videodb.asset import TextStyle

style = TextStyle(
    fontsize=24,
    fontcolor="black",
    boxcolor="white",
    font="Sans",
    text_align="T",
    alpha=1.0,
)
```

### 其他常量

```python
from videodb import (
    IndexType,          # spoken_word、scene
    MediaType,          # video、audio、image
    Segmenter,          # word、sentence、time
    SegmentationType,   # sentence、llm
    TranscodeMode,      # economy、lightning
    ResizeMode,         # crop、fit、pad
    ReframeMode,        # simple、smart
    RTStreamChannelType,
)
```

## 异常

```python
from videodb.exceptions import (
    AuthenticationError,     # 无效或缺失 API 密钥
    InvalidRequestError,     # 错误参数或格式错误的请求
    RequestTimeoutError,     # 请求超时
    SearchError,             # 搜索操作失败（如未索引）
    VideodbError,            # 所有 VideoDB 错误的基类异常
)
```

| 异常 | 常见原因 |
|------|----------|
| `AuthenticationError` | 缺失或无效的 `VIDEO_DB_API_KEY` |
| `InvalidRequestError` | 无效 URL、不支持的格式、错误参数 |
| `RequestTimeoutError` | 服务器响应时间过长 |
| `SearchError` | 索引前搜索、无效搜索类型 |
| `VideodbError` | 服务器错误、网络问题、通用失败 |
