---
name: transcribe-captions
description: "在 Remotion 中转录音频生成字幕。触发词：captions、transcribe、whisper、audio、speech-to-text、remotion"
metadata:
  tags: captions, transcribe, whisper, audio, speech-to-text
---

# 转录音频

Remotion 提供了多个内置选项用于转录音频以生成字幕：

- `@remotion/install-whisper-cpp` - 使用 Whisper.cpp 在服务器上本地转录。快速且免费，但需要服务器基础设施。
  https://remotion.dev/docs/install-whisper-cpp

- `@remotion/whisper-web` - 使用 WebAssembly 在浏览器中转录。无需服务器且免费，但由于 WASM 开销而较慢。
  https://remotion.dev/docs/whisper-web

- `@remotion/openai-whisper` - 使用 OpenAI Whisper API 进行基于云的转录。快速且无需服务器，但需要付费。
  https://remotion.dev/docs/openai-whisper/openai-whisper-api-to-captions