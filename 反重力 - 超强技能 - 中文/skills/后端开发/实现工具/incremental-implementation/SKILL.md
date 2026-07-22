---
name: incremental-implementation
description: 增量交付变更。当实现涉及多个文件的功能或变更时使用。当准备一次性编写大量代码，或任务太大无法一步完成时使用。触发词：增量实现、增量交付、分步实现、渐进式开发、逐步实现、incremental implementation
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/incremental-implementation
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 增量实现

## 概述

以薄垂直切片构建 — 实现一个片段，测试它，验证它，然后扩展。避免一次性实现整个功能。每个增量应使系统保持在可工作、可测试的状态。这就是让大型功能变得可管理的执行纪律。

## 何时使用

- 实现任何涉及多文件的变更
- 从任务分解构建新功能
- 重构现有代码
- 当你忍不住想在测试前写超过约 100 行代码时

**何时不使用：** 范围已经极小的单文件、单函数变更。

## 增量循环

```
┌──────────────────────────────────────┐
│                                      │
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

对于每个切片：

1. **实现** 最小的完整功能片段
2. **测试** — 运行测试套件（如果没有测试则先编写测试）
3. **验证** — 确认切片按预期工作（测试通过、构建成功、手动检查）
4. **提交** — 用描述性消息保存进度（参见 `git-workflow-and-versioning` 了解原子提交指南）
5. **进入下一个切片** — 继续推进，不要从头开始

## 切片策略

### 垂直切片（首选）

构建一条贯穿整个技术栈的完整路径：

```
Slice 1: Create a task (DB + API + basic UI)
    → Tests pass, user can create a task via the UI

Slice 2: List tasks (query + API + UI)
    → Tests pass, user can see their tasks

Slice 3: Edit a task (update + API + UI)
    → Tests pass, user can modify tasks

Slice 4: Delete a task (delete + API + UI + confirmation)
    → Tests pass, full CRUD complete
```

每个切片交付可工作的端到端功能。

### 契约优先切片

当后端和前端需要并行开发时：

```
Slice 0: Define the API contract (types, interfaces, OpenAPI spec)
Slice 1a: Implement backend against the contract + API tests
Slice 1b: Implement frontend against mock data matching the contract
Slice 2: Integrate and test end-to-end
```

### 风险优先切片

优先处理风险最高或最不确定的部分：

```
Slice 1: Prove the WebSocket connection works (highest risk)
Slice 2: Build real-time task updates on the proven connection
Slice 3: Add offline support and reconnection
```

如果切片 1 失败，你在投入切片 2 和 3 之前就能发现问题。

## 实现规则

### 规则 0：简洁优先

在编写任何代码之前，先问："能工作的最简单方案是什么？"

编写代码后，对照以下检查项审视：
- 这能用更少的行数完成吗？
- 这些抽象是否配得上它们引入的复杂度？
- 资深工程师看了会不会说"为什么不直接……"？
- 我是在为假想的未来需求构建，还是在为当前任务构建？

```
SIMPLICITY CHECK:
✗ Generic EventBus with middleware pipeline for one notification
✓ Simple function call

✗ Abstract factory pattern for two similar components
✓ Two straightforward components with shared utilities

✗ Config-driven form builder for three forms
✓ Three form components
```

三行相似的代码胜过一个过早的抽象。先实现朴素的、显然正确的版本。仅在通过测试证明正确性之后才优化。

### 规则 0.5：范围纪律

只触碰任务要求的部分。

不要：
- "清理"你的变更附近的代码
- 重构你没有修改的文件中的导入
- 删除你并不完全理解的注释
- 添加规格说明中没有的功能，即使"看起来有用"
- 在你只是阅读的文件中现代化语法

如果你注意到任务范围之外值得改进的内容，记下来 — 不要去修：

```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has an unused import (unrelated to this task)
- The auth middleware could use better error messages (separate task)
→ Want me to create tasks for these?
```

### 规则 1：一次只做一件事

每个增量变更一个逻辑事务。不要混合关注点：

**错误：** 一个提交同时添加新组件、重构现有组件并更新构建配置。

**正确：** 三个独立的提交 — 每个变更一个。

### 规则 2：保持可编译

每个增量之后，项目必须能构建，现有测试必须通过。不要让代码库在切片之间处于损坏状态。

### 规则 3：为未完成的功能使用特性开关

如果功能尚未准备好面向用户，但你需要合并增量：

```typescript
// Feature flag for work-in-progress
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';

if (ENABLE_TASK_SHARING) {
  // New sharing UI
}
```

这让你可以将小增量合并到主分支，而不暴露未完成的工作。

### 规则 4：安全默认值

新代码应默认采用安全、保守的行为：

```typescript
// Safe: disabled by default, opt-in
export function createTask(data: TaskInput, options?: { notify?: boolean }) {
  const shouldNotify = options?.notify ?? false;
  // ...
}
```

### 规则 5：可回滚友好

每个增量应可独立回退：

- 增量式变更（新文件、新函数）易于回退
- 对现有代码的修改应最小且聚焦
- 数据库迁移应有对应的回滚迁移
- 避免在一个提交中删除某物并在同一提交中替换它 — 分开处理

## 与智能体协作

当指导智能体增量实现时：

```
"Let's implement Task 3 from the plan.

Start with just the database schema change and the API endpoint.
Don't touch the UI yet — we'll do that in the next increment.

After implementing, run `npm test` and `npm run build` to verify
nothing is broken."
```

明确说明每个增量的范围内和范围外内容。

## 增量检查清单

每个增量完成后，验证：

- [ ] 变更只做一件事且完整完成
- [ ] 所有现有测试仍然通过（`npm test`）
- [ ] 构建成功（`npm run build`）
- [ ] 类型检查通过（`npx tsc --noEmit`）
- [ ] 代码规范检查通过（`npm run lint`）
- [ ] 新功能按预期工作
- [ ] 变更已用描述性消息提交

**注意：** 在可能受影响的变更之后运行每个验证命令。成功运行后，除非代码此后有变更，否则不要重复同一命令 — 对未变更的代码重复运行不增加任何信息。

## 常见自我辩解

| 自我辩解 | 现实 |
|---|---|
| "我最后一起测试" | 缺陷会累积。切片 1 的缺陷会让切片 2-5 全错。逐切片测试。 |
| "一次性做完更快" | 在出问题之前*感觉*更快，但当你无法在 500 行变更中找到问题根源时就不同了。 |
| "这些变更太小不值得分开提交" | 小提交没有成本。大提交隐藏缺陷并让回滚痛苦。 |
| "我稍后再加特性开关" | 如果功能未完成，就不应对用户可见。现在就加开关。 |
| "这次重构很小，可以一起加" | 重构和功能混在一起会让两者都更难审查和调试。分开处理。 |
| "我再跑一次构建命令确认一下" | 成功运行后，除非代码此后有变更，重复同一命令毫无意义。在后续编辑后再运行，而不是为了求安心。 |

## 危险信号

- 写了超过 100 行代码却没有运行测试
- 单个增量中包含多个不相关的变更
- "让我顺便也加上这个" — 范围蔓延
- 跳过测试/验证步骤以求更快
- 增量之间构建或测试处于损坏状态
- 大量未提交的变更不断积累
- 在第三个用例需要之前就构建抽象
- "既然我都来了"去触碰任务范围外的文件
- 为一次性操作创建新的工具文件
- 在没有任何中间代码变更的情况下连续两次运行同一构建/测试命令

## 验证

完成一个任务的所有增量后：

- [ ] 每个增量都经过单独测试和提交
- [ ] 完整测试套件通过
- [ ] 构建干净
- [ ] 功能按规格端到端工作
- [ ] 没有未提交的变更残留

## 另见

逐增量验证是局部检查。在声明任务完成之前，应用项目级的完成定义作为最终关卡 — 这是每个增量必须通过的恒定标准，无论任务是什么。参见 `references/definition-of-done.md`。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查，或用户对破坏性或高成本操作的批准。
