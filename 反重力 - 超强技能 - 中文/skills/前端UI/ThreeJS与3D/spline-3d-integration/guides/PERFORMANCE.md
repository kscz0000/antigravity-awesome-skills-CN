# 性能与移动端优化

Spline 场景基于 WebGL — 它们运行在 GPU 上。优化不佳的场景会严重拉低你的 PageSpeed 分数，在中端设备上卡顿，并消耗手机电量。把它们当作视频文件而非图片来对待。

---

## 在集成之前 — 检查场景大小

**在给出 URL 之前，先让用户检查场景文件大小。**

- 低于约 3MB = 通常没问题
- 3–10MB = 可用但尽可能优化
- 超过 10MB = 严重问题，需要优化或换方案
- 超过 20MB = 不要作为实时 3D 嵌入 — 改为导出视频

检查方法：在 Spline 编辑器中 → Export → Code Export → 生成 URL 前会显示文件大小。

**如果场景过大，告诉用户：**
1. 在 Export → Play Settings 中，将 **Geometry Quality** 设为"Performance"
2. 降低细分级别（1 通常足够，最多 2）
3. 删除隐藏或永远不可见的对象
4. 移除未使用的纹理和图片
5. 使用不超过 3 个灯光 — 反射效果优先使用 Matcap 材质（模拟反射而无 GPU 成本）
6. 合并使用相同材质的对象

---

## 优化清单（集成前）

在编写任何嵌入代码之前，请逐项检查：

- [ ] 场景文件大小低于 10MB
- [ ] Play Settings 中 Geometry Quality 设为"Performance"
- [ ] 如果网站有自己的背景色，背景已隐藏
- [ ] 已禁用：Page Scroll、Zoom、Pan（在 Play Settings 中），除非明确需要
- [ ] 页面上最多 1–2 个 Spline 嵌入（绝不超过 3 个）
- [ ] 场景中灯光少于 3 个
- [ ] 除非必要，不使用高分辨率纹理

---

## 加载策略

### 1. 预加载场景文件
添加到 `<head>` 以在脚本执行前开始获取：
```html
<link rel="preload" href="https://prod.spline.design/REPLACE_ME/scene.splinecode" as="fetch" crossorigin>
```

### 2. 加载时显示回退内容
绝不要让用户盯着空白区域。始终渲染一个背景色或静态图片作为占位符：

```css
.spline-wrapper {
  background: #0a0a0a; /* your site's bg color — shows instantly */
  width: 100%;
  height: 100vh;
}
```

### 3. 懒加载（React）
不要在需要之前加载 Spline：
```jsx
const Spline = lazy(() => import('@splinetool/react-spline'));
```

### 4. Intersection Observer（仅在可见时加载）
对于首屏下方的 Spline 场景：
```js
const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    loadSplineScene(); // only load when user scrolls to it
    observer.disconnect();
  }
});
observer.observe(document.getElementById('spline-section'));
```

---

## 移动端策略

Spline 场景是 GPU 密集型的。在移动设备上它们会：
- 快速消耗电量
- 在没有独立 GPU 的设备上卡顿
- 可能导致低端 Android 设备浏览器标签页崩溃

**务必实现以下策略之一：**

### 选项 A — 移动端完全跳过（推荐用于英雄区背景）
```js
if (window.innerWidth < 768) {
  // Don't load Spline — show static background instead
  document.querySelector('.spline-wrapper').style.background = 'url(fallback.jpg) center/cover';
}
```

### 选项 B — 硬件并发数检测
```js
// navigator.hardwareConcurrency = number of CPU cores
// Low core count = likely a low-end device
if (navigator.hardwareConcurrency <= 2 || window.innerWidth < 768) {
  // Skip Spline, use fallback
}
```

### 选项 C — 移动端导出为视频
对于装饰性/非交互场景：在 Spline 中将动画录制为 MP4，在移动端提供该视频。用户获得视觉效果，无 GPU 成本。

```js
const isMobile = window.innerWidth < 768;

if (isMobile) {
  // Show video
  document.getElementById('spline-video').style.display = 'block';
} else {
  // Load Spline
  loadSpline();
}
```

---

## Core Web Vitals（LCP / CLS）

Spline 场景几乎总是**最大内容绘制**元素，这意味着它们直接影响你的 Google 评分。

### 防止布局偏移（CLS）
canvas 在 HTML 之后加载，导致页面跳动。通过预分配空间来修复：

```css
canvas#canvas3d {
  width: 100%;
  height: 100vh;
  /* This tells the browser to reserve this space before the scene loads */
  contain: strict;
}
```

或者对于 web 组件：
```html
<spline-viewer
  url="..."
  style="width: 100%; height: 100vh; display: block;">
</spline-viewer>
```

### Lighthouse 说明
当 Spline 场景是主要的首屏元素时，Lighthouse 通常完全无法计算性能分数。这是 Lighthouse 的已知限制，不一定是网站问题。请改用 WebPageTest 或 Chrome DevTools 进行真实分析。

---

## 何时不使用实时 3D 嵌入

有时 Spline 嵌入是错误的工具。在以下情况下请改用视频或 GIF：

- 动画不响应用户输入（无鼠标跟踪、无点击）
- 场景文件超过 15MB
- 目标用户主要是移动端
- 你需要页面在 PageSpeed 上获得 80 分以上

**如何从 Spline 导出为视频：**
在 Spline 编辑器中 → Export → Video → 录制你的动画 → 用 HandBrake 压缩 → 托管在 GitHub 或 CDN 上 → 以 `<video autoplay loop muted playsinline>` 嵌入
