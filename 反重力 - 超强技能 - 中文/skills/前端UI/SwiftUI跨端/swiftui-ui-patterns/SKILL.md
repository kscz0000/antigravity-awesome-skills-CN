---
name: swiftui-ui-patterns
description: 应用成熟的 SwiftUI UI 模式，涵盖导航、Sheet 弹窗、异步状态和可复用界面。触发词：SwiftUI、SwiftUI模式、SwiftUI导航、SwiftUI组件、SwiftUI状态管理、SwiftUI异步
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# SwiftUI UI 模式

## 快速开始

## 使用场景
- 创建或重构 SwiftUI 页面、流程或可复用 UI 组件时。
- 需要导航、Sheet 弹窗、异步状态、预览或组件模式的指导时。

根据目标选择路径：

### 已有项目

- 确定功能或页面及其主要交互模式（列表、详情、编辑器、设置、多标签）。
- 用 `rg "TabView\("` 或类似方式在仓库中找到相关示例，然后阅读最接近的 SwiftUI 视图。
- 遵循本地规范：优先使用 SwiftUI 原生状态，状态尽量保留在本地，共享依赖通过环境注入。
- 从 `references/components-index.md` 选择对应的组件参考并遵循其指导。
- 如果交互需要通过拖拽或滑动主内容来展示次级内容，在手动实现手势前先阅读 `references/scroll-reveal.md`。
- 用小型、聚焦的子视图和 SwiftUI 原生数据流构建界面。

### 新项目搭建

- 从 `references/app-wiring.md` 开始，连接 TabView + NavigationStack + sheets。
- 基于提供的骨架添加最小的 `AppTab` 和 `RouterPath`。
- 根据你首先需要的 UI 选择下一个组件参考（TabView、NavigationStack、Sheets）。
- 随着新页面的添加扩展路由和 sheet 枚举。

## 通用规则

- 使用现代 SwiftUI 状态管理（`@State`、`@Binding`、`@Observable`、`@Environment`），避免不必要的 ViewModel。
- 如果部署目标包含 iOS 16 或更早版本，无法使用 iOS 17 引入的 Observation API，则回退到 `ObservableObject`：根级持有用 `@StateObject`，注入观察用 `@ObservedObject`，仅对真正共享的应用级状态使用 `@EnvironmentObject`。
- 优先组合，保持视图小而聚焦。
- 使用 async/await 配合 `.task` 以及显式的加载/错误状态。关于重启、取消和防抖的指导，请阅读 `references/async-state.md`。
- 共享应用服务放在 `@Environment` 中，但功能局部的依赖和模型优先使用显式初始化注入。关于根级连接模式，请阅读 `references/app-wiring.md`。
- 优先使用与部署目标匹配的最新 SwiftUI API，当某个模式依赖特定版本时明确标注最低系统版本。
- 仅在编辑遗留文件时保留已有的遗留模式。
- 遵循项目的格式化和风格指南。
- **Sheets**：当状态代表选中的模型时，优先使用 `.sheet(item:)` 而非 `.sheet(isPresented:)`。避免在 sheet 内部使用 `if let`。Sheet 应拥有自己的操作，内部调用 `dismiss()` 而非层层传递 `onCancel`/`onConfirm` 闭包。
- **滚动驱动展示**：优先从滚动偏移量派生标准化的 progress 值，并以此单一数据源驱动视觉状态。避免并行手势状态机，除非仅靠滚动无法表达该交互。

## 状态所有权总结

使用与所有权模型匹配的最窄状态工具：

| 场景 | 推荐模式 |
| --- | --- |
| 单个视图拥有的本地 UI 状态 | `@State` |
| 子视图修改父视图拥有的值类型状态 | `@Binding` |
| iOS 17+ 根级持有的引用类型模型 | `@State` + `@Observable` 类型 |
| iOS 17+ 子视图读取或修改注入的 `@Observable` 模型 | 显式作为存储属性传递 |
| 共享应用服务或配置 | `@Environment(Type.self)` |
| iOS 16 及更早版本的遗留引用模型 | 根级 `@StateObject`，注入时用 `@ObservedObject` |

先选择所有权位置，再选择包装器。当普通值类型状态足够时，不要引入引用类型模型。

## 横切参考

- `references/navigationstack.md`：导航所有权、每标签页历史和枚举路由。
- `references/sheets.md`：集中式模态展示和枚举驱动的 Sheet。
- `references/deeplinks.md`：URL 处理和外部链接路由到应用目的地。
- `references/app-wiring.md`：根级依赖图、环境使用和应用壳连接。
- `references/async-state.md`：`.task`、`.task(id:)`、取消、防抖和异步 UI 状态。
- `references/previews.md`：`#Preview`、fixtures、mock 环境和隔离预览设置。
- `references/performance.md`：稳定标识、观察范围、惰性容器和渲染成本防护。

## 反模式

- 在一个文件中混合布局、业务逻辑、网络请求、路由和格式化的巨型视图。
- 用多个布尔标志处理互斥的 Sheet、Alert 或导航目的地。
- 在 `body` 驱动的代码路径中直接发起实时服务调用，而非使用视图生命周期钩子或注入的模型/服务。
- 用 `AnyView` 来绕过类型不匹配问题，而这些问题本应通过更好的组合来解决。
- 在没有明确所有权理由的情况下，将每个共享依赖默认设为 `@EnvironmentObject` 或全局路由器。

## 新建 SwiftUI 视图的工作流

1. 在编写 UI 代码之前，定义视图的状态、所有权位置和最低系统版本假设。
2. 识别哪些依赖应放在 `@Environment` 中，哪些应作为显式初始化参数。
3. 勾画视图层次、路由模型和展示点；将重复部分提取为子视图。对于复杂导航，阅读 `references/navigationstack.md`、`references/sheets.md` 或 `references/deeplinks.md`。**构建并验证无编译错误后再继续。**
4. 用 `.task` 或 `.task(id:)` 实现异步加载，需要时添加显式的加载和错误状态。当工作依赖于变化的输入或取消时，阅读 `references/async-state.md`。
5. 为主要和次要状态添加预览，当 UI 可交互时添加无障碍标签或标识符。当视图需要 fixtures 或注入 mock 依赖时，阅读 `references/previews.md`。
6. 通过构建验证：确认无编译错误、预览能正常渲染不崩溃、状态变更正确传播，并检查列表标识和观察范围不会导致不必要的重渲染。当页面内容多、滚动密集或频繁更新时，阅读 `references/performance.md`。对于常见的 SwiftUI 编译错误——缺少 `@State` 注解、模糊的 `ViewBuilder` 闭包或泛型类型不匹配——在更新调用方之前解决它们。**如果构建失败：** 仔细阅读错误信息，修复识别出的问题，然后重新构建再继续下一步。如果预览崩溃，隔离有问题的子视图，确认其状态初始化有效，然后重新运行预览再继续。

## 组件参考

使用 `references/components-index.md` 作为入口。每个组件参考应包含：
- 意图和最佳适用场景。
- 带本地规范的最小用法模式。
- 陷阱和性能注意事项。
- 当前仓库中现有示例的路径。

## 添加新的组件参考

- 创建 `references/<component>.md`。
- 保持简短且可操作；链接到当前仓库中的具体文件。
- 用新条目更新 `references/components-index.md`。

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
