---
name: faf-go
description: 引导式访谈达成 Gold Code（100% AI 就绪度）。在帮助用户通过提问完善 .faf 文件时使用。借助 Claude Code 的 AskUserQuestion 实现无缝集成。只需输入 /faf-go 并回答问题直至完成。触发词：faf、Gold Code、100%、AskUserQuestion、引导式访谈、.faf 文件、faf-cli、CLAUDE.md。
risk: unknown
source: https://github.com/Wolfe-Jam/faf-skills/tree/main/skills/faf-go
source_repo: Wolfe-Jam/faf-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/Wolfe-Jam/faf-skills/blob/main/LICENSE
---

# FAF Go — 通往 100% ✪ 的引导之路

**"只需输入 /faf-go，回答问题直至完成。目标 100%。"**

`.faf` 是 **IANA 注册的上下文格式**（`application/vnd.faf+yaml`）——一个由 *你拥有* 的、类型化、可移植的文件，可被任何 AI 读取。**faf-cli 基于 21 个槽位打分**；你的 `app_type` 决定哪些槽位为 *active*，**100% ✪ = 每个 active 槽位都已填写**。本技能就是带您达成该目标的引导式访谈：AI 先填入它能检测到的内容，然后通过 Claude Code 的 AskUserQuestion 仅就那些无法获取的空白向您提问。

## 何时使用本技能

在以下情况触发：
- 用户希望提升其 .faf 分数
- 用户提及 "Gold Code" 或 "100%"
- 用户的项目上下文不完整
- 在 `faf init` 之后，用于补齐缺失字段
- 用户说 "帮我处理一下我的 .faf"

## 与 Claude Code 的集成

FAF Go 是为 Claude Code 量身打造的：
- **AskUserQuestion** - Claude Code 原生的提问界面
- **multiSelect: true** - 支持多选答案（例如 "pytest + WJTTC"）
- **TodoWrite** - 在访谈过程中追踪进度
- **结构化输出** - Claude Code 能理解的 JSON
- **双向同步** - 答案同时流向 .faf 和 CLAUDE.md

### multiSelect 支持

部分问题允许多选：
- `stack.testing` → "pytest + WJTTC"
- `stack.cicd` → "GitHub Actions + Cloud Build"
- `stack.frontend` → "React + Tailwind"
- `human_context.who` → "Developers + AI agents"

当 `multiSelect: true` 时，用户可以勾选 2 个或更多选项。结果以 " + " 连接。

## 工作流

### 步骤 1：检查当前状态

运行 faf score 来了解当前位置：

```bash
faf score --verbose
```

或者获取结构化数据以供程序化使用：

```bash
faf score --json
```

`--json` 会返回分数以及逐槽位明细——其中空槽位就是访谈要问的内容（优先级顺序见步骤 2）。

### 步骤 2：使用 AskUserQuestion 进行提问

针对每个缺失字段，使用 Claude Code 的 AskUserQuestion 工具：

**优先级顺序（影响力从高到低）：**
1. `project.goal` - 这个项目是做什么的？
2. `human_context.why` - 它为什么存在？
3. `human_context.who` - 谁会使用它？
4. `human_context.what` - 它解决什么问题？
5. `project.main_language` - 主要编程语言
6. `stack.database` - 数据库选型
7. `stack.hosting` - 部署在哪里？
8. `stack.frontend` - 前端框架
9. `stack.backend` - 后端框架
10. `human_context.where` - 环境
11. `human_context.when` - 时间线/阶段
12. `human_context.how` - 项目是如何构建的（从 stack 推导）

### 步骤 3：应用答案

收集完答案后，更新 .faf 文件：

```bash
# 读取当前 .faf
cat project.faf

# 更新字段（使用 Edit 工具）
# 然后验证：
faf score
```

### 步骤 4：庆祝或继续

若分数 >= 100：庆祝达成 Gold Code
若分数 < 100：继续问剩余问题

## AskUserQuestion 的问题模板

### 单选问题（选一个）

#### project.goal
```json
{
  "question": "这个项目是做什么的？（用一句话清晰描述）",
  "header": "目标",
  "multiSelect": false,
  "options": [
    {"label": "我来输入", "description": "我自己描述"},
    {"label": "帮我写", "description": "引导我完成"}
  ]
}
```

#### human_context.why
```json
{
  "question": "这个项目为什么存在？",
  "header": "原因",
  "multiSelect": false,
  "options": [
    {"label": "业务需求", "description": "解决一个业务问题"},
    {"label": "个人项目", "description": "学习或爱好"},
    {"label": "开源贡献", "description": "社区贡献"},
    {"label": "我来解释", "description": "自定义原因"}
  ]
}
```

#### stack.database
```json
{
  "question": "你使用什么数据库？",
  "header": "数据库",
  "multiSelect": false,
  "options": [
    {"label": "PostgreSQL", "description": "关系型数据库"},
    {"label": "MongoDB", "description": "文档型数据库"},
    {"label": "SQLite", "description": "文件型数据库"},
    {"label": "不使用", "description": "无数据库"}
  ]
}
```

#### stack.hosting
```json
{
  "question": "该项目部署在哪里？",
  "header": "托管",
  "multiSelect": false,
  "options": [
    {"label": "Vercel", "description": "前端/无服务器"},
    {"label": "AWS", "description": "亚马逊云服务"},
    {"label": "仅本地", "description": "尚未部署"},
    {"label": "其他", "description": "其他平台"}
  ]
}
```

### 多选问题（可多选，用 " + " 连接）

#### stack.testing
```json
{
  "question": "你使用哪些测试工具/方法？",
  "header": "测试",
  "multiSelect": true,
  "options": [
    {"label": "pytest", "description": "Python 测试框架"},
    {"label": "Jest", "description": "JavaScript 测试"},
    {"label": "Vitest", "description": "Vite 原生测试"},
    {"label": "WJTTC", "description": "锦标赛方法论（第二层）"}
  ]
}
```
**结果格式：** `pytest + WJTTC`（业界标准在前，WJTTC 在后）

**排序：** 同时选中时，业界标准测试在前：
- `pytest + WJTTC`（而非 `WJTTC + pytest`）
- WJTTC 也可以独立运行

#### stack.cicd
```json
{
  "question": "你使用哪些 CI/CD 工具？",
  "header": "CI/CD",
  "multiSelect": true,
  "options": [
    {"label": "GitHub Actions", "description": "GitHub 原生 CI/CD"},
    {"label": "Cloud Build", "description": "Google Cloud CI/CD"},
    {"label": "CircleCI", "description": "CircleCI 流水线"},
    {"label": "不使用", "description": "暂无 CI/CD"}
  ]
}
```
**结果格式：** `GitHub Actions + Cloud Build`

#### stack.frontend
```json
{
  "question": "你使用哪些前端技术？",
  "header": "前端",
  "multiSelect": true,
  "options": [
    {"label": "React", "description": "React 框架"},
    {"label": "Next.js", "description": "React 元框架"},
    {"label": "Svelte", "description": "Svelte 框架"},
    {"label": "无/仅 API", "description": "无前端"}
  ]
}
```

#### human_context.who
```json
{
  "question": "谁会使用这个项目？",
  "header": "用户",
  "multiSelect": true,
  "options": [
    {"label": "开发者", "description": "软件开发人员"},
    {"label": "终端用户", "description": "非技术用户"},
    {"label": "AI 智能体", "description": "Claude、Gemini 等"},
    {"label": "内部团队", "description": "仅限本团队"}
  ]
}
```
**结果格式：** `Developers + AI agents`

### 处理多选答案

当用户选择多个选项时，用 " + " 连接：

```python
# 示例：用户选择了 ["pytest", "WJTTC"]
selected = ["pytest", "WJTTC"]
value = " + ".join(selected)  # "pytest + WJTTC"
```

这样在 .faf 文件中就能产生可读、易扫视的值：
```yaml
stack:
  testing: pytest + WJTTC
  cicd: GitHub Actions + Cloud Build
```

## 示例会话

```
User: /faf-go

Claude: 让我先检查你当前的 .faf 状态。

[Runs: faf score --verbose]

你的分数是 45%。让我们一起把它提到 Gold Code！

[Uses AskUserQuestion for project.goal]

User: [选择选项或输入自定义内容]

Claude: 很好！接下来记录这个项目为什么存在。

[Uses AskUserQuestion for human_context.why]

... 一直持续直到 100% ...

Claude: ✪ 达成 GOLD CODE！
你的 AI 现在拥有完整上下文，可发挥锦标赛级表现。
```

## TodoWrite 集成

使用 todos 跟踪进度：

```javascript
[
  {"content": "回答 project.goal 问题", "status": "completed"},
  {"content": "回答 human_context.why 问题", "status": "in_progress"},
  {"content": "回答 stack.database 问题", "status": "pending"},
  {"content": "验证已达成 Gold Code", "status": "pending"}
]
```

## CLI 回退方案

在 Claude Code 之外，可以用 CLI 自带的交互式访谈到达同样的终点：

```bash
faf go            # 交互式终端访谈（--resume 续接上次会话）
```

本技能是该访谈的 **Claude 原生**版本——用 AskUserQuestion 替代终端提示。如需结构化、程序化的数据，请使用 `faf score --json`。

## 成功指标

- 用户达到 100% 分数
- 所有必填字段都填入了有意义的内容
- 没有占位符值（在不合适的地方出现 TBD、Unknown、None）
- 用户理解每个字段的用途

## 完成时

当达成 100% ✪ 时：

```
✪ 100% — Gold Code

project.faf: 完成
CLAUDE.md:   已从 .faf 同步
```

可选地运行 `faf sync`，从 .faf 生成 CLAUDE.md / AGENTS.md。此后你的 AI 在每次会话开始时都将拥有完整的项目上下文。

## 相关技能

- **faf-context** — 构建者的快速上手：把 AI 需要的素材交给它，快速冲 100%
- **faf-wizard** — 自动化一键为任何项目生成 .faf
- **faf-expert** — 精通格式：评分机制、MCP 配置、双向同步、完整的 21 槽位模型

---

> .faf 是格式。project.faf 是文件。
> 100% ✪ AI 就绪度是结果。

---

*MIT · FAF 技能家族成员（faf-context · faf-wizard · faf-expert）。Claude Code 原生。*

## 局限性

- 仅在任务与上游来源和本地项目上下文明确匹配时使用本技能。
- 在应用任何变更之前，请验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要将示例视为针对特定环境的测试、安全审查或用户对破坏性/高成本操作的批准的替代品。