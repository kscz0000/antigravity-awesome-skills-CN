---
title: 禁止对可能为假值的表达式使用 &&
impact: CRITICAL
impactDescription: 防止生产环境崩溃
tags: rendering, conditional, jsx, crash
---

## 禁止对可能为假值的表达式使用 &&

当 `value` 可能为空字符串或 `0` 时，绝不要使用 `{value && <Component />}`。这些值虽然是假值但可被 JSX 渲染——React Native 会尝试将它们作为文本渲染到 `<Text>` 组件外，导致生产环境硬崩溃。

**错误（当 count 为 0 或 name 为 "" 时崩溃）：**

```tsx
function Profile({ name, count }: { name: string; count: number }) {
  return (
    <View>
      {name && <Text>{name}</Text>}
      {count && <Text>{count} items</Text>}
    </View>
  )
}
// If name="" or count=0, renders the falsy value → crash
```

**正确（三元表达式返回 null）：**

```tsx
function Profile({ name, count }: { name: string; count: number }) {
  return (
    <View>
      {name ? <Text>{name}</Text> : null}
      {count ? <Text>{count} items</Text> : null}
    </View>
  )
}
```

**正确（显式布尔转换）：**

```tsx
function Profile({ name, count }: { name: string; count: number }) {
  return (
    <View>
      {!!name && <Text>{name}</Text>}
      {!!count && <Text>{count} items</Text>}
    </View>
  )
}
```

**最佳（提前返回）：**

```tsx
function Profile({ name, count }: { name: string; count: number }) {
  if (!name) return null

  return (
    <View>
      <Text>{name}</Text>
      {count > 0 ? <Text>{count} items</Text> : null}
    </View>
  )
}
```

提前返回最为清晰。在行内使用条件渲染时，优先使用三元表达式或显式布尔检查。

**Lint 规则：** 启用 `react/jsx-no-leaked-render`（来自
[eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-no-leaked-render.md)）可自动检测此问题。
