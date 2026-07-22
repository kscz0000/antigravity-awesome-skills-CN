---
name: progressive-web-app
description: "构建支持离线运行、可安装、具备缓存策略的渐进式 Web 应用（PWA）。当用户提到 PWA、service worker、web app manifest、Workbox、'添加到主屏幕'，或希望 Web 应用支持离线运行、体验接近原生、可安装时触发。"
risk: safe
source: community
date_added: "2026-03-17"
tags: [pwa, web-dev, service-worker, frontend, offline, caching]
tools: [gemini, cursor, claude]
---

# 渐进式 Web 应用（PWA）

## 概述

渐进式 Web 应用是一种利用现代浏览器能力的 Web 应用，即使在网络不可靠的情况下，也能提供快速、可靠、可安装的体验。它的三大核心支柱：

1. **HTTPS** — 生产环境必须使用 HTTPS，service worker 才能注册（开发时 localhost 除外）。
2. **Web App Manifest**（`manifest.json`）— 使应用可安装，并定义其在设备主屏幕上的外观。
3. **Service Worker**（`sw.js`）— 后台脚本，负责拦截网络请求、管理缓存、实现离线功能。

## 何时使用此技能

- 用户希望 Web 应用支持离线运行或在不稳定网络下可用。
- 构建移动优先的 Web 项目，用户需要将应用安装到主屏幕。
- 用户询问缓存策略、service worker，或如何提升 Web 应用的性能和韧性。
- 用户提到 Workbox、web app manifest、后台同步或 Web 推送通知。
- 用户问"我的网站能像 App 一样安装吗？"或"怎么让网站离线也能用？"——即使没用"PWA"这个词。

## 交付物清单

每个 PWA 实现至少需要包含以下文件：

- [ ] `index.html` — 引用 manifest，注册 service worker
- [ ] `manifest.json` — 完整的应用元数据和图标集
- [ ] `sw.js` — 包含 install、activate、fetch 处理器的 service worker
- [ ] `app.js` — 主应用逻辑，包含 SW 注册和安装提示处理
- [ ] `offline.html` — 离线导航失败时的回退页面（必需——缺失会导致安装失败）

---

## 第一步：Web App Manifest（`manifest.json`）

定义应用安装后的表现形式。必须在 `<head>` 中通过 `<link rel="manifest">` 引用。

```json
{
  "name": "My Awesome PWA",
  "short_name": "MyPWA",
  "description": "A fast, offline-capable Progressive Web App.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#ffffff",
  "theme_color": "#0055ff",
  "icons": [
    {
      "src": "/assets/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/assets/screenshots/desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    }
  ]
}
```

**关键字段：**
- `display`：`standalone` 隐藏浏览器 UI；`minimal-ui` 显示最小控件；`browser` 是标准标签页。
- `purpose: "maskable"` 使图标在 Android 上支持自适应图标（安全区域很重要——内容保持在中心 80% 以内）。
- `screenshots` 是可选的，但 Chrome 桌面端的增强安装对话框需要它。

---

## 第二步：HTML 外壳（`index.html`）

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Awesome PWA</title>

  <!-- PWA manifest -->
  <link rel="manifest" href="/manifest.json">

  <!-- Theme color for browser chrome -->
  <meta name="theme-color" content="#0055ff">

  <!-- iOS-specific (Safari doesn't fully use manifest) -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="MyPWA">
  <link rel="apple-touch-icon" href="/assets/icons/icon-192x192.png">

  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <div id="app">
    <header><h1>My PWA</h1></header>
    <main id="content">Loading...</main>
    <!-- Optional: install button, hidden by default -->
    <button id="install-btn" hidden>Install App</button>
  </div>
  <script src="/app.js"></script>
</body>
</html>
```

---

## 第三步：Service Worker 注册与安装提示（`app.js`）

```javascript
// ─── Service Worker Registration ───────────────────────────────────────────
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('[App] SW registered, scope:', registration.scope);
    } catch (err) {
      console.error('[App] SW registration failed:', err);
    }
  });
}

// ─── Install Prompt (Add to Home Screen) ───────────────────────────────────
let deferredPrompt;
const installBtn = document.getElementById('install-btn'); // may be null if omitted

// Capture the browser's install prompt — it fires before the browser's own UI
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault(); // Stop automatic mini-infobar on mobile
  deferredPrompt = e;
  if (installBtn) installBtn.hidden = false; // Show your custom install button
});

if (installBtn) {
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log('[App] Install outcome:', outcome);
    deferredPrompt = null;
    installBtn.hidden = true;
  });
}
// Fires when the app is installed (via browser or your button)
window.addEventListener('appinstalled', () => {
  console.log('[App] PWA installed successfully');
  installBtn.hidden = true;
});
```

---

## 第四步：Service Worker（`sw.js`）

### 缓存版本控制（关键——每次部署必须递增版本号）

```javascript
const CACHE_VERSION = 'v1';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;

// Files to pre-cache during install (the "App Shell")
const APP_SHELL = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/assets/icons/icon-192x192.png',
  '/offline.html', // Fallback page shown when network is unavailable
];
```

### Install — 预缓存 App Shell

```javascript
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      console.log('[SW] Pre-caching app shell');
      return cache.addAll(APP_SHELL);
    })
  );
  // Activate immediately without waiting for old SW to die
  self.skipWaiting();
});
```

### Activate — 清理旧缓存

```javascript
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== STATIC_CACHE && name !== DYNAMIC_CACHE)
          .map((name) => {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    })
  );
  // Take control of all pages immediately
  self.clients.claim();
});
```

### Fetch — 缓存策略

根据资源类型选择合适的策略：

```javascript
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle GET requests from our own origin
  if (request.method !== 'GET' || url.origin !== location.origin) return;

  // Strategy A: Cache-First (for static assets — fast, tolerates stale)
  if (url.pathname.match(/\.(css|js|png|jpg|svg|woff2)$/)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Strategy B: Network-First (for HTML pages — fresh, falls back to cache)
  if (request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Strategy C: Stale-While-Revalidate (for API data — fast and eventually fresh)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(staleWhileRevalidate(request));
    return;
  }
});

// ─── Strategy Implementations ──────────────────────────────────────────────

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    const cache = await caches.open(STATIC_CACHE);
    cache.put(request, response.clone());
    return response;
  } catch {
    // Nothing useful to fall back to for assets
    return new Response('Asset unavailable offline', { status: 503 });
  }
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(DYNAMIC_CACHE);
    cache.put(request, response.clone());
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || caches.match('/offline.html');
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cached = await cache.match(request);
  const fetchPromise = fetch(request).then((response) => {
    cache.put(request, response.clone());
    return response;
  });
  return cached || fetchPromise;
}
```

---

## 边界情况与平台说明

### iOS / Safari 特殊行为

- Safari 支持 manifest 和 service worker，但**不支持 `beforeinstallprompt`** — 用户必须手动通过"分享 → 添加到主屏幕"菜单安装。
- 使用 `apple-mobile-web-app-*` meta 标签（见上方 `index.html`）以确保 iOS 正确集成。
- Safari 可能在约 7 天不活跃后清除 service worker 缓存（智能防追踪机制）。

### HTTPS 要求

- Service worker 只能在 `https://` 源上注册。`http://localhost` 是开发环境的唯一例外。
- 如需在本地使用自定义域名的 HTTPS，可使用 `mkcert` 或 `ngrok` 等工具。

### 部署时的缓存失效

- 部署新资源时，必须递增 `sw.js` 中的 `CACHE_VERSION`。这确保 activate 清除旧缓存，用户获取最新文件。
- 常见做法是通过构建工具（如 Vite、Webpack）自动注入版本号。

### 不透明响应（跨域请求）

- 请求外部源（如 CDN 字体、第三方 API）会返回无法检查的"不透明"响应。缓存时需谨慎——失败的不透明响应仍会返回 `200` 状态码。
- 跨域资源优先使用 `staleWhileRevalidate` 策略，或使用 Workbox 等库来安全处理。

---

## Workbox（可选：生产环境快捷方案）

生产应用建议使用 [Workbox](https://developer.chrome.com/docs/workbox)（Google 的 PWA 库）代替手动实现策略。它能自动处理边界情况、缓存过期和版本控制。

```javascript
// With Workbox (via CDN for simplicity — use npm + bundler in production)
importScripts('https://storage.googleapis.com/workbox-cdn/releases/7.0.0/workbox-sw.js');

const { registerRoute } = workbox.routing;
const { CacheFirst, NetworkFirst, StaleWhileRevalidate } = workbox.strategies;
const { precacheAndRoute } = workbox.precaching;

precacheAndRoute(self.__WB_MANIFEST || []); // Injected by build plugin

registerRoute(({ request }) => request.destination === 'image', new CacheFirst());
registerRoute(({ request }) => request.mode === 'navigate', new NetworkFirst());
registerRoute(({ request }) => request.destination === 'script', new StaleWhileRevalidate());
```

---

## 发布前检查清单

- [ ] 站点通过 HTTPS 提供服务
- [ ] `manifest.json` 包含 `name`、`short_name`、`start_url`、`display`、`icons`（192 + 512）
- [ ] 图标设置了 `purpose: "any maskable"`
- [ ] `sw.js` 在 DevTools → Application → Service Workers 中注册无报错
- [ ] DevTools 中将网络节流为"Offline"时，App Shell 从缓存加载
- [ ] `offline.html` 回退页已缓存，离线导航失败时正确显示
- [ ] Lighthouse PWA 审计通过（Chrome DevTools → Lighthouse 面板）
- [ ] 在 iOS Safari（手动安装流程）和 Android Chrome（安装提示）上测试通过

## 限制

- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，应停下来请求澄清。
