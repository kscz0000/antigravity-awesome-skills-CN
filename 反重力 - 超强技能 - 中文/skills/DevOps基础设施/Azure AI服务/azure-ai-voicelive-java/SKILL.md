---
name: azure-ai-voicelive-java
description: Azure AI VoiceLive Java SDK。使用 WebSocket 技术实现与 AI 助手的实时双向语音对话。触发词：Azure VoiceLive、Java 语音对话、实时语音 SDK、WebSocket 语音、AI 语音助手、双向语音通信、Azure 语音服务、VoiceLiveAsyncClient
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI VoiceLive SDK for Java

使用 WebSocket 技术实现与 AI 助手的实时双向语音对话。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-voicelive</artifactId>
    <version>1.0.0-beta.2</version>
</dependency>
```

## 环境变量

```bash
AZURE_VOICELIVE_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_VOICELIVE_API_KEY=<your-api-key>
```

## 身份验证

### API 密钥

```java
import com.azure.ai.voicelive.VoiceLiveAsyncClient;
import com.azure.ai.voicelive.VoiceLiveClientBuilder;
import com.azure.core.credential.AzureKeyCredential;

VoiceLiveAsyncClient client = new VoiceLiveClientBuilder()
    .endpoint(System.getenv("AZURE_VOICELIVE_ENDPOINT"))
    .credential(new AzureKeyCredential(System.getenv("AZURE_VOICELIVE_API_KEY")))
    .buildAsyncClient();
```

### DefaultAzureCredential（推荐）

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

VoiceLiveAsyncClient client = new VoiceLiveClientBuilder()
    .endpoint(System.getenv("AZURE_VOICELIVE_ENDPOINT"))
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

## 核心概念

| 概念 | 描述 |
|------|------|
| `VoiceLiveAsyncClient` | 语音会话的主入口点 |
| `VoiceLiveSessionAsyncClient` | 用于流式传输的活动 WebSocket 连接 |
| `VoiceLiveSessionOptions` | 会话行为配置 |

### 音频要求

- **采样率**：24kHz（24000 Hz）
- **位深度**：16-bit PCM
- **声道**：单声道（1 channel）
- **格式**：有符号 PCM，小端序

## 核心工作流程

### 1. 启动会话

```java
import reactor.core.publisher.Mono;

client.startSession("gpt-4o-realtime-preview")
    .flatMap(session -> {
        System.out.println("Session started");
        
        // 订阅事件
        session.receiveEvents()
            .subscribe(
                event -> System.out.println("Event: " + event.getType()),
                error -> System.err.println("Error: " + error.getMessage())
            );
        
        return Mono.just(session);
    })
    .block();
```

### 2. 配置会话选项

```java
import com.azure.ai.voicelive.models.*;
import java.util.Arrays;

ServerVadTurnDetection turnDetection = new ServerVadTurnDetection()
    .setThreshold(0.5)                    // 灵敏度 (0.0-1.0)
    .setPrefixPaddingMs(300)              // 语音前的音频
    .setSilenceDurationMs(500)            // 结束轮次的静音时长
    .setInterruptResponse(true)           // 允许打断
    .setAutoTruncate(true)
    .setCreateResponse(true);

AudioInputTranscriptionOptions transcription = new AudioInputTranscriptionOptions(
    AudioInputTranscriptionOptionsModel.WHISPER_1);

VoiceLiveSessionOptions options = new VoiceLiveSessionOptions()
    .setInstructions("You are a helpful AI voice assistant.")
    .setVoice(BinaryData.fromObject(new OpenAIVoice(OpenAIVoiceName.ALLOY)))
    .setModalities(Arrays.asList(InteractionModality.TEXT, InteractionModality.AUDIO))
    .setInputAudioFormat(InputAudioFormat.PCM16)
    .setOutputAudioFormat(OutputAudioFormat.PCM16)
    .setInputAudioSamplingRate(24000)
    .setInputAudioNoiseReduction(new AudioNoiseReduction(AudioNoiseReductionType.NEAR_FIELD))
    .setInputAudioEchoCancellation(new AudioEchoCancellation())
    .setInputAudioTranscription(transcription)
    .setTurnDetection(turnDetection);

// 发送配置
ClientEventSessionUpdate updateEvent = new ClientEventSessionUpdate(options);
session.sendEvent(updateEvent).subscribe();
```

### 3. 发送音频输入

```java
byte[] audioData = readAudioChunk(); // 你的 PCM16 音频数据
session.sendInputAudio(BinaryData.fromBytes(audioData)).subscribe();
```

### 4. 处理事件

```java
session.receiveEvents().subscribe(event -> {
    ServerEventType eventType = event.getType();
    
    if (ServerEventType.SESSION_CREATED.equals(eventType)) {
        System.out.println("Session created");
    } else if (ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED.equals(eventType)) {
        System.out.println("User started speaking");
    } else if (ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED.equals(eventType)) {
        System.out.println("User stopped speaking");
    } else if (ServerEventType.RESPONSE_AUDIO_DELTA.equals(eventType)) {
        if (event instanceof SessionUpdateResponseAudioDelta) {
            SessionUpdateResponseAudioDelta audioEvent = (SessionUpdateResponseAudioDelta) event;
            playAudioChunk(audioEvent.getDelta());
        }
    } else if (ServerEventType.RESPONSE_DONE.equals(eventType)) {
        System.out.println("Response complete");
    } else if (ServerEventType.ERROR.equals(eventType)) {
        if (event instanceof SessionUpdateError) {
            SessionUpdateError errorEvent = (SessionUpdateError) event;
            System.err.println("Error: " + errorEvent.getError().getMessage());
        }
    }
});
```

## 语音配置

### OpenAI 语音

```java
// 可用选项：ALLOY, ASH, BALLAD, CORAL, ECHO, SAGE, SHIMMER, VERSE
VoiceLiveSessionOptions options = new VoiceLiveSessionOptions()
    .setVoice(BinaryData.fromObject(new OpenAIVoice(OpenAIVoiceName.ALLOY)));
```

### Azure 语音

```java
// Azure 标准语音
options.setVoice(BinaryData.fromObject(new AzureStandardVoice("en-US-JennyNeural")));

// Azure 自定义语音
options.setVoice(BinaryData.fromObject(new AzureCustomVoice("myVoice", "endpointId")));

// Azure 个人语音
options.setVoice(BinaryData.fromObject(
    new AzurePersonalVoice("speakerProfileId", PersonalVoiceModels.PHOENIX_LATEST_NEURAL)));
```

## 函数调用

```java
VoiceLiveFunctionDefinition weatherFunction = new VoiceLiveFunctionDefinition("get_weather")
    .setDescription("Get current weather for a location")
    .setParameters(BinaryData.fromObject(parametersSchema));

VoiceLiveSessionOptions options = new VoiceLiveSessionOptions()
    .setTools(Arrays.asList(weatherFunction))
    .setInstructions("You have access to weather information.");
```

## 最佳实践

1. **使用异步客户端** — VoiceLive 需要响应式模式
2. **配置轮次检测** — 实现自然的对话流程
3. **启用降噪** — 提升语音识别效果
4. **优雅处理打断** — 使用 `setInterruptResponse(true)`
5. **使用 Whisper 转录** — 对输入音频进行转录
6. **正确关闭会话** — 对话结束时妥善关闭

## 错误处理

```java
session.receiveEvents()
    .doOnError(error -> System.err.println("Connection error: " + error.getMessage()))
    .onErrorResume(error -> {
        // 尝试重连或清理
        return Flux.empty();
    })
    .subscribe();
```

## 参考链接

| 资源 | URL |
|------|-----|
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-voicelive |
| 示例代码 | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-voicelive/src/samples |

## 使用场景
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不能替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
