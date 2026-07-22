---
name: technical-change-tracker
description: "通过结构化 JSON 记录、状态机和 AI 会话交接追踪代码变更，确保机器人会话连续性"
category: development
risk: safe
source: community
source_repo: Elkidogz/technical-change-skill
source_type: community
date_added: "2026-04-05"
author: Elkidogz
tags: [change-tracking, session-handoff, documentation, accessibility, state-machine]
tools: [claude, cursor, gemini, codex]
---

# 技术变更追踪器

## 概述

通过结构化 JSON 记录和无障碍 HTML 输出追踪每次代码变更。确保 AI 机器人会话在前一个会话过期或被放弃时能无缝恢复。

## 适用场景

- 需要在 AI 编码会话间进行结构化变更追踪
- 机器人会话在任务中途过期，下一个会话需要完整上下文才能继续
- 接手变更历史未文档化的项目

## 工作原理

### 状态机

```
planned -> in_progress -> implemented -> tested -> deployed
             |
             +-> blocked
```

### 命令

`/tc init` | `/tc create` | `/tc update` | `/tc status` | `/tc resume` | `/tc close` | `/tc export` | `/tc dashboard` | `/tc retro`

### 会话交接

每个 TC 存储：进度摘要、后续步骤、阻塞项、关键上下文和正在处理的文件——让下一个机器人会话能准确接续上一个会话的工作。

### 非阻塞式

TC 记账任务通过后台子智能体运行，不会中断编码工作。

## 特性

- 带有仅追加修订历史的结构化 JSON 记录
- 附带日志片段证据的测试用例
- 符合 WCAG AA+ 标准的无障碍 HTML 输出（暗色主题、rem 单位字体）
- 纯 CSS 仪表盘，支持状态筛选
- 仅依赖 Python 标准库——零外部依赖
- 通过 `/tc retro` 从 git 历史批量回溯创建记录

## 完整仓库

https://github.com/Elkidogz/technical-change-skill — MIT 许可证

## 限制

- 仅当任务明确匹配上述范围时才使用此技能
- 输出结果不能替代特定环境的验证、测试或专家审查
- 如果缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清