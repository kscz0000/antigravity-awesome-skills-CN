---
title: 使用回退状态替代 initialState
impact: MEDIUM
impactDescription: 响应式回退，无需同步
tags: state, hooks, derived-state, props, initialState
---

## 使用回退状态替代 initialState

使用 `undefined` 作为初始状态，并用空值合并运算符（`??`）回退到父组件或服务端值。状态仅代表用户意图——`undefined` 表示"用户尚未选择"。这样可以实现响应式回退，当数据源变化时自动更新，而非仅在首次渲染时生效。

**错误（同步状态，丧失响应性）：**

```tsx
type Props = { fallbackEnabled: boolean }

function Toggle({ fallbackEnabled }: Props) {
  const [enabled, setEnabled] = useState(defaultEnabled)
  // If fallbackEnabled changes, state is stale
  // State mixes user intent with default value

  return <Switch value={enabled} onValueChange={setEnabled} />
}
```

**正确（状态为用户意图，响应式回退）：**

```tsx
type Props = { fallbackEnabled: boolean }

function Toggle({ fallbackEnabled }: Props) {
  const [_enabled, setEnabled] = useState<boolean | undefined>(undefined)
  const enabled = _enabled ?? defaultEnabled
  // undefined = user hasn't touched it, falls back to prop
  // If defaultEnabled changes, component reflects it
  // Once user interacts, their choice persists

  return <Switch value={enabled} onValueChange={setEnabled} />
}
```

**配合服务端数据：**

```tsx
function ProfileForm({ data }: { data: User }) {
  const [_theme, setTheme] = useState<string | undefined>(undefined)
  const theme = _theme ?? data.theme
  // Shows server value until user overrides
  // Server refetch updates the fallback automatically

  return <ThemePicker value={theme} onChange={setTheme} />
}
```
