---
name: gh-image
description: "将本地图片上传到 GitHub 并获取规范的 user-attachments 嵌入 URL；用于将截图附加到 PR、issue 或评论，或在 README 中嵌入前后对比图片。触发词：上传图片到 GitHub、截图上传、PR 图片、issue 图片、user-attachments、嵌入图片、gh-image、附图、上传截图。"
category: developer-tools
risk: critical
source: community
source_type: community
source_repo: drogers0/gh-image
date_added: "2026-06-25"
author: drogers0
license: MIT
license_source: "https://github.com/drogers0/gh-image/blob/main/LICENSE"
tags:
  - github
  - images
  - screenshots
  - gh-extension
  - cli
tools:
  - claude-code
  - codex-cli
  - cursor
  - gemini-cli
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "安装并运行一个第三方 gh 扩展，该扩展需要 GitHub user_session cookie 或 GH_SESSION_TOKEN。"
    docs: SKILL.md
---

# 上传图片到 GitHub（gh-image）

GitHub **没有公开的 API** 用于图片上传 —— Web UI 使用的是一个内部接口，
该接口会签发作用域限定于仓库可见性的 `user-attachments` URL。
[`gh-image`](https://github.com/drogers0/gh-image)（MIT，© drogers0）将该流程
复刻为 `gh` CLI 扩展，使智能体能够从终端上传本地图片，并返回可直接嵌入的
Markdown 图片行。

## 概述

本技能驱动 `gh-image` 将本地图片文件转换为托管在 GitHub 上的 `user-attachments`
URL，然后将该 URL 嵌入到拉取请求、issue 或评论中。它补齐了终端智能体缺失的
"附加截图"能力。

## 何时使用本技能

在以下场景使用本技能：

- "把截图附加到 PR" 或 "在 PR 描述中添加图片"
- "把这张图放到 issue 里" / "用这些截图发评论"
- "在 PR 里展示测试结果 / 前后对比"
- 在不离开终端的情况下，将任意本地图片嵌入到 GitHub Markdown

## 工作原理

### 步骤 1：检查前置条件

```bash
gh auth status                                   # gh installed & authenticated
gh extension list | grep -q 'drogers0/gh-image' \
  || gh extension install drogers0/gh-image      # review/pin the extension source first
```

`gh-image` **不会**使用 `gh` 的 token 进行上传（该接口拒绝 token）。
它需要一个 GitHub `user_session` cookie，按以下顺序解析：
`--token <value>` 参数 → `GH_SESSION_TOKEN` 环境变量（在 CI/无头环境使用）→
已登录浏览器的 cookie 存储（本地使用时的默认来源）。

### 步骤 2：上传

```bash
# Use an absolute path; --repo is optional inside a repo working dir.
gh image "/abs/path/screenshot.png" --repo <owner>/<repo>
```

`gh image` 将 Markdown 输出到 **stdout**，每张图片占一行：

```
![screenshot.png](https://github.com/user-attachments/assets/<uuid>)
```

捕获该输出 —— 这就是可嵌入的引用。

### 步骤 3：嵌入到 PR / issue / 评论

```bash
MD="$(gh image "/abs/path/shot.png" --repo owner/repo)"
BODY="$(gh pr view <pr> --repo owner/repo --json body -q .body)"
printf '%s\n\n## Screenshots\n\n%s\n' "$BODY" "$MD" \
  | gh pr edit <pr> --repo owner/repo --body-file -
```

对于其他目标，使用 `gh pr comment`、`gh issue edit` 或 `gh issue comment` 并
配合 `--body-file -`。始终传入 `--body-file -`（而不是内联 `--body`），以避免
多行内容和特殊字符破坏 shell 的引号处理。

### 步骤 4：验证

```bash
gh pr view <pr> --repo owner/repo --json body -q .body   # confirm URL present
```

## 示例

- **将 CleanShot 截图附加到 PR #42：** 上传文件，并将其追加到 PR 正文中的
  `## Screenshots` 标题下。
- **在 README 中嵌入前后对比图：** 上传两张图片，将两行 Markdown
  粘贴到 README 的相关章节。

## 最佳实践

- 优先将 glob 模式解析为绝对路径；对含空格或 Unicode 的路径加上引号。
- 若要控制显示尺寸，使用 HTML 标签代替裸 Markdown：
  `<img width="800" src="https://github.com/user-attachments/assets/<uuid>" />`。
- 在 CI 中，从专用的机器人账号设置 `GH_SESSION_TOKEN`。

## 局限性

- **需要 session cookie。** `user_session` cookie 拥有账户的完全访问权限
  （不像 PAT 那样受限作用域）—— 应像密码一样对待；在 CI 中使用机器人账号。
- **需要对目标仓库的写权限**；强制执行 SAML SSO 的组织需要先在
  `https://github.com/orgs/<org>/sso` 完成 session 授权。
- **私有仓库的图片保持私有：** `user-attachments` URL 继承仓库可见性，
  因此对私有仓库的匿名访问会按设计返回 404/403。
- **Windows + Chrome 127+** 无法读取 cookie（库限制）—— 请使用其他
  浏览器或 `GH_SESSION_TOKEN`。
- 本技能自行嵌入 Markdown；`gh-image` 仅负责输出 URL。