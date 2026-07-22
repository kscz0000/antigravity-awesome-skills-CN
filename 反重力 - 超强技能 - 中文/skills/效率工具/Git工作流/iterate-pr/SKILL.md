---
name: iterate-pr
description: 持续迭代 PR 直到 CI 通过。用于修复 CI 失败、处理审查反馈或持续推送修复直到所有检查通过。自动化反馈-修复-推送-等待循环。触发词：iterate-pr、PR迭代、CI修复、持续集成修复、PR检查、代码审查反馈。
risk: critical
source: community
---

# 迭代 PR 直到 CI 通过

持续迭代当前分支，直到所有 CI 检查通过且审查反馈已处理。

**需要**：GitHub CLI (`gh`) 已认证。

**重要**：所有脚本必须从仓库根目录 (`.git` 所在位置) 运行，而不是从技能目录运行。通过 `${CLAUDE_SKILL_ROOT}` 使用脚本的完整路径。

## 内置脚本

### `scripts/fetch_pr_checks.py`

获取 CI 检查状态并从日志中提取失败片段。

```bash
uv run /scripts/fetch_pr_checks.py [--pr NUMBER]
```

返回 JSON：
```json
{
  "pr": {"number": 123, "branch": "feat/foo"},
  "summary": {"total": 5, "passed": 3, "failed": 2, "pending": 0},
  "checks": [
    {"name": "tests", "status": "fail", "log_snippet": "...", "run_id": 123},
    {"name": "lint", "status": "pass"}
  ]
}
```

### `scripts/fetch_pr_feedback.py`

使用 [LOGAF 量表](https://develop.sentry.dev/engineering-practices/code-review/#logaf-scale) 获取并分类 PR 审查反馈。

```bash
uv run /scripts/fetch_pr_feedback.py [--pr NUMBER]
```

返回 JSON，反馈分类为：
- `high` — 合并前必须处理（`h:`、阻塞项、请求变更）
- `medium` — 应该处理（`m:`、标准反馈）
- `low` — 可选（`l:`、nit、风格、建议）
- `bot` — 信息性自动评论（Codecov、Dependabot 等）
- `resolved` — 已解决的线程

审查机器人反馈（来自 Sentry、Warden、Cursor、Bugbot、CodeQL 等）出现在 `high`/`medium`/`low` 中并带有 `review_bot: true` — 不会放在 `bot` 桶中。

每个反馈项还可能包含：
- `thread_id` — 内联审查评论的 GraphQL 节点 ID（用于回复）

## 工作流程

### 1. 识别 PR

```bash
gh pr view --json number,url,headRefName
```

如果当前分支没有 PR，则停止。

### 2. 收集审查反馈

运行 `${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_feedback.py` 获取 PR 上已发布的分类反馈。

### 3. 按 LOGAF 优先级处理反馈

**自动修复（不提示）：**
- `high` — 必须处理（阻塞项、安全、请求变更）
- `medium` — 应该处理（标准反馈）

修复反馈时：
- 理解根本原因，而不仅仅是表面症状
- 检查附近代码或相关文件中是否有类似问题
- 修复所有实例，而不仅仅是提到的那一个

这包括审查机器人反馈（带有 `review_bot: true` 的项）。将其与人工反馈同等对待：
- 发现真实问题 → 修复它
- 误报 → 跳过，但在简短评论中解释原因
- 永远不要静默忽略审查机器人反馈 — 始终验证发现

**提示用户选择：**
- `low` — 显示编号列表并询问要处理哪些：

```
发现 3 个低优先级建议：
1. [l] "考虑重命名此变量" - @reviewer 在 api.py:42
2. [nit] "可以使用列表推导式" - @reviewer 在 utils.py:18
3. [style] "添加文档字符串" - @reviewer 在 models.py:55

您想处理哪些？（例如 "1,3" 或 "all" 或 "none"）
```

**静默跳过：**
- `resolved` 线程
- `bot` 评论（仅信息性 — Codecov、Dependabot 等）

#### 回复评论

处理每个内联审查评论后，在 PR 线程中回复以确认采取的操作。仅回复带有 `thread_id` 的项（内联审查评论）。

**何时回复：**
- `high` 和 `medium` 项 — 无论已修复还是判定为误报
- `low` 项 — 无论已修复还是用户拒绝

**如何回复：** 使用 `addPullRequestReviewThreadReply` GraphQL 变更，传入 `pullRequestReviewThreadId` 和 `body` 输入。

**回复格式：**
- 1-2 句话：做了什么更改、为什么不是问题、或确认拒绝的项
- 每条回复以 `\n\n*— Claude Code*` 结尾
- 回复前，检查线程是否已有以 `*- Claude Code*` 或 `*— Claude Code*` 结尾的回复，以避免重复循环时产生重复
- 如果 `gh api` 调用失败，记录并继续 — 不要阻塞工作流程

### 4. 检查 CI 状态

运行 `${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_checks.py` 获取结构化失败数据。

**如有待处理则等待：** 如果审查机器人检查（sentry、warden、cursor、bugbot、seer、codeql）仍在运行，则在继续之前等待 — 它们会发布需要评估的可操作反馈。信息性机器人（codecov）不值得等待。

### 5. 修复 CI 失败

对于脚本输出中的每个失败：
1. 阅读 `log_snippet` 并从错误向后追踪，理解失败的原因 — 而不仅仅是失败了什么
2. 阅读相关代码并检查相关问题（例如，如果一个调用点有类型错误，检查其他调用点）
3. 用最小化、针对性的更改修复根本原因
4. 找到受影响代码的现有测试并运行它们。如果修复引入了现有测试未覆盖的行为，扩展测试以覆盖它（添加测试用例，而不是整个新测试文件）

不要仅根据检查名称假设失败内容 — 始终阅读日志。不要"快速修复并祈祷" — 在更改代码前彻底理解失败。

### 6. 本地验证，然后提交并推送

提交前，在本地验证修复：
- 如果修复了测试失败：在本地重新运行该特定测试
- 如果修复了 lint/类型错误：在受影响文件上重新运行 linter 或类型检查器
- 对于任何代码修复：运行覆盖更改代码的现有测试

如果本地验证失败，在继续之前修复 — 不要推送已知损坏的代码。

```bash
git add <files>
git commit -m "fix: <描述性消息>"
git push
```

### 7. 监控 CI 并处理反馈

以循环方式轮询 CI 状态和审查反馈，而不是阻塞：

1. 运行 `uv run /scripts/fetch_pr_checks.py` 获取当前 CI 状态
2. 如果所有检查通过 → 进入退出条件
3. 如果有任何检查失败（无待处理）→ 返回步骤 5
4. 如果检查仍在待处理：
   a. 运行 `uv run /scripts/fetch_pr_feedback.py` 获取新的审查反馈
   b. 立即处理任何新的 high/medium 反馈（同步骤 3）
   c. 如果需要更改，提交并推送（这会重启 CI），然后继续轮询
   d. 休眠 30 秒，然后从子步骤 1 重复
5. 所有检查通过后，做最终反馈检查：`sleep 10`，然后运行 `uv run /scripts/fetch_pr_feedback.py`。处理任何新的 high/medium 反馈 — 如果需要更改，返回步骤 6。

### 8. 重复

如果步骤 7 需要代码更改（来自 CI 通过后的新反馈），返回步骤 2 开始新循环。监控期间的 CI 失败已在步骤 7 的轮询循环中处理。

## 退出条件

**成功**：所有检查通过，CI 后反馈复查干净（无新的未处理 high/medium 反馈，包括审查机器人发现），用户已决定低优先级项。

**请求帮助**：2 次尝试后仍相同失败、反馈需要澄清、基础设施问题。

**停止**：无 PR 存在、分支需要 rebase。

## 后备方案

如果脚本失败，直接使用 `gh` CLI：
- `gh pr checks name,state,bucket,link`
- `gh run view <run-id> --log-failed`
- `gh api repos/{owner}/{repo}/pulls/{number}/comments`


## 使用时机
当处理与上述主要领域或功能相关的任务时，使用此技能。

## 限制
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。