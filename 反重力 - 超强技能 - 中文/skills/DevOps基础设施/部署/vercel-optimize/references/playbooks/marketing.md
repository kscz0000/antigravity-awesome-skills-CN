# 营销站点

落地页、潜在客户捕获表单、A/B 测试变体、区域路由的首页。流量是突发性的（活动驱动高峰）。Bot 流量可能很大。

## 典型计费形态

边缘请求主导。图像优化很高（hero 图像、插图、产品截图）。视频内容的带宽很重要。函数时长通常较低——大多数页面是静态或 ISR。

## 优先级模式

1. **在边缘积极缓存。** 营销页面在活动更新之间很少改变。`Cache-Control: public, s-maxage=86400, stale-while-revalidate=604800` 使 CDN 保持 24 小时热度，并提供一周的过期服务。
2. **Bot 保护。** 营销活动吸引竞争对手抓取工具和不提供价值的 bot 流量，从而推高边缘请求。如果边缘成本 > $100/月且 Bot 保护被禁用，这几乎总是顶部平台建议。
3. **内容驱动部分的 ISR。** 客户徽标、推荐语、"最新博客文章"小部件、定价表——任何来自 CMS 的内容。每小时或 webhook 重新验证。
4. **A/B 测试逻辑在边缘，而不是页面中。** 边缘中间件用于变体分配；为每个变体缓存静态页面。不要在每个请求上呈现变体选择。
5. **延迟所有第三方 JS 到水合之后。** 分析、聊天小部件、营销像素、cookie 横幅。它们都不阻塞 LCP。引用 `vercel-react-best-practices:bundle-defer-third-party`。

## 常见陷阱

- **Hero 图像以原生分辨率提供。** 每个视口（包括移动设备）上的 4MP hero 图像。带 `sizes` 的 `next/image` 是必需的。
- **Cookie 横幅阻塞首次绘制。** 符合 GDPR 的 cookie 横幅经常在头部同步渲染。延迟；在水合之后渲染；通过一个小的内联脚本持久化同意状态。
- **跟踪像素瀑布。** 链式加载的三个不同的分析服务。在水合之后并行加载它们；更好的是，通过 webhook 将其中一些替换为服务端跟踪。
- **`/api/contact` 是唯一的函数但运行很热。** 营销站点大多是静态的，但联系表单会被 bot 垃圾信息攻击。在中间件处限流；考虑一个用于外发电子邮件的队列。

## 交叉引用

- `https://vercel.com/docs/bot-management` — 几乎总是正确的平台建议
- `https://vercel.com/docs/incremental-static-regeneration` — 用于 CMS 驱动的部分
- `https://nextjs.org/docs/app/api-reference/components/image` — hero/插图优化
- `vercel-react-best-practices:bundle-defer-third-party` — 延迟分析/像素
- `https://nextjs.org/docs/app/building-your-application/routing/middleware` — 边缘 A/B 变体路由