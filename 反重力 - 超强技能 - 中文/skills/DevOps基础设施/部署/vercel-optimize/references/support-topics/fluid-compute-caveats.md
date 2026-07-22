---
id: fluid-compute-caveats
title: Fluid compute caveats
status: active
candidateKinds: ["platform_fluid_compute", "cold_start"]
frameworks: ["*"]
priority: 80
citations: ["https://vercel.com/docs/fluid-compute"]
maxBriefChars: 900
---

## 调查简报
Fluid compute 是一个项目级杠杆。当设置关闭且指标显示冷启动或温热实例复用压力时使用它。Fluid 可以在一个函数实例中处理多个调用；避免模块作用域中的每请求状态。

## 需要检查的证据
检查项目事实、`startTypeSplit`、冷热延迟对比以及承载冷启动份额的路由。启用 Fluid 时，审查 Fluid 浮出水面的模块状态危险（而不是创建的）：模块作用域的可变状态、持有每用户数据的懒单例、按每请求输入键控的全局变量。

## 何时不建议
当项目事实显示 Fluid 已启用时，不要推荐启用 fluid compute。不要将其框定为文件级代码修复。

## 验证
说明项目设置、冷启动率或回退慢路由信号、受影响路由的集中度。如果启用，将模块状态审查作为后续跟进。