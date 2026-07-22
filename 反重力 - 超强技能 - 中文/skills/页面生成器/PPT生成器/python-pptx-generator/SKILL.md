---
name: python-pptx-generator
description: "生成使用 python-pptx 构建精美 PowerPoint 演示文稿的完整 Python 脚本，包含真实幻灯片内容。触发词：生成PPT、创建PowerPoint、python-pptx脚本、演示文稿生成、幻灯片制作、PPT脚本"
category: development
risk: safe
source: self
source_type: self
date_added: "2026-04-06"
author: spideyashith
tags: [python, powerpoint, python-pptx, presentations, slide-decks]
tools: [claude, cursor, gemini, codex]
---

# Python PPTX Generator

## 概述

当用户需要一个可直接运行的 Python 脚本来使用 `python-pptx` 创建 PowerPoint 演示文稿时，使用此技能。
它专注于将主题简报转化为完整的幻灯片脚本，包含真实的幻灯片内容、合理的结构和可工作的保存步骤。

## 使用场景

- 当用户需要自动生成 `.pptx` 文件的 Python 脚本时
- 当用户需要将幻灯片内容直接编写并编码到 `python-pptx` 中时
- 当用户需要为演示、课堂或内部简报快速生成演示文稿时

## 工作流程

### 第 1 步：收集演示文稿简报

如果请求中未包含主题、受众、语气和目标幻灯片数量，请主动询问。
如果缺少约束条件，选择保守的默认值并在生成的脚本注释中说明。

### 第 2 步：规划叙事结构

在编写代码之前先规划演示文稿大纲：

1. 标题幻灯片
2. 议程或背景
3. 核心教学或业务要点
4. 总结或后续步骤

保持幻灯片数量符合目标受众的需求，避免填充性质的幻灯片。

### 第 3 步：生成 Python 脚本

编写完整的脚本，要求：

- 从 `python-pptx` 导入 `Presentation`
- 创建演示文稿
- 选择合适的内置布局
- 编写真实的标题和要点内容
- 使用清晰的文件名保存文件
- 保存后打印成功消息

### 第 4 步：确保输出可运行

最终答案应该是一个安装 `python-pptx` 后即可运行的 Python 代码块。
避免伪代码、占位符或缺失导入。

## 示例

### 示例 1：教学演示文稿

```text
User: Create a 5-slide presentation on the basics of machine learning for a high school class.
Output: A complete Python script that creates a title slide, overview, core concepts, examples, and recap.
```

### 示例 2：业务简报

```text
User: Generate a 7-slide deck for sales leadership on Q2 pipeline risks and mitigation options.
Output: A python-pptx script with executive-friendly slide titles, concise bullets, and a final recommendations slide.
```

## 最佳实践

- ✅ 除非用户要求自定义定位，否则使用标准 `python-pptx` 布局
- ✅ 编写适合受众的要点内容，而非占位符
- ✅ 在脚本中显式保存输出文件，例如 `output.pptx`
- ✅ 保持幻灯片标题简短，要点层次清晰易读
- ❌ 不要返回需要用户自行组装的代码片段
- ❌ 不要在未确认 `python-pptx` 功能的情况下使用不支持的样式 API

## 安全说明

- 仅在你控制的环境中安装 `python-pptx`，例如本地虚拟环境
- 如果用户将在共享机器上运行脚本，选择安全的输出路径，避免未经确认覆盖现有演示文稿
- 如果请求包含专有或敏感的演示内容，请勿将其放入公开示例或示例文件名中

## 常见问题

- **问题：** 生成的脚本使用占位符文本而非真实内容
  **解决：** 先撰写叙述内容，然后将每张幻灯片转化为具体的标题和要点

- **问题：** 演示文稿对目标受众来说幻灯片数量过多
  **解决：** 将大纲压缩为最重要的 4 到 8 张幻灯片，除非用户明确需要更多

- **问题：** 脚本忘记保存或打印完成消息
  **解决：** 始终以 `prs.save(...)` 和简短的成功提示结尾

## 相关技能

- `@pptx-official` - 当任务涉及检查或编辑现有 PowerPoint 文件时使用
- `@docx-official` - 当请求的输出是文档而非幻灯片时使用

## 使用限制

- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来寻求澄清。
