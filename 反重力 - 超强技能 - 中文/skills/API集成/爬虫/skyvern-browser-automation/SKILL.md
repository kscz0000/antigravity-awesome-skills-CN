---
name: skyvern-browser-automation
description: "AI 驱动的浏览器自动化 — 导航网站、填写表单、提取结构化数据、使用存储凭证登录，并构建可复用的工作流。触发词：浏览器自动化、网页抓取、表单填写、AI代理、工作流自动化"
category: browser-automation
risk: safe
source: community
source_repo: Skyvern-AI/skyvern
source_type: official
date_added: "2026-04-23"
author: mark1ian
tags: [browser-automation, mcp, web-scraping, form-filling, ai-agents, workflow-automation]
tools: [claude, cursor, gemini, codex]
license: "AGPL-3.0"
license_source: "https://github.com/Skyvern-AI/skyvern/blob/main/LICENSE"
---

# Skyvern 浏览器自动化 — CLI 判断流程

Skyvern 使用 AI 来导航和交互网站。以下每个命令都是可运行的 `skyvern <command>` 调用。

## 何时使用此技能

- 当需要 AI 辅助的浏览器自动化来进行导航、数据提取、表单填写、登录流程或可复用的网站工作流时使用。
- 当确定性选择器不可用，而 Skyvern 的视觉/无障碍推理可以识别页面控件时使用。
- 当一次性浏览器任务需要变成可重复执行的工作流（包含运行历史和验证）时使用。

## 第一步：分类你的任务（始终先执行此步骤）

| 分类 | 信号 | CLI 命令 | 成本 | 发生什么 |
|---|---|---|---|---|
| 快速检查（是/否） | "用户是否已登录？" | `skyvern browser validate` | 1 次 LLM + 截图 | 轻量验证（最多 2 步），返回布尔值。最便宜的 AI 选项。 |
| 快速检查 | "页面显示什么？" | `skyvern browser extract` | 1 次 LLM + 截图 | 专用提取 LLM + schema 验证 + 缓存。 |
| 单次操作（已知目标） | "点击 #submit" | `skyvern browser click/type` | 0 次 LLM | 确定性 Playwright。无 AI。最快。 |
| 单次操作（未知目标） | "点击提交按钮" | `skyvern browser act` | 2-3 次 LLM，无截图 | 推理中无截图。经济型无障碍树。对于视觉目标，使用混合模式（选择器 + 意图）。 |
| 同页多步骤 | "填写表单并提交" | `skyvern browser act` 或原语链 | 2-3 次 LLM 或 0 次 LLM | 标签清晰时使用 `act`。知道选择器时直接使用 click/type/select。 |
| 一次性自主试验 | "试一次看看"，"看看是否可行" | `skyvern browser run-task` | 较高 | 一次性自主代理用于探索。不要用于重复或多页生产自动化。 |
| 多页或可复用自动化 | "导航多页向导"，"设置这个"，"每周自动化这个" | `skyvern workflow create` + `run` | N 次 LLM + 截图 | 构建工作流，每步一个块。每个块获得视觉推理、验证和可复用的运行历史。 |

**MCP 说明：** 如果你使用 Skyvern MCP 而非 CLI，对于同页多步骤 UI 工作优先使用 `observe + execute`。CLI 不直接暴露这对命令。

## 第二步：应用这些决策规则

1. 如果提示中包含选择器、id、XPath 或精确字段目标，使用浏览器原语 — 而非 `act`。
2. 如果只需要是/否答案，使用 `validate` — 而非 `extract` 或 `act`。
3. 如果工作停留在一个页面且标签清晰，使用 `act` 或原语链。
4. 如果用户说"试一次看看"、"看看是否可行"，或明确想要一次性探索试验，使用 `run-task`。
5. 如果任务跨越多页且需要可复用、可调度、可重复，或明确要"设置"为自动化，使用 `workflow create`。
6. 永远不要直接输入密码。始终使用 `skyvern browser login` 配合存储的凭证。

## 第三步：创建会话

每个浏览器命令都需要一个会话。先创建一个：

```bash
# 云端会话（默认 — 适用于公开 URL）
skyvern browser session create --timeout 30

# 本地会话（适用于 localhost URL 或自托管模式）
skyvern browser session create --local --timeout 30

# 通过 CDP 连接现有浏览器
skyvern browser session connect --cdp "ws://localhost:9222"
```

会话状态在命令间持久化。`session create` 之后，后续命令自动附加。
使用 `--session pbs_...` 覆盖。完成后关闭：`skyvern browser session close`。

## 第四步：按分类执行

### 快速检查（是/否）

```bash
skyvern browser validate --prompt "Is the user logged in? Look for a dashboard or avatar."
```

返回 true/false。最便宜的 AI 选项 — 对于布尔检查优先使用而非 extract 或 act。

### 快速检查

```bash
skyvern browser extract \
  --prompt "Extract all product names and prices" \
  --schema '{"type":"object","properties":{"items":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"price":{"type":"string"}}}}}}'
```

使用截图 + 专用提取 LLM。比截图+读取更好，因为 Skyvern 的 LLM 会解释页面。

### 单次操作（已知目标）

```bash
skyvern browser click --selector "#submit-btn"
skyvern browser type --text "user@co.com" --selector "#email"
skyvern browser select --value "US" --intent "the country dropdown"
```

确定性。无 AI。三种定位模式：
1. **意图**：`--intent "the Submit button"`（AI 查找元素）
2. **选择器**：`--selector "#submit-btn"`（CSS/XPath，确定性）
3. **混合**：两者结合（选择器缩小范围，AI 确认）

### 单次操作（未知目标）

```bash
skyvern browser act --prompt "Click the Sign In button"
skyvern browser act --prompt "Close the cookie banner, then click Sign In"
```

**警告：** act 的 LLM 推理中没有截图。它使用经济型无障碍树。
对于标签清晰的元素效果良好。对于视觉复杂的目标，使用 MCP observe+click 或混合模式。

### 同页多步骤

```bash
skyvern browser act --prompt "Fill the shipping form and click Continue"
```

当字段和按钮标签清晰且流程停留在一个页面时使用 `act`。
如果需要更精细的控制，将工作拆分为 `click`、`type`、`select`、`press-key` 和 `wait`。

### 一次性自主试验

```bash
skyvern browser run-task \
  --url "https://example.com" \
  --prompt "Check whether the checkout flow works end to end and extract the confirmation number"
```

使用 `run-task` 来验证可行性或进行一次性探索。如果任务变得足够重要需要重新运行、调试或分享，请将其转换为工作流。

### 多页或可复用自动化 — 每步一个块构建工作流

```bash
skyvern workflow create --definition @checkout-workflow.yaml
skyvern workflow run --id wpid_123 --wait
skyvern workflow status --run-id wr_789
```

每个导航块使用视觉推理 + 验证运行。将复杂流程拆分为多个块（每页/每步一个）。首次运行使用 AI；后续运行回放缓存脚本。

### 重复/生产

```bash
skyvern workflow create --definition @workflow.yaml
skyvern workflow run --id wpid_123 --params '{"email":"user@co.com"}'
skyvern workflow status --run-id wr_789
```

拆分为每步一个块。使用**导航**块执行操作，使用**提取**块获取数据。
首次运行使用 AI；后续运行回放缓存脚本（快 10-100 倍）。
设置 `--run-with agent` 强制 AI 模式用于调试。

## 第五步：验证

在改变页面的操作后始终验证：

```bash
skyvern browser screenshot                          # 视觉检查
skyvern browser validate --prompt "Was the form submitted successfully?"  # 布尔断言
skyvern browser evaluate --expression "document.title"                    # JS 状态检查
```

## 第六步：错误恢复

| 问题 | 修复 |
|---------|-----|
| 操作点击了错误的元素 | 在提示中添加上下文。使用混合模式（选择器 + 意图）。 |
| 提取返回空 | 等待内容加载。放宽必填字段。先检查行数。 |
| 登录成功但下一步失败 | 确保同一会话。添加登录后验证检查。 |
| 找不到元素 | 添加等待：`skyvern browser wait --selector "#el" --state visible` |
| 提示过于复杂 | 拆分为更小的目标 — 每个命令一个意图。 |

## 凭证

永远不要通过 `skyvern browser type` 或 `act` 输入密码。始终使用存储的凭证：

```bash
skyvern credentials add --name "my-login" --type password --username "user@co.com"
skyvern credential list                          # 查找凭证 ID
skyvern browser login --url "https://login.example.com" --credential-id cred_123
```

类型：`password`、`credit_card`、`secret`。还支持 bitwarden、1password 和 azure_vault 提供商。

## 工作流快速参考

```bash
skyvern workflow create --definition @workflow.yaml   # 创建
skyvern workflow run --id wpid_123 --wait             # 运行并等待
skyvern workflow status --run-id wr_789               # 检查状态
skyvern workflow list --search "invoice"              # 查找工作流
skyvern block schema --type navigation                # 发现块类型
skyvern block validate --block-json @block.json       # 创建前验证
```

引擎：已知路径 = 1.0（默认）。动态规划 = 2.0。有疑问时拆分为多个 1.0 块。
状态生命周期：`created -> queued -> running -> completed | failed | canceled | terminated | timed_out`

## 常见模式

**登录流程：**
```bash
skyvern credential list                          # 查找凭证 ID
skyvern browser session create
skyvern browser navigate --url "https://login.example.com"
skyvern browser login --url "https://login.example.com" --credential-id cred_123
skyvern browser validate --prompt "Is the user logged in?"
skyvern browser screenshot
```

**分页循环：**
```bash
skyvern browser extract --prompt "Extract all rows"
skyvern browser validate --prompt "Is there a Next button that is not disabled?"
# 如果为 true：
skyvern browser act --prompt "Click the Next page button"
# 重复提取。停止条件：没有下一页按钮、首行重复、或达到最大页数限制。
```

**调试：**
```bash
skyvern browser screenshot                       # 视觉状态
skyvern browser evaluate --expression "document.title"
skyvern browser evaluate --expression "document.querySelectorAll('table tr').length"
```

## 局限性

- 不要使用 Skyvern 绕过网站访问控制、速率限制、同意网关或禁止自动化的条款。
- 浏览器自动化可以改变远程状态；在提交表单、购买、删除或发送消息之前确认用户意图。
- 对于稳定的生产流程优先使用确定性选择器；AI 操作可能误读未标记或视觉上模糊的控件。
- 仅在支持的凭证库中存储凭证，永远不要通过 `type` 或 `act` 直接输入密码。

## 代理模式

所有命令接受 `--json` 以获取结构化输出。设置 `SKYVERN_NON_INTERACTIVE=1` 防止提示。
使用 `skyvern capabilities --json` 进行完整命令发现。参见 [references/agent-mode.md](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/agent-mode.md)。

## 深入参考

| 参考资料 | 内容 |
|-----------|---------|
| [`references/prompt-writing.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/prompt-writing.md) | 提示模板和反模式 |
| [`references/engines.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/engines.md) | 何时使用任务 vs 工作流 |
| [`references/schemas.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/schemas.md) | 提取的 JSON schema 模式 |
| [`references/pagination.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/pagination.md) | 分页策略和防护措施 |
| [`references/block-types.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/block-types.md) | 工作流块类型详情及示例 |
| [`references/parameters.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/parameters.md) | 参数设计和变量用法 |
| [`references/ai-actions.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/ai-actions.md) | AI 操作模式和示例 |
| [`references/precision-actions.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/precision-actions.md) | 仅意图、仅选择器、混合模式 |
| [`references/credentials.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/credentials.md) | 凭证命名、生命周期、安全 |
| [`references/sessions.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/sessions.md) | 会话复用和新鲜度决策 |
| [`references/common-failures.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/common-failures.md) | 失败模式目录及修复方案 |
| [`references/screenshots.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/screenshots.md) | 截图驱动的调试工作流 |
| [`references/status-lifecycle.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/status-lifecycle.md) | 运行状态和指导 |
| [`references/rerun-playbook.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/rerun-playbook.md) | 重运行流程和对比 |
| [`references/complex-inputs.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/complex-inputs.md) | 日期选择器、上传、下拉菜单 |
| [`references/tool-map.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/tool-map.md) | 按结果分类的完整工具清单 |
| [`references/cli-parity.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/cli-parity.md) | CLI/MCP 映射和代理感知功能 |
| [`references/quick-start-patterns.md`](https://github.com/Skyvern-AI/skyvern/blob/main/skyvern/cli/skills/skyvern/references/quick-start-patterns.md) | 快速入门示例、常见模式和工作流模板 |
