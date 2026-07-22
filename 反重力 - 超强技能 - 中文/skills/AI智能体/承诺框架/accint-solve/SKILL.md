---
name: accint-solve
description: 通过 acc_act(runtime="solve") 将目标路由至 acc 的评分记忆循环；对返回的 brain_frame 进行审议，并通过 continue 提交。触发词：solve、accint-solve、acc_act、brain_frame、评分记忆循环
risk: unknown
source: https://github.com/maxbaluev/accreted-intelligence/tree/main/plugins/claude/skills/solve
source_repo: maxbaluev/accreted-intelligence
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/maxbaluev/accreted-intelligence/blob/main/LICENSE
---

# solve（求解）
## 使用场景

当你需要通过 `acc_act(runtime="solve")` 将目标路由至 acc 的评分记忆循环，对返回的 brain_frame 进行审议，并通过 `continue` 提交结果时，请使用本技能。

本技能只是对两个 MCP 动作的路由封装——本身不包含任何业务逻辑。

1. 调用 `acc_act(runtime="solve", input="<the goal>")`。
2. 若结果是 **final（终态）**：返回答案、`commitment` id 以及引用的 `[ids]`。
3. 若结果是 **brain_frame**：轮到你进行审议——frame 是带类型的
   （包含哪个空洞、检索到了什么、做出了什么预测）。基于 frame 进行推理，然后通过
   `acc_act(runtime="continue", input={"frame_id": ..., "submit_token": ..., "proposal_text": ...})` 提交。
4. `proposal_text` 必须以 `PREDICT: <0.00-1.00> <why>` 结尾；acc 会在所有者看到之前剥离该行，
   并据此校准 Work Model 与后续结果的偏差。
5. 切勿对收到的 frame 置之不理；也切勿在循环外独自推导。
6. 稍后通过 `acc_act(runtime="outcome", ...)` 如实关闭 commitment。

## 局限性

- 仅当任务与上游来源及本地项目上下文明确匹配时，才使用本技能。
- 在应用任何变更前，请核实命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要将示例视为环境专属测试、安全审查或用户对破坏性/高成本操作的授权的替代品。