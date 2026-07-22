---
name: brooks-test
description: "基于十二本经典工程书籍（重点参考 xUnit Test Patterns、《单元测试的艺术》、How Google Tests Software 和《修改代码的艺术》）对测试套件进行质量审查，诊断既有测试套件的结构性问题：脆弱性、Mock 滥用等。触发词：brooks-test、测试质量审查、测试套件诊断、测试脆性、测试重复、Mock 滥用、覆盖率幻觉、架构不匹配。"
risk: unknown
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-test
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 测试质量审查
## 适用场景

当你需要对测试套件进行质量审查时使用本技能。它基于十二本经典工程书籍（重点参考 xUnit Test Patterns、《单元测试的艺术》、How Google Tests Software 和《修改代码的艺术》），诊断既有测试套件的结构性问题：脆弱性、Mock 滥用等。


## 准备工作

1. 阅读 `../_shared/common.md`，了解铁律、项目配置、报告模板和健康评分规则
2. 阅读 `../_shared/source-coverage.md`，了解书籍覆盖范围、例外情况和权衡取舍
3. 阅读 `../_shared/test-decay-risks.md`，了解测试维度症状定义和来源归属
4. 阅读本目录下的 `test-guide.md`，了解测试质量审查框架

## 处理流程

**如果用户尚未提供测试文件或测试目录：** 先按照 `../_shared/common.md` 中的自动范围检测规则确定审查范围，再继续后续步骤。

1. 绘制测试套件全景图（参考指南中"开始之前"章节）
2. 按指定顺序扫描各项测试衰退风险（指南的步骤 1–4）
3. 应用铁律并按报告模板输出（指南的步骤 5）

**报告中的模式行：** `Test Quality Review`

## 使用限制

- 仅在任务与上游来源和本地项目上下文明确匹配时使用本技能。
- 在应用变更前，请先验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要将示例视为针对特定环境的测试、安全审查或破坏性/高成本操作的批准依据。