# React / Next.js / Vue 集成

---

## React / Vite

安装：
```bash
npm install @splinetool/react-spline
```

基础用法：
```jsx
import Spline from '@splinetool/react-spline';

export default function App() {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Spline scene="https://prod.spline.design/REPLACE_ME/scene.splinecode" />
    </div>
  );
}
```

带对象交互和事件监听器：
```jsx
import { useRef } from 'react';
import Spline from '@splinetool/react-spline';

export default function App() {
  const splineRef = useRef();

  function onLoad(splineApp) {
    splineRef.current = splineApp;
  }

  function triggerAnimation() {
    splineRef.current.emitEvent('mouseHover', 'Cube');
  }

  function onSplineEvent(e) {
    console.log('Object interacted:', e.target.name);
  }

  return (
    <div>
      <Spline
        scene="https://prod.spline.design/REPLACE_ME/scene.splinecode"
        onLoad={onLoad}
        onMouseDown={onSplineEvent}
      />
      <button onClick={triggerAnimation}>Trigger</button>
    </div>
  );
}
```

**懒加载（推荐用于性能优化）：**
```jsx
import { lazy, Suspense } from 'react';

const Spline = lazy(() => import('@splinetool/react-spline'));

export default function Hero() {
  return (
    <Suspense fallback={<div style={{ background: '#0a0a0a', width: '100%', height: '100vh' }} />}>
      <Spline scene="https://prod.spline.design/REPLACE_ME/scene.splinecode" />
    </Suspense>
  );
}
```

---

## Next.js

安装：
```bash
npm install @splinetool/react-spline
```

**使用 `/next` 导入**以支持 SSR 和自动模糊占位符：
```jsx
import Spline from '@splinetool/react-spline/next';

export default function Page() {
  return (
    <Spline scene="https://prod.spline.design/REPLACE_ME/scene.splinecode" />
  );
}
```

**使用动态导入（如果遇到水合错误）：**
```jsx
import dynamic from 'next/dynamic';

const Spline = dynamic(() => import('@splinetool/react-spline/next'), {
  ssr: false,
  loading: () => <div style={{ background: '#0a0a0a', width: '100%', height: '100vh' }} />
});

export default function Page() {
  return <Spline scene="https://prod.spline.design/REPLACE_ME/scene.splinecode" />;
}
```

---

## Vue

安装：
```bash
npm install @splinetool/vue-spline
```

```vue
<template>
  <Spline
    scene="https://prod.spline.design/REPLACE_ME/scene.splinecode"
    @spline-loaded="onLoaded"
    @mouseDown="onClick"
  />
</template>

<script>
import Spline from '@splinetool/vue-spline';

export default {
  components: { Spline },
  methods: {
    onLoaded(spline) {
      const obj = spline.findObjectByName('Cube');
      obj.position.x += 10; // NOTE: radians for rotation, not degrees
    },
    onClick(e) {
      console.log('Clicked:', e.target.name);
    }
  }
}
</script>
```

---

## 全屏背景（React）

```jsx
import Spline from '@splinetool/react-spline';
import { useState } from 'react';

export default function HeroSection() {
  const [loaded, setLoaded] = useState(false);

  // Skip Spline on mobile / low-end devices
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
  const isLowEnd = typeof navigator !== 'undefined' && navigator.hardwareConcurrency <= 2;

  return (
    <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>

      {/* Fallback background — always rendered, hidden once Spline loads */}
      <div style={{
        position: 'absolute', inset: 0,
        background: '#0a0a0a',
        zIndex: 0,
        opacity: loaded ? 0 : 1,
        transition: 'opacity 0.5s ease'
      }} />

      {/* Spline scene — only load on capable devices */}
      {!isMobile && !isLowEnd && (
        <Spline
          scene="https://prod.spline.design/REPLACE_ME/scene.splinecode"
          onLoad={() => setLoaded(true)}
          style={{
            position: 'absolute',
            top: 0, left: 0,
            width: '100%', height: '100%',
            zIndex: 0
          }}
        />
      )}

      {/* Content sits on top */}
      <div style={{ position: 'relative', zIndex: 1 }}>
        <h1>Your Content Here</h1>
      </div>

    </div>
  );
}
```

---

## React 属性参考

| 属性 | 类型 | 说明 |
|---|---|---|
| `scene` | string | 场景 URL（必填） |
| `onLoad` | function | 加载完成时传入 splineApp |
| `onMouseDown` | function | 鼠标/触摸按下对象 |
| `onMouseUp` | function | 鼠标/触摸释放 |
| `onMouseHover` | function | 悬停在对象上 |
| `onKeyDown` | function | 按键按下 |
| `onKeyUp` | function | 按键释放 |
| `onStart` | function | 场景已启动 |
| `onScroll` | function | 滚动事件 |
| `style` | object | canvas 的 CSS 样式 |
| `className` | string | CSS 类名 |

完成前请参阅 [PERFORMANCE.md](PERFORMANCE.md) 和 [COMMON_PROBLEMS.md](COMMON_PROBLEMS.md)。
