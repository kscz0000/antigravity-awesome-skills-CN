# 提供商对比指南

本指南对转写、LLM 和 TTS 服务的不同提供商进行对比，帮助你为语音 AI 引擎选择最合适的方案。

## 转写提供商

### Deepgram

**优势：**
- ✅ 转写速度最快（延迟 < 300ms）
- ✅ 出色的流式支持
- ✅ 高准确率（清晰音频下 95%+）
- ✅ 定价友好（$0.0043/分钟）
- ✅ Nova-2 模型针对实时场景优化
- ✅ 文档完善

**劣势：**
- ❌ 对浓重口音的识别略弱
- ❌ 公司体量较小（存在可靠性方面的隐忧）

**最适合：**
- 实时语音对话
- 低延迟应用
- 英语场景应用
- 初创公司与中小型企业

**配置：**
```python
{
    "transcriberProvider": "deepgram",
    "deepgramApiKey": "your-api-key",
    "deepgramModel": "nova-2",
    "language": "en-US"
}
```

---

### AssemblyAI

**优势：**
- ✅ 准确率极高（清晰音频下 96%+）
- ✅ 对口音和方言的识别效果优秀
- ✅ 出色的说话人分离能力
- ✅ 定价有竞争力（$0.00025/秒）
- ✅ 客户支持响应快

**劣势：**
- ❌ 延迟略高于 Deepgram
- ❌ 流式支持较新

**最适合：**
- 对准确率要求极高的应用
- 多说话人场景
- 用户群体多样、存在不同口音
- 企业级应用

**配置：**
```python
{
    "transcriberProvider": "assemblyai",
    "assemblyaiApiKey": "your-api-key",
    "language": "en"
}
```

---

### Azure Speech

**优势：**
- ✅ 企业级可靠性
- ✅ 优秀的多语言支持（100+ 语种）
- ✅ 强大的安全与合规能力
- ✅ 与 Azure 生态深度集成
- ✅ 支持自定义模型训练

**劣势：**
- ❌ 成本较高（$1/小时）
- ❌ 配置相对复杂
- ❌ 比专注流式的提供商略慢

**最适合：**
- 企业级应用
- 多语言需求
- 基于 Azure 的基础设施
- 对合规性敏感的应用

**配置：**
```python
{
    "transcriberProvider": "azure",
    "azureSpeechKey": "your-key",
    "azureSpeechRegion": "eastus",
    "language": "en-US"
}
```

---

### Google Cloud Speech

**优势：**
- ✅ 优秀的多语言支持（125+ 语种）
- ✅ 准确率良好
- ✅ 与 Google Cloud 集成
- ✅ 自动添加标点
- ✅ 支持说话人分离

**劣势：**
- ❌ 流式场景下延迟较高
- ❌ 定价模型较复杂
- ❌ 需要 Google Cloud 账号

**最适合：**
- 多语言应用
- Google Cloud 基础设施
- 需要说话人分离的应用

**配置：**
```python
{
    "transcriberProvider": "google",
    "googleCredentials": "path/to/credentials.json",
    "language": "en-US"
}
```

---

## LLM 提供商

### OpenAI（GPT-4、GPT-3.5）

**优势：**
- ✅ 回复质量最高
- ✅ 指令遵循能力出色
- ✅ 流式响应速度快
- ✅ 大上下文窗口（GPT-4 可达 128k）
- ✅ 业界领先的推理能力

**劣势：**
- ❌ 成本较高（$0.01-0.03/1k tokens）
- ❌ 速率限制可能偏紧
- ❌ 没有免费套餐

**最适合：**
- 高质量的对话 AI
- 复杂推理任务
- 生产环境应用
- 企业级用例

**配置：**
```python
{
    "llmProvider": "openai",
    "openaiApiKey": "your-api-key",
    "openaiModel": "gpt-4-turbo",
    "prompt": "You are a helpful AI assistant."
}
```

**价格：**
- GPT-4 Turbo：$0.01/1k 输入 tokens，$0.03/1k 输出 tokens
- GPT-3.5 Turbo：$0.0005/1k 输入 tokens，$0.0015/1k 输出 tokens

---

### Google Gemini

**优势：**
- ✅ 性价比极高（有免费套餐）
- ✅ 多模态能力
- ✅ 流式支持良好
- ✅ 大上下文窗口（Pro 达 1M tokens）
- ✅ 响应速度快

**劣势：**
- ❌ 质量略低于 GPT-4
- ❌ 行为可预测性稍弱
- ❌ 较新，成熟度有待检验

**最适合：**
- 对成本敏感的应用
- 多模态应用
- 初创公司与原型
- 高并发量应用

**配置：**
```python
{
    "llmProvider": "gemini",
    "geminiApiKey": "your-api-key",
    "geminiModel": "gemini-pro",
    "prompt": "You are a helpful AI assistant."
}
```

**价格：**
- Gemini Pro：免费版每分钟最多 60 次请求
- Gemini Pro（付费）：$0.00025/1k 输入 tokens，$0.0005/1k 输出 tokens

---

### Anthropic Claude

**优势：**
- ✅ 安全性与对齐表现出色
- ✅ 超长上下文窗口（200k tokens）
- ✅ 高质量回复
- ✅ 善于遵循复杂指令
- ✅ 强大的推理能力

**劣势：**
- ❌ 成本高于 Gemini
- ❌ 流式速度慢于 OpenAI
- ❌ 回复风格偏保守

**最适合：**
- 对安全要求严格的应用
- 长上下文应用
- 需要细腻回复的场景
- 企业级应用

**配置：**
```python
{
    "llmProvider": "claude",
    "claudeApiKey": "your-api-key",
    "claudeModel": "claude-3-opus",
    "prompt": "You are a helpful AI assistant."
}
```

**价格：**
- Claude 3 Opus：$0.015/1k 输入 tokens，$0.075/1k 输出 tokens
- Claude 3 Sonnet：$0.003/1k 输入 tokens，$0.015/1k 输出 tokens

---

## TTS 提供商

### ElevenLabs

**优势：**
- ✅ 拟真度最高的声音
- ✅ 出色的情感表现力
- ✅ 支持声音克隆
- ✅ 流式支持良好
- ✅ 多种语言

**劣势：**
- ❌ 成本较高（$0.30/1k 字符）
- ❌ 低价档位有速率限制
- ❌ 偶有发音错误

**最适合：**
- 高品质的语音体验
- 面向客户的应用
- 需要声音克隆的场景
- 对音质要求高的应用

**配置：**
```python
{
    "voiceProvider": "elevenlabs",
    "elevenlabsApiKey": "your-api-key",
    "elevenlabsVoiceId": "voice-id",
    "elevenlabsModel": "eleven_monolingual_v1"
}
```

**价格：**
- 免费版：10k 字符/月
- Starter：$5/月，30k 字符
- Creator：$22/月，100k 字符

---

### Azure TTS

**优势：**
- ✅ 企业级可靠性
- ✅ 语言丰富（100+）
- ✅ 提供神经语音
- ✅ 支持 SSML 精细控制
- ✅ 价格友好（$4/1M 字符）

**劣势：**
- ❌ 拟真度不如 ElevenLabs
- ❌ 配置相对复杂
- ❌ 需要 Azure 账号

**最适合：**
- 企业级应用
- 多语言需求
- 基于 Azure 的基础设施
- 对成本敏感的大规模应用

**配置：**
```python
{
    "voiceProvider": "azure",
    "azureSpeechKey": "your-key",
    "azureSpeechRegion": "eastus",
    "azureVoiceName": "en-US-JennyNeural"
}
```

**价格：**
- 神经语音：$16/1M 字符
- 标准语音：$4/1M 字符

---

### Google Cloud TTS

**优势：**
- ✅ 神经语音质量良好
- ✅ 语言丰富（40+）
- ✅ 提供 WaveNet 语音
- ✅ 定价有竞争力（$4/1M 字符）
- ✅ 支持 SSML

**劣势：**
- ❌ 拟真度不如 ElevenLabs
- ❌ 需要 Google Cloud 账号
- ❌ 配置复杂

**最适合：**
- 多语言应用
- Google Cloud 基础设施
- 性价比高的神经语音

**配置：**
```python
{
    "voiceProvider": "google",
    "googleCredentials": "path/to/credentials.json",
    "googleVoiceName": "en-US-Neural2-F"
}
```

**价格：**
- WaveNet 语音：$16/1M 字符
- Neural2 语音：$16/1M 字符
- 标准语音：$4/1M 字符

---

### Amazon Polly

**优势：**
- ✅ 与 AWS 集成
- ✅ 定价合理（$4/1M 字符）
- ✅ 提供神经语音
- ✅ 支持 SSML
- ✅ 服务稳定

**劣势：**
- ❌ 拟真度不如 ElevenLabs
- ❌ 声音选项较少
- ❌ 需要 AWS 账号

**最适合：**
- 基于 AWS 的基础设施
- 性价比高的神经语音
- 企业级应用

**配置：**
```python
{
    "voiceProvider": "polly",
    "awsAccessKey": "your-access-key",
    "awsSecretKey": "your-secret-key",
    "awsRegion": "us-east-1",
    "pollyVoiceId": "Joanna"
}
```

**价格：**
- 神经语音：$16/1M 字符
- 标准语音：$4/1M 字符

---

### Play.ht

**优势：**
- ✅ 支持声音克隆
- ✅ 声音自然
- ✅ 流式支持良好
- ✅ API 易用
- ✅ 多种语言

**劣势：**
- ❌ 成本高于云服务提供商
- ❌ 公司体量较小
- ❌ 文档相对较少

**最适合：**
- 声音克隆应用
- 高品质语音体验
- 初创公司与中小企业

**配置：**
```python
{
    "voiceProvider": "playht",
    "playhtApiKey": "your-api-key",
    "playhtUserId": "your-user-id",
    "playhtVoiceId": "voice-id"
}
```

**价格：**
- 免费版：2.5k 字符
- Creator：$31/月，50k 字符
- Pro：$79/月，150k 字符

---

## 推荐组合

### 预算敏感的初创公司
```python
{
    "transcriberProvider": "deepgram",  # Fast and affordable
    "llmProvider": "gemini",            # Free tier available
    "voiceProvider": "google"           # Cost-effective neural voices
}
```
**估算成本：** 每分钟对话约 $0.01

---

### 顶级体验
```python
{
    "transcriberProvider": "assemblyai",  # Highest accuracy
    "llmProvider": "openai",              # Best quality responses
    "voiceProvider": "elevenlabs"         # Most natural voices
}
```
**估算成本：** 每分钟对话约 $0.05

---

### 企业级应用
```python
{
    "transcriberProvider": "azure",  # Enterprise reliability
    "llmProvider": "openai",         # Best quality
    "voiceProvider": "azure"         # Enterprise reliability
}
```
**估算成本：** 每分钟对话约 $0.03

---

### 多语言应用
```python
{
    "transcriberProvider": "google",  # 125+ languages
    "llmProvider": "gemini",          # Good multi-language support
    "voiceProvider": "google"         # 40+ languages
}
```
**估算成本：** 每分钟对话约 $0.02

---

## 决策矩阵

| 优先级 | 转写 | LLM | TTS |
|--------|------|-----|-----|
| **最低成本** | Deepgram | Gemini | Google |
| **最高质量** | AssemblyAI | OpenAI | ElevenLabs |
| **最快速度** | Deepgram | OpenAI | ElevenLabs |
| **企业级** | Azure | OpenAI | Azure |
| **多语言** | Google | Gemini | Google |
| **声音克隆** | N/A | N/A | ElevenLabs/Play.ht |

---

## 测试建议

在选定提供商前，请结合你的具体场景进行测试：

1. **构建测试对话**，使用具有代表性的音频
2. **测量端到端延迟**
3. **由真实用户评估质量**
4. **根据预期调用量计算成本**
5. **测试边界场景**（口音、背景噪声、打断）

---

## 切换提供商

多提供商工厂模式让切换非常容易：

```python
# Just change the configuration
config = {
    "transcriberProvider": "deepgram",  # Change to "assemblyai"
    "llmProvider": "gemini",            # Change to "openai"
    "voiceProvider": "google"           # Change to "elevenlabs"
}

# No code changes needed!
factory = VoiceComponentFactory()
transcriber = factory.create_transcriber(config)
agent = factory.create_agent(config)
synthesizer = factory.create_synthesizer(config)
```
