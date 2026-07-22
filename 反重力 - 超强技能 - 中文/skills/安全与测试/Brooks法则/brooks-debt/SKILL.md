---
name: brooks-debt
description: '技术债评估技能，用于识别、分类和优先级排序可维护性问题，帮助团队制定重构路线图，借鉴十二本经典工程学著作。当用户询问技术债、重构优先级、先清理什么，或问"为什么......"时触发。触发词：技术债、技术债务、tech debt、重构优先级、refactoring priority、可维护性、maintainability、技术债评估、代码清理优先级、腐烂风险。'
risk: unknown
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-debt
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 技术债评估
## 何时使用

当你需要识别、分类并按优先级排序代码库中的可维护性问题，以帮助团队制定重构路线图时使用本技能，其依据源自十二本经典工程学著作。触发场景：用户询问技术债、重构优先级、先清理什么，或问"为什么……"

## 配置

1. 阅读 `../_shared/common.md` 以了解铁律、项目配置、报告模板和健康分规则
2. 阅读 `../_shared/source-coverage.md` 以了解书籍级覆盖、例外与权衡
3. 阅读 `../_shared/decay-risks.md` 以了解症状定义和来源归属
4. 阅读本目录下 `debt-guide.md` 以了解技术债分类框架

## 流程

**如果用户未描述代码库或未指向具体区域：** 应用 `../_shared/common.md` 中的自动范围检测以在继续之前确定评估范围。

1. 扫描全部六类腐烂风险（指南步骤 1）；在打分前列出每一条发现
2. 应用 Pain × Spread 优先级公式并对债项意图进行分类（指南步骤 2–3）
3. 按腐烂风险对发现进行分组（指南步骤 4）
4. 使用 common.md 中的报告模板以及债务汇总表输出

**报告中的模式行：** `Tech Debt Assessment`

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时，才可使用本技能。
- 在应用变更之前，请验证命令、生成的代码、依赖项、凭据以及外部服务行为。
- 不可将示例视为环境专属测试、安全审查或用户对破坏性/高成本操作的批准的替代品。