---
name: sequencing
description: "Remotion 的序列模式 - 延迟、剪辑、限制项目时长。触发词：sequence、series、timing、delay、trim、remotion"
metadata:
  tags: sequence, series, timing, delay, trim
---

使用 `<Sequence>` 延迟元素在时间轴中的出现时间。

```tsx
import { Sequence } from "remotion";

const {fps} = useVideoConfig();

<Sequence from={1 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Title />
</Sequence>
<Sequence from={2 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Subtitle />
</Sequence>
```

默认情况下，这会将组件包裹在绝对填充元素中。
如果项目不应该被包裹，请使用 `layout` 属性：

```tsx
<Sequence layout="none">
  <Title />
</Sequence>
```

## 预加载

这会在组件实际播放之前在时间轴中加载它。
始终预加载任何 `<Sequence>`！

```tsx
<Sequence premountFor={1 * fps}>
  <Title />
</Sequence>
```

## 系列

当元素应该一个接一个播放而不重叠时，使用 `<Series>`。

```tsx
import {Series} from 'remotion';

<Series>
  <Series.Sequence durationInFrames={45}>
    <Intro />
  </Series.Sequence>
  <Series.Sequence durationInFrames={60}>
    <MainContent />
  </Series.Sequence>
  <Series.Sequence durationInFrames={30}>
    <Outro />
  </Series.Sequence>
</Series>;
```

与 `<Sequence>` 类似，使用 `<Series.Sequence>` 时，项目默认会被包裹在绝对填充元素中，除非 `layout` 属性设置为 `none`。

### 带重叠的系列

使用负偏移实现重叠序列：

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <SceneA />
  </Series.Sequence>
  <Series.Sequence offset={-15} durationInFrames={60}>
    {/* 在 SceneA 结束前 15 帧开始 */}
    <SceneB />
  </Series.Sequence>
</Series>
```

## 序列内的帧引用

在 Sequence 内部，`useCurrentFrame()` 返回本地帧（从 0 开始）：

```tsx
<Sequence from={60} durationInFrames={30}>
  <MyComponent />
  {/* 在 MyComponent 内部，useCurrentFrame() 返回 0-29，而不是 60-89 */}
</Sequence>
```

## 嵌套序列

序列可以嵌套以实现复杂的时序：

```tsx
<Sequence from={0} durationInFrames={120}>
  <Background />
  <Sequence from={15} durationInFrames={90} layout="none">
    <Title />
  </Sequence>
  <Sequence from={45} durationInFrames={60} layout="none">
    <Subtitle />
  </Sequence>
</Sequence>
```