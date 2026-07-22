---
name: azure-messaging-webpubsub-java
description: "使用 Azure Web PubSub SDK for Java 构建实时 Web 应用。当用户要求实现基于 WebSocket 的消息传递、实时更新、聊天应用或服务器到客户端的推送通知时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Web PubSub SDK for Java

使用 Azure Web PubSub SDK for Java 构建实时 Web 应用。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-messaging-webpubsub</artifactId>
    <version>1.5.0</version>
</dependency>
```

## 客户端创建

### 使用连接字符串

```java
import com.azure.messaging.webpubsub.WebPubSubServiceClient;
import com.azure.messaging.webpubsub.WebPubSubServiceClientBuilder;

WebPubSubServiceClient client = new WebPubSubServiceClientBuilder()
    .connectionString("<connection-string>")
    .hub("chat")
    .buildClient();
```

### 使用访问密钥

```java
import com.azure.core.credential.AzureKeyCredential;

WebPubSubServiceClient client = new WebPubSubServiceClientBuilder()
    .credential(new AzureKeyCredential("<access-key>"))
    .endpoint("<endpoint>")
    .hub("chat")
    .buildClient();
```

### 使用 DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

WebPubSubServiceClient client = new WebPubSubServiceClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint("<endpoint>")
    .hub("chat")
    .buildClient();
```

### 异步客户端

```java
import com.azure.messaging.webpubsub.WebPubSubServiceAsyncClient;

WebPubSubServiceAsyncClient asyncClient = new WebPubSubServiceClientBuilder()
    .connectionString("<connection-string>")
    .hub("chat")
    .buildAsyncClient();
```

## 核心概念

- **Hub**：连接的逻辑隔离单元
- **Group**：Hub 内的连接子集
- **Connection**：单个 WebSocket 客户端连接
- **User**：可以拥有多个连接的实体

## 核心模式

### 向所有连接发送消息

```java
import com.azure.messaging.webpubsub.models.WebPubSubContentType;

// Send text message
client.sendToAll("Hello everyone!", WebPubSubContentType.TEXT_PLAIN);

// Send JSON
String jsonMessage = "{\"type\": \"notification\", \"message\": \"New update!\"}";
client.sendToAll(jsonMessage, WebPubSubContentType.APPLICATION_JSON);
```

### 带过滤条件向所有连接发送

```java
import com.azure.core.http.rest.RequestOptions;
import com.azure.core.util.BinaryData;

BinaryData message = BinaryData.fromString("Hello filtered users!");

// Filter by userId
client.sendToAllWithResponse(
    message,
    WebPubSubContentType.TEXT_PLAIN,
    message.getLength(),
    new RequestOptions().addQueryParam("filter", "userId ne 'user1'"));

// Filter by groups
client.sendToAllWithResponse(
    message,
    WebPubSubContentType.TEXT_PLAIN,
    message.getLength(),
    new RequestOptions().addQueryParam("filter", "'GroupA' in groups and not('GroupB' in groups)"));
```

### 向 Group 发送消息

```java
// Send to all connections in a group
client.sendToGroup("java-developers", "Hello Java devs!", WebPubSubContentType.TEXT_PLAIN);

// Send JSON to group
String json = "{\"event\": \"update\", \"data\": {\"version\": \"2.0\"}}";
client.sendToGroup("subscribers", json, WebPubSubContentType.APPLICATION_JSON);
```

### 向特定连接发送消息

```java
// Send to a specific connection by ID
client.sendToConnection("connectionId123", "Private message", WebPubSubContentType.TEXT_PLAIN);
```

### 向用户发送消息

```java
// Send to all connections for a specific user
client.sendToUser("andy", "Hello Andy!", WebPubSubContentType.TEXT_PLAIN);
```

### 管理 Group

```java
// Add connection to group
client.addConnectionToGroup("premium-users", "connectionId123");

// Remove connection from group
client.removeConnectionFromGroup("premium-users", "connectionId123");

// Add user to group (all their connections)
client.addUserToGroup("admin-group", "userId456");

// Remove user from group
client.removeUserFromGroup("admin-group", "userId456");

// Check if user is in group
boolean exists = client.userExistsInGroup("admin-group", "userId456");
```

### 管理连接

```java
// Check if connection exists
boolean connected = client.connectionExists("connectionId123");

// Close a connection
client.closeConnection("connectionId123");

// Close with reason
client.closeConnection("connectionId123", "Session expired");

// Check if user exists (has any connections)
boolean userOnline = client.userExists("userId456");

// Close all connections for a user
client.closeUserConnections("userId456");

// Close all connections in a group
client.closeGroupConnections("inactive-group");
```

### 生成客户端访问令牌

```java
import com.azure.messaging.webpubsub.models.GetClientAccessTokenOptions;
import com.azure.messaging.webpubsub.models.WebPubSubClientAccessToken;

// Basic token
WebPubSubClientAccessToken token = client.getClientAccessToken(
    new GetClientAccessTokenOptions());
System.out.println("URL: " + token.getUrl());

// With user ID
WebPubSubClientAccessToken userToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions().setUserId("user123"));

// With roles (permissions)
WebPubSubClientAccessToken roleToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions()
        .setUserId("user123")
        .addRole("webpubsub.joinLeaveGroup")
        .addRole("webpubsub.sendToGroup"));

// With groups to join on connect
WebPubSubClientAccessToken groupToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions()
        .setUserId("user123")
        .addGroup("announcements")
        .addGroup("updates"));

// With custom expiration
WebPubSubClientAccessToken expToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions()
        .setUserId("user123")
        .setExpiresAfter(Duration.ofHours(2)));
```

### 授予/撤销权限

```java
import com.azure.messaging.webpubsub.models.WebPubSubPermission;

// Grant permission to send to a group
client.grantPermission(
    WebPubSubPermission.SEND_TO_GROUP,
    "connectionId123",
    new RequestOptions().addQueryParam("targetName", "chat-room"));

// Revoke permission
client.revokePermission(
    WebPubSubPermission.SEND_TO_GROUP,
    "connectionId123",
    new RequestOptions().addQueryParam("targetName", "chat-room"));

// Check permission
boolean hasPermission = client.checkPermission(
    WebPubSubPermission.SEND_TO_GROUP,
    "connectionId123",
    new RequestOptions().addQueryParam("targetName", "chat-room"));
```

### 异步操作

```java
asyncClient.sendToAll("Async message!", WebPubSubContentType.TEXT_PLAIN)
    .subscribe(
        unused -> System.out.println("Message sent"),
        error -> System.err.println("Error: " + error.getMessage())
    );

asyncClient.sendToGroup("developers", "Group message", WebPubSubContentType.TEXT_PLAIN)
    .doOnSuccess(v -> System.out.println("Sent to group"))
    .doOnError(e -> System.err.println("Failed: " + e))
    .subscribe();
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.sendToConnection("invalid-id", "test", WebPubSubContentType.TEXT_PLAIN);
} catch (HttpResponseException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
}
```

## 环境变量

```bash
WEB_PUBSUB_CONNECTION_STRING=Endpoint=https://<resource>.webpubsub.azure.com;AccessKey=...
WEB_PUBSUB_ENDPOINT=https://<resource>.webpubsub.azure.com
WEB_PUBSUB_ACCESS_KEY=<your-access-key>
```

## 客户端角色

| 角色 | 权限 |
|------|------|
| `webpubsub.joinLeaveGroup` | 加入/离开任意 Group |
| `webpubsub.sendToGroup` | 向任意 Group 发送消息 |
| `webpubsub.joinLeaveGroup.<group>` | 加入/离开指定 Group |
| `webpubsub.sendToGroup.<group>` | 向指定 Group 发送消息 |

## 最佳实践

1. **使用 Group**：将连接组织到 Group 中以实现定向消息传递
2. **用户 ID**：将连接与用户 ID 关联以实现用户级消息传递
3. **令牌过期**：设置适当的令牌过期时间以确保安全
4. **角色**：通过角色授予最小必要权限
5. **Hub 隔离**：为不同的应用功能使用独立的 Hub
6. **连接管理**：清理不活跃的连接

## 触发词

- "Web PubSub Java"
- "WebSocket messaging Azure"
- "real-time push notifications"
- "server-sent events"
- "chat application backend"
- "live updates broadcasting"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述描述的范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
