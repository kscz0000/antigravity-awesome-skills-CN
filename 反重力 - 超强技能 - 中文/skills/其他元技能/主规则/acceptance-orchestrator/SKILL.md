---
name: acceptance-orchestrator
description: 当编码任务需要从问题接收到实现、审查、部署和验收验证的端到端驱动时使用，最小化人工干预。触发词：验收编排、端到端交付、闭环交付、acceptance orchestrator、DoD验证、验收驱动开发
risk: safe
source: community
date_added: "2026-03-12"
---

# Acceptance Orchestrator

## 概述

将编码工作编排为一个状态机，仅在验收标准通过证据验证或任务显式升级时才结束。

核心规则：**不要优化"代码已更改"；优化"DoD已证明"。**

## 使用时机
- 任务已有问题或明确的验收标准，应端到端运行并最小化人工干预。
- 需要在实现、审查、部署和最终验证之间进行结构化交接。
- 需要明确的停止条件和升级机制，而非静默的部分完成。

## 必需子技能

- `create-issue-gate`
- `closed-loop-delivery`
- `verification-before-completion`

可选支持技能：
- `deploy-dev`
- `pr-watch`
- `pr-review-autopilot`
- `git-ship`

## 输入

需要以下输入：
- issue id 或 issue body
- issue status
- 验收标准 (DoD)
- 目标环境（默认 `dev`）

固定默认值：
- 最大迭代轮数 = `2`
- PR 审查轮询 = `3m -> 6m -> 10m`

## 状态机

- `intake`
- `issue-gated`
- `executing`
- `review-loop`
- `deploy-verify`
- `accepted`
- `escalated`

## 工作流程

1. **接收**
   - 读取 issue 并提取任务目标 + DoD。

2. **问题门控**
   - 使用 `create-issue-gate` 逻辑。
   - 如果 issue 不是 `ready` 或执行门控不是 `allowed`，立即停止。
   - 当 issue 仍为 `draft` 时不要实现任何内容。

3. **执行**
   - 移交给 `closed-loop-delivery` 进行实现和本地验证。

4. **审查循环**
   - 如果 PR 反馈相关，按以下窗口批量轮询：
     - 等待 `3m`
     - 然后 `6m`
     - 然后 `10m`
   - 在 `10m` 轮次后，停止等待并一起处理所有可见评论。

5. **部署与运行时验证**
   - 如果 DoD 依赖运行时行为，默认仅部署到 `dev`。
   - 用真实日志/API/Lambda 行为验证，而非假设。

6. **完成门控**
   - 在声称完成之前，需要 `verification-before-completion`。
   - 没有新证据不得声称成功。

## 停止条件

仅当每个验收标准都有匹配证据时才进入 `accepted`。

当以下任一情况发生时进入 `escalated`：
- DoD 在 `2` 轮完整循环后仍失败
- 缺少密钥/权限/外部依赖阻塞进度
- 任务需要生产环境操作或破坏性操作审批
- 审查指令冲突且无法同时满足

## 人工门控

以下情况始终停止等待人工确认：
- 超出约定范围的生产/预发布环境部署
- 破坏性 git/数据操作
- 计费或安全态势变更
- 缺少用户提供的验收标准

## 输出契约

报告状态时，始终包含：
- `Status`：intake / executing / accepted / escalated
- `Acceptance Criteria`：通过/失败检查清单
- `Evidence`：命令、日志、API 结果或运行时证明
- `Open Risks`：任何仍不确定的事项
- `Need Human Input`：如果受阻，最小的下一步决策

除非状态为 `accepted`，否则不要报告"完成"。

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清。
