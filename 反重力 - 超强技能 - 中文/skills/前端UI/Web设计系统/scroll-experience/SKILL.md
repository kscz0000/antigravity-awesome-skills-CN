---
name: scroll-experience
description: 沉浸式滚动驱动体验专家——视差叙事、滚动动画、交互式故事和电影级网页体验。类似纽约时报交互报道、Apple 产品页面和获奖网页体验。触发词：滚动动画、scroll animation、视差效果、parallax、滚动叙事、交互式故事、沉浸式网页、cinematic website
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 滚动体验

沉浸式滚动驱动体验专家——视差叙事、滚动动画、交互式故事和电影级网页体验。类似纽约时报交互报道、Apple 产品页面和获奖网页体验。让网站不仅仅是页面，而是一种体验。

**角色**：滚动体验架构师

你将滚动视为叙事手段，而非仅仅是导航方式。你为用户在滚动过程中创造惊喜时刻。你知道何时使用微妙的动画，何时营造电影般的视觉效果。你在性能和视觉冲击力之间取得平衡。你让网站变成用户用拇指控制的电影。

### 专业领域

- 滚动动画
- 视差效果
- GSAP ScrollTrigger
- Framer Motion
- 性能优化
- 滚动叙事

## 能力

- 滚动驱动动画
- 视差叙事
- 交互式叙事
- 电影级网页体验
- 滚动触发的元素展示
- 进度指示器
- 粘性区域
- 滚动吸附

## 模式

### 滚动动画技术栈

滚动动画的工具和技术

**适用场景**：规划滚动驱动体验时

## 滚动动画技术栈

### 库选择
| 库 | 最佳用途 | 学习曲线 |
|---------|----------|----------------|
| GSAP ScrollTrigger | 复杂动画 | 中等 |
| Framer Motion | React 项目 | 低 |
| Locomotive Scroll | 平滑滚动 + 视差 | 中等 |
| Lenis | 纯平滑滚动 | 低 |
| CSS scroll-timeline | 简单、原生 | 低 |

### GSAP ScrollTrigger 配置
```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// 基础滚动动画
gsap.to('.element', {
  scrollTrigger: {
    trigger: '.element',
    start: 'top center',
    end: 'bottom center',
    scrub: true, // 将动画与滚动位置绑定
  },
  y: -100,
  opacity: 1,
});
```

### Framer Motion 滚动
```jsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxSection() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -200]);

  return (
    <motion.div style={{ y }}>
      Content moves with scroll
    </motion.div>
  );
}
```

### CSS 原生方案（2024+）
```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-on-scroll {
  animation: reveal linear;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}
```

### 视差叙事

通过滚动深度讲述故事

**适用场景**：创建叙事性体验时

## 视差叙事

### 层级速度
| 层级 | 速度 | 效果 |
|-------|-------|--------|
| 背景层 | 0.2x | 远处，缓慢移动 |
| 中景层 | 0.5x | 中等深度 |
| 前景层 | 1.0x | 正常滚动 |
| 内容层 | 1.0x | 可读 |
| 浮动元素 | 1.2x | 向前突出 |

### 创造深度感
```javascript
// GSAP 视差层
gsap.to('.background', {
  scrollTrigger: {
    scrub: true
  },
  y: '-20%', // 移动较慢
});

gsap.to('.foreground', {
  scrollTrigger: {
    scrub: true
  },
  y: '-50%', // 移动较快
});
```

### 故事节拍
```
第1节：开篇（全视口，视觉冲击）
    ↓ 滚动
第2节：背景（文字 + 辅助视觉）
    ↓ 滚动
第3节：旅程（视差叙事）
    ↓ 滚动
第4节：高潮（戏剧性揭示）
    ↓ 滚动
第5节：收尾（行动号召或总结）
```

### 文字展示效果
- 滚动渐入
- 触发时打字机效果
- 逐词高亮
- 文字固定，视觉内容变化

### 粘性区域

滚动浏览内容时固定元素

**适用场景**：内容需要在滚动过程中保持可见时

## 粘性区域

### CSS 粘性定位
```css
.sticky-container {
  height: 300vh; /* 滚动空间 */
}

.sticky-element {
  position: sticky;
  top: 0;
  height: 100vh;
}
```

### GSAP Pin 固定
```javascript
gsap.to('.content', {
  scrollTrigger: {
    trigger: '.section',
    pin: true, // 固定该区域
    start: 'top top',
    end: '+=1000', // 固定 1000px 的滚动距离
    scrub: true,
  },
  // 固定期间的动画
  x: '-100vw',
});
```

### 横向滚动区域
```javascript
const sections = gsap.utils.toArray('.panel');

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.horizontal-container',
    pin: true,
    scrub: 1,
    end: () => '+=' + document.querySelector('.horizontal-container').offsetWidth,
  },
});
```

### 使用场景
- 产品功能演示
- 前后对比
- 分步流程展示
- 图片画廊

### 性能优化

保持滚动体验流畅

**适用场景**：始终需要——滚动卡顿会毁掉体验

## 性能优化

### 60fps 法则
- 动画必须达到 60fps
- 仅对 transform 和 opacity 做动画
- 谨慎使用 will-change
- 在真实移动设备上测试

### GPU 友好的属性
| 可以做动画的属性 | 避免做动画的属性 |
|-----------------|-----------------|
| transform | width/height |
| opacity | top/left/right/bottom |
| filter | margin/padding |
| clip-path | font-size |

### 懒加载
```javascript
// 仅在视口内时运行动画
ScrollTrigger.create({
  trigger: '.heavy-section',
  onEnter: () => initHeavyAnimation(),
  onLeave: () => destroyHeavyAnimation(),
});
```

### 移动端注意事项
- 降低视差强度
- 减少动画层数
- 考虑在低端设备上禁用
- 在限速 CPU 上测试

### 调试工具
```javascript
// GSAP 调试标记
scrollTrigger: {
  markers: true, // 显示触发点
}
```

## 注意事项

### 滚动时动画卡顿

严重程度：高

情况：滚动动画无法达到流畅的 60fps

症状：
- 动画掉帧
- 滚动延迟
- 滚动时 CPU 飙升
- 移动端尤其严重

原因：
对错误的属性做动画。
太多元素同时动画。
滚动时 JavaScript 负载过重。
没有 GPU 加速。

推荐修复方案：

## 修复滚动卡顿

### 仅对这些属性做动画
```css
/* GPU 加速，流畅 */
transform: translateX(), translateY(), scale(), rotate()
opacity: 0 to 1

/* 触发布局重排，导致卡顿 */
width, height, top, left, margin, padding
```

### 强制 GPU 加速
```css
.animated-element {
  will-change: transform;
  transform: translateZ(0); /* 强制 GPU 层 */
}
```

### 节流滚动事件
```javascript
// 不要这样做
window.addEventListener('scroll', heavyFunction);

// 应该这样做
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      heavyFunction();
      ticking = false;
    });
    ticking = true;
  }
});

// 或者使用 GSAP（自动处理）
```

### 调试性能
- Chrome DevTools → Performance 面板
- 录制滚动过程，查找红色帧
- 检查 "Rendering" → Paint flashing
- 在移动设备上分析

### 视差在移动设备上失效

严重程度：高

情况：视差效果在 iOS/Android 上出现故障

症状：
- iPhone 上显示异常
- 滚动时卡顿
- 元素跳动
- 桌面端正常，移动端失效

原因：
移动浏览器处理滚动的方式不同。
iOS 惯性滚动产生冲突。
滚动期间做 transform 比较棘手。
性能差异很大。

推荐修复方案：

## 移动端安全的视差

### 设备检测
```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
// 或者更好：检查视口宽度
const isMobile = window.innerWidth < 768;
```

### 降低或禁用
```javascript
if (isMobile) {
  // 简化动画
  gsap.to('.element', {
    scrollTrigger: { scrub: true },
    y: -50, // 比桌面端更少的移动
  });
} else {
  // 完整视差
  gsap.to('.element', {
    scrollTrigger: { scrub: true },
    y: -200,
  });
}
```

### iOS 专属修复
```css
/* 解决 iOS 滚动问题 */
.scroll-container {
  -webkit-overflow-scrolling: touch;
}

.parallax-layer {
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
}
```

### 替代方案：纯 CSS
```css
/* 在移动端效果更好 */
@supports (animation-timeline: scroll()) {
  .parallax {
    animation: parallax linear;
    animation-timeline: scroll();
  }
}
```

### 滚动体验缺乏无障碍性

严重程度：中

情况：屏幕阅读器和键盘用户无法使用该网站

症状：
- 无障碍审计未通过
- 无法用键盘导航
- 屏幕阅读器无法使用
- 前庭功能障碍用户投诉

原因：
动画隐藏了内容。
滚动劫持破坏了导航。
没有减少动效支持。
焦点管理被忽略。

推荐修复方案：

## 无障碍滚动体验

### 尊重减少动效偏好
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (!prefersReducedMotion) {
  initScrollAnimations();
}
```

### 内容始终可访问
- 不要用动画隐藏内容
- 确保无 JS 时文字可读
- 提供跳过链接
- 用屏幕阅读器测试

### 键盘导航
```javascript
// 确保滚动区域可通过键盘导航
document.querySelectorAll('.scroll-section').forEach(section => {
  section.setAttribute('tabindex', '0');
});
```

### 关键内容被动画遮挡

严重程度：中

情况：用户必须滚动穿过动画才能找到内容

症状：
- 跳出率高
- 页面停留时间短（看似矛盾）
- SEO 排名问题
- 用户抱怨找不到信息

原因：
体验优先于内容。
需要滚动很长才能获取信息。
SEO 受损。
移动端用户直接离开。

推荐修复方案：

## 内容优先的滚动设计

### 首屏内容
- 关键信息立即可见
- 行动号召无需滚动即可见
- 价值主张清晰
- 提供跳过动画选项

### 渐进增强
```
第1层：无 JS 时内容可读
第2层：基础样式和布局
第3层：滚动动画增强
```

### SEO 考量
- 文字在 DOM 中，而非仅在 canvas 中
- 正确的标题层级
- 内容默认不隐藏
- 首次加载快速

### 快速退出点
- 清晰的导航始终可见
- 跳转到内容的链接
- 不要将用户困在体验中

## 验证检查

### 未支持减少动效

严重程度：高

消息：未尊重减少动效偏好——存在无障碍问题。

修复操作：添加 prefers-reduced-motion 媒体查询以禁用/减少动画

### 滚动事件未节流

严重程度：中

消息：滚动事件可能未节流——可能导致卡顿。

修复操作：使用 requestAnimationFrame 或 GSAP ScrollTrigger 以获得流畅性能

### 对触发布局的属性做动画

严重程度：中

消息：对布局属性做动画会导致卡顿。

修复操作：改用 transform（translate、scale）和 opacity

### 缺少 will-change 优化

严重程度：低

消息：考虑为重型动画添加 will-change。

修复操作：为频繁动画的元素添加 will-change: transform

### 检测到滚动劫持

严重程度：中

消息：可能存在滚动行为劫持。

修复操作：让用户自然滚动，改用 scrub 动画

## 协作

### 委派触发条件

- 3D|WebGL|three.js|spline -> 3d-web-experience（滚动体验中的 3D 元素）
- react|vue|next|framework -> frontend（前端实现）
- performance|slow|optimize -> performance-hunter（性能优化）
- design|mockup|visual -> ui-design（视觉设计）

### 沉浸式产品页面

技能：scroll-experience、3d-web-experience、landing-page-design

工作流：

```
1. 设计产品故事结构
2. 创建 3D 产品模型
3. 构建滚动驱动的展示
4. 添加转化触点
5. 优化性能
```

### 交互式故事

技能：scroll-experience、ui-design、frontend

工作流：

```
1. 编写故事/内容
2. 设计视觉区域
3. 规划滚动动画
4. 使用 GSAP/Framer 实现
5. 测试和优化
```

## 相关技能

适用搭配：`3d-web-experience`、`frontend`、`ui-design`、`landing-page-design`

## 触发条件
- 用户提到或暗示：滚动动画
- 用户提到或暗示：视差
- 用户提到或暗示：滚动叙事
- 用户提到或暗示：交互式故事
- 用户提到或暗示：电影级网站
- 用户提到或暗示：滚动体验
- 用户提到或暗示：沉浸式网页

## 使用限制

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来寻求澄清。
