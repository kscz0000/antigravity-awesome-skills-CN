---
title: 批量处理 DOM CSS 变更
impact: MEDIUM
impactDescription: 减少回流/重绘
tags: javascript, dom, css, performance, reflow
---

## 批量处理 DOM CSS 变更

避免逐个属性地修改样式。通过类名或 `cssText` 将多个 CSS 变更组合在一起，以最小化浏览器回流。

**错误做法（多次回流）：**

```typescript
function updateElementStyles(element: HTMLElement) {
  // 每一行都会触发一次回流
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
}
```

**正确做法（添加类名 - 单次回流）：**

```typescript
// CSS 文件
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}

// JavaScript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
}
```

**正确做法（修改 cssText - 单次回流）：**

```typescript
function updateElementStyles(element: HTMLElement) {
  element.style.cssText = `
    width: 100px;
    height: 200px;
    background-color: blue;
    border: 1px solid black;
  `
}
```

**React 示例：**

```tsx
// 错误：逐个修改样式
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px'
      ref.current.style.height = '200px'
      ref.current.style.backgroundColor = 'blue'
    }
  }, [isHighlighted])
  
  return <div ref={ref}>Content</div>
}

// 正确：切换类名
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  )
}
```

尽可能优先使用 CSS 类而非内联样式。类由浏览器缓存，并提供更好的关注点分离。
