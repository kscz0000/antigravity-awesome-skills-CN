---
name: build
description: 功能开发流水线——研究、规划、跟踪和实现主要功能。触发词：build、功能开发、特性开发、功能流水线、feature development、research、implementation、progress、phase
risk: unknown
source: community
---

---
name: build
description: 功能开发流水线——研究、规划、跟踪和实现主要功能。
argument-hint: [subcommand] [name]
metadata:
  author: Shpigford
  version: "1.0"
---

功能开发流水线——研究、规划、跟踪和实现主要功能。

## 何时使用
- 你需要一个结构化的工作流，用于跨研究、规划、实现和跟踪阶段构建主要功能。
- 任务涉及将功能推进到命名阶段，如 `research`、`implementation`、`progress` 或 `phase`。
- 你希望通过一个命令来协调功能工作的状态、下一步和分阶段交付。

## 指令

本命令管理一个4阶段功能开发工作流，用于构建主要功能。解析 `$ARGUMENTS` 以确定要运行的子命令。

**提供的参数：** $ARGUMENTS

### 参数解析

解析 $ARGUMENTS 的第一个词以确定子命令：

- `research [name]` → 运行研究阶段
- `implementation [name]` → 运行实现阶段
- `progress [name]` → 运行进度阶段
- `phase [n] [name]` → 运行实现的第 n 阶段
- `status [name]` → 显示当前状态并建议下一步
- （空或无法识别）→ 显示使用帮助

如果参数中未提供功能名称，你必须使用 AskUserQuestion 提示用户输入。

---

## 子命令：Help（空参数）

如果未提供参数，显示此帮助：

```
/build - Feature Development Pipeline

Subcommands:
  /build research [name]        Deep research on a feature idea
  /build implementation [name]  Create phased implementation plan
  /build progress [name]        Set up progress tracking
  /build phase [n] [name]       Execute implementation phase n
  /build status [name]          Show status and next steps

Example workflow:
  /build research chat-interface
  /build implementation chat-interface
  /build progress chat-interface
  /build phase 1 chat-interface
```

然后使用 AskUserQuestion 询问用户想要做什么：

- question: "What would you like to do?"
- header: "Action"
- multiSelect: false
- options:
  - label: "Start new feature research"
    description: "Begin deep research on a new feature idea"
  - label: "Continue existing feature"
    description: "Work on a feature already in progress"
  - label: "Check status"
    description: "See what step to do next for a feature"

---

## 子命令：research

### 步骤 1：获取功能名称

如果参数中没有功能名称，使用 AskUserQuestion：

- question: "What's a short identifier for this feature? (lowercase, hyphens ok - e.g., 'chat-interface', 'user-auth', 'data-export'). Use 'Other' to type it."
- header: "Feature name"
- multiSelect: false
- options:
  - label: "I'll type the name"
    description: "Enter a short, kebab-case identifier for the feature"

### 步骤 2：检查现有研究

检查 `docs/{name}/RESEARCH.md` 是否已存在。

如果存在，使用 AskUserQuestion：

- question: "A RESEARCH.md already exists for this feature. What would you like to do?"
- header: "Existing doc"
- multiSelect: false
- options:
  - label: "Overwrite"
    description: "Replace existing research with fresh exploration"
  - label: "Append"
    description: "Add new research below existing content"
  - label: "Skip"
    description: "Keep existing research, suggest next step"

如果选择"Skip"，建议运行 `/build implementation {name}` 并退出。

### 步骤 3：收集功能上下文

使用 AskUserQuestion 理解功能：

- question: "Describe the feature you want to build. What problem does it solve? What should it do? (Use 'Other' to describe)"
- header: "Description"
- multiSelect: false
- options:
  - label: "I'll describe it"
    description: "Provide a detailed description of the feature"

### 步骤 4：研究范围

使用 AskUserQuestion：

- question: "What aspects should the research focus on?"
- header: "Focus areas"
- multiSelect: true
- options:
  - label: "Technical implementation"
    description: "APIs, libraries, architecture patterns"
  - label: "UI/UX design"
    description: "Interface design, user flows, interactions"
  - label: "Data requirements"
    description: "What data to store, schemas, privacy"
  - label: "Platform capabilities"
    description: "OS APIs, system integrations, permissions"

### 步骤 5：进行深度研究

现在对功能进行深度研究：

1. **代码库探索**：理解现有模式、类似功能、相关代码
2. **网络搜索**：研究最佳实践、类似实现、相关 API
3. **技术深挖**：探索特定技术、库、框架
4. **频繁使用 AskUserQuestion**：验证假设、澄清需求、获取决策输入

研究应涵盖：
- 问题定义和用户需求
- 技术方案和权衡
- 所需数据模型和存储
- UI/UX 考量
- 与现有代码的集成点
- 潜在挑战和风险
- 推荐方案及其理由

### 步骤 6：撰写研究文档

如需要则创建目录：`docs/{name}/`

将发现写入 `docs/{name}/RESEARCH.md`，结构如下：

```markdown
# {Feature Name} Research

## Overview
[Brief description of the feature and its purpose]

## Problem Statement
[What problem this solves, why it matters]

## User Stories / Use Cases
[Concrete examples of how users will use this]

## Technical Research

### Approach Options
[Different ways to implement this, with pros/cons]

### Recommended Approach
[The approach you recommend and why]

### Required Technologies
[APIs, libraries, frameworks needed]

### Data Requirements
[What data needs to be stored/tracked]

## UI/UX Considerations
[Interface design thoughts, user flows]

## Integration Points
[How this connects to existing code/features]

## Risks and Challenges
[Potential issues and mitigation strategies]

## Open Questions
[Things that still need to be decided]

## References
[Links to relevant documentation, examples, articles]
```

### 步骤 7：下一步

撰写研究文档后，通知用户：

"研究完成！文档已保存至 `docs/{name}/RESEARCH.md`

**下一步：** 运行 `/build implementation {name}` 创建分阶段实现计划。"

---

## 子命令：implementation

### 步骤 1：获取功能名称

如果参数中没有功能名称，使用 AskUserQuestion 提示用户输入（与研究阶段相同）。

### 步骤 2：验证研究文档存在

检查 `docs/{name}/RESEARCH.md` 是否存在。

如果不存在：
- 通知用户："未在 `docs/{name}/RESEARCH.md` 找到研究文档"
- 建议："请先运行 `/build research {name}` 创建研究文档。"
- 退出

### 步骤 3：检查现有实现文档

检查 `docs/{name}/IMPLEMENTATION.md` 是否已存在。

如果存在，使用 AskUserQuestion：

- question: "An IMPLEMENTATION.md already exists. What would you like to do?"
- header: "Existing doc"
- multiSelect: false
- options:
  - label: "Overwrite"
    description: "Create a fresh implementation plan"
  - label: "Append"
    description: "Add new phases below existing content"
  - label: "Skip"
    description: "Keep existing plan, suggest next step"

如果选择"Skip"，建议运行 `/build progress {name}` 并退出。

### 步骤 4：阅读研究文档

阅读 `docs/{name}/RESEARCH.md` 以理解：
- 推荐方案
- 技术需求
- 所需数据模型
- UI/UX 设计
- 集成点

### 步骤 5：设计实现阶段

将研究分解为实际的实现阶段。每个阶段应：
- 具有独立价值（交付可用的成果）
- 足够小，可在专注的会话中完成
- 基于前一阶段构建
- 有明确的成功标准

使用 AskUserQuestion 验证阶段划分：

- question: "How granular should the implementation phases be?"
- header: "Phase size"
- multiSelect: false
- options:
  - label: "Small phases (1-2 hours)"
    description: "Many focused phases, easier to track progress"
  - label: "Medium phases (half day)"
    description: "Balanced approach, moderate number of phases"
  - label: "Large phases (full day)"
    description: "Fewer phases, each delivering significant functionality"

### 步骤 6：进行阶段研究

对于你规划的每个阶段，进行针对性研究：
- 网络搜索实现细节
- 审查代码库中的相关代码
- 识别阶段间的依赖关系

使用 AskUserQuestion 解决关于阶段顺序或范围的任何不确定性。

### 步骤 7：撰写实现文档

写入 `docs/{name}/IMPLEMENTATION.md`，结构如下：

```markdown
# {Feature Name} Implementation Plan

## Overview
[Brief recap of what we're building and the approach from research]

## Prerequisites
[What needs to be in place before starting]

## Phase Summary
[Quick overview of all phases]

---

## Phase 1: [Phase Title]

### Objective
[What this phase accomplishes]

### Rationale
[Why this phase comes first, what it enables]

### Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Success Criteria
[How to verify this phase is complete]

### Files Likely Affected
[List of files that will probably need changes]

---

## Phase 2: [Phase Title]

[Same structure as Phase 1]

---

[Continue for all phases]

---

## Post-Implementation
- [ ] Documentation updates
- [ ] Testing strategy
- [ ] Performance validation

## Notes
[Any additional context or decisions made during planning]
```

### 步骤 8：下一步

撰写实现文档后，通知用户：

"实现计划完成！文档已保存至 `docs/{name}/IMPLEMENTATION.md`

**下一步：** 运行 `/build progress {name}` 设置进度跟踪。"

---

## 子命令：progress

### 步骤 1：获取功能名称

如果参数中没有功能名称，使用 AskUserQuestion 提示用户输入。

### 步骤 2：验证实现文档存在

检查 `docs/{name}/IMPLEMENTATION.md` 是否存在。

如果不存在：
- 通知用户："未在 `docs/{name}/IMPLEMENTATION.md` 找到实现文档"
- 建议："请先运行 `/build implementation {name}`。"
- 退出

### 步骤 3：检查现有进度文档

检查 `docs/{name}/PROGRESS.md` 是否已存在。

如果存在，使用 AskUserQuestion：

- question: "A PROGRESS.md already exists. What would you like to do?"
- header: "Existing doc"
- multiSelect: false
- options:
  - label: "Overwrite"
    description: "Start fresh progress tracking"
  - label: "Keep existing"
    description: "Keep current progress, suggest next step"

如果选择"Keep existing"，阅读进度文档并建议下一个未完成的阶段。

### 步骤 4：阅读实现文档

阅读 `docs/{name}/IMPLEMENTATION.md` 以提取：
- 所有阶段标题
- 每个阶段的任务
- 成功标准

### 步骤 5：创建进度文档

写入 `docs/{name}/PROGRESS.md`，结构如下：

```markdown
# {Feature Name} Progress

## Status: Phase 1 - Not Started

## Quick Reference
- Research: `docs/{name}/RESEARCH.md`
- Implementation: `docs/{name}/IMPLEMENTATION.md`

---

## Phase Progress

### Phase 1: [Title from Implementation]
**Status:** Not Started

#### Tasks Completed
- (none yet)

#### Decisions Made
- (none yet)

#### Blockers
- (none)

---

### Phase 2: [Title]
**Status:** Not Started

[Same structure]

---

[Continue for all phases]

---

## Session Log

### [Date will be added as work happens]
- Work completed
- Decisions made
- Notes for next session

---

## Files Changed
(Will be updated as implementation progresses)

## Architectural Decisions
(Major technical decisions and rationale)

## Lessons Learned
(What worked, what didn't, what to do differently)
```

### 步骤 6：下一步

创建进度文档后：

"进度跟踪已设置！文档已保存至 `docs/{name}/PROGRESS.md`

**下一步：** 运行 `/build phase 1 {name}` 开始实现。"

---

## 子命令：phase

### 步骤 1：解析参数

解析参数以提取：
- 阶段编号（如已提供）
- 功能名称（如已提供）

如果两者均未提供，使用 AskUserQuestion 提示输入。

### 步骤 2：获取功能名称

如果未确定功能名称，使用 AskUserQuestion 提示用户输入。

### 步骤 3：验证所有文档存在

检查以下三个文档是否存在：
- `docs/{name}/RESEARCH.md`
- `docs/{name}/IMPLEMENTATION.md`
- `docs/{name}/PROGRESS.md`

如果任何文档缺失，通知用户缺少哪个文档，并建议使用相应的 `/build` 命令创建。

### 步骤 4：获取阶段编号

如果参数中没有阶段编号：

阅读 `docs/{name}/IMPLEMENTATION.md` 提取可用阶段。

使用 AskUserQuestion 让用户选择：

- question: "Which phase would you like to work on?"
- header: "Phase"
- multiSelect: false
- options: [dynamically generated from phases found in IMPLEMENTATION.md, marking completed ones]

### 步骤 5：阅读所有上下文

阅读所有三个文档以充分理解：
- 研究和理由（RESEARCH.md）
- 具体阶段任务和成功标准（IMPLEMENTATION.md）
- 当前进度和已做决策（PROGRESS.md）

### 步骤 6：阶段深度研究

在开始实现之前：

1. **网络搜索**与本阶段相关的具体实现细节
2. **代码库探索**查找相关的现有代码
3. **使用 AskUserQuestion** 澄清阶段需求的任何歧义

### 步骤 7：执行阶段工作

开始实现该阶段：

1. 完成阶段中的每个任务
2. 频繁使用 AskUserQuestion 进行实现决策
3. 遵循"始终可用"理念——边做边测试
4. 在 PROGRESS.md 中记录所做的决策

### 步骤 8：更新进度文档

在工作过程中，更新 `docs/{name}/PROGRESS.md`：

- 将任务标记为已完成
- 记录所做的决策及其原因
- 记录遇到的任何阻碍
- 列出修改的文件
- 添加架构决策
- 用今天的工作更新会话日志

更新阶段状态：
- 开始时标记为"In Progress"
- 所有任务完成且满足成功标准时标记为"Completed"

### 步骤 9：下一步

完成该阶段后：

1. 阅读 PROGRESS.md 确定下一个未完成的阶段
2. 通知用户完成情况并建议下一步操作：

"阶段 {n} 完成！进度已更新至 `docs/{name}/PROGRESS.md`

**下一步：** 运行 `/build phase {n+1} {name}` 继续 [下一阶段标题]。"

或者如果所有阶段都已完成：

"所有阶段已完成！{feature name} 功能实现已完成。

建议：
- 运行测试验证一切正常
- 更新文档
- 创建 PR 进行审查"

---

## 子命令：status

### 步骤 1：获取功能名称

如果参数中没有功能名称，使用 AskUserQuestion 提示用户输入。

### 步骤 2：检查哪些文档存在

检查以下文档是否存在：
- `docs/{name}/RESEARCH.md`
- `docs/{name}/IMPLEMENTATION.md`
- `docs/{name}/PROGRESS.md`

### 步骤 3：确定状态和下一步

根据存在的文档：

**无文档存在：**
"未找到功能 '{name}' 的文档。
**下一步：** 运行 `/build research {name}` 开始。"

**仅 RESEARCH.md 存在：**
"功能 '{name}' 研究已完成。
**下一步：** 运行 `/build implementation {name}` 创建实现计划。"

**RESEARCH.md 和 IMPLEMENTATION.md 存在：**
"功能 '{name}' 的研究和实现计划已完成。
**下一步：** 运行 `/build progress {name}` 设置进度跟踪。"

**三个文档都存在：**
阅读 PROGRESS.md 查找当前阶段状态。
"功能 '{name}' 正在进行中。
**当前状态：** [阶段 X - 状态]
**下一步：** 运行 `/build phase {下一个未完成阶段} {name}` 继续。"

如果所有阶段都已完成：
"功能 '{name}' 实现已完成！"

---

## 重要指南

### 大量使用 AskUserQuestion

在所有阶段中，在以下情况使用 AskUserQuestion：
- 需求存在歧义
- 存在多种可行方案
- 需要验证假设
- 决策将显著影响实现
- 对范围或优先级不确定

### 深度研究期望

"深度研究"意味着：
- 对不同方面进行多次网络搜索
- 彻底的代码库探索
- 阅读相关文档
- 考虑多种方案
- 理解权衡

不要急于完成研究——它是良好实现的基础。

### 进度跟踪

在阶段工作期间实时更新 PROGRESS.md：
- 不要等到最后才更新
- 在做出决策时立即记录
- 立即记录阻碍
- 这为未来的会话创造了宝贵的上下文

### 范围管理

此工作流的一个关键目的是防止范围蔓延：
- 每个阶段应有明确的边界
- 如果出现新需求，将其记录到未来的阶段中
- 不要在实现过程中扩展当前阶段的范围
- 使用 AskUserQuestion 验证某事项是否在范围内

### 始终可用理念

在实现阶段时：
- 边修改边测试
- 不要假设代码有效——要验证
- 如果某事不工作，在继续之前修复它
- 目标是可工作的软件，而不仅仅是写好的代码

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
