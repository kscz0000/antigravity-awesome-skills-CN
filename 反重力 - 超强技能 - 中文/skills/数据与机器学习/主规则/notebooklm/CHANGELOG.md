# 变更日志

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

## [1.3.0] - 2025-11-21

### 新增
- **模块化架构** - 重构代码库以提高可维护性
  - 新增 `config.py` - 集中配置（路径、选择器、超时）
  - 新增 `browser_utils.py` - BrowserFactory 和 StealthUtils 类
  - 所有脚本更清晰的关注点分离

### 变更
- **超时增加到 120 秒** - 长查询不再过早超时
  - `ask_question.py`：30秒 → 120秒
  - `browser_session.py`：30秒 → 120秒
  - 解决 Issue #4

### 修复
- **思考消息检测** - 修复不完整答案显示占位符文本
  - 现在等待 `div.thinking-message` 元素消失后再读取答案
  - 「正在审查内容...」或「正在寻找答案...」等答案不再过早返回
  - 在所有语言和 NotebookLM UI 变更中可靠工作

- **正确的 CSS 选择器** - 更新以匹配当前 NotebookLM UI
  - 从 `.response-content, .message-content` 更改为 `.to-user-container .message-text-content`
  - 所有脚本使用一致的选择器

- **稳定性检测** - 改进答案完整性检查
  - 现在需要 3 次连续稳定轮询而不是 1 秒等待
  - 防止流式传输期间截断响应

## [1.2.0] - 2025-10-28

### 新增
- 初始公开发布
- 通过浏览器自动化集成 NotebookLM
- 基于 Gemini 2.5 的会话式对话
- 笔记本库管理
- 知识库准备工具
- Google 认证与持久会话
