---
title: 使用 CSS content-visibility 优化长列表
impact: HIGH
impactDescription: 更快的首次渲染
tags: rendering, css, content-visibility, long-lists
---

## 使用 CSS content-visibility 优化长列表

应用 `content-visibility: auto` 以延迟屏幕外元素的渲染。

**CSS：**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**示例：**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

对于 1000 条消息，浏览器跳过约 990 个屏幕外元素的布局/绘制（首次渲染速度提升 10 倍）。
