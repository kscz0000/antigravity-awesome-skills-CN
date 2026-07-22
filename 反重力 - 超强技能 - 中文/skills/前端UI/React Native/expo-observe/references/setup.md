# 在现有项目中设置 EAS Observe

EAS Observe 从生产环境中的 Expo 应用收集应用启动性能指标（冷启动、热启动、bundle 加载、TTR、TTI）。本参考文件汇总了将 `expo-observe` 添加到现有项目的步骤。

> 来源：https://docs.expo.dev/eas/observe/get-started/ —— 获取最新指南请查阅此页面。

## SDK 55 与 SDK 56+ 对比概览

库导出内容在 SDK 版本之间存在差异。在复制下面的任何代码片段之前，请根据项目的 SDK 选择合适的版本。

| 关注点 | SDK 55 | SDK 56 及以后 |
|---|---|---|
| 根布局 HOC | `AppMetricsRoot.wrap(...)` | `ObserveRoot.wrap(...)` |
| `markInteractive()` API | 全局：`AppMetrics.markInteractive()` | 钩子：`const { markInteractive } = useObserve()` |
| 导入来源 | `expo-observe` | `expo-observe`（相同包） |

其他方面 —— 包名、构建流程、仪表板、调试模式行为 —— 在各版本中保持一致。

## 前置条件

在安装之前，请确认以下所有条件：

1. **Expo 账号。** 如有需要，请在 [expo.dev/signup](https://expo.dev/signup) 注册。
2. **Expo SDK 55 或更高版本。** 运行 `npx expo-doctor` 检查，运行 `npx expo install --fix` 更新依赖。SDK 56+ 可解锁更新的 `ObserveRoot` / `useObserve` API。
3. **EAS 项目。** 应用的 app config 中必须设置 `extra.eas.projectId`。如果没有，请运行 `eas init` 创建。

## 步骤 1 —— 安装库

在项目根目录下：

```sh
npx expo install --fix
npx expo install expo-observe
```

## 步骤 2 —— 包裹根布局

HOC 会自动测量**首次渲染时间（TTR）**。请将其应用于导出应用根组件的文件。HOC 的名称取决于 SDK 版本。

**SDK 55** —— 使用 `AppMetricsRoot`：

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import { AppMetricsRoot } from 'expo-observe';

function RootLayout() {
  return <Stack />;
}

export default AppMetricsRoot.wrap(RootLayout);
```

**SDK 56 及以后** —— 使用 `ObserveRoot`：

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import { ObserveRoot } from 'expo-observe';

function RootLayout() {
  return <Stack />;
}

export default ObserveRoot.wrap(RootLayout);
```

**未使用 Expo Router**（`App.tsx`）：以相同方式包裹默认导出的 `App` 组件 —— 在 SDK 55 上为 `export default AppMetricsRoot.wrap(App);`，在 SDK 56+ 上为 `export default ObserveRoot.wrap(App);`。

## 步骤 3 —— 标记应用为可交互

TTI **不会**自动采集。当屏幕真正准备好供用户使用时发出信号 —— 即在启动屏阻塞类工作（更新检查、身份验证、初始数据获取、启动屏动画）完成之后。将此调用置于 `useEffect` 中，在该工作 resolve 之后运行。

**SDK 55** —— 调用全局的 `AppMetrics.markInteractive()`：

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { AppMetrics, AppMetricsRoot } from 'expo-observe';
import { useEffect, useState } from 'react';

SplashScreen.preventAutoHideAsync();

function RootLayout() {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    async function prepare() {
      try {
        await authenticateUser();
        await fetchInitialData();
      } catch (e) {
        console.warn(e);
      } finally {
        setIsReady(true);
      }
    }
    prepare();
  }, []);

  useEffect(() => {
    if (isReady) {
      SplashScreen.hide();
      AppMetrics.markInteractive();
    }
  }, [isReady]);

  if (!isReady) return null;
  return <Stack />;
}

export default AppMetricsRoot.wrap(RootLayout);
```

**SDK 56 及以后** —— 使用 `useObserve()` 钩子获取绑定的 `markInteractive`：

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { ObserveRoot, useObserve } from 'expo-observe';
import { useEffect, useState } from 'react';

SplashScreen.preventAutoHideAsync();

function RootLayout() {
  const [isReady, setIsReady] = useState(false);
  const { markInteractive } = useObserve();

  useEffect(() => {
    async function prepare() {
      try {
        await authenticateUser();
        await fetchInitialData();
      } catch (e) {
        console.warn(e);
      } finally {
        setIsReady(true);
      }
    }
    prepare();
  }, []);

  useEffect(() => {
    if (isReady) {
      SplashScreen.hide();
      markInteractive();
    }
  }, [isReady, markInteractive]);

  if (!isReady) return null;
  return <Stack />;
}

export default ObserveRoot.wrap(RootLayout);
```

**未使用 Expo Router：** `App.tsx` 中的结构相同。使用 `SplashScreen.hideAsync()` 代替 `SplashScreen.hide()`，并将 `<Stack />` 替换为应用的根组件树。

### 多个入口屏幕

`markInteractive()` 可安全地重复调用 —— 每个会话中只有**第一次**调用会被记录。如果应用有多个入口屏幕（引导页、登录页、深度链接目标），请在**每个屏幕**上都调用 `markInteractive()`。否则通过深度链接打开、未调用该方法的屏幕的会话将缺少 TTI。

## 步骤 4 —— 构建应用

指标是从真实构建中采集，而不是从 `expo start` 中采集：

```sh
eas build
```

> 默认情况下，从**调试构建**采集的指标不会上报。当原生应用为调试构建，或 JS bundle 为开发 bundle（`__DEV__` 为 `true`）时，构建被视为调试构建。要在测试集成时仍上报指标，请在调用 `configure()` 时设置 `dispatchInDebug: true` —— 参见[在开发环境中启用指标](https://docs.expo.dev/eas/observe/configuration/#enable-metrics-in-development)。这对发布构建没有影响。

## 步骤 5 —— 查看指标

打开 EAS 仪表板中的 **Observe** 选项卡（地址为 `https://expo.dev/accounts/[account]/projects/[project]/observe`）以查看应用的指标。

要通过 EAS CLI 从终端查询指标，请参见 [`./queries.md`](./queries.md)。要解读指标本身的含义，请参见 [`./metrics.md`](./metrics.md)。

## 可选 —— 按路由的导航指标（SDK 56+）

默认情况下，`expo-observe` 仅记录全局应用启动指标。如需额外获取**按路由/按屏幕**的导航指标（`cold_ttr`、`warm_ttr` 和每次导航的 `tti`，每个都带有路由/屏幕标签），请启用相应的导航集成之一。这些集成需要 **SDK 56 或更高版本**；在更早的 SDK 上它们是静默的 no-op。使用 `eas observe:routes`（参见 [`./queries.md`](./queries.md)）查询相关数据。

请选择与应用路由器匹配的集成：

### Expo Router

文档：https://docs.expo.dev/eas/observe/integrations/expo-router/

1. 在模块作用域、**在任何屏幕挂载之前**启用集成（不能在运行时切换 —— 在挂载后调用 `configure()` 会抛出）：

   ```tsx
   // app/_layout.tsx
   import { Observe } from 'expo-observe';

   Observe.configure({
     integrations: { 'expo-router': true },
   });
   ```

2. 在每个屏幕内部调用 `useObserve()`，以获得限定于当前路由的 `markInteractive`，并在屏幕可交互后于 `useEffect` 中调用它：

   ```tsx
   import { useObserve } from 'expo-observe';
   import { useEffect } from 'react';

   export default function Home() {
     const { markInteractive } = useObserve();
     useEffect(() => {
       markInteractive();
     }, [markInteractive]);
     return (/* screen content */);
   }
   ```

事件会使用路由的**模式**（pattern）打标签（例如 `/(tabs)/sessions/[sessionId]`），以便仪表板将不同的参数值归为同一组；同时还会包含已解析的 `url` 和 `routeParams`。要求运行时已安装 `expo-router`，否则该集成将作为 no-op 静默处理。

### React Navigation

文档：https://docs.expo.dev/eas/observe/integrations/react-navigation/

要求 `@react-navigation/native` 7.0.0 或更高版本。屏幕中 `useObserve()` 的使用方式同上，另外还需做**两处**更改：

1. 在模块作用域、挂载之前启用集成：

   ```tsx
   // App.tsx
   import { Observe } from 'expo-observe';

   Observe.configure({
     integrations: { 'react-navigation': true },
   });
   ```

2. 将顶层的 `<NavigationContainer>` 替换为 `<ObserveNavigationContainer>` —— 这是一个可替换的组件，接受相同的 props 并转发相同的 ref。如果你传入了 `linking` 配置，它将用于解析为人类可读的屏幕路径；否则该指标会回退为使用 `route.name`。

   ```tsx
   import { ObserveNavigationContainer } from 'expo-observe/integrations/react-navigation';

   export default function App() {
     return <ObserveNavigationContainer>{/* navigators */}</ObserveNavigationContainer>;
   }
   ```

在两种集成中，即使集成被禁用或路由器包不存在，`useObserve()` 也可以保留在原位 —— 它会回退为使用全局的 `markInteractive`。

## 快速检查清单

- [ ] SDK ≥ 55，EAS 项目已关联。
- [ ] 已通过 `npx expo install` 安装 `expo-observe`。
- [ ] 根组件通过 `AppMetricsRoot.wrap(...)`（SDK 55）或 `ObserveRoot.wrap(...)`（SDK 56+）导出。
- [ ] 在每个入口屏幕真正可交互时调用 `markInteractive()` —— 在 SDK 55 中使用全局的 `AppMetrics.markInteractive()`，在 SDK 56+ 中使用 `useObserve()` 钩子。
- [ ] （可选，SDK 56+）通过 `Observe.configure({ integrations: { ... } })` 启用按路由指标，若使用 React Navigation 则再加上 `<ObserveNavigationContainer>`。
- [ ] 已使用 `eas build` 生成新构建，且指标在 Observe 仪表板中可见。
