---
title: 条件模块加载
impact: HIGH
impactDescription: 仅在需要时加载大型数据
tags: bundle, conditional-loading, lazy-loading
---

## 条件模块加载

仅在功能被激活时才加载大型数据或模块。

**示例（懒加载动画帧）：**

```tsx
function AnimationPlayer({ enabled }: { enabled: boolean }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

`typeof window !== 'undefined'` 检查可防止在 SSR 中打包此模块，从而优化服务器包大小和构建速度。
