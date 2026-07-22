# MV 模式参考

关于判断 SwiftUI 功能应保持纯 MV 还是引入视图模型的精炼指导。

受用户提供的资料"SwiftUI in 2025: Forget MVVM"（Thomas Ricouard）启发，在此重写为实用的重构参考。

## 默认立场

- 默认采用 MV：视图是轻量级的状态表达和编排点。
- 优先使用 `@State`、`@Environment`、`@Query`、`.task`、`.task(id:)` 和 `onChange`，再考虑视图模型。
- 将业务逻辑保留在服务、模型或领域类型中，而非视图 body。
- 在引入视图模型层之前，先将大屏幕拆分为更小的视图类型。
- 避免手动获取或重复 SwiftUI/SwiftData 机制的状态管道。
- 先测试服务、模型和转换；视图应保持简单和声明式。

## 何时避免使用视图模型

当视图模型主要做以下事情时，不要引入：
- 镜像本地视图状态，
- 包装通过 `@Environment` 已可用的值，
- 重复 `@Query`、`@State` 或基于 `Binding` 的数据流，
- 仅因为视图 body 太长而存在，
- 持有可放在 `.task` 加本地视图状态中的一次性异步加载逻辑。

在这些情况下，简化视图和数据流，而非增加间接层。

## 何时视图模型可能合理

当至少满足以下条件之一时，视图模型是合理的：
- 用户明确要求使用，
- 代码库已为该功能标准化视图模型模式，
- 屏幕需要长生命周期的引用模型，其行为不适合仅放在服务中，
- 功能正在适配非 SwiftUI API，需要专用的桥接对象，
- 多个视图共享相同的展示特定状态，且该状态不适合作为应用级环境数据建模。

即便如此，尽可能保持视图模型小型、明确且非可选。

## 推荐模式：本地状态加环境

```swift
struct FeedView: View {
    @Environment(BlueSkyClient.self) private var client

    enum ViewState {
        case loading
        case error(String)
        case loaded([Post])
    }

    @State private var viewState: ViewState = .loading

    var body: some View {
        List {
            switch viewState {
            case .loading:
                ProgressView("Loading feed...")
            case .error(let message):
                ErrorStateView(message: message, retryAction: { await loadFeed() })
            case .loaded(let posts):
                ForEach(posts) { post in
                    PostRowView(post: post)
                }
            }
        }
        .task { await loadFeed() }
    }

    private func loadFeed() async {
        do {
            let posts = try await client.getFeed()
            viewState = .loaded(posts)
        } catch {
            viewState = .error(error.localizedDescription)
        }
    }
}
```

推荐原因：
- 状态靠近渲染它的 UI，
- 依赖来自环境而非包装对象，
- 视图协调 UI 流程，服务负责真正的工作。

## 推荐模式：使用修饰器作为轻量编排

```swift
.task(id: searchText) {
    guard !searchText.isEmpty else {
        results = []
        return
    }
    await searchFeed(query: searchText)
}

.onChange(of: isInSearch, initial: false) {
    guard !isInSearch else { return }
    Task { await fetchSuggestedFeed() }
}
```

使用视图生命周期修饰器进行简单的本地编排。除非行为明显超出视图范围，否则默认不要将这些转换为视图模型。

## SwiftData 说明

SwiftData 有力支持在可能时将数据流保留在视图内。

推荐：

```swift
struct BookListView: View {
    @Query private var books: [Book]
    @Environment(\.modelContext) private var modelContext

    var body: some View {
        List {
            ForEach(books) { book in
                BookRowView(book: book)
                    .swipeActions {
                        Button("Delete", role: .destructive) {
                            modelContext.delete(book)
                        }
                    }
            }
        }
    }
}
```

除非功能有明确理由，否则不要添加手动获取和镜像相同状态的视图模型。

## 测试指导

优先测试：
- 服务和业务规则，
- 模型和状态转换，
- 服务层的异步工作流，
- 使用预览或更高级别 UI 测试的 UI 行为。

不要主要为了让简单 SwiftUI 视图"可测试"而引入视图模型。这通常只增加仪式感，而不改善架构。

## 重构清单

重构为 MV 时：
- 移除仅包装环境依赖或本地视图状态的视图模型。
- 当普通视图状态足够时，替换可选或延迟初始化的视图模型。
- 将业务逻辑从视图 body 提取到服务/模型中。
- 保持视图作为 UI 状态、导航和用户操作的薄协调器。
- 在添加新的间接层之前，先将大型 body 拆分为更小的视图类型。

## 结论

将视图模型视为例外，而非默认。

在现代 SwiftUI 中，默认技术栈是：
- `@State` 用于本地状态，
- `@Environment` 用于共享依赖，
- `@Query` 用于 SwiftData 支持的集合，
- 生命周期修饰器用于轻量编排，
- 服务和模型用于业务逻辑。

仅当功能明确需要时才使用视图模型。