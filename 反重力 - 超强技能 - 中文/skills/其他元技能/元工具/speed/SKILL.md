---
name: speed
description: 启动 RSVP 快速阅读器显示文本。当用户要求"快速阅读"、"速读"、"RSVP阅读"、"Spritz阅读"、"单词逐个显示"时使用。
trigger: command
risk: unknown
source: community
tools: Write, Bash, Read
---

# 快速阅读器

启动 RSVP 快速阅读器，以 Spritz 风格的 ORP（最佳识别点）高亮逐词显示文本。

## 使用场景

- 你想在当前会话中为文本启动 RSVP 快速阅读器。
- 任务是将提供的文本或助手之前的回复转换为逐词阅读视图。
- 你需要快速阅读辅助工具，而非文档转换或摘要。

## 操作说明

1. **获取文本：**
   - 如果提供了 `$ARGUMENTS`，使用该文本
   - 否则，从本次对话中你**之前的回复**中提取主要内容

2. **准备内容：**
   - 去除 Markdown 格式（标题、粗体、链接、代码块）
   - 保留干净、可读的文本
   - 为 JavaScript 转义引号和反斜杠

3. **写入并启动：**
   - 读取 `~/.claude/skills/speed/data/reader.html`
   - 将 `<!-- CONTENT_PLACEHOLDER -->` 替换为：
     ```html
     <script>window.SPEED_READER_CONTENT = "your escaped text";</script>
     <!-- CONTENT_PLACEHOLDER -->
     ```
   - 运行：`open ~/.claude/skills/speed/data/reader.html`

4. **确认：** 告诉用户正在打开。提及按 `空格键` 播放/暂停。

## 参数

$ARGUMENTS

## 限制

- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
