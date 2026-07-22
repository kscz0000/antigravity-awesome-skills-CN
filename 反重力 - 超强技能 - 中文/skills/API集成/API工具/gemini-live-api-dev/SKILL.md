---
name: gemini-live-api-dev
description: 使用本技能构建基于 Gemini Live API 的实时双向流式应用。涵盖基于 WebSocket 的音频/视频/文本流传输、语音活动检测 (VAD)、原生音频特性、函数调用、会话管理、用于客户端认证的临时令牌等。触发词：Live API、实时语音、实时视频、WebSocket 音频流、VAD、临时令牌、会话恢复、Google Search 接入。
risk: unknown
source: https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-live-api-dev
source_repo: google-gemini/gemini-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/google-gemini/gemini-skills/blob/main/LICENSE
---

# Gemini Live API 开发技能
## 适用场景

使用本技能构建基于 Gemini Live API 的实时双向流式应用。涵盖基于 WebSocket 的音频/视频/文本流传输、语音活动检测 (VAD)、原生音频特性、函数调用、会话管理、用于客户端认证的临时令牌等。


## 概述

Live API 支持通过 WebSocket 与 Gemini 进行**低延迟、实时的语音和视频交互**。它持续处理音频、视频或文本流，并即时返回类人的语音回复。

核心能力：
- **双向音频流传输** — 实时麦克风到扬声器对话
- **视频流传输** — 在音频之外同时发送摄像头/屏幕帧
- **文本输入/输出** — 在实时会话中发送和接收文本
- **音频转写** — 获取输入和输出音频的文本转写
- **语音活动检测 (VAD)** — 自动打断处理
- **原生音频** — 思考能力（可通过 `thinkingLevel` 配置）
- **函数调用** — 同步工具调用
- **Google Search 接入** — 基于实时搜索结果生成回复
- **会话管理** — 上下文压缩、会话恢复、GoAway 信号
- **临时令牌** — 安全的客户端认证

> [!NOTE]
> Live API 目前**仅支持 WebSocket**。如需 WebRTC 支持或更简化的集成，请使用 [合作伙伴集成](#partner-integrations)。

## 模型

- `gemini-3.1-flash-live-preview` — 针对低延迟、实时对话进行了优化。支持原生音频输出、思考能力（通过 `thinkingLevel`）。128k 上下文窗口。**推荐用于所有 Live API 场景。**
- `gemini-3.5-live-translate-preview` — 实时流式翻译模型。

> [!WARNING]
> 以下 Live API 模型**已弃用**，将被下线。请迁移到 `gemini-3.1-flash-live-preview`。
> - `gemini-2.5-flash-native-audio-preview-12-2025` — 迁移到 `gemini-3.1-flash-live-preview`。
> - `gemini-live-2.5-flash-preview` — 发布于 2025 年 6 月 17 日。下线时间：2025 年 12 月 9 日。
> - `gemini-2.0-flash-live-001` — 发布于 2025 年 4 月 9 日。下线时间：2025 年 12 月 9 日。

## SDK

- **Python**：`google-genai` — `pip install google-genai`
- **JavaScript/TypeScript**：`@google/genai` — `npm install @google/genai`

> [!WARNING]
> 旧版 SDK `google-generativeai`（Python）和 `@google/generative-ai`（JS）已弃用。请使用上面的新 SDK。

## 合作伙伴集成

为简化实时音视频应用开发，可使用支持通过 **WebRTC** 或 **WebSocket** 接入 Gemini Live API 的第三方集成：

- [LiveKit](https://docs.livekit.io/agents/models/realtime/plugins/gemini/) — 将 Gemini Live API 与 LiveKit Agents 结合使用。
- [Pipecat by Daily](https://docs.pipecat.ai/guides/features/gemini-live) — 使用 Gemini Live 和 Pipecat 创建实时 AI 聊天机器人。
- [Fishjam by Software Mansion](https://docs.fishjam.io/tutorials/gemini-live-integration) — 使用 Fishjam 创建实时音视频流应用。
- [Vision Agents by Stream](https://visionagents.ai/integrations/gemini) — 使用 Vision Agents 构建实时语音和视频 AI 应用。
- [Voximplant](https://voximplant.com/products/gemini-client) — 通过 Voximplant 将呼入和呼出电话接入 Live API。
- [Firebase AI SDK](https://firebase.google.com/docs/ai-logic/live-api?api=dev) — 使用 Firebase AI Logic 快速上手 Gemini Live API。

## 音频格式

- **输入**：原始 PCM，小端序，16 位，单声道。原生采样率 16kHz（其他采样率将被重采样）。MIME 类型：`audio/pcm;rate=16000`
- **输出**：原始 PCM，小端序，16 位，单声道。采样率 24kHz。

> [!IMPORTANT]
> 所有的实时用户输入（音频、视频**以及文本**）请使用 `send_realtime_input` / `sendRealtimeInput`。`send_client_content` / `sendClientContent` **仅**用于植入初始的上下文历史（需要在 `history_config` 中设置 `initial_history_in_client_content`）。**不要**用它来在对话过程中发送新的用户消息。

> [!WARNING]
> 在 `sendRealtimeInput` 中**不要**使用 `media` 字段。请使用具体的键：`audio` 表示音频数据，`video` 表示图像/视频帧，`text` 表示文本输入。

---

## 快速开始

### 认证

#### Python

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
```

#### JavaScript

```js
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({ apiKey: 'YOUR_API_KEY' });
```

### 连接到 Live API

#### Python
```python
from google.genai import types

config = types.LiveConnectConfig(
    response_modalities=[types.Modality.AUDIO],
    system_instruction=types.Content(
        parts=[types.Part(text="You are a helpful assistant.")]
    )
)

async with client.aio.live.connect(model="gemini-3.1-flash-live-preview", config=config) as session:
    pass  # Session is active
```

#### JavaScript
```js
const session = await ai.live.connect({
  model: 'gemini-3.1-flash-live-preview',
  config: {
    responseModalities: ['audio'],
    systemInstruction: { parts: [{ text: 'You are a helpful assistant.' }] }
  },
  callbacks: {
    onopen: () => console.log('Connected'),
    onmessage: (response) => console.log('Message:', response),
    onerror: (error) => console.error('Error:', error),
    onclose: () => console.log('Closed')
  }
});
```

### 发送文本

#### Python
```python
await session.send_realtime_input(text="Hello, how are you?")
```

#### JavaScript
```js
session.sendRealtimeInput({ text: 'Hello, how are you?' });
```

### 发送音频

#### Python
```python
await session.send_realtime_input(
    audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000")
)
```

#### JavaScript
```js
session.sendRealtimeInput({
  audio: { data: chunk.toString('base64'), mimeType: 'audio/pcm;rate=16000' }
});
```

### 发送视频

#### Python
```python
# frame: raw JPEG-encoded bytes
await session.send_realtime_input(
    video=types.Blob(data=frame, mime_type="image/jpeg")
)
```

#### JavaScript
```js
session.sendRealtimeInput({
  video: { data: frame.toString('base64'), mimeType: 'image/jpeg' }
});
```

### 接收音频和文本

> [!IMPORTANT]
> 单个服务器事件可能同时包含**多个内容部分**（例如音频块和转写文本）。请始终处理每个事件中的**全部**部分，避免遗漏内容。

#### Python
```python
async for response in session.receive():
    content = response.server_content
    if content:
        # Audio — process ALL parts in each event
        if content.model_turn:
            for part in content.model_turn.parts:
                if part.inline_data:
                    audio_data = part.inline_data.data
        # Transcription
        if content.input_transcription:
            print(f"User: {content.input_transcription.text}")
        if content.output_transcription:
            print(f"Gemini: {content.output_transcription.text}")
        # Interruption
        if content.interrupted is True:
            pass  # Stop playback, clear audio queue
```

#### JavaScript
```js
// Inside the onmessage callback
const content = response.serverContent;
if (content?.modelTurn?.parts) {
  for (const part of content.modelTurn.parts) {
    if (part.inlineData) {
      const audioData = part.inlineData.data; // Base64 encoded
    }
  }
}
if (content?.inputTranscription) console.log('User:', content.inputTranscription.text);
if (content?.outputTranscription) console.log('Gemini:', content.outputTranscription.text);
if (content?.interrupted) { /* Stop playback, clear audio queue */ }
```

---

## 实时翻译（Gemini Live Translate）

Live API 支持对 70+ 种语言的语音（音频）进行实时、低延迟的流式翻译。有关选项和能力的完整细节，请参阅 [Live Translate 指南](https://ai.google.dev/gemini-api/docs/live-api/live-translate.md.txt)。

### 模型
- `gemini-3.5-live-translate-preview` — 推荐用于所有 Live Translate 场景的翻译模型。

### 配置（`TranslationConfig`）

要启用翻译，请在实时会话配置中指定一个 `TranslationConfig` 对象：

- **Python SDK**：使用 `LiveConnectConfig` 上的 `translation_config` 进行连接配置：
  ```python
  config = types.LiveConnectConfig(
      response_modalities=[types.Modality.AUDIO],
      translation_config=types.TranslationConfig(
          target_language_code="es",  # Target language code (e.g. es, fr, pl)
          echo_target_language=True,
      ),
      input_audio_transcription=types.AudioTranscriptionConfig(),
      output_audio_transcription=types.AudioTranscriptionConfig(),
  )
  ```
- **原生 WebSocket**：将 `translationConfig` 放在 `generationConfig` 中：
  ```json
  {
    "setup": {
      "model": "models/gemini-3.5-live-translate-preview",
      "generationConfig": {
        "responseModalities": ["AUDIO"],
        "translationConfig": {
          "targetLanguageCode": "es",
          "echoTargetLanguage": true
        }
      }
    }
  }
  ```

---

## 限制

- **响应模态** — 每个会话只能是 `TEXT` **或** `AUDIO`，不可同时。原生音频模型仅支持音频。
- **纯音频会话** — 无压缩情况下 15 分钟
- **音视频会话** — 无压缩情况下 2 分钟
- **连接生命周期** — 约 10 分钟（请使用会话恢复）
- **上下文窗口** — 128k token（原生音频）/ 32k token（标准）
- **异步函数调用** — 暂不支持；函数调用仅支持同步。模型在收到工具响应前不会开始响应。
- **主动音频** — Gemini 3.1 Flash Live 暂不支持。请移除该特性的相关配置。
- **情感对话** — Gemini 3.1 Flash Live 暂不支持。请移除该特性的相关配置。
- **代码执行** — 不支持
- **URL 上下文** — 不支持

## 从 Gemini 2.5 Flash Live 迁移

从 `gemini-2.5-flash-native-audio-preview-12-2025` 迁移到 `gemini-3.1-flash-live-preview` 时：

1. **模型字符串** — 将 `gemini-2.5-flash-native-audio-preview-12-2025` 更新为 `gemini-3.1-flash-live-preview`。
2. **思考配置** — 使用 `thinkingLevel`（`minimal`、`low`、`medium`、`high`）代替 `thinkingBudget`。默认值为 `minimal` 以获得最低延迟。
3. **服务器事件** — 单个事件可能同时包含多个内容部分（音频 + 转写）。请处理每个事件中的**全部**部分。
4. **客户端内容** — `send_client_content` 仅用于植入初始上下文历史（在 `history_config` 中设置 `initial_history_in_client_content`）。对话过程中的文本请使用 `send_realtime_input`。
5. **轮次覆盖** — 默认值为 `TURN_INCLUDES_AUDIO_ACTIVITY_AND_ALL_VIDEO`，而非 `TURN_INCLUDES_ONLY_ACTIVITY`。如果持续发送视频帧，请考虑仅在音频活跃期间发送以降低成本。
6. **异步函数调用** — 暂不支持。函数调用仅支持同步。
7. **主动音频与情感对话** — 暂不支持。请移除这些特性的相关配置。

## 最佳实践

1. 测试麦克风音频时请**使用耳机**，防止回声/自打断
2. 对超过 15 分钟的会话**启用上下文窗口压缩**
3. **实现会话恢复**以优雅处理连接重置
4. 在客户端部署中使用**临时令牌** —— 切勿在浏览器中暴露 API key
5. 对所有实时用户输入（音频、视频、文本）**使用 `send_realtime_input`**。仅在为植入初始上下文历史时使用 `send_client_content`
6. 麦克风暂停时发送 `audioStreamEnd`，以清空缓存音频
7. 收到打断信号时**清空音频播放队列**
8. 处理每个服务器事件中的**全部部分** —— 事件可能包含多个内容部分

## 文档查询

### 已安装 MCP 时（推荐）

如果可用 **`search_docs`** 工具（来自 Google MCP 服务器），请将其作为**唯一**的文档来源：

1. 使用查询调用 `search_docs`
2. 阅读返回的文档
3. **信任 MCP 结果**作为 API 细节的唯一来源 —— 它们始终保持最新。

> [!IMPORTANT]
> 当存在 MCP 工具时，**切勿**手动抓取 URL。MCP 提供的文档已建立索引且保持更新，比手动抓取 URL 更准确、更节省 token。

### 未安装 MCP 时（仅作为回退）

如果没有任何 MCP 文档工具，请从官方文档索引抓取：

**llms.txt URL**：`https://ai.google.dev/gemini-api/docs/llms.txt`

该索引包含所有以 `.md.txt` 格式提供的文档页面链接。请使用 web 抓取工具：

1. 抓取 `llms.txt` 以发现可用的文档页面
2. 抓取特定页面（例如 `https://ai.google.dev/gemini-api/docs/live-session.md.txt`）

### 关键文档页面

> [!IMPORTANT]
> 以上并非全部文档页面。请使用 `llms.txt` 索引来发现可用的文档页面。

- [Live API 概述](https://ai.google.dev/gemini-api/docs/live.md.txt) — 快速入门、原生 WebSocket 使用
- [Live Translate](https://ai.google.dev/gemini-api/docs/live-api/live-translate.md.txt) — 翻译的配置选项和能力
- [Live API 能力指南](https://ai.google.dev/gemini-api/docs/live-guide.md.txt) — 语音配置、转写配置、原生音频（思考）、VAD 配置、媒体分辨率
- [Live API 工具使用](https://ai.google.dev/gemini-api/docs/live-tools.md.txt) — 函数调用（同步和异步）、Google Search 接入
- [会话管理](https://ai.google.dev/gemini-api/docs/live-session.md.txt) — 上下文窗口压缩、会话恢复、GoAway 信号
- [临时令牌](https://ai.google.dev/gemini-api/docs/ephemeral-tokens.md.txt) — 浏览器/移动端的客户端安全认证
- [WebSockets API 参考](https://ai.google.dev/api/live.md.txt) — 原生 WebSocket 协议细节

## 支持的语言

Live API 支持 70 种语言，包括：英语、西班牙语、法语、德语、意大利语、葡萄牙语、中文、日语、韩语、印地语、阿拉伯语、俄语等。原生音频模型可自动检测并切换语言。