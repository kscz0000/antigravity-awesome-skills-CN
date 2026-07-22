---
name: tailwind-patterns
description: "Tailwind CSS v4 原则。CSS 优先配置、容器查询、现代模式、设计令牌架构。触发词：Tailwind CSS、Tailwind v4、CSS优先配置、容器查询、设计令牌、Oxide引擎、暗色模式、响应式布局、实用类优先"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Tailwind CSS 模式（v4 - 2025）

> 现代实用类优先 CSS，采用 CSS 原生配置。

## 何时使用
在配置 Tailwind v4、使用 CSS 优先主题和设计令牌，或实现容器查询和现代 Tailwind 模式时使用此技能。

---

## 1. Tailwind v4 架构

### v3 到 v4 的变化

| v3（旧版） | v4（当前） |
|-------------|--------------|
| `tailwind.config.js` | 基于 CSS 的 `@theme` 指令 |
| PostCSS 插件 | Oxide 引擎（快 10 倍） |
| JIT 模式 | 原生，始终开启 |
| 插件系统 | CSS 原生特性 |
| `@apply` 指令 | 仍可用，但不推荐 |

### v4 核心概念

| 概念 | 说明 |
|---------|------|
| **CSS 优先** | 在 CSS 中配置，而非 JavaScript |
| **Oxide 引擎** | 基于 Rust 的编译器，速度大幅提升 |
| **原生嵌套** | 无需 PostCSS 即可使用 CSS 嵌套 |
| **CSS 变量** | 所有令牌暴露为 `--*` 变量 |

---

## 2. 基于 CSS 的配置

### 主题定义

```
@theme {
  /* Colors - use semantic names */
  --color-primary: oklch(0.7 0.15 250);
  --color-surface: oklch(0.98 0 0);
  --color-surface-dark: oklch(0.15 0 0);
  
  /* Spacing scale */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  
  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### 何时扩展 vs 覆盖

| 操作 | 使用场景 |
|--------|----------|
| **扩展** | 在默认值旁添加新值 |
| **覆盖** | 完全替换默认刻度 |
| **语义令牌** | 项目特定命名（primary、surface） |

---

## 3. 容器查询（v4 原生）

### 断点 vs 容器

| 类型 | 响应对象 |
|------|-------------|
| **断点**（`md:`） | 视口宽度 |
| **容器**（`@container`） | 父元素宽度 |

### 容器查询用法

| 模式 | 类名 |
|---------|---------|
| 定义容器 | 父元素上使用 `@container` |
| 容器断点 | 子元素上使用 `@sm:`、`@md:`、`@lg:` |
| 命名容器 | `@container/card` 用于精确匹配 |

### 何时使用

| 场景 | 使用 |
|----------|-----|
| 页面级布局 | 视口断点 |
| 组件级响应式 | 容器查询 |
| 可复用组件 | 容器查询（与上下文无关） |

---

## 4. 响应式设计

### 断点系统

| 前缀 | 最小宽度 | 目标设备 |
|--------|-----------|--------|
| （无） | 0px | 移动优先基础样式 |
| `sm:` | 640px | 大屏手机 / 小平板 |
| `md:` | 768px | 平板 |
| `lg:` | 1024px | 笔记本 |
| `xl:` | 1280px | 桌面 |
| `2xl:` | 1536px | 大屏桌面 |

### 移动优先原则

1. 先写移动端样式（无前缀）
2. 用前缀添加更大屏幕的覆盖样式
3. 示例：`w-full md:w-1/2 lg:w-1/3`

---

## 5. 暗色模式

### 配置策略

| 方法 | 行为 | 使用场景 |
|--------|----------|----------|
| `class` | `.dark` 类切换 | 手动主题切换器 |
| `media` | 跟随系统偏好 | 无用户控制 |
| `selector` | 自定义选择器（v4） | 复杂主题方案 |

### 暗色模式模式

| 元素 | 亮色 | 暗色 |
|---------|-------|------|
| 背景 | `bg-white` | `dark:bg-zinc-900` |
| 文字 | `text-zinc-900` | `dark:text-zinc-100` |
| 边框 | `border-zinc-200` | `dark:border-zinc-700` |

---

## 6. 现代布局模式

### Flexbox 模式

| 模式 | 类名 |
|---------|---------|
| 双轴居中 | `flex items-center justify-center` |
| 垂直堆叠 | `flex flex-col gap-4` |
| 水平排列 | `flex gap-4` |
| 两端对齐 | `flex justify-between items-center` |
| 自动换行 | `flex flex-wrap gap-4` |

### Grid 模式

| 模式 | 类名 |
|---------|---------|
| 自适应响应式 | `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]` |
| 非对称（Bento） | `grid grid-cols-3 grid-rows-2` 配合 span |
| 侧边栏布局 | `grid grid-cols-[auto_1fr]` |

> **注意：** 优先使用非对称/Bento 布局，而非对称的三列网格。

---

## 7. 现代色彩系统

### OKLCH vs RGB/HSL

| 格式 | 优势 |
|--------|-----------|
| **OKLCH** | 感知均匀，更适合设计 |
| **HSL** | 直观的色相/饱和度 |
| **RGB** | 旧版兼容性 |

### 色彩令牌架构

| 层级 | 示例 | 用途 |
|-------|---------|---------|
| **原始层** | `--blue-500` | 原始颜色值 |
| **语义层** | `--color-primary` | 基于用途的命名 |
| **组件层** | `--button-bg` | 组件特定 |

---

## 8. 排版系统

### 字体栈模式

| 类型 | 推荐 |
|------|-------------|
| Sans | `'Inter', 'SF Pro', system-ui, sans-serif` |
| Mono | `'JetBrains Mono', 'Fira Code', monospace` |
| Display | `'Outfit', 'Poppins', sans-serif` |

### 字号刻度

| 类名 | 大小 | 用途 |
|-------|------|-----|
| `text-xs` | 0.75rem | 标签、说明文字 |
| `text-sm` | 0.875rem | 次要文本 |
| `text-base` | 1rem | 正文文本 |
| `text-lg` | 1.125rem | 引导文本 |
| `text-xl`+ | 1.25rem+ | 标题 |

---

## 9. 动画与过渡

### 内置动画

| 类名 | 效果 |
|-------|--------|
| `animate-spin` | 持续旋转 |
| `animate-ping` | 注意力脉冲 |
| `animate-pulse` | 微妙透明度脉冲 |
| `animate-bounce` | 弹跳效果 |

### 过渡模式

| 模式 | 类名 |
|---------|---------|
| 所有属性 | `transition-all duration-200` |
| 特定属性 | `transition-colors duration-150` |
| 带缓动 | `ease-out` 或 `ease-in-out` |
| 悬停效果 | `hover:scale-105 transition-transform` |

---

## 10. 组件提取

### 何时提取

| 信号 | 操作 |
|--------|--------|
| 相同类组合出现 3 次以上 | 提取组件 |
| 复杂状态变体 | 提取组件 |
| 设计系统元素 | 提取并文档化 |

### 提取方法

| 方法 | 使用场景 |
|--------|----------|
| **React/Vue 组件** | 动态，需要 JS |
| **CSS 中的 @apply** | 静态，无需 JS |
| **设计令牌** | 可复用值 |

---

## 11. 反模式

| 不要 | 应该 |
|-------|-----|
| 到处使用任意值 | 使用设计系统刻度 |
| `!important` | 正确修复优先级 |
| 内联 `style=` | 使用实用类 |
| 重复冗长的类列表 | 提取组件 |
| 混用 v3 配置与 v4 | 完全迁移到 CSS 优先 |
| 大量使用 `@apply` | 优先使用组件 |

---

## 12. 性能原则

| 原则 | 实现方式 |
|-----------|----------------|
| **清除未使用的样式** | v4 中自动完成 |
| **避免动态类名** | 不使用模板字符串类名 |
| **使用 Oxide** | v4 默认，快 10 倍 |
| **缓存构建** | CI/CD 缓存 |

---

> **记住：** Tailwind v4 是 CSS 优先的。拥抱 CSS 变量、容器查询和原生特性。配置文件现在是可选的。

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
