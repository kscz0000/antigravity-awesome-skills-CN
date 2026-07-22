---
name: odw
description: 动态多智能体工作流 — 先规划，再通过本地 odw 守护进程编排带对抗验证的并行智能体。当用户要求"工作流"、提到"ultracode"、或提交一个涉及多个文件/项目且适合并行处理的任务时使用。触发词：工作流、workflow、ultracode、多智能体编排、并行处理、odw
risk: unknown
source: https://github.com/Suraj1235/open-dynamic-workflows/tree/main/packages/antigravity-adapter/skills/odw
source_repo: Suraj1235/open-dynamic-workflows
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/Suraj1235/open-dynamic-workflows/blob/main/LICENSE
---

# 开放式动态工作流 (Antigravity)

## 适用场景

当需要动态多智能体工作流时使用本技能 — 先制定计划，再通过本地 odw 守护进程编排带对抗性验证的并行智能体。适用场景包括：用户提出"工作流"需求、提及"ultracode"、或交给你一个跨多个文件/项且适合用并行智能体加速的任务。


与 Codex 适配器为同一标准技能，仅安装路径不同（`~/.gemini/skills/odw/`）。桥接脚本位于同目录的 `scripts/` 下。

## 模型与 API 密钥（请优先阅读）

Antigravity 将模型调用锁定在其内部引擎中 — 技能、工作流、MCP 服务器、`invoke_subagent` 以及 SDK 可以使用其 *工具*，但 **无法从扩展代码中调用其已配置的模型（Gemini/Claude/GPT-OSS）**。因此，与 OpenCode 插件（通过 OpenCode 的模型运行 ODW 真实引擎，无需额外密钥）不同，这里只有两条可行路径：

- **无密钥路径（原生回退）：** Antigravity 自身的智能体编排器使用 `invoke_subagent`（真正的隔离/工作树）和自有模型进行调度 — 无需额外密钥，但这 **不是** ODW 引擎。
- **完整引擎路径（守护进程）：** 真正的 ODW 引擎在本地守护进程中运行，使用 `~/.odw/config.json` 中配置的 **自有** 提供商密钥（Ollama 无需密钥/本地运行）。这是目前在 Antigravity 上获得完整引擎功能的唯一方式。

如果 Antigravity 未来提供文档化的模型调用 API（或 MCP sampling），即可升级为与 OpenCode 相同的无密钥嵌入式路径，无需修改引擎。

## 步骤 0 — 守护进程检查

执行：`node scripts/daemon-bridge.js --check`
- 退出码 0 → 守护进程正在运行；使用下方的守护进程路径。
- 退出码 1 → 守护进程未运行；通过 Antigravity 的 Agent Manager（会话作用域）进行原生编排，并提示用户可从 github.com/Suraj1235/open-dynamic-workflows 安装守护进程（克隆仓库，`npm install`，`npm run setup`，然后 `odw-daemon start`）。

## 守护进程路径

1. **规划：** `node scripts/daemon-bridge.js plan "<task>"` — 输出 JSON 计划，包含任务图、拓扑结构、角色分配、硬性约束及编译后的编排脚本。
2. **确认：** 在执行任何超出只读操作之前，先汇总拓扑 / 智能体数量 / 预估成本 / 预估耗时。
3. **执行：** `node scripts/daemon-bridge.js exec plan.json` → 返回 `wf_...` ID。守护进程接管执行：沙箱化脚本、16–100 个并发智能体、SQLite 检查点、崩溃恢复、预算硬停。即使当前 IDE 会话结束，守护进程仍持续运行。
4. **报告：** `node scripts/daemon-bridge.js result <wf_id>` 阻塞直至完成；转发综合后的结果。

## 原生回退路径

在当前会话内完成：分解任务 → 并行执行 → 对抗性验证 → 综合结果。先陈述计划；每个智能体输出结构化 JSON；任何变更操作前需获得批准。

## 注意事项

- VS Code 扩展（`odw-vscode`）可直接安装到 Antigravity 中（它本身就是 VS Code 分支），并提供实时工作流面板。
- 以编程方式驱动 Antigravity 会话暂无官方 API；超出技能 + MCP + 扩展范围的操作均为实验性功能，不属于本适配器的支持范畴。

## 局限性

- 仅在任务明确匹配上游来源和本地项目上下文时才使用本技能。
- 应用变更前，务必验证命令、生成代码、依赖项、凭据以及外部服务行为。
- 不要将示例替代为环境特定的测试、安全审查，或针对破坏性/高成本操作的用户审批。
