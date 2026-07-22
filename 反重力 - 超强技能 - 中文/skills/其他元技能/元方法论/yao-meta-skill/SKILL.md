---
name: yao-meta-skill
description: 从工作流、提示词、对话记录、文档或笔记中创建、重构、评估并打包智能体技能。用于技能创建、可复用工作流封装、技能改进、评估以及面向团队的分发。涉及技能创作、可复用工作流封装、技能改进、评估、团队就绪分发。
metadata:
  author: Yao Team
category: "skill-authoring"
risk: "safe"
source: "community"
source_repo: "yaojingang/yao-meta-skill"
source_type: "community"
date_added: "2026-06-19"
author: "Yao Team"
license: "MIT"
license_source: "https://github.com/yaojingang/yao-meta-skill/blob/main/LICENSE"
tags:
  - skill-authoring
  - agent-skills
  - 评估
  - 打包
tools:
  - claude-code
  - codex-cli
  - cursor
  - gemini-cli
---

# Yao 元技能

## 适用场景

当工作流匹配以下用户需求时使用：从工作流、提示词、对话记录、文档或笔记中创建、重构、评估并打包智能体技能。用于技能创建、可复用工作流封装、技能改进、评估以及面向团队的分发。


_来源：[yaojingang/yao-meta-skill](https://github.com/yaojingang/yao-meta-skill) (MIT)。_

## 路由规则

- 按 frontmatter `description` 路由。
- 保持 `SKILL.md` 精简；将指南放在 `references/`、逻辑放在 `scripts/`、证据放在 `reports/`。
- 使用最轻量且可靠的流程。

## 模式

- `Scaffold`：探索性或个人用途。`Production`：团队复用。`Library`：共享基础设施。`Governed`：高信任、策略敏感或发布关键。
- 规则：[方法](references/skill-engineering-method.md)、[运行模式](references/operating-modes.md)、[资源边界](references/resource-boundaries.md)。

## 精简工作流

1. 对于一次性或无可复用流程的任务：不创建技能；归为 `near-neighbor`；要求具备 `repeated use` 与 `reusable output contract`。
2. 捕获任务、输出、排除项、约束、规范以及最轻量的适配方式。
3. 按顺序扫描 references：外部基准、用户来源、本地适配；仅呈现不确定或冲突之处。
4. 尽早撰写 `description`，测试路由质量，再按需添加目录与关卡。
5. 仅在有用时引入输出风险、产物设计、提示词质量、系统模型与下一步方向。

实战手册：[方法](references/skill-engineering-method.md)、[意图对话](references/intent-dialogue.md)、[技能 IR](references/skill-ir-method.md)、[输出评估](references/output-eval-method.md)、[审阅工作室](references/review-studio-method.md)。

## Skill OS 2.0 关卡

对于 production、library、governed 或团队分发的工作，发布前需依次通过 Skill IR、目标编译器、触发与输出评估、Skill Atlas、符合性、信任、注册表/打包/安装、升级、漂移、豁免以及 Review Studio 关卡。

## Governed 包边界

对于文件支撑、发布关键或受治理的包，将 `input_files` 命名为 `file-backed fixture` 证据；包含 `owner`、`review cadence`、`input_files`、`output contract`、`rollback boundary`；要求 `trust report` 与 `reports/output_quality_scorecard.md`；将不可用的遥测、审批、指标或基准标记为 `missing evidence`；不得伪造证据。

适用时按字面保留审计标签：`file-backed fixture`、`input_files`、`output contract`、`rollback boundary`、`trust report`、`reports/output_quality_scorecard.md`、`missing evidence`。

## 首轮风格

- 从用户的工作或成果入手，再考虑结构。
- 除非已有足够细节，否则只问 `2-3` 个关键问题。
- 中文语境下语气柔和、贴近陪伴式交流；使用 [意图对话](references/intent-dialogue.md)。

## 输出契约

除非另有要求，否则产出 `SKILL.md`、对齐的 `agents/interface.yaml`、经过论证的资产，以及关于边界、排除项、关卡与下一步的简要摘要。

## 参考图谱

主要参考：[方法](references/skill-engineering-method.md)、[产物设计](references/artifact-design-doctrine.md)、[系统思维](references/systems-thinking-doctrine.md)、[治理](references/governance.md)、[SkillOps 决策](references/skillops-decision-policy.md)。


## 局限

- 当工作流指定了上游工具、账号、API 密钥或本地环境时，需依赖这些前置条件。
- 未经用户明确批准，不会执行破坏性、生产级、付费或对外消息发送等操作。
- 将生成的产物或建议视作最终结果前，请基于用户真实来源进行验证。
