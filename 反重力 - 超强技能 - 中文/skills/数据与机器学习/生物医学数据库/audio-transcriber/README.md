# Audio Transcriber 技能 v1.1.0

将音频录音转换为专业 Markdown 文档，**使用 LLM 集成（Claude/Copilot CLI）生成智能会议纪要/摘要**，并自动进行提示词工程。

## 🆕 v1.1.0 新增功能

- **🧠 LLM 集成** - Claude CLI（首选）或 GitHub Copilot CLI（备选）进行智能处理
- **✨ 智能提示词** - 与 prompt-engineer 技能自动集成
  - 用户提供的提示词 → 自动改进 → 用户选择版本
  - 无提示词 → 分析转录文本 → 建议格式 → 生成结构化提示词
- **📊 进度指示器** - 可视化进度条（tqdm）和旋转器（rich）
- **📁 时间戳文件名** - `transcript-YYYYMMDD-HHMMSS.md` + `ata-YYYYMMDD-HHMMSS.md`
- **🧹 自动清理** - 删除临时文件 `metadata.json` 和 `transcription.json`
- **🎨 Rich 终端界面** - 美观的格式化输出，带面板和颜色

完整 v1.1.0 详情请参阅 **[CHANGELOG.md](./CHANGELOG.md)**。

## 🎯 核心功能

- **📝 丰富的 Markdown 输出** - 带元数据表、时间戳和格式的结构化报告
- **🎙️ 说话人分离** - 自动识别并标记不同的说话人
- **📊 技术元数据** - 提取文件大小、时长、语言、处理时间
- **📋 智能会议纪要/摘要** - 通过 LLM（Claude/Copilot）生成，支持自定义提示词
- **💡 执行摘要** - AI 生成的结构化摘要，包含主题、决策、行动项
- **🌍 多语言** - 支持 99 种语言，自动检测
- **⚡ 零配置** - 自动发现 Faster-Whisper/Whisper 安装
- **🔒 隐私优先** - 100% 本地 Whisper 处理，无需上传云端
- **🚀 灵活模式** - 仅转录或使用 LLM 智能处理

## 📦 安装

### 快速安装（NPX）

```bash
npx cli-ai-skills@latest install audio-transcriber
```

这将自动：
- 下载技能
- 安装 Python 依赖（faster-whisper、tqdm、rich）
- 安装 ffmpeg（macOS 通过 Homebrew）
- 全局设置技能

### 手动安装

#### 1. 安装转录引擎

**推荐（最快）：**
```bash
pip install faster-whisper tqdm rich
```

**备选（原始 Whisper）：**
```bash
pip install openai-whisper tqdm rich
```

#### 2. 安装音频工具（可选）

用于格式转换支持：
```bash
# macOS
brew install ffmpeg

# Linux
apt install ffmpeg
```

#### 3. 安装 LLM CLI（可选 - 用于智能摘要）

**Claude CLI（推荐）：**
```bash
# 参考: https://docs.anthropic.com/en/docs/claude-cli
```

**GitHub Copilot CLI（备选）：**
```bash
gh extension install github/gh-copilot
```

#### 4. 安装技能

**全局安装（通过 git pull 自动更新）：**
```bash
cd /path/to/cli-ai-skills
./scripts/install-skills.sh $(pwd)
```

**仅仓库：**
```bash
# 如果克隆了仓库，技能已经可用
```

## 🚀 使用方法

### 基本转录

```bash
copilot> transcribe audio to markdown: meeting.mp3
```

**输出：**
- `meeting.md` - 完整 Markdown 报告，包含元数据、转录文本、会议纪要、摘要

### 带字幕

```bash
copilot> convert audio file to text with subtitles: interview.wav
```

**生成：**
- `interview.md` - Markdown 报告
- `interview.srt` - 字幕文件

### 批量处理

```bash
copilot> transcreva estes áudios: recordings/*.mp3
```

**处理目录中的所有 MP3 文件。**

### 触发短语

使用以下任意短语激活技能：

- "transcribe audio to markdown"
- "transcreva este áudio"
- "convert audio file to text"
- "extract speech from audio"
- "áudio para texto com metadados"
- "音频转文字"
- "转录音频"
- "会议记录"

## 📋 使用场景

### 1. 团队会议
录制站会、规划会议或回顾会议，自动生成：
- 参与者列表
- 带时间戳的讨论主题
- 做出的决策
- 分配的行动项

### 2. 客户通话
转录客户对话，包含：
- 说话人识别
- 关键协议文档
- 提取后续任务

### 3. 访谈
将访谈转换为文字，包含：
- 问答归属
- 视频字幕生成
- 可搜索的转录文本

### 4. 讲座与培训
记录教育内容，包含：
- 带时间戳的笔记
- 主题分解
- 关键概念摘要

### 5. 内容创作
分析播客、视频、YouTube 内容：
- 完整转录
- 章节标记（时间戳）
- 节目说明摘要

## 📊 输出示例

```markdown
# 音频转录报告

## 📊 元数据

| 字段 | 值 |
|------|------|
| **文件名** | team-standup.mp3 |
| **文件大小** | 3.2 MB |
| **时长** | 00:12:47 |
| **语言** | English (en) |
| **处理日期** | 2026-02-02 14:35:21 |
| **识别的说话人** | 5 |
| **转录引擎** | Faster-Whisper (模型: base) |

---

## 🎙️ 完整转录

**[00:00:12 → 00:00:45]** *Speaker 1*  
Good morning everyone. Let's start with updates from the frontend team.

**[00:00:46 → 00:01:23]** *Speaker 2*  
We completed the dashboard redesign and deployed to staging yesterday.

---

## 📋 会议纪要

### 参与者
- Speaker 1 (会议主持)
- Speaker 2 (前端开发)
- Speaker 3 (后端开发)
- Speaker 4 (设计师)
- Speaker 5 (产品经理)

### 讨论主题
1. **仪表板重设计** (00:00:46)
   - 已完成并部署到预发布环境
   - QA 团队反馈积极

2. **API 性能问题** (00:03:12)
   - 需要数据库查询优化
   - 目标响应时间 < 200ms

### 做出的决策
- ✅ 批准仪表板部署到生产环境
- ✅ 为 API 优化分配 2 个冲刺点

### 行动项
- [ ] **将仪表板部署到生产环境** - 负责人: Speaker 2 - 截止: 2026-02-05
- [ ] **优化数据库查询** - 负责人: Speaker 3
- [ ] **安排用户测试会议** - 负责人: Speaker 5

---

## 📝 执行摘要

团队站会讨论了仪表板重设计的进展，该工作已成功完成并准备部署到生产环境。前端团队收到了 QA 的积极反馈，设计符合用户需求。

后端性能问题被提出，涉及 API 响应时间。团队决定在当前冲刺中优先处理查询优化，目标是响应时间低于 200ms。

下一步包括本周内将仪表板部署到生产环境，并安排用户测试会议以验证新设计与真实用户的体验。

### 关键要点
- 🔹 仪表板重设计完成并通过预发布审核
- 🔹 API 性能优化已优先安排
- 🔹 用户测试安排在下周

### 后续步骤
1. 生产环境部署 (Speaker 2)
2. 数据库优化 (Speaker 3)
3. 用户测试协调 (Speaker 5)
```

## ⚙️ 配置

无需配置！技能会自动：
- 检测 Faster-Whisper 或 Whisper 安装
- 选择最快的可用引擎
- 根据文件大小选择合适的模型
- 自动检测语言

## 🔧 故障排除

### "No transcription tool found"
**解决方案：** 安装 Whisper：
```bash
pip install faster-whisper
```

### "Unsupported format"
**解决方案：** 安装 ffmpeg：
```bash
brew install ffmpeg  # macOS
apt install ffmpeg   # Linux
```

### 处理速度慢
**解决方案：** 使用较小的 Whisper 模型：
```bash
# 编辑技能使用 "tiny" 或 "base" 模型而非 "medium"
```

### 说话人识别效果差
**解决方案：** 
- 确保音频清晰，背景噪音少
- 录制时使用更好的麦克风
- 尝试 "medium" 或 "large" Whisper 模型

## 🛠️ 高级用法

### 自定义模型选择

编辑 `SKILL.md` 步骤 2 更改模型：
```python
model = WhisperModel("small", device="cpu")  # 将 "base" 改为 "small"、"medium" 等
```

### 输出语言控制

强制输出特定语言：
```bash
# 编辑步骤 3 显式设置语言
```

### 批量设置

仅处理特定文件类型：
```bash
copilot> transcribe audio: recordings/*.wav  # 仅 WAV 文件
```

## 📚 常见问题

**问：可以离线使用吗？**  
答：可以！100% 本地处理，初始模型下载后无需联网。

**问：Whisper 和 Faster-Whisper 有什么区别？**  
答：Faster-Whisper 快 4-5 倍，质量相同。如果可用，始终优先选择它。

**问：可以转录 YouTube 视频吗？**  
答：不能直接转录。需要先使用 YouTube 下载器，然后转录音频文件。或改用 `youtube-summarizer` 技能。

**问：说话人识别有多准确？**  
答：准确度取决于音频质量。清晰的录音和独特的声音效果最好。目前使用简单估算；未来版本将使用高级说话人分离技术。

**问：支持哪些语言？**  
答：99 种语言，包括英语、葡萄牙语、西班牙语、法语、德语、中文、日语、阿拉伯语等。

**问：可以编辑会议纪要格式吗？**  
答：可以！编辑 SKILL.md 步骤 3 中的 Markdown 模板。

## 🔗 相关技能

- **youtube-summarizer** - 提取和摘要 YouTube 视频转录文本
- **prompt-engineer** - 优化提示词以获得更好的 AI 摘要

## 📄 许可证

本技能是 cli-ai-skills 仓库的一部分。  
MIT 许可证 - 详见仓库 LICENSE 文件。

## 🤝 贡献

发现 bug 或有功能建议？  
在 [cli-ai-skills 仓库](https://github.com/yourusername/cli-ai-skills) 提交 issue。

---

**版本：** 1.0.0  
**作者：** Eric Andrade  
**创建日期：** 2026-02-02
