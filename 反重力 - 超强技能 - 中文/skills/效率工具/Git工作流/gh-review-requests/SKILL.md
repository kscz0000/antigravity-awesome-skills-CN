---
name: gh-review-requests
description: 获取指定团队被请求审查或团队成员创建的未读 GitHub PR 通知。当用户要求"查找我需要审查的 PR"、"显示我的审查请求"、"什么需要我审查"、"获取 GitHub 审查请求"或"检查团队审查队列"时使用。
allowed-tools: Bash
risk: safe
source: community
---

# GitHub Review Requests

获取未读的 `review_requested` 通知，针对未合并的开放 PR，按 GitHub 团队过滤。

**需要**：GitHub CLI (`gh`) 已认证。

## 何时使用
- 你需要查找特定团队的未读 GitHub PR 审查请求。
- 你想检查哪些开放的 PR 当前需要你或队友的审查。
- 你需要一个过滤后的审查队列，而不是手动浏览 GitHub 通知。

## 步骤 1：识别团队

如果用户未指定团队，询问：

> 我应该按哪个 GitHub 团队过滤？（例如 `streaming-platform`）

接受团队 slug（`streaming-platform`）或显示名称（"Streaming Platform"）—— 在传递给脚本之前转换为小写连字符格式的 slug。

## 步骤 2：运行脚本

```bash
uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_review_requests.py --org getsentry --teams <team-slug>
```

要按多个团队过滤，传递逗号分隔的列表：

```bash
uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_review_requests.py --org getsentry --teams <team slugs>
```

### 脚本输出

```json
{
  "total": 3,
  "prs": [
    {
      "notification_id": "12345",
      "title": "feat(kafka): add workflow to restart a broker",
      "url": "https://github.com/getsentry/ops/pull/19144",
      "repo": "getsentry/ops",
      "pr_number": 19144,
      "author": "bmckerry",
      "reasons": ["opened by: bmckerry"]
    }
  ]
}
```

`reasons` 将包含以下一个或两个：
- `"review requested from: <Team Name>"` — 团队是被请求的审查者
- `"opened by: <login>"` — PR 作者团队成员

## 步骤 3：展示结果

以 markdown 表格形式展示结果，包含完整 URL：

| # | Title | URL | Reason |
|---|-------|-----|--------|
| 1 | feat(kafka): add workflow to restart a broker | https://github.com/getsentry/ops/pull/19144 | opened by: evanh |

如果 `total` 为 0，说："未找到该团队的未读审查请求。"

## 备用方案

如果脚本失败，手动运行：

```bash
gh api notifications --paginate
```

然后对每个 `review_requested` 通知，检查：
- `gh api repos/{repo}/pulls/{number}` — 如果 `state == "closed"` 或 `merged_at` 已设置则跳过
- `gh api repos/{repo}/pulls/{number}/requested_reviewers` — 检查 `teams[].name`
- `gh api orgs/{org}/teams/{slug}/members` — 检查作者是否为成员

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清。
