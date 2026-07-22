---
name: charts
description: "Remotion 的图表和数据可视化模式。适用于创建条形图、饼图、直方图、进度条或任何数据驱动的动画。触发词：charts、data、visualization、bar-chart、pie-chart、graphs、remotion"
metadata:
  tags: charts, data, visualization, bar-chart, pie-chart, graphs
---

# Remotion 中的图表

你可以使用常规 React 代码在 Remotion 中创建条形图 - 允许使用 HTML 和 SVG，也支持 D3.js。

## 禁止非 `useCurrentFrame()` 驱动的动画

禁用第三方库的所有动画。
它们在渲染过程中会导致闪烁。
改为从 `useCurrentFrame()` 驱动所有动画。

## 条形图动画

参见条形图示例获取基本示例实现。

### 交错条形图

你可以像这样为条形图的高度添加动画并实现交错效果：

```tsx
const STAGGER_DELAY = 5;
const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const bars = data.map((item, i) => {
  const delay = i * STAGGER_DELAY;
  const height = spring({
    frame,
    fps,
    delay,
    config: {damping: 200},
  });
  return <div style={{height: height * item.value}} />;
});
```

## 饼图动画

使用 stroke-dashoffset 为扇形添加动画，从 12 点钟方向开始。

```tsx
const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const progress = interpolate(frame, [0, 100], [0, 1]);

const circumference = 2 * Math.PI * radius;
const segmentLength = (value / total) * circumference;
const offset = interpolate(progress, [0, 1], [segmentLength, 0]);

<circle r={radius} cx={center} cy={center} fill="none" stroke={color} strokeWidth={strokeWidth} strokeDasharray={`${segmentLength} ${circumference}`} strokeDashoffset={offset} transform={`rotate(-90 ${center} ${center})`} />;
```