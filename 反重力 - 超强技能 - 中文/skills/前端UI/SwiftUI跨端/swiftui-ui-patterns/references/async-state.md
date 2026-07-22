# 异步状态与任务生命周期

## 意图

当视图加载数据、响应变化的输入或协调应遵循 SwiftUI 视图生命周期的异步工作时，使用此模式。

## 核心规则

- 使用 `.task` 处理属于视图生命周期的加载时工作。
- 当异步工作应随输入变化（如查询、选择或标识符）而重启时，使用 `.task(id:)`。
- 将取消视为视图驱动任务的正常路径。在较长流程中检查 `Task.isCancelled`，避免将取消作为用户可见的错误。
- 对用户驱动的异步工作（如搜索）进行防抖或合并，避免重复请求。
- 面向 UI 的模型和变更保持 main-actor 安全，在服务中执行后台工作，然后将结果发布回 UI 状态。

## 示例：加载时执行

```swift
struct DetailView: View {
  let id: String
  @State private var state: LoadState<Item> = .idle
  @Environment(ItemClient.self) private var client

  var body: some View {
    content
      .task {
        await load()
      }
  }

  @ViewBuilder
  private var content: some View {
    switch state {
    case .idle, .loading:
      ProgressView()
    case .loaded(let item):
      ItemContent(item: item)
    case .failed(let error):
      ErrorView(error: error)
    }
  }

  private func load() async {
    state = .loading
    do {
      state = .loaded(try await client.fetch(id: id))
    } catch is CancellationError {
      return
    } catch {
      state = .failed(error)
    }
  }
}
```

## 示例：输入变化时重启

```swift
struct SearchView: View {
  @State private var query = ""
  @State private var results: [ResultItem] = []
  @Environment(SearchClient.self) private var client

  var body: some View {
    List(results) { item in
      Text(item.title)
    }
    .searchable(text: $query)
    .task(id: query) {
      try? await Task.sleep(for: .milliseconds(250))
      guard !Task.isCancelled, !query.isEmpty else {
        results = []
        return
      }
      do {
        results = try await client.search(query)
      } catch is CancellationError {
        return
      } catch {
        results = []
      }
    }
  }
}
```

## 何时将工作移出视图

- 如果异步流程跨越多个页面或必须在视图关闭后存活，将其移入服务或模型。
- 如果视图主要在协调应用级生命周期或账号变更，在 `app-wiring.md` 的应用壳层级连接。
- 如果重试、缓存或离线策略变得复杂，将策略放在客户端/服务中，让视图只做简单的状态转换。

## 陷阱

- 不要直接从 `body` 发起网络工作。
- 不要忽略搜索、输入建议或快速变化选择的取消。
- 避免在多个地方存储派生的异步状态，一个数据源就够了。
