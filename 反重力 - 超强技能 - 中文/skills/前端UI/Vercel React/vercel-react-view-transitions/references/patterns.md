# 模式与准则

## 使用 `useDeferredValue` 实现可搜索的网格

`useDeferredValue` 会把过滤更新变成一次 transition，从而激活 `<ViewTransition>`：

```tsx
'use client';

import { useDeferredValue, useState, ViewTransition, Suspense } from 'react';

export default function SearchableGrid({ itemsPromise }) {
  const [search, setSearch] = useState('');
  const deferredSearch = useDeferredValue(search);

  return (
    <>
      <input value={search} onChange={(e) => setSearch(e.currentTarget.value)} />
      <ViewTransition>
        <Suspense fallback={<GridSkeleton />}>
          <ItemGrid itemsPromise={itemsPromise} search={deferredSearch} />
        </Suspense>
      </ViewTransition>
    </>
  );
}
```

在延迟列表里给每项加 `<ViewTransition name={...}>` 会在每次按键时触发交叉淡入淡出。用 `default="none"` 修复：

```tsx
{filteredItems.map(item => (
  <ViewTransition key={item.id} name={`item-${item.id}`} share="morph" default="none">
    <ItemCard item={item} />
  </ViewTransition>
))}
```

## 使用 `startTransition` 实现卡片展开 / 折叠

通过共享元素变形在网格视图和详情视图之间切换：

```tsx
'use client';

import { useState, useRef, startTransition, ViewTransition } from 'react';

export default function ItemGrid({ items }) {
  const [expandedId, setExpandedId] = useState(null);
  const scrollRef = useRef(0);

  return expandedId ? (
    <ViewTransition enter="slide-in" name={`item-${expandedId}`}>
      <ItemDetail
        item={items.find(i => i.id === expandedId)}
        onClose={() => {
          startTransition(() => {
            setExpandedId(null);
            setTimeout(() => window.scrollTo({ behavior: 'smooth', top: scrollRef.current }), 100);
          });
        }}
      />
    </ViewTransition>
  ) : (
    <div className="grid grid-cols-3 gap-4">
      {items.map(item => (
        <ViewTransition key={item.id} name={`item-${item.id}`}>
          <ItemCard
            item={item}
            onSelect={() => {
              scrollRef.current = window.scrollY;
              startTransition(() => setExpandedId(item.id));
            }}
          />
        </ViewTransition>
      ))}
    </div>
  );
}
```

## 类型安全的过渡辅助函数

使用 `as const` 数组和派生的类型来防止 ID 冲突：

```tsx
const transitionTypes = ['default', 'transition-to-detail', 'transition-to-list'] as const;
const animationTypes = ['auto', 'none', 'animate-slide-from-left', 'animate-slide-from-right'] as const;

type TransitionType = (typeof transitionTypes)[number];
type AnimationType = (typeof animationTypes)[number];
type TransitionMap = { default: AnimationType } & Partial<Record<Exclude<TransitionType, 'default'>, AnimationType>>;

export function HorizontalTransition({ children, enter, exit }: {
  children: React.ReactNode;
  enter: TransitionMap;
  exit: TransitionMap;
}) {
  return <ViewTransition enter={enter} exit={exit}>{children}</ViewTransition>;
}
```

## 不重新挂载的交叉淡入淡出

省略 `key` 即可触发一次 update（交叉淡入淡出），而非 exit + enter。能避免 Suspense 重新挂载 / 重新请求：

```jsx
<ViewTransition>
  <TabPanel tab={activeTab} />
</ViewTransition>
```

当内容标识发生变化（状态重置）时使用 `key`。在需要交叉淡入淡出的场景（标签、面板、轮播）下省略它。

## 把元素从父级动画中隔离出去

### 持续存在的布局元素

持续存在的元素（顶栏、导航栏、侧栏）会被捕获到页面的过渡快照中。用 `viewTransitionName` 来修复：

```jsx
<nav style={{ viewTransitionName: "persistent-nav" }}>{/* ... */}</nav>
```

然后在样式表中添加 `css-recipes.md` 中"持续元素隔离"的 CSS。对于 `backdrop-blur` / `backdrop-filter`，请使用 `css-recipes.md` 中提供的 backdrop-blur 解决方案。

### 浮动元素

给浮层 / 工具提示自己的 `view-transition-name`：

```jsx
<SelectPopover style={{ viewTransitionName: 'popover' }}>{options}</SelectPopover>
```

全局修复办法：见 `css-recipes.md` 中的持续元素隔离。

## 在骨架屏与内容之间共享控件

让 fallback 和内容里对应的控件拥有相同的 `viewTransitionName`：

```jsx
// Fallback
<input disabled placeholder="Search..." style={{ viewTransitionName: 'search-input' }} />
// Content
<input placeholder="Search..." style={{ viewTransitionName: 'search-input' }} />
```

不要在 `<ViewTransition>` 内部的根 DOM 节点上手动设置 `viewTransitionName` —— React 自动生成的名称会覆盖它。

## 可复用的折叠动画

```jsx
function AnimatedCollapse({ open, children }) {
  if (!open) return null;
  return (
    <ViewTransition enter="expand-in" exit="collapse-out">
      {children}
    </ViewTransition>
  );
}

// Usage: toggle with startTransition
<button onClick={() => startTransition(() => setOpen(o => !o))}>Toggle</button>
<AnimatedCollapse open={open}><SectionContent /></AnimatedCollapse>
```

## 使用 Activity 保留状态

```jsx
<Activity mode={isVisible ? 'visible' : 'hidden'}>
  <ViewTransition enter="slide-in" exit="slide-out">
    <Sidebar />
  </ViewTransition>
</Activity>
```

## 用 `useOptimistic` 排除元素

`useOptimistic` 的值会在过渡快照之前更新，从而被排除在动画之外。控件（如标签）使用乐观值；动画内容使用已提交状态：

```tsx
const [sort, setSort] = useState('newest');
const [optimisticSort, setOptimisticSort] = useOptimistic(sort);

function cycleSort() {
  const nextSort = getNextSort(optimisticSort);
  startTransition(() => {
    setOptimisticSort(nextSort);  // before snapshot — no animation
    setSort(nextSort);            // between snapshots — animates
  });
}

<button>Sort: {LABELS[optimisticSort]}</button>
{items.sort(comparators[sort]).map(item => (
  <ViewTransition key={item.id}><ItemCard item={item} /></ViewTransition>
))}
```

---

## 视图过渡事件

通过 `onEnter`、`onExit`、`onUpdate`、`onShare` 进行命令式控制。始终返回一个清理函数。`onShare` 的优先级高于 `onEnter` / `onExit`。

```jsx
<ViewTransition
  onEnter={(instance, types) => {
    const anim = instance.new.animate(
      [{ transform: 'scale(0.8)', opacity: 0 }, { transform: 'scale(1)', opacity: 1 }],
      { duration: 300, easing: 'ease-out' }
    );
    return () => anim.cancel();
  }}
>
  <Component />
</ViewTransition>
```

`instance` 对象：`instance.old`、`instance.new`、`instance.group`、`instance.imagePair`、`instance.name`。

`types` 数组（第二个参数）允许你根据过渡类型切换动画。

---

## 动画时序

| 交互 | 时长 |
|------------|----------|
| 直接切换（展开 / 折叠） | 100–200ms |
| 路由过渡（滑动） | 150–250ms |
| Suspense 揭示（骨架 → 内容） | 200–400ms |
| 共享元素变形 | 300–500ms |

---

## 故障排查

**VT 没有被激活：** 确认 `<ViewTransition>` 出现在任何 DOM 节点之前。确认状态更新位于 `startTransition` 内。

**"两个 ViewTransition 组件拥有相同的 name"：** 名称必须在全局唯一。使用 ID：`name={`hero-${item.id}`}`。

**`router.back()` 以及浏览器的前进/后退跳过动画：** 改用带显式 URL 的 `router.push()`。参见 SKILL.md 中 "router.back() 与浏览器后退按钮"。

**`flushSync` 会跳过动画：** 改用 `startTransition`。

**只有 update 在播放（没有 enter / exit）：** 没有 `<Suspense>` 时，React 会把交换视作 update。请条件渲染 VT 本身，或者用 `<Suspense>` 包起来。

**布局里的 VT 阻止了页面 VT 的动画：** 父级 VT 内部的嵌套 VT 永远不会触发 enter/exit。如果你的布局里有一个 VT 包裹了 `{children}`，页面级的 enter/exit 将静默失效。移除布局里的 VT。

**带 `useOptimistic` 的列表重排没有动画：** 乐观值在快照之前就已确定。列表顺序应使用已提交状态。

**TS 报错 "Property 'default' is missing"：** 按类型键控的对象必须包含一个 `default` 键。

**Hash 片段导致滚动跳跃：** 不要带 hash 导航；导航完成后通过代码滚动到目标位置。

**Backdrop-blur 闪烁：** 使用 `css-recipes.md` 中提供的 backdrop-blur 解决方案。

**过渡过程中 `border-radius` 丢失：** 把 `border-radius` 直接应用到被捕获的元素上。

**骨架屏中的控件滑出视野：** 让对应的控件使用相同的 `viewTransitionName`。

**批处理：** 动画期间的多次更新会被批处理。A→B→C→D 会变成 B→D。