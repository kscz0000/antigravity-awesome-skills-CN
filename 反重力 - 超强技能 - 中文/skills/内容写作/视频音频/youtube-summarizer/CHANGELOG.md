# 变更日志 - youtube-summarizer

本文件记录了 youtube-summarizer 技能的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/spec/v2.0.0.html)。

---

## [1.2.1] - 2026-02-04

### 🐛 修复

- **`--list` 模式下的退出码传递**
  - **问题：** 即使 `list_available_transcripts()` 失败，脚本总是以状态 0 退出
  - **风险：** 破坏了依赖退出码检测失败的自动化流水线
  - **根本原因：** 忽略了 `list_available_transcripts()` 的返回值
  - **解决方案：** 现在正确检查返回值并在失败时以退出码 1 退出
  - **影响：** 自动化中的脚本现在可以正确检测转录列表何时失败（无效的视频 ID、网络错误等）

### 🔧 变更

- `extract-transcript.py`（第 58-60 行）
  - 变更前：`list_available_transcripts(video_id); sys.exit(0)`
  - 变更后：`success = list_available_transcripts(video_id); sys.exit(0 if success else 1)`

### 📝 备注

- **破坏性变更：** 无 —— 仅影响错误处理行为
- **向后兼容性：** 检查退出码的脚本现在将正常工作
- **迁移：** 现有用户无需任何更改

### 🔗 相关

- 由 Codex 自动审查在 antigravity-awesome-skills PR #62 中识别
- 已在 antigravity-awesome-skills 分支中修复

---

## [1.2.0] - 2026-02-04

### ✨ 新增

- 智能提示词工作流集成
- 使用 Claude CLI 或 GitHub Copilot CLI 进行 LLM 处理
- 带有丰富终端 UI 的进度指示器
- 多种输出格式
- 增强的错误处理

### 🔧 变更

- 转录文本提取逻辑的重大重构
- 改进了 SKILL.md 中的文档
- 更新了安装要求

---

## [1.0.0] - 2025-02-01

### ✨ 首次发布

- YouTube 转录文本提取
- 语言检测与选择
- 基础摘要功能
- Markdown 输出格式
- 多语言支持
