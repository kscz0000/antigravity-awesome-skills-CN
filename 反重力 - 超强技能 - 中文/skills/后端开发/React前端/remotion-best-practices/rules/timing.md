---
name: timing
description: "Remotion 中的插值曲线 - 线性、缓动、弹簧动画。触发词：spring、bounce、easing、interpolation、remotion"
metadata:
  tags: spring, bounce, easing, interpolation
---

使用 `interpolate` 函数进行简单的线性插值。

```ts title="在 100 帧内从 0 到 1"
import {interpolate} from 'remotion';

const opacity = interpolate(frame, [0, 100], [0, 1]);
```

默认情况下，值不会被限制，因此值可能超出 [0, 1] 范围。
以下是限制它们的方法：

```ts title="在 100 帧内从 0 到 1，带外推限制"
const opacity = interpolate(frame, [0, 100], [0, 1], {
  extrapolateRight: 'clamp',
  extrapolateLeft: 'clamp',
});
```

## 弹簧动画

弹簧动画具有更自然的运动。
它们随时间从 0 到 1。

```ts title="在 100 帧内从 0 到 1 的弹簧动画"
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';

const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const scale = spring({
  frame,
  fps,
});
```

### 物理属性

默认配置是：`mass: 1, damping: 10, stiffness: 100`。
这会导致动画在稳定之前有一些弹跳。

可以像这样覆盖配置：

```ts
const scale = spring({
  frame,
  fps,
  config: {damping: 200},
});
```

推荐用于无弹跳自然运动的配置是：`{ damping: 200 }`。

以下是一些常见配置：

```tsx
const smooth = {damping: 200}; // 平滑，无弹跳（微妙的显示）
const snappy = {damping: 20, stiffness: 200}; // 快速，最小弹跳（UI 元素）
const bouncy = {damping: 8}; // 弹跳入场（有趣的动画）
const heavy = {damping: 15, stiffness: 80, mass: 2}; // 沉重，缓慢，小弹跳
```

### 延迟

默认情况下动画立即开始。
使用 `delay` 参数将动画延迟指定帧数。

```tsx
const entrance = spring({
  frame: frame - ENTRANCE_DELAY,
  fps,
  delay: 20,
});
```

### 时长

`spring()` 基于物理属性具有自然时长。
要将动画拉伸到特定时长，请使用 `durationInFrames` 参数。

```tsx
const spring = spring({
  frame,
  fps,
  durationInFrames: 40,
});
```

### 将 spring() 与 interpolate() 结合使用

将弹簧输出（0-1）映射到自定义范围：

```tsx
const springProgress = spring({
  frame,
  fps,
});

// 映射到旋转
const rotation = interpolate(springProgress, [0, 1], [0, 360]);

<div style={{rotate: rotation + 'deg'}} />;
```

### 添加弹簧

弹簧只返回数字，因此可以进行数学运算：

```tsx
const frame = useCurrentFrame();
const {fps, durationInFrames} = useVideoConfig();

const inAnimation = spring({
  frame,
  fps,
});
const outAnimation = spring({
  frame,
  fps,
  durationInFrames: 1 * fps,
  delay: durationInFrames - 1 * fps,
});

const scale = inAnimation - outAnimation;
```

## 缓动

可以将缓动添加到 `interpolate` 函数：

```ts
import {interpolate, Easing} from 'remotion';

const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

默认缓动是 `Easing.linear`。
还有各种其他凸度：

- `Easing.in` 用于开始慢然后加速
- `Easing.out` 用于开始快然后减速
- `Easing.inOut`

以及曲线（从最线性到最弯曲排序）：

- `Easing.quad`
- `Easing.sin`
- `Easing.exp`
- `Easing.circle`

凸度和曲线需要组合成缓动函数：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

也支持三次贝塞尔曲线：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```