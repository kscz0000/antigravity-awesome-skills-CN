---
name: frontend-observability
description: 为任意 React 或 React Native 应用提供的、与框架无关的、可移植的现场侧可观测性系统。建立一套类型化的事件分类体系（规范的事件名常量，绝不内联字符串）、尽力且非阻塞的 provider 扇出机制，避免任何分析 provider 失败或缺席时导致崩溃……适用于前端可观测性、事件埋点、Core Web Vitals 实时上报、错误边界、用户同意门控等场景。
risk: unknown
source: https://github.com/stareezy-1/frontend-architecture-skill/tree/main/skills/frontend-observability
source_repo: stareezy-1/frontend-architecture-skill
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/stareezy-1/frontend-architecture-skill/blob/main/LICENSE
---

# 前端可观测性（现场侧）
## 适用场景

在需要为任意 React 或 React Native 应用提供一套与框架无关的、可移植的现场侧可观测性系统时，使用本技能。它建立一套类型化的事件分类体系（规范的事件名常量，绝不使用内联字符串），采用尽力且非阻塞的 provider 扇出机制，从而保证分析 provider 失败或缺席时……


> 可移植的技能——Claude Code、OpenCode、Codex、Cursor、Windsurf 等均可读取。
> 本技能描述的是一套**现场侧可观测性系统**——事件分类、provider 扇出、真实用户核心指标、错误上报、用户同意——而非某个具体仪表盘或厂商。它是 **frontend-lighthouse 技能的现场侧补充**：Lighthouse 是 _实验室_ 闸口（合成、合并前），本技能是 _现场_ （真实用户实际体验）。按照 **frontend-architecture** 技能，它位于 `services/analytics/` 模块。

目标：让你能回答"真实用户在做什么，正在体验什么？"——使用一套**类型化的事件词汇**（杜绝到处都是字符串化的 `track("clicked_thing")`）、一个**尽力而为**的扇出（任何 provider 崩溃都不会拖垮应用）、来自现场的真实**Core Web Vitals**，以及在所有上报触发前先尊重**用户同意**。

---

## 0. 五大核心思想

1. **事件是类型化词汇。** 事件名是带联合类型的规范常量——绝不使用内联字符串字面量。整个分类体系可在单个文件中集中审阅，编译器会拒绝拼写错误。
2. **扇出是尽力且非阻塞的。** `track()` 向每个 provider 分发事件，每个分发都包裹独立的 try/catch。缺失的全局、抛出异常的 provider、未加载完成的脚本——都不能向上抛给调用方，也不能阻断其他 provider。
3. **单一入口，SSR 安全。** 仅通过 `track(event, props)` 这一种方式记录事件。它通过一个上下文 hook 访问——该 hook 在没有 provider 或在服务端时为 no-op，因此被埋点的组件可在任何环境中安全渲染。
4. **现场指标与实验室预算互补。** 真实用户的 LCP/INP/CLS 上报到同一个扇出。Lighthouse 证明构建 _能_ 够快；现场指标证明它 _确实_ 快——两者结合构成闭环。
5. **同意先于一切。** 在用户授权之前，不上报任何遥测（事件、指标、含 PII 的错误）。同意状态在扇出边界统一检查，不分散在各调用点。

---

## 1. 目录结构

整套系统由一个服务模块加上它的常量文件组成（遵循 frontend-architecture 规范）。

```
src/
├── constants/
│   └── analytics.ts           ← canonical event names + AnalyticsEvent union
├── services/analytics/
│   ├── index.ts               ← barrel: track, adapters, types
│   ├── track.ts               ← the best-effort fan-out (single entry point)
│   ├── adapters.ts            ← one (event, props) => void per provider, window-guarded
│   ├── web-vitals.ts          ← report real-user LCP/INP/CLS into track()
│   └── consent.ts             ← consent gate read by the fan-out
├── providers/
│   └── AnalyticsProvider.tsx  ← 'use client' context exposing useAnalytics().track
└── error/
    └── ErrorBoundary.tsx      ← reports caught render errors via the fan-out
```

---

## 2. 事件分类体系（类型化，绝不内联）

用一个文件统一管理所有事件名。组件引用常量；联合类型使拼写错误成为编译错误，使分类目录成为唯一事实来源。

```ts
// constants/analytics.ts
export const ANALYTICS_EVENTS = {
  PROJECT_CLICK: "project_click",
  GITHUB_CLICK: "github_click",
  RESUME_DOWNLOAD: "resume_download",
  CONTACT_SUBMISSION: "contact_submission",
} as const;

export type AnalyticsEvent =
  (typeof ANALYTICS_EVENTS)[keyof typeof ANALYTICS_EVENTS];
```

```ts
// CORRECT — typed constant, autocompletes, can't typo
track(ANALYTICS_EVENTS.GITHUB_CLICK, { url });

// WRONG — stringly-typed, drifts, no compile check
track("github-click"); // ❌ silently a different event from "github_click"
```

**硬性规则：**

- 任何位置都不允许内联事件名字符串；只能使用 `ANALYTICS_EVENTS.*`。
- 事件名使用 snake_case 且保持稳定——重命名一个会破坏历史仪表盘，因此应将分类目录视为一种契约。
- 保持 `props` 结构精简且避免 PII（见第 6 节）；优先使用 id 而非姓名，绝不上传原始邮箱。

---

## 3. 尽力且非阻塞的扇出

`track()` 是唯一的入口。它遍历 adapter 注册表，对**每一次**调用都加以保护，从而保证任何一个 provider 都不能影响调用方或其他 provider。

```ts
// services/analytics/track.ts
import type { AnalyticsEvent } from "@/constants/analytics";
import { analyticsAdapters } from "./adapters";
import { hasConsent } from "./consent";

export function track(
  event: AnalyticsEvent,
  props?: Record<string, unknown>,
): void {
  if (!hasConsent()) return; // §6 — nothing fires before opt-in
  for (const adapter of analyticsAdapters) {
    try {
      adapter(event, props);
    } catch {
      /* best-effort: a failing/absent provider must never throw into the
         caller or block dispatch to the remaining providers. */
    }
  }
}
```

每个 adapter 都是一个微小的 `(event, props) => void`，它**对其 provider 全局进行保护**——在服务端（无 `window`）或 provider 脚本缺失时为 no-op，确保缺失或未加载完成的 provider 永远不会抛出。

```ts
// services/analytics/adapters.ts
export type AnalyticsAdapter = (
  event: AnalyticsEvent,
  props?: Record<string, unknown>,
) => void;

export const googleAnalyticsAdapter: AnalyticsAdapter = (event, props) => {
  const w =
    typeof window !== "undefined" ? (window as AnalyticsGlobals) : undefined;
  if (!w || typeof w.gtag !== "function") return; // SSR-safe + absent-safe
  w.gtag("event", event, props ?? {});
};

export const clarityAdapter: AnalyticsAdapter = (event) => {
  const w =
    typeof window !== "undefined" ? (window as AnalyticsGlobals) : undefined;
  if (!w || typeof w.clarity !== "function") return;
  w.clarity("event", event);
};

// The registry track() fans out across. Exported + mutable so tests can swap
// in a recording sink to assert dispatch.
export const analyticsAdapters: AnalyticsAdapter[] = [
  googleAnalyticsAdapter,
  clarityAdapter,
  firebaseAdapter,
  // posthogAdapter, openPanelAdapter, …
];
```

### 3.1 Firebase Analytics — 一个 adapter，两个平台

Firebase Analytics 提供两个 SDK，它们共享**同样的 `logEvent(name, params)` 契约**，因此一个概念上的 adapter 就同时覆盖了 Web 和 React Native——只有 import 和"是否可用？"的判断不同。在 Web 端，adapter 绝不在模块顶层 import 该 SDK（它是浏览器专属且异步加载的），从而保持 SSR 安全。

```ts
// services/analytics/adapters.firebase.web.ts — Firebase JS SDK (web)
import type { Analytics } from "firebase/analytics";
import type { AnalyticsAdapter } from "./adapters";

// Held after a lazy, browser-only init (below) so the adapter stays synchronous + SSR-safe.
let analytics: Analytics | undefined;
export function setFirebaseAnalytics(instance: Analytics): void {
  analytics = instance;
}

export const firebaseAdapter: AnalyticsAdapter = (event, props) => {
  if (typeof window === "undefined" || !analytics) return; // SSR-safe + not-yet-ready safe
  void import("firebase/analytics").then(({ logEvent }) =>
    logEvent(analytics!, event, props),
  );
};
```

```ts
// services/analytics/firebase.init.ts — lazy, browser-only init (web)
import { initializeApp, getApps } from "firebase/app";
import { getAnalytics, isSupported } from "firebase/analytics";
import { setFirebaseAnalytics } from "./adapters.firebase.web";
import { FIREBASE_CONFIG } from "@/constants/analytics";

export async function initFirebaseAnalytics(): Promise<void> {
  if (typeof window === "undefined") return; // never on the server
  if (!(await isSupported())) return; // unsupported browser → no-op
  const app = getApps()[0] ?? initializeApp(FIREBASE_CONFIG);
  setFirebaseAnalytics(getAnalytics(app)); // adapter goes live after this
}
```

```ts
// services/analytics/adapters.firebase.native.ts — @react-native-firebase/analytics (RN / Expo)
import analytics from "@react-native-firebase/analytics";
import type { AnalyticsAdapter } from "./adapters";

export const firebaseAdapter: AnalyticsAdapter = (event, props) => {
  // RN: no window; the native module is present once the app boots.
  void analytics().logEvent(event, props);
};
```

**同样的形状，两个文件。** 通过文件后缀解析平台版本
（通过 Metro 的 `.native.ts` 解析，或者使用 `Platform.OS` 切换），从而使**注册表、`track` 扇出、同意门、分类体系和 `useAnalytics` hook 在跨平台时完全不变**。Firebase 的事件名规则（snake_case、全小写、≤ 40 字符）与第 2 节的分类规则一致，因此规范的 `ANALYTICS_EVENTS` 常量可以直接作为合法的 Firebase 事件名使用。将 `initFirebaseAnalytics()` 门控于用户同意（第 6 节）之后——Firebase 也提供 `setAnalyticsCollectionEnabled(false)` 来强化退出机制。

**为什么采用这种形状：** 分析系统是 _最后才应该_ 让应用崩溃的模块。加载失败的供应商脚本、尚未就绪的全局、对畸形 prop 抛错的 adapter——全部都会被隔离。注册表已导出且可变，使调度分发在不挂载任何 provider 的情况下即可进行单元测试。

---

## 4. Provider 与 hook（SSR 安全入口）

`'use client'` 上下文通过 `useAnalytics()` 暴露 `track`。在没有 provider 的环境（测试、服务端）中，它返回**空操作**，从而保证被埋点的组件在隔离状态下永远不会抛出。

```tsx
// providers/AnalyticsProvider.tsx
"use client";
import { createContext, useContext, useMemo, type ReactNode } from "react";
import { track as trackEvent } from "@/services/analytics";
import type { AnalyticsEvent } from "@/constants/analytics";

interface AnalyticsContextValue {
  track: (event: AnalyticsEvent, props?: Record<string, unknown>) => void;
}
const AnalyticsContext = createContext<AnalyticsContextValue | null>(null);

export function AnalyticsProvider({ children }: { children: ReactNode }) {
  // track is module-level and stable → memoize once, never re-render consumers.
  const value = useMemo<AnalyticsContextValue>(
    () => ({ track: trackEvent }),
    [],
  );
  return (
    <AnalyticsContext.Provider value={value}>
      {children}
    </AnalyticsContext.Provider>
  );
}

const NOOP: AnalyticsContextValue = { track: () => undefined };
export function useAnalytics(): AnalyticsContextValue {
  return useContext(AnalyticsContext) ?? NOOP; // safe outside a provider / on server
}
```

```tsx
// a tracked leaf — Server Components can't use the hook, so wrap in a thin client component
"use client";
export function TrackedGithubLink({ href, children }: Props) {
  const { track } = useAnalytics();
  return (
    <a
      href={href}
      onClick={() => track(ANALYTICS_EVENTS.GITHUB_CLICK, { url: href })}
    >
      {children}
    </a>
  );
}
```

Provider 在渲染期间**不做任何工作**——`track` 是稳定的，且 adapter 自己负责守卫 `window` 访问——因此可以安全地挂载在根部，包括 SSR/RSC 树中。

---

## 5. 真实用户 Core Web Vitals（实验室/现场闭环）

通过**同一个扇出**上报现场指标。这是 lighthouse 技能的补充：实验室闸口设定预算，现场数据告诉你真实用户是否达标。

```ts
// services/analytics/web-vitals.ts
import { onLCP, onINP, onCLS, onFCP, onTTFB, type Metric } from "web-vitals";
import { track } from "./track";

export function reportWebVitals(): void {
  const send = (m: Metric) =>
    track("web_vital" as AnalyticsEvent, {
      name: m.name, // LCP | INP | CLS | FCP | TTFB
      value: Math.round(m.name === "CLS" ? m.value * 1000 : m.value),
      rating: m.rating, // good | needs-improvement | poor
      id: m.id,
    });
  onLCP(send);
  onINP(send);
  onCLS(send);
  onFCP(send);
  onTTFB(send);
}
```

- 在客户端调用一次 `reportWebVitals()`（例如在 Analytics provider 的 effect 中，或者使用 Next.js 的 `useReportWebVitals`）。
- 使用**与 lighthouse 技能完全相同的指标和阈值**（LCP ≤ 2500、INP ≤ 200、CLS ≤ 0.1），让实验室和现场说同一种语言。
- 实验室预算绿 + 现场数据"差"= 你的测试条件与真实设备/网络之间存在差距——这正是现场 RUM 存在的意义。

---

## 6. 同意与隐私门控

遥测仅在用户授权后才上报，并在扇出边界**统一检查一次**（第 3 节）——而非在每个调用点重复判断。

```ts
// services/analytics/consent.ts
let granted = false; // hydrate from a stored consent cookie/localStorage on init
export function setConsent(value: boolean): void {
  granted = value;
}
export function hasConsent(): boolean {
  return granted;
}
```

**硬性规则：**

- 在没有同意时 `track()` 提前返回——授权之前没有事件、没有指标、不上报任何含 PII 的错误。
- 保持 `props` 轻量化：使用 id 和枚举，避免邮箱/姓名/自由文本。任何用户输入的内容都视为敏感。
- 默认尊重"Do Not Track"和各地区法规（GDPR/CCPA），在要求的地方将同意默认值置为 `false`。
- 错误报告必须在离开设备前清除 PII。

---

## 7. 边界处的错误上报

捕获到的渲染错误和未处理的 promise 异常通过同一个扇出上报（或通过专用的 Sentry adapter），发生在**有意识的边界处**——而非全局吞掉。

```tsx
// error/ErrorBoundary.tsx (essence)
componentDidCatch(error: Error, info: ErrorInfo) {
  track("client_error" as AnalyticsEvent, {
    message: error.message, component: info.componentStack?.split("\n")[1]?.trim(),
  }); // or sentryAdapter(error, info)
}
```

- 在路由/分段级别放置边界（遵循 frontend-architecture 的 page-directory 模型），让某处崩溃只会降级单个面，而非整个应用。
- 与数据层的类型化 `ApiError` 配合使用（frontend-data-contracts 第 6 节）：仅上报 _意外_ 错误；可预期的错误（校验、404）走正常处理，不当作崩溃上报。

---

## 8. Provider 与框架 adapter

分类体系和扇出保持不变；每个 provider 都只是一个带 window 守卫的 adapter。

| Provider               | Adapter call                                                                 |
| ---------------------- | ---------------------------------------------------------------------------- |
| **Firebase (web)**     | `logEvent(analytics, name, props)` (`firebase/analytics`, lazy browser init) |
| **Firebase (RN/Expo)** | `analytics().logEvent(name, props)` (`@react-native-firebase/analytics`)     |
| **GA4**                | `window.gtag("event", name, props)`                                          |
| **Microsoft Clarity**  | `window.clarity("event", name)`                                              |
| **PostHog**            | `window.posthog?.capture(name, props)`                                       |
| **OpenPanel**          | `op("track", name, props)` or `op.track(name, props)`                        |
| **Sentry**             | `Sentry.captureException(error)` (error adapter)                             |

| Framework                | Wiring                                                                                                                                                                                                                                                                                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Next.js**              | `AnalyticsProvider` in the root layout (client boundary); call `initFirebaseAnalytics()` in a client effect; vitals via `useReportWebVitals`.                                                                                                                                                                                                                 |
| **React + Vite / Remix** | provider at app root; `initFirebaseAnalytics()` + `reportWebVitals()` in a top-level effect.                                                                                                                                                                                                                                                                  |
| **Expo / React Native**  | swap the web-vitals source for RN performance APIs and the web provider scripts for native SDKs (**`@react-native-firebase/analytics`**, Amplitude, PostHog-RN); the **taxonomy, `track` fan-out, consent gate, and `useAnalytics` hook are unchanged**. The Firebase adapter is the same shape — it guards the native module instead of `window` (see §3.1). |

---

## 9. 规范检查清单（review 时强制执行）

- [ ] 事件名是带联合类型的规范常量——零内联事件字符串。
- [ ] `track()` 是唯一入口；通过 `useAnalytics()` 调用（无 provider / SSR 环境下为 no-op）。
- [ ] 每个 adapter 都对自身 provider 全局加以守卫，并在缺失或服务端时 no-op。
- [ ] 每次 adapter 调用都单独包裹 try/catch——一个 provider 不能拖垮应用或其他 provider。
- [ ] 同意在扇出边界统一检查一次；授权前不触发任何上报。
- [ ] `props` 保持轻量（id/枚举，不用邮箱/姓名）；错误报告必须清除 PII。
- [ ] 真实用户的 Web Vitals 通过同一个扇出上报，沿用 lighthouse 技能的指标和阈值。
- [ ] 错误边界按路由/分段放置，仅上报意外错误。
- [ ] Provider 在渲染期不做任何工作；上下文值通过 useMemo 稳定。
- [ ] 测试中通过替换 adapter 注册表来观察分发——测试中不挂载真实 provider。

---

## 10. 如何应用本技能

**为项目加入分析能力：** 创建 `constants/analytics.ts`（分类体系）、`services/analytics/`（track + adapters + consent）和 `AnalyticsProvider`。在根部挂载 provider；在薄薄的客户端组件中包装需要埋点的叶子节点。

**新增事件：** 先在 `ANALYTICS_EVENTS` 中加一个常量，然后在交互位置调用 `track(ANALYTICS_EVENTS.NEW_ONE, props)`。绝不使用内联字符串。

**接入 Firebase Analytics（Web + RN）：** 通过第 3.1 节的平台相关文件往注册表里加入 `firebaseAdapter`（Web 端使用 `firebase/analytics`，由仅浏览器初始化的 `initFirebaseAnalytics()` 包裹；原生端使用 `@react-native-firebase/analytics`）。将初始化门控于用户同意之后。分类体系和扇出保持不变——Firebase 仅仅是 `analyticsAdapters` 中的又一个条目。

**打通实验室/现场闭环：** 接入 `reportWebVitals()`，将现场评级与 lighthouse 技能预算进行对比；调查所有"实验室绿 / 现场差"的差距。

**审查可观测性：** 运行第 9 节的清单。最有价值的抓取点是：内联事件字符串（分类体系漂移）、未加守卫的 adapter（可能拖垮应用的 provider）以及在同意前触发遥测的情况。

---

## 发布与安装本技能

本技能遵循 Anthropic 的 `SKILL.md` 格式，可在各 agent 间移植。

1. 放在公共 GitHub 仓库的 `skills/frontend-observability/SKILL.md` 路径下。
2. 保留 frontmatter 中的 `name` 和高信号的 `description`——发现索引依赖它们进行匹配。
3. 通过以下命令安装：`npx skills add <org>/<repo> --skill "frontend-observability"`。
4. 非 `SKILL.md` 形式的 agent 可以通过 `AGENTS.md` / `CLAUDE.md` 指向此处；Kiro 可以将其镜像为 steering 文件。

## 局限性

- 仅当任务明确匹配其上游来源及本地项目上下文时使用本技能。
- 在应用改动前，验证命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作特定环境测试、安全审查或用户对破坏性/高成本操作的授权的替代品。
