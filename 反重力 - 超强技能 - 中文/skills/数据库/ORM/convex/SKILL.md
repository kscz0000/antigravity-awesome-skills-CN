---
name: convex
description: "Convex 响应式后端专家：模式设计、TypeScript 函数、实时订阅、认证、文件存储、定时任务和部署。"
risk: safe
source: "https://docs.convex.dev"
date_added: "2026-02-27"
---

# Convex

你是 Convex 专家——这是一个开源的响应式后端平台，查询即 TypeScript 代码。你对模式设计、函数编写（查询、变更、动作）、实时数据订阅、认证、文件存储、定时任务和部署工作流有深入的了解，涵盖 React、Next.js、Angular、Vue、Svelte、React Native 和服务端环境。

## 何时使用

- 使用 Convex 作为后端构建新项目时使用
- 将 Convex 添加到现有的 React、Next.js、Angular、Vue、Svelte 或 React Native 应用时使用
- 为 Convex 文档-关系数据库设计模式时使用
- 编写或调试 Convex 函数（查询、变更、动作）时使用
- 实现实时/响应式数据模式时使用
- 使用 Convex Auth 或第三方提供商（Clerk、Auth0 等）设置认证时使用
- 使用 Convex 文件存储、定时函数或 Cron 任务时使用
- 部署或管理 Convex 项目时使用

## 核心概念

Convex 是一个**文档-关系型**数据库，搭配完全托管的后端。核心差异化特性：

- **默认响应式**：查询自动重新运行，并在底层数据变更时向所有连接的客户端推送更新
- **TypeScript 优先**：所有后端逻辑——查询、变更、动作、模式——均使用 TypeScript 编写
- **ACID 事务**：可串行化隔离，配合乐观并发控制
- **无需管理基础设施**：无服务器，自动扩展，零配置
- **端到端类型安全**：类型从模式 → 后端函数 → 客户端钩子贯穿流动

### 函数类型

| 类型             | 用途       | 可读数据库     | 可写数据库        | 可调用外部 API     | 缓存/响应式     |
| :--------------- | :--------- | :------------- | :---------------- | :----------------- | :-------------- |
| **Query**        | 读取数据   | ✅             | ❌                | ❌                 | ✅              |
| **Mutation**     | 写入数据   | ✅             | ✅                | ❌                 | ❌              |
| **Action**       | 副作用     | 通过 `runQuery` | 通过 `runMutation` | ✅                 | ❌              |
| **HTTP Action**  | Webhook/自定义端点 | 通过 `runQuery` | 通过 `runMutation` | ✅                 | ❌              |

## 项目设置

### 新项目（Next.js）

```bash
npx create-next-app@latest my-app
cd my-app && npm install convex
npx convex dev
```

### 添加到现有项目

```bash
npm install convex
npx convex dev
```

`npx convex dev` 命令会：

1. 提示你登录（GitHub）
2. 创建项目和部署
3. 生成 `convex/` 文件夹用于后端函数
4. 实时同步函数到你的开发部署
5. 创建 `.env.local`，包含 `CONVEX_DEPLOYMENT` 和 `NEXT_PUBLIC_CONVEX_URL`

### 文件夹结构

```
my-app/
├── convex/
│   ├── _generated/        ← 自动生成（请勿编辑）
│   │   ├── api.d.ts
│   │   ├── dataModel.d.ts
│   │   └── server.d.ts
│   ├── schema.ts          ← 数据库模式定义
│   ├── tasks.ts           ← 查询/变更函数
│   └── http.ts            ← HTTP 动作（可选）
├── .env.local             ← CONVEX_DEPLOYMENT, NEXT_PUBLIC_CONVEX_URL
└── convex.json            ← 项目配置（可选）
```

## 模式设计

在 `convex/schema.ts` 中使用验证器库定义模式：

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarUrl: v.optional(v.string()),
    tokenIdentifier: v.string(),
  })
    .index("by_token", ["tokenIdentifier"])
    .index("by_email", ["email"]),

  messages: defineTable({
    authorId: v.id("users"),
    channelId: v.id("channels"),
    body: v.string(),
    attachmentId: v.optional(v.id("_storage")),
  })
    .index("by_channel", ["channelId"])
    .searchIndex("search_body", { searchField: "body" }),

  channels: defineTable({
    name: v.string(),
    description: v.optional(v.string()),
    isPrivate: v.boolean(),
  }),
});
```

### 验证器类型

| 验证器                            | TypeScript 类型       | 说明                                           |
| :-------------------------------- | :-------------------- | :--------------------------------------------- |
| `v.string()`                      | `string`              |                                                |
| `v.number()`                      | `number`              | IEEE 754 浮点数                                |
| `v.bigint()`                      | `bigint`              |                                                |
| `v.boolean()`                     | `boolean`             |                                                |
| `v.null()`                        | `null`                |                                                |
| `v.id("tableName")`               | `Id<"tableName">`     | 文档引用                                       |
| `v.array(v.string())`             | `string[]`            |                                                |
| `v.object({...})`                 | `{...}`               | 嵌套对象                                       |
| `v.optional(v.string())`          | `string \| undefined` |                                                |
| `v.union(v.string(), v.number())` | `string \| number`    |                                                |
| `v.literal("active")`             | `"active"`            | 字面量类型                                     |
| `v.bytes()`                       | `ArrayBuffer`         | 二进制数据                                     |
| `v.float64()`                     | `number`              | 显式 64 位浮点数（用于向量索引）               |
| `v.any()`                         | `any`                 | 逃生舱口                                       |

### 索引

```typescript
// 单字段索引
defineTable({ email: v.string() }).index("by_email", ["email"]);

// 复合索引（顺序对范围查询很重要）
defineTable({
  orgId: v.string(),
  createdAt: v.number(),
}).index("by_org_and_date", ["orgId", "createdAt"]);

// 全文搜索索引
defineTable({ body: v.string(), channelId: v.id("channels") }).searchIndex(
  "search_body",
  {
    searchField: "body",
    filterFields: ["channelId"],
  },
);

// 向量搜索索引（用于 AI/嵌入）
defineTable({ embedding: v.array(v.float64()), text: v.string() }).vectorIndex(
  "by_embedding",
  {
    vectorField: "embedding",
    dimensions: 1536,
  },
);
```

## 编写函数

### 查询（读取数据）

查询是响应式的——当数据变更时，客户端自动获取更新。

````typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

// 简单查询 — 列出所有任务
export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

// 带参数和过滤的查询
export const getByChannel = query({
  args: { channelId: v.id("channels") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .order("desc")
      .take(50);
  },
});

// 带认证检查的查询
export const getMyProfile = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return null;

    return await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier),
      )
      .unique();
  },
});

### 分页查询

对列表或无限滚动 UI 使用基于游标的分页。

```typescript
import { query } from "./_generated/server";
import { paginationOptsValidator } from "convex/server";

export const listPaginated = query({
  args: {
    paginationOpts: paginationOptsValidator
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

### 变更（写入数据）

变更以 ACID 事务运行，具有可串行化隔离。

```typescript
import { mutation } from "./_generated/server";
import { v } from "convex/values";

// 插入文档
export const create = mutation({
  args: { text: v.string(), isCompleted: v.boolean() },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      text: args.text,
      isCompleted: args.isCompleted,
    });
    return taskId;
  },
});

// 更新文档
export const update = mutation({
  args: { id: v.id("tasks"), isCompleted: v.boolean() },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, { isCompleted: args.isCompleted });
  },
});

// 删除文档
export const remove = mutation({
  args: { id: v.id("tasks") },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.id);
  },
});

// 多文档事务（自动原子性）
export const transferCredits = mutation({
  args: {
    fromUserId: v.id("users"),
    toUserId: v.id("users"),
    amount: v.number(),
  },
  handler: async (ctx, args) => {
    const fromUser = await ctx.db.get(args.fromUserId);
    const toUser = await ctx.db.get(args.toUserId);
    if (!fromUser || !toUser) throw new Error("用户未找到");
    if (fromUser.credits < args.amount) throw new Error("积分不足");

    await ctx.db.patch(args.fromUserId, {
      credits: fromUser.credits - args.amount,
    });
    await ctx.db.patch(args.toUserId, {
      credits: toUser.credits + args.amount,
    });
  },
});
````

### 动作（外部 API 和副作用）

动作可以调用第三方服务，但不能直接访问数据库——必须使用 `ctx.runQuery` 和 `ctx.runMutation`。

```typescript
import { action } from "./_generated/server";
import { v } from "convex/values";
import { api } from "./_generated/api";

export const sendEmail = action({
  args: { to: v.string(), subject: v.string(), body: v.string() },
  handler: async (ctx, args) => {
    // 调用外部 API
    const response = await fetch("https://api.sendgrid.com/v3/mail/send", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.SENDGRID_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: args.to }] }],
        from: { email: "noreply@example.com" },
        subject: args.subject,
        content: [{ type: "text/plain", value: args.body }],
      }),
    });

    if (!response.ok) throw new Error("邮件发送失败");

    // 通过变更将结果写回数据库
    await ctx.runMutation(api.emails.recordSent, {
      to: args.to,
      subject: args.subject,
      sentAt: Date.now(),
    });
  },
});

// 生成 AI 嵌入
export const generateEmbedding = action({
  args: { text: v.string(), documentId: v.id("documents") },
  handler: async (ctx, args) => {
    const response = await fetch("https://api.openai.com/v1/embeddings", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "text-embedding-3-small",
        input: args.text,
      }),
    });

    const { data } = await response.json();
    await ctx.runMutation(api.documents.saveEmbedding, {
      documentId: args.documentId,
      embedding: data[0].embedding,
    });
  },
});
```

### HTTP 动作（Webhook）

```typescript
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/webhooks/stripe",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.text();
    const signature = request.headers.get("stripe-signature");

    // 在此验证 webhook 签名...

    const event = JSON.parse(body);
    await ctx.runMutation(api.payments.handleWebhook, { event });

    return new Response("OK", { status: 200 });
  }),
});

export default http;
```

## 客户端集成

### React / Next.js

```typescript
// app/ConvexClientProvider.tsx
"use client";
import { ConvexProvider, ConvexReactClient } from "convex/react";
import { ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

```typescript
// app/layout.tsx — 包裹子组件
import { ConvexClientProvider } from "./ConvexClientProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ConvexClientProvider>{children}</ConvexClientProvider>
      </body>
    </html>
  );
}
```

```typescript
// 使用 Convex 钩子的组件
"use client";
import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";

export function TaskList() {
  // 响应式查询 — 数据变更时自动更新
  const tasks = useQuery(api.tasks.list);
  const addTask = useMutation(api.tasks.create);
  const toggleTask = useMutation(api.tasks.update);

  if (tasks === undefined) return <p>加载中...</p>;

  return (
    <div>
      {tasks.map((task) => (
        <div key={task._id}>
          <input
            type="checkbox"
            checked={task.isCompleted}
            onChange={() =>
              toggleTask({ id: task._id, isCompleted: !task.isCompleted })
            }
          />
          {task.text}
        </div>
      ))}
      <button onClick={() => addTask({ text: "新任务", isCompleted: false })}>
        添加任务
      </button>
    </div>
  );
}
```

```typescript
// 使用分页查询的组件
"use client";
import { usePaginatedQuery } from "convex/react";
import { api } from "@/convex/_generated/api";

export function MessageLog() {
  const { results, status, loadMore } = usePaginatedQuery(
    api.messages.listPaginated,
    {}, // 参数
    { initialNumItems: 20 }
  );

  return (
    <div>
      {results.map((msg) => (
        <div key={msg._id}>{msg.body}</div>
      ))}

      {status === "LoadingFirstPage" && <p>加载中...</p>}

      {status === "CanLoadMore" && (
        <button onClick={() => loadMore(20)}>加载更多</button>
      )}
    </div>
  );
}
```

### 认证（第一方 Convex Auth）

Convex 提供了一个健壮的原生认证库（`@convex-dev/auth`），支持 Magic Links、密码和 80+ OAuth 提供商，无需第三方服务。

```typescript
// app/ConvexClientProvider.tsx
"use client";
import { ConvexAuthProvider } from "@convex-dev/auth/react";
import { ConvexReactClient } from "convex/react";
import { ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return (
    <ConvexAuthProvider client={convex}>
      {children}
    </ConvexAuthProvider>
  );
}
```

```typescript
// 客户端登录
import { useAuthActions } from "@convex-dev/auth/react";

export function Login() {
  const { signIn } = useAuthActions();
  return <button onClick={() => signIn("github")}>使用 GitHub 登录</button>;
}
```

### 认证（第三方 Clerk 示例）

如果你更偏好托管的第三方方案如 Clerk：

```typescript
// app/ConvexClientProvider.tsx
"use client";
import { ConvexProviderWithClerk } from "convex/react-clerk";
import { ClerkProvider, useAuth } from "@clerk/nextjs";
import { ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return (
    <ClerkProvider publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!}>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        {children}
      </ConvexProviderWithClerk>
    </ClerkProvider>
  );
}
```

### 认证（Better Auth 组件）

Convex 还有一个社区组件（`@convex-dev/better-auth`），将 Better Auth 库直接集成到 Convex 后端。目前处于**早期 alpha** 阶段。

```bash
npm install better-auth @convex-dev/better-auth
npx convex env set BETTER_AUTH_SECRET your-secret-here
npx convex env set SITE_URL http://localhost:3000
```

Better Auth 提供邮箱/密码、社交登录、双因素认证和会话管理——全部在 Convex 函数内运行，而非外部认证服务器。

### Angular 集成

Convex 没有官方的 Angular 客户端库，但 Angular 应用可以直接使用核心 `convex` 包，配合 Angular 的依赖注入和 Signals。

```typescript
// services/convex.service.ts
import { Injectable, signal, effect, OnDestroy } from "@angular/core";
import { ConvexClient } from "convex/browser";
import { api } from "../../convex/_generated/api";
import { FunctionReturnType } from "convex/server";

@Injectable({ providedIn: "root" })
export class ConvexService implements OnDestroy {
  private client = new ConvexClient(environment.convexUrl);

  // 响应式信号 — 数据变更时自动更新
  tasks = signal<FunctionReturnType<typeof api.tasks.list> | undefined>(
    undefined,
  );

  constructor() {
    // 订阅响应式查询
    this.client.onUpdate(api.tasks.list, {}, (result) => {
      this.tasks.set(result);
    });
  }

  async addTask(text: string) {
    await this.client.mutation(api.tasks.create, {
      text,
      isCompleted: false,
    });
  }

  ngOnDestroy() {
    this.client.close();
  }
}
```

```typescript
// 组件使用
import { Component, inject } from "@angular/core";
import { ConvexService } from "./services/convex.service";

@Component({
  selector: "app-task-list",
  template: `
    @if (convex.tasks(); as tasks) {
      @for (task of tasks; track task._id) {
        <div>{{ task.text }}</div>
      }
    } @else {
      <p>加载中...</p>
    }
    <button (click)="convex.addTask('新任务')">添加任务</button>
  `,
})
export class TaskListComponent {
  convex = inject(ConvexService);
}
```

> **注意：** 社区库 `@robmanganelly/ngx-convex` 提供了更原生的 Angular 体验，将类似 React 的钩子适配为 Angular DI 和 Signals。

## 定时任务与 Cron

### 一次性定时函数

```typescript
import { mutation } from "./_generated/server";
import { api } from "./_generated/api";

export const sendReminder = mutation({
  args: { userId: v.id("users"), message: v.string(), delayMs: v.number() },
  handler: async (ctx, args) => {
    await ctx.scheduler.runAfter(args.delayMs, api.notifications.send, {
      userId: args.userId,
      message: args.message,
    });
  },
});
```

### Cron 任务

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { api } from "./_generated/api";

const crons = cronJobs();

crons.interval("清理旧日志", { hours: 24 }, api.logs.clearOld);

crons.cron(
  "每周摘要",
  "0 9 * * 1", // 每周一上午 9 点
  api.emails.sendWeeklyDigest,
);

export default crons;
```

## 文件存储

```typescript
// 生成上传 URL（变更）
export const generateUploadUrl = mutation({
  args: {},
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});

// 上传后保存文件引用（变更）
export const saveFile = mutation({
  args: { storageId: v.id("_storage"), name: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("files", {
      storageId: args.storageId,
      name: args.name,
    });
  },
});

// 获取文件服务 URL（查询）
export const getFileUrl = query({
  args: { storageId: v.id("_storage") },
  handler: async (ctx, args) => {
    return await ctx.storage.getUrl(args.storageId);
  },
});
```

## 环境变量

```bash
# 为你的部署设置环境变量
npx convex env set OPENAI_API_KEY sk-...
npx convex env set SENDGRID_API_KEY SG...

# 列出当前环境变量
npx convex env list

# 移除环境变量
npx convex env unset OPENAI_API_KEY
```

在动作中访问（不能在查询或变更中访问）：

```typescript
// 仅在动作中可用
const apiKey = process.env.OPENAI_API_KEY;
```

## 部署与 CLI

```bash
# 开发（监听变更，同步到开发部署）
npx convex dev

# 部署到生产环境
npx convex deploy

# 导入数据
npx convex import --table tasks data.jsonl

# 导出数据
npx convex export --path ./backup

# 打开 Convex 控制面板
npx convex dashboard

# 从 CLI 运行函数
npx convex run tasks:list

# 查看日志
npx convex logs
```

## 最佳实践

- ✅ 定义模式——为整个技术栈增加类型安全
- ✅ 为查询使用索引——避免全表扫描
- ✅ 复合索引中等值过滤在前，范围过滤在后
- ✅ 依赖原生确定性——`Date.now()` 和 `Math.random()` 在查询和变更中完全安全，因为 Convex 在每次函数执行开始时冻结时间！
- ✅ 使用 `v.id("tableName")` 作为文档引用，而非普通字符串
- ✅ 使用动作调用外部 API（永远不要从查询或变更中调用外部 API）
- ✅ 从动作中使用 `ctx.runQuery` / `ctx.runMutation`——永远不要在动作中直接访问 `ctx.db`
- ✅ 为所有函数添加参数验证器——它们强制运行时类型安全
- ✅ 文档未找到时返回 `null`，而非抛出错误，除非缺失属于异常情况
- ✅ 优先使用 `withIndex` 而非 `.filter()` 以提升查询性能

## 需要避免的反模式

1. **❌ 在查询/变更中调用外部 API**：只有动作可以调用外部服务。查询和变更运行在 Convex 事务引擎中。
2. **❌ 在变更中做耗时的 CPU 密集型工作**：变更会阻塞数据库提交；将繁重处理卸载到动作中。
3. **❌ 在大表上使用 `.collect()` 而不加限制**：会将所有文档加载到内存。使用 `.take(N)` 或 `.paginate()`。
4. **❌ 跳过模式定义**：没有模式你会失去端到端类型安全，这是 Convex 的主要优势。
5. **❌ 使用 `.filter()` 而非索引**：`.filter()` 执行全表扫描。定义索引并使用 `.withIndex()`。
6. **❌ 在文档中存储大型二进制数据**：使用 Convex 文件存储（`_storage`）存储文件；保持文档精简。
7. **❌ 循环的 `runQuery`/`runMutation` 链**：动作调用变更再调度动作可能造成无限循环。

## 常见陷阱

- **问题：**"查询在首次渲染时返回 `undefined`"
  **解决方案：**这是预期行为——Convex 查询是异步的。渲染前检查 `undefined`（这表示加载中，而非空）。

- **问题：**"变更抛出 `Document not found`"
  **解决方案：**由于乐观并发，文档可能在你的读写之间被删除。在变更内部重新读取。

- **问题：**"`process.env` 在查询/变更中为 undefined"
  **解决方案：**环境变量仅在**动作**中可访问（查询和变更中不可），因为查询/变更运行在确定性事务引擎中。

- **问题：**"函数处理器太慢"
  **解决方案：**为查询模式添加索引。使用 `withIndex()` 替代 `.filter()`。对于复杂操作，拆分为更小的变更。

- **问题：**"模式推送因现有数据而失败"
  **解决方案：**Convex 会根据新模式验证现有数据。要么先迁移现有文档，要么对新字段使用 `v.optional()`。

## 限制

- 查询和变更不能调用外部 HTTP API（使用动作代替）
- 没有原生 SQL——你使用 Convex 查询构建器 API
- 环境变量仅在动作中可用，查询和变更中不可用
- 文档大小限制为 1MB
- 函数执行时间有上限
- 没有 Convex 数据的服务端渲染需要特定的 SSR 模式（使用预加载）
- 模式在写入时强制执行；更改模式需要对现有文档进行数据迁移

## 相关技能

- `@firebase` — 替代 BaaS 方案，使用 Firestore（对比：Convex 是 TypeScript 优先且支持 ACID 事务）
- `@supabase-automation` — 替代方案，使用 PostgreSQL 后端（对比：Convex 是文档-关系型且内置响应式）
- `@prisma-expert` — 传统数据库的 ORM（Convex 同时替代了 ORM 和数据库）
- `@react-patterns` — 与 Convex React 钩子搭配良好的前端模式
- `@nextjs-app-router` — Next.js App Router 集成模式
- `@authentication-oauth` — 认证模式（Convex 支持 Clerk、Auth0、Convex Auth）
- `@stripe` — 通过 Convex 动作和 HTTP webhook 的支付集成

## 资源

- [官方文档](https://docs.convex.dev)
- [Convex Stack（博客）](https://stack.convex.dev)
- [GitHub](https://github.com/get-convex/convex-backend)
- [Discord 社区](https://convex.dev/community)
- [Convex Chef（AI 启动器）](https://chef.convex.dev)
