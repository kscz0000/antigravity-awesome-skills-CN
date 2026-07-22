---
title: 使用延迟状态初始化
impact: MEDIUM
impactDescription: 每次渲染都有浪费的计算
tags: react, hooks, useState, performance, initialization
---

## 使用延迟状态初始化

对于昂贵的初始值，向 `useState` 传递一个函数。不使用函数形式时，初始化器会在每次渲染时运行，即使该值只使用一次。

**错误写法（每次渲染都运行）：**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() 每次渲染都运行，即使已初始化
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  // 当 query 变化时，buildSearchIndex 会不必要地再次运行
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse 每次渲染都运行
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('settings') || '{}')
  )
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

**正确写法（仅运行一次）：**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() 仅在初始渲染时运行
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse 仅在初始渲染时运行
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  })
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

在以下场景使用延迟初始化：从 localStorage/sessionStorage 计算初始值、构建数据结构（索引、映射）、从 DOM 读取、或执行繁重的转换。

对于简单原始类型（`useState(0)`）、直接引用（`useState(props.value)`）或廉价字面量（`useState({})`），函数形式是不必要的。