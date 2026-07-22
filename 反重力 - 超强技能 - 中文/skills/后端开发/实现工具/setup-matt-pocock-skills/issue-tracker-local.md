# Issue 跟踪器：本地 Markdown

本仓库的 Issue 和 PRD 以 Markdown 文件形式存放在 `.scratch/` 中。

## 约定

- 每个功能一个目录：`.scratch/<feature-slug>/`
- PRD 位于 `.scratch/<feature-slug>/PRD.md`
- 实现 Issue 位于 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 开始编号
- 分流状态记录在每个 Issue 文件顶部附近的 `Status:` 行（角色字符串参见 `triage-labels.md`）
- 评论和对话历史追加到文件底部 `## Comments` 标题下

## 当技能说"发布到 Issue 跟踪器"时

在 `.scratch/<feature-slug>/` 下创建新文件（如需要则创建目录）。

## 当技能说"获取相关工单"时

读取引用路径处的文件。用户通常会直接传入路径或 Issue 编号。
