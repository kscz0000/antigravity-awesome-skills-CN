---
name: accint-frames
description: 通过 acc_act(runtime="continue") 排空 acc 的审议队列——即由无头运行检查点化的开放/等待 brain_frames。触发词：帧、排空队列、acc 审议、brain_frames、acc frames。
risk: unknown
source: https://github.com/maxbaluev/accreted-intelligence/tree/main/plugins/claude/skills/frames
source_repo: maxbaluev/accreted-intelligence
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/maxbaluev/accreted-intelligence/blob/main/LICENSE
---

# 帧
## 何时使用

当你需要通过 `acc_act(runtime="continue")` 排空 acc 的审议队列——即由无头运行检查点化的开放/等待 brain_frames 时，请使用本技能。


这是对两个 MCP 动词之上的路由糖——这里不承载任何业务逻辑。

1. 列出队列：`acc frames`（CLI，只读观察）。
2. 对每个开放/等待的帧：读取其类型化空洞（typed hole）+ 已检索的上下文，进行审议，
   然后通过以下方式提交：
   `acc_act(runtime="continue", input={"frame_id": ..., "submit_token": ..., "proposal_text": ...})`。
3. `proposal_text` 必须以 `PREDICT: <0.00-1.00> <why>` 结尾；acc 会在 owner 看到之前
   剥离该行，并据此针对后续结果校准 Work Model。
4. 重复相同的提交会重放缓存的结果——重新提交是安全的。
5. 暴露每个决议的 `commitment` id 与引用的 `[ids]`；在接手新工作前完全排空队列——
   检查点化的帧是无头运行为你保存的工作。

## 限制

- 仅当任务明确匹配其上游来源与本地项目上下文时，才使用本技能。
- 在应用更改前，请验证命令、生成的代码、依赖、凭据与外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性/高成本操作批准的替代。