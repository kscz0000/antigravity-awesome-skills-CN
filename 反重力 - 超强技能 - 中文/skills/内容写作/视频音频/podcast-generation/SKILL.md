---
name: podcast-generation
description: "使用 Azure OpenAI Realtime API 从文本内容生成真实音频叙事。当用户要求'生成播客'、'文本转语音'、'创建音频叙事'或'podcast generation'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 使用 GPT Realtime Mini 生成播客

使用 Azure OpenAI Realtime API 从文本内容生成真实音频叙事。

## 快速开始

1. 配置 Realtime API 环境变量
2. 通过 WebSocket 连接 Azure OpenAI Realtime 端点
3. 发送文本提示，收集 PCM 音频块和转录文本
4. 将 PCM 转换为 WAV 格式
5. 返回 base64 编码的音频供前端播放

## 环境配置

```env
AZURE_OPENAI_AUDIO_API_KEY=your_realtime_api_key
AZURE_OPENAI_AUDIO_ENDPOINT=https://your-resource.cognitiveservices.azure.com
AZURE_OPENAI_AUDIO_DEPLOYMENT=gpt-realtime-mini
```

**注意**：端点不应包含 `/openai/v1/`，只需基础 URL。

## 核心工作流

### 后端音频生成

```python
from openai import AsyncOpenAI
import base64

# Convert HTTPS endpoint to WebSocket URL
ws_url = endpoint.replace("https://", "wss://") + "/openai/v1"

client = AsyncOpenAI(
    websocket_base_url=ws_url,
    api_key=api_key
)

audio_chunks = []
transcript_parts = []

async with client.realtime.connect(model="gpt-realtime-mini") as conn:
    # Configure for audio-only output
    await conn.session.update(session={
        "output_modalities": ["audio"],
        "instructions": "You are a narrator. Speak naturally."
    })
    
    # Send text to narrate
    await conn.conversation.item.create(item={
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": prompt}]
    })
    
    await conn.response.create()
    
    # Collect streaming events
    async for event in conn:
        if event.type == "response.output_audio.delta":
            audio_chunks.append(base64.b64decode(event.delta))
        elif event.type == "response.output_audio_transcript.delta":
            transcript_parts.append(event.delta)
        elif event.type == "response.done":
            break

# Convert PCM to WAV (see scripts/pcm_to_wav.py)
pcm_audio = b''.join(audio_chunks)
wav_audio = pcm_to_wav(pcm_audio, sample_rate=24000)
```

### 前端音频播放

```javascript
// Convert base64 WAV to playable blob
const base64ToBlob = (base64, mimeType) => {
  const bytes = atob(base64);
  const arr = new Uint8Array(bytes.length);
  for (let i = 0; i < bytes.length; i++) arr[i] = bytes.charCodeAt(i);
  return new Blob([arr], { type: mimeType });
};

const audioBlob = base64ToBlob(response.audio_data, 'audio/wav');
const audioUrl = URL.createObjectURL(audioBlob);
new Audio(audioUrl).play();
```

## 语音选项

| 语音 | 风格 |
|------|------|
| alloy | 中性 |
| echo | 温暖 |
| fable | 富有表现力 |
| onyx | 深沉 |
| nova | 友好 |
| shimmer | 清晰 |

## Realtime API 事件

- `response.output_audio.delta` — Base64 音频块
- `response.output_audio_transcript.delta` — 转录文本
- `response.done` — 生成完成
- `error` — 通过 `event.error.message` 处理

## 音频格式

- **输入**：文本提示
- **输出**：PCM 音频（24kHz、16 位、单声道）
- **存储**：Base64 编码的 WAV

## 参考资料

- **完整架构**：参见 references/architecture.md 了解完整技术栈设计
- **代码示例**：参见 references/code-examples.md 了解生产环境模式
- **PCM 转换**：使用 scripts/pcm_to_wav.py 进行音频格式转换

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来寻求澄清。
