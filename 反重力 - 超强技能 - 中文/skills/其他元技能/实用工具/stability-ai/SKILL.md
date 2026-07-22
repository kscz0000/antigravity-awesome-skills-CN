---
name: stability-ai
description: 通过 Stability AI（SD3.5、Ultra、Core）生成图像。支持文生图、图生图、局部重绘、超分辨率放大、背景移除、搜索替换。15 种艺术风格预设。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- image-generation
- stable-diffusion
- ai-art
- api
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Stability AI — 专业图像生成工具

## 概述

通过 Stability AI（SD3.5、Ultra、Core）生成图像。支持文生图、图生图、局部重绘、超分辨率放大、背景移除、搜索替换。15 种艺术风格预设。

## 适用场景

- 涉及 "stability ai" 相关话题
- 涉及 "stable diffusion" 相关话题
- 涉及 "sd3.5" 相关话题
- 涉及图像生成、艺术创作相关话题
- 涉及插画生成相关话题
- 涉及 "image to image" 相关话题

## 不适用场景

- 任务与 stability ai 无关
- 有更简单、更专门的工具可以处理该请求
- 用户需要通用辅助，不涉及特定领域

## 工作原理

通过 Stability AI API 生成艺术图像和写实照片。
**免费**使用 Community License（个人和年营收低于 100 万美元的小企业无限制）。

## 本技能 vs ai-studio-image 选型指南

| 场景 | 推荐技能 |
|------|----------|
| 适合 Instagram/社交媒体的人像照片 | ai-studio-image |
| 数字艺术、插画、概念设计 | **stability-ai** |
| 手机拍摄的日常写实照片 | ai-studio-image |
| 电影级写实画面（8K、高细节） | **stability-ai** |
| 教育材料的专业视觉素材 | ai-studio-image |
| 海报、壁纸、书籍封面、游戏素材 | **stability-ai** |
| 局部重绘（编辑图像局部区域） | **stability-ai** |
| 超分辨率放大（提升分辨率） | **stability-ai** |
| 移除图像背景 | **stability-ai** |
| 搜索替换（替换图像中的对象） | **stability-ai** |
| 擦除图像中的元素 | **stability-ai** |

## 快速配置

1. 在 **platform.stability.ai** 注册账号（免费）
2. 从控制面板复制 API Key
3. 粘贴到 `.env` 文件：`STABILITY_API_KEY=sk-sua-chave-aqui`
4. `pip install -r scripts/requirements.txt`

完整配置说明见 `references/setup-guide.md`。

## 1. 操作模式

| 命令 | 功能 | 端点 |
|------|------|------|
| `--mode generate` | 文生图（SD3.5） | `/generate/sd3` |
| `--mode ultra` | 高品质文生图 | `/generate/ultra` |
| `--mode core` | 快速文生图 | `/generate/core` |
| `--mode img2img` | 图像+文本生成新图 | `/generate/sd3` |
| `--mode upscale` | 分辨率放大（保守模式） | `/upscale/conservative` |
| `--mode upscale-creative` | 分辨率放大（创意增强） | `/upscale/creative` |
| `--mode remove-bg` | 移除背景（透明 PNG） | `/edit/remove-background` |
| `--mode inpaint` | 局部重绘（蒙版编辑） | `/edit/inpaint` |
| `--mode search-replace` | 按描述替换对象 | `/edit/search-and-replace` |
| `--mode erase` | 擦除图像局部 | `/edit/erase` |

## 2. 使用示例

```bash

## 基础生成（SD 3.5 Large）

python scripts/generate.py --prompt "a serene mountain landscape at sunset" --mode generate

## 最高品质（Ultra）

python scripts/generate.py --prompt "cinematic portrait, dramatic lighting" --mode ultra --aspect-ratio 16:9

## 快速迭代（Core）

python scripts/generate.py --prompt "cute cat ninja" --mode core --style anime

## 图生图

python scripts/generate.py --prompt "watercolor style" --mode img2img --image foto.jpg --strength 0.7

## 保守放大

python scripts/generate.py --prompt "landscape photo" --mode upscale --image foto_pequena.jpg

## 移除背景

python scripts/generate.py --mode remove-bg --image produto.jpg

## 蒙版局部重绘

python scripts/generate.py --prompt "red roses" --mode inpaint --image jardim.jpg --mask mascara.png

## 搜索替换

python scripts/generate.py --prompt "a golden retriever" --mode search-replace --image parque.jpg --search "the cat"

## 擦除对象

python scripts/generate.py --mode erase --image foto.jpg --mask area.png

## 列出模型

python scripts/generate.py --list-models

## 列出风格

python scripts/generate.py --list-styles

## 分析提示词（自动建议）

python scripts/generate.py --prompt "anime warrior girl, widescreen" --analyze --json
```

## 3. 宽高比

| 名称 | 比例 | 别名 | 典型用途 |
|------|------|------|----------|
| square | 1:1 | ig, instagram, quadrado | Instagram 动态 |
| portrait | 2:3 | retrato, pinterest | 人像、海报 |
| landscape | 3:2 | paisagem, horizontal | 风景、横幅 |
| photo | 4:5 | ig-feed | Instagram 动态优化 |
| wide | 16:9 | widescreen, youtube, cinema, wallpaper | 影视、YouTube |
| ultrawide | 21:9 | — | 超宽屏显示器 |
| stories | 9:16 | vertical, tiktok, ig-stories | Stories、Reels |
| phone | 9:21 | — | 手机壁纸 |

## 4. 风格预设（15 种）

每种风格会自动向提示词添加修饰词：

| 风格 | 描述 | 适用场景 |
|------|------|----------|
| photorealistic | 电影级写实 | 人像、场景 |
| anime | 日式动漫/漫画 | 角色、场景 |
| digital-art | 精细数字艺术 | 通用插画 |
| oil-painting | 古典油画 | 经典艺术 |
| watercolor | 水彩风格 | 细腻画面 |
| pixel-art | 复古 8/16-bit 像素风 | 复古游戏 |
| 3d-render | 写实 3D 渲染 | 产品、3D 场景 |
| concept-art | 专业概念设计 | 游戏、电影 |
| comic | 漫画/HQ 风格 | 漫画创作 |
| minimalist | 简约风格 | 设计、Logo |
| fantasy | 史诗奇幻艺术 | RPG、中世纪 |
| sci-fi | 未来科幻风 | 赛博朋克、太空 |
| sketch | 铅笔/炭笔素描 | 练习、草稿 |
| pop-art | 波普艺术 | 现代艺术 |
| noir | 黑色电影风格 | 暗黑氛围 |

## 5. 输出

图像保存在 `data/outputs/`，命名格式：`{mode}_{style}_{timestamp}_{index}.png`

元数据保存在 `.meta.json`，包含：原始提示词、最终提示词、模型、宽高比、种子值、耗时、尺寸。

## 与其他技能的协作

- **ai-studio-image**：互补关系 — Stability AI 负责艺术创作，Gemini 负责人像照片
- **instagram**：生成艺术图 → 发布到 Instagram
- **telegram**：生成图像 → 通过 bot 发送

## 速率限制与安全

- **Community License**：每 10 秒 150 次请求
- **每日限额**：100 张/天（通过 `SAFETY_MAX_IMAGES_PER_DAY` 可配置）
- **自动重试**：遇到 429 错误时指数退避重试
- **API Key 容灾**：主 Key + 备用 Key 自动切换

## 文件参考

| 文件 | 用途 |
|------|------|
| `references/setup-guide.md` | 初始配置、API Key、故障排查 |
| `references/prompt-engineering.md` | 高级提示词技巧 |
| `references/api-reference.md` | 端点、参数、响应、错误码 |

## 最佳实践

- 提供清晰、具体的项目背景和需求说明
- 将建议应用到生产代码前先审查
- 结合其他互补技能进行综合分析

## 常见误区

- 将技能用于超出其专业范围的任务
- 不理解具体场景就直接套用建议
- 未提供足够的项目背景信息

## 相关技能

- `ai-studio-image` - 互补技能，增强分析能力
- `comfyui-gateway` - 互补技能，增强分析能力
- `image-studio` - 互补技能，增强分析能力

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 输出结果不能替代针对具体环境的验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，应停止并请求澄清。
