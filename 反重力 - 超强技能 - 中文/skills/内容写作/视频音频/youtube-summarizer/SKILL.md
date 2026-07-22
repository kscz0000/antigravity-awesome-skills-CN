---
name: youtube-summarizer
description: "使用智能分析框架从 YouTube 视频提取转录文本并生成全面、详细的摘要。触发词：YouTube 视频摘要、提取转录、YouTube 转录、视频内容分析、生成摘要"
category: content
risk: safe
source: community
tags: "[video, summarization, transcription, youtube, content-analysis]"
date_added: "2026-02-27"
---

# YouTube 视频摘要生成器

## 用途

本技能使用 STAR + R-I-S-E 框架从 YouTube 视频提取转录文本，并生成全面、详尽的摘要。它会验证视频可用性，使用 `youtube-transcript-api` Python 库提取转录文本，并产出捕获所有洞察、论据和关键要点的详细文档。

本技能专为需要对教学视频、讲座、教程或信息类内容进行彻底内容分析并生成参考文档的用户而设计。

## 何时使用本技能

在以下情况应使用本技能：

- 用户提供 YouTube 视频 URL 并希望获得详细摘要
- 用户需要将视频内容记录为参考文档而无需重新观看
- 用户希望从教学类内容中提取洞察、关键要点和论据
- 用户需要从 YouTube 视频获取转录文本以进行分析
- 用户请求对 YouTube 视频进行"总结"、"摘要"或"提取内容"
- 用户希望获得优先考虑完整性而非简洁性的全面文档

## 步骤 0：发现与设置

在处理视频之前，请验证环境和依赖项：

```bash
# Check if youtube-transcript-api is installed
python3 -c "import youtube_transcript_api" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  youtube-transcript-api not found"
    # Offer to install
fi

# Check Python availability
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi
```

**若依赖缺失，询问用户：**

```
youtube-transcript-api is required but not installed.

Would you like to install it now?
- [ ] Yes - Install with pip (pip install youtube-transcript-api)
- [ ] No - I'll install it manually
```

**如果用户选择"Yes"：**

```bash
pip install youtube-transcript-api
```

**验证安装：**

```bash
python3 -c "import youtube_transcript_api; print('✅ youtube-transcript-api installed successfully')"
```

## 主工作流

### 进度跟踪指南

在整个工作流中，在每个步骤前显示一个可视化进度条，以便让用户随时了解情况。进度条格式为：

```bash
echo "[████░░░░░░░░░░░░░░░░] 20% - Step 1/5: Validating URL"
```

**格式规范：**
- 宽度为 20 个字符（使用 █ 表示已填充，░ 表示空白）
- 百分比递增：步骤 1=20%，步骤 2=40%，步骤 3=60%，步骤 4=80%，步骤 5=100%
- 步骤计数器显示当前/总数（例如，"Step 3/5"）
- 当前阶段的简要说明

**在步骤 1 之前显示初始状态框：**

```
╔══════════════════════════════════════════════════════════════╗
║     📹  YOUTUBE SUMMARIZER - Processing Video                ║
╠══════════════════════════════════════════════════════════════╣
║ → Step 1: Validating URL                 [IN PROGRESS]       ║
║ ○ Step 2: Checking Availability                              ║
║ ○ Step 3: Extracting Transcript                              ║
║ ○ Step 4: Generating Summary                                 ║
║ ○ Step 5: Formatting Output                                  ║
╠══════════════════════════════════════════════════════════════╣
║ Progress: ██████░░░░░░░░░░░░░░░░░░░░░░░░  20%               ║
╚══════════════════════════════════════════════════════════════╝
```

### 步骤 1：验证 YouTube URL

**目标：** 提取视频 ID 并验证 URL 格式。

**支持的 URL 格式：**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

**操作：**

```bash
# Extract video ID using regex or URL parsing
URL="$USER_PROVIDED_URL"

# Pattern 1: youtube.com/watch?v=VIDEO_ID
if echo "$URL" | grep -qE 'youtube\.com/watch\?v='; then
    VIDEO_ID=$(echo "$URL" | sed -E 's/.*[?&]v=([^&]+).*/\1/')
# Pattern 2: youtu.be/VIDEO_ID  
elif echo "$URL" | grep -qE 'youtu\.be/'; then
    VIDEO_ID=$(echo "$URL" | sed -E 's/.*youtu\.be\/([^?]+).*/\1/')
else
    echo "❌ Invalid YouTube URL format"
    exit 1
fi

echo "📹 Video ID extracted: $VIDEO_ID"
```

**如果 URL 无效：**

```
❌ Invalid YouTube URL

Please provide a valid YouTube URL in one of these formats:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID

Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 步骤 2：检查视频和转录文本可用性

**进度：**
```bash
echo "[████████░░░░░░░░░░░░] 40% - Step 2/5: Checking Availability"
```

**目标：** 验证视频存在且转录文本可访问。

**操作：**

```python
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import sys

video_id = sys.argv[1]

try:
    # Get list of available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print(f"✅ Video accessible: {video_id}")
    print("📝 Available transcripts:")
    
    for transcript in transcript_list:
        print(f"  - {transcript.language} ({transcript.language_code})")
        if transcript.is_generated:
            print("    [Auto-generated]")
    
except TranscriptsDisabled:
    print(f"❌ Transcripts are disabled for video {video_id}")
    sys.exit(1)
    
except NoTranscriptFound:
    print(f"❌ No transcript found for video {video_id}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error accessing video: {e}")
    sys.exit(1)
```

**错误处理：**

| 错误 | 消息 | 操作 |
|-------|---------|--------|
| 视频未找到 | "❌ Video does not exist or is private" | 请用户验证 URL |
| 转录文本已禁用 | "❌ Transcripts are disabled for this video" | 无法继续 |
| 无可用转录文本 | "❌ No transcript found (not auto-generated or manually added)" | 无法继续 |
| 私有/受限视频 | "❌ Video is private or restricted" | 请求公开视频 |

### 步骤 3：提取转录文本

**进度：**
```bash
echo "[████████████░░░░░░░░] 60% - Step 3/5: Extracting Transcript"
```

**目标：** 以首选语言检索转录文本。

**操作：**

```python
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "VIDEO_ID"

try:
    # Try to get transcript in user's preferred language first
    # Fall back to English if not available
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id, 
        languages=['pt', 'en']  # Prefer Portuguese, fallback to English
    )
    
    # Combine transcript segments into full text
    full_text = " ".join([entry['text'] for entry in transcript])
    
    # Get video metadata
    from youtube_transcript_api import YouTubeTranscriptApi
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print("✅ Transcript extracted successfully")
    print(f"📊 Transcript length: {len(full_text)} characters")
    
    # Save to temporary file for processing
    with open(f"/tmp/transcript_{video_id}.txt", "w") as f:
        f.write(full_text)
    
except Exception as e:
    print(f"❌ Error extracting transcript: {e}")
    exit(1)
```

**转录文本处理：**

- 将所有转录片段合并为连贯的文本
- 在可用的情况下保留标点和格式
- 移除重复或重叠的片段（如果是自动生成的产物）
- 存储在临时文件中供分析使用

### 步骤 4：生成全面摘要

**进度：**
```bash
echo "[████████████████░░░░] 80% - Step 4/5: Generating Summary"
```

**目标：** 应用增强的 STAR + R-I-S-E 提示词以创建详细摘要。

**应用的提示词：**

使用阶段 2 中（STAR + R-I-S-E 框架）的增强提示词，并将提取的转录文本作为输入。

**操作：**

1. 加载完整的转录文本
2. 应用全面的摘要提示词
3. 使用 AI 模型（Claude/GPT）生成结构化摘要
4. 确保输出遵循定义的结构：
   - 包含视频元数据的头部
   - 执行摘要
   - 详细的逐节拆解
   - 关键洞察和结论
   - 概念和术语
   - 资源和参考

**实现：**

```bash
# Use the transcript file as input to the AI prompt
TRANSCRIPT_FILE="/tmp/transcript_${VIDEO_ID}.txt"

# The AI agent will:
# 1. Read the transcript
# 2. Apply the STAR + R-I-S-E summarization framework
# 3. Generate comprehensive Markdown output
# 4. Structure with headers, lists, and highlights

Read "$TRANSCRIPT_FILE"  # Read transcript into context
```

然后应用完整的摘要提示词（来自阶段 2 中的增强版本）。

### 步骤 5：格式化并呈现输出

**进度：**
```bash
echo "[████████████████████] 100% - Step 5/5: Formatting Output"
```

**目标：** 以干净、结构良好的 Markdown 形式交付摘要。

**输出结构：**

```markdown
# [Video Title]

**Canal:** [Channel Name]  
**Duração:** [Duration]  
**URL:** [https://youtube.com/watch?v=VIDEO_ID]  
**Data de Publicação:** [Date if available]


## 📝 Detailed Summary

### [Topic 1]

[Comprehensive explanation with examples, data, quotes...]

#### [Subtopic 1.1]

[Detailed breakdown...]

### [Topic 2]

[Continued detailed analysis...]


## 📚 Concepts and Terminology

- **[Term 1]:** [Definition and context]
- **[Term 2]:** [Definition and context]


## 📌 Conclusion

[Final synthesis and takeaways]
```


### **示例 2：依赖缺失**

**用户输入：**
```
claude> summarize this youtube video https://youtu.be/abc123
```

**技能响应：**

```
⚠️  youtube-transcript-api not installed

This skill requires the Python library 'youtube-transcript-api'.

Would you like me to install it now?
- [ ] Yes - Install with pip
- [ ] No - I'll install manually
```

**用户选择"Yes"：**

```bash
$ pip install youtube-transcript-api
Successfully installed youtube-transcript-api-0.6.1

✅ Installation complete! Proceeding with video summary...
```


### **示例 4：URL 无效**

**用户输入：**
```
claude> summarize youtube video www.youtube.com/some-video
```

**技能响应：**

```
❌ Invalid YouTube URL format

Expected format examples:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID

Please provide a valid YouTube video URL.
```


## 📊 Executive Summary

This video provides a comprehensive introduction to the fundamental concepts of Artificial Intelligence (AI), designed for beginners and professionals who want to understand the technical foundations and practical applications of modern AI. The instructor covers everything from basic definitions to machine learning algorithms, using practical examples and visualizations to facilitate understanding.

[... continued detailed summary ...]
```

**保存选项：**

```
What would you like to save?
→ Summary + raw transcript

✅ File saved: resumo-exemplo123-2026-02-01.md (includes raw transcript)
[████████████████████] 100% - ✓ Processing complete!
```


Welcome to this comprehensive tutorial on machine learning fundamentals. In today's video, we'll explore the core concepts that power modern AI systems...
```


**版本：** 1.2.0
**最后更新：** 2026-02-02
**维护者：** Eric Andrade

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
