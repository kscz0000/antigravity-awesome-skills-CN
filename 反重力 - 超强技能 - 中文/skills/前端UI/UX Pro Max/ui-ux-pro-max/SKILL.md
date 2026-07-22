---
name: ui-ux-pro-max
description: "Web 和移动端应用的综合设计指南。设计新 UI 组件或页面、选择配色方案和排版、审查代码中的 UX 问题时使用。触发词：UI 设计、UX 设计、界面设计、配色方案、字体搭配、无障碍、响应式、落地页、仪表盘、设计系统"
risk: unknown
source: community
date_added: "2026-02-27"
---

# UI/UX Pro Max - 设计智能

Web 和移动端应用的综合设计指南。涵盖 50+ 种风格、97 套配色方案、57 组字体搭配、99 条 UX 准则和 25 种图表类型，横跨 9 个技术栈。内置可搜索数据库，提供基于优先级的推荐。

## 适用场景
在以下场景中参考这些准则：
- 设计新的 UI 组件或页面
- 选择配色方案和排版
- 审查代码中的 UX 问题
- 构建落地页或仪表盘
- 实现无障碍需求

## 按优先级分类的规则

| 优先级 | 类别 | 影响 | 领域 |
|--------|------|------|------|
| 1 | 无障碍 | 关键 | `ux` |
| 2 | 触控与交互 | 关键 | `ux` |
| 3 | 性能 | 高 | `ux` |
| 4 | 布局与响应式 | 高 | `ux` |
| 5 | 排版与配色 | 中 | `typography`, `color` |
| 6 | 动画 | 中 | `ux` |
| 7 | 风格选择 | 中 | `style`, `product` |
| 8 | 图表与数据 | 低 | `chart` |

## 快速参考

### 1. 无障碍（关键）

- `color-contrast` - 正文文本最低 4.5:1 对比度
- `focus-states` - 交互元素必须有可见的焦点环
- `alt-text` - 有意义的图片需提供描述性 alt 文本
- `aria-labels` - 纯图标按钮需添加 aria-label
- `keyboard-nav` - Tab 顺序与视觉顺序一致
- `form-labels` - 使用带 for 属性的 label

### 2. 触控与交互（关键）

- `touch-target-size` - 触控目标最小 44x44px
- `hover-vs-tap` - 主要交互使用 click/tap
- `loading-buttons` - 异步操作期间禁用按钮
- `error-feedback` - 在问题附近显示清晰的错误信息
- `cursor-pointer` - 可点击元素添加 cursor-pointer

### 3. 性能（高）

- `image-optimization` - 使用 WebP、srcset、懒加载
- `reduced-motion` - 检查 prefers-reduced-motion
- `content-jumping` - 为异步内容预留空间

### 4. 布局与响应式（高）

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - 移动端正文最小 16px
- `horizontal-scroll` - 确保内容适配视口宽度
- `z-index-management` - 定义 z-index 层级（10, 20, 30, 50）

### 5. 排版与配色（中）

- `line-height` - 正文行高 1.5-1.75
- `line-length` - 每行限制 65-75 个字符
- `font-pairing` - 标题与正文字体风格匹配

### 6. 动画（中）

- `duration-timing` - 微交互时长 150-300ms
- `transform-performance` - 使用 transform/opacity，而非 width/height
- `loading-states` - 骨架屏或加载指示器

### 7. 风格选择（中）

- `style-match` - 风格与产品类型匹配
- `consistency` - 所有页面使用统一风格
- `no-emoji-icons` - 使用 SVG 图标，不用 emoji

### 8. 图表与数据（低）

- `chart-type` - 图表类型与数据类型匹配
- `color-guidance` - 使用无障碍配色方案
- `data-table` - 提供表格替代方案以增强无障碍性

## 使用方式

使用下方 CLI 工具搜索特定领域。

---

## 前置条件

检查是否已安装 Python：

```bash
python3 --version || python --version
```

如果未安装 Python，请根据操作系统安装：

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## 技能使用指南

当用户请求 UI/UX 相关工作（设计、构建、创建、实现、审查、修复、优化）时，按以下流程执行：

### 步骤 1：分析用户需求

从用户请求中提取关键信息：
- **产品类型**：SaaS、电商、作品集、仪表盘、落地页等
- **风格关键词**：极简、活泼、专业、优雅、暗色模式等
- **行业**：医疗、金融科技、游戏、教育等
- **技术栈**：React、Vue、Next.js，默认使用 `html-tailwind`

### 步骤 2：生成设计系统（必需）

**始终先执行 `--design-system`** 获取带推理的综合推荐：

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

此命令会：
1. 并行搜索 5 个领域（产品、风格、配色、落地页、排版）
2. 应用 `ui-reasoning.csv` 中的推理规则选择最佳匹配
3. 返回完整设计系统：模式、风格、配色、排版、效果
4. 包含需要避免的反模式

**示例：**
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 步骤 3：补充详细搜索（按需）

获取设计系统后，使用领域搜索获取更多细节：

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**何时使用详细搜索：**

| 需求 | 领域 | 示例 |
|------|------|------|
| 更多风格选项 | `style` | `--domain style "glassmorphism dark"` |
| 图表推荐 | `chart` | `--domain chart "real-time dashboard"` |
| UX 最佳实践 | `ux` | `--domain ux "animation accessibility"` |
| 替代字体 | `typography` | `--domain typography "elegant luxury"` |
| 落地页结构 | `landing` | `--domain landing "hero social-proof"` |

### 步骤 4：技术栈指南（默认：html-tailwind）

获取特定技术栈的最佳实践。用户未指定技术栈时，**默认使用 `html-tailwind`**。

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

可用技术栈：`html-tailwind`、`react`、`nextjs`、`vue`、`svelte`、`swiftui`、`react-native`、`flutter`、`shadcn`

---

## 搜索参考

### 可用领域

| 领域 | 用途 | 示例关键词 |
|------|------|-----------|
| `product` | 产品类型推荐 | SaaS、电商、作品集、医疗、美容、服务 |
| `style` | UI 风格、配色、效果 | glassmorphism、极简、暗色模式、粗野主义 |
| `typography` | 字体搭配、Google Fonts | 优雅、活泼、专业、现代 |
| `color` | 按产品类型的配色方案 | saas、ecommerce、healthcare、beauty、fintech、service |
| `landing` | 页面结构、CTA 策略 | hero、hero-centric、testimonial、pricing、social-proof |
| `chart` | 图表类型、库推荐 | trend、comparison、timeline、funnel、pie |
| `ux` | 最佳实践、反模式 | animation、accessibility、z-index、loading |
| `react` | React/Next.js 性能 | waterfall、bundle、suspense、memo、rerender、cache |
| `web` | Web 界面准则 | aria、focus、keyboard、semantic、virtualize |
| `prompt` | AI 提示词、CSS 关键词 | （风格名称） |

### 可用技术栈

| 技术栈 | 重点 |
|--------|------|
| `html-tailwind` | Tailwind 工具类、响应式、无障碍（默认） |
| `react` | 状态、hooks、性能、模式 |
| `nextjs` | SSR、路由、图片、API 路由 |
| `vue` | Composition API、Pinia、Vue Router |
| `svelte` | Runes、stores、SvelteKit |
| `swiftui` | Views、State、Navigation、Animation |
| `react-native` | Components、Navigation、Lists |
| `flutter` | Widgets、State、Layout、Theming |
| `shadcn` | shadcn/ui 组件、主题、表单、模式 |

---

## 示例工作流

**用户请求：** "为专业护肤服务做一个落地页"

### 步骤 1：分析需求
- 产品类型：美容/SPA 服务
- 风格关键词：优雅、专业、柔和
- 行业：美容/健康
- 技术栈：html-tailwind（默认）

### 步骤 2：生成设计系统（必需）

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**输出：** 完整设计系统，包含模式、风格、配色、排版、效果和反模式。

### 步骤 3：补充详细搜索（按需）

```bash
# 获取动画和无障碍的 UX 指南
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# 如需要，获取替代排版方案
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### 步骤 4：技术栈指南

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**然后：** 综合设计系统 + 详细搜索结果，实现设计。

---

## 输出格式

`--design-system` 标志支持两种输出格式：

```bash
# ASCII 框（默认）- 适合终端显示
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - 适合文档
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## 优化搜索结果的技巧

1. **关键词要具体** - "healthcare SaaS dashboard" > "app"
2. **多次搜索** - 不同关键词揭示不同洞察
3. **组合领域** - 风格 + 排版 + 配色 = 完整设计系统
4. **始终检查 UX** - 搜索 "animation"、"z-index"、"accessibility" 排查常见问题
5. **使用 stack 标志** - 获取特定技术栈的最佳实践
6. **迭代优化** - 首次搜索不匹配时，尝试不同关键词

---

## 专业 UI 常见规则

以下是经常被忽略、导致 UI 显得不专业的问题：

### 图标与视觉元素

| 规则 | 正确做法 | 错误做法 |
|------|---------|---------|
| **不用 emoji 做图标** | 使用 SVG 图标（Heroicons、Lucide、Simple Icons） | 用 🎨 🚀 ⚙️ 等 emoji 做 UI 图标 |
| **稳定的 hover 状态** | hover 时使用颜色/透明度过渡 | 使用导致布局偏移的 scale 变换 |
| **正确的品牌 logo** | 从 Simple Icons 查找官方 SVG | 猜测或使用错误的 logo 路径 |
| **统一的图标尺寸** | 使用固定 viewBox (24x24) 和 w-6 h-6 | 随机混用不同图标尺寸 |

### 交互与光标

| 规则 | 正确做法 | 错误做法 |
|------|---------|---------|
| **cursor pointer** | 所有可点击/可悬停的卡片添加 `cursor-pointer` | 交互元素保留默认光标 |
| **hover 反馈** | 提供视觉反馈（颜色、阴影、边框） | 无任何交互指示 |
| **平滑过渡** | 使用 `transition-colors duration-200` | 瞬间切换状态或过渡太慢（>500ms） |

### 明/暗模式对比度

| 规则 | 正确做法 | 错误做法 |
|------|---------|---------|
| **明模式毛玻璃卡片** | 使用 `bg-white/80` 或更高透明度 | 使用 `bg-white/10`（过于透明） |
| **明模式文本对比度** | 使用 `#0F172A`（slate-900）做文本 | 使用 `#94A3B8`（slate-400）做正文 |
| **明模式弱化文本** | 最低使用 `#475569`（slate-600） | 使用 gray-400 或更浅 |
| **边框可见性** | 明模式使用 `border-gray-200` | 使用 `border-white/10`（不可见） |

### 布局与间距

| 规则 | 正确做法 | 错误做法 |
|------|---------|---------|
| **浮动导航栏** | 添加 `top-4 left-4 right-4` 间距 | 导航栏紧贴 `top-0 left-0 right-0` |
| **内容内边距** | 考虑固定导航栏的高度 | 内容被固定元素遮挡 |
| **统一最大宽度** | 使用相同的 `max-w-6xl` 或 `max-w-7xl` | 混用不同容器宽度 |

---

## 交付前检查清单

交付 UI 代码前，逐项验证：

### 视觉质量
- [ ] 未使用 emoji 做图标（改用 SVG）
- [ ] 所有图标来自统一图标集（Heroicons/Lucide）
- [ ] 品牌 logo 正确（已从 Simple Icons 验证）
- [ ] hover 状态不导致布局偏移
- [ ] 直接使用主题色（bg-primary）而非 var() 包装

### 交互
- [ ] 所有可点击元素都有 `cursor-pointer`
- [ ] hover 状态提供清晰的视觉反馈
- [ ] 过渡动画平滑（150-300ms）
- [ ] 键盘导航时焦点状态可见

### 明/暗模式
- [ ] 明模式文本对比度充足（最低 4.5:1）
- [ ] 毛玻璃/透明元素在明模式下可见
- [ ] 两种模式下边框均可见
- [ ] 交付前测试两种模式

### 布局
- [ ] 浮动元素与边缘有适当间距
- [ ] 内容未被固定导航栏遮挡
- [ ] 在 375px、768px、1024px、1440px 下响应式正常
- [ ] 移动端无水平滚动

### 无障碍
- [ ] 所有图片有 alt 文本
- [ ] 表单输入有 label
- [ ] 颜色不是唯一的信息指示方式
- [ ] 遵循 `prefers-reduced-motion` 设置

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为替代环境特定的验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清。
