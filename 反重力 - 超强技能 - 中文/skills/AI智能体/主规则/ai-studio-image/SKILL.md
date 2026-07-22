---
name: ai-studio-image
description: 通过 Google AI Studio (Gemini) 生成拟人化图像。真实感照片，网红或教育风格，自然光照和细微瑕疵。触发词：生成图像、生成图片、生成照片、创建图像、真实照片、拟人化图像、网红照片、AI照片、AI图像生成、Gemini图像、Google AI Studio图像
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- image-generation
- ai-studio
- google
- photography
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# AI Studio Image — 拟人化图像专家

## 概述

通过 Google AI Studio (Gemini) 生成拟人化图像。真实感照片，网红或教育风格，自然光照和细微瑕疵。

## 何时使用此技能

- 当用户提到"生成图像"或相关话题时
- 当用户提到"生成照片"或相关话题时
- 当用户提到"创建图像"或相关话题时
- 当用户提到"真实照片"或相关话题时
- 当用户提到"拟人化图像"或相关话题时
- 当用户提到"网红照片"或相关话题时

## 不应使用此技能的情况

- 任务与 ai studio image 无关
- 更简单、更具体的工具可以处理请求
- 用户需要的是无领域专业知识的通用帮助

## 工作原理

AI图像与真实照片的区别在于那些难以察觉的细节：手机传感器的轻微颗粒感、不够完美的光照、略微偏离中心的构图、小镜头特有的景深。此技能系统性地将这些特质注入每次生成中。

## AI Studio Image — 拟人化图像专家

通过 Google AI Studio 生成图像的技能，可将任何提示词转换为具有真实人类外观的照片。每张生成的图像都像是真人用手机拍摄的——而非AI生成。

## 1. 配置 API Key

用户需要 Google AI Studio 的 API key：
- 访问 https://aistudio.google.com/apikey
- 创建或复制您的 API key
- 配置为环境变量：

```bash

## Windows

set GEMINI_API_KEY=sua-api-key-aqui

## Linux/Mac

export GEMINI_API_KEY=sua-api-key-aqui
```

或在 `C:\Users\renat\skills\ai-studio-image\` 创建 `.env` 文件：
```
GEMINI_API_KEY=sua-api-key-aqui
```

## 2. 安装依赖

```bash
pip install -r C:\Users\renat\skills\ai-studio-image\scripts\requirements.txt
```

## 3. 生成您的第一张图像

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py --prompt "mulher jovem tomando cafe em cafeteria" --mode influencer --format square
```

## 主要工作流

当用户请求生成图像时，遵循以下流程：

## 步骤 1：识别模式

询问或根据上下文推断：

| 模式 | 使用场景 | 特点 |
|------|----------|------|
| **influencer** | 社交媒体帖子、生活方式、个人品牌 | 美观但自然的风格，鲜艳但不饱和过度的色彩，吸引注意力的构图 |
| **educacional** | 课程材料、教程、演示、信息图 | 干净专业的视觉，聚焦内容，清晰可读的元素 |

如果用户未指定，社交媒体内容默认使用 **influencer**，教学/演示相关内容使用 **educacional**。

## 步骤 2：识别格式

| 格式 | 宽高比 | 理想用途 |
|------|--------|----------|
| `square` | 1:1 | Instagram/Facebook 动态、个人资料 |
| `portrait` | 3:4 | Instagram 竖版、Pinterest |
| `landscape` | 16:9 | YouTube 缩略图、横幅、桌面端 |
| `stories` | 9:16 | Instagram/Facebook Stories、TikTok、Reels |

如果未指定，根据上下文推断（stories → 9:16，动态 → 1:1 等）。

## 步骤 3：转换提示词

**这是最重要的步骤。** 永远不要直接将用户的提示词发送给 API。
始终通过拟人化引擎处理：

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\prompt_engine.py --prompt "prompt do usuario" --mode influencer
```

拟人化引擎添加多层真实感：

**第1层 — 设备与技术：**
- 使用智能手机拍摄（iPhone/Samsung Galaxy）
- 手机镜头的自然景深
- 无闪光灯 — 仅环境光
- 轻微的传感器噪点（低光下高ISO）

**第2层 — 自然光照：**
- 间接阳光 / 黄金时刻 / 窗边光
- 柔和有机的阴影
- 无影棚灯光
- 表面的自然反光

**第3层 — 人类瑕疵：**
- 略微不完美的构图（非数学居中）
- 自然的选择性对焦（背景某处略微失焦）
- 手部微抖（清晰度非绝对）
- 真实环境中的随机元素

**第4层 — 真实性：**
- 真实的面部表情（非影棚摆拍）
- 日常服装和场景
- 真实的皮肤纹理（毛孔、细微痕迹 — 无瓷肌效果）
- 真实的身体比例

**第5层 — 环境语境：**
- 真实场景（非通用素材背景）
- 环境中的日常物品
- 与场景一致的光照
- 与活动相符的时间

## 步骤 4：生成图像

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "prompt humanizado gerado no passo anterior" \
  --mode influencer \
  --format square \
  --model gemini-2-flash-exp \
  --output C:\Users\renat\skills\ai-studio-image\data\outputs\
```

**可用模型（按推荐顺序）：**

| 模型 | 速度 | 质量 | 成本 | 理想用途 |
|------|------|------|------|----------|
| `gemini-2-flash-exp` | 快 | 高 | **免费** | **默认 — 始终使用** |
| `imagen-4` | 中 | 高 | $0.03/张 | 高质量（需要 --force-paid） |
| `imagen-4-ultra` | 慢 | 最高 | $0.06/张 | 印刷、2K（需要 --force-paid） |
| `imagen-4-fast` | 快 | 良好 | $0.02/张 | 大批量（需要 --force-paid） |
| `gemini-flash-image` | 快 | 高 | $0.039/张 | 图像编辑（需要 --force-paid） |
| `gemini-pro-image` | 中 | 最高+4K | $0.134/张 | 参考、4K（需要 --force-paid） |

## 步骤 5：展示与迭代

向用户展示结果。如需调整：
- 重打光：调整光照
- 重构图：改变构图
- 更自然/更不自然：调整瑕疵程度
- 更换场景：改变环境

## 预配置模板

对于常见场景，使用现成模板。执行：

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\templates.py --list
```

可用模板：

## Influencer 模式

| 模板 | 描述 |
|------|------|
| `cafe-lifestyle` | 咖啡馆/餐厅中的人物，手持饮品/食物 |
| `outdoor-adventure` | 户外活动、自然、旅行 |
| `workspace-minimal` | 优雅的书桌、家庭办公 |
| `fitness-natural` | 运动/健康，自然视觉 |
| `food-flat-lay` | 俯拍食物，休闲平铺 |
| `urban-street` | 城市场景、街头风格 |
| `golden-hour-portrait` | 日落金光人像 |
| `mirror-selfie` | 镜子自拍，休闲自然 |
| `product-in-use` | 人物自然使用产品的场景 |
| `behind-scenes` | 幕后花絮、日常真实 |

## Educacional 模式

| 模板 | 描述 |
|------|------|
| `tutorial-step` | 人物演示教程步骤 |
| `whiteboard-explain` | 人物在白板/黑板前讲解 |
| `hands-on-demo` | 双手进行实操演示 |
| `before-after` | 前后对比 |
| `tool-showcase` | 工具/软件使用中 |
| `classroom-natural` | 课堂/工作坊环境 |
| `infographic-human` | 人物指向数据/图表 |
| `interview-setup` | 访谈/播客自然布置 |
| `screen-recording-human` | 人物用笔记本展示屏幕 |
| `team-collaboration` | 团队自然协作 |

使用模板：
```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --template cafe-lifestyle \
  --custom "mulher ruiva, 30 anos, lendo livro" \
  --format square
```

## 拟人化程度

控制注入多少"瑕疵"：

| 级别 | 效果 |
|------|------|
| `ultra` | 最高真实感 — 看起来100%像手机照片 |
| `natural`（默认） | 质量与真实感的完美平衡 |
| `polished` | 更干净，仍自然但更注重美感 |
| `editorial` | 杂志风格，自然但有制作感 |

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "..." --humanization natural
```

## 时间段

光照会显著变化：

| 选项 | 描述 |
|------|------|
| `morning` | 柔和晨光，冷暖色调 |
| `golden-hour` | 日落/日出，金色色调 |
| `midday` | 正午强光，明显阴影 |
| `overcast` | 阴天，均匀漫射光 |
| `night` | 人工照明，暖色调 |
| `indoor` | 室内光线，混合光 |

## 批量生成

生成多个变体：

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "..." --variations 4 --format square
```

## Instagram 技能集成

生成图像并直接发布：
1. 使用 `ai-studio-image` 生成照片
2. 使用 `instagram` 技能发布优化后的配文

## Canva 集成

生成的图像可发送到 Canva 添加文字/品牌元素。

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `GEMINI_API_KEY not found` | 配置环境变量或创建 `.env` |
| `quota exceeded` | 等待速率限制重置或升级计划 |
| `image blocked` | 调整提示词 — 可能包含受限内容 |
| `low quality output` | 将 humanization 提高到 `ultra`，尝试其他模型 |

## 参考资料

详细指南请参阅：
- `references/setup-guide.md` — 完整安装与配置
- `references/prompt-engineering.md` — 拟人化图像提示词高级技巧
- `references/api-reference.md` — Google AI Studio API 文档

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 在将建议应用到生产代码前进行审查
- 与其他互补技能结合进行全面分析

## 常见陷阱

- 将此技能用于超出其专业领域的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目背景以进行准确分析

## 相关技能

- `comfyui-gateway` - 互补技能，用于增强分析
- `image-studio` - 互补技能，用于增强分析
- `stability-ai` - 互补技能，用于增强分析

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
