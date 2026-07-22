---
name: improve-codebase-architecture
description: 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，然后逐一深入你选中的那一个。触发词：改善架构、架构重构、深化模块、代码库架构、重构机会、紧耦合合并、可测试性、AI导航、架构审查、深度模块、浅模块深化、seam设计、删除测试、架构摩擦
disable-model-invocation: true
category: "development"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - engineering
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 改善代码库架构

## 何时使用

当工作流匹配以下用户请求时使用：扫描代码库寻找深化机会，以可视化 HTML 报告呈现，然后逐一深入你选中的那一个。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_

暴露架构摩擦并提出**深化机会**——将浅模块重构为深模块。目标是可测试性和 AI 可导航性。

此命令以项目的领域模型为依据，并建立在共享设计词汇之上：

- 运行 `/codebase-design` 技能获取架构词汇（**module**、**interface**、**depth**、**seam**、**adapter**、**leverage**、**locality**）及其原则（删除测试、"接口即测试面"、"一个 adapter = 假设性 seam，两个 = 真实 seam"）。在每个建议中严格使用这些术语——不要偏移到"component"、"service"、"API"或"boundary"。
- `CONTEXT.md` 中的领域语言为好的 seam 命名；`docs/adr/` 中的 ADR 记录了此命令不应重新审议的决策。

## 流程

### 1. 探索

首先阅读项目的领域词汇表（`CONTEXT.md`）以及你要触及区域中的任何 ADR。

然后使用 Agent 工具并设置 `subagent_type=Explore` 来遍历代码库。不要遵循刻板的启发式规则——有机地探索，记录你感受到摩擦的地方：

- 理解一个概念需要在许多小模块之间跳来跳去的地方在哪里？
- 模块**浅**的地方在哪里——接口几乎和实现一样复杂？
- 纯函数仅为了可测试性被提取出来，但真正的 bug 藏在调用方式中的地方在哪里（缺乏**locality**）？
- 紧耦合的模块在哪里泄漏了它们的 seam？
- 代码库中哪些部分未经测试，或难以通过当前接口进行测试？

对任何你怀疑是浅的东西应用**删除测试**：删除它会集中复杂性，还是仅仅移动它？"是的，集中了"就是你要找的信号。

### 2. 以 HTML 报告呈现候选项

将一个自包含的 HTML 文件写入操作系统临时目录，这样不会在仓库中留下任何东西。从 `$TMPDIR` 解析临时目录，回退到 `/tmp`（Windows 上用 `%TEMP%`），写入 `<tmpdir>/architecture-review-<timestamp>.html`，使每次运行都得到新文件。为用户打开它——Linux 上用 `xdg-open <path>`，macOS 上用 `open <path>`，Windows 上用 `start <path>`——并告诉他们绝对路径。

报告使用 **Tailwind via CDN** 进行布局和样式，使用 **Mermaid via CDN** 绘制图表（当图形/流程/序列能可靠传达结构时）。混合 Mermaid 与手绘 CSS/SVG 视觉元素——当关系是图形结构时（调用图、依赖关系、序列）使用 Mermaid，当你想要更偏向编辑风格的内容时（质量图、剖面图、折叠动画）使用手绘 div/SVG。每个候选项都有一个**前后对比可视化**。注重视觉表现。

对每个候选项，渲染一张卡片，包含：

- **Files**——涉及的文件/模块
- **Problem**——当前架构为何造成摩擦
- **Solution**——用自然语言描述会改变什么
- **Benefits**——用 locality 和 leverage 的术语解释，以及测试将如何改善
- **Before / After diagram**——并排、手绘，展示浅与深
- **Recommendation strength**——`Strong`、`Worth exploring`、`Speculative` 三选一，渲染为徽章

报告末尾以**首推建议**部分收尾：你最应该先处理哪个候选项，以及为什么。

**领域用 CONTEXT.md 词汇，架构用 `/codebase-design` 词汇。** 如果 `CONTEXT.md` 定义了"Order"，就说"the Order intake module"——不是"the FooBarHandler"，也不是"the Order service"。

**ADR 冲突**：如果候选项与现有 ADR 矛盾，仅当摩擦足以值得重新审视该 ADR 时才展示。在卡片中清楚标注（例如一个警告标注：_"contradicts ADR-0007 — but worth reopening because…"_）。不要列出 ADR 禁止的每一个理论性重构。

完整 HTML 脚手架、图表模式和样式指南参见 [HTML-REPORT.md](HTML-REPORT.md)。

不要急于提出接口。文件写好后，询问用户："Which of these would you like to explore?"

### 3. 盘问循环

用户选定候选项后，运行 `/grilling` 技能与他们一起遍历设计树——约束、依赖、深化模块的形状、seam 后面是什么、哪些测试能存活。

副作用在决策结晶时即时发生——运行 `/domain-modeling` 技能以保持领域模型同步更新：

- **用一个 `CONTEXT.md` 中没有的概念为深化模块命名？** 将该术语添加到 `CONTEXT.md`。如果文件不存在则按需创建。
- **在对话中细化了一个模糊术语？** 立即更新 `CONTEXT.md`。
- **用户以一个关键理由拒绝了候选项？** 提供 ADR，措辞为：_"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ 仅在该理由确实会被未来的探索者需要以避免重新建议同一件事时才提供——跳过临时性理由（"现在不值得"）和不言自明的理由。
- **想为深化模块探索替代接口？** 运行 `/codebase-design` 技能并使用其 design-it-twice 并行子代理模式。


## 局限性

- 当工作流指定了上游工具、账户、API 密钥或本地设置时，需要相应条件。
- 未经用户明确批准，不授权执行破坏性、生产环境、付费或外部消息操作。
- 在将生成的产物或建议视为最终结果之前，请对照用户的真实来源进行验证。
