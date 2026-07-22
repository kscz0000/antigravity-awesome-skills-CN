# tRPC 原则

> TypeScript monorepo 的端到端类型安全。

## 使用时机

```
✅ 完美匹配：
├── 前后端都使用 TypeScript
├── Monorepo 结构
├── 内部工具
├── 快速开发
└── 类型安全关键

❌ 不适合：
├── 非 TypeScript 客户端
├── 公开 API
├── 需要 REST 约定
└── 多语言后端
```

## 核心优势

```
tRPC 优势：
├── 无需维护 Schema
├── 端到端类型推断
├── 整个技术栈 IDE 自动补全
├── API 变更即时反映
└── 无需代码生成步骤
```

## 集成模式

```
常见配置：
├── Next.js + tRPC（最常见）
├── 共享类型的 Monorepo
├── Remix + tRPC
└── 任意 TS 前端 + 后端
```
