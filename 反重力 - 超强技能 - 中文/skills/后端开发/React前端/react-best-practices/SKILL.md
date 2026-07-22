---
name: react-best-practices
description: "React 和 Next.js 应用的综合性能优化指南，由 Vercel 维护。适用于编写新的 React 组件或 Next.js 页面、实现数据获取（客户端或服务端）、或审查代码性能问题时使用。触发词：React 最佳实践、React 性能优化、Next.js 优化、React 重构、bundle 优化、React 代码审查"
risk: safe
source: community
date_added: "2026-02-27"
---

# Vercel React 最佳实践

React 和 Next.js 应用的综合性能优化指南，由 Vercel 维护。涵盖 8 个类别共 45 条规则，按影响力优先级排列，用于指导自动化重构和代码生成。

## 何时使用
在以下场景参考本指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码中的性能问题
- 重构现有的 React/Next.js 代码
- 优化 bundle 体积或加载时间

## 按优先级排列的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除瀑布流 | CRITICAL | `async-` |
| 2 | Bundle 体积优化 | CRITICAL | `bundle-` |
| 3 | 服务端性能 | HIGH | `server-` |
| 4 | 客户端数据获取 | MEDIUM-HIGH | `client-` |
| 5 | 重渲染优化 | MEDIUM | `rerender-` |
| 6 | 渲染性能 | MEDIUM | `rendering-` |
| 7 | JavaScript 性能 | LOW-MEDIUM | `js-` |
| 8 | 高级模式 | LOW | `advanced-` |

## 快速参考

### 1. 消除瀑布流 (CRITICAL)

- `async-defer-await` - 将 await 移到实际使用的分支中
- `async-parallel` - 对独立操作使用 Promise.all()
- `async-dependencies` - 对部分依赖使用 better-all
- `async-api-routes` - 在 API 路由中尽早启动 promise，延迟 await
- `async-suspense-boundaries` - 使用 Suspense 实现流式内容

### 2. Bundle 体积优化 (CRITICAL)

- `bundle-barrel-imports` - 直接导入，避免 barrel 文件
- `bundle-dynamic-imports` - 对大型组件使用 next/dynamic
- `bundle-defer-third-party` - 在 hydration 之后再加载分析/日志
- `bundle-conditional` - 仅在功能激活时加载模块
- `bundle-preload` - 在 hover/focus 时预加载以提升感知速度

### 3. 服务端性能 (HIGH)

- `server-cache-react` - 使用 React.cache() 进行请求级去重
- `server-cache-lru` - 使用 LRU 缓存实现跨请求缓存
- `server-serialization` - 最小化传递给客户端组件的数据
- `server-parallel-fetching` - 重构组件以并行获取数据
- `server-after-nonblocking` - 使用 after() 实现非阻塞操作

### 4. 客户端数据获取 (MEDIUM-HIGH)

- `client-swr-dedup` - 使用 SWR 实现自动请求去重
- `client-event-listeners` - 去重全局事件监听器

### 5. 重渲染优化 (MEDIUM)

- `rerender-defer-reads` - 不要订阅仅在回调中使用的状态
- `rerender-memo` - 将昂贵的计算提取到 memo 组件中
- `rerender-dependencies` - 在 effect 中使用原始类型依赖
- `rerender-derived-state` - 订阅派生的布尔值，而非原始值
- `rerender-functional-setstate` - 使用函数式 setState 保持回调稳定
- `rerender-lazy-state-init` - 对昂贵的初始值传函数给 useState
- `rerender-transitions` - 对非紧急更新使用 startTransition

### 6. 渲染性能 (MEDIUM)

- `rendering-animate-svg-wrapper` - 动画应用于 div 包装器而非 SVG 元素
- `rendering-content-visibility` - 对长列表使用 content-visibility
- `rendering-hoist-jsx` - 将静态 JSX 提取到组件外部
- `rendering-svg-precision` - 降低 SVG 坐标精度
- `rendering-hydration-no-flicker` - 对仅客户端数据使用内联脚本
- `rendering-activity` - 使用 Activity 组件处理显示/隐藏
- `rendering-conditional-render` - 使用三元运算符而非 && 进行条件渲染

### 7. JavaScript 性能 (LOW-MEDIUM)

- `js-batch-dom-css` - 通过 class 或 cssText 批量修改 CSS
- `js-index-maps` - 为重复查找构建 Map
- `js-cache-property-access` - 在循环中缓存对象属性访问
- `js-cache-function-results` - 在模块级 Map 中缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取
- `js-combine-iterations` - 将多个 filter/map 合并为一次循环
- `js-length-check-first` - 在昂贵比较之前先检查数组长度
- `js-early-exit` - 函数中尽早返回
- `js-hoist-regexp` - 将 RegExp 创建提升到循环外部
- `js-min-max-loop` - 用循环求最小/最大值而非排序
- `js-set-map-lookups` - 使用 Set/Map 实现 O(1) 查找
- `js-tosorted-immutable` - 使用 toSorted() 实现不可变性

### 8. 高级模式 (LOW)

- `advanced-event-handler-refs` - 将事件处理器存储在 ref 中
- `advanced-use-latest` - useLatest 用于稳定的回调引用

## 使用方法

阅读各规则文件获取详细说明和代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

每条规则文件包含：
- 重要性的简要说明
- 错误代码示例及解释
- 正确代码示例及解释
- 额外的上下文和参考

## 完整编译文档

包含所有规则展开的完整指南：`AGENTS.md`

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
