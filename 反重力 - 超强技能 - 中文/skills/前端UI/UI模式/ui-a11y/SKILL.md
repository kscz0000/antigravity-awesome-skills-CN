---
name: ui-a11y
description: "审查基于 StyleSeed 的组件或页面的 WCAG 2.2 AA 问题，并在代码安全的情况下应用实用的无障碍修复。当用户要求审查无障碍问题、检查 WCAG 合规性、修复无障碍缺陷、审计 UI 可访问性时使用。"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, accessibility, wcag, audit, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI 无障碍审计

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此技能审计组件和页面的无障碍问题，重点关注 Toss seed 的移动 UI 模式。它结合 WCAG 2.2 AA 检查与实用的代码修复，涵盖触摸目标、焦点状态、对比度、标签和减少动画等方面。

## 使用时机

- 审查页面或组件的无障碍回归问题时使用
- StyleSeed UI 看起来精致但键盘或对比度行为不确定时使用
- 在移动优先的屏幕上添加新的交互控件时使用
- 需要按优先级排列的问题列表和可修复项时使用

## 审计领域

### 可感知

- 文本对比度
- 控件和图形的非文本对比度
- 图片的替代文本
- 有意义图标的标签
- 不单独通过颜色传达信息

### 可操作

- 触摸目标至少 44x44px
- 所有交互控件的键盘可达性
- 逻辑 Tab 顺序
- 可见的焦点指示器
- 非必要动画的减少动画支持

### 可理解

- 输入框上的可见标签或 `aria-label`
- 与正确字段关联的错误文本
- 错误和验证的清晰措辞
- 文档语言设置正确

### 健壮

- 尽可能使用语义化 HTML
- 仅在语义不足时正确使用 ARIA
- 没有缺少正确角色和行为的假按钮或链接

## 输出

返回：
1. 发现的问题，按严重程度分组
2. 可直接应用的安全自动修复
3. 需要人工审查或产品判断的项目
4. 无障碍风险级别的简短摘要

## 最佳实践

- 在添加 ARIA 之前先修复语义
- 仅当设计系统 token 仍满足对比度要求时才使用
- 将触摸目标失败视为真正的可用性缺陷，而非润色问题
- 优先选择部分、已验证的修复，而非推测性的无障碍更改

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-a11y/SKILL.md)

## 限制

- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
