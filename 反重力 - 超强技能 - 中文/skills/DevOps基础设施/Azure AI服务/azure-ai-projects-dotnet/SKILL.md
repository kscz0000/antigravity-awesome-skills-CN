---
name: azure-ai-projects-dotnet
description: Azure AI Projects .NET SDK，用于 Azure AI Foundry 项目的高级客户端，包括代理、连接、数据集、部署、评估和索引。触发词：Azure AI Projects、.NET SDK、AI Foundry、Azure代理、Azure Agents、PersistentAgentsClient、AIProjectClient、Azure AI开发、版本化代理、Azure OpenAI
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.AI.Projects (.NET)

用于 Azure AI Foundry 项目操作的高级 SDK，包括代理、连接、数据集、部署、评估和索引。

## 安装

```bash
dotnet add package Azure.AI.Projects
dotnet add package Azure.Identity

# 可选：用于带 OpenAI 扩展的版本化代理
dotnet add package Azure.AI.Projects.OpenAI --prerelease

# 可选：用于底层代理操作
dotnet add package Azure.AI.Agents.Persistent --prerelease
```

**当前版本**：GA v1.1.0，预览版 v1.2.0-beta.5

## 环境变量

```bash
PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
CONNECTION_NAME=<your-connection-name>
AI_SEARCH_CONNECTION_NAME=<ai-search-connection>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.AI.Projects;

var endpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
AIProjectClient projectClient = new AIProjectClient(
    new Uri(endpoint), 
    new DefaultAzureCredential());
```

## 客户端层次结构

```
AIProjectClient
├── Agents          → AIProjectAgentsOperations (版本化代理)
├── Connections     → ConnectionsClient
├── Datasets        → DatasetsClient
├── Deployments     → DeploymentsClient
├── Evaluations     → EvaluationsClient
├── Evaluators      → EvaluatorsClient
├── Indexes         → IndexesClient
├── Telemetry       → AIProjectTelemetry
├── OpenAI          → ProjectOpenAIClient (预览版)
└── GetPersistentAgentsClient() → PersistentAgentsClient
```

## 核心工作流

### 1. 获取持久代理客户端

```csharp
// 从项目客户端获取底层代理客户端
PersistentAgentsClient agentsClient = projectClient.GetPersistentAgentsClient();

// 创建代理
PersistentAgent agent = await agentsClient.Administration.CreateAgentAsync(
    model: "gpt-4o-mini",
    name: "Math Tutor",
    instructions: "You are a personal math tutor.");

// 创建线程并运行
PersistentAgentThread thread = await agentsClient.Threads.CreateThreadAsync();
await agentsClient.Messages.CreateMessageAsync(thread.Id, MessageRole.User, "Solve 3x + 11 = 14");
ThreadRun run = await agentsClient.Runs.CreateRunAsync(thread.Id, agent.Id);

// 轮询等待完成
do
{
    await Task.Delay(500);
    run = await agentsClient.Runs.GetRunAsync(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued || run.Status == RunStatus.InProgress);

// 获取消息
await foreach (var msg in agentsClient.Messages.GetMessagesAsync(thread.Id))
{
    foreach (var content in msg.ContentItems)
    {
        if (content is MessageTextContent textContent)
            Console.WriteLine(textContent.Text);
    }
}

// 清理资源
await agentsClient.Threads.DeleteThreadAsync(thread.Id);
await agentsClient.Administration.DeleteAgentAsync(agent.Id);
```

### 2. 带工具的版本化代理（预览版）

```csharp
using Azure.AI.Projects.OpenAI;

// 创建带网页搜索工具的代理
PromptAgentDefinition agentDefinition = new(model: "gpt-4o-mini")
{
    Instructions = "You are a helpful assistant that can search the web",
    Tools = {
        ResponseTool.CreateWebSearchTool(
            userLocation: WebSearchToolLocation.CreateApproximateLocation(
                country: "US",
                city: "Seattle",
                region: "Washington"
            )
        ),
    }
};

AgentVersion agentVersion = await projectClient.Agents.CreateAgentVersionAsync(
    agentName: "myAgent",
    options: new(agentDefinition));

// 获取响应客户端
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

// 创建响应
ResponseResult response = responseClient.CreateResponse("What's the weather in Seattle?");
Console.WriteLine(response.GetOutputText());

// 清理资源
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### 3. 连接

```csharp
// 列出所有连接
foreach (AIProjectConnection connection in projectClient.Connections.GetConnections())
{
    Console.WriteLine($"{connection.Name}: {connection.ConnectionType}");
}

// 获取特定连接
AIProjectConnection conn = projectClient.Connections.GetConnection(
    connectionName, 
    includeCredentials: true);

// 获取默认连接
AIProjectConnection defaultConn = projectClient.Connections.GetDefaultConnection(
    includeCredentials: false);
```

### 4. 部署

```csharp
// 列出所有部署
foreach (AIProjectDeployment deployment in projectClient.Deployments.GetDeployments())
{
    Console.WriteLine($"{deployment.Name}: {deployment.ModelName}");
}

// 按发布者筛选
foreach (var deployment in projectClient.Deployments.GetDeployments(modelPublisher: "Microsoft"))
{
    Console.WriteLine(deployment.Name);
}

// 获取特定部署
ModelDeployment details = (ModelDeployment)projectClient.Deployments.GetDeployment("gpt-4o-mini");
```

### 5. 数据集

```csharp
// 上传单个文件
FileDataset fileDataset = projectClient.Datasets.UploadFile(
    name: "my-dataset",
    version: "1.0",
    filePath: "data/training.txt",
    connectionName: connectionName);

// 上传文件夹
FolderDataset folderDataset = projectClient.Datasets.UploadFolder(
    name: "my-dataset",
    version: "2.0",
    folderPath: "data/training",
    connectionName: connectionName,
    filePattern: new Regex(".*\\.txt"));

// 获取数据集
AIProjectDataset dataset = projectClient.Datasets.GetDataset("my-dataset", "1.0");

// 删除数据集
projectClient.Datasets.Delete("my-dataset", "1.0");
```

### 6. 索引

```csharp
// 创建 Azure AI Search 索引
AzureAISearchIndex searchIndex = new(aiSearchConnectionName, aiSearchIndexName)
{
    Description = "Sample Index"
};

searchIndex = (AzureAISearchIndex)projectClient.Indexes.CreateOrUpdate(
    name: "my-index",
    version: "1.0",
    index: searchIndex);

// 列出索引
foreach (AIProjectIndex index in projectClient.Indexes.GetIndexes())
{
    Console.WriteLine(index.Name);
}

// 删除索引
projectClient.Indexes.Delete(name: "my-index", version: "1.0");
```

### 7. 评估

```csharp
// 创建评估配置
var evaluatorConfig = new EvaluatorConfiguration(id: EvaluatorIDs.Relevance);
evaluatorConfig.InitParams.Add("deployment_name", BinaryData.FromObjectAsJson("gpt-4o"));

// 创建评估
Evaluation evaluation = new Evaluation(
    data: new InputDataset("<dataset_id>"),
    evaluators: new Dictionary<string, EvaluatorConfiguration> 
    { 
        { "relevance", evaluatorConfig } 
    }
)
{
    DisplayName = "Sample Evaluation"
};

// 运行评估
Evaluation result = projectClient.Evaluations.Create(evaluation: evaluation);

// 获取评估
Evaluation getResult = projectClient.Evaluations.Get(result.Name);

// 列出评估
foreach (var eval in projectClient.Evaluations.GetAll())
{
    Console.WriteLine($"{eval.DisplayName}: {eval.Status}");
}
```

### 8. 获取 Azure OpenAI 聊天客户端

```csharp
using Azure.AI.OpenAI;
using OpenAI.Chat;

ClientConnection connection = projectClient.GetConnection(typeof(AzureOpenAIClient).FullName!);

if (!connection.TryGetLocatorAsUri(out Uri uri) || uri is null)
    throw new InvalidOperationException("Invalid URI.");

uri = new Uri($"https://{uri.Host}");

AzureOpenAIClient azureOpenAIClient = new AzureOpenAIClient(uri, new DefaultAzureCredential());
ChatClient chatClient = azureOpenAIClient.GetChatClient("gpt-4o-mini");

ChatCompletion result = chatClient.CompleteChat("List all rainbow colors");
Console.WriteLine(result.Content[0].Text);
```

## 可用的代理工具

| 工具 | 类 | 用途 |
|------|-------|---------|
| Code Interpreter | `CodeInterpreterToolDefinition` | 执行 Python 代码 |
| File Search | `FileSearchToolDefinition` | 搜索上传的文件 |
| Function Calling | `FunctionToolDefinition` | 调用自定义函数 |
| Bing Grounding | `BingGroundingToolDefinition` | 通过 Bing 进行网页搜索 |
| Azure AI Search | `AzureAISearchToolDefinition` | 搜索 Azure AI 索引 |
| OpenAPI | `OpenApiToolDefinition` | 调用外部 API |
| Azure Functions | `AzureFunctionToolDefinition` | 调用 Azure Functions |
| MCP | `MCPToolDefinition` | Model Context Protocol 工具 |

## 关键类型参考

| 类型 | 用途 |
|------|---------|
| `AIProjectClient` | 主入口点 |
| `PersistentAgentsClient` | 底层代理操作 |
| `PromptAgentDefinition` | 版本化代理定义 |
| `AgentVersion` | 版本化代理实例 |
| `AIProjectConnection` | Azure 资源连接 |
| `AIProjectDeployment` | 模型部署信息 |
| `AIProjectDataset` | 数据集元数据 |
| `AIProjectIndex` | 搜索索引元数据 |
| `Evaluation` | 评估配置和结果 |

## 最佳实践

1. **使用 `DefaultAzureCredential`** 进行生产环境身份验证
2. **使用异步方法**（`*Async`）进行所有 I/O 操作
3. **轮询时使用适当的延迟**（推荐 500ms）等待运行完成
4. **清理资源** — 完成后删除线程、代理和文件
5. **使用版本化代理**（通过 `Azure.AI.Projects.OpenAI`）用于生产场景
6. **存储连接 ID** 而非名称用于工具配置
7. **仅在需要凭据时使用 `includeCredentials: true`**
8. **处理分页** — 使用 `AsyncPageable<T>` 进行列表操作

## 错误处理

```csharp
using Azure;

try
{
    var result = await projectClient.Evaluations.CreateAsync(evaluation);
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 相关 SDK

| SDK | 用途 | 安装命令 |
|-----|---------|---------|
| `Azure.AI.Projects` | 高级项目客户端（本 SDK） | `dotnet add package Azure.AI.Projects` |
| `Azure.AI.Agents.Persistent` | 底层代理操作 | `dotnet add package Azure.AI.Agents.Persistent` |
| `Azure.AI.Projects.OpenAI` | 带 OpenAI 的版本化代理 | `dotnet add package Azure.AI.Projects.OpenAI` |

## 参考链接

| 资源 | URL |
|----------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.AI.Projects |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.ai.projects |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects |
| 示例代码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/samples |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述描述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
