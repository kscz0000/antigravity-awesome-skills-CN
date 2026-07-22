---
name: issues
description: 与 GitHub issues 交互——创建、列出和查看 issues。触发词：GitHub issues、创建 issue、列出 issues、查看 issue、issue 管理、gh issue。
allowed-tools: Bash(gh *)
risk: unknown
source: community
metadata:
  author: Shpigford
  version: "1.0"
---

与 GitHub issues 交互——创建、列出和查看 issues。

## 何时使用
- 用户想要创建、列出、检查或以其他方式处理 GitHub issues。
- 任务涉及通过 GitHub CLI 工作流进行 issue 接收或仓库 issue 管理。
- 需要引导式 issue 流程，在运行命令前收集标题、描述和操作选择。

## 说明

此命令帮助你使用 `gh` CLI 处理 GitHub issues。

### 步骤 1：确定操作

使用 AskUserQuestion 询问用户想要做什么：

**问题：**
- question: "你想对 GitHub issues 做什么操作？"
- header: "操作"
- multiSelect: false
- options:
  - label: "创建新 issue"
    description: "打开一个新 issue，包含标题、正文和可选标签"
  - label: "列出 issues"
    description: "查看当前仓库中的开放 issues"
  - label: "查看 issue"
    description: "按编号查看特定 issue 的详情"

---

## 如果选择"创建新 issue"：

### 步骤 2a：获取 Issue 标题

使用 AskUserQuestion 获取 issue 标题：

**问题：**
- question: "这个 issue 的简短、可扫描的标题是什么？保持简洁（最多 5-10 个词）——详细信息放在正文中。（使用 'Other' 输入你的标题）"
- header: "标题"
- multiSelect: false
- options:
  - label: "我来输入标题"
    description: "输入简洁的标题，如 'Login button unresponsive' 或 'Add dark mode support'"

**标题指南：**
- 保持标题简短且易于扫描（最多 5-10 个词）
- 好的示例："Fix broken password reset flow"
- 不好的示例："When I try to reset my password and click the button nothing happens and I get an error"
- 描述/正文才是放详细信息的地方，不是标题

如果用户提供了一个很长的标题，帮助他们缩短它，并将详细信息移到正文中。

### 步骤 3a：获取 Issue 正文

使用 AskUserQuestion 收集 issue 正文内容：

**问题 1 - Issue 类型上下文：**
- question: "这是什么类型的 issue？"
- header: "类型"
- multiSelect: false
- options:
  - label: "Bug"
    description: "需要修复的损坏问题"
  - label: "Enhancement"
    description: "对现有功能的改进"
  - label: "New feature"
    description: "全新功能"
  - label: "Task"
    description: "常规工作项或杂务"

**问题 2 - 描述：**
- question: "现在提供完整详情。在这里解释上下文、背景和标题放不下的具体细节。（使用 'Other' 输入你的描述）"
- header: "描述"
- multiSelect: false
- options:
  - label: "我来详细描述"
    description: "提供上下文、步骤、示例和任何相关信息"

用户将选择 "Other" 来提供完整描述。

**描述指南：**
- 这里放所有详细信息——要详尽
- 包含上下文：你在做什么，背景是什么？
- 包含具体细节：错误消息、URL、版本等
- 这里细节越多越好——与标题应简洁不同

**问题 3 - 对于 bug，询问复现步骤：**
如果 issue 类型是 "Bug"，使用 AskUserQuestion：

- question: "你能提供复现这个 bug 的步骤吗？（使用 'Other' 输入步骤）"
- header: "复现步骤"
- multiSelect: false
- options:
  - label: "提供步骤"
    description: "我将描述如何复现该问题"
  - label: "无法复现"
    description: "该 bug 是间歇性的或难以复现"

**问题 4 - 预期行为 vs 实际行为（对于 bug）：**
如果 issue 类型是 "Bug"，使用 AskUserQuestion：

- question: "你预期发生什么 vs 实际发生了什么？（使用 'Other' 描述）"
- header: "行为"
- multiSelect: false
- options:
  - label: "描述行为"
    description: "我将解释预期行为 vs 实际行为"

### 步骤 4a：获取标签（可选）

使用 AskUserQuestion 选择标签：

- question: "我们应该添加哪些标签？（如果有）"
- header: "标签"
- multiSelect: true
- options:
  - label: "bug"
    description: "某些东西不工作"
  - label: "enhancement"
    description: "新功能或请求"
  - label: "documentation"
    description: "文档改进"
  - label: "good first issue"
    description: "适合新手"

### 步骤 5a：创建 Issue

根据类型构建 issue 正文：

**对于 Bug 报告：**
```
## Description
[用户的描述]

## Steps to Reproduce
[用户的复现步骤或 "Not easily reproducible"]

## Expected Behavior
[应该发生什么]

## Actual Behavior
[实际发生了什么]
```

**对于功能请求/Enhancements：**
```
## Description
[用户的描述]

## Use Case
[为什么这会有用]
```

**对于 Tasks/其他：**
```
## Description
[用户的描述]
```

运行 gh 命令创建 issue：
```bash
gh issue create --title "[title]" --body "[constructed body]" --label "[labels]"
```

向用户报告 issue URL。

---

## 如果选择"列出 issues"：

### 步骤 2b：筛选选项

使用 AskUserQuestion 确定筛选方式：

- question: "你想如何筛选 issues？"
- header: "筛选"
- multiSelect: false
- options:
  - label: "所有开放 issues"
    description: "显示所有开放 issues"
  - label: "分配给我的"
    description: "分配给当前用户的 issues"
  - label: "我创建的"
    description: "我创建的 issues"
  - label: "按特定标签"
    description: "按标签筛选"

如果选择"按特定标签"，使用 AskUserQuestion：

- question: "按哪个标签筛选？（使用 'Other' 输入自定义标签）"
- header: "标签"
- multiSelect: false
- options:
  - label: "bug"
    description: "Bug 报告"
  - label: "enhancement"
    description: "功能请求"
  - label: "documentation"
    description: "文档 issues"

### 步骤 3b：列出 Issues

运行相应的 gh 命令：
- 所有开放：`gh issue list`
- 分配给我：`gh issue list --assignee @me`
- 我创建的：`gh issue list --author @me`
- 按标签：`gh issue list --label "[label]""`

以清晰的格式显示结果。

---

## 如果选择"查看 issue"：

### 步骤 2c：获取 Issue 编号

使用 AskUserQuestion：

- question: "你想查看哪个 issue 编号？（使用 'Other' 输入编号）"
- header: "Issue #"
- multiSelect: false
- options:
  - label: "输入 issue 编号"
    description: "我将输入 issue 编号"

### 步骤 3c：查看 Issue

运行：`gh issue view [number]`

显示 issue 详情，包括标题、正文、标签、指派人和评论。

---

## 错误处理

如果 `gh` 命令失败：
1. 检查用户是否已认证：`gh auth status`
2. 如果未认证，通知用户运行 `gh auth login`
3. 检查是否在有 GitHub 远程的 git 仓库中
4. 向用户报告具体错误消息

## 重要说明

- **标题应简洁**（5-10 个词）——如果用户提供了长标题，帮助缩短并将详细信息移到正文
- **正文应详细**——鼓励用户提供详尽的上下文、步骤和具体细节
- 始终通过显示 URL 确认 issue 创建成功
- 对于 issue 正文，保留用户的格式和换行
- 如果用户提供的信息很少，也没关系——用他们提供的内容创建 issue
- 使用 HEREDOC 处理正文以保留格式：
  ```bash
  gh issue create --title "Title" --body "$(cat <<'EOF'
  Body content here
  EOF
  )"
  ```

## 限制
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
