# SaaS

多租户应用程序，具有经过鉴权的仪表板、设置、计费。默认由鉴权守护。流量偏向函数时长（每用户数据获取）超过边缘请求。

## 典型计费形态

函数时长主导（每个仪表板请求完整运行函数——鉴权守护内容没有边缘缓存）。边缘请求随 API 表面增长。ISR 很少适用。图像优化很少体现。

## 优先级模式

1. **使用 React.cache() 进行每请求记忆化。** 在同一请求树中多个位置调用的 Server Component 通常重新查询数据库。`React.cache()` 在请求内去重。引用 `vercel-react-best-practices:server-cache-react`。
2. **在 Server Components 中并行数据加载。** 仪表板通常加载用户 + 组织 + 计费 + 最近活动。通过 `Promise.all` 并行运行全部四个。引用 `vercel-react-best-practices:async-parallel` 和 `:server-parallel-fetching`。
3. **Fluid Compute。** 鉴权守护的路由具有更高的冷启动敏感性（每次冷启动都是用户在等待）。如果冷启动信号出现在可观测性中，Fluid Compute 通常是正确的账户级建议。
4. **响应后的异步工作。** 活动日志、审计跟踪、分析事件——任何不阻塞用户的内容——应通过 `after()`（Next 15+）或来自 `@vercel/functions` 的 `waitUntil()` 运行。引用 `vercel-react-best-practices:server-after-nonblocking`。
5. **围绕昂贵 widget 的 Suspense 边界。** 仪表板外壳渲染快速；widget 流式进入。这改变了感知延迟而不改变底层查询。

## 常见陷阱

- **N+1 ORM 查询。** 一个列表页面循环遍历结果并按项获取相关记录。在 Prisma 的 `.map` 内使用 `.findUnique` 尤其常见。使用 `include` 或通过 DataLoader 批处理。
- **顺序会话+权限检查。** `await getSession()` 然后 `await checkPermissions()` 然后 `await loadData()` — 当权限检查不依赖于数据加载时，这些通常可以并行化。
- **Serverless 上没有连接池。** 没有 pooler 的 Prisma 在负载下耗尽数据库。连接池是必需的。
- **从客户端轮询状态。** 每次轮询都是一个函数调用。替换为 SWR + 按需重新验证，或使用由实际改变状态的变更触发的 `revalidateTag`。

## 交叉引用

- `vercel-react-best-practices:server-cache-react` — 每请求去重
- `vercel-react-best-practices:server-parallel-fetching` — 重组为 Promise.all
- `vercel-react-best-practices:async-suspense-boundaries` — 流式传输仪表板外壳
- `vercel-react-best-practices:server-after-nonblocking` — 延迟审计/分析写入（Next 15+）
- `vercel-react-best-practices:client-swr-dedup` — 用 SWR 替换轮询
- `https://vercel.com/docs/fluid-compute` — 当冷启动造成伤害时