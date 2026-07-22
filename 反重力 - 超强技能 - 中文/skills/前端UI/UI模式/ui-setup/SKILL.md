---
name: ui-setup
description: "交互式 StyleSeed 设置向导，用于选择应用类型、品牌色、视觉风格、字体和首个屏幕脚手架。当用户要求'设置UI'、'初始化设计系统'、'配置品牌色'、'选择视觉风格'、'创建首个页面'、'StyleSeed设置'时使用。"
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, design-system, setup, frontend, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI 设置

## 概述

[StyleSeed](https://github.com/bitjaru/styleseed) 的一部分，此设置向导将原始项目转变为设计系统引导的工作空间。它收集配置令牌、选择视觉方向和生成初始页面所需的最小品牌和产品上下文，避免陷入通用 UI。

## 使用时机

- 使用 StyleSeed Toss 种子启动新应用时使用
- 将种子复制到现有项目并需要个性化时使用
- 希望 AI 逐个询问设计决策而不是猜测时使用
- 选择颜色、字体和应用类型后需要首个页面脚手架时使用

## 工作原理

### 步骤 1：逐个提问

不要一次性展示完整问卷。问一个问题，等待回答，存储它，然后继续。

### 步骤 2：捕获应用类型

在处理令牌或布局配方之前识别产品形态。

建议的分类：
- SaaS 仪表盘
- 电商
- 金融科技
- 社交或内容
- 效率工具或内部工具
- 其他（附带简短自由描述）

使用答案选择页面组合模式和首个屏幕的脚手架类型。

### 步骤 3：选择品牌色

提供几个安全的默认选项加上自定义十六进制选项。选择后：
- 更新浅色主题品牌令牌
- 使用更浅的无障碍变体更新深色主题品牌令牌
- 保持所有其他颜色为语义化，而不是到处硬编码品牌色

如果项目使用 StyleSeed Toss 种子，主要目标是 `css/theme.css`。

### 步骤 4：提供可选的视觉参考

询问用户是否想要借鉴已建立品牌或设计语言的感觉。好的例子包括 Stripe、Linear、Vercel、Notion、Spotify、Supabase 和 Airbnb。

使用参考来影响密度、基调和组合，而不是克隆资产或商标。

### 步骤 5：选择字体

确认字体方向：
- 保持默认堆栈
- 如果已安装或可用，切换到首选字体
- 保留展示、标题、正文和说明文字的层次规则

如果种子存在，更新字体相关文件而不是在组件中分散覆盖。

### 步骤 6：生成首个屏幕

询问：
- 应用名称
- 首页或屏幕名称
- 该页面的一句话目的

然后使用种子的页面外壳、顶栏、导航、间距比例和卡片结构来脚手架页面。

## 输出

返回：
1. 捕获的设置决策
2. 更新的文件或令牌
3. 创建的首个页面或脚手架
4. 关于组件、模式、无障碍或文案的任何后续建议

## 最佳实践

- 保持交互对话式，但确定性
- 通过令牌进行品牌色更改，而不是逐个组件编辑
- 使用灵感品牌作为参考，而不是作为复制的许可
- 优先使用语义化令牌和可复用模式，而不是页面特定的 CSS

## 其他资源

- [StyleSeed 仓库](https://github.com/bitjaru/styleseed)
- [StyleSeed Toss 种子](https://github.com/bitjaru/styleseed/tree/main/seeds/toss)
- [源技能](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-setup/SKILL.md)

## 局限性

- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
