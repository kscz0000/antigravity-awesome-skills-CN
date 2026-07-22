---
name: rayden-code
description: 使用 Rayden UI 组件生成 React 代码，包含正确的 props、设计令牌和高级布局模式。当用户要求"生成 React UI"、"Rayden 组件"、"vibe coding UI"、"设计系统代码"时使用。
category: development
risk: safe
source: https://github.com/playbookTV/rayden-ui-design-skill
source_type: community
date_added: 2026-04-10
author: Leslie Williams
tags: react, tailwind, design-system, ui, components, vibe-coding, rayden, rayna-ui, code-generation
tools: Read, Write, Edit, Bash, Glob, Grep
---

# Rayden Code 技能

## 概述

使用 Rayden UI 组件库（34 个组件）生成生产级 React + Tailwind CSS 代码。该技能加载完整的 API 参考，包含每个组件、每个 prop、设计令牌、布局模式和明确的反模式禁用列表——防止产生幻觉组件和通用 AI 输出。基于 Rayna UI 设计系统构建。

## 何时使用此技能

- 你正在使用 Rayden UI 组件构建新页面或功能
- 你想要快速搭建仪表盘、落地页、认证页面、设置页面或数据表格
- 你需要生成精确遵循特定设计系统的 React 代码
- 你想要快速原型 UI，确保组件使用正确且具有高级美感
- 你在进行 vibe coding，希望输出符合设计系统规范

## 工作原理

1. **解析请求** — 识别页面类型、所需组件和数据模型
2. **加载 RAYDEN_RULES.md** — 完整参考：34 个组件及其完整 props、设计理念、令牌类、布局模式、反模式和可访问性规则
3. **规划布局** — 决定页面结构、组件选择、间距、颜色和层次策略
4. **生成代码** — 使用仅文档记录的组件和令牌类编写 React + Tailwind CSS
5. **自我验证** — 运行 16 点检查清单，涵盖正确性（有效组件/props、令牌使用、嵌套）和设计质量（留白、层次、克制、响应式）

## 示例

### Vibe code 一个 SaaS 仪表盘

```
/rayden-code a dashboard with KPI cards, a recent orders table, and an activity feed
```

**使用场景：** 你正在构建内部分析工具，需要一个完整的仪表盘页面，包含 MetricsCard 网格、可排序的 Table 和 ActivityFeed 侧边栏——全部使用正确的 Rayden 导入和令牌类。

### 搭建登录页面

```
/rayden-code login page with email and password
```

**使用场景：** 你需要一个居中的认证表单，包含 Input 组件、主 Button 和正确的视觉层次——遵循 Rayden 的"Auth / Focused Form"模式。

### 构建管理设置页面

```
/rayden-code settings page with profile section, notification toggles, and danger zone
```

**使用场景：** 你正在为应用添加设置区域，需要包含 Toggle 组件的表单区域、危险操作区域和单列约束布局。

### 创建定价页面

```
/rayden-code pricing page with 3 tiers and a feature comparison table
```

**使用场景：** 你需要一个营销定价区域，每个层级使用 Card 组件，推荐方案使用 Badge，以及功能对比使用 Table。

### 构建电商产品网格

```
/rayden-code product catalog with filters, search, and a card grid
```

**使用场景：** 你正在构建商店前端，需要一个响应式产品网格，包含 Chip 筛选器、Input 搜索、Pagination 和带图片的 Cards——全部使用 Rayden 的布局和间距规则。

## 最佳实践

- 用自然语言描述你想要什么——技能会将你的请求映射到正确的组件
- 首先在项目中安装 `@raydenui/ui`（`npm install @raydenui/ui`）
- 在应用入口点导入 `@raydenui/ui/styles.css` 以使设计令牌生效
- 检查生成的代码中的业务逻辑——技能处理 UI，不处理数据获取
- 如果你同时想在 Figma 中构建相同设计，可配合 `/rayden-use` 使用

## 安全与注意事项

- 此技能仅读取其捆绑的规则文件并向你的项目写入代码
- 无外部网络请求
- 不涉及密钥或凭证
- 生成的代码使用标准 React 模式，无 eval 或动态代码执行

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 组件无法正确渲染 | 确保在应用入口导入 `@raydenui/ui/styles.css` |
| "组件不存在"错误 | 技能仅使用文档记录的组件——检查你是否在请求 Rayden 没有的东西 |
| 颜色看起来不对 | 使用令牌类（`bg-primary-500`）而非十六进制值。确保 Rayden CSS 已加载 |
| 布局不响应 | 技能默认生成响应式代码——检查你的 viewport meta 标签是否已设置 |

## 相关技能

- `rayden-use` — 通过 MCP 在 Figma 中构建 Rayden UI 组件和界面（包含在同一包中）

## 局限性
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
