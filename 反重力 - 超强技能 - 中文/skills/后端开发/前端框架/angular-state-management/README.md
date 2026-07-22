# Angular 状态管理

为 AI 智能体和 LLM 优化的 Angular 应用完整状态管理模式。

## 概述

此技能为以下内容提供决策框架和实现模式：

- **基于 Signal 的服务** - 共享数据的轻量级状态
- **NgRx SignalStore** - 具有计算值的功能范围状态
- **NgRx Store** - 企业级全局状态管理
- **RxJS ComponentStore** - 响应式组件级状态
- **表单状态** - 响应式和模板驱动表单模式

## 结构

`SKILL.md` 文件组织如下：

1. **状态分类** - 本地、共享、全局、服务器、URL 和表单状态
2. **选择标准** - 选择正确解决方案的决策树
3. **实现模式** - 每种方法的完整示例
4. **迁移指南** - 从 BehaviorSubject 迁移到 Signals
5. **桥接模式** - 集成 Signals 与 RxJS

## 何时使用每种模式

- **Signal 服务**：共享 UI 状态（主题、用户偏好）
- **NgRx SignalStore**：具有计算值的功能状态
- **NgRx Store**：复杂的功能间依赖
- **ComponentStore**：组件范围的异步操作
- **Reactive Forms**：带验证的表单状态

## 版本

当前版本：1.0.0（2026年2月）

## 参考资料

- [Angular Signals](https://angular.dev/guide/signals)
- [NgRx](https://ngrx.io)
- [NgRx SignalStore](https://ngrx.io/guide/signals)
