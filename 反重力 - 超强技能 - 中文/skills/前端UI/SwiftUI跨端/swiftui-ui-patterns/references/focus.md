# 焦点处理与字段链

## 意图

使用 `@FocusState` 控制键盘焦点、链接字段，并在复杂表单中协调焦点。

## 核心模式

- 使用枚举表示可聚焦的字段。
- 在 `onAppear` 中设置初始焦点。
- 使用 `.onSubmit` 将焦点移动到下一个字段。
- 对于动态字段列表，使用带关联值的枚举（如 `.option(Int)`）。

## 示例：单字段焦点

```swift
struct AddServerView: View {
  @State private var server = ""
  @FocusState private var isServerFieldFocused: Bool

  var body: some View {
    Form {
      TextField("Server", text: $server)
        .focused($isServerFieldFocused)
    }
    .onAppear { isServerFieldFocused = true }
  }
}
```

## 示例：枚举链式焦点

```swift
struct EditTagView: View {
  enum FocusField { case title, symbol, newTag }
  @FocusState private var focusedField: FocusField?

  var body: some View {
    Form {
      TextField("Title", text: $title)
        .focused($focusedField, equals: .title)
        .onSubmit { focusedField = .symbol }

      TextField("Symbol", text: $symbol)
        .focused($focusedField, equals: .symbol)
        .onSubmit { focusedField = .newTag }
    }
    .onAppear { focusedField = .title }
  }
}
```

## 示例：可变字段的动态焦点

```swift
struct PollView: View {
  enum FocusField: Hashable { case option(Int) }
  @FocusState private var focused: FocusField?
  @State private var options: [String] = ["", ""]
  @State private var currentIndex = 0

  var body: some View {
    ForEach(options.indices, id: \.self) { index in
      TextField("Option \(index + 1)", text: $options[index])
        .focused($focused, equals: .option(index))
        .onSubmit { addOption(at: index) }
    }
    .onAppear { focused = .option(0) }
  }

  private func addOption(at index: Int) {
    options.append("")
    currentIndex = index + 1
    DispatchQueue.main.asyncAfter(deadline: .now() + 0.01) {
      focused = .option(currentIndex)
    }
  }
}
```

## 设计要点

- 焦点状态保留在拥有字段的视图本地。
- 使用焦点变更驱动 UX（验证消息、辅助 UI）。
- 使用 ScrollView/Form 时配合 `.scrollDismissesKeyboard(...)`。

## 陷阱

- 不要将焦点状态存储在共享对象中，它是视图本地的。
- 避免在动画期间激进地变更焦点，必要时延迟。
