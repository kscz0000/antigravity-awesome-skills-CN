---
name: stitch-ui-design
description: "Google Stitch 提示词编写专家指南。Google Stitch 是 Google Labs 推出的 AI 驱动 UI 设计工具，本技能帮助用户创建精准、可执行的提示词，生成高质量的 Web 和移动端 UI 设计。触发词：Stitch UI 设计、Google Stitch 提示词、AI UI 生成、UI 设计提示词"
risk: safe
source: self
date_added: "2026-02-27"
---

# Stitch UI 设计提示词指南

Google Stitch 提示词编写专家指南。Google Stitch 是 Google Labs 推出的 AI 驱动 UI 设计工具，本技能帮助用户创建精准、可执行的提示词，生成高质量的 Web 和移动端 UI 设计。

## 什么是 Google Stitch？

Google Stitch 是由 Gemini 2.5 Flash 驱动的实验性 AI UI 生成器，能将文本提示词和视觉参考转化为可用的 UI 设计。支持：

- 从自然语言提示词生成 UI
- 从草图、线框图或截图转换为 UI
- 多屏应用流程和响应式布局
- 导出为 HTML/CSS、Figma 和代码
- 通过变体和标注进行迭代优化

## 核心提示词原则

### 1. 具体且详细

泛泛的提示词只能得到泛泛的结果。带有明确要求的具体提示词才能产出量身定制的专业设计。

**反面示例：**
```
Create a dashboard
```

**正面示例：**
```
Member dashboard with course modules grid, progress tracking bar, 
and community feed sidebar using purple theme and card-based layout
```

**为什么有效：** 明确指定了组件（模块、进度、动态流）、布局结构（网格、侧边栏）、视觉风格（紫色主题、卡片式）和使用场景（会员仪表盘）。

### 2. 定义视觉风格和主题

始终包含配色方案、设计美学和视觉方向，避免产出千篇一律的 AI 设计。

**需要指定的要素：**
- 调色板（主色、强调色）
- 设计风格（极简、现代、活泼、专业、毛玻璃）
- 字体偏好（如有）
- 间距和密度（紧凑、宽松、均衡）

**示例：**
```
E-commerce product page with hero image gallery, add-to-cart CTA, 
reviews section, and related products carousel. Use clean minimalist 
design with sage green accents and generous white space.
```

### 3. 清晰组织多屏流程

对于多屏应用，在生成前用列表逐一说明每个屏幕。

**方法：**
```
Fitness tracking app with:
- Onboarding screen with goal selection
- Home dashboard with daily stats and activity rings
- Workout library with category filters
- Profile screen with achievements and settings
```

Stitch 会在生成多屏前请求确认，确保与你的构想一致。

### 4. 指定平台和响应式行为

说明设计面向手机、平板、桌面还是响应式网页。

**示例：**
```
Mobile app login screen (iOS style) with email/password fields and social auth buttons

Responsive landing page that adapts from mobile (320px) to desktop (1440px) 
with collapsible navigation
```

### 5. 包含功能需求

描述交互元素、状态和用户流程，生成更完整的设计。

**需要指定的要素：**
- 按钮行为和 CTA
- 表单字段和验证
- 导航模式
- 加载状态
- 空状态
- 错误处理

**示例：**
```
Checkout flow with:
- Cart summary with quantity adjusters
- Shipping address form with validation
- Payment method selection (cards, PayPal, Apple Pay)
- Order confirmation with tracking number
```

## 提示词结构模板

使用此模板编写全面的提示词：

```
[Screen/Component Type] for [User/Context]

Key Features:
- [Feature 1 with specific details]
- [Feature 2 with specific details]
- [Feature 3 with specific details]

Visual Style:
- [Color scheme]
- [Design aesthetic]
- [Layout approach]

Platform: [Mobile/Web/Responsive]
```

**示例：**
```
Dashboard for SaaS analytics platform

Key Features:
- Top metrics cards showing MRR, active users, churn rate
- Line chart for revenue trends (last 30 days)
- Recent activity feed with user actions
- Quick action buttons for reports and exports

Visual Style:
- Dark mode with blue/purple gradient accents
- Modern glassmorphic cards with subtle shadows
- Clean data visualization with accessible colors

Platform: Responsive web (desktop-first)
```

## 迭代策略

### 用标注精修

使用 Stitch 的"标注编辑"功能进行针对性修改，无需重写整个提示词。

**工作流程：**
1. 根据提示词生成初始设计
2. 标注需要修改的具体元素
3. 用自然语言描述修改内容
4. Stitch 仅更新标注区域

**标注示例：**
- "把这个按钮放大，使用主色"
- "在这些卡片之间增加间距"
- "改为水平布局"

### 生成变体

请求多个变体以探索不同设计方向：

```
Generate 3 variants of this hero section:
1. Image-focused with minimal text
2. Text-heavy with supporting graphics
3. Video background with overlay content
```

### 渐进式精修

从宽泛开始，在后续提示词中逐步增加细节：

**初始：**
```
E-commerce homepage
```

**精修 1：**
```
Add featured products section with 4-column grid and hover effects
```

**精修 2：**
```
Update color scheme to earth tones (terracotta, sage, cream) 
and add promotional banner at top
```

## 常见用例

### 落地页

```
SaaS landing page for [product name]

Sections:
- Hero with headline, subheadline, CTA, and product screenshot
- Social proof with customer logos
- Features grid (3 columns) with icons
- Testimonials carousel
- Pricing table (3 tiers)
- FAQ accordion
- Footer with links and newsletter signup

Style: Modern, professional, trust-building
Colors: Navy blue primary, light blue accents, white background
```

### 移动应用

```
Food delivery app home screen

Components:
- Search bar with location selector
- Category chips (Pizza, Burgers, Sushi, etc.)
- Restaurant cards with image, name, rating, delivery time, and price range
- Bottom navigation (Home, Search, Orders, Profile)

Style: Vibrant, appetite-appealing, easy to scan
Colors: Orange primary, white background, food photography
Platform: iOS mobile (375px width)
```

### 仪表盘

```
Admin dashboard for content management system

Layout:
- Left sidebar navigation with collapsible menu
- Top bar with search, notifications, and user profile
- Main content area with:
  - Stats overview (4 metric cards)
  - Recent posts table with actions
  - Activity timeline
  - Quick actions panel

Style: Clean, data-focused, professional
Colors: Neutral grays with blue accents
Platform: Desktop web (1440px)
```

### 表单和输入

```
Multi-step signup form for B2B platform

Steps:
1. Account details (company name, email, password)
2. Company information (industry, size, role)
3. Team setup (invite members)
4. Confirmation with success message

Features:
- Progress indicator at top
- Field validation with inline errors
- Back/Next navigation
- Skip option for step 3

Style: Minimal, focused, low-friction
Colors: White background, green for success states
```

## 设计转代码工作流

### 导出选项

Stitch 提供多种导出格式：

1. **HTML/CSS** - 干净的语义化标记，适用于 Web 项目
2. **Figma** - "粘贴到 Figma"，便于设计系统集成
3. **代码片段** - 组件级导出，适用于各框架

### 导出最佳实践

**导出前：**
- 验证响应式断点
- 检查颜色对比度是否符合无障碍标准
- 确保交互状态已定义
- 审查组件命名和结构

**导出后：**
- 重构生成的代码以符合生产标准
- 添加语义化 HTML 标签
- 实现无障碍属性（ARIA 标签、alt 文本）
- 优化图片和资源
- 添加动画和微交互

## 需要避免的反模式

### ❌ 模糊的提示词
```
Make a nice website
```

### ✅ 具体的提示词
```
Portfolio website for photographer with full-screen image gallery, 
project case studies, and contact form. Minimalist black and white 
aesthetic with serif typography.
```

---

### ❌ 缺少上下文
```
Create a login page
```

### ✅ 上下文丰富的提示词
```
Login page for healthcare portal with email/password fields, 
"Remember me" checkbox, "Forgot password" link, and SSO options 
(Google, Microsoft). Professional, trustworthy design with 
blue medical theme.
```

---

### ❌ 没有视觉方向
```
Design an app for task management
```

### ✅ 视觉方向清晰
```
Task management app with kanban board layout, drag-and-drop cards, 
priority labels, and due date indicators. Modern, productivity-focused 
design with purple/teal gradient accents and dark mode support.
```

## 提升效果的技巧

1. **参考现有设计** - 在文本提示词之外上传截图或草图作为视觉参考

2. **使用设计术语** - "hero section""卡片布局""毛玻璃""bento grid"等术语帮助 Stitch 理解你的意图

3. **指定交互行为** - 描述悬停状态、点击行为和过渡动画，获得更完整的设计

4. **以组件思维拆分** - 将复杂屏幕拆解为可复用组件（头部、卡片、表单等）

5. **渐进式迭代** - 做小而聚焦的修改，而非推倒重来

6. **测试响应式** - 始终在多个断点（手机、平板、桌面）验证设计

7. **考虑无障碍** - 在提示词中提及颜色对比度、字号和触控目标尺寸

8. **善用变体** - 生成多个选项以快速探索不同设计方向

## 与开发工作流集成

### Stitch → Figma → 代码
1. 在 Stitch 中用详细提示词生成 UI
2. 导出到 Figma 进行设计系统集成
3. 附带设计规范交付给开发人员
4. 用生产级代码实现

### Stitch → HTML → 框架
1. 在 Stitch 中生成并精修 UI
2. 导出 HTML/CSS 代码
3. 转换为 React/Vue/Svelte 组件
4. 集成到应用代码库

### 快速原型
1. 快速生成多个屏幕变体
2. 与用户或利益相关者测试
3. 根据反馈迭代
4. 确定最终设计进入开发

## 总结

有效的 Stitch 提示词应当具体、上下文丰富且具有视觉描述力。遵循这些原则和模板，你可以生成专业的 UI 设计，为生产级应用打下坚实基础。

**记住：** Stitch 是起点而非终点。用它加速设计流程、快速探索创意、确定视觉方向——然后用人类判断力和生产标准进行打磨。

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为替代环境特定的验证、测试或专家评审。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
