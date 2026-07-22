---
name: expo-observe
description: 用于与 EAS Observe 相关的任何任务——向 Expo 项目添加 `expo-observe`（AppMetricsRoot/ObserveRoot 高阶组件、markInteractive、useObserve 钩子，以及用于按路由指标的 Expo Router / React Navigation 集成），通过 EAS CLI 查询（`eas observe:metrics-summary`、...
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-observe
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# EAS Observe
## 何时使用

当你需要处理与 EAS Observe 相关的任何任务时使用本技能——向 Expo 项目添加 `expo-observe`（AppMetricsRoot/ObserveRoot 高阶组件、markInteractive、useObserve 钩子，以及用于按路由指标的 Expo Router / React Navigation 集成），通过 EAS CLI 查询（`eas observe:metrics-summary`、...


EAS Observe 跟踪生产 Expo 应用的启动、导航和自定义事件性能。

> **权威来源：** https://docs.expo.dev/eas/observe/ —— 当涉及 API 细节时，请始终查阅官方文档，特别是入门、配置、集成以及指标参考页面。EAS Observe 在持续演进；本技能中的参考资料在编写时力求准确，但可能滞后于官方文档。

## 应阅读哪份参考资料

`./references/` 目录下的三个参考文件涵盖了人们通常使用本技能的三类场景：

- **将 EAS Observe 添加到项目中** → [`./references/setup.md`](./references/setup.md)。安装依赖，包裹根布局（SDK 55 使用 `AppMetricsRoot`，SDK 56+ 使用 `ObserveRoot`），调用 `markInteractive()`（SDK 55 通过全局，SDK 56+ 通过 `useObserve()` 钩子），以及通过 Expo Router / React Navigation 集成启用可选的按路由导航指标。
- **从终端查询指标** → [`./references/queries.md`](./references/queries.md)。五个 `eas observe:*` 命令 —— `metrics-summary`、`metrics`、`routes`、`events`、`versions` —— 包括其标志、表格布局、JSON 结构以及常见工作流。
- **阅读仪表板或 CLI 输出** → [`./references/metrics.md`](./references/metrics.md）。每个指标的目标阈值、TTI 中 `frameRate.*` 参数的含义，以及区分"慢但流畅"的启动与主线程争用或硬卡顿的诊断模式。

## 文档快速链接

- 入门：https://docs.expo.dev/eas/observe/get-started/
- 仪表板指南：https://docs.expo.dev/eas/observe/dashboard/
- 指标参考：https://docs.expo.dev/eas/observe/reference/metrics/
- Expo Router 集成：https://docs.expo.dev/eas/observe/integrations/expo-router/
- React Navigation 集成：https://docs.expo.dev/eas/observe/integrations/react-navigation/
- 配置：https://docs.expo.dev/eas/observe/configuration/

## 局限性

- 仅当任务明确匹配本技能的上游产品或 API 范围时才使用本技能。
- 在做出更改之前，请根据最新的官方文档验证命令、API 行为、定价、配额、凭据及部署效果。
- 不要将生成示例视为针对特定环境的测试、安全审查或用户对破坏性/高成本操作的审批的替代品。
