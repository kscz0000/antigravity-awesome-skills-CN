---
name: setup-matt-pocock-skills
description: 为本仓库配置工程技能 — 设置 Issue 跟踪器、分流标签词汇表和领域文档布局。在首次使用其他工程技能之前运行一次。
disable-model-invocation: true
category: "development"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - engineering
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

# Setup Matt Pocock's Skills

## 何时使用

当工作流与用户请求匹配时使用：为本仓库配置工程技能 — 设置 Issue 跟踪器、分流标签词汇表和领域文档布局。在首次使用其他工程技能之前运行一次。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_

搭建工程技能所依赖的仓库级配置：

- **Issue 跟踪器** — Issue 存放的位置（默认为 GitHub；同时开箱支持本地 Markdown）
- **分流标签** — 五个标准分流角色所使用的字符串
- **领域文档** — `CONTEXT.md` 和 ADR 的存放位置，以及读取它们的消费规则

这是一个提示驱动的技能，而非确定性脚本。先探索，展示发现，与用户确认，然后写入。

## 流程

### 1. 探索

查看当前仓库以了解其初始状态。读取已存在的内容；不要假设：

- `git remote -v` 和 `.git/config` — 这是一个 GitHub 仓库吗？是哪个？
- 仓库根目录下的 `AGENTS.md` 和 `CLAUDE.md` — 是否已存在？其中是否已有 `## Agent skills` 部分？
- 仓库根目录下的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 以及任何 `src/*/docs/adr/` 目录
- `docs/agents/` — 此技能的先前输出是否已存在？
- `.scratch/` — 表明本地 Markdown Issue 跟踪器约定已在使用的标志

### 2. 展示发现并询问

总结已有内容和缺失内容。然后**逐一**引导用户做出三个决策 — 展示一个部分，获取用户的回答，再进入下一个。不要一次性抛出三个问题。

假设用户不了解这些术语的含义。每个部分以简短说明开始（它是什么、为什么技能需要它、不同选择会有什么影响）。然后展示选项和默认值。

**部分 A — Issue 跟踪器。**

> 说明："Issue 跟踪器"是本仓库的 Issue 存放位置。`to-issues`、`triage`、`to-prd` 和 `qa` 等技能会从中读写 — 它们需要知道是调用 `gh issue create`、在 `.scratch/` 下写 Markdown 文件，还是遵循你描述的其他工作流。选择你实际用于跟踪本仓库工作的位置。

默认倾向：这些技能为 GitHub 设计。如果 `git remote` 指向 GitHub，建议使用 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管），建议使用 GitLab。否则（或用户偏好时），提供：

- **GitHub** — Issue 存放在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab** — Issue 存放在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 Markdown** — Issue 以文件形式存放在本仓库的 `.scratch/<feature>/` 下（适合个人项目或无远程仓库的项目）
- **其他**（Jira、Linear 等） — 要求用户用一段话描述工作流；技能将以自由格式文本记录

当且仅当用户选择了 **GitHub** 或 **GitLab** 时，追问一个后续问题：

> 说明：开源仓库经常以 Pull Request 的形式收到功能请求，而不只是 Issue — PR 本质上是附带代码的 Issue。如果开启此选项，`/triage` 会将*外部* PR 纳入同一队列，使用与 Issue 相同的标签和状态进行处理（协作者进行中的 PR 不受影响）。如果你不将 PR 作为请求渠道，请保持关闭。

- **PR 作为请求渠道** — 是 / 否（默认：否）。将答案记录在 `docs/agents/issue-tracker.md` 中。对于本地 Markdown 和其他跟踪器，跳过此问题 — 没有 PR。

**部分 B — 分流标签词汇表。**

> 说明：当 `triage` 技能处理传入的 Issue 时，会将其在一个状态机中流转 — 待评估、等待报告者、可供 AFK 智能体认领、需要人工处理、或不予处理。为此，它需要应用标签（或 Issue 跟踪器中的等效物），而这些标签必须匹配你*实际已配置*的字符串。如果你的仓库已使用不同的标签名称（例如用 `bug:triage` 而非 `needs-triage`），请在此映射，技能将应用正确的标签而非创建重复标签。

五个标准角色：

- `needs-triage` — 需要维护者评估
- `needs-info` — 等待报告者补充信息
- `ready-for-agent` — 已完全描述，可供 AFK 智能体处理（智能体无需人工上下文即可认领）
- `ready-for-human` — 需要人工实现
- `wontfix` — 不会处理

默认：每个角色的字符串等于其名称。询问用户是否要覆盖任何标签。如果 Issue 跟踪器中尚无已有标签，默认值即可。

**部分 C — 领域文档。**

> 说明：某些技能（`improve-codebase-architecture`、`diagnosing-bugs`、`tdd`）会读取 `CONTEXT.md` 文件来学习项目的领域语言，以及 `docs/adr/` 中的历史架构决策。它们需要知道仓库是单一全局上下文还是多个上下文（例如包含独立前端/后端上下文的 monorepo），以便在正确位置查找。

确认布局：

- **单上下文** — 仓库根目录下一个 `CONTEXT.md` + `docs/adr/`。大多数仓库属于此类。
- **多上下文** — 根目录下的 `CONTEXT-MAP.md` 指向各上下文各自的 `CONTEXT.md` 文件（通常为 monorepo）。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要添加到 `CLAUDE.md` / `AGENTS.md`（正在编辑的那个）中的 `## Agent skills` 块（选择规则见步骤 4）
- `docs/agents/issue-tracker.md`、`docs/agents/triage-labels.md`、`docs/agents/domain.md` 的内容

让用户在写入前进行编辑。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则如果 `AGENTS.md` 存在，编辑它。
- 如果两者都不存在，询问用户要创建哪一个 — 不要替用户决定。

当 `CLAUDE.md` 已存在时，绝不创建 `AGENTS.md`（反之亦然） — 始终编辑已有的那个。

如果所选文件中已存在 `## Agent skills` 块，就地更新其内容而非追加重复块。不要覆盖用户对周围其他部分的编辑。

该块内容：

```markdown
## Agent skills

### Issue tracker

[一行概述 Issue 跟踪位置，以及外部 PR 是否为分流渠道]。参见 `docs/agents/issue-tracker.md`。

### Triage labels

[一行概述标签词汇表]。参见 `docs/agents/triage-labels.md`。

### Domain docs

[一行概述布局 — "单上下文"或"多上下文"]。参见 `docs/agents/domain.md`。
```

然后使用本技能文件夹中的种子模板作为起点，写入三个文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub Issue 跟踪器
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab Issue 跟踪器
- [issue-tracker-local.md](./issue-tracker-local.md) — 本地 Markdown Issue 跟踪器
- [triage-labels.md](./triage-labels.md) — 标签映射
- [domain.md](./domain.md) — 领域文档消费规则 + 布局

对于"其他"类型的 Issue 跟踪器，根据用户描述从头编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告知用户设置已完成，以及哪些工程技能将会读取这些文件。提及他们稍后可以直接编辑 `docs/agents/*.md` — 只有在要切换 Issue 跟踪器或从头开始时才需要重新运行此技能。


## 限制

- 当工作流指定了上游工具、账户、API 密钥或本地设置时，需要相应的先决条件。
- 未经用户明确批准，不执行破坏性、生产环境、付费或外部消息操作。
- 在将生成的产物或建议视为最终结果之前，请对照用户的真实来源进行验证。
