---
name: ui-review
description: "审查 UI 代码是否符合 StyleSeed 设计系统规范、无障碍性、移动端人体工学、间距规范和实现质量。当用户要求'审查 UI'、'检查设计系统'、'UI 代码审查'、'无障碍检查'、'移动端适配检查'、'StyleSeed 审查'时使用。"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, review, design-system, accessibility, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI 审查

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此技能根据 Toss seed 的约定审查 UI 代码，而不是将其作为通用前端工作进行审查。它专注于设计令牌规范、组件人体工学、无障碍性、移动端就绪度、排版和间距一致性。

## 使用时机

- 当组件或页面应遵循 StyleSeed Toss 设计语言时使用
- 当审查 UI 密集型 PR 的一致性和设计系统违规时使用
- 当输出看起来"基本没问题"但感觉有些微妙的不对劲时使用
- 当需要结构化审查和具体修复方案时使用

## 审查清单

### 设计令牌

- 当存在语义令牌时，不使用硬编码的十六进制颜色
- 当存在令牌化的阴影时，不使用即兴的阴影值
- 不使用系统比例之外的任意圆角选择
- 不使用破坏 seed 节奏的随机间距值

### 组件约定

- 使用项目的 class merge 辅助函数
- 在适当时支持 `className` 扩展
- 使用约定的类型模式
- 避免仅转发一个类字符串的包装组件
- 在发明新组件之前重用现有原语

### 无障碍性

- 触摸目标足够大以适应移动端
- 可见的键盘焦点状态
- 在需要的地方使用标签和 `aria-*` 属性
- 充足的颜色对比度
- 动画尊重减少动效偏好

### 移动端 UX

- 无水平溢出
- 在相关位置处理安全区域
- 可读的文本大小
- 适合拇指操作的交互间距
- 底部导航或固定操作不会遮挡内容

### 排版和间距

- 使用系统的排版层级
- 标题和展示文本不过于松散
- 正文文本保持可读
- 间距遵循 seed 网格而非任意值

## 输出格式

返回：
1. 结论：通过、需要改进或失败
2. 按优先级排序的问题列表，尽可能包含文件和行引用
3. 每个问题的具体修复方案
4. 设计意图不明确时的任何待确认问题

## 最佳实践

- 根据 seed 进行审查，而非个人品味
- 区分风格偏离和真正的可用性或无障碍 bug
- 优先提供可操作的差异对比而非抽象批评
- 当现有组件已解决问题时指出重复

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-review/SKILL.md)

## 限制

- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
