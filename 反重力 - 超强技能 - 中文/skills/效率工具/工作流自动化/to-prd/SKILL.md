---
name: to-prd
description: 将当前对话转化为 PRD 并发布到项目问题追踪器——无需访谈，仅综合你已经讨论过的内容。创建PRD、生成PRD、产品需求文档、写PRD、PRD文档、需求文档、to-prd。
disable-model-invocation: true
category: "project-management"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - project-management
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

## 何时使用

当此工作流匹配用户请求时使用：将当前对话转化为 PRD 并发布到项目问题追踪器——无需访谈，仅综合你已经讨论过的内容。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills) (MIT)。_本技能会基于当前对话上下文和对代码库的理解产出 PRD。不要访谈用户——直接综合你已经了解的内容。

问题追踪器与分流标签词汇应该已经提供给你——如果没有，请运行 `/setup-matt-pocock-skills`。

## 流程

1. 浏览代码库以理解其当前状态（如果你还没有这样做）。在 PRD 全程使用项目的领域术语词汇，并尊重你所触及领域中已有的任何 ADR。

2. 勾勒出你将要测试该功能的接缝点。优先使用已有的接缝点而非新增。尽可能使用最粗粒度的接缝点。如果需要新增接缝点，请在你能做到的尽可能高的层级提出。代码库中的接缝点越少越好——理想数量是 1 个。

与用户确认这些接缝点是否符合预期。

3. 使用下方模板撰写 PRD，然后发布到项目问题追踪器。应用 `ready-for-agent` 分流标签——无需额外分流。

<prd-template>

## Problem Statement

用户所面临的问题，从用户视角描述。

## Solution

针对该问题的解决方案，从用户视角描述。

## User Stories

一份**很长的、编号排列的用户故事列表**。每条用户故事应采用以下格式：

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

该用户故事列表应当**极其详尽**，覆盖该功能的方方面面。

## Implementation Decisions

已做出的实施决策列表。可以包含：

- 将被构建/修改的模块
- 这些模块将被修改的接口
- 开发者的技术澄清
- 架构决策
- Schema 变更
- API 契约
- 具体的交互方式

**不要**包含具体的文件路径或代码片段。它们可能很快就会过时。

例外：如果某个原型产出的代码片段比散文能更精确地表达一项决策（状态机、reducer、schema、类型形状），将其内联到相关决策中，并简要说明它来自原型。裁剪到承载决策的部分——不是可工作的 demo，只是关键片段。

## Testing Decisions

已做出的测试决策列表。包含：

- 关于什么是好测试的描述（只测试外部行为，不测试实现细节）
- 哪些模块将被测试
- 测试的既有参考（即代码库中类似类型的测试）

## Out of Scope

对本次 PRD 而言**超出范围**事项的描述。

## Further Notes

关于该功能的任何补充说明。

</prd-template>


## 局限性

- 当工作流指定了上游工具、账号、API key 或本地配置时，需要具备这些前提。
- 未经用户明确批准，不会执行破坏性、生产环境、付费或对外消息类操作。
- 在将生成的产物或建议视为最终结果之前，请根据用户的真实来源进行校验。