---
name: hig-components-system
description: 'Apple HIG 系统体验组件指南：小组件、实时活动、通知、复杂功能、主屏幕快捷操作、顶部货架、表盘、App Clip 和应用快捷方式。'
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 系统体验

提问前请检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未覆盖的信息。

## 核心原则

### 通用原则

1. **一瞥即得，即时价值。** 系统体验将应用最重要的内容呈现在用户无需启动应用即可看到的界面上。为秒级注意力设计。

2. **尊重平台上下文。** 锁屏小组件与主屏幕小组件有不同的约束。复杂功能远小于顶部货架项目。

### 小组件

3. **展示相关信息，而非全部内容。** 显示最有用的子集，适时更新。

4. **支持多种尺寸，各有独立布局。** 每种尺寸都应是精心设计的，而非另一种尺寸的缩放版本。

5. **点击深层链接。** 将用户带到相关内容，而非应用根屏幕。

### 实时活动

6. **追踪有明确起止时间的事件。** 配送、比分、计时器、行程。同时为灵动岛和锁屏设计。

7. **保持更新和及时。** 过时数据会削弱信任。事件结束后及时终止。

### 通知

8. **尊重用户注意力。** 仅发送用户真正关心的信息通知。禁止促销或低价值通知。

9. **可操作且自包含。** 包含足够的上下文以便理解和操作，无需打开应用。支持通知操作。使用线程和分组。

### 复杂功能

10. **表盘上的聚焦数据。** 为最小可用表示形式设计。支持多种家族。明智预算更新。

### 主屏幕快捷操作

11. **3-4 个最常见任务。** 简短标题，可选副标题，相关 SF Symbol 图标。

### 顶部货架

12. **tvOS 展示窗口。** 展示吸引人的内容：新剧集、精选项目、最近内容。

### App Clip

13. **即时、聚焦的功能，严格的大小预算。** 无需 App Store 下载即可快速加载。仅包含即时任务所需内容，然后提供完整应用安装。

### 应用快捷方式

14. **向 Siri 和 Spotlight 展示关键操作。** 为频繁任务定义快捷方式。使用自然、对话式的触发短语。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [widgets.md](references/widgets.md) | 小组件 | 一瞥即得的信息、尺寸、深层链接、时间线 |
| [live-activities.md](references/live-activities.md) | 实时活动 | 实时追踪、灵动岛、锁屏 |
| [notifications.md](references/notifications.md) | 通知 | 注意力、操作、分组、内容 |
| [complications.md](references/complications.md) | 复杂功能 | 表盘数据、家族、预算更新 |
| [home-screen-quick-actions.md](references/home-screen-quick-actions.md) | 快捷操作 | 触感触控、常见任务、SF Symbols |
| [top-shelf.md](references/top-shelf.md) | 顶部货架 | 精选内容、展示 |
| [app-clips.md](references/app-clips.md) | App Clip | 即时使用、轻量、聚焦任务、NFC/二维码 |
| [watch-faces.md](references/watch-faces.md) | 表盘 | 自定义复杂功能、表盘共享 |
| [app-shortcuts.md](references/app-shortcuts.md) | 应用快捷方式 | Siri、Spotlight、语音触发 |

## 输出格式

1. **系统体验推荐** — 哪种界面最适合该用例。
2. **内容策略** — 显示什么、优先级、省略什么。
3. **更新频率** — 刷新率，包括系统预算约束。
4. **尺寸/家族变体** — 支持哪些以及布局如何适配。
5. **深层链接行为** — 点击后带用户去哪里。

## 需要询问的问题

1. 哪些信息需要在应用外展示？
2. 哪个平台？
3. 数据更新频率如何？
4. 主要的一瞥即得需求是什么？

## 相关技能

- **hig-components-status** — 小组件或实时活动中的进度指示器
- **hig-inputs** — 系统体验的交互模式（复杂功能的数码表冠）
- **hig-technologies** — 应用快捷方式的 Siri、复杂功能的 HealthKit、App Clip 的 NFC

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
