---
name: sred-project-organizer
description: 将项目列表及其相关文档整理为 SRED 格式以供提交。触发词：SRED项目、SRED整理、研发税收抵免、项目文档、SRED格式化、项目归档
risk: unknown
source: community
---

# SRED 项目整理

SRED 要求项目以特定格式呈现。获取过去一年中参与的项目列表，将其按照 SRED 要求的格式进行总结，并附上支持性证据。输出一个 Notion 文档，其中每个可申报 SRED 的项目作为子文档。

## 适用场景
- 你需要将上一年度的工作总结转化为 SRED 格式的项目文档。
- 任务涉及将项目分类为可申报 SRED、收集证据，并在 Notion 中组织输出。
- 你已有或准备生成本整理工具所依赖的上游工作总结。

# 前置条件

开始之前，请确保可以访问 Github、Notion 和 Linear。Notion 和 Linear 应通过 MCP 连接。Github 可以通过 MCP 连接，但如果你有 `gh` CLI 工具的访问权限，也可以使用它。

如果无法访问其中任何一个，请在继续之前提示用户授权。

# 流程

## 步骤 1

提示用户提供一个 Notion 文档链接，该文档是由 `sred-work-summary` 技能生成的上一年度工作总结。

确保：
- 该 Notion 链接指向一个大致符合以下格式的有效文档：

```markdown
# Projects

## [Project Name]
*Summary*: [X] PRs, [X] Notion docs, [X] Linear tickets

### Pull Requests [X]
*[repository name]
[Links to all the PRs]
- [link] - [Merge date]

### Notion Docs [X]
[Links to all the Notion docs]
- [link] - [Creation date]

### Linear Tickets [X]
- [link] - [Creation date]
```

## 步骤 2

对于工作总结中的每个项目，根据 `${CLAUDE_SKILL_ROOT}/references/SRED.md` 中对 SRED 项目的描述进行评估。即查看该项目的相关 Notion 文档和 PR，判断该项目是否属于有效的 SRED 项目。在此过程中应尽量宽泛：能被归类为 SRED 项目的项目越多越好。

输出符合 SRED 模型描述的项目列表和不符合的项目列表。符合 SRED 描述的项目列表称为"可申报 SRED"项目。

确保：
- 工作总结中的所有项目都已被分类为可申报或不可申报。

## 步骤 3

询问用户可申报 SRED 项目列表是否正确。给予用户手动将任何项目分类为可申报或不可申报的选项，并相应调整列表。

## 步骤 4

创建一个名为"SRED 项目描述"的私有 Notion 文档。输出该文档的完整链接。

## 步骤 5

对每个可申报 SRED 项目，执行一系列步骤。

*步骤 1*
创建一个名为"SRED 项目摘要 - <年份> <项目名称>"的私有 Notion 文档，作为步骤 4 中创建的"SRED 项目描述"文档的子文档。该文档应遵循 `${CLAUDE_SKILL_ROOT}/references/project-template.md` 中的模板。

*步骤 2*
填写该文档的"项目描述"和"项目目标"部分。使用这些部分中的 `aside` 区域作为每个部分应包含哪些信息的提示。利用工作总结中收集到的每个项目的所有信息。使用项目的 Notion 文档以及你自己的推理来填写这些部分。

确保：
- 项目描述不超过 100 个词。
- 项目目标不超过 100 个词。

*步骤 3*
向用户提供该项目"SRED 项目摘要"文档的完整 Notion 链接，并要求他们在继续之前进行审查。根据用户要求进行任何修改。

*步骤 4*
每个项目将有一个或多个"技术不确定性"（Uncertainty）。技术不确定性由以下问题定义：
- 我们当时没有答案的挑战或问题是什么？
- 是否有现有技术可以作为解决问题的基础？
- 如果没有，为什么？

审查项目的所有 Notion 文档、Github PR 和 Linear 工单。确定项目的技术不确定性并向用户展示。询问用户这些是否正确或需要调整。

确保：
- 每个技术不确定性的描述仅需几句话。

*步骤 5*
将技术不确定性添加到项目摘要 Notion 文档的"技术不确定性"部分。

确保：
- 技术不确定性的描述仅需几句话。

*步骤 6*
对于上面发现的每个技术不确定性，使用 Notion 文档、Github PR 和 Linear 工单查找为解决该不确定性所做的任何实验或尝试。在该技术不确定性的"实验"部分中为每个实验创建一个要点列表。在"结果 / 经验 / 成功"部分中列出实验的结果以及得出的经验或结论。对于引用的任何 Notion 文档、Github PR 或 Linear 工单，将该资源的链接放入技术不确定性的"不确定性相关文档和链接"部分。

确保：
- 每个实验仅一个要点
- 每个结果/经验/成功仅一个要点

*步骤 7*
获取工作总结中找到的该项目的所有链接，对于未作为技术不确定性一部分链接的链接，将其包含在项目摘要的"项目文档和链接"部分。

确保：
- 提供所有具体链接的列表，而不是摘要或 Github 通知的通用链接。
- 检查每个链接是否与项目及其技术不确定性直接相关。

*步骤 8*
再次向用户提供项目摘要文档的链接，并要求他们在进入下一个可申报 SRED 项目之前进行审查。提醒用户填写文档的"参与者"部分。

## 步骤 6

提供"SRED 项目描述"Notion 文档的链接。

## 示例

工作总结示例：https://www.notion.so/sentry/SRED-Work-Summary-2026-30a8b10e4b5d81f5bc8df3553da55220

## 参考资料

关于什么构成项目以及如何组织的摘要：`${CLAUDE_SKILL_ROOT}/references/SRED.md`
特定项目的 Notion 模板：`${CLAUDE_SKILL_ROOT}/references/project-template.md`

## 资源

SRED 项目的完整文档：https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
