---
name: design-it
description: "将前端设计任务路由到 48 种具体 UI 风格。适用于网站、应用界面或 UI 组件需要特定美学效果的场景。"
category: frontend
risk: safe
source: self
source_type: self
date_added: "2026-06-17"
author: community
tags: [design, ui, frontend]
tools: [claude, cursor, gemini]
---

# Design-It：高级 UI 风格路由

这是 **design-it** 技能系统的主入口。摒弃千篇一律的"AI 流水线"美学，你将拥有 48 种风格鲜明、立场鲜明的设计风格。

## 使用时机

当用户请求构建任意前端界面（网站、应用界面、UI 组件），并且希望采用一种风格鲜明的、有立场的设计美学而非通用默认值时，使用此技能。

## 使用方法

当用户要求你构建前端界面（Web 或 App）时：
1. **识别风格（模糊匹配）**：在用户的提示词中寻找关键词（例如"极简"、"玻璃"、"复古"）。无需精确匹配。利用语义理解，将他们的请求映射到 48 种风格中的一种。例如：
   - "Apple 风格"或"VisionOS" → `spatial-design`、`bento-ui` 或 `glassmorphism`
   - "Windows 8"或"Metro" → `tile-design`
   - "终端"或"黑客" → `sci-fi-interface` 或 `brutalist-typography`
   - "包豪斯"或"干净" → `swiss-design`
   - "赛博"或"黑客帝国" → `cyberpunk-ui`
   如果用户未指定风格，请选择最契合项目背景的一种。
2. **阅读风格参考**：查看下面的 **风格索引**，找到所选风格的正确路径。使用 `view_file` 工具读取其对应的 `SKILL.md`。
3. **选择调色板**：如果用户明确定义了主题或颜色，**请使用他们指定的颜色**。如果用户未指定颜色，你必须从下面的 **10 套通用调色板** 中选择一套。
4. **执行**：按照所选风格的特定原则编写代码。除非用户明确要求，否则不要混合多种风格。

## 通用调色板

如果用户提供了自己的颜色，请使用用户的颜色。否则，你必须使用这 10 套获奖的、高度精致的调色板之一，避免使用通用霓虹色或紫色渐变。选择调色板时，请严格使用以下十六进制色值，并为它们建立 CSS 变量。

1. **Yacht Club**（航海 / 经典优雅）
   - 背景：`#F9F6F0`
   - 主文字/强调：`#1B2A49`
   - CTA/高亮：`#C85A32`
   - 次要基础色：`#E2D8C9`
2. **Desert Mirage**（温暖 / 有机）
   - 背景：`#F4EFEA`
   - 主文字/强调：`#2D2B2A`
   - CTA/高亮：`#A65E44`
   - 次要基础色：`#8C8781`
3. **Industrial Chic**（强烈 / 极简）
   - 背景：`#D1D1D1`
   - 主文字/强调：`#111111`
   - CTA/高亮：`#9A3B3B`
   - 次要基础色：`#757575`
4. **Monochromatic Brown**（舒适 / 怀旧）
   - 背景：`#D9CBBF`
   - 主文字/强调：`#4A362D`
   - CTA/高亮：`#7A4C3A`
   - 次要基础色：`#948275`
5. **Earth-Grounded Elegance**（平静 / 可持续）
   - 背景：`#F7F5F0`
   - 主文字/强调：`#3A4B3A`
   - CTA/高亮：`#8A9A86`
   - 次要基础色：`#D3CEC4`
6. **Minimalist Slate**（专业 / 科技）
   - 背景：`#F4F4F9`
   - 主文字/强调：`#2B303A`
   - CTA/高亮：`#5C6B73`
   - 次要基础色：`#C0C5C1`
7. **Midnight Luxury**（高级 / 暗色模式）
   - 背景：`#0A0A0A`
   - 主文字/强调：`#F5F5F0`
   - CTA/高亮：`#B59A5F`
   - 次要基础色：`#1C1C1C`
8. **Sophisticated Neutral**（高端 / 生活方式）
   - 背景：`#E6E2DD`
   - 主文字/强调：`#1F1C1B`
   - CTA/高亮：`#524036`
   - 次要基础色：`#B8B0A8`
9. **Warm Tech**（企业 / 现代）
   - 背景：`#EAEAEA`
   - 主文字/强调：`#1C252E`
   - CTA/高亮：`#C28F79`
   - 次要基础色：`#2C3E50`
10. **Modern Editorial**（杂志 / 高对比度）
    - 背景：`#F9F9F9`
    - 主文字/强调：`#121212`
    - CTA/高亮：`#D44A3A`
    - 次要基础色：`#8F8F8F`

## 60-30-10 法则
- **60%**：背景 / 次要基础色
- **30%**：主文字 / 强调色
- **10%**：CTA / 高亮色

---

## 风格索引（48 种）

要使用某种风格，你必须读取其文件路径 `<style-folder>/SKILL.md`（相对于本文件所在目录）。

### 现代 UI
- `minimalism`
- `flat-design`
- `flat-design-2`
- `material-design`
- `glassmorphism`
- `neumorphism`
- `skeuomorphism`
- `claymorphism`
- `aurora-ui`
- `bento-ui`

### 深度与 3D
- `3d-ui`
- `isometric-design`
- `layered-design`
- `floating-ui`
- `spatial-design`

### 排版
- `swiss-design`
- `editorial-design`
- `typography-first`
- `brutalist-typography`

### 复古与历史
- `brutalism`
- `neo-brutalism`
- `retro-design`
- `y2k-design`
- `cyber-y2k`
- `vaporwave`
- `synthwave`
- `frutiger-aero`
- `retro-futurism`

### 现代趋势
- `dark-mode`
- `monochromatic-ui`
- `gradient-design`
- `duotone-design`
- `color-blocking`
- `soft-pastel`
- `high-contrast`
- `vibrant-maximalism`
- `maximalism`

### 未来主义
- `cyberpunk-ui`
- `sci-fi-interface`
- `holographic-ui`
- `ai-native-ui`
- `spatial-computing-ui`

### 数据与产品
- `dashboard-design`
- `card-based-design`
- `widget-based-design`
- `tile-design`
- `data-dense-design`
- `command-center-ui`

## Web 与 App 实现
- **Web（React/Vue/HTML）**：原生使用 CSS 变量。布局优先使用 CSS grid/flexbox。悬停状态使用 CSS transition。
- **App（React Native/Flutter/SwiftUI）**：将调色板映射到框架的主题引擎。使用平台特定的阴影（elevation）和动画替代 CSS transition。在遵循核心视觉原则的同时，适配移动端约束。

## 限制

- 此技能不能替代特定环境的验证、测试或专家评审。
- 如果缺少必要的输入、权限或安全边界，请停下来并请求澄清。