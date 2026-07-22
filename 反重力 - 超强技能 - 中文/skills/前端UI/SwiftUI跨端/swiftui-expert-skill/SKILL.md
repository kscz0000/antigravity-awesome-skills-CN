---
name: swiftui-expert-skill
description: 编写、审查或改进 SwiftUI 代码，遵循状态管理、视图组合、性能和 iOS 26+ Liquid Glass 采用的最佳实践。触发词：SwiftUI开发、SwiftUI代码审查、SwiftUI重构、状态管理、视图组合、Liquid Glass、SwiftUI最佳实践、SwiftUI模式、iOS开发、SwiftUI功能开发
risk: unknown
source: community
---

# SwiftUI 专家技能

## 何时使用
- 你正在构建、审查或重构 SwiftUI 代码，需要当前的最佳实践。
- 任务涉及状态管理、视图组合、性能、无障碍或 iOS 26+ Liquid Glass 采用。
- 你需要基于事实的 SwiftUI 指导层，而不锁定到特定的应用架构。

## 概述
使用此技能来构建、审查或改进 SwiftUI 功能，确保正确的状态管理、最优的视图组合和 iOS 26+ Liquid Glass 样式。优先使用原生 API、Apple 设计指导和性能意识模式。本技能聚焦于事实和最佳实践，不强制执行特定的架构模式。

## 工作流决策树

### 1) 审查现有 SwiftUI 代码
- **首先，查阅 `references/latest-apis.md`** 确保仅使用当前未废弃的 API
- 根据选择指南检查属性包装器的使用（参见 `references/state-management.md`）
- 验证视图组合遵循提取规则（参见 `references/view-structure.md`）
- 检查是否应用了性能模式（参见 `references/performance-patterns.md`）
- 验证列表模式使用稳定标识（参见 `references/list-patterns.md`）
- 检查动画模式的正确性（参见 `references/animation-basics.md`、`references/animation-transitions.md`）
- 审查无障碍：正确的分组、特征、Dynamic Type 支持（参见 `references/accessibility-patterns.md`）
- 检查 Liquid Glass 使用的正确性和一致性（参见 `references/liquid-glass.md`）
- 验证 iOS 26+ 可用性处理是否提供了合理的回退方案

### 2) 改进现有 SwiftUI 代码
- **首先，查阅 `references/latest-apis.md`** 将任何废弃 API 替换为现代等效项
- 审计状态管理的包装器选择是否正确（参见 `references/state-management.md`）
- 将复杂视图提取为独立的子视图（参见 `references/view-structure.md`）
- 重构热路径以最小化冗余状态更新（参见 `references/performance-patterns.md`）
- 确保 ForEach 使用稳定标识（参见 `references/list-patterns.md`）
- 改进动画模式（使用 value 参数、正确的过渡，参见 `references/animation-basics.md`、`references/animation-transitions.md`）
- 改进无障碍：使用 `Button` 替代点击手势，为 Dynamic Type 添加 `@ScaledMetric`（参见 `references/accessibility-patterns.md`）
- 当使用 `UIImage(data:)` 时建议图像降采样（作为可选优化，参见 `references/image-optimization.md`）
- 仅在用户明确要求时采用 Liquid Glass

### 3) 实现新 SwiftUI 功能
- **首先，查阅 `references/latest-apis.md`** 仅使用目标部署版本的当前未废弃 API
- 先设计数据流：识别自有状态与注入状态（参见 `references/state-management.md`）
- 为最优差异比较构建视图结构（尽早提取子视图，参见 `references/view-structure.md`）
- 将业务逻辑保留在服务和模型中以保持可测试性（参见 `references/layout-best-practices.md`）
- 使用正确的动画模式（隐式 vs 显式、过渡，参见 `references/animation-basics.md`、`references/animation-transitions.md`、`references/animation-advanced.md`）
- 对可点击元素使用 `Button`，添加无障碍分组和标签（参见 `references/accessibility-patterns.md`）
- 在布局/外观修饰符之后应用玻璃效果（参见 `references/liquid-glass.md`）
- 使用 `#available` 为 iOS 26+ 功能设置门槛并提供回退方案

## 核心指南

### 状态管理
- `@State` 必须为 `private`；用于视图内部状态
- `@Binding` 仅当子视图需要**修改**父视图状态时使用
- `@StateObject` 当视图**创建**对象时使用；`@ObservedObject` 当对象被**注入**时使用
- iOS 17+：`@State` 配合 `@Observable` 类使用；`@Bindable` 用于需要绑定的注入可观察对象
- 使用 `let` 处理只读值；`var` + `.onChange()` 处理响应式读取
- 永远不要向 `@State` 或 `@StateObject` 传入值——它们只接受初始值
- 嵌套的 `ObservableObject` 不会传播变更——直接传递嵌套对象；`@Observable` 可以正常处理嵌套

### 视图组合
- 将复杂视图提取为独立的子视图，以提高可读性和性能
- 状态变更时优先使用修饰符而非条件视图（维持视图标识）
- 保持视图 `body` 简洁纯净（无副作用或复杂逻辑）
- `@ViewBuilder` 函数仅用于小型简单部分
- 优先使用 `@ViewBuilder let content: Content` 而非基于闭包的内容属性
- 将业务逻辑保留在服务和模型中；视图应编排 UI 流程
- 操作处理应引用方法，而非包含内联逻辑
- 视图应在任何上下文中工作（不要假设屏幕尺寸或呈现方式）

### 性能
- 仅向视图传递所需值（避免大型"config"或"context"对象）
- 消除不必要的依赖以减少更新扇出
- 在热路径中赋值状态前检查值是否已变更
- 避免在 `onReceive`、`onChange`、滚动处理程序中进行冗余状态更新
- 最小化频繁执行代码路径中的工作量
- 大型列表使用 `LazyVStack`/`LazyHStack`
- 为 `ForEach` 使用稳定标识（动态内容绝不使用 `.indices`）
- 确保每个 `ForEach` 元素的视图数量恒定
- 避免在 `ForEach` 中内联过滤（预过滤并缓存）
- 避免在列表行中使用 `AnyView`
- 考虑使用 POD 视图实现快速差异比较（或将昂贵视图包装在 POD 父视图中）
- 当遇到 `UIImage(data:)` 时建议图像降采样（作为可选优化）
- 避免布局抖动（深层层级、过多的 `GeometryReader`）
- 按阈值限制频繁的几何更新
- 使用 `Self._logChanges()` 或 `Self._printChanges()` 调试意外的视图更新

### 动画
- 使用带 value 参数的 `.animation(_:value:)`（不带 value 的已废弃版本范围过广）
- 事件驱动动画使用 `withAnimation`（按钮点击、手势）
- 动画性能优先使用变换（`offset`、`scale`、`rotation`）而非布局变更（`frame`）
- 过渡需要在条件结构外部配合动画
- 自定义 `Animatable` 实现必须有显式的 `animatableData`
- 多步序列使用 `.phaseAnimator`（iOS 17+）
- 精确时序控制使用 `.keyframeAnimator`（iOS 17+）
- 动画完成处理程序需要 `.transaction(value:)` 以支持重新执行
- 隐式动画覆盖显式动画（视图树中后出现的优先）

### 无障碍
- 可点击元素优先使用 `Button` 而非 `onTapGesture`（免费获得 VoiceOver 支持）
- 使用 `@ScaledMetric` 处理应随 Dynamic Type 缩放的自定义数值
- 使用 `accessibilityElement(children: .combine)` 分组相关元素以合并标签
- 当默认标签不清晰或缺失时提供 `accessibilityLabel`
- 对应表现为原生控件的自定义控件使用 `accessibilityRepresentation`

### Liquid Glass（iOS 26+）
**仅在用户明确要求时采用。**
- 使用原生 `glassEffect`、`GlassEffectContainer` 和玻璃按钮样式
- 将多个玻璃元素包装在 `GlassEffectContainer` 中
- 在布局和视觉修饰符之后应用 `.glassEffect()`
- `.interactive()` 仅用于可点击/可聚焦元素
- 使用 `glassEffectID` 配合 `@Namespace` 实现变形过渡

## 快速参考

### 属性包装器选择
| 包装器 | 使用场景 |
|--------|----------|
| `@State` | 视图内部状态（必须为 `private`） |
| `@Binding` | 子视图修改父视图的状态 |
| `@StateObject` | 视图拥有一个 `ObservableObject` |
| `@ObservedObject` | 视图接收一个 `ObservableObject` |
| `@Bindable` | iOS 17+：需要绑定的注入 `@Observable` |
| `let` | 来自父视图的只读值 |
| `var` | 通过 `.onChange()` 监听的只读值 |

### Liquid Glass 模式
```swift
// Basic glass effect with fallback
if #available(iOS 26, *) {
    content
        .padding()
        .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))
} else {
    content
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}

// Grouped glass elements
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        GlassButton1()
        GlassButton2()
    }
}

// Glass buttons
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```

## 审查清单

### 最新 API（参见 `references/latest-apis.md`）
- [ ] 未使用废弃修饰符（对照快速查找表检查）
- [ ] API 选择与项目的最低部署目标匹配

### 状态管理
- [ ] `@State` 属性为 `private`
- [ ] `@Binding` 仅在子视图修改父视图状态处使用
- [ ] `@StateObject` 用于自有对象，`@ObservedObject` 用于注入对象
- [ ] iOS 17+：`@State` 配合 `@Observable`，`@Bindable` 用于注入
- [ ] 传入的值未声明为 `@State` 或 `@StateObject`
- [ ] 避免嵌套 `ObservableObject`（或直接传递给子视图）

### Sheet 与导航（参见 `references/sheet-navigation-patterns.md`）
- [ ] 使用 `.sheet(item:)` 处理基于模型的 sheet
- [ ] Sheet 拥有自己的操作并在内部关闭

### ScrollView（参见 `references/scroll-patterns.md`）
- [ ] 使用 `ScrollViewReader` 配合稳定 ID 实现编程式滚动

### 视图结构（参见 `references/view-structure.md`）
- [ ] 状态变更使用修饰符而非条件判断
- [ ] 复杂视图已提取为独立子视图
- [ ] 容器视图使用 `@ViewBuilder let content: Content`

### 性能（参见 `references/performance-patterns.md`）
- [ ] 视图 `body` 保持简洁纯净（无副作用）
- [ ] 仅传递所需值（非大型配置对象）
- [ ] 消除不必要的依赖
- [ ] 状态更新在赋值前检查值是否已变更
- [ ] 热路径最小化状态更新
- [ ] `body` 中无对象创建
- [ ] 重计算已移出 `body`

### 列表模式（参见 `references/list-patterns.md`）
- [ ] ForEach 使用稳定标识（非 `.indices`）
- [ ] 每个 ForEach 元素的视图数量恒定
- [ ] ForEach 中无内联过滤
- [ ] 列表行中无 `AnyView`

### 布局（参见 `references/layout-best-practices.md`）
- [ ] 避免布局抖动（深层层级、过多的 GeometryReader）
- [ ] 按阈值限制频繁的几何更新
- [ ] 业务逻辑保留在服务和模型中（而非视图中）
- [ ] 操作处理引用方法（非内联逻辑）
- [ ] 使用相对布局（非硬编码常量）
- [ ] 视图在任何上下文中工作（上下文无关）

### 动画（参见 `references/animation-basics.md`、`references/animation-transitions.md`、`references/animation-advanced.md`）
- [ ] 使用带 value 参数的 `.animation(_:value:)`
- [ ] 事件驱动动画使用 `withAnimation`
- [ ] 过渡与动画在条件结构外部配对
- [ ] 自定义 `Animatable` 有显式的 `animatableData` 实现
- [ ] 动画性能优先使用变换而非布局变更
- [ ] 多步序列使用阶段动画（iOS 17+）
- [ ] 精确时序使用关键帧动画（iOS 17+）
- [ ] 完成处理程序使用 `.transaction(value:)` 以支持重新执行

### 无障碍（参见 `references/accessibility-patterns.md`）
- [ ] 可点击元素使用 `Button` 而非 `onTapGesture`
- [ ] 应随 Dynamic Type 缩放的自定义值使用 `@ScaledMetric`
- [ ] 相关元素使用 `accessibilityElement(children:)` 分组
- [ ] 自定义控件在适当时使用 `accessibilityRepresentation`

### Liquid Glass（iOS 26+）
- [ ] Liquid Glass 使用 `#available(iOS 26, *)` 并提供回退方案
- [ ] 多个玻璃视图包装在 `GlassEffectContainer` 中
- [ ] `.glassEffect()` 在布局/外观修饰符之后应用
- [ ] `.interactive()` 仅用于用户可交互元素
- [ ] 相关元素的形状和色调保持一致

## 参考文献
- `references/latest-apis.md` - **所有工作流的必读材料。** 按版本分段的废弃到现代 API 过渡指南（iOS 15+ 至 iOS 26+）
- `references/state-management.md` - 属性包装器和数据流
- `references/view-structure.md` - 视图组合、提取和容器模式
- `references/performance-patterns.md` - 性能优化技术和反模式
- `references/list-patterns.md` - ForEach 标识、稳定性和列表最佳实践
- `references/layout-best-practices.md` - 布局模式、上下文无关视图和可测试性
- `references/accessibility-patterns.md` - 无障碍特征、分组、Dynamic Type 和 VoiceOver
- `references/animation-basics.md` - 核心动画概念、隐式/显式动画、时序、性能
- `references/animation-transitions.md` - 过渡、自定义过渡、Animatable 协议
- `references/animation-advanced.md` - 事务、阶段/关键帧动画（iOS 17+）、完成处理程序（iOS 17+）
- `references/sheet-navigation-patterns.md` - Sheet 呈现和导航模式
- `references/scroll-patterns.md` - ScrollView 模式和编程式滚动
- `references/image-optimization.md` - AsyncImage、图像降采样和优化
- `references/liquid-glass.md` - iOS 26+ Liquid Glass API

## 理念

本技能聚焦于**事实和最佳实践**，而非架构观点：
- 我们不强制执行特定架构（如 MVVM、VIPER）
- 我们鼓励为可测试性分离业务逻辑
- 我们优化性能和可维护性
- 我们遵循 Apple 的人机界面指南和 API 设计模式

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
