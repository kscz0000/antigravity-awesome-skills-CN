---
name: antigravity-skill-orchestrator
description: "理解任务需求、动态选择合适技能、使用 agent-memory-mcp 追踪成功技能组合、防止简单任务过度使用技能的元技能。触发词：技能编排、技能组合、任务评估、技能选择、元技能、skill orchestrator、skill combination、task evaluation"
category: meta
risk: safe
source: community
tags: "[orchestration, meta-skill, agent-memory, task-evaluation]"
date_added: "2026-03-13"
---

# antigravity-skill-orchestrator

## 概述

`skill-orchestrator` 是一个元技能，旨在增强 AI 智能体解决复杂问题的能力。它充当智能协调器，首先评估用户请求的复杂度。基于该评估，判断是否需要专业技能。如果需要，它会选择正确的技能组合，使用 `@agent-memory-mcp` 显式追踪这些组合以供未来参考，并指导智能体完成执行过程。关键的是，它包含严格的防护措施，防止对可以用基线能力解决的简单任务不必要地使用专业技能。

## 何时使用此技能

- 处理可能需要多个专业领域的复杂、多步骤问题时使用。
- 不确定哪些特定技能最适合给定用户请求，需要从更广泛的生态系统中发现时使用。
- 用户明确要求对重要任务"编排"、"组合技能"或"使用最佳工具"时使用。
- 想要查找特定类型问题之前成功的技能组合时使用。

## 核心概念

### 任务评估防护措施
并非每个任务都需要专业技能。对于简单问题（例如：小型 CSS 修复、简单脚本编写、重命名变量），**不要使用**专业技能。过度工程化简单任务会浪费 token 和时间。

此外，编排器严禁创建新技能。其唯一目的是组合和使用社区提供的或当前环境中存在的现有技能。

在调用任何技能之前，评估任务：
1. **任务是否简单/独立？** 使用智能体在当前环境中可用的普通文件编辑、搜索和终端能力直接解决。
2. **任务是否复杂/跨领域？** 只有这时才应该进行技能编排。

### 技能选择与组合
当任务被判定为复杂时，识别所需领域（例如：前端、数据库、部署）。在当前环境中搜索可用技能以找到最相关的技能。如果本地未找到所需技能，请查阅主技能目录。

### 主技能目录
Antigravity 生态系统在 `https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/CATALOG.md` 维护着一个高度精选的主技能目录。当本地技能不足时，获取此目录以发现 9 个主要类别中的合适技能：
- `architecture`
- `business`
- `data-ai`
- `development`
- `general`
- `infrastructure`
- `security`
- `testing`
- `workflow`

### 记忆集成 (`@agent-memory-mcp`)
为了构建机构知识，编排器依赖 `agent-memory-mcp` 技能来记录和检索成功的技能组合。

## 分步指南

### 1. 任务评估与防护检查
[当面对可能需要技能的新用户请求时触发]
1. 阅读用户的请求。
2. 问自己："我能否仅用基本的文件编辑和终端命令高效解决这个问题？"
3. 如果是：不调用专业技能直接处理。在此停止编排。
4. 如果否：继续步骤 2。

### 2. 检索过往知识
[如果任务复杂则触发]
1. 使用 `agent-memory-mcp` 提供的 `memory_search` 工具搜索类似的过往任务。
   - 示例查询：`memory_search({ query: "skill combination for react native and firebase", type: "skill_combination" })`
2. 如果存在有效的组合，使用 `memory_read` 读取详情。
3. 如果没有相关记忆，继续步骤 3。

### 3. 发现并选择技能
[如果没有过往知识覆盖此任务则触发]
1. 分析核心需求（例如："需要 React UI、Node.js 后端和 PostgreSQL 数据库"）。
2. 使用当前环境的技能列表或等效发现机制查询本地可用技能，为每个需求找到最佳匹配。
3. **如果本地技能不足**，使用当前环境中可用的网页或命令行检索工具获取主目录：`https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/CATALOG.md`。
4. 扫描目录的 9 个主要类别，识别适合引入当前上下文的技能。
5. 选择所需的最小技能集。**不要过度选择。**

### 4. 应用技能并追踪组合
[使用选定技能执行任务后触发]
1. 假设任务使用新的技能组合成功完成（例如：`@react-patterns` + `@nodejs-backend-patterns` + `@postgresql`）。
2. 使用 `agent-memory-mcp` 的 `memory_write` 记录此组合以供未来使用。
   - 确保类型为 `skill_combination`。
   - 提供描述性的键和详细说明这些技能为何协同良好的内容。

## 示例

### 示例 1：处理简单任务（防护措施实战）
**用户请求：** "将 `index.css` 中提交按钮的颜色改为蓝色。"
**操作：** 技能编排器评估任务。它判定这是一个"简单/独立"任务。它**不**调用专业技能。直接编辑 `index.css`。

### 示例 2：记录新的技能组合
```javascript
// 成功构建复杂功能后使用 agent-memory-mcp 工具
memory_write({ 
  key: "combination-ecommerce-checkout", 
  type: "skill_combination", 
  content: "For e-commerce checkouts, using @stripe-integration combined with @react-state-management and @postgresql effectively handles the full flow from UI state to payment processing to order recording.",
  tags: ["ecommerce", "checkout", "stripe", "react"]
})
```

### 示例 3：检索组合
```javascript
// 开始新的电商任务时
memory_search({ 
  query: "ecommerce checkout", 
  type: "skill_combination" 
})
// 返回键 "combination-ecommerce-checkout"，然后读取：
memory_read({ key: "combination-ecommerce-checkout" })
```

## 最佳实践

- ✅ **应该：** 在查找技能之前始终评估任务复杂度。
- ✅ **应该：** 保持编排的技能数量尽可能少。
- ✅ **应该：** 运行 `memory_write` 时使用高度描述性的键，以便后续易于搜索。
- ❌ **不应该：** 将此技能用于简单的 bug 修复或 UI 微调。
- ❌ **不应该：** 组合具有重叠和冲突指令的技能，除非有明确的冲突解决计划。
- ❌ **不应该：** 尝试构建、生成或创建新技能。仅组合可用的技能。

## 相关技能

- `@agent-memory-mcp` - 此技能运行所必需。提供技能组合的持久存储。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清。
