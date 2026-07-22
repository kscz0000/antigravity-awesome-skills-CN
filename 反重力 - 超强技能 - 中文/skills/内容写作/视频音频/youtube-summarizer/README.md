# 🎥 youtube-summarizer

> 从 YouTube 视频提取转录文本并生成全面、详细的摘要

**版本：** 1.2.0
**状态：** ✨ 零配置 | 🌍 通用
**平台：** GitHub Copilot CLI、Claude Code

---

## 概述

**youtube-summarizer** 技能可自动提取 YouTube 视频的转录文本，并使用 STAR + R-I-S-E 框架生成详尽、结构化的摘要。非常适合在无需重看的情况下记录教学内容、讲座、教程或任何信息类视频。

---

## 功能特性

- 🎯 **自动转录文本提取** —— 使用 `youtube-transcript-api`
- ✅ **视频验证** —— 检查视频是否可访问且具有转录文本
- 🌍 **多语言支持** —— 优先葡萄牙语，回退英语
- 📊 **全面摘要** —— 优先保证细节和完整性
- 📝 **结构化输出** —— 带有标题、章节、洞察的 Markdown
- 🔍 **包含元数据** —— 视频标题、频道、时长、URL
- ⚡ **错误处理** —— 为所有失败场景提供清晰的消息
- 🛠️ **依赖管理** —— 自动提示安装所需依赖
- 📊 **进度条** —— 跨所有步骤的可视化处理跟踪器
- 💾 **灵活的保存选项** —— 仅摘要、摘要+转录或仅转录（v1.2.0 新增）

---

## 快速开始

### 触发条件

使用以下任一短语激活本技能：

```bash
# English
copilot> summarize this video: https://www.youtube.com/watch?v=VIDEO_ID
copilot> summarize youtube video https://youtu.be/VIDEO_ID
copilot> extract youtube transcript https://youtube.com/watch?v=VIDEO_ID

# Portuguese (also supported)
copilot> resume este video: https://www.youtube.com/watch?v=VIDEO_ID
```

### 首次设置

技能将自动检查依赖项并提示安装：

```bash
⚠️  youtube-transcript-api not installed

Would you like me to install it now?
- [x] Yes - Install with pip
- [ ] No - I'll install manually
```

选择"Yes"，技能将自动处理安装。

---

## 使用场景

### 1. **教学视频文档化**

```bash
copilot> summarize this video: https://www.youtube.com/watch?v=abc123
```

**输出：**
- 讲座内容的全面摘要
- 关键概念和术语
- 示例和实际应用
- 视频中提到的资源

### 2. **技术教程分析**

```bash
copilot> summarize youtube video https://youtu.be/xyz789
```

**输出：**
- 教程的分步拆解
- 提到的代码片段和命令
- 突出显示的最佳实践
- 记录的故障排除技巧

### 3. **会议演讲参考**

```bash
copilot> extract youtube transcript https://youtube.com/watch?v=def456
```

**输出：**
- 演讲者的洞察和论据
- 统计数据和数据点
- 案例研究和示例
- 问答环节摘要

### 4. **语言学习内容**

```bash
copilot> summarize youtube video https://youtu.be/ghi789
```

**输出：**
- 使用的词汇和表达
- 解释的语法要点
- 文化参考
- 提到的练习题

### 5. **研究与调查**

```bash
copilot> summarize youtube video https://www.youtube.com/watch?v=jkl012
```

**输出：**
- 呈现的研究发现
- 解释的方法论
- 结果和结论
- 未来工作建议

---

## 输出结构

每个摘要都遵循以下全面结构：

```markdown
# [Video Title]

**Canal:** [Channel Name]
**Duração:** [Duration]
**URL:** [Video URL]
**Data de Publicação:** [Date]

---

## 📊 Síntese Executiva
[High-level overview, 2-3 paragraphs]

---

## 📝 Resumo Detalhado
### [Topic 1]
[Detailed analysis with examples, data, quotes]

### [Topic 2]
[Continued breakdown...]

---

## 💡 Principais Insights
- **Insight 1:** [Explanation]
- **Insight 2:** [Explanation]

---

## 📚 Conceitos e Terminologia
- **Term 1:** [Definition]
- **Term 2:** [Definition]

---

## 🔗 Recursos Mencionados
- [Resource 1]
- [Resource 2]

---

## 📌 Conclusão
[Final synthesis and key takeaways]
```

---

## 依赖要求

- **Python 3.x**（通常在 macOS/Linux 上预装）
- **pip**（Python 包管理器）
- **[youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)** 作者 [Julien Depoix](https://github.com/jdepoix)（由技能自动安装）

### 手动安装（可选）

如果希望手动安装依赖项：

```bash
pip install youtube-transcript-api
```

---

## 支持的 URL 格式

本技能可识别以下 YouTube URL 格式：

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

---

## 限制

### 可处理的视频

✅ 具有自动生成字幕的公开视频  
✅ 具有人工添加字幕/标题的视频  
✅ 任何支持语言的转录文本视频

### 不可处理的视频

❌ 私有或未公开的视频  
❌ 已禁用转录文本的视频  
❌ 受年龄限制的视频（可能需要身份验证）  
❌ 没有任何字幕/副标题的视频

---

## 错误消息

### 没有可用的转录文本

```
❌ No transcript available for this video

This skill requires videos with auto-generated captions or manual subtitles.
Unfortunately, transcripts are not enabled for this video.
```

**解决方案：** 尝试另一个已启用字幕的视频。

### URL 无效

```
❌ Invalid YouTube URL format

Expected format examples:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID
```

**解决方案：** 确保提供完整有效的 YouTube URL。

### 视频无法访问

```
❌ Unable to access video

Possible reasons:
1. Video is private or unlisted
2. Video has been removed
3. Invalid video ID
```

**解决方案：** 验证 URL 并确保视频是公开的。

---

## 常见问题

### Q：生成摘要需要多长时间？

**A：** 取决于视频长度：
- 短视频（5-10 分钟）：30-60 秒
- 中等视频（20-40 分钟）：1-2 分钟
- 长视频（60 分钟以上）：2-5 分钟

### Q：能用英语/葡萄牙语以外的语言总结视频吗？

**A：** 可以！本技能会尝试以视频的原始语言提取转录文本。如果不可用，则回退到英语。

### Q：可以处理 YouTube Music 视频吗？

**A：** 仅当音乐视频启用字幕/转录文本时可以。大多数音乐视频没有转录文本。

### Q：可以自定义摘要长度吗？

**A：** 本技能按设计优先保证完整性（生成详尽摘要）。如果需要更短的摘要，可以让 AI 之后压缩输出。

### Q：这会下载视频吗？

**A：** 不会。仅通过 YouTube 的 API 提取文本转录内容。不会下载任何视频文件。

### Q：可以将摘要保存到文件吗？

**A：** 可以！生成摘要后，本技能提供灵活的保存选项：
- **仅摘要** —— 带有结构化摘要的 Markdown 文件
- **摘要 + 转录文本** —— 带有摘要和原始转录文本的 Markdown 文件
- **仅转录文本** —— 带有原始转录文本的纯文本文件（v1.2.0 中新增）
- **仅显示** —— 不保存任何文件，摘要显示在终端中

文件保存为 `resumo-{VIDEO_ID}-{YYYY-MM-DD}.md`（摘要）或 `transcript-{VIDEO_ID}-{YYYY-MM-DD}.txt`（仅转录文本）。

### Q：什么时候应该只保存转录文本？

**A：** 在以下情况下使用"仅转录文本"选项：
- 需要原始内容以供进一步分析
- 希望使用其他工具处理文本
- 倾向于稍后创建自己的摘要
- 需要转录文本用于文档或归档目的

---

## 安装

### 全局安装（推荐）

全局安装本技能以便在所有项目中使用：

```bash
# Clone the repository
git clone https://github.com/ericgandrade/cli-ai-skills.git
cd cli-ai-skills

# Run the install script
./scripts/install-skills.sh $(pwd)
```

这会在以下位置创建符号链接：
- `~/.copilot/skills/youtube-summarizer/`（GitHub Copilot CLI）
- `~/.claude/skills/youtube-summarizer/`（Claude Code）

### 仓库安装

添加到特定项目：

```bash
# Copy skill to your project
cp -r cli-ai-skills/.github/skills/youtube-summarizer .github/skills/
```

---

## 贡献

发现 bug 或有新功能请求？欢迎贡献！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/youtube-enhancement`
3. 提交更改：`git commit -m "feat(youtube-summarizer): add feature X"`
4. 推送并创建 Pull Request

---

## 许可证

MIT 许可证 —— 有关详细信息，请参阅 LICENSE。

---

## 致谢

- **[youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)** 作者 [Julien Depoix](https://github.com/jdepoix) —— 用于提取 YouTube 视频转录文本的 Python 库
- **Anthropic STAR/R-I-S-E 框架** —— 用于结构化摘要

---

**由 Eric Andrade 用 ❤️ 构建**

*版本 1.1.0 | 最后更新：2026 年 2 月*
