---
name: azure-ai-voicelive-dotnet
description: Azure AI Voice Live .NET SDK。用于构建实时语音AI应用，支持双向WebSocket通信。触发词：Azure语音实时、Voice Live、实时语音AI、双向语音通信、WebSocket语音、.NET语音助手、语音助手开发、实时对话AI。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.AI.VoiceLive (.NET)

用于构建双向语音助手的实时语音AI SDK，基于Azure AI。

## 安装

```bash
dotnet add package Azure.AI.VoiceLive
dotnet add package Azure.Identity
dotnet add package NAudio                    # 用于音频捕获/播放
```

**当前版本**：稳定版 v1.0.0，预览版 v1.1.0-beta.1

## 环境变量

```bash
AZURE_VOICELIVE_ENDPOINT=https://<resource>.services.ai.azure.com/
AZURE_VOICELIVE_MODEL=gpt-4o-realtime-preview
AZURE_VOICELIVE_VOICE=en-US-AvaNeural
# 可选：如果不使用Entra ID则使用API密钥
AZURE_VOICELIVE_API_KEY=<your-api-key>
```

## 身份验证

### Microsoft Entra ID（推荐）

```csharp
using Azure.Identity;
using Azure.AI.VoiceLive;

Uri endpoint = new Uri("https://your-resource.cognitiveservices.azure.com");
DefaultAzureCredential credential = new DefaultAzureCredential();
VoiceLiveClient client = new VoiceLiveClient(endpoint, credential);
```

**所需角色**：`Cognitive Services User`（在Azure门户 → 访问控制中分配）

### API密钥

```csharp
Uri endpoint = new Uri("https://your-resource.cognitiveservices.azure.com");
AzureKeyCredential credential = new AzureKeyCredential("your-api-key");
VoiceLiveClient client = new VoiceLiveClient(endpoint, credential);
```

## 客户端层次结构

```
VoiceLiveClient
└── VoiceLiveSession (WebSocket连接)
    ├── ConfigureSessionAsync()
    ├── GetUpdatesAsync() → SessionUpdate事件
    ├── AddItemAsync() → UserMessageItem, FunctionCallOutputItem
    ├── SendAudioAsync()
    └── StartResponseAsync()
```

## 核心工作流程

### 1. 启动会话并配置

```csharp
using Azure.Identity;
using Azure.AI.VoiceLive;

var endpoint = new Uri(Environment.GetEnvironmentVariable("AZURE_VOICELIVE_ENDPOINT"));
var client = new VoiceLiveClient(endpoint, new DefaultAzureCredential());

var model = "gpt-4o-mini-realtime-preview";

// 启动会话
using VoiceLiveSession session = await client.StartSessionAsync(model);

// 配置会话
VoiceLiveSessionOptions sessionOptions = new()
{
    Model = model,
    Instructions = "You are a helpful AI assistant. Respond naturally.",
    Voice = new AzureStandardVoice("en-US-AvaNeural"),
    TurnDetection = new AzureSemanticVadTurnDetection()
    {
        Threshold = 0.5f,
        PrefixPadding = TimeSpan.FromMilliseconds(300),
        SilenceDuration = TimeSpan.FromMilliseconds(500)
    },
    InputAudioFormat = InputAudioFormat.Pcm16,
    OutputAudioFormat = OutputAudioFormat.Pcm16
};

// 设置模态（语音助手同时支持文本和音频）
sessionOptions.Modalities.Clear();
sessionOptions.Modalities.Add(InteractionModality.Text);
sessionOptions.Modalities.Add(InteractionModality.Audio);

await session.ConfigureSessionAsync(sessionOptions);
```

### 2. 处理事件

```csharp
await foreach (SessionUpdate serverEvent in session.GetUpdatesAsync())
{
    switch (serverEvent)
    {
        case SessionUpdateResponseAudioDelta audioDelta:
            byte[] audioData = audioDelta.Delta.ToArray();
            // 通过NAudio或其他音频库播放音频
            break;
            
        case SessionUpdateResponseTextDelta textDelta:
            Console.Write(textDelta.Delta);
            break;
            
        case SessionUpdateResponseFunctionCallArgumentsDone functionCall:
            // 处理函数调用（参见函数调用部分）
            break;
            
        case SessionUpdateError error:
            Console.WriteLine($"Error: {error.Error.Message}");
            break;
            
        case SessionUpdateResponseDone:
            Console.WriteLine("\n--- 响应完成 ---");
            break;
    }
}
```

### 3. 发送用户消息

```csharp
await session.AddItemAsync(new UserMessageItem("Hello, can you help me?"));
await session.StartResponseAsync();
```

### 4. 函数调用

```csharp
// 定义函数
var weatherFunction = new VoiceLiveFunctionDefinition("get_current_weather")
{
    Description = "Get the current weather for a given location",
    Parameters = BinaryData.FromString("""
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state or country"
                }
            },
            "required": ["location"]
        }
        """)
};

// 添加到会话选项
sessionOptions.Tools.Add(weatherFunction);

// 在事件循环中处理函数调用
if (serverEvent is SessionUpdateResponseFunctionCallArgumentsDone functionCall)
{
    if (functionCall.Name == "get_current_weather")
    {
        var parameters = JsonSerializer.Deserialize<Dictionary<string, string>>(functionCall.Arguments);
        string location = parameters?["location"] ?? "";
        
        // 调用外部服务
        string weatherInfo = $"The weather in {location} is sunny, 75°F.";
        
        // 发送响应
        await session.AddItemAsync(new FunctionCallOutputItem(functionCall.CallId, weatherInfo));
        await session.StartResponseAsync();
    }
}
```

## 语音选项

| 语音类型 | 类 | 示例 |
|------------|-------|---------|
| Azure标准 | `AzureStandardVoice` | `"en-US-AvaNeural"` |
| Azure HD | `AzureStandardVoice` | `"en-US-Ava:DragonHDLatestNeural"` |
| Azure自定义 | `AzureCustomVoice` | 带端点ID的自定义语音 |

## 支持的模型

| 模型 | 描述 |
|-------|-------------|
| `gpt-4o-realtime-preview` | 支持实时音频的GPT-4o |
| `gpt-4o-mini-realtime-preview` | 轻量级，快速交互 |
| `phi4-mm-realtime` | 高性价比多模态 |

## 关键类型参考

| 类型 | 用途 |
|------|---------|
| `VoiceLiveClient` | 创建会话的主客户端 |
| `VoiceLiveSession` | 活跃的WebSocket会话 |
| `VoiceLiveSessionOptions` | 会话配置 |
| `AzureStandardVoice` | 标准Azure语音提供者 |
| `AzureSemanticVadTurnDetection` | 语音活动检测 |
| `VoiceLiveFunctionDefinition` | 函数工具定义 |
| `UserMessageItem` | 用户文本消息 |
| `FunctionCallOutputItem` | 函数调用响应 |
| `SessionUpdateResponseAudioDelta` | 音频块事件 |
| `SessionUpdateResponseTextDelta` | 文本块事件 |

## 最佳实践

1. **始终设置两种模态** — 语音助手需包含`Text`和`Audio`
2. **使用`AzureSemanticVadTurnDetection`** — 提供自然的对话流程
3. **配置合适的静默时长** — 通常500ms可避免过早截断
4. **使用`using`语句** — 确保正确释放会话资源
5. **处理所有事件类型** — 检查错误、音频、文本和函数调用
6. **使用DefaultAzureCredential** — 切勿硬编码API密钥

## 错误处理

```csharp
if (serverEvent is SessionUpdateError error)
{
    if (error.Error.Message.Contains("Cancellation failed: no active response"))
    {
        // 良性错误，可忽略
    }
    else
    {
        Console.WriteLine($"Error: {error.Error.Message}");
    }
}
```

## 音频配置

- **输入格式**：`InputAudioFormat.Pcm16`（16位PCM）
- **输出格式**：`OutputAudioFormat.Pcm16`
- **采样率**：推荐24kHz
- **声道**：单声道

## 相关SDK

| SDK | 用途 | 安装命令 |
|-----|---------|---------|
| `Azure.AI.VoiceLive` | 实时语音（本SDK） | `dotnet add package Azure.AI.VoiceLive` |
| `Microsoft.CognitiveServices.Speech` | 语音转文本、文本转语音 | `dotnet add package Microsoft.CognitiveServices.Speech` |
| `NAudio` | 音频捕获/播放 | `dotnet add package NAudio` |

## 参考链接

| 资源 | URL |
|----------|-----|
| NuGet包 | https://www.nuget.org/packages/Azure.AI.VoiceLive |
| API参考 | https://learn.microsoft.com/dotnet/api/azure.ai.voicelive |
| GitHub源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.VoiceLive |
| 快速入门 | https://learn.microsoft.com/azure/ai-services/speech-service/voice-live-quickstart |

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不应替代特定环境的验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
