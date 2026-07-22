---
name: dos-verify-done-claims
description: "在采信智能体的“完成 / 已交付 / 已修复”声明之前，使用 DOS 内核的 `dos verify` 与 `dos commit-audit`，依据 ground truth（git 血缘 + 该 commit 自身的 diff）进行校验——绝不能依赖智能体的自述。 触发词：验证、done 声明、commit 审计、witness-claim、dos-kernel、质量门。"
category: quality
risk: critical
source: community
source_repo: anthony-chaudhary/dos-kernel
source_type: community
date_added: "2026-06-12"
author: anthony-chaudhary
tags: [verification, git, ai-agents, trust, quality-gate]
tools: [claude, cursor, gemini]
license: "MIT"
license_source: "https://github.com/anthony-chaudhary/dos-kernel/blob/master/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "Setup installs and executes an external PyPI CLI; keep out of plugin-safe bundles."
    docs: SKILL.md
---

# 依据事实校验“完成声明”，而非依赖智能体的自述

## 概述

当 AI 智能体说“done”、“shipped”或“fixed”时，那只是一个**声明（claim）**，而非事实——而由智能体通过重读自己工作来核验的声明，只是*一致性（consistency）*，并非*接地（grounding）*。本技能用一份智能体未曾撰写的证人裁决，取代这种自我汇报：它调用 **DOS 内核**（`dos verify`、`dos commit-audit`），从 git 血缘以及 commit 的真实 diff 来确认声称的效果。DOS 是确定性的——无需 API key，无需 LLM。在本文用法下，裁决仅依赖 git，且为离线；唯一的例外是在装配了 CI oracle 的工作区里调用 `dos verify`，可由 `--no-ci` 抑制（见“安全与注意事项”）。

本技能将 DOS 参考模式“witness-claim”（`anthony-chaudhary/dos-kernel`）改写为不绑定宿主剧本（host-agnostic screenplay）。

## 何时使用本技能

- 当智能体将某个任务/阶段/特性报告为**完成**，而你希望在基于此继续之前，通过证据确认该“完成”时使用。
- 在一次 commit 之后立即使用，以确认该 commit 的**提交信息与其 diff 相符**（比如发现一个 `fix:` 仅仅改动了 README，或“tests pass”把断言都给删了）。
- 在汇集多个子智能体的结果时使用——逐项核验每个声明的效果，而不是相信返回字符串。
- **不要**用它来判断代码是否*正确*——那是测试套件的职责。本技能只检查“声称要做的事是否真的 ship 了”。

## 工作原理

### 第 1 步：安装内核（仅一次）

```bash
python3 -m venv .dos-venv
. .dos-venv/bin/activate
python -m pip install 'dos-kernel==<reviewed-version>'  # provides the `dos` CLI
```

### 第 2 步：审计最新 commit 的声明与它的 diff 是否一致

commit subject 是可伪造的（写消息的人就是它作者）；它改动的文件则不可伪造（git 作证）。`dos commit-audit` 将 subject 与真实 diff 对照评分：

```bash
dos commit-audit --workspace . HEAD --json
```

`commit-audit --json` 输出的是一个 JSON **数组**（即便只有一个 `HEAD`，也只有一个元素），所以要从首元素中读取 `verdict`——例如 `dos commit-audit --workspace . HEAD --json | jq -r '.[0].verdict'`。（没有 `--json` 时，同一裁决会以一行情本形式输出：`· OK …`、`⚑ UNWITNESSED …`、或 `· abstain …`。）裁决的可能取值为：`OK`（diff 支撑该声明的*种类（kind）*）、`CLAIM_UNWITNESSED`（subject 中的声明没有 diff 证据——将“done”视为未证实），或 `ABSTAIN`。它判断的是变更的*种类*，绝不是正确性——正确性还要靠跑测试。

### 第 3 步：核验具名阶段是否真正交付

如果智能体声明某个具体的 plan/phase 已落地，从 git 历史而非对话记录中确认它：

```bash
dos verify --workspace . PLAN PHASE --json --no-ci
```

`--no-ci` 将裁决限定在仅依赖 git（见下文“安全”小节）。加上 `--json` 即可拿到 `shipped` 与 `source` 字段。（默认的文本形式输出 `SHIPPED PLAN PHASE (via grep)` 或 `NOT_SHIPPED PLAN PHASE (via none)`——同一裁决；未交付时进程退出码非零。）

对 `shipped: true` 应按 `source` 分级，因为 git 的回退机制按**可伪造性（forgeability）**给自身打分——而可伪造证据恰恰是本技能要警惕的对象：

- `registry` 或 `grep-artifact`——**不可伪造**（一条 registry 记录，或一个 artefact/diff 凭证）。这可关闭该声明。
- `grep-subject`（或裸 `grep`）——**可伪造**：commit 的 *subject* 或正文带了该 phase 标记，智能体不真正做事也能写出来（哪怕在空 commit 上）。将其视为“按 subject 已交付”，而非已证实——关闭前用 `dos commit-audit` 对该 commit 做佐证（见下）。
- `none`——没有正面证据；接受为“未交付”，而非工具失败。

### 第 4 步：仅汇入已确认的效果

仅当第 2/3 步予以佐证时，才接受智能体的“done”。若 `CLAIM_UNWITNESSED` 或 `shipped: false`，无论智能体叙述得多么自信，工作都没完成——打回。

## 示例

### 示例 1：把关智能体的“我修好 bug 了”声明

```bash
# 智能体已 commit 并声称已修复。检查 diff 是否支撑这一声明。
# commit-audit --json 返回一个数组，所以读取首元素的 verdict：
dos commit-audit --workspace . HEAD --json | jq -r '.[0].verdict'
# OK                -> 变更是声明的种类；这之后去跑测试
# CLAIM_UNWITNESSED -> commit 没做它说的事情；驳回
```

### 示例 2：在关闭工单前确认某功能阶段已交付

```bash
dos verify --workspace . AUTH AUTH2 --json --no-ci
# shipped: true, source: registry|grep-artifact -> 不可伪造；可安全关闭
# shipped: true, source: grep-subject|grep       -> subject/正文可伪造；
#   仅“按 subject 已交付” -> 关闭前用 commit-audit 佐证
# shipped: false, source: none -> 无证据；保持工单开启
```

## 最佳实践

- 每次智能体 commit 后，立刻跑 `dos commit-audit HEAD`。
- 将 `source: none` / `CLAIM_UNWITNESSED` 视为“未完成”，而不是工具错误。
- 仅在**不可伪造**的 `source`（`registry`、`grep-artifact`）上关闭一条声明。对 `grep-subject` / 裸 `grep` 视为可伪造（智能体可写出 subject 文本），关闭前需要佐证。
- 把测试套件单独作为正确性关口——本技能检查的是“是否交付”，不是“是否正确”。
- 不要因为智能体的措辞很自信就接受“done”。
- 不要用它替代代码评审或测试。

## 局限性

- 本技能不能替代特定环境的验证、测试或专家评审。
- 它检查的是声称的变更*是否已交付* / 与 diff 是否相符——而非代码*是否正确*。
- `dos verify` 读的是 git 历史；在没有任何 commit 的仓库里没有可作证的内容（它会如实回报 `source: none`）。
- 如果必需输入（git 仓库、`dos` CLI）缺失，停下并请求澄清。

## 安全与注意事项

- 本技能运行 shell 命令：在隔离的 virtualenv 中安装 `dos-kernel` 以及只读的 `dos` 子命令（`dos commit-audit`、`dos verify`）。这些子命令**绝不修改**仓库或推送。`dos commit-audit` 只读 git 历史和工作区（无网络）。`dos verify` 也仅依赖 git，**除非**工作区接入了 CI oracle（`dos.toml` 中的 `[verify] non_git_oracle`），此时它可能 shell 一条网络检查（如 `gh api`）来出裁决——可加 `--no-ci`（像上文示例那样）强制走仅 git 路径，保证无网络。
- `pip install dos-kernel` 从 PyPI 安装。发行版名称为 `dos-kernel`（PyPI 上单独的 `dos` 是无关包——不要安装它）。请钉住一个已审阅的版本；不要在全局 Python 环境里安装未钉版本的最新发行版。
- 在你打算裁决的那个仓库中运行；`--workspace .` 参数将所有裁决都限定在该仓库。

## 常见陷阱

- **问题**：`dos verify` 返回 `source: none`，看起来像失败。
  **解决**：那是诚实的“无证据”裁决——意味着该 phase 没有 ship commit，因此该声明不成立。重新标记真实的 commit，或保持任务开启。
- **问题**：装错了包。
  **解决**：PyPI 上的包名是 `dos-kernel`，而不是 `dos`。

## 相关技能

- 上游 DOS 参考剧本（`dos-witness-claim`、`dos-goal-gate`），位于 `anthony-chaudhary/dos-kernel`，覆盖了同一套见证纪律在多智能体扇出与自停止智能体上的变体。
