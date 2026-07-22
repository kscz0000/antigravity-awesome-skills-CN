---
name: brooks-harness
description: brooks-lint 插件自身的维护编排器。运行顺序子代理流水线——author → eval → QA → trigger-audit → release——以新增或编辑技能、刷新评测套件，保持四个清单 + README + CHANGELOG + AGENTS/GEMINI 同步，审计触发词……
risk: unknown
source: https://github.com/hyhmrright/brooks-lint/tree/main/.claude/skills/brooks-harness
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# brooks-lint — 维护 Harness（编排器）
## 何时使用

当你需要对 brooks-lint 插件自身进行维护编排时使用本技能。它运行一条顺序子代理流水线——author → eval → QA → trigger-audit → release——以新增或编辑技能、刷新评测套件，保持四个清单 + README + CHANGELOG + AGENTS/GEMINI 同步，审计触发词……


本技能**针对 brooks-lint 仓库自身**编排工作。它运行一条顺序
子代理流水线：每个阶段都是 `.claude/agents/` 中定义的专用代理。使用
`Agent` 工具生成各代理，`subagent_type` 设置为代理名称，并且**始终
使用 `model: "opus"`**。各阶段按顺序依赖，因此这是一条流水线，而非
并行团队。

## 流水线

```
[orchestrator]
   Phase 0  context check
   Phase 1  classify request → select stages
   Phase 2  run selected stages in order, with a QA loop-back:
            skill-author → eval-curator → consistency-qa ─(FAIL)→ back to author
                                              │ PASS
                                              ▼
                            trigger-boundary-auditor   (only if a description changed)
                                              ▼
                                      release-manager  (only if release requested)
   Phase 3  report + collect feedback
```

## Phase 0 — 上下文检查

在动手之前先确定运行模式：

- 若 `_workspace/brooks-harness/` 存在 + 维护者要求重做先前某次运行的部分 →
  **部分重跑**：仅调用受影响的阶段，复用先前的笔记。
- 若 `_workspace/brooks-harness/` 存在 + 收到新的请求 → **新运行**：将旧文件夹移至
  `_workspace/brooks-harness_prev/`，重新开始。
- 若不存在 `_workspace/brooks-harness/` → **首次运行**：创建之。

运行笔记和 QA 报告保存在 `_workspace/brooks-harness/` 下。*真正的*
产物是仓库自身的文件——代理直接编辑 `skills/`、`evals/`、清单；
`_workspace/` 仅保存本次运行的笔记以及用于审计的 PASS/FAIL 判定。

## Phase 1 — 分类请求

选取最小的阶段集合。QA 阶段**绝不跳过**——所有改动都
必须经过此关。

| 请求 | author | eval | QA | trigger-audit | release |
|---------|:------:|:----:|:--:|:-------------:|:-------:|
| 新增技能 | ✓（通过 `new-skill` 脚手架） | ✓ | ✓ | ✓ | — |
| 编辑技能/指南内容 | ✓ | 若代码改动 | ✓ | 若 `description` 改动 | — |
| 编辑 `_shared/` 框架 | ✓ | 若风险定义改动 | ✓ | — | — |
| 仅评测套件 | — | ✓ | ✓ | — | — |
| 修复触发词描述 | ✓ | — | ✓ | ✓ | — |
| 发布 | — | — | ✓ | — | ✓ |
| 完整：变更 + 发布 | ✓ | 按需 | ✓ | 若适用 | ✓ |

## Phase 2 — 运行流水线

按顺序将每个被选中的阶段生成为子代理。向每个代理传入 (a) 任务契约与
(b) 前一阶段的摘要。代理将摘要写入 `_workspace/brooks-harness/`；在阶段间
读取它们。

1. **skill-author**——创建/编辑内容。对于全新的技能，它调用 `new-skill` 脚手架。返回被改动文件列表 +
   与约定相关的选择（新增风险代码、新增 Step 编号、变更的 `description` 触发短语）。
2. **eval-curator**——若 `skill-author` 报告了新增/变动的风险代码或模式，则添加配对的成功路径 + 误报场景，
   并运行 `npm run evals`。
3. **consistency-qa** *(关卡——绝不跳过)*——运行 `npm run validate` + `npm test` + `npm run evals`，随后进行
   跨文档同步检查（清单、README 徽章、CHANGELOG、AGENTS/GEMINI 书籍数、评测数）。写出 PASS/FAIL 判定。
   **若 FAIL：回环到判定中指明的代理（author 或 eval-curator），修复后再次运行 QA。重复一次；若仍然失败，
   停下来并向维护者报告。**
4. **trigger-boundary-auditor**——**仅当 `description` 字段发生变化时**运行。它只读审计六个已发布技能的触发面，
   查找误触发与路由冲突。呈现其发现；若它标记出真实冲突，则回环到 skill-author。
5. **release-manager**——**仅当请求发布且 QA 通过后**运行。通过 `release` 技能完成发布。

## Phase 3 — 报告与反馈

报告：运行的阶段、改动的文件、QA 判定、trigger-audit 发现（如有）以及发布
URL（如有）。然后向维护者敞开反馈通道："在结果、智能体角色或流水线顺序方面
是否有需要调整的地方？" 将已接受的变更记录到 CLAUDE.md 中 harness 变更
日志表中。

## 本 harness 强制执行的约定

- **所有 `Agent` 调用均使用 `model: "opus"`**——harness 质量取决于代理推理能力。
- **consistency-qa 必须为 `general-purpose`**（它运行 npm 脚本）；trigger-boundary-auditor 为
  只读。
- **不创建斜杠命令**——简短形式由 session-start 钩子自动安装。
- **直接推送 main**：改动直接推送到 `main`，无需 PR（依据仓库 CLAUDE.md）；全局
  simplify→review→commit 关卡仍适用于非文档编辑，但技能/指南内容属于 markdown，遵循
  validate 关卡。

## 错误处理

- 失败的阶段以错误为输入重试一次；第二次失败
  则停止流水线并向维护者报告（不静默跳过）。
- QA FAIL 一律不能进入发布。
- 冲突的数据附带来源报告，不删除。
- 高风险 git 操作（`--no-verify`、`--force`、历史改写）需维护者显式授权——
  release-manager 停下并询问。

## 测试场景

**正常流程——"新增 brooks-security 技能"：**Phase 1 选取 author+eval+QA+audit。
skill-author 运行 `new-skill brooks-security`，创建 SKILL.md（含兄弟领域切分的
"Do NOT trigger for:" 子句）+ 指南；eval-curator 添加 S 代码成功路径 + 误报场景；
consistency-qa 运行关卡 → PASS；trigger-boundary-auditor 确认与 brooks-review/audit 无冲突。
报告列出文件 + PASS。

**错误流程——QA FAIL 于书籍计数漂移：**维护者新增第十三本书，但仅编辑 `source-coverage.md`。
consistency-qa 的跨文档检查发现 README 仍写"twelve" → FAIL，归因于 skill-author。编排器
回环；skill-author 更新 README/AGENTS/GEMINI 措辞；QA 重跑 → PASS。未请求发布，流水线止于
Phase 3。

## 局限

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用更改之前，请验证命令、生成的代码、依赖、凭据以及外部服务的行为。
- 切勿将示例视为针对特定环境的测试、安全审查或用户对破坏性/高成本操作的审批的替代。
