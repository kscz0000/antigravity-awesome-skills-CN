---
name: pr-writer
description: "按照 Sentry 工程实践创建 Pull Request。当用户要求'创建 PR''写 PR 描述''提交 pull request'时使用。"
risk: unknown
source: community
---

# PR 编写器

按照 Sentry 的工程实践创建 Pull Request。

**前置条件**：GitHub CLI（`gh`）已认证并可用。

## 何时使用

- 准备开启 Pull Request，需要基于已提交分支 diff 生成结构化描述。
- 希望 PR 正文记录变更内容、变更原因以及审查者所需的上下文。
- 使用 GitHub CLI，需要可重复的 PR 编写流程而非临时撰写描述。

## 前置准备

创建 PR 前，确保所有变更已提交。若有未提交变更，先运行 `sentry-skills:commit` 技能进行提交。

```bash
# 检查未提交变更
git status --porcelain
```

若输出显示任何未提交变更（已修改、已添加或应包含的未跟踪文件），在继续之前调用 `sentry-skills:commit` 技能。

## 流程

### 步骤 1：验证分支状态

```bash
# 检测默认分支 — 记录输出供后续命令使用
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

```bash
# 检查当前分支和状态（将上方检测到的分支名替换 BASE）
git status
git log BASE..HEAD --oneline
```

确保：
- 所有变更已提交
- 分支与远程保持同步
- 如需要，变更已 rebase 到基础分支

### 步骤 2：分析变更

审查将包含在 PR 中的内容：

```bash
# 查看 PR 中的所有提交（将检测到的分支名替换 BASE）
git log BASE..HEAD

# 查看完整 diff
git diff BASE...HEAD
```

在编写描述之前，理解所有变更的范围和目的。

### 步骤 3：编写 PR 描述

使用以下结构编写 PR 描述（忽略仓库的 PR 模板）：

```markdown
<PR 做了什么的简要描述>

<为什么做这些变更 — 动机>

<考虑过的替代方案（如有）>

<审查者需要的额外上下文>
```

**不要包含：**
- "测试计划"章节
- 测试步骤的复选框列表
- diff 的冗余摘要

**要包含：**
- 清晰说明变更内容和原因
- 相关 issue 或 ticket 的链接
- 代码中不明显的上下文
- 需要仔细审查的特定区域说明

### 步骤 4：创建 PR

```bash
gh pr create --draft --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
<描述正文>
EOF
)"
```

**标题格式**遵循提交规范：
- `feat(scope): 添加新功能`
- `fix(scope): 修复 bug`
- `ref: 重构某部分`

## PR 描述示例

### 功能 PR

```markdown
为告警通知添加 Slack 线程回复

当告警更新或解决时，现在会在原始 Slack 线程中发布回复，
而不是创建新消息。这使相关通知保持分组，减少频道噪音。

之前考虑过编辑原始消息，但线程方式更好地保留了事件时间线，
且当原始消息超过 Slack 编辑窗口时仍然有效。

Refs SENTRY-1234
```

### Bug 修复 PR

```markdown
处理用户 API 端点中的 null 响应

用户端点对软删除账户可能返回 null，导致访问用户属性时
仪表盘崩溃。添加 null 检查并返回正确的 404 响应。

在调查 SENTRY-5678 时发现。

Fixes SENTRY-5678
```

### 重构 PR

```markdown
将验证逻辑提取到共享模块

将告警、issues 和 projects 端点中的重复验证代码移至
共享验证器类。行为无变化。

这为在 SENTRY-9999 中添加新验证规则做准备，
避免在端点间重复逻辑。
```

## Issue 引用

在 PR 正文中引用 issue：

| 语法 | 效果 |
|------|------|
| `Fixes #1234` | 合并时关闭 GitHub issue |
| `Fixes SENTRY-1234` | 关闭 Sentry issue |
| `Refs GH-1234` | 链接但不关闭 |
| `Refs LINEAR-ABC-123` | 链接 Linear issue |

## 指导原则

- **一个 PR 对应一个功能/修复** — 不要捆绑无关变更
- **保持 PR 可审查** — 较小的 PR 能获得更快、更好的审查
- **解释原因** — 代码展示做了什么；描述解释为什么
- **尽早标记 WIP** — 使用 draft PR 获取早期反馈

## 编辑已有 PR

创建后需要更新 PR 时，使用 `gh api` 而非 `gh pr edit`：

```bash
# 更新 PR 描述
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER -f body="$(cat <<'EOF'
更新后的描述
EOF
)"

# 更新 PR 标题
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER -f title='new: 新标题'

# 同时更新
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER \
  -f title='new: 标题' \
  -f body='新描述'
```

注意：`gh pr edit` 因 GitHub Projects (classic) 弃用目前存在问题。

## 参考资料

- [Sentry 代码审查指南](https://develop.sentry.dev/engineering-practices/code-review/)
- [Sentry 提交消息规范](https://develop.sentry.dev/engineering-practices/commit-messages/)

## 局限性

- 仅在任务明确匹配上述范围时使用本技能。
- 不要把输出视为环境专属验证、测试或专家审查的替代品。
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清。
