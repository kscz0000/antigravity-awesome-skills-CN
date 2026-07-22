---
name: video-content-extractor
description: "从 MP4 视频中按可配置间隔提取关键帧，运行 Tesseract OCR，并生成包含视频元数据和带时间戳文本转录的结构化 Markdown 报告。"
category: media-processing
risk: safe
source: community
source_repo: 274326424/video-content-extractor
source_type: community
date_added: "2026-06-06"
author: 274326424
tags: [video, ocr, ffmpeg, tesseract, frame-extraction, media]
tools: [codex]
---

# 视频内容提取器

## 概述

自动从 MP4 视频文件中按可配置的时间间隔提取关键帧，对每帧执行 OCR 文字识别，并生成结构化的 Markdown 报告。报告包含视频元数据（时长、分辨率、编解码器）以及按帧排列的 OCR 转录文本和对应时间戳。

本技能面向 Codex CLI 设计，要求本机已安装 FFmpeg 和 Tesseract OCR。

## 适用场景

- 需要从演示视频、讲座或录屏中提取文字内容时使用。
- 想要为不含内嵌字幕的视频文件生成可搜索的转录文本时使用。
- 需要以编程方式分析视频内容并生成结构化摘要时使用。
- 当用户要求"读取屏幕上显示的内容"或"提取这段视频的内容"时使用。

## 工作原理

### 步骤 1：分析视频元数据

技能使用 ffprobe 提取视频元数据：时长、分辨率、帧率、编解码器信息以及文件大小。

### 步骤 2：提取关键帧

通过 FFmpeg，技能按配置的间隔（默认每 30 秒）捕获帧，每一帧保存为带时间戳的 JPEG 图像。

### 步骤 3：OCR 文字识别

每一帧由 Tesseract OCR 处理。若默认 PSM 模式未返回有效文本，将回退到全自动页面分割模式。

### 步骤 4：生成 Markdown 报告

所有提取到的数据将合并为一份结构化的 Markdown 文档。

## 示例

### 示例 1：基本提取

智能体提示词：
使用 video-content-extractor 技能从 lecture.mp4 中提取内容

输出将生成 lecture.md 和 lecture_frames/ 目录。

### 示例 2：自定义间隔

参数：video_path、output_dir、interval（秒）、lang
每 60 秒提取一次，仅识别英文：
python scripts/extract_video.py recording.mp4 ./output 60 eng

### 示例 3：双语内容

使用默认中文 + 英文 OCR 提取：
python scripts/extract_video.py lecture.mp4 . 15 chi_sim+eng

## 最佳实践

- 对于画面切换频繁、文字变化快的快节奏内容，使用较短的间隔（10-15 秒）。
- 对于演示幻灯片或节奏较慢的讲座，使用较长的间隔（30-60 秒），以减少重复帧。
- 处理中文内容时，请确保已安装 Tesseract 中文语言包（chi_sim）。

## 局限性

- 要求本机已安装 FFmpeg 和 Tesseract OCR，并可通过 PATH 访问。
- Tesseract OCR 的识别准确率取决于视频质量、文字大小和字体清晰度。
- 不提取音频，也不执行语音转文字。
- 抽帧基于固定时间间隔（而非场景切换），因此可能产生近似重复的帧。
- 大体积视频配合短间隔会生成大量帧，请确保磁盘空间充足。

## 安全注意事项

- 本技能仅读取视频文件，并写入抽帧结果和 Markdown 报告。
- 不会通过网络发送任何数据，所有处理均在本地完成。
- FFmpeg 和 Tesseract 均使用固定且经过预先审核的参数调用。
- 技能不会修改或删除原始视频文件。

## 常见问题

- 问题：Tesseract 返回乱码文本
  解决：确认已安装正确的语言包。运行 tesseract --list-langs 进行验证。

- 问题：FFmpeg 报"not found"
  解决：确认 FFmpeg 已在 PATH 中。运行 ffmpeg -version 进行验证。

- 问题：大体积视频 OCR 速度慢
  解决：增大 interval 参数以减少处理的帧数。

## 相关技能

- @media-summarizer — 借助视觉和音频线索对视频内容进行摘要。
- @document-ocr — 对静态图像或扫描文档进行 OCR，不涉及视频处理。