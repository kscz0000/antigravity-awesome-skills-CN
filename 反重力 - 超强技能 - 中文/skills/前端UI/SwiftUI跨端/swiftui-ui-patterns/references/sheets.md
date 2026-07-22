# Sheet 弹窗

## 意图

使用集中式 Sheet 路由模式，让任何视图都能展示模态窗口而无需逐层传递属性。这使 Sheet 状态集中在一处，随应用增长而扩展。

## 核心架构

- 定义一个 `SheetDestination` 枚举，描述每个模态窗口并实现 `Identifiable`。
- 在路由器对象中存储当前 Sheet（`presentedSheet: SheetDestination?`）。
- 创建类似 `withSheetDestinations(...)` 的视图修饰符，将枚举映射到具体的 Sheet 视图。
- 将路由器注入环境，让子视图可以直接设置 `presentedSheet`。

## 示例：item 驱动的本地 Sheet

当 Sheet 状态仅限于单个页面且不需要集中路由时使用。

```swift
@State private var selectedItem: Item?

.sheet(item: $selectedItem) { item in
  EditItemSheet(item: item)
}
```

## 示例：SheetDestination 枚举

```swift
enum SheetDestination: Identifiable, Hashable {
  case composer
  case editProfile
  case settings
  case report(itemID: String)

  var id: String {
    switch self {
    case .composer, .editProfile:
      // Use the same id to ensure only one editor-like sheet is active at a time.
      return "editor"
    case .settings:
      return "settings"
    case .report:
      return "report"
    }
  }
}
```

## 示例：withSheetDestinations 修饰符

```swift
extension View {
  func withSheetDestinations(
    sheet: Binding<SheetDestination?>
  ) -> some View {
    sheet(item: sheet) { destination in
      Group {
        switch destination {
        case .composer:
          ComposerView()
        case .editProfile:
          EditProfileView()
        case .settings:
          SettingsView()
        case .report(let itemID):
          ReportView(itemID: itemID)
        }
      }
    }
  }
}
```

## 示例：从子视图发起展示

```swift
struct StatusRow: View {
  @Environment(RouterPath.self) private var router

  var body: some View {
    Button("Report") {
      router.presentedSheet = .report(itemID: "123")
    }
  }
}
```

## 必要的连接

要让子视图正常工作，父视图必须：
- 拥有路由器实例，
- 附加 `withSheetDestinations(sheet: $router.presentedSheet)`（或等效的 `sheet(item:)` 处理器），并在 Sheet 修饰符之后通过 `.environment(router)` 注入，使模态内容能继承它。

这使得子视图对 `router.presentedSheet` 的赋值能在根级驱动展示。

## 示例：需要独立导航的 Sheet

将 Sheet 内容包装在 `NavigationStack` 中，使其能在模态窗口内进行推送。

```swift
struct NavigationSheet<Content: View>: View {
  var content: () -> Content

  var body: some View {
    NavigationStack {
      content()
        .toolbar { CloseToolbarItem() }
    }
  }
}
```

## 示例：Sheet 拥有自己的操作

当操作属于模态本身时，将关闭和确认逻辑放在 Sheet 内部。

```swift
struct EditItemSheet: View {
  @Environment(\.dismiss) private var dismiss
  @Environment(Store.self) private var store

  let item: Item
  @State private var isSaving = false

  var body: some View {
    VStack {
      Button(isSaving ? "Saving..." : "Save") {
        Task { await save() }
      }
    }
  }

  private func save() async {
    isSaving = true
    await store.save(item)
    dismiss()
  }
}
```

## 设计要点

- 集中 Sheet 路由，让功能模块无需逐层传递绑定即可展示模态。
- 使用 `sheet(item:)` 保证同一时间只有一个 Sheet 处于活动状态，并通过枚举驱动展示。
- 当多个 Sheet 互斥时（如编辑器流程），将它们归入相同的 `id`。
- 保持 Sheet 视图轻量，由更小的视图组合而成，避免大型单体。
- 让 Sheet 拥有自己的操作，内部调用 `dismiss()` 而非层层传递 `onCancel` 或 `onConfirm` 闭包。

## 陷阱

- 避免对同一关注点混用 `sheet(isPresented:)` 和 `sheet(item:)`，优先使用单一枚举。
- 当展示状态已携带选中模型时，避免在 Sheet 内部使用 `if let`，优先使用 `sheet(item:)`。
- 不要在 `SheetDestination` 中存储重量级状态，传递轻量级标识符或模型即可。
- 如果同一页面可能弹出多个 Sheet，给它们不同的 `id` 值。
