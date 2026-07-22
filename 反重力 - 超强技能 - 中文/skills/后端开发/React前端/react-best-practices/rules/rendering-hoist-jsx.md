---
title: 提升静态 JSX 元素
impact: LOW
impactDescription: 避免重复创建
tags: rendering, jsx, static, optimization
---

## 提升静态 JSX 元素

将静态 JSX 提取到组件外部以避免重复创建。

**错误写法（每次渲染都重新创建元素）：**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />
}

function Container() {
  return (
    <div>
      {loading && <LoadingSkeleton />}
    </div>
  )
}
```

**正确写法（复用同一元素）：**

```tsx
const loadingSkeleton = (
  <div className="animate-pulse h-20 bg-gray-200" />
)

function Container() {
  return (
    <div>
      {loading && loadingSkeleton}
    </div>
  )
}
```

对于大型且静态的 SVG 节点尤其有用，因为每次渲染重新创建它们的代价很高。

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，编译器会自动提升静态 JSX 元素并优化组件重渲染，无需手动提升。