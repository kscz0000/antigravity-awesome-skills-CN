---
name: rayden-use
description: 通过 Figma MCP 在 Figma 中构建和维护 Rayden UI 组件和界面，强制执行完整的设计令牌规范。当用户需要"构建 Figma 组件"、"设计 UI 界面"、"Rayden 组件"、"设计系统合规检查"、"Figma 设计"时使用。
category: design
risk: safe
source: https://github.com/playbookTV/rayden-ui-design-skill
source_type: community
date_added: 2026-04-10
author: Leslie Williams
tags: figma, design-system, ui, components, mcp, rayden, rayna-ui
tools: mcp__claude_ai_Figma__use_figma, mcp__claude_ai_Figma__get_screenshot, mcp__claude_ai_Figma__whoami, Read
---

# Rayden UI 设计技能

## 概述

通过 Figma MCP 直接在 Figma 中构建和维护 Rayden UI 组件和界面。该技能强制执行 Rayna UI 设计系统——包括解析后的设计令牌、工艺规则、反模式检测和视觉验证——确保每个输出在机械层面正确且视觉上高品质。支持三种风格模式（保守、平衡、表现力），并包含一个专用子代理用于整页界面组合。

## 何时使用此技能

- 你需要在 Figma 中构建新的 Rayden UI 组件及其所有变体
- 你正在从 Rayden 模式组合完整界面（仪表盘、落地页、认证表单、设置页、数据表格）
- 你想要审核现有 Figma 文件的设计系统合规性
- 你需要为现有 Figma 组件添加新变体
- 你正在将 React 组件更新同步回 Figma

## 工作原理

1. **验证环境** — 通过 `whoami` 检查 Figma MCP 连接和写入权限
2. **加载组件数据** — 从 `@raydenui/ai` MCP 服务器或已安装的包中读取 Rayden 组件规格、结构和令牌
3. **加载工艺规则** — 读取支持文件：解析后的令牌值、工艺规则、反模式和界面布局模式
4. **识别任务类型** — 确定是构建单个组件、组合界面、审核还是添加变体
5. **应用风格模式** — 根据保守/平衡/表现力模式调整间距、阴影、排版和视觉权重
6. **使用辅助函数构建** — 使用必需的辅助函数（hexToRgb、loadFonts、applyShadow、applyBorder）生成 Figma Plugin API 代码，每个框架都启用自动布局
7. **视觉验证** — 在每个构建阶段后截图，并根据 8 项验收标准进行验证（对齐、间距、颜色准确性、层级、圆角、阴影、主要操作数量）

## 示例

### 构建包含所有变体的组件

```
/rayden-use Button https://figma.com/file/abc123
```

**使用场景：** 你正在启动一个新的设计系统文件，需要 Button 组件及其所有变体（primary、secondary、grey、destructive），包括实心和描边外观，涵盖 SM 和 LG 尺寸。

### 设计 SaaS 仪表盘

```
/rayden-use dashboard-screen balanced https://figma.com/file/abc123
```

**使用场景：** 你正在设计一个分析仪表盘，需要侧边栏布局配合 KPI 卡片、数据表格和活动动态——全部使用一致的 Rayden 令牌和间距。

### 构建营销落地页

```
/rayden-compose landing expressive https://figma.com/file/abc123
```

**使用场景：** 你需要一个高影响力的落地页，采用更粗的排版、更强的阴影和非对称布局，避免千篇一律的"AI 生成"外观。

### 审核现有设计的合规性

```
/rayden-use audit https://figma.com/file/abc123
```

**使用场景：** 你有一个现有的 Figma 文件，想要检查所有颜色是否匹配 Rayden 令牌、间距是否符合 4px 网格、圆角是否同心。

### 为现有组件添加变体

```
/rayden-use add-variants Input https://figma.com/file/abc123
```

**使用场景：** Input 组件已存在于你的 Figma 文件中，但缺少错误和成功状态——该技能会读取现有结构并扩展它。

## 最佳实践

- 始终在最后提供 Figma 文件 URL 作为参数
- 大多数情况下使用 `balanced` 模式（默认）；`conservative` 用于密集的管理后台 UI，`expressive` 用于营销页面
- 让技能在构建阶段之间截图——这是它验证输出质量的方式
- 将 `@raydenui/ai` 安装为 MCP 服务器以获得最丰富的组件数据访问
- 完成后在 Figma 中审查生成的输出——技能在机械层面进行验证，但人类的审美判断仍然有价值

## 安全与注意事项

- 该技能仅读取本地支持文件并调用 Figma MCP——除 Figma API 外无外部网络请求
- 需要具有目标文件写入权限的 Figma Dev 或 Full 席位
- 不会修改目标 Figma 文档之外的文件
- 所有设计令牌都打包在技能的支持文件中——不涉及密钥或凭据

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| "Font not found" 错误 | 如果 Inter 不可用，技能会回退到 Roboto——为确保最佳效果，请在 Figma 文件中加载 Inter |
| 组件无法合并为变体 | 在调用 `combineAsVariants` 之前，所有组件必须共享同一个父框架 |
| 颜色看起来不对 | 验证你使用的是 tokens.md 中解析后的令牌十六进制值，而不是近似值 |
| Figma 权限被拒绝 | 检查你的 Figma 席位是否为 Dev 或 Full（而非 Viewer），且文件不是只读 |

## 相关技能

- `rayden-code` — 使用 Rayden UI 组件生成 React 代码（包含在同一包中）
- `rayden-compose` — 用于组合整页 Figma 界面的专用子代理（包含在此技能包中）

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
