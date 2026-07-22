---
name: production-audit
description: "审计已上线仓库的生产环境就绪缺口，覆盖 RLS、webhook、密钥暴露、权限授予、Stripe 幂等性、移动端 UX 和部署健康状况。触发词：生产环境审计、上线检查、就绪审查、发布前检查、生产就绪、部署检查、合并后检查、audit、production audit、ready to ship、生产环境会出什么问题、what breaks in prod、is this production-ready"
category: security
risk: critical
source: community
source_repo: commitshow/production-audit
source_type: community
date_added: "2026-05-04"
author: commitshow
tags: [security, audit, production, vibe-coding, rls, webhook, stripe, supabase, mobile]
tools: [claude, cursor, gemini, codex, antigravity]
license: "MIT"
license_source: "https://github.com/commitshow/production-audit/blob/main/LICENSE"
---

# 生产环境审计

## 概述

一个对已上线仓库的部署状态运行外部审计的技能——涵盖在线 URL、GitHub 信号、密钥暴露、RLS 缺口、webhook 幂等性、索引、可观测性、提示注入，以及 AI 辅助项目经常遗漏的其他十几种故障模式。

本技能与会话内安全技能（`security-review`、OWASP 风格、VibeSec、Trail of Bits）**互补**。那些技能在写入时扫描编辑器缓冲区。本技能在你提交后扫描已部署的产品。时机不同、输入不同、发现不同。正式上线前两者都要运行。

本技能通过公共 CLI（`npx commitshow@0.3.23 audit . --json`）封装 [commit.show](https://commit.show) 审计引擎。JSON 信封格式稳定（`schema_version: "1"`，仅增量变更）。写入 `.commitshow/audit.{md,json}` 伴随文件，以便后续智能体会话无需重新运行引擎即可读取先前状态。

## 何时使用此技能

- 当用户询问"生产环境是否就绪"、"生产环境会出什么问题"、"给项目打分"、"我遗漏了什么"、"审计我的仓库"、"准备上线"时使用。
- 在功能分支合并到 `main` 后立即使用（可作为部署前门禁）。
- 在公开发布 / Show HN 帖子 / 投资人演示之前使用。
- 当 `git log` 显示自上次写入 `.commitshow/audit.md` 以来已超过 20 次提交时使用。

### 跳过的情况

- 在活跃的会话内编码期间——使用 `security-review` / OWASP 风格进行行级模式检查。本技能用于合并后 / 上线前的审查。
- 对于库 / 脚手架形式的仓库——引擎最适合**应用形式**；库只能获得部分替代评分。
- 如果 `.commitshow/audit.json` 已存在且不到 1 小时，直接读取而不要重新运行。审计有速率限制（匿名：20/IP/天 · 5/仓库/天 · 2000/天全局）。
- 在私有 / 非 GitHub 仓库内——审计会拉取公共 GitHub 信号，因此私有仓库会返回 `not_found` 错误。

## 工作原理

### 步骤 1：运行审计

从仓库根目录运行。CLI 固定到经审核的确切版本，因此后续的 npm 发布不会被静默选择。因为 `npx` 会以当前用户权限在本地下载并运行 npm 包代码，所以仅在用户明确批准此外部执行后、且仅在本地文件和环境变量对该进程安全可访问的仓库中运行。伴随目录预先创建，stderr 被分离，这样安装/弃用警告不会破坏 JSON 信封：

```bash
mkdir -p .commitshow
npx commitshow@0.3.23 audit . --json \
  > .commitshow/audit.json \
  2> .commitshow/audit.stderr.log
```

这也会在旁边写入人类可读的 `.commitshow/audit.md`。后续调用应与已有的 `audit.json` 进行差异对比，这样你可以用"自昨天审计以来 +5"开头，而不是只给出绝对数字。

如果用户指向的是远程 URL 而不是 `.`，将 `.` 替换为 URL——保持相同的 `mkdir -p` + 版本固定 + stderr 分离：

```bash
mkdir -p .commitshow
npx commitshow@0.3.23 audit github.com/owner/repo --json \
  > .commitshow/audit.json \
  2> .commitshow/audit.stderr.log
```

### 步骤 2：解析信封

JSON 信封格式稳定（`schema_version: "1"`，仅增量变更）。读取以下字段：

| 字段 | 含义 |
|---|---|
| `score.total` | 0-100 生产就绪评分 |
| `score.delta_since_last` | 与上次快照的变化 · 正值 = 改善 |
| `score.band` | `strong`（80+）· `mid`（60-79）· `early`（<60） |
| `concerns[]` | 主要问题，按影响排序 · 每项含 `axis` + `bullet` |
| `strengths[]` | 前 3 个正常的方面 · 仅供参考 |
| `standing` | 可选 · 仅当项目在 commit.show 上参与排名时出现 |
| `snapshot.created_at` / `trigger_type` | 审计运行时间 |

concerns 按决策影响力排序，而非严重程度。位置 1 是应优先处理的问题。

### 步骤 3：向用户呈现

以评分 + 趋势用**一句话**开头，然后列出主要 concerns。不要倾倒完整 JSON。格式：

```
Score: 82/100 (+5 since yesterday) · band: strong

Top concerns:
  ↓ [Security] No API rate limiting on /auth — IP cap missing
  ↓ [Infrastructure] webhook handler at api/stripe.ts — signature verified, but no
    idempotency-key check (replay attack window open)

Want me to fix the webhook idempotency gap first?
```

规则：
- 使用 `concerns[].bullet` 中的原文明细——审计引擎已经编写了行动导向的文案。
- 除非用户明确要求，否则不列出 strengths。它们在此上下文中不可操作。
- 始终以一个提及具体 concern 的跟进问题结尾。不要问"你想做什么？"——而要问"先修复 X？"。
- 如果 `score.delta_since_last` 为负或 null，仅以绝对评分开头。

### 步骤 4：如果用户选择了一个 concern，界定修复范围

对于选定的 concern：
1. 读取明细中引用的文件。
2. 确认缺口与描述匹配（引擎偶尔会在问题已在其他地方缓解时过度标记）。
3. 提出最小化补丁——尽可能单文件。
4. **未经明确批准不得应用。**先展示 diff。用户在决定上线什么；你只是透镜。

应用修复后，建议使用 `--refresh` 重新运行（与步骤 1 相同的规范形式，因此 `audit.json` 仍是差异计算的真相来源）：

```bash
mkdir -p .commitshow
npx commitshow@0.3.23 audit . --json --refresh \
  > .commitshow/audit.json \
  2> .commitshow/audit.stderr.log
```

## 示例

### 示例 1：用户询问"生产环境是否就绪？"

```bash
mkdir -p .commitshow
npx commitshow@0.3.23 audit . --json \
  > .commitshow/audit.json \
  2> .commitshow/audit.stderr.log
```

然后呈现：

```
Score: 67/100 · band: mid

Top concerns:
  ↓ [Security] members table uses column-level GRANT but paid_audits_credit
    column lacks SELECT grant — silent 42501 on every read
  ↓ [Infrastructure] stripe.checkout.sessions.create called without
    idempotencyKey — duplicate-charge surface

Want me to fix the column GRANT first? Single SQL line.
```

### 示例 2：交叉检查特定 concern

用户："给我看 webhook 幂等性缺口在哪里"

```bash
cat .commitshow/audit.json | jq '.concerns[] | select(.axis=="Infrastructure")'
```

在明细中找到文件路径，读取它，确认缺口与描述匹配。

## 最佳实践

- 始终引用 `concerns[].bullet` 中的原文明细——它们已经是行动导向的
- 以评分 + 差值用一句话开头，然后是 concerns
- 以一个提及具体 concern 的跟进问题结尾
- 重新运行前先读取已有的 `.commitshow/audit.json`（1 小时内）
- 用户合并修复后使用 `--refresh`，使下次审计反映变更
- 不要向用户倾倒完整 JSON
- 除非用户明确要求，否则不列出 strengths
- 未经批准不得应用修复——先展示 diff
- 不要因为私有仓库无法审计而责怪用户——解释原因并建议公开

## 局限性

- 本技能不替代环境特定的验证、测试或专家评审。
- 审计引擎针对**已部署应用**（有在线 URL）校准。CLI / 库 / 脚手架形式只能获得部分替代评分（审计支柱上最高约 45/50）——公平但不太好看。
- 在拦截 `*.supabase.co` 的企业防火墙后面，API 调用会失败。没有离线模式——审计依赖公共引擎。
- 冷审计需要 60-90 秒。缓存审计（7 天内）即时返回。`--refresh` 强制绕过缓存（计入速率限制）。

## 安全与安全注意事项

- 本技能执行 `npx commitshow@0.3.23 audit ...`，这会在本地下载并运行该确切 npm 包版本，然后调用公共 API `https://api.commit.show`（代理到 Supabase Edge Functions）。正常使用时不要将确切版本替换为 `latest` 或 semver 范围。
- 将 CLI 视为具有本地进程权限的外部代码。不得在包含密钥或敏感未提交文件的仓库中运行，除非用户已明确接受该风险。不会有意将凭据发送到 API，但本地进程可以访问当前用户可用的文件和环境变量。
- CLI 在当前工作目录写入 `.commitshow/audit.{md,json}`。这些文件可以安全提交（不含密钥），但通常作为临时产物被 gitignore。
- 审计引擎**仅读取**公共 GitHub 信号。它不会修改用户的仓库或推送提交。
- 所有逐项发现修复建议必须以 diff 形式展示并在任何编辑前经用户批准。未经明确确认绝不应用。

## 常见陷阱

- **问题：** 审计对私有仓库返回 `not_found`
  **解决方案：** 引擎仅拉取公共 GitHub 信号。将仓库公开或使用 `--no-network` 进行仅本地的确定性检查。

- **问题：** 触及速率限制（`429`）
  **解决方案：** 等到次日（限制在 UTC 00:00 重置）或在 commit.show 登录以获得更高的每仓库上限。

- **问题：** 对精良的库 / CLI 评分似乎太低
  **解决方案：** 引擎偏向应用形式。CLI / 库 / 脚手架只能获得约 45/50 的部分替代评分上限。这是已知的校准权衡。

- **问题：** 重新运行后 `concerns[]` 为空
  **解决方案：** 重新审计可能命中了缓存。使用 `--refresh` 强制绕过。

## 相关技能

- `@security-review` — 会话内行级安全模式。与本技能配合运行，而非替代。
- `@vibesec` — 针对 vibe-coding 项目的编辑器缓冲区安全审查。不同视角。
- `@owasp-security` — 编码时的 OWASP Top 10 覆盖。互补。
- `@trail-of-bits-skills` — CodeQL / Semgrep 静态分析。不同层级。

## 附加资源

- 规范仓库：<https://github.com/commitshow/production-audit>
- 审计引擎源码：<https://github.com/commitshow/commitshow/blob/main/supabase/functions/analyze-project/index.ts>
- 14 帧故障框架记录在上述引擎源码中。
- JSON schema：稳定于 `schema_version: "1"` · 仅增量变更。
- CLI：<https://github.com/commitshow/cli>
- 公共 REST API：`https://api.commit.show/audit?repo=...&format=json`
- skills.sh 列表：<https://skills.sh/commitshow/production-audit>
