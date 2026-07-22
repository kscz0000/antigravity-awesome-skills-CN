---
name: planning-and-task-breakdown
description: 将工作分解为有序任务。当你有规格说明或明确需求、需要将工作拆分为可实现的任务时使用。当任务太大无法着手、需要估算范围、或可以并行工作时也可使用。触发词：任务分解、规划拆分、工作拆解、task breakdown、planning、计划分解
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/planning-and-task-breakdown
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 规划与任务分解

## 概述

将工作分解为小型、可验证的任务，并附带明确的验收标准。好的任务分解是一个智能体能否可靠完成工作与制造一团乱麻之间的关键区别。每个任务都应足够小，能在一次专注的会话中完成实现、测试和验证。

## 何时使用

- 你有规格说明，需要将其拆分为可实现单元
- 任务太大或太模糊，无法着手
- 工作需要在多个智能体或会话之间并行化
- 你需要向人类传达范围
- 实现顺序不明显

**何时不应使用：** 范围明确的单文件变更，或规格说明中已包含定义良好的任务时。

## 规划流程

### 步骤 1：进入规划模式

在编写任何代码之前，以只读模式运作：

- 阅读规格说明和相关代码库部分
- 识别现有模式和约定
- 映射组件之间的依赖关系
- 记录风险和未知因素

**规划期间不要编写代码。** 输出是计划文档，而非实现。

### 步骤 2：识别依赖图

映射什么依赖于什么：

```
Database schema
    │
    ├── API models/types
    │       │
    │       ├── API endpoints
    │       │       │
    │       │       └── Frontend API client
    │       │               │
    │       │               └── UI components
    │       │
    │       └── Validation logic
    │
    └── Seed data / migrations
```

实现顺序遵循依赖图自底向上：先构建基础。

### 步骤 3：垂直切片

与其先构建所有数据库、再构建所有 API、再构建所有 UI，不如一次构建一条完整的功能路径：

**反面示例（水平切片）：**
```
Task 1: Build entire database schema
Task 2: Build all API endpoints
Task 3: Build all UI components
Task 4: Connect everything
```

**正面示例（垂直切片）：**
```
Task 1: User can create an account (schema + API + UI for registration)
Task 2: User can log in (auth schema + API + UI for login)
Task 3: User can create a task (task schema + API + UI for creation)
Task 4: User can view task list (query + API + UI for list view)
```

每个垂直切片交付可工作、可测试的功能。

### 步骤 4：编写任务

每个任务遵循此结构：

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Tests pass: `npm test -- --grep "feature-name"`
- [ ] Build succeeds: `npm run build`
- [ ] Manual check: [description of what to verify]

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```

### 步骤 5：排序与检查点

按以下方式排列任务：

1. 依赖关系得到满足（先构建基础）
2. 每个任务使系统保持在可工作状态
3. 每 2-3 个任务后设置验证检查点
4. 高风险任务放在前面（快速失败）

添加明确的检查点：

```markdown
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end
- [ ] Review with human before proceeding
```

## 任务规模指南

| 规模 | 文件数 | 范围 | 示例 |
|------|-------|------|------|
| **XS** | 1 | 单个函数或配置变更 | 添加一条验证规则 |
| **S** | 1-2 | 一个组件或端点 | 添加一个新的 API 端点 |
| **M** | 3-5 | 一个功能切片 | 用户注册流程 |
| **L** | 5-8 | 多组件功能 | 带筛选和分页的搜索 |
| **XL** | 8+ | **过大 — 需进一步拆分** | — |

如果任务为 L 或更大，应拆分为更小的任务。智能体在 S 和 M 任务上表现最佳。

**何时应进一步拆分任务：**
- 需要超过一个专注会话（约 2 小时以上的智能体工作量）
- 无法用 3 条或更少的要点描述验收标准
- 涉及两个或更多独立子系统（如认证和计费）
- 你发现自己在任务标题中写了"和"（说明这是两个任务）

## 计划文档模板

```markdown
# Implementation Plan: [Feature/Project Name]

## Overview
[One paragraph summary of what we're building]

## Architecture Decisions
- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

## Task List

### Phase 1: Foundation
- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation
- [ ] Tests pass, builds clean

### Phase 2: Core Features
- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Features
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: ...
- [ ] Task 6: ...

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```

## 并行化机会

当有多个智能体或会话可用时：

- **可安全并行：** 独立的功能切片、已实现功能的测试、文档
- **必须顺序执行：** 数据库迁移、共享状态变更、依赖链
- **需要协调：** 共享 API 契约的功能（先定义契约，再并行化）

## 常见自我辩解

| 自我辩解 | 现实 |
|---|---|
| "边做边想" | 这正是产生混乱和返工的原因。10 分钟的规划能节省数小时。 |
| "任务很明显" | 仍然要写下来。明确的任务能揭示隐藏的依赖和被遗忘的边界情况。 |
| "规划是额外开销" | 规划本身就是任务。没有计划的实现只是在打字。 |
| "我都能记在脑子里" | 上下文窗口是有限的。书面计划能跨越会话边界和压缩存活。 |

## 危险信号

- 没有书面任务列表就开始实现
- 任务只写"实现功能"而无验收标准
- 计划中没有验证步骤
- 所有任务都是 XL 规模
- 任务之间没有检查点
- 未考虑依赖顺序

## 验证

在开始实现之前，确认：

- [ ] 每个任务都有验收标准
- [ ] 每个任务都有验证步骤
- [ ] 任务依赖已识别且排序正确
- [ ] 没有任务涉及超过约 5 个文件
- [ ] 主要阶段之间存在检查点
- [ ] 人类已审查并批准计划

## 另见

验收标准是针对每个任务的，回答"我们是否构建了正确的东西？"。它们叠加在项目级的完成定义（Definition of Done）之上——每个任务在算作完成之前必须跨过的固定门槛。参见 `references/definition-of-done.md`。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代针对具体环境的测试、安全审查，或用户对破坏性或高成本操作的批准。
