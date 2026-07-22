---
name: baseline-ui
description: 验证动画时长、强制排版比例、检查组件无障碍性，并防止 Tailwind CSS 项目中的布局反模式。触发词：构建 UI 组件、审查 CSS 工具、样式 React 视图、强制设计一致性、Tailwind UI 审查、无障碍检查、动画约束、排版规范。
risk: unknown
source: community
---

# Baseline UI

强制执行一套有主见的 UI 基线，防止 AI 生成的界面混乱。

## 何时使用

- 你正在构建或审查基于 Tailwind 的 UI，需要一个严格的基线来约束无障碍、动效、排版和布局。
- 任务是防止通用或粗糙的 AI 生成界面决策在代码库中蔓延。
- 你需要具体的 UI 约束来应用于文件审查或正在进行的前端实现。

## 如何使用

- `/baseline-ui`
  在当前对话中将这些约束应用于任何 UI 工作。

- `/baseline-ui <file>`
  根据以下所有约束审查文件并输出：
  - 违规项（引用确切的行/代码片段）
  - 为什么重要（1 句简短说明）
  - 具体修复建议（代码级别的建议）

## 技术栈

- 必须使用 Tailwind CSS 默认值，除非已存在自定义值或明确要求
- 当需要 JavaScript 动画时，必须使用 `motion/react`（原 `framer-motion`）
- 对于 Tailwind CSS 中的入场和微动画，应该使用 `tw-animate-css`
- 必须使用 `cn` 工具函数（`clsx` + `tailwind-merge`）处理类名逻辑

## 组件

- 对于任何具有键盘或焦点行为的组件，必须使用无障碍组件原语（`Base UI`、`React Aria`、`Radix`）
- 必须优先使用项目现有的组件原语
- 绝不在同一交互表面内混用不同的原语系统
- 如果与现有技术栈兼容，应该优先使用 [`Base UI`](https://base-ui.com/react/components) 作为新原语
- 必须为纯图标按钮添加 `aria-label`
- 绝不手动重建键盘或焦点行为，除非明确要求

## 交互

- 对于破坏性或不可逆操作，必须使用 `AlertDialog`
- 对于加载状态，应该使用结构性骨架屏
- 绝不使用 `h-screen`，使用 `h-dvh`
- 对于固定元素，必须遵守 `safe-area-inset`
- 必须在操作发生的位置旁边显示错误
- 绝不阻止在 `input` 或 `textarea` 元素中粘贴

## 动画

- 绝不添加动画，除非明确要求
- 必须只动画合成器属性（`transform`、`opacity`）
- 绝不动画布局属性（`width`、`height`、`top`、`left`、`margin`、`padding`）
- 应该避免动画绘制属性（`background`、`color`），小型本地 UI（文本、图标）除外
- 入场动画应该使用 `ease-out`
- 交互反馈绝不超过 `200ms`
- 离屏时必须暂停循环动画
- 应该遵守 `prefers-reduced-motion`
- 绝不引入自定义缓动曲线，除非明确要求
- 应该避免动画大图片或全屏表面

## 排版

- 标题必须使用 `text-balance`，正文/段落必须使用 `text-pretty`
- 数据必须使用 `tabular-nums`
- 密集 UI 应该使用 `truncate` 或 `line-clamp`
- 绝不修改 `letter-spacing`（`tracking-*`），除非明确要求

## 布局

- 必须使用固定的 `z-index` 比例（不使用任意 `z-*`）
- 对于正方形元素，应该使用 `size-*` 而非 `w-*` + `h-*`

## 性能

- 绝不动画大型 `blur()` 或 `backdrop-filter` 表面
- 绝不在活动动画之外应用 `will-change`
- 绝不使用 `useEffect` 处理可以用渲染逻辑表达的内容

## 设计

- 绝不使用渐变，除非明确要求
- 绝不使用紫色或多色渐变
- 绝不使用发光效果作为主要交互提示
- 应该使用 Tailwind CSS 默认阴影比例，除非明确要求
- 必须为空状态提供一个明确的下一步操作
- 应该将强调色使用限制为每个视图一个
- 应该在引入新颜色之前使用现有主题或 Tailwind CSS 颜色令牌

## 局限性

- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
