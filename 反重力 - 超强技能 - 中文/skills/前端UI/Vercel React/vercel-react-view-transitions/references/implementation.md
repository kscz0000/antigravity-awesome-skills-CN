# 实施工作流

在为应用添加视图过渡时，请按顺序执行以下步骤。每一步都建立在前一步之上。

## 第 1 步：审计应用

在动手写任何代码之前，请先彻底扫描代码库。搜索：

- **每一个 `<Link>` 和 `router.push`** —— 它们就是你的导航触发器。打开每一个含有它们的文件。
- **每一个 `<Suspense>` 边界** —— 每一个都是揭示动画的候选。查看它们的 fallback 渲染了什么。
- **每一个页面 / 路由组件** —— 把它们列出来。每个页面都需要决定一个 VT 的放置位置。
- **持续存在的元素** —— 在导航之间持续显示的顶栏、导航栏、侧栏、粘性控件。它们需要通过 `viewTransitionName` 进行隔离。
- **共享的视觉元素** —— 在源视图和目标视图上都出现的图片、卡片或头像（例如列表里的缩略图和详情页上的同一张图片）。
- **骨架屏到内容的控件配对** —— 如果 Suspense fallback 渲染了一个控件（搜索框、标签栏），而真实内容中也存在同样的控件，那么两者都需要匹配一个 `viewTransitionName`。

接着对每一种导航进行归类，产出一张导航图：

```
| Route           | Navigates to         | Direction    | VT pattern            |
|-----------------|----------------------|--------------|-----------------------|
| /               | /detail/[id]         | forward      | directional slide     |
| /detail/[id]    | /                    | back         | directional slide     |
| /detail/[id]    | /detail/[other]      | sequential   | directional slide (ordered prev/next) or key+share crossfade |
| /tab/[a]        | /tab/[b]             | lateral      | key+share crossfade   |
| (Suspense)      | (content loads)      | —            | slide-up reveal       |
```

对于每一个共享元素（`name` 属性），要记录每一条导航：哪些路径能形成配对、哪些路径不能 —— 这决定了是否需要把 `enter` / `exit` 作为 `share` 的回退一并加上。

## 第 2 步：添加 CSS 配方

把 `css-recipes.md` 中**完整**的 CSS 配方集复制到你的全局样式表。内容应包括：时序变量、共享 keyframes、淡入淡出、滑动（垂直）、方向性导航（forward/back）、共享元素变形、持续元素隔离以及 reduced motion。

不要自行编写动画 CSS —— 这些配方已经处理好了容易出错的细节：错开的时序、变形时的运动模糊、reduced motion。完成初始设置后，你可以自定义时序变量（`--duration-exit`、`--duration-enter`、`--duration-move`）。

## 第 3 步：隔离持续存在的元素

对第 1 步识别出的每一个持续元素，加上 `viewTransitionName` 样式，以把它从页面内容的过渡快照中抽离出来：

```jsx
<header style={{ viewTransitionName: "site-header" }}>...</header>
```

随后在 `css-recipes.md` 中加上"持续元素隔离"的 CSS（避免该元素在页面过渡期间参与动画）。如果该元素使用了 `backdrop-blur` 或 `backdrop-filter`，请改用 `css-recipes.md` 中的 backdrop-blur 解决方案。

如果某个 Suspense fallback 镜像了一个持续存在的控件（例如骨架中的搜索框），那么真实控件和骨架都应使用相同的 `viewTransitionName`，以便原地变形。

## 第 4 步：添加方向性的页面过渡

对第 1 步识别出的层级导航，使用 `startTransition` 内部的 `addTransitionType` 来给导航方向打标签：

```jsx
startTransition(() => {
  addTransitionType('nav-forward');
  router.push('/detail/1');
});
```

随后把每一个**页面组件**（而不是布局）包到按类型键控的 `<ViewTransition>` 中：

```jsx
<ViewTransition
  enter={{
    "nav-forward": "nav-forward",
    "nav-back": "nav-back",
    default: "none",
  }}
  exit={{
    "nav-forward": "nav-forward",
    "nav-back": "nav-back",
    default: "none",
  }}
  default="none"
>
  <div>...page content...</div>
</ViewTransition>
```

`nav-forward` 与 `nav-back` 这两个 CSS 类来自 `css-recipes.md`，会产生水平方向的滑动。对于不那么在意方向感的简单应用，使用一个裸的 `<ViewTransition default="none">`，并配以 `enter="fade-in"` / `exit="fade-out"`，同样可行。

把它抽成一个可复用的组件，避免每个页面都重复冗长的类型映射：

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

这同时也成了以后添加新过渡类型时唯一需要改动的地方。

**规则：**
- 始终让 `enter` 与 `exit` 成对出现 —— 没有 exit 动画时，旧页面会瞬间消失而新页面却在动画进入。
- 在类型映射对象中务必带上 `default: "none"`，并在组件上写 `default="none"` —— 否则它会在每一次过渡中都触发。
- 把方向性 `<ViewTransition>` 放在每个页面组件里，不要放在布局里。布局在导航之间是持续存在的，永远不会触发 enter/exit。
- 方向性滑动仅用于层级导航或有序序列（上一项 / 下一项）。横向 / 兄弟导航（标签之间）应使用裸的 `<ViewTransition>`（交叉淡入淡出）或 `default="none"`。

## 第 5 步：添加 Suspense 揭示

对第 1 步识别出的每一个 `<Suspense>` 边界，分别把 fallback 和内容包到不同的 `<ViewTransition>` 中：

```jsx
<Suspense
  fallback={
    <ViewTransition exit="slide-down">
      <Skeleton />
    </ViewTransition>
  }
>
  <ViewTransition enter="slide-up" default="none">
    <AsyncContent />
  </ViewTransition>
</Suspense>
```

上面的例子使用 `slide-down` / `slide-up` 实现方向性的垂直运动。对于更简单的揭示，把 `<Suspense>` 直接用裸的 `<ViewTransition>` 包起来，就能得到一个零配置的交叉淡入淡出。选择依据是空间语义 —— 请参考主技能文件中"选择合适的动画风格"一表。

**规则：**
- 始终在内容 `<ViewTransition>` 上使用 `default="none"`，以防止在重新校验或与过渡无关的更新时再次触发动画。
- 在 Suspense `<ViewTransition>` 上使用简单的字符串属性（不要使用类型映射） —— Suspense 解析触发的是独立、且不携带类型的过渡，按类型键控的属性不会匹配。

## 第 6 步：添加共享元素过渡

对第 1 步识别出的每一个共享视觉元素，在源视图和目标视图上添加同名的 `<ViewTransition>` 包装器：

```jsx
// On the source view (e.g., list/grid page)
<ViewTransition name={`photo-${photo.id}`} share="morph" default="none">
  <Image src={photo.src} ... />
</ViewTransition>

// On the target view (e.g., detail page) — same name
<ViewTransition name={`photo-${photo.id}`} share="morph">
  <Image src={photo.src} ... />
</ViewTransition>
```

`share="morph"` 类来自 `css-recipes.md` 中的变形配方（可控时长 + 运动模糊）。想要更简单的交叉淡入淡出，可用 `share="auto"`（浏览器默认行为）。

当列表项包含共享元素时，要把两种模式用两层嵌套的 `<ViewTransition>` 组合起来 —— 详见 `SKILL.md` 中"把共享元素与列表标识组合在一起"。

**规则：**
- 名称必须在全局唯一 —— 使用 `photo-${id}` 这类前缀。
- 在列表侧的共享元素上添加 `default="none"`，以避免在过滤 / 搜索更新时按项触发交叉淡入淡出。

## 第 7 步：逐条验证导航路径

按顺序过一遍第 1 步导航图里的每一行，并确认：

- 在这条导航上 VT 是会挂载 / 卸载，还是保持挂载（同路由）？
- 对于命名 VT：是否能形成共享配对？如果不能，是否有 `enter` / `exit` 作为回退？
- `default="none"` 是否会误关掉你想要的动画？
- 持续存在的元素是否保持静止（没有跟着页面内容一起滑动）？
- Suspense 揭示是否能独立于方向性导航进行播放？

如果某条路径没有动画或出现了相互竞争的动画，请回到对应的步骤重做。

---

## 常见错误

- **裸露的、没有 props 的 `<ViewTransition>`** —— 不加 `default="none"` 时，它会在每一次过渡（每一次导航、每一次 Suspense 解析、每一次重新校验）都触发浏览器默认的交叉淡入淡出。始终设置 `default="none"`，并仅显式启用你想要的触发器。
- **布局中的方向性 `<ViewTransition>`** —— 布局在导航之间持续存在，永远不会卸载 / 重新挂载。`enter` / `exit` 属性不会在路由切换时触发。把外层的按类型键控的 `<ViewTransition>` 放在每个页面组件中。
- **共享元素变形与淡出式 exit 混用** —— 页面淡出与共享变形会相互冲突。请改用方向性的滑动式 exit。
- **自行编写动画 CSS** —— `css-recipes.md` 中的配方已经处理好了错开的时序、变形时的运动模糊以及 reduced motion。直接复制，不要重复造轮子。
- **按类型键控的对象缺少 `default: "none"`** —— TypeScript 要求存在 `default` 键；缺了它，回退值就会是 `"auto"`，从而在每次过渡时都触发。
- **在 Suspense 揭示上使用类型映射** —— Suspense 解析触发的是独立、且不携带类型的过渡。按类型键控的属性不会匹配 —— 改用简单的字符串属性。
- **用裸的 `viewTransitionName` CSS 来触发动画** —— React 只有在 `<ViewTransition>` 组件位于树中时才会调用 `document.startViewTransition`。裸露的 `viewTransitionName` 样式只是用来把元素从父级快照中隔离出去，而不是用来触发动画。
- **把 `update` 触发器用于同路由导航** —— 内容里嵌套的 VT 会从父级窃取 mutation，导致外层 VT 上的 `update` 永远不会触发。改用 `key` + `name` + `share`。
- **可复用组件里带命名的 VT** —— 如果一个带命名 VT 的组件同时在模态 / 弹层 *和* 页面中渲染，两个会同时挂载，破坏变形效果。要么让名称按条件决定，要么把命名 VT 移到具体的消费者那里。
- **用 `router.back()` 实现后退** —— `router.back()` 会触发同步的 `popstate`，与视图过渡不兼容。请改用带显式 URL 的 `router.push()`。

---

针对 Next.js 的具体实施步骤（配置标志、`<Link>` 上的 `transitionTypes`、同路由动态段），请参见 `nextjs.md`。