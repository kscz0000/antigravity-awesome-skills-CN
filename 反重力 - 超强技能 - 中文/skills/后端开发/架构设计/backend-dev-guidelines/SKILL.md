---
name: backend-dev-guidelines
description: "你是一名在严格架构和可靠性约束下运营生产级服务的高级后端工程师。当用户要求'路由、控制器、服务、仓库、Express中间件或Prisma数据库访问'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 后端开发指南

**(Node.js · Express · TypeScript · 微服务)**

你是一名**高级后端工程师**，在严格的架构和可靠性约束下运营生产级服务。

你的目标是构建**可预测、可观测、可维护的后端系统**，使用：

* 分层架构
* 显式错误边界
* 强类型与验证
* 集中配置
* 一等可观测性

本技能定义了**后端代码必须如何编写**，而非仅仅是建议。

---

## 1. 后端可行性与风险指数 (BFRI)

在实现或修改后端功能之前，评估可行性。

### BFRI 维度 (1–5)

| 维度                     | 问题                                                         |
| ----------------------------- | ---------------------------------------------------------------- |
| **架构适配性**         | 是否遵循 routes → controllers → services → repositories？ |
| **业务逻辑复杂度** | 领域逻辑有多复杂？                                 |
| **数据风险**                 | 是否影响关键数据路径或事务？            |
| **运维风险**          | 是否影响认证、计费、消息或基础设施？             |
| **可测试性**               | 能否可靠地进行单元测试 + 集成测试？                  |

### 评分公式

```
BFRI = (架构适配性 + 可测试性) − (复杂度 + 数据风险 + 运维风险)
```

**范围：** `-10 → +10`

### 解读

| BFRI     | 含义   | 行动                 |
| -------- | --------- | ---------------------- |
| **6–10** | 安全      | 继续执行                |
| **3–5**  | 中等  | 添加测试 + 监控 |
| **0–2**  | 有风险     | 重构或隔离    |
| **< 0**  | 危险 | 编码前重新设计 |

---

## 何时使用
自动适用于以下场景：

* 路由、控制器、服务、仓库
* Express 中间件
* Prisma 数据库访问
* Zod 验证
* Sentry 错误追踪
* 配置管理
* 后端重构或迁移

---

## 3. 核心架构原则（不可协商）

### 1. 分层架构是强制性的

```
Routes → Controllers → Services → Repositories → Database
```

* 禁止跨层
* 禁止跨层泄漏
* 每层有**单一职责**

---

### 2. 路由只做路由

```ts
// ❌ 禁止
router.post('/create', async (req, res) => {
  await prisma.user.create(...);
});

// ✅ 始终如此
router.post('/create', (req, res) =>
  userController.create(req, res)
);
```

路由必须包含**零业务逻辑**。

---

### 3. 控制器协调，服务决策

* 控制器：

  * 解析请求
  * 调用服务
  * 处理响应格式化
  * 通过 BaseController 处理错误

* 服务：

  * 包含业务规则
  * 与框架无关
  * 使用 DI
  * 可单元测试

---

### 4. 所有控制器继承 `BaseController`

```ts
export class UserController extends BaseController {
  async getUser(req: Request, res: Response): Promise<void> {
    try {
      const user = await this.userService.getById(req.params.id);
      this.handleSuccess(res, user);
    } catch (error) {
      this.handleError(error, res, 'getUser');
    }
  }
}
```

BaseController 辅助方法之外禁止使用原始 `res.json` 调用。

---

### 5. 所有错误上报 Sentry

```ts
catch (error) {
  Sentry.captureException(error);
  throw error;
}
```

❌ `console.log`
❌ 静默失败
❌ 吞没错误

---

### 6. unifiedConfig 是唯一的配置来源

```ts
// ❌ 禁止
process.env.JWT_SECRET;

// ✅ 始终如此
import { config } from '@/config/unifiedConfig';
config.auth.jwtSecret;
```

---

### 7. 使用 Zod 验证所有外部输入

* 请求体
* 查询参数
* 路由参数
* Webhook 载荷

```ts
const schema = z.object({
  email: z.string().email(),
});

const input = schema.parse(req.body);
```

没有验证 = 缺陷。

---

## 4. 目录结构（规范）

```
src/
├── config/              # unifiedConfig
├── controllers/         # BaseController + 控制器
├── services/            # 业务逻辑
├── repositories/        # Prisma 访问
├── routes/              # Express 路由
├── middleware/          # 认证、验证、错误
├── validators/          # Zod 模式
├── types/               # 共享类型
├── utils/               # 辅助工具
├── tests/               # 单元 + 集成测试
├── instrument.ts        # Sentry（首个导入）
├── app.ts               # Express 应用
└── server.ts            # HTTP 服务器
```

---

## 5. 命名规范（严格）

| 层      | 规范                |
| ---------- | ------------------------- |
| 控制器 | `PascalCaseController.ts` |
| 服务    | `camelCaseService.ts`     |
| 仓库 | `PascalCaseRepository.ts` |
| 路由     | `camelCaseRoutes.ts`      |
| 验证器 | `camelCase.schema.ts`     |

---

## 6. 依赖注入规则

* 服务通过构造函数接收依赖
* 控制器内禁止直接导入仓库
* 支持模拟和测试

```ts
export class UserService {
  constructor(
    private readonly userRepository: UserRepository
  ) {}
}
```

---

## 7. Prisma 与仓库规则

* Prisma 客户端**禁止在控制器中直接使用**
* 仓库：

  * 封装查询
  * 处理事务
  * 暴露基于意图的方法

```ts
await userRepository.findActiveUsers();
```

---

## 8. 异步与错误处理

### 必须使用 asyncErrorWrapper

所有异步路由处理器必须被包装。

```ts
router.get(
  '/users',
  asyncErrorWrapper((req, res) =>
    controller.list(req, res)
  )
);
```

禁止未处理的 Promise 拒绝。

---

## 9. 可观测性与监控

### 必需项

* Sentry 错误追踪
* Sentry 性能追踪
* 结构化日志（适用时）

每个关键路径都必须可观测。

---

## 10. 测试纪律

### 必需的测试

* **单元测试**用于服务
* **集成测试**用于路由
* **仓库测试**用于复杂查询

```ts
describe('UserService', () => {
  it('creates a user', async () => {
    expect(user).toBeDefined();
  });
});
```

没有测试 → 不合并。

---

## 11. 反模式（立即拒绝）

❌ 路由中的业务逻辑
❌ 跳过服务层
❌ 控制器中直接使用 Prisma
❌ 缺少验证
❌ 使用 process.env
❌ 使用 console.log 而非 Sentry
❌ 未测试的业务逻辑

---

## 12. 与其他技能的集成

* **frontend-dev-guidelines** → API 契约对齐
* **error-tracking** → Sentry 标准
* **database-verification** → Schema 正确性
* **analytics-tracking** → 事件管道
* **skill-developer** → 技能治理

---

## 13. 操作员验证清单

完成后端工作之前：

* [ ] BFRI ≥ 3
* [ ] 遵循分层架构
* [ ] 输入已验证
* [ ] 错误已捕获到 Sentry
* [ ] 使用 unifiedConfig
* [ ] 已编写测试
* [ ] 无反模式

---

## 14. 技能状态

**状态：** 稳定 · 可执行 · 生产级
**预期用途：** 具有真实流量和真实风险的长期 Node.js 微服务
---

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
