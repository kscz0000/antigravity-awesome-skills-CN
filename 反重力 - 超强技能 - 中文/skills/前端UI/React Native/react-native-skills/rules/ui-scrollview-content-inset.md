---
title: 使用 contentInset 实现 ScrollView 动态间距
impact: LOW
impactDescription: 更流畅的更新，无需布局重算
tags: scrollview, layout, contentInset, performance
---

## 使用 contentInset 实现 ScrollView 动态间距

当需要在 ScrollView 顶部或底部添加可能变化的间距（键盘、工具栏、动态内容）时，使用 `contentInset` 替代内边距。修改 `contentInset` 不会触发布局重算——它只调整滚动区域而不重新渲染内容。

**错误（内边距导致布局重算）：**

```tsx
function Feed({ bottomOffset }: { bottomOffset: number }) {
  return (
    <ScrollView contentContainerStyle={{ paddingBottom: bottomOffset }}>
      {children}
    </ScrollView>
  )
}
// Changing bottomOffset triggers full layout recalculation
```

**正确（contentInset 实现动态间距）：**

```tsx
function Feed({ bottomOffset }: { bottomOffset: number }) {
  return (
    <ScrollView
      contentInset={{ bottom: bottomOffset }}
      scrollIndicatorInsets={{ bottom: bottomOffset }}
    >
      {children}
    </ScrollView>
  )
}
// Changing bottomOffset only adjusts scroll bounds
```

配合 `contentInset` 使用 `scrollIndicatorInsets` 以保持滚动指示器对齐。对于不会变化的静态间距，使用内边距即可。
