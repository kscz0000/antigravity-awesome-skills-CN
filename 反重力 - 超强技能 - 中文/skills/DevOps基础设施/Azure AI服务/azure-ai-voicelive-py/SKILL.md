---
name: azure-ai-voicelive-py
description: "使用双向 WebSocket 通信构建实时语音 AI 应用。触发词：Azure Voice Live、实时语音、语音AI、WebSocket语音、gpt-4o-realtime、语音助手开发、双向语音通信"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure AI Voice Live SDK

使用双向 WebSocket 通信构建实时语音 AI 应用。

## 安装

```bash
pip install azure-ai-voicelive aiohttp azure-identity
```

## 环境变量

```bash
AZURE_COGNITIVE_SERVICES_ENDPOINT=https://<region>.api.cognitive.microsoft.com
# For API key auth (not recommended for production)
AZURE_COGNITIVE_SERVICES_KEY=<api-key>
```

## 身份验证

**DefaultAzureCredential（推荐）**:
```python
from azure.ai.voicelive.aio import connect
from azure.identity.aio import DefaultAzureCredential

async with connect(
    endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
    credential=DefaultAzureCredential(),
    model="gpt-4o-realtime-preview",
    credential_scopes=["https://cognitiveservices.azure.com/.default"]
) as conn:
    ...
```

**API 密钥**:
```python
from azure.ai.voicelive.aio import connect
from azure.core.credentials import AzureKeyCredential

async with connect(
    endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_COGNITIVE_SERVICES_KEY"]),
    model="gpt-4o-realtime-preview"
) as conn:
    ...
```

## 快速入门

```python
import asyncio
import os
from azure.ai.voicelive.aio import connect
from azure.identity.aio import DefaultAzureCredential

async def main():
    async with connect(
        endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
        credential=DefaultAzureCredential(),
        model="gpt-4o-realtime-preview",
        credential_scopes=["https://cognitiveservices.azure.com/.default"]
    ) as conn:
        # 使用指令更新会话
        await conn.session.update(session={
            "instructions": "You are a helpful assistant.",
            "modalities": ["text", "audio"],
            "voice": "alloy"
        })
        
        # 监听事件
        async for event in conn:
            print(f"Event: {event.type}")
            if event.type == "response.audio_transcript.done":
                print(f"Transcript: {event.transcript}")
            elif event.type == "response.done":
                break

asyncio.run(main())
```

## 核心架构

### 连接资源

`VoiceLiveConnection` 暴露以下资源：

| 资源 | 用途 | 关键方法 |
|------|------|----------|
| `conn.session` | 会话配置 | `update(session=...)` |
| `conn.response` | 模型响应 | `create()`, `cancel()` |
| `conn.input_audio_buffer` | 音频输入 | `append()`, `commit()`, `clear()` |
| `conn.output_audio_buffer` | 音频输出 | `clear()` |
| `conn.conversation` | 对话状态 | `item.create()`, `item.delete()`, `item.truncate()` |
| `conn.transcription_session` | 转录配置 | `update(session=...)` |

## 会话配置

```python
from azure.ai.voicelive.models import RequestSession, FunctionTool

await conn.session.update(session=RequestSession(
    instructions="You are a helpful voice assistant.",
    modalities=["text", "audio"],
    voice="alloy",  # 或 "echo", "shimmer", "sage" 等
    input_audio_format="pcm16",
    output_audio_format="pcm16",
    turn_detection={
        "type": "server_vad",
        "threshold": 0.5,
        "prefix_padding_ms": 300,
        "silence_duration_ms": 500
    },
    tools=[
        FunctionTool(
            type="function",
            name="get_weather",
            description="Get current weather",
            parameters={
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        )
    ]
))
```

## 音频流

### 发送音频（Base64 PCM16）

```python
import base64

# 读取音频块（16-bit PCM, 24kHz 单声道）
audio_chunk = await read_audio_from_microphone()
b64_audio = base64.b64encode(audio_chunk).decode()

await conn.input_audio_buffer.append(audio=b64_audio)
```

### 接收音频

```python
async for event in conn:
    if event.type == "response.audio.delta":
        audio_bytes = base64.b64decode(event.delta)
        await play_audio(audio_bytes)
    elif event.type == "response.audio.done":
        print("Audio complete")
```

## 事件处理

```python
async for event in conn:
    match event.type:
        # 会话事件
        case "session.created":
            print(f"Session: {event.session}")
        case "session.updated":
            print("Session updated")
        
        # 音频输入事件
        case "input_audio_buffer.speech_started":
            print(f"Speech started at {event.audio_start_ms}ms")
        case "input_audio_buffer.speech_stopped":
            print(f"Speech stopped at {event.audio_end_ms}ms")
        
        # 转录事件
        case "conversation.item.input_audio_transcription.completed":
            print(f"User said: {event.transcript}")
        case "conversation.item.input_audio_transcription.delta":
            print(f"Partial: {event.delta}")
        
        # 响应事件
        case "response.created":
            print(f"Response started: {event.response.id}")
        case "response.audio_transcript.delta":
            print(event.delta, end="", flush=True)
        case "response.audio.delta":
            audio = base64.b64decode(event.delta)
        case "response.done":
            print(f"Response complete: {event.response.status}")
        
        # 函数调用
        case "response.function_call_arguments.done":
            result = handle_function(event.name, event.arguments)
            await conn.conversation.item.create(item={
                "type": "function_call_output",
                "call_id": event.call_id,
                "output": json.dumps(result)
            })
            await conn.response.create()
        
        # 错误
        case "error":
            print(f"Error: {event.error.message}")
```

## 常用模式

### 手动轮次模式（无 VAD）

```python
await conn.session.update(session={"turn_detection": None})

# 手动控制轮次
await conn.input_audio_buffer.append(audio=b64_audio)
await conn.input_audio_buffer.commit()  # 用户轮次结束
await conn.response.create()  # 触发响应
```

### 中断处理

```python
async for event in conn:
    if event.type == "input_audio_buffer.speech_started":
        # 用户中断 - 取消当前响应
        await conn.response.cancel()
        await conn.output_audio_buffer.clear()
```

### 对话历史

```python
# 添加系统消息
await conn.conversation.item.create(item={
    "type": "message",
    "role": "system",
    "content": [{"type": "input_text", "text": "Be concise."}]
})

# 添加用户消息
await conn.conversation.item.create(item={
    "type": "message",
    "role": "user", 
    "content": [{"type": "input_text", "text": "Hello!"}]
})

await conn.response.create()
```

## 语音选项

| 语音 | 描述 |
|------|------|
| `alloy` | 中性、平衡 |
| `echo` | 温暖、对话式 |
| `shimmer` | 清晰、专业 |
| `sage` | 冷静、权威 |
| `coral` | 友好、活泼 |
| `ash` | 深沉、稳重 |
| `ballad` | 富有表现力 |
| `verse` | 叙事风格 |

Azure 语音：使用 `AzureStandardVoice`、`AzureCustomVoice` 或 `AzurePersonalVoice` 模型。

## 音频格式

| 格式 | 采样率 | 用途 |
|------|--------|------|
| `pcm16` | 24kHz | 默认，高质量 |
| `pcm16-8000hz` | 8kHz | 电话通信 |
| `pcm16-16000hz` | 16kHz | 语音助手 |
| `g711_ulaw` | 8kHz | 电话通信（美国） |
| `g711_alaw` | 8kHz | 电话通信（欧洲） |

## 轮次检测选项

```python
# 服务器 VAD（默认）
{"type": "server_vad", "threshold": 0.5, "silence_duration_ms": 500}

# Azure 语义 VAD（更智能的检测）
{"type": "azure_semantic_vad"}
{"type": "azure_semantic_vad_en"}  # 英语优化
{"type": "azure_semantic_vad_multilingual"}
```

## 错误处理

```python
from azure.ai.voicelive.aio import ConnectionError, ConnectionClosed

try:
    async with connect(...) as conn:
        async for event in conn:
            if event.type == "error":
                print(f"API Error: {event.error.code} - {event.error.message}")
except ConnectionClosed as e:
    print(f"Connection closed: {e.code} - {e.reason}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

## 参考资料

- **详细 API 参考**：参见 references/api-reference.md
- **完整示例**：参见 references/examples.md
- **所有模型与类型**：参见 references/models.md

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 请勿将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
