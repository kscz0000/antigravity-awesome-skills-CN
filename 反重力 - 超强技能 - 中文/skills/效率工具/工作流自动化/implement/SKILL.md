---
name: implement
description: "基于 PRD 或一组 issues 实现一项工作。触发词：实现、PRD落地、issue实现、按PRD实现"
risk: unknown
source: https://github.com/mattpocock/skills/tree/main/skills/engineering/implement
source_repo: mattpocock/skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/mattpocock/skills/blob/main/LICENSE
---

# 实施技能（Implement）

## 何时使用

当你需要基于 PRD 或一组 issues 实施一项工作时，使用本技能。

按 PRD 或 issues 中描述的内容完成工作。

尽可能在预先约定好的边界处使用 /tdd。

定期运行类型检查和单文件测试，全量测试套件在最后跑一次。

完成后，使用 /review 复盘工作。

把工作提交到当前分支。

## 局限性

- 仅当任务明确匹配上游来源与本地项目场景时使用本技能。
- 在应用变更前，先验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要把示例当作环境特定测试、安全审查或对破坏性 / 高成本操作的用户审批的替代品。