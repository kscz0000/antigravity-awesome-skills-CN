# 输入工具栏（底部固定）

## 意图

使用底部固定的输入栏用于聊天、编辑器或快捷操作，无需与键盘冲突。

## 核心模式

- 使用 `.safeAreaInset(edge: .bottom)` 将工具栏固定在键盘上方。
- 主内容放在 `ScrollView` 或 `List` 中。
- 使用 `@FocusState` 驱动焦点，需要时设置初始焦点。
- 避免将输入栏嵌入滚动内容内部，保持独立。

## 示例：滚动视图 + 底部输入

```swift
@MainActor
struct ConversationView: View {
  @FocusState private var isInputFocused: Bool

  var body: some View {
    ScrollViewReader { _ in
      ScrollView {
        LazyVStack {
          ForEach(messages) { message in
            MessageRow(message: message)
          }
        }
        .padding(.horizontal, .layoutPadding)
      }
      .safeAreaInset(edge: .bottom) {
        InputBar(text: $draft)
          .focused($isInputFocused)
      }
      .scrollDismissesKeyboard(.interactively)
      .onAppear { isInputFocused = true }
    }
  }
}
```

## 设计要点

- 输入栏与可滚动内容在视觉上保持分隔。
- 聊天类页面使用 `.scrollDismissesKeyboard(.interactively)`。
- 确保发送操作可通过键盘回车键或明确的按钮触达。

## 陷阱

- 避免将输入视图放在滚动堆栈内部，否则会随内容跳动。
- 避免嵌套会争抢拖拽手势的滚动视图。
