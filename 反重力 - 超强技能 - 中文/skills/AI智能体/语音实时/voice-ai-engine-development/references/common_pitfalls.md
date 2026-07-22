# 常见陷阱与解决方案

本文档介绍构建语音 AI 引擎时常见的若干问题及其解决方案。

## 1. 音频跳跃/截断

### 问题
机器人的音频在回复中出现跳跃或截断，给用户造成刺耳的体验。

### 症状
- 音频以碎片形式播放
- 句子不完整
- 多个音频流重叠
- 不自然的停顿或间断

### 根本原因
将文本以小块形式（逐句或逐词）送往合成器，会触发多次 TTS API 调用。每次调用都会生成独立的音频流，从而导致：
- 多个音频文件按序播放
- 块之间的时序错位
- 音频可能重叠
- 各块的音色特征不一致

### 解决方案
在送往合成器前先缓存完整的 LLM 回复：

**❌ 错误：逐句 yield**
```python
async def generate_response(self, prompt):
    async for sentence in llm_stream:
        # This creates multiple TTS calls!
        yield GeneratedResponse(message=BaseMessage(text=sentence))
```

**✅ 正确：缓存完整回复**
```python
async def generate_response(self, prompt):
    # Buffer the entire response
    full_response = ""
    async for chunk in llm_stream:
        full_response += chunk
    
    # Yield once with complete response
    yield GeneratedResponse(message=BaseMessage(text=full_response))
```

### 为什么这样做有效
- 整段回复只调用一次 TTS
- 音色特征保持一致
- 时序与节奏正常
- 没有间断或重叠

---

## 2. 回声/反馈环路

### 问题
机器人听到自己说话并对自身音频进行回复，形成无限循环。

### 症状
- 机器人回应自己说过的话
- 对话变得毫无意义
- 转写结果中混入了机器人自己的话
- 系统失去响应

### 根本原因
机器人在说话时转写器仍在处理音频。如果机器人的音频从扬声器播放并被麦克风重新采集，转写器就会把机器人自己的语音也转写下来。

### 解决方案
在机器人开始说话时静音转写器：

```python
# Before sending audio to output
self.transcriber.mute()

# Send audio...
await self.send_speech_to_output(synthesis_result)

# After audio playback complete
self.transcriber.unmute()
```

### 在转写器中的实现
```python
class BaseTranscriber:
    def __init__(self):
        self.is_muted = False
    
    def send_audio(self, chunk: bytes):
        """Client calls this to send audio"""
        if not self.is_muted:
            self.input_queue.put_nowait(chunk)
        else:
            # Send silence instead (prevents echo)
            self.input_queue.put_nowait(self.create_silent_chunk(len(chunk)))
    
    def mute(self):
        """Called when bot starts speaking"""
        self.is_muted = True
    
    def unmute(self):
        """Called when bot stops speaking"""
        self.is_muted = False
    
    def create_silent_chunk(self, size: int) -> bytes:
        """Create a silent audio chunk"""
        return b'\x00' * size
```

### 为什么这样做有效
- 机器人说话时转写器收到静音
- 不会转写机器人自己的语音
- 避免反馈环路
- 保持音频流的连续性

---

## 3. 打断不生效

### 问题
用户无法在句中打断机器人，机器人即使在用户开始说话时仍继续讲下去。

### 症状
- 机器人盖过用户声音
- 用户必须等机器人讲完
- 对话节奏不自然
- 用户体验差

### 根本原因
所有音频块被立即发送给客户端，整条消息在客户端被缓存。等到检测到打断时，音频早已全部发出并排队等待回放。

### 解决方案
按实时回放速率限制音频块：

**❌ 错误：立即发送所有块**
```python
async for chunk in synthesis_result.chunk_generator:
    # Sends all chunks as fast as possible
    output_device.consume_nonblocking(chunk)
```

**✅ 正确：速率限制块**
```python
async for chunk in synthesis_result.chunk_generator:
    # Check for interrupt
    if stop_event.is_set():
        # Calculate partial message
        partial_message = synthesis_result.get_message_up_to(
            chunk_idx * seconds_per_chunk
        )
        return partial_message, True  # cut_off = True
    
    start_time = time.time()
    
    # Send chunk
    output_device.consume_nonblocking(chunk)
    
    # CRITICAL: Wait for chunk duration before sending next
    processing_time = time.time() - start_time
    await asyncio.sleep(max(seconds_per_chunk - processing_time, 0))
    
    chunk_idx += 1
```

### 为什么这样做有效
- 客户端每次只缓存一个块
- 可以在句中触发打断
- 对话节奏自然
- 保持实时回放

### 计算 `seconds_per_chunk`
```python
# For LINEAR16 PCM audio at 16kHz
sample_rate = 16000  # Hz
chunk_size = 1024    # bytes
bytes_per_sample = 2  # 16-bit = 2 bytes

samples_per_chunk = chunk_size / bytes_per_sample
seconds_per_chunk = samples_per_chunk / sample_rate
# = 1024 / 2 / 16000 = 0.032 seconds
```

---

## 4. 流未关闭导致的内存泄漏

### 问题
内存使用随时间不断增长，最终导致应用崩溃。

### 症状
- 内存占用持续上升
- 性能随时间变慢
- WebSocket 连接未关闭
- 资源耗尽

### 根本原因
在对话结束或发生错误时，WebSocket 连接、API 流或异步任务未被正确关闭。

### 解决方案
始终使用上下文管理器并完成清理：

**❌ 错误：未做清理**
```python
async def handle_conversation(websocket):
    conversation = create_conversation()
    await conversation.start()
    
    async for message in websocket.iter_bytes():
        conversation.receive_audio(message)
    # No cleanup! Resources leak
```

**✅ 正确：妥善清理**
```python
async def handle_conversation(websocket):
    conversation = None
    try:
        conversation = create_conversation()
        await conversation.start()
        
        async for message in websocket.iter_bytes():
            conversation.receive_audio(message)
            
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        # Always cleanup
        if conversation:
            await conversation.terminate()
```

### 正确的终止流程
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
    
    # Cancel tasks
    for task in self.tasks:
        if not task.done():
            task.cancel()
```

---

## 5. 对话历史未更新

### 问题
智能体记不住之前的信息或上下文丢失。

### 症状
- 智能体重复自己说过的话
- 没有继承前文上下文
- 每次回复相互独立
- 对话质量差

### 根本原因
对话历史未被正确维护或更新。

### 解决方案
在智能体中维护对话历史：

```python
class Agent:
    def __init__(self):
        self.conversation_history = []
    
    async def generate_response(self, user_input):
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Generate response with full history
        response = await self.llm.generate(self.conversation_history)
        
        # Add bot response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
```

### 处理打断
当机器人被打断时，用部分消息更新历史：

```python
def update_last_bot_message_on_cut_off(self, partial_message):
    """Update history when bot is interrupted"""
    if self.conversation_history and \
       self.conversation_history[-1]["role"] == "assistant":
        # Update with what was actually spoken
        self.conversation_history[-1]["content"] = partial_message
```

---

## 6. WebSocket 连接中断

### 问题
WebSocket 连接意外断开，打断正在进行的对话。

### 症状
- 频繁断连
- 连接超时
- “Connection closed” 错误
- 对话不稳定

### 根本原因
- 缺少心跳/ping 机制
- 空闲超时
- 网络问题
- 服务端过载

### 解决方案
实现心跳与重连：

```python
@app.websocket("/conversation")
async def conversation_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Start heartbeat
    async def heartbeat():
        while True:
            try:
                await websocket.send_json({"type": "ping"})
                await asyncio.sleep(30)  # Ping every 30 seconds
            except:
                break
    
    heartbeat_task = asyncio.create_task(heartbeat())
    
    try:
        async for message in websocket.iter_bytes():
            # Process message
            pass
    finally:
        heartbeat_task.cancel()
```

---

## 7. 高延迟 / 回复过慢

### 问题
用户说话与机器人回复之间存在较长延迟。

### 症状
- 明显的滞后感
- 用户体验差
- 对话节奏不自然
- 用户被迫重复

### 根本原因与解决方案

**1. 未使用流式**
```python
# ❌ Bad: Wait for entire response
response = await llm.complete(prompt)

# ✅ Good: Stream response
async for chunk in llm.complete(prompt, stream=True):
    yield chunk
```

**2. 顺序处理**
```python
# ❌ Bad: Sequential
transcription = await transcriber.transcribe(audio)
response = await agent.generate(transcription)
audio = await synthesizer.synthesize(response)

# ✅ Good: Concurrent with queues
# All workers run simultaneously
```

**3. 块尺寸过大**
```python
# ❌ Bad: Large chunks (high latency)
chunk_size = 8192  # 0.25 seconds

# ✅ Good: Small chunks (low latency)
chunk_size = 1024  # 0.032 seconds
```

---

## 8. 音质问题

### 问题
音质差、有失真或出现伪迹。

### 症状
- 机械感的声音
- 噼啪或爆音
- 音频失真
- 音量不一致

### 根本原因与解决方案

**1. 音频格式错误**
```python
# ✅ Use LINEAR16 PCM at 16kHz
audio_encoding = AudioEncoding.LINEAR16
sample_rate = 16000
```

**2. 格式转换不正确**
```python
# ✅ Proper MP3 to PCM conversion
from pydub import AudioSegment
import io

def mp3_to_pcm(mp3_bytes):
    audio = AudioSegment.from_mp3(io.BytesIO(mp3_bytes))
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)
    audio = audio.set_sample_width(2)  # 16-bit
    return audio.raw_data
```

**3. 缓冲区欠载**
```python
# ✅ Ensure consistent chunk timing
await asyncio.sleep(max(seconds_per_chunk - processing_time, 0))
```

---

## 总结

| 问题 | 根本原因 | 解决方案 |
|------|----------|----------|
| 音频跳跃 | 多次 TTS 调用 | 缓存完整回复 |
| 回声/反馈 | 机器人说话时转写器仍工作 | 静音转写器 |
| 打断不生效 | 块被立即全部发出 | 速率限制块 |
| 内存泄漏 | 流未关闭 | 妥善清理 |
| 上下文丢失 | 历史未维护 | 更新对话历史 |
| 连接中断 | 缺少心跳 | 实现 ping/pong |
| 高延迟 | 顺序处理 | 使用流式 + 队列 |
| 音质差 | 格式/转换错误 | 使用 LINEAR16 PCM 16kHz |

---

## 最佳实践

1. **始终缓存 LLM 回复**，再送往合成器
2. **始终静音转写器**，当机器人说话时
3. **始终对音频块进行速率限制**，以支持打断
4. **始终在 finally 块中清理资源**
5. **始终维护对话历史**以保留上下文
6. **始终使用流式**以获得更低延迟
7. **始终使用 LINEAR16 PCM** 16kHz 处理音频
8. **始终在 worker 循环中实现错误处理**
