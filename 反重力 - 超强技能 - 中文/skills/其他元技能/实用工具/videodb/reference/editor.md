# 时间线编辑指南

VideoDB 提供非破坏性的时间线编辑器，用于从多个资产组合视频、添加文本和图像叠加层、混合音频轨道以及修剪片段——全部在服务端进行，无需重新编码或本地工具。用于修剪、组合片段、在视频上叠加音频/音乐、添加字幕以及分层文本或图像。

## 前提条件

视频、音频和图像**必须上传**到集合后才能用作时间线资产。对于字幕叠加层，视频还必须**索引语音**。

## 核心概念

### Timeline

`Timeline` 是一个虚拟组合层。资产可以**内联**放置（在主轨道上顺序播放）或作为**叠加层**（在特定时间戳分层）。不会修改原始媒体；最终流按需编译。

```python
from videodb.timeline import Timeline

timeline = Timeline(conn)
```

### 资产

时间线上的每个元素都是一个**资产**。VideoDB 提供五种资产类型：

| 资产 | 导入 | 主要用途 |
|------|------|----------|
| `VideoAsset` | `from videodb.asset import VideoAsset` | 视频片段（修剪、排序） |
| `AudioAsset` | `from videodb.asset import AudioAsset` | 音乐、音效、旁白 |
| `ImageAsset` | `from videodb.asset import ImageAsset` | Logo、缩略图、叠加层 |
| `TextAsset` | `from videodb.asset import TextAsset, TextStyle` | 标题、字幕、下三分之一 |
| `CaptionAsset` | `from videodb.editor import CaptionAsset` | 自动渲染的字幕（编辑器 API） |

## 构建时间线

### 内联添加视频片段

内联资产在主视频轨道上一个接一个播放。`add_inline` 方法只接受 `VideoAsset`：

```python
from videodb.asset import VideoAsset

video_a = coll.get_video(video_id_a)
video_b = coll.get_video(video_id_b)

timeline = Timeline(conn)
timeline.add_inline(VideoAsset(asset_id=video_a.id))
timeline.add_inline(VideoAsset(asset_id=video_b.id))

stream_url = timeline.generate_stream()
```

### 修剪 / 子片段

在 `VideoAsset` 上使用 `start` 和 `end` 提取部分内容：

```python
# 只取源视频的 10-30 秒
clip = VideoAsset(asset_id=video.id, start=10, end=30)
timeline.add_inline(clip)
```

### VideoAsset 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `asset_id` | `str` | 必需 | 视频媒体 ID |
| `start` | `float` | `0` | 修剪起点（秒） |
| `end` | `float\|None` | `None` | 修剪终点（`None` = 完整） |

> **警告：** SDK 不验证负时间戳。传递 `start=-5` 会被静默接受但产生损坏或意外的输出。在创建 `VideoAsset` 之前始终确保 `start >= 0`、`start < end` 且 `end <= video.length`。

## 文本叠加层

在时间线的任何位置添加标题、下三分之一或字幕：

```python
from videodb.asset import TextAsset, TextStyle

title = TextAsset(
    text="Welcome to the Demo",
    duration=5,
    style=TextStyle(
        fontsize=36,
        fontcolor="white",
        boxcolor="black",
        alpha=0.8,
        font="Sans",
    ),
)

# 在最开始（t=0）叠加标题
timeline.add_overlay(0, title)
```

### TextStyle 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `fontsize` | `int` | `24` | 字体大小（像素） |
| `fontcolor` | `str` | `"black"` | CSS 颜色名称或十六进制 |
| `fontcolor_expr` | `str` | `""` | 动态字体颜色表达式 |
| `alpha` | `float` | `1.0` | 文本不透明度（0.0–1.0） |
| `font` | `str` | `"Sans"` | 字体系列 |
| `box` | `bool` | `True` | 启用背景框 |
| `boxcolor` | `str` | `"white"` | 背景框颜色 |
| `boxborderw` | `str` | `"10"` | 框边框宽度 |
| `boxw` | `int` | `0` | 框宽度覆盖 |
| `boxh` | `int` | `0` | 框高度覆盖 |
| `line_spacing` | `int` | `0` | 行间距 |
| `text_align` | `str` | `"T"` | 框内文本对齐 |
| `y_align` | `str` | `"text"` | 垂直对齐参考 |
| `borderw` | `int` | `0` | 文本边框宽度 |
| `bordercolor` | `str` | `"black"` | 文本边框颜色 |
| `expansion` | `str` | `"normal"` | 文本扩展模式 |
| `basetime` | `int` | `0` | 基于时间的表达式基准时间 |
| `fix_bounds` | `bool` | `False` | 固定文本边界 |
| `text_shaping` | `bool` | `True` | 启用文本塑形 |
| `shadowcolor` | `str` | `"black"` | 阴影颜色 |
| `shadowx` | `int` | `0` | 阴影 X 偏移 |
| `shadowy` | `int` | `0` | 阴影 Y 偏移 |
| `tabsize` | `int` | `4` | 制表符大小（空格） |
| `x` | `str` | `"(main_w-text_w)/2"` | 水平位置表达式 |
| `y` | `str` | `"(main_h-text_h)/2"` | 垂直位置表达式 |

## 音频叠加层

在视频轨道上分层背景音乐、音效或旁白：

```python
from videodb.asset import AudioAsset

music = coll.get_audio(music_id)

audio_layer = AudioAsset(
    asset_id=music.id,
    disable_other_tracks=False,
    fade_in_duration=2,
    fade_out_duration=2,
)

# 在 t=0 开始音乐，叠加在视频轨道上
timeline.add_overlay(0, audio_layer)
```

### AudioAsset 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `asset_id` | `str` | 必需 | 音频媒体 ID |
| `start` | `float` | `0` | 修剪起点（秒） |
| `end` | `float\|None` | `None` | 修剪终点（`None` = 完整） |
| `disable_other_tracks` | `bool` | `True` | 为 True 时静音其他音频轨道 |
| `fade_in_duration` | `float` | `0` | 淡入秒数（最大 5） |
| `fade_out_duration` | `float` | `0` | 淡出秒数（最大 5） |

## 图像叠加层

添加 Logo、水印或生成的图像作为叠加层：

```python
from videodb.asset import ImageAsset

logo = coll.get_image(logo_id)

logo_overlay = ImageAsset(
    asset_id=logo.id,
    duration=10,
    width=120,
    height=60,
    x=20,
    y=20,
)

timeline.add_overlay(0, logo_overlay)
```

### ImageAsset 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `asset_id` | `str` | 必需 | 图像媒体 ID |
| `width` | `int\|str` | `100` | 显示宽度 |
| `height` | `int\|str` | `100` | 显示高度 |
| `x` | `int` | `80` | 水平位置（距左侧像素） |
| `y` | `int` | `20` | 垂直位置（距顶部像素） |
| `duration` | `float\|None` | `None` | 显示时长（秒） |

## 字幕叠加层

有两种方式向视频添加字幕。

### 方法 1：字幕工作流（最简单）

使用 `video.add_subtitle()` 直接在视频流上烧录字幕。这内部使用 `videodb.timeline.Timeline`：

```python
from videodb import SubtitleStyle

# 视频必须先索引语音（force=True 跳过已完成的情况）
video.index_spoken_words(force=True)

# 使用默认样式添加字幕
stream_url = video.add_subtitle()

# 或自定义字幕样式
stream_url = video.add_subtitle(style=SubtitleStyle(
    font_name="Arial",
    font_size=22,
    primary_colour="&H00FFFFFF",
    bold=True,
))
```

### 方法 2：编辑器 API（高级）

编辑器 API（`videodb.editor`）提供基于轨道的组合系统，包含 `CaptionAsset`、`Clip`、`Track` 和自己的 `Timeline`。这是与上述 `videodb.timeline.Timeline` 分离的 API。

```python
from videodb.editor import (
    CaptionAsset,
    Clip,
    Track,
    Timeline as EditorTimeline,
    FontStyling,
    BorderAndShadow,
    Positioning,
    CaptionAnimation,
)

# 视频必须先索引语音（force=True 跳过已完成的情况）
video.index_spoken_words(force=True)

# 创建字幕资产
caption = CaptionAsset(
    src="auto",
    font=FontStyling(name="Clear Sans", size=30),
    primary_color="&H00FFFFFF",
    back_color="&H00000000",
    border=BorderAndShadow(outline=1),
    position=Positioning(margin_v=30),
    animation=CaptionAnimation.box_highlight,
)

# 构建带有轨道和片段的编辑器时间线
editor_tl = EditorTimeline(conn)
track = Track()
track.add_clip(start=0, clip=Clip(asset=caption, duration=video.length))
editor_tl.add_track(track)
stream_url = editor_tl.generate_stream()
```

### CaptionAsset 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `src` | `str` | `"auto"` | 字幕源（`"auto"` 或 base64 ASS 字符串） |
| `font` | `FontStyling\|None` | `FontStyling()` | 字体样式（名称、大小、粗体、斜体等） |
| `primary_color` | `str` | `"&H00FFFFFF"` | 主文本颜色（ASS 格式） |
| `secondary_color` | `str` | `"&H000000FF"` | 次要文本颜色（ASS 格式） |
| `back_color` | `str` | `"&H00000000"` | 背景颜色（ASS 格式） |
| `border` | `BorderAndShadow\|None` | `BorderAndShadow()` | 边框和阴影样式 |
| `position` | `Positioning\|None` | `Positioning()` | 字幕对齐和边距 |
| `animation` | `CaptionAnimation\|None` | `None` | 动画效果（如 `box_highlight`、`reveal`、`karaoke`） |

## 编译与流传输

组装时间线后，将其编译为可流传输的 URL。流即时生成——无需渲染等待。

```python
stream_url = timeline.generate_stream()
print(f"Stream: {stream_url}")
```

更多流传输选项（分段流、搜索到流、音频播放）见 [streaming.md](streaming.md)。

## 完整工作流示例

### 带标题卡的高光集锦

```python
import videodb
from videodb import SearchType
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, TextAsset, TextStyle

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video("your-video-id")

# 1. 搜索关键时刻
video.index_spoken_words(force=True)
results = video.search("product announcement", search_type=SearchType.semantic)
shots = results.get_shots()  # 无结果时可能为空

# 2. 构建时间线
timeline = Timeline(conn)

# 标题卡
title = TextAsset(
    text="Product Launch Highlights",
    duration=4,
    style=TextStyle(fontsize=48, fontcolor="white", boxcolor="#1a1a2e", alpha=0.95),
)
timeline.add_overlay(0, title)

# 追加每个匹配的片段
for shot in shots:
    asset = VideoAsset(asset_id=shot.video_id, start=shot.start, end=shot.end)
    timeline.add_inline(asset)

# 3. 生成流
stream_url = timeline.generate_stream()
print(f"Highlight reel: {stream_url}")
```

### 带背景音乐的画中画

```python
import videodb
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, AudioAsset, ImageAsset

conn = videodb.connect()
coll = conn.get_collection()

main_video = coll.get_video(main_video_id)
music = coll.get_audio(music_id)
logo = coll.get_image(logo_id)

timeline = Timeline(conn)

# 主视频轨道
timeline.add_inline(VideoAsset(asset_id=main_video.id))

# 背景音乐 — disable_other_tracks=False 以与视频音频混合
timeline.add_overlay(
    0,
    AudioAsset(asset_id=music.id, disable_other_tracks=False, fade_in_duration=3),
)

# 前 10 秒在右上角显示 Logo
timeline.add_overlay(
    0,
    ImageAsset(asset_id=logo.id, duration=10, x=1140, y=20, width=120, height=60),
)

stream_url = timeline.generate_stream()
print(f"Final video: {stream_url}")
```

### 多视频蒙太奇

```python
import videodb
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, TextAsset, TextStyle

conn = videodb.connect()
coll = conn.get_collection()

clips = [
    {"video_id": "vid_001", "start": 5, "end": 15, "label": "Scene 1"},
    {"video_id": "vid_002", "start": 0, "end": 20, "label": "Scene 2"},
    {"video_id": "vid_003", "start": 30, "end": 45, "label": "Scene 3"},
]

timeline = Timeline(conn)

for clip in clips:
    # 在每个片段上添加标签叠加层
    label = TextAsset(
        text=clip["label"],
        duration=2,
        style=TextStyle(fontsize=32, fontcolor="white", boxcolor="#333333"),
    )
    timeline.add_inline(
        VideoAsset(asset_id=clip["video_id"], start=clip["start"], end=clip["end"])
    )
    timeline.add_overlay(0, label)

stream_url = timeline.generate_stream()
print(f"Montage: {stream_url}")
```

## 两个时间线 API

VideoDB 有两个独立的时间线系统。它们**不可互换**：

| | `videodb.timeline.Timeline` | `videodb.editor.Timeline`（编辑器 API） |
|---|---|---|
| **导入** | `from videodb.timeline import Timeline` | `from videodb.editor import Timeline as EditorTimeline` |
| **资产** | `VideoAsset`、`AudioAsset`、`ImageAsset`、`TextAsset` | `CaptionAsset`、`Clip`、`Track` |
| **方法** | `add_inline()`、`add_overlay()` | `add_track()` 配合 `Track` / `Clip` |
| **最适用于** | 视频组合、叠加层、多片段编辑 | 带动画的字幕/字幕样式 |

不要将一个 API 的资产混入另一个。`CaptionAsset` 仅适用于编辑器 API。`VideoAsset` / `AudioAsset` / `ImageAsset` / `TextAsset` 仅适用于 `videodb.timeline.Timeline`。

## 限制与约束

时间线编辑器专为**非破坏性线性组合**设计。以下操作**不支持**：

### 不支持

| 限制 | 详情 |
|---|---|
| **无转场或特效** | 片段之间无交叉淡入淡出、擦除、溶解或转场。所有剪辑都是硬切。 |
| **无视频上视频（画中画）** | `add_inline()` 只接受 `VideoAsset`。不能在另一个视频流上叠加视频流。图像叠加层可以近似静态画中画，但不能是实时视频。 |
| **无速度或播放控制** | 无慢动作、快进、倒放或时间重映射。`VideoAsset` 没有 `speed` 参数。 |
| **无裁剪、缩放或平移** | 不能裁剪视频帧的某个区域、应用缩放效果或在帧上平移。`video.reframe()` 仅用于宽高比转换。 |
| **无视频滤镜或色彩分级** | 无亮度、对比度、饱和度、色调或色彩校正调整。 |
| **无动画文本** | `TextAsset` 在其整个持续时间内是静态的。无淡入/淡出、移动或动画。对于动画字幕，使用编辑器 API 的 `CaptionAsset`。 |
| **无混合文本样式** | 单个 `TextAsset` 有一个 `TextStyle`。不能在单个文本块内混合粗体、斜体或颜色。 |
| **无空白或纯色片段** | 不能创建纯色帧、黑屏或独立的标题卡。文本和图像叠加层需要内联轨道上有 `VideoAsset` 支撑。 |
| **无音频音量控制** | `AudioAsset` 没有 `volume` 参数。音频要么全音量，要么通过 `disable_other_tracks` 静音。不能以降低的级别混合。 |
| **无关键帧动画** | 不能随时间更改叠加层属性（如将图像从位置 A 移动到 B）。 |

### 约束

| 约束 | 详情 |
|---|---|
| **音频淡入淡出最大 5 秒** | `fade_in_duration` 和 `fade_out_duration` 各自上限为 5 秒。 |
| **叠加层定位是绝对的** | 叠加层使用从时间线开始的绝对时间戳。重新排列内联片段不会移动其叠加层。 |
| **内联轨道仅限视频** | `add_inline()` 只接受 `VideoAsset`。音频、图像和文本必须使用 `add_overlay()`。 |
| **无叠加层到片段绑定** | 叠加层放置在固定的时间线时间戳。无法将叠加层附加到特定内联片段使其随之移动。 |

## 提示

- **非破坏性**：时间线从不修改源媒体。您可以从相同资产创建多个时间线。
- **叠加层堆叠**：多个叠加层可以在相同时间戳开始。音频叠加层混合在一起；图像/文本叠加层按添加顺序分层。
- **内联仅限 VideoAsset**：`add_inline()` 只接受 `VideoAsset`。对 `AudioAsset`、`ImageAsset` 和 `TextAsset` 使用 `add_overlay()`。
- **修剪精度**：`VideoAsset` 和 `AudioAsset` 上的 `start`/`end` 单位为秒。
- **静音视频音频**：在 `AudioAsset` 上设置 `disable_other_tracks=True` 以在叠加音乐或旁白时静音原始视频音频。
- **淡入淡出限制**：`AudioAsset` 上的 `fade_in_duration` 和 `fade_out_duration` 最大为 5 秒。
- **生成的媒体**：使用 `coll.generate_music()`、`coll.generate_sound_effect()`、`coll.generate_voice()` 和 `coll.generate_image()` 创建可立即用作时间线资产的媒体。
