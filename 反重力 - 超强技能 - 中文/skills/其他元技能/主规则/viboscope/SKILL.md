---
name: viboscope
description: "心理兼容性匹配——通过验证的心理测量学找到联合创始人、合作者和朋友。触发词：寻找联合创始人、寻找合作伙伴、心理兼容性、性格匹配、合作匹配、cofounder matching、compatibility test"
category: collaboration
risk: safe
source: community
date_added: "2026-03-29"
author: ivanschmidt
tags: [matching, psychology, compatibility, networking, collaboration]
tools: [claude, cursor, codex, gemini, windsurf]
---

# Viboscope

## 概述

Viboscope 帮助通过深度心理兼容性匹配找到合适的人——联合创始人、项目合作伙伴、朋友、恋爱伴侣。它在10个验证维度上建立档案，并与其他用户计算数学兼容性。

## 何时使用此技能

- 寻找联合创始人或项目合作者时使用
- 想要找到工作风格和价值观兼容的人时使用
- 通过邀请链接检查与特定人的兼容性时使用

## 工作原理

### 步骤 1：安装

```bash
curl -fsS https://viboscope.com/api/v1/skill -o viboscope.md
```

保存到您平台的技能目录。

### 步骤 2：建立档案

该技能引导一个5分钟的入门流程，使用以下方式建立心理档案：
- AI 助手画像（最快——2分钟完成90%以上的档案）
- 5份验证问卷（大五人格、价值观、依恋、冲突、工作风格）
- 从工作区文件进行上下文扫描

### 步骤 3：搜索

在7个情境中搜索：商业、恋爱、友谊、专业、智力、爱好、一般。结果包含百分比分数和人类可读的匹配原因解释。

## 示例

### 示例 1：寻找联合创始人

告诉您的 AI 代理："Install Viboscope and find me a cofounder"

代理将引导您完成档案建立，然后搜索商业兼容的匹配对象，具有一致的价值观和互补的工作风格。

### 示例 2：检查兼容性

分享您的邀请链接：`viboscope.com/match/@your_nick`

当有人用他们的 AI 代理打开它时，双方都能看到兼容性分析。

## 链接

- 网站：https://viboscope.com
- GitHub：https://github.com/ivankoriako/viboscope
- API：https://viboscope.com/api/v1

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
