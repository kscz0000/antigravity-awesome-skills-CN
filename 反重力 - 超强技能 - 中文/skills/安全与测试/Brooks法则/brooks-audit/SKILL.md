---
name: brooks-audit
description: "架构审计技能：绘制模块依赖图、检查分层完整性，并基于十二本经典工程著作的洞见标记代码库中的结构性腐化。当用户提出以下需求时触发：审计架构、审查目录或模块结构、检查循环导入、理解架构、模块依赖、分层规则、康威定律。触发词：审计架构、模块依赖、分层完整性、结构腐化、循环依赖、康威定律。"
risk: unknown
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-audit
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 架构审计
## 何时使用

当你需要做架构审计——绘制模块依赖图、检查分层完整性、并标记整个代码库中的结构性腐化（融合十二本经典工程书的智慧）——请使用本技能。触发场景包括：用户要求审计架构、审查目录或模块结构、检查循环导入、理解架构、模块依赖关系、分层规则、康威定律（Conway's Law）等。

## 准备步骤

1. 阅读 `../_shared/common.md`，了解铁律、项目配置、报告模板与健康分规则
2. 阅读 `../_shared/source-coverage.md`，了解各书的覆盖范围、例外与权衡
3. 阅读 `../_shared/decay-risks.md`，了解症状定义与来源出处
4. 阅读本目录下的 `architecture-guide.md`，了解审计框架

## 流程

**新人引导模式：** 如果用户提出的是新人引导报告、代码库巡礼，或者"向新开发者讲解这个代码库"这类需求，请改读本目录下的 `onboarding-guide.md`，并遵循该指南而非 `architecture-guide.md`。该模式以讲解为导向，而非诊断——不输出健康分，也不输出铁律发现。

**如果用户没有指定要审计的文件或目录：** 应用 `../_shared/common.md` 中的"自动范围检测"逻辑，先确定审计范围再继续。

1. 收集代码库上下文，并用 Mermaid 绘制模块依赖图（参见指南的第 0–1 步）
2. 按指定顺序逐项扫描各类腐化风险（参见指南的第 2–4 步）
3. 在 Mermaid 图中按发现结果为节点配色（红/黄/绿）——在第 4 步之后进行
4. 运行可测试性接缝评估（参见指南的第 5 步）
5. 运行康威定律检查（参见指南的第 6 步）
6. 使用 common.md 中的报告模板输出——先放 Mermaid 图，再放发现项

**报告中的模式行：** `Architecture Audit`

## 局限性

- 仅当任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭据以及外部服务行为。
- 不要把示例当作环境专属测试、安全审查，或用户对破坏性/高成本操作的授权替代品。
