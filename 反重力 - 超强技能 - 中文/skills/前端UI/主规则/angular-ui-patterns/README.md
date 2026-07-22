# Angular UI 模式

现代 UI 模式，用于构建健壮的 Angular 应用，针对 AI 智能体和 LLM 进行优化。

## 概述

本技能涵盖以下核心 UI 模式：

- **加载状态** - 骨架屏与旋转器的决策树
- **错误处理** - 错误边界层级和恢复机制
- **渐进式披露** - 使用 `@defer` 实现延迟渲染
- **数据展示** - 处理空状态、加载状态和错误状态
- **表单模式** - 提交状态和验证反馈
- **对话框/模态框模式** - 正确的对话框生命周期管理

## 核心原则

1. **永不显示过期 UI** - 仅在没有数据时显示加载状态
2. **暴露所有错误** - 绝不静默失败
3. **乐观更新** - 在服务器确认前更新 UI
4. **渐进式披露** - 使用 `@defer` 加载非关键内容
5. **优雅降级** - 为失败的功能提供降级方案

## 结构

`SKILL.md` 文件包含：

1. **黄金法则** - 必须遵循的不可协商模式
2. **决策树** - 何时使用骨架屏 vs 旋转器
3. **代码示例** - 正确与错误的实现对比
4. **反模式** - 需要避免的常见错误

## 快速参考

```html
<!-- 数据状态的 Angular 模板模式 -->
@if (error()) {
<app-error-state [error]="error()" (retry)="load()" />
} @else if (loading() && !data()) {
<app-skeleton-state />
} @else if (!data()?.length) {
<app-empty-state message="No items found" />
} @else {
<app-data-display [data]="data()" />
}
```

## 版本

当前版本：1.0.0（2026 年 2 月）

## 参考资料

- [Angular @defer](https://angular.dev/guide/defer)
- [Angular Templates](https://angular.dev/guide/templates)
