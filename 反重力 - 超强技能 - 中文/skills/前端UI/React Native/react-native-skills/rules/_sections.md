# 章节

本文件定义所有章节、其顺序、影响等级和描述。
章节 ID（括号内）是用于分组规则的文件名前缀。

---

## 1. 核心渲染 (rendering)

**影响:** CRITICAL
**描述:** React Native 基础渲染规则。违反会导致运行时崩溃或 UI 损坏。

## 2. 列表性能 (list-performance)

**影响:** HIGH
**描述:** 优化虚拟化列表（FlatList、LegendList、FlashList），实现流畅滚动和快速更新。

## 3. 动画 (animation)

**影响:** HIGH
**描述:** GPU 加速动画、Reanimated 模式，以及避免手势期间的渲染抖动。

## 4. 滚动性能 (scroll)

**影响:** HIGH
**描述:** 跟踪滚动位置而不引起渲染抖动。

## 5. 导航 (navigation)

**影响:** HIGH
**描述:** 使用原生导航器进行堆栈和标签导航，而非基于 JS 的替代方案。

## 6. React 状态 (react-state)

**影响:** MEDIUM
**描述:** 管理 React 状态的模式，避免闭包过期和不必要的重渲染。

## 7. 状态架构 (state)

**影响:** MEDIUM
**描述:** 状态变量和派生值的基本原则。

## 8. React 编译器 (react-compiler)

**影响:** MEDIUM
**描述:** React Compiler 与 React Native 和 Reanimated 的兼容模式。

## 9. 用户界面 (ui)

**影响:** MEDIUM
**描述:** 图片、菜单、模态框、样式和平台一致界面的原生 UI 模式。

## 10. 设计系统 (design-system)

**影响:** MEDIUM
**描述:** 构建可维护组件库的架构模式。

## 11. 单仓 (monorepo)

**影响:** LOW
**描述:** 单仓中的依赖管理和原生模块配置。

## 12. 第三方依赖 (imports)

**影响:** LOW
**描述:** 包装和重新导出第三方依赖以提高可维护性。

## 13. JavaScript (js)

**影响:** LOW
**描述:** 微优化，如提升昂贵的对象创建。

## 14. 字体 (fonts)

**影响:** LOW
**描述:** 原生字体加载以提升性能。
