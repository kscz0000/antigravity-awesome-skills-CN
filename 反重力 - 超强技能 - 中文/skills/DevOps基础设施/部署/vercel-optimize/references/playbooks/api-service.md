# API 服务

无头 API 后端。没有 UI 路由。通常由移动应用、合作伙伴集成或其他 Vercel 项目通过 rewrites 消费。

## 典型计费形态

函数时长主导（每个请求都是一个函数调用）。边缘请求随 API 流量缩放。当服务是第三方 API（Stripe、Twilio 等）的薄壳时，外部 API 成本很重要。

## 优先级模式

1. **在边缘缓存 GET 响应。** 幂等的 GET 端点（目录读取、状态检查、公共数据）应附带 `Cache-Control: public, s-maxage=<seconds>, stale-while-revalidate=<longer>` 部署。CDN 在不调用函数的情况下为重复调用者服务。
2. **在边缘限流，而非函数内。** 具有正确 matcher 范围的中间件在滥用客户端到达你的函数时长账单之前处理它们。
3. **并行外部 API 调用。** 一个"类似 checkout"的端点按顺序调用 Stripe + 库存 + 邮件服务是该画像中最常见的 slow_route。`Promise.all` 是显而易见的修复。
4. **响应后后台工作。** 用于分析、webhook-to-self 和任何不影响响应的写入的 `after()`（Next 15+）。
5. **连接池。** 来自 serverless 函数实例的直接 PG 连接耗尽数据库。使用 PgBouncer / Prisma Accelerate / Neon 的 pooler。

## 常见陷阱

- **公共 GET 上没有 `Cache-Control`。** 这是该画像中最常见的发现，也是最简单的修复。
- **鉴权检查与数据加载串行。** `await checkAuth()` 然后 `await loadData()` — 这些通常是独立的，如果你的鉴权路径不依赖于数据，可以并行运行。
- **一个用户的外部 API 扇出。** 一个"为我构建个人资料"的端点按顺序调用 5 个第三方。即使每个用户的小延迟改善，乘以每个用户也是巨大的。
- **请求路径上的长时间异步操作。** 图像生成、PDF 渲染、大型报告计算。将这些移到后台队列或 `after()`。

## 交叉引用

- `https://vercel.com/docs/caching/cdn-cache` — GET 处理器的 Cache-Control 修复
- `vercel-react-best-practices:async-parallel` — 并行化外部 API 调用
- `vercel-react-best-practices:server-after-nonblocking` — `after()` 用于响应后工作
- `https://vercel.com/docs/fluid-compute` — 当不常调用的端点上的冷启动造成伤害时
- `https://nextjs.org/docs/app/building-your-application/routing/middleware` — 用于限流中间件