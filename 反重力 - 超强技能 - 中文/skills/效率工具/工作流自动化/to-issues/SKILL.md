---
name: to-issues
description: 将计划、规范或 PRD 按追踪子弹式纵向切片拆分为可在项目 issue 跟踪器上独立领取的 issue。触发词：计划拆分、计划转 issue、创建 issue、工作拆分、纵向切片、追踪子弹、PRD 转 issue、spec 转 issue、实现工单、任务分解。
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

# 转 Issue

## 何时使用

当此工作流匹配用户请求时使用：使用追踪子弹式纵向切片，将计划、规范或 PRD 拆分为可在项目 issue 跟踪器上独立领取的 issue。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_

使用纵向切片（追踪子弹）将计划拆分为可独立领取的 issue。

issue 跟踪器与分流标签词汇表应已提供给你 —— 如果没有，请运行 `/setup-matt-pocock-skills`。

## 流程

### 1. 收集上下文

基于对话上下文中已有的内容开展工作。如果用户将 issue 引用（issue 编号、URL 或路径）作为参数传入，请从 issue 跟踪器获取它并阅读其完整正文和评论。

### 2. 探索代码库（可选）

如果你尚未探索代码库，请进行探索以了解代码的当前状态。issue 标题和描述应使用项目的领域术语词汇，并尊重你所涉及区域的 ADR。

寻找对代码进行预重构（prefactor）的机会，以使实现更轻松。"先让变更易于完成，再完成简单的变更。"

### 3. 起草纵向切片

将计划拆分为 **追踪子弹** issue。每个 issue 都是一条穿过所有集成层的细长纵向切片，而不是某一层的横向切片。

<vertical-slice-rules>

- 每个切片交付一条狭窄但完整的路径，贯穿每一层（schema、API、UI、测试）
- 已完成的切片可单独演示或验证
- 任何预重构应优先完成

</vertical-slice-rules>

### 4. 向用户确认

将建议的拆分以编号列表的形式呈现。对每个切片，展示：

- **标题**：简短的描述性名称
- **被阻塞于**：哪些其他切片（如果有）必须先完成
- **涵盖的用户故事**：该切片所处理的用户故事（如果源材料中有的话）

询问用户：

- 粒度是否合适？（太粗 / 太细）
- 依赖关系是否正确？
- 是否需要进一步合并或拆分切片？

迭代直到用户确认拆分。

### 5. 将 issue 发布到 issue 跟踪器

对每个已批准的切片，在 issue 跟踪器上发布一个新 issue。使用下面的 issue 正文模板。这些 issue 被视为可供 AFK 代理领取，因此除非另有指示，请使用正确的分流标签发布。

按依赖顺序发布 issue（阻塞项优先），以便你可以在"被阻塞于"字段中引用真实的 issue 标识符。

<issue-template>
## 父 issue

对 issue 跟踪器上父 issue 的引用（如果源是已有 issue，则可省略本节）。

## 待构建内容

对该纵向切片的简明描述。描述端到端行为，而非逐层实现。

避免使用具体的文件路径或代码片段——它们很快会过时。例外：如果原型生成的代码片段比文字更精确地表达了某个决策（状态机、reducer、schema、类型形状），请在此处内联，并简要注明它来自原型。裁剪到决策密集的部分——不是可工作的演示，只是重要的片段。

## 验收标准

- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

## 被阻塞于

- 对阻塞工单的引用（如果有）

或"无 - 可立即开始"，如果没有阻塞项。

</issue-template>

不要关闭或修改任何父 issue。


## 局限性

- 当工作流指定时，需要上游工具、账户、API 密钥或本地设置。
- 未经用户明确批准，不会授权破坏性、生产环境、付费或外部消息传递操作。
- 在将生成的工件或建议视为最终结论之前，请根据用户的真实来源进行验证。