# 动画标准参考

审查背后的精确数值、曲线与规则。在发现中引用它们而非近似。提炼自 Emil Kowalski 的设计工程哲学（[animations.dev](https://animations.dev/)）。

## 是否应做动画？（频率表）

| 频率 | 决策 |
| --- | --- |
| 100+ 次/天（键盘快捷键、命令面板切换） | 不做动画。任何时候都不要。 |
| 数十次/天（悬停效果、列表导航） | 移除或大幅减弱 |
| 偶发（模态框、抽屉、Toast） | 标准动画 |
| 罕见/首次（引导、反馈、庆祝） | 可加入愉悦感 |

**绝不要在键盘触发的动作上做动画**——它们每天重复数百次；动画会让它们感觉迟钝且脱节。（Raycast 没有打开/关闭动画——这对每天用数百次的东西是正确的。）

动效的合理用途：空间一致性、状态指示、解释、反馈、防止突兀变化。"看起来很酷"出现在频繁出现的元素上不算合理。

## 缓动

决策顺序：
- 进入或退出 → **`ease-out`**（起步快，感觉响应迅速）
- 屏幕上的移动 / 形变 → **`ease-in-out`**
- 悬停 / 颜色变化 → **`ease`**
- 持续运动（跑马灯、进度条） → **`linear`**
- 默认 → **`ease-out`**

**UI 上绝不要 `ease-in`。** 它起步慢，推迟了用户正在关注的瞬间。200ms 的 `ease-out` *感觉上*比 200ms 的 `ease-in` 更快。

内置 CSS 缓动太弱。使用强力自定义曲线：

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* strong ease-out for UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* strong ease-in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like drawer curve (Ionic) */
```

在 [easing.dev](https://easing.dev/) 或 [easings.co](https://easings.co/) 寻找曲线——不要从零手搓。

## 时长

| 元素 | 时长 |
| --- | --- |
| 按钮按下反馈 | 100–160ms |
| 工具提示、小型弹出层 | 125–200ms |
| 下拉菜单、选择器 | 150–250ms |
| 模态框、抽屉 | 200–500ms |
| 营销 / 解释性 | 可更长 |

**规则：UI 动画保持在 300ms 以内。** 180ms 的下拉菜单比 400ms 的更响应。更快的旋转图标会让加载感觉更快（实际时间相同）。工具提示首次之后立即显示（跳过延迟和动画）会让工具栏感觉更快。

## 物理性

- **绝不要 `scale(0)`。** 以 `scale(0.9–0.97)` + `opacity: 0` 起始。现实中没有东西会从无中产生。
- **起点感知的弹出层。** 从触发器缩放，而非居中：
  ```css
  .popover { transform-origin: var(--radix-popover-content-transform-origin); } /* Radix */
  .popover { transform-origin: var(--transform-origin); }                       /* Base UI */
  ```
  **模态框例外**——它们出现在视口居中，保持 `transform-origin: center`。
- **按钮按下反馈。** `:active` 上 `transform: scale(0.97)`，`transition: transform 160ms ease-out`。细微（0.95–0.98）。适用于任何可按压元素。

## 弹簧

因模拟物理而感觉自然；无固定时长——靠参数收敛。适用于：带惯性的拖拽、"活泼"的元素（灵动岛）、可中断手势、装饰性鼠标跟随。

```js
// Apple-style (easier to reason about) — recommended
{ type: "spring", duration: 0.5, bounce: 0.2 }

// Traditional physics (more control)
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

保持反弹微妙（0.1–0.3）；大多数 UI 中避免反弹——留给拖拽关闭与可玩交互。弹簧在被中断时会保持速度（关键帧会从零重启），因此它们非常适合用户可能在动作中途反向的手势。

鼠标交互：使用 `useSpring` 做插值，而不是把值直接绑到鼠标位置（直接 = 人工感、无惯性）。仅当动效为装饰性时才这么做。

## 可中断性

CSS **过渡**可被中断并在动画中途重新定位；**关键帧**会从零重启。对任何快速触发的内容（Toast 的新增、开关），过渡更平滑。

```css
/* Interruptible — good for dynamic UI */
.toast { transition: transform 400ms ease; }

/* Not interruptible — avoid for dynamic UI */
@keyframes slideIn { from { transform: translateY(100%); } to { transform: translateY(0); } }
```

使用 `@starting-style` 在无 JS 时处理入场：

```css
.toast {
  opacity: 1; transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

旧版兜底：`useEffect(() => setMounted(true), [])` + `data-mounted` 属性。

## 非对称时长

在用户决策时慢，在系统响应时快。

```css
.overlay { transition: clip-path 200ms ease-out; }            /* release: fast */
.button:active .overlay { transition: clip-path 2s linear; }  /* press: slow, deliberate */
```

## 性能

- **仅对 `transform` 和 `opacity` 做动画**——它们跳过布局/绘制并在 GPU 上运行。`padding`/`margin`/`height`/`width`/`top`/`left` 会触发全部三个渲染步骤。
- **不要通过父元素上的 CSS 变量驱动子元素变换**——它会对所有子元素重算样式。直接在元素上设置 `transform`。
  ```js
  element.style.setProperty('--swipe-amount', `${d}px`); // bad: recalc on all children
  element.style.transform = `translateY(${d}px)`;        // good: only this element
  ```
- **Framer Motion 简写不是硬件加速的。** `x`/`y`/`scale` 在主线程上通过 rAF 运行，在负载下会丢帧。使用完整的 transform 字符串：
  ```jsx
  <motion.div animate={{ x: 100 }} />                          // drops frames under load
  <motion.div animate={{ transform: "translateX(100px)" }} />  // hardware accelerated
  ```
- **负载下 CSS 动画优于 JS**——它们在主线程外运行；基于 rAF 的动画在浏览器加载/脚本/绘制时会卡顿。对预设动效用 CSS，对动态/可中断动效用 JS。
- **WAAPI** 以 CSS 性能赋予 JS 控制力（硬件加速、可中断、无库）：
  ```js
  element.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
    { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' });
  ```

## 变换与 clip-path

- **`translate` 百分比**相对于元素自身尺寸——`translateY(100%)` 按元素自身高度移动，与尺寸无关（Sonner/Vaul 定位 Toast/抽屉的方式）。优先于硬编码 px。
- **`scale()` 也会缩放子元素**（字体、图标、内容）——这是按下反馈的特性。
- **3D**：`rotateX/Y` + `transform-style: preserve-3d` 实现无 JS 的深度/轨道/翻转。
- **`clip-path: inset(t r b l)`** 是一个强大的动画工具：每个值从对应边向内裁剪。用途：滚动揭示（`inset(0 0 100% 0)` → `inset(0 0 0 0)`）、长按删除覆盖层、无缝 Tab 颜色过渡（复制并裁剪激活副本）、对比滑块。

## 手势与拖拽

- **惯性关闭**：不要要求越过距离阈值——计算速度（`Math.abs(distance)/elapsedMs`）；超过 `~0.11` 即关闭。轻拂一下就够了。
- **边界阻尼**：拖过自然边界时移动量递减（真实物体在停下前会变慢）。
- **指针捕获** 一旦开始拖拽，这样即使指针离开边界也能继续。
- **多点触控保护**：拖拽开始后忽略额外触点（`if (isDragging) return`）——防止跳跃。
- **摩擦优于硬停**——允许过拖并提供递增阻力，而不是一堵隐形的墙。

## 遮盖不完美的交叉淡入

当交叉淡入即使调整了缓动/时长仍显示两个重叠状态时，在过渡期间加入细微的 `filter: blur(2px)`，将其混合为一个感知上的转换。模糊保持 < 20px（重模糊开销大，特别是 Safari）。

## 错峰

成组入场使用错峰；项间 30–80ms。更长的延迟感觉慢。错峰是装饰性的——播放期间绝不要阻塞交互。

```css
.item { opacity: 0; transform: translateY(8px); animation: fadeIn 300ms ease-out forwards; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
```

## 无障碍

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* keep opacity/color, drop transform-based motion */
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* gate hover motion — touch fires false hovers on tap */
}
```

```jsx
const reduce = useReducedMotion();
const closedX = reduce ? 0 : '-100%';
```

reduced-motion 意味着更少、更柔和的动画，而非零——保留有助于理解的过渡，去除位移/位置变化。

## 调试（在感觉不确定时建议审查中采用）

- **慢动作**：将时长提高 2–5 倍或使用 DevTools 动画检查器。检查颜色交叉淡入是否干净、缓动不会突兀停止、`transform-origin` 是否正确、协调属性是否保持同步。
- **逐帧**：Chrome DevTools 动画面板揭示协调属性之间的时序漂移。
- **真实设备** 用于手势（抽屉、滑动）——连上手机，通过 IP 访问开发服务器，使用 Safari 远程开发工具。
- **第二天以全新视角再看**——开发过程中看不见的瑕疵会在之后浮现。

## 一致性

动效需匹配组件的个性：可玩可更弹跳；专业仪表盘应保持利落且快速。Sonner 感觉对的部分原因在于缓动、时长、设计乃至名字和谐统一——稍慢一点，用 `ease` 而非 `ease-out`，以体现优雅。列表进入/退出的不透明度 + 高度是试错；没有公式——调整到感觉对为止。