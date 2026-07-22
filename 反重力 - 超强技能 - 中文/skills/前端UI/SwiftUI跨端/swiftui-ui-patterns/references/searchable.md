# 搜索栏

## 意图

使用 `searchable` 添加原生搜索 UI，支持可选的搜索范围和异步结果。

## 核心模式

- 将 `searchable(text:)` 绑定到本地状态。
- 使用 `.searchScopes` 支持多种搜索模式。
- 使用 `.task(id: searchQuery)` 或防抖任务避免过度请求。
- 结果加载时显示占位符或进度状态。

## 示例：带范围的搜索栏

```swift
@MainActor
struct ExploreView: View {
  @State private var searchQuery = ""
  @State private var searchScope: SearchScope = .all
  @State private var isSearching = false
  @State private var results: [SearchResult] = []

  var body: some View {
    List {
      if isSearching {
        ProgressView()
      } else {
        ForEach(results) { result in
          SearchRow(result: result)
        }
      }
    }
    .searchable(
      text: $searchQuery,
      placement: .navigationBarDrawer(displayMode: .always),
      prompt: Text("Search")
    )
    .searchScopes($searchScope) {
      ForEach(SearchScope.allCases, id: \.self) { scope in
        Text(scope.title)
      }
    }
    .task(id: searchQuery) {
      await runSearch()
    }
  }

  private func runSearch() async {
    guard !searchQuery.isEmpty else {
      results = []
      return
    }
    isSearching = true
    defer { isSearching = false }
    try? await Task.sleep(for: .milliseconds(250))
    results = await fetchResults(query: searchQuery, scope: searchScope)
  }
}
```

## 设计要点

- 搜索为空或无结果时显示占位符。
- 对输入进行防抖，避免频繁请求网络。
- 搜索状态保留在视图本地。

## 陷阱

- 避免对空字符串执行搜索。
- 不要在主线程上阻塞数据获取。
