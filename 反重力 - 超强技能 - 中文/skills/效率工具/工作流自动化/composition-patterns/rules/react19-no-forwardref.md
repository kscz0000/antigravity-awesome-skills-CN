---
title: React 19 API 变更
impact: MEDIUM
impactDescription: 更简洁的组件定义和上下文使用方式
tags: react19, refs, context, hooks
---

## React 19 API 变更

> **⚠️ 仅适用于 React 19+。若你在 React 18 或更早版本上工作，可以跳过此条。**

在 React 19 中，`ref` 现在是一个普通 prop（无需 `forwardRef` 包装），并且 `use()` 取代了 `useContext()`。

**错误示例（在 React 19 中使用 forwardRef）：**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**正确示例（ref 作为普通 prop）：**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**错误示例（在 React 19 中使用 useContext）：**

```tsx
const value = useContext(MyContext)
```

**正确示例（用 use 代替 useContext）：**

```tsx
const value = use(MyContext)
```

`use()` 也可以被条件性地调用，而 `useContext()` 不可以。
