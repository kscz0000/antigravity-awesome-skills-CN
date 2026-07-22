---
name: create-issue-gate
description: 在开始新的实现任务时使用，要求在执行前创建带有严格验收标准的 GitHub issue 作为门禁。
risk: safe
source: community
date_added: "2026-03-12"
---

# Create Issue Gate

## 概述

创建 GitHub issue 作为任务的唯一跟踪入口，并对验收标准设置硬性门禁。

核心规则：**用户未提供明确、可测试的验收标准 => issue 保持 `draft` 状态，阻止执行。**

## 使用时机
- 你正在开始一个新的实现任务，希望 GitHub issue 成为必需的跟踪入口。
- 工作必须被阻止，直到用户提供明确、可测试的验收标准。
- 你需要在执行开始前区分 `draft`、`ready` 和 `blocked` 状态的工作。

## 必填字段

每个 issue 必须包含以下部分：
- Problem（问题）
- Goal（目标）
- Scope（范围）
- Non-Goals（非目标）
- Acceptance Criteria（验收标准）
- Dependencies/Blockers（依赖/阻塞项）
- Status（状态：`draft` | `ready` | `blocked` | `done`）

## 验收标准门禁

验收标准仅在可测试且可通过/失败检查时才有效。

示例：
- 有效："CreateCheckoutLambda-dev 返回一个可打开的第三方支付结账 URL"
- 无效："修复结账" / "改进 UX" / "让它更好"

如果验收标准缺失或不可测试：
- 仍然创建 issue
- 设置 `Status: draft`
- 添加 `Execution Gate: blocked (missing valid acceptance criteria)`
- 不要将任务移至执行阶段

## Issue 创建模式

默认模式是使用 `gh issue create` 直接在 GitHub 上创建。

使用如下正文模板：

```md
## Problem
<什么损坏或缺失>

## Goal
<期望的结果是什么>

## Scope
- <范围内的事项>

## Non-Goals
- <范围外的事项>

## Acceptance Criteria
- <明确、可测试的标准 1>

## Dependencies/Blockers
- <依赖项或 none>

## Status
draft|ready|blocked|done

## Execution Gate
allowed|blocked (<原因>)
```

## 状态规则

- `draft`：缺少/薄弱的验收标准或任务定义不完整
- `ready`：验收标准明确且可测试
- `blocked`：外部依赖阻止进展
- `done`：验收标准已通过证据验证

切勿在没有有效验收标准的情况下将 issue 标记为 `ready`。

## 交接至执行

执行工作流（例如 `closed-loop-delivery`）仅在以下情况下可以启动：
- issue 状态为 `ready`
- execution gate 为 `allowed`

如果 issue 为 `draft`，停止并请求用户提供验收标准。

## 局限性
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清。
