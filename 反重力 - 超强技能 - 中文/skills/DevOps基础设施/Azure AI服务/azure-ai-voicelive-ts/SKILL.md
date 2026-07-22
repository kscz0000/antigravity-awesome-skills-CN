---
name: azure-ai-voicelive-ts
description: Azure AI Voice Live SDK for JavaScript/TypeScript。使用双向 WebSocket 通信构建实时语音 AI 应用。触发词：Azure Voice Live、实时语音AI、语音助手、WebSocket语音、Azure语音SDK、VoiceLiveClient、语音对话、实时音频流、双向语音通信、Node.js语音、浏览器语音AI
risk: unknown
source: community
date_added: '2026-02-27'
---

# @azure/ai-voicelive (JavaScript/TypeScript)

实时语音 AI SDK，用于在 Node.js 和浏览器环境中使用 Azure AI 构建双向语音助手。

## 安装

```bash
npm install @azure/ai-voicelive @azure/identity
# TypeScript 用户
npm install @types/node
```

**当前版本**: 1.0.0-beta.3

**支持的环境**:
- Node.js LTS 版本 (20+)
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

## 环境变量

```bash
AZURE_VOICELIVE_ENDPOINT=https://<resource>.cognitiveservices.azure.com
# 可选：如果不使用 Entra ID 则需要 API 密钥
AZURE_VOICELIVE_API_KEY=<your-api-key>
# 可选：日志
AZURE_LOG_LEVEL=info
```

## 身份验证

### Microsoft Entra ID（推荐）

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { VoiceLiveClient } from "@azure/ai-voicelive";

const credential = new DefaultAzureCredential();
const endpoint = "https://your-resource.cognitiveservices.azure.com";

const client = new VoiceLiveClient(endpoint, credential);
```

### API 密钥

```typescript
import { AzureKeyCredential } from "@azure/core-auth";
import { VoiceLiveClient } from "@azure/ai-voicelive";

const endpoint = "https://your-resource.cognitiveservices.azure.com";
const credential = new AzureKeyCredential("your-api-key");

const client = new VoiceLiveClient(endpoint, credential);
```

## 客户端层级结构

```
VoiceLiveClient
└── VoiceLiveSession (WebSocket 连接)
    ├── updateSession()      → 配置会话选项
    ├── subscribe()          → 事件处理器（Azure SDK 模式）
    ├── sendAudio()          → 流式音频输入
    ├── addConversationItem() → 添加消息/函数输出
    └── sendEvent()          → 发送原始协议事件
```

## 快速开始

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { VoiceLiveClient } from "@azure/ai-voicelive";

const credential = new DefaultAzureCredential();
const endpoint = process.env.AZURE_VOICELIVE_ENDPOINT!;

// 创建客户端并启动会话
const client = new VoiceLiveClient(endpoint, credential);
const session = await client.startSession("gpt-4o-mini-realtime-preview");

// 配置会话
await session.updateSession({
  modalities: ["text", "audio"],
  instructions: "You are a helpful AI assistant. Respond naturally.",
  voice: {
    type: "azure-standard",
    name: "en-US-AvaNeural",
  },
  turnDetection: {
    type: "server_vad",
    threshold: 0.5,
    prefixPaddingMs: 300,
    silenceDurationMs: 500,
  },
  inputAudioFormat: "pcm16",
  outputAudioFormat: "pcm16",
});

// 订阅事件
const subscription = session.subscribe({
  onResponseAudioDelta: async (event, context) => {
    // 处理流式音频输出
    const audioData = event.delta;
    playAudioChunk(audioData);
  },
  onResponseTextDelta: async (event, context) => {
    // 处理流式文本
    process.stdout.write(event.delta);
  },
  onInputAudioTranscriptionCompleted: async (event, context) => {
    console.log("User said:", event.transcript);
  },
});

// 从麦克风发送音频
function sendAudioChunk(audioBuffer: ArrayBuffer) {
  session.sendAudio(audioBuffer);
}
```

## 会话配置

```typescript
await session.updateSession({
  // 模态
  modalities: ["audio", "text"],
  
  // 系统指令
  instructions: "You are a customer service representative.",
  
  // 语音选择
  voice: {
    type: "azure-standard",  // 或 "azure-custom", "openai"
    name: "en-US-AvaNeural",
  },
  
  // 轮次检测 (VAD)
  turnDetection: {
    type: "server_vad",      // 或 "azure_semantic_vad"
    threshold: 0.5,
    prefixPaddingMs: 300,
    silenceDurationMs: 500,
  },
  
  // 音频格式
  inputAudioFormat: "pcm16",
  outputAudioFormat: "pcm16",
  
  // 工具（函数调用）
  tools: [
    {
      type: "function",
      name: "get_weather",
      description: "Get current weather",
      parameters: {
        type: "object",
        properties: {
          location: { type: "string" }
        },
        required: ["location"]
      }
    }
  ],
  toolChoice: "auto",
});
```

## 事件处理（Azure SDK 模式）

SDK 使用基于订阅的事件处理模式：

```typescript
const subscription = session.subscribe({
  // 连接生命周期
  onConnected: async (args, context) => {
    console.log("Connected:", args.connectionId);
  },
  onDisconnected: async (args, context) => {
    console.log("Disconnected:", args.code, args.reason);
  },
  onError: async (args, context) => {
    console.error("Error:", args.error.message);
  },
  
  // 会话事件
  onSessionCreated: async (event, context) => {
    console.log("Session created:", context.sessionId);
  },
  onSessionUpdated: async (event, context) => {
    console.log("Session updated");
  },
  
  // 音频输入事件 (VAD)
  onInputAudioBufferSpeechStarted: async (event, context) => {
    console.log("Speech started at:", event.audioStartMs);
  },
  onInputAudioBufferSpeechStopped: async (event, context) => {
    console.log("Speech stopped at:", event.audioEndMs);
  },
  
  // 转录事件
  onConversationItemInputAudioTranscriptionCompleted: async (event, context) => {
    console.log("User said:", event.transcript);
  },
  onConversationItemInputAudioTranscriptionDelta: async (event, context) => {
    process.stdout.write(event.delta);
  },
  
  // 响应事件
  onResponseCreated: async (event, context) => {
    console.log("Response started");
  },
  onResponseDone: async (event, context) => {
    console.log("Response complete");
  },
  
  // 流式文本
  onResponseTextDelta: async (event, context) => {
    process.stdout.write(event.delta);
  },
  onResponseTextDone: async (event, context) => {
    console.log("\n--- Text complete ---");
  },
  
  // 流式音频
  onResponseAudioDelta: async (event, context) => {
    const audioData = event.delta;
    playAudioChunk(audioData);
  },
  onResponseAudioDone: async (event, context) => {
    console.log("Audio complete");
  },
  
  // 音频转录（助手说的话）
  onResponseAudioTranscriptDelta: async (event, context) => {
    process.stdout.write(event.delta);
  },
  
  // 函数调用
  onResponseFunctionCallArgumentsDone: async (event, context) => {
    if (event.name === "get_weather") {
      const args = JSON.parse(event.arguments);
      const result = await getWeather(args.location);
      
      await session.addConversationItem({
        type: "function_call_output",
        callId: event.callId,
        output: JSON.stringify(result),
      });
      
      await session.sendEvent({ type: "response.create" });
    }
  },
  
  // 调试用的通用处理器
  onServerEvent: async (event, context) => {
    console.log("Event:", event.type);
  },
});

// 完成后清理
await subscription.close();
```

## 函数调用

```typescript
// 在会话配置中定义工具
await session.updateSession({
  modalities: ["audio", "text"],
  instructions: "Help users with weather information.",
  tools: [
    {
      type: "function",
      name: "get_weather",
      description: "Get current weather for a location",
      parameters: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "City and state or country",
          },
        },
        required: ["location"],
      },
    },
  ],
  toolChoice: "auto",
});

// 处理函数调用
const subscription = session.subscribe({
  onResponseFunctionCallArgumentsDone: async (event, context) => {
    if (event.name === "get_weather") {
      const args = JSON.parse(event.arguments);
      const weatherData = await fetchWeather(args.location);
      
      // 发送函数结果
      await session.addConversationItem({
        type: "function_call_output",
        callId: event.callId,
        output: JSON.stringify(weatherData),
      });
      
      // 触发响应生成
      await session.sendEvent({ type: "response.create" });
    }
  },
});
```

## 语音选项

| 语音类型 | 配置 | 示例 |
|------------|--------|---------|
| Azure 标准语音 | `{ type: "azure-standard", name: "..." }` | `"en-US-AvaNeural"` |
| Azure 自定义语音 | `{ type: "azure-custom", name: "...", endpointId: "..." }` | 自定义语音端点 |
| Azure 个人语音 | `{ type: "azure-personal", speakerProfileId: "..." }` | 个人语音克隆 |
| OpenAI | `{ type: "openai", name: "..." }` | `"alloy"`, `"echo"`, `"shimmer"` |

## 支持的模型

| 模型 | 描述 | 使用场景 |
|-------|-------------|----------|
| `gpt-4o-realtime-preview` | GPT-4o 实时音频 | 高质量对话 AI |
| `gpt-4o-mini-realtime-preview` | 轻量级 GPT-4o | 快速、高效的交互 |
| `phi4-mm-realtime` | Phi 多模态 | 成本效益型应用 |

## 轮次检测选项

```typescript
// 服务端 VAD（默认）
turnDetection: {
  type: "server_vad",
  threshold: 0.5,
  prefixPaddingMs: 300,
  silenceDurationMs: 500,
}

// Azure 语义 VAD（更智能的检测）
turnDetection: {
  type: "azure_semantic_vad",
}

// Azure 语义 VAD（英语优化）
turnDetection: {
  type: "azure_semantic_vad_en",
}

// Azure 语义 VAD（多语言）
turnDetection: {
  type: "azure_semantic_vad_multilingual",
}
```

## 音频格式

| 格式 | 采样率 | 使用场景 |
|--------|-------------|----------|
| `pcm16` | 24kHz | 默认，高质量 |
| `pcm16-8000hz` | 8kHz | 电话通信 |
| `pcm16-16000hz` | 16kHz | 语音助手 |
| `g711_ulaw` | 8kHz | 电话通信（美国） |
| `g711_alaw` | 8kHz | 电话通信（欧洲） |

## 核心类型参考

| 类型 | 用途 |
|------|---------|
| `VoiceLiveClient` | 创建会话的主客户端 |
| `VoiceLiveSession` | 活跃的 WebSocket 会话 |
| `VoiceLiveSessionHandlers` | 事件处理器接口 |
| `VoiceLiveSubscription` | 活跃的事件订阅 |
| `ConnectionContext` | 连接事件的上下文 |
| `SessionContext` | 会话事件的上下文 |
| `ServerEventUnion` | 所有服务端事件的联合类型 |

## 错误处理

```typescript
import {
  VoiceLiveError,
  VoiceLiveConnectionError,
  VoiceLiveAuthenticationError,
  VoiceLiveProtocolError,
} from "@azure/ai-voicelive";

const subscription = session.subscribe({
  onError: async (args, context) => {
    const { error } = args;
    
    if (error instanceof VoiceLiveConnectionError) {
      console.error("Connection error:", error.message);
    } else if (error instanceof VoiceLiveAuthenticationError) {
      console.error("Auth error:", error.message);
    } else if (error instanceof VoiceLiveProtocolError) {
      console.error("Protocol error:", error.message);
    }
  },
  
  onServerError: async (event, context) => {
    console.error("Server error:", event.error?.message);
  },
});
```

## 日志

```typescript
import { setLogLevel } from "@azure/logger";

// 启用详细日志
setLogLevel("info");

// 或通过环境变量
// AZURE_LOG_LEVEL=info
```

## 浏览器使用

```typescript
// 浏览器需要打包工具（Vite、webpack 等）
import { VoiceLiveClient } from "@azure/ai-voicelive";
import { InteractiveBrowserCredential } from "@azure/identity";

// 使用浏览器兼容的凭据
const credential = new InteractiveBrowserCredential({
  clientId: "your-client-id",
  tenantId: "your-tenant-id",
});

const client = new VoiceLiveClient(endpoint, credential);

// 请求麦克风访问权限
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
const audioContext = new AudioContext({ sampleRate: 24000 });

// 处理音频并发送到会话
// ...（完整实现请参见示例）
```

## 最佳实践

1. **始终使用 `DefaultAzureCredential`** — 永远不要硬编码 API 密钥
2. **设置两种模态** — 语音助手应包含 `["text", "audio"]`
3. **使用 Azure 语义 VAD** — 比基础服务端 VAD 有更好的轮次检测
4. **处理所有错误类型** — 连接、认证和协议错误
5. **清理订阅** — 完成后调用 `subscription.close()`
6. **使用合适的音频格式** — PCM16 24kHz 提供最佳质量

## 参考链接

| 资源 | URL |
|----------|-----|
| npm 包 | https://www.npmjs.com/package/@azure/ai-voicelive |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-voicelive |
| 示例 | https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-voicelive/samples |
| API 参考 | https://learn.microsoft.com/javascript/api/@azure/ai-voicelive |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
