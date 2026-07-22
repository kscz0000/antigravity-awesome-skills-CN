---
name: hig-inputs
description: "在提问前检查 .claude/apple-design-context.md。使用现有上下文，仅询问尚未覆盖的信息。触发词：输入方式、手势、Apple Pencil、键盘快捷键、游戏控制器、指针、触控板、Digital Crown、眼动追踪、空间交互、焦点系统、遥控器、运动传感器、近距离交互、输入设计、多输入支持"
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 输入方式

在提问前检查 `.claude/apple-design-context.md`。使用现有上下文，仅询问尚未覆盖的信息。

## 核心原则

### 通用原则

1. **支持多种输入方式。** 触控、指针、键盘、Apple Pencil、语音、眼动、手势、控制器。针对每个平台可用的输入方式进行设计。在 iPadOS 上，同时支持触控和指针；在 macOS 上，同时支持指针和键盘。

2. **每个输入操作都提供一致的反馈。** 可见、可听或触觉响应。

### 手势

3. **标准手势必须行为一致。** 点击激活、滑动滚动/导航、捏合缩放、长按显示上下文菜单、拖动移动。不要覆盖系统手势（边缘滑动返回、主屏幕、通知）。

4. **使用标准识别器；保持自定义手势的可发现性。** Apple 内置识别器处理边界情况和无障碍功能。如果添加非标准手势，提供提示或引导教学。

### Apple Pencil

5. **精准绘图、标注和选择。** 支持压感、倾斜和悬停。适当时区分手指和 Pencil（手指平移，Pencil 绘图）。

6. **在文本字段中支持 Scribble。** 用户期望在任何文本输入中用 Pencil 书写。

### 键盘

7. **键盘快捷键和完整导航。** 标准快捷键（Cmd+C/V/Z）加自定义快捷键，在 iPadOS Command 键覆盖层中可见。逻辑 Tab 顺序。

8. **尊重软件键盘。** 键盘出现时调整布局。使用键盘避让 API。

### 游戏控制器

9. **MFi 控制器配合屏幕回退方案。** 映射到扩展游戏手柄配置文件，合理的默认值，可重映射。始终提供触控或键盘替代方案。

### 指针和触控板

10. **原生体验。** 悬停效果、指针形状自适应、标准光标行为。双指滚动、捏合缩放、滑动导航。

### Digital Crown

11. **watchOS 上的主要滚动和值调整输入方式。** 滚动列表、调整值、导航视图。在定位点提供触觉反馈。

### 眼动和空间输入（visionOS）

12. **注视并捏合。** 宽大的点击目标（眼动追踪精度低于触控）。避免持续凝视激活。沉浸式体验中的直接手势操作。

### 焦点系统

13. **对 tvOS 和 visionOS 至关重要。** 可预测的焦点移动。每个交互元素都可获得焦点。清晰的视觉指示器（缩放、高亮、提升）。逻辑焦点分组。

### 遥控器

14. **Siri Remote：有限的交互面。** 触控区域用于滑动、点击板用于选择、少量物理按钮。保持交互简单。

### 运动和近距离感应

15. **陀螺仪、加速度计、UWB：谨慎使用。** 适用于游戏、健身、AR。不用于核心任务。提供校准和重置。对于 UWB，用视觉或触觉提示传达距离和方向。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [gestures.md](references/gestures.md) | 触控手势 | 点击、滑动、捏合、长按、拖动、系统手势 |
| [apple-pencil-and-scribble.md](references/apple-pencil-and-scribble.md) | Apple Pencil | 精准度、压感、倾斜、悬停、手写 |
| [keyboards.md](references/keyboards.md) | 键盘 | 快捷键、导航、软件键盘、Command 键 |
| [game-controls.md](references/game-controls.md) | 游戏控制器 | MFi、扩展游戏手柄、重映射、回退方案 |
| [pointing-devices.md](references/pointing-devices.md) | 指针/触控板 | 悬停、光标变形、触控板手势 |
| [digital-crown.md](references/digital-crown.md) | Digital Crown | 滚动、值调整、触觉定位点 |
| [eyes.md](references/eyes.md) | 眼动追踪 | 注视并点击、凝视定位、点击目标尺寸 |
| [spatial-interactions.md](references/spatial-interactions.md) | 空间输入 | 手势、直接操作、沉浸式输入 |
| [focus-and-selection.md](references/focus-and-selection.md) | 焦点系统 | tvOS/visionOS 导航、焦点指示器、分组 |
| [remotes.md](references/remotes.md) | 遥控器 | 触控面、点击板、简单交互 |
| [gyro-and-accelerometer.md](references/gyro-and-accelerometer.md) | 运动传感器 | 陀螺仪、加速度计、校准、游戏 |
| [nearby-interactions.md](references/nearby-interactions.md) | 近距离交互 | U1 芯片、方向查找、近距离触发 |
| [camera-control.md](references/camera-control.md) | 相机控制 | iPhone 相机硬件按钮、快速启动 |

## 输出格式

1. **按平台推荐的输入方式**及其交互方式。
2. **手势规范表**——标准手势和自定义手势及其预期行为。
3. **键盘快捷键推荐**，遵循系统约定。
4. **无障碍输入替代方案**，用于 VoiceOver、Switch Control 等。

## 需要询问的问题

1. 哪些平台和输入设备？
2. 生产力应用还是休闲应用？
3. 设计中是否有自定义手势？
4. 是否需要游戏控制器支持？

## 相关技能

- **hig-components-status**——响应输入的进度指示器（下拉刷新）
- **hig-components-system**——具有独特输入约束的系统体验
- **hig-technologies**——VoiceOver、Siri 语音输入、ARKit 空间手势上下文

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
