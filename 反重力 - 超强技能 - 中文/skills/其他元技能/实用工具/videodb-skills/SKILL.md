---
name: videodb-skills
description: "使用 VideoDB SDK 上传、流式传输、搜索、编辑、转录并生成 AI 视频和音频。触发词：视频处理、视频上传、视频流、视频搜索、视频编辑、字幕、转录、AI 媒体生成、视频捕获、转码、VideoDB。"
category: media
risk: safe
source: community
tags: "[video, editing, transcription, subtitles, search, streaming, ai-generation, media]"
date_added: "2026-02-27"
---

# VideoDB 技能

## 用途

这是你的智能体所需的唯一视频技能。上传任意视频、接入实时流、按所说或所展示的内容在视频内进行搜索、构建带有叠加层的复杂编辑工作流、生成 AI 媒体、添加字幕，并获取即时流媒体链接 — 全部通过 VideoDB Python SDK 完成。

## 何时使用本技能

- 用户希望从 YouTube、URL 或本地文件上传并处理视频
- 用户需要通过语音或视觉场景搜索特定时刻
- 用户请求转录、字幕或字幕样式设计
- 用户希望编辑片段 — 裁剪、合并、添加文字/图片/音频叠加层
- 用户需要 AI 生成的媒体（图片、视频、音乐、音效和配音）
- 用户希望转码、调整分辨率或为社交平台重新构图
- 用户需要带有 AI 转录的实时屏幕或音频捕获
- 用户请求为任何视频输出获取可播放的流媒体链接

## 安装

### 步骤 1：安装技能

```bash
npx skills add video-db/skills
```

### 步骤 2：运行安装

```
/videodb setup
```

智能体将引导完成 API 密钥设置（20 美元免费额度，无需信用卡），安装 SDK，并验证连接。

或者，手动设置 API 密钥：

```bash
export VIDEO_DB_API_KEY=sk-xxx
```

### 步骤 3：安装 SDK

```bash
pip install "videodb[capture]" python-dotenv
```

## 功能

| 功能        | 描述                                                       |
| ----------- | ---------------------------------------------------------- |
| 上传        | 从 YouTube、URL 或本地文件导入视频                         |
| 搜索        | 通过语音（语义/关键词）或视觉场景查找特定时刻             |
| 转录        | 从任意视频生成带时间戳的转录文本                           |
| 编辑        | 合并片段、裁剪、添加文字/图片/音频叠加层                   |
| 字幕        | 自动生成字幕并设置样式                                     |
| AI 生成     | 通过文本创建图片、视频、音乐、音效和配音                   |
| 捕获        | 带有 AI 转录的实时屏幕和音频捕获                           |
| 转码        | 调整分辨率、质量、宽高比，或为社交平台重新构图             |
| 流媒体      | 为你构建的任何内容获取可播放的 HLS 链接                    |

## 示例

**上传并转录：**

```
"Upload https://www.youtube.com/watch?v=FgrO9ADPZSA and give me a transcript"
```

**跨视频搜索：**

```
"Search for 'product demo' in my latest video"
```

**添加字幕：**

```
"Add subtitles with white text on black background"
```

**多片段编辑：**

```
"Take clips from 10s-30s and 45s-60s, add a title card, and combine them"
```

**AI 媒体生成：**

```
"Generate background music and overlay it on my video"
```

**实时捕获：**

```
"Capture my screen and transcribe it in real-time"
```

**为社交平台重新构图：**

```
"Convert this to vertical for Instagram Reels"
```

## 仓库

https://github.com/video-db/skills

**版本：** 1.1.0
**维护者：** [VideoDB](https://github.com/video-db)

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为可替代特定环境验证、测试或专家审查的结果。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
