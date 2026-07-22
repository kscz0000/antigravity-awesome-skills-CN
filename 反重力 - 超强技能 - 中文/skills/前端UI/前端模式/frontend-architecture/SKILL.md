---
name: frontend-architecture
description: 一种可移植、与框架无关的架构风格，适用于任何 React 或 React Native 前端。以特性模块组织应用，每个模块包含页面/屏幕目录，严格区分服务端状态与 UI 状态，跨模块导入仅通过 barrel 文件，样式就近共置，组件晋升规则清晰。触发词：前端架构、特性模块、模块化前端、React 架构、React Native 架构、barrel 导入、组件晋升、模块化设计、frontend architecture、feature modules、module-based frontend。
risk: unknown
source: https://github.com/stareezy-1/frontend-architecture-skill/tree/main/skills/frontend-architecture
source_repo: stareezy-1/frontend-architecture-skill
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/stareezy-1/frontend-architecture-skill/blob/main/LICENSE
---

# 前端架构（可移植、基于模块）
## 何时使用

当你需要一种可移植、与框架无关的架构风格，应用于任何 React 或 React Native 前端时，请使用本技能。它以特性模块组织应用，每个模块包含页面/屏幕目录，严格区分服务端状态与 UI 状态，跨模块导入仅通过 barrel 文件，样式就近共置，并具备清晰的组件晋升规则。


> 可移植的技能 — 可被 Claude Code、OpenCode、Codex、Cursor、Windsurf 等智能体读取。
> 本技能描述的是**一套结构和一组规则**，而非组件库、状态库或视觉风格。
> 它刻意保持通用：同一套模块/页面/状态模型可以映射到
> **Next.js（App Router）**、**React + Vite（SPA）**、**Remix**，以及 **Expo / React Native**，并且适用于
> **任意**状态管理与样式技术栈。

目标：让任何贡献者都能即时回答三个问题——
**“这段代码应该放在哪里？”**、**“谁可以导入谁？”**、**“这是服务端状态还是 UI 状态？”**——
而无需向他人请教。结构本身让答案显而易见。

---

## 0. 五大核心思想

1. **特性模块拥有自己的全部世界。** 每个特性都是一个自包含的 `modules/{feature}/` 目录，包含自己的页面、组件、hooks、状态、类型，以及一个对外的公共 barrel 文件。
2. **页面/屏幕是目录，而非文件。** 路由是一个文件夹，把它的组件、样式以及仅由它使用的组件/hooks 就近共置在一起。
3. **状态按来源拆分。** 服务端数据存放在 query/cache 层。UI/客户端状态存放在 store 中。两者永不混用 —— 无论你选用哪个库。
4. **跨边界导入只能通过 barrel。** 禁止伸手进入另一个模块的内部；你只能从 `@/modules/{feature}` 导入，而不能更深。
5. **代码是“晋升”出来的，不是预先放好的。** 一开始它尽可能本地化，只有当出现第二个使用者时才向外移动。

下面所有内容都是对这五大思想的具体落地。它们不绑定任何特定库 —— 在第 4 节和第 6 节中挑选你的技术栈。

---

## 1. 目录布局

跨框架的形态完全一致；只是顶层的路由层有所不同（参见第 7 节）。

```
src/
├── app/ or routes/ or navigation/   ← framework routing layer (thin — see §7)
├── modules/                         ← feature modules (the heart of the app)
│   └── {feature}/
│       ├── index.ts                 ← PUBLIC BARREL — the only cross-module entry point
│       ├── README.md                ← what this module owns, its routes, its data deps
│       ├── components/              ← components reused by 2+ pages IN THIS MODULE
│       ├── pages/                   ← page/screen directories (one per route)
│       │   └── {page}/
│       │       ├── {page}.tsx               ← the page/screen component
│       │       ├── {page}.styles.ts         ← ALL styling for this page
│       │       ├── index.ts                 ← re-exports the page component
│       │       ├── components/              ← components used ONLY by this page
│       │       ├── hooks/                   ← hooks used ONLY by this page
│       │       ├── constants/
│       │       └── README.md                ← route, params, permissions, data deps
│       ├── hooks/                   ← data hooks (query/mutation) + module hooks
│       ├── stores/                  ← UI/client state store(s) — never server data
│       ├── services/                ← data-access (API calls) for this feature
│       ├── utils/                   ← pure module utilities (co-located *.test.ts)
│       ├── constants/
│       └── types/                   ← module request/response + view-model types
└── shared/                          ← cross-module building blocks
    ├── components/                  ← components used by 2+ MODULES
    ├── hooks/                       ← cross-cutting hooks
    ├── api-client/                  ← one typed client; the only place that talks to the network
    ├── store/                       ← root store wiring (if your state lib needs one — see §4)
    ├── utils/                       ← formatters, cn()/clsx, helpers
    ├── constants/
    └── types/
```

在脚手架阶段可能为空的所有目录都保留一个 `.gitkeep`，让结构从第一天起就一目了然。

---

## 2. 特性模块

模块是产品的一个纵向切片（例如 `auth`、`billing`、`dashboard`、`settings`）。它包含该特性所需的一切，并刻意暴露一个尽可能小的对外接口。

### 2.1 Barrel（`index.ts`）即契约

`modules/{feature}/index.ts` 是其他模块与路由层**唯一**可以导入的地方。它重新导出：

- 路由挂载的页面/屏幕组件。
- 其他特性确实需要的数据 hooks。
- store hook/slice 及其公共类型。
- 其他特性依赖的公共常量 / 类型。

```ts
// CORRECT — consume the public surface
import { InvoiceListPage, useInvoiceList } from "@/modules/invoice";

// WRONG — reaching into internals couples you to private structure
import { InvoiceListPage } from "@/modules/invoice/pages/invoice-list/invoice-list";
```

请精心维护 barrel 的内容。未导出的部分，默认就是私有的。用简短的注释把导出分组（页面、hooks、store、类型）—— 未来的读者会把 barrel 当作模块的 API 文档。

### 2.2 一个模块 = 一个有界上下文

不要创建 `utils` 模块或 `components` 模块。模块对应的是产品能力，而不是技术分层。技术性的积木块放在 `shared/` 中。

### 2.3 模块 README

每个模块的 `README.md` 应说明：它负责什么、哪些路由渲染它的页面、它的数据依赖（哪些端点/hooks），以及任何跨模块规则。这是新贡献者阅读的第一份文档。

---

## 3. 页面/屏幕以目录形式存在

页面是路由挂载的路由点（在 React Native 中称为“screen”）。它**始终是一个文件夹**，而不是一个散落的文件 —— 即便它最初只是一个组件。这样可以让成长就地发生：当页面需要子组件或 hook 时，那里已经有它的位置。

```
pages/{page}/
├── {page}.tsx          ← the page/screen component
├── {page}.styles.ts    ← every style for this page (no inline styles — see §5)
├── index.ts            ← export { PageComponent } from "./{page}"
├── components/         ← used ONLY by this page
├── hooks/              ← used ONLY by this page
├── constants/
└── README.md           ← route, params, permissions, data deps
```

页面 README 简短且高信号：路由路径、预期的参数、必需的权限/鉴权，以及它依赖的 hooks。它是页面与应用其余部分之间的契约。

**为什么从一开始就使用文件夹：** 一个从单个文件起步的页面，最终必然会长出子行组件、衍生汇总 hook、样式文件。如果页面是一个文件，这些东西就会被随意散落；如果页面是一个文件夹，它们就有了明确的位置，diff 也更易读。

---

## 4. 状态：按来源拆分（不可妥协，与库无关）

两种状态，两种归宿。把它们混在一起是本技能最想避免的、最常见的架构失误。**这种拆分是强制的；具体库由你选择。**

| 状态种类              | 示例                                                                                | 存放位置                                                                                  |
| --------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **服务端状态**        | 获取到的实体、列表、聚合 —— 任何属于 API 的数据                                       | 一个 **query/cache 层**（例如 TanStack Query、RTK Query、SWR、Apollo）                   |
| **UI / 客户端状态**   | 打开的弹窗、表格筛选/排序、向导步骤、正在输入的草稿、预览开关等                          | 一个 **客户端 store**（例如 Zustand、Redux Toolkit、MobX、Jotai、Valtio，或 React Context） |

### 4.1 硬性规则（与库无关）

- **永远不要把服务端的响应镜像到客户端 store 中。** 不要把获取到的实体拷贝到 Zustand/Redux/MobX 里。query/cache 层才是服务端数据的唯一真相来源。
- **永远不要在组件内部直接发起请求。** 组件通过数据 hook 读取服务端数据，通过 store 选择器读取 UI 状态。它不直接调用网络客户端。
- **永远不要把持续变化的值通过 re-render 状态驱动。** 滚动进度、指针位置、拖拽偏移 —— 使用 ref / 动画值，而非 render 状态（后者每一帧都会重渲染整棵组件树）。
- **每个模块一个 store 边界。** 无论你使用什么库，都为每个模块提供一个内聚的 store 单元（Zustand hook、Redux slice、MobX class、Jotai atom 组），并通过模块 barrel 访问。组件只订阅它们所需的最小切片，以避免无谓的重渲染。

### 4.2 选择客户端状态库 —— 形态相同，语法不同

每个项目只挑一个，并保持一致。每种方案都能干净地映射到“每模块一个 store 单元”。注意 **`I` 接口命名约定**：状态接口以 `I` 为前缀（例如 `IFeatureUiState`）。

**Zustand** — `modules/{feature}/stores/{feature}.store.ts`

```ts
import { create } from "zustand";

export interface IFeatureUiState {
  isPreviewOpen: boolean;
  filter: string;
  togglePreview: () => void;
  setFilter: (filter: string) => void;
  reset: () => void;
}

const INITIAL_STATE = { isPreviewOpen: false, filter: "" } as const;

export const useFeatureUiStore = create<IFeatureUiState>()((set) => ({
  ...INITIAL_STATE,
  togglePreview: () => set((s) => ({ isPreviewOpen: !s.isPreviewOpen })),
  setFilter: (filter) => set({ filter }),
  reset: () => set({ ...INITIAL_STATE }),
}));
```

**Redux Toolkit** — `modules/{feature}/stores/{feature}.slice.ts`（在 `shared/store/` 中注册）

```ts
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export interface IFeatureUiState {
  isPreviewOpen: boolean;
  filter: string;
}

const initialState: IFeatureUiState = { isPreviewOpen: false, filter: "" };

export const featureUiSlice = createSlice({
  name: "featureUi",
  initialState,
  reducers: {
    togglePreview: (s) => {
      s.isPreviewOpen = !s.isPreviewOpen;
    },
    setFilter: (s, action: PayloadAction<string>) => {
      s.filter = action.payload;
    },
    reset: () => initialState,
  },
});
```

**MobX** — `modules/{feature}/stores/{feature}.store.ts`

```ts
import { makeAutoObservable } from "mobx";

export interface IFeatureUiState {
  isPreviewOpen: boolean;
  filter: string;
}

export class FeatureUiStore implements IFeatureUiState {
  isPreviewOpen = false;
  filter = "";
  constructor() {
    makeAutoObservable(this);
  }
  togglePreview = () => {
    this.isPreviewOpen = !this.isPreviewOpen;
  };
  setFilter = (filter: string) => {
    this.filter = filter;
  };
  reset = () => {
    this.isPreviewOpen = false;
    this.filter = "";
  };
}
```

**Jotai** — `modules/{feature}/stores/{feature}.atoms.ts`

```ts
import { atom } from "jotai";
export const isPreviewOpenAtom = atom(false);
export const filterAtom = atom("");
```

> 无论选择哪一个，请保持 §4.1 的规则不变。本技能关心的是服务端状态与 UI 状态相互分离、且每个模块拥有一个 store 单元 —— 而不是哪个库来“画出框”。

### 4.3 数据层（服务端状态）

所有网络访问都通过 `shared/api-client/` 中的**一个强类型客户端**。模块把它包装为 query/mutation hooks，并配以 **key factory**，让缓存与失效保持一致。

```ts
// modules/invoice/hooks/invoiceKeys.ts — hierarchical key factory (TanStack Query style)
export const invoiceKeys = {
  all: ["invoices"] as const,
  lists: () => [...invoiceKeys.all, "list"] as const,
  list: (params: IListParams) => [...invoiceKeys.lists(), params] as const,
  details: () => [...invoiceKeys.all, "detail"] as const,
  detail: (id: string) => [...invoiceKeys.details(), id] as const,
} as const;
```

让 `lists()` 失效会刷新每一个筛选后的页面；`detail(id)` 则只针对某一个实体。（RTK Query/SWR/Apollo 用 tag/key 表达同样的思路。）组件绝不直接写裸 `fetch()` —— 它们调用 `useInvoiceList()` / `useCreateInvoice()`。

---

## 5. 样式：就近共置，禁止内联样式（与样式库无关）

把样式放在 JSX 之外、组件主体之外。每个页面或组件都有一个**就近共置的样式文件**。规则不变；语法跟随你选用的样式技术栈。

- **Tailwind（web）：** `{name}.styles.ts` 导出由 `cn()`（clsx + tailwind-merge）组合的具名字符串；变体通过 `cva`。JSX 引用 `styles.header`。
- **CSS Modules / vanilla-extract：** 共置一个 `{name}.module.css` / `{name}.css.ts`；JSX 引用 `styles.header`。
- **styled-components / Emotion：** 共置一个 `{name}.styles.ts`，导出 styled 组件。
- **Tamagui（web + native）：** 共置一个 `{name}.styles.ts`，导出 `styled(...)` 组件，或 `createStyledContext` / `useStyle` token 集合；引用 Tamagui tokens（`$background`、`$space.4`）—— 绝不内联硬编码值。当你的代码库需要**同时覆盖 web 与 React Native** 时，推荐使用 Tamagui。
- **React Native StyleSheet / Nativewind：** 共置一个 `{name}.styles.ts`，导出 `StyleSheet.create({...})`（或 Nativewind 类名）。JSX 引用 `styles.header`。

```ts
// invoice-list.styles.ts (Tailwind example)
export const invoiceListStyles = {
  page: "flex flex-col gap-8",
  header: "flex flex-col gap-1.5",
  title: "text-3xl font-semibold tracking-tight",
} as const;
```

```ts
// invoice-list.styles.ts (Tamagui example — works on web AND native)
import { styled, YStack, Text } from "tamagui";

export const InvoiceListPage = styled(YStack, { flex: 1, gap: "$8" });
export const InvoiceListHeader = styled(YStack, { gap: "$1.5" });
export const InvoiceListTitle = styled(Text, {
  fontSize: "$8",
  fontWeight: "600",
});
```

**在任何技术栈下，组件主体中都不允许出现内联 `style={{...}}` 字面量。** 原因：当样式内联时，它会漂移并重复出现。一个就近共置的样式文件让间距节奏、主题正确性、响应式行为都能在一个地方被审查。请把那些不直观的选择（强调色锁定、断点等）以注释形式记录在那里。

本技能不规定**视觉**层面的设计 —— 那需要与设计/组件技能搭配使用。它只规定**样式应该放在哪里**。

---

## 6. 命名约定

一致的命名让结构自带说明性。

- **接口以 `I` 为前缀** — `IFeatureUiState`、`IInvoiceListParams`、`IUserProfile`。类型别名（联合类型、映射类型、原始类型）**不加**前缀（`type SortDirection = "asc" | "desc"`）。
- **组件**：文件名与导出名采用 `PascalCase` — `InvoiceListPage.tsx`、`LineItemRow.tsx`。
- **页面/屏幕**：目录采用 `kebab-case`，组件文件名与之对应 — `pages/invoice-list/invoice-list.tsx`。
- **Hooks**：采用 `useCamelCase` — `useInvoiceList`、`useFeatureUiStore`。
- **Stores**：`{feature}.store.ts`（Zustand/MobX），`{feature}.slice.ts`（Redux），`{feature}.atoms.ts`（Jotai）。Hook 命名为 `use{Feature}{Purpose}Store`。
- **Styles**：`{name}.styles.ts`，与其所有者就近共置。
- **Constants**：值采用 `SCREAMING_SNAKE_CASE`；文件名采用 `kebab-case` 或 `camelCase`。
- **Barrels**：始终使用 `index.ts`。

---

## 7. 框架适配器

模块/页面/状态模型始终不变。只有顶层的薄路由层会变。页面始终位于 `modules/` 中；路由层只是**挂载**它们。

### 7.1 Next.js（App Router）

- `src/app/` 存放路由段与路由组（`(marketing)`、`(app)`、`(public)`），用于布局/鉴权边界。路由文件保持精简：从模块 barrel 导入页面组件并渲染即可。
- 默认使用 **Server Components**；将需要交互的叶子节点标记为 `"use client"`。Providers（query client、store、主题）放在 `"use client"` 边界内。

```tsx
// app/(app)/invoices/page.tsx — thin route file
import { InvoiceListPage } from "@/modules/invoice";
export default function Page() {
  return <InvoiceListPage />;
}
```

### 7.2 React + Vite（SPA）

- 一个 `src/routes/`（或单一的 `router.tsx`）声明路由表（React Router / TanStack Router），把路径映射到模块的页面组件。一切都在客户端完成。在应用根节点用 query-client 与 store/theme providers 包裹一次整棵树。

### 7.3 Remix

- `app/routes/` 中的路由模块保持精简，仅重新导出/挂载模块的页面组件；loader/action 委托给模块的 `services/`。模块边界不变。

### 7.4 Expo / React Native

- 路由采用 **Expo Router**（基于文件，位于 `app/`）或 React Navigation（`navigation/`）。路由/screen 文件保持精简，从模块 barrel 导入 screen 组件。
- “Pages” 即 “screens” —— 同样的目录模式：`pages/{screen}/{screen}.tsx` + `{screen}.styles.ts`。
- Query 层与客户端 store 原样工作（TanStack Query、Zustand、Redux、MobX、Jotai 在 RN 中都可用）。强类型的 `api-client` 是共享逻辑，开箱即用。
- 样式采用 **Tamagui**（推荐用于共享 web+native）、`StyleSheet` 或 Nativewind。保持模块逻辑与 DOM 解耦。

```tsx
// app/invoices/index.tsx (Expo Router) — thin screen file
import { InvoiceListScreen } from "@/modules/invoice";
export default InvoiceListScreen;
```

### 7.5 在 web + native 之间共享代码

如果你的目标是同时覆盖 web 与 Expo，请将与框架无关的代码（类型、校验器、格式化器、API 客户端契约）下沉到一个共享包，供两端应用消费；对于必须在两端都能渲染的组件，优先选用 **Tamagui**。模块边界在两端保持一致。

---

## 8. 约定清单（评审中强制执行）

- [ ] 新增特性 → 新建 `modules/{feature}/`，包含 `index.ts` + `README.md`，而不是把文件零散丢到 `shared/`。
- [ ] 新增路由 → 一个**页面/屏幕目录**（`{page}.tsx` + `{page}.styles.ts` + `index.ts` + `README.md`），而不是一个散落的文件。
- [ ] 跨模块导入一律走 barrel（`@/modules/{feature}`）—— 禁止使用深层内部路径。
- [ ] 服务端数据放在 query/cache 层；UI 状态放在模块 store；**两者互不渗透**（无论选择什么库）。
- [ ] 组件中不允许出现 `fetch()` —— 只能使用基于共享客户端的强类型数据 hooks。
- [ ] 禁止内联样式 — 使用就近共置的 `{name}.styles.ts`（Tailwind/CSS Modules/Tamagui/StyleSheet/styled-components）。
- [ ] 组件/hooks/utils 放在尽可能小的范围内；只有当出现第二个使用者时才提升。
- [ ] 每模块一个 store 单元，通过 barrel 访问，并提供选择器与 `reset`。
- [ ] 接口使用 `I` 前缀；组件/hooks/文件命名遵循 §6。
- [ ] Query keys/tags 由每模块的 factory 派生；失效按层级进行。
- [ ] 路由文件保持精简 —— 仅挂载模块页面，并只承担布局/鉴权边界。
- [ ] 当路由、参数或数据依赖发生变化时，更新模块/页面 README。

---

## 9. 组件晋升（先本地，再向外）

一个组件诞生于使用它的最窄作用域中，只有当出现第二个使用者时才**晋升**。永远不要“因为它可能被复用”就预先放置它。

| 被以下对象使用的组件    | 存放位置                          | 导入方式                              |
| ---------------------- | --------------------------------- | ---------------------------------- |
| 仅一个页面              | `pages/{page}/components/`        | 页面内的相对路径                       |
| 同一模块的 2+ 个页面     | `modules/{feature}/components/`   | `@/modules/{feature}`（经 barrel）  |
| 跨 2+ 个模块            | `shared/components/`              | `@/shared/...`                      |
| 跨 2+ 个应用/仓库        | 一个已发布的设计系统包             | 包名                                 |

同样的阶梯也适用于 **hooks**、**utils** 和 **constants**：本地 → 模块 → shared → 包。晋升是一个刻意的动作（更新导入位置），而不是一开始就凭直觉拍脑袋。

---

## 10. 如何应用本技能

**为一个新应用搭建脚手架：** 创建 `src/modules/`、`src/shared/` 以及框架路由层（§7）。加入共享的 `api-client`、query 层以及你选定的客户端 store provider。把一个 store 模板放入第一个模块。

**添加一个特性：** 创建 `modules/{feature}/`，包含完整的子目录集合（`pages/ components/ hooks/ stores/ services/ utils/ constants/ types/`）、一个精心维护的 `index.ts`，以及一份 `README.md`。把第一个 screen 作为页面目录来构建。

**决定代码放在哪里：** 问“谁会消费它？” → 选最窄的作用域（§9）。问“这份数据从哪里来？” → 服务端 = query 层，UI = store（§4）。

**审查结构：** 运行 §8 中的清单。最有价值的发现是“状态来源的渗透”（服务端数据进了客户端 store）以及“深层跨模块导入”（绕过 barrel）—— 这两类问题会让架构被侵蚀得最快。

---

## 发布 / 安装本技能

本技能遵循 Anthropic 的 `SKILL.md` 格式，跨智能体可移植。要让它可安装、可被检索（例如在 skills.sh / `npx skills` 上）：

1. 将本目录放到一个**公开 GitHub 仓库**下的 `skills/` 目录中（路径形如 `skills/frontend-architecture/SKILL.md`）。
2. 保留 frontmatter 中的 `name` 与一段高信号的 `description`（如上）—— 检索索引就是匹配这段 description。
3. 在任意项目中通过以下命令安装：`npx skills add <org>/<repo> --skill "frontend-architecture"`。
4. 非 `SKILL.md` 的智能体可以从 `AGENTS.md` / `CLAUDE.md` 指向本文件；Kiro 可以把它镜像为 steering file。

## 局限性

- 仅当任务明确匹配其上游来源与本地项目上下文时，才使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要把示例当作环境专属测试、安全审查，或用户对破坏性/高代价操作的授权的替代品。