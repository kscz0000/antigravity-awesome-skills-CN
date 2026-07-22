---
name: ux-copy
description: "为按钮、空状态、错误、提示、确认和表单引导生成 StyleSeed 的 Toss 风格 UX 微文案。触发词：UX文案、微文案、按钮文案、错误提示、空状态文案、表单提示、Toast文案、确认对话框文案"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ux, copywriting, microcopy, frontend, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UX Copy

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此技能为常见 UI 状态生成简洁的产品文案。遵循 Toss 风格的语调：随意但礼貌、直接、主动，且足够具体以帮助用户恢复或继续操作。

## 何时使用
- 需要按钮标签、帮助文本、提示、空状态或错误消息时使用
- 功能已有 UI 但措辞薄弱或机械时使用
- 希望在整个流程中保持一致的产品语调时使用
- 确认对话框或状态反馈需要更好的措辞时使用

## 语调规则

- 随意但礼貌
- 主动语态优于被动语态
- 在保持诚实的前提下使用积极框架
- 使用平实语言而非内部术语
- 措辞简洁，每个词都有其存在的价值

## 常见模式

### 按钮

需要时使用简短的动作动词加对象。

### 空状态

以友好的观察开头，然后建议下一步操作。

### 错误

用用户能理解的语言解释发生了什么以及接下来该怎么做。不要暴露原始的内部错误字符串。

### 提示

快速确认结果。对于可逆的破坏性操作，添加撤销操作。

### 表单

使用清晰的标签、有用的占位符、具体的帮助文本和纠正性的错误消息。

### 确认对话框

用平实语言陈述操作，如果决策有风险或不可逆，解释其后果。

## 输出

返回：
1. 按 UI 表面分组的请求微文案
2. 关于语调或本地化的注意事项（如相关）
3. 除更好的文案外，UX 可能还需要结构性修复的地方

## 最佳实践

- 让下一步操作显而易见
- 当操作可以精确命名时，避免使用 "Submit" 或 "OK" 等通用标签
- 当出现问题时归咎于系统，而非用户
- 即使没有视觉上下文，错误和空状态也应保持有用

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-copy/SKILL.md)

## 局限性
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
