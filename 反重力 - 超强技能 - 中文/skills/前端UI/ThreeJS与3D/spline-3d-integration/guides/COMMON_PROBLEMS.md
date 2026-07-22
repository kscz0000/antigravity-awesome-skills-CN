# 常见问题与调试

这些是集成后才会浮现的真实问题。在完成任何 Spline 实现之前，请先阅读本文。

---

## 🚨 关键陷阱（会导致网站崩溃）

---

### 1. 滚动劫持 — 页面无法滚动

**现象：** 添加 Spline 后，整个页面停止滚动。用户被卡住。

**原因：** Spline 自动生成的 vanilla JS 导出代码默认在 `<body>` CSS 中注入 `overflow: hidden`。这已内嵌在它们的生成代码中。

**修复：**
```css
/* Add this to your CSS — overrides Spline's injection */
body {
  overflow: auto !important;
}
```

或者在播放设置中（Spline 编辑器 → Export → Play Settings），在生成 URL 之前**禁用"Page Scroll"**。这会从输出中移除 overflow 规则。

**还需检查：** 如果使用 Runtime API 并且嵌入了生成的 `index.html` 文件，请打开它们并手动从 `<style>` 块中移除 `overflow: hidden` 行。

---

### 2. 3D 场景背后的白色方块

**现象：** 你的深色/透明网站在 Spline 场景位置出现一个白色矩形。

**原因：** Spline 导出设置中默认将背景色设为白色。

**修复：**
1. 在 Spline 编辑器中 → Export → Play Settings → 打开 **Hide Background** 开关
2. 点击 **Generate Draft** 或 **Promote to Production** — URL 不会自动更新新设置
3. 复制新的 URL

对于 web 组件，你也可以通过内联方式覆盖：
```html
<spline-viewer url="..." background="transparent"></spline-viewer>
```

---

### 3. Spline 场景间歇性加载失败

**现象：** 页面有时加载正常，有时空白或损坏。感觉是随机的。

**原因：** `prod.spline.design` CDN 偶尔会出现延迟或丢弃请求。没有内置的重试或错误处理。

**修复 — 添加超时回退：**
```js
const TIMEOUT_MS = 8000;

const timeoutId = setTimeout(() => {
  // Spline didn't load in time — show fallback
  document.getElementById('spline-fallback').style.display = 'block';
  document.querySelector('.spline-wrapper').style.display = 'none';
}, TIMEOUT_MS);

// If using Runtime API, clear the timeout on successful load:
spline.load(sceneUrl).then(() => {
  clearTimeout(timeoutId);
});
```

**长期修复：** 下载 `.splinecode` 文件并自行托管在你自己的 CDN 上。这完全消除了第三方依赖，同时也能修复 CORS 问题。

---

### 4. 场景在 Mac 上正常，其他设备都卡顿

**现象：** 在 MacBook Pro 或 M 芯片 Mac 上非常流畅。在中端 Windows 笔记本或 Android 手机上完全损坏 — 卡顿、掉帧，有时甚至崩溃。

**原因：** Spline 使用 WebGL，运行在 GPU 上。Apple Silicon Mac 拥有出色的 GPU 性能。大多数 Windows 笔记本和 Android 设备没有独立 GPU。

**修复 — 加载前检测设备能力：**
```js
function shouldLoadSpline() {
  const isMobile = window.innerWidth < 768;
  const isLowEnd = navigator.hardwareConcurrency <= 2;

  // Optional: test WebGL support
  const canvas = document.createElement('canvas');
  const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
  const noWebGL = !gl;

  return !isMobile && !isLowEnd && !noWebGL;
}

if (shouldLoadSpline()) {
  loadSplineScene();
} else {
  showFallback();
}
```

---

### 5. 布局偏移 — 场景加载时页面跳动

**现象：** 用户看到页面布局后，当 3D 场景加载时所有内容发生偏移/跳动。

**原因：** canvas 在加载前没有预留高度，所以浏览器不知道要分配多少空间。HTML 渲染 → 空间折叠 → 场景加载 → 所有内容跳动。这会严重影响你的 CLS（累积布局偏移）Core Web Vitals 分数。

**修复 — 预分配空间：**
```css
spline-viewer, canvas.spline-canvas {
  display: block;
  width: 100%;
  height: 100vh; /* or whatever your target height is */
  contain: strict; /* tells browser to reserve this space */
}
```

对于 `position: fixed` 的背景来说这不太严重，但对于内联场景来说至关重要。

---

### 6. 旋转值是弧度，不是角度

**现象：** 你尝试将对象旋转到 90 度。它几乎没有移动或疯狂旋转。

**原因：** Spline 的运行时 API 使用**弧度**，不是角度。90 度 = `Math.PI / 2`。180 度 = `Math.PI`。

**修复：**
```js
// WRONG
obj.rotation.y = 90;

// CORRECT
obj.rotation.y = Math.PI / 2; // 90 degrees
obj.rotation.y = Math.PI;     // 180 degrees
obj.rotation.y = Math.PI * 2; // 360 degrees (full rotation)

// Helper function to use if you prefer degrees:
const toRad = (deg) => deg * (Math.PI / 180);
obj.rotation.y = toRad(90);
```

---

### 7. 3D 场景阻止按钮/链接的点击

**现象：** 与 Spline 场景重叠的按钮、CTA 或导航链接无法响应点击。

**原因：** Spline canvas 位于顶层并捕获所有指针事件。

**修复：** 如果场景是装饰性的（不需要交互），在 Spline 包装器上添加 `pointer-events: none`：
```css
.spline-wrapper {
  pointer-events: none; /* scene won't capture any clicks */
}
```

如果你既需要场景上的鼠标交互，又需要在上层有可点击的内容：
```css
.spline-wrapper {
  pointer-events: all; /* scene gets mouse events */
}

.content-overlay {
  position: relative;
  z-index: 10;
  pointer-events: all; /* content also gets mouse events */
}
```

注意：当两者都设置了 `pointer-events: all` 时，最顶层的元素（按 z-index）优先。确保你的内容 div 比 Spline 包装器有更高的 z-index。

---

### 8. Spline 水印可见（免费版）

**现象：** 角落出现一个小的"Built with Spline"标志。

**选项：**

**选项 A — 升级到 Spline 付费方案。** 然后在 Export → Play Settings → 打开"Hide Spline Logo"开关。

**选项 B — CSS 覆盖（免费版变通方案）：**
```css
/* Hides the watermark via CSS — targets the shadow DOM */
spline-viewer::part(logo) {
  display: none;
}

/* Fallback if the above doesn't work */
spline-viewer {
  --spline-viewer-logo-display: none;
}
```

注意：基于 CSS 的隐藏可能会因 Spline 更新而失效。付费方案是可靠的解决方案。

---

### 9. 加载场景时 CORS 错误

**现象：** 场景加载失败，控制台显示 CORS 错误。

**原因：** 浏览器安全策略在某些环境中阻止跨域请求（特别是某些配置下的 localhost 开发服务器）。

**修复 — 自行托管场景文件：**
1. 在 Spline 中 → Export → Code Export → 点击 URL 旁的下载图标
2. 下载 `.splinecode` 文件
3. 托管在你自己的服务器或 CDN 上（与你的网站同源）
4. 更新嵌入代码中的 URL 指向你托管的版本

---

### 10. Next.js 水合错误

**现象：** 在 Next.js 中包含 Spline 组件时出现 React 水合不匹配错误。

**原因：** Spline 仅在客户端渲染（需要浏览器的 WebGL），但 Next.js 也尝试在服务器端渲染。

**修复：**
```jsx
import dynamic from 'next/dynamic';

// ssr: false tells Next.js not to render this on the server
const Spline = dynamic(() => import('@splinetool/react-spline/next'), {
  ssr: false,
  loading: () => <div style={{ background: '#0a0a0a', height: '100vh' }} />
});
```

---

### 11. 场景 URL 未反映最新更改

**现象：** 你在 Spline 编辑器中更新了场景，但嵌入的仍然是旧版本。

**原因：** `prod.spline.design` URL 是一个快照。它**不会**在你修改后自动更新。

**修复：** 每次在 Spline 编辑器中做出更改后，你必须：
1. 转到 Export → Code Export
2. 点击 **"Promote to Production"**（或 "Generate Draft" 获取新的草稿 URL）
3. 现有的 prod URL 将提供更新后的场景 — 无需更改代码中的 URL

---

## 快速诊断表

| 症状 | 最可能原因 | 修复 |
|---|---|---|
| 页面无法滚动 | Spline 注入了 `overflow: hidden` | 添加 `body { overflow: auto !important }` 或在 Play Settings 中禁用 Page Scroll |
| 场景背后有白色方块 | 背景未隐藏 | Play Settings → Hide Background → 重新生成 URL |
| 有时加载，有时空白 | CDN 不稳定 | 添加超时回退；考虑自行托管 |
| Mac 流畅，其他设备卡顿 | GPU 性能差距 | 添加硬件检测，低端设备跳过 |
| 加载时页面跳动 | 未预留空间（CLS） | 在 canvas/viewer 元素上设置明确高度 |
| 旋转看起来不对 | 角度 vs 弧度 | 使用 `Math.PI / 180 * degrees` |
| 按钮不可点击 | Canvas 捕获了指针事件 | 在 Spline 包装器上添加 `pointer-events: none` |
| 水印可见 | 免费版 | 升级或使用 CSS 覆盖 |
| CORS 错误 | 跨域加载 | 自行托管 `.splinecode` 文件 |
| 水合错误（Next.js） | SSR 冲突 | 使用 `dynamic(() => import(...), { ssr: false })` |
| 仍然显示旧场景 | 未发布到生产环境 | 在 Spline 编辑器中点击"Promote to Production" |
