---
name: text-animations
description: "Remotion 的排版和文本动画模式。触发词：typography、text、typewriter、highlighter、remotion"
metadata:
  tags: typography, text, typewriter, highlighter ken
---

## 文本动画

基于 `useCurrentFrame()`，逐字符减少字符串以创建打字机效果。

## 打字机效果

参见 [打字机](assets/text-animations-typewriter.tsx) 获取带有闪烁光标和第一句后暂停的高级示例。

始终使用字符串切片实现打字机效果。不要使用逐字符不透明度。

## 单词高亮

参见 [单词高亮](assets/text-animations-word-highlight.tsx) 获取如何为单词高亮添加动画的示例，就像荧光笔一样。