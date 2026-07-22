---
name: measuring-dom-nodes
description: "在 Remotion 中测量 DOM 元素尺寸。触发词：measure、layout、dimensions、getBoundingClientRect、scale、remotion"
metadata:
  tags: measure, layout, dimensions, getBoundingClientRect, scale
---

# 在 Remotion 中测量 DOM 节点

Remotion 对视频容器应用 `scale()` 变换，这会影响 `getBoundingClientRect()` 的值。使用 `useCurrentScale()` 获取正确的测量值。

## 测量元素尺寸

```tsx
import { useCurrentScale } from "remotion";
import { useRef, useEffect, useState } from "react";

export const MyComponent = () => {
  const ref = useRef<HTMLDivElement>(null);
  const scale = useCurrentScale();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    setDimensions({
      width: rect.width / scale,
      height: rect.height / scale,
    });
  }, [scale]);

  return <div ref={ref}>Content to measure</div>;
};
```