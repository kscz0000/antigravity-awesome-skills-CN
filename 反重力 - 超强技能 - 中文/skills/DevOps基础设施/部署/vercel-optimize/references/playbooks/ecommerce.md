# 电商

具有购物车、结账、产品目录的店面。通常集成 Stripe。流量偏向目录浏览（可缓存）和结账（不可缓存）。

## 典型计费形态

边缘请求主导（目录浏览、图像资产流量）→ 图像优化（产品图像）→ 函数时长（购物车/结账 API）。当产品页面使用 ISR 时，ISR 读取很重要。

## 优先级模式

1. **目录页面：激进的 ISR + 图像优化。** 产品列表和产品详情页面应该 ISR 配合合理的 `revalidate`（60s-3600s）。每个图像都应该经过 `next/image`（或框架等效项）。对于 Vercel 托管的店面，图像成本可以主导其他一切。
2. **结账：保持动态，但并行化外部调用。** 购物车/结账/支付路由正确地是动态的。胜利在于减少它们的函数时长——对 Stripe + 库存 + 税务服务的独立调用使用 `Promise.all`。引用 `vercel-react-best-practices:async-parallel`。
3. **购物车抽屉水合：将 `'use client'` 提升到叶子节点。** 购物车组件是交互式的，但包裹它们的页面不应如此。提升服务端渲染部分向上；只有按钮/表单是客户端。
4. **Webhooks：单独的，而不是在用户路径上。** Stripe/Shopify webhook 处理程序应作为它们自己的路由存在于具有短时长限制的位置。它们不与店面共享流量模式。
5. **仅用于 A/B + 区域路由的边缘中间件。** 目录区域路由很合适。鉴权/购物车状态属于动态页面，而不是中间件。

## 常见陷阱

- **产品图像按原始方式提供。** 数百个变体的 `<img src={product.imageUrl}>` 比账单其他所有部分加起来更贵。始终使用 next/image。
- **店面首页上的 `force-dynamic`。** 通常在开发期间添加以测试购物车状态行为，从未删除。无情地审查。
- **顺序的 Stripe 调用。** "Create customer" → "create subscription" → "create invoice" 通常是三个顺序的 await，其中两个可以并行。
- **产品搜索上的 Bot 流量。** 营销驱动的流量 + 搜索路由上的 bot 流量推高边缘请求成本。Bot 保护通常在一个月内回本。

## 交叉引用

- `vercel-react-best-practices:async-parallel` — 在结账中并行化 Stripe/库存/税务调用
- `vercel-react-best-practices:async-suspense-boundaries` — 流式传输结账外壳，稍后填充购物车抽屉
- `vercel-react-best-practices:bundle-defer-third-party` — 在水合后延迟分析（GA、Mixpanel）
- `https://nextjs.org/docs/app/api-reference/components/image` — 用于目录图像修复
- `https://vercel.com/docs/bot-management` — 用于搜索/产品路由上的 bot 流量