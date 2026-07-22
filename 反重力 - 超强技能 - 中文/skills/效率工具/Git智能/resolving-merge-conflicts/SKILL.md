---
name: resolving-merge-conflicts
description: "用于解决进行中的 git 合并 / rebase 冲突。触发词：合并冲突、rebase 冲突、git冲突、解决冲突、merge conflict"
risk: unknown
source: https://github.com/mattpocock/skills/tree/main/skills/engineering/resolving-merge-conflicts
source_repo: mattpocock/skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/mattpocock/skills/blob/main/LICENSE
---

# 解决合并冲突（Resolving Merge Conflicts）

## 何时使用

当需要解决进行中的 git 合并 / rebase 冲突时使用本技能。

1. **查看当前状态**：检查 git 历史以及冲突文件。

2. **找到每个冲突的原始来源**：深入理解每次改动背后的原因以及最初的意图。阅读提交消息、查看 PR、检查原始 issues / 工单。

3. **逐个解决冲突块**：能保留双方意图的就同时保留；若互不兼容，挑选与本次合并目标一致的那一侧，并注明权衡取舍。**不要**凭空发明新行为。始终要解决冲突，永远不要 `--abort`。

4. 找出项目里的**自动化检查**并运行——通常是先 typecheck，再跑测试，最后格式化。修复合并引入的所有问题。

5. **完成合并 / rebase**：把所有变更暂存并提交。若在 rebase，则继续 rebase 流程，直到所有提交都 rebase 完毕。

## 局限性

- 仅当任务明确匹配上游来源与本地项目场景时使用本技能。
- 在应用变更前，先验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要把示例当作环境特定测试、安全审查或对破坏性 / 高成本操作的用户审批的替代品。