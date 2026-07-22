---
title: 为依赖注入定义通用上下文接口
impact: HIGH
impactDescription: 使状态在不同用例间可被依赖注入
tags: composition, context, state, typescript, dependency-injection
---

## 为依赖注入定义通用上下文接口

为你的组件上下文定义一个**通用接口**，包含三部分：`state`、`actions` 和 `meta`。这个接口是一份契约，任何 Provider 都可以实现它——这使得同一套 UI 组件能够与完全不同的状态实现协同工作。

**核心原则：** 提升状态、组合内部、把状态变成可被依赖注入的东西。

**错误示例（UI 与特定的状态实现耦合）：**

```tsx
function ComposerInput() {
  // 与某个具体的 hook 紧耦合
  const { input, setInput } = useChannelComposerState()
  return <TextInput value={input} onChangeText={setInput} />
}
```

**正确示例（通过通用接口实现依赖注入）：**

```tsx
// 定义一个任何 Provider 都可以实现的通用接口
interface ComposerState {
  input: string
  attachments: Attachment[]
  isSubmitting: boolean
}

interface ComposerActions {
  update: (updater: (state: ComposerState) => ComposerState) => void
  submit: () => void
}

interface ComposerMeta {
  inputRef: React.RefObject<TextInput>
}

interface ComposerContextValue {
  state: ComposerState
  actions: ComposerActions
  meta: ComposerMeta
}

const ComposerContext = createContext<ComposerContextValue | null>(null)
```

**UI 组件消费该接口，而非具体实现：**

```tsx
function ComposerInput() {
  const {
    state,
    actions: { update },
    meta,
  } = use(ComposerContext)

  // 任何实现该接口的 Provider 都可以配合该组件工作
  return (
    <TextInput
      ref={meta.inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}
```

**不同的 Provider 实现同一个接口：**

```tsx
// Provider A：为临时表单提供本地状态
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const inputRef = useRef(null)
  const submit = useForwardMessage()

  return (
    <ComposerContext
      value={{
        state,
        actions: { update: setState, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}

// Provider B：为频道提供全局同步状态
function ChannelProvider({ channelId, children }: Props) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <ComposerContext
      value={{
        state,
        actions: { update, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}
```

**同一套组合 UI 能与两种 Provider 都正常工作：**

```tsx
// 可与 ForwardMessageProvider 一起工作（本地状态）
<ForwardMessageProvider>
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ForwardMessageProvider>

// 可与 ChannelProvider 一起工作（全局同步状态）
<ChannelProvider channelId="abc">
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ChannelProvider>
```

**组件外部的自定义 UI 也可以访问状态与动作：**

关键在于 Provider 边界，而非视觉上的嵌套。需要共享状态的组件不必放在 `Composer.Frame` 内部，只要位于 Provider 之内即可。

```tsx
function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        {/* 编辑器 UI */}
        <Composer.Frame>
          <Composer.Input placeholder="Add a message, if you'd like." />
          <Composer.Footer>
            <Composer.Formatting />
            <Composer.Emojis />
          </Composer.Footer>
        </Composer.Frame>

        {/* 自定义 UI，位于编辑器之外但在 Provider 之内 */}
        <MessagePreview />

        {/* 位于对话框底部的操作 */}
        <DialogActions>
          <CancelButton />
          <ForwardButton />
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

// 这个按钮位于 Composer.Frame 之外，但仍然可以根据其上下文触发提交！
function ForwardButton() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>Forward</Button>
}

// 这个预览组件位于 Composer.Frame 之外，但能读取编辑器的状态！
function MessagePreview() {
  const { state } = use(ComposerContext)
  return <Preview message={state.input} attachments={state.attachments} />
}
```

`ForwardButton` 和 `MessagePreview` 在视觉上并不在编辑器框内，但它们依然可以访问其状态和动作。这就是把状态提升到 Provider 中的强大之处。

UI 是可复用、可组合的片段。状态由 Provider 进行依赖注入。换掉 Provider，UI 保持不变。
