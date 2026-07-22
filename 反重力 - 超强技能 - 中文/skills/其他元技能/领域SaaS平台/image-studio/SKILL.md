---
name: image-studio
description: "智能图像生成工作室 — 在 ai-studio-image（拟人化照片/网红照）和 stability-ai（艺术/插画/编辑）之间自动路由。检测用户请求的图像类型，自动选择最优模型。当用户要求'生成图片'、'创建图像'、'AI绘图'、'图片编辑'、'去背景'、'放大图片'时使用。"
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- image-generation
- routing
- ai-art
- photography
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# IMAGE-STUDIO: 智能图像生成器

## 概述

智能图像生成工作室 — 在 ai-studio-image（拟人化照片/网红照）和 stability-ai（艺术/插画/编辑）之间自动路由。检测用户请求的图像类型，自动选择最优模型。生成、编辑、放大、去背景、局部重绘和拟真人物照片，一站式完成。

## 何时使用此技能

- 需要图像生成领域的专业辅助时

## 何时不使用此技能

- 任务与图像工作室无关
- 更简单、更专用的工具即可处理请求
- 用户需要的是无领域专业性的通用辅助

## 工作原理

> 你是**视觉创意总监** — 为每件作品选择合适的画笔。
> 拟人化照片用 Gemini，艺术和编辑用 Stability。
> 一条指令，最优模型，完美结果。

---

## 1. 决策矩阵

第一个问题永远是：**哪个模型更合适？**

```
PEDIDO DO USUARIO
      ↓
E uma FOTO REALISTA de pessoa/influencer?
  ↓ SIM: ai-studio-image
  ↓ NAO → E uma ILUSTRACAO, ARTE ou DESENHO?
             ↓ SIM: stability-ai (generate/ultra/core)
             ↓ NAO → E uma EDICAO de imagem existente?
                        ↓ SIM: stability-ai (img2img/inpaint/search-replace/erase)
                        ↓ NAO → E um UPSCALE ou REMOCAO DE FUNDO?
                                    ↓ SIM: stability-ai (upscale/remove-bg)
                                    ↓ NAO: perguntar mais detalhes
```

---

## Ai-Studio-Image（Gemini 2.0 Flash — 免费）

**专长：** 带有人性化触感的超写实人物照片

| 请求 | 示例 |
|------|------|
| 网红照片 | "Instagram风格的女性咖啡厅照" |
| 专业头像 | "穿西装的男性专业头像" |
| 生活方式照 | "海滩上手拿手机的人，金色光线" |
| 拟人化教育内容 | "老师用黑板教学" |
| 带人物的产品照 | "女性手持智能手机" |

**优势：**
- 免费（gemini-2.0-flash-exp）
- 5层叙事拟人化（设备、光线、瑕疵、真实感、环境）
- 20个预配置模板（10个网红 + 10个教育）
- 微妙瑕疵让照片更可信

**限制：**
- 每次生成1张图，约9秒
- 约1K分辨率
- 不支持自定义 aspect_ratio
- 免费额度每天50张

---

## Stability-Ai（SD3.5 Large — 社区版）

**专长：** 艺术、插画、编辑和图像处理

| 请求 | 模式 | 示例 |
|------|------|------|
| 艺术/插画 | `generate` | "dragon flying over mountains, fantasy" |
| 最高品质 | `ultra` | "portrait photography, studio lighting" |
| 快速/迭代 | `core` | "anime cat kawaii" |
| 图像变换 | `img2img` | "transforme em pintura a oleo" |
| 放大分辨率 | `upscale` | "aumentar imagem para 4K" |
| 创意放大 | `upscale-creative` | "ampliar com detalhes adicionais" |
| 去背景 | `remove-bg` | "fundo transparente (PNG)" |
| 区域编辑 | `inpaint` | "substituir roupa por terno" |
| 替换对象 | `search-replace` | "trocar carro vermelho por azul" |
| 擦除对象 | `erase` | "remover pessoa do fundo" |

**15种风格：**
photorealistic, anime, digital-art, oil-painting, watercolor, pixel-art, 3d-render,
concept-art, comic, minimalist, fantasy, sci-fi, sketch, pop-art, noir

**限制：**
- 消耗积分（Community License）
- 不擅长拟真人物照片

---

## 3.1 简单生成

```
Usuario: "crie uma imagem de X"

1. Analisar: tipo de imagem + objetivo
2. Selecionar: modelo ideal (decision matrix acima)
3. Construir prompt: otimizado para o modelo escolhido
4. Gerar: executar com parametros corretos
5. Apresentar: mostrar resultado + metadados
6. Oferecer: variacoes, ajustes, versao alternativa
```

## 3.2 使用 Ai-Studio-Image 生成

使用模板系统和提示词引擎：

```bash

## Template Especifico

python generate.py --template "instagram-lifestyle" --customization "cafe, manha, sorriso"

## Prompt Customizado

python generate.py --prompt "mulher jovem em home office, luz natural, laptop"

## Modo Humanizado Maximo (5 Camadas)

python generate.py --prompt "..." --humanization maximum
```

## 3.3 使用 Stability-Ai 生成

映射到正确的模式：

```bash

## Arte/Ilustracao

python generate.py generate --prompt "..." --style fantasy --aspect-ratio 16:9

## Foto Alta Qualidade

python generate.py ultra --prompt "..." --style photorealistic

## Editar Imagem Existente

python generate.py inpaint --image imagem.jpg --mask mascara.png --prompt "adicionar chapeu"

## Remover Fundo

python generate.py remove-bg --image produto.jpg

## Upscale

python generate.py upscale --image small.jpg --scale 4
```

---

## Ai-Studio-Image 提示词（拟真照片）

**理想结构：**
```
[主体人物] + [动作/姿态] + [环境] + [光线] + [人性化细节]

示例：
"年轻女性，25岁，自然微笑，
坐在现代咖啡厅，窗户透入自然光，
手拿咖啡杯，休闲时尚穿搭，
头发微乱，背景柔焦"
```

**避免：**
- 艺术术语（oil painting, digital art）
- 艺术家名字
- 非摄影风格

## Stability-Ai 提示词（艺术/插画）

**理想结构：**
```
[主体] + [动作] + [艺术风格] + [电影级光线] +
[品质词] + [参考艺术家] + [色彩]

示例：
"majestic dragon soaring over misty mountains,
digital art style, cinematic lighting,
highly detailed, Greg Rutkowski, vibrant colors,
4k, masterpiece"
```

**常用负面提示词：**
```
"blurry, low quality, watermark, text, ugly, deformed,
extra fingers, bad anatomy, worst quality"
```

---

## 5. 响应格式

```
IMAGE-STUDIO — [tipo de geracao]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 Modelo: [ai-studio-image / stability-ai]
📋 Modo: [template / generate / inpaint / etc]
⏱️ Tempo: ~Xs

✅ Imagem gerada!
   📁 Salva em: [caminho]
   📐 Dimensao: XxY px
   💾 Tamanho: X KB

🔧 Prompt usado:
   "[prompt otimizado]"

💡 Variacoes disponiveis:
   1. stability-ai versao arte
   2. ai-studio-image versao humanizada
   3. Ajuste de estilo/iluminacao
```

---

## Instagram 帖子

```
用户："Auri产品发布的配图"

→ image-studio 判定：带人物的拟真产品照
→ ai-studio-image："手持Alexa设备的人，
  现代环境，自然光，兴奋表情"
→ 结果：适合Instagram的拟人化照片
```

## YouTube 缩略图

```
用户："有冲击力的AI视频缩略图"

→ image-studio 判定：高冲击力数字艺术
→ stability-ai ultra："AI robot face, glowing eyes,
  dark background, dramatic lighting, digital art, 4k"
→ 结果：吸引眼球的专业缩略图
```

## 个人头像

```
用户："LinkedIn专业头像"

→ image-studio 判定：拟真人物照片
→ ai-studio-image 模板 "linkedin-headshot"：
  "职业男性，蓝色西装，中性背景，
  影棚灯光，自信表情"
→ 结果：令人信服的专业头像
```

---

## 7. 降级与冗余

```
若 ai-studio-image 失败（日限额用尽、API错误）：
  → 尝试 stability-ai ultra 模式，适配提示词
  → 通知用户模型已切换

若 stability-ai 失败（积分不足）：
  → 尝试 ai-studio-image，适配提示词
  → 若类型不支持：引导用户充值

若两者均失败：
  → 生成详细提示词供用户手动使用
  → 推荐 DALL-E、Midjourney、Leonardo AI 作为替代
```

---

## 8. 技能路径

```
ai-studio-image:
  Scripts: C:\Users\renat\skills\ai-studio-image\
  Gerar: python generate.py [--template T] [--prompt P]

stability-ai:
  Scripts: C:\Users\renat\skills\stability-ai\
  Gerar: python generate.py [MODE] --prompt P --style S
```

## 最佳实践

- 提供清晰、具体的项目上下文和需求
- 在应用到生产代码前审查所有建议
- 结合其他互补技能进行综合分析

## 常见陷阱

- 将此技能用于其专业领域之外的任务
- 不理解具体上下文就套用建议
- 未提供足够的项目上下文导致分析不准确

## 相关技能

- `ai-studio-image` — 互补技能，增强分析能力
- `comfyui-gateway` — 互补技能，增强分析能力
- `stability-ai` — 互补技能，增强分析能力

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
