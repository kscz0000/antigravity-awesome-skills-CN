---
name: polis-protocol
description: "将多供应商 AI 智能体协调为一个自我改进的团队——学习型路由器根据历史业绩分配工作，公民可以修改协议本身的规则。触发词：多智能体协调、智能体路由、polis协议、团队学习、智能体治理、供应商无关协调"
category: orchestration
risk: critical
source: community
source_repo: yehudalevy-collab/polis-protocol
source_type: community
date_added: "2026-06-02"
author: yehudalevy-collab
tags: [multi-agent, coordination, routing, orchestration, governance, vendor-agnostic]
tools: [claude, cursor, gemini, codex, antigravity]
license: "MIT"
license_source: "https://github.com/yehudalevy-collab/polis-protocol/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Polis Protocol —— 一个持续进化的智能体团队

## 概述

大多数智能体协调系统是一个被动看板：认领任务、执行、标记完成。它只记录，从不变得更聪明，规则也是冻结的。Polis Protocol 是主动的替代方案——一个由 markdown 文件组成的文件夹，其中每个智能体是一个持有能力卡的"公民"，工作由学习型 bandit 算法路由给在任务标签上业绩最好的智能体，已结算的工作将经验归档并更新路由，公民可以提出并投票修改协议本身的规则。它供应商无关：Antigravity、Claude、Codex 和 Gemini 智能体都可以共享同一个 `_polis/`。

在 Antigravity 中，这把 Manager View 的固定流水线变成一个真正学习谁最擅长每类工作的团队，而不是每次以相同顺序运行相同角色。

## 何时使用此技能

- 当 2 个以上智能体（尤其是跨供应商）在一个项目上协作，且"谁应该做这个"是一个真实问题时使用。
- 当你希望团队随时间可衡量地改进——路由根据结果自适应，而非依赖静态角色标签时使用。
- 当你需要一份持久的、可通过 git 审计的记录，追踪谁做了什么、学到了什么、哪些规则变更了时使用。
- 当 Antigravity 的默认编排过于僵化，你希望在其之上添加路由和治理时使用。

## 工作原理

### 步骤 1：建立一个 polis

默认使用经过审查的 checkout，以便脚手架代码在写入项目前被固定：

```bash
git clone https://github.com/yehudalevy-collab/polis-protocol.git
cd polis-protocol
git checkout <reviewed-commit-sha>
python3 scripts/init_polis.py \
  --project-root . \
  --agent-id gemini-antigravity-yourproject \
  --vendor google --model gemini-3 --tool antigravity
```

如果你倾向使用已发布的 PyPI 包，在审查该版本后安装确切版本，例如 `pipx install polis-protocol==<reviewed-version>`。不要通过未固定的 `uvx` 或 "latest" 工作流来调用该包进行自动化设置。

此操作会写入 `_polis/` 并将技能写入 `.agents/skills/`（Antigravity 读取的路径），以及桥接指针（`GEMINI.md`、`AGENTS.md`），将每个工具指向 `_polis/CONSTITUTION.md`。提示：添加 `--dry-run` 可在任何文件写入前预览；init 永不覆盖已有文件，`polis init --repair` 可恢复缺失文件。

### 步骤 2：注册公民并开启合约

每个智能体在 `_polis/citizens/` 下发布一张能力卡。工作以带有 `required_tags` 的合约形式开启，而非分配给固定角色。

### 步骤 3：按历史业绩路由

```bash
polis route --polis-root _polis \
  --contract _polis/contracts/open/your-task.md --explain
```

路由器打印评分明细（历史记录 / 自评 / 成本 / 可用性 / 已应用经验），并推荐在任务标签上业绩最强的公民。智能体还可以保留文件（`polis reserve src/auth --as <citizen>`），确保两个智能体不会同时编辑同一路径——重叠的声明会被拒绝并告知持有者。

### 步骤 4：结算、学习与修订

```bash
polis contract settle <contract-id> --quality 5
polis reconcile --polis-root _polis
```

已结算的合约会归档一条经验；被接受的经验带有一个有界的 `routing_effect`，路由器在下一个类似任务中读取并在 `--explain` 中引用。失败会变成护栏（`polis guardrail add …`），未来具有相同标签的合约将这些护栏继承为必须通过的验收标准。当一条规则不再有效时，公民可以提出修正案，其他公民投票。你可以自行复现学习声明：`polis bench --mode learning`。

## 示例

### 示例 1：观察团队学习（无需安装，30 秒）

```bash
git clone https://github.com/yehudalevy-collab/polis-protocol.git
cd polis-protocol
git checkout <reviewed-commit-sha>
bash scripts/demo.sh
```

路由器为西班牙语翻译合约推荐 Gemini——因为已结算的工作教会了它该智能体在该标签上有最佳记录，而非因为有人重新分配了任务。

### 示例 2：解释任意路由决策

```bash
python3 scripts/route_contract.py --polis-root examples/research-team/_polis \
  --contract examples/research-team/_polis/contracts/open/parent-newsletter-issue-3.md --explain
```

## 备注

- 无服务器、无运行时、无数据库——整个协议就是 markdown 加两个小型 Python 脚本。
- 设计上供应商无关；Claude 或 Codex 智能体可以加入由 Antigravity 智能体创建的同一个 polis。
- 完整 Antigravity 集成指南：https://github.com/yehudalevy-collab/polis-protocol/blob/main/docs/antigravity.md

## 局限性

- 路由质量取决于准确的公民能力卡和足够多的已结算工作历史以供学习。
- 协议协调智能体工作，但不替代代码审查、测试或明确的维护者审批。
- 多智能体投票和修正案可能为小型、单一负责人的任务增加流程开销。
- 上游脚本是外部代码；固定到已审查的 commit 并在允许写入项目前运行 `--dry-run`。
