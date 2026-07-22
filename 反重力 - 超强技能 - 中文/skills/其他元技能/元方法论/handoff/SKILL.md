---
name: handoff
description: 将当前对话压缩为交接文档，供另一个智能体接手继续工作。交接、handoff、交接文档、会话转交、继续任务、压缩对话、上下文传递
argument-hint: "下一个会话将用于什么目的？"
disable-model-invocation: true
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

## 使用时机

当此工作流匹配用户请求时使用：将当前对话压缩为交接文档，供另一个智能体接手继续工作。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_

编写一份交接文档，总结当前对话，以便新智能体能够继续完成这项工作。保存到用户操作系统的临时目录中，而非当前工作区。

在文档中加入"建议技能（suggested skills）"章节，列出该智能体应当调用的技能。

不要重复其他制品（PRD、计划、ADR、issue、提交、diff）中已有的内容。应改为通过路径或 URL 引用它们。

对所有敏感信息进行脱敏处理，例如 API 密钥、密码或个人身份信息。

如果用户传入了参数，将其视为对下一个会话将聚焦内容的描述，并据此调整文档。


## 局限性

- 当工作流指定了上游工具、账号、API 密钥或本地配置时，需要提前准备这些条件。
- 未经用户明确批准，不得执行破坏性、生产环境、付费或对外发送消息类的操作。
- 在将生成的制品或建议视为最终结论之前，需用用户的真实来源对其进行校验。