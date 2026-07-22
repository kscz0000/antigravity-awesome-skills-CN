---
name: nodejs-best-practices
description: "Node.js 开发原则与决策指南。框架选择、异步模式、安全与架构。教你思考，而非照搬代码。当用户要求'Node.js 最佳实践'、'Node.js 架构'、'框架选择'、'异步模式'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Node.js 最佳实践

> 2025 年 Node.js 开发的原则与决策指南。
> **学会思考，而非死记硬背代码模式。**

## 何时使用
在进行 Node.js 架构决策、选择框架、设计异步模式或应用安全和部署最佳实践时使用此技能。

---

## ⚠️ 如何使用此技能

此技能教你**决策原则**，而非可复制的固定代码。

- 不清楚时询问用户偏好
- 根据上下文选择框架/模式
- 不要每次都用同一个默认方案

---

## 1. 框架选择（2025）

### 决策树

```
What are you building?
│
├── Edge/Serverless (Cloudflare, Vercel)
│   └── Hono (zero-dependency, ultra-fast cold starts)
│
├── High Performance API
│   └── Fastify (2-3x faster than Express)
│
├── Enterprise/Team familiarity
│   └── NestJS (structured, DI, decorators)
│
├── Legacy/Stable/Maximum ecosystem
│   └── Express (mature, most middleware)
│
└── Full-stack with frontend
    └── Next.js API Routes or tRPC
```

### 比较原则

| 因素 | Hono | Fastify | Express |
|--------|------|---------|---------|
| **最适合** | Edge、serverless | 性能 | 遗留项目、学习 |
| **冷启动** | 最快 | 快 | 中等 |
| **生态系统** | 增长中 | 良好 | 最大 |
| **TypeScript** | 原生 | 优秀 | 良好 |
| **学习曲线** | 低 | 中等 | 低 |

### 选择时需要问的问题：
1. 部署目标是什么？
2. 冷启动时间是否关键？
3. 团队是否有现有经验？
4. 是否有遗留代码需要维护？

---

## 2. 运行时考虑（2025）

### 原生 TypeScript

```
Node.js 22+: --experimental-strip-types
├── Run .ts files directly
├── No build step needed for simple projects
└── Consider for: scripts, simple APIs
```

### 模块系统决策

```
ESM (import/export)
├── Modern standard
├── Better tree-shaking
├── Async module loading
└── Use for: new projects

CommonJS (require)
├── Legacy compatibility
├── More npm packages support
└── Use for: existing codebases, some edge cases
```

### 运行时选择

| 运行时 | 最适合 |
|---------|----------|
| **Node.js** | 通用、最大生态系统 |
| **Bun** | 性能、内置打包器 |
| **Deno** | 安全优先、内置 TypeScript |

---

## 3. 架构原则

### 分层结构概念

```
Request Flow:
│
├── Controller/Route Layer
│   ├── Handles HTTP specifics
│   ├── Input validation at boundary
│   └── Calls service layer
│
├── Service Layer
│   ├── Business logic
│   ├── Framework-agnostic
│   └── Calls repository layer
│
└── Repository Layer
    ├── Data access only
    ├── Database queries
    └── ORM interactions
```

### 为什么重要：
- **可测试性**：独立 mock 各层
- **灵活性**：无需修改业务逻辑即可替换数据库
- **清晰性**：每层职责单一

### 何时简化：
- 小脚本 → 单文件即可
- 原型 → 减少结构也是可接受的
- 始终问自己："这个会增长吗？"

---

## 4. 错误处理原则

### 集中式错误处理

```
Pattern:
├── Create custom error classes
├── Throw from any layer
├── Catch at top level (middleware)
└── Format consistent response
```

### 错误响应哲学

```
Client gets:
├── Appropriate HTTP status
├── Error code for programmatic handling
├── User-friendly message
└── NO internal details (security!)

Logs get:
├── Full stack trace
├── Request context
├── User ID (if applicable)
└── Timestamp
```

### 状态码选择

| 场景 | 状态码 | 何时使用 |
|-----------|--------|------|
| 输入错误 | 400 | 客户端发送无效数据 |
| 未认证 | 401 | 缺少或无效凭证 |
| 无权限 | 403 | 已认证但无权访问 |
| 未找到 | 404 | 资源不存在 |
| 冲突 | 409 | 重复或状态冲突 |
| 验证失败 | 422 | Schema 有效但业务规则失败 |
| 服务器错误 | 500 | 我们的错误，记录一切 |

---

## 5. 异步模式原则

### 各模式使用时机

| 模式 | 使用场景 |
|---------|----------|
| `async/await` | 顺序异步操作 |
| `Promise.all` | 并行独立操作 |
| `Promise.allSettled` | 并行但部分可能失败 |
| `Promise.race` | 超时或先到先得 |

### 事件循环意识

```
I/O-bound (async helps):
├── Database queries
├── HTTP requests
├── File system
└── Network operations

CPU-bound (async doesn't help):
├── Crypto operations
├── Image processing
├── Complex calculations
└── → Use worker threads or offload
```

### 避免事件循环阻塞

- 生产环境永远不要使用同步方法（fs.readFileSync 等）
- 将 CPU 密集型工作卸载
- 大数据使用流式处理

---

## 6. 验证原则

### 在边界处验证

```
Where to validate:
├── API entry point (request body/params)
├── Before database operations
├── External data (API responses, file uploads)
└── Environment variables (startup)
```

### 验证库选择

| 库 | 最适合 |
|---------|----------|
| **Zod** | TypeScript 优先、类型推断 |
| **Valibot** | 更小打包体积（可 tree-shake） |
| **ArkType** | 性能关键场景 |
| **Yup** | 现有 React Form 使用 |

### 验证哲学

- 快速失败：尽早验证
- 具体明确：清晰的错误消息
- 不信任：即使是"内部"数据

---

## 7. 安全原则

### 安全检查清单（非代码）

- [ ] **输入验证**：所有输入已验证
- [ ] **参数化查询**：SQL 不使用字符串拼接
- [ ] **密码哈希**：使用 bcrypt 或 argon2
- [ ] **JWT 验证**：始终验证签名和过期时间
- [ ] **速率限制**：防止滥用
- [ ] **安全头**：Helmet.js 或等效方案
- [ ] **HTTPS**：生产环境全面使用
- [ ] **CORS**：正确配置
- [ ] **密钥**：仅使用环境变量
- [ ] **依赖**：定期审计

### 安全心态

```
Trust nothing:
├── Query params → validate
├── Request body → validate
├── Headers → verify
├── Cookies → validate
├── File uploads → scan
└── External APIs → validate response
```

---

## 8. 测试原则

### 测试策略选择

| 类型 | 目的 | 工具 |
|------|---------|-------|
| **单元测试** | 业务逻辑 | node:test、Vitest |
| **集成测试** | API 端点 | Supertest |
| **端到端测试** | 完整流程 | Playwright |

### 测试优先级

1. **关键路径**：认证、支付、核心业务
2. **边界情况**：空输入、边界值
3. **错误处理**：失败时会发生什么？
4. **不值得测试**：框架代码、简单 getter

### 内置测试运行器（Node.js 22+）

```
node --test src/**/*.test.ts
├── No external dependency
├── Good coverage reporting
└── Watch mode available
```

---

## 10. 应避免的反模式

### ❌ 不要：
- 新 edge 项目使用 Express（用 Hono）
- 生产代码使用同步方法
- 业务逻辑放在 controller 中
- 跳过输入验证
- 硬编码密钥
- 不验证就信任外部数据
- CPU 工作阻塞事件循环

### ✅ 要：
- 根据上下文选择框架
- 不清楚时询问用户偏好
- 增长型项目使用分层架构
- 验证所有输入
- 密钥使用环境变量
- 优化前先做性能分析

---

## 11. 决策检查清单

实现前检查：

- [ ] **询问了用户技术栈偏好？**
- [ ] **为当前上下文选择了合适的框架？**（而非默认）
- [ ] **考虑了部署目标？**
- [ ] **规划了错误处理策略？**
- [ ] **识别了验证点？**
- [ ] **考虑了安全需求？**

---

> **记住**：Node.js 最佳实践关乎决策，而非死记模式。每个项目都值得根据其需求进行全新考量。

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。