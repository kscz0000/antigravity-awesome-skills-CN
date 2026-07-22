---
name: azure-speech-to-text-rest-py
description: Azure 语音转文本 REST API（Python），用于短音频识别。无需 Speech SDK，仅通过 HTTP 请求即可完成最长 60 秒音频的语音转文字。当用户要求'Azure语音识别'、'语音转文字REST API'、'短音频转写'、'Speech to Text Python'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure 语音转文本 REST API（短音频）

用于短音频文件（最长 60 秒）语音转文字转写的简单 REST API。无需 SDK — 只需 HTTP 请求。

## 前提条件

1. **Azure 订阅** - [免费创建](https://azure.microsoft.com/free/)
2. **Speech 资源** - 在 [Azure 门户](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices)中创建
3. **获取凭据** - 部署后，前往资源 > 密钥和终结点

## 环境变量

```bash
# Required
AZURE_SPEECH_KEY=<your-speech-resource-key>
AZURE_SPEECH_REGION=<region>  # e.g., eastus, westus2, westeurope

# Alternative: Use endpoint directly
AZURE_SPEECH_ENDPOINT=https://<region>.stt.speech.microsoft.com
```

## 安装

```bash
pip install requests
```

## 快速开始

```python
import os
import requests

def transcribe_audio(audio_file_path: str, language: str = "en-US") -> dict:
    """Transcribe short audio file (max 60 seconds) using REST API."""
    region = os.environ["AZURE_SPEECH_REGION"]
    api_key = os.environ["AZURE_SPEECH_KEY"]
    
    url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
    
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
        "Accept": "application/json"
    }
    
    params = {
        "language": language,
        "format": "detailed"  # or "simple"
    }
    
    with open(audio_file_path, "rb") as audio_file:
        response = requests.post(url, headers=headers, params=params, data=audio_file)
    
    response.raise_for_status()
    return response.json()

# Usage
result = transcribe_audio("audio.wav", "en-US")
print(result["DisplayText"])
```

## 音频要求

| 格式 | 编解码器 | 采样率 | 备注 |
|--------|-------|-------------|-------|
| WAV | PCM | 16 kHz, 单声道 | **推荐** |
| OGG | OPUS | 16 kHz, 单声道 | 文件更小 |

**限制：**
- 音频最长 60 秒
- 发音评估：最长 30 秒
- 无部分/中间结果（仅最终结果）

## Content-Type 请求头

```python
# WAV PCM 16kHz
"Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000"

# OGG OPUS
"Content-Type": "audio/ogg; codecs=opus"
```

## 响应格式

### 简单格式（默认）

```python
params = {"language": "en-US", "format": "simple"}
```

```json
{
  "RecognitionStatus": "Success",
  "DisplayText": "Remind me to buy 5 pencils.",
  "Offset": "1236645672289",
  "Duration": "1236645672289"
}
```

### 详细格式

```python
params = {"language": "en-US", "format": "detailed"}
```

```json
{
  "RecognitionStatus": "Success",
  "Offset": "1236645672289",
  "Duration": "1236645672289",
  "NBest": [
    {
      "Confidence": 0.9052885,
      "Display": "What's the weather like?",
      "ITN": "what's the weather like",
      "Lexical": "what's the weather like",
      "MaskedITN": "what's the weather like"
    }
  ]
}
```

## 分块传输（推荐）

以分块方式流式传输音频，可降低延迟：

```python
import os
import requests

def transcribe_chunked(audio_file_path: str, language: str = "en-US") -> dict:
    """Stream audio in chunks for lower latency."""
    region = os.environ["AZURE_SPEECH_REGION"]
    api_key = os.environ["AZURE_SPEECH_KEY"]
    
    url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
    
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
        "Accept": "application/json",
        "Transfer-Encoding": "chunked",
        "Expect": "100-continue"
    }
    
    params = {"language": language, "format": "detailed"}
    
    def generate_chunks(file_path: str, chunk_size: int = 1024):
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk
    
    response = requests.post(
        url, 
        headers=headers, 
        params=params, 
        data=generate_chunks(audio_file_path)
    )
    
    response.raise_for_status()
    return response.json()
```

## 认证方式

### 方式 1：订阅密钥（简单）

```python
headers = {
    "Ocp-Apim-Subscription-Key": os.environ["AZURE_SPEECH_KEY"]
}
```

### 方式 2：Bearer Token

```python
import requests
import os

def get_access_token() -> str:
    """Get access token from the token endpoint."""
    region = os.environ["AZURE_SPEECH_REGION"]
    api_key = os.environ["AZURE_SPEECH_KEY"]
    
    token_url = f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    
    response = requests.post(
        token_url,
        headers={
            "Ocp-Apim-Subscription-Key": api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "0"
        }
    )
    response.raise_for_status()
    return response.text

# Use token in requests (valid for 10 minutes)
token = get_access_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
    "Accept": "application/json"
}
```

## 查询参数

| 参数 | 必填 | 值 | 说明 |
|-----------|----------|--------|-------------|
| `language` | **是** | `en-US`, `de-DE` 等 | 语音语言 |
| `format` | 否 | `simple`, `detailed` | 结果格式（默认：simple） |
| `profanity` | 否 | `masked`, `removed`, `raw` | 脏话处理方式（默认：masked） |

## 识别状态值

| 状态 | 说明 |
|--------|-------------|
| `Success` | 识别成功 |
| `NoMatch` | 检测到语音但未匹配到词语 |
| `InitialSilenceTimeout` | 仅检测到静音 |
| `BabbleTimeout` | 仅检测到噪音 |
| `Error` | 内部服务错误 |

## 脏话处理

```python
# 用星号遮蔽脏话（默认）
params = {"language": "en-US", "profanity": "masked"}

# 完全移除脏话
params = {"language": "en-US", "profanity": "removed"}

# 保留脏话原文
params = {"language": "en-US", "profanity": "raw"}
```

## 错误处理

```python
import requests

def transcribe_with_error_handling(audio_path: str, language: str = "en-US") -> dict | None:
    """Transcribe with proper error handling."""
    region = os.environ["AZURE_SPEECH_REGION"]
    api_key = os.environ["AZURE_SPEECH_KEY"]
    
    url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
    
    try:
        with open(audio_path, "rb") as audio_file:
            response = requests.post(
                url,
                headers={
                    "Ocp-Apim-Subscription-Key": api_key,
                    "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
                    "Accept": "application/json"
                },
                params={"language": language, "format": "detailed"},
                data=audio_file
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("RecognitionStatus") == "Success":
                return result
            else:
                print(f"Recognition failed: {result.get('RecognitionStatus')}")
                return None
        elif response.status_code == 400:
            print(f"Bad request: Check language code or audio format")
        elif response.status_code == 401:
            print(f"Unauthorized: Check API key or token")
        elif response.status_code == 403:
            print(f"Forbidden: Missing authorization header")
        else:
            print(f"Error {response.status_code}: {response.text}")
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

## 异步版本

```python
import os
import aiohttp
import asyncio

async def transcribe_async(audio_file_path: str, language: str = "en-US") -> dict:
    """Async version using aiohttp."""
    region = os.environ["AZURE_SPEECH_REGION"]
    api_key = os.environ["AZURE_SPEECH_KEY"]
    
    url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
    
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
        "Accept": "application/json"
    }
    
    params = {"language": language, "format": "detailed"}
    
    async with aiohttp.ClientSession() as session:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        
        async with session.post(url, headers=headers, params=params, data=audio_data) as response:
            response.raise_for_status()
            return await response.json()

# Usage
result = asyncio.run(transcribe_async("audio.wav", "en-US"))
print(result["DisplayText"])
```

## 支持的语言

常用语言代码（完整列表见[语言支持](https://learn.microsoft.com/azure/ai-services/speech-service/language-support)）：

| 代码 | 语言 |
|------|----------|
| `en-US` | 英语（美国） |
| `en-GB` | 英语（英国） |
| `de-DE` | 德语 |
| `fr-FR` | 法语 |
| `es-ES` | 西班牙语（西班牙） |
| `es-MX` | 西班牙语（墨西哥） |
| `zh-CN` | 中文（普通话） |
| `ja-JP` | 日语 |
| `ko-KR` | 韩语 |
| `pt-BR` | 葡萄牙语（巴西） |

## 最佳实践

1. **使用 WAV PCM 16kHz 单声道**以获得最佳兼容性
2. **启用分块传输**以降低延迟
3. **缓存 access token** 9 分钟（有效期 10 分钟）
4. **指定正确的语言**以确保识别准确
5. **需要置信度分数时使用详细格式**
6. **在生产代码中处理所有 RecognitionStatus 值**

## 何时不适用此 API

当需要以下功能时，请改用 Speech SDK 或 Batch Transcription API：

- 超过 60 秒的音频
- 实时流式转写
- 部分/中间结果
- 语音翻译
- 自定义语音模型
- 批量转写多个文件

## 参考文件

| 文件 | 内容 |
|------|----------|
| references/pronunciation-assessment.md | 发音评估参数与评分 |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不可替代针对具体环境的验证、测试或专家评审。
- 若缺少所需输入、权限、安全边界或成功标准，应停止并请求澄清。
