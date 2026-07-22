# API 风格选择（2025）

> REST 与 GraphQL 与 tRPC —— 何时使用何种方案？

## 决策树

```
API 消费者是谁？
│
├── 公开 API / 多平台
│   └── REST + OpenAPI（最广泛兼容性）
│
├── 复杂数据需求 / 多前端
│   └── GraphQL（灵活查询）
│
├── TypeScript 前端 + 后端（monorepo）
│   └── tRPC（端到端类型安全）
│
├── 实时 / 事件驱动
│   └── WebSocket + AsyncAPI
│
└── 内部微服务
    └── gRPC（性能）或 REST（简洁）
```

## 对比

| 因素 | REST | GraphQL | tRPC |
|------|------|---------|------|
| **最适合** | 公开 API | 复杂应用 | TS monorepos |
| **学习曲线** | 低 | 中 | 低（如使用 TS） |
| **过度/不足获取** | 常见 | 已解决 | 已解决 |
| **类型安全** | 手动（OpenAPI） | 基于 Schema | 自动 |
| **缓存** | HTTP 原生 | 复杂 | 基于客户端 |

## 选择问题

1. API 消费者是谁？
2. 前端是否使用 TypeScript？
3. 数据关系有多复杂？
4. 缓存是否关键？
5. 公开还是内部 API？
