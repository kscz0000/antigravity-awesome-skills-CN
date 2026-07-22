---
name: ecl-harness-engineer
description: "创建或审计 ECL Agent Harness 基础设施：AGENTS.md、变更追踪、仓库指南、lint 检查、CI 闸门，以及智能体交接文档。"
category: development
risk: safe
source: community
source_repo: qinghui316/ecl-harness-engineer
source_type: community
date_added: "2026-06-13"
author: qinghui316
tags: [codex, agent-harness, ecl, workflow, ci]
tools: [codex, claude, cursor, gemini, antigravity]
license: MIT
license_source: "https://github.com/qinghui316/ecl-harness-engineer/blob/main/LICENSE"
---

# ECL Harness 工程师
设计并创建 Harness 工程基础设施，使 AI 智能体能够在代码库中可靠工作。

> **核心理念**："没有基础设施的智能，只是一个演示。"Agent Harness 是操作系统 —— LLM 只是 CPU。仓库成为唯一的真相之源 —— 如果智能体在上下文中看不到它，它就不存在。

## 何时使用本技能

- 当仓库需要 AI 智能体协作基础设施（例如 `AGENTS.md`、`docs/ECL.md`、`docs/STATUS.md`、harness 变更追踪，或机械验证闸门）时使用。
- 当审计现有 Agent Harness 是否缺少 ECL 生命周期文档、变更模板、lint 检查、环境契约或 CI 集成时使用。
- 当把重复的智能体工作流失败转化为仓库本地文档、测试、lint 规则或轻量级自动演化检查时使用。
- 不要用于普通的业务功能实现，除非请求的工作专门涉及创建或改进仓库 harness。

## 限制

- 本技能用于创建或审计 harness 基础设施；它不能替代目标项目的产品需求、实施规划、代码审查或发布批准。
- 生成的 ECL 文档、linters、脚本和 CI 示例必须先适配仓库的实际技术栈、安全模型和现有贡献者工作流，再强制执行。
- 自动演化建议仅为指导。请通过正常的审查、验证和回滚规范应用 harness 变更，而不是将其作为自主策略变更接受。

## 统一工作流

本技能遵循单一统一工作流，无论项目状态如何（空仓库、已有代码或已有 harness）。核心理念：**检测当前状态与目标状态之间的差距，然后填补它**。

默认采用**核心 ECL harness**。核心包含轻量级自动演化阈值检查：
统计已关闭的变更数量，达到阈值时生成待演化提示，
且 Codex 仅通过证据、验证、评分和回滚来应用 harness 改进。
智能体平台的高级能力（如 eval 数据集、执行追踪、持久状态、
检查点、长期记忆和指标）仅在用户明确要求
智能体评估、可观测性、可恢复执行或长期记忆时作为可选 profile 启用。

本技能改进目标仓库的智能体 harness。它**不**实现普通
业务功能，不替代编码智能体的规划模式，也不创建独立的需求产品。
规划模式适用于实时讨论；ECL 工件是仓库记录，后续智能体、
linters、CI 和归档历史可以查阅。

1. **快速检测 + 意图确认** — 了解现有内容、已通过的检查以及用户期望。
2. **分析** — 架构、harness 状态、环境和项目身份。
3. **入口审查 + 差异合成** — 区分小型工作与结构化工作，支持需求优先
   和计划优先输入，并精确计算要创建或更新的内容。
4. **创建/更新** — 文档、状态交接、linters、ECL/变更脚本、环境配置和 CI。
5. **验证 + 交接** — 运行检查，归因失败原因，更新 STATUS.md，触发自动演化检查，并总结结果。

---

## 阶段 1：快速检测 + 意图确认

**目标**：在 5 分钟内理解项目状态和用户意图。

### 1.1 项目状态检测

运行此快速扫描：

```bash
# 统计文件
file_count=$(find . -type f ! -path './.git/*' ! -path './node_modules/*' ! -path './vendor/*' 2>/dev/null | wc -l)
code_files=$(find . -type f \( -name "*.go" -o -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.rs" \) ! -path './.git/*' ! -path './node_modules/*' ! -path './vendor/*' 2>/dev/null | wc -l)

# 检查 harness 组件
has_agents_md=$(test -f AGENTS.md && echo "yes" || echo "no")
has_architecture=$(test -f docs/ARCHITECTURE.md && echo "yes" || echo "no")
has_linters=$(ls scripts/lint-* 2>/dev/null | wc -l)
has_harness_dir=$(test -d harness && echo "yes" || echo "no")
has_ecl_doc=$(test -f docs/ECL.md && echo "yes" || echo "no")
has_changes_dir=$(test -d harness/changes && echo "yes" || echo "no")
has_change_templates=$(test -d harness/templates/change && echo "yes" || echo "no")
has_change_script=$(ls scripts/harness-change.* 2>/dev/null | wc -l)
has_evolve_script=$(ls scripts/harness-evolve.* 2>/dev/null | wc -l)
has_ecl_lint=$(ls scripts/lint-ecl.* 2>/dev/null | wc -l)
has_encoding_lint=$(ls scripts/lint-encoding.* 2>/dev/null | wc -l)
has_makefile=$(test -f Makefile && echo "yes" || echo "no")
has_package_json=$(test -f package.json && echo "yes" || echo "no")

# 检测技术栈
if test -f go.mod; then TECH="Go"
elif test -f package.json; then TECH="TypeScript/Node.js"
elif test -f requirements.txt || test -f pyproject.toml; then TECH="Python"
else TECH="Unknown"
fi
```

### 1.2 项目状态分类

基于检测结果：

| 状态 | 判定标准 | 动作 |
|-------|----------|--------|
| **空仓库** | file_count < 5 且 code_files = 0 | 先引导用户完成项目选择 |
| **仅有代码** | code_files > 0 且 has_agents_md = "no" | 完整分析 + 核心 harness 创建 |
| **部分 Harness** | has_agents_md = "yes" 且 (has_linters = 0 或 has_harness_dir = "no") | 差距分析 + 填补缺口 |
| **已有 Harness** | 核心 harness 组件齐全 | 审计 + 改进建议 |

同时分类 ECL 就绪度：

| ECL 状态 | 判定标准 | 动作 |
|-----------|----------|--------|
| **ECL 缺失** | has_ecl_doc = "no" 或 has_changes_dir = "no" | 创建 ECL 文档、变更模板和脚本 |
| **ECL 部分** | ECL 文档存在但脚本/模板缺失 | 填补 ECL 自动化缺口 |
| **ECL 就绪** | docs/ECL.md、harness/changes、templates、harness-change、harness-evolve、lint-ecl、lint-encoding 均存在 | 审计索引新鲜度和工作流质量 |

### 1.3 基线验证快照

对于已有项目，在创建或更新 harness 文件之前捕获尽力而为的基线。
该基线仅用于归因：它将预先存在的项目失败与
harness 工作引入的失败区分开。它不得用于削弱默认 CI。

仅运行项目中已存在的命令：

| 生态系统 | 基线命令 |
|-----------|-------------------|
| TypeScript/Node.js | package 脚本，例如 `lint`、`typecheck`、`test`、`build`；检测到时包含嵌套 package 构建脚本 |
| Go | `go test ./...`、`go build ./...`，现有的 `make lint` 或 `make test` |
| Python | 现有的测试/lint 脚本，`python -m compileall .` |

将每个命令记录为 `pass`、`fail` 或 `missing`，并附上简短的失败原因。如果某命令
在 harness 创建前失败，稍后将其报告为**预先存在的项目债**，而不是 harness
失败。默认 CI 仍然严格，除非用户
明确要求临时分阶段发布，否则仍应包含正常的业务闸门。

### 1.4 意图确认

在规划变更之前，对请求范围进行分类：

| 范围 | 默认？ | 包含内容 |
|-------|----------|----------|
| **核心 harness** | 是 | AGENTS.md、docs/ECL.md、docs/STATUS.md、docs、ECL 变更、轻量级自动演化、linters、环境契约、CI |
| **高级 harness** | 否 | 核心 harness 加上明确请求的 eval、追踪、状态、检查点、记忆或指标基础设施 |
| **仅文档** | 否 | 仅 AGENTS.md 和项目文档；暂时跳过 linters、脚本和 CI |

当用户确认工具可用时，确认范围。在 Codex 中，使用 `request_user_input`。
在其他平台上，使用等效的用户选择工具。如果没有此类工具，请使用
检测到的上下文并记录假设。

```json
{
  "question": "What's your priority for this harness setup?",
  "header": "Scope",
  "multiSelect": false,
  "options": [
    {
      "label": "Core harness (Recommended)",
      "description": "Project-first AGENTS.md, ECL changes, STATUS handoff, auto-evolve threshold checks, linters, environment contract, and strict CI"
    },
    {
      "label": "Advanced harness",
      "description": "Core harness plus explicitly requested eval, trace, memory, checkpoint, or metrics infrastructure"
    },
    {
      "label": "Documentation only",
      "description": "AGENTS.md and project docs only; skip linters, scripts, and CI for now"
    }
  ]
}
```

**如果为空仓库**，还要询问基础信息：

```json
{
  "question": "What tech stack for this project?",
  "header": "Tech Stack",
  "multiSelect": false,
  "options": [
    {"label": "Go", "description": "CLI tools, high-performance services, system programming"},
    {"label": "TypeScript/Node.js", "description": "Web APIs, full-stack apps, rapid prototyping"},
    {"label": "Python", "description": "Data processing, ML/AI, scripting"}
  ]
}
```

如果没有用户确认工具可用，请使用检测到的值并记录假设：

```markdown
## Auto-Detected Context

| Field | Value | Confidence | Evidence |
|-------|-------|------------|----------|
| Tech Stack | {TECH} | High | Found {config file} |
| Project State | {state} | High | {criteria matched} |
| Scope | Core harness | Default | No user preference specified |

Proceeding with these assumptions. Tell me if any need adjustment.
```

### 1.5 ECL 工作入口规则

在为目标项目生成 ECL 指导时，保持流程足够小以方便使用：

| 入口类型 | 判定标准 | 必需的 ECL 处理 |
|-------------|----------|-----------------------|
| **小型变更** | 本地的低风险编辑，例如复制、注释、仅样式调整，或单文件 bug 修复，且没有接口、数据、权限、架构或发布影响 | 可选激活变更；仍需在最终响应或现有任务备注中记录验证命令 |
| **结构化变更** | 跨文件/模块行为、API、数据模型、权限、架构、验证链、不清晰的需求，或可能超过 20 分钟的工作 | 使用激活的变更文件，并要求在实施前进行入口/规范/计划审查 |

决策树：

1. 如果已存在激活的变更，继续使用它；不要创建第二个激活上下文。
2. 如果变更是复制、注释、README 文本、格式，或显然的本地单文件修复
   且没有运行时、API、数据、权限、架构或验证链影响，则视为小型变更。
3. 如果变更涉及 API、数据、权限、架构、多模块、发布/运行时
   行为或不清晰的需求，则视为结构化变更。
4. 如果影响不明确，首先进行只读调查。如果检查后仍有不确定性，
   询问一个高影响力问题或升级为结构化变更；不要假设是小型变更。

对于结构化变更，支持两种常见入口：

- **需求优先输入**：将目标用户/场景、证据、成功标准、
  验收标准、非目标、约束、假设和风险提取到 `spec.md`。
- **计划优先输入**：将用户计划视为草稿，将 WHAT/WHY 拆分到 `spec.md`，将 HOW 拆分到
  `plan.md`，然后只询问影响实施方向或验收的高影响力空白。
  如果计划完整且不与仓库证据冲突，不要重复完整
  访谈。如果它与代码、文档、命令或现有 harness 约束冲突，请记录
  冲突并返回到入口审查。

问题允许且预期，但必须有界：每轮最多询问三个高影响力问题。低风险未知项变成假设；高影响力未知项变成
`[NEEDS CLARIFICATION: ...]` 并阻塞实施，直至解决。

对于复杂的结构化变更，使用轻量级迭代循环，而不是将第一个
规范视为最终：

```text
Draft Spec -> Draft Plan -> Review Gaps -> Revise Spec/Plan -> Gate -> Tasks
```

默认最多两个循环。如果关键空白仍然存在，继续最多五个循环；之后，记录一个
阻塞器而不是从猜测中实施。`plan.md` 必须包含任何规划中发现的规范
空白，因为计划经常暴露缺失的验收、边界、权限、数据或验证
要求。

---

## 阶段 2：分析

**目标**：深入理解代码库架构、harness 状态和环境要求。

### 2.1 执行模式

仅当用户授权委托且环境支持时使用子智能体。否则，内联执行相同的职责。

如果使用子智能体，分配：

- 代码架构分析：遵循 `agents/analyzer.md`；输出 `harness/.analysis/architecture.json`。
- Harness 状态审计：遵循 `agents/auditor.md`；输出 `harness/.analysis/audit.json`。
- 环境分析：遵循 `references/environment-detection-guide.md`；输出 `harness/.analysis/environment.json`。

如果内联工作，则在阶段 3 之前产生相同的三个分析工件或等效的内存摘要。

### 2.2 项目身份提取

对于已有项目，在编写文档之前提取目标项目含义：
- 一句话项目身份：它做什么，为谁做。
- 核心工作流或领域模型：用户/系统流程、关键实体、API 资源、作业或命令。
- 主要源代码入口以及常见变更所属的位置。

使用 `README.md`、清单、入口点、路由/控制器、模式/模型和关键源
目录。Harness 文件不足以作为项目身份的证据。

### 2.3 适配器选择

检测到技术栈后，在创建 linters、脚本、CI 或
环境配置之前加载匹配的适配器。适配器指导覆盖特定语言的通用模板。

| 检测到的技术栈 | 必需的适配器 |
|----------------|------------------|
| TypeScript/Node.js | `references/adapters/typescript.md` |
| Go | `references/adapters/go.md` |
| Python | `references/adapters/python.md` |
| Rust | `references/adapters/rust.md` |
| Java | `references/adapters/java.md` |
| 未知/混合 | `references/adapters/generic.md` 加上任何检测到的语言适配器 |

对于 TypeScript/Node.js 项目，优先使用 Node/TS 原生输出：`scripts/lint-deps.mjs` 或
等效文件，`scripts/lint-quality.mjs`、npm/包管理器脚本，以及 Node/TS GitHub Actions。
除非项目实际上是 Go 或已经将 Makefile 作为主要命令界面，否则不要将 Go linter 或仅 Makefile 模式适配到 TypeScript。

### 2.4 命令界面选择

在创建 ECL 脚本之前，选择目标项目的命令界面。不要假设
PowerShell 是唯一的 Windows 选项。该选择通常是自动的；除非项目证据冲突或用户已表达硬性约束，否则不要要求用户
选择脚本格式。

优先级：

1. 现有项目入口点：包管理器脚本、Makefile 目标、README 命令，
   或 CI shell 约定。
2. 明确的用户/项目约束。如果项目拒绝 `.ps1`，不要将 PowerShell
   作为唯一的 harness 入口点。
3. 允许时的 Bash profile。对于接受 Bash 的 Windows 项目，生成 `.sh` 脚本并
   记录先决条件：Git Bash、WSL、MSYS2 或 CI Linux runner。
4. 当项目接受 Windows 原生 PowerShell 时的 PowerShell profile。保持与
   Windows PowerShell 5.1 和 PowerShell 7 兼容。
5. 当这些运行时已经是项目的一等依赖时使用 Node 或 Python profiles。

当证据稀缺时的默认：对于 TypeScript/Node 项目选择 Node/包管理器脚本；
对于允许 Bash 的 Windows 项目选择 Bash profile 并记录 Git Bash/WSL/MSYS2；否则
选择适配器的原生轻量级脚本 profile。

所有 profiles 必须实现相同的 ECL 不变量和命令集。`harness-change`、
`harness-evolve`、`lint-ecl` 和 `lint-encoding` 可以实现为 `.ps1`、`.sh`、`.mjs`、
或 `.py`，但文档、CI、Makefile/package 脚本和验证命令必须一致地使用所选
入口点。

### 2.5 等待分析完成

当子智能体运行时，等待它们的最终报告。等待期间，你可以：
- 审查任何现有文档
- 为阶段 4 准备模板

### 2.5 针对空项目

跳过阶段 2 的分析智能体。而是：
- 使用 `references/greenfield-templates.md` 中的模板
- 根据用户的技术栈选择做出决策
- 设计标准的 3 层架构

---

## 阶段 3：差异合成

**目标**：合并分析结果并精确计算需要创建/更新的内容。

### 3.1 读取分析结果

```bash
cat harness/.analysis/architecture.json
cat harness/.analysis/audit.json
cat harness/.analysis/environment.json
```

### 3.2 计算差异

创建差异列表：

```markdown
## Delta: What Needs to Be Done

### Core To Create (doesn't exist)
- [ ] AGENTS.md
- [ ] docs/ECL.md
- [ ] docs/STATUS.md
- [ ] docs/ARCHITECTURE.md
- [ ] scripts/lint-deps.go
- [ ] scripts/harness-change.{ps1|sh|mjs|py}
- [ ] scripts/harness-evolve.{ps1|sh|mjs|py}
- [ ] scripts/lint-ecl.{ps1|sh|mjs|py}
- [ ] scripts/lint-encoding.{ps1|sh|mjs|py}
- [ ] harness/changes/{active,parking,archive}
- [ ] harness/templates/change/
- [ ] harness/config/environment.json
- [ ] harness/evolution/{state.json,results.tsv,proposals/} (`pending.md` is generated later only when the archive threshold is reached)

### Optional Advanced (only if explicitly requested)
- [ ] harness/eval/ — agent evaluation datasets and runner inputs
- [ ] harness/trace/ — execution traces for agent runs
- [ ] harness/state/ — executor runtime state
- [ ] harness/checkpoints/ — resumable execution checkpoints
- [ ] harness/memory/ — long-term agent memory experiments
- [ ] harness/metrics/ — execution and quality metrics

### To Update (exists but has gaps)
- [ ] docs/DEVELOPMENT.md — missing build commands
- [ ] scripts/lint-quality.py — missing 3 packages in layer map

### Already Good (no changes needed)
- [x] Makefile — has all required targets
- [x] .github/workflows/ci.yml — properly configured
```

### 3.3 与用户确认（如确认工具可用）

对于重大变更：

```json
{
  "question": "I've analyzed the codebase. Ready to proceed with these changes?",
  "header": "Confirm",
  "multiSelect": false,
  "options": [
    {"label": "Yes, proceed with all", "description": "Create/update all identified items"},
    {"label": "Show me the details first", "description": "I'll explain what each change involves"},
    {"label": "Only critical items", "description": "Just P0/P1 items, skip P2/P3 for now"}
  ]
}
```

---

## 阶段 4：创建/更新

**目标**：从差异中创建或更新所有 harness 文件。

### 4.1 执行模式

仅当授权并可用时使用子智能体。否则，内联执行相同的工作。如果使用并行 worker，保持写入作用域不相交。

创建职责：

- 文档：遵循 `agents/creator-docs.md`；创建/更新 AGENTS.md、docs/ECL.md、docs/STATUS.md、docs/ARCHITECTURE.md、docs/DEVELOPMENT.md 和设计文档。AGENTS.md 是目标项目的入口映射，而不是 harness 创建记录。保持首屏以项目为主，但在上下文加载中保留 ECL/当前变更优先级：`AGENTS.md` -> `docs/ECL.md` -> 激活变更（如果存在）-> 自动演化待办（如果存在）-> 否则 `docs/STATUS.md` -> 任务特定的项目文档。
- Linters：遵循 `agents/creator-linters.md`；创建/更新依赖、质量、ECL 和编码检查。
- 配置和脚本：遵循 `agents/creator-config.md`；创建/更新环境契约、harness 脚本、变更目录/模板、轻量级演化状态、harness-change、harness-evolve、Makefile 目标和 CI。仅当确认的范围需要时才创建高级目录。

ECL 变更模板必须包含 `summary.md`、`spec.md`、`plan.md`、`tasks.md` 和
`reviews/review.md`。`spec.md` 捕获 WHAT/WHY，`plan.md` 捕获 HOW 和规划中发现的规范空白，且 `tasks.md` 仅在规范/计划闸门足够好以实施后才生成。不要要求旧的归档变更包含 `plan.md`；兼容性适用于历史。

重要：不要创建静态验证配置，例如 `harness/config/verify.json`。验证计划由执行器在运行时从 `environment.json` 和任务上下文生成。

严格的 CI 规则：默认 CI 必须包含正常的业务质量闸门（`lint`、`typecheck`、`test`、
`build`，以及后端/包特定的等价物，当可用时）加上 harness 检查。不要移除
或跳过业务闸门，因为基线已经是红色。如果基线已经为红色，请说明 CI 将保持红色，直到预先存在的项目问题被修复。仅当用户明确要求时，才生成分阶段或宽松的 CI。

命令界面规则：为选定的 profile 创建 ECL 脚本，而不是硬编码 shell。如果在 Windows 上选择 Bash，请在生成的环境/开发文档中记录 Git Bash、WSL、MSYS2 或 CI Linux shell 要求。如果选择 PowerShell，请检测 `pwsh` 是否可用；如果不可用，
使用 `powershell -NoProfile -ExecutionPolicy Bypass`。PowerShell 模板必须与
Windows PowerShell 5.1 兼容：避免像 `TrimStart(".\")` 这样的歧义重载，并避免非 ASCII 乱码标记字符串字面量在 `.ps1` 中；用 Unicode 码点或其他 PS5 安全的构造表示标记。

### 4.2 对于空项目：还创建业务代码计划

对于空项目，添加一个更多智能体：

```
Agent("create-exec-plan", prompt="""
Create execution plan for business code (harness-executor will implement this):

Tech stack: {TECH}
Project type: {from user choice}
Architecture: 3-layer (Types → Core → Entry Points)

Create: docs/exec-plans/active/bootstrap-code.md

Contents:
- Full source code for initial project structure
- main.go/index.ts/main.py entry point
- Basic types and core logic
- Test files

This is for harness-executor to implement — not ecl-harness-engineer's responsibility.
""")
```

### 4.3 等待创建完成

智能体将在完成时通知。收集它们遇到的任何问题。

---

## 阶段 5：验证 + 交接

**目标**：确保一切正常工作，然后交接或呈现结果。

### 5.1 运行验证

```bash
# 0. 与基线快照进行比较
# 重新运行在阶段 1 中捕获的相同现有 lint/typecheck/test/build 命令。

# 1. Harness 检查通过
make verify-harness || npm run lint:harness || {generated_harness_lint_command}

# 2. 架构 linters 通过
make lint-arch || npm run lint:arch

# 3. 业务构建/测试闸门运行
go build ./... || npm run build || python -m compileall .

# 4. AGENTS.md 大小检查
wc -l AGENTS.md  # Should be 80-120 lines

# 4b. AGENTS.md 内容闸门
# 确认它解释了项目身份、核心工作流/领域模型、源代码入口、
# 基于任务的验证、激活变更优先于 STATUS 的加载，并且不包含
# ECL Harness Engineer 内部边界语言。

# 5. 所有预期文件存在
test -f AGENTS.md && echo "✓ AGENTS.md"
test -f docs/ARCHITECTURE.md && echo "✓ ARCHITECTURE.md"
test -f docs/ECL.md && echo "✓ ECL.md"
test -f docs/STATUS.md && echo "✓ STATUS.md"
test -f scripts/lint-deps* && echo "✓ lint-deps"
test -f scripts/harness-change.* && echo "✓ harness-change"
test -f scripts/lint-ecl.* && echo "✓ lint-ecl"
test -f scripts/harness-evolve.* && echo "✓ harness-evolve"
test -d harness/ && echo "✓ harness/"
test -d harness/changes && echo "✓ harness/changes"
test -f harness/evolution/state.json && echo "✓ evolution state"

# 6. 设计文档存在（不仅仅是索引）
find docs/design-docs -name "*.md" ! -name "index.md" | wc -l
```

对每个验证结果进行分类：

| 分类 | 含义 |
|----------------|---------|
| Harness 通过 | Harness 创建的检查/文件/脚本有效 |
| 预先存在的项目失败 | 同一命令在阶段 1 基线中失败 |
| 新回归 | 命令在阶段 1 通过，在 harness 创建后失败 |
| 不可用 | 命令/脚本在此项目中不存在 |

AGENTS.md 内容闸门：
- 新智能体可以在 30 秒内了解项目做什么。
- 核心产品/系统工作流或领域模型可见。
- 主要源代码入口和任务到目录的映射可见。
- 验证指南映射到任务类型。
- 上下文加载首先读取 `docs/ECL.md`，然后在存在时读取激活变更。
- 如果没有激活变更且 `harness/evolution/pending.md` 存在，则在
  `docs/STATUS.md` 之前读取它，将其提为待维护，除非
  用户已优先处理当前任务，否则询问是否立即处理。读取或询问不会启动自动演化，且必须
  不阻塞普通用户工作。
- 如果没有激活变更且没有待演化，则上下文加载在任务特定的项目文档之前读取 `docs/STATUS.md`。
- 对于结构化工作，`docs/ECL.md` 解释小型变更与结构化变更、有界入口
  审查、计划优先输入处理以及规范/计划审查闸门。
- 归档历史通过 `docs/STATUS.md` 路径或 `harness/changes/INDEX.json` 选择性加载，从历史 `summary.md` 开始。
- 没有技能内部边界泄漏，例如描述本技能自身范围限制作为目标项目规则的章节或句子。

### 5.2 STATUS.md 交接更新

当目标项目使用 ECL 变更时，将 `docs/STATUS.md` 维护为轻量级交接文件。
它在存在激活变更时不是权威的，但在激活变更关闭后它成为默认的近期历史
入口点。

关闭变更交接协议：

1. 在运行 `harness-change close` 之前，读取激活变更 `summary.md`、`spec.md`、
   `plan.md`、`tasks.md` 和相关的 `reviews/`；更新 `docs/STATUS.md`，包括已完成的工作、
   验证结果、剩余风险和下一个推荐的恢复点。
2. 运行 close 命令，使激活变更移动到 `harness/changes/archive/...` 且
   `harness/changes/INDEX.json` 被重建。
3. 关闭后，使用最终的归档路径再次更新 `docs/STATUS.md`，通常指向
   归档的 `summary.md`。
4. 运行 harness lint 命令（`npm run lint:harness`、`make verify-harness`，或生成的
   ECL lint 命令）以确认 STATUS、ECL 结构和 INDEX 状态一致。

钩子和 CI 可以验证 `docs/STATUS.md`，但不得自动写入它或移动变更。

### 5.3 自动演化检查

核心 harness 默认包含轻量级自动演化。脚本层仅检测
是否有足够的新归档证据，并写入 `harness/evolution/pending.md`；Codex 执行
语义改进过程。

触发模型：`harness-change close` 和 `reindex` 运行 `harness-evolve check`；`new` 仅在待办存在时提醒。
钩子和 CI 可以警告，但不得修改文档、脚本、STATUS 或变更。
生成的脚本不调用子智能体。它们仅统计归档证据并创建待办
上下文。当没有激活变更且 Codex 注意到待维护时，除非
用户已优先处理当前任务，否则应询问用户是否立即处理。询问不会启动
待演化。

`harness/evolution/pending.md` 是维护提醒，不是硬锁。读取它用于上下文
不会启动待演化。当 Codex 创建或使用
`auto-evolve-harness-*` 变更、写入演化提案/结果或根据待办
证据编辑 Harness 文件时，待演化开始。一旦开始，使用提案、一个 `harness/evolution/results.tsv`
行和 `harness-evolve mark-complete` 完成；否则停车或关闭阻塞，而不是已完成。

仅应用通过审查的最小证据支持差异。没有独立评分者 =
没有自动应用：用户批准处理待办意味着当环境支持时，有权请求独立
审计/子智能体。如果环境仍需要明确授权，请询问一次。如果评分不可用、被拒绝或询问后仍未获得授权，
记录 `noop` 和 `eval_mode=dry_run`，保留提案，运行 `mark-complete`，然后停止。
机制修复
（`harness-evolve`、待办模板、lint）本身不通过完成待演化；修复后，
仍评估候选归档或留下工作停车/阻塞。

详细的提案格式、评分权重、状态值和复杂度预算位于
`references/ecl-harness.md`。

### 5.4 呈现摘要

```markdown
## Harness Infrastructure Complete

**Project**: {project-name}
**Tech Stack**: {TECH}
**Files Created/Updated**: {count}

### Created Files
- AGENTS.md ({N} lines)
- docs/ARCHITECTURE.md
- docs/ECL.md
- docs/STATUS.md
- docs/DEVELOPMENT.md
- docs/design-docs/{component}.md
- scripts/lint-deps.{ext}
- scripts/lint-quality.{ext}
- scripts/harness-change.{ps1|sh|mjs|py}
- scripts/lint-ecl.{ps1|sh|mjs|py}
- scripts/lint-encoding.{ps1|sh|mjs|py}
- scripts/harness-evolve.{ps1|sh|mjs|py}
- harness/config/environment.json
- harness/changes/
- harness/evolution/
- harness/templates/change/
- Makefile

### Verification Results
- Harness checks: ✓
- Architecture checks: ✓
- Business gates: ✓ or pre-existing failures listed below
- AGENTS.md size: ✓ ({N} lines)

### Pre-existing Project Failures
- {List baseline-red commands and short reasons, or "None observed."}

### New Regressions Introduced By Harness
- {List commands that passed before and failed after, or "None observed."}

### Next Steps
{For empty projects: "Run harness-executor to implement business code from docs/exec-plans/active/bootstrap-code.md"}
{For existing projects: "The harness is ready. AI agents can now use AGENTS.md as their entry point."}
```

### 5.5 自动交接（对于空项目）

如果这是一个带有 bootstrap exec-plan 的空项目，则调用 harness-executor：

```
Skill(skill="harness-executor")
```

上下文："实现位于 docs/exec-plans/active/bootstrap-code.md 的 bootstrap exec-plan"

---

## 核心原则

### 1. 仓库作为唯一真相之源

智能体无法访问 Slack、Google Docs 或部落知识。如果它不在仓库中，它对智能体就不存在。

### 2. AGENTS.md 是地图，不是手册

保持 80-120 行。链接到详细文档，不要嵌入它们。

### 3. 机械地强制不变量

Linter 错误必须是智能体可操作的：
```
✗ BAD: "Forbidden import in core/types/user.go"

✓ GOOD: "core/types/user.go:15 imports core/config (layer 0 → layer 2).
         Layer 0 packages must have NO internal dependencies.

         Fix options:
         1. Move config-dependent logic to a higher layer
         2. Pass the config value as a parameter
         3. Use dependency injection via an interface"
```

### 4. 构建以删除

每个组件都应该是可替换的。昨天需要复杂流水线的功能明天可能只是一个提示。

### 5. 从简单开始

原子化、有据可查的工具 > 复杂的智能体编排。不要过度工程化。

### 6. 变更状态是显式的

为个人开发使用单个 `harness/changes/active/` 任务。使用生成的 `scripts/harness-change.*` 命令将暂停的工作移动到 `parking/`，将关闭的工作移动到 `archive/`。在激活工作关闭后，将 `docs/STATUS.md` 维护为软交接摘要。永远不要手动编辑 `harness/changes/INDEX.json`；它是由 `park`、`close`、`resume` 和 `reindex` 重新生成的索引。结构化变更使用 `spec.md`（WHAT/WHY）、`plan.md`（HOW）和 `tasks.md`（可执行工作）。

### 7. Harness 从证据中演化

每隔几次关闭的变更，生成的 `scripts/harness-evolve.* check` 命令可能会创建
`harness/evolution/pending.md`。将其视为从真实归档证据改进 harness 规则的维护提醒，而不是不相关用户工作的硬阻塞器。如果开始根据待办
证据行动，首先刷新 `harness/changes/INDEX.json` 并使用当前合格的归档
窗口；旧待办文件中的候选归档是触发快照，不是唯一的证据。
然后以提案 + results.tsv + `mark-complete` 完成，或停车/阻塞该工作。
不要将一次性业务 bug 转化为永久流程。仅保留改进审计
分数并通过验证的变更。

---

## 参考文件

| 文件 | 何时读取 | 内容 |
|------|-------------|----------|
| `references/greenfield-templates.md` | 空项目（阶段 2.5） | 完整的 Go/TS/Python 脚手架 |
| `references/documentation-templates.md` | 阶段 4 文档创建 | 带编号章节的文档模板 |
| `references/linter-templates.md` | 阶段 4 linter 创建 | 每种语言的 linter 代码模板 |
| `references/ecl-harness.md` | ECL 感知的 harness 创建 | docs/ECL.md、docs/STATUS.md、变更生命周期、INDEX.json、PowerShell 脚本模板 |
| `references/darwin-eval-prompts.md` | 技能质量评估 | 用于 darwin-skill 审查的 dry-run 提示 |
| `references/environment-detection-guide.md` | 阶段 2 环境分析 | 环境生态系统检测 |
| `references/environment-config-guide.md` | 阶段 4 配置创建 | 启动、服务、环境变量、用户确认模板 |
| `references/adapters/typescript.md` | TypeScript/Node.js 项目 | npm 脚本、Node linters、包管理器检测、CI 默认 |
| `references/adapters/{go,python,rust,java,generic}.md` | 匹配检测到的技术栈 | 特定语言的命令和约定 |

阶段 2 和阶段 4 子智能体的智能体提示位于 `agents/`。

对于小型项目（< 20 个文件）或当子智能体不可用时，请内联执行阶段，而不是生成智能体。