# Next.js 中的视图过渡

## 设置

`<ViewTransition>` 对 `startTransition` / `Suspense` 更新开箱即用。若希望同时为 `<Link>` 导航制作动画：

```js
// next.config.js
const nextConfig = {
  experimental: { viewTransition: true },
};
module.exports = nextConfig;
```

它会把每一次 `<Link>` 导航包到 `document.startViewTransition` 之中。任何带有 `default="auto"` 的 VT 都会在**每一次**链接点击时触发 —— 用 `default="none"` 来防止动画相互竞争。

不要安装 `react@canary` —— 详见 SKILL.md 中"可用性"一节。

---

## Next.js 实施的补充

在执行 `implementation.md` 时，请叠加以下补充：

**第 2 步之后：** 启用上面所述的 experimental 标志。

**第 4 步：** 在 `<Link>` 上使用 `transitionTypes` —— 用法和可用性请参见下方 "`transitionTypes` 属性" 一节。

**第 6 步之后：** 对于同路由的动态段（例如 `/collection/[slug]`），使用 `key` + `name` + `share` 模式 —— 参见下方"同路由动态段过渡"。

---

## 布局级的 ViewTransition

**如果页面拥有自己的 VT，就不要在布局里加一个包裹 `{children}` 的布局级 VT。** 嵌套在父级 VT 里的 VT 永远不会触发 enter/exit —— 页面级的 enter/exit 会静默失效。请彻底移除布局里的 VT。

只有当页面**完全没有**自己的 VT 时，布局里那个裸露的 `<ViewTransition>` 才能工作。

**布局在导航之间是持续存在的** —— `enter` / `exit` 只在初始挂载时触发，而不会在路由切换时触发。不要在布局里使用按类型键控的映射。

---

## `next/link` 上的 `transitionTypes` 属性

无需包装组件，且能在 Server Components 中使用：

```tsx
<Link href="/products/1" transitionTypes={['transition-to-detail']}>View Product</Link>
```

它替代了 `onNavigate` + `startTransition` + `addTransitionType` + `router.push()` 这一套手动组合。把手动的 `startTransition` 留给非链接交互（按钮、表单）。

**可用性：** `transitionTypes` 需要 `experimental.viewTransition: true`，并且在 Next.js 15+ canary 版本与 Next.js 16+ 中可用。如果不可用，请回退到 `startTransition` + `addTransitionType` + `router.push()`（见下方"程序化导航"）。检查方式：`grep -r "transitionTypes" node_modules/next/dist/` —— 如果没有结果，就回退到程序化导航。

---

## 程序化导航

```tsx
'use client';

import { useRouter } from 'next/navigation';
import { startTransition, addTransitionType } from 'react';

function handleNavigate(href: string) {
  const router = useRouter();
  startTransition(() => {
    addTransitionType('nav-forward');
    router.push(href);
  });
}
```

---

## 使用 `router.replace` 进行服务端过滤

对于在服务端（通过 URL 参数）触发重新渲染的搜索 / 排序 / 过滤场景，使用 `startTransition` + `router.replace`。由于状态更新位于 `startTransition` 之内，VT 会被激活：

```tsx
'use client';

import { useRouter } from 'next/navigation';
import { startTransition } from 'react';

function handleSort(sort: string) {
  const router = useRouter();
  startTransition(() => {
    router.replace(`?sort=${sort}`);
  });
}
```

被 `<ViewTransition key={item.id}>` 包裹的列表项会播放重排动画。这是 `patterns.md` 中 `useDeferredValue` 客户端模式对应的服务端组件版本。

---

## 双层模式（方向性 + Suspense）

方向性滑动 + Suspense 揭示之所以能共存，是因为它们的触发时机不同。把方向性 VT 放在**页面组件**中（而不是布局中）：

```tsx
<ViewTransition
  enter={{ "nav-forward": "slide-from-right", default: "none" }}
  exit={{ "nav-forward": "slide-to-left", default: "none" }}
  default="none"
>
  <div>
    <Suspense fallback={<ViewTransition exit="slide-down"><Skeleton /></ViewTransition>}>
      <ViewTransition enter="slide-up" default="none"><Content /></ViewTransition>
    </Suspense>
  </div>
</ViewTransition>
```

---

## 把 `loading.tsx` 当作 Suspense 边界

Next.js 的 `loading.tsx` 就是一个隐式的 `<Suspense>` 边界。在 `loading.tsx` 中用 `<ViewTransition exit="...">` 包住骨架，在 page 中用 `<ViewTransition enter="..." default="none">` 包住内容：

```tsx
// loading.tsx
<ViewTransition exit="slide-down"><PhotoGridSkeleton /></ViewTransition>

// page.tsx
<ViewTransition enter="slide-up" default="none"><PhotoGrid photos={photos} /></ViewTransition>
```

规则与显式 `<Suspense>` 相同：使用简单的字符串属性（不要使用类型映射），因为 Suspense 揭示触发的过渡不携带 transition types。

---

## 跨路由的共享元素

```tsx
// List page
{products.map((product) => (
  <Link key={product.id} href={`/products/${product.id}`} transitionTypes={['nav-forward']}>
    <ViewTransition name={`product-${product.id}`}>
      <Image src={product.image} alt={product.name} width={400} height={300} />
    </ViewTransition>
  </Link>
))}

// Detail page — same name
<ViewTransition name={`product-${product.id}`}>
  <Image src={product.image} alt={product.name} width={800} height={600} />
</ViewTransition>
```

---

## 同路由动态段过渡

当在同一条路由的不同动态段之间导航时（例如 `/collection/[slug]`），页面会保持挂载 —— enter/exit 永远不会触发。请使用 `key` + `name` + `share`：

```tsx
<Suspense fallback={<Skeleton />}>
  <ViewTransition key={slug} name={`collection-${slug}`} share="auto" default="none">
    <Content slug={slug} />
  </ViewTransition>
</Suspense>
```

- `key={slug}` 在变化时强制卸载 / 重新挂载
- `name` + `share="auto"` 创建共享元素的交叉淡入淡出
- 把 VT 放在 `<Suspense>` 之内（不显式给 Suspense 加 key）可以在加载期间保持旧内容可见

---

## Server Components

- `<ViewTransition>` 在 Server Components 与 Client Components 中都能工作
- `<Link transitionTypes>` 在 Server Components 中也可用 —— 不需要 `'use client'`
- 用于程序化导航的 `addTransitionType` 和 `startTransition` 需要 Client Components