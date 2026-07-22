# 理解和改善 SwiftUI 性能（摘要）

背景：Apple 指南，介绍如何使用 Instruments 诊断 SwiftUI 性能问题，以及应用设计模式减少过长或过频的更新。

## 核心概念

- SwiftUI 是声明式的；视图更新由状态、环境和 Observable 数据依赖驱动。
- 视图 body 必须快速计算以满足帧截止时间；过慢或过频的更新会导致卡顿。
- Instruments 是发现长时间运行更新和过高更新频率的主要工具。

## Instruments 工作流程

1. 通过 Product > Profile 进行性能分析。
2. 选择 SwiftUI 模板并录制。
3. 执行目标交互。
4. 停止录制，检查 SwiftUI 轨道和 Time Profiler。

## SwiftUI 时间线通道

- Update Groups：SwiftUI 花在计算更新上的时间概览。
- Long View Body Updates：橙色 >500us，红色 >1000us。
- Long Platform View Updates：SwiftUI 中的 App/UIKit 宿主视图。
- Other Long Updates：几何/文本/布局及其他 SwiftUI 工作。
- Hitches：UI 未及时就绪的帧丢失。

## 诊断长视图 body 更新

- 展开 SwiftUI 轨道；检查模块特定的子轨道。
- 设置检查范围并与 Time Profiler 关联。
- 使用调用树或火焰图识别昂贵的帧。
- 重复更新以收集足够的样本用于分析。
- 过滤到特定更新（Show Calls Made by `MySwiftUIView.body`）。

## 诊断频繁更新

- 使用 Update Groups 找到没有长更新的长活跃组。
- 在组上设置检查范围，分析更新次数。
- 使用因果图（"Show Causes"）查看触发更新的原因。
- 将原因与预期数据流对比；优先处理最高频的原因。

## 修复模式

- 将昂贵工作移出 `body` 并缓存结果。
- 使用 `Observable()` 宏将依赖限定到实际读取的属性。
- 避免将更新扇出到多个视图的广泛依赖。
- 减少布局抖动；将依赖状态的子树与布局读取器隔离。
- 避免存储捕获父状态的闭包；预计算子视图。
- 通过阈值限制频繁更新（如几何数据变化）。

## 验证

- 变更后重新录制，确认更新次数减少、卡顿减少。
