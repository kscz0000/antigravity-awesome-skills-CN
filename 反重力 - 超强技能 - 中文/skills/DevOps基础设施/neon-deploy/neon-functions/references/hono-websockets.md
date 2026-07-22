# Neon Functions 上的 Hono WebSocket 辅助方法

Neon Functions 通过 `{ fetch, upgrade }` 默认导出接受 WebSocket，其中 `upgrade(req, socket, head)` 是原生 Node 握手（见 [WebSocket 服务器](../SKILL.md#websocket-服务器) 章节）。这可以直接与 `ws` 库配合使用。如果你更倾向于在 Hono 应用**内部**声明 WebSocket 路由——`app.get("/ws", upgradeWebSocket(...))` 配合标准的 `onOpen`/`onMessage`/`onClose` 生命周期——你需要一个适配器。

## 为什么需要适配器（以及为什么不用 `@hono/node-ws`）

Hono 的 `upgradeWebSocket()` 在路由层是运行时无关的，但实际握手由各运行时的适配器完成（`hono/cloudflare-workers`、`hono/deno`、`hono/bun`、`@hono/node-server`）。**没有 Neon 的适配器。** Node 侧的 `@hono/node-ws` 已**废弃**，其替代品假定自己拥有 HTTP 服务器（`serve({ websocket })`）——而这正是 Neon 运行时所负责的。

因此引入下方的小型适配器。它仅依赖 `hono` 和 `ws`（无废弃包），改编自 `@hono/node-ws`（MIT 协议）。它不挂载到 `http.Server` 的 `'upgrade'` 事件，而是返回可直接导出的 `{ fetch, upgrade }` 处理器，匹配 Neon 的契约。

## 适配器

```typescript
// src/hono-ws.ts — 将 Hono 的 upgradeWebSocket() 桥接到 Neon 的 { fetch, upgrade }
import { STATUS_CODES, type IncomingMessage } from "node:http";
import type { Duplex } from "node:stream";
import type { Hono } from "hono";
import { WSContext, defineWebSocketHelper } from "hono/ws";
import { WebSocketServer, type WebSocket } from "ws";

type Wire = (ws: WebSocket) => void;

export function createNeonWebSocket(app: Hono, baseUrl = "http://localhost") {
  const wss = new WebSocketServer({ noServer: true });
  // 通过每次请求 env 对象的身份将握手关联到其路由处理器
  const pending = new Map<unknown, Wire>();

  const upgradeWebSocket = defineWebSocketHelper(async (c, events, options) => {
    if (c.req.header("upgrade")?.toLowerCase() !== "websocket") return;
    const url = c.req.url;
    pending.set(c.env, (ws) => {
      const onError = options?.onError ?? ((e: unknown) => console.error(e));
      const ctx = new WSContext<WebSocket>({
        send: (data, opts) => ws.send(data, { compress: opts?.compress }),
        close: (code, reason) => ws.close(code, reason),
        raw: ws,
        url,
        protocol: ws.protocol,
        get readyState() {
          return ws.readyState;
        },
      });
      try {
        events.onOpen?.(new Event("open"), ctx);
      } catch (e) {
        onError(e);
      }
      ws.on("message", (data, isBinary) => {
        for (const chunk of Array.isArray(data) ? data : [data]) {
          try {
            const payload = isBinary
              ? chunk instanceof ArrayBuffer
                ? chunk
                : chunk.buffer.slice(chunk.byteOffset, chunk.byteOffset + chunk.byteLength)
              : chunk.toString("utf-8");
            events.onMessage?.(new MessageEvent("message", { data: payload }), ctx);
          } catch (e) {
            onError(e);
          }
        }
      });
      ws.on("close", (code, reason) => {
        try {
          events.onClose?.(new CloseEvent("close", { code, reason: reason.toString() }), ctx);
        } catch (e) {
          onError(e);
        }
      });
      // Node 24 没有全局 ErrorEvent；浏览器的 ws.onerror 本身收到的是普通 Event
      ws.on("error", (error) => {
        onError(error);
        try {
          events.onError?.(new Event("error"), ctx);
        } catch (e) {
          onError(e);
        }
      });
    });
    return new Response();
  });

  const handler = {
    fetch: (request: Request) => app.fetch(request),
    async upgrade(req: IncomingMessage, socket: Duplex, head: Buffer) {
      const url = new URL(req.url ?? "/", baseUrl);
      const headers = new Headers();
      for (const [key, value] of Object.entries(req.headers)) {
        if (value) headers.append(key, Array.isArray(value) ? value[0] : value);
      }
      // env 对象身份将此请求回链到上面的路由处理器
      const env = { incoming: req, outgoing: undefined };
      const response = await app.request(url, { headers }, env);
      const wire = pending.get(env);
      pending.delete(env);
      if (!wire) {
        socket.end(`HTTP/1.1 ${response.status} ${STATUS_CODES[response.status] ?? ""}\r\nConnection: close\r\nContent-Length: 0\r\n\r\n`);
        return;
      }
      wss.handleUpgrade(req, socket, head, (ws) => wire(ws));
    },
  };

  return { upgradeWebSocket, handler };
}
```

工作原理：`upgrade` 处理器将握手请求通过 `app.request(...)` 运行，使 Hono 的路由器匹配 `upgradeWebSocket` 路由；辅助方法注册一个以每次请求 `env` 对象为键的 `wire` 回调；如果路由匹配，`wss.handleUpgrade` 接受套接字并附加生命周期处理器，否则套接字以路由状态码关闭（如 401/404）。

## 用法

因为握手经由 `app.request` 路由，**认证和其他门控就是路由上的普通 Hono 中间件**——验证 `?token=` 并在升级前返回 401：

```typescript
// src/index.ts
import { Hono } from "hono";
import { createNeonWebSocket } from "./hono-ws";

const app = new Hono();
const { upgradeWebSocket, handler } = createNeonWebSocket(app);

app.get("/", (c) => c.text("ok"));

app.get(
  "/ws",
  async (c, next) => {
    const identity = await verifyToken(c.req.query("token")); // 你的 JWT 校验
    if (!identity) return c.text("Unauthorized", 401);
    await next();
  },
  upgradeWebSocket(() => ({
    onOpen: (_evt, ws) => ws.send("welcome"),
    onMessage: (evt, ws) => ws.send(`echo: ${evt.data}`),
    onClose: () => console.log("disconnected"),
  })),
);

export default handler; // Neon 的 { fetch, upgrade } 契约
```

## 注意事项

- **WS 路由上不放修改请求头的中间件。** 根据 [Hono 文档](https://hono.dev/docs/helpers/websocket)，在 `upgradeWebSocket` 路由上修改请求头的中间件（如 CORS）会抛异常（"can't modify immutable headers"），因为辅助方法内部会重写请求头。仅读取查询/请求头并返回 401 的认证中间件没有问题。
- **发送心跳。** 套接字一旦静默就会被断开——Neon 的窗口为 15 分钟（[超时](../SKILL.md#超时与运行时限制)），但中间代理通常严格得多（几十秒）。每 ~25–30 秒发送一次保活消息以防连接静默。使用原生 `ws` 套接字时用 `ws.ping()`（浏览器自动回复 pong）；通过此辅助方法不持有原始套接字，因此改为发送应用级 `ws.send("ping")` 由客户端忽略。见 [心跳](../SKILL.md#心跳-保持套接字存活)。
- **广播和重连仍然适用。** 此适配器仅处理 per-isolate 握手。要实现跨 isolate 的真正共享聊天，通过 Postgres `LISTEN`/`NOTIFY` 广播，客户端带退避重连——见 [跨 isolate 广播](../SKILL.md#跨-isolate-广播-不要跳过本节)和 [客户端必须重新连接](../SKILL.md#客户端必须重新连接)。
- **仅限 Node 全局变量。** 依赖 `Event`、`MessageEvent` 和 `CloseEvent`（均存在于 Neon 的 Node 24 运行时）。故意避免 `ErrorEvent`，因为它不是 Node 全局变量。
