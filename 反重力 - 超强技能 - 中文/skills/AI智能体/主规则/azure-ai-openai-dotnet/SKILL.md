---
name: azure-ai-openai-dotnet
description: Azure OpenAI .NET SDK 客户端库，用于访问 Azure OpenAI 和 OpenAI 服务。支持聊天补全、嵌入、图像生成、音频转录和助手功能。触发词：Azure OpenAI、.NET SDK、GPT-4、聊天补全、嵌入、DALL-E、Whisper、函数调用、RAG、Azure AI Search、流式响应、结构化输出。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.AI.OpenAI (.NET)

Azure OpenAI Service 客户端库，提供对 OpenAI 模型的访问，包括 GPT-4、GPT-4o、嵌入、DALL-E 和 Whisper。

## 安装

```bash
dotnet add package Azure.AI.OpenAI

# For OpenAI (non-Azure) compatibility
dotnet add package OpenAI
```

**当前版本**: 2.1.0 (稳定版)

## 环境变量

```bash
AZURE_OPENAI_ENDPOINT=https://<resource-name>.openai.azure.com
AZURE_OPENAI_API_KEY=<api-key>                    # For key-based auth
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini          # Your deployment name
```

## 客户端层次结构

```
AzureOpenAIClient (顶层)
├── GetChatClient(deploymentName)      → ChatClient
├── GetEmbeddingClient(deploymentName) → EmbeddingClient
├── GetImageClient(deploymentName)     → ImageClient
├── GetAudioClient(deploymentName)     → AudioClient
└── GetAssistantClient()               → AssistantClient
```

## 身份验证

### API 密钥认证

```csharp
using Azure;
using Azure.AI.OpenAI;

AzureOpenAIClient client = new(
    new Uri(Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!));
```

### Microsoft Entra ID（生产环境推荐）

```csharp
using Azure.Identity;
using Azure.AI.OpenAI;

AzureOpenAIClient client = new(
    new Uri(Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!),
    new DefaultAzureCredential());
```

### 使用 OpenAI SDK 直接连接 Azure

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

ChatClient client = new(
    model: "gpt-4o-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE.openai.azure.com/openai/v1")
    });
```

## 聊天补全

### 基础聊天

```csharp
using Azure.AI.OpenAI;
using OpenAI.Chat;

AzureOpenAIClient azureClient = new(
    new Uri(endpoint),
    new DefaultAzureCredential());

ChatClient chatClient = azureClient.GetChatClient("gpt-4o-mini");

ChatCompletion completion = chatClient.CompleteChat(
[
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("What is Azure OpenAI?")
]);

Console.WriteLine(completion.Content[0].Text);
```

### 异步聊天

```csharp
ChatCompletion completion = await chatClient.CompleteChatAsync(
[
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("Explain cloud computing in simple terms.")
]);

Console.WriteLine($"Response: {completion.Content[0].Text}");
Console.WriteLine($"Tokens used: {completion.Usage.TotalTokenCount}");
```

### 流式聊天

```csharp
await foreach (StreamingChatCompletionUpdate update 
    in chatClient.CompleteChatStreamingAsync(messages))
{
    if (update.ContentUpdate.Count > 0)
    {
        Console.Write(update.ContentUpdate[0].Text);
    }
}
```

### 带选项的聊天

```csharp
ChatCompletionOptions options = new()
{
    MaxOutputTokenCount = 1000,
    Temperature = 0.7f,
    TopP = 0.95f,
    FrequencyPenalty = 0,
    PresencePenalty = 0
};

ChatCompletion completion = await chatClient.CompleteChatAsync(messages, options);
```

### 多轮对话

```csharp
List<ChatMessage> messages = new()
{
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("Hi, can you help me?"),
    new AssistantChatMessage("Of course! What do you need help with?"),
    new UserChatMessage("What's the capital of France?")
};

ChatCompletion completion = await chatClient.CompleteChatAsync(messages);
messages.Add(new AssistantChatMessage(completion.Content[0].Text));
```

## 结构化输出（JSON Schema）

```csharp
using System.Text.Json;

ChatCompletionOptions options = new()
{
    ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
        jsonSchemaFormatName: "math_reasoning",
        jsonSchema: BinaryData.FromBytes("""
            {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": { "type": "string" },
                                "output": { "type": "string" }
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": false
                        }
                    },
                    "final_answer": { "type": "string" }
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": false
            }
            """u8.ToArray()),
        jsonSchemaIsStrict: true)
};

ChatCompletion completion = await chatClient.CompleteChatAsync(
    [new UserChatMessage("How can I solve 8x + 7 = -23?")],
    options);

using JsonDocument json = JsonDocument.Parse(completion.Content[0].Text);
Console.WriteLine($"Answer: {json.RootElement.GetProperty("final_answer")}");
```

## 推理模型（o1、o4-mini）

```csharp
ChatCompletionOptions options = new()
{
    ReasoningEffortLevel = ChatReasoningEffortLevel.Low,
    MaxOutputTokenCount = 100000
};

ChatCompletion completion = await chatClient.CompleteChatAsync(
[
    new DeveloperChatMessage("You are a helpful assistant"),
    new UserChatMessage("Explain the theory of relativity")
], options);
```

## Azure AI Search 集成（RAG）

```csharp
using Azure.AI.OpenAI.Chat;

#pragma warning disable AOAI001

ChatCompletionOptions options = new();
options.AddDataSource(new AzureSearchChatDataSource()
{
    Endpoint = new Uri(searchEndpoint),
    IndexName = searchIndex,
    Authentication = DataSourceAuthentication.FromApiKey(searchKey)
});

ChatCompletion completion = await chatClient.CompleteChatAsync(
    [new UserChatMessage("What health plans are available?")],
    options);

ChatMessageContext context = completion.GetMessageContext();
if (context?.Intent is not null)
{
    Console.WriteLine($"Intent: {context.Intent}");
}
foreach (ChatCitation citation in context?.Citations ?? [])
{
    Console.WriteLine($"Citation: {citation.Content}");
}
```

## 嵌入

```csharp
using OpenAI.Embeddings;

EmbeddingClient embeddingClient = azureClient.GetEmbeddingClient("text-embedding-ada-002");

OpenAIEmbedding embedding = await embeddingClient.GenerateEmbeddingAsync("Hello, world!");
ReadOnlyMemory<float> vector = embedding.ToFloats();

Console.WriteLine($"Embedding dimensions: {vector.Length}");
```

### 批量嵌入

```csharp
List<string> inputs = new()
{
    "First document text",
    "Second document text",
    "Third document text"
};

OpenAIEmbeddingCollection embeddings = await embeddingClient.GenerateEmbeddingsAsync(inputs);

foreach (OpenAIEmbedding emb in embeddings)
{
    Console.WriteLine($"Index {emb.Index}: {emb.ToFloats().Length} dimensions");
}
```

## 图像生成（DALL-E）

```csharp
using OpenAI.Images;

ImageClient imageClient = azureClient.GetImageClient("dall-e-3");

GeneratedImage image = await imageClient.GenerateImageAsync(
    "A futuristic city skyline at sunset",
    new ImageGenerationOptions
    {
        Size = GeneratedImageSize.W1024xH1024,
        Quality = GeneratedImageQuality.High,
        Style = GeneratedImageStyle.Vivid
    });

Console.WriteLine($"Image URL: {image.ImageUri}");
```

## 音频（Whisper）

### 转录

```csharp
using OpenAI.Audio;

AudioClient audioClient = azureClient.GetAudioClient("whisper");

AudioTranscription transcription = await audioClient.TranscribeAudioAsync(
    "audio.mp3",
    new AudioTranscriptionOptions
    {
        ResponseFormat = AudioTranscriptionFormat.Verbose,
        Language = "en"
    });

Console.WriteLine(transcription.Text);
```

### 文本转语音

```csharp
BinaryData speech = await audioClient.GenerateSpeechAsync(
    "Hello, welcome to Azure OpenAI!",
    GeneratedSpeechVoice.Alloy,
    new SpeechGenerationOptions
    {
        SpeedRatio = 1.0f,
        ResponseFormat = GeneratedSpeechFormat.Mp3
    });

await File.WriteAllBytesAsync("output.mp3", speech.ToArray());
```

## 函数调用（工具）

```csharp
ChatTool getCurrentWeatherTool = ChatTool.CreateFunctionTool(
    functionName: "get_current_weather",
    functionDescription: "Get the current weather in a given location",
    functionParameters: BinaryData.FromString("""
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
        """));

ChatCompletionOptions options = new()
{
    Tools = { getCurrentWeatherTool }
};

ChatCompletion completion = await chatClient.CompleteChatAsync(
    [new UserChatMessage("What's the weather in Seattle?")],
    options);

if (completion.FinishReason == ChatFinishReason.ToolCalls)
{
    foreach (ChatToolCall toolCall in completion.ToolCalls)
    {
        Console.WriteLine($"Function: {toolCall.FunctionName}");
        Console.WriteLine($"Arguments: {toolCall.FunctionArguments}");
    }
}
```

## 核心类型参考

| 类型 | 用途 |
|------|------|
| `AzureOpenAIClient` | Azure OpenAI 顶层客户端 |
| `ChatClient` | 聊天补全 |
| `EmbeddingClient` | 文本嵌入 |
| `ImageClient` | 图像生成（DALL-E） |
| `AudioClient` | 音频转录/文本转语音 |
| `ChatCompletion` | 聊天响应 |
| `ChatCompletionOptions` | 请求配置 |
| `StreamingChatCompletionUpdate` | 流式响应块 |
| `ChatMessage` | 基础消息类型 |
| `SystemChatMessage` | 系统提示词 |
| `UserChatMessage` | 用户输入 |
| `AssistantChatMessage` | 助手响应 |
| `DeveloperChatMessage` | 开发者消息（推理模型） |
| `ChatTool` | 函数/工具定义 |
| `ChatToolCall` | 工具调用请求 |

## 最佳实践

1. **生产环境使用 Entra ID** — 避免使用 API 密钥；使用 `DefaultAzureCredential`
2. **复用客户端实例** — 创建一次，跨请求共享
3. **处理速率限制** — 对 429 错误实现指数退避
4. **长响应使用流式传输** — 使用 `CompleteChatStreamingAsync` 获得更好的用户体验
5. **设置适当的超时** — 长时间补全可能需要延长超时时间
6. **使用结构化输出** — JSON Schema 确保响应格式一致
7. **监控 Token 使用量** — 跟踪 `completion.Usage` 进行成本管理
8. **验证工具调用** — 执行前始终验证函数参数

## 错误处理

```csharp
using Azure;

try
{
    ChatCompletion completion = await chatClient.CompleteChatAsync(messages);
}
catch (RequestFailedException ex) when (ex.Status == 429)
{
    Console.WriteLine("Rate limited. Retry after delay.");
    await Task.Delay(TimeSpan.FromSeconds(10));
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Bad request: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Azure OpenAI error: {ex.Status} - {ex.Message}");
}
```

## 相关 SDK

| SDK | 用途 | 安装命令 |
|-----|------|---------|
| `Azure.AI.OpenAI` | Azure OpenAI 客户端（本 SDK） | `dotnet add package Azure.AI.OpenAI` |
| `OpenAI` | OpenAI 兼容 | `dotnet add package OpenAI` |
| `Azure.Identity` | 身份验证 | `dotnet add package Azure.Identity` |
| `Azure.Search.Documents` | AI Search（用于 RAG） | `dotnet add package Azure.Search.Documents` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.AI.OpenAI |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.ai.openai |
| 迁移指南（1.0→2.0） | https://learn.microsoft.com/azure/ai-services/openai/how-to/dotnet-migration |
| 快速入门 | https://learn.microsoft.com/azure/ai-services/openai/quickstart |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
