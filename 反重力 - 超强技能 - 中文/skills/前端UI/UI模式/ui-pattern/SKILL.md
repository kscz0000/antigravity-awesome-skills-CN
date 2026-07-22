---
name: ui-pattern
description: "使用 StyleSeed Toss 原语生成可复用的 UI 模式，如卡片区块、网格、列表、表单和图表容器。当用户要求'创建卡片列表'、'生成网格布局'、'构建表单区块'、'复用 UI 模式'、'设计可复用组件'时使用。"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, patterns, design-system, reuse, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI Pattern

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此技能从种子原语构建可复用的组合模式。适用于卡片列表、网格、表单区块、排行榜和图表容器等跨页面重复出现、需要看起来精心设计而非临时拼凑的区块。

## 使用场景

- 需要可复用的布局模式而非一次性页面区块时使用
- 页面重复相同排列的卡片、行、过滤器或数据块时使用
- 想从现有 StyleSeed 原语构建而非复制标记时使用
- 需要带 props 支持动态内容的模式组件时使用

## 工作原理

### 步骤 1：识别模式类型

常见模式系列包括：
- card section（卡片区块）
- two-column grid（双列网格）
- horizontal scroller（横向滚动器）
- list section（列表区块）
- form section（表单区块）
- stat grid（统计网格）
- data table（数据表格）
- detail card（详情卡片）
- chart card（图表卡片）
- filter bar（过滤条）
- action sheet（操作面板）

### 步骤 2：读取可用的构建块

检查以下两个位置：
- `components/ui/` 用于原语
- `components/patterns/` 用于可扩展的相邻模式

目标是组合，而非复制。

### 步骤 3：应用 StyleSeed 布局规则

保持 Toss 种子默认值完整：
- 基于语义标记的卡片表面
- 使用系统比例的圆角
- 使用阴影标记而非临时阴影值
- 一致的内部间距
- 与页面边距系统对齐的区块包装器

### 步骤 4：使模式动态化

通过 props 暴露数据而非硬编码内容。如果模式有多个变体，保持 API 明确且精简。

### 步骤 5：保持模式跨页面可复用

避免页面特定假设，除非用户明确需要一次性区块。如果标记仅适用于一个路由，它可能属于页面组件而非共享模式。

## 输出

提供：
1. 生成的模式组件
2. 目标位置
3. 预期 props 和使用示例
4. 复用了哪些现有原语的说明

## 最佳实践

- 从解决最小问题的现有构建块开始
- 保持容器、区块和项目职责分离
- 一致使用标记和间距规则
- 优先扩展现有模式而非添加近乎重复的副本

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-pattern/SKILL.md)

## 限制

- 仅当任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清
