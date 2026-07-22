---
name: ux-feedback
description: "为 StyleSeed 组件和页面添加加载、空态、错误和成功反馈状态，附带实用的移动端优先规则。触发词：ux-feedback、反馈状态、加载状态、空态、错误处理、状态管理"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ux, states, loading, error-handling, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UX 反馈状态

## 概述

本技能属于 [StyleSeed](https://github.com/bitjaru/styleseed)，确保依赖数据的 UI 不会只走"快乐路径"。它为每个严肃产品补齐四种核心反馈状态：加载、空态、错误和成功。

## 使用场景
- 当组件或页面需要获取、修改或依赖异步数据时使用
- 当某个流程目前只渲染成功路径时使用
- 当卡片、列表或页面需要更好的状态传达时使用
- 当产品需要清晰的恢复和确认行为时使用

## 四种必选状态

### 加载

使用与最终布局匹配的骨架屏。除非该模式确实需要，否则避免在卡片内使用旋转指示器。骨架屏应略有延迟，避免快速响应时出现闪烁。

### 空态

提供友好的说明和下一步操作指引。零值也应有意义地渲染，而不是直接消失。

### 错误

使用通俗易懂的失败信息，并尽可能提供恢复途径。如果页面其余部分仍可正常工作，将失败限定在受影响的卡片或区域。

### 成功

使用 toast 或类似的轻量确认方式反馈已完成的操作。对于可撤销的破坏性变更，提供撤消功能。

## 输出内容

返回：
1. 识别出的依赖数据区域
2. 为每个区域添加的加载、空态、错误和成功状态
3. 创建的可复用空态或 toast 模式
4. 后续需要处理的分析埋点、重试机制或无障碍适配工作

## 最佳实践

- 加载占位符要与真实布局保持一致
- 尽可能将局部失败隔离开来
- 让恢复操作显而易见，而不是藏在日志或开发者工具里
- 成功反馈要适度使用，但要清晰明确

## 扩展资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-feedback/SKILL.md)

## 限制说明
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出内容视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
