---
title: 避免布尔 props 膨胀
impact: CRITICAL
impactDescription: 防止出现难以维护的组件变体
tags: composition, props, architecture
---

## 避免布尔 props 膨胀

不要添加诸如 `isThread`、`isEditing`、`isDMThread` 之类的布尔 props 来定制组件行为。每个布尔值都会使可能的状态组合翻倍，并产生难以维护的条件逻辑。请改用组合。

**错误示例（布尔 props 会产生指数级复杂度）：**

```tsx
function Composer({
  onSubmit,
  isThread,
  channelId,
  isDMThread,
  dmId,
  isEditing,
  isForwarding,
}: Props) {
  return (
    <form>
      <Header />
      <Input />
      {isDMThread ? (
        <AlsoSendToDMField id={dmId} />
      ) : isThread ? (
        <AlsoSendToChannelField id={channelId} />
      ) : null}
      {isEditing ? (
        <EditActions />
      ) : isForwarding ? (
        <ForwardActions />
      ) : (
        <DefaultActions />
      )}
      <Footer onSubmit={onSubmit} />
    </form>
  )
}
```

**正确示例（组合消除了条件判断）：**

```tsx
// 频道编辑器
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Attachments />
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 主题回复编辑器 - 额外添加"同时发送到频道"字段
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 编辑消息编辑器 - 不同的底部操作
function EditComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.CancelEdit />
        <Composer.SaveEdit />
      </Composer.Footer>
    </Composer.Frame>
  )
}
```

每个变体都明确描述它渲染了什么。我们可以在不共享单一父组件的前提下共享内部结构。
