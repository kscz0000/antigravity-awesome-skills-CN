---
name: imagen
description: "AI 图像生成技能，由 Google Gemini 驱动，支持 UI 占位图、文档插图和设计素材的无缝视觉内容创建。触发词：生成图片、创建图像、AI绘图、generate image、create image、图片生成、图像生成、Gemini 图像、hero image、占位图、图标生成、logo 生成、UI 素材。"
risk: safe
source: "https://github.com/sanjay3290/ai-skills/tree/main/skills/imagen"
date_added: "2026-02-27"
---

# Imagen - AI 图像生成技能

## 概述

本技能使用 Google Gemini 的图像生成模型（`gemini-3-pro-image-preview`）生成图像。它支持在任何 Claude Code 会话中无缝创建图像——无论是构建前端 UI、编写文档，还是需要将概念可视化。

**跨平台支持**：适用于 Windows、macOS 和 Linux。

## 何时使用此技能

在以下情况下自动激活此技能：
- 用户请求生成图像（例如"生成一张...的图片"、"创建一张图片..."）
- 前端开发需要占位图或实际图像
- 文档需要插图或图表
- 可视化概念、架构或想法
- 创建图标、logo 或 UI 素材
- 任何 AI 生成图像可能有帮助的任务

## 工作原理

1. 接收描述所需图像的文本提示词
2. 调用 Google Gemini API 进行图像生成配置
3. 将生成的图像保存到指定位置（默认为当前目录）
4. 返回文件路径供项目使用

## 使用方法

### Python（跨平台 - 推荐）

```bash
# 基本用法
python scripts/generate_image.py "A futuristic city skyline at sunset"

# 指定输出路径
python scripts/generate_image.py "A minimalist app icon for a music player" "./assets/icons/music-icon.png"

# 指定尺寸
python scripts/generate_image.py --size 2K "High resolution landscape" "./wallpaper.png"
```

## 要求

- 必须设置 `GEMINI_API_KEY` 环境变量
- Python 3.6+（仅使用标准库，无需 pip 安装）

## 输出

生成的图像保存为 PNG 文件。脚本返回：
- 成功：生成图像的路径
- 失败：包含详情的错误信息

## 示例

### 前端开发
```
用户："我需要一张落地页的 hero 图像——抽象风格，科技感"
-> 生成并保存图像，提供可在 HTML/CSS 中使用的路径
```

### 文档
```
用户："创建一张展示微服务架构的图表"
-> 生成可视化表示，可用于 README 或文档
```

### UI 素材
```
用户："为用户资料组件生成一张占位头像图像"
-> 创建适合组件使用的尺寸图像
```

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
