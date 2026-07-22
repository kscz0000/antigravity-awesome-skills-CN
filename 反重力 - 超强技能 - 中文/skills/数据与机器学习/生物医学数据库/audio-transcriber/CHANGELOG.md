# 更新日志 - audio-transcriber

本文件记录 audio-transcriber 技能的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

---

## [1.1.0] - 2026-02-03

### ✨ 新增

- **智能提示词工作流**（步骤 3b）- 与 prompt-engineer 技能完整集成
  - **场景 A**：用户提供的提示词自动通过 prompt-engineer 改进
    - 并排显示原始版本和改进版本
    - 单次确认："使用改进版本？[s/n]"
  - **场景 B**：无提示词时自动生成
    - 分析转录文本并建议文档类型（会议纪要、摘要、笔记）
    - 显示建议并请求确认
    - 生成完整结构化提示词（RISEN/RODES/STAR）
    - 显示预览并请求最终确认
    - 如果拒绝则回退到 DEFAULT_MEETING_PROMPT

- **LLM 集成** - 使用 Claude CLI 或 GitHub Copilot CLI 处理转录文本
  - 优先级：Claude > GitHub Copilot > 无（仅转录模式）
  - 步骤 0b：CLI 检测逻辑已文档化
  - 超时处理（默认 5 分钟）
  - CLI 不可用时优雅回退

- **进度指示器** - 长时间操作的可视化反馈
  - `tqdm` 进度条用于 Whisper 转录片段
  - `rich` 旋转器用于 LLM 处理
  - 每个步骤的清晰状态消息

- **基于时间戳的文件命名** - 避免覆盖之前的转录
  - 格式：`transcript-YYYYMMDD-HHMMSS.md`
  - 格式：`ata-YYYYMMDD-HHMMSS.md`
  - 防止重复运行导致数据丢失

- **自动清理** - 处理后删除临时文件
  - 自动删除 `metadata.json` 和 `transcription.json`
  - `--keep-temp` 标志可保留（如需要）
  - 清理输出目录

- **Rich 终端界面** - 使用 `rich` 库的美观输出
  - 提示词预览的格式化面板
  - 颜色编码的状态消息（绿色=成功，黄色=警告，红色=错误）
  - 长时间运行任务的旋转动画

- **双输出支持** - 同时生成转录文本和处理后的会议纪要
  - `transcript-*.md` - 带时间戳的原始转录
  - `ata-*.md` - 智能摘要/会议纪要（如果 LLM 可用）
  - 用户可拒绝 LLM 处理以获取仅转录结果

### 🔧 变更

- **SKILL.md** - 主要文档更新
  - 新增步骤 0b（CLI 检测）
  - 更新步骤 2（进度指示器）
  - 新增步骤 3b（智能提示词工作流，150+ 行）
  - 版本更新至 1.1.0
  - 为两种场景添加详细工作流程图

- **install-requirements.sh** - 添加 UI 库
  - 现在安装 `tqdm` 和 `rich` 包
  - 安装失败时优雅回退
  - 更新成功消息

- **Python 实现** - 完全重构
  - 创建 `scripts/transcribe.py`（516 行）
  - 函数：`detect_cli_tool()`、`invoke_prompt_engineer()`、`handle_prompt_workflow()`、`process_with_llm()`、`transcribe_audio()`、`save_outputs()`、`cleanup_temp_files()`
  - 命令行参数：`--prompt`、`--model`、`--output-dir`、`--keep-temp`
  - 如果缺失则自动安装 `rich` 和 `tqdm`

### 🐛 修复

- **用户提示词不再被忽略** - v1.0.0 完全忽略自定义提示词
  - 现在使用 LLM 处理所有提示词（自定义或自动生成）
  - 将简单提示词改进为结构化框架

- **临时文件清理** - v1.0.0 将 `metadata.json` 和 `transcription.json` 作为垃圾留下
  - 现在处理后自动删除
  - 清理输出目录

- **文件覆盖** - v1.0.0 每次使用相同文件名（如 `meeting.md`）
  - 现在使用时间戳防止数据丢失
  - 每次运行创建唯一文件

- **缺少会议纪要/摘要** - v1.0.0 仅生成原始转录
  - 现在使用 LLM 生成智能会议纪要/摘要
  - 遵循用户的提示词指令

- **无进度反馈** - v1.0.0 处理过程静默（用户不知道是否卡住）
  - 现在显示转录进度条
  - 显示 LLM 处理旋转器
  - 全程清晰的状态消息

### 📝 说明

- **向后兼容性：** 完全兼容 v1.0.0 工作流
- **要求：** Python 3.8+、faster-whisper 或 whisper、tqdm、rich
- **可选：** Claude CLI 或 GitHub Copilot CLI 用于智能处理
- **可选：** prompt-engineer 技能用于自动提示词生成

### 🔗 相关问题

- 修复 #1：用户 RISEN 提示词被忽略
- 修复 #2：临时文件（metadata.json、transcription.json）作为垃圾留下
- 修复 #3：输出不完整（仅原始转录，无会议纪要）
- 修复 #4：缺少可视化进度指示器
- 修复 #5：输出格式无时间戳

---

## [1.0.0] - 2026-02-02

### ✨ 初始发布

- 使用 Faster-Whisper 或 OpenAI Whisper 进行音频转录
- 自动语言检测
- 说话人分离（基础）
- 语音活动检测（VAD）
- 带元数据表的 Markdown 输出
- 依赖安装脚本
- 基本转录示例脚本
- 支持多种音频格式（MP3、WAV、M4A、OGG、FLAC、WEBM）
- FFmpeg 集成用于格式转换
- 零配置理念

### 📝 已知限制（在 v1.1.0 中修复）

- 用户提示词被忽略（无 LLM 集成）
- 仅生成原始转录（无会议纪要/摘要）
- 临时文件未清理
- 无进度指示器
- 重复运行时文件被覆盖
