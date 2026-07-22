---
name: vercel-react-view-transitions
description: "指导 React 与 Next.js 的视图过渡、共享元素动画、路由过渡、过渡类型以及支持 prefers-reduced-motion 的 UI 状态动画。涉及视图过渡、共享元素动画、路由过渡、transition types、reduced-motion 等主题时使用。"
risk: safe
source: "https://github.com/vercel-labs/agent-skills"
date_added: "2026-06-02"
---

# React 视图过渡

使用浏览器原生的 `document.startViewTransition` 在 UI 状态之间制作动画。用 `<ViewTransition>` 声明*内容*，用 `startTransition` / `useDeferredValue` / `Suspense` 决定*时机*，用 CSS 类控制*方式*。不支持的浏览器会优雅地跳过动画。

## 适用场景
- 涉及以下描述时使用此技能：指导 React 与 Next.js 的视图过渡、共享元素动画、路由过渡、过渡类型以及支持 prefers-reduced-motion 的 UI 状态动画。

## 何时添加动画

每个 `<ViewTransition>` 都应表达某种空间关系或连续性。如果你说不出它在表达什么，就不要加。

按以下顺序实现**所有**适用的模式：

| 优先级 | 模式 | 表达的含义 |
|----------|---------|---------------------|
| 1 | **共享元素**（`name`） | "同一对象 —— 进入下一层" |
| 2 | **Suspense 揭示** | "数据加载完成" |
| 3 | **列表标识**（按项 `key`） | "同一批项，重新排列" |
| 4 | **状态变化**（`enter`/`exit`） | "某物出现或消失" |
| 5 | **路由变化**（布局级） | "进入新位置" |

这是一个实现顺序，不是"二选一"的清单。实现所有契合应用的模式。只有当应用确实没有对应用例时才跳过某条。

### 选择动画风格

| 场景 | 动画 | 原因 |
|---------|-----------|-----|
| 层级导航（列表 → 详情） | 按类型键控的 `nav-forward` / `nav-back` | 表达空间深度 |
| 横向导航（标签之间） | 裸 `<ViewTransition>`（淡入淡出）或 `default="none"` | 不存在需要表达的深度 |
| Suspense 揭示 | `enter`/`exit` 字符串属性 | 内容正在呈现 |
| 重新校验 / 后台刷新 | `default="none"` | 静默 —— 不需要动画 |

把方向性滑动留给层级导航（列表 → 详情）以及有序序列（上一张/下一张照片、轮播、分页结果）。对于有序序列，方向传达位置信息："下一张"从右滑入，"上一张"从左滑入。横向 / 无序导航（标签之间）不应使用方向性滑动 —— 它会错误地暗示空间深度。

---

## 可用性

- **Next.js：** 不要安装 `react@canary` —— App Router 内部已捆绑 React canary。`ViewTransition` 开箱即用。`npm ls react` 可能显示一个看起来像稳定版的版本号；这是正常现象。
- **不使用 Next.js：** 安装 `react@canary react-dom@canary`（`ViewTransition` 不在稳定版 React 中）。
- 浏览器支持：Chromium 111+、Firefox 144+、Safari 18.2+。在不支持的浏览器上优雅降级。

---

## 实施工作流

向已有应用添加视图过渡时，**按步骤执行 `references/implementation.md`**。从审计开始 —— 不要跳过它。把 `references/css-recipes.md` 中的 CSS 配方复制到全局样式表 —— 不要自行编写动画 CSS。

---

## 核心概念

### `<ViewTransition>` 组件

```jsx
import { ViewTransition } from 'react';

<ViewTransition>
  <Component />
</ViewTransition>
```

React 会自动分配一个唯一的 `view-transition-name`，并在内部调用 `document.startViewTransition`。永远不要自行调用 `startViewTransition`。

### 动画触发器

| 触发器 | 触发时机 |
|---------|--------------|
| **enter** | 在一次过渡中 `<ViewTransition>` 首次被插入 |
| **exit** | 在一次过渡中 `<ViewTransition>` 首次被移除 |
| **update** | `<ViewTransition>` 内部的 DOM 变更。对于嵌套的 VT，变更作用于最内层 |
| **share** | 命名的 VT 卸载，同时另一个同名 VT 在同一次过渡中挂载 |

只有 `startTransition`、`useDeferredValue` 或 `Suspense` 才能激活 VT。普通的 `setState` 不会触发动画。

### 关键放置规则

`<ViewTransition>` 只有出现在**任何 DOM 节点之前**时才能激活 enter/exit：

```jsx
// Works
<ViewTransition enter="auto" exit="auto">
  <div>Content</div>
</ViewTransition>

// Broken — div wraps the VT, suppressing enter/exit
<div>
  <ViewTransition enter="auto" exit="auto">
    <div>Content</div>
  </ViewTransition>
</div>
```

---

## 使用视图过渡类进行样式化

### Props

取值：`"auto"`（浏览器交叉淡入淡出）、`"none"`（禁用）、`"class-name"`（自定义 CSS），或 `{ [type]: value }` 用于按类型触发的动画。

```jsx
<ViewTransition default="none" enter="slide-in" exit="slide-out" share="morph" />
```

如果 `default` 为 `"none"`，除非显式列出，否则所有触发器都关闭。

### CSS 伪元素

- `::view-transition-old(.class)` —— 离场快照
- `::view-transition-new(.class)` —— 入场快照
- `::view-transition-group(.class)` —— 容器
- `::view-transition-image-pair(.class)` —— 新旧对

可用的动画配方见 `references/css-recipes.md`。

---

## 过渡类型

用 `addTransitionType` 给过渡打标签，让 VT 能根据上下文选择不同的动画。可以多次调用以叠加类型 —— 树中不同的 VT 会响应不同的类型：

```jsx
startTransition(() => {
  addTransitionType('nav-forward');
  addTransitionType('select-item');
  router.push('/detail/1');
});
```

传入对象可以把类型映射到 CSS 类。适用于 `enter`、`exit` **和** `share`：

```jsx
<ViewTransition
  enter={{ 'nav-forward': 'slide-from-right', 'nav-back': 'slide-from-left', default: 'none' }}
  exit={{ 'nav-forward': 'slide-to-left', 'nav-back': 'slide-to-right', default: 'none' }}
  share={{ 'nav-forward': 'morph-forward', 'nav-back': 'morph-back', default: 'morph' }}
  default="none"
>
  <Page />
</ViewTransition>
```

`enter` 和 `exit` 不必对称。例如，淡入但按方向滑出：

```jsx
<ViewTransition
  enter={{ 'nav-forward': 'fade-in', 'nav-back': 'fade-in', default: 'none' }}
  exit={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
  default="none"
>
```

**TypeScript：** `ViewTransitionClassPerType` 要求对象里包含一个 `default` 键。

对于多页面的应用，把按类型键控的 VT 抽成一个可复用的包装器：

```jsx
export function DirectionalTransition({ children }: { children: React.ReactNode }) {
  return (
    <ViewTransition
      enter={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      exit={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      default="none"
    >
      {children}
    </ViewTransition>
  );
}
```

### `router.back()` 与浏览器后退按钮

`router.back()` 和浏览器的后退/前进按钮**不会**触发视图过渡（`popstate` 是同步的，与 `startViewTransition` 不兼容）。请改用带显式 URL 的 `router.push()`。

### 类型与 Suspense

类型在导航期间可用，但在后续的 Suspense 揭示中**不可用**（属于独立的过渡，不携带类型）。页面级 enter/exit 使用类型映射；Suspense 揭示使用简单的字符串属性。

---

## 共享元素过渡

在两个 VT 上使用相同的 `name` —— 一个卸载、一个挂载 —— 即可创建一个共享元素变形：

```jsx
<ViewTransition name="hero-image">
  <img src="/thumb.jpg" onClick={() => startTransition(() => onSelect())} />
</ViewTransition>

// On the other view — same name
<ViewTransition name="hero-image">
  <img src="/full.jpg" />
</ViewTransition>
```

- 同一时刻只能挂载一个具有给定 `name` 的 VT —— 使用唯一名称（`photo-${id}`）。注意可复用组件：如果一个带命名 VT 的组件同时在模态/弹层*和*页面中渲染，两个会同时挂载，破坏变形效果。要么让名称根据 prop 条件化，要么把命名 VT 从共享组件中挪到具体消费者。
- `share` 的优先级高于 `enter`/`exit`。请逐一审视每条导航路径：当没有匹配对形成时（例如目标页面没有相同的 name），就会触发 `enter`/`exit`。考虑是否需要为这些路径准备回退动画。
- 在带有共享变形动画的页面上，永远不要使用淡出式的 exit —— 应改用方向性滑动。

---

## 常见模式

### Enter / Exit

```jsx
{show && (
  <ViewTransition enter="fade-in" exit="fade-out"><Panel /></ViewTransition>
)}
```

### 列表重排

```jsx
{items.map(item => (
  <ViewTransition key={item.id}><ItemCard item={item} /></ViewTransition>
))}
```

在 `startTransition` 内部触发。避免在列表与 VT 之间使用包裹性 `<div>`。

### 把共享元素与列表标识组合在一起

共享元素与列表标识是正交的两个关注点 —— 不要混淆。在列表项包含共享元素（例如，变形到详情视图的图片）的场景下，使用两层嵌套的 `<ViewTransition>` 边界：

```jsx
{items.map(item => (
  <ViewTransition key={item.id}>                                      {/* list identity */}
    <Link href={`/items/${item.id}`}>
      <ViewTransition name={`item-image-${item.id}`} share="morph">   {/* shared element */}
        <Image src={item.image} />
      </ViewTransition>
      <p>{item.name}</p>
    </Link>
  </ViewTransition>
))}
```

外层 VT 处理列表重排 / 进入动画。内层 VT 处理跨路由共享元素变形。缺少任何一层都会让对应的动画静默失效。

### 用 `key` 强制重新进入

```jsx
<ViewTransition key={searchParams.toString()} enter="slide-up" default="none">
  <ResultsGrid />
</ViewTransition>
```

**注意：** 如果包裹的是 `<Suspense>`，修改 `key` 会重新挂载该边界并重新请求数据。

### Suspense Fallback → 内容

简单交叉淡入淡出：
```jsx
<ViewTransition>
  <Suspense fallback={<Skeleton />}><Content /></Suspense>
</ViewTransition>
```

方向性揭示：
```jsx
<Suspense fallback={<ViewTransition exit="slide-down"><Skeleton /></ViewTransition>}>
  <ViewTransition enter="slide-up" default="none"><Content /></ViewTransition>
</Suspense>
```

更多模式见 `references/patterns.md`。

---

## 多个 VT 的交互方式

每个匹配触发器的 VT 会在同一次 `document.startViewTransition` 中同时触发。位于**不同**过渡中的 VT（导航 vs 后续的 Suspense 解析）之间不会相互竞争。

### 自由使用 `default="none"`

如果不加 `default="none"`，每一个 VT 在**每一次**过渡中都会触发浏览器交叉淡入淡出 —— Suspense 解析、`useDeferredValue` 更新、后台重新校验。始终使用 `default="none"`，并仅显式启用所需的触发器。

### 两种模式共存

**模式 A —— 方向性滑动：** 在每个页面上使用按类型键控的 VT，在导航期间触发。
**模式 B —— Suspense 揭示：** 使用简单的字符串属性，在数据加载时触发（不带类型）。

它们之所以能共存，是因为触发时机不同。两端都加 `default="none"` 可防止相互干扰。始终让 `enter` 与 `exit` 成对出现。把方向性 VT 放在页面组件中，而不是布局中。

### 嵌套 VT 的限制

当父级 VT 退出时，其内部的嵌套 VT **不会**触发各自的 enter/exit —— 只有最外层的 VT 会播放动画。页面导航期间按项错开的动画目前无法实现。可参考 [react#36135](https://github.com/facebook/react/pull/36135) 了解实验性的 opt-in 修复方案。

---

## Next.js 集成

关于 Next.js 的设置（`experimental.viewTransition` 标志、`next/link` 上的 `transitionTypes` 属性、App Router 模式、Server Components），请参考 `references/nextjs.md`。

---

## 无障碍

务必把 `references/css-recipes.md` 中支持 reduced motion 的 CSS 加入你的全局样式表。

---

## 参考文件

- **`references/implementation.md`** —— 分步的实施工作流。
- **`references/patterns.md`** —— 模式、动画时序、Events API、故障排查。
- **`references/css-recipes.md`** —— 可直接使用的 CSS 动画配方。
- **`references/nextjs.md`** —— Next.js App Router 模式与 Server Component 细节。

## 完整编译文档

包含所有参考文件展开后的完整指南：`AGENTS.md`

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要把输出当作针对具体环境的验证、测试或专家评审的替代品。
- 当所需的输入、权限、安全边界或成功标准缺失时，停下来向用户确认。