---
name: voice-ai-engine-development
description: "使用 async worker 流水线、流式转写、LLM 智能体和 TTS 合成构建实时对话式 AI 语音引擎，支持打断处理和多提供商切换"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 语音 AI 引擎开发

## 概述

本技能指导你构建具备实时对话能力的生产级语音 AI 引擎。语音 AI 引擎通过流式音频处理、语音转文字转写、LLM 驱动的回复生成以及文字转语音合成，实现用户与 AI 智能体之间自然的双向对话。

其核心架构采用基于异步队列的 worker 流水线：每个组件独立运行，通过 `asyncio.Queue` 对象相互通信，从而在每个阶段实现并发处理、打断处理和实时流式传输。

## 何时使用本技能

在以下场景使用本技能：
- 构建实时语音对话系统
- 实现语音助手或聊天机器人
- 打造支持语音的客服智能体
- 开发具备打断能力的语音 AI 应用
- 集成多个转写、LLM 或 TTS 提供商
- 涉及流式音频处理流水线
- 用户提及 Vocode、voice engine 或 conversational AI

## 核心架构原则

### Worker 流水线模式

每个语音 AI 引擎都遵循以下流水线：

```
Audio In → Transcriber → Agent → Synthesizer → Audio Out
           (Worker 1)   (Worker 2)  (Worker 3)
```

**关键优势：**
- **解耦**：各 worker 只知道自己的输入/输出队列
- **并发**：所有 worker 通过 asyncio 同时运行
- **背压**：队列自动处理速率差异
- **可打断**：流式过程中的任何环节都能被停止

### 基础 Worker 模式

每个 worker 都遵循以下模式：

```python
class BaseWorker:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue   # asyncio.Queue to consume from
        self.output_queue = output_queue # asyncio.Queue to produce to
        self.active = False
    
    def start(self):
        """Start the worker's processing loop"""
        self.active = True
        asyncio.create_task(self._run_loop())
    
    async def _run_loop(self):
        """Main processing loop - runs forever until terminated"""
        while self.active:
            item = await self.input_queue.get()  # Block until item arrives
            await self.process(item)              # Process the item
    
    async def process(self, item):
        """Override this - does the actual work"""
        raise NotImplementedError
    
    def terminate(self):
        """Stop the worker"""
        self.active = False
```

## 组件实现指南

### 1. 转写器（音频 → 文本）

**用途**：将输入的音频块转换为文本转写结果

**接口要求**：
```python
class BaseTranscriber:
    def __init__(self, transcriber_config):
        self.input_queue = asyncio.Queue()   # Audio chunks (bytes)
        self.output_queue = asyncio.Queue()  # Transcriptions
        self.is_muted = False
    
    def send_audio(self, chunk: bytes):
        """Client calls this to send audio"""
        if not self.is_muted:
            self.input_queue.put_nowait(chunk)
        else:
            # Send silence instead (prevents echo during bot speech)
            self.input_queue.put_nowait(self.create_silent_chunk(len(chunk)))
    
    def mute(self):
        """Called when bot starts speaking (prevents echo)"""
        self.is_muted = True
    
    def unmute(self):
        """Called when bot stops speaking"""
        self.is_muted = False
```

**输出格式**：
```python
class Transcription:
    message: str          # "Hello, how are you?"
    confidence: float     # 0.95
    is_final: bool        # True = complete sentence, False = partial
    is_interrupt: bool    # Set by TranscriptionsWorker
```

**支持的提供商**：
- **Deepgram** — 速度快、准确、支持流式
- **AssemblyAI** — 准确率高、对口音友好
- **Azure Speech** — 企业级
- **Google Cloud Speech** — 多语言支持

**关键实现细节**：
- 使用 WebSocket 进行双向流式通信
- 使用 `asyncio.gather()` 并发运行发送与接收任务
- 当机器人说话时静音转写器，防止回声/反馈环路
- 同时处理最终和部分转写结果

### 2. 智能体（文本 → 回复）

**用途**：处理用户输入并生成对话式回复

**接口要求**：
```python
class BaseAgent:
    def __init__(self, agent_config):
        self.input_queue = asyncio.Queue()   # TranscriptionAgentInput
        self.output_queue = asyncio.Queue()  # AgentResponse
        self.transcript = None               # Conversation history
    
    async def generate_response(self, human_input, is_interrupt, conversation_id):
        """Override this - returns AsyncGenerator of responses"""
        raise NotImplementedError
```

**为什么要使用流式回复？**
- **更低延迟**：第一个句子生成即可开始说话
- **更好的打断能力**：能在回复中途停止
- **逐句输出**：对话节奏更自然

**支持的提供商**：
- **OpenAI**（GPT-4、GPT-3.5）— 高质量、速度快
- **Google Gemini** — 多模态、性价比高
- **Anthropic Claude** — 长上下文、回复细腻

**关键实现细节**：
- 在 `Transcript` 对象中维护对话历史
- 使用 `AsyncGenerator` 流式返回回复
- **重要**：在向合成器提交前先缓存完整的 LLM 回复（避免音频跳跃）
- 发生打断时取消当前的生成任务
- 打断时使用部分消息更新对话历史

### 3. 合成器（文本 → 音频）

**用途**：将智能体的文本回复转换为语音音频

**接口要求**：
```python
class BaseSynthesizer:
    async def create_speech(self, message: BaseMessage, chunk_size: int) -> SynthesisResult:
        """
        Returns a SynthesisResult containing:
        - chunk_generator: AsyncGenerator that yields audio chunks
        - get_message_up_to: Function to get partial text (for interrupts)
        """
        raise NotImplementedError
```

**SynthesisResult 结构**：
```python
class SynthesisResult:
    chunk_generator: AsyncGenerator[ChunkResult, None]
    get_message_up_to: Callable[[float], str]  # seconds → partial text
    
    class ChunkResult:
        chunk: bytes          # Raw PCM audio
        is_last_chunk: bool
```

**支持的提供商**：
- **ElevenLabs** — 拟真度最高、支持流式
- **Azure TTS** — 企业级、语种丰富
- **Google Cloud TTS** — 性价比高、音质好
- **Amazon Polly** — 与 AWS 集成
- **Play.ht** — 支持声音克隆

**关键实现细节**：
- 边生成边流式输出音频块
- 将音频转换为 LINEAR16 PCM 格式（16kHz 采样率）
- 实现 `get_message_up_to()` 以支持打断
- 处理音频格式转换（MP3 → PCM）

### 4. 输出设备（音频 → 客户端）

**用途**：将合成好的音频发送回客户端

**关键：用于打断的速率限制**

```python
async def send_speech_to_output(self, message, synthesis_result,
                                stop_event, seconds_per_chunk):
    chunk_idx = 0
    async for chunk_result in synthesis_result.chunk_generator:
        # Check for interrupt
        if stop_event.is_set():
            logger.debug(f"Interrupted after {chunk_idx} chunks")
            message_sent = synthesis_result.get_message_up_to(
                chunk_idx * seconds_per_chunk
            )
            return message_sent, True  # cut_off = True
        
        start_time = time.time()
        
        # Send chunk to output device
        self.output_device.consume_nonblocking(chunk_result.chunk)
        
        # CRITICAL: Wait for chunk to play before sending next one
        # This is what makes interrupts work!
        speech_length = seconds_per_chunk
        processing_time = time.time() - start_time
        await asyncio.sleep(max(speech_length - processing_time, 0))
        
        chunk_idx += 1
    
    return message, False  # cut_off = False
```

**为什么要做速率限制？**
如果不进行速率限制，所有音频块会立即被发送，这会：
- 在客户端缓存整段消息
- 导致打断无法生效（音频早已全部发出）
- 引发时序问题

按每 N 秒发送一块的节奏：
- 保持实时回放
- 可以在句中触发打断
- 保留自然的对话节奏

## 打断机制

打断机制对于自然对话至关重要。

### 打断的工作原理

**场景**：机器人正在说“我觉得今天和明天的天气都会很——”，此时用户打断说“停”。

**第 1 步：用户开始说话**
```python
# TranscriptionsWorker detects new transcription while bot speaking
async def process(self, transcription):
    if not self.conversation.is_human_speaking:  # Bot was speaking!
        # Broadcast interrupt to all in-flight events
        interrupted = self.conversation.broadcast_interrupt()
        transcription.is_interrupt = interrupted
```

**第 2 步：broadcast_interrupt() 停止所有工作**
```python
def broadcast_interrupt(self):
    num_interrupts = 0
    # Interrupt all queued events
    while True:
        try:
            interruptible_event = self.interruptible_events.get_nowait()
            if interruptible_event.interrupt():  # Sets interruption_event
                num_interrupts += 1
        except queue.Empty:
            break
    
    # Cancel current tasks
    self.agent.cancel_current_task()              # Stop generating text
    self.agent_responses_worker.cancel_current_task()  # Stop synthesizing
    return num_interrupts > 0
```

**第 3 步：SynthesisResultsWorker 检测到打断**
```python
async def send_speech_to_output(self, synthesis_result, stop_event, ...):
    async for chunk_result in synthesis_result.chunk_generator:
        # Check stop_event (this is the interruption_event)
        if stop_event.is_set():
            logger.debug("Interrupted! Stopping speech.")
            # Calculate what was actually spoken
            seconds_spoken = chunk_idx * seconds_per_chunk
            partial_message = synthesis_result.get_message_up_to(seconds_spoken)
            # e.g., "I think the weather will be nice today"
            return partial_message, True  # cut_off = True
```

**第 4 步：智能体更新历史**
```python
if cut_off:
    # Update conversation history with partial message
    self.agent.update_last_bot_message_on_cut_off(message_sent)
    # History now shows:
    # Bot: "I think the weather will be nice today" (incomplete)
```

### InterruptibleEvent 模式

流水线中的每个事件都被包装成 `InterruptibleEvent`：

```python
class InterruptibleEvent:
    def __init__(self, payload, is_interruptible=True):
        self.payload = payload
        self.is_interruptible = is_interruptible
        self.interruption_event = threading.Event()  # Initially not set
        self.interrupted = False
    
    def interrupt(self) -> bool:
        """Interrupt this event"""
        if not self.is_interruptible:
            return False
        if not self.interrupted:
            self.interruption_event.set()  # Signal to stop!
            self.interrupted = True
            return True
        return False
    
    def is_interrupted(self) -> bool:
        return self.interruption_event.is_set()
```

## 多提供商工厂模式

使用工厂模式支持多个提供商：

```python
class VoiceHandler:
    """Multi-provider factory for voice components"""
    
    def create_transcriber(self, agent_config: Dict):
        """Create transcriber based on transcriberProvider"""
        provider = agent_config.get("transcriberProvider", "deepgram")
        
        if provider == "deepgram":
            return self._create_deepgram_transcriber(agent_config)
        elif provider == "assemblyai":
            return self._create_assemblyai_transcriber(agent_config)
        elif provider == "azure":
            return self._create_azure_transcriber(agent_config)
        elif provider == "google":
            return self._create_google_transcriber(agent_config)
        else:
            raise ValueError(f"Unknown transcriber provider: {provider}")
    
    def create_agent(self, agent_config: Dict):
        """Create LLM agent based on llmProvider"""
        provider = agent_config.get("llmProvider", "openai")
        
        if provider == "openai":
            return self._create_openai_agent(agent_config)
        elif provider == "gemini":
            return self._create_gemini_agent(agent_config)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    def create_synthesizer(self, agent_config: Dict):
        """Create voice synthesizer based on voiceProvider"""
        provider = agent_config.get("voiceProvider", "elevenlabs")
        
        if provider == "elevenlabs":
            return self._create_elevenlabs_synthesizer(agent_config)
        elif provider == "azure":
            return self._create_azure_synthesizer(agent_config)
        elif provider == "google":
            return self._create_google_synthesizer(agent_config)
        elif provider == "polly":
            return self._create_polly_synthesizer(agent_config)
        elif provider == "playht":
            return self._create_playht_synthesizer(agent_config)
        else:
            raise ValueError(f"Unknown voice provider: {provider}")
```

## WebSocket 集成

语音 AI 引擎通常使用 WebSocket 进行双向音频流式传输：

```python
@app.websocket("/conversation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Create voice components
    voice_handler = VoiceHandler()
    transcriber = voice_handler.create_transcriber(agent_config)
    agent = voice_handler.create_agent(agent_config)
    synthesizer = voice_handler.create_synthesizer(agent_config)
    
    # Create output device
    output_device = WebsocketOutputDevice(
        ws=websocket,
        sampling_rate=16000,
        audio_encoding=AudioEncoding.LINEAR16
    )
    
    # Create conversation orchestrator
    conversation = StreamingConversation(
        output_device=output_device,
        transcriber=transcriber,
        agent=agent,
        synthesizer=synthesizer
    )
    
    # Start all workers
    await conversation.start()
    
    try:
        # Receive audio from client
        async for message in websocket.iter_bytes():
            conversation.receive_audio(message)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    finally:
        await conversation.terminate()
```

## 常见陷阱与解决方案

### 1. 音频跳跃/截断

**问题**：机器人音频在回复中跳跃或被截断。

**原因**：将文本以小块形式送往合成器，导致多次调用 TTS。

**解决方案**：在送往合成器前先缓存完整的 LLM 回复：

```python
# ❌ Bad: Yields sentence-by-sentence
async for sentence in llm_stream:
    yield GeneratedResponse(message=BaseMessage(text=sentence))

# ✅ Good: Buffer entire response
full_response = ""
async for chunk in llm_stream:
    full_response += chunk
yield GeneratedResponse(message=BaseMessage(text=full_response))
```

### 2. 回声/反馈环路

**问题**：机器人听到自己说话并对自身音频进行回复。

**原因**：机器人在说话时转写器未被静音。

**解决方案**：在机器人开始说话时静音转写器：

```python
# Before sending audio to output
self.transcriber.mute()
# After audio playback complete
self.transcriber.unmute()
```

### 3. 打断不生效

**问题**：用户无法在句中打断机器人。

**原因**：所有音频块一次性发送，未做速率限制。

**解决方案**：按真实回放速率限制音频块：

```python
async for chunk in synthesis_result.chunk_generator:
    start_time = time.time()
    
    # Send chunk
    output_device.consume_nonblocking(chunk)
    
    # Wait for chunk duration before sending next
    processing_time = time.time() - start_time
    await asyncio.sleep(max(seconds_per_chunk - processing_time, 0))
```

### 4. 流未关闭导致的内存泄漏

**问题**：内存使用随时间不断增长。

**原因**：WebSocket 连接或 API 流未正确关闭。

**解决方案**：始终使用上下文管理器并完成清理：

```python
try:
    async with websockets.connect(url) as ws:
        # Use websocket
        pass
finally:
    # Cleanup
    await conversation.terminate()
    await transcriber.terminate()
```

## 生产环境考量

### 1. 错误处理

```python
async def _run_loop(self):
    while self.active:
        try:
            item = await self.input_queue.get()
            await self.process(item)
        except Exception as e:
            logger.error(f"Worker error: {e}", exc_info=True)
            # Don't crash the worker, continue processing
```

### 2. 优雅停机

```python
async def terminate(self):
    """Gracefully shut down all workers"""
    self.active = False
    
    # Stop all workers
    self.transcriber.terminate()
    self.agent.terminate()
    self.synthesizer.terminate()
    
    # Wait for queues to drain
    await asyncio.sleep(0.5)
    
    # Close connections
    if self.websocket:
        await self.websocket.close()
```

### 3. 监控与日志

```python
# Log key events
logger.info(f"🎤 [TRANSCRIBER] Received: '{transcription.message}'")
logger.info(f"🤖 [AGENT] Generating response...")
logger.info(f"🔊 [SYNTHESIZER] Synthesizing {len(text)} characters")
logger.info(f"⚠️ [INTERRUPT] User interrupted bot")

# Track metrics
metrics.increment("transcriptions.count")
metrics.timing("agent.response_time", duration)
metrics.gauge("active_conversations", count)
```

### 4. 速率限制与配额

```python
# Implement rate limiting for API calls
from aiolimiter import AsyncLimiter

rate_limiter = AsyncLimiter(max_rate=10, time_period=1)  # 10 calls/second

async def call_api(self, data):
    async with rate_limiter:
        return await self.client.post(data)
```

## 关键设计模式

### 1. 基于队列的生产者-消费者

```python
# Producer
async def producer(queue):
    while True:
        item = await generate_item()
        queue.put_nowait(item)

# Consumer
async def consumer(queue):
    while True:
        item = await queue.get()
        await process_item(item)
```

### 2. 流式生成器

不要一次性返回完整结果：

```python
# ❌ Bad: Wait for entire response
async def generate_response(prompt):
    response = await openai.complete(prompt)  # 5 seconds
    return response

# ✅ Good: Stream chunks as they arrive
async def generate_response(prompt):
    async for chunk in openai.complete(prompt, stream=True):
        yield chunk  # Yield after 0.1s, 0.2s, etc.
```

### 3. 对话状态管理

维护对话历史以保留上下文：

```python
class Transcript:
    event_logs: List[Message] = []
    
    def add_human_message(self, text):
        self.event_logs.append(Message(sender=Sender.HUMAN, text=text))
    
    def add_bot_message(self, text):
        self.event_logs.append(Message(sender=Sender.BOT, text=text))
    
    def to_openai_messages(self):
        return [
            {"role": "user" if msg.sender == Sender.HUMAN else "assistant",
             "content": msg.text}
            for msg in self.event_logs
        ]
```

## 测试策略

### 1. 单独单元测试各 Worker

```python
async def test_transcriber():
    transcriber = DeepgramTranscriber(config)
    
    # Mock audio input
    audio_chunk = b'\x00\x01\x02...'
    transcriber.send_audio(audio_chunk)
    
    # Check output
    transcription = await transcriber.output_queue.get()
    assert transcription.message == "expected text"
```

### 2. 流水线集成测试

```python
async def test_full_pipeline():
    # Create all components
    conversation = create_test_conversation()
    
    # Send test audio
    conversation.receive_audio(test_audio_chunk)
    
    # Wait for response
    response = await wait_for_audio_output(timeout=5)
    
    assert response is not None
```

### 3. 测试打断

```python
async def test_interrupt():
    conversation = create_test_conversation()
    
    # Start bot speaking
    await conversation.agent.generate_response("Tell me a long story")
    
    # Interrupt mid-response
    await asyncio.sleep(1)  # Let it speak for 1 second
    conversation.broadcast_interrupt()
    
    # Verify partial message in transcript
    last_message = conversation.transcript.event_logs[-1]
    assert last_message.text != full_expected_message
```

## 实施工作流

实现语音 AI 引擎时：

1. **从基础 Worker 开始**：先实现基础 worker 模式
2. **加入转写器**：选择提供商并实现流式转写
3. **加入智能体**：实现 LLM 集成与流式回复
4. **加入合成器**：实现带音频流式输出的 TTS
5. **连接流水线**：通过队列将各 worker 串联起来
6. **加入打断**：实现打断机制
7. **加入 WebSocket**：创建 WebSocket 端点用于客户端通信
8. **组件测试**：单独对每个 worker 进行单元测试
9. **集成测试**：对完整流水线进行端到端测试
10. **加入错误处理**：实现健壮的错误处理与日志
11. **性能优化**：加入速率限制、监控和性能优化

## 相关技能

- `@websocket-patterns` — WebSocket 实现细节
- `@async-python` — asyncio 与异步模式
- `@streaming-apis` — 流式 API 集成
- `@audio-processing` — 音频格式转换与处理
- `@systematic-debugging` — 调试复杂的异步流水线

## 资源

**库**：
- `asyncio` — 异步编程
- `websockets` — WebSocket 客户端/服务端
- `FastAPI` — WebSocket 服务端框架
- `pydub` — 音频处理
- `numpy` — 音频数据处理

**API 提供商**：
- 转写：Deepgram、AssemblyAI、Azure Speech、Google Cloud Speech
- LLM：OpenAI、Google Gemini、Anthropic Claude
- TTS：ElevenLabs、Azure TTS、Google Cloud TTS、Amazon Polly、Play.ht

## 小结

构建语音 AI 引擎需要：
- ✅ 异步 worker 流水线实现并发处理
- ✅ 基于队列的组件间通信
- ✅ 每一阶段都进行流式处理（转写、LLM、合成）
- ✅ 支持自然对话的打断机制
- ✅ 用于实时音频回放的速率限制
- ✅ 多提供商支持以提高灵活性
- ✅ 完善的错误处理与优雅停机

**关键洞察**：所有环节都必须支持流式和可打断，才能实现自然、实时的对话。

## 局限
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来主动询问。
