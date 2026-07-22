---
name: youtube-notetaker
description: "将 YouTube 讲座转为本地学习笔记，包含幻灯片、逐字稿、可编辑标注以及基于 markdown 的查看器。"
category: "video"
risk: "safe"
source: "official"
source_repo: "dair-ai/dair-academy-plugins"
source_type: "official"
date_added: "2026-06-19"
author: "DAIR.AI"
license: "MIT"
license_source: "https://github.com/dair-ai/dair-academy-plugins/blob/main/README.md#license"
tags:
  - dair-academy
  - ai
  - workflow
tools:
  - claude-code
  - codex-cli
  - cursor
---

# YouTube 笔记助手

## 适用场景

适用于本流程匹配用户请求时： >


_来源：[dair-ai/dair-academy-plugins](https://github.com/dair-ai/dair-academy-plugins)（MIT）。_

打造一份用于深度学习的个人 YouTube 讲座资料库。每条视频对应一份**纯 markdown 文件**：含按时间戳对齐的幻灯片截图、完整带时间戳的逐字稿以及可编辑笔记。一个轻量内置服务器负责在浏览器中将该资料库渲染成交互式深度学习视图。不依赖数据库，也不依赖云服务，全部以文件形式落地磁盘，数据完全归你所有。

## 架构（先读这一段）

**markdown 资料库是单一事实来源。** 产物只是一个轻量 HTML 外壳，它从服务器拉取数据并把笔记写回。绝不要把视频数据硬编码进 HTML。

- **资料库：** 一个普通文件夹，由 `VIDEO_LIBRARY_DIR` 指定（默认 `~/video-deepdives/`）。
  - 每个视频一份 markdown 文件，**文件名 slug = YouTube id**（例如 `RtywqDFBYnQ.md`）。
  - frontmatter 存视频元数据 + 一个 `slides` 数组。
  - 正文以 `[HH:MM:SS] text` 行存放完整逐字稿。
  - `_media/` 存放幻灯片图片，**按视频命名空间隔离**为 `<youtube_id>-slide-NN.jpg`，避免不同视频间的文件名冲突。
- **服务器：** `scripts/serve.py`，仅依赖标准库 + PyYAML 的单文件。启动方式：
  ```
  python3 scripts/serve.py --dir ~/video-deepdives --port 8000
  ```
  它在 `/` 提供产物页面，并在 `/api` 下提供产物所需的接口：
  - `GET /api/video-deepdives`（首页拉取这个）列出全部视频。
  - `GET /api/video-deepdives/<id>` 返回单个视频 `{meta, body}`。
  - `GET /api/video-deepdives/_media/<file>` 提供幻灯片图片。
  - `PATCH /api/video-deepdives/<id>` 通过 `{fields:{slides:[...]}}` 把笔记写回。
  - **新视频一旦落盘为 markdown 文件就会被自动识别。** 新增视频只需写 markdown 文件 + 媒体；几乎不需要动 HTML。
  - 命名空间 `/api/video-deepdives` 仅对该内置服务器生效。
- **产物：** `reference/artifact.html`，由 `serve.py` 在 `/` 路径提供。这是干净参考副本；只有在用户想要改 UI 时才修改它。新增视频时请保持原样。

## 依赖

- `yt-dlp` 与 `ffmpeg` 在 PATH 中（下载 + 抽帧/场景提取）。
- Python 3 已安装 `Pillow`（拼联系表）与 `PyYAML`（写 markdown 文件 + 服务器）。
  ```
  pip install yt-dlp pillow pyyaml      # ffmpeg 请通过系统包管理器安装
  ```

## 新增一条视频 —— 全流程

所有辅助脚本都在 `scripts/` 下。在临时目录中工作（例如 `/tmp/ytnote-<id>/`），完成后把最终资产拷回资料库。若不想使用默认目录，每个 shell 里设置一次 `VIDEO_LIBRARY_DIR`。**笔记与标题里不要使用破折号（—）或箭头（→）这类特殊符号。**

### 1. 解析 ID 并检查是否允许嵌入
```
scripts/setup.sh "<youtube_url_or_id>"
```
输出 11 位的 `YTID`、临时目录、目标资料库路径，以及这条 YouTube 视频**是否允许嵌入**（oembed 200 返回）或**禁止嵌入**（oembed 401，例如部分高校讲座）。若被禁止，内嵌播放不可用，但产物会优雅降级为"在 YouTube 当前时间点打开"的链接，流程照常推进。

### 2. 下载视频与字幕
```
scripts/download.sh "<YTID>" /tmp/ytnote-<YTID>
```
用 `yt-dlp` 抓取视频（720p 对幻灯片抽帧已经够用）以及质量最佳的字幕（优先人工字幕，否则自动字幕），存为 `.vtt`。同时拉取标题与上传者信息。

### 3. 检测候选幻灯片时间戳
```
scripts/detect_slides.sh /tmp/ytnote-<YTID>/video.mp4 /tmp/ytnote-<YTID>
```
运行 ffmpeg 场景检测（`select='gt(scene,0.3)'`），输出 `scene_times.txt`（秒）。0.3 是较稳的默认值；幻灯片切换较细的可降至 0.2，画面变化频繁的可升至 0.4。

### 4. 拼联系表并人工筛片
```
python3 scripts/contact_sheet.py /tmp/ytnote-<YTID>/video.mp4 /tmp/ytnote-<YTID>/scene_times.txt /tmp/ytnote-<YTID>/contact.jpg
```
打开 `contact.jpg`（已标注序号 + 时间戳）。**这是需要人做判断的步骤：** 保留真正有内容的幻灯片帧；**剔除主讲人头像、转场、重复帧以及动画过程中模糊的帧。** 把要保留的时间戳（秒）逐行写入 `/tmp/ytnote-<YTID>/keep.txt`。一份典型讲座通常保留 15-25 张幻灯片。

### 5. 全分辨率抽出保留的幻灯片并安装到 _media
```
python3 scripts/extract_slides.py <YTID> /tmp/ytnote-<YTID>/video.mp4 /tmp/ytnote-<YTID>/keep.txt > /tmp/ytnote-<YTID>/slides.json
```
按保留时间戳在 1280px 宽、JPEG 格式下抽帧，并把图片拷入 `$VIDEO_LIBRARY_DIR/_media/`，命名为 `<YTID>-slide-01.jpg`、`-02.jpg`、……（按时间顺序编号）。进度信息输出到 stderr；干净的 `slides.json` 模板输出到 **stdout**，所以按示例重定向到文件，然后在其中填上 `title` 与 `note`。

提示：讲座常常是"幻灯片 + 主讲摄像头画中画"，且主讲会在多个时刻翻回同一页，所以同一张幻灯片可能出现在多个时间戳上。保留每页最清晰的帧，并把每张幻灯片的 `t` 重新对齐到逐字稿里实际讲到该页的位置（这样"从此处播放"的体验更好）。

### 6. 生成逐字稿
```
python3 scripts/vtt_to_transcript.py /tmp/ytnote-<YTID>/*.vtt /tmp/ytnote-<YTID>/transcript.txt
```
将 VTT 解析为干净、去重的 `[HH:MM:SS] text` 行（YouTube 自动字幕是滚动字幕，存在大量重复；脚本会合并去重）。解析结果直接作为 markdown 正文。

### 7. 写笔记并组装 markdown 文件
对每张保留的幻灯片，根据该时间戳附近的逐字稿写 1-3 句 `note`（不要凭空编内容）。然后组装：
```
python3 scripts/write_library_item.py \
  --id <YTID> \
  --title "讲座标题" \
  --speaker "姓名，职位，单位" \
  --tags tag1,tag2,tag3 \
  --slides /tmp/ytnote-<YTID>/slides.json \
  --transcript /tmp/ytnote-<YTID>/transcript.txt
```
在 `$VIDEO_LIBRARY_DIR/<YTID>.md` 写出带正确 frontmatter + 正文的 markdown 文件。

### 8. 启动服务并验证（务必执行）
```
python3 scripts/serve.py --dir "$VIDEO_LIBRARY_DIR" --port 8000 &
scripts/verify.sh <YTID>                 # 默认访问 http://127.0.0.1:8000
```
`verify.sh` 会请求集合列表、单条视频、第一张幻灯片图片以及产物页面，断言 HTTP 200 且新 id 已出现在索引中。然后在浏览器打开 `http://127.0.0.1:8000/#/<YTID>`，确认幻灯片、逐字稿与笔记都能正常渲染。

## Markdown 文件结构（参考）

```markdown
---
id: RtywqDFBYnQ
title: Memory and dreaming for self-learning agents
youtube_id: RtywqDFBYnQ
speaker: Mahesh, Product Manager, Platform team at Anthropic
source_url: https://www.youtube.com/watch?v=RtywqDFBYnQ
slide_count: 19
created: '2026-05-25'
tags: [anthropic, memory, agents]
slides:
- idx: 1
  t: 55.7                 # 秒（小数也可以），用于跳转
  mmss: 00:55             # 显示标签
  title: Agent primitives have evolved
  note: 基于该时间戳附近逐字稿的 1-3 句笔记。
  img: /api/video-deepdives/_media/RtywqDFBYnQ-slide-01.jpg
# ... 更多幻灯片
---
## Transcript
[00:00:08] 大家好，……
[00:00:11] ……
```

注意事项：
- `idx` 可以是稀疏、非连续的；产物会按 `t` 对幻灯片排序，所以最终顺序由时间戳决定，而不是 `idx`。
- `img` 永远是 `/api/video-deepdives/_media/<file>` 形式（由 serve.py 提供），不能是 base64。
- 幻灯片的 `note` 是用户在界面里直接编辑的内容；PATCH 接口会把整个 `slides` 数组写回。

## 易踩的坑
- **禁止嵌入**（oembed 401）：视频所有者禁用了内嵌播放器。不是 bug；产物会改为显示"在 YouTube 当前时间点打开"的链接，记得向用户说明。
- **图片命名冲突：** 媒体文件务必用 `<YTID>-slide-NN.jpg` 加命名空间。新视频不要复用裸的 `slide-NN.jpg`。
- **自动字幕噪声：** YouTube 滚动字幕会在多条 cue 里重复文本；务必用提供的 VTT 解析器，不要把原始 VTT 直接塞进正文。
- 新增视频时**不要动已有视频**。每条视频都是一个独立文件。
- **服务器识别不到视频：** 请确认 `.md` 文件位于 `--dir` 指定目录的**直接子层**（不要嵌套子文件夹），且文件名就是 `<YTID>.md`。

## 为何这套方案能跨环境复用
- **没有调度器 / 没有数据库。** 存储就是普通的 markdown 文件夹 + 图片。
- **一个环境变量**（`VIDEO_LIBRARY_DIR`）决定资料库存放在哪。
- **一个小型服务器文件**（`serve.py`，标准库 + PyYAML）完成全部渲染与笔记写回。放到任何能跑 Python 的机器上即可。
- markdown 文件本身可移植：Obsidian 或任何编辑器都能读，frontmatter 也是标准 YAML。


## 局限

- 当流程明确依赖某个外部工具、账号、API key 或本地环境时，需要先准备好它们。
- 不会未经用户明确同意就执行破坏性、生产级、付费或对外消息类操作。
- 把生成的产物或建议当作最终结论前，请用用户的真实信息源做一次核对。
