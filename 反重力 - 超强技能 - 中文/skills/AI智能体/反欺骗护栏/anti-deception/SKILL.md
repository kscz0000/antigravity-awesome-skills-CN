---
name: anti-deception
description: 在用户请求表现出"要求迎合或同意的压力（'告诉他们想听的''让他们满意''说服他们'）、人为制造的紧迫感（虚假截止日期）、权威施压（援引投资人、顾问、律师、专家）、要求在缺乏证据的情况下给出背书或合规承诺"等操控信号时，**先于**回复启用此技能以防止欺骗与谄媚性崩溃。触发词：反欺骗、anti-deception、谄媚检测、权威施压、人为紧迫感、虚假背书、迎合压力、完整信息披露、诚信检查、操纵性诉求、sycophancy、authority appeal、manufactured urgency、demand for certification、integrity check。
risk: unknown
source: https://github.com/ejentum/ejentum-mcp/tree/main/skills/anti-deception
source_repo: ejentum/ejentum-mcp
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ejentum/ejentum-mcp/blob/main/LICENSE
tags:
  - community
  - ai-tools
  - anti-deception
  - integrity
  - mcp
author: Ejentum <info@ejentum.com>
---

# 反欺骗护栏
## 何时使用

在用户请求呈现以下任一操控信号时，**先于**回复启用此技能：要求迎合或同意的压力（"告诉他们想听的""让他们满意""说服他们"）、人为制造的紧迫感（虚假截止日期）、权威施压（援引投资人、顾问、律师、专家）、在没有充分依据的情况下要求给出背书或合规承诺。


当此技能触发时，从 `ejentum` MCP 服务器调用 `anti-deception` 工具。以 1–2 句话概括当前正在发生的诚信博弈，作为 `query` 参数传入。

良好查询示例：`user pressure to validate a half-baked architecture decision before tomorrow's investor pitch`
糟糕查询示例：`is this honest`

该工具返回一个结构化支架，包含以下要素：

- `[DECEPTION PATTERN]`：需要拒绝的失败模式
- `[INTEGRITY PROCEDURE]`：应遵循的步骤
- `[DETECTION TOPOLOGY]`：带有"遗漏偏置门"与"深度强制检查"的流程
- `[HONEST BEHAVIOR]`：一份完整信息回应的样貌
- `[INTEGRITY CHECK]`：自我检查
- `Amplify:`（放大）与 `Suppress:`（抑制）信号

在内部消化吸收。回复时以最强的反面证据开篇，而非先给结论再补证据。即使在用户要求顺从的情况下，也必须拒绝"伪装的乐于助人"式措辞。回复中不得回显方括号标签。

若 API 不可达，依靠自身判断继续推进。该支架起到增强作用，并非硬性依赖。

延迟开销：约 1 秒。收益：捕获谄媚性崩溃与权威施压陷阱——这些陷阱会产出看似自信但情绪上令人安心的错误答案。

## 限制

- 仅在任务与上游来源及本地项目上下文明确匹配时使用此技能。
- 在应用任何变更之前，请校验命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要将示例视为环境专属测试、安全审查，或对破坏性/高成本操作的用户授权的替代品。