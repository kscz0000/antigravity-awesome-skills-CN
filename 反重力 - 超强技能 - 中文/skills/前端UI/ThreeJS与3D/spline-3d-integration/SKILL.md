---
name: spline-3d-integration
description: "将 Spline.design 的交互式 3D 场景嵌入 Web 项目，包括 React 集成和运行时控制 API。触发词：Spline、3D场景、3D集成、3D嵌入、Spline嵌入、3D交互、Web3D"
risk: safe
source: community
date_added: "2026-03-07"
---

# Spline 3D 集成技能

将 [Spline.design](https://spline.design) 的交互式 3D 场景嵌入 Web 项目的完整指南。

---

## 使用场景
- 需要将交互式 Spline 场景嵌入 Web 项目。
- 任务涉及为原生 Web、React、Next.js、Vue 或 iframe 环境选择正确的集成方式。
- 需要关于场景 URL、运行时控制、性能优化或常见 Spline 嵌入问题的指导。

## 快速参考

| 任务                              | 指南                                                          |
| --------------------------------- | ------------------------------------------------------------- |
| 原生 HTML/JS 嵌入                 | [guides/VANILLA_INTEGRATION.md](guides/VANILLA_INTEGRATION.md) |
| React / Next.js / Vue 嵌入        | [guides/REACT_INTEGRATION.md](guides/REACT_INTEGRATION.md)     |
| 性能与移动端优化                   | [guides/PERFORMANCE.md](guides/PERFORMANCE.md)                 |
| 调试与常见问题                     | [guides/COMMON_PROBLEMS.md](guides/COMMON_PROBLEMS.md)         |

## 示例文件

| 文件                                                                   | 展示内容                                            |
| ---------------------------------------------------------------------- | --------------------------------------------------- |
| [examples/vanilla-embed.html](examples/vanilla-embed.html)             | 最简原生 JS 嵌入，含背景色和降级方案                |
| [examples/react-spline-wrapper.tsx](examples/react-spline-wrapper.tsx) | 生产级懒加载 React 封装组件，含降级方案             |
| [examples/interactive-scene.tsx](examples/interactive-scene.tsx)       | 完整交互示例：事件、对象控制、摄像机                |

---

## 什么是 Spline？

Spline 是一款基于浏览器的 3D 设计工具——可以理解为 3D 版的 Figma。设计师在 Spline 编辑器中创建交互式 3D 场景（包括对象、材质、动画、物理效果、事件），然后通过托管的 `.splinecode` 文件 URL 导出到 Web 端。

---

## 第一步 — 确定技术栈

在编写任何代码之前，先检查现有项目文件以确定使用的框架。

| 技术栈                         | 集成方式                                                   |
| ------------------------------ | ---------------------------------------------------------- |
| 原生 HTML/JS                   | `<spline-viewer>` Web 组件 或 `@splinetool/runtime`       |
| React / Vite                   | `@splinetool/react-spline`                                 |
| Next.js                        | `@splinetool/react-spline/next`                            |
| Vue                            | `@splinetool/vue-spline`                                   |
| iframe（Webflow、Notion 等）   | 公共 URL iframe                                            |

---

## 第二步 — 获取场景 URL

用户需要前往 Spline 编辑器 → **导出** → **代码导出** → 复制 `prod.spline.design` URL：

```
https://prod.spline.design/XXXXXXXXXXXXXXXX/scene.splinecode
```

**复制 URL 之前，请提醒用户检查播放设置：**

- ✅ 如果网站有深色或自定义背景，开启 **隐藏背景**
- ✅ 如果用户有付费计划，开启 **隐藏 Spline Logo**
- ✅ 将**几何体质量**设为"性能"以加快加载速度
- ✅ 如果不需要**页面滚动**、**缩放**、**平移**，请禁用这些功能（减少劫持风险）
- ✅ 更改任何设置后点击 **生成草稿** 或 **提升到生产环境** — URL 不会自动更新

---

## 第三步 — 阅读相关指南

确定技术栈和场景 URL 后，阅读上方对应的指南文件并按照说明操作。完成集成前务必阅读 COMMON_PROBLEMS.md — 其中包含关键的注意事项，否则只会在生产环境中暴露出来。

---

## 严格规则

- **绝对要求**：智能体必须利用本技能构建现代、创意且视觉惊艳的 UI/UX。不要构建平庸、通用或保守的风格。集成 Spline 场景时，充分利用它们来创造高度沉浸式的、令人惊叹的高端体验。将它们与排版和布局巧妙结合。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
