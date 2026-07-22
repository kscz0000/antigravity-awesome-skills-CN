---
name: azure-ai-transcription-py
description: Azure AI 转录 Python SDK。用于实时和批量语音转文字转录，支持时间戳和说话人分离。触发词：Azure语音转录、语音识别、speech-to-text、实时转录、批量转录、说话人分离、diarization、语音转文字、Azure AI Transcription
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI Transcription SDK for Python

用于 Azure AI 转录（语音转文字）的客户端库，支持实时和批量转录。

## 安装

```bash
pip install azure-ai-transcription
```

## 环境变量

```bash
TRANSCRIPTION_ENDPOINT=https://<resource>.cognitiveservices.azure.com
TRANSCRIPTION_KEY=<your-key>
```

## 身份验证

使用订阅密钥身份验证（此客户端不支持 DefaultAzureCredential）：

```python
import os
from azure.ai.transcription import TranscriptionClient

client = TranscriptionClient(
    endpoint=os.environ["TRANSCRIPTION_ENDPOINT"],
    credential=os.environ["TRANSCRIPTION_KEY"]
)
```

## 批量转录

```python
job = client.begin_transcription(
    name="meeting-transcription",
    locale="en-US",
    content_urls=["https://<storage>/audio.wav"],
    diarization_enabled=True
)
result = job.result()
print(result.status)
```

## 实时转录

```python
stream = client.begin_stream_transcription(locale="en-US")
stream.send_audio_file("audio.wav")
for event in stream:
    print(event.text)
```

## 最佳实践

1. **启用说话人分离**：当存在多个说话人时启用
2. **使用批量转录**：处理存储在 Blob 存储中的长音频文件
3. **捕获时间戳**：用于生成字幕
4. **指定语言**：提高识别准确率
5. **处理流式背压**：实时转录时注意处理
6. **关闭转录会话**：完成后及时关闭

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确符合上述描述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
