# Neon Functions 上的服务器推送事件 (SSE)

SSE 是 WebSocket 的单向（服务器 → 客户端）流式对应方案：浏览器用 [`EventSource`](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 打开一个长生命周期 `GET` 请求，服务器沿其推送文本帧。在 Neon Functions 上**无需安装适配器或额外库**——与 [Hono WebSocket 辅助方法](hono-websockets.md) 不同，SSE 端点就是普通的 `fetch` 处理器，返回一个 body 为 `ReadableStream` 且 `Content-Type` 为 `text/event-stream` 的 `Response`。运行时只要字节持续流动就保持响应打开（15 分钟心跳，见 [超时](../SKILL.md#超时与运行时限制)）。

当你只需要服务器 → 客户端更新（实时计数器、通知、进度、token 流）时选择 SSE 而非 WebSocket——运行更简单（普通 HTTP，无需 `upgrade`），且 `EventSource` **自动重连**，无需编写客户端退避逻辑。

## 最小化 SSE 端点（无框架）

函数的默认导出是 `{ fetch }`；SSE 不需要更多。返回一个 `ReadableStream` 并向其中写入 `data:` 帧：

```typescript
// src/index.ts
const encoder = new TextEncoder();

export default {
  fetch(request: Request): Response {
    const url = new URL(request.url);
    if (url.pathname !== "/events") return new Response("ok");

    const stream = new ReadableStream<Uint8Array>({
      start(controller) {
        // SSE 帧格式为 `data: <payload>\n\n`。以 `:` 开头的行是
        // 注释——此处用作心跳以防流空闲。
        controller.enqueue(encoder.encode("data: hello\n\n"));
        const timer = setInterval(
          () => controller.enqueue(encoder.encode(": ping\n\n")),
          25_000,
        );
        // cancel() 在客户端断开时触发。
        return () => clearInterval(timer);
      },
    });

    return new Response(stream, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache, no-transform",
        Connection: "keep-alive",
      },
    });
  },
};
```

> 这里为简洁起见从 `start()` 返回了 `cancel()`；你也可以将其声明为流的底层源上的独立 `cancel()` 方法。无论哪种方式，都用它将客户端从广播集合中移除并清理定时器。

## 搭配 Hono

Hono 路由 HTTP 侧；SSE 响应是相同的 `ReadableStream`。返回原始 `Response` 保持对流完全控制（并避免流辅助方法中的并发写入边界情况）：

```typescript
// src/index.ts
import { Hono } from "hono";
import { cors } from "hono/cors";

const app = new Hono();
app.use("*", cors({ origin: process.env.WEB_ORIGIN ?? "*" })); // EventSource 从 SPA 跨域访问

app.get("/events", (c) => {
  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      controller.enqueue(new TextEncoder().encode("data: connected\n\n"));
      // ...将 `controller` 注册到广播集合中；见下方广播部分。
    },
  });
  return new Response(stream, {
    headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache, no-transform" },
  });
});

export default app;
```

## 推送到每个客户端（跨 isolate）

广播规则与 WebSocket 相同（[跨 isolate 广播](../SKILL.md#跨-isolate-广播-不要跳过本节)）：每个 isolate 维护**自己的**打开流集合，所以进程内广播只能到达该 isolate 上的客户端。维护一组 stream controller，用 Postgres `LISTEN`/`NOTIFY` 跨 isolate 广播。真实来源状态保存在 Postgres 中——模块状态不能幸免于驱逐。

```typescript
import { Pool, Client } from "pg";

const encoder = new TextEncoder();
const clients = new Set<ReadableStreamDefaultController<Uint8Array>>();
const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 5 });
const CHANNEL = "events";

// 每个 isolate 一条专用的直连连接来接收事件（LISTEN 需要真实
// 会话——使用 DATABASE_URL_UNPOOLED，不是连接池 URL）
const listener = new Client({ connectionString: process.env.DATABASE_URL_UNPOOLED });
listener.connect().then(() => listener.query(`LISTEN ${CHANNEL}`));
listener.on("notification", (msg) => {
  if (!msg.payload) return;
  const frame = encoder.encode(`data: ${msg.payload}\n\n`);
  for (const controller of clients) {
    try {
      controller.enqueue(frame); // enqueue 是同步的 — 无并发等待隐患
    } catch {
      clients.delete(controller); // controller 已关闭
    }
  }
});

// 在任何修改状态的地方，NOTIFY 以便每个 isolate 推送到自己的流。
function publish(payload: unknown) {
  return pool.query("SELECT pg_notify($1, $2)", [CHANNEL, JSON.stringify(payload)]);
}
```

在流的 `start`/`cancel` 中注册/注销每个连接到 `clients`，并添加模块作用域心跳（`setInterval`，每 ~25–30 秒）向每个 controller 排入 `: ping\n\n` 以使空闲流保持存活（见 [注意事项](#注意事项)）。

## 线路格式（纯文本）

每个事件以换行分隔字段，以空行结束：

```
data: a one-line payload\n\n
event: count\ndata: 42\n\n          # 命名事件 → addEventListener("count", …)
id: 7\ndata: resumable\n\n            # 设置 EventSource.lastEventId 用于恢复
: this is a comment / heartbeat\n\n   # 客户端忽略；保持流温热
retry: 5000\n\n                       # 告诉客户端重连前等待多久
```

发送不带 `event:` 字段的 `data:` 会投递默认 `message` 事件，客户端用 `EventSource.onmessage` 读取（无需 `addEventListener`）。

## 客户端

```typescript
const source = new EventSource(`${FUNCTION_URL}/events`); // 仅限 GET
source.onmessage = (e) => console.log("update", e.data);  // 默认 "message" 事件
source.onerror = () => {/* EventSource 自动重连；无需操作 */};
// source.close() 停止。
```

`EventSource` **按服务器的 `retry:` 间隔自动重连**，如果设置了 `id:` 则回放 `Last-Event-ID`——所以与 WebSocket 不同，你不需要写重连循环。它的限制：**仅支持 GET 且无法设置请求头**，所以认证方式与 [WebSocket](../SKILL.md#websocket-服务器) 相同——`?token=` 查询参数（流式传输前用 `jwtVerify` 验证）或 cookie。（如需 `Authorization` 请求头可使用现代 `eventsource` polyfill。）

## 注意事项

- **必须心跳否则会断。** 流只在有字节流动时保持打开——Neon 的窗口为 15 分钟（[超时](../SKILL.md#超时与运行时限制)），但中间代理通常严格得多（几十秒）。每 ~25–30 秒发出一个 `: ping\n\n` 注释以防流静默。
- **`no-transform`。** 设置 `Cache-Control: no-cache, no-transform` 以防代理缓冲或改写流。
- **Enqueue 是同步的。** `controller.enqueue()` 不返回 promise，所以从 `LISTEN` 处理器广播不会在写入中途交叉 await——用 `try/catch` 包裹并丢弃已关闭的 controller。
- **CORS。** SPA 跨域访问函数，所以设置 `Access-Control-Allow-Origin`。`EventSource` 默认不发送凭据，所以 `*` 对公开流没有问题。
- **仅单向。** SSE 是服务器 → 客户端。客户端 → 服务器由浏览器发起普通 `fetch`/`POST` 请求（通常到同一函数）；只有需要双向低延迟帧时才选择 [WebSocket](../SKILL.md#websocket-服务器)。

综合起来——一个 Hono `fetch` SSE 端点、`LISTEN`/`NOTIFY` 广播、心跳、Postgres 中持久化的计数器，以及消费它的纯客户端 TanStack Router SPA——这些组合成单函数上的完整实时后端。
