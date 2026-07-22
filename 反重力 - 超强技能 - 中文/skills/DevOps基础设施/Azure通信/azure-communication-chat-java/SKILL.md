---
name: azure-communication-chat-java
description: "使用 Java 构建实时聊天应用，支持会话线程管理、消息收发、参与者管理和已读回执。触发词：Azure聊天Java、实时消息Java、聊天线程、聊天参与者、已读回执、输入通知、Azure Communication Services聊天"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Communication Chat (Java)

使用 Java 构建实时聊天应用，支持会话线程管理、消息收发、参与者管理和已读回执。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-chat</artifactId>
    <version>1.6.0</version>
</dependency>
```

## 创建客户端

```java
import com.azure.communication.chat.ChatClient;
import com.azure.communication.chat.ChatClientBuilder;
import com.azure.communication.chat.ChatThreadClient;
import com.azure.communication.common.CommunicationTokenCredential;

// ChatClient 需要 CommunicationTokenCredential（用户访问令牌）
String endpoint = "https://<resource>.communication.azure.com";
String userAccessToken = "<user-access-token>";

CommunicationTokenCredential credential = new CommunicationTokenCredential(userAccessToken);

ChatClient chatClient = new ChatClientBuilder()
    .endpoint(endpoint)
    .credential(credential)
    .buildClient();

// 异步客户端
ChatAsyncClient chatAsyncClient = new ChatClientBuilder()
    .endpoint(endpoint)
    .credential(credential)
    .buildAsyncClient();
```

## 核心概念

| 类 | 用途 |
|-------|---------|
| `ChatClient` | 创建/删除聊天线程，获取线程客户端 |
| `ChatThreadClient` | 线程内操作（消息、参与者、回执） |
| `ChatParticipant` | 聊天线程中的用户及其显示名称 |
| `ChatMessage` | 消息内容、类型、发送者信息、时间戳 |
| `ChatMessageReadReceipt` | 每个参与者的已读回执追踪 |

## 创建聊天线程

```java
import com.azure.communication.chat.models.*;
import com.azure.communication.common.CommunicationUserIdentifier;
import java.util.ArrayList;
import java.util.List;

// 定义参与者
List<ChatParticipant> participants = new ArrayList<>();

ChatParticipant participant1 = new ChatParticipant()
    .setCommunicationIdentifier(new CommunicationUserIdentifier("<user-id-1>"))
    .setDisplayName("Alice");

ChatParticipant participant2 = new ChatParticipant()
    .setCommunicationIdentifier(new CommunicationUserIdentifier("<user-id-2>"))
    .setDisplayName("Bob");

participants.add(participant1);
participants.add(participant2);

// 创建线程
CreateChatThreadOptions options = new CreateChatThreadOptions("项目讨论")
    .setParticipants(participants);

CreateChatThreadResult result = chatClient.createChatThread(options);
String threadId = result.getChatThread().getId();

// 获取线程客户端用于后续操作
ChatThreadClient threadClient = chatClient.getChatThreadClient(threadId);
```

## 发送消息

```java
// 发送文本消息
SendChatMessageOptions messageOptions = new SendChatMessageOptions()
    .setContent("大家好！")
    .setSenderDisplayName("Alice")
    .setType(ChatMessageType.TEXT);

SendChatMessageResult sendResult = threadClient.sendMessage(messageOptions);
String messageId = sendResult.getId();

// 发送 HTML 消息
SendChatMessageOptions htmlOptions = new SendChatMessageOptions()
    .setContent("<strong>重要：</strong>下午3点开会")
    .setType(ChatMessageType.HTML);

threadClient.sendMessage(htmlOptions);
```

## 获取消息

```java
import com.azure.core.util.paging.PagedIterable;

// 列出所有消息
PagedIterable<ChatMessage> messages = threadClient.listMessages();

for (ChatMessage message : messages) {
    System.out.println("ID: " + message.getId());
    System.out.println("类型: " + message.getType());
    System.out.println("内容: " + message.getContent().getMessage());
    System.out.println("发送者: " + message.getSenderDisplayName());
    System.out.println("创建时间: " + message.getCreatedOn());
    
    // 检查是否已编辑或删除
    if (message.getEditedOn() != null) {
        System.out.println("编辑时间: " + message.getEditedOn());
    }
    if (message.getDeletedOn() != null) {
        System.out.println("删除时间: " + message.getDeletedOn());
    }
}

// 获取特定消息
ChatMessage message = threadClient.getMessage(messageId);
```

## 更新和删除消息

```java
// 更新消息
UpdateChatMessageOptions updateOptions = new UpdateChatMessageOptions()
    .setContent("更新后的消息内容");

threadClient.updateMessage(messageId, updateOptions);

// 删除消息
threadClient.deleteMessage(messageId);
```

## 管理参与者

```java
// 列出参与者
PagedIterable<ChatParticipant> participants = threadClient.listParticipants();

for (ChatParticipant participant : participants) {
    CommunicationUserIdentifier user = 
        (CommunicationUserIdentifier) participant.getCommunicationIdentifier();
    System.out.println("用户: " + user.getId());
    System.out.println("显示名称: " + participant.getDisplayName());
}

// 添加参与者
List<ChatParticipant> newParticipants = new ArrayList<>();
newParticipants.add(new ChatParticipant()
    .setCommunicationIdentifier(new CommunicationUserIdentifier("<new-user-id>"))
    .setDisplayName("Charlie")
    .setShareHistoryTime(OffsetDateTime.now().minusDays(7))); // 共享最近7天

threadClient.addParticipants(newParticipants);

// 移除参与者
CommunicationUserIdentifier userToRemove = new CommunicationUserIdentifier("<user-id>");
threadClient.removeParticipant(userToRemove);
```

## 已读回执

```java
// 发送已读回执
threadClient.sendReadReceipt(messageId);

// 获取已读回执列表
PagedIterable<ChatMessageReadReceipt> receipts = threadClient.listReadReceipts();

for (ChatMessageReadReceipt receipt : receipts) {
    System.out.println("消息ID: " + receipt.getChatMessageId());
    System.out.println("已读者: " + receipt.getSenderCommunicationIdentifier());
    System.out.println("阅读时间: " + receipt.getReadOn());
}
```

## 输入通知

```java
import com.azure.communication.chat.models.TypingNotificationOptions;

// 发送输入通知
TypingNotificationOptions typingOptions = new TypingNotificationOptions()
    .setSenderDisplayName("Alice");

threadClient.sendTypingNotificationWithResponse(typingOptions, Context.NONE);

// 简单输入通知
threadClient.sendTypingNotification();
```

## 线程操作

```java
// 获取线程属性
ChatThreadProperties properties = threadClient.getProperties();
System.out.println("主题: " + properties.getTopic());
System.out.println("创建时间: " + properties.getCreatedOn());

// 更新主题
threadClient.updateTopic("新项目讨论主题");

// 删除线程
chatClient.deleteChatThread(threadId);
```

## 列出线程

```java
// 列出用户的所有聊天线程
PagedIterable<ChatThreadItem> threads = chatClient.listChatThreads();

for (ChatThreadItem thread : threads) {
    System.out.println("线程ID: " + thread.getId());
    System.out.println("主题: " + thread.getTopic());
    System.out.println("最后消息: " + thread.getLastMessageReceivedOn());
}
```

## 分页

```java
import com.azure.core.http.rest.PagedResponse;

// 分页获取消息
int maxPageSize = 10;
ListChatMessagesOptions listOptions = new ListChatMessagesOptions()
    .setMaxPageSize(maxPageSize);

PagedIterable<ChatMessage> pagedMessages = threadClient.listMessages(listOptions);

pagedMessages.iterableByPage().forEach(page -> {
    System.out.println("页面状态码: " + page.getStatusCode());
    page.getElements().forEach(msg -> 
        System.out.println("消息: " + msg.getContent().getMessage()));
});
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    threadClient.sendMessage(messageOptions);
} catch (HttpResponseException e) {
    switch (e.getResponse().getStatusCode()) {
        case 401:
            System.out.println("未授权 - 请检查令牌");
            break;
        case 403:
            System.out.println("禁止访问 - 用户不在该线程中");
            break;
        case 404:
            System.out.println("线程未找到");
            break;
        default:
            System.out.println("错误: " + e.getMessage());
    }
}
```

## 消息类型

| 类型 | 描述 |
|------|-------------|
| `TEXT` | 普通聊天消息 |
| `HTML` | HTML 格式消息 |
| `TOPIC_UPDATED` | 系统消息 - 主题已更改 |
| `PARTICIPANT_ADDED` | 系统消息 - 参与者已加入 |
| `PARTICIPANT_REMOVED` | 系统消息 - 参与者已离开 |

## 环境变量

```bash
AZURE_COMMUNICATION_ENDPOINT=https://<resource>.communication.azure.com
AZURE_COMMUNICATION_USER_TOKEN=<user-access-token>
```

## 最佳实践

1. **令牌管理** - 用户令牌会过期；使用 `CommunicationTokenRefreshOptions` 实现刷新逻辑
2. **分页** - 对于大型线程，使用带 `maxPageSize` 的 `listMessages(options)` 进行分页
3. **共享历史** - 添加参与者时设置 `shareHistoryTime` 以控制消息可见性
4. **消息类型** - 从用户消息中过滤系统消息（`PARTICIPANT_ADDED` 等）
5. **已读回执** - 仅在用户实际查看消息时发送回执

## 触发词

- "聊天应用 Java"、"实时消息 Java"
- "聊天线程"、"聊天参与者"、"聊天消息"
- "已读回执"、"输入通知"
- "Azure Communication Services 聊天"

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
