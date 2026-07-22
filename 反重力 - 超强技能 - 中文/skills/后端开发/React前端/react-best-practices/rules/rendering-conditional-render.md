---
title: 使用显式条件渲染
impact: LOW
impactDescription: 防止渲染 0 或 NaN
tags: rendering, conditional, jsx, falsy-values
---

## 使用显式条件渲染

当条件可能是 `0`、`NaN` 或其他会渲染的 falsy 值时，使用显式三元运算符（`? :`）代替 `&&` 进行条件渲染。

**错误（count 为 0 时渲染 "0"）：**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// When count = 0, renders: <div>0</div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

**正确（count 为 0 时不渲染）：**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// When count = 0, renders: <div></div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```
