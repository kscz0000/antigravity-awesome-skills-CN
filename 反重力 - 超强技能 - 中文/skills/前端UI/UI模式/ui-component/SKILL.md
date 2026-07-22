---
name: ui-component
description: "生成遵循 StyleSeed Toss 规范的 UI 组件，涵盖结构、设计令牌、无障碍和组件人体工学。"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, components, design-system, frontend, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI 组件

## 概述

本技能是 [StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，生成遵循 Toss 种子设计语言的组件，而非临时拼凑标记和样式。重点在于语义令牌、可预测的类型、可复用的变体，以及移动端友好的无障碍默认值。

## 适用场景
- 需要在基于 StyleSeed 的项目中创建新的 UI 原语或组合组件
- 希望组件与现有 Toss 种子规范保持一致
- 组件需要可复用、强类型、由设计令牌驱动
- AI 可能会自行发明间距、颜色或交互模式时

## 工作原理

### 第一步：读取本地设计上下文

生成代码前，先检查种子的真实来源：
- `CLAUDE.md` 获取规范
- `css/theme.css` 获取语义令牌
- `components/ui/` 中至少一个代表性组件

如果用户有更好的本地示例，优先遵循本地代码库而非通用模板。

### 第二步：选择正确的存放位置

将输出放在应有的位置：
- `src/components/ui/` 用于原语和底层构建块
- `src/components/patterns/` 用于组合型区块或多部分模式

如果现有原语可以安全扩展，不要创建新的。

### 第三步：遵循结构规则

除非宿主项目有强烈的不同意见，否则使用以下默认值：
- 使用 function 声明而非 `const` 组件
- 使用 `React.ComponentProps<>` 或等效的原生 prop 类型
- 支持 `className` 透传
- 使用 `cn()` 或项目的标准类合并工具
- 使用 `data-slot` 进行组件标识
- 仅在确实需要变体时使用 CVA 或等效方案

### 第四步：仅使用语义令牌

如果设计系统有对应的令牌，不要硬编码视觉值。

推荐示例：
- `bg-card`
- `text-foreground`
- `text-muted-foreground`
- `border-border`
- `shadow-[var(--shadow-card)]`

### 第五步：保持 StyleSeed 排版和间距

- 使用种子已定义的比例
- 优先使用 6px 的倍数
- 在支持的地方使用逻辑间距工具类
- 标题和展示文字紧凑，正文可读，辅助文字克制

### 第六步：内置无障碍

- 交互元素的触摸目标至少 44x44px
- 键盘焦点必须可见
- 在适当的地方透传 `aria-*` 属性
- 非必要动效尊重 reduced-motion 偏好

## 输出内容

提供：
1. 生成的组件
2. 目标路径
3. 所需的导入或依赖
4. 关于变体、令牌或后续集成工作的说明

## 最佳实践

- 优先组合现有原语，而非发明新的
- 保持组件 API 小而可预测
- 优先使用语义布局类而非任意值
- 导出命名组件，除非宿主项目一致使用其他标准

## 扩展资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-component/SKILL.md)

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
