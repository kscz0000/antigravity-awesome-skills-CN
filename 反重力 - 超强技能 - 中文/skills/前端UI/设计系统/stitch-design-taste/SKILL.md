---
name: stitch-design-taste
description: "用于生成 Google Stitch DESIGN.md 设计系统，涵盖高端排版、色彩、布局、动效意图及反泛化 UI 规则。触发词：设计系统、Stitch、前端设计、UI规范、排版规则、色彩系统、动效设计、反模式"
category: frontend
risk: safe
source: community
source_repo: Leonxlnx/taste-skill
source_type: community
date_added: "2026-04-17"
author: Leonxlnx
tags: [stitch, design-system, frontend, ui]
tools: [claude, cursor, codex, antigravity]
---
# Stitch Design Taste — 语义化设计系统技能

## 适用场景

- 用户需要兼容 Google Stitch 的 DESIGN.md 或用于 AI 屏幕生成的语义化设计系统时使用
- 将高端前端审美规则转化为 Stitch 友好的视觉描述、色彩角色、排版规范和组件行为时使用
- 设计系统需要在屏幕生成前阻止泛化 AI UI 模式时使用

## 局限性

- 本技能为 Stitch 生成语义化设计系统指南，不保证 Stitch 能精确渲染每个约束
- 生成的 `DESIGN.md` 文件仍需对照实际产品简报、品牌约束、无障碍需求和屏幕内容进行审查
- 动效章节记录的是实现意图，供后续编码智能体使用，因为 Stitch 本身可能只生成静态屏幕


## 概述
本技能生成专为 Google Stitch 屏幕生成优化的 `DESIGN.md` 文件。它将经过实战检验的反平庸前端工程指令转化为 Stitch 原生的语义化设计语言——描述性的自然语言规则配合精确数值，使 Stitch 的 AI 智能体能够解读并生成高端、非泛化的界面。

生成的 `DESIGN.md` 作为**唯一事实来源**，引导 Stitch 生成符合精心策划的高品位设计语言的新屏幕。Stitch 通过**"视觉描述"**来理解设计，辅以具体的色彩值、排版规范和组件行为。

## 前置条件
- 通过 [labs.google.com/stitch](https://labs.google.com/stitch) 访问 Google Stitch
- 可选：Stitch MCP Server，用于与 Cursor、Antigravity 或 Gemini CLI 进行编程集成

## 目标
生成一个编码以下内容的 `DESIGN.md` 文件：
1. **视觉氛围** — 情绪、密度和设计哲学
2. **色彩校准** — 中性色、强调色和带色号的禁用模式
3. **排版架构** — 字体栈、层级缩放和反模式
4. **组件行为** — 按钮、卡片、输入框及交互状态
5. **布局原则** — 栅格系统、间距哲学、响应式策略
6. **动效哲学** — 动画引擎规范、弹簧物理、持续微交互
7. **反模式** — 被禁用的 AI 设计陈词滥调的明确清单

## 分析与综合指令

### 1. 定义氛围
评估目标项目的意图。使用品味光谱中富有感染力的形容词：
- **密度：** "画廊般通透"（1–3）→ "日常应用均衡"（4–7）→ "驾驶舱般密集"（8–10）
- **变化：** "可预测的对称"（1–3）→ "偏移的不对称"（4–7）→ "艺术化混乱"（8–10）
- **动效：** "静态克制"（1–3）→ "流畅 CSS"（4–7）→ "电影级编排"（8–10）

默认基线：变化 8，动效 6，密度 4。根据用户的氛围描述动态调整。

### 2. 映射色彩面板
每种颜色需提供：**描述性名称** + **色号** + **功能角色**。

**强制约束：**
- 最多 1 种强调色，饱和度低于 80%
- 严格禁止"AI 紫/蓝霓虹"美学——禁止紫色按钮发光、禁止霓虹渐变
- 使用绝对中性底色（Zinc/Slate）配合高对比度的单一强调色
- 整个输出坚持同一色板——禁止冷暖灰混搭
- 永远不要使用纯黑（`#000000`）——使用 Off-Black、Zinc-950 或 Charcoal

### 3. 建立排版规则
- **展示/标题：** 紧凑字距，受控缩放。不要声嘶力竭。通过字重和颜色建立层级，而非仅靠巨大字号
- **正文：** 宽松行高，每行最多 65 个字符
- **字体选择：** `Inter` 在高端/创意场景中被禁止。强制使用独特字体：`Geist`、`Outfit`、`Cabinet Grotesk` 或 `Satoshi`
- **衬线禁令：** 通用衬线字体（`Times New Roman`、`Georgia`、`Garamond`、`Palatino`）被禁止。如在编辑/创意场景需要衬线体，仅使用独特的现代衬线字体：`Fraunces`、`Gambarino`、`Editorial New` 或 `Instrument Serif`。仪表盘或软件 UI 中始终禁止衬线体
- **仪表盘约束：** 仅使用无衬线字体组合（`Geist` + `Geist Mono` 或 `Satoshi` + `JetBrains Mono`）
- **高密度覆盖：** 当密度超过 7 时，所有数字必须使用等宽字体

### 4. 定义 Hero 区域
Hero 是第一印象，必须富有创意、引人注目，绝不能泛化：
- **内联图片排版：** 在标题的文字或字母之间直接嵌入小尺寸的上下文图片或视觉元素。图片以内联方式放置在字体高度，圆角处理，充当视觉标点。这是标志性创意技法
- **禁止重叠：** 文字绝不能重叠图片或其他文字。每个元素占据自己干净的空间区域
- **禁止填充文字：** "向下滚动探索"、"向下滑动"、滚动箭头图标、弹跳箭头均被禁止。内容应自然吸引用户
- **不对称结构：** 当变化超过 4 时，居中 Hero 布局被禁止
- **CTA 克制：** 最多一个主 CTA，不设"了解更多"等次要链接

### 5. 描述组件样式
对每种组件类型，描述形状、颜色、阴影深度和交互行为：
- **按钮：** 按下状态提供触觉反馈。禁止霓虹外发光。禁止自定义鼠标光标
- **卡片：** 仅在层级需要高度差时使用。阴影色调匹配背景色。高密度布局中用顶部分隔线或留白替代卡片
- **输入框/表单：** 标签在输入框上方，辅助文字可选，错误提示在下方。标准间距
- **加载状态：** 匹配布局尺寸的骨架屏——禁止通用圆形加载器
- **空状态：** 精心设计的组合画面，引导用户如何填充数据
- **错误状态：** 清晰的行内错误提示

### 6. 定义布局原则
- 禁止元素重叠——每个元素占据自己清晰的空间区域。禁止绝对定位的内容堆叠
- 当变化超过 4 时，居中 Hero 区域被禁止——强制使用分屏、左对齐或不对称留白
- 通用的"3 个等宽卡片横排"功能行被禁止——使用 2 列交错、不对称栅格或横向滚动
- CSS Grid 优先于 Flexbox 计算——永远不要使用 `calc()` 百分比 hack
- 使用 max-width 约束来限制布局（如 1400px 居中）
- 全高区域必须使用 `min-h-[100dvh]`——永远不要用 `h-screen`（iOS Safari 灾难性跳变）

### 7. 定义响应式规则
每个设计必须在所有视口下正常工作：
- **移动端优先折叠（< 768px）：** 所有多列布局折叠为单列，无例外
- **禁止水平滚动：** 移动端水平溢出是严重失败
- **排版缩放：** 标题通过 `clamp()` 缩放。正文最小 `1rem`/`14px`
- **触控目标：** 所有交互元素最小 `44px` 点击区域
- **图片行为：** 内联排版图片（文字间的照片）在移动端堆叠到标题下方
- **导航：** 桌面端水平导航折叠为简洁的移动端菜单
- **间距：** 垂直区域间距按比例缩减（`clamp(3rem, 8vw, 6rem)`）

### 8. 编码动效哲学
- **弹簧物理默认值：** `stiffness: 100, damping: 20`——高端、有重量感。禁止线性缓动
- **持续微交互：** 每个活跃组件都应有无限循环状态（脉冲、打字机、浮动、微光）
- **交错编排：** 永远不要瞬间挂载列表——使用级联延迟实现瀑布式展开
- **性能：** 仅通过 `transform` 和 `opacity` 执行动画。永远不要对 `top`、`left`、`width`、`height` 做动画。颗粒/噪点滤镜仅用于固定伪元素

### 9. 列出反模式（AI 破绽）
在 DESIGN.md 中将这些编码为明确的"绝不允许"规则：
- 禁止任何位置出现 emoji
- 禁止使用 `Inter` 字体
- 禁止通用衬线字体（`Times New Roman`、`Georgia`、`Garamond`）——需要时仅用独特现代衬线体
- 禁止纯黑（`#000000`）
- 禁止霓虹/外发光阴影
- 禁止过度饱和的强调色
- 禁止在大标题上过度使用渐变文字
- 禁止自定义鼠标光标
- 禁止元素重叠——始终保持干净的空间分离
- 禁止 3 列等宽卡片布局
- 禁止通用名称（"John Doe"、"Acme"、"Nexus"）
- 禁止虚假整数（`99.99%`、`50%`）
- 禁止 AI 文案陈词滥调（"Elevate"、"Seamless"、"Unleash"、"Next-Gen"）
- 禁止填充性 UI 文字："Scroll to explore"、"Swipe down"、滚动箭头、弹跳箭头
- 禁止失效的 Unsplash 链接——使用 `picsum.photos` 或 SVG 头像
- 禁止居中 Hero 区域（用于高变化项目）

## 输出格式（DESIGN.md 结构）

```markdown
# Design System: [Project Title]

## 1. Visual Theme & Atmosphere
(Evocative description of the mood, density, variance, and motion intensity.
Example: "A restrained, gallery-airy interface with confident asymmetric layouts
and fluid spring-physics motion. The atmosphere is clinical yet warm — like a
well-lit architecture studio.")

## 2. Color Palette & Roles
- **Canvas White** (#F9FAFB) — Primary background surface
- **Pure Surface** (#FFFFFF) — Card and container fill
- **Charcoal Ink** (#18181B) — Primary text, Zinc-950 depth
- **Muted Steel** (#71717A) — Secondary text, descriptions, metadata
- **Whisper Border** (rgba(226,232,240,0.5)) — Card borders, 1px structural lines
- **[Accent Name]** (#XXXXXX) — Single accent for CTAs, active states, focus rings
(Max 1 accent. Saturation < 80%. No purple/neon.)

## 3. Typography Rules
- **Display:** [Font Name] — Track-tight, controlled scale, weight-driven hierarchy
- **Body:** [Font Name] — Relaxed leading, 65ch max-width, neutral secondary color
- **Mono:** [Font Name] — For code, metadata, timestamps, high-density numbers
- **Banned:** Inter, generic system fonts for premium contexts. Serif fonts banned in dashboards.

## 4. Component Stylings
* **Buttons:** Flat, no outer glow. Tactile -1px translate on active. Accent fill for primary, ghost/outline for secondary.
* **Cards:** Generously rounded corners (2.5rem). Diffused whisper shadow. Used only when elevation serves hierarchy. High-density: replace with border-top dividers.
* **Inputs:** Label above, error below. Focus ring in accent color. No floating labels.
* **Loaders:** Skeletal shimmer matching exact layout dimensions. No circular spinners.
* **Empty States:** Composed, illustrated compositions — not just "No data" text.

## 5. Layout Principles
(Grid-first responsive architecture. Asymmetric splits for Hero sections.
Strict single-column collapse below 768px. Max-width containment.
No flexbox percentage math. Generous internal padding.)

## 6. Motion & Interaction
(Spring physics for all interactive elements. Staggered cascade reveals.
Perpetual micro-loops on active dashboard components. Hardware-accelerated
transforms only. Isolated Client Components for CPU-heavy animations.)

## 7. Anti-Patterns (Banned)
(Explicit list of forbidden patterns: no emojis, no Inter, no pure black,
no neon glows, no 3-column equal grids, no AI copywriting clichés,
no generic placeholder names, no broken image links.)
```

## 最佳实践
- **描述到位：** "深色墨炭 (#18181B)"——而不是"深色文字"
- **功能导向：** 解释每个元素的用途
- **保持一致：** 全文使用统一术语
- **精确数值：** 在括号中包含精确色号、rem 值、像素值
- **态度鲜明：** 这不是中立模板——它强制执行特定的高端美学

## 成功技巧
1. 从氛围开始——在细化设计令牌之前先理解整体感觉
2. 寻找规律——识别一致的间距、尺寸和样式
3. 语义化思维——按用途而非外观命名颜色
4. 考虑层级——记录视觉权重如何传达重要性
5. 编码禁令——反模式与规则本身同等重要

## 常见陷阱
- 使用未经翻译的技术术语（"rounded-xl"而非"大幅圆角"）
- 省略色号或仅使用描述性名称
- 忽略设计元素的功能角色
- 氛围描述过于模糊
- 忽略反模式清单——正是这些让输出显得高端
- 默认使用泛化"安全"设计，而非强制执行精心策划的美学
