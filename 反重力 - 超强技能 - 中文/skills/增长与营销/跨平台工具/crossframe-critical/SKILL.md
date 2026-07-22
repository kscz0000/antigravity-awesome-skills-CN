---
name: crossframe-critical
description: "Use only when the user explicitly names crossframe-critical for a Chinese structural critique dossier, article plan, or long-form critical essay."
category: content
risk: safe
source: community
source_repo: xi-kari/crossframe-skill
source_type: community
date_added: 2026-06-16
author: xi-kari
license: MIT
license_source: https://github.com/xi-kari/crossframe-skill/blob/main/LICENSE
tools:
  - "Agent Skills"
  - Codex
  - Claude
tags:
  - crossframe
  - chinese
  - critique
  - essay
  - structural-analysis
---
# CrossFrame 批判（CrossFrame Critical） 触发词：批判文章、结构批判、批判底稿、批判矩阵、篇章方案、crossframe-critical、中文批判长文


## 何时使用此技能

- 仅当用户明确点名 `crossframe-critical`、`$crossframe-critical`，或要求测试这个批判平行技能时使用。
- 用于中文的结构批判档案、批判矩阵、文章方案与长文批判写作。
- 不要把它放进默认的 `crossframe-suite` 路由。

## 打包来源说明

本份 AAS-ready 副本保留下方原始 CrossFrame 技能主体。中文仍是规范语义层；英文元数据仅用于发现、安装与仓库审查。

## 局限

- 技能主体刻意以中文为规范语言；英文元数据仅用于发现，不能替代原中文术语。
- 必须在明确 CrossFrame 调用或 `crossframe-suite` 路由之后才使用；不要把它当作通用默认推理层。
- 它负责结构化分析、起草与审稿，但不能替代来源核验、领域判断，也不能替代法律、医疗、财务判断。

> **本 skill 不独立触发。** 所有 CrossFrame 任务统一从 `crossframe-suite` 入口调度。用户无需直接调用本 skill；suite 根据路由规则在需要时自动加载。

这是本地的平行测试技能，不能替代 `crossframe`、`crossframe-essay`、`crossframe-public` 或 `crossframe-suite`。

## 定位

`crossframe-critical` 写中文批判长文：先用 CrossFrame 搭起结构、证据边界、尺度、机制候选与判断档位，再把输出锻造成批判。

批判可以吸收马克思主义的问题意识：利益、成本转嫁、异化、商品化、意识形态、自然化的支配与条件的再生产；但不能机械地把所有题目都套进阶级/资本话术。

## 必读清单

每次触发都要读取：

1. `../crossframe/SKILL.md`
2. `../crossframe/references/read-routing-map.md`
3. 若批判涉及高责任、公开、AI/过程性产物、生命周期、无法退出主体或文章输出场景，复用 `../crossframe/templates/read-state-capsule.md` 作为 `v5-read-state-capsule`，并跑 `../crossframe/worksheets/source-anchor-integrity-check.md`；若胶囊缺失，回到 `../crossframe/SKILL.md`，不要在此自造来源路由。
4. `protocols/critical-article-protocol.md`
5. `references/critical-matrix.md`
6. `references/example-and-evidence-rules.md`
7. 若涉及真实公共对象、最新事实、机构、平台、政策、人物、公司、数据、AI/过程性产物或强判断，读取 `../crossframe/references/source-ledger-workflow.md` 并建立来源台账。
8. `templates/critical-output-template.md`

若题目需要长文风格控制，附加读取 `../crossframe-essay/SKILL.md`，只复用其篇章纪律，不要搬它的整套输出契约。

## 工作流

1. 先搭 CrossFrame 底座：分析对象、事实边界、尺度窗口、机制候选、判断档位与证据缺口。
2. 应用批判矩阵：成本链、受益链、权力/资源分配、概念遮蔽、再生产机制、弱信号与反向条件。
3. 规划篇章：中心命题、读者位置、例子、段落顺序、字数分配与结尾余味。
4. 从档案起写完整长文。除非用户另行指定，正文默认 1800-2800 中文字。
5. 跑一次最终边界检查：没有人格审判、没有扣帽子、没有阴谋论、没有未核验的强判断，也没有口号替代分析。

## 输出

默认输出正好有三块可见结构：

```text
# 批判底稿
# 篇章方案
# 正文
```

除非用户明确要求，不要把结果压成短答、清单、备忘或诊断摘要。

## 硬规则

- 先从 CrossFrame 结构出发，再变成批判；不要从义愤出发、用结构词去装饰。
- 批判机制、利益、话术、制度与责任链；不要把结构批判变成人格审判。
- 真实或近期公共事件，做事实主张前必须查源，并附可见的来源台账摘要。未核验的例子必须标注为类比、假设或常见模式。
- 除非用户提供了一个边界非常窄的案例且明确要求不展开，否则正文里至少用两个具体例子。
- 至少写一个反向条件、证据缺口或撤回条件。
- 不要把马克思主义术语当声望词汇用。若一个术语说不清谁付出、谁获益、什么被遮蔽、条件如何重复，就把它删掉。
