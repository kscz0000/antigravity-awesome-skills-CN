---
name: minimalist-ui
description: "创建温暖单色调、利落边框、克制动效和扁平便当盒布局的编辑风格界面时使用。当用户要求'极简UI'、'编辑风格界面'、'Notion风格'、'Linear风格'、'温暖单色调设计'时使用。"
category: frontend
risk: safe
source: community
source_repo: Leonxlnx/taste-skill
source_type: community
date_added: "2026-04-17"
author: Leonxlnx
tags: [frontend, design, minimalism, ui]
tools: [claude, cursor, codex, antigravity]
---
# 协议：高级实用极简主义 UI 架构师

## 适用场景

- 用户需要受 Notion、Linear 等编辑风格工作台启发的精致极简 UI 时使用。
- 设计温暖单色调界面，搭配利落边框、充裕留白、柔和粉彩点缀和安静动效时使用。
- 任务需要回避渐变、重阴影、高饱和色、药丸形组件和通用 SaaS 视觉风格时使用。

## 局限性

- 极简主义在内容密集时可能掩盖层级关系；需用真实内容验证可扫读性、对比度和导航清晰度。
- 本技能假定产品能支撑克制的配色和排版驱动的布局；无正当理由不要覆盖已有品牌体系。
- 微妙动效和扁平表面仍需在目标项目中验证响应式、键盘和屏幕阅读器兼容性。


## 1. 协议概览
名称：高级实用极简主义与编辑风格 UI
描述：面向生成高度精致、超极简"文档风格"Web 界面的高级前端工程指令，对标顶级工作台平台。本协议严格执行高对比度温暖单色调配色、定制排版层级、精密结构宏观留白、便当盒网格布局，以及带刻意柔和粉彩点缀的超扁平组件架构。主动拒绝通用 SaaS 设计趋势。

## 2. 绝对负面约束（禁止元素）
AI 必须严格避免以下通用 Web 开发默认做法：
- 禁止使用 "Inter"、"Roboto" 或 "Open Sans" 字体。
- 禁止使用 "Lucide"、"Feather" 或标准 "Heroicons" 等通用细线图标库。
- 禁止使用 Tailwind 默认重投影（如 `shadow-md`、`shadow-lg`、`shadow-xl`）。阴影应几乎不存在，或重度定制为超弥散、低透明度（< 0.05）。
- 禁止为大元素或区域使用主色背景（如亮蓝、亮绿或亮红 hero 区域）。
- 禁止使用渐变、霓虹色或 3D 毛玻璃效果（导航栏微模糊除外）。
- 禁止对大容器、卡片或主按钮使用 `rounded-full`（药丸形）。
- 禁止在代码、标记、文本内容、标题或 alt 文本中使用 emoji。用正规图标或简洁 SVG 原语替代。
- 禁止使用 "John Doe"、"Acme Corp" 或 "Lorem Ipsum" 等通用占位名。使用真实、贴合语境的内容。
- 禁止使用 AI 文案套话："Elevate"、"Seamless"、"Unleash"、"Next-Gen"、"Game-changer"、"Delve"。写平实、具体的语言。

## 3. 排版架构
界面必须依靠极端排版对比和优质字体选择来建立编辑感。
- 主无衬线体（正文、UI、按钮）：使用干净、几何感或系统原生有个性的字体。目标：`font-family: 'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`。
- 编辑衬线体（Hero 标题与引文）：目标：`font-family: 'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`。紧凑字距（`letter-spacing: -0.02em` 至 `-0.04em`）和紧凑行高（`1.1`）。
- 等宽体（代码、快捷键、元数据）：目标：`font-family: 'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`。
- 文字颜色：正文绝不可用纯黑（`#000000`）。使用偏黑/炭灰（`#111111` 或 `#2F3437`），行高设为 `1.6` 以保证可读性。次要文字用灰（`#787774`）。

## 4. 色彩体系（温暖单色调 + 点缀粉彩）
色彩是稀缺资源，仅用于语义含义或微妙点缀。
- 画布/背景：纯白 `#FFFFFF` 或暖骨白/灰白 `#F7F6F3` / `#FBFBFA`。
- 主表面（卡片）：`#FFFFFF` 或 `#F9F9F8`。
- 结构边框/分隔线：超浅灰 `#EAEAEA` 或 `rgba(0,0,0,0.06)`。
- 点缀色：仅使用高去饱和、水洗粉彩色，用于标签、行内代码背景或微妙图标背景。
  - 浅红：`#FDEBEC`（文字：`#9F2F2D`）
  - 浅蓝：`#E1F3FE`（文字：`#1F6C9F`）
  - 浅绿：`#EDF3EC`（文字：`#346538`）
  - 浅黄：`#FBF3DB`（文字：`#956400`）

## 5. 组件规格
- 便当盒功能网格：
  - 使用非对称 CSS Grid 布局。
  - 卡片必须严格使用 `border: 1px solid #EAEAEA`。
  - 圆角必须利落：最大 `8px` 或 `12px`。
  - 内边距必须充裕（如 `24px` 至 `40px`）。
- 主行动号召（按钮）：
  - 实色背景 `#111111`，文字 `#FFFFFF`。
  - 微圆角（`4px` 至 `6px`）。无 box-shadow。
  - 悬停状态为微妙颜色偏移至 `#333333` 或微缩放 `transform: scale(0.98)`。
- 标签与状态徽章：
  - 药丸形（`border-radius: 9999px`），极小字号（`text-xs`），大写加宽字距（`letter-spacing: 0.05em`）。
  - 背景必须使用定义的柔和粉彩色。
- 手风琴（FAQ）：
  - 去除所有容器框。仅用 `border-bottom: 1px solid #EAEAEA` 分隔条目。
  - 使用干净锐利的 `+` 和 `-` 图标切换状态。
- 快捷键微 UI：
  - 用 `<kbd>` 标签将快捷键渲染为物理按键：`border: 1px solid #EAEAEA`、`border-radius: 4px`、`background: #F7F6F3`，使用等宽字体。
- 仿操作系统窗口装饰：
  - 模拟软件时，用极简容器包裹，白色顶栏含三个浅灰小圆点（模拟 macOS 窗口控件）。

## 6. 图标与图像指引
- 系统图标：使用 "Phosphor Icons（Bold 或 Fill 粗细）" 或 "Radix UI Icons"，呈现技术感、略粗笔触的美学。统一所有图标的笔触宽度。
- 插画：单色、粗犷连续线墨线素描，白底，配一个偏移几何形状填充柔和粉彩色。
- 摄影：使用高质量、去饱和、暖调图像。施加微妙叠加（`opacity: 0.04` 暖颗粒）使照片融入单色调体系。禁止使用过饱和素材照片。无真实素材时使用可靠占位图如 `https://picsum.photos/seed/{context}/1200/800`。
- Hero 与区域背景：区域不应显得空洞扁平。使用极低透明度的全宽背景图、柔和径向光斑（`radial-gradient` 暖调 `opacity: 0.03`）或极简几何线图案增加深度，同时不破坏干净美学。

## 7. 微妙动效与微动画
动效应感觉不可见——存在但不分散注意力。目标是安静精致，而非炫技。
- 滚动入场：元素进入视口时柔和淡入。使用 `translateY(12px)` + `opacity: 0`，`600ms` 内过渡，缓动 `cubic-bezier(0.16, 1, 0.3, 1)`。使用 `IntersectionObserver`，禁止 `window.addEventListener('scroll')`。
- 悬停状态：卡片以超微妙阴影偏移抬起（`box-shadow` 从 `0 0 0` 过渡至 `0 2px 8px rgba(0,0,0,0.04)`，`200ms`）。按钮在 `:active` 时响应 `scale(0.98)`。
- 交错出场：列表和网格条目以级联延迟入场（`animation-delay: calc(var(--index) * 80ms)`）。禁止同时挂载所有元素。
- 背景氛围动效：可选。单个极慢移动的径向渐变光斑（`animation-duration: 20s+`、`opacity: 0.02-0.04`）在 hero 区域后方漂移。必须应用于 `position: fixed; pointer-events: none` 图层。禁止放在滚动容器上。
- 性能：仅通过 `transform` 和 `opacity` 实现动画。禁止触发布局的属性（`top`、`left`、`width`、`height`）。谨慎使用 `will-change: transform`，仅用于正在动画的元素。

## 8. 执行协议
编写前端代码（HTML、React、Tailwind、Vue）或设计布局时：
1. 先确立宏观留白。区域间使用大垂直内边距（如 Tailwind 的 `py-24` 或 `py-32`）。
2. 将主排版内容宽度限制为 `max-w-4xl` 或 `max-w-5xl`。
3. 立即应用定制排版层级和单色调色彩变量。
4. 确保每张卡片、分隔线和边框严格遵守 `1px solid #EAEAEA` 规则。
5. 为所有主要内容块添加滚动入场动画。
6. 确保区域通过图像、氛围渐变或微妙纹理拥有视觉深度——不留空洞扁平背景。
7. 输出的代码应原生体现这种高端、整洁、编辑美学，无需手动调整。
