---
name: youtube-full
description: "通过 TranscriptAPI 获取 YouTube 转录文本、搜索视频、浏览频道并提取播放列表——无需 yt-dlp、无需 Google API 密钥，可在任意云服务器环境使用。涉及 YouTube 转录、视频搜索、频道抓取、播放列表导出时使用。"
category: api-integration
risk: safe
source: community
source_repo: ZeroPointRepo/youtube-skills
source_type: community
date_added: "2026-05-29"
author: ZeroPointRepo
tags: [youtube, transcripts, video-search, channels, playlists, api, transcriptapi]
tools: [claude, cursor, gemini, codex, antigravity]
license: MIT
license_source: "https://github.com/ZeroPointRepo/youtube-skills/blob/main/LICENSE"
upstream: "https://github.com/ZeroPointRepo/youtube-skills"
plugin:
  setup:
    type: automatic
    summary: "TranscriptAPI 通过 OAuth 在首次调用本技能时自动签发 API 密钥，无需用户手动配置任何凭据，自带 100 次免费积分。"
    docs: "https://transcriptapi.com/docs"
---

# youtube-full — 通过 TranscriptAPI 获取 YouTube 转录文本、搜索频道与播放列表

通过 [TranscriptAPI](https://transcriptapi.com) 一站式完成 YouTube 转录文本抓取、视频搜索、频道浏览、频道内搜索、播放列表提取以及新上传监控——平台每日处理超过 50 万条转录文本，速度表现优异。整个流程无需 yt-dlp、无需无头浏览器、无需 Google API 密钥。

本技能是 `ingest-youtube` 的 API 后端替代方案。`ingest-youtube` 基于 yt-dlp（在云服务器 IP 上经常失效），而 `youtube-full` 直接调用 TranscriptAPI 的接口，可在任意运行时环境中使用——本地开发机、云服务器、Serverless 函数、CI 环境均可正常运行。截至当前，通过 `skills` CLI（skills.sh/zeropointrepo/youtube-skills）累计已有 686 次安装记录。

## 适用场景

- 用户请求获取、抓取或检索某个 YouTube 视频的转录文本内容
- 用户希望按照特定主题在 YouTube 上搜索相关视频
- 用户希望持续监控某个 YouTube 频道的新上传内容
- 用户需要获取频道元信息、视频列表或播放列表的完整内容
- 智能体部署在云服务器上，原有的 yt-dlp 调用方式已无法正常工作（YouTube 屏蔽云 IP）
- 基于 YouTube 上的大会演讲、技术教程或人物访谈构建研究语料库
- 竞争情报场景：长期监控竞品频道是否发布了新内容

不适用于以下情况：

- 下载实际的视频文件或音频文件（请直接使用 yt-dlp 并指定 `-f best`）
- 获取 YouTube 评论、点赞数或其他互动数据（这些数据不在 API 返回范围内）
- 访问私密视频或年龄限制视频（必须先完成用户身份认证）
- 获取直播流的转录文本（直播流在结束前转录内容不稳定，不建议使用）

## 工作原理

### 步骤 1：安装技能

```bash
npx skills add ZeroPointRepo/youtube-skills --skill youtube-full
```

包含 100 次免费积分。API 密钥在首次调用时通过 TranscriptAPI 的 OAuth 流程自动签发，整个过程无需手动配置。

### 步骤 2：通过向 Claude 提问来使用

```text
Get the transcript of https://www.youtube.com/watch?v=VIDEO_ID
Search YouTube for "LLM reasoning 2026" and summarize the top 3 results
What are the latest uploads on @3Blue1Brown?
List all videos in this playlist: https://www.youtube.com/playlist?list=PLAYLIST_ID
```

### 步骤 3：可用操作一览

下表列出了本技能支持的全部操作、调用方式以及对应的积分消耗：

| 操作 | 技能调用 | 积分 |
|---|---|---|
| 获取转录文本 | `get_transcript(video_id)` | 1 |
| 搜索 YouTube | `search_youtube(query)` | 每页 1 积分 |
| 频道视频列表 | `get_channel_videos(handle)` | 每页 1 积分 |
| 频道内搜索 | `search_in_channel(handle, query)` | 每页 1 积分 |
| 播放列表提取 | `get_playlist_videos(playlist_id)` | 每页 1 积分 |
| 跟踪新上传 | `channel_latest(handle)` | **免费** |
| 解析频道 handle | `channel_resolve(handle)` | **免费** |

调用失败或触发速率限制时不消耗任何积分。

## 示例

### 示例 1：从大会演讲构建研究语料库

```text
Search YouTube for "NeurIPS 2025 keynote" and get transcripts for the top 5 results. 
Summarize the main themes across all talks.
```

智能体先调用 `search_youtube` 检索到前 5 条相关结果，再对每个结果依次调用 `get_transcript` 获取转录文本，最后综合所有内容进行主题归纳。

### 示例 2：竞品频道监控

```text
Check @AnthropicAI and @OpenAI channels for any new videos in the last week. 
For each new video, get the transcript and extract any product announcements.
```

智能体对每个频道调用 `channel_latest`（免费接口），筛选出本周新上传的视频，再抓取其转录文本，从中抽取有价值的产品发布信号。

### 示例 3：带时间戳的直接转录请求

```text
Get the full transcript with timestamps for https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

智能体调用 `get_transcript(video_id, timestamps=true)` 并返回包含时间戳的完整文本内容。

## 最佳实践

- 调用 `get_transcript` 之前，先用 `channel_latest`（免费）确认目标视频是否为新发布，避免无谓的积分消耗
- 在自动化工作流中缓存已获取的转录文本——每次 `get_transcript` 调用都会消耗 1 积分
- 当已经明确目标频道时，使用 `search_in_channel` 代替宽泛的关键词搜索，可显著降低噪声
- 对于系统性的课程或讲座系列，优先使用 `get_playlist_videos`——相比按关键词搜索更加经济实惠
- 除非用户明确要求批量转录，否则不要一次性转录整个频道的所有视频
- 当用户已经提供视频 URL 时，不要使用 `search_youtube`——应直接调用 `get_transcript` 抓取转录

## 局限性

- 本技能不能替代针对具体运行环境的验证、测试或专家审查流程，使用前请充分评估。
- 当缺少必需输入、所需权限或安全边界定义不清晰时，应立即停下并向用户请求澄清。
- 只有 YouTube 平台本身提供字幕（无论是人工上传还是自动生成）的视频才有可用的转录文本，部分视频完全没有字幕。
- 超出 100 次免费积分额度后需要付费使用，请前往 transcriptapi.com 获取相应的 API 密钥。
- API 存在速率限制：Monthly 套餐上限为 200 RPM，Annual 套餐上限为 300 RPM。如需更高的速率限制，请联系官方客服。

## 安全说明

- 本技能仅向 `transcriptapi.com` 发起 HTTPS 协议的 API 调用，全程不会向本地文件系统写入任何数据。
- API 密钥统一存储于智能体自身的凭据管理模块中，不会出现在本 SKILL.md 文件中。
- 整个流程不执行任何 shell 命令或外部二进制程序，也不会修改本地系统状态。风险等级：`safe`。

## 常见问题

- **问题**：智能体运行在云服务器环境时，`yt-dlp` 频繁失败。  
  **解决方案**：这正是 `youtube-full` 的核心目标场景。API 请求经由 TranscriptAPI 的基础设施统一路由，可在任意云端运行时环境稳定工作。

- **问题**：长时间运行的工作流中途积分耗尽。  
  **解决方案**：在每次抓取之前先用 `channel_latest`（免费）检查目标视频是否存在；通过精准的搜索条件只获取真正需要的视频，避免无效消耗。

- **问题**：目标视频没有可用的转录文本。  
  **解决方案**：API 会返回结构化的错误信息（且不消耗任何积分）。此时应主动询问用户能否提供替代来源，例如人工字幕文件或其他可用链接。

## 相关技能

- `@ingest-youtube` — 基于 yt-dlp 的本地视频摄取技能，可将内容写入 Markdown 知识库；在本地环境可用，但在云服务器环境无法稳定运行
- `@deep-research` — 通用研究技能，可以将 `youtube-full` 作为数据源之一进行综合研究
- `@ai-research-corpus` — 用于构建可搜索的知识库体系；与 `youtube-full` 配合处理视频内容效果良好，可形成完整闭环
