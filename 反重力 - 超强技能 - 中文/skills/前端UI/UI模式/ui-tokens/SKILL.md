---
name: ui-tokens
description: "列出、添加和更新 StyleSeed 设计令牌，同时保持 JSON 源文件、CSS 变量和暗色模式值同步。触发词：设计令牌、UI令牌、design tokens、CSS变量同步、暗色模式令牌、StyleSeed、令牌管理"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, tokens, design-system, theming, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI Tokens

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此技能管理设计令牌，确保真实源文件不会漂移分离。适用于同时使用 Toss seed 的 JSON 令牌文件和 CSS 实现的团队。

## 何时使用
- 需要检查当前令牌集时使用
- 想要添加新的颜色、阴影、圆角、间距或排版令牌时使用
- 需要更新令牌并安全传播变更时使用
- 项目同时有 JSON 令牌文件和 CSS 变量且必须保持一致时使用

## 工作原理

### 支持的操作

- `list`：以人类可读形式显示当前令牌
- `add`：引入新令牌并将其接入实现
- `update`：更改现有令牌值并审计下游使用情况

### 典型真实源分离

对于 Toss seed：
- JSON 位于 `tokens/` 目录
- CSS 变量和主题配置位于 `css/theme.css`
- 排版支持在字体和基础 CSS 文件中

### 规则

- 保持 JSON 和 CSS 同步
- 优先使用语义化名称而非描述性名称
- 在相关处提供暗色模式支持
- 更新令牌实现，而不仅仅是源清单
- 检查可能已过时的直接组件使用

## 输出

返回：
1. 请求的令牌清单或变更摘要
2. 每个被修改的文件
3. 任何需要审查的受影响组件或工具
4. 如果新令牌需要更广泛采用时的后续操作

## 最佳实践

- 添加语义意图，而非一次性的品牌色
- 优先扩展现有尺度，避免令牌膨胀
- 保持命名与系统其余部分一致
- 引入新颜色时审查对比度和无障碍性

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-tokens/SKILL.md)

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
