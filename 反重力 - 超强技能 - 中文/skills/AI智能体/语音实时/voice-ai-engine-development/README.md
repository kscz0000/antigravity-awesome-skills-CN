# 语音 AI 引擎开发技能

使用异步 worker 流水线、流式转写、LLM 智能体和 TTS 合成，构建生产级实时对话式 AI 语音引擎。

## 概述

本技能为构建语音 AI 引擎提供全面指导，使 AI 智能体能够与用户进行自然、双向的对话。内容覆盖从音频输入到音频输出的完整架构，包括：

- **异步 Worker 流水线模式** — 通过基于队列的通信实现并发处理
- **流式转写** — 实时语音转文字
- **LLM 驱动的智能体** — 具备上下文感知的对话 AI
- **文字转语音合成** — 自然流畅的语音生成
- **打断处理** — 用户可以在句中打断机器人
- **多提供商支持** — 轻松在不同服务商之间切换

## 快速开始

```python
# Use the skill in your AI assistant
@voice-ai-engine-development I need to build a voice assistant that can handle real-time conversations with interrupts
```

## 包含内容

### 主技能文件
- `SKILL.md` — 语音 AI 引擎开发的完整指南

### 示例
- `complete_voice_engine.py` — 完整可运行的实现
- `gemini_agent_example.py` — 带正确回复缓存的 LLM 智能体
- `interrupt_system_example.py` — 打断处理演示

### 模板
- `base_worker_template.py` — 创建新 worker 的模板
- `multi_provider_factory_template.py` — 多提供商工厂模式

### 参考
- `common_pitfalls.md` — 常见问题与解决方案
- `provider_comparison.md` — 转写、LLM 和 TTS 提供商对比

## 核心概念

### Worker 流水线模式

每个语音 AI 引擎都遵循以下流水线：

```
Audio In → Transcriber → Agent → Synthesizer → Audio Out
           (Worker 1)   (Worker 2)  (Worker 3)
```

每个 worker：
- 通过 asyncio 独立运行
- 通过 asyncio.Queue 对象通信
- 可以在流式过程中被停止以实现打断
- 优雅地处理错误

### 关键实现细节

1. **缓存 LLM 回复** — 在送往合成器前始终缓存完整的 LLM 回复，避免音频跳跃
2. **静音转写器** — 机器人说话时静音转写器，防止回声/反馈环路
3. **音频速率限制** — 按实时速度发送音频块，以支持打断
4. **妥善清理** — 始终在 finally 块中释放资源，避免内存泄漏

## 支持的提供商

### 转写
- Deepgram（速度最快，最适合实时）
- AssemblyAI（准确率最高）
- Azure Speech（企业级）
- Google Cloud Speech（多语言）

### LLM
- OpenAI GPT-4（质量最高）
- Google Gemini（性价比高）
- Anthropic Claude（注重安全）

### TTS
- ElevenLabs（声音最自然）
- Azure TTS（企业级）
- Google Cloud TTS（性价比高）
- Amazon Polly（AWS 集成）
- Play.ht（声音克隆）

## 常见使用场景

- 客服语音机器人
- 语音助手
- 电话自动化系统
- 语音应用
- 交互式语音应答（IVR）系统
- 语音辅导系统

## 架构亮点

### 异步 Worker 模式
```python
class BaseWorker:
    async def _run_loop(self):
        while self.active:
            item = await self.input_queue.get()
            await self.process(item)
```

### 打断机制
```python
# User interrupts bot mid-sentence
if stop_event.is_set():
    partial_message = get_message_up_to(seconds_spoken)
    return partial_message, True  # cut_off = True
```

### 多提供商工厂
```python
factory = VoiceComponentFactory()
transcriber = factory.create_transcriber(config)  # Deepgram, AssemblyAI, etc.
agent = factory.create_agent(config)              # OpenAI, Gemini, etc.
synthesizer = factory.create_synthesizer(config)  # ElevenLabs, Azure, etc.
```

## 测试

本技能包含以下示例：
- 单独单元测试各 worker
- 完整流水线的集成测试
- 打断功能测试
- 使用不同提供商的测试

## 最佳实践

1. ✅ 在每个阶段（转写、LLM、合成）始终使用流式
2. ✅ 在合成前缓存完整的 LLM 回复
3. ✅ 机器人说话时静音转写器
4. ✅ 速率限制音频块以支持打断
5. ✅ 维护对话历史以保留上下文
6. ✅ 在 worker 循环中使用合适的错误处理
7. ✅ 在 finally 块中清理资源
8. ✅ 音频使用 16kHz 的 LINEAR16 PCM

## 常见陷阱

详见 `references/common_pitfalls.md`，以下问题的详细解决方案：
- 音频跳跃/截断
- 回声/反馈环路
- 打断不生效
- 内存泄漏
- 对话上下文丢失
- 高延迟
- 音质差

## 贡献

本技能是 Antigravity Awesome Skills 仓库的一部分，欢迎贡献！

## 相关技能

- `@websocket-patterns` — WebSocket 实现
- `@async-python` — Asyncio 模式
- `@streaming-apis` — 流式 API 集成
- `@audio-processing` — 音频格式转换

## 许可证

MIT 许可证 — 详见仓库 LICENSE 文件

## 资源

- [Vocode 文档](https://docs.vocode.dev/)
- [Deepgram API](https://developers.deepgram.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [ElevenLabs API](https://elevenlabs.io/docs/)

---

**为 Antigravity 社区用 ❤️ 打造**
