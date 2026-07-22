---
id: skill-issue
name: skill-issue
description: "诊断编码智能体技能为何不触发——为每个 SKILL.md 按 A–F 评级，模拟给定提示词会触发哪个技能，并标记一个技能静默遮蔽另一个技能的冲突。"
category: meta
risk: safe
source: community
source_repo: mishanefedov/skill-issue
source_type: community
date_added: "2026-06-02"
author: mishanefedov
tags: [skills, linter, activation, meta, ci]
tools: [claude, cursor, gemini, codex]
license: "MIT"
license_source: "https://github.com/mishanefedov/skill-issue/blob/main/LICENSE"
---

# skill-issue — skill activation audit

## 概述

编码智能体根据每个技能始终在线的 `name` +
`description` 来决定运行哪个技能。一个技能可能实现得完美无缺，却从不触发——因为
描述太模糊，匹配不上用户实际的措辞，或者因为一个
更具体的兄弟技能静默胜出。`skill-issue` 专门审计这一层面，
为每个技能按 A–F 评级，模拟给定提示词会触发哪个技能，并
报告一个技能遮蔽另一个技能的冲突集群。

## 何时使用此技能

- 当你写的技能似乎从不触发，而你不知道原因时使用
- 当用户说"为什么我的技能不触发"、"哪个技能会响应 X"或"审计我的技能"时使用
- 在编写或安装新的 SKILL.md 之后使用，以确认它确实会被选中
- 在 CI 中使用，当 PR 添加了空描述/重复/冲突元数据的技能时使构建失败

## 工作原理

安装 CLI（`npm i -g @misha_misha/skill-issue`、`brew install mishanefedov/skill-issue/skill-issue` 或 `npx @misha_misha/skill-issue`），然后：

```bash
skill-issue ~/.claude/skills                       # grade every skill A–F (+ collisions summary)
skill-issue ~/.codex/skills --why "deploy to prod" # which skill fires for this prompt, and why
skill-issue <dir> --collisions                     # clusters of skills that shadow each other
skill-issue <dir> --fix                            # append a "Use when …" clause to weak descriptions
skill-issue <dir> --json                           # machine-readable; exits non-zero on errors
```

默认使用离线启发式；加 `--llm` 可通过本地 `claude`/`codex` CLI 进行评判。

## 示例

### 示例 1：审计已安装的技能

```bash
skill-issue ~/.claude/skills
# F  deploy-helper  ✗ no description — can never fire
# C  shipit         ! no "use when …" trigger clause
# A  rollback-prod  ✓ will fire on its triggers
```

### 示例 2：诊断冲突

```bash
skill-issue ~/.claude/skills --why "deploy the app to prod"
#  1. shipit       0.74  ← would fire
#  2. land-deploy  0.69  (margin 0.05 — ambiguous, likely collision)
```

## 局限性

- 离线评分基于启发式，应视为分诊信号，而非最终质量判定。
- 冲突报告突出可能的遮蔽情况，但不同智能体的路由器对元数据的权重可能不同。
- `--fix` 模式可以改善弱触发措辞，但生成的编辑在提交前仍需维护者审查。
