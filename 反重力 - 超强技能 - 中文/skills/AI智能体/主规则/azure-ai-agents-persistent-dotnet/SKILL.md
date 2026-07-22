---
name: azure-ai-agents-persistent-dotnet
description: Azure AI Agents Persistent .NET SDK。用于创建和管理具有线程、消息、运行和工具的持久化 AI 智能体的底层 SDK。触发词：Azure AI Agents、持久化智能体、.NET SDK、智能体线程、智能体消息、智能体运行、智能体工具、PersistentAgentsClient、CodeInterpreterToolDefinition、FileSearchToolDefinition、FunctionToolDefinition、BingGroundingToolDefinition、AzureAISearchToolDefinition、智能体流式响应、智能体函数调用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.AI.Agents.Persistent (.NET)

用于创建和管理具有线程、消息、运行和工具的持久化 AI 智能体的底层 SDK。

## 安装

```bash
dotnet add package Azure.AI.Agents.Persistent --prerelease
dotnet add package Azure.Identity
```

**当前版本**：稳定版 v1.1.0，预览版 v1.2.0-beta.8

## 环境变量

```bash
PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_BING_CONNECTION_ID=<bing-connection-resource-id>
AZURE_AI_SEARCH_CONNECTION_ID=<search-connection-resource-id>
```

## 身份验证

```csharp
using Azure.AI.Agents.Persistent;
using Azure.Identity;

var projectEndpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());
```

## 客户端层级结构

```
PersistentAgentsClient
├── Administration  → 智能体 CRUD 操作
├── Threads         → 线程管理
├── Messages        → 消息操作
├── Runs            → 运行执行和流式处理
├── Files           → 文件上传/下载
└── VectorStores    → 向量存储管理
```

## 核心工作流程

### 1. 创建智能体

```csharp
var modelDeploymentName = Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");

PersistentAgent agent = await client.Administration.CreateAgentAsync(
    model: modelDeploymentName,
    name: "Math Tutor",
    instructions: "You are a personal math tutor. Write and run code to answer math questions.",
    tools: [new CodeInterpreterToolDefinition()]
);
```

### 2. 创建线程和消息

```csharp
// 创建线程
PersistentAgentThread thread = await client.Threads.CreateThreadAsync();

// 创建消息
await client.Messages.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "I need to solve the equation `3x + 11 = 14`. Can you help me?"
);
```

### 3. 运行智能体（轮询模式）

```csharp
// 创建运行
ThreadRun run = await client.Runs.CreateRunAsync(
    thread.Id,
    agent.Id,
    additionalInstructions: "Please address the user as Jane Doe."
);

// 轮询等待完成
do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    run = await client.Runs.GetRunAsync(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued || run.Status == RunStatus.InProgress);

// 获取消息
await foreach (PersistentThreadMessage message in client.Messages.GetMessagesAsync(
    threadId: thread.Id, 
    order: ListSortOrder.Ascending))
{
    Console.Write($"{message.Role}: ");
    foreach (MessageContent content in message.ContentItems)
    {
        if (content is MessageTextContent textContent)
            Console.WriteLine(textContent.Text);
    }
}
```

### 4. 流式响应

```csharp
AsyncCollectionResult<StreamingUpdate> stream = client.Runs.CreateRunStreamingAsync(
    thread.Id, 
    agent.Id
);

await foreach (StreamingUpdate update in stream)
{
    if (update.UpdateKind == StreamingUpdateReason.RunCreated)
    {
        Console.WriteLine("--- Run started! ---");
    }
    else if (update is MessageContentUpdate contentUpdate)
    {
        Console.Write(contentUpdate.Text);
    }
    else if (update.UpdateKind == StreamingUpdateReason.RunCompleted)
    {
        Console.WriteLine("\n--- Run completed! ---");
    }
}
```

### 5. 函数调用

```csharp
// 定义函数工具
FunctionToolDefinition weatherTool = new(
    name: "getCurrentWeather",
    description: "Gets the current weather at a location.",
    parameters: BinaryData.FromObjectAsJson(new
    {
        Type = "object",
        Properties = new
        {
            Location = new { Type = "string", Description = "City and state, e.g. San Francisco, CA" },
            Unit = new { Type = "string", Enum = new[] { "c", "f" } }
        },
        Required = new[] { "location" }
    }, new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase })
);

// 创建带函数的智能体
PersistentAgent agent = await client.Administration.CreateAgentAsync(
    model: modelDeploymentName,
    name: "Weather Bot",
    instructions: "You are a weather bot.",
    tools: [weatherTool]
);

// 在轮询过程中处理函数调用
do
{
    await Task.Delay(500);
    run = await client.Runs.GetRunAsync(thread.Id, run.Id);

    if (run.Status == RunStatus.RequiresAction 
        && run.RequiredAction is SubmitToolOutputsAction submitAction)
    {
        List<ToolOutput> outputs = [];
        foreach (RequiredToolCall toolCall in submitAction.ToolCalls)
        {
            if (toolCall is RequiredFunctionToolCall funcCall)
            {
                // 执行函数并获取结果
                string result = ExecuteFunction(funcCall.Name, funcCall.Arguments);
                outputs.Add(new ToolOutput(toolCall, result));
            }
        }
        run = await client.Runs.SubmitToolOutputsToRunAsync(run, outputs, toolApprovals: null);
    }
}
while (run.Status == RunStatus.Queued || run.Status == RunStatus.InProgress);
```

### 6. 使用向量存储的文件搜索

```csharp
// 上传文件
PersistentAgentFileInfo file = await client.Files.UploadFileAsync(
    filePath: "document.txt",
    purpose: PersistentAgentFilePurpose.Agents
);

// 创建向量存储
PersistentAgentsVectorStore vectorStore = await client.VectorStores.CreateVectorStoreAsync(
    fileIds: [file.Id],
    name: "my_vector_store"
);

// 创建文件搜索资源
FileSearchToolResource fileSearchResource = new();
fileSearchResource.VectorStoreIds.Add(vectorStore.Id);

// 创建带文件搜索的智能体
PersistentAgent agent = await client.Administration.CreateAgentAsync(
    model: modelDeploymentName,
    name: "Document Assistant",
    instructions: "You help users find information in documents.",
    tools: [new FileSearchToolDefinition()],
    toolResources: new ToolResources { FileSearch = fileSearchResource }
);
```

### 7. Bing 地面化

```csharp
var bingConnectionId = Environment.GetEnvironmentVariable("AZURE_BING_CONNECTION_ID");

BingGroundingToolDefinition bingTool = new(
    new BingGroundingSearchToolParameters(
        [new BingGroundingSearchConfiguration(bingConnectionId)]
    )
);

PersistentAgent agent = await client.Administration.CreateAgentAsync(
    model: modelDeploymentName,
    name: "Search Agent",
    instructions: "Use Bing to answer questions about current events.",
    tools: [bingTool]
);
```

### 8. Azure AI Search

```csharp
AzureAISearchToolResource searchResource = new(
    connectionId: searchConnectionId,
    indexName: "my_index",
    topK: 5,
    filter: "category eq 'documentation'",
    queryType: AzureAISearchQueryType.Simple
);

PersistentAgent agent = await client.Administration.CreateAgentAsync(
    model: modelDeploymentName,
    name: "Search Agent",
    instructions: "Search the documentation index to answer questions.",
    tools: [new AzureAISearchToolDefinition()],
    toolResources: new ToolResources { AzureAISearch = searchResource }
);
```

### 9. 清理资源

```csharp
await client.Threads.DeleteThreadAsync(thread.Id);
await client.Administration.DeleteAgentAsync(agent.Id);
await client.VectorStores.DeleteVectorStoreAsync(vectorStore.Id);
await client.Files.DeleteFileAsync(file.Id);
```

## 可用工具

| 工具 | 类 | 用途 |
|------|-------|---------|
| Code Interpreter | `CodeInterpreterToolDefinition` | 执行 Python 代码，生成可视化 |
| File Search | `FileSearchToolDefinition` | 通过向量存储搜索上传的文件 |
| Function Calling | `FunctionToolDefinition` | 调用自定义函数 |
| Bing Grounding | `BingGroundingToolDefinition` | 通过 Bing 进行网络搜索 |
| Azure AI Search | `AzureAISearchToolDefinition` | 搜索 Azure AI Search 索引 |
| OpenAPI | `OpenApiToolDefinition` | 通过 OpenAPI 规范调用外部 API |
| Azure Functions | `AzureFunctionToolDefinition` | 调用 Azure Functions |
| MCP | `MCPToolDefinition` | Model Context Protocol 工具 |
| SharePoint | `SharepointToolDefinition` | 访问 SharePoint 内容 |
| Microsoft Fabric | `MicrosoftFabricToolDefinition` | 访问 Fabric 数据 |

## 流式更新类型

| 更新类型 | 描述 |
|-------------|-------------|
| `StreamingUpdateReason.RunCreated` | 运行已启动 |
| `StreamingUpdateReason.RunInProgress` | 运行处理中 |
| `StreamingUpdateReason.RunCompleted` | 运行已完成 |
| `StreamingUpdateReason.RunFailed` | 运行出错 |
| `MessageContentUpdate` | 文本内容块 |
| `RunStepUpdate` | 步骤状态变更 |

## 关键类型参考

| 类型 | 用途 |
|------|---------|
| `PersistentAgentsClient` | 主入口点 |
| `PersistentAgent` | 具有模型、指令、工具的智能体 |
| `PersistentAgentThread` | 对话线程 |
| `PersistentThreadMessage` | 线程中的消息 |
| `ThreadRun` | 智能体在线程上的执行 |
| `RunStatus` | Queued、InProgress、RequiresAction、Completed、Failed |
| `ToolResources` | 组合工具资源 |
| `ToolOutput` | 函数调用响应 |

## 最佳实践

1. **始终释放客户端** — 使用 `using` 语句或显式释放
2. **使用适当的延迟轮询** — 状态检查之间建议 500ms
3. **清理资源** — 完成后删除线程和智能体
4. **处理所有运行状态** — 检查 `RequiresAction`、`Failed`、`Cancelled`
5. **使用流式处理实现实时用户体验** — 比轮询更好的用户体验
6. **存储 ID 而非对象** — 通过 ID 引用智能体/线程
7. **使用异步方法** — 所有操作都应该是异步的

## 错误处理

```csharp
using Azure;

try
{
    var agent = await client.Administration.CreateAgentAsync(...);
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Resource not found");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 相关 SDK

| SDK | 用途 | 安装命令 |
|-----|---------|---------|
| `Azure.AI.Agents.Persistent` | 底层智能体（本 SDK） | `dotnet add package Azure.AI.Agents.Persistent` |
| `Azure.AI.Projects` | 高层项目客户端 | `dotnet add package Azure.AI.Projects` |

## 参考链接

| 资源 | URL |
|----------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.AI.Agents.Persistent |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.ai.agents.persistent |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Agents.Persistent |
| 示例代码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Agents.Persistent/samples |

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
