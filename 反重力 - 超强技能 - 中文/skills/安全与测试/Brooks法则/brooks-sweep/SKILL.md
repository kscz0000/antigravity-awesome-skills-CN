---
name: brooks-sweep
description: "全量扫描模式：在所有质量维度上运行统一分析——代码腐化、架构、技术债、测试质量——然后直接对代码库应用修复。安全的变更会自动应用；有风险的变更在执行前需要确认。借鉴十二本经典著作……"
risk: unknown
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-sweep
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 全量扫描与自动修复
## 何时使用

当你需要全量扫描模式时使用此技能：在所有质量维度上运行统一分析——代码腐化、架构、技术债、测试质量——然后直接对代码库应用修复。安全的变更会自动应用；有风险的变更在执行前需要确认。借鉴十二本经典著作……


## 准备工作

1. 阅读 `../_shared/common.md`，了解铁律、项目配置、报告模板和健康分规则
2. 阅读 `../_shared/source-coverage.md`，了解书籍层面的覆盖范围、例外和权衡
3. 阅读 `../_shared/decay-risks.md`，了解生产风险症状的定义
4. 阅读 `../_shared/test-decay-risks.md`，了解测试风险症状的定义
5. 阅读本目录下的 `sweep-guide.md`，了解统一的扫描与修复流程

## 流程

**如果用户未指定项目或目录：** 在继续之前，应用 `../_shared/common.md` 中的自动作用域检测来确定审查范围。

1. 显示预飞同意通知，并等待用户的一次性批准（指南的步骤 0）
2. 枚举作用域并初始化 `unresolvable` / `non_critical_rounds` / `fix_log` 状态（指南的步骤 1）
3. 按顺序运行四个维度——review、test、debt、audit——每个维度进行扫描、分类、应用 Safe + Extended-Safe 修复，并通过项目测试命令进行验证（指南的步骤 2–5）
4. 迭代：重新扫描修改过的文件 + 同模块 + 静态消费方；在干净的轮次上收敛，将 3 次重试失败的项移入 `unresolvable` 集合，将非关键轮次上限设为 3（指南的步骤 6）
5. 汇总残留项和不可解项，并输出全量扫描报告（指南的步骤 7–8）

**报告中的模式行：** `Full Sweep`

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时，才使用此技能。
- 在应用更改之前，请验证命令、生成的代码、依赖、凭据和外部服务的行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或高成本操作的批准的替代品。