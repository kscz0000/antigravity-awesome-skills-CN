---
title: 将状态管理与 UI 解耦
impact: MEDIUM
impactDescription: 可在不修改 UI 的情况下替换状态实现
tags: composition, state, architecture
---

## 将状态管理与 UI 解耦

Provider 组件应该是唯一知晓状态如何被管理的地方。UI 组件消费上下文接口，它们并不关心状态来自 `useState`、Zustand，还是服务器同步。

**错误示例（UI 与状态实现耦合）：**

```tsx
function ChannelComposer({ channelId }: { channelId: string }) {
  // UI 组件直接知道全局状态的实现细节
  const state = useGlobalChannelState(channelId)
  const { submit, updateInput } = useChannelSync(channelId)

  return (
    <Composer.Frame>
      <Composer.Input
        value={state.input}
        onChange={(text) => sync.updateInput(text)}
      />
      <Composer.Submit onPress={() => sync.submit()} />
    </Composer.Frame>
  )
}
```

**正确示例（状态管理被隔离在 Provider 中）：**

```tsx
// Provider 负责处理所有状态管理细节
function ChannelProvider({
  channelId,
  children,
}: {
  channelId: string
  children: React.ReactNode
}) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update, submit }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

// UI 组件只关心上下文接口
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 用法
function Channel({ channelId }: { channelId: string }) {
  return (
    <ChannelProvider channelId={channelId}>
      <ChannelComposer />
    </ChannelProvider>
  )
}
```

**不同的 Provider，相同的 UI：**

```tsx
// 用于临时表单的本地状态
function ForwardMessageProvider({ children }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
    >
      {children}
    </Composer.Provider>
  )
}

// 用于频道的全局同步状态
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)

  return (
    <Composer.Provider state={state} actions={{ update, submit }}>
      {children}
    </Composer.Provider>
  )
}
```

同一个 `Composer.Input` 组件可以与这两种 Provider 都一起工作，因为它只依赖上下文接口，不依赖具体实现。
