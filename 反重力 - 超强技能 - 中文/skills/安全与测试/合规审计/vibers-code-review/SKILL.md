---
name: vibers-code-review
description: 面向 AI 生成 GitHub 项目的人工审查工作流，由 Vibers 服务提供基于规格的反馈、安全审查和后续 PR。触发词：代码审查、AI 代码审查、人工代码审查、代码评审、PR 审查、spec 审查、安全审查、follow-up PR、Vibers 审查、AI 生成代码审查。
risk: critical
source: https://github.com/marsiandeployer/vibers-action
date_added: "2026-03-17"
---

# Vibers — 面向 AI 生成项目的人工代码审查

你推送代码。我们对照你的规格审查代码，修复问题，并发送 PR。

## 何时使用

在以下情况下使用本技能：

- 你希望对推送到 GitHub 的 AI 生成代码进行人工审查
- 你有项目规格，希望审查者对照检查实现
- 你希望审查反馈以包含建议修复的后续 PR 形式交付
- 你愿意授予 Vibers 服务对仓库的协作者访问权限

## 快速开始（3 步）

### 第 1 步. 添加协作者

进入你的仓库 → Settings → Collaborators → 添加 **`marsiandeployer`**

### 第 2 步. 添加 GitHub Action

创建 `.github/workflows/vibers.yml`：

```yaml
name: Vibers Code Review
on:
  push:
    branches: [main]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - uses: marsiandeployer/vibers-action@v1
        with:
          spec_url: 'https://docs.google.com/document/d/YOUR_SPEC_ID/edit'
          telegram_contact: '@your_telegram'
```

| 参数 | 说明 |
|-----------|-------------|
| `spec_url` | 你的规格链接（Google Doc、Notion 等）。**必须可公开访问**（或"拥有链接的任何人可查看"）。无法访问规格则无法进行审查。 |
| `review_scope` | `full`（默认）、`security` 或 `spec-compliance` |
| `telegram_contact` | 你的 Telegram —— 审查完成时我们会通过它联系你 |

### 第 3 步. 为你的 AI 智能体添加提交规范

将以下内容添加到项目的 `CLAUDE.md`、`.cursorrules` 或 `AGENTS.md` 中：

```markdown
## Commit messages

Every commit MUST include a "How to test" section in the body:
- Live URL to open and verify the change
- Step-by-step what to click/check
- Test credentials if login is required
- Expected result for each step

Example:
  feat: Add user registration form

  How to test:
  - Open https://myapp.vercel.app/register
  - Fill in email/password, submit
  - Check that confirmation email arrives
  - Try submitting with invalid email — should show error
  - Login: test@example.com / demo123
```

如果没有"How to test"部分，审查者只能猜测要验证什么，审查耗时会更长。

**完成。** 现在每次推送都会触发通知。你通常会在 24 小时内收到包含修复的 PR。

## 设置之后会发生什么

1. 你推送代码 → GitHub Action 将提交详情发送给我们
2. 我们阅读你的规格并审查变更的文件
3. 我们直接在代码中修复问题并提交 PR
4. 你审查该 PR，决定合并或评论

我们检查：规格合规、安全（OWASP Top 10）、AI 幻觉（伪造的 API/import）、逻辑 bug、UI 问题。

我们不检查：代码风格（请使用 ESLint/Prettier）、性能基准、完整 QA（请使用 Playwright/Cypress）。

## 局限性

- 需要一个 GitHub 仓库并将 `marsiandeployer` 添加为协作者
- 所引用的规格必须对审查工作流可访问
- 本服务不能替代完整 QA、基准测试或本地安全审查
- 周转时间取决于外部 Vibers 审查服务

## 定价

| 套餐 | 费率 | 详情 |
|------|------|---------|
| **Promo** | $1/小时 | 完整审查 + 包含修复的 PR。我们仅要求你提供真实反馈。 |
| **Standard** | $15/小时 | 完整审查 + 安全审计 + 优先周转。 |

无订阅。无合同。按次审查付费。

## 反馈与支持

直接从你的智能体发送反馈：

```bash
curl -X POST https://vibers.onout.org/feedback \
  -H 'Content-Type: application/json' \
  -d '{"message": "Your question or issue", "repo": "https://github.com/you/your-repo"}'
```

`message` 和 `repo` 都是必填项。响应：`{"status": "accepted"}`。

联系方式：
- Telegram：[@onoutnoxon](https://t.me/onoutnoxon)
- Moltbook：[moltbook.com](https://moltbook.com) — 用户 **noxon**
- GitHub：[marsiandeployer](https://github.com/marsiandeployer)

## 常见问题

**需要 API 密钥吗？**
不需要。添加协作者 + action 即可。

**支持哪些语言？**
JS/TS、Python、React、Next.js、Django、Flask 等。只要在 GitHub 上，我们都能审查。

**如果我不同意某项修复怎么办？**
在该 PR 上评论。我们会讨论并调整。

**可以在不使用 GitHub 的情况下使用吗？**
可以 —— 通过 Telegram 把你的代码和规格发给我们即可。
