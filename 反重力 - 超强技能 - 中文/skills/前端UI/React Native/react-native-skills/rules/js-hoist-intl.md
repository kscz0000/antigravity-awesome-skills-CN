---
title: Hoist Intl Formatter Creation
impact: LOW-MEDIUM
impactDescription: 避免昂贵的对象重复创建
tags: javascript, intl, optimization, memoization
---

## 提升 Intl 格式化器创建

不要在渲染函数或循环内创建 `Intl.DateTimeFormat`、`Intl.NumberFormat` 或
`Intl.RelativeTimeFormat`。这些对象实例化开销很大。当区域设置/选项是静态的时，提升到模块作用域。

**错误示例（每次渲染创建新格式化器）：**

```tsx
function Price({ amount }: { amount: number }) {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  })
  return <Text>{formatter.format(amount)}</Text>
}
```

**正确示例（提升到模块作用域）：**

```tsx
const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
})

function Price({ amount }: { amount: number }) {
  return <Text>{currencyFormatter.format(amount)}</Text>
}
```

**动态区域设置时，使用 memoize：**

```tsx
const dateFormatter = useMemo(
  () => new Intl.DateTimeFormat(locale, { dateStyle: 'medium' }),
  [locale]
)
```

**常用格式化器提升示例：**

```tsx
// Module-level formatters
const dateFormatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' })
const timeFormatter = new Intl.DateTimeFormat('en-US', { timeStyle: 'short' })
const percentFormatter = new Intl.NumberFormat('en-US', { style: 'percent' })
const relativeFormatter = new Intl.RelativeTimeFormat('en-US', {
  numeric: 'auto',
})
```

创建 `Intl` 对象的开销远大于 `RegExp` 或普通对象——每次实例化都要解析区域设置数据并构建内部查找表。
