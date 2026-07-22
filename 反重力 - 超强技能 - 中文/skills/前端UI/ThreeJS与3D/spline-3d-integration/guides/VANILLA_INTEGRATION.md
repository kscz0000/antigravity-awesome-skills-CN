# 原生 JS / HTML 集成

根据你需要的控制程度，有两种方法。

---

## 方法 A — Web 组件（推荐用于大多数场景）

无需 npm。只需添加到 HTML 即可。支持懒加载、透明背景和鼠标交互。

```html
<!-- In <head> — loads the web component -->
<script type="module" src="https://unpkg.com/@splinetool/viewer/build/spline-viewer.js"></script>

<!-- Basic embed -->
<spline-viewer url="https://prod.spline.design/REPLACE_ME/scene.splinecode"></spline-viewer>

<!-- With mouse-following interactivity (e.g. cursor-tracking robots) -->
<spline-viewer
  url="https://prod.spline.design/REPLACE_ME/scene.splinecode"
  events-target="global">
</spline-viewer>

<!-- Transparent background -->
<spline-viewer
  url="https://prod.spline.design/REPLACE_ME/scene.splinecode"
  background="transparent">
</spline-viewer>
```

---

## 方法 B — Runtime API（需要编程控制时使用）

当你需要操作对象、触发动画或从自己的 JS 响应事件时使用。

安装：
```bash
npm install @splinetool/runtime
```

或通过 CDN（无需安装）：
```html
<script type="module">
  import { Application } from 'https://unpkg.com/@splinetool/runtime@latest/build/runtime.module.js';
  // ... rest of your code
</script>
```

基础用法：
```js
import { Application } from '@splinetool/runtime';

const canvas = document.getElementById('canvas3d');
const spline = new Application(canvas);

spline.load('https://prod.spline.design/REPLACE_ME/scene.splinecode').then(() => {
  console.log('Scene loaded');
});
```

带对象交互：
```js
spline.load(sceneUrl).then(() => {
  const obj = spline.findObjectByName('Cube');
  // or by ID: spline.findObjectById('uuid-here')

  obj.position.x += 50;
  obj.rotation.y += Math.PI / 4; // NOTE: radians, NOT degrees
  obj.scale.x = 2;
});
```

带事件监听器：
```js
spline.load(sceneUrl).then(() => {
  spline.addEventListener('mouseDown', (e) => {
    console.log('Clicked:', e.target.name);
  });
});
```

以编程方式触发动画：
```js
spline.load(sceneUrl).then(() => {
  const obj = spline.findObjectByName('MyObject');
  obj.emitEvent('mouseHover');       // forward
  obj.emitEventReverse('mouseHover'); // reverse
});
```

---

## 全屏背景设置

最常见的用例 — Spline 场景作为所有内容的背景。

```html
<!DOCTYPE html>
<html>
<head>
  <script type="module" src="https://unpkg.com/@splinetool/viewer/build/spline-viewer.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      /* DO NOT add overflow: hidden here — it will break page scroll */
      position: relative;
    }

    .spline-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      /* pointer-events: none — use this if scene is decorative only */
      /* pointer-events: all — use this if you want mouse interaction */
      pointer-events: all;
    }

    .content {
      position: relative;
      z-index: 1;
      /* Make sure content elements don't get blocked by the 3D scene */
    }

    /* Fallback shown while Spline loads or if it fails */
    .spline-fallback {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      z-index: 0;
      background: #0a0a0a; /* match your site's base color */
      display: none; /* hidden by default, shown via JS if needed */
    }
  </style>
</head>
<body>
  <!-- Fallback (shown if Spline fails to load) -->
  <div class="spline-fallback" id="spline-fallback"></div>

  <!-- Spline background -->
  <div class="spline-bg">
    <spline-viewer
      url="https://prod.spline.design/REPLACE_ME/scene.splinecode"
      events-target="global"
      style="width:100%; height:100%;">
    </spline-viewer>
  </div>

  <!-- Your website content -->
  <div class="content">
    <h1>Your Content Here</h1>
  </div>

  <script>
    // Show fallback if Spline hasn't loaded after 8 seconds
    setTimeout(() => {
      const viewer = document.querySelector('spline-viewer');
      if (!viewer || !viewer.shadowRoot) {
        document.getElementById('spline-fallback').style.display = 'block';
      }
    }, 8000);

    // Skip Spline entirely on low-end mobile to save battery + performance
    if (window.innerWidth < 768 || navigator.hardwareConcurrency <= 2) {
      document.querySelector('.spline-bg').style.display = 'none';
      document.getElementById('spline-fallback').style.display = 'block';
    }
  </script>
</body>
</html>
```

---

## 可用事件类型

| 事件 | 使用场景 |
|---|---|
| `mouseDown` | 点击/触摸对象 |
| `mouseUp` | 点击后释放 |
| `mouseHover` | 光标进入对象区域 |
| `mousePress` | 持续按住点击 |
| `keyDown` | 按键按下 |
| `keyUp` | 按键释放 |
| `start` | 场景已加载并启动 |
| `scroll` | 页面滚动 |

---

## 预加载（减少感知加载时间）

添加到 `<head>` 以在脚本运行前开始获取场景文件：

```html
<link rel="preload" href="https://prod.spline.design/REPLACE_ME/scene.splinecode" as="fetch" crossorigin>
```

完整优化策略请参阅 [PERFORMANCE.md](PERFORMANCE.md)。
调试问题请参阅 [COMMON_PROBLEMS.md](COMMON_PROBLEMS.md)。
