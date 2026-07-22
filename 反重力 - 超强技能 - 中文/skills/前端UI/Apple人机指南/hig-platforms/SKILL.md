---
name: hig-platforms
description: Apple 人机交互指南平台特定设计。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 平台设计

提问前请检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未覆盖的信息。

## 核心原则

1. **每个平台都有独特的身份。** 不要在平台之间移植设计。尊重每个平台的规范、交互模型和用户期望。

2. **iOS：触控优先。** 手持屏幕上的直接操作。优化单手使用。导航使用标签栏和推入/弹出栈。

3. **iPadOS：扩展画布。** 支持分屏视图、侧拉和台前调度。使用侧边栏和多列布局。同时支持指针、键盘和触控。

4. **macOS：指针和键盘。** 可接受密集的信息展示。广泛使用菜单栏、工具栏和键盘快捷键。窗口可调整大小，具有精确控制。

5. **tvOS：遥控和焦点。** 远距离观看。为 Siri Remote 设计基于焦点的导航。大文本、简单布局、线性导航。

6. **visionOS：空间交互。** 使用窗口、体积和空间的 3D 环境。眼动追踪用于定位，间接手势用于交互。尊重人体工学舒适区域。

7. **watchOS：一瞥即得且简短。** 信息可一瞥即得。简短交互。数码表冠、触觉和复杂功能用于及时内容。

8. **游戏：自有范式。** 可自由定义游戏内交互模型，但仍需尊重系统交互的平台规范（通知、无障碍、控制器）。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [designing-for-ios.md](references/designing-for-ios.md) | iOS | 触控、标签栏、导航栈、手势、屏幕尺寸、安全区域 |
| [designing-for-ipados.md](references/designing-for-ipados.md) | iPadOS | 多任务、侧边栏、指针、键盘、Apple Pencil、台前调度 |
| [designing-for-macos.md](references/designing-for-macos.md) | macOS | 菜单栏、工具栏、窗口管理、键盘快捷键、密集布局、Dock |
| [designing-for-tvos.md](references/designing-for-tvos.md) | tvOS | 焦点引擎、Siri Remote、后仰体验、内容优先、视差 |
| [designing-for-visionos.md](references/designing-for-visionos.md) | visionOS | 空间计算、窗口/体积/空间、眼动追踪、手势、深度 |
| [designing-for-watchos.md](references/designing-for-watchos.md) | watchOS | 一瞥即得的 UI、数码表冠、复杂功能、通知、触觉 |
| [designing-for-games.md](references/designing-for-games.md) | 游戏 | 控制器、沉浸式体验、平台特定规范、无障碍 |

## 决策框架

1. **确定主要使用场景。** 移动中（iOS/watchOS）、桌前（macOS）、沙发上（tvOS）、空间环境（visionOS）？

2. **匹配输入与交互。** 触控用于直接操作、指针用于精确、凝视+手势用于空间、数码表冠用于快速滚动、遥控用于焦点导航。

3. **适配而非复制。** macOS 侧边栏在 iPhone 上变成标签栏。visionOS 体积在 watchOS 上没有等效物。转换意图，而非实现。

4. **利用平台优势。** iOS 上的实时活动、macOS 上的桌面小组件、watchOS 上的复杂功能、visionOS 上的沉浸式空间。

5. **保持品牌一致性**，同时尊重每个平台的视觉语言和交互模式。

## 输出格式

1. **平台特定建议**，引用相关 HIG 章节。
2. **平台差异表**，比较导航、输入、布局和规范。
3. **每个平台的实现说明**，包括推荐 API 和适配策略。

## 需要询问的问题

1. 您的目标平台有哪些？
2. 新应用还是适配现有应用？如果是现有应用，基础平台是哪个？
3. SwiftUI 还是 UIKit/AppKit？
4. 需要支持旧版操作系统吗？
5. 主要使用场景？（移动中、桌前、沙发上、空间、一瞥即得？）

## 相关技能

- **hig-foundations** — 跨平台的共享原则（颜色、排版、无障碍、布局）
- **hig-patterns** — 在不同平台上表现不同的交互模式
- **hig-components-layout** — 因平台而异的导航结构（标签栏、侧边栏、分屏视图）
- **hig-components-content** — 跨平台适配的内容展示

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
