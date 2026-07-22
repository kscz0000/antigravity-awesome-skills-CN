---
name: documentation-and-adrs
description: 记录决策与文档。用于制定架构决策、变更公共 API、发布功能，或记录未来工程师和智能体理解代码库所需的上下文时。触发词：ADR、架构决策记录、文档、决策记录、技术决策、ADR 模板。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/documentation-and-adrs
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 文档与架构决策记录（ADR）

## 概述

记录决策，而不仅仅是记录代码。最高价值的文档捕捉的是 *为什么* —— 即导致该决策的背景、约束和权衡。代码展示的是构建了 *什么*；文档解释的是 *为什么这样构建* 以及 *考虑了哪些替代方案*。这些上下文对未来在代码库中工作的人类和智能体至关重要。

## 适用场景

- 制定重要的架构决策
- 在多个相互竞争的方案之间做选择
- 新增或变更公共 API
- 发布改变用户可见行为的功能
- 为项目引入新的团队成员（或智能体）
- 当你发现自己反复解释同一件事时

**不适用场景：** 不要为显而易见的代码写文档。不要添加只是复述代码本身的注释。不要为一次性原型写文档。

## 架构决策记录（ADR）

ADR 捕捉重大技术决策背后的推理过程。它们是你能编写的最高价值的文档。

### 何时编写 ADR

- 选择框架、库或主要依赖项
- 设计数据模型或数据库 schema
- 选择身份验证策略
- 决定 API 架构（REST vs. GraphQL vs. tRPC）
- 在构建工具、托管平台或基础设施之间选择
- 任何推翻成本很高的决策

### ADR 模板

将 ADR 存放在 `docs/decisions/` 下，按顺序编号：

```markdown
# ADR-001：使用 PostgreSQL 作为主数据库

## 状态
已接受 | 被 ADR-XXX 取代 | 已弃用

## 日期
2025-01-15

## 背景
任务管理应用需要一个主数据库。关键需求：
- 关系型数据模型（用户、任务、团队及其关系）
- 任务状态变更需要 ACID 事务
- 支持对任务内容的全文检索
- 可用托管服务（团队规模小，运维能力有限）

## 决策
使用 PostgreSQL 配合 Prisma ORM。

## 已考虑的替代方案

### MongoDB
- 优点：schema 灵活，易于上手
- 缺点：我们的数据本质上是关系型的；需要手动管理关系
- 拒绝原因：在文档型数据库中存放关系数据会导致复杂的 join 或数据冗余

### SQLite
- 优点：零配置，嵌入式，读性能好
- 缺点：并发写入能力有限，生产环境无可用的托管服务
- 拒绝原因：不适用于生产环境的多用户 Web 应用

### MySQL
- 优点：成熟，生态广泛
- 缺点：PostgreSQL 在 JSON 支持、全文检索和生态工具方面更优
- 拒绝原因：PostgreSQL 更契合我们的功能需求

## 后果
- Prisma 提供类型安全的数据库访问和迁移管理
- 可以直接使用 PostgreSQL 的全文检索，无需再引入 Elasticsearch
- 团队需要具备 PostgreSQL 知识（通用技能，风险低）
- 使用托管服务（Supabase、Neon 或 RDS）
```

### ADR 生命周期

```
已提议 → 已接受 →（已取代 或 已弃用）
```

- **不要删除旧 ADR。** 它们承载着历史上下文。
- 当决策变更时，编写一份新 ADR，引用并取代旧的那份。

## 行内文档

### 何时添加注释

注释的是 *为什么*，而不是 *做了什么*：

```typescript
// BAD：复述代码本身
// Increment counter by 1
counter += 1;

// GOOD：解释不显而易见的意图
// Rate limit uses a sliding window — reset counter at window boundary,
// not on a fixed schedule, to prevent burst attacks at window edges
if (now - windowStart > WINDOW_SIZE_MS) {
  counter = 0;
  windowStart = now;
}
```

### 何时不要注释

```typescript
// Don't comment self-explanatory code
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Don't leave TODO comments for things you should just do now
// TODO: add error handling  ← Just add it

// Don't leave commented-out code
// const oldImplementation = () => { ... }  ← Delete it, git has history
```

### 记录已知的坑

```typescript
/**
 * IMPORTANT: This function must be called before the first render.
 * If called after hydration, it causes a flash of unstyled content
 * because the theme context isn't available during SSR.
 *
 * See ADR-003 for the full design rationale.
 */
export function initializeTheme(theme: Theme): void {
  // ...
}
```

## API 文档

针对公共 API（REST、GraphQL、库接口）：

### 与类型同行（TypeScript 首选）

```typescript
/**
 * Creates a new task.
 *
 * @param input - Task creation data (title required, description optional)
 * @returns The created task with server-generated ID and timestamps
 * @throws {ValidationError} If title is empty or exceeds 200 characters
 * @throws {AuthenticationError} If the user is not authenticated
 *
 * @example
 * const task = await createTask({ title: 'Buy groceries' });
 * console.log(task.id); // "task_abc123"
 */
export async function createTask(input: CreateTaskInput): Promise<Task> {
  // ...
}
```

### REST API 使用 OpenAPI / Swagger

```yaml
paths:
  /api/tasks:
    post:
      summary: Create a task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskInput'
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '422':
          description: Validation error
```

## README 结构

每个项目都应该有一个 README，至少涵盖：

```markdown
# Project Name

One-paragraph description of what this project does.

## Quick Start
1. Clone the repo
2. Install dependencies: `npm install`
3. Set up environment: `cp .env.example .env`
4. Run the dev server: `npm run dev`

## Commands
| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm test` | Run tests |
| `npm run build` | Production build |
| `npm run lint` | Run linter |

## Architecture
Brief overview of the project structure and key design decisions.
Link to ADRs for details.

## Contributing
How to contribute, coding standards, PR process.
```

## 变更日志维护

针对已发布的功能：

```markdown
# Changelog

## [1.2.0] - 2025-01-20
### Added
- Task sharing: users can share tasks with team members (#123)
- Email notifications for task assignments (#124)

### Fixed
- Duplicate tasks appearing when rapidly clicking create button (#125)

### Changed
- Task list now loads 50 items per page (was 20) for better UX (#126)
```

## 面向智能体的文档

针对 AI 智能体上下文的特别考量：

- **CLAUDE.md / rules 文件** —— 记录项目约定，让智能体遵守
- **规格文件** —— 保持规格更新，确保智能体构建正确的东西
- **ADR** —— 帮助智能体理解过往决策的 *原因*（避免重复决策）
- **行内坑点** —— 防止智能体掉入已知陷阱

## 常见的自我开脱

| 自我开脱 | 现实 |
|---|---|
| "代码本身就是文档" | 代码展示 *做了什么*，它无法展示 *为什么*、拒绝过哪些替代方案、受哪些约束影响。 |
| "等 API 稳定了再写文档" | 写文档的过程恰恰能让 API 更快稳定。文档就是设计的第一次检验。 |
| "没人看文档" | 智能体会看。未来的工程师会看。三个月后的你自己也会看。 |
| "ADR 是额外开销" | 一份 10 分钟的 ADR，能避免六个月后再为同一个决策争论两个小时。 |
| "注释会过时" | 解释 *为什么* 的注释是稳定的。解释 *做了什么* 的注释才会过时 —— 这正是只写前者的原因。 |

## 危险信号

- 架构决策没有书面记录其理由
- 公共 API 没有文档或类型说明
- README 没有说明如何运行项目
- 用注释掉的代码代替删除
- TODO 注释挂了好几周没处理
- 在有重要架构选型的项目里没有 ADR
- 文档只是复述代码，没有解释意图

## 验证

完成文档工作后：

- [ ] 所有重要架构决策都有对应的 ADR
- [ ] README 涵盖快速开始、命令列表和架构概览
- [ ] API 函数都有参数和返回类型文档
- [ ] 已知坑点在行内代码处有相应说明
- [ ] 没有残留注释掉的代码
- [ ] 规则文件（CLAUDE.md 等）保持最新且准确

## 局限性

- 仅当任务与上游来源及本地项目上下文明确匹配时，才使用本技能。
- 在应用变更前，验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要把示例当作环境特定测试、安全审查，或对破坏性 / 高成本操作的批准来使用。