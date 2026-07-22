# Issue 跟踪器：GitLab

本仓库的 Issue 和 PRD 存放在 GitLab Issues 中。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建 Issue**：`glab issue create --title "..." --description "..."`。多行描述使用 heredoc。传入 `--description -` 打开编辑器。
- **读取 Issue**：`glab issue view <number> --comments`。使用 `-F json` 获取机器可读输出。
- **列出 Issue**：`glab issue list -F json`，配合适当的 `--label` 过滤器。
- **评论 Issue**：`glab issue note <number> --message "..."`。GitLab 将评论称为"notes"。
- **添加/移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可用逗号分隔或重复标志。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，因此先用 `glab issue note <number> --message "..."` 发表说明，然后关闭。
- **合并请求**：GitLab 将 PR 称为"合并请求"。使用 `glab mr create`、`glab mr view`、`glab mr note` 等 — 与 `gh pr ...` 形状相同，用 `mr` 替代 `pr`，用 `note`/`--message` 替代 `comment`/`--body`。

从 `git remote -v` 推断仓库 — 在克隆内运行时 `glab` 会自动处理。

## 合并请求作为分流渠道

**MR 作为请求渠道：否。** _(如果本仓库将外部合并请求视为功能请求，设为 `yes`；`/triage` 会读取此标志。)_

设为 `yes` 时，MR 使用与 Issue 相同的标签和状态，使用 `glab mr` 的等价命令：

- **读取 MR**：`glab mr view <number> --comments` 和 `glab mr diff <number>` 获取差异。
- **列出待分流的外部 MR**：`glab mr list -F json`，然后仅保留作者非项目成员/拥有者的 MR（贡献者的 MR，而非维护者进行中的工作）。
- **评论/标签/关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

与 GitHub 不同，GitLab 对 Issue 和 MR 分别编号，因此 `#42` 在明确所指对象后是无歧义的。

## 当技能说"发布到 Issue 跟踪器"时

创建一个 GitLab Issue。

## 当技能说"获取相关工单"时

运行 `glab issue view <number> --comments`。
