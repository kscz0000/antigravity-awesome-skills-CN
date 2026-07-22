# Darwin 评估提示

使用这些 dry-run 提示来通过 darwin-skill 评估 ecl-harness-engineer 质量。
它们仅是评估提示；除非用户明确要求，否则不要生成文件。

## 提示 1：现有 TypeScript 项目

```text
Use ecl-harness-engineer to create an ECL-aware Harness for an existing TypeScript project.
The project already has package.json, src/, and tests/, but no AGENTS.md or harness/.
Explain the files you would create and the validation commands.
```

预期：检测 TypeScript，建议将 AGENTS.md 作为映射，docs/ECL.md、docs/STATUS.md、架构/开发文档、changes active/parking/archive、生成的 INDEX.json 工作流、lint-ecl、lint-encoding 和 package 脚本或 Makefile 验证，而不编写业务代码。

## 提示 2：审计部分 Harness

```text
Use ecl-harness-engineer to audit a project that already has AGENTS.md and docs/ARCHITECTURE.md,
but no harness/changes and no lint-ecl. Return the gaps and priorities first.
```

预期：视为部分 Harness/ECL 缺失或部分，识别缺失的 ECL 文档/脚本/模板，尽可能保留现有文档，并避免在没有差异审查的情况下覆盖。

## 提示 3：个人变更跟踪

```text
Use ecl-harness-engineer to add personal-development change tracking to a small project:
single active task, parking/archive, and automatic INDEX.json generation.
```

预期：推荐 summary/spec/plan/tasks/reviews 变更模板、单一激活规则、docs/STATUS.md 交接、脚本生成的 INDEX.json、显式的 park/close/resume 转换，以及没有自动文档变更的钩子/CI 验证。

## 提示 4：恢复最近的工作

```text
Use ecl-harness-engineer to explain how an agent should resume recent work in a project with
docs/STATUS.md, no active change, and several archived changes in harness/changes/archive.
Which files should be loaded first, and should the full archive be read?
```

预期：首先加载 AGENTS.md 和 docs/ECL.md，然后在没有激活变更的情况下加载 docs/STATUS.md。使用 STATUS 归档路径或 INDEX.json 选择历史，仅从归档的 summary.md 开始，不要默认加载完整归档。

## 提示 5：激活变更覆盖 STATUS

```text
Use ecl-harness-engineer to define context loading for a project that has both docs/STATUS.md and
harness/changes/active/summary.md. Which source controls the current task?
```

预期：激活变更控制当前任务。在任务特定文档之前读取激活的 summary/spec/plan/tasks/reviews。STATUS 在存在激活时不是权威的。

## 提示 6：核心 Harness 不得创建高级空目录

```text
Use ecl-harness-engineer to create a harness for a normal existing TypeScript project. The user wants
agent onboarding, ECL change tracking, lint checks, and CI only. List the directories you would
create under harness/.
```

预期：选择核心 harness profile。创建 `harness/config`、`harness/changes` 和 `harness/templates/change`。不要创建 `harness/eval`、`harness/trace`、`harness/state`、`harness/checkpoints`、`harness/memory` 或 `harness/metrics`。

## 提示 7：显式高级 Eval Profile

```text
Use ecl-harness-engineer to add an agent evaluation framework to a project that already has the core
ECL harness. The user wants reusable eval prompts and benchmark datasets for testing agent
behavior over time.
```

预期：将其视为高级 harness 请求。加载 eval 指导，建议 `harness/eval` 和数据集或提示 fixtures，定义如何运行和评分 eval，并避免触及不相关的核心 ECL 文件，除非需要链接 eval 工作流。

## 提示 8：显式可观测性和记忆 Profile

```text
Use ecl-harness-engineer to add trace logging and long-term agent memory to a project. The user wants
to debug long-running agent sessions and inspect recurring failures.
```

预期：将其视为高级 harness 请求。加载可观测性和持久性指导，为 `harness/trace` 和 `harness/memory` 定义读/写协议，包括验证或保留规则，并且不要将这些目录呈现为正常的首日 harness 默认值。

## 提示 9：普通业务功能不得触发 Harness 创建

```text
Add a login button to this React app and wire it to the existing auth route.
```

预期：不要使用 ecl-harness-engineer。这是普通的应用程序功能实现，而不是 harness 创建或审计工作。

## 提示 10：自动演化阈值检查是核心

```text
Use ecl-harness-engineer to create a normal ECL harness. The project has no eval or memory request.
Should auto-evolve be included, and which files or scripts are part of it?
```

预期：包括轻量级 `harness/evolution/state.json`、`results.tsv`、`proposals/` 和 `scripts/harness-evolve.*` 作为核心阈值检查基础设施。不要创建 `harness/eval`、`harness/trace`、`harness/state`、`harness/checkpoints`、`harness/memory` 或 `harness/metrics`。

## 提示 11：关闭触发待演化

```text
A project has 10 archived ECL changes and harness/evolution/state.json says the last evolution
processed 5 archives with threshold 5. What should the generated harness-change close command do after
moving the active change to archive?
```

预期：重建 `INDEX.json`，运行 `harness-evolve check`，如果没有 pending 文件，则生成 `harness/evolution/pending.md`。脚本不得直接编辑 AGENTS.md、docs/ECL.md、STATUS、lint 规则或 CI。

## 提示 12：Pending 不覆盖激活工作

```text
The repository has both harness/changes/active/summary.md and harness/evolution/pending.md.
Which context should Codex handle first?
```

预期：激活变更保持权威。在关闭或停车激活变更之前，首先读取激活的 summary/spec/plan/tasks/reviews 并推迟自动演化。

## 提示 13：Harness 演化的 Darwin 棘轮

```text
Auto-evolve proposes a harness delta based on recent archives, but the new audit score is lower
and lint-ecl fails. What should happen?
```

预期：回滚自动演化差异，在 `harness/evolution/results.tsv` 中记录 `revert`，保留提案以供审计，并运行 `harness-evolve mark-complete`，以便同一待办周期不会无限重复。

## 提示 14：没有独立评分者意味着仅提案

```text
Auto-evolve found a possible harness improvement, but this run has no available independent
auditor/subagent. Can Codex apply the delta automatically?
```

预期：不可以。用户批准处理 pending 意味着在可用时有权请求独立审计/子智能体。如果环境仍需要明确授权，请询问一次。如果评分仍不可用，生成并保留提案，记录 `status=noop` 和 `eval_mode=dry_run`，运行 `harness-evolve mark-complete`，并且不得自动应用差异。自动应用需要独立评分。

## 提示 15：独立评分低于阈值

```text
The main auto-evolve flow rates a proposal at 84, but the independent auditor scores it 79 because
the evidence is weak. What should happen?
```

预期：在应用之前拒绝提案，在 `results.tsv` 中记录 `rejected`，并保持 harness 文件不变。

## 提示 16：与项目无关的候选

```text
Auto-evolve proposes adding a broad prompt-engineering rule from an article, but no archived change
shows this project had that failure. The proposal otherwise looks reasonable.
```

预期：拒绝该候选，因为与项目无关。它可以保留在提案内的拒绝候选中，但不得进入 AGENTS.md、ECL、STATUS、lint 或 CI。

## 提示 17：接受的候选需要证据和目标文件

```text
An auto-evolve proposal accepts a candidate but lists no archive summary and no target project files
or commands. Is it valid?
```

预期：不可以。接受的候选需要归档证据和项目相关性。独立审查必须返回 `rejected` 或 `noop`。

## 提示 18：小型变更跳过完整 ECL

```text
Use ecl-harness-engineer guidance for a project where the user asks: "Fix one typo in README.md."
Should the harness require a full active change with spec/plan/tasks?
```

预期：视为小型变更。不需要完整的激活变更。智能体应进行本地修复，保留不相关的文件，并报告使用的验证。

## 提示 19：模糊需求需要有界入口

```text
Use ecl-harness-engineer guidance for a user request: "Add a permissions module."
What should the agent do before generating implementation tasks?
```

预期：视为结构化变更。提取草稿 `spec.md` 并询问最多三个关于用户/场景、验收标准、权限/数据边界或兼容性的高影响力问题。不要从第一个模糊需求生成实施任务。

## 提示 20：用户已提供计划

```text
The user provides a detailed implementation plan for adding role-based access control, including
files to change and test commands. How should ecl-harness-engineer guidance handle this?
```

预期：将用户计划视为草稿输入，而不是最终真相。将 WHAT/WHY 拆分到 `spec.md`，将 HOW 拆分到 `plan.md`。如果目标用户、验收标准、非目标和验证清晰，不要从头开始重新访谈。如果任何高影响力空白仍然存在，只询问这些问题。

## 提示 21：计划缺少验收标准

```text
The user gives a plan with implementation steps for a search feature but no success metrics,
non-goals, or validation scenario. Can the agent proceed to implementation?
```

预期：不可以。在 `spec.md` 中将缺失的验收和边界信息记录为 `[NEEDS CLARIFICATION: ...]`，询问有界的高影响力问题，并阻止实施，直到满足规范/计划闸门。

## 提示 22：规划暴露规范空白

```text
During draft planning, the agent realizes a proposed API change may require data migration and
backward compatibility decisions that were not in the spec. Where should this be recorded?
```

预期：在 `plan.md` 中的 `Spec Gaps Found From Planning` 下记录它，在 `spec.md` 中添加或更新相关的开放问题，并保持 `plan_review` 待定，直到解决。

## 提示 23：平台范围的边界检查

```text
Use ecl-harness-engineer to improve AI coding workflow. Should it create a Jira/Confluence sync,
a chat UI for requirements intake, or default eval/trace/memory directories?
```

预期：不可以。将技能范围限定在 harness 创建/审计、ECL 模板、脚本、lint 闸门和文档。高级平台目录或外部同步仅在明确请求时出现。

## 提示 24：边界小型变更需要只读检查

```text
The user asks to change one default configuration value in a single file, but the setting affects
application startup behavior. Should ecl-harness-engineer guidance treat this as Small Change?
```

预期：不是自动的。首先检查只读以确定运行时影响。如果启动、验证或兼容性行为发生变化，将其视为结构化变更或在实施之前询问一个高影响力问题。

## 提示 25：完整计划不需要重新访谈

```text
The user provides a plan with clear goal, acceptance criteria, non-goals, constraints, target files,
risks, and verification commands, and it matches repository evidence. Should the agent ask a new
round of intake questions?
```

预期：不可以。将 WHAT/WHY 拆分到 `spec.md`，将 HOW 拆分到 `plan.md`，生成可执行的 `tasks.md`，并在不重复完整访谈的情况下通过计划审查继续。

## 提示 26：计划与仓库证据冲突

```text
The user provides a plan that references a package manager and test command that do not exist in the
repository. What should the agent do?
```

预期：在入口审查中记录冲突，不要盲目接受计划，并在实施之前询问或纠正高影响力的不匹配。

## 提示 27：没有子智能体的自动演化

```text
An auto-evolve pending file exists, but the current environment cannot use an independent
auditor/subagent. Can the agent apply the proposed harness delta automatically?
```

预期：不可以。生成的脚本不调用子智能体。如果支持独立审查但未授权，智能体先询问用户授权。如果评分不可用、被拒绝或询问后仍未授权，则写入提案，记录 `status=noop` 和 `eval_mode=dry_run`，运行 `harness-evolve mark-complete`，并且不得在没有独立评分的情况下自动应用。

## 提示 28：现有激活变更胜出

```text
A user asks for a small README wording fix while `harness/changes/active/summary.md` exists for an
ongoing related documentation task. Should the agent create a new active change or skip ECL?
```

预期：两者都不是。继续使用现有的激活变更上下文，因为只能有一个激活变更。不要创建第二个激活变更。

## 提示 29：Pending 读取不是阻塞器

```text
No active change exists and harness/evolution/pending.md exists. The user asks for a small README
wording fix and does not ask to handle auto-evolve. Must the agent complete auto-evolve first?
```

预期：不可以。作为维护上下文读取或提及 pending，除非用户已优先处理 README 修复，否则询问是否立即处理。读取或询问不会启动待演化，并且不得阻塞普通用户工作。

## 提示 30：部分自动演化不能关闭已完成

```text
An agent starts auto-evolve, fixes a bug in scripts/harness-evolve.ps1, writes a keep result for
that machinery repair, but does not evaluate the pending candidate archives or run
harness-evolve mark-complete. Can it close the auto-evolve change as completed?
```

预期：不可以。机制修复不完成待演化。智能体必须继续评估候选归档并以提案 + results.tsv + mark-complete 完成，或 park/close blocked。

## 提示 31：自动演化归档不是证据

```text
The archive contains four normal changes and one auto-evolve-harness-* change tagged auto-evolve.
Threshold is 5. Should harness-evolve check generate a new pending file?
```

预期：不可以。阈值仅统计合格的归档。自动演化归档仍可用于审计，但从阈值计数和候选归档中排除。

## 提示 32：用户批准意味着独立审查请求

```text
No active change exists and pending auto-evolve exists. Codex asks whether to handle it now, and the
user says yes. The user does not separately say "use a subagent." Should Codex request an
independent auditor/subagent if the environment supports it?
```

预期：是。用户批准处理 pending 意味着在可用时有权请求独立审查。如果环境仍需要明确授权，请询问一次。没有评分者，记录 `noop + dry_run + mark-complete` 并且不自动应用。

## 提示 33：新证据胜过陈旧 Pending 快照

```text
pending.md was generated at five archived changes. Before the user approves handling it, three more
ordinary changes are archived. Which archives should Codex evaluate?
```

预期：重建 `harness/changes/INDEX.json` 并使用当前合格的归档窗口。pending.md 中列出的候选归档是触发快照，而不是唯一的证据来源。

## 提示 34：用户拒绝 Pending 维护

```text
Codex notices pending maintenance and asks whether to handle it now. The user says no, finish the
current feature first. What should happen?
```

预期：通过正常的小型/结构化入口继续当前任务。不要 mark-complete 或写入 results.tsv，因为待演化尚未开始。提及 pending 仍然存在。