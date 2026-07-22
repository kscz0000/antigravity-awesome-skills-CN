# 集成与可观测性

Neon Function 是一个**长驻 Node.js 24 进程，运行 Web 标准请求/响应处理器**——不是边缘 Worker 或短命 Lambda。这意味着任何在普通 Node 进程中可用的集成 SDK 在这里也可以直接使用：你在模块加载时、处理器开始服务请求之前初始化一次，然后它就在 isolate 的整个生命周期内保持生效。

本参考文档以接入 Sentry 进行错误和性能监控为例；相同的模式（首先导入初始化模块、用环境变量门控、部署时传入密钥）也适用于其他 Node SDK（OpenTelemetry、日志、分析）。

## Sentry（错误与性能监控）

因为运行时是普通 Node 进程，使用 Node SDK `@sentry/node`——不是边缘/无服务器封装。它通过 `neon deploy` 的 esbuild 干净打包，无需额外构建配置。

有三个层值得监控，来自所有层的错误汇入同一个 Sentry 项目：

1. HTTP 框架（未处理的路由错误）。
2. Node 函数运行时（未捕获异常 / 未处理拒绝，由 SDK 捕获）。
3. 应用自身的已捕获失败——例如 Agent 重试并回退而非抛出异常。

### 1. 在其他一切之前初始化

将 `Sentry.init` 放在独立模块中，作为入口文件的第一个导入，确保进程在任何其他代码（你的处理器、数据库连接池、Agent）加载之前就被监控。

```typescript
// src/instrument.ts
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  enabled: Boolean(process.env.SENTRY_DSN),
  tracesSampleRate: 1.0,
  // NEON_BRANCH（分支名称）在每个分支上注入，包括默认分支——所以
  // 不能用作"这是否是一个分支"的真值标志。将项目的默认分支视为
  // "production"（通过 neon.ts env 传入其名称），其他分支按名称标记。
  environment:
    process.env.NEON_BRANCH && process.env.NEON_BRANCH !== process.env.PRODUCTION_BRANCH
      ? process.env.NEON_BRANCH
      : "production",
});

export { Sentry };
```

```typescript
// src/index.ts
import "./instrument"; // 必须是第一个导入，在框架/Agent 之前
import { Sentry } from "./instrument";
import { Hono } from "hono";
// ... 函数的其余部分
```

- **用 DSN 门控 `enabled`。** 本地开发（`neon dev`）和未配置密钥的分支因此成为空操作——无初始化、无噪音——无需改动代码。
- **基于注入的分支名称标记环境。** 每个 Neon 分支运行自己的一份函数，运行时在每个分支中注入 `NEON_BRANCH`（分支**名称**，如 `main` 或 `preview/add-auth`）——包括默认分支。同样的值也由 `neon env pull` / `neon-env run` / `neon dev` 写入本地开发环境，所以本地和部署的运行结果一致。因为它始终存在，不要将其用作布尔标志（那样会把每个分支标记成一样的）。而是将它与你的默认分支名称比较（通过 `neon.ts` `env` 传入，如 `PRODUCTION_BRANCH`），这样默认分支显示为 `production`，功能/预览分支按名称标记——在 Sentry 仪表板中保持可分离。

### 2. 将 DSN 作为部署时密钥提供

DSN 是你自己的密钥，所以按部署设置（参见 SKILL.md 中的"环境变量"）。部署时传入：

```bash
neon functions deploy <slug> --src src/index.ts \
  --env "SENTRY_DSN=https://…@…ingest.us.sentry.io/…"
```

或在 `neon.ts` 函数的 `env` 下声明（从 `process.env` 读取以避免硬编码）：

```typescript
functions: {
  <slug>: {
    name: "…",
    source: "src/index.ts",
    env: { SENTRY_DSN: process.env.SENTRY_DSN! },
  },
}
```

### 3. 捕获未处理的路由错误

在 HTTP 框架中接入顶层错误处理器，使路由中抛出的任何错误都被上报。使用 Hono 时 `onError` 覆盖了这一点。注意一个问题：如 `cors()` 的框架中间件通常**不会**装饰错误响应，所以在 500 响应上重新添加你需要的请求头。

```typescript
app.onError((err, c) => {
  Sentry.captureException(err);
  c.header("access-control-allow-origin", "*"); // cors() 不在错误响应上运行
  return c.json({ error: "internal_error" }, 500);
});
```

### 4. 显式上报 Agent（及其他被吞没的）失败

长运行 Agent 工作负载——Neon Functions 的目标场景——通常会**自行捕获错误并回退**（重试不同模型、返回降级结果）而非抛出。这些失败永远不会到达路由错误处理器，所以用同一个 `Sentry` 实例显式上报，并添加标签以便在仪表板中过滤和分组。

一个典型的跨多个模型解析页面的 Agent 上报三种情况：

```typescript
// 可恢复：一次模型尝试失败，Agent 将尝试下一个模型。
Sentry.captureException(err, {
  level: "warning",
  tags: { component: "agent", phase: "parse-attempt", model },
  extra: { url, source },
});

// 终端：所有模型都失败了。
Sentry.captureException(err, {
  level: "error",
  tags: { component: "agent", phase: "parse-all-failed" },
  extra: { url, source },
});

// 非异常失败：Agent 根本无法获取输入页面。
Sentry.captureMessage("agent could not fetch page", {
  level: "warning",
  tags: { component: "agent", phase: "fetch" },
  extra: { url, source },
});
```

- 用 `level` 区分可恢复（`warning`）和终端（`error`）失败。
- 用 `tags` 标注你想过滤/分组的维度——`component`、`phase`、`model`。
- 用 `extra` 添加每次事件的上下文——正在处理的 URL、内容来源。

### 验证接线

- 临时添加一个抛出异常的路由（`app.get("/debug-sentry", () => { throw new Error("sentry test"); })`），访问它，确认 500 出现在 Sentry 中，然后移除该路由。
- 触发一个真实的下游失败（如将 fetch 指向 `https://httpstat.us/500`）以确认显式的 Agent 级别捕获生效。

## 其他 Node 集成

相同模式推广到任何 Node 集成（OpenTelemetry、结构化日志、产品分析）：

1. 在专用初始化模块的模块作用域中初始化一次，在处理器之前导入。
2. 用环境变量门控以便本地开发和未配置分支为空操作。
3. 通过部署时的 `--env KEY=VALUE` 或 `neon.ts` 中函数的 `env` 传递密钥。

标准 Node SDK 通过 `neon deploy` 的 esbuild 打包无需修改。
