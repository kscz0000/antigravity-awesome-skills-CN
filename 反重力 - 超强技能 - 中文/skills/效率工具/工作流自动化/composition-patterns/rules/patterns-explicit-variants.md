---
title: 创建明确的组件变体
impact: MEDIUM
impactDescription: 代码自解释，不存在隐藏的条件判断
tags: composition, variants, architecture
---

## 创建明确的组件变体

不要使用一个组件加上一堆布尔 props，而应创建明确的变体组件。每个变体按需组合所需的部分，代码本身就是文档。

**错误示例（一个组件拥有多种模式）：**

```tsx
// 这个组件究竟会渲染什么？
<Composer
  isThread
  isEditing={false}
  channelId='abc'
  showAttachments
  showFormatting={false}
/>
```

**正确示例（明确的变体）：**

```tsx
// 一眼就能看出渲染了什么
<ThreadComposer channelId="abc" />

// 或
<EditMessageComposer messageId="xyz" />

// 或
<ForwardMessageComposer messageId="123" />
```

每种实现都是唯一的、明确的、自包含的，但它们又都可以复用共享的部分。

**实现：**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ThreadProvider channelId={channelId}>
      <Composer.Frame>
        <Composer.Input />
        <AlsoSendToChannelField channelId={channelId} />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </ThreadProvider>
  )
}

function EditMessageComposer({ messageId }: { messageId: string }) {
  return (
    <EditMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.CancelEdit />
          <Composer.SaveEdit />
        </Composer.Footer>
      </Composer.Frame>
    </EditMessageProvider>
  )
}

function ForwardMessageComposer({ messageId }: { messageId: string }) {
  return (
    <ForwardMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input placeholder="Add a message, if you'd like." />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Mentions />
        </Composer.Footer>
      </Composer.Frame>
    </ForwardMessageProvider>
  )
}
```

每个变体都明确说明了：

- 它使用了哪个 Provider/状态
- 它包含了哪些 UI 元素
- 它提供了哪些操作

无需推理布尔 props 的组合。不存在不可能的状态。
