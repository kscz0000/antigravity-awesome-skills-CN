---
name: voice-agents
description: 语音代理代表了AI交互的前沿 - 人类与AI系统自然对话。触发词：voice agent、speech to text、text to speech、whisper、elevenlabs、deepgram、realtime api、voice assistant、voice ai、conversational ai、tts、stt、asr。
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 语音代理

语音代理代表了AI交互的前沿 - 人类与AI系统自然对话。挑战不仅在于语音识别与合成，更在于以低于800毫秒的延迟实现自然的对话流，同时处理打断、背景噪音和情感细微差别。

本技能涵盖两种架构：语音到语音（OpenAI Realtime API，最低延迟、最自然）和管道式（STT→LLM→TTS，更可控、更易调试）。关键洞察：延迟是约束条件。人类期望在500毫秒内得到响应，每一毫秒都至关重要。

2025年84%的组织正在增加语音AI预算。今年是语音代理走向主流的一年。

## 原则

- 延迟是约束条件 - 目标端到端 <800毫秒
- 抖动（方差）与绝对延迟同等重要
- VAD质量决定对话流畅度
- 打断处理决定体验的成败
- 从聚焦的MVP起步，根据真实对话迭代
- 组合最佳组件（Deepgram STT + ElevenLabs TTS）

## 能力

- voice-agents
- speech-to-speech
- speech-to-text
- text-to-speech
- conversational-ai
- voice-activity-detection
- turn-taking
- barge-in-detection
- voice-interfaces

## 范围

- phone-system-integration → backend
- audio-processing-dsp → audio-specialist
- music-generation → audio-specialist
- accessibility-compliance → accessibility-specialist

## 工具

### 语音到语音

- OpenAI Realtime API - 何时使用：最低延迟、最自然的对话。注意：gpt-4o-realtime-preview，原生语音，低于500毫秒
- Pipecat - 何时使用：开源语音编排。注意：Daily支持，企业级，模块化

### 语音到文本

- OpenAI Whisper - 何时使用：最高精度、多语言。注意：gpt-4o-transcribe效果最佳
- Deepgram Nova-3 - 何时使用：生产负载，WER降低54%。注意：150-184毫秒TTFT，嘈杂音频下90%+准确率
- AssemblyAI - 何时使用：实时流式、说话人分离。注意：精度与延迟平衡良好

### 文本到语音

- ElevenLabs - 何时使用：最自然的语音、情感控制。注意：Flash模型75毫秒延迟，V3支持表达力
- OpenAI TTS - 何时使用：与OpenAI技术栈集成。注意：gpt-4o-mini-tts，13种语音，支持流式
- Deepgram Aura-2 - 何时使用：经济高效的生产TTS。注意：比ElevenLabs便宜40%，TTFB为184毫秒

### 框架

- Pipecat - 何时使用：开源语音代理编排。注意：Silero VAD、SmartTurn、打断处理
- Vapi - 何时使用：托管式语音代理平台。注意：无需基础设施管理
- Retell AI - 何时使用：低延迟语音代理。注意：打断时上下文保持最佳

## 模式

### 语音到语音架构

直接音频到音频处理以实现最低延迟

**何时使用**：追求最大自然度、情感保留、实时对话

# 语音到语音架构：

"""
[用户音频] → [S2S模型] → [代理音频]

优势：
- 最低延迟（低于500毫秒）
- 保留情感、强调、口音
- 最自然的对话流

劣势：
- 对响应的控制较少
- 更难调试/审计
- 无法轻松修改所说内容
"""

## OpenAI Realtime API
"""
import { RealtimeClient } from '@openai/realtime-api-beta';

const client = new RealtimeClient({
  apiKey: process.env.OPENAI_API_KEY,
});

// 配置语音对话
client.updateSession({
  modalities: ['text', 'audio'],
  voice: 'alloy',
  input_audio_format: 'pcm16',
  output_audio_format: 'pcm16',
  instructions: `You are a helpful customer service agent.
    Be concise and friendly. If you don't know something,
    say so rather than making things up.`,
  turn_detection: {
    type: 'server_vad',  // 或 'semantic_vad'
    threshold: 0.5,
    prefix_padding_ms: 300,
    silence_duration_ms: 500,
  },
});

// 处理音频流
client.on('conversation.item.input_audio_transcription', (event) => {
  console.log('User said:', event.transcript);
});

client.on('response.audio.delta', (event) => {
  // 将音频流式传输到扬声器
  audioPlayer.write(Buffer.from(event.delta, 'base64'));
});

// 发送用户音频
client.appendInputAudio(audioBuffer);
"""

## 使用场景：
- 实时客户支持
- 语音助手
- 交互式语音应答（IVR）
- 实时语言翻译

### 管道式架构

分离的 STT → LLM → TTS 以实现最大控制

**何时使用**：需要知道/控制具体所说内容、调试、合规性

# 管道式架构：

"""
[音频] → [STT] → [文本] → [LLM] → [文本] → [TTS] → [音频]

优势：
- 每一步完全可控
- 可记录/审计所有文本
- 易于调试
- 可混用最佳组件

劣势：
- 延迟较高（通常700-1200毫秒）
- 丢失部分情感/细微差别
- 需要管理更多组件
"""

## 生产管道示例
"""
import { Deepgram } from '@deepgram/sdk';
import { ElevenLabsClient } from 'elevenlabs';
import OpenAI from 'openai';

// 初始化客户端
const deepgram = new Deepgram(process.env.DEEPGRAM_API_KEY);
const elevenlabs = new ElevenLabsClient();
const openai = new OpenAI();

async function processVoiceInput(audioStream) {
  // 1. 语音到文本（Deepgram Nova-3）
  const transcription = await deepgram.transcription.live({
    model: 'nova-3',
    punctuate: true,
    endpointing: 300,  // 结束前的静默毫秒数
  });

  transcription.on('transcript', async (data) => {
    if (data.is_final && data.speech_final) {
      const userText = data.channel.alternatives[0].transcript;
      console.log('User:', userText);

      // 2. LLM处理
      const completion = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: [
          { role: 'system', content: 'You are a concise voice assistant.' },
          { role: 'user', content: userText }
        ],
        max_tokens: 150,  // 保持语音响应简短
      });

      const agentText = completion.choices[0].message.content;
      console.log('Agent:', agentText);

      // 3. 文本到语音（ElevenLabs）
      const audioStream = await elevenlabs.textToSpeech.stream({
        voice_id: 'voice_id_here',
        text: agentText,
        model_id: 'eleven_flash_v2_5',  // 最低延迟
      });

      // 流式播放给用户
      playAudioStream(audioStream);
    }
  });

  // 将音频管道传输到转录
  audioStream.pipe(transcription);
}
"""

## 优化技巧：
- LLM仍在生成时启动TTS（流式）
- 在用户说话期间预计算第一段响应
- 使用Flash/turbo模型以降低延迟

### 语音活动检测模式

检测用户何时开始/停止说话

**何时使用**：所有语音代理都需要VAD以进行轮次管理

# 语音活动检测（VAD）：

"""
VAD类型：
1. 基于能量：简单、快速、对噪音敏感
2. 基于模型：Silero VAD，更准确
3. 语义VAD：理解语义，最适合对话
"""

## Silero VAD（流行的开源方案）
"""
import { SileroVAD } from '@pipecat-ai/silero-vad';

const vad = new SileroVAD({
  threshold: 0.5,           // 语音概率阈值
  min_speech_duration: 250, // 确认语音前的毫秒数
  min_silence_duration: 500, // 静默毫秒数 = 轮次结束
});

vad.on('speech_start', () => {
  console.log('User started speaking');
  // 停止任何正在播放的TTS（打断）
  audioPlayer.stop();
});

vad.on('speech_end', () => {
  console.log('User finished speaking');
  // 触发响应生成
  processTranscript();
});

// 将音频送入VAD
audioStream.on('data', (chunk) => {
  vad.process(chunk);
});
"""

## OpenAI 语义VAD
"""
// 在Realtime API会话配置中
client.updateSession({
  turn_detection: {
    type: 'semantic_vad',  // 使用语义而非仅静默
    // 在"嗯..."后等待更久
    // 在"是的，没错。"后更快响应
  },
});
"""

## 打断处理
"""
// 当用户打断时：
function handleBargeIn() {
  // 1. 立即停止TTS
  audioPlayer.stop();

  // 2. 取消待处理的LLM生成
  llmController.abort();

  // 3. 重置状态
  conversationState.checkpoint();

  // 4. 监听新输入
  startListening();
}

// VAD触发打断
vad.on('speech_start', () => {
  if (audioPlayer.isPlaying) {
    handleBargeIn();
  }
});
"""

### 延迟优化模式

实现端到端响应时间 <800毫秒

**何时使用**：生产环境语音代理

# 延迟优化：

"""
目标指标：
- 端到端：<800毫秒（理想：<500毫秒）
- 首Token时间（TTFT）：<300毫秒
- 打断响应：<200毫秒
- 抖动方差：标准差<100毫秒
"""

## 管道延迟细分
"""
典型细分：
- VAD处理：50-100毫秒
- STT首结果：150-200毫秒
- LLM TTFT：100-300毫秒
- TTS TTFA：75-200毫秒
- 音频缓冲：50-100毫秒

总计：425-900毫秒
"""

## 优化策略

### 1. 全程流式
"""
// 实时流式转录STT结果
stt.on('partial_transcript', (text) => {
  // 在最终转录前开始处理
  llmPreprocessor.prepare(text);
});

// 将LLM输出流式传输到TTS
const llmStream = await openai.chat.completions.create({
  stream: true,
  // ...
});

for await (const chunk of llmStream) {
  tts.appendText(chunk.choices[0].delta.content);
}
"""

### 2. 预计算
"""
// 在用户说话时，预测并准备
stt.on('partial_transcript', async (text) => {
  // 预取相关上下文
  const context = await retrieveContext(text);

  // 预计算可能的第一句
  const firstSentence = await generateOpener(context);
});
"""

### 3. 使用低延迟模型
"""
// STT：Deepgram Nova-3（150毫秒 TTFT）
// LLM：gpt-4o-mini（GPT-4类中最快）
// TTS：ElevenLabs Flash（75毫秒）或 Deepgram Aura-2（184毫秒）
"""

### 4. 边缘部署
"""
// 在更靠近用户的地方运行推理
// - 邻近用户的云区域
// - VAD/STT的边缘计算
// - WebSocket而非HTTP以降低开销
"""

### 对话设计模式

设计自然的语音对话

**何时使用**：构建语音UX

# 对话设计：

## 语音优先原则
"""
语音与文本不同：
- 没有撤销按钮 - 第一次就要说对
- 线性 - 用户无法回滚
- 瞬时性 - 容易错过信息
- 情感性 - 语气与文字同样重要
"""

## 响应设计
"""
# 保持响应简短（最长10-20秒）
# 把答案放在前面
# 为列表使用提示语

不好："我找到了几个选项。第一个是...第二个是..."
好："我找到3个选项。要我逐一介绍吗？"

# 确认理解
不好："我将向John转账500美元。"
好："也就是向John Smith转账500美元。可以继续吗？"
"""

## 语音提示
"""
system_prompt = '''
你是一个语音助手。遵循以下规则：

1. 简洁 - 响应控制在30字以内
2. 使用自然语言 - 缩写、口语
3. 绝不使用格式（项目符号、列表编号）
4. 拼出数字和缩写
5. 以问题结束以保持对话流畅
6. 如不清楚，请求澄清
7. 除非被问及，不要说"我是AI"

好："好的。我会把提醒设在下午三点。还有别的吗？"
坏："我已经设置了一个下午3:00的提醒。今天还有什么我可以帮您的吗？"
'''
"""

## 错误恢复
"""
// 优雅处理识别错误
const errorResponses = {
  no_speech: "我没听清楚。能再说一遍吗？",
  unclear: "抱歉，我不太确定我理解对了。你说的是[重复]。是这样吗？",
  timeout: "还在吗？我在这里，随时可以继续。",
};

// 始终为复杂问题提供人工后备
if (confidenceScore < 0.6) {
  response = "我想确保我没理解错。你想和人工客服聊聊吗？";
}
"""

## 尖锐问题

### 响应延迟超过800毫秒

严重程度：CRITICAL

场景：构建语音代理管道

症状：
对话感觉尴尬。用户重复自己的话。"你还在吗？"的问题。用户挂断或放弃。尽管答案正确，但满意度低。

为什么会失败：
在人类对话中，响应通常在500毫秒内到达。任何超过800毫秒的响应都让人觉得代理迟钝或困惑。用户失去信心和耐心。每个组件都会增加延迟：VAD（100毫秒）+ STT（200毫秒）+ LLM（300毫秒）+ TTS（200毫秒）= 800毫秒。

推荐修复：

# 测量并为每个组件分配延迟预算：

## 目标延迟：
- VAD处理：<100毫秒
- STT首Token时间：<200毫秒
- LLM首Token时间：<300毫秒
- TTS首音频时间：<150毫秒
- 端到端总计：<800毫秒

## 优化策略：

1. 使用低延迟模型：
   - STT：Deepgram Nova-3（150毫秒）对比 Whisper（500毫秒+）
   - TTS：ElevenLabs Flash（75毫秒）对比 标准（200毫秒+）
   - LLM：gpt-4o-mini 流式

2. 全程流式：
   - 不要等待完整的STT转录
   - 将LLM输出流式传输到TTS
   - 在TTS完成前开始音频播放

3. 预计算：
   - 在用户说话时准备上下文
   - 并行生成开场白

4. 边缘部署：
   - 在边缘运行VAD/STT
   - 使用最近的云区域

## 持续测量：
在每个阶段记录时间戳，跟踪P50/P95延迟

### 响应时间方差破坏节奏

严重程度：HIGH

场景：响应时间不一致的语音代理

症状：
对话感觉不可预测。用户不知道何时该说话。有时代理立即响应，有时长时间停顿后响应。用户与代理抢话，代理与用户抢话。

为什么会失败：
抖动（响应时间方差）对对话节奏的破坏超过绝对延迟。始终如一的800毫秒感觉比400毫秒和1200毫秒交替好。用户无法适应不可预测的时机。

推荐修复：

# 抖动指标目标：
- 标准差：<100毫秒
- P95-P50差距：<200毫秒

## 减少抖动来源：

1. 一致的模型加载：
   - 保持模型热加载
   - 在连接开始时预加载

2. 缓冲音频输出：
   - 小缓冲区（50-100毫秒）平滑播放
   - 在缓冲填满前不要开始播放

3. 处理LLM方差：
   - gpt-4o-mini比更大的模型更稳定
   - 设置 max_tokens 限制长响应

4. 监控和告警：
   - 跟踪响应时间分布
   - 抖动峰值时告警

## 实现：
const MIN_RESPONSE_TIME = 400;  // 毫秒

async function respondWithConsistentTiming(text) {
  const startTime = Date.now();
  const audio = await generateSpeech(text);

  const elapsed = Date.now() - startTime;
  if (elapsed < MIN_RESPONSE_TIME) {
    await delay(MIN_RESPONSE_TIME - elapsed);
  }

  playAudio(audio);
}

### 使用静默时长进行轮次检测

严重程度：HIGH

场景：检测用户何时说完

症状：
代理在用户思考中途打断。或在用户说完后等待太久。"让我想想..."触发过早响应。简短回答在响应前有尴尬的停顿。

为什么会失败：
简单的静默检测（例如"500毫秒静默后结束轮次"）不理解对话。人类会在句子中间停顿。"是的。"需要快速响应，"嗯，让我想想..."则需要耐心。固定超时两者都不适合。

推荐修复：

# 使用语义VAD：

## OpenAI 语义VAD：
client.updateSession({
  turn_detection: {
    type: 'semantic_vad',
    // 在"嗯..."后等待更久
    // 在"是的，没错。"后更快响应
  },
});

## Pipecat SmartTurn：
const pipeline = new Pipeline({
  vad: new SileroVAD(),
  turnDetection: new SmartTurn(),
});

// SmartTurn 考虑：
// - 语音内容（完整句子？）
// - 韵律（语调下降？）
// - 上下文（问过问题？）

## 后备方案：自适应静默阈值：
function calculateSilenceThreshold(transcript) {
  const endsWithComplete = transcript.match(/[.!?]$/);
  const hasFillers = transcript.match(/um|uh|like|well/i);

  if (endsWithComplete && !hasFillers) {
    return 300;  // 快速响应
  } else if (hasFillers) {
    return 1500;  // 等待继续
  }
  return 700;  // 默认
}

### 用户打断时代理未停止

严重程度：HIGH

场景：用户试图在代理说话中途打断

症状：
代理与用户抢话。用户必须等待代理说完。令人沮丧的体验。用户放弃并挂断电话。"停！停！"不起作用。

为什么会失败：
没有打断处理，TTS会播放完毕而不管用户输入。这违反了基本的对话规范 - 在人类对话中，我们被打断时会停下来。

推荐修复：

# 实现打断检测：

## 基本打断：
vad.on('speech_start', () => {
  if (ttsPlayer.isPlaying) {
    // 1. 立即停止音频
    ttsPlayer.stop();

    // 2. 取消待处理的TTS生成
    ttsController.abort();

    // 3. 检查点对话状态
    conversationState.save();

    // 4. 监听新输入
    startTranscription();
  }
});

## 高级：区分打断类型：
vad.on('speech_start', async () => {
  if (!ttsPlayer.isPlaying) return;

  // 等待200毫秒获取首词
  await delay(200);
  const firstWords = getTranscriptSoFar();

  if (isBackchannel(firstWords)) {
    // "嗯嗯"、"是的" - 不打断
    return;
  }

  if (isClarification(firstWords)) {
    // "什么？"、"抱歉？" - 重复最后一句
    repeatLastSentence();
  } else {
    // 真正的打断 - 停止并倾听
    handleFullInterruption();
  }
});

## 响应时间目标：
- 打断响应：<200毫秒
- 用户应立即感到被听到

### 为语音生成长度不一的响应

严重程度：MEDIUM

场景：为语音代理响应提示LLM

症状：
代理啰嗦。用户跟不上信息。"能重复一遍吗？"的请求。用户打断要求更短版本。所传递信息的理解度低。

为什么会失败：
文本可以扫读和重读。语音是线性和瞬时的。在聊天中有效的3段式响应在语音中令人难以承受。用户工作记忆中只能保留约7项。

推荐修复：

# 在提示中限制响应长度：

system_prompt = '''
你是一个语音助手。响应控制在30字以内。
对于复杂信息，分块传递并在每块之间确认理解。

不要这样说："这里有三个选项。首先，你可以...
第二...第三..."

这样说："我找到3个选项。要我逐一介绍吗？"

永远不要在未暂停确认的情况下列出超过3项。
'''

## 在生成时强制执行：
const response = await openai.chat.completions.create({
  max_tokens: 100,  // 硬性限制
  // ...
});

## 分块模式：
if (information.length > 3) {
  response = `我有 ${information.length} 项。让我逐一来介绍。第一项：${information[0]}。准备好下一项了吗？`;
}

## 渐进式披露：
"我找到你的账户了。想知道余额、最近交易还是别的？"
// 不要一次性倾倒所有信息

### 在语音中使用项目符号/数字/Markdown

严重程度：MEDIUM

场景：为语音格式化LLM输出

症状：
"第一项：项目一"被大声朗读。数字被读成"一二三"而不是"一、二、三"。语音中有Markdown痕迹。机器人般、不自然的表达。

为什么会失败：
TTS模型读它收到的内容。用于视觉显示的文本格式在大声朗读时听起来很机械化。用户无法在音频中"看到"结构。

推荐修复：

# 提示口语化格式：

system_prompt = '''
为口语表达格式化响应：
- 没有项目符号、编号列表或markdown
- 拼出数字："二十三"而非"23"
- 拼出缩写："美国"而非"US"
- 使用口头提示语："有三件事。首先..."
- 永远不要使用星号、破折号或特殊字符
'''

## 后处理：
function prepareForSpeech(text) {
  return text
    // 移除markdown
    .replace(/[*_#`]/g, '')
    // 转换数字
    .replace(/\d+/g, numToWords)
    // 展开缩写
    .replace(/\betc\b/gi, 'et cetera')
    .replace(/\be\.g\./gi, 'for example')
    // 添加停顿
    .replace(/\. /g, '... ')
    .replace(/, /g, '... ');
}

## SSML精确控制：
<speak>
  总价是 <say-as interpret-as="currency">$49.99</say-as>。
  <break time="500ms"/>
  要继续吗？
</speak>

### 嘈杂环境下VAD/STT失败

严重程度：MEDIUM

场景：用户在车内、咖啡馆、户外

症状：
"我没听清楚"频繁出现。背景噪音触发误启动。风扇/空调导致持续监听。汽车引擎噪音使STT混乱。

为什么会失败：
默认VAD阈值适用于安静环境。实际使用包括触发误报的背景噪音或掩盖语音导致漏报。

推荐修复：

# 实现噪音处理：

## 1. STT中降噪：
const transcription = await deepgram.transcription.live({
  model: 'nova-3',
  noise_reduction: true,
  // 或
  smart_format: true,
});

## 2. 自适应VAD阈值：
// 测量环境噪音水平
const ambientLevel = measureAmbientNoise(5000);  // 5秒采样

vad.setThreshold(ambientLevel * 1.5);  // 高于环境

## 3. 置信度过滤：
stt.on('transcript', (data) => {
  if (data.confidence < 0.7) {
    // 低置信度 - 可能是噪音
    askForRepeat();
    return;
  }
  processTranscript(data.transcript);
});

## 4. 回声消除：
// 防止代理的语音被转录
const echoCanceller = new EchoCanceller();
echoCanceller.reference(ttsOutput);
const cleanedAudio = echoCanceller.process(userAudio);

### STT产生不正确或幻觉的文本

严重程度：MEDIUM

场景：处理不清晰或带口音的语音

症状：
代理响应了用户没说过的内容。姓名一直被叫错。技术术语被误听。"我说的是X，不是Y"的挫败感。

为什么会失败：
STT模型会产生幻觉，特别是在专有名词、技术术语或带口音的语音上。这些错误通过管道传播，产生莫名其妙的响应。

推荐修复：

# 缓解STT错误：

## 1. 使用关键词/偏置：
const transcription = await deepgram.transcription.live({
  keywords: ['Acme Corp', 'ProductName', 'John Smith'],
  keyword_boost: 'high',
});

## 2. 关键信息确认：
if (containsNameOrNumber(transcript)) {
  response = `我听到的是"${name}"。正确吗？`;
}

## 3. 基于置信度的后备：
if (confidence < 0.8) {
  response = `我想你说的是"${transcript}"。我理解对了吗？`;
}

## 4. 多假设处理：
// 一些STT API返回n-best列表
const alternatives = transcription.alternatives;
if (alternatives[0].confidence - alternatives[1].confidence < 0.1) {
  // 模糊 - 请求澄清
}

## 5. 错误纠正模式：
promptPattern = `
  用户可能会纠正之前的错误。如果他们说"不，我说的是X"
  或"不是Y，是Z"，请相应更新你的理解。
`;

## 验证检查

### 缺少延迟测量

严重程度：ERROR

语音代理必须在每个阶段跟踪延迟

消息：语音管道没有延迟跟踪。在每个阶段添加时间戳以测量性能。

### 使用批量STT而非流式STT

严重程度：WARNING

流式STT显著降低延迟

消息：使用了批量转录。考虑在语音代理中使用流式以降低延迟。

### TTS无流式输出

严重程度：WARNING

流式TTS缩短首音频时间

消息：TTS无流式。流式音频以缩短首音频时间。

### 硬编码VAD静默阈值

严重程度：WARNING

固定静默阈值不能适应对话

消息：固定静默阈值。考虑使用语义VAD或自适应阈值以获得更好的轮次管理。

### 缺少打断处理

严重程度：WARNING

语音代理应在用户打断时停止

消息：VAD没有打断处理。在用户开始说话时停止TTS。

### 语音提示无长度限制

严重程度：WARNING

语音提示应限制响应长度

消息：语音提示无长度限制。在系统提示中添加"响应控制在30字以内"。

### 发送给TTS的Markdown格式

严重程度：WARNING

Markdown将被TTS逐字读取

消息：检查TTS输入中的Markdown。在发送给TTS之前去除格式。

### STT无错误处理

严重程度：WARNING

STT可能失败或返回低置信度

消息：STT无错误处理。检查置信度分数并处理失败。

### WebSocket无重连

严重程度：WARNING

实时API需要重连处理

消息：实时连接无重连逻辑。优雅地处理断开。

### 缺少噪音处理

严重程度：INFO

实际音频包括背景噪音

消息：考虑为实际音频质量添加噪音处理。

## 协作

### 委派触发器

- 用户需要电话/电话集成 -> backend（Twilio、Vonage、SIP集成）
- 用户需要LLM优化 -> llm-architect（模型选择、提示工程、微调）
- 用户需要语音代理的工具 -> agent-tool-builder（语音上下文的工具设计）
- 用户需要多代理语音系统 -> multi-agent-orchestration（协同工作的语音代理）
- 用户需要无障碍合规性 -> accessibility-specialist（语音接口的无障碍）

## 相关技能

与以下技能配合使用：`agent-tool-builder`、`multi-agent-orchestration`、`llm-architect`、`backend`

## 何时使用
- 用户提及或暗示：voice agent
- 用户提及或暗示：speech to text
- 用户提及或暗示：text to speech
- 用户提及或暗示：whisper
- 用户提及或暗示：elevenlabs
- 用户提及或暗示：deepgram
- 用户提及或暗示：realtime api
- 用户提及或暗示：voice assistant
- 用户提及或暗示：voice ai
- 用户提及或暗示：conversational ai
- 用户提及或暗示：tts
- 用户提及或暗示：stt
- 用户提及或暗示：asr

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将此输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
