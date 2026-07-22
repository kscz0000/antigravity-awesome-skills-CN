---
name: github
description: "使用 `gh` CLI 处理 issues、pull requests、Actions 运行和 GitHub API 查询。触发词：gh CLI、GitHub CLI、gh issue、gh pr、gh run、gh api、GitHub 命令行、GitHub issue、GitHub PR、GitHub Actions、CI 失败、工作流运行"
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# GitHub 技能

使用 `gh` CLI 与 GitHub 交互。当不在 git 目录中时，始终指定 `--repo owner/repo`，或直接使用 URL。

## 何时使用

- 当用户询问 GitHub issues、pull requests、工作流运行或 CI 失败时。
- 当你需要从命令行使用 `gh issue`、`gh pr`、`gh run` 或 `gh api` 时。

## Pull Requests

检查 PR 上的 CI 状态：
```bash
gh pr checks 55 --repo owner/repo
```

列出最近的工作流运行：
```bash
gh run list --repo owner/repo --limit 10
```

查看运行并查看哪些步骤失败：
```bash
gh run view <run-id> --repo owner/repo
```

仅查看失败步骤的日志：
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

### 调试 CI 失败

按照以下顺序调查失败的 CI 运行：

1. **检查 PR 状态** — 确定哪些检查失败：
   ```bash
   gh pr checks 55 --repo owner/repo
   ```
2. **列出最近的运行** — 找到相关的运行 ID：
   ```bash
   gh run list --repo owner/repo --limit 10
   ```
3. **查看失败的运行** — 查看哪些作业和步骤失败：
   ```bash
   gh run view <run-id> --repo owner/repo
   ```
4. **获取失败日志** — 获取失败步骤的详细输出：
   ```bash
   gh run view <run-id> --repo owner/repo --log-failed
   ```

## 高级查询 API

`gh api` 命令用于访问其他子命令无法获取的数据。

获取具有特定字段的 PR：
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON 输出

大多数命令支持 `--json` 进行结构化输出。你可以使用 `--jq` 进行过滤：

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

## 限制

- 仅当任务明显符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
