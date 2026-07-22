# Form

## 意图

使用 `Form` 构建结构化设置、分组输入和操作行。此模式为数据录入页面保持一致的布局、间距和无障碍性。

## 核心模式

- 仅当表单在 Sheet 中或没有现有导航上下文的独立视图中展示时，才用 `NavigationStack` 包装。
- 将相关控件分组到 `Section` 块中。
- 需要设计系统颜色时使用 `.scrollContentBackground(.hidden)` 加自定义背景色。
- 适当时应用 `.formStyle(.grouped)` 实现分组样式。
- 输入密集的表单使用 `@FocusState` 管理键盘焦点。

## 示例：设置式表单

```swift
@MainActor
struct SettingsView: View {
  @Environment(Theme.self) private var theme

  var body: some View {
    NavigationStack {
      Form {
        Section("General") {
          NavigationLink("Display") { DisplaySettingsView() }
          NavigationLink("Haptics") { HapticsSettingsView() }
        }

        Section("Account") {
          Button("Edit profile") { /* open sheet */ }
            .buttonStyle(.plain)
        }
        .listRowBackground(theme.primaryBackgroundColor)
      }
      .navigationTitle("Settings")
      .navigationBarTitleDisplayMode(.inline)
      .scrollContentBackground(.hidden)
      .background(theme.secondaryBackgroundColor)
    }
  }
}
```

## 示例：带验证的模态表单

```swift
@MainActor
struct AddRemoteServerView: View {
  @Environment(\.dismiss) private var dismiss
  @Environment(Theme.self) private var theme

  @State private var server: String = ""
  @State private var isValid = false
  @FocusState private var isServerFieldFocused: Bool

  var body: some View {
    NavigationStack {
      Form {
        TextField("Server URL", text: $server)
          .keyboardType(.URL)
          .textInputAutocapitalization(.never)
          .autocorrectionDisabled()
          .focused($isServerFieldFocused)
          .listRowBackground(theme.primaryBackgroundColor)

        Button("Add") {
          guard isValid else { return }
          dismiss()
        }
        .disabled(!isValid)
        .listRowBackground(theme.primaryBackgroundColor)
      }
      .formStyle(.grouped)
      .navigationTitle("Add Server")
      .navigationBarTitleDisplayMode(.inline)
      .scrollContentBackground(.hidden)
      .background(theme.secondaryBackgroundColor)
      .scrollDismissesKeyboard(.immediately)
      .toolbar { CancelToolbarItem() }
      .onAppear { isServerFieldFocused = true }
    }
  }
}
```

## 设计要点

- 设置和输入页面优先使用 `Form` 而非自定义堆栈。
- 行按钮使用 `.contentShape(Rectangle())` 和 `.buttonStyle(.plain)` 保持可点击。
- 使用列表行背景保持分区样式与主题一致。

## 陷阱

- 避免在 `Form` 内使用重量级自定义布局，会导致间距问题。
- 需要高度自定义布局时，优先使用 `ScrollView` + `VStack`。
- 不要混用多种背景策略，选择默认 Form 样式或自定义颜色之一。
