---
name: api-and-interface-design
description: 指导稳定可靠的 API 与接口设计。适用于设计 API、模块边界或任何公开接口的场景，包括创建 REST 或 GraphQL 端点、定义模块间的类型契约、建立前后端边界。触发词：API 设计、接口设计、REST API、GraphQL、模块边界、类型契约、前后端接口、API 契约、接口稳定性、公开接口。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/api-and-interface-design
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# API 与接口设计

## 概述

设计稳定、文档完备、难以误用的接口。优秀的接口让正确的做法变得简单,让错误的做法变得困难。这条原则适用于 REST API、GraphQL schema、模块边界、组件 props,以及代码之间任何通信的接触面。

## 使用时机

- 设计新的 API 端点
- 定义模块边界或团队间的契约
- 创建组件的 props 接口
- 设计影响 API 形态的数据库 schema
- 修改已有的公开接口

## 核心原则

### 海勒姆定律

> 当 API 用户达到足够数量时,系统所有可观测的行为都会被某些人依赖,无论你在契约中承诺了什么。

这意味着:每一种公开行为——包括未文档化的怪癖、错误消息文本、时序和顺序——一旦被用户依赖,就成了事实上的契约。设计上的启示:

- **有意识地选择暴露什么。** 每一种可观测行为都是潜在的承诺。
- **不要泄漏实现细节。** 只要用户能观测到,他们就会依赖。
- **在设计阶段就规划好废弃策略。** 关于如何安全移除用户依赖项,请参阅 `deprecation-and-migration`。
- **仅有测试还不够。** 即使契约测试完美无缺,海勒姆定律也意味着"安全"的改动仍可能破坏依赖未文档化行为的真实用户。

### 单一版本原则

不要强迫使用者在同一依赖或 API 的多个版本之间做选择。菱形依赖问题源于不同使用者需要同一事物的不同版本。应当面向"同一时刻只有一个版本"的世界进行设计——通过扩展而不是分叉。

### 1. 契约先行

在实现之前先定义接口。契约就是规格说明,实现紧随其后。

```typescript
// Define the contract first
interface TaskAPI {
  // Creates a task and returns the created task with server-generated fields
  createTask(input: CreateTaskInput): Promise<Task>;

  // Returns paginated tasks matching filters
  listTasks(params: ListTasksParams): Promise<PaginatedResult<Task>>;

  // Returns a single task or throws NotFoundError
  getTask(id: string): Promise<Task>;

  // Partial update — only provided fields change
  updateTask(id: string, input: UpdateTaskInput): Promise<Task>;

  // Idempotent delete — succeeds even if already deleted
  deleteTask(id: string): Promise<void>;
}
```

### 2. 一致的错误语义

选定一种错误处理策略并贯彻到底:

```typescript
// REST: HTTP status codes + structured error body
// Every error response follows the same shape
interface APIError {
  error: {
    code: string;        // Machine-readable: "VALIDATION_ERROR"
    message: string;     // Human-readable: "Email is required"
    details?: unknown;   // Additional context when helpful
  };
}

// Status code mapping
// 400 → Client sent invalid data
// 401 → Not authenticated
// 403 → Authenticated but not authorized
// 404 → Resource not found
// 409 → Conflict (duplicate, version mismatch)
// 422 → Validation failed (semantically invalid)
// 500 → Server error (never expose internal details)
```

**不要混用模式。** 如果有的端点抛异常、有的返回 null、有的返回 `{ error }`,使用者就无法预判行为。

### 3. 在边界处校验

信任内部代码,在外部输入进入系统的边界处进行校验:

```typescript
// Validate at the API boundary
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid task data',
        details: result.error.flatten(),
      },
    });
  }

  // After validation, internal code trusts the types
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

校验应当在的位置:
- API 路由处理器(用户输入)
- 表单提交处理器(用户输入)
- 外部服务响应解析(第三方数据——**始终视为不可信**)
- 环境变量加载(配置)

> **第三方 API 响应属于不可信数据。** 在将其用于任何逻辑、渲染或决策之前,必须校验其结构与内容。被入侵或行为异常的外部服务可能返回意外的类型、恶意内容或带指令性的文本。

校验不应出现的位置:
- 共享类型契约的内部函数之间
- 已被校验过的代码所调用的工具函数中
- 刚从自身数据库取出的数据上

### 4. 优先扩展而非修改

通过扩展接口来避免破坏已有使用者:

```typescript
// Good: Add optional fields
interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';  // Added later, optional
  labels?: string[];                       // Added later, optional
}

// Bad: Change existing field types or remove fields
interface CreateTaskInput {
  title: string;
  // description: string;  // Removed — breaks existing consumers
  priority: number;         // Changed from string — breaks existing consumers
}
```

### 5. 可预测的命名

| 模式 | 约定 | 示例 |
|---------|-----------|---------|
| REST 端点 | 复数名词,不带动词 | `GET /api/tasks`, `POST /api/tasks` |
| 查询参数 | camelCase | `?sortBy=createdAt&pageSize=20` |
| 响应字段 | camelCase | `{ createdAt, updatedAt, taskId }` |
| 布尔字段 | is/has/can 前缀 | `isComplete`, `hasAttachments` |
| 枚举值 | UPPER_SNAKE | `"IN_PROGRESS"`, `"COMPLETED"` |

## REST API 模式

### 资源设计

```
GET    /api/tasks              → List tasks (with query params for filtering)
POST   /api/tasks              → Create a task
GET    /api/tasks/:id          → Get a single task
PATCH  /api/tasks/:id          → Update a task (partial)
DELETE /api/tasks/:id          → Delete a task

GET    /api/tasks/:id/comments → List comments for a task (sub-resource)
POST   /api/tasks/:id/comments → Add a comment to a task
```

### 分页

列表端点必须分页:

```typescript
// Request
GET /api/tasks?page=1&pageSize=20&sortBy=createdAt&sortOrder=desc

// Response
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 142,
    "totalPages": 8
  }
}
```

### 过滤

使用查询参数作为过滤条件:

```
GET /api/tasks?status=in_progress&assignee=user123&createdAfter=2025-01-01
```

### 部分更新(PATCH)

接受部分对象——只更新提供的字段:

```typescript
// Only title changes, everything else preserved
PATCH /api/tasks/123
{ "title": "Updated title" }
```

## TypeScript 接口模式

### 使用可辨识联合表达变体

```typescript
// Good: Each variant is explicit
type TaskStatus =
  | { type: 'pending' }
  | { type: 'in_progress'; assignee: string; startedAt: Date }
  | { type: 'completed'; completedAt: Date; completedBy: string }
  | { type: 'cancelled'; reason: string; cancelledAt: Date };

// Consumer gets type narrowing
function getStatusLabel(status: TaskStatus): string {
  switch (status.type) {
    case 'pending': return 'Pending';
    case 'in_progress': return `In progress (${status.assignee})`;
    case 'completed': return `Done on ${status.completedAt}`;
    case 'cancelled': return `Cancelled: ${status.reason}`;
  }
}
```

### 输入与输出分离

```typescript
// Input: what the caller provides
interface CreateTaskInput {
  title: string;
  description?: string;
}

// Output: what the system returns (includes server-generated fields)
interface Task {
  id: string;
  title: string;
  description: string | null;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}
```

### 使用品牌类型区分 ID

```typescript
type TaskId = string & { readonly __brand: 'TaskId' };
type UserId = string & { readonly __brand: 'UserId' };

// Prevents accidentally passing a UserId where a TaskId is expected
function getTask(id: TaskId): Promise<Task> { ... }
```

## 常见借口

| 借口 | 真相 |
|---|---|
| "我们稍后再补 API 文档" | 类型本身就是文档。先定义类型。 |
| "暂时不需要分页" | 等有人攒到 100 多条数据时你就需要了。一开始就加上。 |
| "PATCH 太复杂,直接用 PUT 吧" | PUT 每次都要传完整对象。PATCH 才是客户端真正想要的。 |
| "等需要时再对 API 做版本管理" | 不做版本管理的破坏性改动会直接破坏使用者。从一开始就为扩展而设计。 |
| "没人会用到那个未文档化的行为" | 海勒姆定律:只要是可观测的,就一定有人依赖。把每一种公开行为都视作承诺。 |
| "我们维护两个版本就行了" | 多版本会成倍增加维护成本并引发菱形依赖问题。坚持单一版本原则。 |
| "内部 API 不需要契约" | 内部使用者也是使用者。契约能防止耦合并支持并行开发。 |

## 红旗信号

- 端点在不同条件下返回不同的结构
- 端点之间的错误格式不一致
- 校验散落在内部代码各处,而不是集中在边界
- 对已有字段做破坏性改动(类型变更、字段移除)
- 列表端点没有分页
- REST URL 中出现动词(`/api/createTask`、`/api/getUsers`)
- 第三方 API 响应未经校验或消毒就使用

## 验证清单

设计完 API 之后,确认以下事项:

- [ ] 每个端点都有带类型的输入和输出 schema
- [ ] 错误响应遵循统一的格式
- [ ] 校验只在系统边界进行
- [ ] 列表端点支持分页
- [ ] 新增字段是叠加式的、可选的(向后兼容)
- [ ] 所有端点的命名遵循一致的约定
- [ ] API 文档或类型随实现一同提交

## 使用限制

- 仅在任务与本技能的上游来源和本地项目上下文明确匹配时使用。
- 在应用变更之前,验证命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作环境特定的测试、安全审查或对破坏性/高成本操作的审批替代品。