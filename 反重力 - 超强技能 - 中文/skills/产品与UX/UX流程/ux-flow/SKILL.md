---
name: ux-flow
description: "使用 StyleSeed UX 模式设计用户流程和屏幕结构，如渐进式披露、轮毂式导航和信息金字塔。触发词：用户流程、UX流程、屏幕结构、导航设计、信息架构、渐进式披露、hub-and-spoke、onboarding流程、checkout流程"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ux, flows, navigation, product-design, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UX Flow

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此技能在绘制屏幕之前先设计流程。它使用经过验证的 UX 模式来定义入口点、出口、屏幕清单和导航结构，使实现具有连贯的用户旅程，而非一堆互不关联的页面。

## 何时使用
- 规划引导流程、结账流程、账户管理、仪表板或下钻流程时使用
- 新功能跨越多个屏幕或模态状态时使用
- 用户需要通过任务的清晰路径而非单个孤立页面时使用
- 在构建组件之前，UI 需要导航逻辑时使用

## 工作原理

### 信息架构原则

- 渐进式披露：仅在需要时揭示复杂性
- 米勒定律：将内容分块为可管理的组
- 希克定律：最小化每个屏幕的决策过载

### 常见导航模型

- 轮毂式：用于仪表板和详情视图
- 线性流程：用于引导、表单和结账
- 标签导航：用于 3 到 5 个顶级区域

### 流程规则

- 每个流程都有明确的入口点
- 每个流程都有明确的出口或成功条件
- 关键功能通常应可在主页三次点击内到达
- 非根屏幕需要返回导航
- 加载、空状态和错误状态需要明确的恢复路径

## 输出

提供：
1. ASCII 流程图
2. 屏幕清单，包含每个屏幕的用途
3. 加载、空状态和错误状态的边缘情况
4. 推荐接下来实现的页面脚手架和可复用模式

## 最佳实践

- 优先考虑清晰度而非密度
- 让一个屏幕回答一个主要问题
- 对于有风险或破坏性的步骤，保持逃生通道可见
- 在绘制详细布局之前定义状态转换

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-flow/SKILL.md)

## 局限性
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
