---
name: voice-ai-development
description: 语音 AI 应用开发专家——涵盖实时语音代理到语音功能应用。涉及 OpenAI Realtime API、Vapi 语音代理、Deepgram 转录、ElevenLabs 合成、LiveKit 实时基础设施以及 WebRTC 基础。触发词：voice ai、voice agent、speech to text、text to speech、realtime voice、vapi、deepgram、elevenlabs、livekit、openai realtime。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 语音 AI 开发

语音 AI 应用开发专家——从实时语音代理到语音功能应用。
涉及 OpenAI Realtime API、Vapi 语音代理、Deepgram 转录、ElevenLabs 合成、LiveKit 实时基础设施以及 WebRTC 基础。掌握如何构建低延迟、生产可用的语音体验。

**角色**：语音 AI 架构师

你是构建实时语音应用的专家。你时刻关注延迟预算、音质和用户体验。你深知语音应用快如闪电时令人惊艳，而一旦变慢就彻底崩溃。你会针对每个用例选择合适的供应商组合，并对主观响应速度进行不懈优化。

### 专长领域

- 实时音频流
- 语音代理架构
- 供应商选型
- 延迟优化
- 音质调优

## 能力清单

- OpenAI Realtime API
- Vapi 语音代理
- Deepgram STT/TTS
- ElevenLabs 语音合成
- LiveKit 实时基础设施
- WebRTC 音频处理
- 语音代理设计
- 延迟优化

## 前置条件

- 0：异步编程
- 1：WebSocket 基础
- 2：音频概念（采样率、编解码器）
- 必备技能：Python 或 Node.js、供应商 API 密钥、音频处理知识

## 适用范围

- 0：延迟因供应商而异
- 1：每分钟成本会累加
- 2：质量取决于网络状况
- 3：调试过程复杂

## 技术生态

### 核心供应商

- OpenAI Realtime API
- Vapi
- Deepgram
- ElevenLabs

### 基础设施

- LiveKit
- Daily.co
- Twilio

### 常见集成

- WebRTC
- WebSockets
- 电话网络（SIP/PSTN）

### 目标平台

- Web 应用
- 移动应用
- 呼叫中心
- 语音助手

## 模式

### OpenAI Realtime API

基于 GPT-4o 的原生语音对语音

**使用场景**：当你希望获得一体化的语音 AI，无需单独的 STT/TTS

import asyncio
import websockets
import json
import base64

OPENAI_API_KEY = "sk-..."

async def voice_session():
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(url, extra_headers=headers) as ws:
        # 配置会话
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",  # alloy, echo, fable, onyx, nova, shimmer
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",  # 语音活动检测
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 500
                },
                "tools": [
                    {
                        "type": "function",
                        "name": "get_weather",
                        "description": "Get weather for a location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }))

        # 发送音频（PCM16、24kHz、单声道）
        async def send_audio(audio_bytes):
            await ws.send(json.dumps({
                "type": "input_audio_buffer.append",
                "audio": base64.b64encode(audio_bytes).decode()
            }))

        # 接收事件
        async for message in ws:
            event = json.loads(message)

            if event["type"] == "response.audio.delta":
                # 播放音频块
                audio = base64.b64decode(event["delta"])
                play_audio(audio)

            elif event["type"] == "response.audio_transcript.done":
                print(f"Assistant said: {event['transcript']}")

            elif event["type"] == "input_audio_buffer.speech_started":
                print("User started speaking")

            elif event["type"] == "response.function_call_arguments.done":
                # 处理工具调用
                name = event["name"]
                args = json.loads(event["arguments"])
                result = call_function(name, args)
                await ws.send(json.dumps({
                    "type": "conversation.item.create",
                    "item": {
                        "type": "function_call_output",
                        "call_id": event["call_id"],
                        "output": json.dumps(result)
                    }
                }))

### Vapi 语音代理

使用 Vapi 平台构建语音代理

**使用场景**：电话端代理、快速部署

# Vapi 提供托管式语音代理，支持 webhook

from flask import Flask, request, jsonify
import vapi

app = Flask(__name__)
client = vapi.Vapi(api_key="...")

# 创建一个助手
assistant = client.assistants.create(
    name="Support Agent",
    model={
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful support agent..."
            }
        ]
    },
    voice={
        "provider": "11labs",
        "voiceId": "21m00Tcm4TlvDq8ikWAM"  # Rachel
    },
    firstMessage="Hi! How can I help you today?",
    transcriber={
        "provider": "deepgram",
        "model": "nova-2"
    }
)

# 用于会话事件的 webhook
@app.route("/vapi/webhook", methods=["POST"])
def vapi_webhook():
    event = request.json

    if event["type"] == "function-call":
        # 处理工具调用
        name = event["functionCall"]["name"]
        args = event["functionCall"]["parameters"]

        if name == "check_order":
            result = check_order(args["order_id"])
            return jsonify({"result": result})

    elif event["type"] == "end-of-call-report":
        # 通话结束——保存转录
        transcript = event["transcript"]
        save_transcript(event["call"]["id"], transcript)

    return jsonify({"ok": True})

# 发起外呼
call = client.calls.create(
    assistant_id=assistant.id,
    customer={
        "number": "+1234567890"
    },
    phoneNumber={
        "twilioPhoneNumber": "+0987654321"
    }
)

# 或创建网页通话
web_call = client.calls.create(
    assistant_id=assistant.id,
    type="web"
)
# 返回 WebRTC 连接的 URL

### Deepgram STT + ElevenLabs TTS

业界领先的转录与合成方案

**使用场景**：追求高品质语音、自定义流水线

import asyncio
from deepgram import DeepgramClient, LiveTranscriptionEvents
from elevenlabs import ElevenLabs

# Deepgram 实时转录
deepgram = DeepgramClient(api_key="...")

async def transcribe_stream(audio_stream):
    connection = deepgram.listen.live.v("1")

    async def on_transcript(result):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            print(f"Heard: {transcript}")
            if result.is_final:
                # 处理最终转录
                await handle_user_input(transcript)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    await connection.start({
        "model": "nova-2",  # 最佳质量
        "language": "en",
        "smart_format": True,
        "interim_results": True,  # 获取部分结果
        "utterance_end_ms": 1000,
        "vad_events": True,  # 语音活动检测
        "encoding": "linear16",
        "sample_rate": 16000
    })

    # 流式传输音频
    async for chunk in audio_stream:
        await connection.send(chunk)

    await connection.finish()

# ElevenLabs 流式合成
eleven = ElevenLabs(api_key="...")

def text_to_speech_stream(text: str):
    """流式输出 TTS 音频块。"""
    audio_stream = eleven.text_to_speech.convert_as_stream(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
        model_id="eleven_turbo_v2_5",  # 速度最快
        text=text,
        output_format="pcm_24000"  # 原始 PCM，延迟最低
    )

    for chunk in audio_stream:
        yield chunk

# 或使用 WebSocket 实现最低延迟
async def tts_websocket(text_stream):
    async with eleven.text_to_speech.stream_async(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_turbo_v2_5"
    ) as tts:
        async for text_chunk in text_stream:
            audio = await tts.send(text_chunk)
            yield audio

        # 刷新剩余音频
        final_audio = await tts.flush()
        yield final_audio

### LiveKit 实时基础设施

面向语音应用的 WebRTC 基础设施

**使用场景**：构建定制化的实时语音应用

from livekit import api, rtc
import asyncio

# 服务端：创建房间和令牌
lk_api = api.LiveKitAPI(
    url="wss://your-livekit.livekit.cloud",
    api_key="...",
    api_secret="..."
)

async def create_room(room_name: str):
    room = await lk_api.room.create_room(
        api.CreateRoomRequest(name=room_name)
    )
    return room

def create_token(room_name: str, participant_name: str):
    token = api.AccessToken(
        api_key="...",
        api_secret="..."
    )
    token.with_identity(participant_name)
    token.with_grants(api.VideoGrants(
        room_join=True,
        room=room_name
    ))
    return token.to_jwt()

# 代理端：连接并处理音频
async def voice_agent(room_name: str):
    room = rtc.Room()

    @room.on("track_subscribed")
    def on_track(track, publication, participant):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            # 处理传入音频
            audio_stream = rtc.AudioStream(track)
            asyncio.create_task(process_audio(audio_stream))

    token = create_token(room_name, "agent")
    await room.connect("wss://your-livekit.livekit.cloud", token)

    # 发布代理的音频
    source = rtc.AudioSource(sample_rate=24000, num_channels=1)
    track = rtc.LocalAudioTrack.create_audio_track("agent-voice", source)
    await room.local_participant.publish_track(track)

    # 从 TTS 发送音频
    async def speak(text: str):
        for audio_chunk in text_to_speech(text):
            await source.capture_frame(rtc.AudioFrame(
                data=audio_chunk,
                sample_rate=24000,
                num_channels=1,
                samples_per_channel=len(audio_chunk) // 2
            ))

    return room, speak

# 使用 STT 处理音频
async def process_audio(audio_stream):
    async for frame in audio_stream:
        # 发送到 Deepgram 或其他 STT
        await transcriber.send(frame.data)

### 完整语音代理流水线

集成所有组件的完整语音代理

**使用场景**：定制生产级语音代理

import asyncio
from dataclasses import dataclass
from typing import AsyncIterator

@dataclass
class VoiceAgentConfig:
    stt_provider: str = "deepgram"
    tts_provider: str = "elevenlabs"
    llm_provider: str = "openai"
    vad_enabled: bool = True
    interrupt_enabled: bool = True

class VoiceAgent:
    def __init__(self, config: VoiceAgentConfig):
        self.config = config
        self.is_speaking = False
        self.conversation_history = []

    async def process_audio_stream(
        self,
        audio_in: AsyncIterator[bytes],
        audio_out: asyncio.Queue
    ):
        """主音频处理循环。"""

        # STT 流式处理
        async def transcribe():
            transcript_buffer = ""
            async for audio_chunk in audio_in:
                # 检测用户打断
                if self.is_speaking and self.config.interrupt_enabled:
                    if await self.detect_speech(audio_chunk):
                        await self.stop_speaking()

                result = await self.stt.transcribe(audio_chunk)
                if result.is_final:
                    yield result.transcript

        # 处理转录文本
        async for user_text in transcribe():
            if not user_text.strip():
                continue

            self.conversation_history.append({
                "role": "user",
                "content": user_text
            })

            # 流式生成回复
            self.is_speaking = True
            async for audio_chunk in self.generate_response(user_text):
                await audio_out.put(audio_chunk)
            self.is_speaking = False

    async def generate_response(self, text: str) -> AsyncIterator[bytes]:
        """通过 TTS 流式输出 LLM 回复。"""

        # LLM token 流
        llm_stream = self.llm.stream_chat(self.conversation_history)

        # TTS 缓冲区（需约 50 字符以获得良好韵律）
        text_buffer = ""
        full_response = ""

        async for token in llm_stream:
            text_buffer += token
            full_response += token

            # 当累积足够文本时送入 TTS
            if len(text_buffer) > 50 or token in ".!?":
                async for audio in self.tts.synthesize_stream(text_buffer):
                    yield audio
                text_buffer = ""

        # 刷新剩余内容
        if text_buffer:
            async for audio in self.tts.synthesize_stream(text_buffer):
                yield audio

        self.conversation_history.append({
            "role": "assistant",
            "content": full_response
        })

    async def detect_speech(self, audio: bytes) -> bool:
        """语音活动检测。"""
        # 使用 WebRTC VAD 或 Silero VAD
        return self.vad.is_speech(audio)

    async def stop_speaking(self):
        """处理用户打断。"""
        self.is_speaking = False
        # 清空音频队列
        # 停止 TTS 生成

# 延迟优化建议：
# 1. 全链路使用流式处理（STT、LLM、TTS）
# 2. 在 LLM 结束前提前启动 TTS（缓冲约 50 字符）
# 3. 使用 PCM 音频格式（无编码开销）
# 4. 保持 WebSocket 连接存活
# 5. 选择靠近用户的区域端点

## 验证检查项

### 非流式 TTS

严重程度：高

说明：非流式 TTS 会带来显著的延迟。

修复建议：使用 tts.synthesize_stream() 或 tts.convert_as_stream()

### 硬编码采样率

严重程度：中

说明：硬编码采样率可能导致格式不匹配。

修复建议：将采样率定义为常量，并明确记录预期格式

### WebSocket 缺少重连机制

严重程度：高

说明：WebSocket 连接需要重连逻辑。

修复建议：添加带指数退避的重试循环

### 缺少 VAD 配置

严重程度：中

说明：VAD 需要调优才能获得良好体验。

修复建议：配置 threshold 和 silence_duration_ms

### 阻塞式音频处理

严重程度：高

说明：音频处理应采用异步以避免阻塞。

修复建议：使用 async def 并 await 音频操作

### 缺少打断处理

严重程度：中

说明：语音代理应处理用户打断。

修复建议：添加 barge-in 检测并取消当前响应

### 音频队列无法清空

严重程度：低

说明：音频队列应支持在打断时清空。

修复建议：添加在打断时清空队列的方法

### WebSocket 缺少错误处理

严重程度：高

说明：WebSocket 操作需要错误处理。

修复建议：用 try/except 包裹 ConnectionClosed 异常

## 协作

### 委派触发器

- agent graph|workflow|state -> langgraph（语音背后需要复杂的代理逻辑）
- extract|structured|json -> structured-output（需要从语音中提取结构化数据）
- observability|tracing|monitoring -> langfuse（需要监控语音代理质量）
- frontend|web|react -> nextjs-app-router（需要为语音代理提供 Web 界面）

### 智能语音代理

技能：voice-ai-development、langgraph、structured-output

工作流：

```
1. 设计带工具的代理图
2. 添加语音接口层
3. 使用结构化输出处理工具响应
4. 针对语音延迟进行优化
```

### 可监控的语音代理

技能：voice-ai-development、langfuse

工作流：

```
1. 使用所选供应商构建语音代理
2. 添加 Langfuse 回调
3. 跟踪延迟、质量和会话流程
4. 基于指标持续迭代
```

### 电话端代理

技能：voice-ai-development、twilio

工作流：

```
1. 搭建 Vapi 或自定义代理
2. 连接 Twilio 以接入 PSTN
3. 处理呼入/呼出通话
4. 实现呼叫路由逻辑
```

## 相关技能

可与以下技能良好配合：`langgraph`、`structured-output`、`langfuse`

## 使用时机
- 用户提及或暗示：voice ai
- 用户提及或暗示：voice agent
- 用户提及或暗示：speech to text
- 用户提及或暗示：text to speech
- 用户提及或暗示：realtime voice
- 用户提及或暗示：vapi
- 用户提及或暗示：deepgram
- 用户提及或暗示：elevenlabs
- 用户提及或暗示：livekit
- 用户提及或暗示：openai realtime

## 局限性
- 仅当任务明确匹配上述适用范围时使用本技能。
- 不要把本技能的输出视为环境特定验证、测试或专家审查的替代品。
- 若缺少必要的输入、权限、安全边界或成功标准，应主动停下并请求澄清。
