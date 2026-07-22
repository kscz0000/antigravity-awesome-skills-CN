---
name: audio-transcriber
description: "使用 LLM 集成将音频录音转换为专业 Markdown 文档，生成智能摘要。触发词：音频转文字、转录音频、会议记录、语音转文本、transcribe audio、meeting minutes、whisper转录、音频转写"
category: content
risk: safe
source: community
tags: "[audio, transcription, whisper, meeting-minutes, speech-to-text]"
date_added: "2026-02-27"
---

## 目的

本技能自动化音频转文字转录，输出专业 Markdown 文档，提取丰富的技术元数据（说话人、时间戳、语言、文件大小、时长）并生成结构化会议纪要和执行摘要。使用 Faster-Whisper 或 Whisper，零配置即可工作，无需硬编码路径或 API 密钥，适用于任何项目。

受 Plaud 等工具启发，本技能将原始音频录音转化为可执行的文档，非常适合会议、访谈、讲座和内容分析场景。

## 何时使用

在以下情况下调用本技能：

- 用户需要将音频/视频文件转录为文字
- 用户希望从录音自动生成会议纪要
- 用户需要对话中的说话人识别（说话人分离）
- 用户需要字幕/字幕文件（SRT、VTT 格式）
- 用户需要长音频内容的执行摘要
- 用户询问"转录这个音频"、"将音频转为文字"、"从录音生成会议笔记"等变体
- 用户有常见格式的音频文件（MP3、WAV、M4A、OGG、FLAC、WEBM）

## 工作流程

### 步骤 0：发现（自动检测转录工具）

**目标：** 无需用户配置即可识别可用的转录引擎。

**操作：**

运行检测命令查找已安装的工具：

```bash
# 检查 Faster-Whisper（首选 - 快 4-5 倍）
if python3 -c "import faster_whisper" 2>/dev/null; then
    TRANSCRIBER="faster-whisper"
    echo "✅ Faster-Whisper detected (optimized)"
# 回退到原始 Whisper
elif python3 -c "import whisper" 2>/dev/null; then
    TRANSCRIBER="whisper"
    echo "✅ OpenAI Whisper detected"
else
    TRANSCRIBER="none"
    echo "⚠️  No transcription tool found"
fi

# 检查 ffmpeg（音频格式转换）
if command -v ffmpeg &>/dev/null; then
    echo "✅ ffmpeg available (format conversion enabled)"
else
    echo "ℹ️  ffmpeg not found (limited format support)"
fi
```

**如果未找到转录工具：**

提供使用提供的脚本自动安装：

```bash
echo "⚠️  No transcription tool found"
echo ""
echo "🔧 Auto-install dependencies? (Recommended)"
read -p "Run installation script? [Y/n]: " AUTO_INSTALL

if [[ ! "$AUTO_INSTALL" =~ ^[Nn] ]]; then
    # Get skill directory (works for both repo and symlinked installations)
    SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Run installation script
    if [[ -f "$SKILL_DIR/scripts/install-requirements.sh" ]]; then
        bash "$SKILL_DIR/scripts/install-requirements.sh"
    else
        echo "❌ Installation script not found"
        echo ""
        echo "📦 Manual installation:"
        echo "  pip install faster-whisper  # Recommended"
        echo "  pip install openai-whisper  # Alternative"
        echo "  brew install ffmpeg         # Optional (macOS)"
        exit 1
    fi
    
    # Verify installation succeeded
    if python3 -c "import faster_whisper" 2>/dev/null || python3 -c "import whisper" 2>/dev/null; then
        echo "✅ Installation successful! Proceeding with transcription..."
    else
        echo "❌ Installation failed. Please install manually."
        exit 1
    fi
else
    echo ""
    echo "📦 Manual installation required:"
    echo ""
    echo "Recommended (fastest):"
    echo "  pip install faster-whisper"
    echo ""
    echo "Alternative (original):"
    echo "  pip install openai-whisper"
    echo ""
    echo "Optional (format conversion):"
    echo "  brew install ffmpeg  # macOS"
    echo "  apt install ffmpeg   # Linux"
    echo ""
    exit 1
fi
```

这确保用户可以通过一次确认安装依赖，或者根据偏好选择手动安装。

**如果找到转录工具：**

继续步骤 0b（CLI 检测）。


### 步骤 1：验证音频文件

**目标：** 验证文件是否存在，检查格式，并提取元数据。

**操作：**

1. **接受用户提供的文件路径或 URL：**
   - 本地文件：`meeting.mp3`
   - URL：`https://example.com/audio.mp3`（下载到临时目录）

2. **验证文件存在：**

```bash
if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "❌ File not found: $AUDIO_FILE"
    exit 1
fi
```

3. **使用 ffprobe 或文件工具提取元数据：**

```bash
# Get file size
FILE_SIZE=$(du -h "$AUDIO_FILE" | cut -f1)

# Get duration and format using ffprobe
DURATION=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null)
FORMAT=$(ffprobe -v error -select_streams a:0 -show_entries \
    stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null)

# Convert duration to HH:MM:SS
DURATION_HMS=$(date -u -r "$DURATION" +%H:%M:%S 2>/dev/null || echo "Unknown")
```

4. **检查文件大小**（对云 API 警告大文件）：

```bash
SIZE_MB=$(du -m "$AUDIO_FILE" | cut -f1)
if [[ $SIZE_MB -gt 25 ]]; then
    echo "⚠️  Large file ($FILE_SIZE) - processing may take several minutes"
fi
```

5. **验证格式**（支持：MP3、WAV、M4A、OGG、FLAC、WEBM）：

```bash
EXTENSION="${AUDIO_FILE##*.}"
SUPPORTED_FORMATS=("mp3" "wav" "m4a" "ogg" "flac" "webm" "mp4")

if [[ ! " ${SUPPORTED_FORMATS[@]} " =~ " ${EXTENSION,,} " ]]; then
    echo "⚠️  Unsupported format: $EXTENSION"
    if command -v ffmpeg &>/dev/null; then
        echo "🔄 Converting to WAV..."
        ffmpeg -i "$AUDIO_FILE" -ar 16000 "${AUDIO_FILE%.*}.wav" -y
        AUDIO_FILE="${AUDIO_FILE%.*}.wav"
    else
        echo "❌ Install ffmpeg to convert formats: brew install ffmpeg"
        exit 1
    fi
fi
```


### 步骤 3：生成 Markdown 输出

**目标：** 创建包含元数据、转录文本、会议纪要和摘要的结构化 Markdown。

**输出模板：**

```markdown
# 音频转录报告

## 📊 元数据

| 字段 | 值 |
|------|------|
| **文件名** | {filename} |
| **文件大小** | {file_size} |
| **时长** | {duration_hms} |
| **语言** | {language} ({language_code}) |
| **处理日期** | {process_date} |
| **识别的说话人** | {num_speakers} |
| **转录引擎** | {engine} (模型: {model}) |


## 📋 会议纪要

### 参与者
- {speaker_1}
- {speaker_2}
- ...

### 讨论主题
1. **{topic_1}** ({timestamp})
   - {key_point_1}
   - {key_point_2}

2. **{topic_2}** ({timestamp})
   - {key_point_1}

### 做出的决策
- ✅ {decision_1}
- ✅ {decision_2}

### 行动项
- [ ] **{action_1}** - 负责人: {speaker} - 截止日期: {date_if_mentioned}
- [ ] **{action_2}** - 负责人: {speaker}


*由 audio-transcriber 技能 v1.0.0 生成*  
*转录引擎: {engine} | 处理时间: {elapsed_time}s*
```

**实现：**

使用 Python 或 bash 配合 AI 模型（Claude/GPT）进行智能摘要：

```python
def generate_meeting_minutes(segments):
    """从转录文本中提取主题、决策和行动项。"""
    
    # Group segments by topic (simple clustering by timestamps)
    topics = cluster_by_topic(segments)
    
    # Identify action items (keywords: "should", "will", "need to", "action")
    action_items = extract_action_items(segments)
    
    # Identify decisions (keywords: "decided", "agreed", "approved")
    decisions = extract_decisions(segments)
    
    return {
        "topics": topics,
        "decisions": decisions,
        "action_items": action_items
    }

def generate_summary(segments, max_paragraphs=5):
    """使用 AI（Claude/GPT API 或本地模型）创建执行摘要。"""
    
    full_text = " ".join([s["text"] for s in segments])
    
    # Use Chain of Density approach (from prompt-engineer frameworks)
    summary_prompt = f"""
    Summarize the following transcription in {max_paragraphs} concise paragraphs.
    Focus on key topics, decisions, and action items.
    
    Transcription:
    {full_text}
    """
    
    # Call AI model (placeholder - user can integrate Claude API or use local model)
    summary = call_ai_model(summary_prompt)
    
    return summary
```

**输出文件命名：**

```bash
# v1.1.0: 使用时间戳防止覆盖
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
TRANSCRIPT_FILE="transcript-${TIMESTAMP}.md"
ATA_FILE="ata-${TIMESTAMP}.md"

echo "$TRANSCRIPT_CONTENT" > "$TRANSCRIPT_FILE"
echo "✅ 转录文件已保存: $TRANSCRIPT_FILE"

if [[ -n "$ATA_CONTENT" ]]; then
    echo "$ATA_CONTENT" > "$ATA_FILE"
    echo "✅ 会议纪要已保存: $ATA_FILE"
fi
```


#### **场景 A：用户提供自定义提示词**

**工作流程：**

1. **显示用户的提示词：**
   ```
   📝 用户提供的提示词：
   ┌──────────────────────────────────┐
   │ [用户提示词预览]                  │
   └──────────────────────────────────┘
   ```

2. **使用 prompt-engineer 自动改进（如果可用）：**
   ```bash
   🔧 使用 prompt-engineer 改进提示词...
   [调用: gh copilot -p "melhore este prompt: {user_prompt}"]
   ```

3. **显示两个版本：**
   ```
   ✨ 改进版本：
   ┌──────────────────────────────────┐
   │ Role: 你是一个文档记录员...       │
   │ Instructions: 转换...             │
   │ Steps: 1) ... 2) ...              │
   │ End Goal: ...                     │
   └──────────────────────────────────┘

   📝 原始版本：
   ┌──────────────────────────────────┐
   │ [用户原始提示词]                  │
   └──────────────────────────────────┘
   ```

4. **询问使用哪个版本：**
   ```bash
   💡 使用改进版本？[s/n] (默认: s):
   ```

5. **使用选定的提示词处理：**
   - 如果 "s"：使用改进版本
   - 如果 "n"：使用原始版本


#### **LLM 处理（两种场景）**

确定提示词后：

```python
from rich.progress import Progress, SpinnerColumn, TextColumn

def process_with_llm(transcript, prompt, cli_tool='claude'):
    full_prompt = f"{prompt}\n\n---\n\nTranscrição:\n\n{transcript}"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task(
            description=f"🤖 使用 {cli_tool} 处理中...",
            total=None
        )
        
        if cli_tool == 'claude':
            result = subprocess.run(
                ['claude', '-'],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
        elif cli_tool == 'gh-copilot':
            result = subprocess.run(
                ['gh', 'copilot', 'suggest', '-t', 'shell', full_prompt],
                capture_output=True,
                text=True,
                timeout=300
            )
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None
```

**进度输出：**
```
🤖 使用 claude 处理中... ⠋
[完成后:]
✅ 会议纪要生成成功！
```


#### **最终输出**

**成功（两个文件）：**
```bash
💾 保存文件中...

✅ 已创建文件：
  - transcript-20260203-023045.md  (原始转录)
  - ata-20260203-023045.md         (LLM 处理)

🧹 已删除临时文件：metadata.json, transcription.json

✅ 完成！总时间：3m 45s
```

**仅转录（用户拒绝 LLM）：**
```bash
💾 保存文件中...

✅ 已创建文件：
  - transcript-20260203-023045.md

ℹ️  未生成会议纪要（用户拒绝 LLM 处理）

🧹 已删除临时文件：metadata.json, transcription.json

✅ 完成！
```


### 步骤 5：显示结果摘要

**目标：** 显示完成状态和后续步骤。

**输出：**

```bash
echo ""
echo "✅ 转录完成！"
echo ""
echo "📊 结果："
echo "  文件: $OUTPUT_FILE"
echo "  语言: $LANGUAGE"
echo "  时长: $DURATION_HMS"
echo "  说话人: $NUM_SPEAKERS"
echo "  字数: $WORD_COUNT"
echo "  处理时间: ${ELAPSED_TIME}s"
echo ""
echo "📝 已生成："
echo "  - $OUTPUT_FILE (Markdown 报告)"
[if alternative formats:]
echo "  - ${OUTPUT_FILE%.*}.srt (字幕)"
echo "  - ${OUTPUT_FILE%.*}.json (结构化数据)"
echo ""
echo "🎯 后续步骤："
echo "  1. 审阅会议纪要和行动项"
echo "  2. 与参与者分享报告"
echo "  3. 跟踪行动项直至完成"
```


## 使用示例

### **示例 1：基本转录**

**用户输入：**
```bash
copilot> transcribe audio to markdown: meeting-2026-02-02.mp3
```

**技能输出：**

```bash
✅ Faster-Whisper detected (optimized)
✅ ffmpeg available (format conversion enabled)

📂 文件: meeting-2026-02-02.mp3
📊 大小: 12.3 MB
⏱️  时长: 00:45:32

🎙️  处理中...
[████████████████████] 100%

✅ 检测到语言: Portuguese (pt-BR)
👥 识别的说话人: 4
📝 生成 Markdown 输出...

✅ 转录完成！

📊 结果：
  文件: meeting-2026-02-02.md
  语言: pt-BR
  时长: 00:45:32
  说话人: 4
  字数: 6,842
  处理时间: 127s

📝 已生成：
  - meeting-2026-02-02.md (Markdown 报告)

🎯 后续步骤：
  1. 审阅会议纪要和行动项
  2. 与参与者分享报告
  3. 跟踪行动项直至完成
```


### **示例 3：批量处理**

**用户输入：**
```bash
copilot> transcreva estes áudios: recordings/*.mp3
```

**技能输出：**

```bash
📦 批量模式：发现 5 个文件
  1. team-standup.mp3
  2. client-call.mp3
  3. brainstorm-session.mp3
  4. product-demo.mp3
  5. retrospective.mp3

🎙️  批量处理中...

[1/5] team-standup.mp3 ✅ (2m 34s)
[2/5] client-call.mp3 ✅ (15m 12s)
[3/5] brainstorm-session.mp3 ✅ (8m 47s)
[4/5] product-demo.mp3 ✅ (22m 03s)
[5/5] retrospective.mp3 ✅ (11m 28s)

✅ 批量处理完成！
📝 已生成 5 个 Markdown 报告
⏱️  总处理时间: 6m 15s
```


### **示例 5：大文件警告**

**用户输入：**
```bash
copilot> transcribe audio to markdown: conference-keynote.mp3
```

**技能输出：**

```bash
✅ Faster-Whisper detected (optimized)

📂 文件: conference-keynote.mp3
📊 大小: 87.2 MB
⏱️  时长: 02:15:47
⚠️  大文件 (87.2 MB) - 处理可能需要几分钟

继续？[Y/n]:
```

**用户：** `Y`

```bash
🎙️  处理中...（可能需要 10-15 分钟）
[████░░░░░░░░░░░░░░░░] 20% - 预计剩余时间: 12m
```


本技能是**平台无关的**，可在任何具有 GitHub Copilot CLI 的终端环境中工作。它不依赖于特定的项目配置或外部 API，遵循零配置理念。

## 限制
- 仅当任务明显符合上述描述的范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
