---
name: ui-motion
description: 将命名 StyleSeed 动效应用到组件 —— 可以是 5 种人格种子之一（Spring/Silk/Snap/Float/Pulse × entrance/exit/hover/press/layout），也可以是动效库中某个具名的关键字动作（toggle-flip、toggle-curtain、reveal-blur、pop-in、shimmer 等）。翻译 vibe 后选定种子与上下文（hover/press/entrance/exit/layout），展开对应 recipe，覆盖 `<motion.X>` 上。触发词：UI 动效、motion、动画、transition、easing、spring、tween、framer-motion、AnimatePresence。
risk: unknown
source: https://github.com/bitjaru/styleseed/tree/main/engine/.claude/skills/ss-motion
source_repo: bitjaru/styleseed
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/bitjaru/styleseed/blob/main/LICENSE
---

# 动效种子应用器
## 何时使用

当你需要将一种命名的 StyleSeed 动效应用到组件时使用本技能 —— 可以是 5 种人格种子之一（Spring/Silk/Snap/Float/Pulse × entrance/exit/hover/press/layout），也可以是动效库中某个具名的关键字动作（toggle-flip、toggle-curtain、reveal-blur、pop-in、shimmer …）。将 vibe 翻译为动效…


## 何时不要使用

- 关于通用 framer-motion 文档或学习内容 → 访问 framer-motion 官网
- 涉及非 React 动效（纯 CSS 过渡、GSAP） —— 本技能仅面向 `motion.X` JSX
- 涉及完整的滚动联动时间线或视差 —— 超出 DESIGN-LANGUAGE.md 规则 59 的范围
- 想要调整现有的 FadeIn/FadeUp/Stagger 包装器 —— 直接编辑 `engine/components/ui/motion.tsx`

## Vibe → 种子 映射

在应用前，先将用户的提示词翻译为五种种子之一。使用来自 `engine/motion/index.ts` 的查找表：

| 用户可能说的词 | 种子 |
|---|---|
| 弹跳的、有弹簧感的、俏皮的、有活力的、生动的 | **Spring** |
| 平滑的、丝滑的、流畅的、优雅的、镇定的、连续的 | **Silk** |
| 灵敏的、快速的、即时的、果断的、利落的、精准的 | **Snap** |
| 飘浮的、轻柔的、无重感的、梦幻的、氛围感的、漂浮的 | **Float** |
| 有节奏的、有冲击感的、搏动的、心跳的、节拍的 | **Pulse** |
| "Toss 风格"、"Arc 风格" | **Spring**（按品牌默认） |
| "Stripe 风格"、"Notion 风格" | **Silk** |
| "Linear 风格"、"Raycast 风格"、"Vercel 风格" | **Snap** |

如果用户只说出一个*品牌*名，则使用该品牌在 `BRAND_DEFAULT_SEED` 中的默认种子。如果用户明确指定了种子名（`spring`、`silk` 等），请照原样尊重它。

## 推荐模式 —— 用例 → 动效（当用户描述的是*时刻*而非 vibe 时）

如果用户描述的是**这个东西是什么**（"点赞按钮"、"模态框"、"加载
状态"、"信息流中的条目"），而不是某种感受，则从用例映射表
（`engine/motion/library.ts` 中的 `MOTION_BY_USECASE`，从 `@engine/motion` 导出）中进行推荐：

| 用例 | 选用 | 原因 |
|---|---|---|
| 主按钮 / CTA 按下 | `spring · press` | 触感扎实、自信 —— 该有的"按下手感" |
| 模态框 / 对话框 / 抽屉入场 | `silk · entrance` | 平滑；严肃/破坏性内容绝不应该回弹 |
| 下拉 / 浮层 / 菜单 | `snap · entrance` | 即时、精准 —— 高频 UI 不该让用户等 |
| Toast / 行内通知 | `spring · entrance` | 小巧友好的登场，非阻塞 |
| 列表 / 信息流条目出现 | `stagger-cascade` | 编排出场顺序，轻盈自然 |
| 特性 / 营销卡片悬停 | `tilt-3d` | 在内容轻量的营销页面上允许深度/花样 |
| 仪表盘 / 数据卡片悬停 | `snap · hover` | 仅做轻微上抬 —— 让密集 UI 保持安静 |
| 点赞 / 收藏 / 互动 | `like-burst` | 一次性的庆祝性效果，为点击带来回报 |
| 直播 / 在线 / 录制指示点 | `pulse-beat` | 循环心跳 = "活着的" |
| 加载 / 骨架屏 | `shimmer` | 平静且带方向感的进度 |
| 成功 / 确认 | `pop-in` | 积极的"完成"小提示 |
| 开关 / Tab / 分段切换 | `toggle-flip` | 醒目、易识别的切换 |
| 页面 / 路由切换 | `silk · entrance` | 平滑、克制，不抢戏 |
| 数字 / 余额 / KPI / 价格揭示 | **无** | 不要动效化展示值 —— 必须一眼读出 |

**两条反规则覆盖整张表**（如偏离，请明确指出）：
1. **一个产品只用一种种子。** 如果该项目已经在使用某种种子，请保持一致 —— 不要引入第二种人格。
2. **永远不要延迟载荷。** 不要把余额、价格或搜索结果用动效引出；动效服务于可操作性，而非内容本身。

## 命名动效关键字（具名动作）

种子定义一种*人格*（淡入/缩放的感觉）。`engine/motion/library.ts` 中的
**motion 库**则补充了*具名动作* —— 翻转、幕布擦除、形变 —— 每个都对应一个独立关键字。
当用户想要具体的、可识别的动效而不是通用感觉时，优先选用关键字。

`engine/motion/library.ts`（从 `@engine/motion` 导出为 `MOTION_LIBRARY` / `MOTION_BY_KEY`）
是**唯一权威来源** —— 每个关键字都携带自己可直接运行的 `snippet`。请从那里读取
snippet；切勿手写参数。

| 关键字 | 动作 | 在用户希望……时说出它 |
|---|---|---|
| `toggle-flip` | 3D Y 轴卡片翻转 | 开关/切换在两面之间翻转 |
| `toggle-slide` | 滑动堆叠交换 | 当前值滑出、下一个值滑入 |
| `toggle-morph` | 胶囊 ⇄ 圆形 形变 | 控件在切换时改变形状 |
| `toggle-curtain` | 自上而下的 clip-path 擦除 | 面板如幕布般揭开 |
| `reveal-blur` | blur(12px)→0 对焦入场 | 内容对焦拉入到位 |
| `reveal-rise` | 带遮罩的 clip-path 文本上升 | 标题/文本攀升进入视野 |
| `reveal-unfold` | 从顶端开始的 scaleY 展开 | 手风琴/面板展开 |
| `pop-in` | 从 0 开始的 spring 过冲 | 徽章/对勾以弹跳方式出现 |
| `press-squish` | 缩小 + 倾斜 | 按钮在点击时感觉 Q 弹有触感 |
| `tap-ripple` | 自点击点向外辐射涟漪 | Material 风格的按下反馈 |
| `pulse-beat` | 循环缩放搏动 | 直播/录制/心跳指示 |
| `wiggle` | 快速横向抖动 | 错误 / 输入无效的反馈 |
| `shimmer` | 骨架屏加载扫光 | 加载占位 |
| `stagger-cascade` | 子项依次淡入上升 | 列表逐个动效出现 |

**应用关键字：**

1. 从 `engine/motion/library.ts` 中读取精确配方 —— 找到 `key` 匹配的条目，
   原样复制其 `snippet`（它是经过校准且可直接运行的）。
2. 仅将元素/内容适配到用户的 JSX；保留过渡参数。
3. 如果关键字是有状态的（toggle、ripple），请按 snippet 中展示的方式接入 `useState`。
   如果是一次性揭示类，用 `key` 变更来重放。
4. 告诉用户你应用了哪个关键字，以便他们在别处复用保持一致，并指引他们到
   `/motion` 预览或复制其他关键字。

如果用户描述了某个动作但没有精确匹配的关键字，则回退到 种子 + 上下文。如果
他们提到的关键字根本不存在，则建议表中与之最接近的真实项 —— 切勿凭空发明关键字。

## 上下文检测

从提示词中推断下列五种上下文之一：

- "on hover" / "when hovered" → `hover`
- "on press" / "on tap" / "on click" → `press`
- "when it appears" / "on mount" / "entering" → `entrance`
- "when it leaves" / "on close" / "exiting" → `exit`（需要 `<AnimatePresence>`）
- "when layout changes" / "FLIP" / "rearranging" → `layout`

如有歧义，默认 `entrance`。如果多种上下文都合理（例如按钮同时需要 `hover` 和 `press`），则同时应用。

## 应用步骤

应用种子：**$0** · 上下文：**$1** · 目标：**$ARGUMENTS**

1. **读取目标文件** 到给定路径（如果未给出路径，则询问用户是哪个文件）。定位用户所指
   的 JSX 元素 —— 通常是 `<button>`、`<div>`、`<Card>` 之类。

2. **确认导入路径**。组件文件必须能够导入：
   - 来自 `"framer-motion"` 的 `motion`（以及用于 `exit` 的 `AnimatePresence`）
   - 来自 `"@engine/motion"` 的所选种子 —— 在不使用 `@engine/*` 别名的项目中，
     请使用到 `engine/motion` 的相对路径

3. **将目标标签替换为 `<motion.X>` 并展开种子配方**：

   ```tsx
   // hover example
   <motion.button {...spring.hover}>Save</motion.button>

   // press + hover combined
   <motion.button {...spring.press} {...spring.hover}>Save</motion.button>

   // entrance (mount)
   <motion.div {...silk.entrance}>...</motion.div>

   // exit (requires AnimatePresence wrapper somewhere up the tree)
   <AnimatePresence>
     {open && <motion.div {...silk.entrance} {...silk.exit} />}
   </AnimatePresence>

   // layout (FLIP)
   <motion.div {...snap.layout}>...</motion.div>
   ```

4. **不要内联参数**。种子的核心价值在于参数来自单一来源。切勿将
   `{ type: "spring", stiffness: 300, damping: 18 }` 之类展开进 JSX —— 始终
   使用展开运算符应用配方。

5. **尊重 `prefers-reduced-motion`**，特别是在长时间停留的页面中。对于一次性
   交互（hover/press），framer-motion 已自带节流。对于长生命周期页面中的
   mount/exit/layout 序列，请从 `@engine/motion` 导入 `usePrefersReducedMotion`
   和 `REDUCED_TRANSITION`，在启用减弱动效时覆盖过渡。

6. **复核验证**：重新读取文件，确认 JSX 仍可正确解析（括号匹配、motion 标签
   已闭合、用到 `exit` 时 AnimatePresence 已就位）。

7. **告知用户你应用了哪种种子与上下文**，并推荐一个可能接下来会用到的相关上下文
   （"要不要也加个 `press` 让它点击起来更带感？"）。

## 用户意图模糊时的默认行为

- 未指定文件 → 询问 "改哪个文件？"
- 没有 vibe 词 → 询问 "有 vibe 词、品牌名或种子名吗？"
- vibe 为 "自然的" 或 "像个真应用" → 默认 **Silk**（五种中最稳妥的）
- 元素为 CTA 按钮 → 额外加上 `press`

## 禁止行为

- 不要凭空创造新种子名。种子恰好五种。
- 不要通过本技能编辑 `engine/motion/seeds/*.ts` —— 这些是手工校准的。
  新增种子只能通过单独的、明确的请求进行。
- 不要引入第三方动画库（gsap、anime.js）。StyleSeed 仅面向 framer-motion。
- 不要添加滚动联动、视差或无限循环动画（DESIGN-LANGUAGE.md 规则 59）。

## 局限性

- 仅当任务与其上游来源及本地项目上下文明确匹配时，才使用本技能。
- 在应用更改前，请核对命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作特定环境测试、安全审查或用户对破坏性/高代价操作的批准。
