---
name: azure-ai-agents-persistent-java
description: Azure AI Agents Persistent SDK for Java。用于创建和管理具有线程、消息、运行和工具的持久化 AI 智能体的底层 SDK。触发词：Azure AI Agents、Java SDK、持久化智能体、PersistentAgentsClient、AI 代理、线程管理、消息运行、工具调用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI Agents Persistent SDK for Java

用于创建和管理具有线程、消息、运行和工具的持久化 AI 智能体的底层 SDK。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents-persistent</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
```

## 环境变量

```bash
PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

## 身份验证

```java
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

String endpoint = System.getenv("PROJECT_ENDPOINT");
PersistentAgentsClient client = new PersistentAgentsClientBuilder()
    .endpoint(endpoint)
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

## 核心概念

Azure AI Agents Persistent SDK 提供底层 API，用于管理可跨会话复用的持久化智能体。

### 客户端层级

| 客户端 | 用途 |
|--------|------|
| `PersistentAgentsClient` | 同步客户端，用于智能体操作 |
| `PersistentAgentsAsyncClient` | 异步客户端，用于智能体操作 |

## 核心工作流

### 1. 创建智能体

```java
// 创建带工具的智能体
PersistentAgent agent = client.createAgent(
    modelDeploymentName,
    "Math Tutor",
    "You are a personal math tutor."
);
```

### 2. 创建线程

```java
PersistentAgentThread thread = client.createThread();
```

### 3. 添加消息

```java
client.createMessage(
    thread.getId(),
    MessageRole.USER,
    "I need help with equations."
);
```

### 4. 运行智能体

```java
ThreadRun run = client.createRun(thread.getId(), agent.getId());

// 轮询等待完成
while (run.getStatus() == RunStatus.QUEUED || run.getStatus() == RunStatus.IN_PROGRESS) {
    Thread.sleep(500);
    run = client.getRun(thread.getId(), run.getId());
}
```

### 5. 获取响应

```java
PagedIterable<PersistentThreadMessage> messages = client.listMessages(thread.getId());
for (PersistentThreadMessage message : messages) {
    System.out.println(message.getRole() + ": " + message.getContent());
}
```

### 6. 清理资源

```java
client.deleteThread(thread.getId());
client.deleteAgent(agent.getId());
```

## 最佳实践

1. **生产环境使用 DefaultAzureCredential** 进行身份验证
2. **轮询间隔适当** — 状态检查之间建议间隔 500ms
3. **及时清理资源** — 使用完毕后删除线程和智能体
4. **处理所有运行状态** — 检查 RequiresAction、Failed、Cancelled 等状态
5. **高并发场景使用异步客户端** 以获得更好的吞吐量

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    PersistentAgent agent = client.createAgent(modelName, name, instructions);
} catch (HttpResponseException e) {
    System.err.println("Error: " + e.getResponse().getStatusCode() + " - " + e.getMessage());
}
```

## 参考链接

| 资源 | URL |
|------|-----|
| Maven Package | https://central.sonatype.com/artifact/com.azure/azure-ai-agents-persistent |
| GitHub Source | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents-persistent |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不应替代特定环境的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
