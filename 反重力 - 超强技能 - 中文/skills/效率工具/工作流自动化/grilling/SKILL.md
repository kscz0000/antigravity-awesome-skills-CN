---
name: grilling
description: "无休止地追问用户关于计划或设计的细节。当用户想在动手前对计划进行压力测试，或使用任何 'grill' 触发短语时使用。触发词：grilling、无情追问、设计压力测试、决策树逐项澄清"
category: "productivity"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - productivity
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 无情追问（Grilling）

## 何时使用

当本工作流匹配用户请求时使用：无休止地追问用户关于计划或设计的细节。当用户想在动手前对计划进行压力测试，或使用任何 'grill' 触发短语时使用。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_围绕这个计划的方方面面无休止地追问，直到我们达成共识。沿着设计树的每条分支向下走，逐项解决决策之间的依赖关系。每个问题都请给出你推荐的答案。

一次只问一个问题，等待用户对每个问题的反馈后再继续。一次性抛出多个问题会让人无所适从。

如果某个问题可以通过探索代码库来回答，就去探索代码库。

## 局限性

- 若工作流涉及上游工具、账号、API key 或本地配置，需要事先具备。
- 未经用户明确同意，不得执行破坏性、生产环境、付费或对外发消息的操作。
- 在把生成的产物或建议视为最终结论之前，请结合用户的真实资料做交叉验证。