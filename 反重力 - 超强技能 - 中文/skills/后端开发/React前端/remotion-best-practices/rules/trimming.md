---
name: trimming
description: "Remotion 的剪辑模式 - 裁剪动画的开头或结尾。触发词：sequence、trim、clip、cut、offset、remotion"
metadata:
  tags: sequence, trim, clip, cut, offset
---

使用带有负 `from` 值的 `<Sequence>` 来裁剪动画的开头。

## 裁剪开头

负的 `from` 值会将时间向后移动，使动画从中间开始：

```tsx
import { Sequence, useVideoConfig } from "remotion";

const fps = useVideoConfig();

<Sequence from={-0.5 * fps}>
  <MyAnimation />
</Sequence>
```

动画在其进度的第 15 帧出现 - 前 15 帧被裁剪掉。
在 `<MyAnimation>` 内部，`useCurrentFrame()` 从 15 开始而不是 0。

## 裁剪结尾

使用 `durationInFrames` 在指定时长后卸载内容：

```tsx

<Sequence durationInFrames={1.5 * fps}>
  <MyAnimation />
</Sequence>
```

动画播放 45 帧，然后组件被卸载。

## 裁剪和延迟

嵌套序列以同时裁剪开头和延迟出现时间：

```tsx
<Sequence from={30}>
  <Sequence from={-15}>
    <MyAnimation />
  </Sequence>
</Sequence>
```

内部序列从开头裁剪 15 帧，外部序列将结果延迟 30 帧。