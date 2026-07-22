---
name: spec-driven-development
description: 在编码前创建规格说明。当启动新项目、新功能或重大变更且尚无规格说明时使用。当需求不清晰、存在歧义或仅有模糊想法时使用。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/spec-driven-development
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# Spec-Driven Development

## 概述

在编写任何代码之前，先编写结构化的规格说明。规格说明是你与人类工程师之间的共享事实来源——它定义了我们要构建什么、为什么构建，以及如何判断完成。没有规格说明的代码就是猜测。

## 何时使用

- 启动新项目或新功能
- 需求模糊或不完整
- 变更涉及多个文件或模块
- 即将做出架构决策
- 任务实现预计超过 30 分钟

**何时不使用：** 单行修复、错别字纠正，或需求明确且自包含的变更。

## 门控工作流

规格驱动开发有四个阶段。在当前阶段经过验证之前，不要进入下一阶段。

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

### 阶段 1：明确规格

从高层愿景开始。向人类提出澄清问题，直到需求具体化。

**立即暴露假设。** 在编写任何规格内容之前，列出你的假设：

```
ASSUMPTIONS I'M MAKING:
1. This is a web application (not native mobile)
2. Authentication uses session-based cookies (not JWT)
3. The database is PostgreSQL (based on existing Prisma schema)
4. We're targeting modern browsers only (no IE11)
→ Correct me now or I'll proceed with these.
```

不要静默填补模糊的需求。规格说明的全部目的就是在代码编写之前暴露误解——假设是最危险的误解形式。

**编写覆盖以下六个核心领域的规格文档：**

1. **目标** — 我们在构建什么，为什么？用户是谁？成功是什么样的？

2. **命令** — 完整的可执行命令含标志位，而不只是工具名。
   ```
   Build: npm run build
   Test: npm test -- --coverage
   Lint: npm run lint --fix
   Dev: npm run dev
   ```

3. **项目结构** — 源代码在哪里，测试在哪里，文档放在哪里。
   ```
   src/           → Application source code
   src/components → React components
   src/lib        → Shared utilities
   tests/         → Unit and integration tests
   e2e/           → End-to-end tests
   docs/          → Documentation
   ```

4. **代码风格** — 一个真实的代码示例胜过三段描述。包含命名约定、格式规则和优秀输出的示例。

5. **测试策略** — 使用什么框架、测试放在哪里、覆盖率期望、不同关注点使用什么测试级别。

6. **边界** — 三级体系：
   - **必须做：** 提交前运行测试、遵循命名约定、验证输入
   - **先询问：** 数据库模式变更、添加依赖、修改 CI 配置
   - **绝不：** 提交密钥、编辑 vendor 目录、未经批准删除失败测试

**规格模板：**

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements, test levels]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Open Questions
[Anything unresolved that needs human input]
```

**将指令重新定义为成功标准。** 当收到模糊需求时，将其转化为具体条件：

```
REQUIREMENT: "Make the dashboard faster"

REFRAMED SUCCESS CRITERIA:
- Dashboard LCP < 2.5s on 4G connection
- Initial data load completes in < 500ms
- No layout shift during load (CLS < 0.1)
→ Are these the right targets?
```

这让你能够围绕明确的目标进行循环、重试和问题解决，而不是猜测"更快"意味着什么。

### 阶段 2：规划

基于已验证的规格说明，生成技术实现计划：

1. 识别主要组件及其依赖关系
2. 确定实现顺序（什么必须先构建）
3. 记录风险和缓解策略
4. 识别哪些可以并行构建、哪些必须顺序构建
5. 定义阶段间的验证检查点

> 关于这些步骤背后的依赖图映射和垂直切分机制，请遵循 `planning-and-task-breakdown`；它是权威来源。上方的要点是轻量级摘要；如果两者出现分歧，以 `planning-and-task-breakdown` 为准。

计划应当是可审查的：人类应该能够读完它后说"是的，方法正确"或"不，修改 X"。

### 阶段 3：任务

将计划分解为离散的、可实现的任务：

- 每个任务应能在单次专注会话中完成
- 每个任务有明确的验收标准
- 每个任务包含验证步骤（测试、构建、手动检查）
- 任务按依赖排序，而非按感知的重要性排序
- 任何任务不应涉及超过约 5 个文件的修改

> 关于完整的任务规模确定和依赖排序机制，请遵循 `planning-and-task-breakdown`；它是权威来源。下方模板是轻量级内联形式；如果两者出现分歧，以 `planning-and-task-breakdown` 为准。

**任务模板：**
```markdown
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [How to confirm — test command, build, manual check]
  - Files: [Which files will be touched]
```

### 阶段 4：实现

按照 `skills/incremental-implementation/SKILL.md`（`incremental-implementation`）和 `skills/test-driven-development/SKILL.md`（`test-driven-development`）逐个执行任务。使用 `skills/context-engineering/SKILL.md`（`context-engineering`）在每个步骤加载正确的规格段落和源文件，而不是用整个规格淹没智能体。

## 保持规格的生命力

规格是活文档，不是一次性产物：

- **决策变更时更新** — 如果你发现数据模型需要更改，先更新规格，再实现。
- **范围变更时更新** — 新增或削减的功能应在规格中体现。
- **提交规格** — 规格属于版本控制，与代码一起管理。
- **在 PR 中引用规格** — 将每个 PR 关联回它所实现的规格段落。

## 常见自我辩解

| 自我辩解 | 现实 |
|---|---|
| "这很简单，不需要规格" | 简单任务不需要长规格，但仍需要验收标准。两行的规格也可以。 |
| "我先写代码再写规格" | 那是文档，不是规格。规格的价值在于在编码之前强制澄清。 |
| "规格会拖慢我们" | 15 分钟的规格能避免数小时的返工。15 分钟的瀑布胜过 15 小时的调试。 |
| "需求反正会变" | 正因如此规格才是活文档。过时的规格仍好于没有规格。 |
| "用户知道他们想要什么" | 即使清晰的请求也有隐含假设。规格能暴露这些假设。 |

## 红旗信号

- 在没有任何书面需求的情况下开始写代码
- 在澄清"完成"意味着什么之前就问"我该直接开始构建吗？"
- 实现规格或任务列表中未提及的功能
- 做出架构决策却没有记录
- 因为"显然该构建什么"而跳过规格

## 验证

在进入实现之前，确认：

- [ ] 规格覆盖了全部六个核心领域
- [ ] 人类已审查并批准了规格
- [ ] 成功标准是具体且可测试的
- [ ] 边界（必须做/先询问/绝不）已定义
- [ ] 规格已保存到仓库中的文件

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性或高成本操作的批准。
