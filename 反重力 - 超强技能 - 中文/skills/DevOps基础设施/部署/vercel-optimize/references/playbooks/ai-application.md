# AI 应用

由 LLM 支持的应用、智能体、代码沙箱工具、RAG 流水线。成本形态由按 token 的 AI Gateway 支出和 Sandbox 活跃计算时间主导，而不是边缘请求或函数时长。许多 AI 客户也有 SaaS 表面（鉴权、仪表板），但成本杠杆位于仪表板的上游。

## 典型计费形态

AI Gateway > Sandbox Active Compute > Function Duration > Function Invocations。边缘请求通常安静；ISR 很少适用。如果每个工具调用 span 以全保真度捕获，Observability Events 会快速攀升。

## 优先级模式

1. **提供者故障转移。** 在提供者之间（OpenAI + Anthropic，或模型族对）配置具有 active-active 后备链的 AI Gateway。关键路径智能体不能是单提供者的——否则来自一个提供者的 429 变成用户可见的故障。现场示例：MELI 运行自研 active-active 路由，因为针对单一提供者的 retry-on-error 降低了他们的 NLP-on-support 流程。
2. **OIDC 无密钥认证，而非显式 API 密钥。** 在生产中，使用 AI Gateway OIDC 绑定，以便请求由部署身份签名。在本地开发中，`vercel env run -- <cmd>` 每次运行轮换 OIDC。在仓库 env 变量中使用显式的 `AI_GATEWAY_API_KEY` 是倒退——它绕过了无密钥并创建了一个长期存在的密钥。
3. **Sandbox 复用优于每次请求 `Sandbox.create`。** 每个新沙箱至少消耗 1 分钟计费计算（启动 + 销毁四舍五入）。当不需要隔离时（单租户智能体、共享工作区），按名称池化沙箱（`sandbox.get(name)`）——死亡时自动快照 + 下次获取时自动恢复是持久化模型。
4. **`after()` / `waitUntil()` 用于工具日志记录。** 工具调用遥测、审计写入和分析不应阻塞用户响应。对于不影响流式响应的任何写入，使用 `after()`（Next 15+）或来自 `@vercel/functions` 的 `waitUntil()`。
5. **Fluid Compute 用于 JIT/进程热度。** 流式 LLM 响应受益于温热的进程；GraphQL/Apollo JIT 缓存 + 持久化文档计划只有在进程跨请求存活时才回本。Fluid 是默认；在 AI 工作负载上禁用它几乎总是错误的。

## 常见陷阱

- **单提供者锁定。** "我们正在使用 AI Gateway" 并不意味着故障转移——提供者列表仍然需要配置。单提供者网关是更薄的封装，而不是多提供者韧性。
- **每个请求一个 Sandbox。** 在每个请求的处理器内 `new Sandbox(...)` 而没有 `id` 参数会每次创建一个新的 microVM。当隔离允许时，池化更便宜。
- **BYOK 后备成本不可见。** AI Gateway 与 BYOK 在 429 / 提供者故障时静默回退到系统积分；成本从"免费 BYOK"迁移到"计费积分"，除非跟踪，否则没有单独信号。
- **Observability Events 失控。** 以 100% 采样率捕获每个工具调用 + 每个流式增量——events SKU 攀升至账单的 30% 以上。在扩大流量之前限制 span 基数。

## 交叉引用

- [external-api-critical-path](../support-topics/external-api-critical-path.md) — 顺序 vs 并行调用；AI Gateway 是众多外部 API 之一
- [fluid-compute-caveats](../support-topics/fluid-compute-caveats.md) — 模块状态危险和共享实例注意事项
- [function-duration-io-and-after](../support-topics/function-duration-io-and-after.md) — `after()` 用于响应后工具日志记录
- [observability-events-cost-attribution](../support-topics/observability-events-cost-attribution.md) — 当 Observability Events 攀升至账单的 20% 以上时
- [use-cache-remote-shared-origin-data](../support-topics/use-cache-remote-shared-origin-data.md) — 缓存共享的 LLM 上下文或嵌入查找
- `https://vercel.com/docs/ai-gateway` — 提供者配置、故障转移链
- `https://vercel.com/docs/vercel-sandbox` — `sandbox.get(name)` 和活跃计算计费