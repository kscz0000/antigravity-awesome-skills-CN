---
name: hig-project-context
description: 创建或更新共享的 Apple 设计上下文文档，供其他 HIG 技能定制指导。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 项目上下文

创建并维护 `.claude/apple-design-context.md`，以便其他 HIG 技能可以跳过重复问题。

提问前请检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未覆盖的信息。

## 收集上下文

提问前，从以下位置自动发现上下文：

1. **README.md** — 产品描述、平台目标
2. **Package.swift / .xcodeproj** — 支持的平台、最低操作系统版本、依赖项
3. **Info.plist** — 应用类别、所需功能、支持的方向
4. **现有代码** — 导入语句揭示框架（SwiftUI vs UIKit、HealthKit 等）
5. **Assets.xcassets** — 颜色资产、图标集、深色模式变体
6. **无障碍审计** — 搜索无障碍修饰符/属性

展示发现并请用户确认或更正。然后收集仍然缺失的信息：

### 1. 产品概述
- 应用做什么？（一句话）
- 类别（生产力、社交、健康、游戏、工具等）
- 阶段（概念、开发、已发布、重新设计）

### 2. 目标平台
- 哪些 Apple 平台？（iOS、iPadOS、macOS、tvOS、watchOS、visionOS）
- 最低操作系统版本
- 通用还是平台特定？

### 3. 技术栈
- UI 框架：SwiftUI、UIKit、AppKit 还是混合？
- 架构：单窗口、多窗口、基于文档？
- 使用的 Apple 技术？（HealthKit、CloudKit、ARKit 等）

### 4. 设计系统
- 系统默认还是自定义设计系统？
- 品牌颜色、字体、图标风格？
- 深色模式和动态字体支持状态

### 5. 无障碍要求
- 目标级别（基准、增强、全面）
- 特定考虑因素（VoiceOver、切换控制等）
- 法规要求（WCAG、Section 508）

### 6. 用户上下文
- 主要用户画像（1-3 个）
- 关键用例和环境（桌前、移动中、一瞥即得、沉浸式）
- 已知痛点或设计挑战

### 7. 现有设计资产
- Figma/Sketch 文件？
- 使用 Apple Design Resources？
- 现有组件库？

## 上下文文档模板

使用以下结构生成 `.claude/apple-design-context.md`：

```markdown
# Apple 设计上下文

## 产品
- **名称**：[应用名称]
- **描述**：[一句话]
- **类别**：[类别]
- **阶段**：[概念 / 开发 / 已发布 / 重新设计]

## 平台
| 平台 | 支持 | 最低版本 | 备注 |
|----------|-----------|--------|-------|
| iOS      | 是/否    |        |       |
| iPadOS   | 是/否    |        |       |
| macOS    | 是/否    |        |       |
| tvOS     | 是/否    |        |       |
| watchOS  | 是/否    |        |       |
| visionOS | 是/否    |        |       |

## 技术
- **UI 框架**：[SwiftUI / UIKit / AppKit / 混合]
- **架构**：[单窗口 / 多窗口 / 基于文档]
- **Apple 技术**：[列出任何：HealthKit、CloudKit、ARKit 等]

## 设计系统
- **基础**：[系统默认 / 自定义设计系统]
- **品牌颜色**：[列出或引用]
- **排版**：[系统字体 / 自定义字体]
- **深色模式**：[已支持 / 尚未 / 不适用]
- **动态字体**：[已支持 / 尚未 / 不适用]

## 无障碍
- **目标级别**：[基准 / 增强 / 全面]
- **关键考虑因素**：[列出任何特定需求]

## 用户
- **主要画像**：[描述]
- **关键用例**：[列出]
- **已知挑战**：[列出]
```

## 更新上下文

更新现有上下文文档时：

1. 读取当前 `.claude/apple-design-context.md`
2. 询问有什么变化
3. 仅更新已更改的部分
4. 保留所有未更改的信息

## 相关技能

- **hig-platforms** — 平台特定指导
- **hig-foundations** — 颜色、排版、布局决策
- **hig-patterns** — UX 模式建议
- **hig-components-*** — 组件建议
- **hig-inputs** — 输入方法覆盖
- **hig-technologies** — Apple 技术相关性

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
