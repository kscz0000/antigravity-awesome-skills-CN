# 转录工具对比

audio-transcriber 技能支持的音频转录引擎综合对比。

## 概览

| 工具 | 类型 | 速度 | 质量 | 成本 | 隐私 | 离线 | 语言 |
|------|------|-------|---------|------|---------|---------|-----------|
| **Faster-Whisper** | 开源 | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 免费 | 100% | ✅ | 99 |
| **Whisper** | 开源 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 免费 | 100% | ✅ | 99 |
| Google Speech-to-Text | 商业 API | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | $0.006/15秒 | 部分 | ❌ | 125+ |
| Azure Speech | 商业 API | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | $1/小时 | 部分 | ❌ | 100+ |
| AssemblyAI | 商业 API | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | $0.00025/秒 | 部分 | ❌ | 99 |

---

## Faster-Whisper（推荐）

### 优点
✅ **比原始 Whisper 快 4-5 倍**  
✅ **与原始 Whisper 质量相同**  
✅ **内存占用更低**（减少 50-60% RAM）  
✅ **免费开源**  
✅ **100% 离线**（隐私有保障）  
✅ **安装简单**（`pip install faster-whisper`）  
✅ **Whisper 的直接替代品**

### 缺点
❌ 需要 Python 3.8+  
❌ 初始模型下载（约 100MB-1.5GB）  
❌ GPU 可选但可显著加速

### 安装

```bash
pip install faster-whisper
```

### 使用示例

```python
from faster_whisper import WhisperModel

# 加载模型（首次运行自动下载）
model = WhisperModel("base", device="cpu", compute_type="int8")

# 转录
segments, info = model.transcribe("audio.mp3", language="pt")

# 打印结果
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### 模型大小

| 模型 | 大小 | 内存 | CPU 速度 | 质量 |
|-------|------|-----|-------------|---------|
| `tiny` | 39 MB | ~1 GB | 很快（约 10x 实时） | 基础 |
| `base` | 74 MB | ~1 GB | 快（约 7x 实时） | 良好 |
| `small` | 244 MB | ~2 GB | 中等（约 4x 实时） | 很好 |
| `medium` | 769 MB | ~5 GB | 慢（约 2x 实时） | 优秀 |
| `large` | 1550 MB | ~10 GB | 很慢（约 1x 实时） | 最佳 |

**推荐：** 生产环境使用 `small` 或 `medium`。

---

## Whisper（原始版）

### 优点
✅ **官方 OpenAI 模型**  
✅ **出色的质量**  
✅ **免费开源**  
✅ **100% 离线**  
✅ **文档完善**  
✅ **庞大的社区**

### 缺点
❌ **比 Faster-Whisper 慢**（4-5 倍）  
❌ **内存占用更高**  
❌ 需要 PyTorch（大型依赖）  
❌ 大模型强烈推荐 GPU

### 安装

```bash
pip install openai-whisper
```

### 使用示例

```python
import whisper

# 加载模型
model = whisper.load_model("base")

# 转录
result = model.transcribe("audio.mp3", language="pt")

# 打印结果
print(result["text"])
```

### 何时使用 Whisper vs. Faster-Whisper

**使用 Faster-Whisper 如果：**
- 速度很重要
- 可用内存有限
- 处理大量文件

**使用原始 Whisper 如果：**
- Faster-Whisper 安装有问题
- 需要精确的 OpenAI 实现
- 项目依赖中已有 Whisper

---

## Google Cloud Speech-to-Text

### 优点
✅ **非常准确**（行业领先）  
✅ **处理快速**（云基础设施）  
✅ **125+ 种语言**  
✅ **词级时间戳**  
✅ **标点和大小写**  
✅ **说话人分离**（高级版）

### 缺点
❌ **需要联网**（仅云端）  
❌ **需要付费**（免费额度后）  
❌ **隐私问题**（音频上传到 Google）  
❌ 需要 GCP 账户设置  
❌ 复杂的身份验证

### 定价

- **免费额度：** 60 分钟/月
- **标准版：** $0.006 每 15 秒（$1.44/小时）
- **高级版：** $0.009 每 15 秒（含说话人分离）

### 安装

```bash
pip install google-cloud-speech
```

### 设置

1. 创建 GCP 项目
2. 启用 Speech-to-Text API
3. 创建服务账户并下载 JSON 密钥
4. 设置环境变量：
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
   ```

### 使用示例

```python
from google.cloud import speech

client = speech.SpeechClient()

with open("audio.wav", "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="pt-BR",
)

response = client.recognize(config=config, audio=audio)

for result in response.results:
    print(result.alternatives[0].transcript)
```

---

## Azure Speech Services

### 优点
✅ **高准确度**  
✅ **100+ 种语言**  
✅ **实时转录**  
✅ **自定义模型**（用自己的数据训练）  
✅ **良好的 Microsoft 生态系统集成**

### 缺点
❌ **需要联网**  
❌ **需要付费**（免费额度后）  
❌ **隐私问题**（云端处理）  
❌ 需要 Azure 账户  
❌ 设置复杂

### 定价

- **免费额度：** 5 小时/月
- **标准版：** $1.00 每音频小时

### 安装

```bash
pip install azure-cognitiveservices-speech
```

### 设置

1. 创建 Azure 账户
2. 创建 Speech 资源
3. 获取 API 密钥和区域
4. 设置环境变量：
   ```bash
   export AZURE_SPEECH_KEY="your-key"
   export AZURE_SPEECH_REGION="your-region"
   ```

### 使用示例

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get('AZURE_SPEECH_KEY'),
    region=os.environ.get('AZURE_SPEECH_REGION')
)

audio_config = speechsdk.audio.AudioConfig(filename="audio.wav")
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config
)

result = speech_recognizer.recognize_once()
print(result.text)
```

---

## AssemblyAI

### 优点
✅ **现代、开发者友好的 API**  
✅ **出色的准确度**  
✅ **高级功能**（情感分析、主题检测、PII 脱敏）  
✅ **说话人分离**（包含）  
✅ **处理快速**  
✅ **文档完善**

### 缺点
❌ **需要联网**  
❌ **需要付费**（无免费额度，仅试用额度）  
❌ **隐私问题**（云端处理）  
❌ 需要 API 密钥

### 定价

- **免费试用：** $50 额度
- **标准版：** $0.00025 每秒（约 $0.90/小时）

### 安装

```bash
pip install assemblyai
```

### 设置

1. 在 assemblyai.com 注册
2. 获取 API 密钥
3. 设置环境变量：
   ```bash
   export ASSEMBLYAI_API_KEY="your-key"
   ```

### 使用示例

```python
import assemblyai as aai

aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("audio.mp3")

print(transcript.text)

# 说话人分离
for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")
```

---

## 推荐矩阵

### 使用 Faster-Whisper 如果：
- ✅ 隐私至关重要（本地处理）
- ✅ 希望零成本（永久免费）
- ✅ 需要离线能力
- ✅ 处理大量文件（速度重要）
- ✅ 预算有限

### 使用 Google Speech-to-Text 如果：
- ✅ 需要绝对最佳的准确度
- ✅ 有云服务预算
- ✅ 需要高级功能（标点、说话人分离）
- ✅ 已在使用 GCP 生态系统

### 使用 Azure Speech 如果：
- ✅ 在 Microsoft 生态系统中
- ✅ 需要自定义模型训练
- ✅ 需要实时转录
- ✅ 有 Azure 额度

### 使用 AssemblyAI 如果：
- ✅ 需要高级功能（情感、主题）
- ✅ 希望最佳的 API 体验
- ✅ 需要自动 PII 脱敏
- ✅ 重视开发者体验

---

## 性能基准

**测试：** 1 小时播客（MP3，44.1kHz，立体声）

| 工具 | 处理时间 | 准确度 | 成本 |
|------|----------------|----------|------|
| Faster-Whisper (small) | 8 分钟 | 94% | $0 |
| Whisper (small) | 32 分钟 | 94% | $0 |
| Google Speech | 2 分钟 | 96% | $1.44 |
| Azure Speech | 3 分钟 | 95% | $1.00 |
| AssemblyAI | 4 分钟 | 96% | $0.90 |

*基准测试在 MacBook Pro M1，16GB RAM 上运行*

---

## 结论

**对于 audio-transcriber 技能：**

1. **首选：** Faster-Whisper（速度、质量、隐私、成本的最佳平衡）
2. **备选：** Whisper（如果 Faster-Whisper 不可用）
3. **可选：** 云 API（用户选择用于高级功能）

这确保技能对大多数用户开箱即用，同时允许高级用户在需要时集成商业服务。
