# Stitch UI 设计技能

Google Stitch 提示词编写专家指南。Google Stitch 是 AI 驱动的 UI 设计工具。

## 概述

本技能提供全面的指导，帮助你在 Google Stitch 中编写精准、可执行的提示词，生成高质量的 UI 设计。涵盖提示词结构、具体化技巧、迭代策略和设计转代码工作流。

## 包含内容

### SKILL.md
核心提示词原则和技巧：
- 具体化和细节要求
- 视觉风格定义
- 多屏流程组织
- 平台和响应式规范
- 功能需求
- 提示词模板
- 迭代策略
- 常见用例
- 需要避免的反模式

### 参考资料

#### prompt-examples.md
按类别组织的 Stitch 提示词示例库：
- 落地页
- 移动应用
- 仪表盘
- 电商
- 表单和认证
- 内容平台
- SaaS 应用

每个示例包含详细的组件拆解、样式规范和平台要求。

#### advanced-techniques.md
面向生产级设计的高级策略：
- 图片转 UI 工作流
- 设计系统集成
- 响应式设计策略
- 无障碍设计考量
- 性能优化
- 组件复用
- 原子设计方法论
- 导出和交付最佳实践

## 适用场景

在以下情况使用本技能：
- 在 Google Stitch 中创建 UI 设计
- 生成移动端或 Web 应用界面
- 编写有效的 Stitch 提示词
- 将草图或线框图转为数字 UI
- 构建设计系统
- 创建响应式布局
- 确保无障碍合规
- 优化设计转代码工作流

## 核心原则

1. **具体明确** - 泛泛的提示词只能得到泛泛的结果
2. **定义视觉风格** - 始终包含配色、美学和设计方向
3. **结构清晰** - 明确列出组件和区块
4. **指定平台** - 说明是手机、平板、桌面还是响应式
5. **包含功能** - 描述交互、状态和用户流程
6. **渐进式迭代** - 做聚焦的修改而非推倒重来

## 快速开始

### 基础提示词模板

```
[Screen/Component Type] for [User/Context]

Key Features:
- [Feature 1 with specific details]
- [Feature 2 with specific details]
- [Feature 3 with specific details]

Visual Style:
- [Color scheme]
- [Design aesthetic]
- [Layout approach]

Platform: [Mobile/Web/Responsive]
```

### 使用示例

```
Dashboard for SaaS analytics platform

Key Features:
- Top metrics cards showing MRR, active users, churn rate
- Line chart for revenue trends (last 30 days)
- Recent activity feed with user actions
- Quick action buttons for reports and exports

Visual Style:
- Dark mode with blue/purple gradient accents
- Modern glassmorphic cards with subtle shadows
- Clean data visualization with accessible colors

Platform: Responsive web (desktop-first)
```

## 最佳实践

### 推荐做法 ✅
- 提供具体的组件细节
- 定义清晰的视觉方向
- 指定响应式行为
- 包含交互状态
- 使用设计术语
- 必要时参考现有设计
- 用标注进行迭代
- 从一开始就考虑无障碍

### 避免做法 ❌
- 使用模糊描述（"好看的网站"）
- 省略视觉风格指导
- 忘记指定平台
- 忽略响应式需求
- 跳过无障碍考量
- 推倒重来而非渐进修改

## 与开发集成

### Stitch → Figma → 代码
1. 在 Stitch 中用详细提示词生成 UI
2. 导出到 Figma 进行设计系统集成
3. 附带设计规范交付给开发人员
4. 用生产级代码实现

### Stitch → HTML → 框架
1. 在 Stitch 中生成并精修 UI
2. 导出 HTML/CSS 代码
3. 转换为 React/Vue/Svelte 组件
4. 集成到应用代码库

## 资源

- **SKILL.md** - 核心提示词指南
- **prompt-examples.md** - 30+ 详细提示词示例
- **advanced-techniques.md** - 生产级设计策略

## 成功技巧

1. 从清晰的需求和上下文出发
2. 使用提示词模板保持一致性
3. 参考类似用例的示例
4. 用标注进行渐进式迭代
5. 生成变体以探索不同选项
6. 始终指定视觉风格和平台
7. 在每个提示词中考虑无障碍
8. 导出后先精修再用于生产

## 关于 Google Stitch

Google Stitch 是由 Gemini 2.5 Flash 驱动的实验性 AI UI 生成器，能将文本提示词和视觉参考转化为可用的 UI 设计。支持文本转 UI 生成、图片转 UI 转换、多屏流程，以及导出为 HTML/CSS、Figma 和代码。

---

**注意：** 本技能旨在帮助你为 Stitch 编写有效的提示词。输出质量取决于提示词的具体程度和清晰度。将模板和示例作为起点，然后根据你的独特需求进行定制。
