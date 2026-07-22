# Angular 最佳实践

针对 AI 智能体和 LLM 优化的 Angular 应用性能优化与最佳实践。

## 概述

此技能提供以下方面的优先级性能指南：

- **变更检测** - OnPush 策略、Signals、Zoneless 应用
- **异步操作** - 避免瀑布流、SSR 预加载
- **包优化** - 懒加载、`@defer`、摇树优化
- **渲染性能** - TrackBy、虚拟滚动、CDK
- **SSR 与水合** - 服务端渲染模式
- **模板优化** - 结构指令、管道记忆化
- **状态管理** - 高效响应式模式
- **内存管理** - 订阅清理、分离引用

## 结构

`SKILL.md` 文件按优先级组织：

1. **关键优先级** - 最大的性能收益（变更检测、异步）
2. **高优先级** - 显著影响（包、渲染）
3. **中优先级** - 明显改进（SSR、模板）
4. **低优先级** - 增量收益（内存、清理）

每条规则包含：

- ❌ **错误** - 不应该做什么
- ✅ **正确** - 推荐的模式
- 📝 **原因** - 影响说明

## 快速参考清单

**新组件：**

- [ ] 使用 `ChangeDetectionStrategy.OnPush`
- [ ] 使用 Signals 管理响应式状态
- [ ] 使用 `@defer` 处理非关键内容
- [ ] 使用 `trackBy` 处理 `*ngFor` 循环
- [ ] 订阅必须有清理逻辑

**性能审查：**

- [ ] 无异步瀑布流（并行数据获取）
- [ ] 路由已懒加载
- [ ] 大型库已代码分割
- [ ] 图片使用 `NgOptimizedImage`

## 版本

当前版本：1.0.0（2026年2月）

## 参考资料

- [Angular Performance](https://angular.dev/guide/performance)
- [Zoneless Angular](https://angular.dev/guide/zoneless)
- [Angular SSR](https://angular.dev/guide/ssr)
