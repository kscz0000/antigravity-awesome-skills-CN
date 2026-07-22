---
name: ux-audit
description: "基于 Nielsen 启发式原则和移动端 UX 最佳实践审计界面，以 StyleSeed Toss 设计语言为实现上下文。触发词：UX审计、可用性审计、Nielsen启发式、移动端UX、界面审计、用户体验审查、StyleSeed"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ux, audit, usability, mobile, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UX Audit

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此技能审计可用性而非仅仅视觉效果。它使用 Nielsen 的 10 条启发式原则加上现代移动端 UX 预期，发现导航、反馈、恢复、层次结构和认知负荷方面的问题。

## 何时使用
- 当界面感觉别扭但代码和样式看起来正确时使用
- 在实现前后评估流程时使用
- 审查移动优先产品的可用性退化时使用
- 当你希望发现被框架为用户体验问题并提供修复建议时使用

## 审计框架

根据以下内容审查目标：
- 系统状态可见性
- 系统与现实世界语言的匹配
- 用户控制与自由
- 一致性与标准
- 错误预防
- 识别而非回忆
- 灵活性与效率
- 美观与极简设计
- 错误恢复
- 帮助、引导和空状态指导

添加移动端特定检查：可达性、触控人体工程学、输入负担和拇指友好的操作位置。

## 输出

返回：
1. 按优先级排序的问题列表
2. 每个问题违反的启发式原则
3. 为什么该问题对真实用户重要
4. 针对页面、组件或流程的具体修复建议

## 最佳实践

- 从用户而非实现者的角度评判体验
- 将高严重性的流程阻塞问题与次要的打磨问题分开
- 包含恢复和状态管理指导，而不仅是布局评论
- 将建议关联到具体的 UI 变更

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-audit/SKILL.md)

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
