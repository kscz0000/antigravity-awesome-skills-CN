---
name: sred-work-summary
description: 回溯过去一年的工作，创建一个 Notion 文档，将相关链接归入项目分组，以便后续作为 SRED 项目进行文档化。触发词：SRED工作总结、年度工作汇总、PR归档、项目分组、SRED准备、工作回顾
risk: unknown
source: community
---

# SRED 工作总结

收集指定年份内一个人完成的所有 Github PR、Notion 文档和 Linear 工单。将所有这些链接归入项目分组。将所有内容放入一个私有 Notion 文档中，并返回该文档的链接。

## 适用场景
- 你需要将一年的 PR、Notion 文档和 Linear 工单收集到项目分组中，为 SRED 做准备。
- 任务是在编写各个 SRED 项目描述之前，构建上游的 Notion 工作总结。
- 你需要一个跨 GitHub、Notion 和 Linear 的可重复收集工作流，覆盖固定时间窗口。

## 前置条件

开始之前，请确保可以访问 Github、Notion 和 Linear。Notion 和 Linear 应通过 MCP 连接。Github 可以通过 MCP 连接，但如果你有 `gh` CLI 工具的访问权限，也可以使用它。

如果无法访问其中任何一个，请在继续之前提示用户授权。

## 流程

### 步骤 1

```bash
# 获取当前年份
date +%Y
```

此命令的输出是当前年份。
当前年份减一即为上一年。

### 步骤 2

从用户处收集所有必需信息：

*Github 用户名*：用户的 github 用户名是什么？

*Github 仓库*：应该在哪些 Github 仓库中搜索 PR？

用户可以指定逗号分隔的列表，或提供包含仓库的目录。在第二种情况下，在指定目录中使用以下命令：

```bash
# 查找 github 仓库
find . -maxdepth 2 -name ".git" -type d | sed 's/\/.git$//' | sort
```

确保：
- 列出的所有仓库都在 `getsentry` Github 组织中。

此输出在下文中称为"用户仓库"。

*事故文档*：询问用户是否要包含事故文档。

答案为是或否。如果答案为否，将在后续搜索中排除某些文档。

*其他用户*：询问是否有其他用户可能创建了 Notion 文档。

这应该是一个逗号分隔的名称列表。记住为"其他用户"。

### 步骤 3

创建一个名为"SRED 工作总结 [当前年份]"的私有 Notion 文档。该文档在下文中称为"工作总结"。

如果同名文档已存在，通知用户重命名现有文档并停止执行。

确保：
- 如果工作总结已存在，停止执行。

### 步骤 4

时间窗口为上一年的 2 月 1 日至当年的 1 月 31 日。
查找在该时间窗口内由给定 github 用户名在用户仓库中创建的所有 Github PR。
如果用户不想包含事故文档，则忽略标题或描述中包含 `INC-X`、`inc-X` 的 Github PR。
使用 Github MCP 或 `gh` 命令完成此操作。

查找在该时间窗口内用户创建的所有 Notion 文档。
如果用户不想包含事故文档，则忽略标题中包含 `INC-XXXX` 的 Notion 文档。
使用 Notion MCP 完成此操作。

查找在该时间窗口内分配给用户的所有 Linear 工单。
如果用户不想包含事故文档，则忽略标题中包含 `INC-XXXX` 的 Linear 工单。
使用 Linear MCP 完成此操作。

确保：
- 所有 Github PR 都是在时间窗口内创建或合并的，且由用户发起。
- 所有 Notion 文档都是在时间窗口内创建的，且由用户创建。
- 所有 Linear 工单都是在时间窗口内开启或完成的，且完成时分配给该用户。

### 步骤 5

对于步骤 4 中找到的每个 Github PR、Notion 文档和 Linear 工单，将链接放入步骤 3 中创建的私有文档。

确保：
- 工作总结中有所有 Github PR 的链接
- 工作总结中有所有 Notion 文档的链接
- 工作总结中有所有 Linear 工单的链接
- 不要截断链接列表。不要使用"...还有 75 个"之类的省略。确保所有 Github PR、Notion 文档和 Linear 工单的完整集合在文档中可见。

### 步骤 6

运用你的智能将工作总结文档中所有的 Github、Notion 和 Linear 工单链接归入项目分组。该文档的格式如下所示。

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

对于 Github PR，使用 PR 的标题和描述进行分组。
对于 Notion 文档，使用完整文档进行分组。
对于 Linear 工单，使用工单的标题和描述进行分组。

确保：
- 文件中的所有链接都已分配到某个项目。
- 文件遵循上述指定的格式。
- 不要截断链接列表。不要使用"...还有 75 个"之类的省略。确保所有 Github PR、Notion 文档和 Linear 工单的完整集合在文档中可见。

### 步骤 7

搜索"其他用户"创建的 Notion 文档。将与工作总结中项目相关的文档链接添加到工作总结的相应项目中。

### 步骤 8

向用户返回工作总结 Notion 文档的链接。

确保：
- 最终输出中包含实际的 Notion 文档链接。

## 资源

这是 2025 年的工作总结文档示例：https://www.notion.so/sentry/Work-Summary-Feb-2025-Jan-2026-3068b10e4b5d81d3a40cfa6ad3fe1078?source=copy_link

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
