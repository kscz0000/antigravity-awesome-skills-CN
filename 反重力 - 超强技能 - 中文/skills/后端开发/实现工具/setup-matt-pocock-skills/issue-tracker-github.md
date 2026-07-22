# Issue 跟踪器：GitHub

本仓库的 Issue 和 PRD 存放在 GitHub Issues 中。所有操作使用 `gh` CLI。

## 约定

- **创建 Issue**：`gh issue create --title "..." --body "..."`。多行正文使用 heredoc。
- **读取 Issue**：`gh issue view <number> --comments`，通过 `jq` 过滤评论，同时获取标签。
- **列出 Issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合适当的 `--label` 和 `--state` 过滤器。
- **评论 Issue**：`gh issue comment <number> --body "..."`
- **添加/移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

从 `git remote -v` 推断仓库 — 在克隆内运行时 `gh` 会自动处理。

## Pull Request 作为分流渠道

**PR 作为请求渠道：否。** _(如果本仓库将外部 PR 视为功能请求，设为 `yes`；`/triage` 会读取此标志。)_

设为 `yes` 时，PR 使用与 Issue 相同的标签和状态，使用 `gh pr` 的等价命令：

- **读取 PR**：`gh pr view <number> --comments` 和 `gh pr diff <number>` 获取差异。
- **列出待分流的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，然后仅保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的记录（排除 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论/标签/关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的 Issue 和 PR 共享同一编号空间，因此裸 `#42` 可能是其中任一 — 用 `gh pr view 42` 尝试，回退到 `gh issue view 42`。

## 当技能说"发布到 Issue 跟踪器"时

创建一个 GitHub Issue。

## 当技能说"获取相关工单"时

运行 `gh issue view <number> --comments`。
