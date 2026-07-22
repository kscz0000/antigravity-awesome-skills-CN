---
title: 优先使用 children 进行组合，而非 render props
impact: MEDIUM
impactDescription: 更整洁的组合方式，可读性更佳
tags: composition, children, render-props
---

## 优先使用 children 而非 render props

在组合时使用 `children` 而非 `renderX` 类型的 props。children 更易读、组合更自然，且不需要理解回调签名。

**错误示例（render props）：**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
}: {
  renderHeader?: () => React.ReactNode
  renderFooter?: () => React.ReactNode
  renderActions?: () => React.ReactNode
}) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {renderFooter ? renderFooter() : <DefaultFooter />}
      {renderActions?.()}
    </form>
  )
}

// 用法很别扭且缺乏灵活性
return (
  <Composer
    renderHeader={() => <CustomHeader />}
    renderFooter={() => (
      <>
        <Formatting />
        <Emojis />
      </>
    )}
    renderActions={() => <SubmitButton />}
  />
)
```

**正确示例（带 children 的复合组件）：**

```tsx
function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerFooter({ children }: { children: React.ReactNode }) {
  return <footer className='flex'>{children}</footer>
}

// 用法很灵活
return (
  <Composer.Frame>
    <CustomHeader />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Emojis />
      <SubmitButton />
    </Composer.Footer>
  </Composer.Frame>
)
```

**适合使用 render props 的场景：**

```tsx
// 当需要把数据回传给子组件时，render props 表现良好
<List
  data={items}
  renderItem={({ item, index }) => <Item item={item} index={index} />}
/>
```

当父组件需要向子组件提供数据或状态时，使用 render props。在组合静态结构时，使用 children。
