---
name: swiftui-performance-audit
description: 基于代码审查和性能分析证据，审计 SwiftUI 性能问题。触发词：SwiftUI性能、性能审计、渲染卡顿、滚动掉帧、CPU占用高、内存增长、视图更新过多、布局抖动、SwiftUI Instruments
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# SwiftUI 性能审计

## 快速开始

使用此技能从代码入手诊断 SwiftUI 性能问题，当代码审查无法解释症状时，再请求性能分析证据。

## 使用场景
- 用户报告 SwiftUI 中渲染缓慢、滚动卡顿、布局抖动或 CPU 占用过高。
- 需要以代码审查为主，辅以 Instruments 指导来获取性能分析证据。

## 工作流程

1. 分类症状：渲染缓慢、滚动卡顿、CPU 占用高、内存增长、卡顿或视图更新过多。
2. 如有代码，使用 `references/code-smells.md` 进行代码优先审查。
3. 如无代码，请求最小有效切片：目标视图、数据流、复现步骤和部署目标。
4. 如代码审查无法定论或需要运行时证据，使用 `references/profiling-intake.md` 引导用户进行性能分析。
5. 使用 `references/report-template.md` 总结可能的原因、证据、修复方案和验证步骤。

## 1. 信息收集

收集：
- 目标视图或功能代码。
- 症状和精确的复现步骤。
- 数据流：`@State`、`@Binding`、环境依赖和 Observable 模型。
- 问题出现在真机还是模拟器，以及是在 Debug 还是 Release 模式下观察到的。

尽可能请用户分类问题：
- CPU 飙升或电量消耗快
- 滚动卡顿或掉帧
- 内存占用高或图片压力大
- 卡顿或交互无响应
- 视图更新过多或更新范围意外过广

完整的性能分析收集清单，请阅读 `references/profiling-intake.md`。

## 2. 代码优先审查

重点关注：
- 观察范围过广或环境读取导致的失效风暴。
- 列表和 `ForEach` 中不稳定的身份标识。
- `body` 或视图构建器中的重计算工作。
- 复杂层级、`GeometryReader` 或偏好链导致的布局抖动。
- 主线程上的大图解码或缩放工作。
- 动画或过渡效果的应用范围过广。

使用 `references/code-smells.md` 获取详细的代码异味目录和修复指南。

提供：
- 附带代码引用的可能根因。
- 建议的修复和重构方案。
- 如需要，提供最小复现或埋点建议。

## 3. 引导用户进行性能分析

如果代码审查无法解释问题，请求运行时证据：
- SwiftUI 时间线和 Time Profiler 调用树的 trace 导出或截图。
- 设备/系统/构建配置。
- 被分析的确切交互操作。
- 如用户在对比变更，提供变更前后的指标。

使用 `references/profiling-intake.md` 获取精确的清单和收集步骤。

## 4. 分析与诊断

- 将证据映射到最可能的类别：失效、身份抖动、布局抖动、主线程工作、图片开销或动画开销。
- 按影响程度而非解释难度排列问题优先级。
- 区分代码层面的怀疑和有 trace 支撑的证据。
- 明确指出性能分析仍不充分的地方，以及哪些额外证据可以降低不确定性。

## 5. 修复

实施针对性修复：
- 缩小状态作用域，减少观察扇出。
- 稳定 `ForEach` 和列表的身份标识。
- 将重计算工作从 `body` 移至基于输入更新的派生状态、模型层预计算、记忆化辅助函数或后台预处理。`@State` 仅用于视图自有状态，不要作为任意计算的临时缓存。
- 仅在相等性判断比重计算子树更便宜且输入确实具有值语义时，才使用 `equatable()`。
- 在渲染前对图片进行降采样。
- 降低布局复杂度，尽可能使用固定尺寸。

使用 `references/code-smells.md` 获取示例、Observation 相关的扇出指导和修复模式。

## 6. 验证

请用户重新运行相同的采集，并与基线指标对比。
如有数据，总结差异（CPU、掉帧、内存峰值）。

## 输出

提供：
- 简要指标表（如有数据则含变更前后对比）。
- 按影响排序的首要问题。
- 附带预估工作量的修复建议。

格式化最终审计报告时使用 `references/report-template.md`。

## 参考资料

- 性能分析收集清单：`references/profiling-intake.md`
- 常见代码异味和修复模式：`references/code-smells.md`
- 审计输出模板：`references/report-template.md`
- 用户提供 Apple 文档和 WWDC 资源时，添加至 `references/` 目录。
- 使用 Instruments 优化 SwiftUI 性能：`references/optimizing-swiftui-performance-instruments.md`
- 理解和改善 SwiftUI 性能：`references/understanding-improving-swiftui-performance.md`
- 理解应用中的卡顿：`references/understanding-hangs-in-your-app.md`
- 揭秘 SwiftUI 性能（WWDC23）：`references/demystify-swiftui-performance-wwdc23.md`

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出作为特定环境验证、测试或专家审查的替代品。
- 如缺少必要输入、权限、安全边界或成功标准，停止并请求澄清。
