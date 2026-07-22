---
name: accint-commitments
description: 对 acc 的开放承诺进行分类，并通过 acc_act(runtime="outcome") 以诚实的现实世界判定关闭它们。触发词：承诺管理、acc 承诺、开放承诺、承诺关闭、acc_act、outcome、承诺判定、承诺分诊、acc commitments、self_graded、waiting、owner、runtime。
risk: unknown
source: https://github.com/maxbaluev/accreted-intelligence/tree/main/plugins/claude/skills/commitments
source_repo: maxbaluev/accreted-intelligence
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/maxbaluev/accreted-intelligence/blob/main/LICENSE
---

# 承诺管理
## 使用时机

当你需要对 acc 的开放承诺进行分类，并通过 `acc_act(runtime="outcome")` 以诚实的现实世界判定关闭它们时，使用本技能。


两个 MCP 动词之上的路由糖衣——此处不包含任何业务逻辑。

1. 列出开放承诺：`acc commitments`（CLI，只读观察）。
2. 对每个可关闭的承诺：`acc_act(runtime="outcome", input={"ref": "<id>", "good": true|false, "note": "..."})`。
3. 来源归属规范：默认的 `self_graded` 是一个弱先验（积分按 0.25× 计算）。
   仅在所有者已校验时传入 `owner`；仅在现实已校验时传入 `external`/`runtime`
   （真实回复、测试通过、现实世界结果）。绝不要把自己的评分标记为现实。
4. 保持真正处于等待中的承诺处于开放状态——`waiting` 是一等干净状态。

## 局限

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，验证命令、生成的代码、依赖、凭据以及外部服务行为。
- 不要把示例当作特定环境测试、安全审查，或用户对破坏性/高成本操作的授权的替代品。
