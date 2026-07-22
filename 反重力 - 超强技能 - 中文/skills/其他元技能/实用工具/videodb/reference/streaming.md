# 流媒体与播放

VideoDB 按需生成流，返回 HLS 兼容的 URL，可在任何标准视频播放器中即时播放。无需渲染时间或导出等待 — 编辑、搜索和合成立即流式传输。

## 前置条件

视频**必须先上传**到集合才能生成流。对于基于搜索的流，视频还必须已**建立索引**（语音和/或场景）。索引详情请参阅 [search.md](search.md)。

## 核心概念

### 流生成

VideoDB 中的每个视频、搜索结果和时间线都可以生成**流 URL**。该 URL 指向一个按需编译的 HLS（HTTP Live Streaming）清单。

```python
# 从视频生成
stream_url = video.generate_stream()

# 从时间线生成
stream_url = timeline.generate_stream()

# 从搜索结果生成
stream_url = results.compile()
```

## 流式传输单个视频

### 基本播放

```python
import videodb

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video("your-video-id")

# 生成流 URL
stream_url = video.generate_stream()
print(f"Stream: {stream_url}")

# 在默认浏览器中打开
video.play()
```

### 带字幕

```python
# 先索引并添加字幕
video.index_spoken_words(force=True)
video.add_subtitle()

# 流现在包含字幕
stream_url = video.generate_stream()
```

### 特定片段

通过传入时间戳范围的时间线，仅流式传输视频的一部分：

```python
# 流式传输第 10-30 秒和第 60-90 秒
stream_url = video.generate_stream(timeline=[(10, 30), (60, 90)])
print(f"Segment stream: {stream_url}")
```

## 流式传输时间线合成

构建多资源合成并实时流式传输：

```python
import videodb
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, AudioAsset, ImageAsset, TextAsset, TextStyle

conn = videodb.connect()
coll = conn.get_collection()

video = coll.get_video(video_id)
music = coll.get_audio(music_id)

timeline = Timeline(conn)

# 主视频内容
timeline.add_inline(VideoAsset(asset_id=video.id))

# 背景音乐叠加（从第 0 秒开始）
timeline.add_overlay(0, AudioAsset(asset_id=music.id))

# 开头的文字叠加
timeline.add_overlay(0, TextAsset(
    text="Live Demo",
    duration=3,
    style=TextStyle(fontsize=48, fontcolor="white", boxcolor="#000000"),
))

# 生成合成流
stream_url = timeline.generate_stream()
print(f"Composed stream: {stream_url}")
```

**重要：** `add_inline()` 仅接受 `VideoAsset`。使用 `add_overlay()` 添加 `AudioAsset`、`ImageAsset` 和 `TextAsset`。

详细的时间线编辑请参阅 [editor.md](editor.md)。

## 流式传输搜索结果

将搜索结果编译为包含所有匹配片段的单一流：

```python
from videodb import SearchType

video.index_spoken_words(force=True)
results = video.search("key announcement", search_type=SearchType.semantic)

# 将所有匹配的镜头编译为一个流
stream_url = results.compile()
print(f"Search results stream: {stream_url}")

# 或直接播放
results.play()
```

### 流式传输单个搜索命中

```python
results = video.search("product demo", search_type=SearchType.semantic)

for i, shot in enumerate(results.get_shots()):
    stream_url = shot.generate_stream()
    print(f"Hit {i+1} [{shot.start:.1f}s-{shot.end:.1f}s]: {stream_url}")
```

## 音频播放

获取音频内容的签名播放 URL：

```python
audio = coll.get_audio(audio_id)
playback_url = audio.generate_url()
print(f"Audio URL: {playback_url}")
```

## 完整工作流示例

### 搜索到流管道

将搜索、时间线合成和流式传输整合到一个工作流中：

```python
import videodb
from videodb import SearchType
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, TextAsset, TextStyle

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video("your-video-id")

video.index_spoken_words(force=True)

# 搜索关键时刻
queries = ["introduction", "main demo", "Q&A"]
timeline = Timeline(conn)

for query in queries:
    # 查找匹配片段
    results = video.search(query, search_type=SearchType.semantic)
    for shot in results.get_shots():
        timeline.add_inline(
            VideoAsset(asset_id=shot.video_id, start=shot.start, end=shot.end)
        )

    # 在第一个镜头上添加章节标签叠加
    timeline.add_overlay(0, TextAsset(
        text=query.title(),
        duration=2,
        style=TextStyle(fontsize=36, fontcolor="white", boxcolor="#222222"),
    ))

stream_url = timeline.generate_stream()
print(f"Dynamic compilation: {stream_url}")
```

### 多视频流

将来自不同视频的片段合并为单一流：

```python
import videodb
from videodb.timeline import Timeline
from videodb.asset import VideoAsset

conn = videodb.connect()
coll = conn.get_collection()

video_clips = [
    {"id": "vid_001", "start": 0, "end": 15},
    {"id": "vid_002", "start": 10, "end": 30},
    {"id": "vid_003", "start": 5, "end": 25},
]

timeline = Timeline(conn)
for clip in video_clips:
    timeline.add_inline(
        VideoAsset(asset_id=clip["id"], start=clip["start"], end=clip["end"])
    )

stream_url = timeline.generate_stream()
print(f"Multi-video stream: {stream_url}")
```

### 条件流组装

根据搜索可用性动态构建流：

```python
import videodb
from videodb import SearchType
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, TextAsset, TextStyle

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video("your-video-id")

video.index_spoken_words(force=True)

timeline = Timeline(conn)

# 尝试查找特定内容；回退到完整视频
topics = ["opening remarks", "technical deep dive", "closing"]

found_any = False
for topic in topics:
    results = video.search(topic, search_type=SearchType.semantic)
    shots = results.get_shots()
    if shots:
        found_any = True
        for shot in shots:
            timeline.add_inline(
                VideoAsset(asset_id=shot.video_id, start=shot.start, end=shot.end)
            )
        # 为该章节添加标签叠加
        timeline.add_overlay(0, TextAsset(
            text=topic.title(),
            duration=2,
            style=TextStyle(fontsize=32, fontcolor="white", boxcolor="#1a1a2e"),
        ))

if found_any:
    stream_url = timeline.generate_stream()
    print(f"Curated stream: {stream_url}")
else:
    # 回退到完整视频流
    stream_url = video.generate_stream()
    print(f"Full video stream: {stream_url}")
```

### 活动回顾

将活动录制处理为包含多个章节的可流式回顾：

```python
import videodb
from videodb import SearchType
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, AudioAsset, ImageAsset, TextAsset, TextStyle

conn = videodb.connect()
coll = conn.get_collection()

# 上传活动录制
event = coll.upload(url="https://example.com/event-recording.mp4")
event.index_spoken_words(force=True)

# 生成背景音乐
music = coll.generate_music(
    prompt="upbeat corporate background music",
    duration=120,
)

# 生成标题图片
title_img = coll.generate_image(
    prompt="modern event recap title card, dark background, professional",
    aspect_ratio="16:9",
)

# 构建回顾时间线
timeline = Timeline(conn)

# 来自搜索的主视频片段
keynote = event.search("keynote announcement", search_type=SearchType.semantic)
if keynote.get_shots():
    for shot in keynote.get_shots()[:5]:
        timeline.add_inline(
            VideoAsset(asset_id=shot.video_id, start=shot.start, end=shot.end)
        )

demo = event.search("product demo", search_type=SearchType.semantic)
if demo.get_shots():
    for shot in demo.get_shots()[:5]:
        timeline.add_inline(
            VideoAsset(asset_id=shot.video_id, start=shot.start, end=shot.end)
        )

# 叠加标题卡图片
timeline.add_overlay(0, ImageAsset(
    asset_id=title_img.id, width=100, height=100, x=80, y=20, duration=5
))

# 叠加章节标签
timeline.add_overlay(5, TextAsset(
    text="Keynote Highlights",
    duration=3,
    style=TextStyle(fontsize=40, fontcolor="white", boxcolor="#0d1117"),
))

# 叠加背景音乐
timeline.add_overlay(0, AudioAsset(
    asset_id=music.id, fade_in_duration=3
))

# 流式传输最终回顾
stream_url = timeline.generate_stream()
print(f"Event recap: {stream_url}")
```

---

## 提示

- **HLS 兼容性**：流 URL 返回 HLS 清单（`.m3u8`）。它们在 Safari 中原生工作，在其他浏览器中通过 hls.js 或类似库工作。
- **按需编译**：流在请求时由服务端编译。首次播放可能有短暂的编译延迟；相同合成的后续播放会被缓存。
- **缓存**：不带参数第二次调用 `video.generate_stream()` 会返回缓存的流 URL，而不是重新编译。
- **片段流**：`video.generate_stream(timeline=[(start, end)])` 是流式传输特定片段的最快方式，无需构建完整的 `Timeline` 对象。
- **内联与叠加**：`add_inline()` 仅接受 `VideoAsset`，将资源按顺序放在主轨道上。`add_overlay()` 接受 `AudioAsset`、`ImageAsset` 和 `TextAsset`，在给定的开始时间将它们叠加在上层。
- **TextStyle 默认值**：`TextStyle` 默认为 `font='Sans'`、`fontcolor='black'`。使用 `boxcolor`（而非 `bgcolor`）设置文字背景色。
- **与生成结合**：使用 `coll.generate_music(prompt, duration)` 和 `coll.generate_image(prompt, aspect_ratio)` 为时间线合成创建资源。
- **播放**：`.play()` 在默认系统浏览器中打开流 URL。对于编程使用，直接使用 URL 字符串。
