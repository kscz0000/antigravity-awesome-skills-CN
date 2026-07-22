---
name: electron-development
description: "掌握 Electron 桌面应用开发，涵盖安全 IPC、contextIsolation、preload 脚本、多进程架构、electron-builder 打包、代码签名和自动更新。"
risk: safe
source: community
date_added: "2026-03-12"
---

# Electron 开发

你是一名资深 Electron 工程师，专注于安全、生产级桌面应用架构。你在 Electron 多进程模型、IPC 安全模式、原生 OS 集成、应用打包、代码签名和自动更新策略方面拥有深厚专业知识。

## 使用此技能的场景

- 从零构建新的 Electron 桌面应用
- 加固 Electron 应用安全（contextIsolation、sandbox、CSP、nodeIntegration）
- 设置 main、renderer 和 preload 进程之间的 IPC 通信
- 使用 electron-builder 或 electron-forge 打包和分发 Electron 应用
- 使用 electron-updater 实现自动更新
- 调试主进程问题或渲染进程崩溃
- 管理多窗口和应用生命周期
- 集成原生 OS 功能（菜单、托盘、通知、文件系统对话框）
- 优化 Electron 应用性能和包体积

## 不使用此技能的场景

- 构建仅 Web 应用，无需桌面分发 → 使用 `react-patterns`、`nextjs-best-practices`
- 构建 Tauri 应用（基于 Rust 的桌面替代方案）→ 如可用则使用 `tauri-development`
- 构建 Chrome 扩展 → 使用 `chrome-extension-developer`
- 实现深度后端/服务器逻辑 → 使用 `nodejs-backend-patterns`
- 构建移动应用 → 使用 `react-native-architecture` 或 `flutter-expert`

## 指南

1. 分析项目结构，识别进程边界。
2. 强制执行安全默认值：`contextIsolation: true`、`nodeIntegration: false`、`sandbox: true`。
3. 在 preload 脚本中使用显式白名单设计 IPC 通道。
4. 使用适当工具实现、测试和构建。
5. 发布前根据生产安全检查清单进行验证。

---

## 核心专业领域

### 1. 项目结构与架构

**推荐的项目布局：**
```
my-electron-app/
├── package.json
├── electron-builder.yml        # 或 forge.config.ts
├── src/
│   ├── main/
│   │   ├── main.ts             # 主进程入口
│   │   ├── ipc-handlers.ts     # IPC 通道处理器
│   │   ├── menu.ts             # 应用菜单
│   │   ├── tray.ts             # 系统托盘
│   │   └── updater.ts          # 自动更新逻辑
│   ├── preload/
│   │   └── preload.ts          # main ↔ renderer 之间的桥接
│   ├── renderer/
│   │   ├── index.html          # 入口 HTML
│   │   ├── App.tsx             # UI 根组件（React/Vue/Svelte/原生）
│   │   ├── components/
│   │   └── styles/
│   └── shared/
│       ├── constants.ts        # IPC 通道名称、共享枚举
│       └── types.ts            # 共享 TypeScript 接口
├── resources/
│   ├── icon.png                # 应用图标（1024x1024）
│   └── entitlements.mac.plist  # macOS 权限配置
├── tests/
│   ├── unit/
│   └── e2e/
└── tsconfig.json
```

**关键架构原则：**
- **分离入口点**：main、preload 和 renderer 各自有独立的构建配置。
- **共享类型，而非共享模块**：`shared/` 目录仅包含类型、常量和枚举 — 绝不包含跨进程边界导入的可执行代码。
- **保持主进程精简**：main 进程应负责编排窗口、处理 IPC 和管理应用生命周期。业务逻辑应放在 renderer 或专用 worker 进程中。

---

### 2. 进程模型（Main / Renderer / Preload / Utility）

Electron 运行**多个进程**，这些进程在设计上是隔离的：

| 进程 | 角色 | Node.js 访问 | DOM 访问 |
|---------|------|----------------|------------|
| **Main** | 应用生命周期、窗口、原生 API、IPC 枢纽 | ✅ 完全 | ❌ 无 |
| **Renderer** | UI 渲染、用户交互 | ❌ 无（默认） | ✅ 完全 |
| **Preload** | main 和 renderer 之间的安全桥接 | ✅ 有限（通过 contextBridge） | ✅ 页面加载前 |
| **Utility** | CPU 密集型任务、后台工作 | ✅ 完全 | ❌ 无 |

**带安全默认值的 BrowserWindow（强制）：**
```typescript
import { BrowserWindow } from 'electron';
import path from 'node:path';

function createMainWindow(): BrowserWindow {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      // ── 安全默认值（切勿修改）──
      contextIsolation: true,     // 隔离 preload 与 renderer 上下文
      nodeIntegration: false,     // 阻止 renderer 中使用 require()
      sandbox: true,              // 操作系统级进程沙箱
      
      // ── PRELOAD 脚本 ──
      preload: path.join(__dirname, '../preload/preload.js'),
      
      // ── 额外加固 ──
      webSecurity: true,          // 强制同源策略
      allowRunningInsecureContent: false,
      experimentalFeatures: false,
    },
  });

  // 内容安全策略
  win.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:;"
        ],
      },
    });
  });

  return win;
}
```

> ⚠️ **关键**：生产环境中绝不要设置 `nodeIntegration: true` 或 `contextIsolation: false`。这些设置会通过 XSS 漏洞使 renderer 暴露于远程代码执行（RCE）攻击。

---

### 3. 安全 IPC 通信

IPC 是 main 和 renderer 进程之间通信的**唯一**安全通道。所有 IPC 必须通过 preload 脚本传递。

**Preload 脚本（contextBridge + 显式白名单）：**
```typescript
// src/preload/preload.ts
import { contextBridge, ipcRenderer } from 'electron';

// ── 白名单：仅暴露特定通道 ──
const ALLOWED_SEND_CHANNELS = [
  'file:save',
  'file:open',
  'app:get-version',
  'dialog:show-open',
] as const;

const ALLOWED_RECEIVE_CHANNELS = [
  'file:saved',
  'file:opened',
  'app:version',
  'update:available',
  'update:progress',
  'update:downloaded',
  'update:error',
] as const;

type SendChannel = typeof ALLOWED_SEND_CHANNELS[number];
type ReceiveChannel = typeof ALLOWED_RECEIVE_CHANNELS[number];

contextBridge.exposeInMainWorld('electronAPI', {
  // 单向：renderer → main
  send: (channel: SendChannel, ...args: unknown[]) => {
    if (ALLOWED_SEND_CHANNELS.includes(channel)) {
      ipcRenderer.send(channel, ...args);
    }
  },

  // 双向：renderer → main → renderer（请求/响应）
  invoke: (channel: SendChannel, ...args: unknown[]) => {
    if (ALLOWED_SEND_CHANNELS.includes(channel)) {
      return ipcRenderer.invoke(channel, ...args);
    }
    return Promise.reject(new Error(`通道 "${channel}" 不被允许`));
  },

  // 单向：main → renderer（订阅）
  on: (channel: ReceiveChannel, callback: (...args: unknown[]) => void) => {
    if (ALLOWED_RECEIVE_CHANNELS.includes(channel)) {
      const listener = (_event: Electron.IpcRendererEvent, ...args: unknown[]) => callback(...args);
      ipcRenderer.on(channel, listener);
      return () => ipcRenderer.removeListener(channel, listener);
    }
    return () => {};
  },
});
```

**主进程 IPC 处理器：**
```typescript
// src/main/ipc-handlers.ts
import { ipcMain, dialog, BrowserWindow } from 'electron';
import { readFile, writeFile } from 'node:fs/promises';

export function registerIpcHandlers(): void {
  // invoke() 模式：向 renderer 返回值
  ipcMain.handle('file:open', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [{ name: '文本文件', extensions: ['txt', 'md'] }],
    });
    
    if (canceled || filePaths.length === 0) return null;
    
    const content = await readFile(filePaths[0], 'utf-8');
    return { path: filePaths[0], content };
  });

  ipcMain.handle('file:save', async (_event, filePath: string, content: string) => {
    // 验证输入 — 绝不盲目信任 renderer 数据
    if (typeof filePath !== 'string' || typeof content !== 'string') {
      throw new Error('参数无效');
    }
    await writeFile(filePath, content, 'utf-8');
    return { success: true };
  });

  ipcMain.handle('app:get-version', () => {
    return process.versions.electron;
  });
}
```

**Renderer 使用（类型安全）：**
```typescript
// src/renderer/App.tsx — 或任何 renderer 代码
// electronAPI 通过 contextBridge 全局可用

declare global {
  interface Window {
    electronAPI: {
      send: (channel: string, ...args: unknown[]) => void;
      invoke: (channel: string, ...args: unknown[]) => Promise<unknown>;
      on: (channel: string, callback: (...args: unknown[]) => void) => () => void;
    };
  }
}

// 通过 IPC 打开文件
async function openFile() {
  const result = await window.electronAPI.invoke('file:open');
  if (result) {
    console.log('文件内容:', result.content);
  }
}

// 订阅来自主进程的更新
const unsubscribe = window.electronAPI.on('update:available', (version) => {
  console.log('有可用更新:', version);
});

// 卸载时清理
// unsubscribe();
```

**IPC 模式总结：**

| 模式 | 方法 | 用例 |
|---------|--------|----------|
| **即发即弃** | `ipcRenderer.send()` → `ipcMain.on()` | 日志、遥测、非关键通知 |
| **请求/响应** | `ipcRenderer.invoke()` → `ipcMain.handle()` | 文件操作、对话框、数据查询 |
| **推送到 renderer** | `webContents.send()` → `ipcRenderer.on()` | 进度更新、下载状态、自动更新 |

> ⚠️ 生产环境中**绝不要**使用 `ipcRenderer.sendSync()` — 它会阻塞 renderer 的事件循环并冻结 UI。

---

### 4. 安全加固

#### 生产安全检查清单

```
── 强制项 ──
[ ] contextIsolation: true
[ ] nodeIntegration: false
[ ] sandbox: true
[ ] webSecurity: true
[ ] allowRunningInsecureContent: false

── IPC ──
[ ] Preload 使用 contextBridge 并带显式通道白名单
[ ] 所有 IPC 输入在主进程中验证
[ ] 未向 renderer 上下文暴露原始 ipcRenderer
[ ] 未使用 ipcRenderer.sendSync()

── 内容 ──
[ ] 所有窗口设置了内容安全策略（CSP）头
[ ] 未使用 eval()、new Function() 或带不可信数据的 innerHTML
[ ] 远程内容（如有）在权限受限的独立 BrowserView 中加载
[ ] protocol.registerSchemesAsPrivileged() 使用最小权限

── 导航 ──
[ ] webContents 'will-navigate' 事件被拦截 — 阻止意外 URL
[ ] webContents 'new-window' 事件被拦截 — 防止弹窗利用
[ ] 未对未净化的 URL 使用 shell.openExternal()

── 打包 ──
[ ] ASAR 归档已启用（防止源码被随意查看）
[ ] 应用中未打包敏感凭证或 API 密钥
[ ] Windows 和 macOS 均已配置代码签名
[ ] 自动更新使用 HTTPS 并验证签名
```

**防止导航劫持：**
```typescript
// 在主进程中，创建 BrowserWindow 后
win.webContents.on('will-navigate', (event, url) => {
  const parsedUrl = new URL(url);
  // 仅允许应用内导航
  if (parsedUrl.origin !== 'http://localhost:5173') { // 开发服务器
    event.preventDefault();
    console.warn(`已阻止导航至: ${url}`);
  }
});

// 阻止打开新窗口
win.webContents.setWindowOpenHandler(({ url }) => {
  try {
    const externalUrl = new URL(url);
    const allowedHosts = new Set(['example.com', 'docs.example.com']);

    // 绝不将 renderer 控制的原始 URL 转发给操作系统。
    // 未验证的链接可能导致钓鱼或滥用平台 URL 处理程序。
    if (externalUrl.protocol === 'https:' && allowedHosts.has(externalUrl.hostname)) {
      require('electron').shell.openExternal(externalUrl.toString());
    } else {
      console.warn(`已阻止外部 URL: ${url}`);
    }
  } catch {
    console.warn(`拒绝无效外部 URL: ${url}`);
  }

  return { action: 'deny' }; // 阻止所有新的 Electron 窗口
});
```

**自定义协议注册（安全）：**
```typescript
import { protocol } from 'electron';
import path from 'node:path';
import { readFile } from 'node:fs/promises';
import { URL } from 'node:url';

// 注册自定义协议以安全加载本地资源
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true } },
]);

app.whenReady().then(() => {
  protocol.handle('app', async (request) => {
    const url = new URL(request.url);
    const baseDir = path.resolve(__dirname, '../renderer');
    // 去除前导斜杠，使 path.resolve 保持 baseDir 作为根目录。
    const relativePath = path.normalize(decodeURIComponent(url.pathname).replace(/^[/\\]+/, ''));
    const filePath = path.resolve(baseDir, relativePath);

    if (!filePath.startsWith(baseDir)) {
      return new Response('禁止访问', { status: 403 });
    }

    const data = await readFile(filePath);
    return new Response(data);
  });
});
```

---

### 5. 跨进程状态管理

**策略 1：主进程作为唯一数据源（推荐大多数应用使用）**
```typescript
// src/main/store.ts
import { app } from 'electron';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

interface AppState {
  theme: 'light' | 'dark';
  recentFiles: string[];
  windowBounds: { x: number; y: number; width: number; height: number };
}

const DEFAULTS: AppState = {
  theme: 'light',
  recentFiles: [],
  windowBounds: { x: 0, y: 0, width: 1200, height: 800 },
};

class Store {
  private data: AppState;
  private filePath: string;

  constructor() {
    this.filePath = path.join(app.getPath('userData'), 'settings.json');
    this.data = this.load();
  }

  private load(): AppState {
    try {
      const raw = readFileSync(this.filePath, 'utf-8');
      return { ...DEFAULTS, ...JSON.parse(raw) };
    } catch {
      return { ...DEFAULTS };
    }
  }

  get<K extends keyof AppState>(key: K): AppState[K] {
    return this.data[key];
  }

  set<K extends keyof AppState>(key: K, value: AppState[K]): void {
    this.data[key] = value;
    writeFileSync(this.filePath, JSON.stringify(this.data, null, 2));
  }
}

export const store = new Store();
```

**策略 2：electron-store（轻量级持久存储）**
```typescript
import Store from 'electron-store';

const store = new Store({
  schema: {
    theme: { type: 'string', enum: ['light', 'dark'], default: 'light' },
    windowBounds: {
      type: 'object',
      properties: {
        width: { type: 'number', default: 1200 },
        height: { type: 'number', default: 800 },
      },
    },
  },
});

// 使用
store.set('theme', 'dark');
console.log(store.get('theme')); // 'dark'
```

**多窗口状态同步：**
```typescript
// 主进程：向所有窗口广播状态变更
import { BrowserWindow } from 'electron';

function broadcastToAllWindows(channel: string, data: unknown): void {
  for (const win of BrowserWindow.getAllWindows()) {
    if (!win.isDestroyed()) {
      win.webContents.send(channel, data);
    }
  }
}

// 当主题变更时：
ipcMain.handle('settings:set-theme', (_event, theme: 'light' | 'dark') => {
  store.set('theme', theme);
  broadcastToAllWindows('settings:theme-changed', theme);
});
```

---

### 6. 构建、签名与分发

#### electron-builder 配置

```yaml
# electron-builder.yml
appId: com.mycompany.myapp
productName: My App
directories:
  output: dist
  buildResources: resources

files:
  - "out/**/*"       # 编译后的 main + preload
  - "renderer/**/*"  # 构建后的 renderer 资源
  - "package.json"

asar: true
compression: maximum

# ── macOS ──
mac:
  category: public.app-category.developer-tools
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: resources/entitlements.mac.plist
  entitlementsInherit: resources/entitlements.mac.plist
  target:
    - target: dmg
      arch: [x64, arm64]
    - target: zip
      arch: [x64, arm64]

# ── Windows ──
win:
  target:
    - target: nsis
      arch: [x64, arm64]
  signingHashAlgorithms: [sha256]

nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
  perMachine: false

# ── Linux ──
linux:
  target:
    - target: AppImage
    - target: deb
  category: Development
  maintainer: your-email@example.com

# ── 自动更新 ──
publish:
  provider: github
  owner: your-org
  repo: your-repo
```

#### 代码签名

```bash
# macOS：需要 Apple 开发者证书
# 构建前设置环境变量：
export CSC_LINK="path/to/Developer_ID_Application.p12"
export CSC_KEY_PASSWORD="your-password"

# Windows：需要 EV 或标准代码签名证书
# 设置环境变量：
export WIN_CSC_LINK="path/to/code-signing.pfx"
export WIN_CSC_KEY_PASSWORD="your-password"

# 构建签名应用
npx electron-builder --mac --win --publish never
```

#### 使用 electron-updater 自动更新

```typescript
// src/main/updater.ts
import { autoUpdater } from 'electron-updater';
import { BrowserWindow } from 'electron';
import log from 'electron-log';

export function setupAutoUpdater(mainWindow: BrowserWindow): void {
  autoUpdater.logger = log;
  autoUpdater.autoDownload = false; // 让用户决定
  autoUpdater.autoInstallOnAppQuit = true;

  autoUpdater.on('update-available', (info) => {
    mainWindow.webContents.send('update:available', {
      version: info.version,
      releaseNotes: info.releaseNotes,
    });
  });

  autoUpdater.on('download-progress', (progress) => {
    mainWindow.webContents.send('update:progress', {
      percent: Math.round(progress.percent),
      bytesPerSecond: progress.bytesPerSecond,
    });
  });

  autoUpdater.on('update-downloaded', () => {
    mainWindow.webContents.send('update:downloaded');
  });

  autoUpdater.on('error', (err) => {
    log.error('更新错误:', err);
    mainWindow.webContents.send('update:error', err.message);
  });

  // 每 4 小时检查一次更新
  setInterval(() => autoUpdater.checkForUpdates(), 4 * 60 * 60 * 1000);
  autoUpdater.checkForUpdates();
}

// 通过 IPC 暴露给 renderer
ipcMain.handle('update:download', () => autoUpdater.downloadUpdate());
ipcMain.handle('update:install', () => autoUpdater.quitAndInstall());
```

#### 包体积优化

- ✅ 使用 `asar: true` 将源码打包为单个归档文件
- ✅ 在 electron-builder 配置中设置 `compression: maximum`
- ✅ 排除开发依赖：`"files"` 模式应仅包含编译输出
- ✅ 使用打包工具（Vite、webpack、esbuild）对 renderer 进行 tree-shaking
- ✅ 审计随应用分发的 `node_modules` — 使用 `electron-builder` 的 `files` 排除模式
- ✅ 考虑使用 `@electron/rebuild` 处理原生模块，而非为所有平台预构建
- ❌ 不要打包整个 `node_modules` — 仅打包生产依赖

---

### 7. 开发体验与调试

#### 带热重载的开发环境

```json
// package.json scripts
{
  "scripts": {
    "dev": "concurrently \"npm run dev:renderer\" \"npm run dev:main\"",
    "dev:renderer": "vite",
    "dev:main": "electron-vite dev",
    "build": "electron-vite build",
    "start": "electron ."
  }
}
```

**推荐工具链：**
- **electron-vite** 或 **electron-forge with Vite plugin** — 现代化、快速的 renderer HMR
- **tsx** 或 **ts-node** — 开发时在主进程中运行 TypeScript
- **concurrently** — 同时运行 renderer 开发服务器和 Electron

#### 调试主进程

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "调试主进程",
      "type": "node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "${workspaceFolder}/node_modules/.bin/electron",
      "args": [".", "--remote-debugging-port=9223"],
      "sourceMaps": true,
      "outFiles": ["${workspaceFolder}/out/**/*.js"],
      "env": {
        "NODE_ENV": "development"
      }
    }
  ]
}
```

**其他调试技巧：**
```typescript
// 仅在开发环境启用 DevTools
if (process.env.NODE_ENV === 'development') {
  win.webContents.openDevTools({ mode: 'detach' });
}

// 从命令行检查特定 renderer 进程：
// electron . --inspect=5858 --remote-debugging-port=9223
```

#### 测试策略

**单元测试（Vitest / Jest）：**
```typescript
// tests/unit/store.test.ts
import { describe, it, expect, vi } from 'vitest';

// 为单元测试模拟 Electron 模块
vi.mock('electron', () => ({
  app: { getPath: () => '/tmp/test' },
}));

describe('Store', () => {
  it('对缺失的键返回默认值', () => {
    // 在无 Electron 运行时测试 store 逻辑
  });
});
```

**E2E 测试（Playwright + Electron）：**
```typescript
// tests/e2e/app.spec.ts
import { test, expect, _electron as electron } from '@playwright/test';

test('应用启动并显示主窗口', async () => {
  const app = await electron.launch({ args: ['.'] });
  const window = await app.firstWindow();

  // 等待应用完全加载
  await window.waitForLoadState('domcontentloaded');

  const title = await window.title();
  expect(title).toBe('My App');

  // 截图用于视觉回归
  await window.screenshot({ path: 'tests/screenshots/main-window.png' });

  await app.close();
});

test('通过 IPC 的文件打开对话框正常工作', async () => {
  const app = await electron.launch({ args: ['.'] });
  const window = await app.firstWindow();

  // 在 renderer 上下文中通过 evaluate 测试 IPC
  const version = await window.evaluate(async () => {
    return window.electronAPI.invoke('app:get-version');
  });

  expect(version).toBeTruthy();
  await app.close();
});
```

**Electron 的 Playwright 配置：**
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  retries: 1,
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

---

## 应用生命周期管理

```typescript
// src/main/main.ts
import { app, BrowserWindow } from 'electron';
import { registerIpcHandlers } from './ipc-handlers';
import { setupAutoUpdater } from './updater';
import { store } from './store';

let mainWindow: BrowserWindow | null = null;

app.whenReady().then(() => {
  registerIpcHandlers();
  mainWindow = createMainWindow();

  // 恢复窗口边界
  const bounds = store.get('windowBounds');
  if (bounds) mainWindow.setBounds(bounds);

  // 关闭时保存窗口边界
  mainWindow.on('close', () => {
    if (mainWindow) store.set('windowBounds', mainWindow.getBounds());
  });

  // 自动更新（仅生产环境）
  if (app.isPackaged) {
    setupAutoUpdater(mainWindow);
  }

  // macOS：点击 dock 图标时重新创建窗口
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      mainWindow = createMainWindow();
    }
  });
});

// 所有窗口关闭时退出（macOS 除外）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// 安全：阻止创建额外的 renderer
app.on('web-contents-created', (_event, contents) => {
  contents.on('will-attach-webview', (event) => {
    event.preventDefault(); // 阻止 <webview> 标签
  });
});
```

---

## 常见问题诊断

### 启动时白屏
**症状**：应用启动但 renderer 显示空白/白色页面
**根本原因**：`loadFile`/`loadURL` 路径不正确、构建输出缺失、CSP 阻止脚本
**解决方案**：验证传递给 `win.loadFile()` 或 `win.loadURL()` 的路径相对于打包应用是否存在。检查 DevTools 控制台的 CSP 违规。开发时，确保 Vite/webpack 开发服务器在 Electron 启动前运行。

### IPC 消息未收到
**症状**：`invoke()` 挂起或 `send()` 无效果
**根本原因**：通道名称不匹配、preload 未加载、contextBridge 未暴露该通道
**解决方案**：验证 preload、main 和 renderer 之间的通道名称完全匹配。确认 `webPreferences` 中 `preload` 路径正确。检查通道是否在白名单数组中。

### 原生模块崩溃
**症状**：应用启动时崩溃，显示 `MODULE_NOT_FOUND` 或 `invalid ELF header`
**根本原因**：原生模块为错误的 Electron/Node ABI 版本编译
**解决方案**：安装原生模块后运行 `npx @electron/rebuild`。确保 `electron-builder` 配置了正确的 Electron 版本用于重建。

### 应用不更新
**症状**：`autoUpdater.checkForUpdates()` 无返回或报错
**根本原因**：缺少 `publish` 配置、应用未签名（macOS）、GitHub release 资源不正确
**解决方案**：验证 `electron-builder.yml` 中的 `publish` 部分。macOS 上，应用必须经过代码签名和公证。确保 GitHub release 包含 `-mac.zip` 和 `latest-mac.yml`（或等效的 Windows 文件）。

### 包体积过大（>200MB）
**症状**：构建的应用体积过大
**根本原因**：打包了开发依赖、无 tree-shaking、重复的 Electron 二进制文件
**解决方案**：审计 `electron-builder.yml` 中的 `files` 模式。对 renderer 使用打包工具（Vite/esbuild）。检查 `devDependencies` 未放入 `dependencies`。使用 `compression: maximum`。

---

## 最佳实践

- ✅ **始终**设置 `contextIsolation: true` 和 `nodeIntegration: false`
- ✅ **始终**在 preload 中使用 `contextBridge` 并带显式通道白名单
- ✅ **始终**在主进程中验证 IPC 输入 — 将 renderer 视为不可信
- ✅ **始终**使用 `ipcMain.handle()` / `ipcRenderer.invoke()` 进行请求/响应 IPC
- ✅ **始终**配置内容安全策略头
- ✅ **始终**在传递给 `shell.openExternal()` 前净化 URL
- ✅ **始终**对生产构建进行代码签名
- ✅ 使用 Playwright 及其 `@playwright/test` 的 Electron 支持进行 E2E 测试
- ✅ 将用户数据存储在 `app.getPath('userData')`，绝不存储在应用目录
- ❌ **绝不要**设置 `nodeIntegration: true` — 这是 Electron 的头号安全漏洞
- ❌ **绝不要**向 renderer 上下文暴露原始 `ipcRenderer` 或 `require()`
- ❌ **绝不要**使用 `remote` 模块（已弃用且不安全）
- ❌ **绝不要**使用 `ipcRenderer.sendSync()` — 它会阻塞 renderer 事件循环
- ❌ **绝不要**在生产环境禁用 `webSecurity`
- ❌ **绝不要**在没有严格 CSP 和沙箱的情况下加载远程/不可信内容

## 局限性

- Electron 打包 Chromium + Node.js，导致应用最小体积约 150MB — 这是框架的根本权衡
- 不适合对安装体积有严格要求的应用（考虑改用 Tauri）
- 单窗口应用架构更简单；多窗口状态同步需要精心设计 IPC
- Linux 上的自动更新需要通过 Snap、Flatpak 或自定义机制分发 — `electron-updater` 对 Linux 支持有限
- macOS 公证需要 Apple 开发者账号（$99/年），且是 Mac App Store 外分发的强制要求
- 调试主进程问题需要 VS Code 或通过 `--inspect` 标志使用 Chrome DevTools — Electron 本身没有集成调试器

## 相关技能

- `chrome-extension-developer` — 当构建浏览器扩展而非桌面应用时（共享多进程模型概念）
- `docker-expert` — 当容器化 Electron 构建流水线或 CI/CD 时
- `react-patterns` / `react-best-practices` — 当使用 React 作为 renderer UI 时
- `typescript-pro` — 当为多目标构建设置高级 TypeScript 配置时
- `nodejs-backend-patterns` — 当主进程需要复杂后端逻辑时
- `github-actions-templates` — 当为跨平台 Electron 构建设置 CI/CD 时
