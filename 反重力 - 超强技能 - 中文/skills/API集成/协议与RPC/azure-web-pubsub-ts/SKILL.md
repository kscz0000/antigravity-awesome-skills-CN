---
name: azure-web-pubsub-ts
description: "使用 WebSocket 连接和发布/订阅模式进行实时消息传递。当用户要求'Azure Web PubSub'、'WebSocket 实时消息'、'发布订阅模式'、'实时通信 TypeScript'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Web PubSub SDK for TypeScript

使用 WebSocket 连接和发布/订阅模式进行实时消息传递。

## 安装

```bash
# Server-side management
npm install @azure/web-pubsub @azure/identity

# Client-side real-time messaging
npm install @azure/web-pubsub-client

# Express middleware for event handlers
npm install @azure/web-pubsub-express
```

## 环境变量

```bash
WEBPUBSUB_CONNECTION_STRING=Endpoint=https://<resource>.webpubsub.azure.com;AccessKey=<key>;Version=1.0;
WEBPUBSUB_ENDPOINT=https://<resource>.webpubsub.azure.com
```

## 服务端：WebPubSubServiceClient

### 身份验证

```typescript
import { WebPubSubServiceClient, AzureKeyCredential } from "@azure/web-pubsub";
import { DefaultAzureCredential } from "@azure/identity";

// Connection string
const client = new WebPubSubServiceClient(
  process.env.WEBPUBSUB_CONNECTION_STRING!,
  "chat"  // hub name
);

// DefaultAzureCredential (recommended)
const client2 = new WebPubSubServiceClient(
  process.env.WEBPUBSUB_ENDPOINT!,
  new DefaultAzureCredential(),
  "chat"
);

// AzureKeyCredential
const client3 = new WebPubSubServiceClient(
  process.env.WEBPUBSUB_ENDPOINT!,
  new AzureKeyCredential("<access-key>"),
  "chat"
);
```

### 生成客户端访问令牌

```typescript
// Basic token
const token = await client.getClientAccessToken();
console.log(token.url);  // wss://...?access_token=...

// Token with user ID
const userToken = await client.getClientAccessToken({
  userId: "user123",
});

// Token with permissions
const permToken = await client.getClientAccessToken({
  userId: "user123",
  roles: [
    "webpubsub.joinLeaveGroup",
    "webpubsub.sendToGroup",
    "webpubsub.sendToGroup.chat-room",  // specific group
  ],
  groups: ["chat-room"],  // auto-join on connect
  expirationTimeInMinutes: 60,
});
```

### 发送消息

```typescript
// Broadcast to all connections in hub
await client.sendToAll({ message: "Hello everyone!" });
await client.sendToAll("Plain text", { contentType: "text/plain" });

// Send to specific user (all their connections)
await client.sendToUser("user123", { message: "Hello!" });

// Send to specific connection
await client.sendToConnection("connectionId", { data: "Direct message" });

// Send with filter (OData syntax)
await client.sendToAll({ message: "Filtered" }, {
  filter: "userId ne 'admin'",
});
```

### 群组管理

```typescript
const group = client.group("chat-room");

// Add user/connection to group
await group.addUser("user123");
await group.addConnection("connectionId");

// Remove from group
await group.removeUser("user123");

// Send to group
await group.sendToAll({ message: "Group message" });

// Close all connections in group
await group.closeAllConnections({ reason: "Maintenance" });
```

### 连接管理

```typescript
// Check existence
const userExists = await client.userExists("user123");
const connExists = await client.connectionExists("connectionId");

// Close connections
await client.closeConnection("connectionId", { reason: "Kicked" });
await client.closeUserConnections("user123");
await client.closeAllConnections();

// Permissions
await client.grantPermission("connectionId", "sendToGroup", { targetName: "chat" });
await client.revokePermission("connectionId", "sendToGroup", { targetName: "chat" });
```

## 客户端：WebPubSubClient

### 连接

```typescript
import { WebPubSubClient } from "@azure/web-pubsub-client";

// Direct URL
const client = new WebPubSubClient("<client-access-url>");

// Dynamic URL from negotiate endpoint
const client2 = new WebPubSubClient({
  getClientAccessUrl: async () => {
    const response = await fetch("/negotiate");
    const { url } = await response.json();
    return url;
  },
});

// Register handlers BEFORE starting
client.on("connected", (e) => {
  console.log(`Connected: ${e.connectionId}`);
});

client.on("group-message", (e) => {
  console.log(`${e.message.group}: ${e.message.data}`);
});

await client.start();
```

### 发送消息

```typescript
// Join group first
await client.joinGroup("chat-room");

// Send to group
await client.sendToGroup("chat-room", "Hello!", "text");
await client.sendToGroup("chat-room", { type: "message", content: "Hi" }, "json");

// Send options
await client.sendToGroup("chat-room", "Hello", "text", {
  noEcho: true,        // Don't echo back to sender
  fireAndForget: true, // Don't wait for ack
});

// Send event to server
await client.sendEvent("userAction", { action: "typing" }, "json");
```

### 事件处理

```typescript
// Connection lifecycle
client.on("connected", (e) => {
  console.log(`Connected: ${e.connectionId}, User: ${e.userId}`);
});

client.on("disconnected", (e) => {
  console.log(`Disconnected: ${e.message}`);
});

client.on("stopped", () => {
  console.log("Client stopped");
});

// Messages
client.on("group-message", (e) => {
  console.log(`[${e.message.group}] ${e.message.fromUserId}: ${e.message.data}`);
});

client.on("server-message", (e) => {
  console.log(`Server: ${e.message.data}`);
});

// Rejoin failure
client.on("rejoin-group-failed", (e) => {
  console.log(`Failed to rejoin ${e.group}: ${e.error}`);
});
```

## Express 事件处理器

```typescript
import express from "express";
import { WebPubSubEventHandler } from "@azure/web-pubsub-express";

const app = express();

const handler = new WebPubSubEventHandler("chat", {
  path: "/api/webpubsub/hubs/chat/",
  
  // Blocking: approve/reject connection
  handleConnect: (req, res) => {
    if (!req.claims?.sub) {
      res.fail(401, "Authentication required");
      return;
    }
    res.success({
      userId: req.claims.sub[0],
      groups: ["general"],
      roles: ["webpubsub.sendToGroup"],
    });
  },
  
  // Blocking: handle custom events
  handleUserEvent: (req, res) => {
    console.log(`Event from ${req.context.userId}:`, req.data);
    res.success(`Received: ${req.data}`, "text");
  },
  
  // Non-blocking
  onConnected: (req) => {
    console.log(`Client connected: ${req.context.connectionId}`);
  },
  
  onDisconnected: (req) => {
    console.log(`Client disconnected: ${req.context.connectionId}`);
  },
});

app.use(handler.getMiddleware());

// Negotiate endpoint
app.get("/negotiate", async (req, res) => {
  const token = await serviceClient.getClientAccessToken({
    userId: req.user?.id,
  });
  res.json({ url: token.url });
});

app.listen(8080);
```

## 核心类型

```typescript
// Server
import {
  WebPubSubServiceClient,
  WebPubSubGroup,
  GenerateClientTokenOptions,
  HubSendToAllOptions,
} from "@azure/web-pubsub";

// Client
import {
  WebPubSubClient,
  WebPubSubClientOptions,
  OnConnectedArgs,
  OnGroupDataMessageArgs,
} from "@azure/web-pubsub-client";

// Express
import {
  WebPubSubEventHandler,
  ConnectRequest,
  UserEventRequest,
  ConnectResponseHandler,
} from "@azure/web-pubsub-express";
```

## 最佳实践

1. **使用 Entra ID 身份验证** — 生产环境推荐 `DefaultAzureCredential`
2. **启动前注册处理器** — 避免遗漏初始事件
3. **使用群组作为频道** — 按主题/房间组织消息
4. **处理重连** — 客户端默认自动重连
5. **在 handleConnect 中验证** — 尽早拒绝未授权连接
6. **使用 noEcho** — 需要时防止消息回显给发送者

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不能替代针对特定环境的验证、测试或专家审查。
- 如缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
