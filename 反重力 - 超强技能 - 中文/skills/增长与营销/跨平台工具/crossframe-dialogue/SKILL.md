---
name: crossframe-dialogue
description: "当 CrossFrame Suite 路由中文读者回信、编辑回复、咨询式短答复或边界感知的结构建议时使用。跨框架对话、中文短答复、读者回信、咨询式回应、结构判断。"
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
  - dialogue
  - reader-reply
  - consultation
---
# CrossFrame 对话（CrossFrame Dialogue）

## 何时使用本技能

- 当 `crossframe-suite` 将一项明确的 CrossFrame 任务路由为读者回信、编辑回复、咨询式短答复或边界感知的建议时使用。
- 当答复应先把结构判断翻译为朴素中文，再做必要的术语映射时使用。
- 除非用户明确指名调用本同级技能，否则不要单独使用。

## 打包来源说明

本 AAS 就绪副本保留了原始 CrossFrame 技能主体。中文是权威语义层；英文元数据仅用于发现、安装与仓库审阅。

## 限制

- 技能主体刻意以中文为权威；英文元数据仅用于发现，不能替代原始中文术语。
- 仅在显式 CrossFrame 调用或 `crossframe-suite` 路由之后使用；不要把它当作通用的默认推理层。
- 它组织分析、起草与审阅，但不取代来源核查、领域专业判断，也不构成法律、医疗或财务判断。

> **本 skill 不独立触发。** 所有 CrossFrame 任务统一从 `crossframe-suite` 入口调度。用户无需直接调用本 skill；suite 会按路由规则在需要时自动加载。

若用户希望把短答复扩展为长文、公共评论、组织备忘录或案例沉淀，应先读取 `../crossframe-suite/SKILL.md` 进行总调度；本 skill 只负责短答复、编辑回信和咨询式回应。

## 定位

`crossframe-dialogue` 是 `crossframe` 与 `crossframe-essay` 的平行短答复 skill。它不复制 CrossFrame 全文，不写长文，也不把咨询式回应伪装成处方。默认输出短小但有洞察的结构化答复：接住问题、划出事实边界、给出结构判断、必要时批评、提出稳妥建议、明确停止/升级条件。

中文是权威语义；`CrossFrame Dialogue` 只是传播名与 skill id。遇到中英文理解冲突时，以中文术语和中文判断为准。

## 必读

每次触发后先读取：

1. `../crossframe/SKILL.md`
2. `../crossframe/references/read-routing-map.md`
3. 若问题触及高责任、公共制度、亲密关系、长期演化、框架治理、AI 现实验证、弱信号/不透明、无法退出、工具化、隐喻/来源透明或文章输出等场景，需追加读取 `../crossframe/references/continuity-bundles.md`，并按需使用 `../crossframe/worksheets/source-continuity-check.md`；未完成联读时只能降档处理。
4. 复用 `../crossframe/templates/read-state-capsule.md` 规定的 `v5-read-state-capsule`，并在高责任、公共、AI/过程性产物、生命周期、无法退出主体或文章输出等场景执行 `../crossframe/worksheets/source-anchor-integrity-check.md`。若胶囊缺失，回到 `../crossframe/SKILL.md` 补齐；本 skill 不重新发明源路由。
5. `protocols/dialogue-protocol.md`
6. `references/dialogue-quality-gates.md`

若用户要求亲切、编辑、同志口吻、答读者问、报刊回信、耐心解答、给意见，或问题天然像读者来信，再按需读取：

- `../crossframe-essay/SKILL.md`
- `../crossframe-essay/protocols/editorial-comrade-voice-protocol.md`
- `../crossframe-essay/references/editorial-voice-principles.md`
- `references/voice-bridge.md`

若涉及安全、法律、医疗心理、公开指控、处分、名誉、公共资源、强权力关系或紧急伤害风险，请读取 `protocols/consultation-boundary-protocol.md`。

## 默认流程

1. 判断回应类型：答读者问、编辑回信、咨询式回应、公共问题短评、概念问答、行动边界建议。
2. 用 `../crossframe/references/read-routing-map.md` 选择必要的 CrossFrame 协议、概念卡、模板或边界协议。
3. 做内部微型 intake：对象、事实边界、证据缺口、尺度窗口、机制候选、责任链/成本链、用户的真实用途。
4. 至少比较两个机制候选；证据不足时降低判断档位，不强判。
5. 把后台概念翻译为现实行为；术语仅在必要时映射，不在前台堆砌。
6. 输出短答复；除非用户要求，不展示完整工作表、长文底稿或概念链。

## 默认输出

默认 4 到 8 个短段，或使用 `templates/default-short-answer.md`：

- 先接住问题：说明困惑为何值得被认真对待。
- 再划事实边界：哪些是已知，哪些只是推测。
- 给出结构判断：现在更像哪一类机制，而不是谁天生如何。
- 必要时批评：批评行为、流程、责任转嫁或伪修复，不进行人格审判。
- 给稳妥建议：观察信号、低风险动作、修复条件、边界设置或退出转移。
- 写停止/升级条件：在何种情况下不再解释、需要求助、升级到专业/制度/安全路径，或撤回本判断。

## 硬规则

- 不输出“只安慰不判断”的答复。
- 不把结构诊断写成人格审判、道德宣判、命运预言或群体标签。
- 不用术语堆砌替代现实解释；删掉术语后第一段仍必须成立。
- 不把“爱”“理解”“修复”写成单方继续忍耐的义务。
- 不把 AI 报告、合规文本、道歉、复盘、声明或流程入口直接当作高成本证据。
- 不在证据不足时给出强处分、公开指控、法律/医疗/心理处方或不可逆建议。
- 不用宏大尺度取消低尺度的痛苦、责任、证据与行动边界。

## 失败自检

输出前快速检查：

1. 我有没有接住问题，但没有停在安慰？
2. 我有没有区分事实、解释、机制候选与判断档位？
3. 我有没有把批评指向行为/结构/责任链，而不是人格？
4. 我有没有给出可观察信号、低风险动作、停止条件或升级条件？
5. 删掉术语后，读者还能否知道该看什么、不要做什么？