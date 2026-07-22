---
name: agentflow
description: "通过看板工具（Asana、GitHub Projects、Linear）编排自主 AI 开发流水线。管理多工作器 Claude Code 调度、确定性质量门控、对抗性审查、单任务成本追踪和崩溃恢复流水线执行。触发词：AgentFlow、AI流水线编排、看板自动化、多智能体调度、自主开发流水线、Claude Code调度、质量门控、对抗性审查、成本追踪、crash-proof编排"
risk: safe
source: community
date_added: "2026-04-02"
---

# AgentFlow

## 概述

AgentFlow 将你现有的看板工具转变为完全自主的 AI 开发流水线。它不需要构建自定义编排基础设施，而是将你的项目管理工具（Asana、GitHub Projects、Linear）视为分布式状态机——任务在阶段间流转，AI 智能体通过评论读写状态，人类通过他们已使用的同一界面进行干预。

结果是从手机即可获得完整的流水线可观测性，免费的崩溃恢复（状态存储在你的项目管理工具中，而非内存中），以及随时通过拖拽卡片进行人工干预的能力。

## 何时使用此技能

- 当需要跨完整开发生命周期（构建、审查、测试、集成）编排多个 Claude Code 工作器时使用
- 当希望在 AI 审查 AI 生成的代码之前运行确定性质量门控（tsc/eslint/tests）时使用
- 当希望从看板或手机获得完整的流水线可见性时使用
- 当运行需要自主任务调度和成本追踪的个人或团队项目时使用
- 当需要能够从会话重启中恢复的崩溃恢复编排时使用

## 核心概念

### 7阶段看板流水线

任务流经：Backlog、Research、Build、Review、Test、Integrate、Done。每个阶段都有特定的门控。看板本身就是编排层——无需单独的数据库、消息队列或自定义基础设施。

### 无状态编排器

由 crontab 驱动的单次扫描每 15 分钟运行一次。无守护进程，无会话依赖。如果崩溃，下一次扫描会从中断处继续，因为所有状态都存储在你的项目管理工具中。

### 确定性优先于概率性

硬性门控（tsc + eslint + tests）在任何 AI 审查之前运行，以接近零成本捕获约 60% 的问题。AI 审查作为第二层随后进行。

### 对抗性审查

不同的 AI 智能体审查代码，必须在决定通过之前列出 3 个问题。这防止了橡皮图章式的批准。

### 传递优先级调度

自动解除最多下游工作阻塞的任务优先构建，自动计算关键路径。

## 技能 / 命令

### `/spec-to-board`
将 SPEC.md 分解为看板上的原子任务，并映射依赖关系。

### `/sdlc-orchestrate`
基于传递优先级和冲突检测将任务分发给工作器。作为 crontab 扫描运行。

### `/sdlc-worker --slot <N>`
在终端槽位中运行工作器，拾取任务、构建代码并创建 PR。并行运行 3-4 个工作器。

### `/sdlc-health`
实时流水线状态仪表盘，显示每个任务的当前阶段、分配的智能体、重试次数和累计成本。

### `/sdlc-stop`
优雅关闭：活动工作器完成当前任务，未启动的任务返回 Backlog。

## 分步指南

### 1. 编写规格说明

为你的项目创建描述你想要构建内容的 `SPEC.md`。

### 2. 分解为任务

```
claude -p "/spec-to-board"
```

这会读取你的 SPEC.md，将其分解为原子任务，映射依赖关系，并在看板上创建它们。

### 3. 启动工作器

打开 3-4 个终端窗口，每个作为工作器槽位：

```bash
# Terminal 2 — Builder
claude -p "/sdlc-worker --slot T2"

# Terminal 3 — Builder
claude -p "/sdlc-worker --slot T3"

# Terminal 4 — Reviewer
claude -p "/sdlc-worker --slot T4"

# Terminal 5 — Tester
claude -p "/sdlc-worker --slot T5"
```

### 4. 启动编排器

```bash
# Add to crontab (runs every 15 minutes)
crontab -e
# Add: */15 * * * * ~/.claude/sdlc/agentflow-cron.sh >> /tmp/agentflow-orchestrate.log 2>&1
```

### 5. 监控和干预

在手机上打开你的看板。观察任务流经流水线。将任何卡片拖到 "Needs Human" 进行干预。运行 `/sdlc-health` 获取终端仪表盘。

### 6. 停止流水线

```
claude -p "/sdlc-stop"
```

## 质量门控

每个阶段在晋升前强制执行特定门控：

- **Build 到 Review**：`tsc` + `eslint` + `npm test` 必须全部通过（确定性）
- **Review 到 Test**：对抗性审查者必须在通过前列出 3 个问题
- **Test 到 Integrate**：新文件达到 80% 覆盖率阈值
- **Integrate 到 Done**：合并后 main 上的完整测试套件；失败时自动回滚

## 成本追踪

单任务成本追踪，带有阶段上限（Sonnet 默认值）：

- Research：~$0.10
- Build：~$0.40
- Review：~$0.10
- Test：~$0.05
- Integrate：~$0.03

自动防护：$3/$8 警告，$10/$20 硬性停止（Sonnet/Opus），并升级给人工处理。

## 安全与恢复

- **自动回滚**：集成失败触发 `git revert`（新提交，永不强制推送）
- **阻塞任务**：2 次失败尝试后，任务升级为人工审查
- **死亡智能体检测**：每 5 分钟心跳，10 分钟超时后重新分配
- **优雅关闭**：`/sdlc-stop` 排空工作器，将未启动的任务返回 backlog
- **范围蔓延检测**：PR 差异文件与预测文件列表进行比较
- **规格漂移检测**：SHA-256 哈希比较捕获冲刺中途的需求变更

## 安装

```bash
# Clone the repo
git clone https://github.com/UrRhb/agentflow.git

# Copy skills and prompts to your Claude Code config
cp -r agentflow/skills/* ~/.claude/skills/
cp -r agentflow/prompts/* ~/.claude/sdlc/prompts/
cp agentflow/conventions.md ~/.claude/sdlc/conventions.md
```

或作为 Claude Code 插件安装：

```bash
/plugin marketplace add UrRhb/agentflow
/plugin install agentflow
```

## 最佳实践

- 建议：在运行 `/spec-to-board` 之前编写清晰的 SPEC.md
- 建议：对于典型项目，从 3-4 个工作器开始
- 建议：从看板监控，需要时将卡片拖到 "Needs Human"
- 建议：定期审查 LEARNINGS.md——它捕获常见失败模式
- 禁止：跳过确定性质量门控——它们能低成本捕获大多数问题
- 禁止：强制推送到 main——AgentFlow 使用 `git revert` 确保安全
- 禁止：运行超过项目并行度支持的工作器数量

## 故障排除

### 问题：工作器似乎卡住或死亡
**症状：** 任务卡片 15+ 分钟未移动，无新评论
**解决方案：** 编排器通过心跳检测死亡智能体并在 10 分钟后重新分配。如果问题持续，运行 `/sdlc-health` 检查状态并手动将卡片拖回 Backlog。

### 问题：触发成本防护
**症状：** 任务移动到 "Needs Human" 并带有 COST:CRITICAL 标签
**解决方案：** 审查任务的评论线程以获取累计上下文。决定是增加预算、简化任务，还是将其拆分为更小的部分。

### 问题：合并后集成测试失败
**症状：** 任务从 main 自动回滚
**解决方案：** 自动回滚保护 main 稳定性。检查任务评论中的重试上下文，其中包含已尝试内容和失败内容。下一个分配的工作器将使用此上下文。

## 相关技能

- `@brainstorming` - 在 AgentFlow 之前使用以设计 SPEC.md
- `@writing-plans` - 补充规格编写用于任务分解
- `@test-driven-development` - 与 AgentFlow 的质量门控配合良好
- `@subagent-driven-development` - 多智能体协调的替代方法

## 其他资源

- [AgentFlow Repository](https://github.com/UrRhb/agentflow)
- [Architecture Documentation](https://github.com/UrRhb/agentflow/blob/main/docs/architecture.md)
- [Gap Registry (45 failure modes)](https://github.com/UrRhb/agentflow/blob/main/docs/gap-registry.md)
- [Getting Started Guide](https://github.com/UrRhb/agentflow/blob/main/docs/getting-started.md)

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
