---
name: web-media-getter
description: "通过单一查询跨多个免费图片 / 视频 / GIF 接口（素材库 + 历史档案 + GIF 引擎），返回规范化、附带许可证标签的结果，并可选地进行 Top-K 下载与署名 sidecar 落地。是本地语义搜索与生成式媒体在检索侧的对应能力。涉及媒体检索、图片下载、视频下载、GIF、素材库、归档、署名、媒体获取、免费素材时使用。"
risk: safe
source: community
source_type: community
source_repo: connerkward/web-media-getter-skill
date_added: "2026-06-16"
author: Conner K Ward
license: MIT
tags:
  - media
  - images
  - video
  - gif
  - stock
  - archival
  - attribution
tools:
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
---
## 适用场景

需要一张真实或历史档案类照片 / 片段（主视觉、贴图、参考图、历史影像），或需要一个表情反应 / 动图 GIF，而非生成式内容时使用 —— 一次查询横向扫描多个免费图片 / 视频 / GIF 来源，并下载附带许可证标签的结果。

_来源：[connerkward/web-media-getter-skill](https://github.com/connerkward/web-media-getter-skill)（MIT）。_

# web-media

一次扇出查询多个免费图片 / 视频来源，返回规范化的结果列表，可选下载 Top-K 并附带署名 sidecar。脚本零依赖、仅用标准库。

**脚本：** `webmedia.py`（位于本目录）。**密钥：** `PEXELS_API_KEY`、`PIXABAY_API_KEY`
配置于 `central/.env`（可选 —— 5 个免密钥来源无需配置即可使用）。

## 数据来源

| 来源 | 是否需要密钥 | 最适合 | 媒体类型 |
|--------|------|----------|-------|
| openverse | 无 | CC 网络图片（Flickr、博物馆） | image |
| wikimedia | 无 | 事实性 / 历史 / 地标照片 | image |
| internetarchive | 无 | **历史/档案**图像 + 影片 | image, video |
| loc | 无 | 美国历史版画 / 照片 | image |
| nasa | 无 | 太空影像 + 视频 | image, video |
| pexels | 免费密钥 | 现代素材图 + **短视频片段** | image, video |
| pixabay | 免费密钥 | 现代摄影 / 插画 + **短片段** | image, video |
| klipy | 免费密钥 | **GIF** —— 推荐（免费、无限制、Tenor 平替） | gif |
| giphy | 免费密钥 | **GIF** —— 库最大（生产密钥需审批） | gif |

GIF 来源仅在指定 `--type gif` 时触发。密钥：`KLIPY_API_KEY`、`GIPHY_API_KEY`
配置于 `central/.env`。（Tenor 适配器已移除 —— Google 于 2026-06-30 终止该 API。）
**klipy** 是首选（免费 + 无限制）；
其适配器 **未经验证 —— 假定请求 / 响应与 Tenor 兼容**；
配置密钥时请按 docs.klipy.com 核查。`webmedia.py "shrug" --type gif --count 6 --json`

## 用法

```bash
webmedia.py "1950s street scene" --type image --count 8 --json
webmedia.py "rocket launch" --type video --source nasa,internetarchive
webmedia.py "car factory 1930s" --source all --download --out /tmp/cars
```

- `--source all`（默认） | `nokey`（仅免密钥来源） | 逗号分隔列表（`wikimedia,pexels`）
- `--type image|video` · `--count N` · `--json` · `--download --out DIR`
- `--download` 抓取每条结果的直链媒体 URL，并写入 `attribution.json`
  （含 source、author、license、url、page_url），与文件放在同一目录。

## 记录字段

`{source, title, url, thumb, dl, page_url, author, license, w, h, type}` ——
`dl` 为可直接下载的媒体 URL（仅存在页面时为 None）。

## 视频注意事项（重要）

档案来源（Internet Archive、Europeana、LoC）托管 **整部影片 / 纪录片**，
而非单镜头。因此：
- **现代单片段** → `pexels` / `pixabay`（天生就是短片段，直链 MP4）。一次搞定。
- **历史单镜头** → 先在此处获取 IA 影片，再抽取目标镜头：
  - **Twelve Labs** Marengo 检索（免费 600 分钟）—— 传入 IA 公开 MP4 URL，
    获得 "car on assembly line" 对应的时间戳定位，用 ffmpeg 裁剪。语义化、成本低。
  - 或使用 **PySceneDetect**（免费、本地）将影片切分为镜头，再用 `muser` 技能中的
    CLIP 给关键帧排序。全程离线。

## 音频：freesound + 音频 QA

`webmedia.py` 面向图片 / 视频。**音效**（真实、CC 授权）以及 **音频评判**
（Claude 无法听音）这两个场景，另有同源脚本位于 `central/scripts/`：

- **`freesound-fetch.py "<query>" [count] [max_sec] [out_dir]`** —— 搜索 freesound.org
  并下载短时长的高品质 MP3 预览。每个文件打印一行 JSON，含 `license` / `user`
  便于署名。密钥：`FREESOUND_API_KEY` 配置于 `central/.env`
  （基于 token 的读取；完整原文件需 OAuth —— 预览足以满足音效需求）。
- **`audio-judge.py <file> "<target>"`** —— 将片段发送至 OpenAI 的 `gpt-audio`
  （原生音频模型），返回 JSON `{heard, score, matches, suggestion}`，从而形成
  "生成 / 拉取 → 评判 → 迭代" 的循环。自动从 `.env` 读取真实的 `sk-` `OPENAI_API_KEY`
  （忽略本地 `lm-studio` stub 环境变量）。对不足 2 秒的片段会补零静音，
  避免语音微调的模型拒绝处理。**注意：** 它能可靠地 *描述* 音频并过滤明显不匹配项，
  但对于 "刺耳" 这类主观品质的判断并不可信 —— 它几乎把任何蜂鸣都标成 "尖锐 / 高频"。
  把它当作粗筛工具，不要让它直接决定最终美学判断；务必人工听感复核。

## 在整体中的定位

这是 **互联网检索** 能力 —— 与 `muser`（本地语义搜索）和 `fal`（生成）并列。
未来的 `media` 路由器会同时扇出这三路，按相关性（CLIP）排序候选，
将美学方向的成片交给 `lookdev`。除非模型在没有该路由器时已被证明会路由错误，
否则不要急于实现。

## 局限

- 结果取决于第三方接口的可用性、配额、凭证以及许可证元数据质量。
- 商用或公开发布前，仍需人工复核许可证标签与署名字段。
- 相关性排序能找出看起来合理的素材，但最终美学契合度、品牌安全与音频适用性仍需人工把控。
