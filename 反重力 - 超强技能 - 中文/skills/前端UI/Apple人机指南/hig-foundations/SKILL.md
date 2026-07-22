---
name: hig-foundations
description: Apple 人机交互指南设计基础。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 设计基础

提问前请检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未覆盖的信息。

## 核心原则

1. **内容优先于装饰。** 减少视觉杂乱。使用系统提供的材质和细微的分隔线，而非厚重的边框和背景。

2. **从一开始就构建无障碍。** 从第一天起就为 VoiceOver、动态字体、减少动态、增强对比度和切换控制设计。每个交互元素都需要无障碍标签。

3. **使用系统颜色和材质。** 系统颜色自适应浅色/深色模式、增强对比度和活力。优先使用语义颜色（`label`、`secondaryLabel`、`systemBackground`）而非硬编码值。

4. **使用平台字体和图标。** 默认使用 SF Pro、SF Compact、SF Mono。衬线字体用 New York。遵循推荐尺寸的字体层级。图标使用 SF Symbols。

5. **匹配平台规范。** 使外观和行为与系统标准保持一致。为每个操作提供直接、响应式的操作和清晰的反馈。

6. **尊重隐私。** 仅在需要时请求权限，清楚解释原因，在请求数据前提供价值。为最小化数据收集设计。

7. **支持国际化。** 适应文本扩展、从右到左的脚本和不同的日期/数字格式。使用 Auto Layout 进行动态内容尺寸调整。

8. **有目的地使用动效。** 动画应传达含义和空间关系。通过提供淡入淡出替代方案来尊重减少动态偏好。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [accessibility.md](references/accessibility.md) | 无障碍 | VoiceOver、动态字体、颜色对比度、运动无障碍、切换控制、音频描述 |
| [app-icons.md](references/app-icons.md) | 应用图标 | 图标网格、平台特定尺寸、单一焦点、无透明度 |
| [branding.md](references/branding.md) | 品牌塑造 | 在 Apple 设计语言中整合品牌标识、微妙品牌化、自定义色调 |
| [color.md](references/color.md) | 颜色 | 系统颜色、动态颜色、语义颜色、自定义调色板、对比度比率 |
| [dark-mode.md](references/dark-mode.md) | 深色模式 | 抬升表面、语义颜色、适配调色板、活力、两种模式测试 |
| [icons.md](references/icons.md) | 图标 | 字形图标、SF Symbols 集成、自定义图标设计、图标粗细、光学对齐 |
| [images.md](references/images.md) | 图像 | 图像分辨率、@2x/@3x 资产、矢量资产、图像无障碍 |
| [immersive-experiences.md](references/immersive-experiences.md) | 沉浸式体验 | AR/VR 设计、空间沉浸、舒适区域、渐进式沉浸级别 |
| [inclusion.md](references/inclusion.md) | 包容性 | 多元化表现、非性别化语言、文化敏感性、包容性默认值 |
| [layout.md](references/layout.md) | 布局 | 边距、间距、对齐、安全区域、自适应布局、可读内容指南 |
| [materials.md](references/materials.md) | 材质 | 活力、模糊、半透明、系统材质、材质厚度 |
| [motion.md](references/motion.md) | 动效 | 动画曲线、转场、连续性、减少动态支持、基于物理的动效 |
| [privacy.md](references/privacy.md) | 隐私 | 权限请求、使用说明、隐私营养标签、最小化数据收集 |
| [right-to-left.md](references/right-to-left.md) | 从右到左 | RTL 布局镜像、双向文本、翻转的图标、例外情况 |
| [sf-symbols.md](references/sf-symbols.md) | SF Symbols | 符号类别、渲染模式、可变颜色、自定义符号、粗细匹配 |
| [spatial-layout.md](references/spatial-layout.md) | 空间布局 | visionOS 窗口放置、深度、人体工学区域、Z 轴设计 |
| [typography.md](references/typography.md) | 排版 | SF Pro、动态字体尺寸、文本样式、自定义字体、字体粗细层级、行间距 |
| [writing.md](references/writing.md) | 文案 | UI 文案指南、语气、大写规则、错误消息、按钮标签、简洁性 |

## 综合应用基础

考虑原则如何相互作用：

1. **颜色 + 深色模式 + 无障碍** — 自定义调色板必须在两种模式下都能工作，同时保持 WCAG 对比度比率。从系统语义颜色开始。

2. **排版 + 无障碍 + 布局** — 动态字体必须在不破坏布局的情况下缩放。使用文本样式和 Auto Layout 适应完整的字体尺寸范围。

3. **图标 + 品牌塑造 + SF Symbols** — 自定义图标应匹配 SF Symbols 的粗细和光学尺寸。品牌元素应整合而非覆盖系统规范。

4. **动效 + 无障碍 + 反馈** — 每个动画都必须有减少动态替代方案。动效应加强空间关系，而非装饰。

5. **隐私 + 文案 + 引导流程** — 权限请求需要清晰、具体的使用说明。在用户能理解益处时再请求。

## 输出格式

1. **引用具体的 HIG 基础**，包括文件和章节。
2. **说明用户目标平台的平台差异**。
3. **提供具体的代码模式**（SwiftUI/UIKit/AppKit）。
4. **解释无障碍影响**（对比度比率、动态字体缩放、VoiceOver 行为）。

## 需要询问的问题

1. 您的目标平台有哪些？
2. 您有现有的品牌指南吗？
3. 您的目标无障碍级别是什么？（WCAG AA、AAA、Apple 基准？）
4. 系统颜色还是自定义？

## 相关技能

- **hig-platforms** — 基础如何应用于各平台（例如 watchOS 与 macOS 的字体缩放差异）
- **hig-patterns** — 文案和无障碍等基础至关重要的交互模式
- **hig-components-layout** — 实现布局原则的结构组件
- **hig-components-content** — 使用颜色、排版和图像的内容展示

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
