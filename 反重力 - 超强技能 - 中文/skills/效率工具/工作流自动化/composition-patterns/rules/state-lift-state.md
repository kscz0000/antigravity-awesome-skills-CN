---
title: 将状态提升到 Provider 组件中
impact: HIGH
impactDescription: 允许状态在组件边界之外共享
tags: composition, state, context, providers
---

## 将状态提升到 Provider 组件中

将状态管理迁移到专门的 Provider 组件中。这使得主 UI 之外的兄弟组件也能访问和修改状态，无需 props 透传或别扭的 refs。

**错误示例（状态被局限在组件内部）：**

```tsx
function ForwardMessageComposer() {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer />
    </Composer.Frame>
  )
}

// 问题：这个按钮如何访问编辑器的状态？
function ForwardMessageDialog() {
  return (
    <Dialog>
      <ForwardMessageComposer />
      <MessagePreview /> {/* 需要编辑器的状态 */}
      <DialogActions>
        <CancelButton />
        <ForwardButton /> {/* 需要调用 submit */}
      </DialogActions>
    </Dialog>
  )
}
```

**错误示例（使用 useEffect 把状态同步上去）：**

```tsx
function ForwardMessageDialog() {
  const [input, setInput] = useState('')
  return (
    <Dialog>
      <ForwardMessageComposer onInputChange={setInput} />
      <MessagePreview input={input} />
    </Dialog>
  )
}

function ForwardMessageComposer({ onInputChange }) {
  const [state, setState] = useState(initialState)
  useEffect(() => {
    onInputChange(state.input) // 每次变化都同步 😬
  }, [state.input])
}
```

**错误示例（提交时通过 ref 读取状态）：**

```tsx
function ForwardMessageDialog() {
  const stateRef = useRef(null)
  return (
    <Dialog>
      <ForwardMessageComposer stateRef={stateRef} />
      <ForwardButton onPress={() => submit(stateRef.current)} />
    </Dialog>
  )
}
```

**正确示例（状态被提升到 Provider）：**

```tsx
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        <ForwardMessageComposer />
        <MessagePreview /> {/* 自定义组件可以访问状态与动作 */}
        <DialogActions>
          <CancelButton />
          <ForwardButton /> {/* 自定义组件可以访问状态与动作 */}
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

function ForwardButton() {
  const { actions } = use(Composer.Context)
  return <Button onPress={actions.submit}>Forward</Button>
}
```

`ForwardButton` 在视觉上位于 `Composer.Frame` 之外，但因为它处在 Provider 内部，所以依然可以访问 submit 动作。即使它是一次性的组件，它依然可以从 UI 外部访问编辑器的状态和动作。

**核心洞察：** 需要共享状态的组件不必在视觉上互相嵌套——它们只需要位于同一个 Provider 之下。
