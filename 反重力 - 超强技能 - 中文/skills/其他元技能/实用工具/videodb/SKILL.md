---
name: videodb
description: 视频和音频感知、索引与编辑。摄入文件/URL/直播流，构建视觉/语音索引，带时间戳搜索，编辑时间线，添加叠加层/字幕，生成媒体，创建实时警报。触发词：视频处理、视频索引、视频搜索、字幕生成、时间线编辑、直播流处理、桌面录制、video editing、transcription、video search
category: media
risk: safe
source: community
tags: "[video, editing, transcription, subtitles, search, streaming, ai-generation, media, live-streams, desktop-capture]"
date_added: "2026-02-27"
allowed-tools: Read Grep Glob Bash(python:*)
argument-hint: "[task description]"
---

# VideoDB 技能

**视频、直播流和桌面会话的感知 + 记忆 + 操作。**

在以下情况使用此技能：

## 何时使用
- 需要对文件、URL、桌面会话或直播流进行视频或音频感知、索引、搜索或时间线编辑。
- 任务涉及时间戳、可搜索证据、字幕、片段、叠加层或实时监控警报。
- 您希望用一个工作流整合摄入、理解、检索和媒体操作。

## 1) 桌面感知
- 启动/停止**桌面会话**，捕获**屏幕、麦克风和系统音频**
- 流式传输**实时上下文**并存储**情景会话记忆**
- 对屏幕上所说内容和发生的事情运行**实时警报/触发器**
- 生成**会话摘要**、可搜索时间线和**可播放证据链接**

## 2) 视频摄入 + 流式传输
- 摄入**文件或 URL**并返回**可播放的网络流链接**
- 转码/标准化：**编解码器、比特率、帧率、分辨率、宽高比**

## 3) 索引 + 搜索（时间戳 + 证据）
- 构建**视觉**、**语音**和**关键词**索引
- 搜索并返回带有**时间戳**和**可播放证据**的精确时刻
- 从搜索结果自动创建**片段**

## 4) 时间线编辑 + 生成
- 字幕：**生成**、**翻译**、**烧录**
- 叠加层：**文本/图像/品牌标识**、动态字幕
- 音频：**背景音乐**、**旁白**、**配音**
- 通过**时间线操作**进行程序化组合和导出

## 5) 直播流 (RTSP) + 监控
- 连接**RTSP/直播源**
- 运行**实时视觉和语音理解**，为监控工作流发出**事件/警报**

---

## 常见输入
- 本地**文件路径**、公开**URL**或**RTSP URL**
- 桌面捕获请求：**启动 / 停止 / 摘要会话**
- 所需操作：获取理解上下文、转码规格、索引规格、搜索查询、片段范围、时间线编辑、警报规则

## 常见输出
- **流 URL**
- 带有**时间戳**和**证据链接**的搜索结果
- 生成的资产：字幕、音频、图像、片段
- 直播流的**事件/警报载荷**
- 桌面**会话摘要**和记忆条目

---

## 规范提示词（示例）
- "Start desktop capture and alert when a password field appears."
- "Record my session and produce an actionable summary when it ends."
- "Ingest this file and return a playable stream link."
- "Index this folder and find every scene with people, return timestamps."
- "Generate subtitles, burn them in, and add light background music."
- "Connect this RTSP URL and alert when a person enters the zone."

## 运行 Python 代码

在运行任何 VideoDB 代码之前，切换到项目目录并加载环境变量：

```python
from dotenv import load_dotenv
load_dotenv(".env")

import videodb
conn = videodb.connect()
```

这会从以下位置读取 `VIDEO_DB_API_KEY`：
1. 环境变量（如果已导出）
2. 当前目录中项目的 `.env` 文件

如果密钥缺失，`videodb.connect()` 会自动抛出 `AuthenticationError`。

当简短的内联命令可行时，不要编写脚本文件。

编写内联 Python（`python -c "..."`）时，始终使用格式正确的代码——使用分号分隔语句并保持可读性。对于超过约3条语句的内容，改用 heredoc：

```bash
python << 'EOF'
from dotenv import load_dotenv
load_dotenv(".env")

import videodb
conn = videodb.connect()
coll = conn.get_collection()
print(f"Videos: {len(coll.get_videos())}")
EOF
```

## 设置

当用户要求"setup videodb"或类似内容时：

### 1. 安装 SDK

```bash
pip install "videodb[capture]" python-dotenv
```

如果 `videodb[capture]` 在 Linux 上失败，请安装不带 capture 扩展的版本：

```bash
pip install videodb python-dotenv
```

### 2. 配置 API 密钥

用户必须使用**任一**方法设置 `VIDEO_DB_API_KEY`：

- **在终端中导出**（启动 Claude 之前）：`export VIDEO_DB_API_KEY=your-key`
- **项目 `.env` 文件**：在项目的 `.env` 文件中保存 `VIDEO_DB_API_KEY=your-key`

在 https://console.videodb.io 获取免费 API 密钥（50次免费上传，无需信用卡）。

**不要**自行读取、写入或处理 API 密钥。始终让用户设置它。

## 快速参考

### 上传媒体

```python
# URL
video = coll.upload(url="https://example.com/video.mp4")

# YouTube
video = coll.upload(url="https://www.youtube.com/watch?v=VIDEO_ID")

# 本地文件
video = coll.upload(file_path="/path/to/video.mp4")
```

### 转录 + 字幕

```python
# force=True 跳过视频已索引时的错误
video.index_spoken_words(force=True)
text = video.get_transcript_text()
stream_url = video.add_subtitle()
```

### 视频内搜索

```python
from videodb.exceptions import InvalidRequestError

video.index_spoken_words(force=True)

# search() 在未找到结果时抛出 InvalidRequestError。
# 始终用 try/except 包装，并将"No results found"视为空结果。
try:
    results = video.search("product demo")
    shots = results.get_shots()
    stream_url = results.compile()
except InvalidRequestError as e:
    if "No results found" in str(e):
        shots = []
    else:
        raise
```

### 场景搜索

```python
import re
from videodb import SearchType, IndexType, SceneExtractionType
from videodb.exceptions import InvalidRequestError

# index_scenes() 没有 force 参数——如果场景索引
# 已存在，它会抛出错误。从错误中提取现有索引 ID。
try:
    scene_index_id = video.index_scenes(
        extraction_type=SceneExtractionType.shot_based,
        prompt="Describe the visual content in this scene.",
    )
except Exception as e:
    match = re.search(r"id\s+([a-f0-9]+)", str(e))
    if match:
        scene_index_id = match.group(1)
    else:
        raise

# 使用 score_threshold 过滤低相关性噪音（推荐：0.3+）
try:
    results = video.search(
        query="person writing on a whiteboard",
        search_type=SearchType.semantic,
        index_type=IndexType.scene,
        scene_index_id=scene_index_id,
        score_threshold=0.3,
    )
    shots = results.get_shots()
    stream_url = results.compile()
except InvalidRequestError as e:
    if "No results found" in str(e):
        shots = []
    else:
        raise
```

### 时间线编辑

**重要：** 在构建时间线之前始终验证时间戳：
- `start` 必须 >= 0（负值会被静默接受但产生损坏的输出）
- `start` 必须 < `end`
- `end` 必须 <= `video.length`

```python
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, TextAsset, TextStyle

timeline = Timeline(conn)
timeline.add_inline(VideoAsset(asset_id=video.id, start=10, end=30))
timeline.add_overlay(0, TextAsset(text="The End", duration=3, style=TextStyle(fontsize=36)))
stream_url = timeline.generate_stream()
```

### 转码视频（分辨率/质量更改）

```python
from videodb import TranscodeMode, VideoConfig, AudioConfig

# 服务端更改分辨率、质量或宽高比
job_id = conn.transcode(
    source="https://example.com/video.mp4",
    callback_url="https://example.com/webhook",
    mode=TranscodeMode.economy,
    video_config=VideoConfig(resolution=720, quality=23, aspect_ratio="16:9"),
    audio_config=AudioConfig(mute=False),
)
```

### 重构宽高比（用于社交平台）

**警告：** `reframe()` 是一个缓慢的服务端操作。对于长视频，可能需要几分钟并可能超时。最佳实践：
- 尽可能使用 `start`/`end` 限制为短片段
- 对于完整长度的视频，使用 `callback_url` 进行异步处理
- 先在 `Timeline` 上修剪视频，然后对较短的结果进行重构

```python
from videodb import ReframeMode

# 始终优先重构短片段：
reframed = video.reframe(start=0, end=60, target="vertical", mode=ReframeMode.smart)

# 完整长度视频的异步重构（返回 None，结果通过 webhook）：
video.reframe(target="vertical", callback_url="https://example.com/webhook")

# 预设："vertical" (9:16), "square" (1:1), "landscape" (16:9)
reframed = video.reframe(start=0, end=60, target="square")

# 自定义尺寸
reframed = video.reframe(start=0, end=60, target={"width": 1280, "height": 720})
```

### 生成媒体

```python
image = coll.generate_image(
    prompt="a sunset over mountains",
    aspect_ratio="16:9",
)
```

## 错误处理

```python
from videodb.exceptions import AuthenticationError, InvalidRequestError

try:
    conn = videodb.connect()
except AuthenticationError:
    print("Check your VIDEO_DB_API_KEY")

try:
    video = coll.upload(url="https://example.com/video.mp4")
except InvalidRequestError as e:
    print(f"Upload failed: {e}")
```

### 常见陷阱

| 场景 | 错误消息 | 解决方案 |
|------|----------|----------|
| 索引已索引的视频 | `Spoken word index for video already exists` | 使用 `video.index_spoken_words(force=True)` 跳过已索引的情况 |
| 场景索引已存在 | `Scene index with id XXXX already exists` | 使用 `re.search(r"id\s+([a-f0-9]+)", str(e))` 从错误中提取现有的 `scene_index_id` |
| 搜索未找到匹配 | `InvalidRequestError: No results found` | 捕获异常并视为空结果（`shots = []`） |
| 重构超时 | 在长视频上无限期阻塞 | 使用 `start`/`end` 限制片段，或传递 `callback_url` 进行异步处理 |
| 时间线上的负时间戳 | 静默产生损坏的流 | 在创建 `VideoAsset` 之前始终验证 `start >= 0` |
| `generate_video()` / `create_collection()` 失败 | `Operation not allowed` 或 `maximum limit` | 计划限制的功能——告知用户计划限制 |

## 附加文档

参考文档位于此 SKILL.md 文件相邻的 `reference/` 目录中。如需定位，请使用 Glob 工具。

- [reference/api-reference.md](reference/api-reference.md) - 完整的 VideoDB Python SDK API 参考
- [reference/search.md](reference/search.md) - 视频搜索深入指南（语音和基于场景）
- [reference/editor.md](reference/editor.md) - 时间线编辑、资产和组合
- [reference/streaming.md](reference/streaming.md) - HLS 流式传输和即时播放
- [reference/generative.md](reference/generative.md) - AI 驱动的媒体生成（图像、视频、音频）
- [reference/rtstream.md](reference/rtstream.md) - 直播流摄入工作流 (RTSP/RTMP)
- [reference/rtstream-reference.md](reference/rtstream-reference.md) - RTStream SDK 方法和 AI 管道
- [reference/capture.md](reference/capture.md) - 桌面捕获工作流
- [reference/capture-reference.md](reference/capture-reference.md) - 捕获 SDK 和 WebSocket 事件
- [reference/use-cases.md](reference/use-cases.md) - 常见视频处理模式和示例

## 屏幕录制（桌面捕获）

使用 `ws_listener.py` 在录制会话期间捕获 WebSocket 事件。桌面捕获仅支持 **macOS**。

### 快速开始

1. **启动监听器**：`python scripts/ws_listener.py &`
2. **获取 WebSocket ID**：`cat /tmp/videodb_ws_id`
3. **运行捕获代码**（完整工作流见 reference/capture.md）
4. **事件写入**：`/tmp/videodb_events.jsonl`

### 查询事件

```python
import json
events = [json.loads(l) for l in open("/tmp/videodb_events.jsonl")]

# 获取所有转录文本
transcripts = [e["data"]["text"] for e in events if e.get("channel") == "transcript"]

# 获取最近5分钟的视觉描述
import time
cutoff = time.time() - 300
recent_visual = [e for e in events 
                 if e.get("channel") == "visual_index" and e["unix_ts"] > cutoff]
```

### 实用脚本

- [scripts/ws_listener.py](scripts/ws_listener.py) - WebSocket 事件监听器（转储到 JSONL）

完整捕获工作流见 [reference/capture.md](reference/capture.md)。

**当 VideoDB 支持该操作时，不要使用 ffmpeg、moviepy 或本地编码工具。** 以下操作均由 VideoDB 服务端处理——修剪、合并片段、叠加音频或音乐、添加字幕、文本/图像叠加层、转码、分辨率更改、宽高比转换、针对平台要求调整大小、转录和媒体生成。仅对 reference/editor.md 中限制下列出的操作回退到本地工具（转场、速度更改、裁剪/缩放、色彩分级、音量混合）。

### 何时使用什么

| 问题 | VideoDB 解决方案 |
|------|------------------|
| 平台拒绝视频宽高比或分辨率 | `video.reframe()` 或带 `VideoConfig` 的 `conn.transcode()` |
| 需要为 Twitter/Instagram/TikTok 调整视频大小 | `video.reframe(target="vertical")` 或 `target="square"` |
| 需要更改分辨率（如 1080p → 720p） | 带 `VideoConfig(resolution=720)` 的 `conn.transcode()` |
| 需要在视频上叠加音频/音乐 | `Timeline` 上的 `AudioAsset` |
| 需要添加字幕 | `video.add_subtitle()` 或 `CaptionAsset` |
| 需要合并/修剪片段 | `Timeline` 上的 `VideoAsset` |
| 需要生成旁白、音乐或音效 | `coll.generate_voice()`, `generate_music()`, `generate_sound_effect()` |

## 仓库

https://github.com/video-db/skills

**维护者：** [VideoDB](https://github.com/video-db)

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
