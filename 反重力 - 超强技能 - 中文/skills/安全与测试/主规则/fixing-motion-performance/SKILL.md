---
name: fixing-motion-performance
description: >
  审计并修复动画性能问题，包括布局抖动、合成器属性、滚动联动运动和模糊效果。当动画卡顿、过渡抖动，或审查 CSS/JS 动画性能时使用。触发词：动画性能、布局抖动、合成器、滚动联动、模糊、will-change、rAF。
risk: safe
source: community
---

# fixing-motion-performance

修复动画性能问题。

## 使用方法

- `/fixing-motion-performance`
  将这些约束应用于本对话中的所有 UI 动画工作。

- `/fixing-motion-performance <file>`
  按下方所有规则审查该文件并报告：
  - 违规点（引用准确的行或片段）
  - 为什么重要（一句话）
  - 具体修复建议（代码级）

除非明确请求，否则不要迁移动画库。在现有栈中应用规则。

## 何时使用

在以下情况参考这些指南：
- 添加或修改 UI 动画（CSS、WAAPI、Motion、rAF、GSAP）
- 重构卡顿的交互或过渡
- 实现滚动联动或滚动揭示效果
- 动画化布局、滤镜、遮罩、渐变或 CSS 变量
- 审查使用 will-change、transform 或测量的组件

## 渲染步骤词汇表

- composite（合成）：transform、opacity
- paint（绘制）：color、borders、gradients、masks、images、filters
- layout（布局）：size、position、flow、grid、flex

## 规则类别（按优先级）

| 优先级 | 类别 | 影响 |
|:------:|------|:----:|
| 1 | 禁止的模式 | 严重 |
| 2 | 选择机制 | 严重 |
| 3 | 测量 | 高 |
| 4 | 滚动 | 高 |
| 5 | 绘制 | 中-高 |
| 6 | 图层 | 中 |
| 7 | 模糊与滤镜 | 中 |
| 8 | 视图过渡 | 低 |
| 9 | 工具边界 | 严重 |

## 速查

### 1. 禁止的模式（严重）

- 不要在同一帧内交错布局读取和写入
- 不要在大型或有意义的表面上持续动画布局
- 不要从 scrollTop、scrollY 或 scroll 事件驱动动画
- requestAnimationFrame 循环必须带停止条件
- 不要混合多个动画系统，每个都测量或变更布局

### 2. 选择机制（严重）

- 默认使用 transform 和 opacity 进行运动
- 仅在交互需要时使用 JS 驱动的动画
- paint 或 layout 动画仅在小、隔离的表面上可接受
- 一次性效果比连续运动更可接受
- 偏好降级技术而非完全移除运动

### 3. 测量（高）

- 测量一次，然后通过 transform 或 opacity 动画
- 在写入前批处理所有 DOM 读取
- 不要在动画过程中重复读取布局
- 偏好类布局效果使用 FLIP 风格过渡
- 偏好批处理测量和写入的方法

### 4. 滚动（高）

- 偏好使用 Scroll 或 View Timelines 实现滚动联动（当可用时）
- 使用 IntersectionObserver 处理可见性和暂停
- 不要轮询 scroll 位置以做动画
- 离屏时暂停或停止动画
- 滚动联动运动不得在大型表面上触发连续的 layout 或 paint

### 5. 绘制（中-高）

- paint 触发的动画仅允许在小、隔离的元素上
- 不要在大型容器上动画 paint 密集的属性
- 不要为 transform、opacity 或 position 动画 CSS 变量
- 不要动画继承的 CSS 变量
- 将动画化的 CSS 变量限定在本地，避免继承

### 6. 图层（中）

- 合成器运动需要图层提升，绝不能假设其存在
- 临时、外科手术式地使用 will-change
- 避免大量或大型的提升图层
- 性能重要时用工具验证图层行为

### 7. 模糊与滤镜（中）

- 模糊动画保持小（≤ 8px）
- 模糊仅用于短、一次性效果
- 永远不要持续动画模糊
- 永远不要在大型表面上动画模糊
- 在模糊之前优先使用 opacity 和 translate

### 8. 视图过渡（低）

- 视图过渡仅用于导航级别的更改
- 交互密集型 UI 避免视图过渡
- 需要中断或取消时避免视图过渡
- 将尺寸变化视为可能触发布局

### 9. 工具边界（严重）

- 除非明确请求，否则不要迁移或重写动画库
- 在现有动画系统中应用这些规则
- 永远不要部分迁移 API 或在同一组件内混用风格

## 常见修复

```css
/* 布局抖动：动画 transform 而非 width */
/* before */ .panel { transition: width 0.3s; }
/* after */  .panel { transition: transform 0.3s; }

/* 滚动联动：使用 scroll-timeline 替代 JS */
/* before */ window.addEventListener('scroll', () => el.style.opacity = scrollY / 500)
/* after */  .reveal { animation: fade-in linear; animation-timeline: view(); }
```

```js
// 测量：批处理读取后写入（FLIP）
// before — 布局抖动
el.style.left = el.getBoundingClientRect().left + 10 + 'px';
// after — 测量一次，通过 transform 动画
const first = el.getBoundingClientRect();
el.classList.add('moved');
const last = el.getBoundingClientRect();
el.style.transform = `translateX(${first.left - last.left}px)`;
requestAnimationFrame(() => { el.style.transition = 'transform 0.3s'; el.style.transform = ''; });
```

## 审查指导

- 首先强制执行严重规则（禁止的模式、工具边界）
- 选择匹配意图的最便宜的渲染工作
- 对于任何非默认选择，说明正当性约束（表面大小、持续时间或交互要求）
- 审查时，偏好可操作的注释和具体替代方案，而非理论

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
