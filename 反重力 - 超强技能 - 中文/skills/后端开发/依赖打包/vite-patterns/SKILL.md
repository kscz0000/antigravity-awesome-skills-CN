---
name: vite-patterns
description: Vite 构建工具模式，涵盖配置、插件、HMR、环境变量、代理设置、SSR、库模式、依赖预打包和构建优化。当使用 vite.config.ts、Vite 插件或基于 Vite 的项目时激活。触发词：Vite、构建工具、vite.config、HMR、环境变量、代理、SSR、库模式、预打包、构建优化、vite插件、vite配置、vite项目、Vite模式、Vite最佳实践、Rolldown
origin: ECC
---

# Vite 模式

面向 Vite 8+ 项目的构建工具与开发服务器模式。涵盖配置、环境变量、代理设置、库模式、依赖预打包以及常见的生产环境陷阱。

## 何时使用

- 配置 `vite.config.ts` 或 `vite.config.js`
- 设置环境变量或 `.env` 文件
- 为 API 后端配置开发服务器代理
- 优化构建输出（代码分块、压缩、静态资源）
- 使用 `build.lib` 发布库
- 排查依赖预打包或 CJS/ESM 互操作问题
- 调试 HMR、开发服务器或构建错误
- 选择或排序 Vite 插件

## 工作原理

- **开发模式**以原生 ESM 形式提供源文件——不进行打包。转换按模块请求按需进行，因此冷启动速度快且 HMR 精准。
- **构建模式**使用 Rolldown（v7+）或 Rollup（v5–v6）为生产环境打包应用，具备 tree-shaking、代码分割和基于 Oxc 的压缩能力。
- **依赖预打包**通过 esbuild 将 CJS/UMD 依赖一次性转换为 ESM，并将结果缓存于 `node_modules/.vite` 下，后续启动可跳过此步骤。
- **插件**在开发与构建中共享统一接口——同一个插件对象同时适用于开发服务器的按需转换和生产流水线。
- **环境变量**在构建时静态内联。`VITE_` 前缀的变量会成为打包产物中的公开常量；无此前缀的变量对客户端代码不可见。

## 示例

### 配置结构

#### 基本配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': new URL('./src', import.meta.url).pathname },
  },
})
```

#### 条件配置

```typescript
// vite.config.ts
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd())   // 仅 VITE_ 前缀（安全）

  return {
    plugins: [react()],
    server: command === 'serve' ? { port: 3000 } : undefined,
    define: {
      __API_URL__: JSON.stringify(env.VITE_API_URL),
    },
  }
})
```

#### 关键配置项

| 键 | 默认值 | 说明 |
|-----|---------|-------------|
| `root` | `'.'` | 项目根目录（`index.html` 所在位置） |
| `base` | `'/'` | 部署后静态资源的公共基础路径 |
| `envPrefix` | `'VITE_'` | 暴露给客户端的环境变量前缀 |
| `build.outDir` | `'dist'` | 输出目录 |
| `build.minify` | `'oxc'` | 压缩器（`'oxc'`、`'terser'` 或 `false`） |
| `build.sourcemap` | `false` | `true`、`'inline'` 或 `'hidden'` |

### 插件

#### 常用插件

大多数插件需求由少数几个维护良好的包即可覆盖。在自行编写之前优先考虑以下插件。

| 插件 | 用途 | 使用场景 |
|--------|---------|-------------|
| `@vitejs/plugin-react-swc` | 通过 SWC 实现 React HMR + Fast Refresh | React 应用默认选择（比 Babel 版本更快） |
| `@vitejs/plugin-react` | 通过 Babel 实现 React HMR + Fast Refresh | 仅在需要 Babel 插件时使用（emotion、MobX 装饰器） |
| `@vitejs/plugin-vue` | Vue 3 SFC 支持 | Vue 应用 |
| `vite-plugin-checker` | 在工作线程中运行 `tsc` + ESLint，并通过 HMR 叠加层展示 | **任何 TypeScript 应用**——Vite 在 `vite build` 期间**不会**进行类型检查 |
| `vite-tsconfig-paths` | 遵循 `tsconfig.json` 中的 `paths` 别名 | 当 `tsconfig.json` 中已有别名配置时 |
| `vite-plugin-dts` | 在库模式下生成 `.d.ts` 文件 | 发布 TypeScript 库 |
| `vite-plugin-svgr` | 将 SVG 作为 React 组件导入 | 将 SVG 作为组件使用的 React 应用 |
| `rollup-plugin-visualizer` | 打包产物的树状图/旭日图报告 | 定期进行打包体积审计（使用 `enforce: 'post'`） |
| `vite-plugin-pwa` | 零配置 PWA + Workbox | 需要离线能力的应用 |

**关键提醒：**`vite build` 会转译但**不会**进行类型检查。类型错误会悄无声息地发布到生产环境，除非添加 `vite-plugin-checker` 或在 CI 中运行 `tsc --noEmit`。

#### 编写自定义插件

自定义插件编写需求很少——大多数场景已有现成插件覆盖。当确实需要时，先在 `vite.config.ts` 中以内联方式编写，仅当需要复用时再提取出来。

```typescript
// vite.config.ts — 最小内联插件
function myPlugin(): Plugin {
  return {
    name: 'my-plugin',                       // 必填，必须唯一
    enforce: 'pre',                           // 'pre' | 'post'（可选）
    apply: 'build',                           // 'build' | 'serve'（可选）
    transform(code, id) {
      if (!id.endsWith('.custom')) return
      return { code: transformCustom(code), map: null }
    },
  }
}
```

**关键钩子：**`transform`（修改源码）、`resolveId` + `load`（虚拟模块）、`transformIndexHtml`（注入 HTML）、`configureServer`（添加开发中间件）、`hotUpdate`（自定义 HMR——v7+ 中替代已废弃的 `handleHotUpdate`）。

**虚拟模块**使用 `\0` 前缀约定——`resolveId` 返回 `'\0virtual:my-id'` 以便其他插件跳过。用户代码导入 `'virtual:my-id'`。

完整的插件 API 请参阅 [vite.dev/guide/api-plugin](https://vite.dev/guide/api-plugin)。开发期间使用 `vite-plugin-inspect` 调试转换流水线。

### HMR API

框架插件（`@vitejs/plugin-react`、`@vitejs/plugin-vue` 等）会自动处理 HMR。仅当构建自定义状态存储、开发工具或需要在更新间保持状态的框架无关工具时，才直接使用 `import.meta.hot`。

```typescript
// src/store.ts — 为原生模块手动实现 HMR
if (import.meta.hot) {
  // 在更新间保持状态（必须修改属性，不可对 .data 重新赋值）
  import.meta.hot.data.count = import.meta.hot.data.count ?? 0

  // 模块被替换前清理副作用
  import.meta.hot.dispose((data) => clearInterval(data.intervalId))

  // 接受本模块自身的更新
  import.meta.hot.accept()
}
```

所有 `import.meta.hot` 代码都会在生产构建中被 tree-shake 移除——无需手动移除守卫代码。

### 环境变量

Vite 按以下顺序加载 `.env`、`.env.local`、`.env.[mode]` 和 `.env.[mode].local`（后加载的覆盖先加载的）；`*.local` 文件应加入 gitignore，用于存放本地密钥。

#### 客户端访问

只有 `VITE_` 前缀的变量才会暴露给客户端代码：

```typescript
import.meta.env.VITE_API_URL   // string
import.meta.env.MODE            // 'development' | 'production' | 自定义
import.meta.env.BASE_URL        // base 配置值
import.meta.env.DEV             // boolean
import.meta.env.PROD            // boolean
import.meta.env.SSR             // boolean
```

#### 在配置中使用环境变量

```typescript
// vite.config.ts
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())          // 仅 VITE_ 前缀（安全）
  return {
    define: {
      __API_URL__: JSON.stringify(env.VITE_API_URL),
    },
  }
})
```

### 安全性

#### `VITE_` 前缀并非安全边界

任何以 `VITE_` 为前缀的变量都会在构建时**静态内联到客户端打包产物中**。压缩、Base64 编码和禁用 source map 都**无法**隐藏它。有决心的攻击者可以从发布的 JavaScript 中提取任何 `VITE_` 变量。

**原则：**只有公开值（API URL、功能开关、公钥）才能放在 `VITE_` 变量中。密钥（API Token、数据库 URL、私钥）**必须**存在于服务器端，通过 API 或 serverless 函数提供。

#### `loadEnv('')` 陷阱

```typescript
// 错误：传入 '' 作为第三个参数会加载所有环境变量——包括服务器密钥——
// 并通过 `define` 使它们可被内联到客户端代码中。
const env = loadEnv(mode, process.cwd(), '')

// 正确：显式指定前缀列表
const env = loadEnv(mode, process.cwd(), ['VITE_', 'APP_'])
```

#### 生产环境的 Source Map

生产环境 source map 会泄露原始源代码。除非上传到错误追踪服务（Sentry、Bugsnag）并在之后删除本地文件，否则应禁用：

```typescript
build: {
  sourcemap: false,                                  // 默认值——保持此设置
}
```

#### `.gitignore` 检查清单

- `.env.local`、`.env.*.local`——本地密钥覆盖
- `dist/`——构建输出
- `node_modules/.vite`——预打包缓存（过期条目会导致幽灵错误）

### 服务器代理

```typescript
// vite.config.ts — server.proxy
server: {
  proxy: {
    '/foo': 'http://localhost:4567',                    // 字符串简写

    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,                               // 虚拟主机后端需要
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
}
```

如需 WebSocket 代理，在路由配置中添加 `ws: true`。

### 构建优化

#### 手动分块

```typescript
// vite.config.ts — build.rolldownOptions
build: {
  rolldownOptions: {
    output: {
      // 对象形式：将特定包分组
      manualChunks: {
        'react-vendor': ['react', 'react-dom'],
        'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-popover'],
      },
    },
  },
}
```

```typescript
// 函数形式：按启发式规则分割
manualChunks(id) {
  if (id.includes('node_modules/react')) return 'react-vendor'
  if (id.includes('node_modules')) return 'vendor'
}
```

### 性能

#### 避免桶文件（Barrel Files）

桶文件（`index.ts` 重新导出目录中的所有内容）会强制 Vite 加载每个被重新导出的文件，即使只导入单个符号。这是官方文档标记的**头号**开发服务器性能杀手。

```typescript
// 错误——导入一个工具函数却强制 Vite 加载整个桶文件
import { slash } from '@/utils'

// 正确——直接导入，只加载一个文件
import { slash } from '@/utils/slash'
```

#### 明确指定导入扩展名

每个隐式扩展名会通过 `resolve.extensions` 触发最多 6 次文件系统检查。在大型代码库中，这些开销会累积。

```typescript
// 错误
import Component from './Component'

// 正确
import Component from './Component.tsx'
```

收窄 `tsconfig.json` 中的 `allowImportingTsExtensions` + `resolve.extensions`，仅保留实际使用的扩展名。

#### 预热热路径路由

`server.warmup.clientFiles` 在浏览器请求之前预先转换已知的热入口——消除大型应用上的冷加载请求瀑布流。

```typescript
// vite.config.ts
server: {
  warmup: {
    clientFiles: ['./src/main.tsx', './src/routes/**/*.tsx'],
  },
}
```

#### 分析慢速开发服务器

当 `vite dev` 感觉缓慢时，首先运行 `vite --profile`，与应用交互，然后按 `p+回车` 保存 `.cpuprofile` 文件。在 [Speedscope](https://www.speedscope.app) 中加载该文件，找出哪些插件在消耗时间——通常是社区插件中的 `buildStart`、`config` 或 `configResolved` 钩子。

### 库模式

发布 npm 包时使用 `build.lib`。有两个容易踩的坑比配置细节更重要：

1. **不会自动生成类型声明**——添加 `vite-plugin-dts` 或单独运行 `tsc --emitDeclarationOnly`。
2. **peer 依赖必须外部化**——未列出的 peer 依赖会被打包进库中，导致消费者端出现重复运行时错误。

```typescript
// vite.config.ts
build: {
  lib: {
    entry: 'src/index.ts',
    formats: ['es', 'cjs'],
    fileName: (format) => `my-lib.${format}.js`,
  },
  rolldownOptions: {
    external: ['react', 'react-dom', 'react/jsx-runtime'],  // 所有 peer 依赖
  },
}
```

### SSR 外部化

裸 `createServer({ middlewareMode: true })` 的设置属于框架作者的领域。大多数应用应使用 Nuxt、Remix、SvelteKit、Astro 或 TanStack Start。作为框架用户，你**会**在 SSR 中依赖出问题时调整的是外部化配置：

```typescript
// vite.config.ts — ssr 选项
ssr: {
  external: ['node-native-package'],           // 在 SSR 打包产物中保持为 require()
  noExternal: ['esm-only-package'],            // 强制打包进 SSR 输出（修复大多数 SSR 错误）
  target: 'node',                              // 'node' 或 'webworker'
}
```

### 依赖预打包

Vite 预打包依赖以将 CJS/UMD 转换为 ESM 并减少请求数量。

```typescript
// vite.config.ts — optimizeDeps
optimizeDeps: {
  include: [
    'lodash-es',                              // 强制预打包已知的重型依赖
    'cjs-package',                            // 导致互操作问题的 CJS 依赖
    'deep-lib/components/**',                 // glob 匹配深层导入
  ],
  exclude: ['local-esm-package'],             // 排除的依赖必须是有效的 ESM
  force: true,                                // 忽略缓存，重新优化（临时调试用）
}
```

### 常见陷阱

#### 开发环境与构建环境行为不一致

开发环境使用 esbuild/Rolldown 进行转换；构建环境使用 Rolldown 进行打包。CJS 库在两者之间可能表现不同。部署前始终通过 `vite build && vite preview` 验证。

#### 部署后的过期分块

新构建会生成新的分块哈希。活跃会话中的用户会请求已不存在的旧文件名。Vite 没有内置解决方案。缓解措施：

- 在部署窗口期内保留旧的 `dist/assets/` 文件
- 在路由中捕获动态导入错误并强制页面重新加载

#### Docker 与容器

Vite 默认绑定到 `localhost`，容器外部无法访问：

```typescript
// vite.config.ts — Docker/容器设置
server: {
  host: true,                                  // 绑定 0.0.0.0
  hmr: { clientPort: 3000 },                   // 如果位于反向代理之后
}
```

#### Monorepo 文件访问

Vite 将文件服务限制在项目根目录。根目录外的包会被阻止：

```typescript
// vite.config.ts — monorepo 文件访问
server: {
  fs: {
    allow: ['..'],                             // 允许父目录（工作区根目录）
  },
}
```

### 反模式

```typescript
// 错误：将 envPrefix 设为 '' 会向客户端暴露所有环境变量（包括密钥）
envPrefix: ''

// 错误：假设 require() 在应用源码中可用——Vite 是 ESM 优先的
const lib = require('some-lib')                // 请使用 import

// 错误：将每个 node_module 拆成独立分块——产生数百个小文件
manualChunks(id) {
  if (id.includes('node_modules')) {
    return id.split('node_modules/')[1].split('/')[0]   // 每个包一个分块
  }
}

// 错误：库模式下未将 peer 依赖外部化——导致重复运行时错误
// 使用 build.lib 但未配置 rolldownOptions.external

// 错误：使用已废弃的 esbuild 压缩器
build: { minify: 'esbuild' }                  // 使用 'oxc'（默认）或 'terser'

// 错误：通过重新赋值修改 import.meta.hot.data
import.meta.hot.data = { count: 0 }           // 错误：必须修改属性，不能重新赋值
import.meta.hot.data.count = 0                 // 正确
```

**流程性反模式：**

- **`vite preview` 不是生产服务器**——它只是对构建产物进行冒烟测试。将 `dist/` 部署到真正的静态托管服务（NGINX、Cloudflare Pages、Vercel Static）或使用多阶段 Dockerfile。
- **期望 `vite build` 进行类型检查**——它只做转译。类型错误会悄无声息地发布到生产环境。添加 `vite-plugin-checker` 或在 CI 中运行 `tsc --noEmit`。
- **默认引入 `@vitejs/plugin-legacy`**——它会使打包体积膨胀约 40%，破坏 source-map 打包分析工具，且对 95% 以上使用现代浏览器的用户来说毫无必要。基于真实分析数据而非假设来决定是否使用。
- **手写 30 多条 `resolve.alias` 条目来重复 `tsconfig.json` 中的 paths 配置**——改用 `vite-tsconfig-paths`。在 Excalidraw 和 PostHog 中观察到此问题；新项目中应避免。
- **依赖变更后遗留过期的 `node_modules/.vite`**——预打包缓存会导致幽灵错误。切换分支或修补依赖后应清除该目录。

## 快速参考

| 模式 | 使用场景 |
|---------|-------------|
| `defineConfig` | 始终使用——提供类型推断 |
| `loadEnv(mode, root, ['VITE_'])` | 在配置中访问环境变量（显式指定前缀） |
| `vite-plugin-checker` | 任何 TypeScript 应用（填补类型检查缺口） |
| `vite-tsconfig-paths` | 替代手写的 `resolve.alias` |
| `optimizeDeps.include` | 导致互操作问题的 CJS 依赖 |
| `server.proxy` | 开发时将 API 请求路由到后端 |
| `server.host: true` | Docker、容器、远程访问 |
| `server.warmup.clientFiles` | 预热热路径路由 |
| `build.lib` + `external` | 发布 npm 包 |
| `manualChunks`（对象形式） | 第三方库分块拆分 |
| `vite --profile` | 调试慢速开发服务器 |
| `vite build && vite preview` | 本地冒烟测试生产构建产物（不是生产服务器） |

## 相关技能

- `frontend-patterns`——React 组件模式
- `docker-patterns`——使用 Vite 的容器化开发
- `nextjs-turbopack`——Next.js 的替代打包方案
