---
name: swiftui-view-refactor
description: 将 SwiftUI 视图重构为更小的组件，保持稳定、明确的数据流。触发词：SwiftUI重构、视图拆分、组件化、数据流优化
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# SwiftUI 视图重构

## 概述
将 SwiftUI 视图重构为小型、明确、稳定的视图类型。默认采用原生 SwiftUI：视图内使用本地状态，共享依赖通过环境注入，业务逻辑放在服务/模型中，仅当需求或现有代码明确需要时才使用视图模型。

## 适用场景
- 清理大型 SwiftUI 视图或拆分冗长的 `body` 实现。
- 需要更小的子视图、明确的依赖注入或更好的 Observation 使用方式。

## 核心准则

### 1) 视图排列顺序（从上到下）
- 强制执行此顺序，除非现有文件有更强的本地约定需要保留。
- Environment
- `private`/`public` `let`
- `@State` / 其他存储属性
- 计算属性 `var`（非视图）
- `init`
- `body`
- 计算视图构建器 / 其他视图辅助方法
- 辅助函数 / 异步函数

### 2) 默认使用 MV，而非 MVVM
- 视图应是轻量级的状态表达和编排点，而非业务逻辑的容器。
- 优先使用 `@State`、`@Environment`、`@Query`、`.task`、`.task(id:)` 和 `onChange`，再考虑视图模型。
- 通过 `@Environment` 注入服务和共享模型；将领域逻辑保留在服务/模型中，而非视图 body。
- 不要仅为镜像本地视图状态或包装环境依赖而引入视图模型。
- 如果屏幕变大，先将 UI 拆分为子视图，再考虑新建视图模型层。

### 3) 强烈优先使用专用子视图类型，而非计算 `some View` 辅助方法
- 标记超过一屏或包含多个逻辑部分的 `body` 属性。
- 对于非简单部分，优先提取专用 `View` 类型，特别是当它们有状态、异步工作、分支逻辑或值得独立预览时。
- 计算 `some View` 辅助方法应稀少且简短。不要用 `private var header: some View` 风格的片段构建整个屏幕。
- 向提取的子视图传递小型、明确的输入（数据、绑定、回调），而非传递整个父视图状态。
- 如果提取的子视图变得可复用或具有独立意义，将其移至单独文件。

推荐：

```swift
var body: some View {
    List {
        HeaderSection(title: title, subtitle: subtitle)
        FilterSection(
            filterOptions: filterOptions,
            selectedFilter: $selectedFilter
        )
        ResultsSection(items: filteredItems)
        FooterSection()
    }
}

private struct HeaderSection: View {
    let title: String
    let subtitle: String

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title).font(.title2)
            Text(subtitle).font(.subheadline)
        }
    }
}

private struct FilterSection: View {
    let filterOptions: [FilterOption]
    @Binding var selectedFilter: FilterOption

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack {
                ForEach(filterOptions, id: \.self) { option in
                    FilterChip(option: option, isSelected: option == selectedFilter)
                        .onTapGesture { selectedFilter = option }
                }
            }
        }
    }
}
```

避免：

```swift
var body: some View {
    List {
        header
        filters
        results
        footer
    }
}

private var header: some View {
    VStack(alignment: .leading, spacing: 6) {
        Text(title).font(.title2)
        Text(subtitle).font(.subheadline)
    }
}
```

### 3b) 将操作和副作用提取到 `body` 外
- 不要在视图 body 中内联复杂的按钮操作。
- 不要将业务逻辑埋在 `.task`、`.onAppear`、`.onChange` 或 `.refreshable` 内。
- 优先从视图调用小型私有方法，将真正的业务逻辑移入服务/模型。
- body 应该读起来像 UI，而非视图控制器。

```swift
Button("Save", action: save)
    .disabled(isSaving)

.task(id: searchText) {
    await reload(for: searchText)
}

private func save() {
    Task { await saveAsync() }
}

private func reload(for searchText: String) async {
    guard !searchText.isEmpty else {
        results = []
        return
    }
    await searchService.search(searchText)
}
```

### 4) 保持稳定的视图树（避免顶层条件视图切换）
- 避免 `body` 或计算视图通过 `if/else` 返回完全不同的根分支。
- 优先使用单一稳定的基础视图，在各部分/修饰器内使用条件（`overlay`、`opacity`、`disabled`、`toolbar` 等）。
- 根级分支切换会导致身份混乱、更广泛的失效和额外的重新计算。

推荐：

```swift
var body: some View {
    List {
        documentsListContent
    }
    .toolbar {
        if canEdit {
            editToolbar
        }
    }
}
```

避免：

```swift
var documentsListView: some View {
    if canEdit {
        editableDocumentsList
    } else {
        readOnlyDocumentsList
    }
}
```

### 5) 视图模型处理（仅当已存在或明确请求时）
- 将视图模型视为遗留或显式需求模式，而非默认选择。
- 除非请求或现有代码明确需要，否则不要引入视图模型。
- 如果视图模型存在，尽可能使其非可选。
- 通过 `init` 向视图传递依赖，然后在视图的 `init` 中创建视图模型。
- 避免 `bootstrapIfNeeded` 模式和其他延迟初始化的变通方案。

示例（基于 Observation）：

```swift
@State private var viewModel: SomeViewModel

init(dependency: Dependency) {
    _viewModel = State(initialValue: SomeViewModel(dependency: dependency))
}
```

### 6) Observation 使用
- 对于 iOS 17+ 的 `@Observable` 引用类型，在拥有视图中将其存储为 `@State`。
- 显式向下传递可观察对象；除非 UI 真正需要，否则避免可选状态。
- 如果部署目标包含 iOS 16 或更早版本，在拥有者处使用 `@StateObject`，注入遗留可观察模型时使用 `@ObservedObject`。

## 工作流程

1. 重新排列视图以匹配排列规则。
2. 从 `body` 中移除内联操作和副作用；将业务逻辑移入服务/模型，视图中仅保留薄编排层。
3. 通过提取专用子视图类型来缩短冗长的 body；避免用多个计算 `some View` 辅助方法重建屏幕。
4. 确保稳定的视图结构：避免基于 `if` 的顶层分支切换；将条件移至局部部分/修饰器。
5. 如果视图模型存在或被明确要求，将可选视图模型替换为在 `init` 中初始化的非可选 `@State` 视图模型。
6. 确认 Observation 使用：iOS 17+ 根 `@Observable` 模型使用 `@State`，仅当部署目标需要时才使用遗留包装器。
7. 保持行为完整：除非被要求，否则不要更改布局或业务逻辑。

## 备注

- 优先使用小型、明确的视图类型，而非大型条件块和大型计算 `some View` 属性。
- 将计算视图构建器放在 `body` 下方，非视图计算变量放在 `init` 上方。
- 好的 SwiftUI 重构应使视图从上到下读起来是数据流加布局，而非混合布局和命令式逻辑。
- 有关 MV 优先的指导和原理，请参阅 `references/mv-patterns.md`。

## 大型视图处理

当 SwiftUI 视图文件超过约 300 行时，应积极拆分。将有意义的部分提取为专用 `View` 类型，而非将复杂性隐藏在多个计算属性中。使用带 `// MARK: -` 注释的 `private` 扩展来组织操作和辅助方法，但不要将扩展作为将大屏幕拆分为更小视图类型的替代方案。如果提取的子视图被复用或具有独立意义，将其移至单独文件。

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。