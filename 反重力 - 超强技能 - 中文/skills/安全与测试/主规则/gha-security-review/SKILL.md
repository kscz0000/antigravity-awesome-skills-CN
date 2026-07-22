---
name: gha-security-review
description: "发现 GitHub Actions 工作流中可利用的漏洞。每项发现必须包含具体的利用场景——如果无法构建攻击，就不要报告。当用户要求审查 GitHub Actions 工作流安全时使用。"
risk: safe
source: community
date_added: 2026-03-16
---

<!--
攻击模式和真实案例来源于 StepSecurity 的 HackerBot Claw 攻击活动分析 (2025): https://www.stepsecurity.io/blog/hackerbot-claw-github-actions-exploitation
-->

# GitHub Actions 安全审查

发现 GitHub Actions 工作流中可利用的漏洞。每项发现必须包含具体的利用场景——如果无法构建攻击，就不要报告。

本技能编码了来自真实 GitHub Actions 攻击的攻击模式——而非通用的 CI/CD 理论。

## 使用时机

- 你正在审查 GitHub Actions 工作流的可利用安全问题。
- 任务需要从外部攻击者追踪到工作流执行或密钥泄露的具体攻击路径。
- 你需要对工作流文件、组合操作或工作流相关脚本进行安全审查，且仅输出有证据支持的发现。

## 范围

审查提供的工作流（文件、差异或仓库）。根据需要研究代码库，在报告前追踪完整的攻击路径。

### 需审查的文件

- `.github/workflows/*.yml` — 所有工作流定义
- `action.yml` / `action.yaml` — 仓库中的组合操作
- `.github/actions/*/action.yml` — 本地可复用操作
- 工作流加载的配置文件：`CLAUDE.md`、`AGENTS.md`、`Makefile`、`.github/` 下的 shell 脚本

### 超出范围

- 其他仓库中的工作流（仅记录依赖关系）
- GitHub App 安装权限（如相关则记录）

## 威胁模型

仅报告可被**外部攻击者**利用的漏洞——即**没有**仓库写入权限的人。攻击者可以从 fork 提交 PR、创建 issue 和发表评论。他们无法推送到分支、触发 `workflow_dispatch` 或触发手动工作流。

**不要标记**需要写入权限才能利用的漏洞：

- `workflow_dispatch` 输入注入 — 需要写入权限才能触发
- 受保护分支上仅 `push` 工作流中的表达式注入
- 所有调用方都是内部的 `workflow_call` 输入注入
- 仅 `workflow_dispatch`/`schedule` 工作流中的密钥

## 置信度

仅报告 **HIGH** 和 **MEDIUM** 置信度的发现。不要报告理论性问题。

| 置信度 | 标准 | 操作 |
|---|---|---|
| **HIGH** | 已追踪完整攻击路径，确认可利用 | 报告并附带利用场景和修复方案 |
| **MEDIUM** | 攻击路径部分确认，存在不确定环节 | 报告为需验证 |
| **LOW** | 理论性或已在其他地方缓解 | 不报告 |

对于每项 HIGH 发现，提供全部五个要素：

1. **入口点** — 攻击者如何进入？（fork PR、issue 评论、分支名等）
2. **载荷** — 攻击者发送什么？（实际代码/YAML/输入）
3. **执行机制** — 载荷如何运行？（表达式展开、checkout + 脚本等）
4. **影响** — 攻击者获得什么？（令牌窃取、代码执行、仓库写入权限）
5. **PoC 草图** — 攻击者会遵循的具体步骤

如果无法构建全部五个要素，报告为 MEDIUM（需验证）。

---

## 步骤 1：分类触发器并加载参考

对于每个工作流，识别触发器并加载相应参考：

| 触发器 / 模式 | 加载参考 |
|---|---|
| `pull_request_target` | `references/pwn-request.md` |
| 带命令解析的 `issue_comment` | `references/comment-triggered-commands.md` |
| `run:` 块中的 `${{ }}` | `references/expression-injection.md` |
| PAT / 部署密钥 / 提权凭证 | `references/credential-escalation.md` |
| 检出 PR 代码 + 配置文件加载 | `references/ai-prompt-injection-via-ci.md` |
| 第三方操作（尤其是未固定版本的） | `references/supply-chain.md` |
| `permissions:` 块或密钥使用 | `references/permissions-and-secrets.md` |
| 自托管 runner、缓存/artifact 使用 | `references/runner-infrastructure.md` |
| 任何已确认的发现 | `references/real-world-attacks.md` |

选择性加载参考——仅加载与发现的触发器相关的内容。

## 步骤 2：检查漏洞类别

### 检查 1：Pwn Request

工作流是否使用 `pull_request_target` 且检出 fork 代码？
- 查找指向 PR head 的 `actions/checkout` 的 `ref:`
- 查找会来自 fork 的本地操作（`./.github/actions/`）
- 检查是否有任何 `run:` 步骤执行来自检出 PR 的代码

### 检查 2：表达式注入

在外部可触发的工作流中，`${{ }}` 表达式是否用于 `run:` 块内？
- 映射每个 `run:` 步骤中的每个 `${{ }}` 表达式
- 确认值是攻击者可控的（PR 标题、分支名、评论正文——而非数字 ID、SHA 或仓库名）
- 确认表达式在 `run:` 块中，而非 `if:`、`with:` 或作业级 `env:`

### 检查 3：未授权命令执行

`issue_comment` 触发的工作流是否在未授权的情况下执行命令？
- 是否有 `author_association` 检查？
- 任何 GitHub 用户都能触发该命令吗？
- 命令处理程序是否也使用了可注入的表达式？

### 检查 4：凭证提权

提权凭证（PAT、部署密钥）是否可被不受信任的代码访问？
- 每个密钥的影响范围是什么？
- 被攻陷的工作流能否窃取长期有效的令牌？

### 检查 5：配置文件投毒

工作流是否从 PR 提供的文件加载配置？
- AI 智能体指令：`CLAUDE.md`、`AGENTS.md`、`.cursorrules`
- 构建配置：`Makefile`、shell 脚本

### 检查 6：供应链

第三方操作是否安全固定？

### 检查 7：权限和密钥

工作流权限是否最小化？密钥是否正确限定范围？

### 检查 8：Runner 基础设施

自托管 runner、缓存或 artifact 是否安全使用？

## 安全模式（不要标记）

报告前，检查该模式是否实际安全：

| 模式 | 为何安全 |
|---|---|
| `pull_request_target` 但不检出 fork 代码 | 从不执行攻击者代码 |
| `run:` 中的 `${{ github.event.pull_request.number }}` | 仅数字——不可注入 |
| `${{ github.repository }}` / `github.repository_owner` | 仓库所有者控制此值 |
| `${{ secrets.* }}` | 不是表达式注入向量 |
| `if:` 条件中的 `${{ }}` | 由 Actions 运行时求值，而非 shell |
| `with:` 输入中的 `${{ }}` | 作为字符串参数传递，不经 shell 求值 |
| 固定到完整 SHA 的操作 | 不可变引用 |
| `pull_request` 触发器（非 `_target`） | 在 fork 上下文中以只读令牌运行 |
| `workflow_dispatch`/`schedule`/受保护分支 `push` 中的任何表达式 | 需要写入权限——超出威胁模型 |

**关键区别：** `${{ }}` 在 `run:` 块中是危险的（shell 展开），但在 `if:`、`with:` 和作业/步骤级 `env:` 中是安全的（Actions 运行时求值）。

## 步骤 3：报告前验证

包含任何发现前，读取实际的工作流 YAML 并追踪完整的攻击路径：

1. **读取完整工作流** — 不要仅依赖 grep 输出
2. **追踪触发器** — 确认事件并检查控制执行的 `if:` 条件
3. **追踪表达式/检出** — 确认它在 `run:` 块中或实际引用了 fork 代码
4. **确认攻击者控制** — 验证值映射到外部攻击者可设置的内容
5. **检查现有缓解措施** — 环境变量包装、author_association 检查、受限权限、SHA 固定

如果任何环节断裂，标记为 MEDIUM（需验证）或放弃该发现。

**如果没有检查产生发现，报告零发现。不要编造问题。**

## 步骤 4：报告发现

````markdown
## GitHub Actions 安全审查

### 发现

#### [GHA-001] [标题] (严重程度: Critical/High/Medium)
- **工作流**: `.github/workflows/release.yml:15`
- **触发器**: `pull_request_target`
- **置信度**: HIGH — 通过攻击路径追踪确认
- **利用场景**:
  1. [分步攻击过程]
- **影响**: [攻击者获得什么]
- **修复**: [修复问题的代码]

### 需验证
[MEDIUM 置信度项目，说明需要验证什么]

### 已审查并确认安全
[已审查并确认安全的工作流]
````

如果没有发现："未发现可利用的漏洞。所有工作流已审查并确认安全。"

## 局限性

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
