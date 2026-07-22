---
name: frontend-slides-frontend-slides
description: 从零开始或通过转换 PowerPoint 文件，创建视觉效果惊艳、动画丰富的 HTML 演示文稿。当用户想要构建演示文稿、将 PPT/PPTX 转换为网页、或为演讲/路演创建幻灯片时使用。通过可视化探索帮助非设计师发现自己的审美偏好。触发词：HTML演示文稿、网页幻灯片、HTML幻灯片、PPT转HTML、PPTX转网页、演讲幻灯片、路演PPT、演示文稿制作、动画幻灯片、前端幻灯片、HTML presentation、presentation slides、web slides、PPT to HTML、slide deck、pitch deck
risk: unknown
source: https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides
source_repo: zarazhangrui/frontend-slides
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zarazhangrui/frontend-slides/blob/main/LICENSE
---

# 前端幻灯片
## 使用场景

当你需要从零开始或通过转换 PowerPoint 文件，创建视觉效果惊艳、动画丰富的 HTML 演示文稿时，请使用本技能。当用户想要构建演示文稿、将 PPT/PPTX 转换为网页、或为演讲/路演创建幻灯片时使用。通过可视化探索帮助非设计师发现自己的审美偏好……

创建零依赖、动画丰富的 HTML 演示文稿，全部在浏览器中运行。

## 核心原则

1. **零依赖** — 单个 HTML 文件，内联 CSS/JS。无需 npm，无需构建工具。
2. **展示而非描述** — 生成可视化预览，而非抽象选项。人们通过看见才能发现自己想要的。
3. **独特设计** — 拒绝通用的"AI 速成审美"。每份演示文稿都必须感觉是量身定制的。
4. **渐进式披露** — 先阅读轻量级的样式索引。对于大胆模板，使用小型预览卡片作为样式预览，并在用户选定模板后再加载完整的 `design.md`。
5. **固定 16:9 画布（不可妥协）** — 每份演示文稿使用 1920×1080 幻灯片画布，整体缩放至视口。幻灯片在任何屏幕上（包括手机）都必须保持 16:9。不得为了让设备适配而重排幻灯片内容。

## 设计美学

你往往倾向于收敛到通用、随大流的输出。在前端设计中，这会形成用户口中的"AI 速成审美"。请避免这种倾向：打造富有创意、独特的前端作品，让人感到惊喜和愉悦。

聚焦于：

- **字体排印**：选择美观、独特、有趣的字体。避免使用 Arial、Inter 这类通用字体；选择能够提升前端美感的独特字体。
- **色彩与主题**：坚持统一的美学。使用 CSS 变量保持一致性。主导色加锐利点缀色，比胆怯、均匀分布的调色板效果更好。从 IDE 主题和文化美学中汲取灵感。
- **动效**：使用动画来营造效果和微交互。在 HTML 中优先使用纯 CSS 方案。在 React 中可用时使用 Motion 库。聚焦高光时刻：一次编排精良的页面加载配合错开揭示（animation-delay）所带来的愉悦感，远胜于零散的微交互。
- **背景**：营造氛围和层次感，而不是默认使用纯色。叠加 CSS 渐变，使用几何图案，或添加与整体美学契合的情境化效果。

避免通用 AI 生成的美学：

- 过度使用的字体族（Inter、Roboto、Arial、系统字体）
- 老套的配色方案（尤其是白底上的紫色渐变）
- 可预测的布局和组件模式
- 缺乏情境特色的千篇一律的设计

富有创意地诠释，做出让人觉得真正为情境量身设计的意料之外的选择。在浅色与深色主题、不同字体、不同美学之间变化。你仍然倾向于在不同代际间收敛到常见选择（例如 Space Grotesk）。请避免这种倾向：跳出思维定式至关重要！

## 固定画布规则

以下不变量适用于**每份**演示文稿中的**每一张**幻灯片：

- 每份演示文稿都有一个填充浏览器窗口的视口包裹层。
- 每张幻灯片都在固定的 1920×1080 画布内编写。
- 画布统一缩放以适应视口。可以加黑边/留白，但不得重新布局内容。
- 不要使用响应式断点来为手机重排幻灯片内容。
- 在 1920×1080 设计尺寸下使用固定的内部幻灯片度量。
- 幻灯片可见性必须由 `.active` / `.visible` 控制，使用来自 `viewport-base.css` 的 `visibility`、`opacity` 和 `pointer-events`。不要使用 `display: none` / `display: block` 来切换幻灯片；后续的布局类（例如 `.slide-content { display: flex; }`）可能会覆盖它们，导致所有幻灯片同时可见。
- `clamp()` 仅可用于画布外的非幻灯片 UI，或用于完整画布不可行时的小型回退预览。
- 包含 `prefers-reduced-motion` 支持
- 绝不要直接对 CSS 函数取负（`-clamp()`、`-min()`、`-max()` 会被静默忽略） — 请使用 `calc(-1 * clamp(...))` 代替

**生成时，请阅读 `viewport-base.css` 并将其完整内容包含在每份演示文稿中。**

### 内容密度模式

询问用户这主要是"阅读型"演示文稿还是"演讲型"演示文稿，然后围绕答案进行设计：

| 密度模式 | 最适合 | 设计行为 |
| ------------- | -------- | --------------- |
| **低密度 / 演讲主导型** | 公开演讲、主题演讲式分享、现场讲解 | 每张幻灯片一个观点，字号大，视觉层次鲜明，留白充足，最多 1-3 个要点，必要时多几张幻灯片 |
| **高密度 / 阅读优先型** | 报告、讲义、异步审阅、详细内部文档 | 更具自包含性的幻灯片，结构化的网格/表格/注释，可读时可放 4-8 个要点或 4-6 张卡片，间距紧凑但仍精心设计 |

基线限制依然适用：不滚动、不溢出、不重叠面板、文字不低于舒适阅读字号。如果内容超出所选密度模式的承载能力，请拆分成更多幻灯片，而不是缩小到拥挤的程度。

---

## 阶段 0：识别模式

确定用户的需求：

- **模式 A：新建演示文稿** — 从零创建。进入阶段 1。
- **模式 B：PPT 转换** — 转换 .pptx 文件。进入阶段 4。
- **模式 C：增强** — 改进现有的 HTML 演示文稿。阅读它、理解它、增强它。**遵循下方的模式 C 修改规则。**

### 模式 C：修改规则

在增强现有演示文稿时，固定画布适配是最大的风险：

1. **添加内容之前：** 盘点现有元素，与密度限制对比
2. **添加图片时：** 将其放入 1920×1080 幻灯片画布内。如果幻灯片已达最大内容容量，请拆分为两张幻灯片
3. **添加文字时：** 每张幻灯片最多 4-6 个要点。超出限制？拆分为续接幻灯片
4. **任何修改之后，验证：** 幻灯片画布保持 16:9，无文字溢出卡片，无面板重叠，并且在 1280×720 及一个手机视口下的截图看起来正确
5. **主动重组：** 如果修改将导致溢出，请自动拆分内容并通知用户。不要等待被问及

**向现有幻灯片添加图片时：** 先将图片移到新幻灯片，或减少其他内容。绝不要在未检查现有内容是否已填满 1920×1080 幻灯片画布的情况下添加图片。

---

## 阶段 1：内容发现（新建演示文稿）

**一次性提出所有问题**，让用户一次性填写完毕。如果当前环境提供原生的结构化问题 UI，请使用它；否则用一条简洁的、带清晰编号选项的消息询问：

**问题 1 — 目的**（标题："目的"）：
本演示文稿的用途是什么？选项：路演 PPT / 教学教程 / 大会演讲 / 内部演示

**问题 2 — 长度**（标题："长度"）：
大约需要多少张幻灯片？选项：短 5-10 张 / 中 10-20 张 / 长 20+ 张

**问题 3 — 内容**（标题："内容"）：
是否已准备好内容？选项：内容齐全 / 粗略笔记 / 仅话题方向

**问题 4 — 密度**（标题："密度"）：
演示文稿应该感觉多密集？选项：

- "低密度 / 演讲主导型" — 大观点、少文字、更多视觉留白
- "高密度 / 阅读优先型" — 为异步阅读提供更多自包含的细节

**不要在阶段 1 询问行内编辑相关问题。** 用户在看到草稿前不应被要求选择编辑行为。行内编辑是草稿之后的能力：除非用户明确要求锁定/仅导出的文件，否则默认包含它。

记住用户的密度选择。它会影响幻灯片数量、字号比例、每张幻灯片的文字量、布局密度，以及是偏向电影感的演讲者幻灯片还是自包含的阅读型幻灯片。

如果用户已有内容，请让其分享。

### 步骤 1.2：图片评估（如果提供了图片）

如果用户选择"无图片" → 跳到阶段 2。

如果用户提供图片文件夹：

1. **扫描** — 列出所有图片文件（.png、.jpg、.svg、.webp 等）
2. **检查每张图片** — 使用智能体可用的图像理解能力。如果图像读取不可用，使用文件名/元数据，仅在必要时请用户澄清
3. **评估** — 评估每张图：展示内容、可用或不可用（附原因）、所代表的概念、主色调
4. **共同设计大纲** — 精选图片与文字共同决定幻灯片结构。这不是"先规划幻灯片再加图片" — 而是从一开始就同时围绕两者设计（例如，3 张截图 → 3 张特性幻灯片，1 个 logo → 标题/收尾幻灯片）
5. **使用同样的结构化问题机制确认大纲**（如可用）："这份幻灯片大纲和图片选择看起来合适吗？"选项：看起来不错 / 调整图片 / 调整大纲

**预览中的 Logo：** 如果识别出可用的 Logo，请将其（base64）嵌入阶段 2 的每个样式预览中 —— 用户能看到自己的品牌以三种不同风格呈现。

---

## 阶段 2：风格发现

**这是"展示而非描述"阶段。** 大多数人无法用语言表达自己的设计偏好。

### 步骤 2.0：直接生成 3 个样式预览

基于目的、受众、情绪和内容密度，生成 3 个截然不同的单页 HTML 预览，展示字体、配色、动画和整体美学。

不要询问用户是否需要选项或预设选择器。默认的发现体验始终是可视化对比。

如果用户已经给出氛围提示，请使用它。如果未给出，请从场合、受众、内容和重要程度推断可能的情绪。让选项足够多样化，以便用户能够通过视觉反应，而无需提前表达品味。

如果用户明确指明预设或大胆模板，请将其作为其中一个选项，并围绕它生成剩余的预览位。

阅读 [STYLE_PRESETS.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/STYLE_PRESETS.md) 获取安全的预设候选。如果 [bold-template-pack/selection-index.json](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/bold-template-pack/selection-index.json) 存在，请一并阅读该精简索引，但暂时不要阅读任何 `design.md` 文件。

| 情绪                | 建议预设                                      |
| ------------------- | ---------------------------------------------- |
| 印象深刻/自信       | Bold Signal、Electric Studio、Dark Botanical |
| 兴奋/充满活力       | Creative Voltage、Neon Cyber、Split Pastel   |
| 平静/专注           | Notebook Tabs、Paper & Ink、Swiss Modern     |
| 受启发/被打动       | Dark Botanical、Vintage Editorial、Pastel Geometry |

**预览组合规则：**

- 默认生成 3 个预览：1 个来自 `STYLE_PRESETS.md` 的安全预设，至少 1 个来自 `bold-template-pack/selection-index.json` 的大胆模板，以及 1 个自由发挥。
- 自由发挥可以是第二个大胆模板，也可以是自主生成的自定义设计。选择能针对用户的场合、受众、情绪和内容产生最强、最有用对比的那一个。
- 不要强制每个表现力选项都来自模板库。如果简报中存在比现有模板更尖锐、更具体的设计机会，请使用自由发挥位自由设计。
- 对于保守或高风险的演示文稿，让安全预设尤其克制；选择一个平静、更高正式度的大胆模板；让自由发挥要么是另一个克制的模板，要么是感觉权威而非装饰的自定义设计。
- 对于表现力强的演示文稿，保留安全预设作为可读的备用方案；选择一个强力的大胆模板；让自由发挥大胆冒险、贴合情境，并与其他两个预览明显不同。
- 如果大胆模板匹配感觉较弱，请将自由发挥用作自定义设计，或退回使用另一个安全预设，而不是硬塞模板。

**自定义自由设计规则：**

- 遵循上方的设计美学部分：拒绝通用"AI 速成审美"、默认字体/颜色/布局选择、白底紫色渐变的套路、千篇一律的仪表盘/卡片观感。
- 契合用户声明的场合、受众、情绪/氛围和内容密度。自定义设计应当是为本次演示文稿量身打造的，而非仅仅"有风格"。
- 制定一个深思熟虑的视觉主张：独特的字体排印、坚定的配色、可识别的布局系统，以及一个强有力的氛围或图形手法。
- 保持对完整演示文稿的可行性。预览必须暗示一个可以扩展到分节、内容、引用、对比和收尾幻灯片的设计系统。
- 使用固定的 1920×1080 画布规则，并通过与其他选项相同的预览真实性检查。
- 永远不要在幻灯片本身上渲染"自定义""自由发挥""AI 生成"或设计流程相关的标签。

**大胆模板选择规则：**

- 将用户目的和情绪与 `mood`、`tone`、`best_for`、`avoid_for`、`formality`、`density` 和 `scheme` 进行匹配。
- 将 `best_for` 示例视为软信号，而非严格的行业筛选。
- 保持三个预览彼此真正不同。
- 选定大胆模板候选后，仅从选择索引中 `preview_md` 路径读取这些候选的 `preview.md` 文件。
- `preview.md` 仅用于标题幻灯片预览。在用户选定最终模板之前，不要阅读完整的 `design.md` 文件。
- 除非选定的最终 `design.md` 缺少关键实现细节，否则不要阅读或复制 `template.html`。

**预览真实性规则（不可妥协）：**

- 每个样式预览都必须看起来像用户演示文稿的真实第一张幻灯片，而非诊断卡片。
- 永远不要在幻灯片上渲染内部工作流文字：不要出现 `preview`、`generated from`、`preview.md`、`template`、`preset`、`style option`、`Option A/B/C`、文件名、路径或源文档标签。
- 永远不要在幻灯片本身上渲染模板名称或 slug 名称。模板/样式名称仅出现在给用户的消息中。
- 永远不要将用户需求备注渲染为幻灯片内容，例如"尖锐而挑衅""安全选项""大胆选项""用于内部分享"或"受众：……"，除非用户明确希望这些确切措辞出现在演示文稿中。
- 如果幻灯片需要装饰元素，只使用真正的演示文稿装饰：演示文稿标题、分节标题、日期、作者、公司、页码，或用户材料中的真实内容短语。
- 打开预览之前，检查可见文字，如出现任何内部元数据请修改。

将预览保存到 `.frontend-slides/slide-previews/`（style-a.html、style-b.html、style-c.html）。每个都应自包含且紧凑，展示一张带动画的标题幻灯片。

自动为用户打开每个预览。

### 步骤 2.1：用户选择

询问（标题："样式"）：
您更喜欢哪个样式预览？选项：样式 A：[名称] / 样式 B：[名称] / 样式 C：[名称] / 混合元素

如果选择"混合元素"，请询问具体细节。

---

## 阶段 3：生成演示文稿

使用阶段 1 的内容（文字，或文字 + 精选图片）和阶段 2 的样式生成完整演示文稿。

如果提供了图片，幻灯片大纲已经在步骤 1.2 中纳入了它们。如果没有，CSS 生成的视觉元素（渐变、形状、图案）将提供视觉趣味 — 这是一条完全受支持的一类路径。

全程应用用户的密度选择：

- **低密度 / 演讲主导型：** 使用更多幻灯片，每张承载更少观点。偏好大标题、短语、视觉隐喻、分节停顿、引用/陈述幻灯片，以及适合演讲者的节奏。
- **高密度 / 阅读优先型：** 让幻灯片更具自包含性。使用结构化网格、对比表、带注释的图表、标题和简洁的解释性文案。保持层次分明，让它感觉是经过设计的，而不是把文档粘贴到幻灯片上。

如果用户陈述的需求是混合的，选择更接近的那一种，而非凭空创造中间方案：现场受众说服默认低密度；异步传阅或详细审阅默认高密度。

永远不要让高密度变成视觉杂乱。如果高密度幻灯片开始溢出，请拆分或重新设计为更清晰的结构。

如果用户从 `bold-template-pack` 中选择了大胆模板，请在生成前阅读该模板的完整 `design.md`。不要阅读其他大胆模板。将 `design.md` 视为设计配方：

- 保留其字体、配色、装饰词汇、间距节奏和组件语法。
- 将最终演示文稿生成为统一缩放至视口的固定 1920×1080 画布，无论源模板原本是否使用 `deck-stage.js` 或视口流体 CSS。
- 将 `design.md` 中的视口流体值视为设计比例，转换为 1920×1080 画布坐标。不要在最终演示文稿中将它们保留为活动的视口回流规则。
- 将输出保持为单个自包含的 Frontend Slides HTML 文件。
- 不要复制演示幻灯片内容或过于字面地模仿源模板。
- 仅将 `template.html` 作为选定模板的最终参考。
- 生成后，在浏览器渲染截图中验证内容溢出和面板重叠。仅 `scrollHeight` 检查是不够的，因为网格面板可能在视觉上相互覆盖。

如果用户选择了自主生成的自定义自由发挥，请将该预览的 CSS 和布局视为设计配方：

- 保留其字体、配色、装饰词汇、间距节奏、网格逻辑和组件语法。
- 将同一视觉系统扩展到整份演示文稿。在用户已选择自定义方向后，不要切换到预设或大胆模板。
- 从该系统设计任何缺失的幻灯片布局，而不是从其他样式导入模式。
- 像对待其他演示文稿一样，保持输出固定画布、单文件、并经过视觉验证。

**生成之前，请阅读以下支持文件：**

- [html-template.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/html-template.md) — HTML 架构和 JS 特性
- [viewport-base.css](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/viewport-base.css) — 强制 CSS（完整包含）
- [animation-patterns.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/animation-patterns.md) — 所选感觉的动画参考

**关键要求：**

- 单个自包含 HTML 文件，所有 CSS/JS 内联
- 在 `<style>` 块中包含 `viewport-base.css` 的完整内容
- 使用 Fontshare 或 Google Fonts 的字体 — 永远不要使用系统字体
- 添加详细注释解释每个部分
- 每个部分都需要清晰的 `/* === 章节名称 === */` 注释块

---

## 阶段 4：PPT 转换

转换 PowerPoint 文件时：

1. **提取内容** — 运行 `python scripts/extract-pptx.py <input.pptx> <output_dir>`（如需请安装 python-pptx：`pip install python-pptx`）
2. **与用户确认** — 展示提取的幻灯片标题、内容摘要和图片数量
3. **样式选择** — 进入阶段 2 进行样式发现
4. **生成 HTML** — 转换为所选样式，保留所有文字、图片（来自 assets/）、幻灯片顺序以及演讲者备注（作为 HTML 注释）

---

## 阶段 5：交付

1. **清理** — 如果存在 `.frontend-slides/slide-previews/`，删除它
2. **打开** — 使用 `open [文件名].html` 在浏览器中启动
3. **总结** — 告诉用户：
   - 文件位置、样式名称、幻灯片数量
   - 导航方式：方向键、空格、启用时的滑动/点击
   - 如何自定义：`:root` CSS 变量用于配色，字体链接用于字体排版，`.reveal` 类用于动画
   - 可用行内文字编辑：将鼠标悬停左上角或按 E 进入编辑模式，点击任意文字进行编辑，Ctrl+S 保存
   - 提供草稿后的自然后续操作：请求修改、直接在浏览器中编辑文字、或导出/分享

---

## 阶段 6：分享与导出（可选）

交付后，**询问用户：** _"您想分享这份演示文稿吗？我可以将其部署到线上 URL（在包括手机在内的任何设备上都能用），或导出为 PDF。"_

选项：

- **部署到 URL** — 可分享的链接，可在任何设备上使用
- **导出为 PDF** — 适用于邮件、Slack、打印的通用文件
- **两者都要**
- **暂不需要**

如果用户拒绝，止步于此。如果选择一项或两项，继续下方操作。

### 6A：部署到线上 URL（Vercel）

将演示文稿部署到 Vercel —— 一个免费的托管平台。该链接可在任何设备（手机、平板、笔记本电脑）上使用，并在用户自行下架前一直保持在线。

**如果用户从未部署过，请逐步引导：**

1. **检查是否已安装 Vercel CLI** — 运行 `npx vercel --version`。如果未找到，请先安装 Node.js（macOS 上 `brew install node`，或从 https://nodejs.org 下载）。

2. **检查用户是否已登录** — 运行 `npx vercel whoami`。
   - 如果**未**登录，说明：_"Vercel 是一个免费的托管服务。您需要一个账户才能部署。我来引导您完成："_
     - 步骤 1：让用户在浏览器中打开 https://vercel.com/signup
     - 步骤 2：他们可以使用 GitHub、Google、邮箱注册 —— 哪种方便选哪种
     - 步骤 3：注册完成后，运行 `vercel login` 并按提示操作（它会打开浏览器窗口进行授权）
     - 步骤 4：使用 `vercel whoami` 确认登录
   - 等待用户确认已登录后再继续。

3. **部署** — 运行部署脚本：

   ```bash
   bash scripts/deploy.sh <path-to-presentation>
   ```

   该脚本既接受文件夹（含 index.html），也接受单个 HTML 文件。

4. **分享 URL** — 告诉用户：
   - 线上 URL（来自脚本输出）
   - 可在任何设备上使用 — 可以通过短信、Slack、邮件分享
   - 后续下架：访问 https://vercel.com/dashboard 并删除项目
   - Vercel 免费套餐很慷慨 —— 不会被收费

**⚠ 部署注意事项：**

- **本地图片/视频必须随 HTML 一起上传。** 部署脚本会自动检测 HTML 中通过 `src="..."` 引用的文件并打包。但如果演示文稿通过 CSS `background-image` 或异常路径引用文件，可能会漏掉。**部署前请验证：** 打开部署后的 URL，检查所有图片是否正常加载。如果有损坏，最安全的修复方法是将 HTML 和所有资产放入单个文件夹并部署该文件夹，而不是部署单独的 HTML 文件。
- **当演示文稿有很多资产时，优先使用文件夹部署。** 如果演示文稿与图片位于同一文件夹中（例如 `my-deck/index.html` + `my-deck/logo.png`），请直接部署该文件夹：`bash scripts/deploy.sh ./my-deck/`。这比部署单个 HTML 文件更可靠，因为整个文件夹内容会原样上传。
- **文件名中的空格可以工作但可能引发问题。** 脚本会处理文件名中的空格，但 Vercel URL 会将空格编码为 `%20`。如果可能，请避免在图片文件名中使用空格。如果用户的图片包含空格，脚本会处理 —— 但如果图片仍然损坏，将文件名中的空格替换为连字符即可修复。
- **重新部署会更新同一 URL。** 对同一演示文稿再次运行部署脚本会覆盖先前的部署。URL 保持不变 —— 无需分享新链接。

### 6B：导出为 PDF

将每张幻灯片截屏并合并为 PDF。非常适合邮件附件、嵌入文档或打印。

**注意：** 动画和交互性不会保留 —— PDF 是静态快照。这是正常且可预期的；请向用户说明，以免他们感到意外。

1. **运行导出脚本：**

   ```bash
   bash scripts/export-pdf.sh <path-to-html> [output.pdf]
   ```

   如果未指定输出路径，PDF 将保存在 HTML 文件旁边。

2. **幕后发生了什么**（向用户简要说明）：
   - 无头浏览器以 1920×1080（标准宽屏）打开演示文稿
   - 逐张截屏每张幻灯片
   - 所有截屏合并为单个 PDF
   - 脚本需要 Playwright（一个浏览器自动化工具） —— 如果缺失将自动安装

3. **如果 Playwright 安装失败：**
   - 最常见的问题是 Chromium 未下载。运行：`npx playwright install chromium`
   - 如果也失败，可能是网络/防火墙问题。请用户尝试不同的网络。

4. **交付 PDF** — 脚本会自动打开它。告诉用户：
   - 文件位置和大小
   - 可在任何地方使用 —— 邮件、Slack、Notion、Google Docs、打印
   - 动画被替换为其最终视觉状态（看起来仍然很棒，只是静态的）

**⚠ PDF 导出注意事项：**

- **首次运行较慢。** 脚本会安装 Playwright 并下载 Chromium 浏览器（约 150MB）到临时目录。每个会话仅发生一次。警告用户首次可能需要 30-60 秒 —— 同一会话内的后续导出会更快。
- **幻灯片必须使用 `class="slide"`。** 导出脚本通过查询 `.slide` 元素来查找幻灯片。如果演示文稿使用不同的类名，脚本将报告"找到 0 张幻灯片"并失败。本技能生成的所有演示文稿都使用 `.slide`，因此这只对外部创建的 HTML 有影响。
- **本地图片必须能通过 HTTP 加载。** 脚本启动本地服务器并通过它加载 HTML（这样 Google Fonts 和相对图片路径才能生效）。如果图片使用绝对文件系统路径（例如 `src="/Users/name/photo.png"`）而不是相对路径（例如 `src="photo.png"`），它们将无法加载。生成的演示文稿始终使用相对路径，但转换或用户提供的演示文稿可能不是 —— 请检查并修复。
- **本地图片会出现在 PDF 中**，只要它们与 HTML 文件位于同一目录（或相对于 HTML 文件）。导出脚本通过 HTTP 提供 HTML 的父目录，因此像 `src="photo.png"` 这样的相对路径可以正确解析 —— 包括带空格的文件名。如果图片仍未出现，请检查：(1) 图片文件确实存在于所引用路径，(2) 路径是相对路径，而不是像 `/Users/name/photo.png` 这样的绝对文件系统路径。
- **大型演示文稿会产生大型 PDF。** 每张幻灯片都被截屏为完整的 1920×1080 PNG。18 张幻灯片的演示文稿可能产生约 20MB 的 PDF。如果 PDF 超过 10MB，询问用户：_"PDF 文件大小为 [大小]。需要我压缩吗？它会略显模糊，但文件会小很多。"_ 如果同意，使用 `--compact` 标志重新运行导出：
  ```bash
  bash scripts/export-pdf.sh <path-to-html] [output.pdf] --compact
  ```
  这将以 1280×720 而不是 1920×1080 渲染，通常将文件大小削减 50-70%，视觉差异极小。

---

## 支持文件

| 文件                                               | 用途                                                              | 阅读时机              |
| -------------------------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| [STYLE_PRESETS.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/STYLE_PRESETS.md)               | 12 个精心策划的视觉预设，包含配色、字体和标志性元素 | 阶段 2（样式选择） |
| [bold-template-pack/selection-index.json](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/bold-template-pack/selection-index.json) | 大胆模板候选的精简元数据 | 阶段 2（样式选择） |
| [bold-template-pack/templates/*/preview.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/bold-template-pack/templates/) | 候选大胆标题预览的轻量级样式卡片 | 阶段 2 候选筛选后 |
| [bold-template-pack/templates/*/design.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/bold-template-pack/templates/) | 仅所选大胆模板的详细设计系统文档 | 阶段 3 用户选定后 |
| [viewport-base.css](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/viewport-base.css)             | 强制固定画布 CSS — 复制到每份演示文稿             | 阶段 3（生成）      |
| [html-template.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/html-template.md)               | HTML 结构、JS 特性、代码质量标准                  | 阶段 3（生成）      |
| [animation-patterns.md](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/animation-patterns.md)     | CSS/JS 动画片段和效果-感觉指南                    | 阶段 3（生成）      |
| [scripts/extract-pptx.py](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/scripts/extract-pptx.py) | 用于 PPT 内容提取的 Python 脚本                             | 阶段 4（转换）      |
| [scripts/deploy.sh](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/scripts/deploy.sh)             | 将幻灯片部署到 Vercel 以便即时分享                          | 阶段 6（分享）         |
| [scripts/export-pdf.sh](https://github.com/zarazhangrui/frontend-slides/tree/main/plugins/frontend-slides/skills/frontend-slides/scripts/export-pdf.sh)     | 将幻灯片导出为 PDF                                                 | 阶段 6（分享）         |

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时，才使用本技能。
- 在应用更改之前，请验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例视为针对特定环境的测试、安全审查或用户对破坏性或昂贵操作的批准的替代品。