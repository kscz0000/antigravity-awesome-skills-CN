---
name: brooks-review
description: "PR 代码审查：以症状 → 根源 → 后果 → 修复 的具体发现揭示腐化风险、设计坏味与可维护性问题，汲取十二本经典工程著作之精华。触发词：用户要求审查代码、检查 PR、分享 diff 或粘贴代码寻求……"
risk: unknown
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-review
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — PR 审查
## 何时使用

当你需要获得 PR 代码审查、以"症状 → 根源 → 后果 → 修复"的具体发现揭示腐化风险、设计坏味与可维护性问题，并参考十二本经典工程著作时，请使用本技能。触发场景：用户要求审查代码、检查 PR、分享 diff 或粘贴代码寻求……

## 准备工作

1. 阅读 `../_shared/common.md`，了解铁律、项目配置、报告模板与健康分规则
2. 阅读 `../_shared/source-coverage.md`，了解著作覆盖率、例外情况与权衡
3. 阅读 `../_shared/decay-risks.md`，了解症状定义与根源归属
4. 阅读本目录下的 `pr-review-guide.md`，了解分析流程

## 流程

**若用户未指定文件或粘贴代码：** 先按 `../_shared/common.md` 的"自动范围探测"规则确定审查范围，再继续。

1. 明确审查范围，然后按指定顺序扫描各项腐化风险（指南步骤 1–6）
2. 执行快速测试检查（指南步骤 7）——纯文档或非生产改动可跳过
3. 对每条发现应用铁律
4. 按 common.md 的报告模板输出

**报告中的模式行：** `PR Review`

## 局限

- 仅在任务与上游来源及本地项目上下文明确匹配时使用本技能。
- 在应用变更前，请核实命令、生成的代码、依赖、凭据与外部服务行为。
- 切勿将示例视为环境专属测试、安全审查或用户对破坏性、高成本操作的审批的替代品。
