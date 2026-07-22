---
name: animejs-animation
description: 高级 JavaScript 动画库技能，用于创建复杂、高性能的网页动画。触发词：Anime.js动画、JS动画库、网页动画、SVG动画、时间轴动画、交错动画、高性能动画、交互式动画、DOM动画、CSS动画
risk: safe
source: community
date_added: "2026-03-07"
---

# Anime.js 动画技能

[Anime.js](https://animejs.com/) 是一个轻量但极其强大的 JavaScript 动画引擎。它擅长处理复杂的时间轴、交错效果，以及对 DOM、CSS 和 SVG 的精确控制。

## 上下文

此技能用于创建高保真、令人惊叹的网页动画，远超简单的 CSS 过渡效果。它是打造获奖级交互网站的首选工具。

## 何时使用

在以下情况下触发此技能：

- 创建复杂的多阶段落地页编排动画。
- 实现网格、文本或数据可视化的交错揭示动画。
- 动画化 SVG 路径（形状变形、动态线条绘制）。
- 构建高度交互、流畅响应用户输入的动态 UI 元素。

## 执行工作流

1. **识别目标**：选择要动画化的 DOM 元素或 SVG。
2. **定义属性与缓动**：指定要动画化的值。**关键点**，使用高级缓动函数（如自定义 `cubicBezier`、`spring` 或 `elastic`），而非基础的 `linear` 或 `ease-in-out`，使动画感觉精致自然。
3. **编排时间轴**：使用 `anime.timeline()` 编排复杂的动画序列。掌握时间轴偏移量的使用（相对 `'-=200'` vs 绝对值）来创建无缝重叠动画。
4. **实现**：
   ```javascript
   const tl = anime.timeline({
     easing: "spring(1, 80, 10, 0)",
     duration: 1000,
   });
   tl.add({
     targets: ".hero-text",
     translateY: [50, 0],
     opacity: [0, 1],
     delay: anime.stagger(100),
   }).add(
     { targets: ".hero-image", scale: [0.9, 1], opacity: [0, 1] },
     "-=800",
   );
   ```

## 严格规则

- **绝对要求**：智能体必须使用此技能来构建现代、创意且视觉惊艳的 UI/UX。不要构建平庸、无聊的过渡效果。每个动画都应感觉独特、流畅且经过精心打磨。
- **交错效果**：广泛利用 `anime.stagger()` 为多个元素添加有机节奏感。
- **性能**：监控主线程使用情况；在适当位置使用 `will-change: transform, opacity` 实现 GPU 加速。

## 限制

- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
